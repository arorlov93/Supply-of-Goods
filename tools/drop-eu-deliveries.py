# -*- coding: utf-8 -*-
"""Снять с сайта утверждение, что мы поставляли В Европейский союз.

Заказчик сказал 10.11.2026: в Европу ничего не отправлялось. Значит всё,
что написано про поставки В ЕС, неправда и уходит со страниц.

Что НЕ трогаем, и почему. Закупки ИЗ ЕС были: мостовое оборудование для
Находки и бассейновое оборудование для вилл на Бали куплены у европейских
производителей. Это заказчик подтвердил отдельно, поэтому /projects
остаётся как есть, вместе с плашками "European Union -> Russia" и
"China & EU -> Indonesia".

Коридор "Americas & EU -> West Africa" тоже остаётся: это предложение
возить оттуда, а не утверждение, что мы уже возили.

Справочные страницы про правила ЕС (декларация характеристик, CE,
ветеринарный сертификат, Binding Tariff Information) остаются: это
знание, которое мы продаём, а не рассказ о собственных отгрузках.

Запуск: python3.13 tools/drop-eu-deliveries.py
Повторный запуск ничего не меняет.
"""
import pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

# Тизер на /experience, стоит в блоке коридоров на шести страницах.
TEASER = [
    ("China, the Russian north and the European Union: three regimes, "
     "one method.",
     "China and the Russian north: two regimes, one method."),
    ("China, the Russian north and the European Union: three supply regimes "
     "and one method.",
     "China and the Russian north: two supply regimes and one method."),
]

# Точечные правки /experience: заголовок, описания, вводный абзац, JSON-LD.
EXPERIENCE = [
    ("Twenty years of supply work: China, Russia, European Union",
     "Twenty years of supply work: China and the Russian north"),
    ("discharge onto unequipped Russian shores, food and equipment into the "
     "European Union.",
     "discharge onto unequipped Russian shores where there is no quay and "
     "the navigation window is measured in weeks."),
    ("An account of three kinds of supply work: container programmes out of "
     "China, discharge onto unequipped shorelines in the Russian north, and "
     "food and equipment into the European Union.",
     "An account of two kinds of supply work: container programmes out of "
     "China, and discharge onto unequipped shorelines in the Russian north."),
    ('\n  "European Union import compliance",', ""),
]

# Вводный абзац /experience свёрстан с переносами строк, поэтому regex.
LEDE = (r"Food and equipment into the European Union\.\s*Three very different\s*regimes",
        "Two very different regimes")

# Раздел "Europe: the regime is the product" целиком, до следующего h2.
SECTION = (r"(?s)\n\s*<h2>Europe: the regime is the product</h2>.*?"
           r"(?=\n\s*<h2>Food, equipment and materials are not three businesses</h2>)")

# /about: перечисление того, что делала команда. После снятия третьего
# пункта список стал из двух, поэтому перед вторым возвращается союз.
ABOUT = [(", and food and equipment into the European Union under its own "
          "certification regime.", "."),
         ("out of China, delivery to unequipped shorelines in the Russian "
          "north", "out of China, and delivery to unequipped shorelines in "
          "the Russian north")]


def apply(path, pairs, rx=()):
    p = SITE / path
    s = p.read_text()
    before = s
    for old, new in pairs:
        if old not in s:
            if new and new in s:
                continue            # уже поправлено
            if not new:
                continue            # удаление уже сделано
            print("  ВНИМАНИЕ: %s, не найдено: %s" % (path, old[:52]))
            continue
        if s.count(old) != 1:
            print("  ВНИМАНИЕ: %s, встречается %d раз: %s"
                  % (path, s.count(old), old[:52]))
            continue
        s = s.replace(old, new, 1)
    for pat, new in rx:
        s = re.sub(pat, new, s)
    if s != before:
        p.write_text(s)
        return True
    return False


def main():
    changed = []

    # --- 1. раздел про поставки в ЕС на /experience
    p = SITE / "experience.html"
    s = p.read_text()
    n = len(re.findall(SECTION, s))
    if n:
        s = re.sub(SECTION, "", s)
        p.write_text(s)
        print("  /experience: раздел \"Europe: the regime is the product\" снят")

    # --- 2. заголовок, описания, вводный абзац, JSON-LD там же
    if apply("experience.html", EXPERIENCE, [LEDE]):
        changed.append("experience.html")

    # --- 3. абзац на /about
    if apply("about.html", ABOUT):
        changed.append("about.html")

    # --- 4. тизер в блоке коридоров, по всем страницам
    t = 0
    for q in sorted(SITE.rglob("*.html")):
        s = q.read_text()
        b = s
        for old, new in TEASER:
            s = s.replace(old, new)
        if s != b:
            q.write_text(s)
            t += 1
            name = str(q.relative_to(SITE))
            if name not in changed:
                changed.append(name)
    print("  тизер поправлен на страницах: %d" % t)

    # проверка: слова про поставки В ЕС не должны остаться
    left = []
    for q in sorted(SITE.rglob("*.html")):
        s = q.read_text()
        for bad in ("into the European Union", "three regimes",
                    "three supply regimes"):
            if bad in s:
                left.append("%s: %s" % (q.relative_to(SITE), bad))
    print("страниц поправлено: %d" % len(changed))
    if left:
        print("ОСТАЛОСЬ ПРОВЕРИТЬ ВРУЧНУЮ:")
        for x in left:
            print("   ", x)
    else:
        print("утверждений о поставках в ЕС на сайте не осталось")
    return 0


if __name__ == "__main__":
    sys.exit(main())
