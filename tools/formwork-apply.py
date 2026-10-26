# -*- coding: utf-8 -*-
"""Подключить слой темы Formwork на всех страницах.

Глубина restyle: содержание и раскладка остаются, меняется система. Слой
подключается последним, после собственных таблиц стилей страницы, иначе
он не победит в каскаде: на странице их три-пять, и выигрывает последняя.

Прежние ссылки на шрифты снимаются: Schibsted Grotesk, Newsreader и IBM
Plex Mono темой не предусмотрены, а грузить их незачем.

Запуск: python3.13 tools/formwork-apply.py
"""
import pathlib, re

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
MARK = "<!-- formwork -->"

LINK = (MARK + '\n<link rel="preload" href="/css/formwork.css" as="style">\n'
        '<link rel="stylesheet" href="/css/formwork.css">')

# прежний набор гарнитур
OLD_FONTS = re.compile(
    r'<link rel="preload" href="/fonts/fonts\.css"[^>]*>\s*'
    r'<link rel="stylesheet" href="/fonts/fonts\.css">\s*', re.S)
PREV = re.compile(re.escape(MARK) + r".*?<link rel=\"stylesheet\" href=\"/css/formwork\.css\">\s*", re.S)


def main():
    n = 0
    for p in sorted(SITE.rglob("*.html")):
        s = s0 = p.read_text()
        s = PREV.sub("", s)
        s = OLD_FONTS.sub("", s)
        # последним перед </body> стоят наши же блоки правок; слой темы
        # должен идти после них
        if "</body>" in s:
            s = s.replace("</body>", LINK + "\n</body>", 1)
        else:
            s += LINK
        if s != s0:
            p.write_text(s)
            n += 1
    print(f"страниц подключено: {n}")


if __name__ == "__main__":
    main()
