# -*- coding: utf-8 -*-
"""Снимает с четырёх главных страниц строчку, которая отменяет главное
утверждение сайта.

Что стояло. Под перечнем шести категорий на главной и на трёх языковых
главных:

  «These are the lanes we already run, food among them. They are where we
  start, not where we stop: name a product outside this list and we will
  source it the same way.»

Почему снимаем. На той же странице сайт говорит «Principal, not a
broker». Обещание достать что угодно, названное покупателем, это дословно
описание работы брокера: посредник берёт заказ на любой товар, потому что
не держит ни одной полосы. Два утверждения стоят в двадцати строках друг
от друга, и покупатель верит худшему.

Так это и прочли. Совет директоров по сайту
(`founder/board-site.md`) поставил широту первым пунктом в двух рамках
из трёх: по рамке Offers это позиция брокера, которая противоречит
единственному утверждению, стоящему того, чтобы его делать; по рамке
Monopoly заголовок называет бесконечный рынок и не занимает в нём
ничего. Замер подтверждает: 1 095 показов, 6 кликов, 0,55 процента,
средняя позиция 23,5.

Что остаётся. Первое предложение целиком, без обещания. Перечень
категорий не трогаем, страницы категорий не трогаем. Снимается ровно
обещание, а не охват.

Правка идёт и в собранные страницы, и в tools/i18n.json, иначе сборка
вернёт строчку обратно. Ключ словаря это сама английская фраза, поэтому
старый ключ удаляется, а новый, усечённый, добавляется с усечёнными
переводами: они дословные начала прежних, ничего не переведено заново.

Запуск: python3.13 tools/drop-broker-line.py
Повторный запуск ничего не меняет.
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
I18N = ROOT / "tools" / "i18n.json"

EN_OLD = ("These are the lanes we already run, food among them. They are where "
          "we start, not where we stop: name a product outside this list and we "
          "will source it the same way.")
EN_NEW = "These are the lanes we already run, food among them."

# Переводы: ровно начало прежних строк из i18n.json, до двоеточия.
PAIRS = [
    (EN_OLD, EN_NEW),
    ("Voici les flux que nous opérons déjà, l’alimentaire "
     "compris. C’est notre point de départ, pas notre limite : "
     "nommez un produit hors de cette liste et nous le sourcerons de la "
     "même façon.",
     "Voici les flux que nous opérons déjà, l’alimentaire "
     "compris."),
    ("Estas son las rutas que ya operamos, la alimentación entre ellas. "
     "Son el punto de partida, no el límite: nombre un producto fuera de "
     "esta lista y lo abasteceremos igual.",
     "Estas son las rutas que ya operamos, la alimentación entre ellas."),
    ("Das sind die Verkehre, die wir bereits fahren, Lebensmittel "
     "eingeschlossen. Sie sind der Anfang, nicht die Grenze: Nennen Sie ein "
     "Produkt außerhalb dieser Liste, und wir beschaffen es genauso.",
     "Das sind die Verkehre, die wir bereits fahren, Lebensmittel "
     "eingeschlossen."),
]


def main():
    pages = 0
    for p in sorted(SITE.rglob("*.html")):
        s = p.read_text()
        t = s
        for old, new in PAIRS:
            if old in t:
                t = t.replace(old, new)
        if t != s:
            p.write_text(t)
            print("  %s: строчка снята" % p.relative_to(SITE))
            pages += 1

    # Словарь правим текстом, а не разбором и обратной записью: файл
    # сгруппирован пустыми строками, короткие записи лежат по одной в
    # строку, и json.dumps всё это разносит, превращая правку одной
    # записи в пятьсот строк разницы.
    raw = I18N.read_text()
    moved = 0
    if EN_OLD in raw:
        out = raw
        for old, new in PAIRS:
            out = out.replace('"%s"' % old, '"%s"' % new)
        json.loads(out)          # не выпускаем сломанный словарь
        I18N.write_text(out)
        moved = 1
        print("  i18n.json: ключ и три перевода усечены")

    # Последняя проверка: обещания не должно остаться ни на одной странице.
    left = [str(p.relative_to(SITE)) for p in SITE.rglob("*.html")
            if any(w in p.read_text() for w in
                   ("outside this list", "hors de cette liste",
                    "fuera de esta lista", "außerhalb dieser Liste"))]
    if left:
        print("  ВНИМАНИЕ: обещание осталось на %s" % ", ".join(left))
        return 1

    print("страниц поправлено: %d, словарь: %d" % (pages, moved))
    return 0


if __name__ == "__main__":
    sys.exit(main())
