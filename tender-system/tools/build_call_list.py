#!/usr/bin/env python3
"""Звонковая таблица тендеров/контактов (приоритет Флорида).
Источники: SAM.gov (POC-телефон/город/дата/стоимость/описание) + FL local procurement (проверенные .gov
телефоны) + FL-подрядчики из пермитов Miami-Dade (телефон+объект → звонок на final-clean суб)."""
import json, os, glob, time, urllib.request, datetime, csv, sys, re as _re

DISC = os.path.join(os.path.dirname(__file__), "..", "discovery")
REP = os.path.join(os.path.dirname(__file__), "..", "reports")
today = datetime.date.today()
SERVICE_CATS = {"janitorial", "landscaping", "painting", "debris", "flooring"}
CAP = int(sys.argv[1]) if len(sys.argv) > 1 else 70

FIELDS = ["Наименование конкурса", "Краткое описание", "Город", "Дата (дедлайн)", "Стоимость закупки",
          "Где искать стоимость", "Телефон", "Контакт (имя/email)", "Set-aside", "Категория", "Источник", "Ссылка"]

def prow(*vals):
    return dict(zip(FIELDS, vals))

def _striphtml(s):
    if isinstance(s, dict): s = s.get("body", "") or ""
    if not isinstance(s, str): return ""
    s = _re.sub(r"<[^>]+>", " ", s)
    s = _re.sub(r"&nbsp;|&amp;|&rsquo;|&ldquo;|&rdquo;|&#39;", " ", s)
    return _re.sub(r"\s+", " ", s).strip()

def latest_scan():
    return sorted(glob.glob(os.path.join(DISC, "sam-2026-*.json")))[-1]

def opp_detail(oid):
    req = urllib.request.Request(f"https://sam.gov/api/prod/opps/v2/opportunities/{oid}",
                                 headers={"Accept": "application/hal+json"})
    full = json.load(urllib.request.urlopen(req, timeout=25))
    d = full.get("data2", {}) or {}
    pop = d.get("placeOfPerformance", {}) or {}
    city = (pop.get("city", {}) or {}).get("name", "")
    st = (pop.get("state", {}) or {}).get("code", "")
    sol = d.get("solicitation", {}) or {}
    dl = (sol.get("deadlines", {}) or {}).get("response", "")
    if isinstance(dl, str) and "T" in dl: dl = dl[:10]
    sa = (sol.get("setAside", {}) or {}).get("value", "")
    val = (d.get("award", {}) or {}).get("amount", "") or ""
    phone = name = email = ""
    for pc in (d.get("pointOfContact", []) or []):
        if not name: name = pc.get("fullName", "") or ""
        if not email: email = pc.get("email", "") or ""
        ph = (pc.get("phone", "") or "").strip()
        if ph and not phone: phone = ph
    desc = _striphtml(full.get("description", ""))[:150]
    return city, st, dl, sa, val, phone, name, email, desc

def main():
    scan = latest_scan()
    opps = json.load(open(scan))
    cand = []
    for o in opps:
        if not any(c in SERVICE_CATS for c in o.get("cats", [])): continue
        try: dd = datetime.date.fromisoformat(o["deadline"])
        except Exception: continue
        if today <= dd <= today + datetime.timedelta(days=60):
            cand.append(o)
    cand.sort(key=lambda x: x["deadline"])
    cand = cand[:CAP]

    SAM_HINT = ("В пакете солиситейшена (SOW/прайс-лист, кол-во/NTE) · award ceiling в opp · "
                "история USASpending по агентству+NAICS · спросить у CO")
    rows = []
    for o in cand:
        try:
            city, st, dl, sa, val, phone, name, email, desc = opp_detail(o["id"])
        except Exception:
            city = st = dl = sa = val = phone = name = email = desc = ""
        has = str(val).replace('.', '', 1).isdigit()
        rows.append(prow(o["title"][:90], desc, f"{city}, {st}".strip(", "), dl or o.get("deadline", ""),
                         (f"${float(val):,.0f}" if has else ""), ("" if has else SAM_HINT),
                         phone, f"{name} · {email}".strip(" ·"), sa, "/".join(o.get("cats", [])),
                         "SAM.gov", o["link"]))
        time.sleep(0.15)

    ASK = "Спросить про бюджет ближайших клининг/grounds-контрактов"
    platform = [
        prow("ТЕНДЕР: Miami-Dade JLS — Janitorial & Landscaping (SBE пул)", "Округ отдаёт клининг/grounds задания сертифицированным SBE-фирмам", "Miami, FL", "rolling — нужна SBE-серт.", "right-sized задания", "Размер task order спросить у SBD; порядок сумм — в прошлых JLS-award", "305-375-1939", "Small Business Development · sbdcert@miamidade.gov", "SBE set-aside", "janitorial/landscaping", "Miami-Dade SPD", "miamidade.gov/global/strategic-procurement/janitorial-and-landscaping-services.page"),
        prow("ТЕНДЕР: City of Tampa — Janitorial @ Water Eng.", "Уборка Water Engineering; перевыпуск (инкумбент истекает)", "Tampa, FL", "имминентно", "$3,152,000 (инкумбент)", "", "813-274-8351", "Buyer Eryn Berg (Water Dept) — SLBE-restricted", "SLBE set-aside", "janitorial", "OpenGov 25-P-00234", "procurement.opengov.com/portal/cityoftampa"),
        prow("ТЕНДЕР: FSW College 26-02 — Painting/Pressure JOC", "Job-order покраска и pressure cleaning по кампусам FSW", "Fort Myers, FL", "проверить addendum (BidNet)", "JOC unit-price", "Unit-price форма в пакете BidNet; спросить Procurement", "239-489-9256", "FSW Procurement · purchasing@fsw.edu · Dir. 239-489-9102", "open", "painting/pressure", "BidNet / fsw.edu", "fsw.edu/procurement"),
        prow("ТЕНДЕР: Early Learning Coalition PBC — Janitorial", "Уборка 2 объектов ~18,500 SF (daily + monthly deep clean)", "West Palm Beach, FL", "recompete watch", "$25,000–$70,000/год", "", "561-214-8000", "ELC PBC Admin — контакт из конкретного RFP", "open", "janitorial", "BidNet ITB 26-100", "elcpalmbeach.org/procurement"),
        prow("ТЕНДЕР: Broward Schools — Grounds Maintenance (7 зон)", "Кошение/обрезка/удобрение по 7 зонам; можно бид на 1 зону", "Fort Lauderdale, FL", "recompete watch (до 2028)", "$11,000,000 (всего, ~$3.6M/год)", "", "754-321-0505", "Broward Schools Procurement · PurchasingHelpdesk@browardschools.com", "open (по зонам)", "landscaping", "RFP26-008 (DemandStar)", "browardschools.com/bcps-departments/procurement"),
        prow("ЗВОНОК: Miami-Dade County — Strategic Procurement", "Регистрация вендора; узнать будущие janitorial/grounds биды", "Miami, FL", "постоянно", "—", ASK, "305-375-5773", "Vendor Outreach 305-375-4252 · Small Biz 305-375-1939", "—", "все категории", "Miami-Dade SPD", "miamidade.gov/global/strategic-procurement/contact.page"),
        prow("ЗВОНОК: Miami-Dade County Public Schools — Procurement", "Регистрация вендора; custodial/grounds по школам", "Miami, FL", "постоянно", "—", ASK, "305-995-4288", "M-DCPS Procurement (also 305-995-7254)", "—", "janitorial/grounds", "M-DCPS", "procurement.dadeschools.net"),
        prow("ЗВОНОК: Broward County — Purchasing Division", "Регистрация вендора; клининг/grounds по объектам округа", "Fort Lauderdale, FL", "постоянно", "—", ASK, "954-357-6066", "Broward County Purchasing", "—", "все категории", "Broward County", "broward.org/Purchasing"),
        prow("ЗВОНОК: Palm Beach County — Purchasing", "Регистрация вендора; клининг/grounds по округу", "West Palm Beach, FL", "постоянно", "—", ASK, "561-616-6800", "PBC Purchasing · purchase@pbcgov.org", "—", "все категории", "Palm Beach County", "discover.pbc.gov/procurement"),
        prow("ЗВОНОК: School District of Palm Beach County — Purchasing", "Custodial/grounds биды по школам PBC", "West Palm Beach, FL", "постоянно", "—", ASK, "561-434-8214", "PBC Schools Purchasing", "—", "janitorial/grounds", "PBC Schools", "palmbeachschools.org/departments/purchasing"),
        prow("ЗВОНОК: City of Miami — Procurement", "Регистрация в iSupplier; клининг по объектам города", "Miami, FL", "постоянно", "—", ASK, "305-416-1922", "City of Miami Procurement (iSupplier)", "—", "все категории", "City of Miami", "miami.gov"),
        prow("ЗВОНОК: City of Miami Beach — Procurement", "Регистрация вендора; клининг/pressure по городу", "Miami Beach, FL", "постоянно", "—", ASK, "305-673-7490", "procurement@miamibeachfl.gov", "—", "все категории", "City of Miami Beach", "miamibeachfl.gov/city-hall/procurement"),
        prow("ЗВОНОК: City of Fort Lauderdale — Procurement Services", "Регистрация вендора; клининг по городу", "Fort Lauderdale, FL", "постоянно", "—", ASK, "954-828-5933", "purchase@fortlauderdale.gov · CPO 954-828-5677", "—", "все категории", "City of Ft Lauderdale", "fortlauderdale.gov"),
    ]
    rows += platform

    # Доп. FL-агентства (проверено агентом 25.08). (v)=verified live, (i)=из индекса .gov — проверить перед обзвоном.
    # tuple: (имя, описание, город, телефон, контакт, портал/источник)
    fl2 = [
        ("City of Hialeah — Purchasing", "Регистрация вендора; клининг по городу", "Hialeah, FL", "305-883-5865", "Purchasing@hialeahfl.gov", "OpenGov"),
        ("City of Coral Gables — Procurement", "Регистрация; клининг/grounds", "Coral Gables, FL", "305-460-5102", "procurement@coralgables.com", "Public Purchase"),
        ("City of Homestead — Procurement", "Регистрация вендора", "Homestead, FL", "305-224-4620", "vendors@homesteadfl.gov", "OpenGov"),
        ("City of Aventura — Purchasing", "Регистрация вендора (наш город HQ)", "Aventura, FL", "305-466-8925", "—", "DemandStar"),
        ("City of Pembroke Pines — Procurement", "Регистрация; клининг по городу", "Pembroke Pines, FL", "954-518-9020", "purchasing@ppines.com", "OpenGov"),
        ("City of Hollywood — Procurement", "Регистрация вендора", "Hollywood, FL", "954-921-3299", "Sstewart@hollywoodfl.org", "OpenGov"),
        ("City of Pompano Beach — Procurement", "Регистрация вендора", "Pompano Beach, FL", "954-786-4098", "purchasing@copbfl.com", "OpenGov"),
        ("City of Boca Raton — Purchasing", "Регистрация в supplier-портале", "Boca Raton, FL", "561-393-7871", "online supplier reg", "Own portal"),
        ("FIU — Procurement Services", "Крупный кампус — janitorial/grounds спрос", "Miami, FL", "305-348-2161", "vendors@fiu.edu", "PantherSoft / bids.fiu.edu"),
        ("Miami Dade College — Purchasing", "Много кампусов — клининг", "Miami, FL", "305-237-2402", "purchasing@mdc.edu", "eSupplier + BidNet"),
        ("Broward College — Procurement", "Кампусы — janitorial/grounds", "Fort Lauderdale, FL", "954-201-7350", "procurement@broward.edu", "Euna OpenBids + MFMP"),
        ("University of Miami — Supply Chain", "Частный универ; крупный кампус", "Coral Gables, FL", "305-284-5751", "—", "Jaggaer"),
        ("Jackson Health System — Procurement", "Крупная больничная сеть — клининг", "Miami, FL", "305-585-7333", "Procurement.Services@jhsmiami.org", "Infor Supplier Portal"),
        ("Miami-Dade Vendor Services (Port/MIA/Transit/WASD)", "Одна регистрация на порт, аэропорт, транзит, воду", "Miami, FL", "305-375-5773", "DTPW 786-469-5225 · WASD 305-665-7477", "INFORMS"),
        ("South Florida Water Management District — Procurement", "Клининг/grounds по объектам district", "West Palm Beach, FL", "561-682-2011", "CMDM@sfwmd.gov", "Own portal"),
        ("City of Sunrise — Purchasing (проверить номер)", "Регистрация вендора", "Sunrise, FL", "954-572-2274 (проверить)", "Purchasing@sunrisefl.gov", "DemandStar"),
        ("City of West Palm Beach — Procurement (проверить)", "Регистрация вендора", "West Palm Beach, FL", "561-822-2100 (проверить)", "Procurement@wpb.org", "DemandStar"),
        ("City of Coral Springs — Purchasing (проверить)", "Регистрация вендора", "Coral Springs, FL", "954-344-1101 (проверить)", "LBermudez@coralsprings.gov", "OpenGov/DemandStar"),
        ("City of Miramar — Procurement (проверить)", "Регистрация вендора", "Miramar, FL", "954-602-3311 (проверить)", "procurementdept@miramarfl.gov", "DemandStar"),
        ("Nova Southeastern University — Procurement (проверить)", "Частный универ; кампус Davie", "Davie, FL", "954-262-8841 (проверить)", "purchasing@nova.edu", "SAP Ariba + DemandStar"),
        ("Broward Health — Vendor Relations (проверить)", "Больничная сеть — клининг", "Fort Lauderdale, FL", "954-473-7289 (проверить)", "vendorrelations@browardhealth.org", "Own VRS portal"),
        ("City of Doral — Procurement (без звонков)", "Телефон не принимают — только email/портал", "Doral, FL", "", "procurement@cityofdoral.com", "Own + DemandStar"),
        ("Palm Beach State College — Purchasing (без звонков)", "Телефон по закупкам не принимают — email/портал", "Lake Worth, FL", "", "purchasing@pbsc.edu", "DemandStar"),
        ("Memorial Healthcare System — Supply Chain (email/портал)", "Больничная сеть; Facilities 954-265-8670", "Hollywood, FL", "954-265-8670", "vendorinquiry@mhs.net (Facilities line)", "DemandStar"),
    ]
    for nm, ds, ci, ph, ct, portal in fl2:
        rows.append(prow(f"ЗВОНОК: {nm}", ds, ci, "постоянно", "—", ASK, ph, ct, "—", "все категории", portal, ""))

    # FL-подрядчики из пермитов Miami-Dade (телефон+объект) → звонок на final-clean суб
    mdc = os.path.join(os.path.dirname(__file__), "..", "outreach", "mdc-2026-08", "recipients.csv")
    gc = 0
    if os.path.exists(mdc):
        seen = set()
        for r in csv.DictReader(open(mdc)):
            ph = (r.get("phone", "") or "").strip()
            if not ph or ph in seen: continue
            if r.get("status", "") in ("SKIP_COMPETITOR", "SKIP_NATIONAL", "OPTED_OUT"): continue
            seen.add(ph)
            pv = (r.get("project_value", "") or r.get("total_value", "") or "").strip()
            try: pvs = f"${float(pv):,.0f} (объект)" if pv else ""
            except Exception: pvs = ""
            rows.append(prow(
                f"GC (final-clean суб): {r.get('contractor','')[:50]}",
                f"Активный объект: {(r.get('project_addr','') or '').strip()} · {r.get('services','')}".strip(" ·"),
                f"{r.get('city','')}, FL".strip(", "), "по графику закрытия объекта", pvs,
                "Уборку считаем от площади объекта — спросить GC метраж/срок сдачи",
                ph, r.get("email", "") if "@" in (r.get("email", "") or "") else "",
                "—", "final-clean sub", "Miami-Dade permits", ""))
            gc += 1

    out = os.path.join(REP, f"call-list-{today.isoformat()}.csv")
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    wp = sum(1 for r in rows if r["Телефон"])
    print(f"scan={os.path.basename(scan)} · SAM={len(cand)} · platform={len(platform)} · GC-permits={gc} · total={len(rows)} · с телефоном={wp}")
    print("wrote", out)

if __name__ == "__main__":
    main()
