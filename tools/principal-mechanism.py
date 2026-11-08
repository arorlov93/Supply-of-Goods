# -*- coding: utf-8 -*-
"""Ставит механизм рядом с утверждением «Principal, not a broker».

Находка панели. Эту фразу разобрали 32 покупателя из ста, и **ни один**
не прочёл её как успокоение. Логика у всех одна и она неприятно верная:
если вы берёте товар в собственность и держите контракт, значит деньги
уходят вам, а не заводу, и тогда мне тем более нужно знать, кого я
назову в претензии и чем защищён платёж. Утверждение поднимает планку
доверия и ничем её не закрывает.

В группе «обожжён трейдером», это 15 человек, **100 процентов** назвали
условием аккредитив или платёж против документов. Не скидку, не отзыв,
не фотографию склада. Механизм.

Почему именно это, а не референс. Референс просили 79 из 100, и его у
компании нет: ни одной доведённой поставки, ни одного заказчика, на
которого можно сослаться. Выдумать нельзя. Единственная честная замена
социальному доказательству это структура сделки, которую покупатель
контролирует своим банком, а не нашим словом.

Что делает скрипт. Дописывает в плитку «принципал, не брокер» на всех
четырёх главных второе предложение про аккредитив с платежом по
предъявлении против документов. Плитка остаётся одна, сетка из четырёх
не трогается: пятая плитка сломала бы раскладку, а переписывать
соседние утверждения никто не просил.

Формулировка нарочно условная, «где этого требует ваш банк». Безусловное
обещание «никакого задатка по любому заказу» компанию связывает, и в
правилах прямо сказано ничего обязывающего без прямой команды не
выпускать. Сказанное здесь компания и так исполняет: котировка
бесплатна, это уже написано в разделе вопросов на странице контактов.

Запуск: python3.13 tools/principal-mechanism.py
Повторный запуск ничего не дублирует.
"""
import pathlib, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

ADD = {
 "index.html":
   (" Where your bank requires it, we work under a letter of credit at sight "
    "against documents, so your money moves only when the papers are right."),
 "fr/index.html":
   (" Quand votre banque l’exige, nous travaillons sous crédit "
    "documentaire payable à vue contre documents : l’argent ne part "
    "que lorsque les pièces sont conformes."),
 "es/index.html":
   (" Cuando su banco lo exige, trabajamos con crédito documentario "
    "pagadero a la vista contra documentos: el dinero solo sale cuando los "
    "documentos están conformes."),
 "de/index.html":
   (" Wo Ihre Bank es verlangt, arbeiten wir mit einem Akkreditiv zahlbar bei "
    "Sicht gegen Dokumente: Das Geld fließt erst, wenn die Papiere "
    "stimmen."),
}

ANCHOR = {
 "index.html":
   "the contract, the payment and the responsibility sit with one company.",
 "fr/index.html":
   "le contrat, le paiement et la responsabilité reposent sur une seule "
   "société.",
 "es/index.html":
   "el contrato, el pago y la responsabilidad recaen en una sola empresa.",
 "de/index.html":
   "damit Vertrag, Zahlung und Verantwortung bei einem Unternehmen liegen.",
}


def main():
    done = skipped = 0
    for name, anchor in ANCHOR.items():
        p = SITE / name
        s = p.read_text()
        add = ADD[name]
        if add.strip() in s:
            skipped += 1
            continue
        if anchor not in s:
            print("  ВНИМАНИЕ: плитка на %s не найдена, правка не применена" % name)
            continue
        p.write_text(s.replace(anchor, anchor + add, 1))
        print("  %s: механизм поставлен рядом с утверждением" % name)
        done += 1
    print("главных поправлено: %d (уже было: %d)" % (done, skipped))
    return 0


if __name__ == "__main__":
    sys.exit(main())
