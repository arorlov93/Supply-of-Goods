# -*- coding: utf-8 -*-
"""Фотографии нормального разрешения, в обход ограничения на API Викисклада.

API отдаёт 429 с общего выходного адреса, поэтому здесь используются обычные
страницы: категория -> список файлов, страница файла -> лицензия и размер,
Special:FilePath -> сам файл. Этот путь не ограничивается.

Берутся только свободные лицензии. CC BY и BY-SA допускаются, автор пишется
в media/CREDITS.json и выводится на странице титров.

Запуск: python3.13 tools/fetch-photos2.py [слот ...]
"""
import io, json, re, sys, time, pathlib, urllib.parse, urllib.request

UA = "ISPGroupSiteBot/1.0 (info@ispgroupgc.com)"
BASE = "https://commons.wikimedia.org"
MEDIA = pathlib.Path(__file__).resolve().parent.parent / "site" / "media"
FREE = re.compile(r"(cc0|public domain|cc[ -]by(-sa)?[ -]\d|no known copyright)", re.I)

# слот -> категории Викисклада, от более подходящих к менее
SLOTS = {
    "quarry-cut":      ["Quality_images_of_ceramic_tiles", "Ceramic_tile_factories", "Tile_manufacturing"],
    "quarry-stone":    ["Cement_plants", "Concrete_plants", "Building_material_shops"],
    "port-noir":       ["Quality_images_of_container_terminals", "Container_terminals_at_night", "Container_cranes"],
    "steel-tubes":     ["Steel_pipes", "Steel_products", "Pipe_stacks"],
    "machinery":       ["Quality_images_of_machine_tools", "Industrial_machinery", "Machine_tools"],
    "silos":           ["Industrial_plants", "Chemical_plants", "Factories"],
    "tools-flat":      ["Hand_tools", "Tool_shops", "Hardware_stores"],
    "pallets-wall":    ["Corrugated_fiberboard", "Packaging_materials", "Warehouses"],
    "coldstore":       ["Cold_storage", "Refrigerated_warehouses", "Food_warehouses"],
    "loading-truck":   ["Loading_of_trucks", "Cargo_trucks", "Logistics_centres"],
    "ship-aerial":     ["Aerial_photographs_of_container_ships", "Container_ships", "Cargo_ships"],
    "crane-dusk":      ["Container_cranes_at_sunset", "Ports_at_sunset", "Harbour_cranes"],
}

LAST = [0.0]

def get(url, binary=False, pause=4.5):
    gap = pause - (time.time() - LAST[0])
    if gap > 0:
        time.sleep(gap)
    LAST[0] = time.time()
    for attempt in range(5):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                data = r.read()
            return data if binary else data.decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 4:
                raise
            time.sleep(25 * (attempt + 1))
    raise RuntimeError("limit")


def files_in(cat):
    try:
        html = get(f"{BASE}/wiki/Category:{cat}")
    except Exception:
        return []
    names, seen = [], set()
    for m in re.finditer(r'href="/wiki/(File:[^"]+?\.(?:jpg|jpeg|JPG|png))"', html):
        n = urllib.parse.unquote(m.group(1))
        if n not in seen:
            seen.add(n); names.append(n)
    return names[:8]


def info(name):
    """Размер, лицензия и автор со страницы файла."""
    html = get(f"{BASE}/wiki/{urllib.parse.quote(name)}")
    # на странице несколько размеров, нужен самый большой: это оригинал.
    # числа идут с разделителями тысяч, поэтому они вычищаются
    pairs = []
    for m in re.finditer(r'([\d][\d,\u00a0\u202f ]{2,8})\s*×\s*([\d][\d,\u00a0\u202f ]{2,8})', html):
        try:
            a = int(re.sub(r'[^\d]', '', m.group(1)))
            b = int(re.sub(r'[^\d]', '', m.group(2)))
        except ValueError:
            continue
        if 100 < a < 20000 and 100 < b < 20000:
            pairs.append((a, b))
    if not pairs:
        return None
    w, h = max(pairs, key=lambda t: t[0] * t[1])
    lic = ""
    for m in re.finditer(r'(CC0|public domain|CC BY-SA \d\.\d|CC BY \d\.\d)', html, re.I):
        lic = m.group(1); break
    author = ""
    a = re.search(r'id="fileinfotpl_aut".*?</td>\s*<td[^>]*>(.*?)</td>', html, re.S)
    if a:
        author = re.sub(r"<[^>]+>", " ", a.group(1))
        author = re.sub(r"\s+", " ", author).strip()[:70]
    return {"w": w, "h": h, "lic": lic, "author": author}


def grab(slot, name, meta):
    from PIL import Image
    raw = get(f"{BASE}/wiki/Special:FilePath/{urllib.parse.quote(name[5:])}", binary=True, pause=6.0)
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    if im.width > 2400:
        im = im.resize((2400, round(im.height * 2400 / im.width)), Image.LANCZOS)
    im.save(MEDIA / f"{slot}.jpg", "JPEG", quality=82, optimize=True, progressive=True)
    im.save(MEDIA / f"{slot}.webp", "WEBP", quality=80, method=5)
    return im.size


def main(only=None):
    credits = json.loads((MEDIA / "CREDITS.json").read_text())
    for slot, cats in SLOTS.items():
        if only and slot not in only:
            continue
        picked = None
        for cat in cats:
            for name in files_in(cat):
                try:
                    m = info(name)
                except Exception:
                    continue
                if not m or m["w"] < 1800 or m["w"] / m["h"] < 1.15:
                    continue
                if not FREE.search(m["lic"] or ""):
                    continue
                picked = (name, m); break
            if picked:
                break
        if not picked:
            print(f"  нет  {slot}: подходящего кадра не найдено", flush=True); continue
        name, m = picked
        try:
            w, h = grab(slot, name, m)
        except Exception as e:
            print(f"  нет  {slot}: {str(e)[:60]}", flush=True); continue
        credits[f"{slot}.jpg"] = {
            "title": name[5:].replace("_", " "), "license": m["lic"],
            "author": m["author"] or None,
            "source": f"{BASE}/wiki/{urllib.parse.quote(name)}",
        }
        print(f"  ok   {slot}: {m['w']}x{m['h']} -> {w}x{h}  {m['lic']}  {name[5:][:40]}", flush=True)
        (MEDIA / "CREDITS.json").write_text(json.dumps(credits, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(sys.argv[1:] or None)
