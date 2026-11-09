# -*- coding: utf-8 -*-
"""Механизм платежа из придаточного предложения в самостоятельный блок.

Что было. Аккредитив стоял одним предложением внутри плитки «Principal, not
a broker», то есть внутри утверждения, которое на панели из ста провалилось
у всех 32 читателей. Рамка Offers назвала аккредитив сильнейшим активом
сайта и отдельным пунктом претензии то, что он **закопан** там.

Что ставим. Второй экран всех четырёх главных: блок «деньги идут против
документов», четыре шага, из которых третий и четвёртый это ровно то
возражение, которое панель назвала после правок 8 ноября.

Аккредитив обсуждают 76 процентов панели и 100 процентов из 38 обожжённых
трейдером. Но 26 процентов обожжённых говорят одно: **аккредитив платит
против документов, а не против товара.** Комплект может быть чистым, а
контейнер не тем. Шаг 04 отвечает на это предотгрузочной инспекцией
названной третьей стороны внутри комплекта по аккредитиву, и это стоит
ноль: программа Камеруна её и так требует от тех же трёх органов.

Про Кот-д'Ивуар на главной не сказано ничего. На странице страны источники
расходились и номер декрета мы не ставили; то же правило держим здесь.

Вёрстка. Секция намеренно НЕ объявляется сценой: скрипт прокрутки
перечисляет сцены при загрузке, и новая сцена не обслуживается. С
data-reveal всё работает, его наблюдатель универсальный.

Запуск: python3.13 tools/payment-block.py
Повторный запуск ничего не меняет. CSS темы после правки надо перехешировать:
python3.13 tools/css-version.py
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
MERCURY = SITE / "css" / "mercury.css"

MARK = "<!-- ============ ПЛАТЁЖ ============ -->"

CSS = """
/* 06b payment */
#s-pay{background:var(--paper);color:var(--black);padding:clamp(90px,14vh,170px) var(--gut)}
#s-pay .pay-wrap{max-width:var(--maxw);margin:0 auto}
#s-pay .lead{max-width:60ch;margin:18px 0 0}
"""

CSS_ANCHOR = "/* 07 why */"

H2 = {
 "index.html":    ["THE MONEY MOVES", "AGAINST DOCUMENTS."],
 "fr/index.html": ["L’ARGENT PART", "CONTRE DOCUMENTS."],
 "es/index.html": ["EL DINERO SALE", "CONTRA DOCUMENTOS."],
 "de/index.html": ["DAS GELD GEHT", "GEGEN DOKUMENTE."],
}

LEAD = {
 "index.html":
   "You have no history with us, and we will not manufacture a reference in "
   "order to pretend otherwise. A payment structure your own bank controls "
   "is the only guarantee a seller without that history can honestly offer, "
   "so we put it first rather than in a footnote.",
 "fr/index.html":
   "Vous n’avez pas d’historique avec nous, et nous ne fabriquerons pas une "
   "référence pour faire croire le contraire. Une structure de paiement que "
   "votre propre banque contrôle est la seule garantie qu’un vendeur sans "
   "historique chez vous puisse honnêtement offrir : nous la mettons en "
   "premier, pas en note de bas de page.",
 "es/index.html":
   "No tiene historial con nosotros y no vamos a fabricar una referencia "
   "para aparentar lo contrario. Una estructura de pago que controla su "
   "propio banco es la única garantía que puede ofrecer honestamente un "
   "vendedor sin ese historial, y por eso la ponemos delante y no en una "
   "nota al pie.",
 "de/index.html":
   "Sie haben keine Vorgeschichte mit uns, und wir werden keine Referenz "
   "erfinden, um das Gegenteil zu behaupten. Eine Zahlungsstruktur, die "
   "Ihre eigene Bank kontrolliert, ist die einzige Garantie, die ein "
   "Verkäufer ohne diese Vorgeschichte ehrlich anbieten kann. Darum steht "
   "sie vorn und nicht in einer Fußnote.",
}

STEPS = {
 "index.html": [
  ("Before anything is due",
   "We do not charge to quote and we take no deposit to study a file. "
   "Nothing is payable while the specification, the pack, the Incoterm and "
   "the document set are being agreed in writing."),
  ("The instrument",
   "Where your bank requires it, the transaction runs under a documentary "
   "credit payable at sight against presentation of documents, or under a "
   "documentary collection. Your bank releases the money, not us."),
  ("What releases it",
   "Payment is made against the document set named in the credit: bill of "
   "lading, invoice, packing list, certificate of origin and the "
   "certificates your port of entry requires. A document missing or "
   "non-conforming means the money stays where it is."),
  ("Against the goods, not only the paper",
   "A credit pays against documents, so the document set includes a "
   "pre-shipment inspection certificate from a named third party: SGS, "
   "Intertek or TÜV Rheinland. Cameroon’s own programme already requires "
   "it from exactly those bodies. We make it a condition of payment, so a "
   "clean file and the wrong container cannot be the same thing."),
 ],
 "fr/index.html": [
  ("Avant que quoi que ce soit soit dû",
   "La cotation n’est pas facturée et nous ne demandons pas d’acompte pour "
   "étudier un dossier. Rien n’est dû pendant que la spécification, "
   "l’emballage, l’Incoterm et le jeu de documents sont arrêtés par écrit."),
  ("L’instrument",
   "Quand votre banque l’exige, la transaction se fait sous crédit "
   "documentaire payable à vue contre présentation des documents, ou en "
   "remise documentaire. C’est votre banque qui libère l’argent, pas nous."),
  ("Ce qui libère l’argent",
   "Le paiement intervient contre le jeu de documents nommé dans le "
   "crédit : connaissement, facture, liste de colisage, certificat "
   "d’origine et les certificats qu’exige votre port d’entrée. Une pièce "
   "manquante ou non conforme, et l’argent reste où il est."),
  ("Contre la marchandise, pas seulement contre le papier",
   "Un crédit paie contre documents : le jeu de documents comprend donc un "
   "certificat d’inspection avant expédition délivré par un tiers nommé, "
   "SGS, Intertek ou TÜV Rheinland. Le programme camerounais l’exige déjà "
   "de ces trois organismes. Nous en faisons une condition de paiement, "
   "pour qu’un dossier propre et le mauvais conteneur ne puissent pas être "
   "la même chose."),
 ],
 "es/index.html": [
  ("Antes de que haya nada que pagar",
   "No cobramos por cotizar ni pedimos anticipo para estudiar un "
   "expediente. Nada es pagadero mientras se acuerdan por escrito la "
   "especificación, el embalaje, el Incoterm y el juego de documentos."),
  ("El instrumento",
   "Cuando su banco lo exige, la operación va bajo crédito documentario "
   "pagadero a la vista contra presentación de documentos, o en cobranza "
   "documentaria. Es su banco el que libera el dinero, no nosotros."),
  ("Qué libera el dinero",
   "El pago se hace contra el juego de documentos nombrado en el crédito: "
   "conocimiento de embarque, factura, lista de empaque, certificado de "
   "origen y los certificados que exige su puerto de entrada. Un documento "
   "que falte o no sea conforme, y el dinero se queda donde está."),
  ("Contra la mercancía, no sólo contra el papel",
   "Un crédito paga contra documentos, así que el juego incluye un "
   "certificado de inspección previa al embarque de un tercero nombrado: "
   "SGS, Intertek o TÜV Rheinland. El programa de Camerún ya lo exige de "
   "esos mismos tres organismos. Lo convertimos en condición de pago, para "
   "que un expediente limpio y el contenedor equivocado no puedan ser la "
   "misma cosa."),
 ],
 "de/index.html": [
  ("Bevor überhaupt etwas fällig ist",
   "Wir berechnen das Angebot nicht und verlangen keine Anzahlung, um "
   "einen Fall zu prüfen. Solange Spezifikation, Verpackung, Incoterm und "
   "Dokumentensatz schriftlich festgelegt werden, ist nichts fällig."),
  ("Das Instrument",
   "Wo Ihre Bank es verlangt, läuft das Geschäft über ein Dokumenten"
   "akkreditiv, zahlbar bei Sicht gegen Vorlage der Dokumente, oder über "
   "ein Dokumenteninkasso. Das Geld gibt Ihre Bank frei, nicht wir."),
  ("Was das Geld freigibt",
   "Gezahlt wird gegen den im Akkreditiv genannten Dokumentensatz: "
   "Konnossement, Rechnung, Packliste, Ursprungszeugnis und die "
   "Zertifikate, die Ihr Einfuhrhafen verlangt. Fehlt ein Dokument oder "
   "ist es nicht konform, bleibt das Geld, wo es ist."),
  ("Gegen die Ware, nicht nur gegen das Papier",
   "Ein Akkreditiv zahlt gegen Dokumente, deshalb gehört ein "
   "Vorversandinspektionszertifikat einer benannten dritten Stelle dazu: "
   "SGS, Intertek oder TÜV Rheinland. Das kamerunische Programm verlangt "
   "es bereits von genau diesen Stellen. Wir machen es zur "
   "Zahlungsbedingung, damit eine saubere Akte und der falsche Container "
   "nicht dasselbe sein können."),
 ],
}

BLACK = ' style="color:var(--black)"'


def section(name):
    lines = "\n      ".join(
        '<span class="ln"><span>%s</span></span>' % x for x in H2[name])
    steps = "\n      ".join(
        '<li><span class="k">%02d</span><h3>%s</h3><p>%s</p></li>'
        % (i + 1, t, b) for i, (t, b) in enumerate(STEPS[name]))
    return """%s
<section id="s-pay" aria-labelledby="h-pay" data-reveal>
  <div class="pay-wrap">
    <h2 class="display sm" id="h-pay"%s>
      %s
    </h2>
    <p class="lead">%s</p>
    <ol class="steps">
      %s
    </ol>
  </div>
</section>

""" % (MARK, BLACK, lines, LEAD[name], steps)


def main():
    pages = 0
    for name in ("index.html", "fr/index.html", "es/index.html", "de/index.html"):
        p = SITE / name
        s = p.read_text()
        orig = s

        if CSS.strip() not in s:
            if CSS_ANCHOR not in s:
                print("  ВНИМАНИЕ: %s, якорь CSS не найден" % name)
            else:
                s = s.replace(CSS_ANCHOR, CSS.strip() + "\n\n" + CSS_ANCHOR, 1)

        if MARK not in s:
            anchor = '<section id="s-journey"'
            if anchor not in s:
                print("  ВНИМАНИЕ: %s, якорь секции не найден" % name)
            else:
                s = s.replace(anchor, section(name) + anchor, 1)

        if s != orig:
            p.write_text(s)
            pages += 1
            print("  %s: блок платежа поставлен" % name)

    # Тема перекрашивает полосы в графит. Без этого блок встанет светлым
    # пятном посреди тёмной страницы.
    m = MERCURY.read_text()
    changed = 0
    for old, new in (("#s-cats, #s-proc, #s-why, #s-lane {",
                      "#s-cats, #s-proc, #s-why, #s-lane, #s-pay {"),
                     ("#s-lane h2,", "#s-lane h2, #s-pay h2, #s-pay h3,"),
                     ("#s-lane p,", "#s-lane p, #s-pay p,")):
        if new in m:
            continue
        if old not in m:
            print("  ВНИМАНИЕ: mercury.css, не найдено: %s" % old)
            continue
        m = m.replace(old, new, 1)
        changed += 1
    if changed:
        MERCURY.write_text(m)
        print("  mercury.css: правил дополнено %d (нужен css-version.py)" % changed)

    print("главных поправлено: %d" % pages)
    return 0


if __name__ == "__main__":
    sys.exit(main())
