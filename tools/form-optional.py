# -*- coding: utf-8 -*-
"""Какие поля формы обязательны, а какие нет.

Что видит посетитель. Восемь полей подряд. Помечено как необязательное
ровно одно, «Company», и то лишь подсказкой внутри поля. Остальные
читаются как обязательные.

Что на самом деле. Сервер требует три вещи: имя, почту и суть запроса,
причём сутью считается любое из двух полей, «Product or equipment» или
«Anything else». Всё прочее, количество, порт назначения и условия
поставки, можно не заполнять, и заявка пройдёт.

Почему это стоит денег. Человек, который ещё не знает ни количества, ни
порта, видит стену обязательных полей и уходит. А это и есть тот, ради
кого на сайте написано «опишите задачу, спецификацию составим вместе».

Правка простая и честная: над формой одна строка о том, что нужно на
самом деле, и пометка «optional» у четырёх полей. Ничего не прячем и не
переставляем: порядок полей продуман, короткая форма с дозаполнением
потом здесь хуже, потому что второго захода в B2B обычно не бывает.

Запуск: python3.13 tools/form-optional.py
Повторный запуск ничего не дублирует.
"""
import pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

OPT = '<span class="opt">optional</span>'
OPT_FR = '<span class="opt">facultatif</span>'

# поле -> нужна ли пометка
MARK = ["f-co", "f-qty", "f-port", "f-note"]

LEAD = ('<p class="formlede">Three things are enough to start: your name, an '
        'e-mail we can reply to, and what you need. Everything else helps us '
        'quote faster, and you can leave it blank.</p>')
LEAD_FR = ('<p class="formlede">Trois choses suffisent pour commencer : votre '
           'nom, un e-mail pour la r&eacute;ponse et ce dont vous avez besoin. '
           'Le reste nous aide &agrave; chiffrer plus vite et peut rester vide.</p>')


def main():
    done = 0
    for name, opt, lead in (("contact.html", OPT, LEAD),
                            ("contact-fr.html", OPT_FR, LEAD_FR)):
        p = SITE / name
        if not p.is_file():
            continue
        s = p.read_text()
        if 'class="opt"' in s:
            print(f"  {name}: уже помечено")
            continue

        for fid in MARK:
            # пометка идёт внутрь подписи, в конец: читающий экран вслух
            # произносит её вместе с названием поля, а не отдельной строкой
            s = re.sub(r'(<label for="%s">)([^<]*)(</label>)' % fid,
                       lambda m: m.group(1) + m.group(2) + " " + opt + m.group(3),
                       s, count=1)

        # подсказка «Optional» внутри поля компании теперь лишняя
        s = s.replace(' placeholder="Optional"', "")

        s = s.replace('<form id="cf" novalidate>', lead + '<form id="cf" novalidate>', 1)
        p.write_text(s)
        print(f"  {name}: помечено полей {len(MARK)}, строка над формой добавлена")
        done += 1

    print(f"страниц правлено: {done}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
