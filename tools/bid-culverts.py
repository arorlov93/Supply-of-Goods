# -*- coding: utf-8 -*-
"""Сборка заявки на водопропускные трубы Манти-Ласаль, 1240LS26Q0079.

Накладывает наши данные и цены поверх государственных форм, ничего в них не
меняя. Подпись не ставится нигде: её ставит человек.

Запуск:  python3.13 tools/bid-culverts.py
Выход:   bids/1240LS26Q0079/*.pdf
"""
import io, os, sys
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

SRC = os.environ.get("CULV_SRC", "/tmp/claude-0/-home-user-Supply-of-Goods/"
      "4f5e4e6d-222f-57da-93ad-94f5b2132f9f/scratchpad/culv")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "bids", "1240LS26Q0079")

ATT = "1240LS26Q0079 Manti-LaSal National Forest Culverts - Attachment 1.pdf"
A1  = "1240LS26Q0079 Manit-LaSal National Forest Culverts - Amendment 001 Q and A SF30.pdf"
A2  = "1240LS26Q0079 Manti-LaSal National Forest Culverts  Amendment 002 Q and A Clarification SF30.pdf"

# ---------------------------------------------------------------- наши данные
CO      = "ISP GROUP LLC"
ADDR1   = "16395 Biscayne Blvd Apt 818"
ADDR2   = "Aventura, FL 33160-5743"
UEI     = "WA46PAMTYMQ7"
CAGE    = "217F4"
EMAIL   = "info@ispgroupgc.com"
PHONE   = "(929) 830-0038"
REP     = "Aleksandr Orlov"
TITLE   = "Member"
DATE    = os.environ.get("BID_DATE", "")   # оставляем пустым под подпись
ORIGIN  = "United States"  # по всем восьми позициям, пока поставщик не сказал иное

# ------------------------------------------------------- цены, доллары за шт
# меняются одной правкой, когда придут котировки поставщиков
PRICES = {
    "0001": 272.00, "0002": 453.00, "0003": 356.00, "0004": 594.00,
    "0005": 906.00, "0006":  37.00, "0007":  48.00, "0008":  80.00,
    "0009": 4260.00,
}
QTY = {"0001": 10, "0002": 20, "0003": 60, "0004": 60, "0005": 10,
       "0006": 15, "0007": 60, "0008": 10, "0009": 1}
ROW_Y = {"0001": 382.3, "0002": 356.5, "0003": 330.8, "0004": 305.0,
         "0005": 279.2, "0006": 253.6, "0007": 239.4, "0008": 225.2,
         "0009": 211.1}
TOTAL_Y = 196.9
ORIGIN_Y = {"0001": 295.7, "0002": 281.3, "0003": 266.9, "0004": 252.5,
            "0005": 238.1, "0006": 223.7, "0007": 209.3, "0008": 194.9}


def money(v):
    return "{:,.2f}".format(v)


def overlay(draw, pagesize=letter):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=pagesize)
    draw(c)
    c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]


def stamp(src, pages, out):
    r = PdfReader(src)
    w = PdfWriter()
    for i, p in enumerate(r.pages):
        if i in pages:
            p.merge_page(overlay(pages[i]))
        w.add_page(p)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "wb") as f:
        w.write(f)
    print("  ->", os.path.relpath(out))


# ------------------------------------------------------------- страница SF1449
def sf1449(c):
    c.setFont("Helvetica", 8.5)
    c.drawString(26, 485, CO)
    c.drawString(26, 474, ADDR1)
    c.drawString(26, 463, ADDR2)
    c.drawString(26, 452, "UEI " + UEI + "   CAGE " + CAGE)
    if PHONE:
        c.drawString(100, 392, PHONE)
    c.setFont("Helvetica", 8.5)
    c.drawString(26, 50, REP + (", " + TITLE if TITLE else ""))
    if DATE:
        c.drawString(233, 50, DATE)


# ------------------------------------------------- страница 3: цены построчно
def schedule(c):
    c.setFont("Helvetica", 9)
    total = 0.0
    for clin, y in ROW_Y.items():
        unit = PRICES[clin]
        line = unit * QTY[clin]
        total += line
        c.drawRightString(494, y, money(unit))
        c.drawRightString(568, y, money(line))
    c.setFont("Helvetica-Bold", 9.5)
    c.drawRightString(568, TOTAL_Y, money(total))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(497, 170.5, "Y")


# --------------------------------------- страница 4: данные компании-участника
def company(c):
    c.setFont("Helvetica", 9)
    c.drawString(292, 713, CO)
    c.drawString(292, 688, UEI)
    c.drawString(292, 663, EMAIL)
    if PHONE:
        c.drawString(292, 638, PHONE)
    c.drawString(292, 613, REP + (", " + TITLE if TITLE else ""))
    if DATE:
        c.drawString(292, 563, DATE)


# ---------------------------------------- страница 10: страна происхождения
def origin(c):
    c.setFont("Helvetica", 9)
    for clin, y in ORIGIN_Y.items():
        c.drawString(205, y, ORIGIN)


# ------------------------------------------------------------- поправки SF30
def sf30(c):
    c.setFont("Helvetica", 8.5)
    c.drawString(26, 630, CO)
    c.drawString(26, 619, ADDR1)
    c.drawString(26, 608, ADDR2)
    c.drawString(26, 597, "UEI " + UEI + "   CAGE " + CAGE)
    c.drawString(26, 131, REP + (", " + TITLE if TITLE else ""))
    if DATE:
        c.drawString(236, 95, DATE)


def main():
    print("Заявка 1240LS26Q0079, сборка:")
    stamp(os.path.join(SRC, ATT),
          {0: sf1449, 2: schedule, 3: company, 9: origin},
          os.path.join(OUT, "01 Quote ISP GROUP LLC - 1240LS26Q0079.pdf"))
    stamp(os.path.join(SRC, A1), {0: sf30},
          os.path.join(OUT, "02 Amendment 0001 signed - 1240LS26Q0079.pdf"))
    stamp(os.path.join(SRC, A2), {0: sf30},
          os.path.join(OUT, "03 Amendment 0002 signed - 1240LS26Q0079.pdf"))
    tot = sum(PRICES[k] * QTY[k] for k in QTY)
    print("Итого по заявке: $%s" % money(tot))


if __name__ == "__main__":
    main()
