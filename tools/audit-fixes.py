# -*- coding: utf-8 -*-
"""Исправления по внешнему аудиту от 27.10.2026.

Аудит проверял не код, а то, что написано, и нашёл то, чего не ловили
мои проверки: контраст, сдвиг макета и вес ничего не говорят о том,
правду ли говорит текст и не противоречит ли он сам себе. Для сайта,
который продаёт компетентность, это дороже любой технической ошибки.

Здесь правится только то, что я подтвердил сам, на живом сайте. Один
пункт аудита, про битые картинки, оказался ложным: сайт не ссылается на
безверсионные пути, инструмент аудита сам отрезал хеш и получил 404.

Что правится:

1. Счётчик руководств. Написано 12 и «Twelve», фактически 16.
2. Опечатка «Tükiye» на четырёх страницах, а не на двух.
3. Вступление политики. «Collects nothing about you» не соответствует
   тому, что ниже на той же странице перечислен счётчик.
4. Пошлина и условия поставки. «Duty included» без оговорки
   противоречит DAP, где растаможку и пошлину платит покупатель.
5. Экспортная лицензия в Китае. Общая регистрация внешнеторговых
   операторов отменена с 30.12.2022, осталась таможенная регистрация
   плюс лицензии на отдельные контролируемые товары.
6. «In your own jurisdiction» на about. Американская компания не может
   обещать покупателю его собственную юрисдикцию.
7. «Moves a target by a fifth or more» на services. Цифра без
   доказательства.
8. Ответственность за код ТН ВЭД сформулирована как абсолют.

Запуск: python3.13 tools/audit-fixes.py
Повторный запуск ничего не меняет.
"""
import pathlib, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

# файл -> [(что заменить, на что, сколько раз ожидаем)]
FIXES = {
"guides.html": [
 ("<b>12</b> guides", "<b>16</b> guides", None),
 ("12 guides", "16 guides", None),
 ("Twelve, in the order we would read them.",
  "Sixteen, in the order we would read them.", None),
],
"privacy.html": [
 ("The short version is that the site itself collects nothing about you.",
  "The short version: nothing is stored on your device, page views are counted "
  "without a profile, and your details reach us only when you choose to send the "
  "enquiry form.", None),
],
"supply.html": [
 ("Priced landed, with freight, insurance, port charges, duty and certification "
  "included and the rate validity stated.",
  "Priced landed, with freight, insurance, port charges, estimated duty and "
  "certification shown line by line, and the rate validity stated. Who actually "
  "pays the duty follows the agreed Incoterm.", None),
],
"about.html": [
 ("You deal with one counterparty, one invoice and one currency, in your own "
  "jurisdiction.",
  "You deal with one counterparty, one invoice and one currency.", None),
],
"services.html": [
 ("Negotiating against the second rather than the first regularly moves a target "
  "by a fifth or more.",
  "Negotiating against the second rather than the first moves the target. We show "
  "the source, the period and the limits of the comparison, so the size of the "
  "move is yours to judge rather than ours to claim.", None),
],
"landed-price.html": [
 ("Yes, at the classification we have agreed in writing with you before the order.",
  "It is shown as a line in the build-up, at the classification we have agreed in "
  "writing with you before the order. Who pays it follows the Incoterm: under DAP "
  "import clearance and duty stay with the buyer, and the quotation says so.", None),
],
"china.html": [
 ("Business licence, export licence, beneficiary name match, factory check",
  "Business licence, exporter of record, beneficiary name match, factory check", None),
 ("the export licence shows whether the entity can ship in its own name",
  "the customs registration shows whether the entity exports in its own name, with a "
  "product licence on top of it where the goods are controlled", None),
 ("The importer of record, not the Chinese seller who typed it on the invoice.",
  "The importer of record usually carries the primary liability for the entry, not "
  "the seller who typed the code on the invoice, although the exact position depends "
  "on the law of the destination and on the facts.", None),
],
}

# опечатка встречается на нескольких страницах, правим по всему сайту
GLOBAL = [("Tükiye", "Türkiye")]


def main():
    total = 0
    for name, pairs in FIXES.items():
        p = SITE / name
        if not p.is_file():
            print(f"  нет файла {name}")
            continue
        s = p.read_text()
        before = s
        for old, new, _ in pairs:
            n = s.count(old)
            if n:
                s = s.replace(old, new)
                print(f"  {name}: {n} замен, «{old[:46]}…»")
                total += n
        if s != before:
            p.write_text(s)

    for old, new in GLOBAL:
        hit = 0
        for p in sorted(SITE.rglob("*.html")):
            s = p.read_text()
            n = s.count(old)
            if n:
                p.write_text(s.replace(old, new))
                hit += n
        if hit:
            print(f"  по всему сайту: {hit} замен «{old}» -> «{new}»")
            total += hit

    print(f"всего правок: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
