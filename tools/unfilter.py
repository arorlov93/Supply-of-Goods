# -*- coding: utf-8 -*-
"""Снять цветокоррекцию из CSS: теперь она в самих файлах.

На страницах стояло шесть разных наборов filter для фотографий, от
saturate(.7) до grayscale(.42) с sepia. Это и была одна из причин, по
которой библиотека выглядела разнородной: один и тот же кадр на двух
страницах отличался по цвету. Плюс браузер пересчитывает filter при каждой
отрисовке, а на прокрутке это заметно.

Коррекция перенесена в файлы (tools/grade.py), поэтому статические наборы
отсюда убираются. Остаются только те, что не про цвет, а про поведение:
подложка под липкой шапкой и затемнение, завязанное на прогресс прокрутки.

Запуск: python3.13 tools/unfilter.py
"""
import pathlib, re

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

# убираются только эти, перечисленные дословно: подстановка по образцу
# задела бы подложку шапки и затемнение по прогрессу прокрутки
DROP = [
    "filter:saturate(.72) contrast(1.12) brightness(.8)",
    "filter:grayscale(.42) contrast(1.04) saturate(.85) sepia(.06)",
    "filter:saturate(.8) contrast(1.06) brightness(.95)",
    "filter:saturate(.78) contrast(1.06) brightness(.94)",
    "filter:saturate(.7) contrast(1.09) brightness(.8)",
    "filter:saturate(.78) contrast(1.06) brightness(.92)",
    "filter:saturate(.72) contrast(1.04)",
]


def main():
    pages = hits = 0
    for p in sorted(SITE.rglob("*.html")):
        s = s0 = p.read_text()
        for d in DROP:
            if d in s:
                hits += s.count(d)
                s = s.replace(d + ";", "").replace(d, "")
        s = re.sub(r";{2,}", ";", s)
        if s != s0:
            p.write_text(s)
            pages += 1
    print(f"наборов снято: {hits}, страниц затронуто: {pages}")


if __name__ == "__main__":
    main()
