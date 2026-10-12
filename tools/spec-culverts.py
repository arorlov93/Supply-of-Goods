# -*- coding: utf-8 -*-
"""Спецификация для поставщиков труб. Одна страница, по-английски.

Всё содержание подтверждено ответами заказчика в поправке 001 и 002.
Ни номера закупки, ни заказчика, ни сроков подачи здесь нет и быть не может,
см. CLAUDE.md раздел 1.
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bids",
                   "1240LS26Q0079", "ISP GROUP - Material Specification - CMP Price UT.pdf")

ITEMS = [
    ("1", "Corrugated steel pipe, 18 in diameter x 12 ft length, 16 gauge, galvanized, ends rerolled annular for hugger bands", "10 EA"),
    ("2", "Corrugated steel pipe, 18 in diameter x 20 ft length, 16 gauge, galvanized, ends rerolled annular for hugger bands", "20 EA"),
    ("3", "Corrugated steel pipe, 24 in diameter x 12 ft length, 16 gauge, galvanized, ends rerolled annular for hugger bands", "60 EA"),
    ("4", "Corrugated steel pipe, 24 in diameter x 20 ft length, 16 gauge, galvanized, ends rerolled annular for hugger bands", "60 EA"),
    ("5", "Corrugated steel pipe, 36 in diameter x 20 ft length, 16 gauge, galvanized, ends rerolled annular for hugger bands", "10 EA"),
    ("6", "Annular hugger band with bolts, 18 in", "15 EA"),
    ("7", "Annular hugger band with bolts, 24 in", "60 EA"),
    ("8", "Annular hugger band with bolts, 36 in", "10 EA"),
]


def main():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica",
                          fontSize=9.5, leading=12.5, spaceAfter=5)
    small = ParagraphStyle("s", parent=body, fontSize=8.5, leading=10.5, spaceAfter=0)
    h1 = ParagraphStyle("h1", parent=ss["Normal"], fontName="Helvetica-Bold",
                        fontSize=13, leading=16, spaceAfter=2)
    h2 = ParagraphStyle("h2", parent=ss["Normal"], fontName="Helvetica-Bold",
                        fontSize=10, leading=13, spaceBefore=9, spaceAfter=3)

    doc = SimpleDocTemplate(os.path.abspath(OUT), pagesize=letter,
                            leftMargin=0.8*inch, rightMargin=0.8*inch,
                            topMargin=0.7*inch, bottomMargin=0.7*inch,
                            title="ISP GROUP LLC Material Specification",
                            author="ISP GROUP LLC")
    f = []
    f.append(Paragraph("ISP GROUP LLC", h1))
    f.append(Paragraph("16395 Biscayne Blvd, North Miami Beach, FL 33160 &nbsp;|&nbsp; "
                       "(929) 830-0038 &nbsp;|&nbsp; info@ispgroupgc.com &nbsp;|&nbsp; "
                       "www.ispgroupgc.com", small))
    f.append(Spacer(1, 12))
    f.append(Paragraph("Material Specification", h1))
    f.append(Paragraph("Corrugated steel pipe and coupling bands, delivered to Price, Utah 84501", body))

    f.append(Paragraph("1. Quantities", h2))
    data = [[Paragraph("<b>Item</b>", small), Paragraph("<b>Description</b>", small),
             Paragraph("<b>Quantity</b>", small)]]
    for n, d, q in ITEMS:
        data.append([Paragraph(n, small), Paragraph(d, small), Paragraph(q, small)])
    t = Table(data, colWidths=[0.42*inch, 5.48*inch, 0.8*inch], repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eeeeee")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    f.append(t)
    f.append(Paragraph("Total 2,640 linear feet of pipe, approximately 25 short tons.", body))

    f.append(Paragraph("2. Pipe standard", h2))
    f.append(Paragraph(
        "Pipe shall conform to <b>AASHTO M 36</b>. Metallic coating shall conform to "
        "<b>AASHTO M 218</b>; M 196, M 274 or M 289 are equally acceptable. "
        "Helical corrugation with rerolled annular ends. <b>No specific corrugation "
        "profile is required</b>: the manufacturer's standard profile is acceptable "
        "provided the diameter, length, 16 gauge thickness, galvanization and band "
        "compatibility are met. A 2-2/3 in x 1/2 in profile is typical and acceptable.", body))

    f.append(Paragraph("3. Band standard", h2))
    f.append(Paragraph(
        "Annular hugger bands that mate with the rerolled annular pipe ends. "
        "Approximately <b>12 inches wide, H-12 style or approved equal</b>, galvanized "
        "steel, with bolt-bar-strap connectors, supplied complete with bolts. "
        "<b>O-ring gaskets are not required.</b> Band quantities above are correct as "
        "written and are not one per pipe.", body))

    f.append(Paragraph("4. Origin", h2))
    f.append(Paragraph(
        "Material must be of <b>United States origin</b>. We cannot accept "
        "Canadian-origin product on this order. Please state the country of origin "
        "and the mill location of the coil with your quotation.", body))

    f.append(Paragraph("5. Delivery", h2))
    f.append(Paragraph(
        "900 North 1100 East, Price, Utah 84501. All quantities within <b>60 days</b> "
        "of our purchase order. <b>Multiple truckloads and partial shipments are "
        "acceptable</b> within that window. Offloading equipment is on site; the yard "
        "has a locked gate, so the delivery date and window will be agreed with you in "
        "advance. Quote F.o.b. destination, or F.o.b. origin with the freight to 84501 "
        "stated separately as a lump sum and the number of trucks.", body))

    f.append(Paragraph("6. To be supplied with your quotation", h2))
    f.append(Paragraph(
        "Manufacturer technical data sheet showing diameter, length, gauge, "
        "galvanization and coupling band compatibility. Unit price per line, lead time "
        "from purchase order, how long the price stays firm, and your payment terms.", body))

    doc.build(f)
    print("  ->", os.path.relpath(os.path.abspath(OUT), os.getcwd()))


if __name__ == "__main__":
    main()
