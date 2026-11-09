# -*- coding: utf-8 -*-
"""Снять с сайта утверждение, что эти маршруты уже отработаны.

Зачем. Сайт в одном месте честно говорит, что ни одной доведённой поставки
нет, и это единственное, за что его хвалили: ни один из 250 покупателей не
поставил эту честность в вину, несколько назвали её причиной доверять. В
другом месте тот же сайт пишет «lanes we already run», «4 active
corridors», «The four we run now». Покупатель, который увидит оба
утверждения, сделает худший вывод из возможных, и это ровно тот механизм,
который рамка Product называет так: половина решения не разбавляет хорошую
позицию, а дискредитирует её.

Что меняется. Везде, где стоит утверждение о прошлом («уже возим», «уже
отработано», «уже существует»), ставится утверждение о настоящем («котируем»,
«готовы котировать»). Числа, факты и структура не трогаются: меняется только
время глагола и то, что из него следует.

Что НЕ меняется, и это осознанно:

* «A document set that has already cleared at that destination» в разделе
  «What a working corridor contains». Это определение того, из чего состоит
  рабочий коридор, а не утверждение, что наш такой. Там же «a settlement
  route the banks on both ends already accept».
* «we will publish other corridors as we run them» на landed-price-index:
  будущее время, утверждения о прошлом в нём нет.
* «the lane everybody already uses» в пакете страниц про стоимость фрахта:
  это про чужие маршруты.

Словарь переводов правится тоже, иначе сборка вернёт прежнюю строчку.

Запуск: python3.13 tools/drop-already-run.py
Повторный запуск ничего не меняет.
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
I18N = ROOT / "tools" / "i18n.json"

# (что ищем, на что меняем). Применяется ко всем страницам, сколько бы раз
# ни встретилось: одна и та же фраза стоит и в видимом тексте, и в
# разметке JSON-LD, и обе должны говорить одно и то же.
SWAPS = [
 # --- главные, подпись над рядом категорий
 ("These are the lanes we already run, food among them.",
  "These are the categories we quote, food among them."),
 ("Voici les flux que nous opérons déjà, l’alimentaire compris.",
  "Voici les catégories que nous cotons, l’alimentaire compris."),
 ("Estas son las rutas que ya operamos, la alimentación entre ellas.",
  "Estas son las categorías que cotizamos, la alimentación entre ellas."),
 ("Das sind die Verkehre, die wir bereits fahren, Lebensmittel "
  "eingeschlossen.",
  "Das sind die Kategorien, die wir anbieten, Lebensmittel eingeschlossen."),

 # --- страницы коридоров, хвост «почему маршрут, а не товар».
 # Строка в исходнике перенесена после «These are», поэтому ищем хвост.
 ("the routes we already run.", "the routes we quote."),

 # --- ссылки на страницу коридоров
 ("Four routes we already run end to end.",
  "Four routes we quote end to end."),
 ("The four routes we run end to end.", "The four routes we quote end to end."),
 ("Four routes we run end to end.", "Four routes we quote end to end."),

 # --- сама страница коридоров
 ("Four routes we run end to end, with the producers, forwarder, customs "
  "broker and document set already in place on each one.",
  "Four routes we quote end to end: what the chain on each one has to "
  "contain before a price means anything."),
 ("Trade corridors we run | China, Türkiye, West Africa, SADC",
  "Trade corridors we quote | China, Türkiye, West Africa, SADC"),
 ("We run lanes, not a catalogue", "We quote lanes, not a catalogue"),
 ("We run lanes, <em>not a catalogue</em>",
  "We quote lanes, <em>not a catalogue</em>"),
 ("4 active corridors", "4 corridors"),
 ("The four we run now", "The four we quote now"),
 ("We open new lanes, and most of the four below started as one. What we "
  "will tell you",
  "We open new lanes. What we will tell you"),

 # --- срок до прайса: число остаётся, оговорка перестаёт быть про прошлое
 ("A landed price in about ten working days on a lane we already run. On a "
  "new lane it is longer, and we say how much longer at the start.",
  "A landed price in about ten working days. Where the destination has a "
  "certification regime we have not worked under before it is longer, and "
  "we say how much longer at the start."),
 ("Un prix rendu sous une dizaine de jours ouvrés sur une ligne que nous "
  "exploitons déjà.",
  "Un prix rendu sous une dizaine de jours ouvrés. Quand la destination a "
  "un régime de certification que nous n’avons pas encore pratiqué, c’est "
  "plus long, et nous le disons au départ."),
 ("About ten working days to a landed price on a lane we already run, from "
  "the moment the specification is agreed. On a new lane it is longer "
  "because the producer shortlist has to be built, and we say how much "
  "longer before we start.",
  "About ten working days to a landed price, from the moment the "
  "specification is agreed. Where the producer shortlist has to be built "
  "from scratch it is longer, and we say how much longer before we start."),
 ("a landed price in about ten working days on a lane we already run. The "
  "time goes into producer verification and freight, not into the "
  "arithmetic.",
  "a landed price in about ten working days. The time goes into producer "
  "verification and freight, not into the arithmetic."),

 # --- то же утверждение другими словами
 ("No. The six are where producer relationships and a documented lane "
  "already exist, so a quotation comes back in days rather than weeks.",
  "No. The six are the categories we are set up to quote, so a quotation "
  "comes back in days rather than weeks."),
 ("The categories below are simply where we have already done that.",
  "The categories below are simply where we are set up to do that."),
 ("Six categories where producer relationships and a documented lane "
  "already exist.",
  "Six categories, with a page for each."),
 ("These are lanes where producers are already verified and a document set "
  "has cleared before, so a comparison comes back in days rather than "
  "weeks:",
  "These are the origins we can price now, so a comparison comes back in "
  "days rather than weeks:"),
 ("A worked example from a lane we run: quartz surface products",
  "A worked example: quartz surface products"),
]


def main():
    pages, hits = 0, 0
    files = sorted(SITE.glob("*.html")) + sorted(SITE.glob("*/*.html"))
    for p in files:
        s = p.read_text()
        orig = s
        n = 0
        for old, new in SWAPS:
            if old in s:
                n += s.count(old)
                s = s.replace(old, new)
        if s != orig:
            p.write_text(s)
            pages += 1
            hits += n
            print("  %s: %d" % (p.relative_to(SITE), n))

    raw = I18N.read_text()
    moved = 0
    for old, new in SWAPS:
        if old in raw:
            moved += raw.count(old)
            raw = raw.replace(old, new)
    if moved:
        json.loads(raw)          # не выпускаем сломанный словарь
        I18N.write_text(raw)
        print("  i18n.json: строк заменено %d" % moved)

    print("страниц поправлено: %d, замен: %d" % (pages, hits))
    return 0


if __name__ == "__main__":
    sys.exit(main())
