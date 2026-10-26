# -*- coding: utf-8 -*-
"""Языковые версии сайта.

Источник правды это готовый HTML в site/, а не старый генератор в tools/:
сайт давно разошёлся с ним по вёрстке и теме. Поэтому переводы делаются
подстановкой строк в живую страницу, а не пересборкой.

Запуск:  python3 tools/make-languages.py
Результат: site/fr/, site/es/, site/de/ плюс hreflang и переключатель языка
на всех версиях, включая английскую.
"""
import pathlib, re, sys, html, json

ROOT = pathlib.Path(__file__).resolve().parent.parent / "site"
LANGS = ["fr", "es", "de"]
NAME = {"en": "English", "fr": "Français", "es": "Español", "de": "Deutsch"}

# ── Переводы главной. Ключ это английский оригинал, ровно как в HTML. ──────────
HOME = {
# навигация и общие
"What we do":            {"fr":"Notre métier","es":"Qué hacemos","de":"Was wir tun"},
"What we supply":        {"fr":"Ce que nous fournissons","es":"Qué suministramos","de":"Was wir liefern"},
"Corridors":             {"fr":"Corridors","es":"Corredores","de":"Korridore"},
"Guides":                {"fr":"Guides","es":"Guías","de":"Leitfäden"},
"About":                 {"fr":"À propos","es":"Quiénes somos","de":"Über uns"},
"Contact":               {"fr":"Contact","es":"Contacto","de":"Kontakt"},
"Request a quote":       {"fr":"Demander un prix","es":"Solicitar precio","de":"Angebot anfordern"},
"Skip to content":       {"fr":"Aller au contenu","es":"Ir al contenido","de":"Zum Inhalt springen"},
"Scroll":                {"fr":"Défiler","es":"Desplazar","de":"Scrollen"},

# сцена 01
"ISP GROUP LLC · Aventura, Florida":
    {"fr":"ISP GROUP LLC · Aventura, Floride","es":"ISP GROUP LLC · Aventura, Florida","de":"ISP GROUP LLC · Aventura, Florida"},
"WE BUY":      {"fr":"NOUS ACHETONS","es":"COMPRAMOS","de":"WIR KAUFEN"},
"IN OUR OWN":  {"fr":"EN NOTRE","es":"EN NOMBRE","de":"IM EIGENEN"},
"NAME.":       {"fr":"PROPRE NOM.","es":"PROPIO.","de":"NAMEN."},
"We find the producer, confirm it can legally ship to your country, buy the goods ourselves and deliver them to your port. Principal, not a broker.":
 {"fr":"Nous trouvons le producteur, vérifions qu’il peut légalement expédier vers votre pays, achetons la marchandise nous-mêmes et la livrons à votre port. Négociant pour compte propre, pas courtier.",
  "es":"Localizamos al productor, confirmamos que puede exportar legalmente a su país, compramos la mercancía en nombre propio y la entregamos en su puerto. Actuamos como principal, no como intermediario.",
  "de":"Wir finden den Hersteller, prüfen, ob er rechtlich in Ihr Land liefern darf, kaufen die Ware auf eigene Rechnung und liefern sie an Ihren Hafen. Eigenhändler, kein Makler."},
"Discuss your requirements":
 {"fr":"Exposez votre besoin","es":"Cuéntenos su necesidad","de":"Bedarf besprechen"},

# сцена 02
"01 — Origin": {"fr":"01 — Origine","es":"01 — Origen","de":"01 — Ursprung"},
"FROM THE":    {"fr":"À LA","es":"DESDE EL","de":"AB"},
"SOURCE.":     {"fr":"SOURCE.","es":"ORIGEN.","de":"WERK."},
"A container is the last twenty per cent of the job. The work that decides the price and the risk happens at the mill, the plant and the establishment, months before anything is loaded.":
 {"fr":"Le conteneur, c’est les derniers vingt pour cent du travail. Ce qui décide du prix et du risque se joue à l’usine, à l’atelier et à l’établissement agréé, des mois avant le chargement.",
  "es":"El contenedor es el último veinte por ciento del trabajo. Lo que determina el precio y el riesgo ocurre en la acería, en la planta y en el establecimiento, meses antes de cargar nada.",
  "de":"Der Container ist die letzten zwanzig Prozent der Arbeit. Was über Preis und Risiko entscheidet, geschieht im Walzwerk, im Betrieb und im zugelassenen Haus, Monate vor der Verladung."},

# сцена 03
"02 — Sourcing and procurement":
 {"fr":"02 — Sourcing et achats","es":"02 — Búsqueda y compras","de":"02 — Beschaffung und Einkauf"},
"FIND THE":      {"fr":"TROUVER LA","es":"ENCONTRAR LA","de":"DIE RICHTIGE"},
"RIGHT SOURCE.": {"fr":"BONNE SOURCE.","es":"FUENTE CORRECTA.","de":"QUELLE FINDEN."},
"Supplier identification":
 {"fr":"Identification des fournisseurs","es":"Identificación de proveedores","de":"Lieferantensuche"},
"Procurement coordination":
 {"fr":"Coordination des achats","es":"Coordinación de compras","de":"Einkaufskoordination"},
"Specification and verification":
 {"fr":"Spécification et vérification","es":"Especificación y verificación","de":"Spezifikation und Prüfung"},
"Commercial negotiation":
 {"fr":"Négociation commerciale","es":"Negociación comercial","de":"Kommerzielle Verhandlung"},

# сцена 04
"03 — What we supply":
 {"fr":"03 — Ce que nous fournissons","es":"03 — Qué suministramos","de":"03 — Was wir liefern"},
"SIX CATEGORIES.": {"fr":"SIX CATÉGORIES.","es":"SEIS CATEGORÍAS.","de":"SECHS KATEGORIEN."},
"Where we already have producer relationships and a documented lane.":
 {"fr":"Là où nous avons déjà des relations producteurs et une route documentée.",
  "es":"Donde ya tenemos relaciones con productores y una ruta documentada.",
  "de":"Dort, wo wir bereits Herstellerkontakte und eine dokumentierte Route haben."},
"Building and finishing materials":
 {"fr":"Matériaux de construction et de finition","es":"Materiales de construcción y acabado","de":"Bau- und Ausbaustoffe"},
"Stone · tile · cement · cable":
 {"fr":"Pierre · carrelage · ciment · câble","es":"Piedra · azulejo · cemento · cable","de":"Stein · Fliesen · Zement · Kabel"},
"Industrial equipment and machinery":
 {"fr":"Équipements et machines industriels","es":"Equipos y maquinaria industrial","de":"Industrieanlagen und Maschinen"},
"Lines · compressors · pumps":
 {"fr":"Lignes · compresseurs · pompes","es":"Líneas · compresores · bombas","de":"Anlagen · Kompressoren · Pumpen"},
"Tools, hardware and fasteners":
 {"fr":"Outillage, quincaillerie et fixations","es":"Herramientas, ferretería y fijaciones","de":"Werkzeuge, Beschläge und Befestiger"},
"Power tools · abrasives · fixings":
 {"fr":"Électroportatif · abrasifs · fixations","es":"Eléctricas · abrasivos · fijaciones","de":"Elektrowerkzeug · Schleifmittel · Befestigung"},
"Metals and pipe": {"fr":"Métaux et tubes","es":"Metales y tubería","de":"Metalle und Rohre"},
"Sections · sheet · line pipe":
 {"fr":"Profilés · tôle · tubes de conduite","es":"Perfiles · chapa · tubería de línea","de":"Profile · Blech · Leitungsrohr"},
"Paper, packaging and consumables":
 {"fr":"Papier, emballage et consommables","es":"Papel, embalaje y consumibles","de":"Papier, Verpackung und Verbrauchsgüter"},
"Board · film · facility supply":
 {"fr":"Carton · film · fournitures de site","es":"Cartón · film · suministros de planta","de":"Karton · Folie · Objektbedarf"},
"Food, commodities and beverages":
 {"fr":"Alimentaire, matières premières et boissons","es":"Alimentación, materias primas y bebidas","de":"Lebensmittel, Rohwaren und Getränke"},
"Frozen · staples · branded drinks":
 {"fr":"Surgelé · denrées de base · boissons de marque","es":"Congelado · básicos · bebidas de marca","de":"Tiefkühl · Grundnahrung · Markengetränke"},

# сцена 05
"04 — Movement": {"fr":"04 — Acheminement","es":"04 — Movimiento","de":"04 — Transport"},
"ACROSS BORDERS,": {"fr":"AU-DELÀ DES","es":"A TRAVÉS DE","de":"ÜBER GRENZEN,"},
"TO YOUR PORT.":   {"fr":"FRONTIÈRES.","es":"LAS FRONTERAS.","de":"ZU IHREM HAFEN."},
"Ocean, rail and road into one quoted number, with the Incoterm written on it. A price that does not say where the goods stop is not a price.":
 {"fr":"Maritime, ferroviaire et routier réunis en un seul prix, avec l’Incoterm écrit dessus. Un prix qui ne dit pas où la marchandise s’arrête n’est pas un prix.",
  "es":"Marítimo, ferroviario y terrestre en una sola cifra, con el Incoterm escrito en ella. Un precio que no dice dónde se detiene la mercancía no es un precio.",
  "de":"See, Schiene und Straße in einer Zahl, mit dem Incoterm darauf. Ein Preis, der nicht sagt, wo die Ware endet, ist kein Preis."},

# сцена 06
"05 — How we work": {"fr":"05 — Notre méthode","es":"05 — Cómo trabajamos","de":"05 — So arbeiten wir"},
"ONE PROCESS,": {"fr":"UN PROCESSUS,","es":"UN PROCESO,","de":"EIN ABLAUF,"},
"FIVE STEPS.":  {"fr":"CINQ ÉTAPES.","es":"CINCO PASOS.","de":"FÜNF SCHRITTE."},
"Understand": {"fr":"Comprendre","es":"Entender","de":"Verstehen"},
"You send the product, the quantity and the destination. We come back with the questions that decide the price, not with a brochure.":
 {"fr":"Vous envoyez le produit, la quantité et la destination. Nous revenons avec les questions qui décident du prix, pas avec une plaquette.",
  "es":"Usted envía el producto, la cantidad y el destino. Volvemos con las preguntas que deciden el precio, no con un folleto.",
  "de":"Sie nennen Produkt, Menge und Bestimmungsort. Wir kommen mit den Fragen zurück, die den Preis entscheiden, nicht mit einer Broschüre."},
"Source": {"fr":"Sourcer","es":"Buscar","de":"Beschaffen"},
"We approach producers directly and establish that they can legally ship to your country before anything else is discussed.":
 {"fr":"Nous contactons les producteurs directement et établissons qu’ils peuvent légalement expédier vers votre pays avant toute autre discussion.",
  "es":"Contactamos directamente con los productores y comprobamos que pueden exportar legalmente a su país antes de hablar de nada más.",
  "de":"Wir sprechen Hersteller direkt an und klären zuerst, ob sie rechtlich in Ihr Land liefern dürfen."},
"Structure": {"fr":"Structurer","es":"Estructurar","de":"Strukturieren"},
"Specification, pack, Incoterm, payment terms and the document set are agreed in writing, line by line, on one basis.":
 {"fr":"Spécification, conditionnement, Incoterm, conditions de paiement et jeu documentaire sont convenus par écrit, ligne par ligne, sur une même base.",
  "es":"Especificación, embalaje, Incoterm, condiciones de pago y juego documental se acuerdan por escrito, línea por línea, sobre una misma base.",
  "de":"Spezifikation, Verpackung, Incoterm, Zahlungsbedingungen und Dokumentensatz werden schriftlich vereinbart, Zeile für Zeile, auf einer Basis."},
"Coordinate": {"fr":"Coordonner","es":"Coordinar","de":"Koordinieren"},
"Purchase, documents and transport are coordinated within the agreed scope, with a single point of contact on our side.":
 {"fr":"Achat, documents et transport sont coordonnés dans le périmètre convenu, avec un interlocuteur unique de notre côté.",
  "es":"Compra, documentos y transporte se coordinan dentro del alcance acordado, con un único interlocutor por nuestra parte.",
  "de":"Einkauf, Dokumente und Transport werden im vereinbarten Umfang koordiniert, mit einem Ansprechpartner auf unserer Seite."},
"Deliver": {"fr":"Livrer","es":"Entregar","de":"Liefern"},
"The goods arrive at the agreed place on the agreed terms, and the paperwork arrives with them rather than after them.":
 {"fr":"La marchandise arrive au lieu convenu selon les conditions convenues, et les documents arrivent avec elle, pas après.",
  "es":"La mercancía llega al lugar acordado en las condiciones acordadas, y los documentos llegan con ella, no después.",
  "de":"Die Ware kommt am vereinbarten Ort zu den vereinbarten Bedingungen an, und die Papiere kommen mit ihr, nicht danach."},

# сцена 07
"06 — Why ISP Group": {"fr":"06 — Pourquoi ISP Group","es":"06 — Por qué ISP Group","de":"06 — Warum ISP Group"},
"A broker passes your enquiry on.":
 {"fr":"Un courtier transmet votre demande.","es":"Un intermediario traslada su consulta.","de":"Ein Makler reicht Ihre Anfrage weiter."},
"We take the position.":
 {"fr":"Nous prenons la position.","es":"Nosotros tomamos la posición.","de":"Wir gehen ins Risiko."},
"Principal, not a broker":
 {"fr":"Pour compte propre, pas courtier","es":"Principal, no intermediario","de":"Eigenhändler, kein Makler"},
"We buy in our own name, so the contract, the payment and the responsibility sit with one company.":
 {"fr":"Nous achetons en notre propre nom : le contrat, le paiement et la responsabilité tiennent dans une seule société.",
  "es":"Compramos en nombre propio: el contrato, el pago y la responsabilidad quedan en una sola empresa.",
  "de":"Wir kaufen im eigenen Namen: Vertrag, Zahlung und Verantwortung liegen bei einem Unternehmen."},
"Admissibility before price":
 {"fr":"L’admissibilité avant le prix","es":"La admisibilidad antes que el precio","de":"Zulässigkeit vor Preis"},
"An offer from a producer that cannot legally ship to your destination is not an offer, whatever the number on it.":
 {"fr":"L’offre d’un producteur qui ne peut pas légalement expédier vers votre destination n’est pas une offre, quel que soit le chiffre.",
  "es":"La oferta de un productor que no puede exportar legalmente a su destino no es una oferta, diga lo que diga la cifra.",
  "de":"Das Angebot eines Herstellers, der nicht an Ihr Ziel liefern darf, ist kein Angebot, gleich welche Zahl darauf steht."},
"One basis for every quotation":
 {"fr":"Une seule base pour toutes les offres","es":"Una sola base para cada oferta","de":"Eine Basis für jedes Angebot"},
"Same Incoterm, same pack, same line items, so the numbers you compare are actually comparable.":
 {"fr":"Même Incoterm, même conditionnement, mêmes postes : les chiffres que vous comparez sont réellement comparables.",
  "es":"Mismo Incoterm, mismo embalaje, mismas partidas: las cifras que compara son realmente comparables.",
  "de":"Gleicher Incoterm, gleiche Verpackung, gleiche Positionen: die Zahlen sind wirklich vergleichbar."},
"A single point of contact":
 {"fr":"Un interlocuteur unique","es":"Un único interlocutor","de":"Ein Ansprechpartner"},
"One company answers for the goods, the documents and the lane, from first enquiry to arrival.":
 {"fr":"Une seule société répond de la marchandise, des documents et de la route, de la première demande à l’arrivée.",
  "es":"Una sola empresa responde por la mercancía, los documentos y la ruta, desde la consulta hasta la llegada.",
  "de":"Ein Unternehmen haftet für Ware, Dokumente und Route, von der ersten Anfrage bis zur Ankunft."},

# форма
"07 — Start": {"fr":"07 — Démarrer","es":"07 — Empezar","de":"07 — Start"},
"SEND A SPECIFICATION.":
 {"fr":"ENVOYEZ UN CAHIER","es":"ENVÍE UNA","de":"SPEZIFIKATION"},
"GET A LANDED PRICE.":
 {"fr":"DES CHARGES.","es":"ESPECIFICACIÓN.","de":"SENDEN."},
"Name": {"fr":"Nom","es":"Nombre","de":"Name"},
"Work e-mail": {"fr":"E-mail professionnel","es":"Correo de trabajo","de":"Geschäftliche E-Mail"},
"Company": {"fr":"Société","es":"Empresa","de":"Unternehmen"},
"Country": {"fr":"Pays","es":"País","de":"Land"},
"Category": {"fr":"Catégorie","es":"Categoría","de":"Kategorie"},
"Other": {"fr":"Autre","es":"Otro","de":"Sonstiges"},
"Terms to quote": {"fr":"Incoterm souhaité","es":"Incoterm a cotizar","de":"Gewünschter Incoterm"},
"Not sure, advise": {"fr":"Je ne sais pas, conseillez-moi","es":"No estoy seguro, aconséjenme","de":"Unklar, bitte beraten"},
"Quantity": {"fr":"Quantité","es":"Cantidad","de":"Menge"},
"Destination port or city": {"fr":"Port ou ville de destination","es":"Puerto o ciudad de destino","de":"Zielhafen oder Zielort"},
"Specification": {"fr":"Spécification","es":"Especificación","de":"Spezifikation"},
"Website": {"fr":"Site web","es":"Sitio web","de":"Webseite"},
"Start a trade request": {"fr":"Envoyer la demande","es":"Enviar la solicitud","de":"Anfrage senden"},
"Sent straight to info@ispgroupgc.com. We reply within one working day.":
 {"fr":"Envoyé directement à info@ispgroupgc.com. Nous répondons sous un jour ouvré.",
  "es":"Se envía directamente a info@ispgroupgc.com. Respondemos en un día hábil.",
  "de":"Geht direkt an info@ispgroupgc.com. Wir antworten innerhalb eines Werktags."},

# подвал
"Supply": {"fr":"Fournitures","es":"Suministro","de":"Lieferung"},
"Building materials": {"fr":"Matériaux de construction","es":"Materiales de construcción","de":"Baustoffe"},
"Industrial equipment": {"fr":"Équipements industriels","es":"Equipos industriales","de":"Industrieanlagen"},
"Tools and hardware": {"fr":"Outillage et quincaillerie","es":"Herramientas y ferretería","de":"Werkzeug und Beschläge"},
"Paper and packaging": {"fr":"Papier et emballage","es":"Papel y embalaje","de":"Papier und Verpackung"},
"Food and beverages": {"fr":"Alimentaire et boissons","es":"Alimentación y bebidas","de":"Lebensmittel und Getränke"},
"How we work": {"fr":"Notre méthode","es":"Cómo trabajamos","de":"So arbeiten wir"},
"Experience": {"fr":"Expérience","es":"Experiencia","de":"Erfahrung"},
"Verify a supplier": {"fr":"Vérifier un fournisseur","es":"Verificar un proveedor","de":"Lieferanten prüfen"},
"Incoterms": {"fr":"Incoterms","es":"Incoterms","de":"Incoterms"},
"Landed price": {"fr":"Prix rendu","es":"Precio puesto en destino","de":"Landed-Price"},
"HS codes": {"fr":"Codes SH","es":"Códigos HS","de":"HS-Codes"},
"All guides": {"fr":"Tous les guides","es":"Todas las guías","de":"Alle Leitfäden"},
"United States": {"fr":"États-Unis","es":"Estados Unidos","de":"Vereinigte Staaten"},
"Privacy": {"fr":"Confidentialité","es":"Privacidad","de":"Datenschutz"},
"Terms": {"fr":"Conditions","es":"Condiciones","de":"AGB"},
"Photography licensed CC0 or public domain; see media credits.":
 {"fr":"Photographies sous licence CC0 ou domaine public ; voir les crédits.",
  "es":"Fotografías con licencia CC0 o de dominio público; véanse los créditos.",
  "de":"Fotos unter CC0 oder gemeinfrei; siehe Bildnachweise."},
}

META = {
 "title": {"en":"ISP Group LLC: sourcing, supply and delivery to your port",
  "fr":"ISP Group LLC : sourcing, approvisionnement et livraison à votre port",
  "es":"ISP Group LLC: sourcing, suministro y entrega en su puerto",
  "de":"ISP Group LLC: Beschaffung, Lieferung und Zustellung an Ihren Hafen"},
 "desc": {"en":"ISP GROUP LLC buys goods in its own name and delivers them to the buyer's port. Building materials, industrial equipment, tools, metals and pipe, paper and packaging, food and beverages.",
  "fr":"ISP GROUP LLC achète la marchandise en son propre nom et la livre à votre port. Matériaux de construction, équipements industriels, outillage, métaux et tubes, papier et emballage, alimentaire et boissons.",
  "es":"ISP GROUP LLC compra la mercancía en nombre propio y la entrega en su puerto. Materiales de construcción, equipos industriales, herramientas, metales y tubería, papel y embalaje, alimentación y bebidas.",
  "de":"ISP GROUP LLC kauft Ware im eigenen Namen und liefert sie an Ihren Hafen. Baustoffe, Industrieanlagen, Werkzeuge, Metalle und Rohre, Papier und Verpackung, Lebensmittel und Getränke."},
}

# внутренние ссылки главной: в языковой версии ведут на английские страницы,
# пока те не переведены, поэтому остаются абсолютными от корня
LINKS = ["services","supply","corridors","guides","about","contact","building-materials",
         "industrial-equipment","tools-hardware","metals-pipe","paper-packaging",
         "food-agricultural","experience","verify-supplier","incoterms","landed-price",
         "hs-code","privacy","terms"]


def switcher(cur):
    """Переключатель языка для шапки."""
    out = ['<div class="langsw" aria-label="Language">']
    for code in ["en"] + LANGS:
        href = "/" if code == "en" else f"/{code}/"
        if code == cur:
            out.append(f'<span aria-current="true">{code.upper()}</span>')
        else:
            out.append(f'<a href="{href}" hreflang="{code}" title="{NAME[code]}">{code.upper()}</a>')
    out.append("</div>")
    return "".join(out)


SW_CSS = """
.langsw{display:flex;gap:9px;align-items:center;font-family:var(--mono);font-size:11px;
  letter-spacing:.1em;margin-left:18px}
.langsw a{text-decoration:none;opacity:.55}
.langsw a:hover{opacity:1}
.langsw [aria-current]{color:var(--gold);opacity:1}
"""


def hreflang(cur):
    rows = []
    for code in ["en"] + LANGS:
        href = "https://ispgroupgc.com/" if code == "en" else f"https://ispgroupgc.com/{code}/"
        rows.append(f'<link rel="alternate" hreflang="{code}" href="{href}">')
    rows.append('<link rel="alternate" hreflang="x-default" href="https://ispgroupgc.com/">')
    return "\n".join(rows)


def translate(src, lang):
    s = src
    # порядок по убыванию длины, чтобы длинная фраза не разрезалась короткой
    for en in sorted(HOME, key=len, reverse=True):
        tr = HOME[en].get(lang)
        if not tr:
            continue
        # в HTML те же тексты могут стоять с сущностями: &middot;, &amp;, &rsquo;
        for a, b in ((en, tr),
                     (en.replace("\u00b7", "&middot;"), tr),
                     (html.escape(en), tr),
                     (en.replace("\u2019", "&rsquo;"), tr),
                     (en.replace("\u2014", "&mdash;"), tr),
                     (en.replace("\u2014", "&mdash;").replace("\u00b7", "&middot;"), tr)):
            s = s.replace(">" + a + "<", ">" + b + "<")
        # значения в атрибутах: placeholder, title, option
        s = s.replace('placeholder="' + en + '"', 'placeholder="' + tr + '"')
    return s


def build():
    src = (ROOT / "index.html").read_text()
    made = []

    # общие вставки на английской версии
    en = src
    en = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', "", en)
    en = en.replace('<link rel="canonical" href="https://ispgroupgc.com/">',
                    '<link rel="canonical" href="https://ispgroupgc.com/">\n' + hreflang("en"))
    if ".langsw{" not in en:
        en = en.replace("</style>", SW_CSS + "</style>", 1)
    en = en.replace('<a class="cta" href="#request">', switcher("en") + '\n    <a class="cta" href="#request">')
    (ROOT / "index.html").write_text(en)

    for lang in LANGS:
        d = ROOT / lang
        d.mkdir(exist_ok=True)
        s = translate(en, lang)
        s = s.replace('<html lang="en">', f'<html lang="{lang}">')
        s = s.replace('<link rel="canonical" href="https://ispgroupgc.com/">',
                      f'<link rel="canonical" href="https://ispgroupgc.com/{lang}/">')
        s = s.replace(f'<title>{META["title"]["en"]}</title>', f'<title>{META["title"][lang]}</title>')
        s = s.replace(META["desc"]["en"], META["desc"][lang])
        s = s.replace(switcher("en"), switcher(lang))
        # относительные ссылки становятся абсолютными, иначе внутри /fr/ они ломаются
        for slug in LINKS:
            s = s.replace(f'href="{slug}"', f'href="/{slug}"')
        s = s.replace('href="media/', 'href="/media/')
        s = s.replace('src="media/', 'src="/media/')
        s = s.replace('srcset="media/', 'srcset="/media/')
        (d / "index.html").write_text(s)
        made.append(f"{lang}/index.html")
    return made


if __name__ == "__main__":
    for f in build():
        print("создано:", f)
