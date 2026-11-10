# -*- coding: utf-8 -*-
"""Политика соответствия в PDF: site/ISP_GROUP_COMPLIANCE_POLICY.pdf.

Файл, на который ведёт кнопка со страницы /compliance.

Подпись НЕ ставится. Правило работы: подпись за человека не ставится
нигде и никогда, включая государственные формы. В документе оставлено
пустое поле для подписи и даты, их заполняет участник общества сам, от
руки или своей электронной подписью.

Содержание построено на абзаце из брифа и на обычной структуре программы
соответствия OFAC: приверженность руководства, оценка риска, внутренние
процедуры, проверка, обучение, хранение записей. Никаких утверждений,
которых нельзя подтвердить: ни о проведённых аудитах, ни об отдельном
офицере по соответствию, ни о датах проверок.

Запуск: python3.13 tools/compliance-pdf.py
"""
import pathlib, sys
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, ListFlowable, ListItem)
from reportlab.lib import colors

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "ISP_GROUP_COMPLIANCE_POLICY.pdf"

INK = colors.HexColor("#15161c")
MUTED = colors.HexColor("#5d6070")
RULE = colors.HexColor("#c9ccd6")

H1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=17, leading=21,
                    textColor=INK, spaceAfter=4)
SUB = ParagraphStyle("sub", fontName="Helvetica", fontSize=9.5, leading=13,
                     textColor=MUTED, spaceAfter=18)
H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.5, leading=14,
                    textColor=INK, spaceBefore=14, spaceAfter=5)
P = ParagraphStyle("p", fontName="Helvetica", fontSize=9.6, leading=14.2,
                   textColor=INK, alignment=TA_JUSTIFY, spaceAfter=7)
LI = ParagraphStyle("li", parent=P, alignment=0, spaceAfter=3)
SMALL = ParagraphStyle("small", fontName="Helvetica", fontSize=8.4, leading=11.6,
                       textColor=MUTED)

COMPANY = "ISP GROUP LLC"
DETAILS = [
    ("Legal name", "ISP GROUP LLC"),
    ("Florida Document No.", "M26000003981"),
    ("EIN", "38-4380828"),
    ("Unique Entity ID (UEI)", "WA46PAMTYMQ7"),
    ("CAGE code", "217F4"),
    ("Registered office", "16395 Biscayne Blvd, North Miami Beach, FL 33160, USA"),
    ("Contact", "info@ispgroupgc.com, +1 929 830 0038"),
]

SECTIONS = [
 ("1. Purpose and scope", [
  "This policy states how ISP GROUP LLC complies with the sanctions and "
  "export control laws of the United States. It applies to the company, to "
  "its member and to anyone acting for it, in every transaction, in every "
  "country, without exception.",
  "ISP GROUP LLC is a company incorporated in the State of Florida and is "
  "subject to United States law, including the sanctions programmes "
  "administered by the Office of Foreign Assets Control of the US Department "
  "of the Treasury (OFAC) and the export control regulations administered by "
  "the Bureau of Industry and Security of the US Department of Commerce "
  "(BIS).",
 ]),
 ("2. Commitment", [
  "The member of the company is responsible for compliance with this policy "
  "and may not delegate that responsibility away. No commercial "
  "consideration, no customer relationship and no order value justifies a "
  "departure from it. Where a transaction cannot be made compliant, the "
  "company declines the transaction.",
 ]),
 ("3. Who we screen, and when", [
  "Before every quotation, before every contract and before every payment we "
  "screen:",
 ], [
  "the counterparty, by legal name and by any trading name used;",
  "the owners of the counterparty, and any person who controls it;",
  "the end user of the goods, where that is not the counterparty;",
  "the consignee, the notify party and the ultimate destination;",
  "the vessel, the carrier and the bank, where they are known to us.",
 ], [
  "Screening is repeated before payment because ownership and listings "
  "change between the quotation and the shipment. A clear screening result "
  "obtained at the quotation stage is not carried forward to settlement.",
 ]),
 ("4. Lists we screen against", [
  "We screen against the Specially Designated Nationals and Blocked Persons "
  "List and the Consolidated Sanctions List of OFAC, the Denied Persons, "
  "Entity and Unverified Lists of BIS, the Consolidated United Nations "
  "Security Council Sanctions List, the consolidated list of the European "
  "Union and the UK Sanctions List.",
  "Ownership is assessed against the fifty per cent rule: an entity owned, "
  "directly or indirectly, fifty per cent or more in the aggregate by one or "
  "more blocked persons is itself treated as blocked, whether or not it "
  "appears on a list by name.",
 ]),
 ("5. What we will not do", [
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
 ("6. Red flags", [
  "A transaction is stopped and reviewed before it proceeds where any of the "
  "following appears:",
 ], [
  "the end user is unwilling to be named, or the stated end use does not fit "
  "the goods or the quantity;",
  "the delivery address, the consignee or the routing changes after the "
  "contract is agreed, or the routing is not commercially sensible;",
  "payment is offered from a third party, from an unrelated jurisdiction, or "
  "in a manner that obscures its origin;",
  "the counterparty asks for documents to show something other than the "
  "facts;",
  "the counterparty, its owners or the destination are connected to a "
  "sanctioned territory.",
 ], [
  "A red flag is resolved on the evidence or the transaction is declined. "
  "It is not resolved by assurance alone.",
 ]),
 ("7. Records", [
  "Screening results, the identity evidence obtained, the end user "
  "information and the reasons for any decision to decline are kept with the "
  "transaction file for at least five years from the date of the "
  "transaction, in line with the record keeping periods of the US sanctions "
  "and export control regulations.",
 ]),
 ("8. Training and review", [
  "Anyone acting for the company is made aware of this policy before "
  "handling an enquiry. The policy is reviewed at least once a year and "
  "whenever a sanctions programme that affects our trade changes "
  "materially.",
 ]),
 ("9. Reporting a concern", [
  "A concern about a transaction, a counterparty or this policy may be "
  "raised directly with the member at info@ispgroupgc.com. A concern raised "
  "in good faith has no adverse consequence for the person raising it.",
 ]),
]


def rule(w=6.9 * inch):
    t = Table([[""]], colWidths=[w], rowHeights=[0.5])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.6, RULE)]))
    return t


def bullets(items):
    return ListFlowable(
        [ListItem(Paragraph(x, LI), leftIndent=12, value="bullet") for x in items],
        bulletType="bullet", bulletFontSize=6, bulletOffsetY=-1.5,
        leftIndent=14, spaceBefore=2, spaceAfter=7)


def build():
    doc = SimpleDocTemplate(
        str(OUT), pagesize=LETTER,
        leftMargin=0.8 * inch, rightMargin=0.8 * inch,
        topMargin=0.75 * inch, bottomMargin=0.75 * inch,
        title="Sanctions and Export Control Compliance Policy",
        author=COMPANY, subject="Compliance policy")

    f = []
    f.append(Paragraph("Sanctions and Export Control Compliance Policy", H1))
    f.append(Paragraph(COMPANY + " &mdash; United States", SUB))
    f.append(rule())
    f.append(Spacer(1, 14))

    for sec in SECTIONS:
        head, paras = sec[0], sec[1]
        f.append(Paragraph(head, H2))
        for t in paras:
            f.append(Paragraph(t, P))
        if len(sec) > 2:
            f.append(bullets(sec[2]))
        if len(sec) > 3:
            for t in sec[3]:
                f.append(Paragraph(t, P))

    f.append(Spacer(1, 16))
    f.append(rule())
    f.append(Spacer(1, 10))
    f.append(Paragraph("Company details", H2))
    rows = [[Paragraph(k, SMALL), Paragraph(v, SMALL)] for k, v in DETAILS]
    t = Table(rows, colWidths=[2.0 * inch, 4.9 * inch])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, colors.HexColor("#e4e6ec")),
    ]))
    f.append(t)

    # Поле подписи остаётся пустым: подпись ставит человек, а не инструмент.
    f.append(Spacer(1, 26))
    f.append(Paragraph("Approved by", H2))
    sig = Table([["", ""], [Paragraph("Signature", SMALL), Paragraph("Date", SMALL)],
                 [Paragraph("Aleksandr Orlov, Member", SMALL), ""]],
                colWidths=[3.4 * inch, 2.2 * inch], rowHeights=[26, 14, 14])
    sig.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (0, 0), 0.6, INK),
        ("LINEBELOW", (1, 0), (1, 0), 0.6, INK),
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ]))
    f.append(sig)

    doc.build(f)
    return OUT


if __name__ == "__main__":
    p = build()
    print("  %s, %.1f КБ" % (p.relative_to(ROOT), p.stat().st_size / 1024))
    print("  подпись не поставлена: поле оставлено пустым под живую подпись")
    sys.exit(0)
