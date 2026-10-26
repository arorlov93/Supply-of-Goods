# -*- coding: utf-8 -*-
"""Кандидаты в фотографии: поиск через Openverse, листы для отбора глазами.

Почему так, а не по Викискладу напрямую. Выходной адрес контейнера общий, и
Викисклад отдаёт на него 429 со сроком повтора 600 секунд, причём и на API,
и на upload.wikimedia.org, и на миниатюры. Openverse индексирует тот же
массив, лимита на нас не кладёт и в ответе сразу даёт натуральные ширину и
высоту плюс прямую ссылку на файл. То есть вся разведка идёт без единого
обращения к Викискладу, а по нему потом забираются только отобранные кадры.

Снимки берутся с source=wikimedia: у flickr и rawpixel отдача без ключа
упирается в 1024 пикселя, а слоты во весь экран требуют от 2000.

Автоматика не понимает, что на кадре: попытка взять «первый подходящий по
размеру» однажды дала для цементного завода придорожный щит. Поэтому скрипт
только собирает варианты и клеит контактный лист, выбор делает человек, а
полное разрешение забирает ov-apply.py.

Запуск: python3.13 tools/ov-candidates.py <слот> [слот ...]
        python3.13 tools/ov-candidates.py --all
"""
import io, json, sys, time, pathlib, urllib.parse, urllib.request
from PIL import Image, ImageDraw

UA = "ISPGroupSiteBot/1.0 (info@ispgroupgc.com)"
# Photon отдаёт файл только браузерному клиенту
BROWSER_UA = "Mozilla/5.0 (X11; Linux x86_64) ISPGroupSiteBot/1.0"
API = "https://api.openverse.org/v1/images/"
OUT = pathlib.Path("/tmp/claude-0/-home-user-Supply-of-Goods/"
                   "4f5e4e6d-222f-57da-93ad-94f5b2132f9f/scratchpad/ov")
MINW, MINH = 1800, 1000
MAXW = 7000           # выше этого пережиматели отказываются тянуть файл
MAXPIX = 36_000_000


def proxies(url, width):
    """Викисклад отдаёт нам 429 на весь контейнер, включая upload и миниатюры,
    поэтому кадры идут через общедоступные пережиматели: они тянут файл своими
    адресами, а нам отдают нужную ширину. Их два, потому что на отдельных
    файлах то один, то другой отвечает отказом."""
    bare = url.split("://", 1)[-1]
    sep = "&" if "?" in url else "?"
    return [
        # weserv берёт с любым User-Agent, Photon требует браузерного
        ("https://images.weserv.nl/?url="
         + urllib.parse.quote(bare, safe="") + f"&w={width}", UA),
        ("https://i0.wp.com/" + bare + sep + f"w={width}", BROWSER_UA),
    ]


def fetch_image(url, width):
    for p, ua in proxies(url, width):
        try:
            return get(p, binary=True, pause=0.4, ua=ua)
        except Exception:
            continue
    return None

# слот -> запросы, от точного к общему. Запросов несколько на слот потому
# что выдача узкая: один запрос часто оставляет после отбора по размеру
# две-три карточки, и выбирать оказывается не из чего.
SLOTS = {
    # путь груза: завод -> контейнер -> трал -> причал -> море -> порт
    "j-works":    ["factory loading dock", "warehouse forklift loading",
                   "industrial plant shipping", "factory interior production"],
    "j-stuffing": ["loading shipping container", "container loading cargo",
                   "forklift container loading", "cargo container warehouse"],
    "j-road":     ["container truck highway", "semi trailer truck container",
                   "truck container transport road", "container lorry"],
    "j-quay":     ["container terminal gantry crane", "container terminal quay",
                   "port container crane", "container terminal loading"],
    "j-sea":      ["container ship sea", "container vessel ocean",
                   "cargo ship containers sea", "container ship underway"],
    "j-arrival":  ["straddle carrier container", "reach stacker container yard",
                   "container terminal yard", "container handling port"],
    # герой главной
    "port-noir":  ["container terminal night", "port crane night lights",
                   "container terminal dusk", "harbour night industrial"],
    # стройматериалы: нужен склад и товар, а не карьер и не ручная добыча
    "build-mat":  ["bricks pallet stacked", "cement bags pallet",
                   "concrete blocks stacked", "building materials pallets"],
    "build-site": ["lumber timber yard stacked", "building materials warehouse",
                   "construction materials storage", "timber stack sawmill"],
    # металл и труба
    "steel":      ["steel pipes stacked", "steel tubes bundle",
                   "steel pipe factory", "steel pipes warehouse"],
    "steel2":     ["steel coils warehouse", "steel rebar bundles",
                   "steel profiles stacked", "metal sheets stacked"],
    # оборудование и инструмент
    "equipment":  ["cnc machine tool", "machine shop lathe",
                   "metalworking machine factory", "industrial machine workshop"],
    "equipment2": ["industrial pumps valves", "factory machinery hall",
                   "industrial equipment plant", "pipes valves industrial plant"],
    "tools":      ["hand tools workbench", "tools workshop wall",
                   "hardware tools shop", "power tools bench"],
    # прочее
    "docs":       ["signing contract document", "documents paperwork desk",
                   "office documents signature", "contract paper desk"],
    "office":     ["office business meeting", "modern office interior",
                   "business desk office work", "office conference room"],
    "agri":       ["grain silo terminal", "grain elevator", "bulk grain terminal",
                   "grain storage silos"],
    "cold":       ["cold storage warehouse", "refrigerated warehouse",
                   "food warehouse pallets", "freezer warehouse"],
}

LAST = [0.0]


def get(url, binary=False, pause=1.1, ua=UA):
    for attempt in range(5):
        gap = pause - (time.time() - LAST[0])
        if gap > 0:
            time.sleep(gap)
        LAST[0] = time.time()
        req = urllib.request.Request(url, headers={"User-Agent": ua})
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                d = r.read()
            return d if binary else d.decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503) or attempt == 4:
                raise
            time.sleep(15 * (attempt + 1))
    raise RuntimeError("лимит")


def search(q, page=1):
    url = API + "?" + urllib.parse.urlencode({
        "q": q, "source": "wikimedia", "license": "cc0,pdm,by",
        "page_size": "20", "page": str(page), "mature": "false",
    })
    try:
        return json.loads(get(url)).get("results") or []
    except Exception as e:
        print(f"    запрос «{q}» не прошёл: {str(e)[:50]}", flush=True)
        return []


def collect(slot, queries, want=40):
    """Кандидатов набирается с запасом: указатель Openverse местами
    устаревший, и часть ссылок ведёт на файлы, которых на Викискладе уже
    нет. Живые отбираются позже, по тому, скачалась миниатюра или нет."""
    rows, seen = [], set()
    for q in queries:
        for page in (1, 2):
            if len(rows) >= want:
                break
            for r in search(q, page):
                if len(rows) >= want:
                    break
                u = r.get("url") or ""
                w, h = r.get("width") or 0, r.get("height") or 0
                key = u.rsplit("/", 1)[-1]
                if not u or key in seen or w < MINW or h < MINH:
                    continue
                if w > MAXW or w * h > MAXPIX:     # пережиматель не возьмёт
                    continue
                if not u.lower().endswith((".jpg", ".jpeg")):
                    continue
                if w / h < 1.15:                   # нужен горизонтальный кадр
                    continue
                seen.add(key)
                rows.append({
                    "i": len(rows), "url": u, "w": w, "h": h,
                    "lic": r.get("license", ""), "title": (r.get("title") or "")[:80],
                    "author": (r.get("creator") or "")[:70],
                    "src": r.get("foreign_landing_url") or u,
                    "thumb": r.get("thumbnail") or "", "q": q,
                })
    return rows


def sheet(slot, rows, keep=12):
    """Контактный лист: четыре карточки в ряд, с номером и разрешением.

    В лист попадают только кадры, которые удалось скачать, после чего они
    перенумеровываются. Иначе номер на листе не совпадал бы с номером в
    rows.json, и ov-apply.py ставил бы в слот не тот кадр."""
    d = OUT / slot
    d.mkdir(parents=True, exist_ok=True)
    live, thumbs = [], []
    for r in rows:
        if len(live) >= keep:
            break
        raw = fetch_image(r["url"], 420)
        if not raw:
            continue
        try:
            im = Image.open(io.BytesIO(raw)).convert("RGB")
        except Exception:
            continue
        r = dict(r, i=len(live))
        live.append(r)
        thumbs.append(im)
    (d / "rows.json").write_text(json.dumps(live, ensure_ascii=False, indent=1))
    if not live:
        print(f"{slot}: живых кандидатов 0 из {len(rows)}", flush=True)
        return
    cw, ch, cols = 420, 300, 4
    nrows = (len(live) + cols - 1) // cols
    sh = Image.new("RGB", (cw * cols, ch * nrows), (22, 24, 29))
    dr = ImageDraw.Draw(sh)
    for r, im in zip(live, thumbs):
        im.thumbnail((cw - 8, ch - 30))
        x, y = (r["i"] % cols) * cw, (r["i"] // cols) * ch
        sh.paste(im, (x + (cw - im.width) // 2, y + 4))
        dr.text((x + 8, y + ch - 22), f'{r["i"]}  {r["w"]}x{r["h"]}  {r["lic"]}',
                fill=(240, 240, 240))
    sh.save(d / "sheet.png")
    print(f"{slot}: живых {len(live)} из {len(rows)} -> {d / 'sheet.png'}", flush=True)


def main(args):
    names = list(SLOTS) if args[:1] == ["--all"] else args
    for slot in names:
        if slot not in SLOTS:
            print(f"нет такого слота: {slot}", flush=True)
            continue
        sheet(slot, collect(slot, SLOTS[slot]))


if __name__ == "__main__":
    main(sys.argv[1:])
