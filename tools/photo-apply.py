# -*- coding: utf-8 -*-
"""Поставить выбранный кандидат в библиотеку сайта.

Запуск: python3.13 tools/photo-apply.py <слот> <номер кандидата> [<целевой файл>]
Номер берётся с контактного листа, который делает photo-candidates.py.
"""
import io, json, re, sys, time, pathlib, urllib.parse, urllib.request
from PIL import Image

UA = "ISPGroupSiteBot/1.0 (info@ispgroupgc.com)"
BASE = "https://commons.wikimedia.org"
CAND = pathlib.Path("/tmp/claude-0/-home-user-Supply-of-Goods/"
                    "4f5e4e6d-222f-57da-93ad-94f5b2132f9f/scratchpad/cand")
MEDIA = pathlib.Path(__file__).resolve().parent.parent / "site" / "media"


def get(url):
    for a in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or a == 4:
                raise
            time.sleep(25 * (a + 1))


def main(slot, idx, target=None):
    rows = json.loads((CAND / slot / "names.json").read_text())
    row = next(r for r in rows if r["i"] == int(idx))
    name = row["name"]
    target = target or slot
    raw = get(f"{BASE}/wiki/Special:FilePath/{urllib.parse.quote(name[5:])}")
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    src = im.size
    if im.width > 2400:
        im = im.resize((2400, round(im.height * 2400 / im.width)), Image.LANCZOS)
    im.save(MEDIA / f"{target}.jpg", "JPEG", quality=84, optimize=True, progressive=True)
    im.save(MEDIA / f"{target}.webp", "WEBP", quality=82, method=5)

    cred = json.loads((MEDIA / "CREDITS.json").read_text())
    cred[f"{target}.jpg"] = {
        "title": name[5:].replace("_", " "),
        "license": row.get("lic", ""),
        "author": None,
        "source": f"{BASE}/wiki/{urllib.parse.quote(name)}",
    }
    (MEDIA / "CREDITS.json").write_text(json.dumps(cred, ensure_ascii=False, indent=1))
    print(f"{target}: {src[0]}x{src[1]} -> {im.size[0]}x{im.size[1]}  {row.get('lic')}  {name[5:][:50]}")


if __name__ == "__main__":
    main(*sys.argv[1:])
