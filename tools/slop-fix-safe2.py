# -*- coding: utf-8 -*-
"""Вторая часть безопасных правок по разбору Hallmark.

Первый проход закрыл простые замены. Здесь три места, где нужно переписать
правило целиком, а не подставить значение:

10a  Подчёркивание в меню выезжало анимацией right со 100% до 0. Браузер на
     это пересчитывает разметку каждый кадр. Теперь полоса стоит на месте и
     растягивается через transform:scaleX, что считает композитор.
     Первый проход заменил только строку :hover и оставил правило
     рассогласованным, здесь это исправлено.
34   clip нужен и на html, и на body: на одном body правило не держит.
50   В мобильной раскладке .jwrap схлопывается в одну колонку шириной 1fr,
     а в ней лежит картинка, которая не даёт колонке сжаться.

Запуск: python3.13 tools/slop-fix-safe2.py
"""
import pathlib, re

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

OLD_AFTER = re.compile(
    r'\.navlinks a::after\{content:"";position:absolute;left:0;right:100%;bottom:0;'
    r'height:2px;\s*background:var\(--gold\);transition:right \.26s ease\}')
NEW_AFTER = ('.navlinks a::after{content:"";position:absolute;left:0;right:0;bottom:0;'
             'height:2px;\n  background:var(--gold);transform:scaleX(0);transform-origin:left;'
             'transition:transform .26s ease}')


def main():
    pages = 0
    counts = {}
    for p in sorted(SITE.rglob("*.html")):
        s = s0 = p.read_text()

        if OLD_AFTER.search(s):
            s = OLD_AFTER.sub(NEW_AFTER, s)
            counts["10a"] = counts.get("10a", 0) + 1
        # текущий пункт меню был подчёркнут через right:0
        s = s.replace(".navlinks a[aria-current]::after{right:0}",
                      ".navlinks a[aria-current]::after{transform:scaleX(1)}")

        # 34: clip обязан стоять и на html
        if "html{overflow-x:clip}" not in s:
            s2 = re.sub(r"(\bbody\{\n?\s*margin:0;)", r"html{overflow-x:clip}\n\1", s, count=1)
            if s2 != s:
                s = s2
                counts["34"] = counts.get("34", 0) + 1

        # 50: одноколоночная раскладка пути груза держит картинку
        if ".jwrap{grid-template-columns:1fr}" in s:
            s = s.replace(".jwrap{grid-template-columns:1fr}",
                          ".jwrap{grid-template-columns:minmax(0,1fr)}")
            counts["50"] = counts.get("50", 0) + 1

        if s != s0:
            p.write_text(s)
            pages += 1
    print(f"страниц изменено: {pages}")
    for k in sorted(counts):
        print(f"  правило {k}: страниц {counts[k]}")


if __name__ == "__main__":
    main()
