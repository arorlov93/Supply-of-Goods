# -*- coding: utf-8 -*-
"""Три числа наверх страницы контактов, и честный ответ про окно поставки.

Зачем. Рамка Product и рамка Offers обе говорят одно: продукт кончается
раньше, чем покупатель может что-то сделать. Ни минимума кроме «полный
контейнер», ни срока, ни названного следующего шага. На панели это бьёт в
две группы: у «только цены» отсутствие срока назвал 91 процент, а полный
контейнер как минимум назвали 25 процентов в целом и 36 процентов
снабженцев. Восемь человек отказали **только** из-за минимума, причём двое
похвалили всё остальное.

Два числа из трёх на странице уже стоят, в чипах первого экрана: один
рабочий день на ответ, десять рабочих дней до прайса рендер. Не стояло
третье, настоящий минимум, хотя в раскрывашке внизу он есть. Поднимаем его
в чипы, вместе с оговоркой про сборный контейнер, потому что именно
оговорка и снимает возражение.

Четвёртое число, окно поставки, **не ставим, и это осознанно.** Проверенного
значения нет: компания не довела ни одной поставки, а время транзита,
переписанное с сайта линии, это не обязательство. Вместо числа на странице
стоит то, что в цене действительно есть и что проверяется: окно погрузки,
подтверждённое производителем письменно, названный рейс со своим транзитом
и дата, к которой комплект документов должен быть собран. Правило
CLAUDE.md тут работает буквально: нет проверенного значения, значит поле
остаётся пустым.

Французская страница получает то же самое, плюс две починки: в ответе про
минимум не было оговорки о сборном контейнере, которая есть в английском,
и в блоке французских страниц не было трёх новых страниц допустимости.

Запуск: python3.13 tools/contact-numbers.py
Повторный запуск ничего не меняет.
"""
import json, pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
MERCURY = SITE / "css" / "mercury.css"

# Починка, без которой правка не доезжает до телефона. Страничная вёрстка
# на экранах до 900 пикселей ставит колонку со снимком первой
# (.chero .heroside{order:-1}). На страницах стран в этой колонке только
# снимок, и это верно. На страницах контактов в ней же лежит форма заявки,
# поэтому телефон открывал страницу на пустой форме, а заголовок, подзаголовок
# и те самые три числа уезжали примерно на 1500 пикселей вниз. Замерено на
# 390: форма на 426, заголовок на 1527. Дефект не новый, он есть и в
# выложенной версии, но именно он съедал бы весь смысл этой правки.
CSS_FIX = """
/* Колонка с формой заявки не выносится наверх. Подробности в
   tools/contact-numbers.py. */
@media (max-width: 900px) {
  .chero .heroside:has(.cform) { order: 0 !important; }
}
"""

CHIP = {
 "contact.html": (
   '<span class="chip"><b>10</b> working days to a landed price</span>',
   '<span class="chip"><b>1</b> container minimum, consolidated if needed'
   '</span>'),
 "contact-fr.html": (
   '<span class="chip"><b>10</b> jours ouvrés jusqu’au prix rendu</span>',
   '<span class="chip"><b>1</b> conteneur minimum, groupé si besoin</span>'),
}

# Три числа и пять инкотермов в одном потоке переносов читались как семь
# равных чипов в три ряда. Разводим на две строки: числа отдельно, базисы
# отдельно.
SPLIT = ('<span class="chip">FOB</span>',
         '</div><div class="chips" style="margin-top:10px">'
         '<span class="chip">FOB</span>')

WINDOW = {
 "contact.html": (
   '<p class="pnote">We do not ask for a fee to quote',
   "<p>On the delivery window we will not print a number we have not run. "
   "We have no completed shipment behind us, and a transit time copied off "
   "a carrier’s web page is not a commitment. What the quotation carries "
   "instead is dated and specific: the loading window the producer confirms "
   "in writing, the named sailing with its transit, and the date by which "
   "the document set has to be complete. If one of the three moves, you "
   "hear it on the day it moves, not at the end.</p>"),
 "contact-fr.html": (
   '<p class="pnote">Pas de frais de cotation',
   "<p>Sur le délai de livraison, nous n’afficherons pas un chiffre que "
   "nous n’avons pas tenu. Nous n’avons pas encore d’expédition menée à son "
   "terme derrière nous, et un temps de transit recopié sur le site d’un "
   "armateur n’est pas un engagement. Ce que porte la cotation est daté et "
   "précis : la fenêtre de chargement confirmée par écrit par le "
   "producteur, le navire nommé avec son temps de transit, et la date à "
   "laquelle le jeu de documents doit être complet. Si l’un des trois "
   "bouge, vous l’apprenez le jour où il bouge, pas à la fin.</p>"),
}

FAQ_COUNT = {
 "contact.html": ("Four things people check before sending a first enquiry.",
                  "Five things people check before sending a first enquiry."),
 "contact-fr.html": ("Trois points vérifiés avant un premier contact.",
                     "Quatre points vérifiés avant un premier contact."),
}

# Якорь это хвост последней раскрывашки. Блок обязан начинаться с
# закрывающего </details>, иначе новый вопрос встаёт ВНУТРЬ предыдущего:
# замена съедает его закрывающий тег. Один раз так и вышло, починка ниже.
FAQ_NEW = {
 "contact.html": (
   "</details></div></div></section>",
   "</details><details><summary>When would it actually arrive?</summary><p>Honestly: "
   "we quote a window, we do not promise a date, and we have no completed "
   "shipment behind us to point at. The quotation names the loading window "
   "the producer has confirmed, the sailing and its transit, and the date "
   "the document set has to be complete. Those three are what a delivery "
   "date is made of, and you get them in writing before you commit rather "
   "than afterwards.</p></details></div></div></section>"),
 "contact-fr.html": (
   "</details></div></div></section>",
   "</details><details><summary>Quand la marchandise arrive-t-elle vraiment ?</summary>"
   "<p>Honnêtement : nous donnons une fenêtre, pas une date, et nous n’avons "
   "pas d’expédition menée à son terme à vous montrer. La cotation nomme la "
   "fenêtre de chargement confirmée par le producteur, le navire et son "
   "temps de transit, et la date à laquelle le jeu de documents doit être "
   "complet. C’est de ces trois éléments qu’une date de livraison est "
   "faite, et vous les avez par écrit avant de vous engager, pas après."
   "</p></details></div></div></section>"),
}

# Французский ответ про минимум был короче английского: в нём не было
# оговорки про сборный контейнер, а именно она и снимает возражение.
# Каждая тройка это (признак «уже сделано», что ищем, на что меняем).
# Признак отдельным полем нужен потому, что текст ответа про минимум стоит
# на странице дважды, в разметке и в JSON-LD, и одной проверкой «новое уже
# есть» вторую правку не отличить от первой.
FR_FIXES = [
 ("fournisseurs dans un même conteneur.</p>",
  "<p>Nous travaillons en conteneurs complets. Pour une première commande, "
  "un ou deux conteneurs à conditions commerciales complètes avant le "
  "démarrage d’un programme mensuel.</p>",
  "<p>Nous travaillons en conteneurs complets, parce que c’est là que "
  "l’économie du transport tient. Pour une première commande, un ou deux "
  "conteneurs à conditions commerciales complètes avant le démarrage d’un "
  "programme mensuel. Pour un essai, nous pouvons grouper plusieurs "
  "fournisseurs dans un même conteneur.</p>"),
 ('fournisseurs dans un même conteneur."',
  "Nous travaillons en conteneurs complets. Pour une première commande, un "
  "ou deux conteneurs à conditions commerciales complètes avant le "
  "démarrage d’un programme mensuel.",
  "Nous travaillons en conteneurs complets, parce que c’est là que "
  "l’économie du transport tient. Pour une première commande, un ou deux "
  "conteneurs à conditions commerciales complètes avant le démarrage d’un "
  "programme mensuel. Pour un essai, nous pouvons grouper plusieurs "
  "fournisseurs dans un même conteneur."),
 ('<a class="lanelink" href="admissibilite-cote-divoire">',
  '<a class="lanelink" href="decoupes-volaille">',
  '<a class="lanelink" href="admissibilite-cote-divoire"><b>Côte d’Ivoire'
  '</b><span>Le dossier documentaire à l’import.</span></a>'
  '<a class="lanelink" href="admissibilite-senegal"><b>Sénégal</b>'
  '<span>Le dossier documentaire à l’import.</span></a>'
  '<a class="lanelink" href="admissibilite-cameroun"><b>Cameroun</b>'
  '<span>Le dossier documentaire à l’import.</span></a>'
  '<a class="lanelink" href="decoupes-volaille">'),
]


# Починка первого прогона: вопрос встал внутрь предыдущей раскрывашки.
REPAIR = {
 "contact.html":
   ("</p><details><summary>When would it actually arrive?",
    "</p></details><details><summary>When would it actually arrive?"),
 "contact-fr.html":
   ("</p><details><summary>Quand la marchandise arrive-t-elle vraiment ?",
    "</p></details><details><summary>Quand la marchandise arrive-t-elle "
    "vraiment ?"),
}

# Разметка FAQPage для поиска собирается полной сборкой, запускать которую
# нельзя, поэтому новый вопрос дописывается в неё здесь же.
LD = {
 "contact.html": (
   '"text": "English and Russian in correspondence.',
   '{"@type": "Question", "name": "When would it actually arrive?", '
   '"acceptedAnswer": {"@type": "Answer", "text": "Honestly: we quote a '
   'window, we do not promise a date, and we have no completed shipment '
   'behind us to point at. The quotation names the loading window the '
   'producer has confirmed, the sailing and its transit, and the date the '
   'document set has to be complete. Those three are what a delivery date '
   'is made of, and you get them in writing before you commit rather than '
   'afterwards."}}'),
 "contact-fr.html": (
   '"text": "Un accusé de réception avec les questions ouvertes',
   '{"@type": "Question", "name": "Quand la marchandise arrive-t-elle '
   'vraiment ?", "acceptedAnswer": {"@type": "Answer", "text": '
   '"Honnêtement : nous donnons une fenêtre, pas une date, et nous n’avons '
   'pas d’expédition menée à son terme à vous montrer. La cotation nomme la '
   'fenêtre de chargement confirmée par le producteur, le navire et son '
   'temps de transit, et la date à laquelle le jeu de documents doit être '
   'complet. C’est de ces trois éléments qu’une date de livraison est '
   'faite, et vous les avez par écrit avant de vous engager, pas après."}}'),
}


def ld_add(name, s):
    """Добавляет вопрос в конец mainEntity, если разметка на странице есть."""
    if name not in LD or LD[name][1] in s:
        return s, False
    m = re.search(r'(?s)("@type": "FAQPage", "mainEntity": \[.*?)\]\}', s)
    if not m or LD[name][0] not in m.group(1):
        return s, False
    out = s[:m.end(1)] + ", " + LD[name][1] + "]}" + s[m.end():]
    json.loads(re.search(r'(?s)\{"@context".*?\]\}', out).group(0))
    return out, True


def main():
    pages = 0
    for name in ("contact.html", "contact-fr.html"):
        p = SITE / name
        s = p.read_text()
        orig = s
        steps = []

        anchor, chip = CHIP[name]
        if chip not in s:
            if anchor not in s:
                print("  ВНИМАНИЕ: %s, чип прайса не найден" % name)
            else:
                s = s.replace(anchor, anchor + chip, 1)
                steps.append("минимум в чипы")

        if SPLIT[1] not in s:
            if SPLIT[0] not in s:
                print("  ВНИМАНИЕ: %s, чип FOB не найден" % name)
            else:
                s = s.replace(SPLIT[0], SPLIT[1], 1)
                steps.append("чипы в две строки")

        anchor, para = WINDOW[name]
        if para not in s:
            if anchor not in s:
                print("  ВНИМАНИЕ: %s, якорь абзаца не найден" % name)
            else:
                s = s.replace(anchor, para + anchor, 1)
                steps.append("окно поставки")

        old, new = FAQ_COUNT[name]
        if new not in s:
            if old not in s:
                print("  ВНИМАНИЕ: %s, счёт вопросов не найден" % name)
            else:
                s = s.replace(old, new, 1)
                steps.append("счёт вопросов")

        anchor, block = FAQ_NEW[name]
        if "</summary>" in block.split("<p>")[0] and block not in s:
            head = block.split("<summary>")[1].split("</summary>")[0]
            if head in s:
                pass                      # вопрос уже стоит
            elif anchor not in s:
                print("  ВНИМАНИЕ: %s, хвост раскрывашек не найден" % name)
            else:
                s = s.replace(anchor, block, 1)
                steps.append("вопрос про прибытие")

        old, new = REPAIR[name]
        if old in s:
            s = s.replace(old, new, 1)
            steps.append("вопрос вынут из соседней раскрывашки")

        s, ok = ld_add(name, s)
        if ok:
            steps.append("разметка FAQPage")

        if name == "contact-fr.html":
            for done, old, new in FR_FIXES:
                if done in s:
                    continue
                if old not in s:
                    print("  ВНИМАНИЕ: contact-fr.html, не найдено: %s"
                          % old[:40])
                    continue
                s = s.replace(old, new, 1)
                steps.append("французская починка")

        if s != orig:
            p.write_text(s)
            pages += 1
            print("  %s: %s" % (name, ", ".join(steps)))

    m = MERCURY.read_text()
    if CSS_FIX.strip() not in m:
        MERCURY.write_text(m.rstrip("\n") + "\n" + CSS_FIX)
        print("  mercury.css: порядок колонок на телефоне "
              "(нужен css-version.py)")

    print("страниц контактов поправлено: %d" % pages)
    return 0


if __name__ == "__main__":
    sys.exit(main())
