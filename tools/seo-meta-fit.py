# -*- coding: utf-8 -*-
"""Подогнать заголовки и описания под то, что показывает выдача.

Google обрезает заголовок примерно на 60 знаках, описание примерно на
160. Обрезанное описание теряет хвост, а вместе с ним призыв и половину
смысла; обрезанный заголовок теряет название компании.

Было: восемь заголовков длиннее 60 и двадцать одно описание длиннее 160.
Длиннее всех испанская и французская химия, 260 знаков: в выдаче от них
остаётся меньше двух третей.

Правило правки: ключевые слова остаются в начале, уходит хвост и
перечисления, которые и так не поместятся. Ни одного нового утверждения
о компании здесь не появляется, только сокращение уже написанного.

Запуск: python3.13 tools/seo-meta-fit.py
Повторный запуск ничего не меняет.
"""
import pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
TMAX, DMAX = 60, 160

# страница -> новый заголовок
TITLES = {
 "index.html":
   "Industrial chemicals and equipment | ISP Group LLC",
 "chemicals.html":
   "Oilfield and water treatment chemicals | ISP Group",
 "fr/index.html":
   "Admissibilité avant le prix : Afrique de l’Ouest",
 "fr/chemicals.html":
   "Produits chimiques pour l’eau et le pétrole | ISP Group",
 "fr/compliance.html":
   "Sanctions et contrôle des exportations | ISP Group",
 "es/chemicals.html":
   "Químicos para tratamiento de agua y petróleo | ISP Group",
 "es/compliance.html":
   "Sanciones y control de exportaciones | ISP Group",
 "de/chemicals.html":
   "Wasseraufbereitungs- und Ölfeldchemikalien | ISP Group",
}

# страница -> новое описание
DESCR = {
 "index.html": None,
 "chemicals.html":
   "Phosphonates, scale and corrosion inhibitors, demulsifiers, PAC, ion "
   "exchange resins and molecular sieves from ISO-certified plants.",
 "compliance.html":
   "ISP Group LLC is a US company under OFAC sanctions and export control "
   "law. Every counterparty and end user is screened before payment.",
 "central-asia.html":
   "Chemicals and equipment from China and India to Kazakhstan, Uzbekistan, "
   "Turkmenistan and Azerbaijan, by rail via Khorgos and by sea via Aktau.",
 "experience.html":
   "Twenty years of our team’s supply work: container programmes out of "
   "China and discharge onto unequipped Russian shores.",
 "demurrage-detention.html":
   "What demurrage is, how the daily rate escalates, why free time is "
   "negotiated, and the US rules that let you refuse a late invoice.",
 "ispm-15.html":
   "Which wood packaging is in scope, how to read the IPPC mark, what HT, "
   "DH and MB mean, and what a US port does when the mark is wrong.",
 "admissibilite-cameroun.html":
   "BESC du CNCC et évaluation de la conformité avant embarquement de "
   "l’ANOR : qui délivre quoi pour un conteneur à destination de Douala.",
 "admissibilite-cote-divoire.html":
   "BSC, certificat de conformité avant embarquement, documents "
   "sanitaires : qui délivre quoi, et quand, pour un conteneur vers Abidjan.",
 "admissibilite-senegal.html":
   "BESC du COSEC, programme de vérification des importations, normes de "
   "l’ASN : qui délivre quoi pour un conteneur à destination de Dakar.",
 "fr/index.html":
   "Le dossier qui décide si un conteneur sort du port, pays par pays : "
   "Côte d’Ivoire, Sénégal, Cameroun. Nous travaillons contre documents.",
 "fr/chemicals.html":
   "Phosphonates, inhibiteurs d’entartrage et de corrosion, "
   "désémulsifiants, PAC, résines échangeuses d’ions et tamis moléculaires.",
 "fr/compliance.html":
   "ISP Group LLC est une société américaine soumise aux sanctions de "
   "l’OFAC. Chaque contrepartie et utilisateur final est contrôlé.",
 "fr/central-asia.html":
   "Produits chimiques et équipements de Chine et d’Inde vers le "
   "Kazakhstan, l’Ouzbékistan, le Turkménistan et l’Azerbaïdjan, par rail.",
 "es/index.html":
   "Una oferta de un productor que no puede enviar legalmente a su país no "
   "es una oferta. Compramos en nombre propio y entregamos en su puerto.",
 "es/chemicals.html":
   "Fosfonatos, inhibidores de incrustaciones y corrosión, "
   "desemulsionantes, PAC, resinas de intercambio iónico y tamices "
   "moleculares.",
 "es/compliance.html":
   "ISP Group LLC es una empresa estadounidense sujeta a las sanciones de "
   "la OFAC. Verificamos cada contraparte y usuario final.",
 "es/central-asia.html":
   "Productos químicos y equipos desde China e India hacia Kazajistán, "
   "Uzbekistán, Turkmenistán y Azerbaiyán, por ferrocarril vía Khorgos.",
 "de/index.html":
   "Ein Angebot von einem Hersteller, der nicht legal in Ihr Land liefern "
   "darf, ist kein Angebot. Wir kaufen im eigenen Namen und liefern.",
 "de/chemicals.html":
   "Phosphonate, Scale- und Korrosionsinhibitoren, Demulgatoren, PAC, "
   "Ionenaustauscherharze und Molekularsiebe aus ISO-zertifizierten Werken.",
 "de/compliance.html":
   "ISP Group LLC ist ein US-Unternehmen unter OFAC-Sanktions- und "
   "Exportkontrollrecht. Jede Gegenpartei wird vorab geprüft.",
 "de/central-asia.html":
   "Chemikalien und Ausrüstung aus China und Indien nach Kasachstan, "
   "Usbekistan, Turkmenistan und Aserbaidschan, per Bahn über Khorgos.",
}


def set_meta(s, name, value, prop=False):
    attr = "property" if prop else "name"
    rx = re.compile(r'(<meta %s="%s" content=")(.*?)(">)' % (attr, re.escape(name)),
                    re.S)
    if not rx.search(s):
        return s, False
    cur = rx.search(s).group(2)
    if cur == value:
        return s, False
    return rx.sub(lambda m: m.group(1) + value.replace("\\", "\\\\") + m.group(3),
                  s, count=1), True


def main():
    n = 0
    for rel, new in TITLES.items():
        p = SITE / rel
        s = p.read_text()
        m = re.search(r"<title>(.*?)</title>", s, re.S)
        if not m:
            print("  ВНИМАНИЕ: %s, нет title" % rel)
            continue
        if m.group(1).strip() != new:
            s = s[:m.start(1)] + new + s[m.end(1):]
            # og:title повторяет заголовок, иначе соцсети покажут старый
            s, _ = set_meta(s, "og:title", new, prop=True)
            p.write_text(s)
            n += 1

    for rel, new in DESCR.items():
        if new is None:
            continue
        p = SITE / rel
        s = p.read_text()
        s, a = set_meta(s, "description", new)
        s, b = set_meta(s, "og:description", new, prop=True)
        if a or b:
            p.write_text(s)
            n += 1
    print("страниц поправлено: %d" % n)

    # --- проверка: ничего не должно вылезать за лимиты
    bad = []
    for p in sorted(SITE.rglob("*.html")):
        s = p.read_text()
        rel = str(p.relative_to(SITE))
        if rel == "crm.html":
            continue                      # служебная, закрыта от индекса
        t = re.search(r"<title>(.*?)</title>", s, re.S)
        d = re.search(r'<meta name="description" content="(.*?)"', s, re.S)
        t = t.group(1).strip() if t else ""
        d = d.group(1).strip() if d else ""
        if len(t) > TMAX:
            bad.append("%s: заголовок %d" % (rel, len(t)))
        if len(d) > DMAX:
            bad.append("%s: описание %d" % (rel, len(d)))
        if not d:
            bad.append("%s: описания нет" % rel)
    if bad:
        print("НЕ ВЛЕЗАЕТ:")
        for x in bad:
            print("   ", x)
        return 1
    print("все заголовки до %d, все описания до %d" % (TMAX, DMAX))
    return 0


if __name__ == "__main__":
    sys.exit(main())
