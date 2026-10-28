# -*- coding: utf-8 -*-
"""Ссылки на три новые страницы из тех, где они уместны по смыслу.

Зачем. Ссылка в подвале стоит на всех страницах сразу и поэтому весит
мало: поисковик понимает, что она служебная. Ссылка из текста по теме
весит заметно больше, потому что она выбрана, а не проставлена везде.
Для сайта, который вообще не в индексе, внутренняя перелинковка это
единственный рычаг, который работает сразу: она не приводит людей, но
показывает поисковику, какие страницы на сайте главные.

Куда и почему именно туда:

* стоимость до ворот и коды ТН ВЭД ведут на индекс, потому что индекс
  это ровно та цифра, про которую там написано словами;
* проверка поставщика и китайский коридор ведут на проверку чужого
  предложения, потому что человек, читающий про проверку, держит в руках
  предложение;
* коридоры, что мы поставляем и турецкий коридор ведут на три
  происхождения, потому что это их прямое продолжение.

Карточка добавляется в уже существующую сетку «читать дальше», новых
блоков на страницах не появляется.

Запуск: python3.13 tools/crosslink.py
Повторный запуск ничего не дублирует.
"""
import pathlib, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

CARD = ('<a class="lanelink" href="{href}"><b>{title}</b><span>{sub}</span></a>')

INDEX = dict(href="landed-price-index", title="The landed price index",
             sub="What freight and insurance actually add, by origin, from customs data.")
CHECK = dict(href="quote-check", title="Send us the quote you already have",
             sub="We rebuild it as a landed price and benchmark it. Free, no obligation.")
THREE = dict(href="three-origins", title="Three origins, one price sheet",
             sub="One specification priced out of three continents, landed.")

PLAN = {
    "landed-price.html": INDEX,
    "hs-code.html": INDEX,
    "customs-data-pricing.html": INDEX,
    "verify-supplier.html": CHECK,
    "china.html": CHECK,
    "proforma-invoice.html": CHECK,
    "corridors.html": THREE,
    "supply.html": THREE,
    "turkiye.html": THREE,
}

ANCHOR = '<div class="lanelinks">'


def main():
    done = skipped = 0
    for name, card in PLAN.items():
        p = SITE / name
        if not p.is_file():
            print(f"  нет файла {name}")
            continue
        s = p.read_text()
        i = s.find(ANCHOR)
        # Проверять наличие ссылки по всей странице нельзя: такая же стоит в
        # подвале, и тогда карточка не добавится никогда. Смотрим только
        # внутрь самой сетки.
        grid = s[i: s.find("</div>", i)] if i >= 0 else ""
        if ('href="%s"' % card["href"]) in grid:
            skipped += 1
            continue
        if i < 0:
            print(f"  {name}: сетки «читать дальше» нет, пропускаю")
            continue
        i += len(ANCHOR)
        s = s[:i] + CARD.format(**card) + s[i:]
        p.write_text(s)
        print(f"  {name} -> {card['href']}")
        done += 1
    print(f"ссылок добавлено: {done}, уже было: {skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
