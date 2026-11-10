# -*- coding: utf-8 -*-
"""Пункты 5 и 6 брифа от 10.11.2026: уточнить историю, не удаляя её.

5. /experience и /projects получают пометку о том, чей это опыт: работы
   выполнены участниками команды в прежних компаниях, до образования
   ISP GROUP LLC в 2026 году. Текст взят из брифа дословно.

6. /about получает абзац об опыте руководителя в закупках крупных
   государственных и публичных компаний.

Чего этот инструмент НЕ делает, и почему. Бриф требует проставить годы у
каждого проекта и год поставки у поставок из ЕС. Годов нет: ни на сайте,
ни в брифе, ни в материалах. Выдумывать даты нельзя, это прямое правило
работы, поэтому годы не ставятся и вынесены в отчёт отдельным вопросом.
Как только годы будут названы, они встают сюда списком и проставляются
одним прогоном.

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


def add_css(s):
    if CSS.strip() in s:
        return s
    return s.replace("</head>", "<style>%s</style>\n</head>" % CSS, 1)


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
    print("ГОДЫ НЕ ПРОСТАВЛЕНЫ: проверенных дат нет, нужен список от заказчика")
    return 0


if __name__ == "__main__":
    sys.exit(main())
