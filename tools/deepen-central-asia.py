# -*- coding: utf-8 -*-
"""Наполнить /central-asia содержанием. Английская версия.

Было 81 слово. У четырёх соседних страниц коридоров от 995 до 1249.
Страница в восемьдесят слов не ранжируется ни по одному запросу, и
пятый коридор из брифа существует только в меню.

Текст построен по образцу остальных коридоров: вводный абзац, таблица
фактов, пять разделов, вопросы покупателей, призыв. Содержание это
устройство маршрута и то, что спрашивает таможня. Ничего о себе сверх
того, что уже обещано на сайте: работа от своего имени, полный комплект
документов, инспекция третьей стороной, аккредитив.

Чего тут сознательно нет. Ни России, ни Беларуси, ни маршрутов через
них: это прямое требование брифа от 10.11.2026, пункт 8. Ни Ирана: это
санкционный риск для компании, пункт 8 CLAUDE.md. Ни сроков доставки в
днях: проверенных цифр у нас нет, а выдуманный срок на странице о
логистике это обещание, которое первым же рейсом не исполнится.

Запуск: python3.13 tools/deepen-central-asia.py
Повторный запуск ничего не меняет.
"""
import json, pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
PAGE = SITE / "central-asia.html"

STEPS = [
 ("s1", "Landlocked changes the arithmetic", [
  "On a sea lane the freight is a line in the quotation. On this one it is "
  "most of the quotation. There is no discharge port at the destination, so "
  "every tonne finishes its journey on rail or on a truck, and on goods that "
  "are heavy for their value, which is what industrial chemicals and "
  "materials are, the land leg decides whether the deal exists at all.",
  "That changes what a quotation has to contain. A sea freight rate tells "
  "you almost nothing here. What matters is the rail tariff for the wagon or "
  "the container, the dwell at the border crossing, the cost of moving the "
  "goods between two railway systems, and who pays for the box while it "
  "waits. We price those four as named lines rather than folding them into a "
  "single figure you cannot interrogate.",
 ]),
 ("s2", "The gauge changes at the border", [
  "Chinese railways run on standard gauge. Kazakhstan and its neighbours run "
  "on the wider gauge used across the region. The two do not meet, so at "
  "Khorgos and at Dostyk every load either changes wagon or the wagon "
  "changes its running gear. This is not a formality. It is a physical "
  "operation with a cost, a queue and a failure mode.",
  "The failure mode matters more than the cost. Drummed liquids and bagged "
  "solids that are handled loose at a transloading terminal arrive with "
  "split bags, dented drums and a short delivery. A container avoids it: the "
  "box is lifted across in one move and the goods inside are never touched. "
  "That is why we quote containerised wherever the product and the volume "
  "allow it, and why we say so when a product does not allow it.",
 ]),
 ("s3", "The Caspian leg is a schedule risk, not a distance", [
  "For cargo that crosses the Caspian the water is the short part. Aktau and "
  "Kuryk sit on the eastern shore, Alat on the western, and the sailing "
  "itself is a matter of hours. The waiting is not. Sailings are allocated "
  "rather than scheduled in the way a container line schedules, weather "
  "closes the ports, and a missed slot is measured in days.",
  "So we do not quote a transit time that assumes every connection holds. We "
  "quote a window, we say what can move it, and we tell you the cost of the "
  "delay rather than discovering it with you later. If a date is genuinely "
  "fixed at your end, say so at the enquiry: it changes the routing we "
  "recommend and sometimes it changes the pack.",
 ]),
 ("s4", "What the customs office asks for, country by country", [
  "The commercial set is the same everywhere: invoice, packing list, "
  "certificate of origin and the transport document. For chemicals two more "
  "travel with the goods and are read carefully: the safety data sheet, with "
  "the UN number, the hazard class and the packing group, and the "
  "certificate of analysis for the batch that is actually in the drums.",
  "Conformity is where the countries differ. In Kazakhstan and Kyrgyzstan "
  "goods inside the scope of the customs union technical regulations carry "
  "the conformity mark, and the declaration or certificate is issued before "
  "the goods move, not after they arrive. Uzbekistan, Turkmenistan and "
  "Azerbaijan each run their own regime. In most of them the registration "
  "obligation sits with the importer rather than with the seller, which is "
  "precisely why we raise it in the first week: we will tell you what the "
  "producer can document, and what is yours to hold is yours to confirm.",
  "Language is part of the file. A document the office cannot read is a "
  "document that is missing, and a translation produced at the border costs "
  "more than one produced at the plant.",
 ]),
 ("s5", "Winter is part of the specification", [
  "This is a continental climate and the cargo is in it for weeks. Rail "
  "wagons are not heated and containers are not insulated. Several of the "
  "products that move down this corridor crystallise, stratify or freeze "
  "below a stated temperature, and once a drummed liquid has frozen it is "
  "rarely the same product afterwards.",
  "The answer is not a note in an e-mail. The contract states the lowest "
  "temperature the cargo is expected to see, the pack is chosen for it, and "
  "where the product genuinely cannot take the season, the honest answer is "
  "to ship it in a different one. A shipment released in November crosses in "
  "deep winter, and that is a decision taken at the order, not at the "
  "border.",
 ]),
]

TENDER_H = "Tenders in the region"
TENDER = [
 "National oil, gas, power, mining and water companies in these countries "
 "buy through tender, and the file decides the outcome more often than the "
 "price does.",
 "For a tender we provide the manufacturer's letter of authorization naming "
 "the tender, certificates of origin and quality, the product documents your "
 "committee lists, and the commercial terms in the form the tender asks for "
 "them. Where the tender requires a bid bond, a local representative or a "
 "registration that only the bidder can hold, we say so at the start rather "
 "than at submission. Send the tender number and the closing date with the "
 "enquiry and the file is assembled to that date.",
]

FAQ_H = "What buyers ask about this lane"
FAQ_LEDE = ("The questions that decide whether a shipment on this corridor "
            "works, answered the way we answer them on a first call.")
FAQ = [
 ("How long does it take from China to Kazakhstan?",
  "It depends on the crossing and on the slot, and anyone who answers with a "
  "single number is quoting the best case. We give a window for the specific "
  "shipment, name what can move it, and update it when the wagon is "
  "allocated. A figure that holds only when nothing goes wrong is not a "
  "figure you can plan against."),
 ("Can you deliver to our site, or only to the border?",
  "To the site where the destination allows it, under a delivered term, with "
  "the inland leg priced as its own line so you can see what it costs. Where "
  "only the importer can clear the goods, we deliver to the agreed point "
  "before clearance and hand over the full document set."),
 ("Who handles customs clearance?",
  "Usually the importer, because in most of these countries the registration "
  "and the conformity obligations sit with the buyer and cannot be "
  "transferred to a foreign seller. We supply the documents that clearance "
  "needs, in the language it needs them, and we check the set against the "
  "destination's list before the goods leave."),
 ("Do you move hazardous chemicals on this corridor?",
  "Where the classification allows it and the carriers accept it. The UN "
  "number, the class and the packing group decide the pack, the labelling, "
  "the wagon and the documents, and they are settled before production. "
  "Where a product cannot move compliantly on this route we say so and "
  "propose the route it can move on."),
 ("What payment terms do you work on?",
  "A documentary credit payable at sight against the document set, which is "
  "the structure we prefer with a buyer we have no history with. The set "
  "includes a pre-shipment inspection certificate from an agency you name, "
  "so the money moves against the goods and not only against paper."),
 ("We are not a national company. Will you still quote?",
  "Yes. Distributors, contractors and plant operators buy on this corridor "
  "too. The volume that makes the economics work is a full container load; "
  "below that the land leg per tonne rises faster than any saving on the "
  "goods, and we will tell you so rather than quote it."),
]

CTA_H = "Send a specification. Get a landed price."
CTA = ("Product, grade, quantity and the delivery point are enough to start. "
       "No account, no registration, no fee.")


def toc():
    return ('<nav class="toc" aria-label="On this page"><ol>%s</ol></nav>'
            % "".join('<li><a href="#%s"><span>%02d</span>%s</a></li>'
                      % (sid, i + 1, h) for i, (sid, h, _) in enumerate(STEPS)))


def prose():
    out = []
    for i, (sid, h, paras) in enumerate(STEPS):
        out.append('<div class="pblock"><span class="k">%02d</span>'
                   '<h2 id="%s">%s</h2><div class="ptext">%s</div></div>'
                   % (i + 1, sid, h, "".join("<p>%s</p>" % p for p in paras)))
    return '<div class="prose">%s</div>' % "".join(out)


def extra():
    t = ('<div class="lede" style="margin-top:56px"><h2>%s</h2>'
         '<p class="intro">%s</p></div>%s'
         % (TENDER_H, TENDER[0],
            "".join('<p class="ca-a">%s</p>' % p for p in TENDER[1:])))
    qa = "".join("<details><summary>%s</summary><p>%s</p></details>" % (q, a)
                 for q, a in FAQ)
    f = ('<div class="lede" style="margin-top:56px"><h2>%s</h2>'
         '<p class="intro">%s</p></div><div style="margin-top:34px">%s</div>'
         % (FAQ_H, FAQ_LEDE, qa))
    c = ('<div class="lede" style="margin-top:56px"><h2>%s</h2>'
         '<p class="intro">%s</p><p style="margin-top:18px">'
         '<a class="btn" href="/contact#enquiry">Request a quote</a></p></div>'
         % (CTA_H, CTA))
    return t + f + c


CSS = """
/* развёрнутый пятый коридор */
.ca-a{margin:0 0 20px;line-height:1.62;color:var(--ink-2);max-width:72ch}
"""


def main():
    s = PAGE.read_text()
    before = s
    block = toc() + prose() + extra()

    if 'id="s1"' not in s:
        # всё содержание встаёт после таблицы фактов, перед карточкой химии
        anchor = '<div class="lanelinks" style="margin-top:48px">'
        if anchor not in s:
            print("  ВНИМАНИЕ: якорь не найден, страница не тронута")
            return 1
        s = s.replace(anchor, block + anchor, 1)

    if '"@type": "FAQPage"' not in s:
        data = {"@context": "https://schema.org", "@type": "FAQPage",
                "mainEntity": [{"@type": "Question", "name": q,
                                "acceptedAnswer": {"@type": "Answer", "text": a}}
                               for q, a in FAQ]}
        s = s.replace("</body>", '<script type="application/ld+json">%s</script>\n'
                      % json.dumps(data, ensure_ascii=False) + "</body>", 1)

    if CSS.strip() not in s:
        s = s.replace("</head>", "<style>%s</style>\n</head>" % CSS, 1)

    if s != before:
        PAGE.write_text(s)
        print("  /central-asia дополнена")
    else:
        print("  /central-asia уже дополнена")
    txt = re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<(script|style).*?</\1>", "", s))
    print("слов на странице: примерно %d" % len(txt.split()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
