# -*- coding: utf-8 -*-
"""Наполнить /chemicals содержанием. Английская версия.

Было 364 слова при 995-1249 у соседних страниц коридоров. Пять шагов
"как мы поставляем" состояли из одного предложения каждый. Страница
такого объёма не конкурирует ни за один коммерческий запрос, и это
главная причина, по которой химия из брифа никуда не выходит.

Что добавлено и откуда взято. Весь текст это либо знание о товаре и о
том, как устроена его закупка, либо описание того, что мы и так делаем
и что уже написано в других разделах сайта: аккредитив против
документов, инспекция третьей стороной, полный комплект документов,
работа от своего имени, контейнерными партиями. Ни одной новой
характеристики компании, ни одной цифры о себе, ни одного названия
завода здесь не появляется.

Самая ценная часть это раздел о пересчёте на активное вещество. Две
цены за килограмм продукта несравнимы, пока их не привели к цене за
килограмм активного вещества, и покупатели промышленной химии ищут
ровно это.

Запуск: python3.13 tools/deepen-chemicals.py
Повторный запуск ничего не меняет.
"""
import json, pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
PAGE = SITE / "chemicals.html"

# --- пять шагов: каждый разворачивается из одного предложения в раздел
STEPS = {
 "s1": [
  "A chemical name is not a specification. ATMP at fifty per cent in water "
  "and ATMP at ninety-five per cent as a solid are the same molecule and two "
  "different purchases: different freight, different handling, different "
  "price per kilogram of the thing that actually works. The first question "
  "we ask is never the quantity. It is the active content and the test "
  "method it is measured by.",
  "For a scale inhibitor or a phosphonate, tell us the grade, the active "
  "content, the form and the limits that matter to you: chloride, iron, free "
  "phosphate, colour. For a coagulant, the alumina content and the basicity, "
  "and whether it has to meet a drinking water standard. For an ion exchange "
  "resin, the type and matrix, the ionic form it ships in, bead size and "
  "uniformity coefficient, moisture retention and total capacity. For a "
  "molecular sieve, the type, the form and size, static water adsorption, "
  "crush strength and attrition.",
  "Tell us the end use as well, not only the product. End use decides which "
  "impurity matters. A resin for condensate polishing and a resin for metal "
  "recovery can carry the same type designation and fail each other's duty.",
 ],
 "s2": [
  "We send the technical data sheet, the safety data sheet and a specimen "
  "certificate of analysis before any price. They are not formalities and "
  "they are not interchangeable. The data sheet is what the producer "
  "undertakes to make. The certificate of analysis is what one batch "
  "actually was. A producer who will not show a recent certificate before "
  "the order is telling you something about the next one.",
  "The safety data sheet has to be in the format and the language the "
  "destination requires, and it carries the facts that decide the shipment: "
  "UN number, hazard class, packing group, and the labelling the terminal "
  "will look for. Those three lines decide whether a product travels in a "
  "standard container, whether the port accepts it, and what the freight "
  "costs. A quotation that arrives without them is not yet comparable to "
  "anything.",
 ],
 "s3": [
  "We quote on one basis: named Incoterm and port, pack and net weight, lead "
  "time from order to readiness, the document set that travels with the "
  "goods, and how long the price holds. Everything that is not in that line "
  "is not in the price.",
  "Then convert before you compare. Two offers for the same phosphonate, one "
  "at fifty per cent active and one at sixty, are not fifteen per cent "
  "apart: on active basis the cheaper looking one can be the dearer. Add the "
  "pack: drums that are priced with a deposit, bags that the destination "
  "will not accept and that have to be repacked, an IBC that cannot be "
  "returned. Add the Incoterm: an FOB price and a CIF price are different "
  "numbers for the same cargo. We put every offer on the same active basis, "
  "the same pack and the same Incoterm, and that comparison is what we send "
  "you, with the arithmetic shown.",
 ],
 "s4": [
  "Production runs against the agreed specification, and every batch leaves "
  "with its own certificate of analysis, dated, with the batch number that "
  "appears on the drums. Retained samples stay with the producer for the "
  "shelf life of the product, which is what makes a later claim possible at "
  "all.",
  "Where the order justifies it, or your tender requires it, an independent "
  "inspector attends before shipment. You name the agency, we do not: SGS, "
  "Intertek and Bureau Veritas all work at the origins we buy from. The "
  "scope is yours to set, and the useful one covers sampling and sealing, "
  "quantity and net weight, pack condition and marking, container cleanliness "
  "and the seal number. The inspection certificate goes into the document "
  "set named in the credit, so the money moves against the goods and not "
  "only against paper.",
 ],
 "s5": [
  "Pack is a cost decision and it is taken before production, not after. "
  "Twenty-five kilogram bags, two hundred and fifty kilogram drums, one "
  "tonne intermediate bulk containers and, for liquids in volume, a tank "
  "container. Each changes the weight that fits in a container, the labour "
  "at the far end and the price per kilogram landed. Wooden pallets travel "
  "under the international standard for wood packaging and carry the mark "
  "that proves it.",
  "Temperature is part of the specification, not an afterthought. Several of "
  "these products crystallise, stratify or freeze below a stated "
  "temperature, and a winter shipment into a continental destination has to "
  "say so in the contract. So does shelf life: the date of manufacture on "
  "the certificate of analysis, not the date of shipment, is what the clock "
  "runs from.",
  "Goods move by sea, by rail or by road, under our contract from the plant "
  "gate to the agreed delivery point, with the documents travelling with "
  "them.",
 ],
}

# --- новый раздел: допустимость
ADMIS_H = "What decides whether a chemical is admissible"
ADMIS = [
 "A chemical is admissible or it is not, and that is settled before the "
 "order rather than at the border. Three things decide it.",
 "The first is the regime at destination. Industrial chemicals are "
 "registered, notified or licensed under different rules in each market, and "
 "the obligation usually sits with the importer rather than with us. We will "
 "tell you what the producer can document; what your authority requires of "
 "you is yours to confirm, and we would rather raise it in week one than "
 "find it at the quay.",
 "The second is the use. Anything that touches drinking water is judged "
 "against a potable water standard, and the certificate has to name the "
 "grade and the plant. An industrial grade of the same product, at the same "
 "assay, is not a substitute for it and no paperwork makes it one.",
 "The third is the hazard classification. The UN number, the class and the "
 "packing group decide the stowage, the documents, the labelling and often "
 "whether a terminal will handle the box at all. They are properties of the "
 "product, decided at the plant. A shipment that is right commercially and "
 "wrong on one label is still a shipment that does not clear.",
]

# --- FAQ. Ответы повторяют то, что уже обещано в других разделах сайта.
FAQ_H = "What buyers ask before the first order"
FAQ = [
 ("Can you quote a product that is not in the table?",
  "Usually yes. The table is what we quote most often, not the limit of what "
  "we buy. Send the product, the grade and the active content, and we will "
  "come back on whether we can source it properly or not. If we cannot, we "
  "say so rather than send you a quotation we cannot stand behind."),
 ("What is the smallest order you will handle?",
  "We work in full container loads, because that is where the economics "
  "hold. A first order is normally one or two containers on full commercial "
  "terms. Below that the freight per kilogram rises faster than any saving "
  "on the goods, and we would be selling you a worse deal than you can get "
  "locally."),
 ("Do you supply drinking water grade?",
  "Where the producer holds the certification for it and can show it by "
  "plant and by grade, yes, and the certificate travels with the goods. "
  "Where it holds only an industrial grade, we say so and quote the "
  "industrial grade as what it is."),
 ("Can we nominate the inspection agency?",
  "Yes, and we would rather you did. You name the agency and the scope, the "
  "inspection happens before shipment, and the certificate goes into the "
  "document set named in the credit. An inspector we chose ourselves would "
  "prove less to you."),
 ("Can you bid into our tender?",
  "Yes. For a tender we provide the manufacturer's letter of authorization, "
  "certificates of origin and quality and the product documents your "
  "committee requires. Send the tender number and the deadline with the "
  "enquiry so the file is assembled to the right date."),
 ("How are we protected if the goods are wrong?",
  "By the structure rather than by a promise. The specification is agreed in "
  "writing before production, every batch carries its own certificate of "
  "analysis, an inspector you name attends before shipment, and payment is "
  "made against the document set named in the credit. Each of those is a "
  "point at which a wrong consignment stops instead of arriving."),
]

CSS = """
/* развёрнутые разделы химии */
.chem-q{margin:0 0 6px;font-size:1.02rem;font-weight:600;color:var(--ink)}
.chem-a{margin:0 0 22px;line-height:1.62;color:var(--ink-2);max-width:72ch}
"""


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def main():
    s = PAGE.read_text()
    before = s

    # 1. развернуть пять шагов
    for sid, paras in STEPS.items():
        m = re.search(r'(?s)(<h2 id="%s">.*?</h2><div class="ptext">)(.*?)(</div>)'
                      % sid, s)
        if not m:
            print("  ВНИМАНИЕ: шаг %s не найден" % sid)
            continue
        # Прежнее предложение-заглушка не сохраняется: оно пересказывает
        # первый же абзац развёрнутого текста, и рядом они читаются как
        # повтор.
        body = "".join("<p>%s</p>" % p for p in paras)
        if m.group(2) == body:
            continue                       # уже развёрнут
        s = s[:m.start(2)] + body + s[m.end(2):]

    # 2. раздел о допустимости, перед блоком "For tenders"
    if ADMIS_H not in s:
        block = ('<div class="lede" style="margin-top:56px"><h2>%s</h2>'
                 '<p class="intro">%s</p></div>%s'
                 % (ADMIS_H, ADMIS[0],
                    "".join('<p class="chem-a">%s</p>' % p for p in ADMIS[1:])))
        anchor = '<div class="lede" style="margin-top:56px"><h2>For tenders</h2>'
        if anchor in s:
            s = s.replace(anchor, block + anchor, 1)
        else:
            print("  ВНИМАНИЕ: блок For tenders не найден")

    # 3. FAQ перед формой
    if FAQ_H not in s:
        qa = "".join('<p class="chem-q">%s</p><p class="chem-a">%s</p>' % (q, a)
                     for q, a in FAQ)
        block = ('<div class="lede" style="margin-top:56px"><h2>%s</h2></div>%s'
                 % (FAQ_H, qa))
        anchor = '<div class="lede" id="rfq">'
        if anchor in s:
            s = s.replace(anchor, block + anchor, 1)
        else:
            print("  ВНИМАНИЕ: блок формы не найден")

    # 4. разметка FAQPage: из-за неё выдача показывает вопросы под ссылкой
    if '"@type": "FAQPage"' not in s:
        data = {"@context": "https://schema.org", "@type": "FAQPage",
                "mainEntity": [{"@type": "Question", "name": q,
                                "acceptedAnswer": {"@type": "Answer", "text": a}}
                               for q, a in FAQ]}
        tag = ('<script type="application/ld+json">%s</script>\n'
               % json.dumps(data, ensure_ascii=False))
        s = s.replace("</body>", tag + "</body>", 1)

    # 5. стили
    if CSS.strip() not in s:
        s = s.replace("</head>", "<style>%s</style>\n</head>" % CSS, 1)

    if s != before:
        PAGE.write_text(s)
        print("  /chemicals дополнена")
    else:
        print("  /chemicals уже дополнена")

    txt = re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<(script|style).*?</\1>", "", s))
    print("слов на странице: примерно %d" % len(txt.split()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
