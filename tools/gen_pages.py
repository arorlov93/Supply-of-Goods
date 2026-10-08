# -*- coding: utf-8 -*-
"""Общий сборщик страниц сайта.

Шапка, подвал, шрифты и стили берутся из index.html, поэтому правка оформления
делается в одном месте и не расходится по тридцати файлам. Содержание страниц
лежит в отдельных модулях content_*.py: генератор ничего не знает про тексты.
"""
import re, json, html, os

SITE = "site"
HOST = "https://ispgroupgc.com/"

# ─── навигация: одно определение на весь сайт ──────────────────────────────
NAV = [("What we supply", "supply.html"),
       ("Corridors",      "corridors.html"),
       ("Guides",         "guides.html"),
       ("About",          "about.html"),
       ("Contact",        "contact.html")]

NAV_FR = [("Afrique de l\'Ouest", "afrique-ouest.html"),
          ("D\u00e9coupes",         "decoupes-volaille.html"),
          ("Certificat",           "certificat-veterinaire.html"),
          ("Contact",              "contact-fr.html"),
          ("English",              "index.html")]

CORRIDORS = [("china.html",           "China &rarr; worldwide"),
             ("turkiye.html",         "T&uuml;rkiye &rarr; United States"),
             ("west-africa.html",     "Americas &amp; EU &rarr; West Africa"),
             ("southern-africa.html", "Intra-Africa")]

ICON = ("<link rel=\"icon\" href=\"data:image/svg+xml,"
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'>"
        "<rect width='64' height='64' rx='12' fill='%230b4a40'/>"
        "<text x='32' y='43' font-family='Georgia,serif' font-size='30' font-weight='400'"
        " fill='%23e8d9b4' text-anchor='middle'>IG</text></svg>\">")


def assets():
    s = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
    return s[s.index('<link rel="preconnect"'):s.index("</head>")]


def navbar(lang="en"):
    home = "index.html" if lang == "en" else "index-fr.html"
    items = "".join('      <a href="%s">%s</a>\n' % (h, t)
                     for t, h in (NAV if lang == "en" else NAV_FR))
    quote = "Request a " if lang == "en" else "Demander un "
    word = "quote" if lang == "en" else "devis"
    anchor = "contact.html#enquiry" if lang == "en" else "contact-fr.html#enquiry"
    return ('<nav>\n  <div class="wrap navin">\n'
            '    <a class="logo" href="%s">ISP Group <em>Global Commerce</em></a>\n'
            '    <button class="navtoggle" id="navtoggle" type="button"\n'
            '      aria-expanded="false" aria-controls="navmenu" aria-label="Menu">'
            '<span></span></button>\n'
            '    <div class="navlinks" id="navmenu">\n%s    </div>\n'
            '    <a class="btn" href="%s">'
            '<span class="btn-long">%s</span>%s</a>\n'
            '  </div>\n</nav>' % (home, items, anchor, quote, word))


FOOT_FR = """<footer>
  <div class="wrap">
    <dl class="fgrid">
      <div><dt>Soci&eacute;t&eacute;</dt><dd>ISP GROUP LLC<br><span style="color:var(--ink-2)">&Eacute;tats-Unis</span></dd></div>
      <div><dt>Courriel</dt><dd><a href="mailto:info@ispgroupgc.com">info@ispgroupgc.com</a></dd></div>
      <div><dt>Si&egrave;ge</dt><dd>16395 Biscayne Blvd<br><span style="color:var(--ink-2)">North Miami Beach, FL 33160<br>&Eacute;tats-Unis</span></dd></div>
      <div><dt>Pages</dt><dd style="line-height:1.95"><a href="afrique-ouest.html" style="display:block">Afrique de l&rsquo;Ouest</a><a href="decoupes-volaille.html" style="display:block">D&eacute;coupes de volaille</a><a href="certificat-veterinaire.html" style="display:block">Certificat v&eacute;t&eacute;rinaire</a></dd></div>
      <div><dt>English</dt><dd style="line-height:1.95"><a href="index.html" style="display:block">Full site in English</a><a href="guides.html" style="display:block">Guides</a></dd></div>
    </dl>
    <p class="fbottom">ISP GROUP LLC &middot; Global Commerce &middot; Sourcing, n&eacute;goce et
      approvisionnement international en mati&eacute;riaux, produits et &eacute;quipements industriels.</p>
  </div>
</footer>"""


def footer(lang="en"):
    if lang != "en":
        return FOOT_FR
    cor = "".join('<a href="%s" style="display:block">%s</a>' % (h, t) for h, t in CORRIDORS)
    return """<footer>
  <div class="wrap">
    <dl class="fgrid">
      <div><dt>Entity</dt><dd>ISP GROUP LLC<br><span style="color:var(--ink-2)">United States</span></dd></div>
      <div><dt>Email</dt><dd><a href="mailto:info@ispgroupgc.com">info@ispgroupgc.com</a></dd></div>
      <div><dt>Registered office</dt><dd>16395 Biscayne Blvd<br><span style="color:var(--ink-2)">North Miami Beach, FL 33160<br>United States</span></dd></div>
      <div><dt>Corridors</dt><dd style="line-height:1.95">%s</dd></div>
      <div><dt>Reading</dt><dd style="line-height:1.95"><a href="guides.html" style="display:block">Guides</a><a href="experience.html" style="display:block">Twenty years of supply work</a><a href="supply.html" style="display:block">What we supply</a></dd></div>
    </dl>
    <p class="credits">Photography: pipe by JWPhotowerks; straddle carrier by Lars K. Jensen (CC BY).
      All other images CC0 or public domain. Full list with links in media/CREDITS.json.</p>
    <p class="fbottom">ISP GROUP LLC &middot; Global Commerce &middot; International sourcing,
      trading and supply of materials, products and industrial equipment.</p>
  </div>
</footer>""" % cor


FXJS = open("fx.js").read() if os.path.exists("fx.js") else ""


def plain(s):
    return html.unescape(re.sub("<[^>]+>", "", s))


def crumbs(trail):
    """trail: [(подпись, ссылка или None), ...], последний элемент без ссылки."""
    out = []
    for i, (label, href) in enumerate(trail):
        if i: out.append("<span>/</span>")
        out.append('<a href="%s">%s</a>' % (href, label) if href else "<b>%s</b>" % label)
    return '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % " ".join(out)


def prose(blocks):
    """blocks: [("h2", текст) | ("p", текст) | ("ul", [пункты]) | ("note", текст)]"""
    out, n, opened = [], 0, False
    for kind, text in blocks:
        if kind == "h2":
            if opened: out.append("</div></div>")
            n += 1
            out.append('<div class="pblock"><span class="k">%02d</span><h2>%s</h2>'
                       '<div class="ptext">' % (n, text))
            opened = True
        elif kind == "raw":
            out.append(text)
        elif kind == "ul":
            out.append("<ul class=\"plist\">%s</ul>" % "".join("<li>%s</li>" % x for x in text))
        elif kind == "note":
            out.append('<p class="pnote">%s</p>' % text)
        else:
            out.append("<p>%s</p>" % text)
    if opened: out.append("</div></div>")
    return "".join(out)


def faq_html(items):
    return "".join("<details><summary>%s</summary><p>%s</p></details>" % (q, a)
                   for q, a in items)


def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}}
                           for q, a in items]}


def crumb_ld(trail, url):
    items = []
    for i, (label, href) in enumerate(trail):
        items.append({"@type": "ListItem", "position": i + 1, "name": plain(label),
                      "item": HOST + (href if href else url.rsplit("/", 1)[-1])})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": items}


def linkgrid(items):
    """items: [(href, заголовок, подпись)]"""
    return '<div class="lanelinks">%s</div>' % "".join(
        '<a class="lanelink" href="%s"><b>%s</b><span>%s</span></a>' % x for x in items)


def factcard(title, rows):
    body = "".join('<tr><th scope="row">%s</th><td>%s</td></tr>' % r for r in rows)
    return ('<aside class="factcard"><span class="eyebrow">%s</span>'
            '<table class="facts"><tbody>%s</tbody></table></aside>' % (title, body))


CTA_FR = """<section class="cta">
  <div class="wrap">
    <span class="eyebrow">Pour commencer</span>
    <div class="lede">
      <h2>Envoyez un cahier des charges. Recevez un prix rendu.</h2>
      <p class="intro">Le produit, la quantit&eacute; et le port de destination suffisent pour
        d&eacute;marrer. Si vous n&rsquo;avez qu&rsquo;un probl&egrave;me &agrave; r&eacute;soudre,
        d&eacute;crivez-le et nous r&eacute;digerons le cahier des charges avec vous.</p>
    </div>
    <div class="ctarow">
      <a class="btn" href="contact-fr.html#enquiry">Demander un devis</a>
      <span class="mail">info@ispgroupgc.com</span>
    </div>
  </div>
</section>"""

CTA = """<section class="cta">
  <div class="wrap">
    <span class="eyebrow">Get started</span>
    <div class="lede">
      <h2>Send a specification. Get a landed price.</h2>
      <p class="intro">Product, quantity and destination port is enough to start. If you only
        have a problem, describe it and we will write the specification with you.</p>
    </div>
    <div class="ctarow">
      <a class="btn" href="contact.html#enquiry">Request a quote</a>
      <span class="mail">info@ispgroupgc.com</span>
    </div>
  </div>
</section>"""


def build(spec, extra_css="", lang="en"):
    """spec — словарь страницы, см. content_*.py."""
    slug = spec["slug"]
    url = HOST + ("" if slug == "index" else slug + ".html")
    img = spec.get("img")
    ld = list(spec.get("ld", []))
    if spec.get("faq"): ld.append(faq_ld(spec["faq"]))
    if spec.get("trail"): ld.append(crumb_ld(spec["trail"], url))
    ldjs = "".join('<script type="application/ld+json">%s</script>\n'
                   % json.dumps(d, ensure_ascii=False) for d in ld)

    hero_right = spec.get("hero_right", "")
    body = ['<header class="hero chero" id="top">',
            '  <div class="wrap chero-g%s">' % ("" if hero_right else " chero-1"),
            "    <div>",
            "      " + (crumbs(spec["trail"]) if spec.get("trail")
                        else '<span class="eyebrow">%s</span>' % spec.get("eyebrow", "")),
            "      <h1>%s</h1>" % spec["h1"],
            '      <p class="sub">%s</p>' % spec["sub"]]
    if spec.get("chips"):
        body.append('      <div class="chips">%s</div>' %
                    "".join('<span class="chip">%s</span>' % c for c in spec["chips"]))
    cta1 = ('<a class="btn" href="contact.html#enquiry">Request a quote</a>' if lang == "en"
            else '<a class="btn" href="contact-fr.html#enquiry">Demander un devis</a>')
    body.append('      <div class="ctarow" style="margin-top:28px">' + cta1
                + spec.get("hero_cta", "") + "</div>")
    body.append("    </div>")
    if hero_right: body.append("    " + hero_right)
    body.append("  </div>\n</header>\n\n<main>")

    if img:
        f, w, h, alt, cap = img
        body.append('<section><div class="wrap">'
                    '<figure class="mediafig" style="margin-bottom:44px">'
                    '<div class="shot"><span class="pz"><img src="media/%s" width="%d" '
                    'height="%d" loading="lazy" alt="%s"></span></div>'
                    '<figcaption>%s</figcaption></figure>' % (f, w, h, alt, cap))
    else:
        body.append('<section><div class="wrap">')

    if spec.get("lede"):
        body.append('<div class="lede"><h2>%s</h2><p class="intro">%s</p></div>' % spec["lede"])
    if spec.get("body"):
        body.append('<div class="prose">%s</div>' % prose(spec["body"]))
    body.append(spec.get("tail", ""))
    body.append("</div></section>")

    if spec.get("faq"):
        body.append('<section id="faq"><div class="wrap">'
                    '<span class="eyebrow">Questions</span>'
                    '<div class="lede"><h2>%s</h2><p class="intro">%s</p></div>'
                    '<div style="margin-top:34px">%s</div></div></section>'
                    % (spec.get("faq_h2", "Questions we are asked"),
                       spec.get("faq_sub", "The answers we give on a first call."),
                       faq_html(spec["faq"])))

    if spec.get("related"):
        body.append('<section><div class="wrap"><span class="eyebrow">%s</span>'
                    '<div class="lede"><h2>%s</h2><p class="intro">%s</p></div>%s'
                    "</div></section>"
                    % (spec.get("related_eyebrow", "Keep reading"),
                       spec["related"][0], spec["related"][1],
                       linkgrid(spec["related"][2])))

    body.append(CTA if lang == "en" else CTA_FR)
    body.append("</main>")

    og_img = HOST + "media/" + (img[0] if img else "terminal.jpg")
    alts = spec.get("alts", "")
    return """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
{alts}<meta property="og:type" content="article">
<meta property="og:site_name" content="ISP Group Global Commerce">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{ogt}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{ogi}">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#eef1ef">
{icon}
<title>{title}</title>
{assets}
<style>{css}</style>
</head>
<body>
{nav}

{body}

{foot}
{ld}{fx}</body>
</html>
""".format(lang=lang, desc=spec["desc"], url=url, alts=alts, ogt=plain(spec["h1"]),
           ogi=og_img, robots=spec.get("robots", "index,follow,max-image-preview:large"),
           icon=ICON, title=spec["title"], assets=assets(), css=extra_css,
           nav=navbar(lang), body="\n".join(body), foot=footer(lang), ld=ldjs, fx=FXJS)
