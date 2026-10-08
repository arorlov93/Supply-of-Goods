# -*- coding: utf-8 -*-
"""Сборка сайта: страницы, навигация на уже существующих файлах, sitemap."""
import os, re, sys, json, importlib
import gen_pages as G

CSS = open("fx.css", encoding="utf-8").read()
SITE = "site"
built = []


def write(spec, lang="en", extra_js=""):
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


def sitemap(slugs, extra=()):
    rows = [(G.HOST, "1.0", "monthly")]
    for s in slugs:
        if s in ("index", "404"): continue
        pr = "0.9" if s in ("supply", "corridors", "guides", "contact", "about",
                            "services") else "0.8"
        rows.append((G.HOST + s + ".html", pr, "monthly"))
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
