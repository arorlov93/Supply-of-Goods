#!/usr/bin/env python3
"""Сбор живых лотов под параметры заказчика.

Фильтр: вся РФ · стройматериалы, инструменты, мебель, одежда, хозтовары для
коммунальных служб · обеспечение собственными деньгами до 2,5 млн ₽ (выше — БГ).
"""
import sys, re, json, datetime as dt, collections
sys.path.insert(0, "/root/.claude/skills/ru-tenders-sourcing/scripts")
import scrape

TODAY = dt.date.today()
CASH_CAP = 2_500_000          # потолок собственных денег на обеспечение

CATS = {
    "стройматериалы": "/tendery-stroitelnye-materialy",
    "оборуд. и материалы для стройки/ремонта": "/tendery-oborudovanie-i-materialy-dlya-stroitelstva-i-remonta-montaj-i-obslujivanie",
    "отделочные материалы": "/tendery-otdelochnye-materialy",
    "инструменты": "/tendery-instrumenty",
    "метизы и крепёж": "/tendery-metizy-krepejnye-izdeliya",
    "сантехника и трубы": "/tendery-santehnicheskie-izdeliya-nemetallicheskie-truby",
    "светотехника": "/tendery-svetotehnicheskaya-produkciya-lampy-i-drugoe-osvetitelnoe-oborudovanie",
    "хозтовары и бытовая химия": "/tendery-hozyajstvennye-tovary-tovary-shirokogo-potrebleniya-bytovaya-himiya-i-parfyumeriya",
    "одежда, обувь, спецодежда": "/tendery-obuv-specobuv-odejda-specodejda",
    "одежда/СИЗ/текстиль/тара": "/tendery-odejda-obuv-sredstva-zashchity-tekstil-hoztovary-tara-i-upakovka",
    "текстиль и мягкий инвентарь": "/tendery-tekstil-i-tekstilnye-izdeliya-materialy-dlya-proizvodstva-tekstilya-myagkij-inventar-vetosh",
    "канцелярия": "/tendery-kancelyarskie-prinadlejnosti",
}


def d(s):
    try:
        return dt.datetime.strptime(s, "%d.%m.%Y").date()
    except Exception:
        return None


def security_rub(row):
    """Обеспечение контракта в рублях. Возвращает (сумма, вид)."""
    s = (row.get("sec_contract") or "").strip()
    if not s:
        return None, "не установлено"
    m = re.match(r"([\d.,]+)\s*%", s)
    if m and row.get("nmck"):
        pct = float(m.group(1).replace(",", "."))
        return row["nmck"] * pct / 100, f"{pct}%"
    digits = re.sub(r"[^\d]", "", s)
    if digits:
        return int(digits), "фикс."
    return None, s


def sweep(path, pages=6):
    out, seen = [], set()
    for pg in range(1, pages + 1):
        url = scrape.BASE + path + (f"?page={pg}" if pg > 1 else "")
        rows = scrape.parse(scrape.fetch(url))
        if not rows:
            break
        live = 0
        for r in rows:
            if r["num"] in seen:
                continue
            seen.add(r["num"])
            end = d(r["end"])
            if not end or end < TODAY:
                continue
            live += 1
            r["end_date"] = end.isoformat()
            r["days_left"] = (end - TODAY).days
            r["sec_rub"], r["sec_kind"] = security_rub(r)
            out.append(r)
        if live == 0 and pg > 2:
            break
    return out


if __name__ == "__main__":
    allr = []
    for name, path in CATS.items():
        r = sweep(path)
        for x in r:
            x["cat"] = name
        allr += r
        print(f"{name:42} живых: {len(r)}", file=sys.stderr)
    uniq = {x["num"]: x for x in allr}
    res = sorted(uniq.values(), key=lambda x: -(x["nmck"] or 0))
    json.dump(res, open("lots.json", "w"), ensure_ascii=False, indent=1)
    print(f"\nвсего живых лотов: {len(res)}", file=sys.stderr)
