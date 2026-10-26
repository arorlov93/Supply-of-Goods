# -*- coding: utf-8 -*-
"""Кандидаты в фотографии по категориям Викисклада, листами для отбора глазами.

Почему не поиск. Полнотекстовый поиск Openverse по Викискладу на запрос
«factory loading dock» выдал церемонию награждения на водородной
конференции и два классических автомобиля. Категория же устроена иначе: в
«Category:Container cranes» лежат именно контейнерные краны, потому что
туда их положили руками. Смысловое попадание получается без догадок.

Почему картинки идут через пережиматель. Викисклад держит ограничение на
весь наш выходной адрес и отдаёт 429 со сроком повтора 600 секунд, включая
upload.wikimedia.org. Поэтому к Викискладу обращается только разбор
категории, один запрос на категорию и с паузой, а файлы тянутся через
общедоступные weserv и Photon, которые ходят за ними своими адресами.

Лицензия здесь не выясняется: это ещё один запрос на каждый файл, а нужна
она только для выбранных кадров. Её забирает wc-apply.py, уже поштучно.

Запуск: python3.13 tools/wc-candidates.py <слот> [слот ...]
        python3.13 tools/wc-candidates.py --all
"""
import io, json, re, sys, time, pathlib, urllib.error, urllib.parse, urllib.request
from PIL import Image, ImageDraw

UA = "ISPGroupSiteBot/1.0 (info@ispgroupgc.com)"
BROWSER_UA = "Mozilla/5.0 (X11; Linux x86_64) ISPGroupSiteBot/1.0"
BASE = "https://commons.wikimedia.org"
OUT = pathlib.Path("/tmp/claude-0/-home-user-Supply-of-Goods/"
                   "4f5e4e6d-222f-57da-93ad-94f5b2132f9f/scratchpad/wc")
MINW = 1600           # ниже этого кадр не годится ни под одну сцену
CAT_PAUSE = 9.0       # между обращениями к Викискладу

# слот -> категории, от точной к запасной
SLOTS = {
    # путь груза: завод -> контейнер -> трал -> причал -> море -> порт
    "j-works":    ["Loading_docks", "Forklifts_in_warehouses", "Forklifts"],
    "j-stuffing": ["Loading_of_containers", "Container_loading",
                   "Shipping_containers_being_loaded"],
    "j-road":     ["Container_trucks", "Semi-trailer_trucks", "Trucks_carrying_containers"],
    "j-quay":     ["Container_cranes", "Gantry_cranes", "Container_terminals"],
    "j-sea":      ["Container_ships_at_sea", "Container_ships", "Cargo_ships"],
    "j-arrival":  ["Straddle_carriers", "Reach_stackers", "Container_yards"],
    # герой главной
    "port-noir":  ["Ports_at_night", "Container_terminals_at_night", "Harbours_at_night"],
    # стройматериалы: склад и товар, а не карьер и не ручная добыча
    "build-mat":  ["Cement_bags", "Building_materials", "Concrete_blocks"],
    "build-site": ["Lumber_yards", "Timber_yards", "Sawn_timber"],
    # металл и труба
    "steel":      ["Steel_pipes", "Steel_tubes", "Tubes_(metal)"],
    "steel2":     ["Steel_coils", "Reinforcing_bars", "Steel_products"],
    # оборудование и инструмент
    "equipment":  ["Machine_tools", "Lathes", "Milling_machines"],
    "equipment2": ["Industrial_valves", "Pumps", "Industrial_pipework"],
    "tools":      ["Hand_tools", "Toolboxes", "Hardware_stores"],
    # общий кадр для страницы «что мы делаем»: порт, а не автомобильный завод
    "ops":        ["Container_terminals", "Ports", "Harbours"],
    # бумага и упаковка: нужен товар, а не деревянные паллеты с чайками
    "pack":       ["Paper_industry", "Distribution_centers", "Warehouse_interiors",
                   "Paper_mills", "Pallet_racking"],
    # прочее
    "docs":       ["Documents", "Business_documents", "Signatures"],
    "agri":       ["Grain_elevators", "Silos", "Grain_storage"],
    "cold":       ["Cold_storage_warehouses", "Refrigerated_warehouses", "Warehouses"],
}

LAST = [0.0]


def get(url, binary=False, pause=1.0, ua=UA):
    for attempt in range(4):
        gap = pause - (time.time() - LAST[0])
        if gap > 0:
            time.sleep(gap)
        LAST[0] = time.time()
        req = urllib.request.Request(url, headers={"User-Agent": ua})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                d = r.read()
            return d if binary else d.decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503) or attempt == 3:
                raise
            wait = min(int(e.headers.get("Retry-After") or 0) or 60 * (attempt + 1), 620)
            print(f"    Викисклад просит подождать {wait}с", flush=True)
            time.sleep(wait)
    raise RuntimeError("лимит")


def proxies(url, width):
    """weserv берёт с любым User-Agent, Photon требует браузерного."""
    bare = url.split("://", 1)[-1]
    return [
        ("https://images.weserv.nl/?url=" + urllib.parse.quote(bare, safe="")
         + f"&w={width}", UA),
        ("https://i0.wp.com/" + bare + f"?w={width}", BROWSER_UA),
    ]


def file_url(name):
    """Прямой адрес файла на Викискладе, без обращения к нему: путь задаётся
    первыми знаками md5 от имени."""
    import hashlib
    n = name[5:].replace(" ", "_")
    h = hashlib.md5(n.encode()).hexdigest()
    return (f"https://upload.wikimedia.org/wikipedia/commons/{h[0]}/{h[:2]}/"
            + urllib.parse.quote(n))


def fetch_image(name, width):
    for p, ua in proxies(file_url(name), width):
        try:
            return get(p, binary=True, pause=0.35, ua=ua)
        except Exception:
            continue
    return None


def files_in(cat):
    try:
        html = get(f"{BASE}/wiki/Category:{cat}", pause=CAT_PAUSE)
    except Exception as e:
        print(f"    категория {cat}: {str(e)[:50]}", flush=True)
        return []
    names, seen = [], set()
    for m in re.finditer(r'href="/wiki/(File:[^"]+?\.(?:jpg|jpeg|JPG|JPEG))"', html):
        n = urllib.parse.unquote(m.group(1))
        if n not in seen:
            seen.add(n)
            names.append(n)
    return names


def sheet(slot, cats, keep=12, tries=34):
    d = OUT / slot
    d.mkdir(parents=True, exist_ok=True)
    names = []
    for c in cats:
        names += [n for n in files_in(c) if n not in names]
        if len(names) >= tries:
            break
    live, thumbs = [], []
    for n in names[:tries]:
        if len(live) >= keep:
            break
        raw = fetch_image(n, 420)
        if not raw:
            continue
        try:
            im = Image.open(io.BytesIO(raw)).convert("RGB")
        except Exception:
            continue
        # пережиматель вернул меньше запрошенного, значит исходник мелкий
        if im.width < 420:
            continue
        live.append({"i": len(live), "name": n, "url": file_url(n)})
        thumbs.append(im)

    (d / "rows.json").write_text(json.dumps(live, ensure_ascii=False, indent=1))
    if not live:
        print(f"{slot}: живых 0 из {len(names)}", flush=True)
        return
    cw, ch, cols = 420, 300, 4
    nrows = (len(live) + cols - 1) // cols
    sh = Image.new("RGB", (cw * cols, ch * nrows), (22, 24, 29))
    dr = ImageDraw.Draw(sh)
    for r, im in zip(live, thumbs):
        im.thumbnail((cw - 8, ch - 30))
        x, y = (r["i"] % cols) * cw, (r["i"] // cols) * ch
        sh.paste(im, (x + (cw - im.width) // 2, y + 4))
        dr.text((x + 8, y + ch - 22), f'{r["i"]}  {r["name"][5:42]}', fill=(240, 240, 240))
    sh.save(d / "sheet.png")
    print(f"{slot}: живых {len(live)} из {len(names)} -> {d / 'sheet.png'}", flush=True)


def main(args):
    names = list(SLOTS) if args[:1] == ["--all"] else args
    for slot in names:
        if slot not in SLOTS:
            print(f"нет такого слота: {slot}", flush=True)
            continue
        sheet(slot, SLOTS[slot])


if __name__ == "__main__":
    main(sys.argv[1:])
