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
# /user/tokens/verify отвечает только токену с правами на уровне пользователя.
# Токен, выданный на аккаунт, этот запрос отбивает, хотя Pages и зону открывает
# прекрасно. Поэтому отказ здесь не повод останавливаться: настоящая проверка
# ниже, по доступу к списку проектов Pages, и она же нужна для работы.
if cf "$API/user/tokens/verify" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('   ', d['result']['status'] if d.get('success') else 'на уровне пользователя не проверяется')
sys.exit(0 if d.get('success') else 1)"; then :; else
  echo "    токен аккаунтный, проверяю по доступу к Pages"
fi

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

say "3a. Проверяю, что все снимки и стили на страницах существуют"
# Имена файлов снимков и таблицы стилей версионные, хэш в имя ставят
# tools/media-version.py и tools/css-version.py уже после того, как страница
# собрана. Забыть этот шаг легко, а наружу это выходит либо страницей вообще
# без картинок, либо страницей без стилей: браузер получает 404. Со снимками
# на странице референсов так уже случилось. Дешевле проверить здесь за
# полсекунды, чем увидеть на живом сайте.
python3 - "$DIR" <<'PYCHECK'
import pathlib, re, sys
site = pathlib.Path(sys.argv[1])
bad = {}
for page in sorted(site.rglob("*.html")):
    t = page.read_text()
    refs = set(re.findall(r'(?:src|href)="(media/[^"]+)"', t))
    refs |= set(re.findall(r'(media/[A-Za-z0-9_.\-]+\.(?:webp|jpg|png|svg))', t))
    # стили и скрипты подключаются от корня, поэтому ведущая косая снимается
    refs |= {r.lstrip("/") for r in re.findall(r'(?:href|src)="(/(?:css|js|fonts)/[^"]+)"', t)}
    for ref in refs:
        if not (site / ref).is_file():
            bad.setdefault(page.name, set()).add(ref)
if bad:
    for name in sorted(bad):
        print("    НЕТ ФАЙЛА на %s:" % name)
        for r in sorted(bad[name]):
            print("       ", r)
    print("    выкладка остановлена: запустите tools/media-version.py"
          " и tools/css-version.py")
    sys.exit(1)
print("    все ссылки на снимки и стили живы")
PYCHECK

say "4. Загружаю $(ls "$DIR"/*.html | wc -l) страниц и $(find "$DIR/functions" -name '*.js' 2>/dev/null | wc -l) функций"
# Запускать обязательно из самого каталога сайта. Wrangler ищет папку
# functions рядом с собой, а не внутри того каталога, что ему передали.
# Выкладка из корня репозитория молча уносит все функции: форма заявки
# начинает отвечать 405, CRM 404, редирект www перестаёт работать. Это
# уже случалось, поэтому здесь cd, а ниже проверка.
( cd "$DIR" && npx --yes wrangler@3 pages deploy . \
    --project-name="$PROJECT" --branch=main --commit-dirty=true )

say "4a. Проверяю, что функции живы"
for i in 1 2 3 4 5 6; do
  code=$(curl -sS -o /dev/null -w "%{http_code}" --max-time 20 "https://$DOMAIN/api/leads" || echo 000)
  case "$code" in
    403|503) echo "    /api/leads отвечает $code, функции работают"; break ;;
    *) if [ "$i" = 6 ]; then
         echo "    /api/leads отвечает $code. Функции НЕ выложены, форма заявки в базу писать не будет."
         exit 1
       fi
       sleep 5 ;;
  esac
done

say "4b. Подаю адреса в поисковые индексы"
# IndexNow: Bing, Yandex, Seznam, Naver принимают подачу одним запросом.
# Без этого новые и изменённые страницы ждут, пока поисковик придёт сам,
# а это недели. За поиском ChatGPT и DuckDuckGo стоит индекс Bing, то
# есть это ещё и условие, при котором нас вообще способна процитировать
# языковая модель. Google так не умеет, ему нужна Search Console.
python3 "$(dirname "$0")/indexnow.py" || echo "    подача не прошла, выкладке это не мешает"

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
