# -*- coding: utf-8 -*-
"""Вывести три новые страницы из слепой зоны поиска.

Страницы /chemicals, /compliance и /central-asia собраны отдельным
прогоном и в общую обвязку сайта не попали. Для поиска это значит
следующее.

1. На /chemicals ведут две внутренние ссылки, на /central-asia одна, на
   /fr/central-asia ни одной. Для сравнения: на /china их 68, на
   /corridors 78. Страница, на которую никто не ссылается, получает долю
   веса, близкую к нулю, и обходится роботом в последнюю очередь.

2. Нет тегов hreflang. Четыре языковые версии одного текста без них
   считаются дублями, и в выдачу попадает одна, выбранная не нами.
   В карте сайта hreflang есть, но карта это подсказка, а теги на
   странице сигнал прямой.

3. Нет BreadcrumbList. Это та разметка, из-за которой в выдаче под
   заголовком показывается путь, а не голый адрес.

Что делает инструмент:

   футер, блок Supply / Fournitures / Suministros / Lieferungen
       + ссылка на /chemicals первым пунктом
   футер, блок Corridors
       + ссылка на /central-asia пятым коридором
   карточки коридоров на четырёх страницах коридоров
       + карточка Central Asia & Caspian
   /supply, блок категорий
       + карточка промышленной химии
   двенадцать новых страниц
       + полный набор hreflang и BreadcrumbList

Запуск: python3.13 tools/seo-newpages.py
Повторный запуск ничего не меняет.
"""
import json, pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
HOST = "https://ispgroupgc.com"
LANGS = ("en", "fr", "es", "de")

# --- названия на четырёх языках
CHEM_T = {"en": "Industrial chemicals", "fr": "Produits chimiques",
          "es": "Productos químicos", "de": "Industriechemikalien"}
CA_T = {"en": "Central Asia &amp; Caspian", "fr": "Asie centrale et Caspienne",
        "es": "Asia Central y Caspio", "de": "Zentralasien und Kaspisches Meer"}
CA_SUB = {
 "en": "Chemicals and equipment from China and India to Central Asia and the "
       "Caspian, by rail and by road.",
 "fr": "Produits chimiques et équipements de Chine et d’Inde vers l’Asie "
       "centrale et la Caspienne, par rail et par route.",
 "es": "Productos químicos y equipos desde China e India hacia Asia Central "
       "y el Caspio, por ferrocarril y por carretera.",
 "de": "Chemikalien und Ausrüstung aus China und Indien nach Zentralasien "
       "und zum Kaspischen Meer, per Bahn und Straße.",
}
CHEM_SUB = {
 "en": "Water treatment, oilfield and process chemicals, with COA, TDS and "
       "SDS for every batch.",
 "fr": "Produits chimiques pour le traitement de l’eau, les champs "
       "pétroliers et les procédés, avec COA, TDS et FDS pour chaque lot.",
 "es": "Productos químicos para tratamiento de agua, campos petroleros y "
       "procesos, con COA, TDS y SDS en cada lote.",
 "de": "Chemikalien für Wasseraufbereitung, Ölfeld und Prozesse, mit COA, "
       "TDS und SDB zu jeder Charge.",
}
# заголовки блока Supply в футере локалей
SUPPLY_H = {"en": "Supply", "fr": "Fournitures", "es": "Suministro",
            "de": "Lieferprogramm"}
# первая ссылка этого блока, перед которой встаёт химия
FIRST = {"en": '<a href="building-materials">Building materials</a>',
         "fr": '<a href="/building-materials">Matériaux de construction</a>',
         "es": '<a href="/building-materials">Materiales de construcci\u00f3n</a>',
         "de": '<a href="/building-materials">Baustoffe</a>'}

# страницы, у которых есть все четыре языковые версии
MULTI = ("chemicals", "compliance", "central-asia")
CRUMB2 = {"en": ("Corridors", "Supply"), "fr": ("Corridors", "Fournitures"),
          "es": ("Corredores", "Suministros"), "de": ("Korridore", "Lieferungen")}


def url(slug, lg):
    return "%s/%s" % (HOST, slug) if lg == "en" else "%s/%s/%s" % (HOST, lg, slug)


def path_of(slug, lg):
    return SITE / ("%s.html" % slug if lg == "en" else "%s/%s.html" % (lg, slug))


def lang_of(p):
    rel = str(p.relative_to(SITE))
    return rel.split("/")[0] if rel[:2] in ("fr", "es", "de") and "/" in rel else "en"


# ---------------------------------------------------------------- hreflang
def hreflang(slug, lg, s):
    if 'hreflang="x-default"' in s:
        return s
    tags = "".join('<link rel="alternate" hreflang="%s" href="%s">' % (l, url(slug, l))
                   for l in LANGS)
    tags += '<link rel="alternate" hreflang="x-default" href="%s">' % url(slug, "en")
    return s.replace("</head>", tags + "\n</head>", 1)


# -------------------------------------------------------------- breadcrumbs
# Середина цепочки у каждой страницы своя. /chemicals это товарная
# категория и ведёт от раздела поставок, /central-asia это коридор и ведёт
# от раздела коридоров. У /compliance промежуточного раздела нет вообще,
# поэтому цепочка из двух звеньев, а не из трёх с выдуманной серединой.
HUB = {
 "chemicals": {"en": ("Supply", HOST + "/supply")},
 "central-asia": {"en": ("Corridors", HOST + "/corridors")},
}


def crumbs(slug, lg, s):
    # свою прежнюю разметку снимаем и ставим заново
    s = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema\.org",'
               r' "@type": "BreadcrumbList".*?</script>\n?', "", s, flags=re.S)
    m = re.search(r"<title>(.*?)</title>", s, re.S)
    name = re.sub(r"\s*\|\s*ISP Group LLC\s*$", "", (m.group(1).strip() if m else slug))
    home = HOST + "/" if lg == "en" else "%s/%s/" % (HOST, lg)
    items = [{"@type": "ListItem", "position": 1,
              "name": "ISP Group Global Commerce", "item": home}]
    # Промежуточное звено ставится только там, где раздел существует.
    # В локалях страниц /supply и /corridors нет, и подставлять вместо них
    # локальную главную нельзя: получилось бы два звена с одним адресом.
    hub = HUB.get(slug, {}).get(lg)
    if hub:
        items.append({"@type": "ListItem", "position": 2,
                      "name": hub[0], "item": hub[1]})
    items.append({"@type": "ListItem", "position": len(items) + 1,
                  "name": name, "item": url(slug, lg)})
    data = {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": items}
    tag = '<script type="application/ld+json">%s</script>\n' % json.dumps(
        data, ensure_ascii=False)
    return s.replace("</body>", tag + "</body>", 1)


# ------------------------------------------------------------------- футеры
def foot_supply(s, lg):
    """Химия и пятый коридор в блоке товарных категорий футера.

    В локалях ссылка ведёт на локальную страницу, а не на английскую:
    у /chemicals и /central-asia есть все четыре языковые версии, и
    отправлять француза на английский текст незачем.
    """
    if lg == "en":
        link = '<a href="chemicals">%s</a>' % CHEM_T["en"]
    else:
        link = ('<a href="/%s/chemicals">%s</a>'
                '<a href="/%s/central-asia">%s</a>'
                % (lg, CHEM_T[lg], lg, CA_T[lg]))
    if link in s:
        return s
    # первая редакция ставила в локалях ссылку на английскую страницу
    wrong = '<a href="/chemicals">%s</a>' % CHEM_T[lg]
    if lg != "en" and wrong in s:
        return s.replace(wrong, link, 1)
    anchor = "<h3>%s</h3>" % SUPPLY_H[lg]
    if anchor not in s or FIRST[lg] not in s:
        return s
    return s.replace(FIRST[lg], link + FIRST[lg], 1)


def foot_corridors(s):
    """Пятый коридор в списке коридоров футера."""
    link = ('<a href="central-asia" style="display:block">Central Asia '
            '&amp; Caspian</a>')
    if link in s:
        return s
    anchor = '<a href="southern-africa" style="display:block">Intra-Africa</a>'
    if anchor not in s:
        return s
    return s.replace(anchor, anchor + link, 1)


# ---------------------------------------------------------------- карточки
def lane_card(slug, title, sub, lg="en"):
    href = slug if lg == "en" else "/%s/%s" % (lg, slug)
    return ('<a class="lanelink" href="%s"><b>%s</b><span>%s</span></a>'
            % (href, title, sub))


def corridor_cards(s):
    """Карточка пятого коридора рядом с остальными четырьмя."""
    card = lane_card("central-asia", CA_T["en"], CA_SUB["en"])
    if 'href="central-asia"><b>' in s:
        return s
    m = re.search(r'<a class="lanelink" href="southern-africa">.*?</a>', s, re.S)
    if not m:
        return s
    return s[:m.end()] + card + s[m.end():]


CATS = ("building-materials.html", "industrial-equipment.html",
        "tools-hardware.html", "metals-pipe.html", "paper-packaging.html",
        "food-agricultural.html")


def cat_cards(s):
    """Химия в блоке "Other categories" на страницах товарных категорий.

    Это шесть самых близких по теме страниц. Ссылка оттуда весит больше
    футерной: она стоит в тексте, среди таких же категорий, и по ней
    действительно переходят.
    """
    if 'href="chemicals"><b>' in s:
        return s
    card = lane_card("chemicals", "Industrial chemicals", CHEM_SUB["en"])
    m = re.search(r'<div class="lanelinks"><a class="lanelink"', s)
    if not m:
        return s
    i = m.end() - len('<a class="lanelink"')
    return s[:i] + card + s[i:]


def supply_cards(s):
    """Карточка химии в списке товарных категорий на /supply."""
    card = lane_card("chemicals", "Industrial chemicals", CHEM_SUB["en"])
    if 'href="chemicals"><b>' in s:
        return s
    m = re.search(r'<a class="lanelink" href="building-materials">.*?</a>', s, re.S)
    if not m:
        return s
    return s[:m.start()] + card + s[m.start():]


def main():
    touched = set()

    # 1. hreflang и хлебные крошки на двенадцати новых страницах
    for slug in MULTI:
        for lg in LANGS:
            p = path_of(slug, lg)
            if not p.exists():
                print("  ВНИМАНИЕ: нет файла %s" % p.relative_to(SITE))
                continue
            s = b = p.read_text()
            s = hreflang(slug, lg, s)
            s = crumbs(slug, lg, s)
            if s != b:
                p.write_text(s)
                touched.add(str(p.relative_to(SITE)))

    # 2. футеры, по всем страницам сайта
    for p in sorted(SITE.rglob("*.html")):
        s = b = p.read_text()
        s = foot_supply(s, lang_of(p))
        s = foot_corridors(s)
        if s != b:
            p.write_text(s)
            touched.add(str(p.relative_to(SITE)))

    # 3. карточка пятого коридора на страницах коридоров
    for n in ("china.html", "turkiye.html", "west-africa.html",
              "southern-africa.html"):
        p = SITE / n
        s = b = p.read_text()
        s = corridor_cards(s)
        if s != b:
            p.write_text(s)
            touched.add(n)

    # 3a. карточка химии на страницах товарных категорий
    for n in CATS:
        q = SITE / n
        t = c = q.read_text()
        t = cat_cards(t)
        if t != c:
            q.write_text(t)
            touched.add(n)

    # 4. карточка химии на /supply
    p = SITE / "supply.html"
    s = b = p.read_text()
    s = supply_cards(s)
    if s != b:
        p.write_text(s)
        touched.add("supply.html")

    print("страниц поправлено: %d" % len(touched))

    # --- проверка результата
    inb = {}
    for p in sorted(SITE.rglob("*.html")):
        s = re.sub(r"(?s)<script.*?</script>", "", p.read_text())
        for h in re.findall(r'href="([^"#?]+)"', s):
            if h.startswith(("http", "mailto", "tel", "//")):
                continue
            h = h.strip("/").split("#")[0]
            if h:
                inb[h] = inb.get(h, 0) + 1
    for slug in MULTI:
        for lg in LANGS:
            key = slug if lg == "en" else "%s/%s" % (lg, slug)
            print("  ссылок на /%s: %d" % (key, inb.get(key, 0)))
    bad = []
    for slug in MULTI:
        for lg in LANGS:
            s = path_of(slug, lg).read_text()
            if 'hreflang="x-default"' not in s:
                bad.append("%s/%s: нет hreflang" % (lg, slug))
            if "BreadcrumbList" not in s:
                bad.append("%s/%s: нет крошек" % (lg, slug))
    if bad:
        print("ОСТАЛОСЬ:")
        for x in bad:
            print("   ", x)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
