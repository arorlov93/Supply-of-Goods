#!/usr/bin/env python3
"""Поиск свободных фотографий через Openverse с фильтром по лицензии.

  python3 find_photos.py <папка> "запрос один" "запрос два" ...

cc0 и pdm не требуют указания автора. by требует, и автор пишется в CREDITS.json.
Источники, которые из песочницы не работают: unsplash.com (401), pexels и
stocksnap (403), upload.wikimedia.org (429). Rawpixel отдаёт файлы, но со своим
водяным знаком на всех бесплатных размерах. Остаётся Flickr через Openverse.
"""
import json, subprocess, urllib.parse, re, os, sys, time
from PIL import Image

UA = "SiteBuild/1.0 (contact in site footer)"
LIC = os.environ.get("OV_LICENSE", "cc0,pdm")     # добавь ",by" если готов указывать авторов


def ov(q, page=1, n=20):
    u = ("https://api.openverse.org/v1/images/?q=" + urllib.parse.quote(q) +
         f"&license={LIC}&page_size={n}&page={page}&extension=jpg")
    try:
        out = subprocess.run(["curl", "-s", "--max-time", "40", "-A", UA, u],
                             capture_output=True).stdout
        return json.loads(out).get("results") or []
    except Exception:
        return []


def grab(outdir, queries, per=4, minw=900):
    os.makedirs(outdir, exist_ok=True)
    got = []
    for qi, q in enumerate(queries):
        n = 0
        for page in (1, 2):
            for it in ov(q, page):
                u = it.get("url") or ""
                if "live.staticflickr.com" not in u:
                    continue
                w, h = it.get("width") or 0, it.get("height") or 0
                if h >= w * 0.95:                 # только горизонтальные
                    continue
                key = f"q{qi}_{n+1}"
                base = re.sub(r"_[a-z]\.jpg$", "", u)
                p = os.path.join(outdir, key + ".jpg")
                for suf in ("_h.jpg", "_b.jpg", ".jpg"):   # 1600, 1024, оригинал
                    subprocess.run(["curl", "-sL", "--max-time", "70", "-A", UA,
                                    base + suf, "-o", p], capture_output=True)
                    try:
                        im = Image.open(p)
                        if im.size[0] >= minw:
                            got.append({"key": key, "file": p, "size": list(im.size),
                                        "title": (it.get("title") or "")[:60],
                                        "license": it.get("license"),
                                        "author": it.get("creator"),
                                        "source": it.get("foreign_landing_url"),
                                        "query": q})
                            n += 1
                            break
                    except Exception:
                        pass
                if n >= per:
                    break
            if n >= per:
                break
        time.sleep(0.25)
    json.dump(got, open(os.path.join(outdir, "CREDITS.json"), "w"),
              ensure_ascii=False, indent=1)
    print(f"скачано {len(got)}; дальше собери контактный лист и посмотри глазами")
    for g in got:
        print(f"  {g['key']:8} {str(g['size']):12} {g['license']:4} {g['title']}")
    return got


if __name__ == "__main__":
    grab(sys.argv[1], sys.argv[2:])
