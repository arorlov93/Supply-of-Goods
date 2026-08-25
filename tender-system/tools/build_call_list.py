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
    # Строки с других платформ — телефоны ВЕРИФИЦИРОВАНЫ по официальным .gov/.edu (25.08.2026).
    # (a) КОНКРЕТНЫЕ ТЕНДЕРЫ с известной стоимостью/контактом:
    platform = [
        ["ТЕНДЕР: Miami-Dade JLS — Janitorial & Landscaping (SBE пул)", "Miami, FL", "rolling — нужна SBE-серт.", "right-sized задания (пул)", "305-375-1939", "Small Business Development · sbdcert@miamidade.gov", "SBE set-aside", "janitorial/landscaping", "Miami-Dade SPD", "miamidade.gov/global/strategic-procurement/janitorial-and-landscaping-services.page"],
        ["ТЕНДЕР: City of Tampa — Janitorial @ Water Eng. (recompete)", "Tampa, FL", "имминентно", "$3,152,000 (инкумбент)", "813-274-8351", "Buyer Eryn Berg (Water Dept) — SLBE-restricted", "SLBE set-aside", "janitorial", "OpenGov 25-P-00234", "procurement.opengov.com/portal/cityoftampa"],
        ["ТЕНДЕР: FSW College 26-02 — Painting/Pressure JOC", "Fort Myers, FL", "проверить addendum на BidNet", "JOC unit-price", "239-489-9256", "FSW Procurement · purchasing@fsw.edu · Dir. R.Pence 239-489-9102", "open", "painting/pressure", "BidNet / fsw.edu/procurement", "fsw.edu/procurement"],
        ["ТЕНДЕР: Early Learning Coalition PBC — Janitorial", "West Palm Beach, FL", "recompete watch", "$25,000–$70,000/год", "561-214-8000", "ELC PBC Admin — контакт брать из конкретного RFP", "open", "janitorial", "BidNet ITB 26-100", "elcpalmbeach.org/procurement"],
        ["ТЕНДЕР: Broward Schools — Grounds Maintenance (7 зон)", "Fort Lauderdale, FL", "recompete watch (до 2028)", "$11,000,000 (всего, ~$3.6M/год)", "754-321-0505", "Broward Schools Procurement · PurchasingHelpdesk@browardschools.com", "open (по зонам)", "landscaping", "RFP26-008 (DemandStar)", "browardschools.com/bcps-departments/procurement"],
        # (b) ЗВОНКИ В ЗАКУПКИ — регистрация вендора + узнать про будущие клининг/grounds биды:
        ["ЗВОНОК: Miami-Dade County — Strategic Procurement", "Miami, FL", "постоянно (регистрация вендора)", "—", "305-375-5773", "Vendor Outreach 305-375-4252 · Small Biz 305-375-1939", "—", "все категории", "Miami-Dade SPD", "miamidade.gov/global/strategic-procurement/contact.page"],
        ["ЗВОНОК: Miami-Dade County Public Schools — Procurement", "Miami, FL", "постоянно", "—", "305-995-4288", "M-DCPS Procurement Mgmt Svcs (also 305-995-7254)", "—", "janitorial/grounds", "M-DCPS", "procurement.dadeschools.net"],
        ["ЗВОНОК: Broward County — Purchasing Division", "Fort Lauderdale, FL", "постоянно", "—", "954-357-6066", "Broward County Purchasing", "—", "все категории", "Broward County", "broward.org/Purchasing"],
        ["ЗВОНОК: Palm Beach County — Purchasing", "West Palm Beach, FL", "постоянно", "—", "561-616-6800", "PBC Purchasing · purchase@pbcgov.org", "—", "все категории", "Palm Beach County", "discover.pbc.gov/procurement"],
        ["ЗВОНОК: School District of Palm Beach County — Purchasing", "West Palm Beach, FL", "постоянно", "—", "561-434-8214", "PBC Schools Purchasing", "—", "janitorial/grounds", "PBC Schools", "palmbeachschools.org/departments/purchasing"],
        ["ЗВОНОК: City of Miami — Procurement", "Miami, FL", "постоянно", "—", "305-416-1922", "City of Miami Procurement (iSupplier портал)", "—", "все категории", "City of Miami", "miami.gov"],
        ["ЗВОНОК: City of Miami Beach — Procurement", "Miami Beach, FL", "постоянно", "—", "305-673-7490", "procurement@miamibeachfl.gov", "—", "все категории", "City of Miami Beach", "miamibeachfl.gov/city-hall/procurement"],
        ["ЗВОНОК: City of Fort Lauderdale — Procurement Services", "Fort Lauderdale, FL", "постоянно", "—", "954-828-5933", "purchase@fortlauderdale.gov · CPO G.Marcos 954-828-5677", "—", "все категории", "City of Ft Lauderdale", "fortlauderdale.gov/government/departments-i-z/procurement-services"],
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
