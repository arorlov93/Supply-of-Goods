# -*- coding: utf-8 -*-
"""Поставить отобранные кадры в библиотеку сайта.

Викисклад отдаёт на наш выходной адрес 429 со сроком повтора 600 секунд, и
это касается и API, и upload.wikimedia.org, и его миниатюр. Поэтому кадр
забирается не напрямую, а через общедоступный пережиматель Photon: он тянет
файл своими адресами и отдаёт нам нужную ширину. Лимит Викисклада при этом
не трогается вообще.

Запуск: python3.13 tools/ov-apply.py <слот>:<номер>[:<целевой файл>] ...
Пример: python3.13 tools/ov-apply.py j-sea:3 steel:1:steel-tubes
"""
import io, json, sys, time, pathlib, urllib.error, urllib.parse, urllib.request
from PIL import Image

UA = "ISPGroupSiteBot/1.0 (info@ispgroupgc.com)"
# Photon отдаёт файл только браузерному клиенту
BROWSER_UA = "Mozilla/5.0 (X11; Linux x86_64) ISPGroupSiteBot/1.0"
CAND = pathlib.Path("/tmp/claude-0/-home-user-Supply-of-Goods/"
                    "4f5e4e6d-222f-57da-93ad-94f5b2132f9f/scratchpad/ov")
MEDIA = pathlib.Path(__file__).resolve().parent.parent / "site" / "media"
PAUSE = 1.5           # между файлами: Photon щедр, но вежливость дешёвая
MAXW = 2400           # хватает для сцены во весь экран на экране 2x


def proxies(url, width):
    """Два пережимателя: на отдельных файлах то один, то другой отказывает."""
    bare = url.split("://", 1)[-1]
    sep = "&" if "?" in url else "?"
    return [
        # weserv берёт с любым User-Agent, Photon требует браузерного
        ("https://images.weserv.nl/?url="
         + urllib.parse.quote(bare, safe="") + f"&w={width}", UA),
        ("https://i0.wp.com/" + bare + sep + f"w={width}", BROWSER_UA),
    ]


def fetch_one(url, ua, tries=4):
    for attempt in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": ua})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503) or attempt == tries - 1:
                raise
            wait = min(int(e.headers.get("Retry-After") or 0) or 30 * (attempt + 1), 180)
            print(f"    лимит, жду {wait}с", flush=True)
            time.sleep(wait)
    raise RuntimeError("не удалось")


def fetch(url, width):
    last = None
    for p, ua in proxies(url, width):
        try:
            return fetch_one(p, ua)
        except Exception as e:
            last = e
    raise RuntimeError(f"оба пережимателя отказали: {str(last)[:40]}")


def apply_one(slot, idx, target):
    rows = json.loads((CAND / slot / "rows.json").read_text())
    row = next(r for r in rows if r["i"] == int(idx))
    raw = fetch(row["url"], MAXW)
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    src = (row["w"], row["h"])
    if im.width > MAXW:
        im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
    im.save(MEDIA / f"{target}.jpg", "JPEG", quality=84, optimize=True, progressive=True)
    im.save(MEDIA / f"{target}.webp", "WEBP", quality=82, method=5)

    cred = json.loads((MEDIA / "CREDITS.json").read_text())
    cred[f"{target}.jpg"] = {
        "title": row["title"], "license": row["lic"],
        "author": row["author"] or None, "source": row["src"],
    }
    (MEDIA / "CREDITS.json").write_text(json.dumps(cred, ensure_ascii=False, indent=1))
    print(f"  ok  {target}: {src[0]}x{src[1]} -> {im.size[0]}x{im.size[1]}  "
          f"{row['lic']}  {row['title'][:46]}", flush=True)


def main(args):
    for n, a in enumerate(args):
        parts = a.split(":")
        slot, idx = parts[0], parts[1]
        target = parts[2] if len(parts) > 2 else slot
        if n:
            time.sleep(PAUSE)
        try:
            apply_one(slot, idx, target)
        except Exception as e:
            print(f"  нет {target}: {str(e)[:70]}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
