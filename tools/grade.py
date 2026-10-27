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
import pathlib, re, shutil, sys
from PIL import Image, ImageEnhance

ROOT = pathlib.Path(__file__).resolve().parent.parent
MEDIA = ROOT / "site" / "media"
SRC = ROOT / "media-src"
# имена в media версионированы хэшем содержимого, см. tools/media-version.py;
# слот (имя мастера в media-src) это имя без хэша
VERSIONED = re.compile(r"^(.+)\.[0-9a-f]{8}$")

# Доля холода в тенях и тепла в светах. Больше - и кадр отдаёт синевой,
# что на порту читается как дешёвый фильтр.
SHADOW = (0, 0, 0)
HIGH = (0, 0, 0)
# Цвет остаётся в файле, а обесцвечивает его CSS: по наведению на снимок
# фильтр снимается и кадр оживает. Держать для этого второй, цветной
# комплект файлов не нужно, и по наведению ничего не догружается.
SAT = 0.88
# Контраст 1.35 был рассчитан на чёрно-белый кадр. В цвете он же вытягивает
# цветную засветку: натриевые лампы на складе дают едкую желтизну, и кадр
# читается как дешёвый фильтр. Поэтому в файл кладётся мягкая градация, а
# жёсткость Formwork добавляет CSS там же, где обесцвечивает, и уходит
# вместе с обесцвечиванием при наведении.
CONTRAST = 1.12
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


# Предельная ширина по слоту. Кадр крупнее, чем нужно на экране, это не
# запас качества, а лишние байты и лишняя работа по раскодированию прямо во
# время прокрутки. Значения взяты по замеру самой широкой выдачи на сайте
# при двойной плотности пикселей, с запасом около 1,15.
# Замер: tools/ (см. отчёт по избыточности), пересчитывать при смене вёрстки.
MAXW = {
    "j-quay": 1700, "j-road": 1700, "j-arrival": 1700,
    "timber": 1200, "steel-tubes": 1200, "equipment": 1200, "port-noir": 1200,
}


def slot_of(path):
    m = VERSIONED.match(path.stem)
    return m.group(1) if m else path.stem


def main(only=None):
    SRC.mkdir(exist_ok=True)
    # webp лежит под своим хэшем, отличным от хэша jpg: собираем по слоту
    webp = {slot_of(f): f for f in MEDIA.glob("*.webp")}
    done = 0
    for jpg in sorted(MEDIA.glob("*.jpg")):
        slot = slot_of(jpg)
        if only and slot not in only:
            continue
        master = SRC / f"{slot}.jpg"
        if not master.exists():
            shutil.copyfile(jpg, master)       # первый прогон: кадр как пришёл
        im = grade(Image.open(master))
        cap = MAXW.get(slot)
        if cap and im.width > cap:
            im = im.resize((cap, round(im.height * cap / im.width)), Image.LANCZOS)
        im.save(jpg, "JPEG", quality=84, optimize=True, progressive=True)
        im.save(webp.get(slot, MEDIA / f"{slot}.webp"), "WEBP", quality=82, method=5)
        done += 1
    print(f"кадров приведено к общему виду: {done}")
    print(f"оригиналы лежат в {SRC}")


if __name__ == "__main__":
    main(sys.argv[1:] or None)
