# -*- coding: utf-8 -*-
"""Пятый коридор: Центральная Азия и Каспий. Пункт 4 брифа от 10.11.2026.

Делает три вещи:
  * страницу /central-asia на четырёх языках, тем же способом, что и
    /chemicals: из готовой china.html с подменой шапки и подвала;
  * ссылку на неё в перечне коридоров на /corridors;
  * счётчик на /corridors: «4 corridors» становится «5 corridors».

Страница собрана на четырёх языках, потому что бриф требует четыре языка
для всех своих текстов, а этот коридор ведёт именно химию: с /chemicals
на него ссылка на том же языке.

Запуск: python3.13 tools/page-central-asia.py
Повторный запуск переписывает страницу тем же содержимым.
"""
import importlib.util, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
_spec = importlib.util.spec_from_file_location(
    "pagechem", pathlib.Path(__file__).parent / "page-chemicals.py")
pc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pc)

LANGS = ("en", "fr", "es", "de")
SLUG = "central-asia"
OUT = {k: (SLUG + ".html" if k == "en" else "%s/%s.html" % (k, SLUG)) for k in LANGS}
URL = {k: ("https://ispgroupgc.com/" + SLUG if k == "en"
           else "https://ispgroupgc.com/%s/%s" % (k, SLUG)) for k in LANGS}

NAME = {"en": "Central Asia &amp; Caspian", "fr": "Asie centrale et Caspienne",
        "es": "Asia Central y Caspio", "de": "Zentralasien und Kaspisches Meer"}

META = {
 "en": ("Central Asia and Caspian corridor | ISP Group LLC",
        "Chemicals and equipment from China and India to Kazakhstan, "
        "Uzbekistan, Turkmenistan, Azerbaijan, Kyrgyzstan and Mongolia, by "
        "rail through Khorgos and by sea through Turkmenbashi and Aktau."),
 "fr": ("Corridor Asie centrale et Caspienne | ISP Group LLC",
        "Produits chimiques et équipements de Chine et d’Inde vers le "
        "Kazakhstan, l’Ouzbékistan, le Turkménistan, l’Azerbaïdjan, le "
        "Kirghizistan et la Mongolie, par rail via Khorgos et par mer via "
        "Turkmenbachi et Aktaou."),
 "es": ("Corredor Asia Central y Caspio | ISP Group LLC",
        "Productos químicos y equipos desde China e India hacia Kazajistán, "
        "Uzbekistán, Turkmenistán, Azerbaiyán, Kirguistán y Mongolia, por "
        "ferrocarril vía Khorgos y por mar vía Turkmenbashi y Aktau."),
 "de": ("Korridor Zentralasien und Kaspisches Meer | ISP Group LLC",
        "Chemikalien und Ausrüstung aus China und Indien nach Kasachstan, "
        "Usbekistan, Turkmenistan, Aserbaidschan, Kirgisistan und der "
        "Mongolei, per Bahn über Khorgos und per See über Turkmenbaschi und "
        "Aktau."),
}

H1 = {
 "en": "Central Asia <em>and the Caspian</em>",
 "fr": "Asie centrale <em>et Caspienne</em>",
 "es": "Asia Central <em>y el Caspio</em>",
 "de": "Zentralasien <em>und Kaspisches Meer</em>",
}

BODY = {
 "en": "Chemicals and equipment from China and India to Central Asia and the "
       "Caspian by rail through Khorgos and by sea through Turkmenbashi and "
       "Aktau. Tenders of national oil, gas, power and mining companies, "
       "with the manufacturer’s authorization and the document set each "
       "customs office requires.",
 "fr": "Produits chimiques et équipements de Chine et d’Inde vers l’Asie "
       "centrale et la Caspienne, par rail via Khorgos et par mer via "
       "Turkmenbachi et Aktaou. Appels d’offres des compagnies nationales de "
       "pétrole, de gaz, d’électricité et des mines, avec l’autorisation du "
       "fabricant et le jeu de documents exigé par chaque bureau de douane.",
 "es": "Productos químicos y equipos desde China e India hacia Asia Central "
       "y el Caspio, por ferrocarril vía Khorgos y por mar vía Turkmenbashi "
       "y Aktau. Licitaciones de compañías nacionales de petróleo, gas, "
       "electricidad y minería, con la autorización del fabricante y el "
       "juego de documentos que exige cada aduana.",
 "de": "Chemikalien und Ausrüstung aus China und Indien nach Zentralasien "
       "und zum Kaspischen Meer, per Bahn über Khorgos und per See über "
       "Turkmenbaschi und Aktau. Ausschreibungen nationaler Öl-, Gas-, "
       "Energie- und Bergbauunternehmen, mit der Autorisierung des "
       "Herstellers und dem Dokumentensatz, den das jeweilige Zollamt "
       "verlangt.",
}

SUB = {
 "en": "Six destinations, two ways in: rail through Khorgos, sea through the Caspian.",
 "fr": "Six destinations, deux entrées : le rail par Khorgos, la mer par la Caspienne.",
 "es": "Seis destinos, dos entradas: ferrocarril por Khorgos, mar por el Caspio.",
 "de": "Sechs Ziele, zwei Wege: Bahn über Khorgos, See über das Kaspische Meer.",
}

COUNTRIES = ["Kazakhstan", "Uzbekistan", "Turkmenistan", "Azerbaijan",
             "Kyrgyzstan", "Mongolia"]
COUNTRIES_L = {
 "en": COUNTRIES,
 "fr": ["Kazakhstan", "Ouzbékistan", "Turkménistan", "Azerbaïdjan",
        "Kirghizistan", "Mongolie"],
 "es": ["Kazajistán", "Uzbekistán", "Turkmenistán", "Azerbaiyán",
        "Kirguistán", "Mongolia"],
 "de": ["Kasachstan", "Usbekistan", "Turkmenistan", "Aserbaidschan",
        "Kirgisistan", "Mongolei"],
}

FACTS_H = {"en": "Countries", "fr": "Pays", "es": "Países", "de": "Länder"}
WAYS_H = {"en": "Ways in", "fr": "Voies d’entrée", "es": "Vías de entrada",
          "de": "Zuwege"}
WAYS = {
 "en": "Rail through Khorgos; sea through Turkmenbashi and Aktau",
 "fr": "Rail via Khorgos ; mer via Turkmenbachi et Aktaou",
 "es": "Ferrocarril vía Khorgos; mar vía Turkmenbashi y Aktau",
 "de": "Bahn über Khorgos; See über Turkmenbaschi und Aktau",
}
CARGO_H = {"en": "Typical cargo", "fr": "Marchandises types",
           "es": "Carga habitual", "de": "Typische Ladung"}
CARGO = {
 "en": "Industrial chemicals, equipment, materials",
 "fr": "Produits chimiques industriels, équipements, matériaux",
 "es": "Productos químicos industriales, equipos, materiales",
 "de": "Industriechemikalien, Ausrüstung, Materialien",
}
LINK_CHEM = {"en": "Water treatment and oilfield chemicals",
             "fr": "Chimie de l’eau et des champs pétroliers",
             "es": "Química para agua y campos petroleros",
             "de": "Chemie für Wasseraufbereitung und Ölfeld"}

IMG = ("media/truck-road.01f52d2a.webp", "media/truck-road.6e089b93.jpg")
ALT = {"en": "Container trucks on a long-distance road",
       "fr": "Camions porte-conteneurs sur une route longue distance",
       "es": "Camiones portacontenedores en una carretera de larga distancia",
       "de": "Containerlastwagen auf einer Fernstraße"}


def hero(lg):
    home = "/" if lg == "en" else "/%s/" % lg
    chips = "".join('<span class="chip">%s</span>' % c for c in COUNTRIES_L[lg])
    return (
      '<header class="hero chero" id="top">\n  <div class="wrap chero-g">\n    <div>\n'
      '      <nav class="crumbs" aria-label="Breadcrumb"><a href="%s">ISP Group</a> '
      '<span>/</span> <b>%s</b></nav>\n'
      '      <h1>%s</h1>\n      <p class="sub">%s</p>\n'
      '      <div class="chips">%s</div>\n    </div>\n'
      '    <div class="heroside"><div class="shot"><span class="pz">'
      '<img src="/%s" srcset="/media/truck-road-349.60fbde29.webp 349w, /media/truck-road.01f52d2a.webp 900w" sizes="(max-width: 480px) 349px, (max-width: 900px) 731px, 509px" alt="%s" width="1040" height="1300" fetchpriority="high" decoding="async">'
      '</span></div></div>\n  </div>\n</header>'
      % (home, NAME[lg], H1[lg], SUB[lg], chips, IMG[0], ALT[lg]))


def main_html(lg):
    chem = "/chemicals" if lg == "en" else "/%s/chemicals" % lg
    facts = ("<table class=\"facts\"><tbody>"
             "<tr><th scope=\"row\">%s</th><td>%s</td></tr>"
             "<tr><th scope=\"row\">%s</th><td>%s</td></tr>"
             "<tr><th scope=\"row\">%s</th><td>%s</td></tr>"
             "</tbody></table>"
             % (FACTS_H[lg], ", ".join(COUNTRIES_L[lg]),
                WAYS_H[lg], WAYS[lg], CARGO_H[lg], CARGO[lg]))
    return """<main id="main" tabindex="-1">
<section data-reveal><div class="wrap">
  <div class="lede"><h2>%s</h2><p class="intro">%s</p></div>
  %s
  <div class="lanelinks" style="margin-top:48px">
    <a class="lanelink" href="%s"><b>%s</b><span>%s</span></a>
  </div>
</div></section>
</main>""" % (NAME[lg], BODY[lg], facts, chem, LINK_CHEM[lg], CARGO[lg])


def build(lg, shell):
    s = shell
    url = URL[lg]
    title, desc = META[lg]
    e = pc.esc
    s = re.sub(r"(?s)<title>.*?</title>", lambda _m: "<title>%s</title>" % e(title), s, count=1)
    for pat, val in (
        (r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % e(desc)),
        (r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s">' % url),
        (r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="%s">' % url),
        (r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="%s">' % e(title)),
        (r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="%s">' % e(desc)),
    ):
        s = re.sub(pat, lambda _m, v=val: v, s, count=1)
    s = re.sub(r'<html lang="[^"]*"', '<html lang="%s"' % lg, s, count=1)
    alts = "".join('<link rel="alternate" hreflang="%s" href="%s">\n' % (k, URL[k]) for k in LANGS)
    alts += '<link rel="alternate" hreflang="x-default" href="%s">' % URL["en"]
    s = re.sub(r'(?s)<link rel="alternate" hreflang="en"[^>]*>.*?'
               r'<link rel="alternate" hreflang="x-default"[^>]*>', lambda _m: alts, s, count=1)
    s = re.sub(r'(?s)<header class="hero chero".*?</header>', lambda _m: hero(lg), s, count=1)
    s = re.sub(r'(?s)<section class="glance">.*?</section>\s*', "", s, count=1)
    s = re.sub(r'(?s)<main id="main".*?</main>', lambda _m: main_html(lg), s, count=1)
    s = s.replace(' aria-current="page"', "")
    s = re.sub(r'(?s)<script type="application/ld\+json">.*?</script>\s*', "", s)
    s = pc.swap_chrome(s, lg)
    if lg != "en":
        s = pc.absolutize(s)
    return s


def corridors_page():
    """Ссылка и счётчик на /corridors."""
    p = SITE / "corridors.html"
    s = p.read_text()
    o = s
    link = ('<a class="lanelink" href="central-asia"><b>Central Asia &amp; Caspian</b>'
            '<span>Chemicals and equipment into Kazakhstan, Uzbekistan, '
            'Turkmenistan, Azerbaijan, Kyrgyzstan and Mongolia.</span></a>')
    if 'href="central-asia"' not in s:
        anchor = '<a class="lanelink" href="southern-africa">'
        if anchor not in s:
            print("  ВНИМАНИЕ: corridors.html, якорь перечня не найден")
        else:
            m = re.search(re.escape(anchor) + r'.*?</a>', s, re.S)
            s = s[:m.end()] + link + s[m.end():]
    s = s.replace("4 corridors", "5 corridors")
    s = s.replace("The four we quote now", "The five we quote now")
    s = s.replace("The four corridors", "The five corridors")
    s = s.replace("Four routes we quote end to end.", "Five routes we quote end to end.")
    s = s.replace("The four routes we quote end to end.", "The five routes we quote end to end.")
    if s != o:
        p.write_text(s)
        return True
    return False


def counters_elsewhere():
    """Та же четвёрка упоминается ссылками на других страницах."""
    n = 0
    for p in sorted(SITE.glob("*.html")):
        s = p.read_text(); o = s
        s = s.replace("The four routes we quote end to end.", "The five routes we quote end to end.")
        s = s.replace("Four routes we quote end to end.", "Five routes we quote end to end.")
        if s != o:
            p.write_text(s); n += 1
    return n


def main():
    shell = (SITE / "china.html").read_text()
    for lg in LANGS:
        p = SITE / OUT[lg]
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(build(lg, shell))
        print("  %s" % OUT[lg])
    print("  corridors.html: %s" % ("ссылка и счётчик" if corridors_page() else "без изменений"))
    print("  счётчик на других страницах: %d" % counters_elsewhere())
    return 0


if __name__ == "__main__":
    sys.exit(main())
