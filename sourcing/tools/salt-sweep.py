#!/usr/bin/env python3
"""Полный обход соляных категорий rostender с пагинацией.

Листаем, пока встречаются лоты с неистёкшим сроком подачи. Выдача отсортирована
по дате публикации, поэтому идём вглубь, пока доля живых не упадёт до нуля.
"""
import datetime as dt, json, re, sys, time
import scrape

TODAY = dt.date.today()
CATS = {
    "соль техническая / галит": "/tendery-tehnicheskie-soli",
    "антигололёдные реагенты": "/category/tendery-antigololednye-reagenty",
    "химическая продукция": "/tendery-himicheskaya-produkciya",
    "продукция карьеров (песок, щебень)": "/tendery-produkciya-kamennyh-karerov-shcheben-pesok-glina",
}
SALT = re.compile(r"сол[ьие]|галит|пгм|противогололед|антигололед|реагент|пескосол|хлорид натрия", re.I)


def d(s):
    try:
        return dt.datetime.strptime(s, "%d.%m.%Y").date()
    except Exception:
        return None


def sweep(path, pages=12, salt_only=True):
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
            if salt_only and not SALT.search(r["title"]):
                continue
            r["end_date"] = end.isoformat()
            out.append(r)
        print(f"  стр.{pg:>2}: всего {len(rows):3}, живых {live:3}, "
              f"подходящих накоплено {len(out)}", file=sys.stderr)
        if live == 0 and pg > 2:
            break
        time.sleep(0.3)
    return out


if __name__ == "__main__":
    allr = []
    for name, path in CATS.items():
        print(f"\n### {name}", file=sys.stderr)
        r = sweep(path)
        for x in r:
            x["cat"] = name
        allr += r
    # дедуп по номеру
    uniq = {x["num"]: x for x in allr}
    res = sorted(uniq.values(), key=lambda x: -(x["nmck"] or 0))
    json.dump(res, open("salt_live.json", "w"), ensure_ascii=False, indent=1)
    print(f"\nживых соляных лотов: {len(res)}")
    tot = sum(x["nmck"] or 0 for x in res)
    print(f"суммарная НМЦК: {tot:,.0f} ₽".replace(",", " "))
