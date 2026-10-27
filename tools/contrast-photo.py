# -*- coding: utf-8 -*-
"""Яркость фона под текстом по снимкам из tools/contrast-photo.js."""
import json, pathlib, sys
from PIL import Image

OUT = pathlib.Path(sys.argv[1])
meta = json.loads((OUT / "meta.json").read_text())


def lum(rgb):
    def f(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


bad = 0
for m in meta:
    p = pathlib.Path(m["file"])
    if not p.exists():
        continue
    im = Image.open(p).convert("RGB")
    im.thumbnail((48, 48))
    px = list(im.getdata())
    # фон берётся как средняя яркость: букв на снимке уже нет
    L_bg = sum(lum(c) for c in px) / len(px)
    L_fg = lum(m["color"])
    ratio = (max(L_fg, L_bg) + .05) / (min(L_fg, L_bg) + .05)
    need = 3 if (m["px"] >= 24 or (m["px"] >= 18.66 and m["bold"])) else 4.5
    if ratio < need - 0.05:
        bad += 1
        print(f'{m["page"]}  <{m["tag"]}> {ratio:.2f}:1 нужно {need}  «{m["text"]}»')
print(f"текста поверх фотографий проверено {len(meta)}, нарушений {bad}")
sys.exit(1 if bad else 0)
