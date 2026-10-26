# -*- coding: utf-8 -*-
"""Единая цветокоррекция фотобиблиотеки.

Свободные снимки собраны у разных людей, разными камерами и в разную погоду.
По отдельности каждый приемлем, вместе они выглядят как папка находок, а не
как съёмка для одного сайта. Дорого смотрится не редкий кадр, а серия: один
контраст, один уход теней в холод, одна насыщенность.

Поэтому кадры приводятся к общему виду здесь, в файлах, а не фильтром в CSS.
Фильтр в браузере пересчитывается на каждый кадр прокрутки и был одной из
причин рывков, да и на разных страницах он стоял разный.

Оригиналы хранятся в media-src рядом с репозиторием и не выкладываются:
коррекция всегда считается от них, поэтому повторный запуск не наслаивается
сам на себя и правку всегда можно отыграть назад.

Запуск: python3.13 tools/grade.py [слот ...]   (без имён: вся библиотека)
"""
import pathlib, shutil, sys
from PIL import Image, ImageEnhance

ROOT = pathlib.Path(__file__).resolve().parent.parent
MEDIA = ROOT / "site" / "media"
SRC = ROOT / "media-src"

# Доля холода в тенях и тепла в светах. Больше - и кадр отдаёт синевой,
# что на порту читается как дешёвый фильтр.
SHADOW = (0, 0, 0)
HIGH = (0, 0, 0)
SAT = 0.0          # тема Formwork: только чёрно-белое
CONTRAST = 1.35    # жёсткое: белые чистые, чёрные глубокие
GAMMA = 0.93       # экспозиция чуть выше


def curve():
    """Таблицы на канал: тени уводятся в холод, света в тепло, переход
    плавный, чтобы на небе не появилось полос."""
    tables = []
    for ch in range(3):
        t = []
        for i in range(256):
            x = i / 255.0
            # вес теней и светов, плавно и без излома в середине
            w_lo = (1 - x) ** 2
            w_hi = x ** 2
            v = x * 255 + SHADOW[ch] * w_lo + HIGH[ch] * w_hi
            # лёгкая S-кривая: середина чуть разводится по контрасту
            v = v + (v - 128) * (CONTRAST - 1) * (1 - abs(x - 0.5) * 1.2)
            t.append(max(0, min(255, int(round(v)))))
        tables.append(t)
    return tables[0] + tables[1] + tables[2]


LUT = curve()


def grade(im):
    im = im.convert("RGB")
    im = ImageEnhance.Color(im).enhance(SAT)
    im = im.point(LUT)
    if GAMMA != 1.0:
        g = [max(0, min(255, int(round(255 * (i / 255) ** GAMMA)))) for i in range(256)]
        im = im.point(g * 3)
    return im


def main(only=None):
    SRC.mkdir(exist_ok=True)
    done = 0
    for jpg in sorted(MEDIA.glob("*.jpg")):
        slot = jpg.stem
        if only and slot not in only:
            continue
        master = SRC / f"{slot}.jpg"
        if not master.exists():
            shutil.copyfile(jpg, master)       # первый прогон: кадр как пришёл
        im = grade(Image.open(master))
        im.save(jpg, "JPEG", quality=84, optimize=True, progressive=True)
        im.save(MEDIA / f"{slot}.webp", "WEBP", quality=82, method=5)
        done += 1
    print(f"кадров приведено к общему виду: {done}")
    print(f"оригиналы лежат в {SRC}")


if __name__ == "__main__":
    main(sys.argv[1:] or None)
