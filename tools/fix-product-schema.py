# -*- coding: utf-8 -*-
"""Снять критическую ошибку разметки, о которой сообщил Search Console.

Письмо от 12.11.2026: «Описания товара: структурированные данные. Задайте
значение для одного из следующих элементов данных: offers, review или
aggregateRating.» Критическая, то есть страницы с ней не допускаются к
показу расширенных результатов.

Причина. На шести страницах товарных категорий внутри каталога стоит
узел типа Product с одним только названием. Google требует у Product
цену, отзыв или рейтинг. Ни одного из трёх у нас нет и быть не может:
цены на сайте мы не публикуем, отзывов и рейтингов не собираем.

Решение. Тип меняется с Product на Service, а название получает приставку
«Supply of». Мы торговая компания: мы не производим эти товары, мы
оказываем услугу их поставки, и Service описывает это точнее, чем
Product. Так уже сделано на /services, и по этой странице Search Console
замечаний не присылал.

Альтернативы и почему они отброшены. Добавить offers нельзя: Offer без
цены ошибку не снимает, а цену ставить запрещено правилами работы.
Удалить каталог целиком можно, но тогда теряется перечень того, что мы
поставляем, а расширенных результатов у OfferCatalog всё равно нет.

Запуск: python3.13 tools/fix-product-schema.py
Повторный запуск ничего не меняет.
"""
import json, pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"


def fix(node):
    """Заменить Product на Service внутри itemOffered. Возвращает счётчик."""
    n = 0
    if isinstance(node, dict):
        io = node.get("itemOffered")
        if isinstance(io, dict) and io.get("@type") == "Product":
            io["@type"] = "Service"
            name = io.get("name")
            if name and not name.startswith("Supply of "):
                io["name"] = "Supply of " + name[0].lower() + name[1:]
            n += 1
        for v in node.values():
            n += fix(v)
    elif isinstance(node, list):
        for v in node:
            n += fix(v)
    return n


def main():
    total = 0
    pages = []
    for p in sorted(SITE.rglob("*.html")):
        s = p.read_text()
        out = s
        for m in re.finditer(r'(?s)<script type="application/ld\+json">(.*?)</script>',
                             s):
            raw = m.group(1)
            if '"Product"' not in raw:
                continue
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as e:
                print("  ВНИМАНИЕ: %s, разметка не разбирается: %s"
                      % (p.relative_to(SITE), e))
                continue
            k = fix(data)
            if not k:
                continue
            new = json.dumps(data, ensure_ascii=False)
            out = out.replace(raw, new, 1)
            total += k
        if out != s:
            p.write_text(out)
            pages.append(str(p.relative_to(SITE)))

    print("узлов исправлено: %d на %d страницах" % (total, len(pages)))
    for x in pages:
        print("   ", x)

    # --- проверка: ни одного Product не осталось, разметка разбирается
    left, bad = [], 0
    for p in sorted(SITE.rglob("*.html")):
        s = p.read_text()
        for m in re.finditer(r'(?s)<script type="application/ld\+json">(.*?)</script>',
                             s):
            try:
                d = json.loads(m.group(1))
            except json.JSONDecodeError as e:
                bad += 1
                print("  СЛОМАНО: %s %s" % (p.relative_to(SITE), e))
                continue

            def walk(o):
                if isinstance(o, dict):
                    if o.get("@type") == "Product":
                        left.append(str(p.relative_to(SITE)))
                    for v in o.values():
                        walk(v)
                elif isinstance(o, list):
                    for v in o:
                        walk(v)
            walk(d)
    if bad:
        return 1
    if left:
        print("ОСТАЛИСЬ Product на:", ", ".join(sorted(set(left))))
        return 1
    print("узлов Product на сайте не осталось, вся разметка разбирается")
    return 0


if __name__ == "__main__":
    sys.exit(main())
