#!/usr/bin/env python3
"""TopoJSON land-110m -> компактная строка контуров для Canvas.

Выход: кольца через "|", точки через пробел, каждая точка "dlon,dlat" в
десятых долях градуса относительно предыдущей. 47 колец, ~8.5 КБ.

Данные: curl -sL https://cdn.jsdelivr.net/npm/world-atlas@2.0.2/land-110m.json -o land.json
"""
import json, math, sys
sys.setrecursionlimit(50000)


def rdp(pts, eps):
    if len(pts) < 3:
        return list(pts)
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1
    nn = math.hypot(dx, dy)
    dmax, idx = 0.0, 0
    for i in range(1, len(pts) - 1):
        px, py = pts[i]
        dd = (abs(dy * px - dx * py + x2 * y1 - y2 * x1) / nn) if nn > 1e-12 \
             else math.hypot(px - x1, py - y1)
        if dd > dmax:
            dmax, idx = dd, i
    if dmax > eps:
        return rdp(pts[:idx + 1], eps)[:-1] + rdp(pts[idx:], eps)
    return [pts[0], pts[-1]]


def simplify_ring(r, eps):
    """Замкнутое кольцо нельзя гнать через RDP напрямую: концы совпадают, базовый
    отрезок вырождается, расстояние до него у всех точек нулевое, и кольцо
    схлопывается в линию. Режем по самой дальней от старта точке."""
    closed = abs(r[0][0] - r[-1][0]) < 1e-9 and abs(r[0][1] - r[-1][1]) < 1e-9
    if not closed:
        return rdp(r, eps)
    x0, y0 = r[0]
    k = max(range(1, len(r) - 1), key=lambda i: (r[i][0] - x0) ** 2 + (r[i][1] - y0) ** 2)
    return rdp(r[:k + 1], eps)[:-1] + rdp(r[k:], eps)


def convert(path_in, path_out, eps=0.5, min_span=2.5):
    d = json.load(open(path_in))
    sc, tr = d["transform"]["scale"], d["transform"]["translate"]

    def decode(a):
        x = y = 0
        out = []
        for dx, dy in a:
            x += dx
            y += dy
            out.append((x * sc[0] + tr[0], y * sc[1] + tr[1]))
        return out

    arcs = [decode(a) for a in d["arcs"]]

    def ring(idxs):
        pts = []
        for i in idxs:
            a = arcs[~i][::-1] if i < 0 else arcs[i]
            pts.extend(a if not pts else a[1:])
        return pts

    polys = []

    def walk(g):
        t = g.get("type")
        if t == "Polygon":
            polys.append(g["arcs"])
        elif t == "MultiPolygon":
            polys.extend(g["arcs"])
        elif t == "GeometryCollection":
            for x in g["geometries"]:
                walk(x)

    walk(d["objects"]["land"])

    out = []
    for p in polys:
        r = ring(p[0])                      # только внешнее кольцо, дырки на глобусе не нужны
        if len(r) < 6:
            continue
        s = simplify_ring(r, eps)
        if len(s) < 6:
            continue
        xs = [q[0] for q in s]
        ys = [q[1] for q in s]
        if (max(xs) - min(xs)) < min_span and (max(ys) - min(ys)) < min_span:
            continue
        out.append([[round(a, 1), round(b, 1)] for a, b in s])
    out.sort(key=len, reverse=True)

    parts = []
    for rr in out:
        px = py = 0
        buf = []
        for lon, lat in rr:
            x, y = int(round(lon * 10)), int(round(lat * 10))
            buf.append(f"{x - px},{y - py}")
            px, py = x, y
        parts.append(" ".join(buf))
    s = "|".join(parts)
    open(path_out, "w").write(s)
    print(f"колец {len(out)}, точек {sum(len(x) for x in out)}, {len(s)} байт")
    return s


if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "land.txt")
