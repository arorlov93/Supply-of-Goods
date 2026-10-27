# -*- coding: utf-8 -*-
"""Заголовки страниц под запрос, а не под бренд.

Что было. На девяти содержательных страницах заголовок оканчивался на
«| ISP Group». В выдаче у заголовка примерно шестьдесят знаков, и на
этих страницах двенадцать из них уходили на имя, которое пока никто не
ищет: сайт новый, брендового спроса нет. Для известной компании это
полезная подпись, для неизвестной это выброшенная четверть строки.

Что делается. Вместо имени в заголовок ставятся слова, которые человек
набирает в поиске. Заголовок страницы и заголовок в тексте расходятся
намеренно: <title> обращён к поиску, <h1> к читателю, и это не уловка,
а разные адресаты. Редакционный заголовок на самой странице не
меняется, og:title тоже остаётся прежним: в соцсетях уместна живая
формулировка, а не поисковая.

Türkiye в одном заголовке продублировано как Turkey: в стране пишут
по-разному, а ищут чаще латинским написанием.

Запуск: python3.13 tools/titles-query.py
Повторный запуск ничего не меняет.
"""
import pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

NEW = {
 "bill-of-lading.html":       "Bill of lading and telex release: originals and consignee",
 "china.html":                "Sourcing from China: factory or trader, inspection, payment",
 "customs-data-pricing.html": "How to find the real import price from customs data",
 "experience.html":           "Twenty years of supply work: China, Russia, European Union",
 "landed-price.html":         "What a landed price must include, line by line",
 "southern-africa.html":      "Durban to Gaborone: SADC supply and SACU transit paperwork",
 "turkiye.html":              "Stone and tile from Turkey, Türkiye, to the United States",
 "verify-supplier.html":      "How to verify a supplier is a factory, not a trader",
 "veterinary-certificate.html":"Veterinary certificate for frozen meat: establishment approval",
 "west-africa.html":          "Frozen poultry into Lomé and Cotonou: admissibility and cuts",
}


def main():
    done = skipped = 0
    seen = {}
    for p in sorted(SITE.glob("*.html")):
        s = p.read_text()
        m = re.search(r"<title>(.*?)</title>", s, re.S)
        if not m:
            continue
        cur = m.group(1).strip()
        want = NEW.get(p.name)
        if want and cur != want:
            s = s[: m.start(1)] + want + s[m.end(1):]
            p.write_text(s)
            cur = want
            done += 1
        elif want:
            skipped += 1
        if cur in seen:
            print(f"  ПОВТОР заголовка: {p.name} и {seen[cur]}")
        seen[cur] = p.name
        if len(cur) > 65:
            print(f"  длинно ({len(cur)}): {p.name}: {cur}")

    print(f"заголовков переписано: {done}, уже было: {skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
