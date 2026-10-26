# -*- coding: utf-8 -*-
"""Номер раздела вынести из заголовка в отдельную ячейку сетки.

И .pblock, и .steps li это сетка из трёх колонок: узкая под номер, затем
заголовок, затем текст. Номер при этом лежал внутри <h2> или <h3>, то есть
ячеек было две: заголовок попадал в колонку шириной 70px, ломался по одному
слову в строку и последним словом ложился поверх абзаца. На узких экранах
то же самое подтверждают правила .pblock .ptext{grid-column:2} и
.steps p{grid-column:2}: они нужны только если без них текст встал бы в
третью колонку. Отдельные стили .pblock .k с padding-top:10px писались для
ячейки, а не для строчного элемента внутри заголовка.

Карточки .jsteps устроены иначе, там номер внутри заголовка стоит верно,
поэтому берём только два разметочных случая.

Запуск: python3.13 tools/fix-number-cells.py
Повторный запуск ничего не меняет: исправленная разметка под шаблон не
подходит.
"""
import pathlib, re

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

PATTERNS = (
    # <div class="pblock"><h2 id="s3"><span class="k">03</span>Заголовок</h2>
    (re.compile(r'(<div class="pblock">)<h2([^>]*)>(<span class="k">[^<]*</span>)'),
     r'\1\3<h2\2>'),
    # <li><h3><span class="k">01</span>Заголовок</h3>
    (re.compile(r'(<li>)\s*<h3([^>]*)>(<span class="k">[^<]*</span>)([^<]*)</h3>'),
     r'\1\3<h3\2>\4</h3>'),
)


def main():
    total = 0
    for p in sorted(SITE.rglob("*.html")):
        s = s0 = p.read_text()
        n = 0
        for pat, rep in PATTERNS:
            s, k = pat.subn(rep, s)
            n += k
        if s != s0:
            p.write_text(s)
            total += n
            print(f"{p.relative_to(SITE)}: номеров вынесено {n}")
    print("итого:", total)


if __name__ == "__main__":
    main()
