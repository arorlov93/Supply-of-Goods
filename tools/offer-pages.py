# -*- coding: utf-8 -*-
"""Три страницы: проверка чужого предложения, три происхождения, индекс.

Зачем они вместе. Это одна воронка, а не три текста. Индекс показывает
цифру, которую больше нигде не прочитать; проверка чужого предложения
превращает любопытство в разговор, ничем не обязывая покупателя; сравнение
трёх происхождений превращает разговор в заказ. Порядок обратный тому, как
их читают, и прямой тому, как они работают.

Что в них настоящего. Индекс считается из открытых деклараций UN Comtrade,
см. tools/lpi-fetch.py. Ни одна цифра здесь не придумана, и ни одна не
наша: это то, что покупатель может проверить сам по тому же источнику. Для
торговой компании это и есть главный довод, потому что остальные её доводы
проверить нельзя.

Чего в них нет. Обещаний сроком, которых компания не подтверждала, имён
покупателей, отзывов и любых показателей, которых я не видел в источнике.

Запуск: python3.13 tools/offer-pages.py
Перед ним нужен tools/lpi-fetch.py, он готовит data/lpi-<год>.json.
"""
import collections, json, os, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(os.path.dirname(HERE))

import pagekit as PK
import search_mod as SRCH

PERIOD = "2024"
DATA = os.path.join("data", f"lpi-{PERIOD}.json")


# ─────────────────────────────────────────────── индекс: таблицы и цифры
def load():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def load_fx():
    """Дневная часть: курсы ЕЦБ, см. tools/fx-daily.py. Если файла нет,
    страница собирается без этого блока, а не падает."""
    p = os.path.join("data", "fx.json")
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def fx_block(fx):
    if not fx or not fx.get("rows"):
        return []
    rows = "".join(
        "<tr><td>%s</td><td>%s</td><td>$%s</td><td><b>%+.2f%%</b></td></tr>"
        % (r["code"], r["who"],
           ("%.6f" % r["usd"]).rstrip("0").rstrip("."), r["change"])
        for r in fx["rows"])
    return [
     ("h2", "What the seller&rsquo;s currency is doing"),
     ("p", "The table above is an annual picture. This part changes every working day, "
           "and on a contract it moves real money: an offer written in euros and paid "
           "thirty days later is a different price in dollars from the one you agreed."),
     # Обёртка с опознавательным id: содержимое этого блока подменяет на
     # свежее функция site/functions/_fx.js прямо в ответе сервера. То, что
     # собрано здесь, остаётся запасным вариантом на случай, когда источник
     # недоступен, и показывается оно с той датой, с которой собрано.
     ("raw", '<div id="fx-live"><div class="tablewrap"><table class="lpi"><thead><tr>'
             '<th>Currency</th><th>Sellers who invoice in it</th>'
             '<th>One unit, in dollars</th><th>Change over a month</th>'
             '</tr></thead><tbody>%s</tbody></table></div>'
             '<p class="pnote">European Central Bank reference rates for %s, against '
             '%s. The bank publishes on working days only, so over a weekend this '
             'shows the last published day rather than today: the date here is the '
             'date of the figures, not the date we fetched them.</p></div>'
             % (rows, fx["date"], fx["compared_to"])),
     ("p", "Read it next to the freight column. On a cheap, heavy cargo the freight "
           "share decides the deal and a two per cent currency move is noise. On "
           "machinery the freight share is small and the same two per cent is the whole "
           "margin. Which of the two you are buying decides which number to watch."),
    ]


def medians(rows):
    by = collections.defaultdict(list)
    for r in rows:
        by[r["origin"]].append(r["uplift"])
    return sorted(((o, statistics.median(v), len(v)) for o, v in by.items()),
                  key=lambda x: x[1])


def spread(rows):
    """Самый большой разрыв между происхождениями внутри одного товара."""
    out = []
    for hs in {r["hs"] for r in rows}:
        g = [r for r in rows if r["hs"] == hs]
        if len(g) < 3:
            continue
        lo = min(g, key=lambda x: x["uplift"])
        hi = max(g, key=lambda x: x["uplift"])
        out.append((hi["uplift"] - lo["uplift"], lo, hi))
    return sorted(out, reverse=True, key=lambda x: x[0])


def table(rows):
    head = ("<thead><tr><th>Product</th><th>HS</th><th>Origin</th>"
            "<th>CIF, $/kg</th><th>FOB, $/kg</th><th>Freight and insurance</th>"
            "</tr></thead>")
    body = "".join(
        "<tr><td>%s</td><td><code>%s</code></td><td>%s</td>"
        "<td>%.3f</td><td>%.3f</td><td><b>%.1f%%</b></td></tr>"
        % (r["product"], r["hs"], r["origin"], r["cif_kg"], r["fob_kg"], r["uplift"])
        for r in rows)
    return ('<div class="tablewrap"><table class="lpi">%s<tbody>%s</tbody></table></div>'
            % (head, body))


def index_page(doc, fx=None):
    rows = doc["rows"]
    med = medians(rows)
    sp = spread(rows)
    cheapest, dearest = med[0], med[-1]
    top = sp[0]

    groups = []
    for g in dict.fromkeys(r["group"] for r in rows):
        groups.append('<h3 class="lpi-h">%s</h3>%s'
                      % (g, table([r for r in rows if r["group"] == g])))

    med_rows = "".join("<tr><td>%s</td><td><b>%.1f%%</b></td><td>%d</td></tr>"
                       % (o, m, n) for o, m, n in med)

    blocks = [
     ("h2", "The one number most quotations leave out"),
     ("p", "Customs authorities publish every import twice: once as the value of the "
           "goods at the seller&rsquo;s door, and once as the value of the same "
           "consignment landed at the border. The gap between those two figures is "
           "freight and insurance, measured from actual declarations rather than "
           "estimated by anybody with something to sell."),
     ("p", "That gap is the line buyers are least able to check and sellers are most "
           "likely to leave out. Published as a percentage by origin, it says something "
           "uncomfortable and useful: on some goods the country you buy from moves the "
           "landed price more than any negotiation on the factory price will."),
     ("raw", '<div class="answer"><h2>The short answer</h2><ol class="alist">'
             '<li><b>Freight and insurance ran from %.1f&nbsp;%% to %.1f&nbsp;%% of goods '
             'value</b> across the groups below, on United States imports in %s.</li>'
             '<li><b>%s was the heaviest origin and %s the lightest</b> by median: '
             '%.1f&nbsp;%% against %.1f&nbsp;%%.</li>'
             '<li><b>%s shows the widest spread:</b> %.1f&nbsp;%% from %s against '
             '%.1f&nbsp;%% from %s, a gap of %.0f points on the same product.</li>'
             '</ol><p class="anote">Source: UN Comtrade reporter data, United States '
             'imports, %s. Method and exclusions below.</p></div>'
             % (min(r["uplift"] for r in rows), max(r["uplift"] for r in rows), PERIOD,
                dearest[0], cheapest[0], dearest[1], cheapest[1],
                top[1]["product"], top[1]["uplift"], top[1]["origin"],
                top[2]["uplift"], top[2]["origin"], top[0], PERIOD)),

     ("__FX__", ""),

     ("h2", "Freight and insurance by origin"),
     ("p", "Median across all the product groups below. A median rather than an average, "
           "because one cement cargo distorts an average and tells you nothing about the "
           "lane you are actually buying on."),
     ("raw", '<div class="tablewrap"><table class="lpi"><thead><tr><th>Origin</th>'
             '<th>Median freight and insurance</th><th>Product groups counted</th>'
             '</tr></thead><tbody>%s</tbody></table></div>' % med_rows),
     ("p", "Distance explains less of this than weight does. Power tools out of Viet Nam "
           "carry close to nothing, because a tool is worth a great deal per kilogram. "
           "Cement out of the same country carries a share many times larger, because "
           "cement is worth almost nothing per kilogram and the ship costs the same "
           "either way. The rule worth taking away: <b>the cheaper the goods are by "
           "weight, the more the origin decides the deal.</b>"),

     ("h2", "The full table"),
     ("p", "Every row is one product group from one origin, as declared to United States "
           "customs in %s. CIF is the landed value at the border, FOB the value at the "
           "seller&rsquo;s door, and the last column the difference as a share of FOB."
           % PERIOD),
     ("raw", "".join(groups)),
     ("raw", '<p style="margin-top:26px"><a class="btn btn-ghost" href="/data/lpi-%s.csv" '
             'download>Download the table as CSV</a></p>' % PERIOD),

     ("h2", "Method, and what this is not"),
     ("p", "The figures come from UN Comtrade, which republishes what national customs "
           "services report. The reporter here is the United States and the flow is "
           "imports, so every row is a declaration made to US customs. Unit values are "
           "value divided by net weight. Freight and insurance is the CIF value less the "
           "FOB value, as a share of FOB."),
     ("ul", [
      "<b>What is excluded.</b> Rows without a weight or without one of the two values, "
      "rows under 50 tonnes for the year, and rows where the uplift came out below one "
      "per cent or above sixty. Those last are reporting artefacts rather than freight. "
      "%d rows were dropped on these rules out of %d collected." % (
          doc["dropped"], doc["dropped"] + len(rows)),
      "<b>What the numbers are not.</b> They are national annual averages across every "
      "buyer, every incoterm variant and every box on the water that year. They are a "
      "benchmark, not a quotation for your shipment.",
      "<b>What they are good for.</b> Telling you whether the freight line in a "
      "quotation you are holding is in the right part of the map, and which origins are "
      "worth pricing at all before you start.",
     ]),
     ("note", "Built %s from the %s reporting year. We republish it when the source "
              "updates. If a figure here looks wrong to you, the source is public and we "
              "would rather be corrected than quoted." % (doc["built"], PERIOD)),
    ]

    out = []
    for b in blocks:
        if b[0] == "__FX__":
            out.extend(fx_block(fx))
        else:
            out.append(b)
    blocks = out

    ld = [{
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": "Freight and insurance by origin: the ISP Group landed price index",
        "description": ("Freight and insurance as a share of goods value, by product "
                        "group and country of origin, computed from United States "
                        "customs declarations republished by UN Comtrade."),
        "url": PK.HOST + "landed-price-index",
        "temporalCoverage": PERIOD,
        "dateModified": (fx or {}).get("date", doc["built"]),
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "creator": {"@type": "Organization", "name": "ISP GROUP LLC", "url": PK.HOST},
        # description обязателен и у вложенного набора данных тоже: Search Console
        # 29.10 отбила проверку «Отсутствует поле description», указав объект
        # UN Comtrade, то есть именно этот isBasedOn, а не внешний Dataset.
        "isBasedOn": {"@type": "Dataset", "name": "UN Comtrade",
                      "description": "United Nations international trade statistics "
                                     "database, which republishes customs declarations "
                                     "reported by national statistical authorities, "
                                     "including United States imports valued both CIF "
                                     "and FOB.",
                      "url": "https://comtradeplus.un.org/"},
        "variableMeasured": [
            {"@type": "PropertyValue", "name": "CIF unit value", "unitText": "USD per kg"},
            {"@type": "PropertyValue", "name": "FOB unit value", "unitText": "USD per kg"},
            {"@type": "PropertyValue", "name": "Freight and insurance share",
             "unitText": "percent of FOB value"},
        ],
        "distribution": [{"@type": "DataDownload", "encodingFormat": "text/csv",
                          "contentUrl": PK.HOST + f"data/lpi-{PERIOD}.csv"}],
    }]

    return PK.build({
     "slug": "landed-price-index",
     "crumb": "Landed price index",
     "title": "Freight and insurance by origin: landed price index",
     "desc": ("What freight and insurance actually add to goods value, by product group "
              "and country of origin, from United States customs declarations."),
     "og_title": "What freight and insurance actually add, by origin",
     "og_img": "vessel.jpg",
     "og_alt": "Container ship under way",
     "h1": "What freight and insurance <em>actually add</em>",
     "sub": ("Measured from customs declarations rather than estimated. United States "
             "imports, %s reporting year, %d product groups across %d origins." %
             (PERIOD, len({r["hs"] for r in rows}), len({r["origin"] for r in rows}))),
     "chips": ["UN Comtrade", "%s reporting year" % PERIOD,
               "%d rows" % len(rows), "CSV included"],
     "lede": ("A number you can check, from a source we did not control",
              "Everything else a trading company tells you about price has to be taken "
              "on trust. This does not. It is computed from declarations made to customs "
              "by thousands of importers, republished by the United Nations, and the "
              "working is below so you can repeat it."),
     "blocks": blocks,
     "ld": ld,
     "faq": [
      ("Why does freight matter more on some goods than others?",
       "Because a ship charges for space and weight, not for value. Carrying a tonne of "
       "cement costs about what carrying a tonne of power tools costs, but the cement is "
       "worth a fraction as much, so the same freight bill is a far larger share of it. "
       "That is why the heaviest percentages in the table sit on the cheapest goods."),
      ("Can I use these figures in my own quotation?",
       "As a sanity check, yes. As a price, no. They are annual national averages across "
       "every buyer and every route into one country. If the freight line in a quotation "
       "you are holding is far outside the band here, that is worth a question to the "
       "seller. If it is inside, it is not proof that the rest of the quotation is fair."),
      ("Why the United States as the reporting country?",
       "Because it is the market this company sells into, and because its declarations "
       "are the ones a buyer here can go and check. The same calculation works for any "
       "reporter in the source, and we will publish other corridors as we run them."),
      ("Who can use this table?",
       "Anyone. It is published under CC BY, the source is named and the method is "
       "written out. Cite it, argue with it, or send us a correction."),
     ],
     "faq_h2": "Questions about the index",
     "faq_sub": "The four that come up as soon as somebody reads the table.",
     "related": ("Where this becomes a price for you",
                 "The index tells you what is normal. These two tell you what yours is.",
                 [("/quote-check", "Send us the quote you already have",
                   "We rebuild it as a landed price and benchmark it. Free, no obligation."),
                  ("/three-origins", "Three origins, one price sheet",
                   "One specification priced out of three continents, landed."),
                  ("/landed-price", "What a landed price must include",
                   "Every line between a factory price and your own gate."),
                  ("/china", "Sourcing from China",
                   "Factory or trader, inspection, payment, and the checks between.")]),
     "cta_h2": "Want this run on your actual shipment?",
     "cta_p": ("The table says what is normal. Send us the quotation you are holding and "
               "we will tell you where yours sits, line by line."),
     "cta_href": "/quote-check",
     "cta": "Send a quotation for checking",
    })


# ────────────────────────────────────────────── проверка чужого предложения
def quote_check(doc):
    rows = doc["rows"]
    med = medians(rows)
    return PK.build({
     "slug": "quote-check",
     "crumb": "Quote check",
     "title": "Send the quotation you already have. We check it free",
     # Выдача обрезает описание около 160 знаков, поэтому оно считается.
     "desc": ("Send a quotation you already hold. We rebuild it as a landed price, "
              "benchmark it against customs data and check the seller. Free, two "
              "working days."),
     "og_title": "You already have a quotation. Send it to us",
     "og_img": "signing.jpg",
     "og_alt": "Signing paperwork across a desk",
     "h1": "You already have a quotation. <em>Send it to us.</em>",
     "sub": ("We rebuild it as a landed price, benchmark the goods against what "
             "comparable shipments actually declared at customs, and tell you whether "
             "the seller is a factory or a trader. Two working days. No charge, and no "
             "obligation to buy anything from us."),
     "chips": ["Free", "Two working days", "No obligation",
               "We never contact your supplier"],
     "lede": ("Why a competitor would read your quotation for nothing",
              "Because the hardest thing to find in this trade is an honest second "
              "opinion. Everybody you show a price to starts selling. We would rather "
              "show you how we work on a purchase you have already made up your mind "
              "about, and be the first call on the next one."),
     "blocks": [
      ("h2", "What comes back, on one page"),
      ("ul", [
       "<b>The quotation rebuilt as a landed price.</b> Every line between the price you "
       "were given and your own gate, at the Incoterm actually written in the offer, with "
       "the lines that were left out named.",
       "<b>A benchmark from customs data.</b> What comparable goods declared on that lane, "
       "and where the freight line in your offer sits against the published band. Our "
       "<a href=\"/landed-price-index\">landed price index</a> is the public part of the "
       "same work.",
       "<b>Factory or trader.</b> Registration, scope of business, whether the entity "
       "exports in its own name, and whether the bank account name matches the seller. "
       "These are the checks that separate a producer from a reseller with a website.",
       "<b>The questions we would ask before paying.</b> Written out, so you can send "
       "them yourself without us anywhere near the conversation.",
      ]),
      ("h2", "What we need from you"),
      ("p", "The quotation, and the destination. That is the minimum. Everything else "
            "makes the answer sharper rather than possible."),
      ("ul", [
       "The offer itself, as a file or pasted text. Black out the seller&rsquo;s name if "
       "you prefer; it costs us the authenticity check and nothing else.",
       "Where the goods have to arrive, and on what Incoterm the offer is written.",
       "The specification or standard, if the offer does not state one. Half the "
       "disagreements about price are disagreements about what was priced.",
      ]),
      ("note", "If the offer names a standard, a grade or a certificate, leave those in. "
               "They are usually where the difference between two prices actually hides."),

      ("h2", "What we will not do"),
      ("p", "This matters more than anything above, so it is written plainly."),
      ("ul", [
       "<b>We will not contact your supplier.</b> Not to check the offer, not afterwards, "
       "not ever on the strength of something you sent us for review.",
       "<b>We will not use your quotation to approach that producer ourselves.</b>",
       "<b>We will not publish it.</b> Anything we ever write about this work is "
       "anonymised and aggregated, like the index, with no buyer, seller or price "
       "identifiable.",
      ]),
      ("p", "A supplier who publishes what he learns about you is telling you what he "
            "will publish about everyone. We would rather be the opposite of that, and "
            "say so before you send anything."),

      ("h2", "Why we do it for nothing"),
      ("p", "Because of the order things happen in. You have a purchase in front of you "
            "that you are not going to give us. We would rather spend two days being "
            "useful on it than spend the same two days sending you a brochure you did "
            "not ask for, and then be the company you think of on the one after."),
      ("p", "If the offer you are holding turns out to be good, we will say so. That "
            "answer costs us nothing and tells you more about us than a lower number "
            "would."),
     ],
     "extra": ('<div class="answer" style="margin-top:38px">'
               '<h2>What the benchmark looks like</h2>'
               '<p>Freight and insurance ran at a median of %.1f&nbsp;%% of goods value '
               'out of %s and %.1f&nbsp;%% out of %s on United States imports in %s. '
               'If the offer in your hand is far outside the band for your lane, that is '
               'the first question to ask, and we will have asked it for you.</p>'
               '<p class="anote">The whole table, the method and the source are on the '
               '<a href="/landed-price-index">landed price index</a>.</p></div>'
               % (med[0][1], med[0][0], med[-1][1], med[-1][0], PERIOD)),
     "faq": [
      ("Is this really free, or is it free until you send an invoice?",
       "Free. There is no charge and no stage at which one appears. We are spending the "
       "time to show you how we work, on a purchase you have already decided to make "
       "somewhere else."),
      ("What if my quotation is from one of your own suppliers?",
       "Then we will tell you that, and we will not take the review any further. "
       "Reviewing an offer from a producer we also buy from is not a second opinion, it "
       "is a conflict, and you would be right not to trust the answer."),
      ("How do I know you will not go round me to the factory?",
       "You have our word in writing above, and the practical answer underneath it: a "
       "trading company that does that once never gets a second quotation to look at. "
       "The whole value of this to us depends on it not happening."),
      ("Two working days from when?",
       "From the point we have the offer and the destination. If what arrives is not "
       "enough to work from, we say so the same day rather than letting the clock run."),
     ],
     "faq_h2": "Questions before you send anything",
     "faq_sub": "The four that anybody sensible asks first.",
     "related": ("Before you send it",
                 "The three guides that cover most of what a review finds.",
                 [("/landed-price", "What a landed price must include",
                   "Every line between a factory price and your own gate."),
                  ("/verify-supplier", "How to verify a supplier is a factory",
                   "The checks that separate a producer from a reseller."),
                  ("/incoterms", "Incoterms 2020 explained",
                   "Who pays for what, and where the risk actually passes."),
                  ("/landed-price-index", "The landed price index",
                   "What freight and insurance add, by origin, from customs data.")]),
     "cta_h2": "Send the quotation",
     "cta_p": ("Paste it or attach it, tell us where the goods have to arrive, and we "
               "will come back within two working days."),
     "cta_href": "/contact#enquiry",
     "cta": "Send it for checking",
    })


# ──────────────────────────────────────────────────── три происхождения
def three_origins(doc):
    rows = doc["rows"]
    sp = spread(rows)
    top = sp[0]
    origins = sorted({r["origin"] for r in rows})

    return PK.build({
     "slug": "three-origins",
     "crumb": "Three origins",
     "title": "One specification priced out of three origins, landed",
     "desc": ("The same specification priced from three countries, landed at your gate, "
              "with lead time, certification and duty named. A decision document, not a "
              "quotation."),
     "og_title": "One specification. Three origins. One comparison",
     "og_img": "containers-wall.jpg",
     "og_alt": "Wall of stacked shipping containers",
     "h1": "One specification. <em>Three origins.</em> One comparison.",
     "sub": ("Most sellers can quote you one country. We price the same specification out "
             "of three and land all three at your gate, so the choice in front of you is "
             "where to buy from rather than which brochure to believe."),
     "chips": ["China", "T&uuml;rkiye", "European Union", "India &middot; Viet Nam &middot; Korea"],
     "lede": ("The question is not which supplier. It is which continent",
              "Two offers from the same country differ by a few per cent and a lot of "
              "noise. Two offers from different continents differ by freight, duty, lead "
              "time and certification at once, and almost nobody puts those four on one "
              "page because almost nobody buys from more than one of them."),
     "blocks": [
      ("h2", "What the sheet contains"),
      ("p", "One page, one specification, three columns. Each column is a real producer "
            "we have verified, not a market average."),
      ("ul", [
       "<b>Landed price at your gate</b>, at one agreed Incoterm, with freight, insurance, "
       "port charges, estimated duty and certification shown line by line.",
       "<b>Lead time from a confirmed order</b>, separated into production and transit, "
       "because the two fail for different reasons and only one of them can be chased.",
       "<b>Certification and admissibility</b> at the destination: which marks the goods "
       "carry, which the destination requires, and what has to be arranged for the gap.",
       "<b>Duty exposure</b> at the classification we agree in writing before the order, "
       "including anti-dumping measures where they apply, because on steel and tile they "
       "very often do.",
       "<b>What we would not buy there, and why.</b> One column usually loses. Saying so "
       "is the part of the sheet worth paying for.",
      ]),

      ("h2", "Why origin moves the price more than haggling does"),
      ("p", "This is not an opinion. Freight and insurance as a share of goods value, "
            "measured from customs declarations, varies by origin far more than the few "
            "per cent a negotiation on the factory price usually moves."),
      ("raw", '<div class="answer"><h2>One product, two origins</h2>'
              '<ol class="alist"><li><b>%s from %s:</b> freight and insurance ran '
              '%.1f&nbsp;%% of goods value.</li><li><b>The same product from %s:</b> '
              '%.1f&nbsp;%%.</li><li><b>A gap of %.0f points</b> before anybody argues '
              'about the price of the goods themselves.</li></ol>'
              '<p class="anote">United States imports, %s reporting year. Source, method '
              'and the full table on the <a href="/landed-price-index">landed price '
              'index</a>.</p></div>'
              % (top[1]["product"], top[2]["origin"], top[2]["uplift"],
                 top[1]["origin"], top[1]["uplift"], top[0], PERIOD)),
      ("p", "Duty does the same thing in the other direction, and the two do not move "
            "together. The cheapest goods often arrive from the origin with the heaviest "
            "freight and the lightest duty, or the reverse. One column at a time cannot "
            "show you that. Three can."),

      ("h2", "Which origins we can price now"),
      ("p", "These are lanes where producers are already verified and a document set has "
            "cleared before, so a comparison comes back in days rather than weeks: "
            + ", ".join(origins) + "."),
      ("p", "A country outside that list is a sourcing project rather than a quotation. "
            "We will say so, say how long building the lane takes, and quote the work "
            "honestly instead of pretending it is routine."),

      ("h2", "What we need to start"),
      ("ul", [
       "The specification, or the standard and grade. If you only have a problem to "
       "solve, describe it and we will write the specification with you.",
       "Quantity and how often, because a trial load and a programme price differently.",
       "Where it has to arrive and by when.",
      ]),
      ("note", "We do not need to know who else you are talking to, and we would rather "
               "not. The comparison is between producers, not between us and somebody "
               "else&rsquo;s offer."),
     ],
     "faq": [
      ("Will all three columns be real producers?",
       "Yes. Each one is an entity we have checked: registration, scope of business, "
       "whether it exports in its own name, and whether the bank account name matches. A "
       "column we cannot verify does not go on the sheet, and we say why it is missing."),
      ("What does the comparison cost?",
       "On the lanes listed above, nothing, because the work is the work we would do "
       "anyway to quote you. Building a new lane takes real time and we quote that "
       "separately and in advance."),
      ("Can I take the sheet and buy direct?",
       "You can. Most of what is on it is checkable once you know what to check, and the "
       "guides on this site tell you how. What you would be giving up is the part that "
       "is not on paper: one counterparty carrying the goods, the documents and the "
       "failure."),
      ("Why three and not five?",
       "Because beyond three columns nobody decides. Three is enough to show the shape "
       "of the trade-off and few enough to read in one sitting."),
     ],
     "faq_h2": "Questions about the comparison",
     "faq_sub": "The four we are asked before the first sheet.",
     "related": ("The corridors behind the columns",
                 "Each one written out: producers, documents and what goes wrong.",
                 [("/china", "Sourcing from China",
                   "Factory or trader, inspection, payment, and the checks between."),
                  ("/turkiye", "Stone and tile from T&uuml;rkiye",
                   "Block against slab, grading, crating and the duty check."),
                  ("/corridors", "All four corridors",
                   "What has to exist on a route before anything can be quoted."),
                  ("/landed-price-index", "The landed price index",
                   "What freight and insurance add, by origin, from customs data.")]),
     "cta_h2": "Name the product. We will price it three ways.",
     "cta_p": ("Specification, quantity and destination is enough to start. The first "
               "sheet comes back on the lanes above within ten working days."),
     "cta_href": "/contact#enquiry",
     "cta": "Ask for the comparison",
    })


def csv_file(doc):
    out = ["group,hs,product,origin,cif_usd_per_kg,fob_usd_per_kg,freight_insurance_pct,tonnes"]
    for r in doc["rows"]:
        out.append('"%s",%s,"%s","%s",%.3f,%.3f,%.1f,%d'
                   % (r["group"], r["hs"], r["product"], r["origin"],
                      r["cif_kg"], r["fob_kg"], r["uplift"], r["tonnes"]))
    d = os.path.join("site", "data")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, f"lpi-{PERIOD}.csv")
    open(p, "w", encoding="utf-8").write("\n".join(out) + "\n")
    return p


def main():
    doc = load()
    fx = load_fx()
    print("   собрана:", index_page(doc, fx))
    for fn in (quote_check, three_origins):
        print("   собрана:", fn(doc))
    print("   таблица:", csv_file(doc))

    # карта сайта
    sm = os.path.join("site", "sitemap.xml")
    t = open(sm, encoding="utf-8").read()
    added = 0
    for slug, pr in (("landed-price-index", "0.9"), ("quote-check", "0.9"),
                     ("three-origins", "0.9")):
        if PK.HOST + slug + "<" in t:
            continue
        t = t.replace("</urlset>",
                      '  <url><loc>%s%s</loc><lastmod>%s</lastmod>'
                      '<changefreq>monthly</changefreq><priority>%s</priority></url>\n'
                      '</urlset>' % (PK.HOST, slug, doc["built"], pr))
        added += 1
    open(sm, "w", encoding="utf-8").write(t)
    print("   адресов добавлено в карту сайта:", added)

    n, size = SRCH.build_index()
    print(f"   индекс поиска: {n} страниц, {size/1024:.0f} КБ")
    return 0


if __name__ == "__main__":
    sys.exit(main())
