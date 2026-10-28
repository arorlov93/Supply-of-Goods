# -*- coding: utf-8 -*-
"""Снимки объектов для страницы поставочных референсов.

Откуда. Две презентации, которые дал владелец: подрядная презентация по
объектам в России и материалы девелопера по вилам на Бали. Снимки лежат
внутри PDF отдельными файлами, их видно pdfimages, пересжимать страницу
целиком не нужно.

Что здесь важно. На сайте уже наведён порядок с весом и сдвигом макета,
и девять новых снимков могут всё это сломать. Поэтому каждый кадр идёт
тремя файлами: широкий на крупный экран, средний и узкий на телефон,
плюс JPEG для соцсетей и старых клиентов. Размеры жёстко прописаны в
разметке, значит места под снимок браузер резервирует заранее и страница
не прыгает.

Кадры обрезаются до 16:10. Не из любви к пропорции, а потому что в сетке
они стоят рядом: разная высота соседних плиток читается как ошибка.

Имена здесь базовые, без хэша. Хэш проставит tools/media-version.py, он
же перепишет ссылки на страницах.

Запуск: python3.13 tools/ref-photos.py
Повторный запуск перезаписывает файлы тем же содержимым.
"""
import pathlib, sys
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
MEDIA = ROOT / "site" / "media"
SCRATCH = pathlib.Path(
    "/tmp/claude-0/-home-user-Supply-of-Goods/"
    "4f5e4e6d-222f-57da-93ad-94f5b2132f9f/scratchpad")

RU = SCRATCH / "pres" / "big"
BALI = SCRATCH / "bali" / "raw"

# имя на сайте -> исходный файл
SOURCES = {
    "ref-bridge":    RU / "p21-005.png",    # железнодорожный мост, Находка
    "ref-resort":    RU / "p22-010.png",    # монолит и опалубка, Артём
    "ref-ferry":     RU / "p11-005.png",    # причал паромной переправы, Холмск
    "ref-shore":     RU / "p12-007.png",    # отсыпка берега, Никольское
    "ref-moles":     RU / "p10-007.png",    # тетраподы, молы порта Холмск
    "ref-moscow":    RU / "p13-005.png",    # Мясницкая 21с8, Москва
    "ref-plant":     RU / "p20-005.png",    # рыбозавод, Петропавловск-Камчатский
    "ref-villa":     BALI / "i-000.jpg",    # вилла снаружи, вывеска, улица
    "ref-villa-pool": BALI / "i-030.jpg",   # гостиная с видом на бассейн
    "ref-villa-in":  BALI / "i-026.jpg",    # внутренняя отделка
}

# Ширина показа в сетке около 620 точек на широком экране и около 390 на
# телефоне. Верхняя ступень взята с запасом на экран двойной плотности.
WIDTHS = [390, 760, 1240]
RATIO = 16 / 10
QUALITY = 82
# Кадры, которым нужен ещё и JPEG: он уходит в og:image
OG = {"ref-bridge"}
# Кадры, которым нужна верхняя ступень. Только шапка: плитки сетки
# показываются на 346 точках, крупный файл там никто не увидит, а
# телефон с тройной плотностью его честно скачает.
FULL = {"ref-bridge"}


# Доля высоты, с которой начинается полоса кадра. По умолчанию 0.38: на
# стройке небо сверху пустое, а низ кадра это то, ради чего снимок и взят.
# Где кадр устроен иначе, доля задаётся отдельно.
CROP_Y = {
    # Вертикальный рендер улицы: дом, вывеска и вход внизу, сверху одни пальмы.
    "ref-villa": 0.72,
}


def crop_to_ratio(im, frac=0.38):
    w, h = im.size
    if w / h > RATIO:
        new_w = int(round(h * RATIO))
        off = (w - new_w) // 2
        return im.crop((off, 0, off + new_w, h))
    new_h = int(round(w / RATIO))
    off = int((h - new_h) * frac)
    return im.crop((0, off, w, off + new_h))


def main():
    missing = [str(p) for p in SOURCES.values() if not p.is_file()]
    if missing:
        print("нет исходников:")
        for m in missing:
            print("  ", m)
        return 1

    MEDIA.mkdir(parents=True, exist_ok=True)
    made = 0
    for name, src in SOURCES.items():
        im = Image.open(src).convert("RGB")
        im = crop_to_ratio(im, CROP_Y.get(name, 0.38))
        nat_w = im.size[0]
        # Верхняя ступень это сам исходник, но не крупнее последней из
        # WIDTHS: кадр на 1724 точки показывать негде, а весит он вдвое.
        top = min(nat_w, WIDTHS[-1])
        widths = [w for w in WIDTHS if w < top] + ([top] if name in FULL else [])
        widths = widths or [min(nat_w, WIDTHS[-2])]
        for w in widths:
            h = int(round(w / RATIO))
            frame = im.resize((w, h), Image.LANCZOS)
            stem = name if w == top else f"{name}-{w}"
            frame.save(MEDIA / f"{stem}.webp", quality=QUALITY, method=6)
            made += 1
            if w == top and name in OG:
                # JPEG нужен только тому кадру, который уходит в карточку
                # соцсетей: WebP там до сих пор понимают не все. Остальным
                # девяти он не нужен ни разу, а это полтора мегабайта
                # файлов, на которые никто никогда не сошлётся.
                frame.save(MEDIA / f"{stem}.jpg", quality=QUALITY,
                           optimize=True, progressive=True)
                made += 1
        print(f"  {name:16s} {im.size[0]}x{im.size[1]} -> {widths}")

    total = sum((MEDIA / f).stat().st_size
                for f in [p.name for p in MEDIA.iterdir()]
                if f.startswith("ref-"))
    print(f"файлов записано: {made}, суммарно {total/1024:.0f} КБ")
    return 0


if __name__ == "__main__":
    sys.exit(main())
