# -*- coding: utf-8 -*-
"""Адрес почты и реквизиты должны быть видны машине, а не только человеку.

Две находки, обе подтверждены тем, что сайт прочитан так, как его читает
языковая модель: запросом страницы и разбором текста.

Первая. На главной и трёх языковых версиях нет пометки email_off.
Cloudflare по умолчанию подменяет любой почтовый адрес на [email
protected] и прячет настоящий за скриптом. Это задумано против
сборщиков спама, но стоит дороже, чем даёт: адреса не видит посетитель
без скриптов, не видит поисковик и не видит языковая модель. Проверено:
на вопрос «как связаться с ISP Group» по тексту главной почта не
читается вовсе. На остальных сорока двух страницах пометка стоит, на
четырёх главных её забыли.

Вторая. UEI и CAGE на главной есть, но только внутри разметки данных.
Разметку читает поисковик, а вот обычное чтение страницы, которым
пользуются ассистенты, теги script выбрасывает. То есть единственные
проверяемые реквизиты компании для языковой модели не существуют.
Выносим их в подвал обычным текстом: заодно покупатель может проверить
компанию в SAM.gov, не спрашивая нас.

Запуск: python3.13 tools/entity-visible.py
Повторный запуск ничего не дублирует.
"""
import pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

UEI = "WA46PAMTYMQ7"
CAGE = "217F4"

# Подвал общего образца: колонка Entity
FOOT_OLD = ('<dt>Entity</dt><dd>ISP GROUP LLC<br>'
            '<span style="color:var(--ink-2)">United States</span></dd>')
FOOT_NEW = ('<dt>Entity</dt><dd>ISP GROUP LLC<br>'
            '<span style="color:var(--ink-2)">United States<br>'
            'UEI %s<br>CAGE %s</span></dd>' % (UEI, CAGE))

# Французский образец подвала. Он стоит на afrique-ouest,
# decoupes-volaille и certificat-veterinaire, то есть ровно на трёх
# страницах, которые по Search Console берут больше всего кликов:
# afrique-ouest на позиции 1,0, decoupes-volaille с CTR 9,1 процента.
# Реквизитов там не было, потому что прежний образец искал только
# английское Entity.
FOOT_FR_OLD = ('<dt>Soci&eacute;t&eacute;</dt><dd>ISP GROUP LLC<br>'
               '<span style="color:var(--ink-2)">&Eacute;tats-Unis</span></dd>')
FOOT_FR_NEW = ('<dt>Soci&eacute;t&eacute;</dt><dd>ISP GROUP LLC<br>'
               '<span style="color:var(--ink-2)">&Eacute;tats-Unis<br>'
               'UEI %s<br>CAGE %s</span></dd>' % (UEI, CAGE))

# Подвал главной собран отдельно и выглядит иначе. Языковые главные
# отличаются от английской только словом «Соединённые Штаты», поэтому
# прежний образец их не находил, и на них UEI оставался только внутри
# тега script, то есть для читателя и для языковой модели его не было.
HOME_TPL = ('<p class="muted" style="margin:0;font-size:14px;line-height:1.7">'
            '16395 Biscayne Blvd<br>North Miami Beach, FL 33160<br>%s')
COUNTRY = ["United States", "&Eacute;tats-Unis", "États-Unis",
           "Estados Unidos", "Vereinigte Staaten"]
HOMES = [(HOME_TPL % c + "</p>",
          HOME_TPL % c + "<br>UEI %s &middot; CAGE %s</p>" % (UEI, CAGE))
         for c in COUNTRY]


def main():
    off = 0
    for p in sorted(SITE.rglob("*.html")):
        if p.name == "crm.html":
            continue            # внутренняя страница, почты на ней нет
        s = p.read_text()
        if "email_off" in s or "<body>" not in s:
            continue
        s = s.replace("<body>", "<body>\n<!--email_off-->", 1)
        s = s.replace("</body>", "<!--/email_off-->\n</body>", 1)
        p.write_text(s)
        print(f"  {p.relative_to(SITE)}: почта открыта для чтения")
        off += 1

    ent = 0
    for p in sorted(SITE.rglob("*.html")):
        s = p.read_text()
        # Проверяем видимый текст, а не весь файл: UEI внутри тега
        # script есть почти везде, и прежняя проверка принимала его за
        # выполненную работу.
        if ("UEI %s" % UEI) in re.sub(r"(?s)<script.*?</script>", "", s):
            continue
        t = s
        if FOOT_OLD in t:
            t = t.replace(FOOT_OLD, FOOT_NEW, 1)
        elif FOOT_FR_OLD in t:
            t = t.replace(FOOT_FR_OLD, FOOT_FR_NEW, 1)
        else:
            for old, new in HOMES:
                if old in t:
                    t = t.replace(old, new, 1)
                    break
        if t != s:
            p.write_text(t)
            ent += 1

    print(f"страниц с открытой почтой: {off}, с видимыми реквизитами: {ent}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
