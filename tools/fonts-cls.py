# -*- coding: utf-8 -*-
"""Убирает сдвиг макета от подмены шрифта.

Замер до правки: сдвиг макета 0.132 на 41 странице из 46, на главной
0.183. Порог Core Web Vitals это 0.1, то есть страницы его не проходили.
Разбор показал, что крупнейший сдвиг даёт надпись в логотипе: её ширина
прыгает с 240 до 325 точек на пятисотой миллисекунде, и следом едет вся
шапка и первый экран.

Причин две, обе правятся здесь.

Первая. Шрифты объявлены в отдельном файле, который подключён строкой
@import внутри главного файла стилей. Браузер узнаёт про шрифты только
после того, как загрузит и разберёт главный файл, то есть на один обход
сети позже, чем мог бы. Объявления переносятся прямо в главный файл.

Вторая. У шрифтов стоит font-display: swap. Это прямое указание
браузеру: покажи запасным шрифтом, а когда приедет свой, перерисуй. Та
самая перерисовка и есть сдвиг. Ставим optional: браузер ждёт шрифт сто
миллисекунд, и если тот не успел, эта загрузка страницы просто идёт
запасным шрифтом, без скачка. Вместе с предзагрузкой ниже свой шрифт
успевает почти всегда, а в редких случаях посетитель видит ровный текст
вместо дёргающегося.

Третья мера, предзагрузка. Три начертания, которыми набран первый экран,
объявляются в начале каждой страницы, чтобы запрос ушёл сразу, а не
после разбора стилей. Остальные начертания ждут своей очереди: тянуть
всё подряд значит отнимать полосу у главной картинки экрана.

Запуск: python3.13 tools/fonts-cls.py
Повторный запуск ничего не дублирует.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
MAIN = SITE / "css" / "formwork.css"
FONTS = SITE / "fonts" / "formwork.css"

PRELOAD = [
    "/fonts/oswald-700-latin.woff2",
    "/fonts/archivo-400-latin.woff2",
    "/fonts/archivo-500-latin.woff2",
]

MARK = "<!-- шрифты первого экрана -->"
LINKS = MARK + "\n" + "\n".join(
    f'<link rel="preload" href="{p}" as="font" type="font/woff2" crossorigin>' for p in PRELOAD
) + "\n"


def fix_css():
    if "@font-face" in MAIN.read_text():
        print("  стили: объявления шрифтов уже на месте")
        return 0
    faces = FONTS.read_text()
    faces = faces.replace("font-display: swap;", "font-display: optional;")
    s = MAIN.read_text()
    if '@import url("/fonts/formwork.css");' not in s:
        print("  ОШИБКА: не нашёл строку @import со шрифтами")
        return 1
    # @import обязан стоять раньше любых правил, поэтому его строку просто
    # убираем, а объявления дописываем следом за остальными @import
    s = s.replace('@import url("/fonts/formwork.css");\n', "")
    m = list(re.finditer(r"^@import[^\n]*\n", s, re.M))
    at = m[-1].end() if m else 0
    s = s[:at] + "\n/* Гарнитуры: раньше подключались строкой @import из\n" \
                 "   /fonts/formwork.css, то есть браузер узнавал о них на один\n" \
                 "   обход сети позже. Перенесены сюда. font-display: optional\n" \
                 "   вместо swap, иначе подмена шрифта двигает макет. */\n" + faces + s[at:]
    MAIN.write_text(s)
    print(f"  стили: объявления перенесены, swap заменён на optional")
    return 0


def fix_pages():
    done = skipped = 0
    for p in sorted(SITE.rglob("*.html")):
        if p.name == "crm.html":
            skipped += 1
            continue
        s = p.read_text()
        if MARK in s:
            skipped += 1
            continue
        # перед первым подключением стилей: шрифт нужен раньше, чем стиль,
        # который его назначит
        m = re.search(r'<link rel="stylesheet"', s)
        if not m:
            print(f"  ОШИБКА: нет стилей в {p.relative_to(SITE)}")
            return 1
        p.write_text(s[: m.start()] + LINKS + s[m.start():])
        done += 1
    print(f"  страниц с предзагрузкой: {done}, пропущено: {skipped}")
    return 0


def main():
    return fix_css() or fix_pages()


if __name__ == "__main__":
    sys.exit(main())
