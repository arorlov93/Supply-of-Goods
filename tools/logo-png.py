# -*- coding: utf-8 -*-
"""Экспорт логотипа в PNG через chromium. Фон прозрачный.

Запуск: python3.13 tools/logo-png.py
"""
import os, re, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = os.path.abspath(os.path.join(HERE, "..", "brand"))
CHROME = "/opt/pw-browsers/chromium"

JOBS = [
    ("logo-light.svg",         "logo-light.png",        1400),
    ("logo-dark.svg",          "logo-dark.png",         1400),
    ("logo-light-plain.svg",   "logo-light-plain.png",  1200),
    ("logo-dark-plain.svg",    "logo-dark-plain.png",   1200),
    ("logo-stacked-light.svg", "logo-stacked-light.png", 900),
    ("logo-stacked-dark.svg",  "logo-stacked-dark.png",  900),
    ("logo-light.svg",         "logo-email.png",         720),
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
        html = ('<!doctype html><meta charset="utf-8">'
                '<style>html,body{margin:0;background:transparent}'
                'img{display:block;width:%dpx;height:%dpx}</style>'
                '<img src="file://%s">' % (width, h, sp))
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False,
                                         encoding="utf8") as f:
            f.write(html)
            tmp = f.name
        out = os.path.join(BRAND, dst)
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                        "--hide-scrollbars", "--default-background-color=00000000",
                        "--window-size=%d,%d" % (width, h),
                        "--screenshot=" + out, "file://" + tmp],
                       capture_output=True)
        os.unlink(tmp)
        print("  -> brand/%s  %dx%d" % (dst, width, h))


if __name__ == "__main__":
    main()
