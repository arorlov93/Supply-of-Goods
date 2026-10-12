# -*- coding: utf-8 -*-
"""Логотип ISP GROUP LLC. Текст превращается в кривые, шрифт не нужен нигде.

Типографика сайта: Schibsted Grotesk. Цвета сайта: чернила #0e2a26,
золото #b8862b, кремовый #e8d9b4, глубокая зелень #071c19.

Запуск:  python3.13 tools/logo.py
Выход:   brand/*.svg
"""
import os
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.environ.get("SG_TTF", "/tmp/claude-0/-home-user-Supply-of-Goods/"
       "4f5e4e6d-222f-57da-93ad-94f5b2132f9f/scratchpad/logo/sg.ttf")
OUT = os.path.join(HERE, "..", "brand")

INK = "#0e2a26"
GOLD = "#b8862b"
CREAM = "#e8d9b4"
DEEP = "#071c19"

_cache = {}


def font(weight):
    if weight not in _cache:
        f = TTFont(FONT)
        _cache[weight] = instantiateVariableFont(f, {"wght": weight}, inplace=True)
    return _cache[weight]


def text_paths(s, weight, size, tracking=0.0):
    """Вернуть (d-строка пути, ширина) для строки, базовая линия в y=0,
    координаты уже в пикселях, ось y вниз."""
    f = font(weight)
    upm = f["head"].unitsPerEm
    scale = size / upm
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    hmtx = f["hmtx"]
    kern = None
    try:
        kern = f["kern"].kernTables[0].kernTable
    except Exception:
        pass
    d = []
    x = 0.0
    prev = None
    for ch in s:
        gname = cmap.get(ord(ch))
        if gname is None:
            x += size * 0.3
            prev = None
            continue
        if prev and kern:
            x += kern.get((prev, gname), 0) * scale
        pen = SVGPathPen(gs, ntos=lambda v: "%.2f" % v)
        gs[gname].draw(pen)
        cmds = pen.getCommands()
        if cmds:
            d.append('<path transform="translate(%.2f 0) scale(%.5f %.5f)" d="%s"/>'
                     % (x, scale, -scale, cmds))
        x += hmtx[gname][0] * scale + tracking
        prev = gname
    if s:
        x -= tracking
    return "".join(d), x


REACH = 0.62   # насколько линия выходит за шар, в долях радиуса


def mark(cx, cy, r, stroke, ring, dot):
    """Знак: шар это мир, линия выходит за него вправо и упирается в точку.
    Читается как путь товара из мира в конкретный адрес."""
    end = cx + r * (1 + REACH)
    return (
        '<g fill="none" stroke="%s" stroke-width="%.2f" stroke-linecap="round">'
        '<circle cx="%.2f" cy="%.2f" r="%.2f"/>'
        '<ellipse cx="%.2f" cy="%.2f" rx="%.2f" ry="%.2f"/>'
        '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/>'
        '</g>'
        '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s"/>'
        % (ring, stroke,
           cx, cy, r,
           cx, cy, r * 0.46, r,
           cx - r, cy, end - stroke * 1.2, cy,
           end, cy, stroke * 1.75, dot)
    )


def svg(w, h, body, bg=None):
    b = '<rect width="%.0f" height="%.0f" fill="%s"/>' % (w, h, bg) if bg else ""
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.0f %.0f" '
            'width="%.0f" height="%.0f" role="img" aria-label="ISP GROUP">'
            '%s%s</svg>' % (w, h, w, h, b, body))


def write(name, s):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    open(p, "w", encoding="utf8").write(s)
    print("  ->", os.path.relpath(os.path.abspath(p),
                                  os.path.abspath(os.path.join(HERE, ".."))))


def lockup(word_color, sub_color, ring, dot, bg=None, sub=True):
    size = 54.0
    d1, w1 = text_paths("ISP", 700, size, tracking=-0.6)
    d2, w2 = text_paths("GROUP", 400, size, tracking=1.2)
    gap = size * 0.30
    r = size * 0.50
    pad = 28.0
    mx = pad + r
    tx = mx + r * (1 + REACH) + size * 0.42
    base = pad + size * 0.74
    body = [mark(mx, base - size * 0.26, r, size * 0.072, ring, dot)]
    body.append('<g fill="%s" transform="translate(%.2f %.2f)">%s</g>'
                % (word_color, tx, base, d1))
    body.append('<g fill="%s" transform="translate(%.2f %.2f)">%s</g>'
                % (sub_color, tx + w1 + gap, base, d2))
    w = tx + w1 + gap + w2 + pad
    h = pad * 2 + size * 0.74
    if sub:
        ds, ws = text_paths("GLOBAL COMMERCE", 500, size * 0.228, tracking=size * 0.105)
        body.append('<g fill="%s" opacity=".78" transform="translate(%.2f %.2f)">%s</g>'
                    % (sub_color, tx, base + size * 0.40, ds))
        h += size * 0.40
        w = max(w, tx + ws + pad)
    return svg(w, h, "".join(body), bg)


def stacked(word_color, sub_color, ring, dot, bg=None):
    size = 58.0
    d1, w1 = text_paths("ISP", 700, size, tracking=-0.6)
    d2, w2 = text_paths("GROUP", 400, size, tracking=1.2)
    gap = size * 0.30
    total = w1 + gap + w2
    ds, ws = text_paths("GLOBAL COMMERCE", 500, size * 0.205, tracking=size * 0.115)
    r = size * 0.62
    pad = 30.0
    w = max(total, ws, r * 2 * (1 + REACH)) + pad * 2
    cx = w / 2 - r * REACH / 2
    top = pad + r
    base = top + r + size * 1.00
    body = [mark(cx, top, r, size * 0.068, ring, dot)]
    body.append('<g fill="%s" transform="translate(%.2f %.2f)">%s</g>'
                % (word_color, cx - total / 2, base, d1))
    body.append('<g fill="%s" transform="translate(%.2f %.2f)">%s</g>'
                % (sub_color, cx - total / 2 + w1 + gap, base, d2))
    body.append('<g fill="%s" opacity=".78" transform="translate(%.2f %.2f)">%s</g>'
                % (sub_color, cx - ws / 2, base + size * 0.44, ds))
    h = base + size * 0.44 + pad * 0.6
    return svg(w, h, "".join(body), bg)


def icon(bg, ring, dot, size=512.0):
    r = size * 0.235
    return svg(size, size,
               '<rect width="%.0f" height="%.0f" rx="%.0f" fill="%s"/>%s'
               % (size, size, size * 0.22, bg,
                  mark(size / 2 - r * REACH / 2, size / 2, r, size * 0.042,
                       ring, dot)))


def main():
    print("Логотип ISP GROUP:")
    write("logo-light.svg", lockup(INK, INK, INK, GOLD))
    write("logo-dark.svg", lockup("#ffffff", CREAM, CREAM, GOLD))
    write("logo-light-plain.svg", lockup(INK, INK, INK, GOLD, sub=False))
    write("logo-dark-plain.svg", lockup("#ffffff", CREAM, CREAM, GOLD, sub=False))
    write("logo-stacked-light.svg", stacked(INK, INK, INK, GOLD))
    write("logo-stacked-dark.svg", stacked("#ffffff", CREAM, CREAM, GOLD))
    write("mark-ink.svg", svg(140, 100, mark(50, 50, 36, 3.0, INK, GOLD)))
    write("mark-cream.svg", svg(140, 100, mark(50, 50, 36, 3.0, CREAM, GOLD)))
    write("icon.svg", icon(DEEP, CREAM, GOLD))
    write("logo-email.svg", lockup(INK, INK, INK, GOLD, bg="#ffffff"))


if __name__ == "__main__":
    main()
