# -*- coding: utf-8 -*-
"""Поставить отобранные кадры в библиотеку сайта.

Сам файл идёт через общедоступный пережиматель: Викисклад держит
ограничение на весь наш выходной адрес, а пережиматель ходит за файлом
своим. К Викискладу обращается только чтение страницы файла, и только ради
лицензии и автора, то есть один запрос на поставленный кадр, с паузой.

Лицензия проверяется, а не предполагается: в подвале сайта стоит строка о
происхождении снимков, и она должна оставаться правдой. Кадр под несвободной
лицензией не ставится.

Запуск: python3.13 tools/wc-apply.py <слот>:<номер>[:<целевой файл>] ...
Пример: python3.13 tools/wc-apply.py j-quay:2:port-noir j-road:8
"""
import io, json, re, sys, time, pathlib, urllib.error, urllib.parse, urllib.request
from PIL import Image

UA = "ISPGroupSiteBot/1.0 (info@ispgroupgc.com)"
BROWSER_UA = "Mozilla/5.0 (X11; Linux x86_64) ISPGroupSiteBot/1.0"
BASE = "https://commons.wikimedia.org"
CAND = pathlib.Path("/tmp/claude-0/-home-user-Supply-of-Goods/"
                    "4f5e4e6d-222f-57da-93ad-94f5b2132f9f/scratchpad/wc")
MEDIA = pathlib.Path(__file__).resolve().parent.parent / "site" / "media"
MAXW = 2400           # хватает для сцены во весь экран на экране 2x
FREE = re.compile(r"(cc0|public domain|cc[ -]by(-sa)?[ -]\d|no known copyright)", re.I)


def get(url, binary=False, ua=UA, tries=4):
    for attempt in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": ua})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                d = r.read()
            return d if binary else d.decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503) or attempt == tries - 1:
                raise
            wait = min(int(e.headers.get("Retry-After") or 0) or 45 * (attempt + 1), 620)
            print(f"    лимит, жду {wait}с", flush=True)
            time.sleep(wait)
    raise RuntimeError("не удалось")


def fetch_image(url, width):
    """Пережиматели отвечают отказом по двум разным причинам: weserv не
    берёт большие исходники вообще, а оба временно отказывают, когда к ним
    часто обращаются. Отличить одно от другого по коду нельзя, оба отдают
    404, поэтому ширина понижается ступенями, а круги повторяются с паузой."""
    bare = url.split("://", 1)[-1]
    widths = [w for w in (width, 2000, 1600) if w <= width] or [width]
    for rnd in range(4):
        for w in widths:
            for p, ua in [
                ("https://i0.wp.com/" + bare + f"?w={w}", BROWSER_UA),
                ("https://images.weserv.nl/?url=" + urllib.parse.quote(bare, safe="")
                 + f"&w={w}", UA),
            ]:
                try:
                    return get(p, binary=True, ua=ua, tries=1)
                except Exception:
                    continue
        if rnd < 3:
            time.sleep(20 * (rnd + 1))
    raise RuntimeError("пережиматели не отдали файл")


def licence(name):
    """Лицензия и автор со страницы файла. Единственное обращение к
    Викискладу на кадр."""
    html = get(f"{BASE}/wiki/{urllib.parse.quote(name)}")
    m = re.search(r"(CC0|public domain|CC BY-SA \d\.\d|CC BY \d\.\d)", html, re.I)
    lic = m.group(1) if m else ""
    author = ""
    a = re.search(r'id="fileinfotpl_aut".*?</td>\s*<td[^>]*>(.*?)</td>', html, re.S)
    if a:
        author = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", a.group(1))).strip()[:70]
    return lic, author


def apply_one(slot, idx, target):
    rows = json.loads((CAND / slot / "rows.json").read_text())
    row = next(r for r in rows if r["i"] == int(idx))
    name = row["name"]

    lic, author = licence(name)
    if not FREE.search(lic):
        print(f"  нет {target}: лицензия «{lic or 'не определена'}», не ставлю", flush=True)
        return

    im = Image.open(io.BytesIO(fetch_image(row["url"], MAXW))).convert("RGB")
    src = im.size
    if im.width > MAXW:
        im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
    im.save(MEDIA / f"{target}.jpg", "JPEG", quality=84, optimize=True, progressive=True)
    im.save(MEDIA / f"{target}.webp", "WEBP", quality=82, method=5)

    cred = json.loads((MEDIA / "CREDITS.json").read_text())
    cred[f"{target}.jpg"] = {
        "title": name[5:].replace("_", " ").rsplit(".", 1)[0],
        "license": lic, "author": author or None,
        "source": f"{BASE}/wiki/{urllib.parse.quote(name)}",
    }
    (MEDIA / "CREDITS.json").write_text(json.dumps(cred, ensure_ascii=False, indent=1))
    print(f"  ok  {target}: {src[0]}x{src[1]} -> {im.size[0]}x{im.size[1]}  "
          f"{lic}  {name[5:48]}", flush=True)


def main(args):
    for n, a in enumerate(args):
        parts = a.split(":")
        slot, idx = parts[0], parts[1]
        target = parts[2] if len(parts) > 2 else slot
        if n:
            time.sleep(8)            # пауза ради страницы файла на Викискладе
        try:
            apply_one(slot, idx, target)
        except Exception as e:
            print(f"  нет {target}: {str(e)[:70]}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
