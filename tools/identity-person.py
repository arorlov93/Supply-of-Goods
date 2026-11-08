# -*- coding: utf-8 -*-
"""Называет человека, с которым имеет дело покупатель.

Находка. Из 66 страниц сайта **ни одна** не называет ни одного человека.
Проверено поиском по фамилии представителя: ноль совпадений.

Чем это стоило. На панели из ста смоделированных покупателей
(`founder/panel/results.md`, зерно 289500) отсутствие названного
человека назвали 78 из 100, это второе по частоте возражение из десяти,
а первое, «хочу позвонить референсу», мы закрыть пока не можем вообще.
В группе «проверяет, кто вы, до ответа» это 92 процента, в группе
«первый импорт» 93.

Отдельно важно, что фраза сайта «Principal, not a broker» без имени
работает против него: её разобрали 32 покупателя из ста, и ни один не
прочёл как успокоение. Логика у всех одна: если вы берёте товар в
собственность и держите контракт, значит деньги уходят вам, и тогда мне
тем более нужно знать, кого я назову в претензии. Утверждение поднимает
планку доверия и ничем её не закрывает.

Что ставим. Только проверяемое, ничего обещанного:

* представитель, как он записан в карточке SAM: Aleksandr Orlov, Member.
  Должность не переводится ни на один язык, это юридическое обозначение
  участника общества, и в карточке реестра стоит именно так;
* на странице контактов к этому добавляется, **как проверить компанию
  самостоятельно**: UEI и CAGE уже стоят в подвале, но лежат серым
  текстом без указания, что с ними делать.

Почему ссылка ведёт на поиск, а не на карточку. Проверено браузером:
sam.gov/entity/<UEI> отдаёт 404, страница поиска не читает запрос из
адреса, у карточки внутренний идентификатор, а не UEI. Прямой ссылки на
карточку не существует, поэтому номера стоят текстом, а ссылка ведёт на
вход в поиск по реестру организаций. Срок действия регистрации на
странице не пишем: он протухнет молча.

Запуск: python3.13 tools/identity-person.py
Повторный запуск ничего не дублирует.
"""
import pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

PERSON = "Aleksandr Orlov, Member"
UEI = "WA46PAMTYMQ7"
CAGE = "217F4"
SAM = "https://sam.gov/search/?index=ei"

# Два образца подвала: колонка списка на 62 страницах и абзац на
# четырёх главных.
FOOTERS = [
    ("UEI %s<br>CAGE %s</span>" % (UEI, CAGE),
     "UEI %s<br>CAGE %s<br>%s</span>" % (UEI, CAGE, PERSON)),
    ("UEI %s &middot; CAGE %s</p>" % (UEI, CAGE),
     "UEI %s &middot; CAGE %s<br>%s</p>" % (UEI, CAGE, PERSON)),
    # about.html носит реквизиты не в подвале, а своей сноской в тексте.
    # Это страница «кто мы», то есть ровно то место, где имя человека
    # нужнее всего после страницы контактов.
    ("Registered in Florida, United States. UEI %s, CAGE %s.</p>" % (UEI, CAGE),
     "Registered in Florida, United States. UEI %s, CAGE %s. "
     "Represented by %s.</p>" % (UEI, CAGE, PERSON)),
]

# Абзац «Где мы» на странице контактов. Заменяется целиком, потому что
# порядок предложений меняется: сначала кто мы и чем это проверяется,
# потом адрес и языки.
WHERE_EN_OLD = (
    "<p>ISP GROUP LLC is a United States company. The registered office is at "
    "16395 Biscayne Blvd, North Miami Beach, Florida 33160. Correspondence in "
    "English and Russian; written enquiries are answered faster than any other "
    "channel.</p>")
WHERE_EN_NEW = (
    "<p>ISP GROUP LLC is a United States company. Enquiries are handled by "
    "%s, on +1 929 830 0038.</p>"
    "<p>The company is registered as an entity in the United States federal "
    "award system under UEI %s and CAGE %s. Both are public. You can look them "
    "up yourself in the <a href=\"%s\">entity search on sam.gov</a> rather than "
    "take our word for it.</p>"
    "<p>The registered office is at 16395 Biscayne Blvd, North Miami Beach, "
    "Florida 33160. Correspondence in English and Russian; written enquiries "
    "are answered faster than any other channel.</p>")

WHERE_FR_OLD = (
    "<p>ISP GROUP LLC est une société américaine. Siège au "
    "16395 Biscayne Blvd, North Miami Beach, Floride 33160. Correspondance en "
    "français, en anglais et en russe ; une demande écrite reçoit "
    "une réponse plus vite que tout autre canal.</p>")
WHERE_FR_NEW = (
    "<p>ISP GROUP LLC est une société américaine. Vos demandes "
    "sont traitées par %s, au +1 929 830 0038.</p>"
    "<p>La société est enregistrée comme entité dans le "
    "système fédéral américain des marchés publics sous "
    "le UEI %s et le CAGE %s. Ces deux numéros sont publics. Vous pouvez "
    "les vérifier vous-même dans la "
    "<a href=\"%s\">recherche d’entités sur sam.gov</a> sans avoir "
    "à nous croire sur parole.</p>"
    "<p>Siège au 16395 Biscayne Blvd, North Miami Beach, Floride 33160. "
    "Correspondance en français, en anglais et en russe ; une demande "
    "écrite reçoit une réponse plus vite que tout autre "
    "canal.</p>")

# Французский абзац один прогон уже встал на страницу с незаполненными
# подстановками: в первой версии инструмента не было оператора
# форматирования, и на contact-fr.html оказались буквальные %s. Держим
# испорченный вариант в списке образцов, чтобы инструмент сам его
# заменил, а не оставил ждать ручной правки.
WHERE_FR_BROKEN = WHERE_FR_NEW          # шаблон без подстановки, как он и встал

WHERE = {"contact.html": ([WHERE_EN_OLD], WHERE_EN_NEW % (PERSON, UEI, CAGE, SAM)),
         "contact-fr.html": ([WHERE_FR_OLD, WHERE_FR_BROKEN],
                             WHERE_FR_NEW % (PERSON, UEI, CAGE, SAM))}


def main():
    foot = skipped = 0
    for p in sorted(SITE.rglob("*.html")):
        s = p.read_text()
        if PERSON in s:
            skipped += 1
            continue
        t = s
        for old, new in FOOTERS:
            if old in t:
                t = t.replace(old, new, 1)
                break
        if t != s:
            p.write_text(t)
            foot += 1

    where = 0
    for name, (olds, new) in WHERE.items():
        p = SITE / name
        s = p.read_text()
        if new in s:
            continue
        hit = next((o for o in olds if o in s), None)
        if hit is None:
            print("  ВНИМАНИЕ: абзац «где мы» на %s не найден, "
                  "правка не применена" % name)
            continue
        p.write_text(s.replace(hit, new, 1))
        where += 1
        print("  %s: абзац «где мы» назвал человека и способ проверки" % name)

    print("подвалов с именем представителя: %d (уже было: %d), "
          "страниц контактов: %d" % (foot, skipped, where))
    return 0


if __name__ == "__main__":
    sys.exit(main())
