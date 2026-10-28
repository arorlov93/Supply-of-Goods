# -*- coding: utf-8 -*-
"""Страница на каждую товарную группу: что фрахт добавляет именно к ней.

Зачем это, а не ещё один текст. У сайта нет ни одной внешней ссылки, и
поэтому его не видит ни поиск, ни языковые модели, которые ходят через
поиск. Ссылку ставят не за красивые слова, а за то, чего больше нигде
нет. У нас такое есть ровно одно: посчитанная из таможенных деклараций
надбавка фрахта и страховки по происхождению.

Сводная страница индекса отвечает на общий вопрос. А человек ищет узко:
«сколько фрахт добавляет к плитке», «почему цемент из Вьетнама дороже
доставить, чем купить». На такие запросы сегодня не отвечает никто,
потому что ни у кого нет цифры.

Чем это не дорвеи. У шестнадцати страниц разные числа, разный разброс,
разные выводы и разные крайние происхождения: у цемента разрыв 48
пунктов, у ручного инструмента 2.7. Текст про плотность стоимости
считается из самих данных, а не подставляется шаблоном. Страница, у
которой нечего сказать своего, здесь не создаётся.

Запуск: python3.13 tools/product-pages.py
Перед ним нужен tools/lpi-fetch.py.
"""
import collections, json, os, re, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(os.path.dirname(HERE))

import pagekit as PK
import search_mod as SRCH

PERIOD = "2024"
DATA = os.path.join("data", f"lpi-{PERIOD}.json")

# Короткое имя для адреса страницы. Пишется руками, а не режется из
# названия: адрес читают люди, и «freight-cost-ceramic-tile» понятнее,
# чем «freight-ceramic-and-porcelain-tile».
SLUG = {
    "0303": ("frozen-fish", "frozen fish"),
    "2523": ("cement", "cement"),
    "4804": ("kraft-paper", "kraft paper and board"),
    "4810": ("coated-paper", "coated paper and board"),
    "4819": ("cartons", "cartons and boxes"),
    "6802": ("worked-stone", "worked stone"),
    "6907": ("ceramic-tile", "ceramic and porcelain tile"),
    "7304": ("seamless-pipe", "seamless tube and pipe"),
    "7306": ("welded-pipe", "welded tube and pipe"),
    "7308": ("steel-structures", "steel structures"),
    "7318": ("fasteners", "screws, bolts and fasteners"),
    "8207": ("tool-parts", "interchangeable tool parts"),
    "8413": ("pumps", "pumps for liquids"),
    "8414": ("compressors", "compressors and fans"),
    "8428": ("lifting-machinery", "lifting and handling machinery"),
    "8467": ("power-tools", "hand and power tools"),
}


def density(cif):
    """Плотность стоимости решает всё. Корабль берёт за место и вес, а не
    за ценность, поэтому доля фрахта это почти целиком функция того,
    сколько стоит килограмм. Полосы подобраны по самим данным: внутри
    полосы выводы для покупателя одни и те же."""
    if cif < 1:
        return ("under a dollar a kilogram",
                "At this value the ship, not the factory, is the main thing you are "
                "buying. Freight is charged for weight and space, and when a kilogram "
                "is worth less than a dollar the same freight bill swallows a large "
                "part of the invoice. Origin decides this purchase more than price "
                "negotiation ever will.")
    if cif < 5:
        return ("a few dollars a kilogram",
                "Heavy enough for the route to matter and valuable enough for the "
                "factory price to matter too. This is the band where the two pull "
                "against each other: the cheapest goods often come from the origin "
                "with the heaviest freight, and the comparison has to be made landed "
                "rather than at the factory gate.")
    if cif < 20:
        return ("in the middle, five to twenty dollars a kilogram",
                "Freight is a real line but no longer the deciding one. What usually "
                "decides here is specification and certification: whether the goods "
                "arrive to the standard the destination requires, and what has to be "
                "arranged when they do not.")
    return ("well over twenty dollars a kilogram",
            "Dense value. Freight is a small share, and chasing it is the wrong "
            "economy: a one per cent move on the goods price is worth more than "
            "halving the shipping bill. Lead time and specification are where the "
            "money is on this kind of purchase.")


def page(doc, hs, rs):
    slug_tail, nice = SLUG[hs]
    slug = "freight-cost-" + slug_tail
    rs = sorted(rs, key=lambda r: r["uplift"])
    lo, hi = rs[0], rs[-1]
    ups = [r["uplift"] for r in rs]
    med = statistics.median(ups)
    cif_med = statistics.median(r["cif_kg"] for r in rs)
    total_t = sum(r["tonnes"] for r in rs) or 1
    big = max(rs, key=lambda r: r["tonnes"])
    band, reading = density(cif_med)
    product = rs[0]["product"]
    group = rs[0]["group"]

    table = ("<div class=\"tablewrap\"><table class=\"lpi\"><thead><tr>"
             "<th>Origin</th><th>CIF, $/kg</th><th>FOB, $/kg</th>"
             "<th>Freight and insurance</th></tr></thead><tbody>"
             + "".join("<tr><td>%s</td><td>%.3f</td><td>%.3f</td><td><b>%.1f%%</b></td></tr>"
                       % (r["origin"], r["cif_kg"], r["fob_kg"], r["uplift"])
                       for r in sorted(rs, key=lambda r: -r["uplift"]))
             + "</tbody></table></div>")

    blocks = [
     ("h2", "The number"),
     ("raw", '<div class="answer"><h2>The short answer</h2><ol class="alist">'
             '<li><b>Freight and insurance ran from %.1f&nbsp;%% to %.1f&nbsp;%% of goods '
             'value</b> on %s imported into the United States in %s.</li>'
             '<li><b>Lightest from %s at %.1f&nbsp;%%, heaviest from %s at %.1f&nbsp;%%.</b> '
             'A spread of %.0f points on the same product, before anybody argues about '
             'the price of the goods.</li>'
             '<li><b>Median across the %d origins: %.1f&nbsp;%%.</b> Median rather than '
             'average, because one unusual cargo moves an average and tells you nothing '
             'about your lane.</li></ol>'
             '<p class="anote">Computed from United States customs declarations '
             'republished by UN Comtrade, %s reporting year, HS %s. Method on the '
             '<a href="/landed-price-index">landed price index</a>.</p></div>'
             % (lo["uplift"], hi["uplift"], nice, PERIOD,
                lo["origin"], lo["uplift"], hi["origin"], hi["uplift"],
                hi["uplift"] - lo["uplift"], len(rs), med, PERIOD, hs)),

     ("h2", "By origin"),
     ("p", "CIF is the value landed at the border, FOB the value at the seller&rsquo;s "
           "door, and the last column the difference as a share of FOB. Every row is "
           "what importers actually declared, not an estimate."),
     ("raw", table),

     ("h2", "Why this product sits where it does"),
     ("p", "A kilogram of %s declared at a median of <b>$%.2f</b>, which puts it %s."
           % (nice, cif_med, band)),
     ("p", reading),
     ("p", "That is the whole mechanism, and it is worth stating plainly because it "
           "decides how to buy: <b>a ship charges for weight and space, never for "
           "value.</b> Carrying a tonne of anything costs about what carrying a tonne "
           "of anything else costs. The cheaper the goods are by weight, the larger "
           "the share that same bill takes."),

     ("h2", "Where it actually comes from"),
     ("p", "Freight share and trade share are different questions, and on this product "
           "they have different answers. %s supplied <b>%s tonnes</b> of the %s tonnes "
           "in this table, %.0f per cent of it, the largest of the %d origins here. "
           "%s"
           % (big["origin"], f"{big['tonnes']:,}".replace(",", "&thinsp;"),
              f"{total_t:,}".replace(",", "&thinsp;"),
              big["tonnes"] / total_t * 100, len(rs),
              ("The same origin is also the cheapest to ship from, so volume and "
               "freight point the same way here, which is unusual."
               if big["origin"] == lo["origin"] else
               "It is not the cheapest to ship from: that is %s, at %.1f per cent "
               "against %.1f. Volume follows price, capacity and habit, not freight."
               % (lo["origin"], lo["uplift"], big["uplift"])))),
     ("p", "Worth reading next to the table above, because the two together say "
           "something a single number cannot: the lane everybody already uses is not "
           "automatically the lane that lands cheapest."),

     ("h2", "What to do with this"),
     ("ul", [
      "<b>Check the freight line in the offer you are holding.</b> If it sits far "
      "outside the band above for your origin, that is a question for the seller. If "
      "it sits inside, it is not proof the rest of the offer is fair.",
      "<b>Compare landed, not at the factory gate.</b> On this product the gap between "
      "origins is %.0f points. An offer that wins on the factory price can lose on the "
      "quay." % (hi["uplift"] - lo["uplift"]),
      "<b>Treat these as a benchmark, not a quotation.</b> They are national annual "
      "averages across every buyer, incoterm and route into one country.",
     ]),
     ("note", "We buy and ship this category. If you are holding an offer on %s and "
              "want it rebuilt as a landed price and checked against this data, "
              "<a href=\"/quote-check\">send it over</a>. Free, two working days, and "
              "we never contact your supplier." % nice),
    ]

    ld = [{
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": "Freight and insurance on %s by origin" % nice,
        "description": ("Freight and insurance as a share of goods value for %s "
                        "(HS %s) imported into the United States, by country of "
                        "origin, from customs declarations." % (nice, hs)),
        "url": PK.HOST + slug,
        "temporalCoverage": PERIOD,
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "creator": {"@type": "Organization", "name": "ISP GROUP LLC", "url": PK.HOST},
        "isBasedOn": {"@type": "Dataset", "name": "UN Comtrade",
                      "url": "https://comtradeplus.un.org/"},
    }]

    return PK.build({
     "slug": slug,
     "crumb": nice[0].upper() + nice[1:],
     "title": "Freight cost on %s: %.0f to %.0f%% by origin" % (nice, lo["uplift"], hi["uplift"]),
     "desc": ("What freight and insurance actually add to %s, by country of origin, "
              "from United States customs declarations. %.1f%% to %.1f%%, HS %s."
              % (nice, lo["uplift"], hi["uplift"], hs))[:158],
     "og_title": "Freight and insurance on %s, by origin" % nice,
     "og_img": "vessel.jpg",
     "og_alt": "Container ship under way",
     "h1": "What freight adds to <em>%s</em>" % nice,
     "sub": ("Measured from customs declarations rather than estimated. %.1f per cent "
             "of goods value at the lightest origin, %.1f at the heaviest, on United "
             "States imports in %s."
             % (lo["uplift"], hi["uplift"], PERIOD)),
     "chips": ["HS %s" % hs, "%d origins" % len(rs),
               "%s reporting year" % PERIOD, "UN Comtrade"],
     "lede": ("The line most quotations leave out, for one product",
              "Customs publishes every import twice: once at the seller&rsquo;s door "
              "and once landed at the border. The gap is freight and insurance, "
              "measured rather than claimed. Here it is for %s alone." % nice),
     "blocks": blocks,
     "ld": ld,
     "faq": [
      ("Is this the freight cost I will pay?",
       "No. It is what importers across one whole country declared over a year, on "
       "every route and every incoterm. Your shipment has one route, one season and one "
       "carrier. Use it to judge whether the number you were given is in the right part "
       "of the map, not as a price."),
      ("Why is %s so much lighter than %s on this product?" % (lo["origin"], hi["origin"]),
       "Distance is part of it, but the larger part is what else travels that lane and "
       "how full the ships come back. A route with balanced two-way traffic prices "
       "lower per tonne than one where boxes return empty. On %s the gap between those "
       "two origins is %.0f points, which is wider than most negotiations move the "
       "factory price." % (nice, hi["uplift"] - lo["uplift"])),
      ("Does the biggest supplier give the best landed price?",
       "Not automatically, and on this product that is worth checking: %s ships the "
       "largest volume at %.1f per cent freight, while %s sits at %.1f. Volume follows "
       "capacity and habit as much as cost, and a lane everybody uses is not the same "
       "as a lane that lands cheapest."
       % (big["origin"], big["uplift"], lo["origin"], lo["uplift"])),
     ],
     "faq_h2": "Questions on this figure",
     "faq_sub": "The three that come up when somebody first reads the number.",
     "related": ("The rest of the picture",
                 "The same calculation across every category, and what to do with it.",
                 [("/landed-price-index", "The full landed price index",
                   "Sixteen product groups, eight origins, method and CSV."),
                  ("/quote-check", "Send us the quote you already have",
                   "Rebuilt as a landed price and benchmarked. Free, no obligation."),
                  ("/three-origins", "Three origins, one price sheet",
                   "One specification priced out of three continents, landed."),
                  ("/landed-price", "What a landed price must include",
                   "Every line between a factory price and your own gate.")]),
     "cta_h2": "Holding an offer on %s?" % nice,
     "cta_p": ("Send it over and we will rebuild it as a landed price, check the freight "
               "line against this data and tell you whether the seller is a factory."),
     "cta_href": "/quote-check",
     "cta": "Send it for checking",
    }), slug, nice, lo, hi


def main():
    with open(DATA, encoding="utf-8") as f:
        doc = json.load(f)
    by = collections.defaultdict(list)
    for r in doc["rows"]:
        by[r["hs"]].append(r)

    made = []
    for hs, rs in sorted(by.items()):
        if hs not in SLUG or len(rs) < 4:
            print("  пропуск HS%s: мало происхождений" % hs)
            continue
        path, slug, nice, lo, hi = page(doc, hs, rs)
        made.append((slug, nice, lo, hi))
        print("  собрана:", path)

    # карта сайта
    sm = os.path.join("site", "sitemap.xml")
    t = open(sm, encoding="utf-8").read()
    added = 0
    for slug, *_ in made:
        if PK.HOST + slug + "<" in t:
            continue
        t = t.replace("</urlset>",
                      '  <url><loc>%s%s</loc><lastmod>%s</lastmod>'
                      '<changefreq>monthly</changefreq><priority>0.7</priority></url>\n'
                      '</urlset>' % (PK.HOST, slug, doc["built"]))
        added += 1
    open(sm, "w", encoding="utf-8").write(t)
    print("  адресов в карту сайта:", added)

    # сетка ссылок на самом индексе: без неё шестнадцать страниц сироты
    idx = os.path.join("site", "landed-price-index.html")
    s = open(idx, encoding="utf-8").read()
    if 'class="prodgrid"' not in s:
        cards = "".join(
            '<a class="lanelink" href="/%s"><b>%s</b>'
            '<span>%.1f%% to %.1f%% of goods value, by origin.</span></a>'
            % (slug, nice[0].upper() + nice[1:], lo["uplift"], hi["uplift"])
            for slug, nice, lo, hi in made)
        block = ('<section data-reveal><div class="wrap">'
                 '<span class="eyebrow">One product at a time</span>'
                 '<div class="lede"><h2>The same figure, per product</h2>'
                 '<p class="intro">The table above is the whole picture. These are the '
                 'sixteen parts of it, each with its own spread and its own reading.</p>'
                 '</div><div class="lanelinks prodgrid">%s</div></div></section>\n' % cards)
        anchor = '<section data-reveal id="faq">'
        s = s.replace(anchor, block + anchor, 1)
        open(idx, "w", encoding="utf-8").write(s)
        print("  сетка на шестнадцать страниц добавлена на индекс")

    # llms.txt
    lp = os.path.join("site", "llms.txt")
    t = open(lp, encoding="utf-8").read()
    rows = "".join(
        "- [Freight on %s](%s%s): %.1f%% to %.1f%% of goods value by origin, from "
        "United States customs declarations, %s.\n"
        % (nice, PK.HOST, slug, lo["uplift"], hi["uplift"], PERIOD)
        for slug, nice, lo, hi in made if PK.HOST + slug + ")" not in t)
    if rows:
        if "## Freight by product" not in t:
            t = t.rstrip() + "\n\n## Freight by product\n\n" + rows
        open(lp, "w", encoding="utf-8").write(t)
        print("  строк в llms.txt:", rows.count("\n"))

    n, size = SRCH.build_index()
    print(f"  индекс поиска: {n} страниц, {size/1024:.0f} КБ")
    return 0


if __name__ == "__main__":
    sys.exit(main())
