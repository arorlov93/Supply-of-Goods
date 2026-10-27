# -*- coding: utf-8 -*-
"""Переносит файл темы из конца документа в голову.

Что было. Строка <link rel="stylesheet" href="/css/formwork.css"> стояла
последней в документе, после </body>. Браузер в таком случае сначала
показывает страницу тем оформлением, которое уже знает, то есть
страничным <style> в голове, и только потом, получив тему, перекрашивает
и переверстывает всё заново.

Чем это стоило. Замер на живом сайте: в 75 мс логотип набран запасной
гарнитурой из страничного CSS, в 811 мс приезжает тема и гарнитура
меняется. Текст меняет ширину и высоту, за ним едет шапка, за шапкой
первый экран. Сдвиг макета 0.14 при пороге Core Web Vitals 0.1. Человек
при этом видит, как страница перестраивается у него под курсором.

Почему перенос правильный, а не вредный. Тему иногда уводят в конец,
чтобы она не задерживала первую отрисовку. Здесь это не работает: тема
не дополняет оформление, а заменяет его целиком, и показывать страницу
до неё значит показывать не ту страницу. Правильное место файла,
который решает, как всё выглядит, это голова документа.

Порядок внутри головы важен: тема должна стоять после страничного
<style>, иначе перестанет его перекрывать. Поэтому вставляем перед
закрытием головы.

Запуск: python3.13 tools/css-in-head.py
Повторный запуск ничего не меняет.
"""
import pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
SHEET = '<link rel="stylesheet" href="/css/formwork.css">'
MARK = "<!-- шрифты первого экрана -->"
PRELOADS = [
    "/fonts/oswald-700-latin.woff2",
    "/fonts/archivo-400-latin.woff2",
    "/fonts/archivo-500-latin.woff2",
]
BLOCK = (
    MARK + "\n"
    + "\n".join(
        f'<link rel="preload" href="{p}" as="font" type="font/woff2" crossorigin>' for p in PRELOADS
    )
    + "\n" + SHEET + "\n"
)


def main():
    moved = already = 0
    for p in sorted(SITE.rglob("*.html")):
        if p.name == "crm.html":
            continue
        s = p.read_text()
        head_end = s.find("</head>")
        if head_end < 0:
            print(f"  ОШИБКА: нет </head> в {p.relative_to(SITE)}")
            return 1

        if s.find(SHEET) >= 0 and s.find(SHEET) < head_end:
            already += 1
            continue

        # убираем всё, что было вынесено в хвост документа
        s = s.replace(BLOCK, "")
        s = s.replace(SHEET + "\n", "").replace(SHEET, "")
        s = re.sub(
            re.escape(MARK) + r"\n(?:<link rel=\"preload\" href=\"/fonts/[^\"]+\"[^>]*>\n)+",
            "",
            s,
        )

        head_end = s.find("</head>")
        s = s[:head_end] + BLOCK + s[head_end:]
        p.write_text(s)
        moved += 1

    print(f"тема перенесена в голову: {moved} страниц, уже было: {already}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
