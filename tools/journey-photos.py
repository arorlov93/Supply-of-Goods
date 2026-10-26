# -*- coding: utf-8 -*-
"""Привязать шесть шагов пути груза к своим кадрам.

Раздел «From the works to your port» показывал кадры, взятые из общей
библиотеки: machinery на первом шаге стоял ещё на десяти других страницах,
terminal и vessel тоже. Рассказ про шесть передач груза разваливался,
потому что картинки были не про него и повторялись по сайту.

Теперь у каждого шага свой кадр, отобранный под него и больше нигде не
использованный. Подмена идёт по имени файла, разметка не трогается.

Запуск: python3.13 tools/journey-photos.py
"""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
MEDIA = SITE / "media"

# шаг -> было -> стало
STEPS = [
    ("01 завод",     "machinery",     "j-works"),
    ("02 контейнер", "loading-truck", "j-stuffing"),
    ("03 дорога",    "truck-road",    "j-road"),
    ("04 причал",    "terminal",      "j-quay"),
    ("05 море",      "vessel",        "j-sea"),
    ("06 порт",      "straddle",      "j-arrival"),
]


def main():
    missing = [new for _, _, new in STEPS if not (MEDIA / f"{new}.jpg").exists()]
    if missing:
        print("нет файлов, подмена не делается:", ", ".join(missing))
        return 1

    p = SITE / "index.html"
    s = p.read_text()
    start = s.index('<ol class="jsteps">')
    end = s.index("</ol>", start)
    block = s[start:end]

    done = []
    for label, old, new in STEPS:
        a, b = f"media/{old}.webp", f"media/{new}.webp"
        c, d = f"media/{old}.jpg", f"media/{new}.jpg"
        if a in block or c in block:
            block = block.replace(a, b).replace(c, d)
            done.append(f"{label}: {old} -> {new}")

    s = s[:start] + block + s[end:]
    p.write_text(s)
    for line in done:
        print("  ", line)
    print(f"шагов перепривязано: {len(done)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
