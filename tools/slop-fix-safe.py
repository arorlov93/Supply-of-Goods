# -*- coding: utf-8 -*-
"""Правки по разбору Hallmark, не меняющие вид страницы.

Hallmark (github.com/Nutlope/hallmark) это набор правил против того, что в
нём названо «сгенерированным видом». Его линтер нашёл на сайте 3378
нарушений. Здесь закрыты только те, которые ничего не меняют на экране:
их можно применить разом и проверить счётчиком, а не глазами.

Что чинится и почему:

34   overflow-x:hidden на body ломает position:sticky в Safari и Chrome.
     clip делает то же самое, но липкие элементы продолжают работать.
10a  анимация width и right заставляет браузер пересчитывать разметку на
     каждом кадре. Тот же эффект даёт transform, который считает композитор.
7a   чистый #fff рядом с тёплой бумагой выглядит дырой. Белый берётся из
     токена, подкрашенного в сторону основного тона.
50   дорожка сетки шириной 1fr с картинкой внутри не даёт картинке сжаться
     ниже её натуральной ширины, и сетка распирает страницу вбок.
55a  прописные с интерлиньяжем 0.9 сталкиваются надстрочными элементами,
     когда заголовок переносится.

Запуск: python3.13 tools/slop-fix-safe.py
"""
import pathlib, re

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"


def fix_overflow(s):
    # 34: clip вместо hidden, иначе ломается sticky
    return re.sub(r"overflow-x:\s*hidden", "overflow-x:clip", s), "34"


def fix_width_anim(s):
    # 10a: чёрточка у крупной кнопки росла по width, теперь тянется по X
    a = (".btn-lg::after{content:\"\";width:22px;height:1px;background:currentColor;"
         "transition:width .3s}")
    b = (".btn-lg::after{content:\"\";width:34px;height:1px;background:currentColor;"
         "transform:scaleX(.647);transform-origin:left;transition:transform .3s}")
    s = s.replace(a, b)
    s = s.replace(".btn-lg:hover::after{width:34px}",
                  ".btn-lg:hover::after{transform:scaleX(1)}")
    # 10a: подчёркивание в меню ездило по right
    s = s.replace(".navlinks a:hover::after{right:0}",
                  ".navlinks a:hover::after{transform:scaleX(1)}")
    return s, "10a"


def fix_pure_white(s):
    # 7a: белый подкрашивается в сторону бумаги, чистый #fff выбивается
    s = re.sub(r"color:#fff\b", "color:var(--paper)", s)
    s = re.sub(r"color:#ffffff\b", "color:var(--paper)", s)
    return s, "7a"


def fix_image_tracks(s):
    # 50: дорожка с картинкой не должна быть голой 1fr
    for a, b in [("minmax(0,.82fr) minmax(0,1.18fr)", None)]:
        pass
    s = re.sub(r"grid-template-columns:\s*1fr\s+1fr\b",
               "grid-template-columns:minmax(0,1fr) minmax(0,1fr)", s)
    s = re.sub(r"grid-template-columns:\s*repeat\((\d+),\s*1fr\)",
               r"grid-template-columns:repeat(\1,minmax(0,1fr))", s)
    s = re.sub(r"grid-template-columns:\s*1\.1fr\s+\.9fr\b",
               "grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr)", s)
    s = re.sub(r"grid-template-columns:\s*\.9fr\s+1\.1fr\b",
               "grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr)", s)
    return s, "50"


def fix_caps_leading(s):
    # 55a: прописные с интерлиньяжем .9 сталкиваются при переносе
    return s.replace("letter-spacing:-.035em;line-height:.9;",
                     "letter-spacing:-.035em;line-height:1;"), "55a"


FIXES = [fix_overflow, fix_width_anim, fix_pure_white, fix_image_tracks, fix_caps_leading]


def main():
    touched = {}
    pages = 0
    for p in sorted(SITE.rglob("*.html")):
        s = s0 = p.read_text()
        for f in FIXES:
            before = s
            s, tag = f(s)
            if s != before:
                touched[tag] = touched.get(tag, 0) + 1
        if s != s0:
            p.write_text(s)
            pages += 1
    print(f"страниц изменено: {pages}")
    for k in sorted(touched):
        print(f"  правило {k}: затронуто страниц {touched[k]}")


if __name__ == "__main__":
    main()
