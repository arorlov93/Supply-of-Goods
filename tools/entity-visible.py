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

# Подвал главной собран отдельно и выглядит иначе
HOME_OLD = ('<p class="muted" style="margin:0;font-size:14px;line-height:1.7">'
            '16395 Biscayne Blvd<br>North Miami Beach, FL 33160<br>United States</p>')
HOME_NEW = ('<p class="muted" style="margin:0;font-size:14px;line-height:1.7">'
            '16395 Biscayne Blvd<br>North Miami Beach, FL 33160<br>United States<br>'
            'UEI %s &middot; CAGE %s</p>' % (UEI, CAGE))


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
        if UEI in s and ("UEI %s" % UEI) in s:
            continue
        t = s
        if FOOT_OLD in t:
            t = t.replace(FOOT_OLD, FOOT_NEW, 1)
        elif HOME_OLD in t:
            t = t.replace(HOME_OLD, HOME_NEW, 1)
        if t != s:
            p.write_text(t)
            ent += 1

    print(f"страниц с открытой почтой: {off}, с видимыми реквизитами: {ent}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
