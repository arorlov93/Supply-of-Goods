# -*- coding: utf-8 -*-
"""Страница /compliance на четырёх языках и ссылка на неё в подвале всех
страниц. Пункт 3 брифа от 10.11.2026.

Собирается тем же способом, что и /chemicals: из готовой china.html, с
подменой шапки и подвала на локальные. Вспомогательные функции берутся
из tools/page-chemicals.py, чтобы правило сборки было одно.

Про PDF. Кнопка ведёт на /ISP_GROUP_COMPLIANCE_POLICY.pdf, сам файл
делает tools/compliance-pdf.py. Подпись в нём НЕ ставится: по правилам
работы подпись за человека не ставится нигде и никогда, включая
государственные формы. В документе оставлено пустое поле для подписи,
подписывает его участник общества сам.

Запуск: python3.13 tools/page-compliance.py
Повторный запуск переписывает страницы тем же содержимым.
"""
import importlib.util, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

_spec = importlib.util.spec_from_file_location(
    "pagechem", pathlib.Path(__file__).parent / "page-chemicals.py")
pc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pc)

LANGS = ("en", "fr", "es", "de")
OUT = {"en": "compliance.html", "fr": "fr/compliance.html",
       "es": "es/compliance.html", "de": "de/compliance.html"}
URL = {k: ("https://ispgroupgc.com/compliance" if k == "en"
           else "https://ispgroupgc.com/%s/compliance" % k) for k in LANGS}
PDF = "/ISP_GROUP_COMPLIANCE_POLICY.pdf"

META = {
 "en": ("Sanctions and export control compliance | ISP Group LLC",
        "ISP Group LLC is a US company subject to US law, including OFAC "
        "sanctions and export control regulations. Every counterparty, its "
        "owners and the end user are screened before every quotation, "
        "contract and payment."),
 "fr": ("Conformité aux sanctions et au contrôle des exportations | ISP Group LLC",
        "ISP Group LLC est une société américaine soumise au droit des "
        "États-Unis, y compris aux sanctions de l’OFAC et au contrôle des "
        "exportations. Chaque contrepartie, ses propriétaires et "
        "l’utilisateur final sont contrôlés avant chaque cotation, contrat "
        "et paiement."),
 "es": ("Cumplimiento de sanciones y control de exportaciones | ISP Group LLC",
        "ISP Group LLC es una empresa estadounidense sujeta a la legislación "
        "de los Estados Unidos, incluidas las sanciones de la OFAC y el "
        "control de exportaciones. Cada contraparte, sus propietarios y el "
        "usuario final se verifican antes de cada cotización, contrato y "
        "pago."),
 "de": ("Sanktions- und Exportkontroll-Compliance | ISP Group LLC",
        "ISP Group LLC ist ein US-Unternehmen und unterliegt US-Recht, "
        "einschließlich OFAC-Sanktionen und Exportkontrolle. Jede "
        "Gegenpartei, ihre Eigentümer und der Endverwender werden vor jedem "
        "Angebot, Vertrag und jeder Zahlung geprüft."),
}

CRUMB = {"en": "Compliance", "fr": "Conformité", "es": "Cumplimiento",
         "de": "Compliance"}

H1 = {
 "en": "Sanctions and <em>export control</em>",
 "fr": "Sanctions et <em>contrôle des exportations</em>",
 "es": "Sanciones y <em>control de exportaciones</em>",
 "de": "Sanktionen und <em>Exportkontrolle</em>",
}

SUB = {
 "en": "What we check, when we check it, and what we will not do.",
 "fr": "Ce que nous vérifions, à quel moment, et ce que nous ne ferons pas.",
 "es": "Qué verificamos, cuándo lo verificamos y qué no haremos.",
 "de": "Was wir prüfen, wann wir es prüfen und was wir nicht tun.",
}

BODY = {
 "en": "ISP Group LLC is a US company subject to US law, including OFAC "
       "sanctions and export control regulations. We screen every "
       "counterparty, its owners and the end user against OFAC, UN, EU and "
       "UK lists before every quotation, contract and payment. We do not "
       "deal with sanctioned persons or comprehensively sanctioned "
       "territories, and we never misstate the origin, destination or end "
       "user of goods.",
 "fr": "ISP Group LLC est une société américaine soumise au droit des "
       "États-Unis, y compris aux sanctions de l’OFAC et à la réglementation "
       "sur le contrôle des exportations. Nous contrôlons chaque "
       "contrepartie, ses propriétaires et l’utilisateur final au regard des "
       "listes de l’OFAC, de l’ONU, de l’Union européenne et du Royaume-Uni "
       "avant chaque cotation, chaque contrat et chaque paiement. Nous ne "
       "traitons pas avec des personnes sanctionnées ni avec des territoires "
       "faisant l’objet de sanctions globales, et nous ne déclarons jamais "
       "faussement l’origine, la destination ou l’utilisateur final des "
       "marchandises.",
 "es": "ISP Group LLC es una empresa estadounidense sujeta a la legislación "
       "de los Estados Unidos, incluidas las sanciones de la OFAC y la "
       "normativa de control de exportaciones. Verificamos a cada "
       "contraparte, a sus propietarios y al usuario final contra las listas "
       "de la OFAC, la ONU, la Unión Europea y el Reino Unido antes de cada "
       "cotización, cada contrato y cada pago. No tratamos con personas "
       "sancionadas ni con territorios sujetos a sanciones integrales, y "
       "nunca declaramos falsamente el origen, el destino ni el usuario "
       "final de la mercancía.",
 "de": "ISP Group LLC ist ein US-Unternehmen und unterliegt US-Recht, "
       "einschließlich der OFAC-Sanktionen und der "
       "Exportkontrollvorschriften. Wir prüfen jede Gegenpartei, ihre "
       "Eigentümer und den Endverwender gegen die Listen von OFAC, UN, EU "
       "und Vereinigtem Königreich vor jedem Angebot, jedem Vertrag und "
       "jeder Zahlung. Wir handeln nicht mit sanktionierten Personen oder "
       "umfassend sanktionierten Gebieten, und wir machen niemals falsche "
       "Angaben zu Ursprung, Bestimmungsort oder Endverwender der Ware.",
}

BTN = {
 "en": "Download our Compliance Policy (PDF)",
 "fr": "Télécharger notre politique de conformité (PDF)",
 "es": "Descargar nuestra política de cumplimiento (PDF)",
 "de": "Unsere Compliance-Richtlinie herunterladen (PDF)",
}

DETAILS_H = {
 "en": "Company details", "fr": "Identification de la société",
 "es": "Datos de la empresa", "de": "Unternehmensangaben",
}
ROWS = {
 "en": [("Legal name", "ISP GROUP LLC"),
        ("Florida Document No.", "M26000003981"),
        ("EIN", "38-4380828"),
        ("UEI", "WA46PAMTYMQ7"),
        ("CAGE", "217F4"),
        ("Registered office", "16395 Biscayne Blvd, North Miami Beach, FL 33160, USA")],
 "fr": [("Raison sociale", "ISP GROUP LLC"),
        ("N° de document, Floride", "M26000003981"),
        ("EIN", "38-4380828"),
        ("UEI", "WA46PAMTYMQ7"),
        ("CAGE", "217F4"),
        ("Siège social", "16395 Biscayne Blvd, North Miami Beach, FL 33160, USA")],
 "es": [("Razón social", "ISP GROUP LLC"),
        ("N.º de documento, Florida", "M26000003981"),
        ("EIN", "38-4380828"),
        ("UEI", "WA46PAMTYMQ7"),
        ("CAGE", "217F4"),
        ("Domicilio social", "16395 Biscayne Blvd, North Miami Beach, FL 33160, USA")],
 "de": [("Firmenname", "ISP GROUP LLC"),
        ("Dokument-Nr. Florida", "M26000003981"),
        ("EIN", "38-4380828"),
        ("UEI", "WA46PAMTYMQ7"),
        ("CAGE", "217F4"),
        ("Sitz", "16395 Biscayne Blvd, North Miami Beach, FL 33160, USA")],
}

CSS = """
/* страница соответствия */
.comp-body{max-width:66ch;font-size:clamp(1rem,1.1vw,1.12rem);line-height:1.7}
table.cdet{width:100%;max-width:720px;border-collapse:collapse;
  margin-top:clamp(22px,3vh,32px);font-size:.95rem}
table.cdet th{text-align:left;font-weight:400;color:var(--ink-2);
  padding:12px 20px 12px 0;border-bottom:1px solid var(--rule);white-space:nowrap;
  vertical-align:top}
table.cdet td{padding:12px 0;border-bottom:1px solid var(--rule);
  font-family:var(--mono,ui-monospace,monospace);font-size:.92em}
"""


def hero(lg):
    home = "/" if lg == "en" else "/%s/" % lg
    return (
      '<header class="hero chero" id="top">\n  <div class="wrap chero-g">\n    <div>\n'
      '      <nav class="crumbs" aria-label="Breadcrumb"><a href="%s">ISP Group</a> '
      '<span>/</span> <b>%s</b></nav>\n'
      '      <h1>%s</h1>\n      <p class="sub">%s</p>\n'
      '      <div class="ctarow" style="margin-top:28px">'
      '<a class="btn" href="%s" download>%s</a></div>\n'
      '    </div>\n    <div class="heroside"></div>\n  </div>\n</header>'
      % (home, CRUMB[lg], H1[lg], SUB[lg], PDF, BTN[lg]))


def main_html(lg):
    rows = "".join("<tr><th scope=\"row\">%s</th><td>%s</td></tr>" % r
                   for r in ROWS[lg])
    return """<main id="main" tabindex="-1">
<section data-reveal><div class="wrap">
  <p class="comp-body">%s</p>
  <div class="lede" style="margin-top:56px"><h2>%s</h2></div>
  <table class="cdet"><tbody>%s</tbody></table>
  <p style="margin-top:34px"><a class="btn" href="%s" download>%s</a></p>
</div></section>
</main>""" % (BODY[lg], DETAILS_H[lg], rows, PDF, BTN[lg])


def build(lg, shell):
    s = shell
    url = URL[lg]
    title, desc = META[lg]
    e = pc.esc
    s = re.sub(r"(?s)<title>.*?</title>", lambda _m: "<title>%s</title>" % e(title), s, count=1)
    s = re.sub(r'<meta name="description" content="[^"]*">',
               lambda _m: '<meta name="description" content="%s">' % e(desc), s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">',
               lambda _m: '<link rel="canonical" href="%s">' % url, s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*">',
               lambda _m: '<meta property="og:url" content="%s">' % url, s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">',
               lambda _m: '<meta property="og:title" content="%s">' % e(title), s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">',
               lambda _m: '<meta property="og:description" content="%s">' % e(desc), s, count=1)
    s = re.sub(r'<html lang="[^"]*"', '<html lang="%s"' % lg, s, count=1)

    alts = "".join('<link rel="alternate" hreflang="%s" href="%s">\n' % (k, URL[k])
                   for k in LANGS)
    alts += '<link rel="alternate" hreflang="x-default" href="%s">' % URL["en"]
    s = re.sub(r'(?s)<link rel="alternate" hreflang="en"[^>]*>.*?'
               r'<link rel="alternate" hreflang="x-default"[^>]*>',
               lambda _m: alts, s, count=1)

    s = re.sub(r'(?s)<header class="hero chero".*?</header>', lambda _m: hero(lg), s, count=1)
    s = re.sub(r'(?s)<section class="glance">.*?</section>\s*', "", s, count=1)
    s = re.sub(r'(?s)<main id="main".*?</main>', lambda _m: main_html(lg), s, count=1)
    s = s.replace(' aria-current="page"', "")
    s = re.sub(r'(?s)<script type="application/ld\+json">.*?</script>\s*', "", s)
    if CSS.strip() not in s:
        s = s.replace("</head>", "<style>%s</style>\n</head>" % CSS, 1)
    s = pc.swap_chrome(s, lg)
    if lg != "en":
        s = pc.absolutize(s)
    return s


# -------------------------------------------------- ссылка в подвале всех страниц
FOOT_LINK = {
 "en": "Compliance", "fr": "Conformité", "es": "Cumplimiento", "de": "Compliance",
}


def footer_links():
    """Ссылка встаёт в нижнюю строку подвала, рядом с Privacy и Terms."""
    n = 0
    for p in sorted(SITE.glob("*.html")) + sorted(SITE.glob("*/*.html")):
        s = p.read_text()
        lg = "en"
        m = re.search(r'<html lang="([a-z]{2})"', s)
        if m and m.group(1) in LANGS:
            lg = m.group(1)
        href = "/compliance" if lg == "en" else "/%s/compliance" % lg
        link = '<a href="%s" style="display:inline">%s</a>' % (href, FOOT_LINK[lg])
        if link in s:
            continue
        # якорь: ссылка на условия в нижней строке подвала
        m = re.search(r'<a href="(/?terms)"([^>]*)>([^<]*)</a>', s)
        if not m:
            continue
        s = s[:m.end()] + link + s[m.end():]
        p.write_text(s)
        n += 1
    return n


def main():
    shell = (SITE / "china.html").read_text()
    for lg in LANGS:
        p = SITE / OUT[lg]
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(build(lg, shell))
        print("  %s" % OUT[lg])
    n = footer_links()
    print("ссылка в подвале добавлена на страниц: %d" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
