# -*- coding: utf-8 -*-
"""Экспорт логотипа в PNG. Фон прозрачный.

Растеризация идёт через cairosvg, а не скриншотом браузера: скриншот обрезал
низ картинки, из-за чего пропадал дескриптор и срезался шар.

Запуск: python3.13 tools/logo-png.py
"""
import os
import re
import cairosvg

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = os.path.abspath(os.path.join(HERE, "..", "brand"))

JOBS = [
    ("logo-light.svg",         "logo-light.png",        1600),
    ("logo-dark.svg",          "logo-dark.png",         1600),
    ("logo-light-plain.svg",   "logo-light-plain.png",  1400),
    ("logo-dark-plain.svg",    "logo-dark-plain.png",   1400),
    ("logo-stacked-light.svg", "logo-stacked-light.png", 900),
    ("logo-stacked-dark.svg",  "logo-stacked-dark.png",  900),
    # подпись в письме: без дескриптора, он на такой высоте нечитаем
    ("logo-light-plain.svg",   "logo-email.png",         760),
    ("mark-ink.svg",           "mark-ink.png",           420),
    ("mark-cream.svg",         "mark-cream.png",         420),
    ("icon.svg",               "favicon-512.png",        512),
    ("icon.svg",               "favicon-180.png",        180),
    ("icon.svg",               "favicon-32.png",          32),
]


def viewbox(path):
    s = open(path, encoding="utf8").read()
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s)
    return float(m.group(1)), float(m.group(2))


def main():
    for src, dst, width in JOBS:
        sp = os.path.join(BRAND, src)
        vw, vh = viewbox(sp)
        h = round(width * vh / vw)
        out = os.path.join(BRAND, dst)
        cairosvg.svg2png(url=sp, write_to=out,
                         output_width=width, output_height=h)
        print("  -> brand/%s  %dx%d" % (dst, width, h))


if __name__ == "__main__":
    main()
