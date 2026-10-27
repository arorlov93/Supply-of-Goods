#!/usr/bin/env bash
# Выкладка Worker дожима писем (mailer/worker.js) и расписания к нему.
#
# Это отдельный Worker, а не часть сайта: Pages Functions не умеют
# запускаться по расписанию, а дожим нужен именно по расписанию.
#
# Нужны переменные окружения:
#   CLOUDFLARE_API_TOKEN    права Account > Workers Scripts > Edit
#   CLOUDFLARE_ACCOUNT_ID
#   D1_ID                   идентификатор базы заявок (та же, что у Pages)
#   DRAIN_KEY               необязательно, ключ ручного запуска для проверки
#
# Идемпотентно: повторный запуск обновляет скрипт и расписание.
set -euo pipefail

NAME="${NAME:-ispgroupgc-mailer}"
SRC="$(cd "$(dirname "$0")/.." && pwd)/mailer/worker.js"
API="https://api.cloudflare.com/client/v4"
CRON="${CRON:-* * * * *}"

say() { printf '\n\033[1m%s\033[0m\n' "$*"; }
chk() { python3 -c "
import json,sys
d=json.load(sys.stdin)
if d.get('success'): print('    готово')
else: print('    ОШИБКА:', d.get('errors')); sys.exit(1)
"; }

[ -n "${CLOUDFLARE_API_TOKEN:-}" ] || { echo "нет CLOUDFLARE_API_TOKEN"; exit 1; }
[ -n "${CLOUDFLARE_ACCOUNT_ID:-}" ] || { echo "нет CLOUDFLARE_ACCOUNT_ID"; exit 1; }
[ -n "${D1_ID:-}" ] || { echo "нет D1_ID"; exit 1; }
[ -f "$SRC" ] || { echo "нет файла $SRC"; exit 1; }

# Привязки собираются питоном, чтобы ключ не попал в строку команды и не
# засветился в списке процессов.
META=$(D1_ID="$D1_ID" DRAIN_KEY="${DRAIN_KEY:-}" python3 -c "
import json, os
b = [{'type': 'd1', 'name': 'DB', 'id': os.environ['D1_ID']}]
if os.environ.get('DRAIN_KEY'):
    b.append({'type': 'secret_text', 'name': 'DRAIN_KEY', 'text': os.environ['DRAIN_KEY']})
print(json.dumps({
    'main_module': 'worker.js',
    'compatibility_date': '2026-10-01',
    'bindings': b,
}))
")

say "1. Загружаю Worker «$NAME»"
curl -sS --max-time 60 -X PUT \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -F "metadata=$META;type=application/json" \
  -F "worker.js=@$SRC;type=application/javascript+module" \
  "$API/accounts/$CLOUDFLARE_ACCOUNT_ID/workers/scripts/$NAME" | chk

say "2. Ставлю расписание «$CRON»"
curl -sS --max-time 60 -X PUT \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d "[{\"cron\":\"$CRON\"}]" \
  "$API/accounts/$CLOUDFLARE_ACCOUNT_ID/workers/scripts/$NAME/schedules" | chk

say "Готово. Дожим идёт по расписанию «$CRON»."
