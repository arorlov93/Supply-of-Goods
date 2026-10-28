# -*- coding: utf-8 -*-
"""Предзагрузка шапки: один файл вместо двух.

Что нашлось при замере. На главной стоит строка

    <link rel="preload" as="image" href="media/ops.<хэш>.webp" fetchpriority="high">

а сам снимок в разметке лежит в <picture> с набором ступеней 390, 780,
1536 и 2400. Эти двое друг про друга не знают. Предзагрузка тянет
исходник на 2400 точек и 314 КБ всегда, независимо от экрана, а
<picture> после разбора разметки выбирает по своим правилам ступень
1536 и тянет ещё 145 КБ. Итого 459 КБ на один снимок, и так на каждом
устройстве: замер подтвердил обе загрузки и на 1440, и на 390.

Почему так вышло. preload с голым href это запрос на конкретный файл.
Чтобы предзагрузка участвовала в том же выборе, что и <picture>, ей
нужно отдать тот же набор и те же размеры показа через imagesrcset и
imagesizes. Тогда браузер считает её тем же ресурсом, берёт одну
ступень и второй раз не ходит.

href при этом остаётся: он нужен браузерам, которые imagesrcset не
понимают. Ставим в него не исходник, а среднюю ступень, чтобы и в этом
случае не качать лишнего.

Запуск: python3.13 tools/hero-preload.py
Повторный запуск ничего не меняет.
"""
import pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
PRELOAD = re.compile(r'<link rel="preload" as="image" href="(/?)(media/[^"]+)"([^>]*)>')


def main():
    fixed = skipped = 0
    for p in sorted(SITE.rglob("*.html")):
        s = p.read_text()
        m = PRELOAD.search(s)
        if not m:
            continue
        if "imagesrcset" in m.group(0):
            skipped += 1
            continue
        slash, href, rest = m.group(1), m.group(2), m.group(3)
        stem = href.rsplit("/", 1)[-1].split(".")[0]

        # набор и размеры берём у того самого <source>, который и выиграет
        src = re.search(r'<source srcset="([^"]*%s[^"]*)" sizes="([^"]*)"' % re.escape(stem), s)
        if not src:
            print(f"  {p.name}: не нашёл <source> для {stem}, пропускаю")
            continue
        srcset, sizes = src.group(1), src.group(2)

        # href ставим на среднюю ступень: он сработает только там, где
        # imagesrcset не понимают, и тянуть туда исходник незачем
        steps = re.findall(r'(media/[^\s,]+)\s+(\d+)w', srcset)
        steps.sort(key=lambda x: int(x[1]))
        mid = steps[len(steps) // 2][0] if steps else href

        new = ('<link rel="preload" as="image" href="%s%s" '
               'imagesrcset="%s" imagesizes="%s"%s>'
               % (slash, mid, srcset, sizes, rest))
        s = s[: m.start()] + new + s[m.end():]
        p.write_text(s)
        print(f"  {p.name}: предзагрузка согласована, {len(steps)} ступеней")
        fixed += 1

    print(f"страниц исправлено: {fixed}, уже было: {skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
