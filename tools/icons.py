# -*- coding: utf-8 -*-
"""Иконки сайта: настоящая марка вместо нарисованной в адресной строке.

До этого на всех страницах стояла единственная ссылка rel=icon с картинкой
прямо в адресе: тёмный квадрат с буквами IG, набранными Georgia. К логотипу
компании это отношения не имело. Заодно браузеры и телефоны просили с корня
apple-touch-icon.png и site.webmanifest, которых не было, и получали 404.

Здесь ссылка заменяется на готовые файлы из brand, в корень кладутся копии
под теми именами, по которым их спрашивают без спроса, и пишется манифест.

Запуск: python3.13 tools/icons.py
"""
import pathlib, re, shutil

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
BRAND = SITE / "brand"

MANIFEST = """{
 "name": "ISP GROUP LLC",
 "short_name": "ISP GROUP",
 "description": "International sourcing and supply",
 "start_url": "/",
 "display": "standalone",
 "background_color": "#0f1216",
 "theme_color": "#0f1216",
 "icons": [
  {"src": "/brand/favicon-32.png", "sizes": "32x32", "type": "image/png"},
  {"src": "/brand/favicon-180.png", "sizes": "180x180", "type": "image/png"},
  {"src": "/brand/favicon-512.png", "sizes": "512x512", "type": "image/png"},
  {"src": "/brand/icon.svg", "sizes": "any", "type": "image/svg+xml"}
 ]
}
"""

LINKS = (
    '<link rel="icon" href="/brand/icon.svg" type="image/svg+xml">\n'
    '<link rel="icon" href="/brand/favicon-32.png" sizes="32x32" type="image/png">\n'
    '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
    '<link rel="manifest" href="/site.webmanifest">\n'
    '<meta name="theme-color" content="#0f1216">'
)

# старая ссылка: картинка целиком в адресе, с кавычками внутри
OLD = re.compile(r'<link rel="icon" href="data:image/svg\+xml,.*?">\s*', re.S)
# следы прошлых прогонов, чтобы скрипт можно было запускать повторно
PREV = re.compile(
    r'<link rel="icon" href="/brand/icon\.svg".*?'
    r'<meta name="theme-color" content="#0f1216">\s*', re.S)


def main():
    shutil.copyfile(BRAND / "favicon-180.png", SITE / "apple-touch-icon.png")
    shutil.copyfile(BRAND / "favicon-32.png", SITE / "favicon.ico")
    (SITE / "site.webmanifest").write_text(MANIFEST)

    done = 0
    for p in sorted(SITE.rglob("*.html")):
        s = s0 = p.read_text()
        s = PREV.sub("", s)
        if OLD.search(s):
            s = OLD.sub(LINKS + "\n", s, count=1)
        elif "/brand/icon.svg" not in s:
            s = s.replace("</head>", LINKS + "\n</head>", 1)
        s = OLD.sub("", s)          # если старых ссылок было несколько
        if s != s0:
            p.write_text(s)
            done += 1
    print(f"страниц исправлено: {done}")
    print("в корень положены: apple-touch-icon.png, favicon.ico, site.webmanifest")


if __name__ == "__main__":
    main()
