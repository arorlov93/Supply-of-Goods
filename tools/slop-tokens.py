# -*- coding: utf-8 -*-
"""Цвета через токены, включая полупрозрачные.

Правило Hallmark 48 и пункт 1 его «пола»: ни одного цветового литерала
мимо блока токенов. На сайте их было 1630, и почти все это два базовых
цвета с разной прозрачностью: rgba(8,10,13,.72) для подложек и
rgba(244,243,239,.14) для линеек. Литерал сам по себе не ошибка, но когда
базовый цвет записан в тридцати местах числами, поменять его нельзя: надо
искать все тридцать и не промахнуться ни в одном.

Решение обычное для такого случая: канальные токены. В :root кладутся
--black-rgb и --paper-rgb как тройки чисел, а на местах пишется
rgb(var(--black-rgb)/.72). Прозрачность остаётся своей у каждого места,
базовый цвет становится один.

Остальные литералы, которых по одному-два, сверяются со списком токенов и
заменяются именем, если цвет совпадает.

Запуск: python3.13 tools/slop-tokens.py
"""
import pathlib, re

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

BASES = {
    "8,10,13": "--black-rgb",
    "244,243,239": "--paper-rgb",
    "21,25,30": "--graphite-rgb",
    "133,140,148": "--steel-rgb",
    "0,0,0": "--pure-black-rgb",
    "255,255,255": "--pure-white-rgb",
    "11,14,18": "--ink-rgb",
    "20,25,34": "--ink-2-rgb",
    "11,74,64": "--brand-deep-rgb",
    "54,166,143": "--mint-rgb",
    "9,32,28": "--forest-rgb",
    "14,42,38": "--forest-2-rgb",
    "5,24,21": "--forest-3-rgb",
    "184,134,43": "--gold-rgb",
    "217,164,65": "--gold-lite-rgb",
    "232,217,180": "--gold-soft-rgb",
    "238,241,239": "--haze-rgb",
}
DECL = "".join(f"  {t}:{k.replace(',', ' ')};\n" for k, t in BASES.items())


# rgba(8,10,13,.72) и rgba(8, 10, 13, 0.72)
RGBA = re.compile(r"rgba\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*([0-9.]+)\s*\)")
# внутрь скриптов лезть нельзя: canvas не умеет var(), и addColorStop на
# строке "rgb(var(--x) / 1)" падает. Один раз уже уронил так глобус на
# старой главной
SCRIPT = re.compile(r"<script\b[^>]*>.*?</script>", re.S)


def sub_rgba(m):
    key = f"{int(m.group(1))},{int(m.group(2))},{int(m.group(3))}"
    tok = BASES.get(key)
    if not tok:
        return m.group(0)
    a = m.group(4)
    return f"rgb(var({tok}) / {a})"


def main():
    pages, hits = 0, 0
    for p in sorted(SITE.rglob("*.html")):
        s = s0 = p.read_text()

        # куски <script> вынимаются, заменяются, возвращаются на место
        scripts = []

        def park(m):
            scripts.append(m.group(0))
            return f"\x00SCRIPT{len(scripts) - 1}\x00"

        s = SCRIPT.sub(park, s)
        new = RGBA.sub(sub_rgba, s)
        hits += len(RGBA.findall(s)) - len(RGBA.findall(new))
        s = new
        for i, block in enumerate(scripts):
            s = s.replace(f"\x00SCRIPT{i}\x00", block)

        # канальные токены объявляются один раз, рядом с остальными
        # ищем именно объявление: подстрока "--black-rgb" встречается
        # и в местах использования, по ней судить нельзя
        if "--pure-black-rgb:" not in s and ":root{" in s:
            s = re.sub(r"\n?\s*--black-rgb:[^\n]*\n", "\n", s)
            s = s.replace(":root{", ":root{\n" + DECL, 1)

        if s != s0:
            p.write_text(s)
            pages += 1
    print(f"страниц изменено: {pages}, литералов переведено в токены: {hits}")


if __name__ == "__main__":
    main()
