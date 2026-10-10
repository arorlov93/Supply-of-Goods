# -*- coding: utf-8 -*-
"""Сканер открытых закупок SAM.gov под товарные группы ISP GROUP LLC.

Работает через тот же поисковый эндпоинт, которым пользуется сайт SAM.gov,
поэтому ключ API не нужен.

Отбор сделан по кодам федеральной классификации товаров (PSC), а не по словам:
по словам в выдачу лезет стройка и услуги, а нам нужна поставка товара.
Берутся только два типа извещений, на которые можно подать прямо сейчас:
Solicitation и Combined Synopsis/Solicitation.

Запуск:  python3 sam-scan.py [мин_дней] [макс_дней]
Выгрузка: sourcing/sam-live.json плюс отчёт в консоль.
"""
import json, sys, time, urllib.parse, urllib.request, datetime, os

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
BASE = "https://sam.gov/api/prod/sgs/v1/search/"

# PSC это Product Service Code. Числовые группы это товар, буквенные услуги.
PSC = {
    "tools-hardware": ["5305", "5306", "5307", "5310", "5315", "5320", "5325",
                       "5340", "5345", "5350", "5110", "5120", "5130", "5133",
                       "5136", "5140", "5180", "5210", "5220"],
    "metals-pipe":    ["4710", "4720", "4730", "4810", "4820", "9510", "9515",
                       "9520", "9525", "9530", "9535", "9540", "9545"],
    "building-materials": ["5610", "5620", "5630", "5640", "5650", "5660",
                           "5670", "5675", "5680", "5450", "5410"],
    "industrial-equipment": ["4310", "4320", "4330", "6115", "6117", "4110",
                             "4120", "4130", "3930", "3950", "3990"],
    "paper-packaging": ["8115", "8125", "8135", "7510", "7520", "7530", "8540"],
    "food-agricultural": ["8905", "8910", "8915", "8920", "8925", "8930",
                          "8940", "8945", "8950", "8955", "8960", "8970"],
}

# Боевые системы и всё, что к ним крепится, не наша торговля.
BAD = ("ammunition", "missile", "warhead", "ordnance", "explosive", "flare",
       "countermeasure", "weapon", "torpedo", "grenade", "cartridge")

# Закупочные центры, которые покупают запчасти к технике по номерам NSN.
# Там действует одобренный источник и техдокументация, новой торговой
# компании там делать нечего, поэтому отсекаем их целиком.
NSN_OFFICES = ("NAVSUP", "DLA AVIATION", "DLA LAND", "DLA MARITIME", "DLA TROOP",
               "NUWC", "NSWC", "MSC ", "FLEET READINESS", "AFSC", "AFLCMC",
               "ACC-", "W6Q", "TACOM", "CECOM", "DEFENSE LOGISTICS",
               "DLA MECHANICSBURG", "SPRMM", "SPRRA", "SPRDL", "SPE",
               "COMMANDING OFFICER", "FA8", "FA5", "FA2", "NAVFAC", "NAVAIR")

# Признаки позиции по номеру NSN прямо в заголовке.
import re as _re
NSN_TITLE = _re.compile(
    r"(^\d{2}--)|(\bNSN\b)|(\bP/?N[: ])|(\bNIIN\b)|(,\s?[A-Z]{2,}\b.*,)")


def is_nsn(title, office):
    up = (office or "").upper()
    if any(k in up for k in NSN_OFFICES):
        return True
    return bool(NSN_TITLE.search(title or ""))


def fetch(psc, size=100, page=0):
    url = BASE + "?" + urllib.parse.urlencode({
        "random": int(time.time()), "index": "opp", "page": page,
        "mode": "search", "sort": "-modifiedDate", "size": size, "mfe": "true",
        "is_active": "true", "notice_type": "o,k", "psc": psc})
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept": "application/hal+json"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.load(r)


def val(x):
    return x.get("value") if isinstance(x, dict) else x


COMMERCIAL_ONLY = os.environ.get("ALL_ITEMS") != "1"


def main():
    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    today = datetime.date.today()
    out, seen = [], set()

    for group, codes in PSC.items():
        for code in codes:
            try:
                d = fetch(code)
            except Exception as e:
                print("!", code, e, flush=True)
                continue
            for r in (d.get("_embedded", {}) or {}).get("results", []) or []:
                nid = r.get("_id") or r.get("id")
                if not nid or nid in seen:
                    continue
                title = (r.get("title") or "").strip()
                if any(w in title.lower() for w in BAD):
                    continue
                dl = r.get("responseDateActual") or r.get("responseDate")
                days = None
                if dl:
                    try:
                        days = (datetime.date.fromisoformat(dl[:10]) - today).days
                    except Exception:
                        pass
                if days is None or not (lo <= days <= hi):
                    continue
                oh = r.get("organizationHierarchy") or []
                office = oh[-1].get("name", "") if len(oh) > 1 else ""
                if COMMERCIAL_ONLY and is_nsn(title, office):
                    continue
                seen.add(nid)
                out.append({
                    "group": group, "psc": code, "id": nid, "title": title,
                    "type": val(r.get("type")),
                    "agency": oh[0].get("name", "") if oh else "",
                    "office": office,
                    "deadline": dl, "days": days,
                    "setaside": val(r.get("typeOfSetAside")) or "unrestricted",
                    "naics": r.get("naics") or "",
                    "url": "https://sam.gov/opp/%s/view" % nid,
                })
            time.sleep(.25)

    out.sort(key=lambda x: x["days"])
    here = os.path.dirname(os.path.abspath(__file__))
    json.dump(out, open(os.path.join(here, "..", "sam-live.json"), "w"),
              ensure_ascii=False, indent=1)

    print("подать можно на:", len(out))
    for g in PSC:
        rows = [x for x in out if x["group"] == g]
        if not rows:
            continue
        print("\n== %s (%d)" % (g, len(rows)))
        for x in rows[:12]:
            print("  %3d дн  %-9s %-26s %s" % (
                x["days"], x["psc"], (x["office"] or x["agency"])[:26],
                x["title"][:66]))


if __name__ == "__main__":
    main()
