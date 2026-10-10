# -*- coding: utf-8 -*-
"""Техническая часть заявки 1240LS26Q0079: лист соответствия спецификации.

Требование солиситации, пункт 5: Technical Information of the items listed in
the schedule demonstrating that the offered item meets specifications.
Фактор 1 разрешает закрыть его спецлистом или брошюрой производителя. Этот
лист идёт первым, брошюра поставщика прикладывается отдельным файлом.
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "bids", "1240LS26Q0079",
                   "04 Technical Information - 1240LS26Q0079.pdf")

PIPE_SPEC = ("Corrugated steel pipe, 16 gauge (0.064 in nominal wall), hot dip "
             "galvanized, 2-2/3 in x 1/2 in corrugation, ends rerolled annular "
             "for standard coupling bands. Manufactured to ASTM A760 and "
             "AASHTO M36, zinc coated sheet to ASTM A929.")
BAND_SPEC = ("Hugger type coupling band, galvanized steel, width and corrugation "
             "matched to the pipe, furnished complete with bolts and nuts. "
             "Manufactured to ASTM A760 and AASHTO M36.")

ROWS = [
    ("0001", '18 in dia. x 12 ft culvert, 16 ga galvanized, CMP ends for standard bands', "10 EA", PIPE_SPEC),
    ("0002", '18 in dia. x 20 ft culvert, 16 ga galvanized, CMP ends for standard bands', "20 EA", PIPE_SPEC),
    ("0003", '24 in dia. x 12 ft culvert, 16 ga galvanized, CMP ends for standard bands', "60 EA", PIPE_SPEC),
    ("0004", '24 in dia. x 20 ft culvert, 16 ga galvanized, CMP ends for standard bands', "60 EA", PIPE_SPEC),
    ("0005", '36 in dia. x 20 ft culvert, 16 ga galvanized, CMP ends for standard bands', "10 EA", PIPE_SPEC),
    ("0006", '18 in CMP hugger band with bolts', "15 EA", BAND_SPEC),
    ("0007", '24 in CMP hugger band with bolts', "60 EA", BAND_SPEC),
    ("0008", '36 in CMP hugger band with bolts', "10 EA", BAND_SPEC),
]


def main():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica",
                          fontSize=9.5, leading=12.5, spaceAfter=6)
    small = ParagraphStyle("s", parent=body, fontSize=8, leading=10)
    h1 = ParagraphStyle("h1", parent=ss["Normal"], fontName="Helvetica-Bold",
                        fontSize=13, leading=16, spaceAfter=2)
    h2 = ParagraphStyle("h2", parent=ss["Normal"], fontName="Helvetica-Bold",
                        fontSize=10, leading=13, spaceBefore=10, spaceAfter=4)

    doc = SimpleDocTemplate(os.path.abspath(OUT), pagesize=letter,
                            leftMargin=0.8 * inch, rightMargin=0.8 * inch,
                            topMargin=0.7 * inch, bottomMargin=0.7 * inch,
                            title="Technical Information 1240LS26Q0079",
                            author="ISP GROUP LLC")
    f = []
    f.append(Paragraph("ISP GROUP LLC", h1))
    f.append(Paragraph("16395 Biscayne Blvd, North Miami Beach, FL 33160 &nbsp;|&nbsp; "
                       "UEI WA46PAMTYMQ7 &nbsp;|&nbsp; CAGE 217F4 &nbsp;|&nbsp; "
                       "info@ispgroupgc.com", small))
    f.append(Spacer(1, 12))
    f.append(Paragraph("Technical Information", h1))
    f.append(Paragraph("Solicitation 1240LS26Q0079, Manti-LaSal National Forest "
                       "Culverts and Hardware", body))

    f.append(Paragraph("1. Items offered", h2))
    data = [[Paragraph("<b>CLIN</b>", small), Paragraph("<b>Item required</b>", small),
             Paragraph("<b>Qty</b>", small), Paragraph("<b>Technical characteristics offered</b>", small)]]
    for clin, item, qty, spec in ROWS:
        data.append([Paragraph(clin, small), Paragraph(item, small),
                     Paragraph(qty, small), Paragraph(spec, small)])
    t = Table(data, colWidths=[0.45 * inch, 1.85 * inch, 0.45 * inch, 3.15 * inch],
              repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eeeeee")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    f.append(t)
    f.append(Paragraph("Every offered item meets or exceeds the diameter, length, "
                       "gauge, coating and end treatment stated in the Schedule of "
                       "Items. O-ring gaskets are not included, which Amendment 0002 "
                       "confirms is acceptable.", body))

    f.append(Paragraph("2. Delivery", h2))
    f.append(Paragraph("All items will be delivered within 60 days after award, "
                       "F.o.b. destination, to the Forest Service Yard, 900 North "
                       "1100 East, Price, UT 84501. Our answer to the delivery "
                       "question in the Schedule of Items is Y. We will telephone "
                       "ahead to agree the delivery date so that the gate is open "
                       "and an offloading operator is present, and we will deliver "
                       "in as few shipments as the load allows. Earlier delivery "
                       "will be offered if the mill releases sooner.", body))

    f.append(Paragraph("3. Country of origin and Buy American", h2))
    f.append(Paragraph("All items offered under CLIN 0001 through 0008 are domestic "
                       "end products of the United States, as entered in the Country "
                       "of Origin table. The Buy American, Free Trade Agreements, "
                       "Israeli Trade Act Certificate at 52.225-4 is completed on "
                       "that basis.", body))

    f.append(Paragraph("4. Offer validity, amendments and registration", h2))
    f.append(Paragraph("Prices are firm for 90 calendar days from the date set for "
                       "receipt of offers. Amendments 0001 and 0002 are acknowledged "
                       "and signed copies are enclosed. ISP GROUP LLC is actively "
                       "registered in SAM.gov under UEI WA46PAMTYMQ7 and CAGE 217F4, "
                       "including NAICS 331210, and will remain so through award.", body))

    f.append(Paragraph("5. Enclosures", h2))
    f.append(Paragraph("01 Quote, Attachment 1 completed with the Schedule of Items, "
                       "Quoter's Company Information, Country of Origin table and "
                       "SF-1449 blocks 17a and 30a to 30c.<br/>"
                       "02 Amendment 0001, signed.<br/>"
                       "03 Amendment 0002, signed.<br/>"
                       "04 This Technical Information sheet.<br/>"
                       "05 Manufacturer specification sheet for the offered pipe and "
                       "bands.", body))

    doc.build(f)
    print("  ->", os.path.relpath(os.path.abspath(OUT), os.getcwd()))


if __name__ == "__main__":
    main()
