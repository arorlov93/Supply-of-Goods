# -*- coding: utf-8 -*-
"""Поиск чистых поставок по SAM.gov: привёз и всё.

Отличие от sam-scan.py: здесь не наши шесть товарных групп, а все товарные
классы федеральной классификации, и жёсткий отсев всего, что требует работ на
месте. Нужна закупка, где обязанность поставщика заканчивается на выгрузке.

Запуск:  python3 sam-supply.py [мин_дней] [макс_дней]
Выгрузка: sourcing/sam-supply.json
"""
import json, sys, time, urllib.parse, urllib.request, datetime, os, re

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
BASE = "https://sam.gov/api/prod/sgs/v1/search/"
DET = "https://sam.gov/api/prod/opps/v2/opportunities/%s?random=1"

# Все товарные классы, которые торговая компания может привезти.
# Оружие, боеприпасы, суда, самолёты, топливо и живые животные пропущены.
GROUPS = {
    "машины и оборудование": ["34", "35", "36", "37", "38", "39", "30", "31"],
    "трубы, клапаны, насосы": ["47", "48", "43", "44", "45", "46", "40"],
    "холод и климат":        ["41", "42"],
    "инструмент":            ["51", "52", "49"],
    "крепёж и скобяное":     ["53"],
    "стройматериалы":        ["54", "55", "56"],
    "электрика и свет":      ["59", "61", "62", "63", "58"],
    "мебель и быт":          ["71", "72", "73", "74"],
    "канцелярия и бумага":   ["75", "76"],
    "уборка и химия":        ["79", "80", "68"],
    "упаковка и тара":       ["81"],
    "текстиль и одежда":     ["83", "84"],
    "гигиена":               ["85"],
    "продовольствие":        ["89", "87"],
    "металл и прокат":       ["95", "93", "94"],
    "прочее":                ["99", "66", "67", "69", "78"],
}

# Закупочные центры, которые покупают запчасти по номерам NSN от одобренных
# источников. Новой торговой компании там нечего делать.
NSN_OFFICES = ("NAVSUP", "DLA AVIATION", "DLA LAND", "DLA MARITIME", "NUWC",
               "NSWC", "MSC ", "FLEET READINESS", "AFSC", "AFLCMC", "TACOM",
               "CECOM", "DLA MECHANICSBURG", "SPRMM", "SPRDL", "NAVAIR",
               "DEFENSE MICROELECTRONICS")
NSN_TITLE = re.compile(r"(^\d{2}--)|(\bNSN\b)|(\bP/?N[: ])|(\bNIIN\b)")

# Всё, что означает работы на месте или услугу, а не привоз товара.
NOT_SUPPLY = (
    "install", "installation", "service", "services", "maintenance", "repair",
    "overhaul", "construction", "renovation", "remodel", "replacement of",
    "removal", "demolition", "design", "design-build", "idiq construction",
    "inspection", "testing service", "calibration", "training", "support",
    "rental", "lease", "study", "survey", "audit", "cleaning", "janitorial",
    "laundry", "catering", "meal support", "disposal", "recycling", "haul",
    "upgrade", "retrofit", "refurbish", "sources sought", "industry day",
    "request for information", "rfi ", "market research",
)

# Боевое и то, что мы не возим принципиально.
BAD = ("ammunition", "missile", "warhead", "ordnance", "explosive", "flare",
       "countermeasure", "weapon", "torpedo", "grenade", "cartridge", "armor",
       "ballistic", "drone", "narcotic")


def fetch(psc, page=0):
    url = BASE + "?" + urllib.parse.urlencode({
        "random": int(time.time()), "index": "opp", "page": page,
        "mode": "search", "sort": "-modifiedDate", "size": 100, "mfe": "true",
        "is_active": "true", "notice_type": "o,k", "psc": psc})
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept": "application/hal+json"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.load(r)


def detail(nid):
    req = urllib.request.Request(DET % nid, headers={
        "User-Agent": UA, "Accept": "application/hal+json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r).get("data2", {})


def val(x):
    return x.get("value") if isinstance(x, dict) else x


def main():
    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    today = datetime.date.today()
    out, seen = [], set()

    for group, codes in GROUPS.items():
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
                low = title.lower()
                if any(w in low for w in BAD) or any(w in low for w in NOT_SUPPLY):
                    continue
                if NSN_TITLE.search(title):
                    continue
                oh = r.get("organizationHierarchy") or []
                office = oh[-1].get("name", "") if len(oh) > 1 else ""
                if any(k in office.upper() for k in NSN_OFFICES):
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
                seen.add(nid)
                out.append({
                    "group": group, "psc": code, "id": nid, "title": title,
                    "agency": oh[0].get("name", "") if oh else "",
                    "office": office, "deadline": dl, "days": days,
                    "url": "https://sam.gov/opp/%s/view" % nid})
            time.sleep(.25)

    # подробности только по отобранным: там видно резерв, место и контакт
    for x in out:
        try:
            d2 = detail(x["id"])
            s = d2.get("solicitation") or {}
            pl = d2.get("placeOfPerformance") or {}
            x["setaside"] = s.get("setAside") or "нет"
            x["state"] = ((pl.get("state") or {}).get("code") or "")
            x["city"] = ((pl.get("city") or {}).get("name") or "")
            x["number"] = d2.get("solicitationNumber") or ""
            x["naics"] = [c.get("code") for c in (d2.get("naics") or [])]
            x["poc"] = [c.get("email") for c in (d2.get("pointOfContact") or [])
                        if c.get("email")][:2]
        except Exception:
            pass
        time.sleep(.12)

    out.sort(key=lambda z: z["days"])
    here = os.path.dirname(os.path.abspath(__file__))
    json.dump(out, open(os.path.join(here, "..", "sam-supply.json"), "w"),
              ensure_ascii=False, indent=1)

    print("чистых поставок:", len(out), "\n")
    for g in GROUPS:
        rows = [x for x in out if x["group"] == g]
        if not rows:
            continue
        print("== %s (%d)" % (g, len(rows)))
        for x in rows:
            print("  %3d дн %-2s %-7s %-26s %s" % (
                x["days"], x.get("state", ""), x.get("setaside", "")[:7],
                (x["office"] or x["agency"])[:26], x["title"][:62]))
        print()


if __name__ == "__main__":
    main()
