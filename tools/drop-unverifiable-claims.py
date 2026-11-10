# -*- coding: utf-8 -*-
"""Снять два утверждения, которые нечем подтвердить.

Заказчик сказал 10.11.2026: убрать везде.

1. "Authorized distributor of the manufacturers we quote". Мы торговая
   компания и покупаем у заводов по сделке. Дистрибьюторского договора
   ни с одним из них нет, значит слово "authorized" подтвердить нечем.
   Покупатель промышленной химии проверяет это одним письмом заводу.

2. "Free samples before the first order". Образец оплачивает завод или
   мы, бесплатность зависит от позиции и объёма, обещать её заранее
   нельзя.

Строка доверия на главных не схлопывается до двух пунктов: на их место
встают два обещания, которые на сайте уже опубликованы и подкреплены
отдельными разделами, а значит проверяемы:

   платёж по аккредитиву против документов  -> блок #s-pay на главной
   инспекция третьей стороной до отгрузки   -> тот же блок и страницы
                                               допустимости по странам

Переводы взяты из уже переведённых блоков тех же страниц, не придуманы.

Запуск: python3.13 tools/drop-unverifiable-claims.py
Повторный запуск ничего не меняет.
"""
import pathlib, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

LANGS = ("en", "fr", "es", "de")
HOME = {"en": "index.html", "fr": "fr/index.html",
        "es": "es/index.html", "de": "de/index.html"}
CHEM = {"en": "chemicals.html", "fr": "fr/chemicals.html",
        "es": "es/chemicals.html", "de": "de/chemicals.html"}

# --- строка доверия: что на что меняется
TRUST = {
 "en": [("Authorized distributor of the manufacturers we quote",
         "Payment at sight against documents, never in advance"),
        ("Free samples before the first order",
         "Pre-shipment inspection by an agency you name")],
 "fr": [("Distributeur agréé des fabricants que nous cotons",
         "Paiement à vue contre documents, jamais d’avance"),
        ("Échantillons gratuits avant la première commande",
         "Inspection avant expédition par un organisme que vous nommez")],
 "es": [("Distribuidor autorizado de los fabricantes que cotizamos",
         "Pago a la vista contra documentos, nunca por adelantado"),
        ("Muestras gratuitas antes del primer pedido",
         "Inspección previa al embarque por una entidad que usted nombre")],
 "de": [("Autorisierter Händler der Hersteller, die wir anbieten",
         "Zahlung bei Sicht gegen Dokumente, nie im Voraus"),
        ("Kostenlose Muster vor der ersten Bestellung",
         "Vorversandinspektion durch eine von Ihnen benannte Stelle")],
}

# --- вводный абзац /chemicals: убрать оговорку про дистрибьюторство
LEDE = {
 "en": ("manufacturers we have verified, as their authorized distributor, and "
        "deliver", "manufacturers we have verified, and deliver"),
 "fr": ("fabricants que nous avons vérifiés, en qualité de distributeur "
        "agréé, et livrons", "fabricants que nous avons vérifiés, et livrons"),
 "es": ("fabricantes que hemos verificado, como su distribuidor autorizado, "
        "y entregamos", "fabricantes que hemos verificado, y entregamos"),
 "de": ("Werken an, die wir geprüft haben, als deren autorisierter Händler, "
        "und liefern", "Werken an, die wir geprüft haben, und liefern"),
}

# --- карточка "Documents first" на /chemicals: убрать бесплатные образцы
SAMPLES = {
 "en": ("TDS, SDS and a sample COA before any price; free samples on request.",
        "TDS, SDS and a sample COA before any price."),
 "fr": ("TDS, FDS et un COA type avant tout prix ; échantillons gratuits sur "
        "demande.", "TDS, FDS et un COA type avant tout prix."),
 "es": ("TDS, SDS y un COA de muestra antes de cualquier precio; muestras "
        "gratuitas a solicitud.",
        "TDS, SDS y un COA de muestra antes de cualquier precio."),
 "de": ("TDS, SDB und ein Muster-COA vor jedem Preis; kostenlose Muster auf "
        "Anfrage.", "TDS, SDB und ein Muster-COA vor jedem Preis."),
}

GONE = ("authorized distributor", "Authorized distributor", "free samples",
        "Free samples", "distributeur agréé", "Distributeur agréé",
        "Échantillons gratuits", "échantillons gratuits",
        "distribuidor autorizado", "Distribuidor autorizado",
        "Muestras gratuitas", "muestras gratuitas",
        "autorisierter Händler", "Autorisierter Händler",
        "Kostenlose Muster", "kostenlose Muster")


def swap(path, pairs):
    p = SITE / path
    s = p.read_text()
    before = s
    for old, new in pairs:
        if old not in s:
            if new in s:
                continue                       # уже поправлено
            print("  ВНИМАНИЕ: %s, не найдено: %s" % (path, old[:48]))
            continue
        if s.count(old) != 1:
            print("  ВНИМАНИЕ: %s, встречается %d раз: %s"
                  % (path, s.count(old), old[:48]))
            continue
        s = s.replace(old, new, 1)
    if s != before:
        p.write_text(s)
        return True
    return False


def main():
    changed = []
    for lg in LANGS:
        if swap(HOME[lg], TRUST[lg]):
            changed.append(HOME[lg])
        if swap(CHEM[lg], [LEDE[lg], SAMPLES[lg]]):
            changed.append(CHEM[lg])
    print("страниц поправлено: %d (%s)" % (len(changed), ", ".join(changed)
                                           or "уже были поправлены"))

    left = []
    for q in sorted(SITE.rglob("*.html")):
        s = q.read_text()
        for bad in GONE:
            if bad in s:
                left.append("%s: %s" % (q.relative_to(SITE), bad))
    if left:
        print("ОСТАЛОСЬ НА СТРАНИЦАХ:")
        for x in left:
            print("   ", x)
        return 1
    print("ни дистрибьюторства, ни бесплатных образцов на сайте не осталось")
    return 0


if __name__ == "__main__":
    sys.exit(main())
