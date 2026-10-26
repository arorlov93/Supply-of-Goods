# -*- coding: utf-8 -*-
"""Голос подписей: убрать моноширинные капители с разрядкой.

Правила Hallmark 67 и 64. Подпись, заголовок столбца, хлебная крошка, чип,
кнопка и ярлык поля набирались моноширинным шрифтом прописными с разрядкой
до 0.18em и кеглем от 0.57rem. Это самый частый признак страницы, собранной
моделью: такой набор не несёт смысла, он просто «выглядит технично». На
сайте таких случаев было больше тысячи на 46 страницах.

Правятся сами объявления, а не каскад поверх: накрыть их блоком в конце
страницы недостаточно, потому что в исходнике они остаются, а читает
исходник и человек, и линтер.

Регистр самого текста не трогается, поэтому FOB, CIF и EAC остаются
прописными: это аббревиатуры, а не украшение. Снимается принудительный
uppercase в CSS, разрядка и моноширинная гарнитура, а слишком мелкий кегль
поднимается до читаемого.

Запуск: python3.13 tools/slop-labels.py
"""
import pathlib, re

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
MARK = "/* голос подписей */"

# роли подписи по разбору линтера: ключ ищется в селекторе правила
LABEL_KEYS = [
    ".eyebrow", ".crumbs", ".chip", ".meta", ".upd", ".backlink", ".searchhint",
    ".cat ul", ".card .n", ".card .cap span", ".steps .k", ".jsteps .k",
    ".num span", ".step .out", ".svc-list i", ".yrs small", ".heroside .caption",
    ".scroll-cue", ".scroll-hint", ".langsw", ".facts th", ".lanes th",
    ".ptable th", ".fgrid dt", "figcaption", "label", "table.credits th",
    ".skip", ".btn", ".btn-lg", ".cta", ".foot h3", ".foot h4", ".k",
]

RULE = re.compile(r"([^{}@/]+?)\{([^{}]*)\}")
PREV = re.compile(r"<style>" + re.escape(MARK) + r".*?</style>\s*", re.S)


def is_label(sel):
    s = sel.strip()
    if s.startswith("@") or not s:
        return False
    return any(k in s for k in LABEL_KEYS)


def fix_body(body):
    out = body
    # моноширинный голос ярлыка -> основная гарнитура
    out = re.sub(r"font-family:\s*var\(--fm\)", "font-family:var(--sans)", out)
    # разрядка: у подписи её быть не должно
    out = re.sub(r";?\s*letter-spacing:\s*\.?\d*\.?\d+em", "", out)
    # принудительные прописные: регистр задаёт текст, а не оформление
    out = re.sub(r";?\s*text-transform:\s*uppercase", "", out)
    # кегль ниже 0.7rem нечитаем даже для подписи
    def bump(m):
        v = float(m.group(1))
        return f"font-size:{max(v, 0.8):.2f}rem".rstrip("0").rstrip(".") + "rem" \
            if False else f"font-size:{max(v, 0.8)}rem"
    out = re.sub(r"font-size:\s*(0?\.\d+)rem",
                 lambda m: f"font-size:{max(float(m.group(1)), 0.8)}rem", out)
    out = re.sub(r"font-size:\s*(\d+)px",
                 lambda m: f"font-size:{max(int(m.group(1)), 12)}px", out)
    out = re.sub(r";{2,}", ";", out).strip().lstrip(";")
    return out


def main():
    pages = 0
    rules = 0
    for p in sorted(SITE.rglob("*.html")):
        s = s0 = p.read_text()
        s = PREV.sub("", s)          # следы прошлой, неверной попытки

        def repl(m):
            nonlocal rules
            sel, body = m.group(1), m.group(2)
            if not is_label(sel):
                return m.group(0)
            nb = fix_body(body)
            if nb != body:
                rules += 1
            return f"{sel}{{{nb}}}"

        s = RULE.sub(repl, s)
        if s != s0:
            p.write_text(s)
            pages += 1
    print(f"страниц изменено: {pages}, правил переписано: {rules}")


if __name__ == "__main__":
    main()
