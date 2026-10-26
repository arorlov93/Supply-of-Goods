# -*- coding: utf-8 -*-
"""Кандидаты в фотографии: миниатюры для отбора глазами.

Автоматика не понимает, что на кадре. Попытка выбрать «первый подходящий по
размеру и лицензии» дала для цементного завода придорожный рекламный щит.
Поэтому роль скрипта сведена к сбору вариантов, а выбор делает человек по
контактному листу. Полное разрешение забирает photo-apply.py.

Запуск: python3.13 tools/photo-candidates.py <слот> <Категория> [Категория ...]
"""
import io, json, re, sys, time, pathlib, urllib.parse, urllib.request
from PIL import Image, ImageDraw

UA = "ISPGroupSiteBot/1.0 (info@ispgroupgc.com)"
BASE = "https://commons.wikimedia.org"
OUT = pathlib.Path("/tmp/claude-0/-home-user-Supply-of-Goods/"
                   "4f5e4e6d-222f-57da-93ad-94f5b2132f9f/scratchpad/cand")
FREE = re.compile(r"(cc0|public domain|cc[ -]by(-sa)?[ -]\d|no known copyright)", re.I)
LAST = [0.0]


def get(url, binary=False, pause=4.5):
    for a in range(5):
        gap = pause - (time.time() - LAST[0])
        if gap > 0:
            time.sleep(gap)
        LAST[0] = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                d = r.read()
            return d if binary else d.decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code != 429 or a == 4:
                raise
            time.sleep(25 * (a + 1))


def files_in(cat, limit=16):
    try:
        html = get(f"{BASE}/wiki/Category:{cat}")
    except Exception:
        return []
    names, seen = [], set()
    for m in re.finditer(r'href="/wiki/(File:[^"]+?\.(?:jpg|jpeg|JPG))"', html):
        n = urllib.parse.unquote(m.group(1))
        if n not in seen:
            seen.add(n)
            names.append(n)
    return names[:limit]


def info(name):
    html = get(f"{BASE}/wiki/{urllib.parse.quote(name)}")
    pairs = []
    for m in re.finditer(r'([\d][\d,   ]{2,8})\s*×\s*([\d][\d,   ]{2,8})', html):
        try:
            a = int(re.sub(r"[^\d]", "", m.group(1)))
            b = int(re.sub(r"[^\d]", "", m.group(2)))
        except ValueError:
            continue
        if 100 < a < 20000 and 100 < b < 20000:
            pairs.append((a, b))
    if not pairs:
        return None
    w, h = max(pairs, key=lambda t: t[0] * t[1])
    m = re.search(r'(CC0|public domain|CC BY-SA \d\.\d|CC BY \d\.\d)', html, re.I)
    return {"w": w, "h": h, "lic": m.group(1) if m else ""}


def main(slot, cats, want=8):
    d = OUT / slot
    d.mkdir(parents=True, exist_ok=True)
    rows = []
    for cat in cats:
        for name in files_in(cat):
            if len(rows) >= want:
                break
            m = info(name)
            if not m or m["w"] < 1800 or m["w"] / m["h"] < 1.1:
                continue
            if not FREE.search(m["lic"] or ""):
                continue
            try:
                raw = get(f"{BASE}/wiki/Special:FilePath/{urllib.parse.quote(name[5:])}?width=560",
                          binary=True, pause=5.0)
                im = Image.open(io.BytesIO(raw)).convert("RGB")
            except Exception:
                continue
            im.thumbnail((440, 300))
            card = Image.new("RGB", (440, 322), (24, 27, 33))
            card.paste(im, ((440 - im.width) // 2, 0))
            ImageDraw.Draw(card).text((8, 304), f"{len(rows)}   {m['w']}x{m['h']}   {m['lic']}",
                                      fill=(235, 235, 235))
            card.save(d / f"{len(rows):02d}.png")
            rows.append({"i": len(rows), "name": name, **m})
        if len(rows) >= want:
            break
    (d / "names.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
    print(f"{slot}: кандидатов {len(rows)}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
