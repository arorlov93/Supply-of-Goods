#!/usr/bin/env python3
"""Контактный лист из папки с картинками, чтобы посмотреть кандидатов глазами.

Без этого шага на сайт легко попадает файл с водяным знаком или архивный
снимок вместо современного: по названию и метаданным это не видно.

  python3 contact_sheet.py <папка> <выход.jpg> [колонок]
Потом прочитать выход.jpg как изображение.
"""
import sys, os, glob
from PIL import Image, ImageDraw

src = sys.argv[1]
dst = sys.argv[2] if len(sys.argv) > 2 else "sheet.jpg"
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 5
TW, TH = 330, 220

files = []
for f in sorted(glob.glob(os.path.join(src, "*.jpg")) + glob.glob(os.path.join(src, "*.png"))):
    if os.path.getsize(f) < 15000:
        continue
    try:
        im = Image.open(f)
        files.append((os.path.splitext(os.path.basename(f))[0], f, im.size))
    except Exception:
        pass

rows = (len(files) + cols - 1) // cols
sheet = Image.new("RGB", (TW * cols, (TH + 22) * max(rows, 1)), (16, 22, 30))
d = ImageDraw.Draw(sheet)
for i, (n, f, sz) in enumerate(files):
    im = Image.open(f).convert("RGB")
    w, h = im.size
    s = max(TW / w, TH / h)
    im = im.resize((int(w * s), int(h * s)), Image.LANCZOS)
    im = im.crop(((im.width - TW) // 2, (im.height - TH) // 2,
                  (im.width - TW) // 2 + TW, (im.height - TH) // 2 + TH))
    cx, cy = (i % cols) * TW, (i // cols) * (TH + 22)
    sheet.paste(im, (cx, cy))
    d.text((cx + 6, cy + TH + 4), f"{n} {sz[0]}x{sz[1]}", fill=(225, 235, 242))
sheet.save(dst, quality=84)
print(f"{len(files)} картинок -> {dst} {sheet.size}")
