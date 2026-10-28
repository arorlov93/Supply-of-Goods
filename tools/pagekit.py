# -*- coding: utf-8 -*-
"""Сборка страницы из готового скелета.

Общий сборщик site уже есть, но пользоваться им нельзя: он берёт тексты
из content_*.py, а там лежат версии до правок внешнего аудита. Полная
пересборка вернула бы на about «in your own jurisdiction», а на services
«на пятую часть и больше».

Поэтому страницы-одиночки собираются иначе: берётся готовая about.html,
у неё заменяются голова и содержимое, а шапка, подвал, шрифты, стили,
поиск и счётчик остаются те же. Так новая страница не отстаёт от сайта
по виду и не тянет за собой старые тексты.

Модуль не запускается сам, его используют tools/offer-pages.py и
подобные.
"""
import json, os, pathlib, re

SITE = "site"
HOST = "https://ispgroupgc.com/"
DONOR = os.path.join(SITE, "about.html")

CTA = """<section data-reveal class="cta">
  <div class="wrap">
    <div class="lede">
      <h2>{h2}</h2>
      <p class="intro">{p}</p>
    </div>
    <div class="ctarow">
      <a class="btn" href="{href}">{btn}</a>
      <span class="mail">info@ispgroupgc.com</span>
    </div>
  </div>
</section>
</main>"""


def prose(blocks, start=0):
    """blocks: [("h2", текст) | ("p", ...) | ("ul", [...]) | ("note", ...) | ("raw", ...)]"""
    out, n, opened = [], start, False
    for kind, text in blocks:
        if kind == "h2":
            if opened:
                out.append("</div></div>")
            n += 1
            out.append('<div class="pblock"><span class="k">%02d</span>'
                       '<h2 id="s%d">%s</h2><div class="ptext">' % (n, n, text))
            opened = True
        elif kind == "raw":
            out.append(text)
        elif kind == "ul":
            out.append('<ul class="plist">%s</ul>'
                       % "".join("<li>%s</li>" % x for x in text))
        elif kind == "note":
            out.append('<p class="pnote">%s</p>' % text)
        else:
            out.append("<p>%s</p>" % text)
    if opened:
        out.append("</div></div>")
    return "".join(out), n


def toc(blocks):
    heads = [t for k, t in blocks if k == "h2"]
    if len(heads) < 3:
        return ""
    items = "".join('<li><a href="#s%d"><span>%02d</span>%s</a></li>' % (i, i, h)
                    for i, h in enumerate(heads, 1))
    return ('<nav class="toc" aria-label="On this page">'
            '<span class="eyebrow">On this page</span><ol>%s</ol></nav>' % items)


def crumbs(label):
    return ('<nav class="crumbs" aria-label="Breadcrumb">'
            '<a href="/">ISP Group</a> <span>/</span> <b>%s</b></nav>' % label)


def faq_html(items):
    return "".join("<details><summary>%s</summary><p>%s</p></details>" % q for q in items)


def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}}
                           for q, a in items]}


def crumb_ld(slug, label):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "ISP Group", "item": HOST},
                {"@type": "ListItem", "position": 2, "name": label, "item": HOST + slug}]}


def linkgrid(items):
    return '<div class="lanelinks">%s</div>' % "".join(
        '<a class="lanelink" href="%s"><b>%s</b><span>%s</span></a>' % x for x in items)


HEAD_META = """<meta name="description" content="{desc}">
<link rel="canonical" href="{host}{slug}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="ISP Group Global Commerce">
<meta property="og:url" content="{host}{slug}">
<meta property="og:title" content="{ogt}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{host}media/{ogi}">
<meta property="og:image:alt" content="{oga}">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#0b0e12">
<title>{title}</title>
"""


def build(spec):
    """spec: slug, title, desc, og_title, og_img, og_alt, crumb, h1, sub,
    chips, lede, blocks, faq, faq_h2, faq_sub, related, ld (доп. разметка),
    extra (кусок разметки после прозы)."""
    donor = open(DONOR, encoding="utf-8").read()

    head = donor[: donor.index("</head>")]
    a = head.index('<meta name="description"')
    b = head.index("</title>") + len("</title>") + 1
    # Имена снимков версионные: og:image должен указывать на существующий
    # файл, иначе карточка в соцсетях и в мессенджерах приходит пустой.
    og = spec.get("og_img", "terminal.jpg")
    if not re.fullmatch(r".+\.[0-9a-f]{8}\..+", og):
        base, _, ext = og.rpartition(".")
        found = sorted(pathlib.Path(SITE, "media").glob(f"{base}.*.{ext}"))
        if found:
            og = found[0].name
        else:
            raise SystemExit(f"нет файла для og:image: {spec['og_img']}")

    head = head[:a] + HEAD_META.format(
        desc=spec["desc"], host=HOST, slug=spec["slug"], ogt=spec["og_title"],
        ogi=og, oga=spec.get("og_alt", ""),
        title=spec["title"]) + head[b:]

    prefix = donor[donor.index("<body>"): donor.index('<header class="hero')]
    suffix = donor[donor.index("<footer"):]
    suffix = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', "",
                    suffix, flags=re.S)

    ld = list(spec.get("ld", []))
    if spec.get("faq"):
        ld.append(faq_ld(spec["faq"]))
    ld.append(crumb_ld(spec["slug"], spec["crumb"]))
    ldjs = "".join('<script type="application/ld+json">%s</script>\n'
                   % json.dumps(d, ensure_ascii=False) for d in ld)
    suffix = suffix.replace("<!--/email_off-->", ldjs + "<!--/email_off-->", 1)

    body, _ = prose(spec["blocks"])
    chips = "".join('<span class="chip">%s</span>' % c for c in spec.get("chips", []))

    out = [
        '<header class="hero chero" id="top">',
        '  <div class="wrap chero-g chero-1">',
        "    <div>",
        "      " + crumbs(spec["crumb"]),
        "      <h1>%s</h1>" % spec["h1"],
        '      <p class="sub">%s</p>' % spec["sub"],
        ('      <div class="chips">%s</div>' % chips) if chips else "",
        '      <div class="ctarow" style="margin-top:28px">'
        '<a class="btn" href="%s">%s</a></div>' % (spec.get("cta_href", "/contact#enquiry"),
                                                   spec.get("cta", "Request a quote")),
        "    </div>",
        "  </div>",
        "</header>",
        "",
        '<main id="main" tabindex="-1">',
        '<section data-reveal><div class="wrap">',
        '<div class="lede"><h2>%s</h2><p class="intro">%s</p></div>' % spec["lede"],
        toc(spec["blocks"]),
        '<div class="prose">%s</div>' % body,
        spec.get("extra", ""),
        "</div></section>",
    ]
    if spec.get("faq"):
        out.append('<section data-reveal id="faq"><div class="wrap">'
                   '<span class="eyebrow">Questions</span>'
                   '<div class="lede"><h2>%s</h2><p class="intro">%s</p></div>'
                   '<div style="margin-top:34px">%s</div></div></section>'
                   % (spec.get("faq_h2", "Questions on this"),
                      spec.get("faq_sub", "The ones we are asked most often."),
                      faq_html(spec["faq"])))
    if spec.get("related"):
        out.append('<section data-reveal><div class="wrap">'
                   '<span class="eyebrow">Keep reading</span>'
                   '<div class="lede"><h2>%s</h2><p class="intro">%s</p></div>%s'
                   "</div></section>"
                   % (spec["related"][0], spec["related"][1],
                      linkgrid(spec["related"][2])))

    # Призыв и закрытие main. Без них страница теряет единственную кнопку
    # внизу и остаётся с незакрытым main: браузер это чинит сам, разборщик
    # разметки нет.
    out.append(CTA.format(
        h2=spec.get("cta_h2", "Send a specification. Get a landed price."),
        p=spec.get("cta_p", "Product, quantity and destination port is enough to "
                   "start. If you only have a problem, describe it and we will write "
                   "the specification with you."),
        href=spec.get("cta_href", "/contact#enquiry"),
        btn=spec.get("cta", "Request a quote")))

    page = head + "</head>\n" + prefix + "\n".join(out) + "\n\n" + suffix
    page = page.replace(' aria-current="page"', "")
    path = os.path.join(SITE, spec["slug"] + ".html")
    open(path, "w", encoding="utf-8").write(page)
    return path
