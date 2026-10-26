# -*- coding: utf-8 -*-
"""Убрать надстрочные подписи над заголовками.

Правило Hallmark 54 и пункт 9 его «пола»: никаких eyebrow. Надстрочная
подпись над крупным заголовком, вида «03 — What we supply», это самый
узнаваемый признак страницы, собранной моделью. Она ничего не добавляет:
заголовок под ней говорит ровно то же самое, только крупнее. Нумерация
разделов тоже служебная, читателю она не нужна, а длинное тире в ней
нарушает ещё и правило 19.

Номера шагов пути груза при этом не выбрасываются: они несут смысл
последовательности. Они переезжают внутрь заголовка шага, из отдельной
строки над ним становясь его началом. Тогда это не надпись над заголовком,
а часть заголовка.

Запуск: python3.13 tools/slop-eyebrows.py
"""
import pathlib, re

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

# подпись над заголовком: убирается целиком
EYEBROW = re.compile(
    r'<span class="eyebrow[^"]*"[^>]*>.*?</span>\s*', re.S)
# номер шага перед заголовком: переезжает внутрь него
STEP = re.compile(
    r'<span class="k">([^<]{1,12})</span>\s*<(h[23])([^>]*)>(.*?)</\2>', re.S)


def main():
    pages, cut, moved = 0, 0, 0
    for p in sorted(SITE.rglob("*.html")):
        s = s0 = p.read_text()

        n = len(EYEBROW.findall(s))
        s = EYEBROW.sub("", s)
        cut += n

        def step(m):
            nonlocal moved
            moved += 1
            num, tag, attrs, text = m.groups()
            return f'<{tag}{attrs}><span class="k">{num}</span>{text}</{tag}>'

        s = STEP.sub(step, s)

        if s != s0:
            p.write_text(s)
            pages += 1
    print(f"страниц изменено: {pages}")
    print(f"  надстрочных подписей убрано: {cut}")
    print(f"  номеров шагов перенесено в заголовок: {moved}")


if __name__ == "__main__":
    main()
