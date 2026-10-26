# -*- coding: utf-8 -*-
"""Замена фотобиблиотеки сайта на снимки нормального разрешения.

Старые файлы были шириной 460-1040 пикселей и на полноэкранных сценах
превращались в мыло. Здесь они заменяются кадрами с Викисклада шириной от
2000 пикселей, только с лицензиями CC0 и public domain, чтобы строка в
подвале сайта оставалась правдой.

Запуск: python3.13 tools/fetch-photos.py
"""
import json, re, io, pathlib, urllib.request, urllib.parse, sys
from PIL import Image

UA = "ISPGroupSiteBot/1.0 (info@ispgroupgc.com)"
API = "https://commons.wikimedia.org/w/api.php"
MEDIA = pathlib.Path(__file__).resolve().parent.parent / "site" / "media"
OK_LICENCE = re.compile(r"^(cc0|public domain|pd|no restrictions)", re.I)

# слот на сайте -> поисковый запрос
WANT = {
    "port-noir":       "container terminal gantry crane dusk",
    "containers-wall": "stacked shipping containers",
    "quarry-stone":    "limestone quarry excavator",
    "pipe":            "steel pipes stacked industry",
    "machinery":       "factory machine shop industrial machinery",
    "ship-aerial":     "container ship aerial view sea",
    "loading-truck":   "truck loading warehouse cargo",
    "crane-dusk":      "harbour crane sunset port",
    "quarry-cut":      "granite stone blocks quarry",
    "robots":          "factory production line industrial plant",
    "tools-flat":      "hand tools workbench",
    "pallets-wall":    "warehouse pallets stacked cardboard",
    "coldstore":       "cold storage warehouse frozen",
    "steel-tubes":     "steel tubes mill stack",
    "vessel":          "cargo ship at sea",
    "terminal":        "port container terminal aerial",
}


import time, random

LAST = [0.0]

def get(url, tries=6):
    """Викисклад делит лимит на весь выходной адрес, поэтому запросы редкие
    и с нарастающей паузой при отказе."""
    for n in range(tries):
        gap = 7.0 - (time.time() - LAST[0])
        if gap > 0:
            time.sleep(gap)
        LAST[0] = time.time()
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503) or n == tries - 1:
                raise
            wait = min(90, 12 * (n + 1)) + random.uniform(0, 4)
            print(f"      лимит, жду {wait:.0f}с", flush=True)
            time.sleep(wait)
    raise RuntimeError("не удалось")


def search(query, limit=14):
    q = urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "search",
        "gsrnamespace": "6", "gsrsearch": query, "gsrlimit": str(limit),
        "prop": "imageinfo", "iiprop": "url|size|extmetadata",
    })
    data = json.loads(get(API + "?" + q))
    pages = (data.get("query") or {}).get("pages") or {}
    out = []
    for p in pages.values():
        ii = p["imageinfo"][0]
        meta = ii.get("extmetadata", {})
        lic = (meta.get("LicenseShortName") or {}).get("value", "")
        if not OK_LICENCE.match(lic.strip()):
            continue
        if ii["width"] < 2000 or ii["height"] < 1100:
            continue
        if ii["width"] / ii["height"] < 1.15:          # нужен горизонтальный кадр
            continue
        out.append({
            "title": p["title"], "url": ii["url"],
            "w": ii["width"], "h": ii["height"], "lic": lic,
            "author": re.sub(r"<[^>]+>", "", (meta.get("Artist") or {}).get("value", "")).strip()[:80],
            "src": (meta.get("DescriptionShortUrl") or {}).get("value", ""),
        })
    out.sort(key=lambda x: -x["w"])
    return out


def save(slot, cand):
    raw = get(cand["url"])
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    # 2400 по ширине хватает для сцены во весь экран на экране 2x
    if im.width > 2400:
        im = im.resize((2400, round(im.height * 2400 / im.width)), Image.LANCZOS)
    im.save(MEDIA / f"{slot}.jpg", "JPEG", quality=82, optimize=True, progressive=True)
    im.save(MEDIA / f"{slot}.webp", "WEBP", quality=80, method=5)
    return im.size


def main(only=None):
    credits = json.loads((MEDIA / "CREDITS.json").read_text())
    done, failed = [], []
    for slot, query in WANT.items():
        if only and slot not in only:
            continue
        try:
            cands = search(query)
            if not cands:
                failed.append((slot, "нет кадров под лицензией CC0 или PD")); continue
            c = cands[0]
            w, h = save(slot, c)
            credits[f"{slot}.jpg"] = {
                "title": c["title"].replace("File:", ""),
                "license": c["lic"], "author": c["author"] or None,
                "source": c["src"] or c["url"],
            }
            done.append(f"{slot}: {c['w']}x{c['h']} -> {w}x{h}  {c['lic']}")
            print("  ok  ", done[-1], flush=True)
        except Exception as e:
            failed.append((slot, str(e)[:80]))
            print("  нет ", slot, "|", str(e)[:70], flush=True)
    (MEDIA / "CREDITS.json").write_text(json.dumps(credits, ensure_ascii=False, indent=1))
    for d in done:
        print("  ok  ", d)
    for s, e in failed:
        print("  нет ", s, "|", e)
    print(f"\nзаменено {len(done)}, не вышло {len(failed)}")


if __name__ == "__main__":
    main(sys.argv[1:] or None)
