# -*- coding: utf-8 -*-
"""Убрать строки, склеенные точками-разделителями.

Правило Hallmark 63: строка вида «Компания · Описание · Ссылка · Ссылка»
это признак сгенерированной страницы. Точка там не разделяет смысл, она
просто заполняет место, где должна быть структура. В подвале такая строка
стояла на всех страницах сайта.

Становится: название и описание отдельными строками, ссылки отдельной
строкой с нормальным промежутком. Читается то же самое, но видно, что
части разные по назначению, а не нанизаны на точки.

Чипы с перечислением условий поставки («FOB · CFR · CIF · DAP») разбиты на
отдельные чипы, по одному на условие. Это и правило закрывает, и попадать
по ним пальцем становится возможно.

Запуск: python3.13 tools/slop-dots.py
"""
import pathlib, re

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

FOOT = re.compile(
    r'<p class="fbottom">(.*?)</p>', re.S)
# чип, внутри которого перечисление через точку
CHIP = re.compile(r'<span class="chip">([^<]*?&middot;[^<]*?)</span>')


def rebuild_foot(m):
    inner = m.group(1)
    links = re.findall(r"<a [^>]*>.*?</a>", inner, re.S)
    text = re.sub(r"<a [^>]*>.*?</a>", "", inner, flags=re.S)
    text = re.sub(r"&nbsp;|&middot;", " ", text)
    text = re.sub(r"\s+", " ", text).strip(" ·,")
    # первая точка-разделитель отделяла название от описания
    parts = [p.strip() for p in text.split("·") if p.strip()]
    if not parts:
        return m.group(0)
    name = parts[0]
    rest = " ".join(parts[1:]).strip()
    out = [f'<p class="fbottom"><span class="fname">{name}</span>']
    if rest:
        out.append(f'<span class="fdesc">{rest}</span>')
    if links:
        out.append('<span class="flinks">' + "".join(links) + "</span>")
    out.append("</p>")
    return "".join(out)


def split_chip(m):
    parts = [p.strip() for p in m.group(1).split("&middot;") if p.strip()]
    return "".join(f'<span class="chip">{p}</span>' for p in parts)


CSS_MARK = "/* подвал без точек-разделителей */"
CSS = f"""<style>{CSS_MARK}
.fbottom{{display:flex;flex-direction:column;gap:6px;align-items:flex-start}}
.fbottom .fdesc{{max-width:62ch}}
.fbottom .flinks{{display:flex;gap:22px;margin-top:4px}}
</style>
"""
PREV = re.compile(r"<style>" + re.escape(CSS_MARK) + r".*?</style>\s*", re.S)


def main():
    pages, feet, chips = 0, 0, 0
    for p in sorted(SITE.rglob("*.html")):
        s = s0 = p.read_text()

        new = FOOT.sub(rebuild_foot, s)
        if new != s:
            feet += 1
            s = new

        new = CHIP.sub(split_chip, s)
        if new != s:
            chips += 1
            s = new

        s = PREV.sub("", s)
        if "</body>" in s:
            s = s.replace("</body>", CSS + "</body>", 1)

        if s != s0:
            p.write_text(s)
            pages += 1
    print(f"страниц изменено: {pages}, подвалов перестроено: {feet}, "
          f"страниц с разбитыми чипами: {chips}")


if __name__ == "__main__":
    main()
