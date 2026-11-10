# -*- coding: utf-8 -*-
"""Вынести содержание политики соответствия на саму страницу. Английская.

Было 97 слов и кнопка на PDF. Проблемы две, и обе серьёзные.

Для поиска: PDF индексируется хуже страницы, а у нас в нём лежат девять
разделов, которые как раз и отвечают на запросы вида "sanctions
compliance supplier" и "OFAC screening policy". Текст есть, но он
спрятан.

Для покупателя: тендерный комитет и служба комплаенса крупного
покупателя смотрят страницу до того, как скачают файл. Девяносто семь
слов не дают им ничего, и до PDF доходит не каждый.

Текст ниже это пересказ разделов 3, 4, 5, 6 и 7 той же политики, слово
в слово по смыслу. Ни одного нового обязательства здесь не появляется:
если бы появилось, оно разошлось бы с подписанным документом.

Запуск: python3.13 tools/deepen-compliance.py
Повторный запуск ничего не меняет.
"""
import json, pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
PAGE = SITE / "compliance.html"

BLOCKS = [
 ("Who we screen, and when", [
  "Before every quotation, before every contract and before every payment we "
  "screen the counterparty by legal name and by any trading name it uses, "
  "the owners of the counterparty and any person who controls it, the end "
  "user of the goods where that is not the counterparty, the consignee, the "
  "notify party and the ultimate destination, and the vessel, the carrier "
  "and the bank where they are known to us.",
  "The screening is repeated before payment, not carried forward from the "
  "quotation. Ownership changes and listings change between a quotation and "
  "a shipment, and a clear result obtained in week one proves nothing about "
  "week ten.",
 ]),
 ("The lists we screen against", [
  "The Specially Designated Nationals and Blocked Persons List and the "
  "Consolidated Sanctions List of the US Office of Foreign Assets Control; "
  "the Denied Persons, Entity and Unverified Lists of the US Bureau of "
  "Industry and Security; the Consolidated United Nations Security Council "
  "Sanctions List; the consolidated list of the European Union; and the UK "
  "Sanctions List.",
  "Ownership is assessed against the fifty per cent rule. An entity owned, "
  "directly or indirectly, fifty per cent or more in the aggregate by one or "
  "more blocked persons is treated as blocked itself, whether or not it "
  "appears on any list by name.",
 ]),
 ("What we will not do", [
  "We do not deal with persons or entities subject to sanctions, nor with "
  "comprehensively sanctioned territories.",
  "We never misstate the origin, the destination or the end user of goods, "
  "in a document, in a declaration or in correspondence, and we do not "
  "accept an instruction to do so.",
  "We do not structure a transaction, a routing or a payment in order to "
  "avoid the application of a sanctions or export control rule, and we do "
  "not assist another party to do so.",
  "We do not supply goods where we know, or have reason to believe, that "
  "they are intended for a prohibited end use, including a military, "
  "nuclear, missile or chemical and biological weapons end use where that "
  "end use is controlled.",
 ]),
 ("What stops a transaction", [
  "A transaction is stopped and reviewed before it proceeds where the end "
  "user is unwilling to be named or the stated end use does not fit the "
  "goods or the quantity; where the delivery address, the consignee or the "
  "routing changes after the contract is agreed, or the routing is not "
  "commercially sensible; where payment is offered from a third party, from "
  "an unrelated jurisdiction, or in a manner that obscures its origin; where "
  "the counterparty asks for documents to show something other than the "
  "facts; or where the counterparty, its owners or the destination are "
  "connected to a sanctioned territory.",
  "Each of those is resolved on evidence or the transaction is declined. An "
  "assurance by itself does not resolve any of them. Where a transaction "
  "cannot be made compliant, we decline it, and no order value changes that "
  "answer.",
 ]),
 ("Records", [
  "Screening results, the identity evidence obtained, the end user "
  "information and the reasons for any decision to decline are kept with the "
  "transaction file for at least five years from the date of the "
  "transaction, in line with the record keeping periods of the US sanctions "
  "and export control regulations.",
  "A concern about a transaction, a counterparty or this policy may be "
  "raised directly with the member at info@ispgroupgc.com. A concern raised "
  "in good faith has no adverse consequence for the person raising it.",
 ]),
]

CSS = """
/* разделы политики соответствия */
.comp-h{margin:40px 0 10px;font-size:1.14rem;line-height:1.3;color:var(--ink)}
.comp-p{margin:0 0 16px;line-height:1.62;color:var(--ink-2);max-width:72ch}
"""


def main():
    s = PAGE.read_text()
    before = s

    if BLOCKS[0][0] not in s:
        out = []
        for h, paras in BLOCKS:
            out.append('<h2 class="comp-h">%s</h2>%s'
                       % (h, "".join('<p class="comp-p">%s</p>' % p
                                     for p in paras)))
        anchor = '<div class="lede" style="margin-top:56px"><h2>Company details</h2>'
        if anchor not in s:
            print("  ВНИМАНИЕ: якорь не найден, страница не тронута")
            return 1
        s = s.replace(anchor, "".join(out) + anchor, 1)

    if CSS.strip() not in s:
        s = s.replace("</head>", "<style>%s</style>\n</head>" % CSS, 1)

    if s != before:
        PAGE.write_text(s)
        print("  /compliance дополнена")
    else:
        print("  /compliance уже дополнена")
    txt = re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<(script|style).*?</\1>", "", s))
    print("слов на странице: примерно %d" % len(txt.split()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
