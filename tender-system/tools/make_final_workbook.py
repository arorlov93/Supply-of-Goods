#!/usr/bin/env python3
"""ИТОГОВЫЙ документ обзвона — 3 вкладки: P1 Отделка · P2 Уборка · P3 Демонтаж.
Описание по-русски + оценка бюджета НАШЕЙ работы от площади объекта.
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
# ставки $/SF под НАШ субподряд (South Florida, конкурентно для новой фирмы): (низ, верх)
RATE = {"P1": (9.0, 15.0), "P2": (0.30, 0.45), "P3": (3.0, 6.0)}
# доля от стоимости стройки, если метраж не указан
FRAC = {"P1": (0.15, 0.25), "P2": (0.01, 0.02), "P3": (0.05, 0.10)}

def d2(s):
    try: return datetime.date.fromisoformat(s[:10])
    except: return None
def phone_fmt(p):
    d = "".join(c for c in (p or "") if c.isdigit())
    if len(d) < 10 or d[-10:] == "0000000000": return ""
    return f"({d[-10:-7]}) {d[-7:-4]}-{d[-4:]}"
def tier(age):
    return "🟢 ≤30д" if age <= 30 else ("🟢 31-90д" if age <= 90 else "🟡 91-180д")
def num(s):
    try: return float(re.sub(r"[^0-9.]", "", str(s or "")))
    except: return 0.0

# --- перевод описания на русский ---
DESC_MAP = [
    (("TENANT IMPROVEMENT", "TENANT"), "Отделка под арендатора (build-out)"),
    (("INTERIOR BUILDOUT", "INTERIOR BUILD OUT", "BUILDOUT", "BUILD OUT"), "Отделка помещения под ключ (build-out)"),
    (("CHANGE OF USE", "CHANGE USE", "ESTABLISH USE"), "Смена назначения помещения (полный ремонт)"),
    (("INTERIOR RENOVATION", "INTERIOR RENO", "INT RENO", "RENOVATION", "RENO"), "Внутренняя реновация"),
    (("INTERIOR ALTERATION", "ALTERATION INTERIOR", "INT ALTERATION", "INTERIOR ALT", "ALT INT", "ALTERATION"), "Внутренняя перепланировка"),
    (("INTERIOR REMODELING", "INTERIOR REMODEL", "INT REMODEL", "INT REMOD", "REMODELING/REPAIRS", "REMODELING", "REMODEL"), "Внутренний ремонт помещения"),
    (("NEW CONSTRUC", "NEW CONSTRUCTION", "NEW STORE", "NEW WAREHOUSE", "NEW BLDG", "GROUND UP", "NEW "), "Новое строительство"),
    (("SHELL",), "Возведение коробки (shell)"),
    (("ADDITION",), "Пристройка"),
    (("LEGALIZATION", "LEGALIZE"), "Легализация ранее выполненных работ"),
    (("WALK IN COOLER", "COOLER"), "Установка холодильной камеры"),
    (("WALL OPENING", "WALL OPENINGS"), "Устройство проёма в стене"),
    (("PARTIAL DEMO", "DEMOLITION", "DEMOLISH", "DEMO"), "Демонтаж / снос"),
    (("STORAGE/OFFICE", "STORAGE"), "Складско-офисные работы"),
    (("REPAIR",), "Ремонт/восстановление"),
]
def ru_desc(cmt, app):
    txt = (cmt or "").upper() + " " + (app or "").upper()
    for keys, ru in DESC_MAP:
        if any(k in txt for k in keys):
            return ru
    return "Коммерческий ремонт"
APP_RU = {"ALTER - INTERIOR": "Внутр. ремонт", "NEW": "Новое стр-во", "SHELL ONLY": "Коробка (shell)",
          "ADDITION - ATTACHED": "Пристройка", "DEMOLISH": "Снос", "ALTER - EXTERIOR": "Наружн. ремонт",
          "REPAIR": "Ремонт"}

def budget(pri, sf, val):
    lo, hi = RATE[pri]
    if sf and sf > 50:
        return f"${round(sf*lo,-2):,.0f} – ${round(sf*hi,-2):,.0f}", f"{sf:,.0f} SF"
    if val and val > 500:
        flo, fhi = FRAC[pri]
        return f"~${round(val*flo,-2):,.0f} – ${round(val*fhi,-2):,.0f} (от стройки)", "метраж не указан"
    return "уточнить у GC", (f"{sf:,.0f} SF" if sf else "—")

# --- веб-сверка (топ-45 P1) ---
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

def rowdata(a, pri, svc):
    ph = phone_fmt(a.get("ContractorPhone")); gc = (a.get("ContractorName") or "").strip()
    dt = d2(a.get("PermitIssuedDate"))
    if not ph or not gc or not dt: return None
    age = (TODAY - dt).days
    st, found = vmap.get((gc.title(), ph), ("", ""))
    sf = num(a.get("SquareFootage")); val = num(a.get("EstimatedValue"))
    bud, sfs = budget(pri, sf, val)
    return {"owner": (a.get("OwnerName") or "").title(), "gc": gc.title(), "phone": ph,
            "addr": (a.get("PropertyAddress") or "").title(),
            "use": TARGET.get(a.get("ProposedUseDescription"), (a.get("ProposedUseDescription") or "").title()),
            "work": APP_RU.get((a.get("ApplicationTypeDescription") or "").upper(), (a.get("ApplicationTypeDescription") or "").title()),
            "desc": ru_desc(a.get("DetailDescriptionComments"), a.get("ApplicationTypeDescription")),
            "sf": sfs, "bud": bud, "date": dt.isoformat(), "tier": tier(age),
            "st": st, "found": found, "svc": svc, "age": age}

# --- P1/P2 ---
feats = []
for off in (0, 1000):
    feats += [f["attributes"] for f in json.load(open(f"{SP}/md2_{off}.json")).get("features", [])]
p1 = []; p2 = []; seen = set()
for a in feats:
    if a.get("ProposedUseDescription") not in TARGET: continue
    app = (a.get("ApplicationTypeDescription") or "").upper(); cmt = (a.get("DetailDescriptionComments") or "").upper()
    key = ((a.get("ContractorName") or "").strip(), phone_fmt(a.get("ContractorPhone")), (a.get("PropertyAddress") or "").strip())
    if not all(key) or key in seen: continue
    interior = ("ALTER - INTERIOR" in app) or any(k in cmt for k in ("REMODEL","BUILDOUT","BUILD OUT","RENO","TENANT","ALTERATION","ALT INT","INT ALT","CHANGE OF USE","CHANGE USE","LEGALIZATION","ESTABLISH USE","FINISH"))
    newb = any(k in app for k in ("NEW", "SHELL", "ADDITION"))
    if interior:
        r = rowdata(a, "P1", "Покраска + гипсокартон + полы")
        if r: p1.append(r); seen.add(key)
    elif newb:
        r = rowdata(a, "P2", "Final clean на сдаче (+ отделка позже)")
        if r: p2.append(r); seen.add(key)
# --- P3 ---
p3 = []; seen3 = set()
for a in [x["attributes"] for x in json.load(open(f"{SP}/demo2.json")).get("features", [])]:
    if a.get("ProposedUseDescription") not in TARGET: continue
    if "DEMO" not in (a.get("ApplicationTypeDescription") or "").upper(): continue
    key = ((a.get("ContractorName") or "").strip(), phone_fmt(a.get("ContractorPhone")), (a.get("PropertyAddress") or "").strip())
    if not all(key) or key in seen3: continue
    r = rowdata(a, "P3", "Демонтаж / вывоз мусора (суб)")
    if r: p3.append(r); seen3.add(key)
for lst in (p1, p2, p3): lst.sort(key=lambda r: r["age"])

# --- workbook ---
wb = openpyxl.Workbook(); wb.remove(wb.active)
BRAND = "2E4A62"
COLS = ["Заказчик", "Подрядчик (GC)", "Телефон GC", "Объект", "Назначение", "Тип работ",
        "Описание (RU)", "Площадь", "Оценка нашей работы ($)", "Дата", "Актуальность", "Веб-сверка", "Альт. телефон", "Что предложить"]
hf = Font(bold=True, color="FFFFFF"); thin = Side(style="thin", color="D0D0D0")
bd = Border(left=thin, right=thin, top=thin, bottom=thin)
green = Font(color="1E7A34", bold=True); amber = Font(color="9A6A00"); grey = Font(color="777777")
budf = Font(bold=True, color="10508A")
def build(title, data, headcolor, subtitle, rate_note):
    ws = wb.create_sheet(title)
    hint = f"{title} — {subtitle} · {len(data)} объектов · Miami-Dade, активные (CO нет), ≤180д · {rate_note} · звони по «Телефон GC»"
    ws.append([hint]); ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(COLS))
    ws["A1"].font = Font(bold=True, color="FFFFFF"); ws["A1"].fill = PatternFill("solid", fgColor=headcolor)
    ws["A1"].alignment = Alignment(vertical="center")
    ws.append(COLS)
    for c in ws[2]:
        c.font = hf; c.fill = PatternFill("solid", fgColor=BRAND); c.border = bd
        c.alignment = Alignment(vertical="center", wrap_text=True, horizontal="center")
    rowfill = PatternFill("solid", fgColor={"P1":"DCE9F7","P2":"FDE9D8","P3":"ECECEC"}[title[:2]])
    for r in data:
        ws.append([r["owner"], r["gc"], r["phone"], r["addr"], r["use"], r["work"], r["desc"],
                   r["sf"], r["bud"], r["date"], r["tier"], r["st"], r["found"], r["svc"]])
        row = ws[ws.max_row]
        for c in row:
            c.alignment = Alignment(vertical="top", wrap_text=True); c.border = bd; c.fill = rowfill
        row[8].font = budf
        vc = row[11]
        if r["st"].startswith("✓"): vc.font = green
        elif r["st"].startswith("≠"): vc.font = amber
        elif r["st"].startswith("—"): vc.font = grey
    for i, wd in enumerate([19, 23, 15, 21, 14, 14, 26, 11, 22, 11, 12, 11, 14, 28], 1):
        ws.column_dimensions[get_column_letter(i)].width = wd
    ws.freeze_panes = "A3"; ws.auto_filter.ref = f"A2:{get_column_letter(len(COLS))}{ws.max_row}"
    ws.row_dimensions[1].height = 26

build("P1 · Отделка", p1, "2E5E8C", "Покраска + гипсокартон + полы", "ставка $9–15/SF (полный пакет отделки)")
build("P2 · Уборка", p2, "B5651D", "Final clean после стройки", "ставка $0.30–0.45/SF")
build("P3 · Демонтаж", p3, "555555", "Демонтаж / вывоз мусора", "ставка $3–6/SF")

out = os.path.join(os.path.dirname(__file__), "..", "reports", "ISP-обзвон-ИТОГ-2026-08-26.xlsx")
wb.save(out)
print("wrote", out)
print(f"P1 отделка: {len(p1)} | P2 уборка: {len(p2)} | P3 демонтаж: {len(p3)}")
