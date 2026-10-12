# -*- coding: utf-8 -*-
"""Полный обход закупок SAM.gov. Замена sam-scan.py и sam-supply.py.

Чем отличается от прежних сканеров, которые показывали 94 закупки вместо
двадцати двух тысяч:

1. ПАГИНАЦИЯ. Прежние читали только первую страницу по 100 записей на код
   PSC. В группе 53 их 2465, то есть видно было четыре процента.
2. СЛОВА-УБИЙЦЫ УБРАНЫ. Прежний фильтр выбрасывал всё, где в заголовке есть
   support, service, installation и ещё тридцать слов. Это резало законные
   поставки пачками.
3. ЗАКУПОЧНЫЕ ЦЕНТРЫ НЕ ВЫРЕЗАЮТСЯ ЦЕЛИКОМ. Прежний выбрасывал NAVSUP, DLA
   и прочих вместе со всем, что они покупают. Теперь они только помечаются.
4. ВСЕ ТОВАРНЫЕ ГРУППЫ, а не выбранные руками.
5. РЕЗЕРВ НЕ ФИЛЬТРУЕТСЯ НА ИНДЕКСЕ. В поисковом индексе поля резерва нет
   вообще, прежний фильтр просто ничего не делал. Резерв берётся из
   карточки на втором проходе.

Запуск:  python3 sam-full.py [мин_дней] [макс_дней] [группы через запятую]
Пример:  python3 sam-full.py 5 45 47,53,56,95
Выгрузка: sourcing/sam-full.json
"""
import datetime, json, os, re, sys, time, urllib.parse, urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
BASE = "https://sam.gov/api/prod/sgs/v1/search/"
DET = "https://sam.gov/api/prod/opps/v2/opportunities/%s?random=1"
HDR = {"User-Agent": UA, "Accept": "application/hal+json"}

# Все товарные классы. Оружие и боеприпасы исключены принципиально.
GROUPS = {
    "крепёж и скобяное": ["53"], "трубы и клапаны": ["47", "48"],
    "насосы и компрессоры": ["43"], "холод и климат": ["41"],
    "пожарное и спасательное": ["42"], "сантехника и вода": ["45", "46"],
    "стройматериалы": ["56", "54", "55"], "металлопрокат": ["95", "93", "94"],
    "погрузка и хранение": ["39", "40"], "инструмент": ["51", "52"],
    "освещение и сигнализация": ["62", "63"], "электрика": ["61", "59", "60"],
    "мебель": ["71", "72"], "кухня и общепит": ["73"],
    "канцелярия и книги": ["75", "76"], "уборка и химия": ["79", "80", "68"],
    "тара и упаковка": ["81"], "текстиль и одежда": ["83", "84"],
    "гигиена": ["85"], "продовольствие": ["89", "87"],
    "медицина и лаборатория": ["65", "66"], "спорт и досуг": ["77", "78"],
    "машины и оборудование": ["34", "35", "36", "37", "38", "30"],
    "прочее": ["99", "67", "69", "70", "74", "91", "96"],
}

# Только то, что мы не возим принципиально. Ничего про услуги: услуги
# отсеиваются типом извещения и проверкой карточки, а не словами в названии.
BAD = ("missile", "warhead", "ordnance", "explosive", "grenade", "torpedo",
       "ammunition", "cartridge", "detonator", "propellant")

# Закупка запчасти по номеру NSN: не отбрасываем, а помечаем.
NSN_TITLE = re.compile(r"(^\d{2}--)|(\bNSN\b)|(\bP/?N[: ])|(\bNIIN\b)")
NSN_OFFICE = ("NAVSUP", "DLA AVIATION", "DLA LAND", "DLA MARITIME", "NUWC",
              "NSWC", "FLEET READINESS", "AFSC", "AFLCMC", "TACOM", "CECOM",
              "DLA MECHANICSBURG", "SPRMM", "SPRDL", "NAVAIR", "DLA TROOP")


def page(psc, pg, size=100):
    url = BASE + "?" + urllib.parse.urlencode({
        "random": int(time.time()), "index": "opp", "page": pg,
        "mode": "search", "sort": "-modifiedDate", "size": size, "mfe": "true",
        "is_active": "true", "notice_type": "o,k", "psc": psc})
    with urllib.request.urlopen(urllib.request.Request(url, headers=HDR),
                                timeout=60) as r:
        return json.load(r)


def detail(nid):
    with urllib.request.urlopen(
            urllib.request.Request(DET % nid, headers=HDR), timeout=30) as r:
        return json.load(r).get("data2", {}) or {}


def main():
    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 45
    only = set(sys.argv[3].split(",")) if len(sys.argv) > 3 else None
    today = datetime.date.today()
    out, seen = [], set()
    scanned = 0

    for group, codes in GROUPS.items():
        for code in codes:
            if only and code not in only:
                continue
            pg, total = 0, None
            while True:
                try:
                    d = page(code, pg)
                except Exception as e:
                    print("! psc %s стр %d %s" % (code, pg, e), flush=True)
                    break
                if total is None:
                    total = d.get("page", {}).get("totalElements", 0)
                rows = (d.get("_embedded") or {}).get("results") or []
                if not rows:
                    break
                scanned += len(rows)
                for r in rows:
                    nid = r.get("_id") or r.get("id")
                    if not nid or nid in seen:
                        continue
                    title = (r.get("title") or "").strip()
                    if any(w in title.lower() for w in BAD):
                        continue
                    dl = r.get("responseDateActual") or r.get("responseDate")
                    if not dl:
                        continue
                    try:
                        days = (datetime.date.fromisoformat(dl[:10]) - today).days
                    except Exception:
                        continue
                    if not (lo <= days <= hi):
                        continue
                    oh = r.get("organizationHierarchy") or []
                    office = oh[-1].get("name", "") if len(oh) > 1 else ""
                    seen.add(nid)
                    out.append({
                        "group": group, "psc": code, "id": nid, "title": title,
                        "agency": oh[0].get("name", "") if oh else "",
                        "office": office, "deadline": dl, "days": days,
                        "nsn": bool(NSN_TITLE.search(title)) or
                              any(k in office.upper() for k in NSN_OFFICE),
                        "number": r.get("solicitationNumber") or "",
                        "url": "https://sam.gov/opp/%s/view" % nid})
                pg += 1
                if pg * 100 >= (total or 0):
                    break
                time.sleep(.15)
            print("  psc %-3s всего %-6s в окне %d" % (
                code, total, sum(1 for x in out if x["psc"] == code)), flush=True)

    # карточки только по отобранным: там резерв, место и контакт
    for i, x in enumerate(out):
        try:
            d2 = detail(x["id"])
            s = d2.get("solicitation") or {}
            pl = d2.get("placeOfPerformance") or {}
            x["setaside"] = s.get("setAside") or "нет"
            x["state"] = ((pl.get("state") or {}).get("code") or "")
            x["city"] = ((pl.get("city") or {}).get("name") or "")
            x["naics"] = [c.get("code") for c in (d2.get("naics") or [])]
            x["poc"] = [c.get("email") for c in (d2.get("pointOfContact") or [])
                        if c.get("email")][:2]
        except Exception:
            x["setaside"] = "?"
        if i % 50 == 0:
            print("    карточки %d/%d" % (i, len(out)), flush=True)
        time.sleep(.1)

    out.sort(key=lambda z: z["days"])
    here = os.path.dirname(os.path.abspath(__file__))
    json.dump(out, open(os.path.join(here, "..", "sam-full.json"), "w"),
              ensure_ascii=False, indent=1)
    print("\nпросмотрено записей: %d" % scanned)
    print("в окне %d до %d дней: %d" % (lo, hi, len(out)))
    print("из них не по номеру NSN: %d" % sum(1 for x in out if not x["nsn"]))


if __name__ == "__main__":
    main()
