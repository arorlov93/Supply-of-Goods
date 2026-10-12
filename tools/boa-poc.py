# -*- coding: utf-8 -*-
"""Форма контактных лиц для рамочного соглашения на металл, W519TC26BOAS.

Attachment 002, Point of Contact Information Form. Подпись не ставится.
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bids",
                   "W519TC26BOAS", "Attachment 002 POC Form - ISP GROUP LLC.pdf")

ROWS = [
    ("Company Name:", "ISP GROUP LLC"),
    ("UEI:", "WA46PAMTYMQ7"),
    ("CAGE:", "217F4"),
    ("Address:", "16395 Biscayne Blvd, North Miami Beach, FL 33160, United States"),
    ("Name:", "Aleksandr Orlov, Member"),
    ("Email:", "info@ispgroupgc.com"),
    ("Phone Number:", "(929) 830-0038"),
]


def main():
    ss = getSampleStyleSheet()
    cell = ParagraphStyle("c", parent=ss["Normal"], fontName="Helvetica",
                          fontSize=11, leading=14)
    lab = ParagraphStyle("l", parent=cell, fontName="Helvetica-Bold")
    h = ParagraphStyle("h", parent=ss["Normal"], fontName="Helvetica-Bold",
                       fontSize=13, leading=17, spaceAfter=4)
    sub = ParagraphStyle("s", parent=ss["Normal"], fontName="Helvetica",
                         fontSize=9.5, leading=13, spaceAfter=16,
                         textColor=colors.HexColor("#444444"))

    doc = SimpleDocTemplate(os.path.abspath(OUT), pagesize=letter,
                            leftMargin=1.0*inch, rightMargin=1.0*inch,
                            topMargin=1.0*inch, bottomMargin=1.0*inch,
                            title="POC Information Form ISP GROUP LLC",
                            author="ISP GROUP LLC")
    f = [Paragraph("POINT OF CONTACT INFORMATION FORM", h),
         Paragraph("Attachment 002 to W519TC26BOAS, Basic Ordering Agreement for Steel, "
                   "US Army Contracting Command, Rock Island", sub)]
    data = [[Paragraph(a, lab), Paragraph(b, cell)] for a, b in ROWS]
    t = Table(data, colWidths=[1.7*inch, 4.8*inch])
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#888888")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f2f2f2")),
    ]))
    f.append(t)
    doc.build(f)
    print("  ->", os.path.relpath(os.path.abspath(OUT), os.getcwd()))


if __name__ == "__main__":
    main()
