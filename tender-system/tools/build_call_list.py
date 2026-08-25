#!/usr/bin/env python3
"""Собрать звонковую таблицу тендеров из последнего SAM-скана: title/city/date/value/phone/contact.
Открывает каждый релевантный opp (v2 API) ради POC-телефона, города, дедлайна, стоимости."""
import json, os, glob, time, urllib.request, datetime, csv, sys

DISC = os.path.join(os.path.dirname(__file__), "..", "discovery")
REP = os.path.join(os.path.dirname(__file__), "..", "reports")
today = datetime.date.today()

# наши self-perform услуги (звоним как исполнитель) + supply
SERVICE_CATS = {"janitorial", "landscaping", "painting", "debris", "flooring"}
CAP = int(sys.argv[1]) if len(sys.argv) > 1 else 70

def latest_scan():
    files = sorted(glob.glob(os.path.join(DISC, "sam-2026-*.json")))
    return files[-1]

def opp_detail(oid):
    req = urllib.request.Request(f"https://sam.gov/api/prod/opps/v2/opportunities/{oid}",
                                 headers={"Accept": "application/hal+json"})
    d = json.load(urllib.request.urlopen(req, timeout=25)).get("data2", {})
    pop = d.get("placeOfPerformance", {}) or {}
    city = (pop.get("city", {}) or {}).get("name", "")
    st = (pop.get("state", {}) or {}).get("code", "")
    sol = d.get("solicitation", {}) or {}
    dl = (sol.get("deadlines", {}) or {}).get("response", "")
    if isinstance(dl, str) and "T" in dl: dl = dl[:10]
    sa = (sol.get("setAside", {}) or {}).get("value", "")
    award = d.get("award", {}) or {}
    val = award.get("amount", "") or ""
    pocs = d.get("pointOfContact", []) or []
    phone, name, email = "", "", ""
    for pc in pocs:
        if pc.get("phone"):
            phone = pc.get("phone", ""); name = pc.get("fullName", ""); email = pc.get("email", "")
            break
    if not phone and pocs:
        name = pocs[0].get("fullName", ""); email = pocs[0].get("email", "")
    return city, st, dl, sa, val, phone, name, email

def main():
    scan = latest_scan()
    opps = json.load(open(scan))
    # релевантные услуги + near-term дедлайн
    cand = []
    for o in opps:
        if not any(c in SERVICE_CATS for c in o.get("cats", [])): continue
        try: dd = datetime.date.fromisoformat(o["deadline"])
        except Exception: continue
        if today <= dd <= today + datetime.timedelta(days=60):
            cand.append(o)
    cand.sort(key=lambda x: x["deadline"])
    cand = cand[:CAP]
    rows = []
    for o in cand:
        try:
            city, st, dl, sa, val, phone, name, email = opp_detail(o["id"])
        except Exception:
            city = st = dl = sa = val = phone = name = email = ""
        rows.append({
            "Наименование конкурса": o["title"][:90],
            "Город": f"{city}, {st}".strip(", "),
            "Дата (дедлайн)": dl or o.get("deadline", ""),
            "Стоимость закупки": (f"${float(val):,.0f}" if str(val).replace('.','',1).isdigit() else ""),
            "Телефон": phone,
            "Контакт (имя/email)": f"{name} · {email}".strip(" ·"),
            "Set-aside": sa,
            "Категория": "/".join(o.get("cats", [])),
            "Источник": "SAM.gov",
            "Ссылка": o["link"],
        })
        time.sleep(0.15)
    # строки с других платформ (из наших отчётов — проверенные телефоны)
    platform = [
        ["Miami-Dade JLS — Janitorial & Landscaping (SBE пул)", "Miami, FL", "rolling (нужна SBE)", "right-sized задания", "305-375-3111", "Small Business Development · sbdcert@miamidade.gov", "SBE set-aside", "janitorial/landscaping", "Miami-Dade County", "miamidade.gov/global/strategic-procurement/janitorial-and-landscaping-services.page"],
        ["City of Tampa — Janitorial @ Water Engineering (recompete)", "Tampa, FL", "imminent", "$3,152,000 (инкумбент)", "813-274-8351", "City of Tampa Procurement (SLBE)", "SLBE set-aside", "janitorial", "OpenGov 25-P-00234", "procurement.opengov.com/portal/cityoftampa"],
        ["Early Learning Coalition Palm Beach — Janitorial", "West Palm Beach, FL", "recompete watch", "$25,000–$70,000/год", "561-514-3300", "ELC Palm Beach Procurement", "open", "janitorial", "BidNet ITB 26-100", "elcpalmbeach.org"],
        ["FSW College 26-02 — Painting/Pressure Cleaning JOC", "Fort Myers, FL", "проверить addendum", "JOC unit-price", "239-489-9089", "FSW Procurement Services", "open", "painting/pressure", "BidNet", "bidnetdirect.com/florida"],
        ["Broward County Public Schools — Grounds (7 зон)", "Fort Lauderdale, FL", "recompete watch", "$11,000,000 (всего)", "754-321-0505", "Broward Schools Procurement", "open", "landscaping", "RFP26-008 (DemandStar)", "browardschools.com"],
        ["City of Fort Lauderdale — Janitorial Citywide (rebid)", "Fort Lauderdale, FL", "recompete watch", "$500,000–$2,000,000", "954-828-5140", "City of Ft Lauderdale Procurement", "open", "janitorial", "BidNet opp #494", "bidnetdirect.com/florida"],
    ]
    fields = ["Наименование конкурса","Город","Дата (дедлайн)","Стоимость закупки","Телефон","Контакт (имя/email)","Set-aside","Категория","Источник","Ссылка"]
    for pr in platform:
        rows.append(dict(zip(fields, pr)))
    out = os.path.join(REP, f"call-list-{today.isoformat()}.csv")
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    withphone = sum(1 for r in rows if r["Телефон"])
    print(f"scan={os.path.basename(scan)} · SAM opps opened={len(cand)} · platform rows={len(platform)} · total={len(rows)} · с телефоном={withphone}")
    print("wrote", out)

if __name__ == "__main__":
    main()
