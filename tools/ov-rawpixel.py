# -*- coding: utf-8 -*-
"""Кандидаты с rawpixel через Openverse, для карточек.

Зачем отдельно от wc-candidates. По некоторым темам в категориях
Викисклада просто нет годного: на «бумагу и упаковку» он дал пустые
стеллажи, брендовый снимок поставщика стеллажей и мотоциклы на полках.
У rawpixel по тем же словам лежат снятые студийно кадры под CC0.

Ограничение rawpixel: без ключа он отдаёт не больше 1024 пикселей по
ширине. Для сцены во весь экран этого мало, а для карточки направления
достаточно: она показывается примерно на 350 пикселях, то есть 700 на
экране с удвоенной плотностью. Поэтому скрипт годится только для
карточек, и это не недосмотр, а граница применения.

Запуск: python3.13 tools/ov-rawpixel.py <слот> <запрос> [<запрос> ...]
"""
import io, json, sys, time, urllib.parse, urllib.request, pathlib
from PIL import Image, ImageDraw

UA = "ISPGroupSiteBot/1.0 (info@ispgroupgc.com)"
API = "https://api.openverse.org/v1/images/"
OUT = pathlib.Path("/tmp/claude-0/-home-user-Supply-of-Goods/"
                   "4f5e4e6d-222f-57da-93ad-94f5b2132f9f/scratchpad/rp")
MINW = 700            # ниже этого даже карточка будет мылом


def get(url, binary=False):
    for attempt in range(4):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                d = r.read()
            return d if binary else d.decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503) or attempt == 3:
                raise
            time.sleep(20 * (attempt + 1))
    raise RuntimeError("лимит")


def search(q):
    url = API + "?" + urllib.parse.urlencode({
        "q": q, "source": "rawpixel", "license": "cc0",
        "page_size": "20", "mature": "false",
    })
    try:
        return json.loads(get(url)).get("results") or []
    except Exception as e:
        print(f"    запрос «{q}»: {str(e)[:50]}", flush=True)
        return []


def main(slot, queries, keep=12):
    d = OUT / slot
    d.mkdir(parents=True, exist_ok=True)
    live, thumbs, seen = [], [], set()
    for q in queries:
        if len(live) >= keep:
            break
        for r in search(q):
            if len(live) >= keep:
                break
            u = r.get("url") or ""
            if not u or u in seen:
                continue
            seen.add(u)
            try:
                im = Image.open(io.BytesIO(get(u, binary=True))).convert("RGB")
            except Exception:
                continue
            if im.width < MINW:
                continue
            live.append({
                "i": len(live), "url": u, "w": im.width, "h": im.height,
                "lic": r.get("license", ""), "title": (r.get("title") or "")[:70],
                "author": (r.get("creator") or "")[:60],
                "src": r.get("foreign_landing_url") or u, "q": q,
            })
            thumbs.append(im)

    (d / "rows.json").write_text(json.dumps(live, ensure_ascii=False, indent=1))
    if not live:
        print(f"{slot}: живых 0", flush=True)
        return
    cw, ch, cols = 420, 300, 4
    nrows = (len(live) + cols - 1) // cols
    sh = Image.new("RGB", (cw * cols, ch * nrows), (22, 24, 29))
    dr = ImageDraw.Draw(sh)
    for r, im in zip(live, thumbs):
        im.thumbnail((cw - 8, ch - 30))
        x, y = (r["i"] % cols) * cw, (r["i"] // cols) * ch
        sh.paste(im, (x + (cw - im.width) // 2, y + 4))
        dr.text((x + 8, y + ch - 22), f'{r["i"]}  {r["w"]}x{r["h"]}  {r["title"][:30]}',
                fill=(240, 240, 240))
    sh.save(d / "sheet.png")
    print(f"{slot}: живых {len(live)} -> {d / 'sheet.png'}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
