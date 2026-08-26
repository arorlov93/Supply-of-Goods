#!/usr/bin/env python3
"""ИТОГОВЫЙ документ обзвона — 3 вкладки под направления:
  P1 ОТДЕЛКА (покраска+гипсокартон+полы) · P2 УБОРКА (final clean) · P3 ДЕМОНТАЖ.
Miami-Dade RER, активные (CO нет), свежесть ≤180д, телефон подрядчика. + веб-сверка топ-45 P1."""
import json, os, re, datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

SP = "/tmp/claude-0/-home-user-Supply-of-Goods/4f5e4e6d-222f-57da-93ad-94f5b2132f9f/scratchpad"
TODAY = datetime.date(2026, 8, 26)
TARGET = {
    "RETAIL SALES": "Ритейл", "OFFICE - PROFESSIONAL BUILDINGS": "Офис", "OFFICE USE ONLY": "Офис",
    "OFFICE - SALES": "Офис", "RESTAURANT-CAFETERIA": "Ресторан",
    "RESTAURANT/CAFET/BAR/LOUNGE/NIGHT CLUB": "Ресторан/бар", "BAR/COCKTAIL LOUNGE/RESTAURANTS": "Ресторан/бар",
    "BAR-LOUNGE-NIGHT CLUB": "Бар", "BAKERY PLANT": "Пекарня", "BANQUET HALL": "Банкетный зал",
    "CONVENIENCE STORE": "Магазин у дома", "PACKAGE STORE": "Ликёр-магазин",
    "CLINIC/SANITARIUMS/HEALTH CENTERS": "Клиника", "BEAUTY SALON-BARBER SHOP": "Салон/барбершоп",
    "GYM/EXERCISE CLUB": "Спортзал", "COIN LAUNDRY-DRY CLEANING": "Прачечная/химчистка",
    "DAYCARE - KINDERGARTEN": "Детсад", "WAREHOUSE/STORAGE": "Склад", "WAREHOUSE": "Склад",
}
def d2(s):
    try: return datetime.date.fromisoformat(s[:10])
    except: return None
def phone_fmt(p):
    d = "".join(c for c in (p or "") if c.isdigit())
    if len(d) < 10 or d[-10:] == "0000000000": return ""
    return f"({d[-10:-7]}) {d[-7:-4]}-{d[-4:]}"
def tier(age):
    return "🟢 ≤30д" if age <= 30 else ("🟢 31-90д" if age <= 90 else "🟡 91-180д")

# --- web-verify map (top-45 P1) ---
verify = json.load(open(f"{SP}/verify_p1.json"))
res = {}
for fn in ("verify_A.txt", "verify_B.txt", "verify_C.txt"):
    for ln in open(f"{SP}/{fn}"):
        parts = [p.strip() for p in ln.strip().split("|")]
        if len(parts) < 2 or not parts[0].isdigit(): continue
        found = next((p[6:].strip() for p in parts if p.startswith("found:")), "")
        res[int(parts[0])] = (parts[1], "" if found == "-" else found)
STAT = {"MATCH": "✓ совпал", "DIFFERENT": "≠ другой №", "NOT_FOUND": "— нет в вебе"}
vmap = {}
for i, v in enumerate(verify):
    if i in res:
        st, found = res[i]
        vmap[(v["gc"], v["phone"])] = (STAT.get(st, ""), found)

def rowdata(a, svc):
    ph = phone_fmt(a.get("ContractorPhone")); gc = (a.get("ContractorName") or "").strip()
    dt = d2(a.get("PermitIssuedDate"))
    if not ph or not gc or not dt: return None
    age = (TODAY - dt).days
    st, found = vmap.get((gc.title(), ph), ("", ""))
    return [(a.get("OwnerName") or "").title(), gc.title(), ph,
            (a.get("PropertyAddress") or "").title(), TARGET.get(a.get("ProposedUseDescription"), (a.get("ProposedUseDescription") or "").title()),
            (a.get("ApplicationTypeDescription") or "").title().replace("Alter", "Ремонт"),
            (a.get("DetailDescriptionComments") or "").strip().title(),
            dt.isoformat(), tier(age), st, found, svc, age]

# --- P1/P2 source ---
feats = []
for off in (0, 1000):
    feats += [f["attributes"] for f in json.load(open(f"{SP}/md_{off}.json")).get("features", [])]
p1 = []; p2 = []; seen = set()
for a in feats:
    if a.get("ProposedUseDescription") not in TARGET: continue
    app = (a.get("ApplicationTypeDescription") or "").upper()
    cmt = (a.get("DetailDescriptionComments") or "").upper()
    key = ((a.get("ContractorName") or "").strip(), phone_fmt(a.get("ContractorPhone")), (a.get("PropertyAddress") or "").strip())
    if not all(key) or key in seen: continue
    interior = ("ALTER - INTERIOR" in app) or any(k in cmt for k in ("REMODEL","BUILDOUT","BUILD OUT","RENO","TENANT","ALTERATION","ALT INT","INT ALT","CHANGE OF USE","CHANGE USE","LEGALIZATION","ESTABLISH USE","FINISH"))
    newb = any(k in app for k in ("NEW", "SHELL", "ADDITION"))
    if interior:
        r = rowdata(a, "Покраска + гипсокартон + полы")
        if r: p1.append(r); seen.add(key)
    elif newb:
        r = rowdata(a, "Final clean на сдаче (+ отделка позже)")
        if r: p2.append(r); seen.add(key)

# --- P3 demo source ---
p3 = []; seen3 = set()
for a in [x["attributes"] for x in json.load(open(f"{SP}/demo.json")).get("features", [])]:
    if a.get("ProposedUseDescription") not in TARGET: continue
    app = (a.get("ApplicationTypeDescription") or "").upper()
    if "DEMO" not in app: continue  # только DEMOLISH-тип
    key = ((a.get("ContractorName") or "").strip(), phone_fmt(a.get("ContractorPhone")), (a.get("PropertyAddress") or "").strip())
    if not all(key) or key in seen3: continue
    r = rowdata(a, "Демонтаж / вывоз мусора (суб)")
    if r: p3.append(r); seen3.add(key)

for lst in (p1, p2, p3): lst.sort(key=lambda r: r[-1])  # freshest first

# --- workbook ---
wb = openpyxl.Workbook(); wb.remove(wb.active)
BRAND = "2E4A62"
COLS = ["Заказчик", "Подрядчик (GC)", "Телефон GC (пермит)", "Объект", "Назначение",
        "Тип работ", "Описание", "Дата", "Актуальность", "Веб-сверка", "Альт. телефон", "Что предложить"]
hf = Font(bold=True, color="FFFFFF"); thin = Side(style="thin", color="D0D0D0")
bd = Border(left=thin, right=thin, top=thin, bottom=thin)
green = Font(color="1E7A34", bold=True); amber = Font(color="9A6A00"); grey = Font(color="777777")
def build(title, data, headcolor, subtitle=""):
    ws = wb.create_sheet(title)
    hint = f"{title} — {subtitle} · {len(data)} объектов · Miami-Dade · активные (CO нет) · свежесть ≤180д · звони по «Телефон GC»; ✓ = номер подтверждён вебом"
    ws.append([hint]); ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(COLS))
    ws["A1"].font = Font(bold=True, color="FFFFFF"); ws["A1"].fill = PatternFill("solid", fgColor=headcolor)
    ws["A1"].alignment = Alignment(vertical="center")
    ws.append(COLS)
    for c in ws[2]:
        c.font = hf; c.fill = PatternFill("solid", fgColor=BRAND); c.border = bd
        c.alignment = Alignment(vertical="center", wrap_text=True, horizontal="center")
    rowfill = PatternFill("solid", fgColor={"P1":"DCE9F7","P2":"FDE9D8","P3":"ECECEC"}[title[:2]])
    for r in data:
        ws.append([r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11]])
        row = ws[ws.max_row]
        for c in row:
            c.alignment = Alignment(vertical="top", wrap_text=True); c.border = bd; c.fill = rowfill
        vc = row[9]
        if r[9].startswith("✓"): vc.font = green
        elif r[9].startswith("≠"): vc.font = amber
        elif r[9].startswith("—"): vc.font = grey
    for i, wd in enumerate([20, 24, 18, 22, 15, 15, 18, 11, 12, 12, 16, 30], 1):
        ws.column_dimensions[get_column_letter(i)].width = wd
    ws.freeze_panes = "A3"; ws.auto_filter.ref = f"A2:{get_column_letter(len(COLS))}{ws.max_row}"
    ws.row_dimensions[1].height = 22

build("P1 · Отделка", p1, "2E5E8C", "Покраска + гипсокартон + полы")
build("P2 · Уборка", p2, "B5651D", "Final clean после стройки")
build("P3 · Демонтаж", p3, "555555", "Демонтаж / вывоз мусора")

out = os.path.join(os.path.dirname(__file__), "..", "reports", "ISP-обзвон-ИТОГ-2026-08-26.xlsx")
wb.save(out)
print("wrote", out)
print(f"P1 отделка: {len(p1)} | P2 уборка: {len(p2)} | P3 демонтаж: {len(p3)}")
