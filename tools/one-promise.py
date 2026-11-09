# -*- coding: utf-8 -*-
"""Одно обещание на всех четырёх главных.

Что было. Французскую главную 8 ноября перевели на «допустимость прежде
цены». Английская, испанская и немецкая остались на «назовите товар, мы
доставим»: это обещание брокера, то самое, строчку про которое из текста
сайта убрали, а из заголовка нет.

Почему это хуже, чем просто непоследовательность. Рамка Product на втором
разборе поставила это первым пунктом и сформулировала так: **половина
фокуса не разбавляет хорошую позицию, а дискредитирует её.** Покупатель,
который пришёл на обещание «назовите товар», попадает на сайт, который
обслуживает одну полосу, и делает единственный возможный вывод.

Панель на 250 покупателях даёт этому число, которого в прошлом прогоне
не было вовсе: **109 человек из 250, 43 процента, сказали «это не мой
регион»**. В сегменте Южной Африки 95 процентов, у снабженцев 56, у
первых импортёров 49, а у франкоязычной Западной Африки, то есть у тех,
кто пришёл на французскую главную, всего 15.

Что ставим. Заголовок «допустимость прежде цены» на трёх оставшихся
языках. Это утверждение не привязано к региону: оно про то, что решает
вход груза в любую страну, и остаётся верным для любого порта. Полоса
живёт ниже, на страницах по странам.

Плюс одна строчка в лиде, которой нет сейчас ни на одном языке:
документный комплект расписан по Абиджану, Дакару и Дуале, **назовите
другой порт, и мы распишем его так же.** Это не возврат к «назовите
товар»: там обещали достать что угодно, здесь обещают разобрать правила
ввоза, то есть ровно то, чем компания и занимается.

Словарь переводов правится тоже, иначе сборка вернёт прежний заголовок.
Подстановка в make-languages.py идёт по тексту узла целиком, поэтому
короткие ключи безопасны: совпасть может только узел, равный ключу.

Запуск: python3.13 tools/one-promise.py
Повторный запуск ничего не меняет.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
I18N = ROOT / "tools" / "i18n.json"

IND = "\n" + " " * 12

H1 = {
 "index.html":    ["ADMISSIBILITY", "BEFORE", "PRICE."],
 "es/index.html": ["ADMISIBILIDAD", "ANTES", "QUE EL PRECIO."],
 "de/index.html": ["ZULÄSSIGKEIT", "VOR", "DEM PREIS."],
}

H1_OLD = {
 "index.html":    ["NAME THE", "PRODUCT.", "WE DELIVER IT."],
 "es/index.html": ["DÍGANOS QUÉ", "PRODUCTO.", "SE LO ENTREGAMOS."],
 "de/index.html": ["NENNEN SIE", "DIE WARE.", "WIR LIEFERN SIE."],
}

PORTS = {
 "index.html":
   " The document file is written out port by port for Abidjan, Dakar and "
   "Douala. Name another port and we will set out the same file for it.",
 "fr/index.html":
   " Le dossier documentaire est écrit port par port pour Abidjan, Dakar "
   "et Douala. Nommez un autre port et nous établirons le même "
   "dossier pour lui.",
 "es/index.html":
   " El expediente documental está escrito puerto por puerto para "
   "Abiyán, Dakar y Duala. Indíquenos otro puerto y prepararemos el "
   "mismo expediente para él.",
 "de/index.html":
   " Der Dokumentensatz ist Hafen für Hafen für Abidjan, Dakar und "
   "Douala ausgeschrieben. Nennen Sie uns einen anderen Hafen, und wir "
   "erstellen denselben Satz dafür.",
}

LEAD_OLD = {
 "index.html":
   "Industrial goods, building materials, equipment, packaging and food. We "
   "find the producer, verify it, buy in our own name and deliver to your "
   "port. Principal, not a broker.",
 "es/index.html":
   "Bienes industriales, materiales de construcción, equipos, envases y "
   "alimentos. Localizamos al productor, lo verificamos, compramos en nombre "
   "propio y entregamos en su puerto. Actuamos como principal, no como "
   "intermediario.",
 "de/index.html":
   "Industriegüter, Baustoffe, Ausrüstung, Verpackung und "
   "Lebensmittel. Wir finden den Hersteller, prüfen ihn, kaufen auf "
   "eigene Rechnung und liefern an Ihren Hafen. Eigenhändler, kein "
   "Makler.",
}

LEAD_NEW = {
 "index.html":
   "An offer from a producer that cannot legally ship to your country is not "
   "an offer, whatever the number on it. We buy in our own name, we carry the "
   "document file through to your port, and where your bank requires it we "
   "work against documents.",
 "es/index.html":
   "Una oferta de un productor que no puede enviar legalmente a su país "
   "no es una oferta, sea cual sea la cifra. Compramos en nombre propio, "
   "llevamos el expediente documental hasta su puerto y, cuando su banco lo "
   "exige, trabajamos contra documentos.",
 "de/index.html":
   "Ein Angebot von einem Hersteller, der nicht legal in Ihr Land liefern "
   "darf, ist kein Angebot, gleich welche Zahl darauf steht. Wir kaufen im "
   "eigenen Namen, führen den Dokumentensatz bis zu Ihrem Hafen und "
   "arbeiten gegen Dokumente, wo Ihre Bank es verlangt.",
}

# Французский лид уже стоит с 8 ноября, его только дополняем портами.
LEAD_FR = ("Une offre d’un producteur qui ne peut pas légalement "
           "expédier vers votre pays n’est pas une offre, quel que "
           "soit le chiffre dessus. Nous achetons en notre propre nom, nous "
           "portons le dossier documentaire jusqu’à votre port, et "
           "quand votre banque l’exige nous travaillons contre "
           "documents.")

# Словарь: ключ это английский оригинал. Меняем три ключа заголовка и лид.
I18N_SWAPS = [
 ("NAME THE", "ADMISSIBILITY",
  {"fr": "L’ADMISSIBILITÉ", "es": "ADMISIBILIDAD",
   "de": "ZULÄSSIGKEIT"}),
 ("PRODUCT.", "BEFORE",
  {"fr": "AVANT", "es": "ANTES", "de": "VOR"}),
 ("WE DELIVER IT.", "PRICE.",
  {"fr": "LE PRIX.", "es": "QUE EL PRECIO.", "de": "DEM PREIS."}),
]


# Заголовок окна и описание для поиска. Французские title и description уже
# стоят с 8 ноября, у них правятся только og-теги, которые тогда пропустили.
META = {
 "index.html": {
  "title": "Admissibility before price: ISP Group LLC, supply to your port",
  "desc": "An offer from a producer that cannot legally ship to your country "
          "is not an offer. We buy in our own name and carry the document "
          "file through to your port.",
  "og": "Admissibility before price. ISP Group LLC",
 },
 "fr/index.html": {
  "og": "L’admissibilité avant le prix. ISP Group LLC",
 },
 "es/index.html": {
  "title": "La admisibilidad antes que el precio: ISP Group LLC",
  "desc": "Una oferta de un productor que no puede enviar legalmente a su "
          "país no es una oferta. Compramos en nombre propio y llevamos el "
          "expediente documental hasta su puerto.",
  "og": "La admisibilidad antes que el precio. ISP Group LLC",
 },
 "de/index.html": {
  "title": "Zulässigkeit vor dem Preis: ISP Group LLC",
  "desc": "Ein Angebot von einem Hersteller, der nicht legal in Ihr Land "
          "liefern darf, ist kein Angebot. Wir kaufen im eigenen Namen und "
          "führen den Dokumentensatz bis zu Ihrem Hafen.",
  "og": "Zulässigkeit vor dem Preis. ISP Group LLC",
 },
}


def set_attr(s, pat, value):
    """Подставляет content=... в один тег. Повторный вызов ничего не меняет."""
    m = re.search(pat, s)
    if not m or m.group(1) == value:
        return s, False
    return s[:m.start(1)] + value + s[m.end(1):], True


def meta(name, s):
    cfg = META[name]
    done = []
    if "title" in cfg:
        s, ok = set_attr(s, r"<title>([^<]*)</title>", cfg["title"])
        if ok:
            done.append("title")
    desc = cfg.get("desc")
    if desc:
        s, ok = set_attr(
            s, r'<meta name="description" content="([^"]*)"', desc)
        if ok:
            done.append("description")
    else:
        m = re.search(r'<meta name="description" content="([^"]*)"', s)
        desc = m.group(1) if m else None
    s, ok = set_attr(
        s, r'<meta property="og:title" content="([^"]*)"', cfg["og"])
    if ok:
        done.append("og:title")
    if desc:
        s, ok = set_attr(
            s, r'<meta property="og:description" content="([^"]*)"', desc)
        if ok:
            done.append("og:description")
    return s, done


def span(line):
    return '<span class="ln"><span>%s</span></span>' % line


def i18n_lead(raw):
    """Ключ лида в словаре это прежний английский лид, которого на страницах
    больше нет. Переписываем ключ и три перевода на то, что реально стоит."""
    old_key = LEAD_OLD["index.html"]
    if '"%s":' % old_key not in raw:
        return raw, False
    new_key = LEAD_NEW["index.html"] + PORTS["index.html"]
    block = ('"%s": {\n  "fr": "%s",\n  "es": "%s",\n  "de": "%s"}'
             % (new_key,
                LEAD_FR + PORTS["fr/index.html"],
                LEAD_NEW["es/index.html"] + PORTS["es/index.html"],
                LEAD_NEW["de/index.html"] + PORTS["de/index.html"]))
    pat = r'"%s":\s*\{.*?\}' % re.escape(old_key)
    out, n = re.subn(pat, lambda m: block, raw, count=1, flags=re.S)
    return out, bool(n)


def main():
    pages = 0
    for name in ("index.html", "fr/index.html", "es/index.html", "de/index.html"):
        p = SITE / name
        s = p.read_text()
        orig = s
        steps = []

        if name in H1:
            new = IND.join(span(x) for x in H1[name])
            old = IND.join(span(x) for x in H1_OLD[name])
            if new in s:
                pass
            elif old in s:
                s = s.replace(old, new, 1)
                steps.append("заголовок")
            else:
                print("  ВНИМАНИЕ: %s, прежний заголовок не найден" % name)

        if name in LEAD_OLD:
            if LEAD_NEW[name] not in s and LEAD_OLD[name] in s:
                s = s.replace(LEAD_OLD[name], LEAD_NEW[name], 1)
                steps.append("лид")
            elif LEAD_NEW[name] not in s:
                print("  ВНИМАНИЕ: %s, прежний лид не найден" % name)

        base = LEAD_FR if name == "fr/index.html" else LEAD_NEW[name]
        if base in s and PORTS[name].strip() not in s:
            s = s.replace(base, base + PORTS[name], 1)
            steps.append("порты")

        s, done = meta(name, s)
        steps.extend(done)

        if s != orig:
            p.write_text(s)
            pages += 1
            print("  %s: %s" % (name, ", ".join(steps)))

    raw = I18N.read_text()
    moved = 0
    for old, new, tr in I18N_SWAPS:
        if '"%s":' % old not in raw:
            continue
        line = '"%s": {"fr": "%s", "es": "%s", "de": "%s"}' % (
            new, tr["fr"], tr["es"], tr["de"])
        raw = re.sub(r'"%s":\s*\{[^}]*\}' % re.escape(old), line, raw, count=1)
        moved += 1
    raw, lead_moved = i18n_lead(raw)
    if lead_moved:
        print("  i18n.json: лид заменён")
    if moved or lead_moved:
        json.loads(raw)          # не выпускаем сломанный словарь
        I18N.write_text(raw)
        print("  i18n.json: ключей заголовка заменено %d" % moved)

    print("главных поправлено: %d" % pages)
    return 0


if __name__ == "__main__":
    sys.exit(main())
