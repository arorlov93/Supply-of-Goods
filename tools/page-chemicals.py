# -*- coding: utf-8 -*-
"""Страница /chemicals на четырёх языках. Пункт 2 брифа от 10.11.2026.

Как устроено. Полная пересборка сайта запрещена, поэтому страница
собирается из уже собранной china.html: у неё верная голова с версткой
содержательной страницы (chero, lede, toc, prose, cta), верный подвал и
верные стили. Меняются голова, шапка статьи и всё содержимое main.

Языки. Шапка и подвал не переводятся по словарю, а берутся целиком из
соответствующей локальной главной (site/fr/index.html и так далее): там
они уже переведены и выверены. Содержание страницы написано на четырёх
языках здесь, а не прогоняется через подстановку: таблица продуктов и
техническая терминология подстановкой не переводятся.

Форма. Отправка идёт на тот же /api/quote, что и остальные формы сайта,
с полем kind=chemicals. По нему функция ставит в письме тему
«Chemicals RFQ», см. tools/chem-form-api.py. Телефон, марка и номер
тендера кладутся в поле spec отдельными строками: заводить под них
колонки в базе значит менять схему D1 вслепую, а выигрыша нет.

Запуск: python3.13 tools/page-chemicals.py
Повторный запуск переписывает страницы тем же содержимым.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
SHELL = SITE / "china.html"
LANGS = ("en", "fr", "es", "de")
OUT = {"en": "chemicals.html", "fr": "fr/chemicals.html",
       "es": "es/chemicals.html", "de": "de/chemicals.html"}
URL = {"en": "https://ispgroupgc.com/chemicals",
       "fr": "https://ispgroupgc.com/fr/chemicals",
       "es": "https://ispgroupgc.com/es/chemicals",
       "de": "https://ispgroupgc.com/de/chemicals"}

META = {
 "en": ("Oilfield and water treatment chemicals | ISP Group",
        "Phosphonates, scale and corrosion inhibitors, demulsifiers, PAC, "
        "ion exchange resins and molecular sieves from ISO-certified "
        "plants."),
 "fr": ("Produits chimiques pour l’eau et le pétrole | ISP Group",
        "Phosphonates, inhibiteurs d’entartrage et de corrosion, "
        "désémulsifiants, PAC, résines échangeuses d’ions et tamis "
        "moléculaires."),
 "es": ("Químicos para tratamiento de agua y petróleo | ISP Group",
        "Fosfonatos, inhibidores de incrustaciones y corrosión, "
        "desemulsionantes, PAC, resinas de intercambio iónico y tamices "
        "moleculares."),
 "de": ("Wasseraufbereitungs- und Ölfeldchemikalien | ISP Group",
        "Phosphonate, Scale- und Korrosionsinhibitoren, Demulgatoren, "
        "PAC, Ionenaustauscherharze und Molekularsiebe aus "
        "ISO-zertifizierten Werken."),
}

CRUMB = {"en": "Chemicals", "fr": "Chimie", "es": "Química", "de": "Chemie"}

H1 = {
 "en": "Water treatment and <em>oilfield chemicals</em>",
 "fr": "Chimie de l’eau et <em>des champs pétroliers</em>",
 "es": "Química para agua y <em>campos petroleros</em>",
 "de": "Chemie für Wasseraufbereitung <em>und Ölfeld</em>",
}

SUB = {
 "en": "Scale and corrosion control, coagulation, ion exchange, demulsifying "
       "and gas drying. Supplied as principal, with the document set that "
       "lets the goods clear and the batch be checked.",
 "fr": "Lutte contre l’entartrage et la corrosion, coagulation, échange "
       "d’ions, désémulsification et séchage du gaz. Fournis en notre propre "
       "nom, avec le jeu de documents qui permet le dédouanement et le "
       "contrôle du lot.",
 "es": "Control de incrustaciones y corrosión, coagulación, intercambio "
       "iónico, desemulsión y secado de gas. Suministrados en nombre propio, "
       "con el juego de documentos que permite despachar la mercancía y "
       "verificar el lote.",
 "de": "Scale- und Korrosionsschutz, Koagulation, Ionenaustausch, "
       "Demulgierung und Gastrocknung. Im eigenen Namen geliefert, mit dem "
       "Dokumentensatz für Verzollung und Chargenprüfung.",
}

CHIPS = {
 "en": ["Oil &amp; gas", "Power and CHP", "Water utilities", "Mining",
        "Principal, <b>not a broker</b>"],
 "fr": ["Pétrole et gaz", "Électricité et cogénération", "Services d’eau",
        "Mines", "Principal, <b>pas courtier</b>"],
 "es": ["Petróleo y gas", "Energía y cogeneración", "Servicios de agua",
        "Minería", "Principal, <b>no intermediario</b>"],
 "de": ["Öl und Gas", "Strom und KWK", "Wasserversorger", "Bergbau",
        "Eigenhändler, <b>kein Makler</b>"],
}

LEDE = {
 "en": ("What we supply, and to whom",
        "We supply process chemicals to oil and gas producers, power plants, "
        "mining companies, water utilities and chemical distributors. We "
        "quote from manufacturers we have verified, and deliver to your port "
        "or warehouse with the full "
        "document set."),
 "fr": ("Ce que nous fournissons, et à qui",
        "Nous fournissons des produits chimiques de procédé aux producteurs "
        "de pétrole et de gaz, aux centrales électriques, aux sociétés "
        "minières, aux services d’eau et aux distributeurs de produits "
        "chimiques. Nous cotons depuis des fabricants que nous avons "
        "vérifiés, et livrons à votre port "
        "ou à votre entrepôt avec le jeu de documents complet."),
 "es": ("Qué suministramos y a quién",
        "Suministramos productos químicos de proceso a productores de "
        "petróleo y gas, centrales eléctricas, empresas mineras, servicios "
        "de agua y distribuidores químicos. Cotizamos desde fabricantes que "
        "hemos verificado, y entregamos en "
        "su puerto o almacén con el juego de documentos completo."),
 "de": ("Was wir liefern, und an wen",
        "Wir liefern Prozesschemikalien an Öl- und Gasproduzenten, "
        "Kraftwerke, Bergbauunternehmen, Wasserversorger und "
        "Chemiedistributoren. Wir bieten aus Werken an, die wir geprüft "
        "haben, und liefern an Ihren Hafen "
        "oder Ihr Lager mit dem vollständigen Dokumentensatz."),
}

TABLE_HEAD = {
 "en": ("Group", "Products", "Applications", "Packing"),
 "fr": ("Famille", "Produits", "Applications", "Conditionnement"),
 "es": ("Familia", "Productos", "Aplicaciones", "Envase"),
 "de": ("Gruppe", "Produkte", "Anwendungen", "Gebinde"),
}

TABLE = {
 "en": [
  ("Phosphonates and scale inhibitors",
   "ATMP 50 % and 95 % solid, HEDP 60 % and 90 % solid, PBTCA 50 %, DTPMPA 50 %",
   "Cooling and boiler water, oilfield scale control",
   "25 kg bags, 250 kg drums, 1,250 kg IBC"),
  ("RO antiscalants", "Antiscalant for reverse osmosis and desalination",
   "RO and SWRO membranes", "1,000 kg IBC"),
  ("Coagulants",
   "PAC 28–30 % Al<sub>2</sub>O<sub>3</sub>, drinking water (NSF/ANSI 60) and industrial grade",
   "Drinking water, wastewater, paper, textile, mining", "25 kg bags"),
  ("Ion exchange resins",
   "Strong acid cation (gel, H/Na), strong base anion (gel and macroporous, Cl), weak base anion",
   "Demineralization, softening, condensate polishing, uranium and gold recovery",
   "25 L bags"),
  ("Oilfield chemicals",
   "Demulsifiers, demulsifier intermediates, corrosion inhibitors",
   "Crude oil treatment, pipelines, produced water", "Drums, IBC"),
  ("Adsorbents", "Molecular sieves 3A, 4A, 13X; activated alumina",
   "Gas dehydration, air drying, catalyst support", "Steel drums, bags"),
 ],
 "fr": [
  ("Phosphonates et inhibiteurs d’entartrage",
   "ATMP 50 % et 95 % solide, HEDP 60 % et 90 % solide, PBTCA 50 %, DTPMPA 50 %",
   "Eau de refroidissement et de chaudière, lutte contre l’entartrage en champ pétrolier",
   "Sacs de 25 kg, fûts de 250 kg, IBC de 1 250 kg"),
  ("Antitartres pour osmose inverse", "Antitartre pour osmose inverse et dessalement",
   "Membranes OI et OI d’eau de mer", "IBC de 1 000 kg"),
  ("Coagulants",
   "PAC 28–30 % Al<sub>2</sub>O<sub>3</sub>, qualité eau potable (NSF/ANSI 60) et qualité industrielle",
   "Eau potable, eaux usées, papier, textile, mines", "Sacs de 25 kg"),
  ("Résines échangeuses d’ions",
   "Cationique forte (gel, H/Na), anionique forte (gel et macroporeuse, Cl), anionique faible",
   "Déminéralisation, adoucissement, polissage des condensats, récupération d’uranium et d’or",
   "Sacs de 25 L"),
  ("Produits pour champs pétroliers",
   "Désémulsifiants, intermédiaires de désémulsifiants, inhibiteurs de corrosion",
   "Traitement du brut, conduites, eaux de production", "Fûts, IBC"),
  ("Adsorbants", "Tamis moléculaires 3A, 4A, 13X ; alumine activée",
   "Déshydratation du gaz, séchage de l’air, support de catalyseur", "Fûts acier, sacs"),
 ],
 "es": [
  ("Fosfonatos e inhibidores de incrustaciones",
   "ATMP 50 % y 95 % sólido, HEDP 60 % y 90 % sólido, PBTCA 50 %, DTPMPA 50 %",
   "Agua de refrigeración y de caldera, control de incrustaciones en campo petrolero",
   "Sacos de 25 kg, bidones de 250 kg, IBC de 1.250 kg"),
  ("Antiincrustantes para ósmosis inversa", "Antiincrustante para ósmosis inversa y desalación",
   "Membranas OI y OI de agua de mar", "IBC de 1.000 kg"),
  ("Coagulantes",
   "PAC 28–30 % Al<sub>2</sub>O<sub>3</sub>, grado agua potable (NSF/ANSI 60) y grado industrial",
   "Agua potable, aguas residuales, papel, textil, minería", "Sacos de 25 kg"),
  ("Resinas de intercambio iónico",
   "Catiónica fuerte (gel, H/Na), aniónica fuerte (gel y macroporosa, Cl), aniónica débil",
   "Desmineralización, ablandamiento, pulido de condensados, recuperación de uranio y oro",
   "Sacos de 25 L"),
  ("Químicos para campo petrolero",
   "Desemulsionantes, intermedios de desemulsionantes, inhibidores de corrosión",
   "Tratamiento de crudo, tuberías, agua producida", "Bidones, IBC"),
  ("Adsorbentes", "Tamices moleculares 3A, 4A, 13X; alúmina activada",
   "Deshidratación de gas, secado de aire, soporte de catalizador", "Bidones de acero, sacos"),
 ],
 "de": [
  ("Phosphonate und Scale-Inhibitoren",
   "ATMP 50 % und 95 % fest, HEDP 60 % und 90 % fest, PBTCA 50 %, DTPMPA 50 %",
   "Kühl- und Kesselwasser, Scale-Kontrolle im Ölfeld",
   "25-kg-Säcke, 250-kg-Fässer, 1.250-kg-IBC"),
  ("RO-Antiscalants", "Antiscalant für Umkehrosmose und Entsalzung",
   "RO- und SWRO-Membranen", "1.000-kg-IBC"),
  ("Koagulationsmittel",
   "PAC 28–30 % Al<sub>2</sub>O<sub>3</sub>, Trinkwasserqualität (NSF/ANSI 60) und Industriequalität",
   "Trinkwasser, Abwasser, Papier, Textil, Bergbau", "25-kg-Säcke"),
  ("Ionenaustauscherharze",
   "Stark saure Kationen (Gel, H/Na), stark basische Anionen (Gel und makroporös, Cl), schwach basische Anionen",
   "Entsalzung, Enthärtung, Kondensatreinigung, Uran- und Goldgewinnung",
   "25-L-Säcke"),
  ("Ölfeldchemikalien",
   "Demulgatoren, Demulgator-Zwischenprodukte, Korrosionsinhibitoren",
   "Rohölaufbereitung, Rohrleitungen, Lagerstättenwasser", "Fässer, IBC"),
  ("Adsorbentien", "Molekularsiebe 3A, 4A, 13X; aktiviertes Aluminiumoxid",
   "Gastrocknung, Lufttrocknung, Katalysatorträger", "Stahlfässer, Säcke"),
 ],
}

STEPS_H = {
 "en": "How we supply chemicals", "fr": "Comment nous livrons la chimie",
 "es": "Cómo suministramos la química", "de": "Wie wir Chemie liefern",
}
STEPS = {
 "en": [
  ("Specification", "You send the grade, quantity, destination and your tender requirements."),
  ("Documents first", "TDS, SDS and a sample COA before any price."),
  ("Quotation", "One basis, covering Incoterm, pack, lead time and document set."),
  ("Production and inspection", "Batch COA from the plant; third-party inspection (SGS, Intertek or Bureau Veritas) where required."),
  ("Delivery", "By sea, rail or truck, FOB or CIF your port or delivered to site, documents with the goods."),
 ],
 "fr": [
  ("Spécification", "Vous indiquez la qualité, la quantité, la destination et les exigences de votre appel d’offres."),
  ("Les documents d’abord", "TDS, FDS et un COA type avant tout prix."),
  ("Cotation", "Une seule base, couvrant l’Incoterm, le conditionnement, le délai et le jeu de documents."),
  ("Production et inspection", "COA de lot délivré par l’usine ; inspection par tiers (SGS, Intertek ou Bureau Veritas) lorsque c’est exigé."),
  ("Livraison", "Par mer, rail ou route, FOB ou CIF votre port ou rendu sur site, documents avec la marchandise."),
 ],
 "es": [
  ("Especificación", "Usted indica el grado, la cantidad, el destino y los requisitos de su licitación."),
  ("Primero los documentos", "TDS, SDS y un COA de muestra antes de cualquier precio."),
  ("Cotización", "Una sola base, con Incoterm, envase, plazo y juego de documentos."),
  ("Producción e inspección", "COA de lote emitido por la planta; inspección por tercero (SGS, Intertek o Bureau Veritas) cuando se exige."),
  ("Entrega", "Por mar, ferrocarril o camión, FOB o CIF su puerto o entregado en obra, documentos con la mercancía."),
 ],
 "de": [
  ("Spezifikation", "Sie nennen Qualität, Menge, Bestimmungsort und die Anforderungen Ihrer Ausschreibung."),
  ("Zuerst die Dokumente", "TDS, SDB und ein Muster-COA vor jedem Preis."),
  ("Angebot", "Eine Basis, mit Incoterm, Gebinde, Lieferzeit und Dokumentensatz."),
  ("Produktion und Inspektion", "Chargen-COA vom Werk; Drittprüfung (SGS, Intertek oder Bureau Veritas), wo gefordert."),
  ("Lieferung", "Per See, Bahn oder Lkw, FOB oder CIF Ihr Hafen oder frei Baustelle, Dokumente mit der Ware."),
 ],
}

TENDER = {
 "en": ("For tenders",
        "We bid in tenders of national oil, gas and power companies. For each "
        "tender we provide the manufacturer’s letter of authorization, "
        "certificates of origin and quality, and the product documents your "
        "tender committee requires."),
 "fr": ("Pour les appels d’offres",
        "Nous soumissionnons aux appels d’offres des compagnies nationales de "
        "pétrole, de gaz et d’électricité. Pour chaque appel d’offres, nous "
        "fournissons la lettre d’autorisation du fabricant, les certificats "
        "d’origine et de qualité, et les documents produit exigés par votre "
        "commission d’appel d’offres."),
 "es": ("Para licitaciones",
        "Participamos en licitaciones de compañías nacionales de petróleo, gas "
        "y electricidad. Para cada licitación aportamos la carta de "
        "autorización del fabricante, los certificados de origen y calidad y "
        "los documentos de producto que exija su comité de licitación."),
 "de": ("Für Ausschreibungen",
        "Wir nehmen an Ausschreibungen nationaler Öl-, Gas- und "
        "Energieunternehmen teil. Für jede Ausschreibung stellen wir das "
        "Autorisierungsschreiben des Herstellers, Ursprungs- und "
        "Qualitätszeugnisse sowie die Produktdokumente bereit, die Ihr "
        "Ausschreibungsgremium verlangt."),
}

PAY = {
 "en": ("Payment terms",
        "Payment terms are agreed per order: letter of credit, documentary "
        "collection or staged payment against documents."),
 "fr": ("Conditions de paiement",
        "Les conditions de paiement sont convenues commande par commande : "
        "crédit documentaire, remise documentaire ou paiement échelonné "
        "contre documents."),
 "es": ("Condiciones de pago",
        "Las condiciones de pago se acuerdan por pedido: crédito "
        "documentario, cobranza documentaria o pago escalonado contra "
        "documentos."),
 "de": ("Zahlungsbedingungen",
        "Die Zahlungsbedingungen werden je Auftrag vereinbart: Akkreditiv, "
        "Dokumenteninkasso oder gestaffelte Zahlung gegen Dokumente."),
}

FORM_H = {
 "en": "Request a chemicals quote", "fr": "Demander un prix sur la chimie",
 "es": "Solicitar precio de química", "de": "Chemie-Angebot anfordern",
}
FORM_LEDE = {
 "en": "Product, grade and destination are enough to start. No account, no "
       "registration, no fee. We reply within one working day.",
 "fr": "Le produit, la qualité et la destination suffisent pour démarrer. "
       "Pas de compte, pas d’inscription, pas de frais. Réponse sous un jour ouvré.",
 "es": "El producto, el grado y el destino bastan para empezar. Sin cuenta, "
       "sin registro, sin cargo. Respondemos en un día hábil.",
 "de": "Produkt, Qualität und Bestimmungsort genügen für den Anfang. Kein "
       "Konto, keine Registrierung, keine Gebühr. Antwort binnen eines Arbeitstages.",
}
FIELDS = {
 "en": ["Company", "Country", "Product", "Grade / concentration",
        "Quantity per year", "Delivery point", "Tender number", "E-mail",
        "Phone", "optional", "Send the request", "Sending",
        "Please give your company, an e-mail and the product.",
        "Request received.",
        "We reply within one working day. If you have heard nothing by then, write to"],
 "fr": ["Société", "Pays", "Produit", "Qualité / concentration",
        "Quantité par an", "Lieu de livraison", "Numéro d’appel d’offres",
        "E-mail", "Téléphone", "facultatif", "Envoyer la demande", "Envoi",
        "Indiquez votre société, un e-mail et le produit.",
        "Demande reçue.",
        "Réponse sous un jour ouvré. Sans nouvelles d’ici là, écrivez à"],
 "es": ["Empresa", "País", "Producto", "Grado / concentración",
        "Cantidad por año", "Punto de entrega", "Número de licitación",
        "Correo electrónico", "Teléfono", "opcional", "Enviar la solicitud",
        "Enviando", "Indique su empresa, un correo y el producto.",
        "Solicitud recibida.",
        "Respondemos en un día hábil. Si no tiene noticias para entonces, escriba a"],
 "de": ["Firma", "Land", "Produkt", "Qualität / Konzentration",
        "Menge pro Jahr", "Lieferort", "Ausschreibungsnummer", "E-Mail",
        "Telefon", "optional", "Anfrage senden", "Senden",
        "Bitte Firma, E-Mail und Produkt angeben.",
        "Anfrage erhalten.",
        "Antwort binnen eines Arbeitstages. Hören Sie bis dahin nichts, schreiben Sie an"],
}

CSS = """
/* таблица продуктов и форма заявки на химию */
.ptab-wrap{overflow-x:auto;margin-top:clamp(22px,3vh,34px)}
table.ptab{width:100%;border-collapse:collapse;font-size:.92rem;min-width:680px}
table.ptab th{text-align:left;font-weight:500;padding:12px 16px 12px 0;
  border-bottom:1px solid var(--rule);color:var(--ink-2);white-space:nowrap}
table.ptab td{padding:14px 16px 14px 0;border-bottom:1px solid var(--rule);
  vertical-align:top;color:var(--ink-2)}
table.ptab td:first-child{color:var(--ink);font-weight:500;min-width:13rem}
table.ptab sub{font-size:.76em}
.cform-chem{margin-top:clamp(26px,4vh,44px);max-width:720px}
.cform-chem .fgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px 20px}
.cform-chem .f-full{grid-column:1 / -1}
.cform-chem label{display:block;font-size:13px;color:var(--ink-2);margin:0 0 6px}
.cform-chem .opt{color:var(--ink-3)}
.cform-chem input{width:100%;padding:12px 14px;border:1px solid var(--rule);
  border-radius:var(--radius-nav,10px);background:transparent;color:inherit;font:inherit}
.cform-chem input:focus-visible{outline:2px solid var(--brand);outline-offset:1px}
.cform-chem button{margin-top:20px}
.cform-chem .cresult{margin:0}
/* ловушка для ботов: поле есть в разметке, человек его не видит */
.cform-chem .hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
@media (max-width:620px){.cform-chem .fgrid{grid-template-columns:minmax(0,1fr)}}
"""


def form(lg):
    f = FIELDS[lg]
    def inp(i, fid, typ="text", full=False, opt=False):
        lab = f[i] + ('  <span class="opt">%s</span>' % f[9] if opt else "")
        return ('<div%s><label for="%s">%s</label>'
                '<input id="%s" type="%s"></div>'
                % (' class="f-full"' if full else "", fid, lab, fid, typ))
    return """<div class="lede" id="rfq"><h2>%s</h2><p class="intro">%s</p></div>
<form class="cform-chem" id="chemf" novalidate>
  <div class="fgrid">
    %s
    %s
    %s
    %s
    %s
    %s
    %s
    %s
    %s
  </div>
  <div class="hp" aria-hidden="true"><label for="c-website">Website</label><input id="c-website" type="text" tabindex="-1" autocomplete="off"></div>
  <button class="btn" type="submit">%s</button>
  <p class="cresult" id="chem-out" hidden></p>
</form>""" % (
      FORM_H[lg], FORM_LEDE[lg],
      inp(0, "c-co"), inp(1, "c-country"),
      inp(2, "c-product"), inp(3, "c-grade"),
      inp(4, "c-qty"), inp(5, "c-dest"),
      inp(7, "c-mail", "email"), inp(8, "c-phone", "tel"),
      inp(6, "c-tender", "text", full=True, opt=True),
      f[10])


SCRIPT = """<script>
(function(){
  var f=document.getElementById('chemf'); if(!f) return;
  var T=%s;
  function v(id){var e=document.getElementById(id);return e?(e.value||'').trim():'';}
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var out=document.getElementById('chem-out');
    var co=v('c-co'), mail=v('c-mail'), prod=v('c-product');
    if(!co||!mail||!prod){ out.textContent=T.need; out.hidden=false; return; }
    var spec=[T.product+': '+prod];
    if(v('c-grade'))  spec.push(T.grade+': '+v('c-grade'));
    if(v('c-tender')) spec.push(T.tender+': '+v('c-tender'));
    if(v('c-phone'))  spec.push(T.phone+': '+v('c-phone'));
    var data={kind:'chemicals', name:co, co:co, mail:mail, country:v('c-country'),
      cat:prod, qty:v('c-qty'), dest:v('c-dest'), spec:spec.join('\\n'),
      website:v('c-website'), page:location.pathname};
    var btn=f.querySelector('button[type=submit]'); var label=btn.textContent;
    btn.disabled=true; btn.textContent=T.sending;
    fetch('/api/quote',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify(data)})
      .then(function(r){return r.json().catch(function(){return null;});})
      .then(function(j){
        if(!j||!j.ok) throw 0;
        var ref=j.id?(' #'+j.id):'';
        f.innerHTML='<p class="cresult" style="margin:0"><b>'+T.done+'</b>'+ref+' '+
          T.tail+' <a class="mail" href="mailto:info@ispgroupgc.com">info@ispgroupgc.com</a>.</p>';
        if(window.gtag) gtag('event','quote_submit',{page:'chemicals'});
      })
      .catch(function(){
        out.textContent=T.need; out.hidden=false;
        btn.disabled=false; btn.textContent=label;
      });
  });
})();
</script>"""


HOST = "https://ispgroupgc.com"
ALT_HERO = {
 "en": "Steel pipe ends stacked in a yard",
 "fr": "Extrémités de tubes acier empilées sur un terre-plein",
 "es": "Extremos de tubería de acero apilados en un patio",
 "de": "Stahlrohrenden gestapelt auf einem Lagerplatz",
}
IMG = ("media/pipe.5ffeea4c.webp", "media/pipe.81b8af7b.jpg")


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def hero(lg):
    chips = "".join('<span class="chip">%s</span>' % c for c in CHIPS[lg])
    home = "/" if lg == "en" else "/%s/" % lg
    return (
      '<header class="hero chero" id="top">\n  <div class="wrap chero-g">\n    <div>\n'
      '      <nav class="crumbs" aria-label="Breadcrumb"><a href="%s">ISP Group</a> '
      '<span>/</span> <b>%s</b></nav>\n'
      '      <h1>%s</h1>\n'
      '      <p class="sub">%s</p>\n'
      '      <div class="chips">%s</div>\n'
      '      <div class="ctarow" style="margin-top:28px">'
      '<a class="btn" href="#rfq">%s</a></div>\n'
      '    </div>\n'
      '    <div class="heroside"><div class="shot"><span class="pz">'
      '<img src="/%s" srcset="/media/pipe-334.7c4291c3.webp 334w, /media/pipe.5ffeea4c.webp 900w" sizes="(max-width: 480px) 349px, (max-width: 900px) 731px, 509px" alt="%s" width="1040" height="1300" fetchpriority="high" decoding="async">'
      '</span></div></div>\n  </div>\n</header>'
      % (home, CRUMB[lg], H1[lg], SUB[lg], chips, FORM_H[lg], IMG[0], ALT_HERO[lg]))


def main_html(lg):
    hd = TABLE_HEAD[lg]
    rows = "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % r
        for r in TABLE[lg])
    table = ('<div class="ptab-wrap"><table class="ptab"><thead><tr>'
             '<th>%s</th><th>%s</th><th>%s</th><th>%s</th></tr></thead>'
             '<tbody>%s</tbody></table></div>' % (hd[0], hd[1], hd[2], hd[3], rows))

    steps = "".join(
        '<div class="pblock"><span class="k">%02d</span><h2 id="s%d">%s</h2>'
        '<div class="ptext"><p>%s</p></div></div>' % (i, i, h, t)
        for i, (h, t) in enumerate(STEPS[lg], 1))

    toc = "".join('<li><a href="#s%d"><span>%02d</span>%s</a></li>' % (i, i, h)
                  for i, (h, _) in enumerate(STEPS[lg], 1))

    lede_h, lede_t = LEDE[lg]
    t_h, t_t = TENDER[lg]
    p_h, p_t = PAY[lg]

    return """<main id="main" tabindex="-1">
<section data-reveal><div class="wrap">
  <div class="lede"><h2>%s</h2><p class="intro">%s</p></div>
  %s
  <nav class="toc" aria-label="%s"><ol>%s</ol></nav>
  <div class="prose">%s</div>
  <div class="lede" style="margin-top:56px"><h2>%s</h2><p class="intro">%s</p></div>
  <div class="lede" style="margin-top:40px"><h2>%s</h2><p class="intro">%s</p></div>
  %s
</div></section>
</main>""" % (lede_h, lede_t, table, STEPS_H[lg], toc, steps,
              t_h, t_t, p_h, p_t, form(lg))


def swap_chrome(s, lg):
    """Шапка и подвал берутся из локальной главной: там они уже переведены."""
    if lg == "en":
        return s
    loc = (SITE / lg / "index.html").read_text()
    for tag in ("nav", "footer"):
        m = re.search(r"(?s)<%s[^>]*>.*?</%s>" % (tag, tag), loc)
        if not m:
            print("  ВНИМАНИЕ: %s, %s на локальной главной не найден" % (lg, tag))
            continue
        s = re.sub(r"(?s)<%s[^>]*>.*?</%s>" % (tag, tag), lambda _m: m.group(0), s, count=1)
    return s


def absolutize(s):
    """Локальная страница лежит в /xx/, относительные ссылки оттуда бьют мимо."""
    def fix(m):
        attr, val = m.group(1), m.group(2)
        if re.match(r"^(https?:|//|/|#|mailto:|tel:|data:)", val):
            return m.group(0)
        return '%s="/%s"' % (attr, val)
    return re.sub(r'\b(href|src)="([^"]+)"', fix, s)


def build(lg, shell):
    s = shell
    url = URL[lg]
    title, desc = META[lg]

    s = re.sub(r"(?s)<title>.*?</title>", lambda _m: "<title>%s</title>" % esc(title), s, count=1)
    s = re.sub(r'<meta name="description" content="[^"]*">',
               lambda _m: '<meta name="description" content="%s">' % esc(desc), s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">',
               lambda _m: '<link rel="canonical" href="%s">' % url, s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*">',
               lambda _m: '<meta property="og:url" content="%s">' % url, s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">',
               lambda _m: '<meta property="og:title" content="%s">' % esc(title), s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">',
               lambda _m: '<meta property="og:description" content="%s">' % esc(desc), s, count=1)
    s = re.sub(r'<meta property="og:image" content="[^"]*">',
               lambda _m: '<meta property="og:image" content="%s/%s">' % (HOST, IMG[1]), s, count=1)
    s = re.sub(r'<html lang="[^"]*"', '<html lang="%s"' % lg, s, count=1)

    # hreflang: четыре языка плюс x-default на английскую
    alts = "".join('<link rel="alternate" hreflang="%s" href="%s">\n' % (k, URL[k])
                   for k in LANGS)
    alts += '<link rel="alternate" hreflang="x-default" href="%s">' % URL["en"]
    s = re.sub(r'(?s)<link rel="alternate" hreflang="en"[^>]*>.*?'
               r'<link rel="alternate" hreflang="x-default"[^>]*>',
               lambda _m: alts, s, count=1)

    s = re.sub(r'(?s)<header class="hero chero".*?</header>', lambda _m: hero(lg), s, count=1)
    # у страницы-образца между шапкой и main стоит полоса фактов, она не нужна
    s = re.sub(r'(?s)<section class="glance">.*?</section>\s*', "", s, count=1)
    s = re.sub(r'(?s)<main id="main".*?</main>', lambda _m: main_html(lg), s, count=1)
    s = s.replace(' aria-current="page"', "")

    # разметка данных образца описывает другую статью
    s = re.sub(r'(?s)<script type="application/ld\+json">.*?</script>\s*', "", s)

    # стили страницы и скрипт формы
    if CSS.strip() not in s:
        s = s.replace("</head>", "<style>%s</style>\n</head>" % CSS, 1)
    tr = FIELDS[lg]
    import json as _json
    t = _json.dumps({"need": tr[12], "sending": tr[11], "done": tr[13],
                     "tail": tr[14], "product": tr[2], "grade": tr[3],
                     "tender": tr[6], "phone": tr[8]}, ensure_ascii=False)
    s = s.replace("</body>", (SCRIPT % t) + "\n</body>", 1)

    s = swap_chrome(s, lg)
    if lg != "en":
        s = absolutize(s)
    return s


def main():
    shell = SHELL.read_text()
    for lg in LANGS:
        p = SITE / OUT[lg]
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(build(lg, shell))
        print("  %s" % OUT[lg])
    print("страниц собрано: %d" % len(LANGS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
