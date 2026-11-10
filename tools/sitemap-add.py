# -*- coding: utf-8 -*-
"""Карта сайта: новые страницы с hreflang. Пункт 9 брифа от 10.11.2026.

Карта собирается шагом полной сборки, запускать которую нельзя, поэтому
новые адреса дописываются сюда отдельно. Для каждой страницы, у которой
есть четыре языковые версии, ставится полный набор xhtml:link, как уже
сделано у главной: без него Google считает версии дублями.

Запуск: python3.13 tools/sitemap-add.py
Повторный запуск ничего не меняет.
"""
import datetime, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
SM = SITE / "sitemap.xml"
HOST = "https://ispgroupgc.com"
LANGS = ("en", "fr", "es", "de")

# слаг -> приоритет
MULTI = {"chemicals": "0.9", "compliance": "0.6", "central-asia": "0.8"}


def url_for(slug, lg):
    return "%s/%s" % (HOST, slug) if lg == "en" else "%s/%s/%s" % (HOST, lg, slug)


def alts(slug):
    out = "".join('<xhtml:link rel="alternate" hreflang="%s" href="%s"/>'
                  % (lg, url_for(slug, lg)) for lg in LANGS)
    return out + ('<xhtml:link rel="alternate" hreflang="x-default" href="%s"/>'
                  % url_for(slug, "en"))


def main():
    if not SM.exists():
        print("  ВНИМАНИЕ: sitemap.xml не найден")
        return 1
    s = SM.read_text()
    today = datetime.date.today().isoformat()
    added = 0
    rows = []
    for slug, prio in MULTI.items():
        for lg in LANGS:
            loc = url_for(slug, lg)
            if "<loc>%s</loc>" % loc in s:
                continue
            rows.append('  <url><loc>%s</loc><lastmod>%s</lastmod>'
                        '<changefreq>monthly</changefreq><priority>%s</priority>%s</url>\n'
                        % (loc, today, prio, alts(slug)))
            added += 1
    if added:
        s = s.replace("</urlset>", "".join(rows) + "</urlset>", 1)
        SM.write_text(s)

    # проверка: файл должен остаться разбираемым XML
    import xml.etree.ElementTree as ET
    ET.fromstring(SM.read_text())
    total = len(re.findall(r"<loc>", SM.read_text()))
    print("  адресов добавлено: %d, всего в карте: %d" % (added, total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
