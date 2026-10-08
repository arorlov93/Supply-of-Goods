# -*- coding: utf-8 -*-
"""Сборка сайта: страницы, навигация на уже существующих файлах, sitemap."""
import os, re, sys, json, importlib
import gen_pages as G


# Выдача обрезает описание около 160 знаков и заголовок около 60. Тексты в
# content_*.py написаны для людей, здесь лежат укороченные варианты для сниппета.
DESC = {
 "about": "United States trading company. We buy in our own name, verify producers before "
          "quoting and deliver on agreed Incoterms.",
 "guides": "Plain answers to what comes up before a first order: Incoterms, landed price, "
           "supplier checks, letters of credit, HS codes.",
 "building-materials": "Stone, porcelain and ceramic tile, cement, insulation, sanitary ware "
           "and cable, bought against EN and ISO standards.",
 "industrial-equipment": "Production lines, compressors, pumps, generators and material "
           "handling, with mark, voltage and spares specified.",
 "tools-hardware": "Power and hand tools, abrasives, measuring instruments and fixings, to "
           "specification or to brand, with the safety marks.",
 "container-loading": "Container capacities, why dense cargo fills on weight, when LCL is "
           "false economy, and how consolidation keeps FCL economics.",
 "hs-code": "The importer of record is liable for the tariff code, not the seller who typed "
           "it. What a wrong one costs and how to fix it in advance.",
 "landed-price": "Every line between a factory price and your own gate: freight, surcharges, "
           "insurance, terminal handling, duty, broker, inland leg.",
 "verify-supplier": "Business licence, export right, scope of business and the bank account "
           "name: the checks that separate a factory from a trader.",
 "afrique-ouest": "Conteneurs frigorifiques vers le Togo et le B\u00e9nin : agr\u00e9ment de "
           "l\u2019\u00e9tablissement, d\u00e9coupes, cha\u00eene du froid, paiement.",
}
TITLE = {
 "veterinary-certificate": "Veterinary certificates for frozen meat | ISP Group",
}

CSS = open("fx.css", encoding="utf-8").read()
SITE = "site"
built = []


def write(spec, lang="en", extra_js=""):
    spec = dict(spec)
    if spec["slug"] in DESC: spec["desc"] = DESC[spec["slug"]]
    if spec["slug"] in TITLE: spec["title"] = TITLE[spec["slug"]]
    html = G.build(spec, extra_css=CSS, lang=lang)
    if extra_js:
        html = html.replace("</body>", extra_js + "\n</body>", 1)
    path = os.path.join(SITE, spec["slug"] + ".html")
    open(path, "w", encoding="utf-8").write(html)
    built.append(spec["slug"])
    return path


def retrofit_nav(paths):
    """Поменять шапку и подвал на уже собранных вручную страницах."""
    nav = G.navbar()
    foot = G.footer()
    for p in paths:
        s = open(p, encoding="utf-8").read()
        s = re.sub(r"<nav>.*?</nav>", lambda m: nav, s, count=1, flags=re.S)
        s = re.sub(r"<footer[^>]*>.*?</footer>", lambda m: foot, s, count=1, flags=re.S)
        # ссылки на форму запроса ведут теперь на страницу контактов
        s = s.replace('href="index.html#enquiry"', 'href="contact.html#enquiry"')
        open(p, "w", encoding="utf-8").write(s)
        print("   шапка обновлена:", p)


def hreflang(pairs, host):
    """Взаимные ссылки между языковыми версиями. Google требует, чтобы ссылка
    стояла с обеих сторон, иначе пара игнорируется целиком."""
    import re as _re
    for en, fr in pairs:
        tags = ('<link rel="alternate" hreflang="en" href="%s%s">\n'
                '<link rel="alternate" hreflang="fr" href="%s%s">\n'
                '<link rel="alternate" hreflang="x-default" href="%s%s">\n'
                % (host, "" if en == "index.html" else en, host, fr,
                   host, "" if en == "index.html" else en))
        for f in (en, fr):
            path = os.path.join(SITE, f)
            if not os.path.exists(path):
                print("   hreflang пропущен, нет файла:", f); continue
            t = open(path, encoding="utf-8").read()
            t = _re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n', "", t)
            t = t.replace('<meta property="og:type"', tags + '<meta property="og:type"', 1)
            open(path, "w", encoding="utf-8").write(t)
    print("   hreflang проставлен на парах:", len(pairs))


def pretty_urls(host):
    """Cloudflare Pages отдаёт /page.html как 308 на /page. Поэтому ссылки,
    canonical, og:url и hreflang должны сразу указывать на конечный адрес,
    иначе canonical сам оказывается редиректом."""
    import re as _re, glob as _glob
    files = _glob.glob(os.path.join(SITE, "*.html"))
    known = {os.path.basename(f) for f in files}

    def href(m):
        q, name, rest = m.group(1), m.group(2), m.group(3)
        if name not in known:
            return m.group(0)
        if name == "index.html":
            return 'href=%s/%s%s' % (q, rest, q)
        return 'href=%s%s%s%s' % (q, name[:-5], rest, q)

    for f in files:
        t = open(f, encoding="utf-8").read()
        t = _re.sub(r'href=(")([a-z0-9][a-z0-9\-]*\.html)((?:#[^"]*)?)\1', href, t)
        # абсолютные адреса в canonical, og:url, hreflang и структурных данных
        t = t.replace(host + "index.html", host)
        t = _re.sub(r'(%s)([a-z0-9][a-z0-9\-]*)\.html' % _re.escape(host), r"\1\2", t)
        # клавиатурный пропуск навигации и пометка текущего пункта меню
        if 'class="skip"' not in t:
            t = t.replace("<body>", '<body>\n<a class="skip" href="#main">Skip to content</a>', 1)
        t = t.replace("<main>", '<main id="main" tabindex="-1">', 1)
        slug = os.path.basename(f)[:-5]
        t = _re.sub(r'(<div class="navlinks" id="navmenu">)(.*?)(</div>)',
                    lambda m: m.group(1) + _re.sub(
                        r'<a href="(%s)">' % _re.escape(slug),
                        r'<a href="\1" aria-current="page">', m.group(2)) + m.group(3),
                    t, count=1, flags=_re.S)
        # Cloudflare по умолчанию подменяет почту на [email protected] и
        # прячет её за скриптом. Для B2B-контакта это вред: адрес перестают
        # видеть и посетитель без JS, и поисковик. Отключаем для всей страницы.
        # WebP на 28 % легче; og:image оставляем JPEG ради соцсетей
        t = _re.sub(r'(<img[^>]*src="media/[a-z0-9]+)\.jpg', r"\1.webp", t)
        if "<!--email_off-->" not in t:
            t = t.replace("<body>", "<body>\n<!--email_off-->", 1)
            t = t.replace("</body>", "<!--/email_off-->\n</body>", 1)
        open(f, "w", encoding="utf-8").write(t)
    print("   адреса без .html и email_off проставлены на", len(files), "страницах")


def sitemap(slugs, extra=()):
    rows = [(G.HOST, "1.0", "monthly")]
    for s in slugs:
        if s in ("index", "404"): continue
        pr = "0.9" if s in ("supply", "corridors", "guides", "contact", "about",
                            "services") else "0.8"
        rows.append((G.HOST + s, pr, "monthly"))
    for u, pr, c in extra: rows.append((u, pr, c))
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    seen = set()
    for u, pr, c in rows:
        if u in seen: continue
        seen.add(u)
        out.append('  <url><loc>%s</loc><lastmod>2026-10-08</lastmod>'
                   '<changefreq>%s</changefreq><priority>%s</priority></url>' % (u, c, pr))
    out.append("</urlset>")
    open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    return len(seen)
