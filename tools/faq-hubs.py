# -*- coding: utf-8 -*-
"""Вопросы и ответы на узловых страницах.

Из сорока шести страниц блок вопросов стоял на тридцати четырёх, и его
не было ровно там, где он нужнее всего: на «что мы поставляем», на
«коридорах» и на «руководствах». Это страницы, куда человек попадает из
поиска с общим вопросом, а не с готовой темой.

Зачем. Короткий прямой ответ на отдельный вопрос это то, что поисковик
поднимает в расширенный ответ, а языковая модель берёт в цитату: его
можно вынуть со страницы целиком, не потеряв смысл. Связный текст на
три экрана так вынуть нельзя.

Разметка добавляется вместе с видимым блоком, а не вместо него:
размечать то, чего нет на странице, нельзя, и правила поисковиков это
прямо запрещают.

Вопросы взяты настоящие, те, что задают до первого заказа, и ответы
совпадают с тем, что написано на самих страницах.

Запуск: python3.13 tools/faq-hubs.py
Повторный запуск ничего не дублирует.
"""
import json, pathlib, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
ANCHOR = '<section data-reveal class="cta">'

DATA = {
"supply.html": [
 ("Do you only supply these six categories?",
  "No. The six are where producer relationships and a documented lane already exist, so a quotation comes back in days rather than weeks. A product outside them is a sourcing project: we say so, we say how long it will take, and we quote the work honestly rather than pretending it is routine."),
 ("What is the minimum order?",
  "There is no fixed minimum. The practical floor is whatever makes the freight sensible: a full container on most lines, or a consolidated part load where several suppliers in the same region ship together. Below that it is the logistics cost per unit that decides, not a policy of ours."),
 ("Can you supply to a specification rather than to a brand?",
  "Yes, and across most of these categories that is the cheaper answer. A written specification with the standard, the tolerance and the certificates is what makes offers from different producers comparable. Where a brand is required we buy the brand, and the check becomes authenticity and channel instead."),
 ("How long does a quotation take?",
  "A first reply within one working day, and a landed price in about ten working days on a lane we already run. The time goes into producer verification and freight, not into the arithmetic."),
],
"corridors.html": [
 ("What is a trade corridor, and why should a buyer care?",
  "It is the whole chain on one route: verified producers, a forwarder, a customs broker and a document set that has cleared before. It matters because a price is only as good as the chain behind it, and on a new route that chain has to be built before anything can be quoted honestly."),
 ("Can you ship to a country that is not on this list?",
  "Usually yes, and the first shipment takes longer. What has to be built first is the admissibility check for the destination, a broker who has cleared this product there, and a document set that has actually passed. We say how long that will take before we quote, not after."),
 ("Why do you quote some lanes DAP rather than FOB?",
  "Because on a corridor where the inland leg carries most of the risk, a price at the port tells the buyer very little. DAP puts the ocean freight, the port charges, the transit documentation and the road leg into one number at the agreed place."),
 ("Do you handle customs clearance at the destination?",
  "We coordinate it through the broker on the lane and put the document set in the buyer's hands before the vessel arrives. The importer of record remains the buyer unless the contract says otherwise, because that is who is liable for the classification and the duty."),
],
"guides.html": [
 ("Do I have to register or leave an email to read these?",
  "No. Every guide is open, there is nothing gated and nothing to download. They were written because we were answering the same questions on the phone over and over."),
 ("Which should I read first if I have never imported?",
  "Incoterms, then what a landed price has to include. The first decides who pays for what and where the risk passes. The second shows every line between a factory price and your own gate, including the three that are usually left out."),
 ("I already have a supplier. Which ones apply to me?",
  "How to verify a supplier is a factory, who is liable for the HS code, and the proforma invoice. Those three cover the mistakes that cost money after a deal already looks agreed."),
 ("Are these specific to the United States?",
  "The rules described are international: Incoterms, the Harmonized System, documentary credits and the bill of lading work the same way everywhere. Where a figure is country specific, the guide says which country it applies to."),
],
}


def visible(items):
    out = ['<section data-reveal id="faq"><div class="wrap"><div class="lede">'
           '<h2>Questions on this</h2><p class="intro">The ones we are asked most often.</p></div>'
           '<div style="margin-top:34px">']
    for q, a in items:
        out.append(f"<details><summary>{q}</summary><p>{a}</p></details>")
    out.append("</div></div></section>\n")
    return "".join(out)


def schema(items):
    d = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in items
        ],
    }
    return ('<script type="application/ld+json">'
            + json.dumps(d, ensure_ascii=False, indent=1)
            + "</script>\n")


def main():
    done = skipped = 0
    for name, items in DATA.items():
        p = SITE / name
        if not p.is_file():
            print(f"  нет файла {name}")
            continue
        s = p.read_text()
        if "FAQPage" in s:
            skipped += 1
            continue
        i = s.find(ANCHOR)
        if i < 0:
            print(f"  ОШИБКА: не нашёл призыв к действию в {name}")
            return 1
        s = s[:i] + visible(items) + s[i:]
        h = s.find("</head>")
        s = s[:h] + schema(items) + s[h:]
        p.write_text(s)
        done += 1
    print(f"страниц с блоком вопросов добавлено: {done}, уже было: {skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
