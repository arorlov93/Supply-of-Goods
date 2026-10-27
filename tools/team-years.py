# -*- coding: utf-8 -*-
"""Двадцать лет это опыт команды, а не возраст компании.

Внешний аудит указал на расхождение: на сайте заявлены двадцать лет
работы, а ISP GROUP LLC как юридическое лицо значительно моложе.
Владелец подтвердил, что двадцать лет это опыт людей, а не срок жизни
компании. Формулировки приводятся в соответствие.

Порядок важности обратный тому, как кажется.

Первое и главное это разметка данных. Там стояло foundingDate 2006,
то есть машиночитаемое утверждение о дате основания компании. Его
читают поисковик, карточка организации и языковая модель, и опровергнуть
его одной проверкой в реестре проще всего. Поле убирается целиком:
ставить вместо него выдуманную дату нельзя, а настоящую я не знаю.

Второе это описание компании в той же разметке и в мета-тегах: опыт
переносится с компании на команду.

Третье это видимый текст на about и experience. Переписывается ровно
там, где фраза читается как возраст компании, и не трогается там, где
она и так привязана к людям, например «behind the company are».

Ссылка «Twenty years of supply work» в подвале сорока двух страниц не
меняется: это подпись к странице, которая сама теперь объясняет, чей
это опыт.

Запуск: python3.13 tools/team-years.py
Повторный запуск ничего не меняет.
"""
import pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

OLD_DESC = ("International trading and sourcing company with twenty years of supply "
            "experience.")
NEW_DESC = ("International trading and sourcing company. Its team brings twenty years "
            "of supply experience.")

FIXES = {
"about.html": [
 ('<span class="chip"><b>20</b> years of supply work</span>',
  '<span class="chip"><b>20</b> years of team experience</span>'),
 ("Behind the company are twenty years of supply work across four continents:",
  "Behind the company is a team with twenty years of supply work across four "
  "continents:"),
],
"experience.html": [
 ("Twenty years of supply work across four continents",
  "Twenty years of our team's supply work across four continents"),
 ("that is where twenty years turns into something you can actually sell.",
  "that is where the team's twenty years turns into something you can actually "
  "sell."),
 ("What twenty years actually buys",
  "What those twenty years actually buy"),
],
}


def main():
    total = 0

    # 1. foundingDate из разметки: утверждение о компании, которое я не могу
    #    подтвердить, а опровергнуть его можно за минуту
    for p in sorted(SITE.rglob("*.html")):
        s = p.read_text()
        new = re.sub(r'\n?\s*"foundingDate":\s*"\d{4}",?', "", s)
        # запятая могла остаться висеть перед закрывающей скобкой
        new = re.sub(r",(\s*\n\s*[}\]])", r"\1", new)
        if new != s:
            p.write_text(new)
            print(f"  {p.relative_to(SITE)}: убрано foundingDate")
            total += 1

    # 2. описание компании: опыт у команды, а не у юридического лица
    for p in sorted(SITE.rglob("*.html")):
        s = p.read_text()
        if OLD_DESC in s:
            n = s.count(OLD_DESC)
            p.write_text(s.replace(OLD_DESC, NEW_DESC))
            print(f"  {p.relative_to(SITE)}: описание, {n} замен")
            total += n

    # 3. видимый текст там, где фраза читается как возраст компании
    for name, pairs in FIXES.items():
        p = SITE / name
        if not p.is_file():
            continue
        s = p.read_text()
        before = s
        for old, new in pairs:
            n = s.count(old)
            if n:
                s = s.replace(old, new)
                print(f"  {name}: {n} замен, «{old[:44]}…»")
                total += n
        if s != before:
            p.write_text(s)

    print(f"всего правок: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
