# -*- coding: utf-8 -*-
"""Пункты 5 и 6 брифа от 10.11.2026: уточнить историю, не удаляя её.

5. /experience и /projects получают пометку о том, чей это опыт: работы
   выполнены участниками команды в прежних компаниях, до образования
   ISP GROUP LLC в 2026 году. Текст взят из брифа дословно.

6. /about получает абзац об опыте руководителя в закупках крупных
   государственных и публичных компаний.

Годы названы заказчиком 10.11.2026 и проставлены ниже, в YEARS. Названы
они по регионам, а не по отдельным объектам, поэтому и ставятся по
регионам: период поставок в регион. Приписать диапазон региона к
конкретной стройке нельзя, это было бы уже не его датой. Подпись под
фотографией курорта в Артёме остаётся как есть: даты 2017-2024 там взяты
у подрядчика и так и помечены.

Год поставок из ЕС отсюда же: оборудование бассейна на Бали входит в
балийскую программу 2023-2026, мостовое оборудование в приморскую
2017-2026. Отдельной даты отгрузки из ЕС заказчик не называл, поэтому
стоит период программы, а не выдуманный месяц.

Запуск: python3.13 tools/history-provenance.py
Повторный запуск ничего не меняет.
"""
import pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

NOTE = ("Work performed by members of our team at their previous companies, "
        "before ISP Group LLC was formed in 2026.")

ABOUT = ("Our managing member has eight years of experience in large public "
         "and state-owned company procurement. We know what a tender "
         "committee checks, and we prepare the file accordingly.")

CSS = """
/* пометка о происхождении опыта */
.provenance{margin:clamp(20px,3vh,30px) 0 0;padding:14px 18px;
  border-left:2px solid var(--gold);background:rgb(var(--paper-rgb) / .04);
  font-size:.93rem;line-height:1.55;color:var(--ink-2);max-width:72ch}
"""

YEARS_CSS = """
/* годы поставок по регионам */
.pyears{margin:14px 0 0;font-size:.95rem;line-height:1.6;color:var(--ink-2);
  max-width:68ch;letter-spacing:.005em}
.pyears b{color:var(--ink);font-weight:600}
"""

# Регион -> период поставок. Названо заказчиком 10.11.2026.
YEARS = (("Primorye", "2017 to 2026"),
         ("Kamchatka", "2019 to 2026"),
         ("Sakhalin", "2022 to 2026"),
         ("Moscow", "2023 to 2025"))
BALI = "2023 to 2026"

RU_LINE = ('<p class="pyears">Supply ran into each region over a different '
           'period. ' + " ".join("<b>%s</b> %s." % (r, y) for r, y in YEARS)
           + "</p>")

# Первая редакция строки с годами: запятые внутри запятых читались тяжело.
# Правка одноразовая, нужна только для файлов, записанных до неё.
REPAIR = [('<p class="pyears">Supply ran into each region over a different '
           'period: <b>Primorye</b>, 2017 to 2026, <b>Kamchatka</b>, '
           '2019 to 2026, <b>Sakhalin</b>, 2022 to 2026, <b>Moscow</b>, '
           '2023 to 2025.</p>', RU_LINE)]

BALI_LINE = ('<p class="pyears">Supply into the villa project ran from '
             '<b>2023 to 2026</b>. The pool plant came out of the European '
             'Union inside that period.</p>')

EXP_LINE = ('<p class="pyears">The supply programmes behind this section ran '
            'into Primorye from 2017 to 2026, Kamchatka from 2019 to 2026 and '
            'Sakhalin from 2022 to 2026.</p>')

# (куда дописать, что дописать) для страницы /projects
PROJ = [
    # 01: сколько шли сами программы
    ("Three programmes: two running into Russia, one into Indonesia.",
     "Three programmes: two running into Russia between 2017 and 2026, one "
     "into Indonesia between 2023 and 2026."),
    # 01: мостовое оборудование из ЕС
    ("because the specification and the service life decided it rather than "
     "the price.</li>",
     "because the specification and the service life decided it rather than "
     "the price. Supplied into the Primorye programme, 2017 to 2026.</li>"),
    # 01: отделка и бассейн на Бали
    ("shipped into Indonesia from two continents against one fit-out "
     "programme.</li>",
     "shipped into Indonesia from two continents against one fit-out "
     "programme, 2023 to 2026.</li>"),
    # 02: годы по регионам России
    ("Different packages on one import channel.</p>",
     "Different packages on one import channel.</p>" + RU_LINE),
    # 03: годы по Бали
    ("against the developer&rsquo;s fit-out programme.</p>",
     "against the developer&rsquo;s fit-out programme.</p>" + BALI_LINE),
]

# то же для /experience
EXP = [("infrastructure stops existing.</p>",
        "infrastructure stops existing.</p>\n\n    " + EXP_LINE)]


def add_css(s):
    if CSS.strip() in s:
        return s
    return s.replace("</head>", "<style>%s</style>\n</head>" % CSS, 1)


def add_years_css(s):
    if YEARS_CSS.strip() in s:
        return s
    return s.replace("</head>", "<style>%s</style>\n</head>" % YEARS_CSS, 1)


def put_years(name, pairs):
    """Проставить годы. Повторный запуск ничего не меняет."""
    p = SITE / name
    s = p.read_text()
    before = s
    s = add_years_css(s)
    for old, new in REPAIR:
        s = s.replace(old, new)
    for old, new in pairs:
        if new in s:
            continue
        if old not in s:
            print("  ВНИМАНИЕ: %s, якорь не найден: %s" % (name, old[:46]))
            continue
        if s.count(old) != 1:
            print("  ВНИМАНИЕ: %s, якорь встречается %d раз: %s"
                  % (name, s.count(old), old[:46]))
            continue
        s = s.replace(old, new, 1)
    if s != before:
        p.write_text(s)
        return True
    return False


def main():
    done = []

    # --- 5. пометка на страницах истории
    for name in ("experience.html", "projects.html"):
        p = SITE / name
        s = p.read_text()
        if NOTE in s:
            continue
        s = add_css(s)
        # Ставим сразу после вводного абзаца страницы: это первое, что
        # читают после заголовка, и дальше весь текст читается верно.
        # Две страницы свёрстаны по-разному, поэтому якоря два.
        off = None
        for pat in (r'(?s)<div class="lede">.*?</div>', r'(?s)<p class="lead">.*?</p>'):
            m = re.search(pat, s)
            if m:
                off = m.end()
                break
        if off is None:
            print("  ВНИМАНИЕ: %s, вводный блок не найден" % name)
            continue
        s = s[:off] + '\n<p class="provenance">%s</p>' % NOTE + s[off:]
        p.write_text(s)
        done.append(name)

    # --- 6. абзац на /about
    p = SITE / "about.html"
    s = p.read_text()
    if ABOUT not in s:
        anchor = ('That account is written out in full on '
                  '<a href="experience">twenty years of supply work</a>.</p>')
        if anchor not in s:
            print("  ВНИМАНИЕ: about.html, якорь абзаца не найден")
        else:
            s = s.replace(anchor, anchor + "<p>%s</p>" % ABOUT, 1)
            p.write_text(s)
            done.append("about.html")

    print("страниц поправлено: %d (%s)" % (len(done), ", ".join(done) or "нет"))

    # --- 5, вторая часть: годы поставок по регионам
    y = []
    if put_years("projects.html", PROJ):
        y.append("projects.html")
    if put_years("experience.html", EXP):
        y.append("experience.html")
    print("годы проставлены: %s" % (", ".join(y) or "уже стояли"))
    print("  Приморье 2017-2026, Камчатка 2019-2026, Сахалин 2022-2026,")
    print("  Москва 2023-2025, Бали 2023-2026 (в т.ч. бассейн из ЕС)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
