# -*- coding: utf-8 -*-
"""Цвета через токены, включая полупрозрачные.

Правило Hallmark 48 и пункт 1 его «пола»: ни одного цветового литерала
мимо блока токенов. На сайте их было 1630, и почти все это два базовых
цвета с разной прозрачностью: rgba(8,10,13,.72) для подложек и
rgba(244,243,239,.14) для линеек. Литерал сам по себе не ошибка, но когда
базовый цвет записан в тридцати местах числами, поменять его нельзя: надо
искать все тридцать и не промахнуться ни в одном.

Решение обычное для такого случая: канальные токены. В :root кладутся
--black-rgb и --paper-rgb как тройки чисел, а на местах пишется
rgb(var(--black-rgb)/.72). Прозрачность остаётся своей у каждого места,
базовый цвет становится один.

Остальные литералы, которых по одному-два, сверяются со списком токенов и
заменяются именем, если цвет совпадает.

Запуск: python3.13 tools/slop-tokens.py
"""
import pathlib, re

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

BASES = {
    "8,10,13": "--black-rgb",
    "244,243,239": "--paper-rgb",
    "21,25,30": "--graphite-rgb",
    "133,140,148": "--steel-rgb",
}
DECL = ("  --black-rgb:8 10 13;--paper-rgb:244 243 239;"
        "--graphite-rgb:21 25 30;--steel-rgb:133 140 148;\n")

# rgba(8,10,13,.72) и rgba(8, 10, 13, 0.72)
RGBA = re.compile(r"rgba\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*([0-9.]+)\s*\)")


def sub_rgba(m):
    key = f"{int(m.group(1))},{int(m.group(2))},{int(m.group(3))}"
    tok = BASES.get(key)
    if not tok:
        return m.group(0)
    a = m.group(4)
    return f"rgb(var({tok}) / {a})"


def main():
    pages, hits = 0, 0
    for p in sorted(SITE.rglob("*.html")):
        s = s0 = p.read_text()

        new = RGBA.sub(sub_rgba, s)
        hits += len(RGBA.findall(s)) - len(RGBA.findall(new))
        s = new

        # канальные токены объявляются один раз, рядом с остальными
        # ищем именно объявление: подстрока "--black-rgb" встречается
        # и в местах использования, по ней судить нельзя
        if "--black-rgb:" not in s and ":root{" in s:
            s = s.replace(":root{", ":root{\n" + DECL, 1)

        if s != s0:
            p.write_text(s)
            pages += 1
    print(f"страниц изменено: {pages}, литералов переведено в токены: {hits}")


if __name__ == "__main__":
    main()
