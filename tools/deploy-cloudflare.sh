#!/usr/bin/env bash
# Выкладка site/ на Cloudflare Pages и привязка ispgroupgc.com.
# Идемпотентно: повторный запуск просто обновляет содержимое.
#
# Нужны две переменные окружения:
#   CLOUDFLARE_API_TOKEN   токен с правами Account > Cloudflare Pages > Edit
#                          и Zone > DNS > Edit, Zone > Zone > Read для ispgroupgc.com
#   CLOUDFLARE_ACCOUNT_ID  необязательно, иначе определяется автоматически
set -euo pipefail

PROJECT="${PROJECT:-ispgroupgc}"
DOMAIN="${DOMAIN:-ispgroupgc.com}"
DIR="$(cd "$(dirname "$0")/.." && pwd)/site"
API="https://api.cloudflare.com/client/v4"

say() { printf '\n\033[1m%s\033[0m\n' "$*"; }
cf()  { curl -sS --max-time 60 -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
             -H "Content-Type: application/json" "$@"; }
ok()  { python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(0 if d.get('success') else 1)"; }

[ -n "${CLOUDFLARE_API_TOKEN:-}" ] || { echo "нет CLOUDFLARE_API_TOKEN"; exit 1; }
[ -d "$DIR" ] || { echo "нет каталога $DIR"; exit 1; }

say "1. Проверяю токен"
cf "$API/user/tokens/verify" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('   ', d['result']['status'] if d.get('success') else d.get('errors'))
sys.exit(0 if d.get('success') else 1)"

if [ -z "${CLOUDFLARE_ACCOUNT_ID:-}" ]; then
  say "2. Определяю аккаунт"
  CLOUDFLARE_ACCOUNT_ID=$(cf "$API/accounts" | python3 -c "
import json,sys; r=json.load(sys.stdin)['result']
print(r[0]['id']); print('   ', r[0]['name'], file=sys.stderr)")
  export CLOUDFLARE_ACCOUNT_ID
fi
echo "    account: $CLOUDFLARE_ACCOUNT_ID"

say "3. Проект Pages «$PROJECT»"
if cf "$API/accounts/$CLOUDFLARE_ACCOUNT_ID/pages/projects/$PROJECT" | ok; then
  echo "    уже существует"
else
  cf -X POST "$API/accounts/$CLOUDFLARE_ACCOUNT_ID/pages/projects" \
     -d "{\"name\":\"$PROJECT\",\"production_branch\":\"main\"}" \
   | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('    создан' if d.get('success') else '    ОШИБКА: %s' % d.get('errors'))
sys.exit(0 if d.get('success') else 1)"
fi

say "4. Загружаю $(ls "$DIR"/*.html | wc -l) страниц"
npx --yes wrangler@3 pages deploy "$DIR" \
    --project-name="$PROJECT" --branch=main --commit-dirty=true

say "5. Привязываю домены"
for d in "$DOMAIN" "www.$DOMAIN"; do
  if cf -X POST "$API/accounts/$CLOUDFLARE_ACCOUNT_ID/pages/projects/$PROJECT/domains" \
        -d "{\"name\":\"$d\"}" | ok; then
    echo "    $d привязан"
  else
    echo "    $d уже привязан или требует записи DNS вручную"
  fi
done

say "6. Проверяю DNS"
ZONE=$(cf "$API/zones?name=$DOMAIN" | python3 -c "
import json,sys; r=json.load(sys.stdin).get('result') or []
print(r[0]['id'] if r else '')")
if [ -n "$ZONE" ]; then
  for name in "$DOMAIN" "www.$DOMAIN"; do
    have=$(cf "$API/zones/$ZONE/dns_records?name=$name" | python3 -c "
import json,sys; r=json.load(sys.stdin).get('result') or []
print(len(r))")
    if [ "$have" = "0" ]; then
      cf -X POST "$API/zones/$ZONE/dns_records" \
        -d "{\"type\":\"CNAME\",\"name\":\"$name\",\"content\":\"$PROJECT.pages.dev\",\"proxied\":true}" \
        | ok && echo "    $name -> $PROJECT.pages.dev создан" || echo "    $name: не удалось создать"
    else
      echo "    $name: запись уже есть"
    fi
  done
else
  echo "    зона $DOMAIN не видна этому токену, добавь CNAME вручную"
fi

say "Готово"
echo "  https://$DOMAIN  и  https://$PROJECT.pages.dev"
echo "  Сертификат выпускается несколько минут после первой привязки."
