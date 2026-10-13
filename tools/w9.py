#!/usr/bin/env python3.13
"""Собирает W-9 для ISP GROUP LLC на официальном бланке IRS редакции March 2024.

Значения наносятся на страницу как содержимое, а поля формы убираются. Так
файл выглядит одинаково в любой программе и никто не поправит в нём цифры.

Поля подписи и даты на бланке не заполняются и заполнены быть не могут:
подписывает человек, см. CLAUDE.md, раздел 4.

    python3.13 tools/w9.py [путь-к-пустому-бланку] [куда-писать]

Пустой бланк: https://www.irs.gov/pub/irs-pdf/fw9.pdf
"""

import io
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas

# Данные ровно как в карточке SAM. Менять только вслед за SAM.
NAME = "ISP GROUP LLC"
BUSINESS_NAME = ""          # строка 2 пустая, торгового имени нет
LLC_CLASS = "S"             # строка 3a, классификация LLC: C, S или P
ADDRESS = "16395 Biscayne Blvd Apt 818"
CITY_STATE_ZIP = "Aventura, FL 33160-5743"
EIN = "384380828"           # девять цифр без дефиса

FONT = "Helvetica"
SIZE = 10

# Координаты взяты из прямоугольников полей самого бланка IRS.
X_TEXT = 61.0
Y_NAME = 664.0
Y_BUSINESS = 640.0
Y_ADDRESS = 496.0
Y_CITY = 472.0

LLC_BOX = (74.0, 592.0)       # галочка «Limited liability company»
LLC_LETTER = (420.0, 591.5)   # буква классификации рядом с ней

EIN_Y = 356.0
EIN_FIRST_X = 424.8           # центр первой цифры, шаг 14.4
EIN_SECOND_X = 468.0          # центр третьей цифры
EIN_STEP = 14.4


def overlay(width: float, height: float):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(width, height))
    c.setFont(FONT, SIZE)

    c.drawString(X_TEXT, Y_NAME, NAME)
    if BUSINESS_NAME:
        c.drawString(X_TEXT, Y_BUSINESS, BUSINESS_NAME)
    c.drawString(X_TEXT, Y_ADDRESS, ADDRESS)
    c.drawString(X_TEXT, Y_CITY, CITY_STATE_ZIP)

    c.setFont(FONT, 9)
    c.drawString(*LLC_BOX, "X")
    c.setFont(FONT, SIZE)
    c.drawString(*LLC_LETTER, LLC_CLASS)

    digits = EIN.replace("-", "").strip()
    if len(digits) != 9 or not digits.isdigit():
        raise SystemExit(f"EIN должен быть девятью цифрами, получено: {EIN!r}")
    for i, d in enumerate(digits[:2]):
        c.drawCentredString(EIN_FIRST_X + i * EIN_STEP, EIN_Y, d)
    for i, d in enumerate(digits[2:]):
        c.drawCentredString(EIN_SECOND_X + i * EIN_STEP, EIN_Y, d)

    c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]


def main() -> None:
    blank = Path(sys.argv[1] if len(sys.argv) > 1 else "fw9.pdf")
    out = Path(sys.argv[2] if len(sys.argv) > 2
               else "company/W-9 ISP GROUP LLC.pdf")

    if not blank.exists():
        raise SystemExit(
            f"Нет пустого бланка {blank}. Скачать:\n"
            "  curl -o fw9.pdf https://www.irs.gov/pub/irs-pdf/fw9.pdf"
        )

    reader = PdfReader(str(blank))
    page = reader.pages[0]          # страницы 2-6 это инструкция, не отдаём
    box = page.mediabox
    page.merge_page(overlay(float(box.width), float(box.height)))

    writer = PdfWriter()
    writer.add_page(page)
    # Убираем поля формы: значения уже впечатаны, редактировать нечего.
    if "/Annots" in writer.pages[0]:
        del writer.pages[0]["/Annots"]
    root = writer._root_object
    if "/AcroForm" in root:
        del root["/AcroForm"]

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("wb") as fh:
        writer.write(fh)
    print(f"записано: {out}")


if __name__ == "__main__":
    main()
