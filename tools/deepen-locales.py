# -*- coding: utf-8 -*-
"""Перенести наполнение /chemicals, /central-asia и /compliance в локали.

Английские версии наполнены инструментами deepen-chemicals.py,
deepen-central-asia.py и deepen-compliance.py. Локальные остались
тонкими: от 77 до 443 слов против 669-1651 у английских. Бриф от
10.11.2026 требует все тексты на четырёх языках, и покупатели, ради
которых он писался, читают по-разному: дистрибьютор в Западной Африке
по-французски, латиноамериканский по-испански, европейский
промышленник по-немецки.

Разметка у локальных страниц та же, что у английских, заголовки
переведены. Поэтому якоря для шагов (s1-s5) общие, а текстовые якоря
берутся из словаря языка.

Перевод смысловой, не дословный: термины закупки в каждом языке свои.
ТДС/ПБ: fiche technique и fiche de données de sécurité, ficha técnica и
ficha de datos de seguridad, Datenblatt и Sicherheitsdatenblatt.
Содержание не меняется: ни одного обещания, которого нет в английской
версии.

Запуск: python3.13 tools/deepen-locales.py
Повторный запуск ничего не меняет.
"""
import json, pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

CSS = """
/* наполнение локальных страниц */
.chem-q{margin:0 0 6px;font-size:1.02rem;font-weight:600;color:var(--ink)}
.chem-a{margin:0 0 22px;line-height:1.62;color:var(--ink-2);max-width:72ch}
.ca-a{margin:0 0 20px;line-height:1.62;color:var(--ink-2);max-width:72ch}
.comp-h{margin:40px 0 10px;font-size:1.14rem;line-height:1.3;color:var(--ink)}
.comp-p{margin:0 0 16px;line-height:1.62;color:var(--ink-2);max-width:72ch}
"""

# =====================================================================
#  ФРАНЦУЗСКИЙ
# =====================================================================
FR = {
"tenders_h": "Pour les appels d’offres",
"details_h": "Identification de la société",
"cta_btn": "Demander une cotation",

"chem_steps": {
 "s1": [
  "Un nom de produit n’est pas une spécification. L’ATMP à cinquante pour "
  "cent en solution et l’ATMP à quatre-vingt-quinze pour cent en solide sont "
  "la même molécule et deux achats différents : fret différent, manutention "
  "différente, prix différent au kilogramme de ce qui agit réellement. Notre "
  "première question n’est jamais la quantité. C’est la teneur en matière "
  "active et la méthode d’essai qui la mesure.",
  "Pour un inhibiteur d’entartrage ou un phosphonate, indiquez la qualité, "
  "la teneur en matière active, la forme et les limites qui comptent pour "
  "vous : chlorures, fer, phosphates libres, couleur. Pour un coagulant, la "
  "teneur en alumine et la basicité, et si le produit doit répondre à une "
  "norme eau potable. Pour une résine échangeuse d’ions, le type et la "
  "matrice, la forme ionique de livraison, la granulométrie et le "
  "coefficient d’uniformité, la rétention d’humidité et la capacité totale. "
  "Pour un tamis moléculaire, le type, la forme et la taille, l’adsorption "
  "statique d’eau, la résistance à l’écrasement et l’attrition.",
  "Indiquez aussi l’usage final, pas seulement le produit. C’est l’usage "
  "qui décide quelle impureté compte. Une résine pour polissage de condensat "
  "et une résine pour récupération de métaux peuvent porter la même "
  "désignation et échouer chacune au service de l’autre.",
 ],
 "s2": [
  "Nous envoyons la fiche technique, la fiche de données de sécurité et un "
  "certificat d’analyse type avant tout prix. Ce ne sont pas des "
  "formalités et ils ne sont pas interchangeables. La fiche technique est ce "
  "que le producteur s’engage à fabriquer. Le certificat d’analyse est ce "
  "qu’un lot a réellement été. Un producteur qui refuse de montrer un "
  "certificat récent avant la commande vous dit quelque chose sur le lot "
  "suivant.",
  "La fiche de données de sécurité doit être au format et dans la langue "
  "exigés à destination, et elle porte les éléments qui décident de "
  "l’expédition : numéro ONU, classe de danger, groupe d’emballage et "
  "étiquetage que le terminal vérifiera. Ces trois lignes décident si le "
  "produit voyage en conteneur standard, si le port l’accepte et ce que "
  "coûte le fret. Une cotation qui arrive sans elles n’est comparable à "
  "rien.",
 ],
 "s3": [
  "Nous cotons sur une base unique : incoterm et port nommés, "
  "conditionnement et poids net, délai entre commande et disponibilité, jeu "
  "de documents qui accompagne la marchandise, et durée de validité du prix. "
  "Ce qui n’est pas dans cette ligne n’est pas dans le prix.",
  "Ensuite, convertissez avant de comparer. Deux offres pour le même "
  "phosphonate, l’une à cinquante pour cent de matière active et l’autre à "
  "soixante, ne sont pas éloignées de quinze pour cent : ramenées à la "
  "matière active, la moins chère en apparence peut être la plus chère. "
  "Ajoutez le conditionnement : fûts facturés avec consigne, sacs que la "
  "destination refuse et qu’il faut reconditionner, GRV non repris. Ajoutez "
  "l’incoterm : un prix FOB et un prix CIF sont deux nombres pour la même "
  "marchandise. Nous ramenons chaque offre à la même base de matière active, "
  "au même conditionnement et au même incoterm, et c’est cette comparaison "
  "que nous vous envoyons, calcul apparent.",
 ],
 "s4": [
  "La production suit la spécification convenue, et chaque lot part avec son "
  "propre certificat d’analyse, daté, portant le numéro de lot inscrit sur "
  "les fûts. Les échantillons témoins restent chez le producteur pendant la "
  "durée de conservation du produit, ce qui est la seule chose qui rende une "
  "réclamation ultérieure possible.",
  "Lorsque la commande le justifie, ou que votre appel d’offres l’exige, un "
  "inspecteur indépendant intervient avant expédition. C’est vous qui "
  "nommez l’organisme, pas nous : SGS, Intertek et Bureau Veritas "
  "travaillent tous aux origines où nous achetons. Le périmètre vous "
  "appartient ; le périmètre utile couvre l’échantillonnage et le scellement, "
  "la quantité et le poids net, l’état et le marquage des emballages, la "
  "propreté du conteneur et le numéro de plomb. Le certificat d’inspection "
  "entre dans le jeu de documents nommé dans le crédit, de sorte que "
  "l’argent se déplace contre la marchandise et pas seulement contre du "
  "papier.",
 ],
 "s5": [
  "Le conditionnement est une décision de coût, et elle se prend avant la "
  "production, pas après. Sacs de vingt-cinq kilogrammes, fûts de deux cent "
  "cinquante kilogrammes, grands récipients pour vrac d’une tonne et, pour "
  "les liquides en volume, conteneur-citerne. Chacun change le poids qui "
  "entre dans un conteneur, la main-d’œuvre à l’arrivée et le prix au "
  "kilogramme rendu. Les palettes en bois voyagent sous la norme "
  "internationale relative aux emballages en bois et portent la marque qui "
  "le prouve.",
  "La température fait partie de la spécification, ce n’est pas un détail de "
  "dernière minute. Plusieurs de ces produits cristallisent, se stratifient "
  "ou gèlent en dessous d’une température donnée, et une expédition d’hiver "
  "vers une destination continentale doit le dire au contrat. La durée de "
  "conservation aussi : c’est la date de fabrication portée au certificat "
  "d’analyse, et non la date d’expédition, qui lance le compte à rebours.",
  "La marchandise voyage par mer, par rail ou par route, sous notre contrat "
  "depuis la sortie d’usine jusqu’au point de livraison convenu, les "
  "documents voyageant avec elle.",
 ],
},
"chem_admis_h": "Ce qui décide de l’admissibilité d’un produit chimique",
"chem_admis": [
 "Un produit chimique est admissible ou il ne l’est pas, et cela se règle "
 "avant la commande plutôt qu’à la frontière. Trois choses en décident.",
 "La première est le régime à destination. Les produits chimiques "
 "industriels sont enregistrés, notifiés ou soumis à licence selon des "
 "règles propres à chaque marché, et l’obligation pèse le plus souvent sur "
 "l’importateur, pas sur nous. Nous vous dirons ce que le producteur peut "
 "documenter ; ce que votre autorité exige de vous reste à vous de le "
 "confirmer, et nous préférons en parler la première semaine plutôt que de "
 "le découvrir à quai.",
 "La deuxième est l’usage. Tout ce qui touche à l’eau potable est jugé "
 "contre une norme eau potable, et le certificat doit nommer la qualité et "
 "l’usine. Une qualité industrielle du même produit, au même titre, n’en est "
 "pas un substitut, et aucun document ne la transforme en tel.",
 "La troisième est le classement de danger. Le numéro ONU, la classe et le "
 "groupe d’emballage décident de l’arrimage, des documents, de l’étiquetage "
 "et souvent de l’acceptation du conteneur par le terminal. Ce sont des "
 "propriétés du produit, décidées à l’usine. Une expédition parfaite sur le "
 "plan commercial et fausse sur une étiquette reste une expédition qui ne "
 "sort pas.",
],
"chem_faq_h": "Ce que les acheteurs demandent avant la première commande",
"chem_faq": [
 ("Pouvez-vous coter un produit qui n’est pas dans le tableau ?",
  "En général oui. Le tableau est ce que nous cotons le plus souvent, pas la "
  "limite de ce que nous achetons. Envoyez le produit, la qualité et la "
  "teneur en matière active, et nous vous dirons si nous pouvons le sourcer "
  "correctement ou non. Si nous ne le pouvons pas, nous le disons plutôt que "
  "d’envoyer une cotation que nous ne pourrions pas tenir."),
 ("Quelle est la plus petite commande que vous traitez ?",
  "Nous travaillons en conteneurs complets, parce que c’est là que "
  "l’économie du dossier tient. Une première commande, c’est normalement un "
  "ou deux conteneurs à des conditions pleinement commerciales. En dessous, "
  "le fret au kilogramme monte plus vite que toute économie sur la "
  "marchandise, et nous vous vendrions une opération moins bonne que ce que "
  "vous trouvez localement."),
 ("Fournissez-vous une qualité eau potable ?",
  "Lorsque le producteur détient la certification correspondante et peut la "
  "présenter par usine et par qualité, oui, et le certificat voyage avec la "
  "marchandise. Lorsqu’il ne détient qu’une qualité industrielle, nous le "
  "disons et cotons la qualité industrielle pour ce qu’elle est."),
 ("Pouvons-nous désigner l’organisme d’inspection ?",
  "Oui, et nous le préférons. Vous nommez l’organisme et le périmètre, "
  "l’inspection a lieu avant expédition, et le certificat entre dans le jeu "
  "de documents nommé dans le crédit. Un inspecteur que nous aurions choisi "
  "nous-mêmes vous prouverait moins de choses."),
 ("Pouvez-vous répondre à notre appel d’offres ?",
  "Oui. Pour un appel d’offres nous fournissons la lettre d’autorisation du "
  "fabricant, les certificats d’origine et de qualité et les documents "
  "produits que votre commission exige. Envoyez le numéro et la date limite "
  "avec la demande, le dossier sera monté pour cette date."),
 ("Comment sommes-nous protégés si la marchandise n’est pas conforme ?",
  "Par la structure plutôt que par une promesse. La spécification est "
  "convenue par écrit avant la production, chaque lot porte son certificat "
  "d’analyse, un inspecteur que vous nommez intervient avant expédition, et "
  "le paiement se fait contre le jeu de documents nommé dans le crédit. "
  "Chacun de ces points est un endroit où une marchandise non conforme "
  "s’arrête au lieu d’arriver."),
],

"ca_steps": [
 ("s1", "Être enclavé change l’arithmétique", [
  "Sur une ligne maritime, le fret est une ligne de la cotation. Ici, il est "
  "l’essentiel de la cotation. Il n’y a pas de port de déchargement à "
  "destination : chaque tonne finit son trajet sur rail ou sur camion, et "
  "sur des marchandises lourdes par rapport à leur valeur, ce que sont les "
  "produits chimiques et les matériaux industriels, c’est le trajet terrestre "
  "qui décide si l’affaire existe.",
  "Cela change ce que doit contenir une cotation. Un taux de fret maritime "
  "ne vous apprend presque rien ici. Ce qui compte, c’est le tarif "
  "ferroviaire du wagon ou du conteneur, l’attente au poste frontière, le "
  "coût du transfert entre deux réseaux ferroviaires, et qui paie le "
  "conteneur pendant qu’il attend. Nous chiffrons ces quatre postes en "
  "lignes nommées plutôt que de les fondre dans un nombre unique que vous ne "
  "pourriez pas interroger.",
 ]),
 ("s2", "L’écartement change à la frontière", [
  "Les chemins de fer chinois circulent à l’écartement standard. Le "
  "Kazakhstan et ses voisins circulent à l’écartement large utilisé dans la "
  "région. Les deux ne se rejoignent pas : à Khorgos et à Dostyk, chaque "
  "chargement change de wagon ou le wagon change de bogies. Ce n’est pas une "
  "formalité. C’est une opération physique, avec un coût, une file d’attente "
  "et un mode de défaillance.",
  "Le mode de défaillance compte plus que le coût. Les liquides en fûts et "
  "les solides en sacs manipulés en vrac sur un terminal de transbordement "
  "arrivent avec des sacs éventrés, des fûts enfoncés et un manquant. Le "
  "conteneur l’évite : la caisse est transférée en un seul mouvement et la "
  "marchandise à l’intérieur n’est jamais touchée. C’est pourquoi nous "
  "cotons en conteneur partout où le produit et le volume le permettent, et "
  "pourquoi nous le disons quand un produit ne le permet pas.",
 ]),
 ("s3", "La traversée de la Caspienne est un risque d’horaire", [
  "Pour la marchandise qui traverse la Caspienne, l’eau est la partie "
  "courte. Aktaou et Kouryk sont sur la rive est, Alat sur la rive ouest, et "
  "la traversée elle-même se compte en heures. L’attente, non. Les départs "
  "sont attribués plutôt que programmés comme le ferait une compagnie "
  "maritime, la météo ferme les ports, et un créneau manqué se compte en "
  "jours.",
  "Nous ne cotons donc pas un délai de transit qui suppose que toutes les "
  "correspondances tiennent. Nous donnons une fourchette, nous disons ce qui "
  "peut la déplacer, et nous vous annonçons le coût du retard au lieu de le "
  "découvrir avec vous plus tard. Si une date est réellement ferme chez "
  "vous, dites-le à la demande : cela change l’itinéraire que nous "
  "recommandons et parfois le conditionnement.",
 ]),
 ("s4", "Ce que demande la douane, pays par pays", [
  "Le jeu commercial est partout le même : facture, liste de colisage, "
  "certificat d’origine et document de transport. Pour les produits "
  "chimiques, deux pièces supplémentaires voyagent avec la marchandise et "
  "sont lues attentivement : la fiche de données de sécurité, avec le numéro "
  "ONU, la classe de danger et le groupe d’emballage, et le certificat "
  "d’analyse du lot réellement présent dans les fûts.",
  "C’est sur la conformité que les pays diffèrent. Au Kazakhstan et au "
  "Kirghizistan, les marchandises entrant dans le champ des règlements "
  "techniques de l’union douanière portent la marque de conformité, et la "
  "déclaration ou le certificat est délivré avant le départ, pas après "
  "l’arrivée. L’Ouzbékistan, le Turkménistan et l’Azerbaïdjan appliquent "
  "chacun leur propre régime. Dans la plupart d’entre eux, l’obligation "
  "d’enregistrement pèse sur l’importateur et non sur le vendeur, et c’est "
  "précisément pour cela que nous en parlons la première semaine : nous vous "
  "dirons ce que le producteur peut documenter, et ce qui vous revient "
  "restera à vous de le confirmer.",
  "La langue fait partie du dossier. Un document que le bureau ne peut pas "
  "lire est un document manquant, et une traduction faite à la frontière "
  "coûte plus cher qu’une traduction faite à l’usine.",
 ]),
 ("s5", "L’hiver fait partie de la spécification", [
  "Le climat est continental et la marchandise y reste des semaines. Les "
  "wagons ne sont pas chauffés et les conteneurs ne sont pas isolés. "
  "Plusieurs des produits qui empruntent ce corridor cristallisent, se "
  "stratifient ou gèlent en dessous d’une température donnée, et un liquide "
  "en fût qui a gelé n’est que rarement le même produit ensuite.",
  "La réponse n’est pas une note dans un courriel. Le contrat indique la "
  "température la plus basse que la marchandise rencontrera, le "
  "conditionnement est choisi pour elle, et lorsque le produit ne supporte "
  "réellement pas la saison, la réponse honnête est de l’expédier à une "
  "autre. Une expédition libérée en novembre traverse en plein hiver, et "
  "cela se décide à la commande, pas à la frontière.",
 ]),
],
"ca_tender_h": "Les appels d’offres dans la région",
"ca_tender": [
 "Les compagnies nationales de pétrole, de gaz, d’électricité, de mines et "
 "d’eau de ces pays achètent par appel d’offres, et c’est le dossier qui "
 "décide de l’issue plus souvent que le prix.",
 "Pour un appel d’offres, nous fournissons la lettre d’autorisation du "
 "fabricant nommant l’appel d’offres, les certificats d’origine et de "
 "qualité, les documents produits que votre commission énumère, et les "
 "conditions commerciales dans la forme demandée. Lorsque l’appel d’offres "
 "exige une garantie de soumission, un représentant local ou un "
 "enregistrement que seul le soumissionnaire peut détenir, nous le disons au "
 "début et non au dépôt. Envoyez le numéro et la date de clôture avec la "
 "demande, le dossier sera monté pour cette date.",
],
"ca_faq_h": "Ce que les acheteurs demandent sur ce corridor",
"ca_faq_lede": ("Les questions qui décident si une expédition sur ce corridor "
                "fonctionne, répondues comme nous y répondons au premier "
                "appel."),
"ca_faq": [
 ("Combien de temps faut-il de la Chine au Kazakhstan ?",
  "Cela dépend du poste frontière et du créneau, et quiconque répond par un "
  "nombre unique vous donne le meilleur cas. Nous donnons une fourchette "
  "pour l’expédition concernée, nous disons ce qui peut la déplacer, et nous "
  "l’actualisons quand le wagon est attribué. Un chiffre qui ne tient que si "
  "rien ne va de travers n’est pas un chiffre sur lequel planifier."),
 ("Livrez-vous jusqu’à notre site ou seulement à la frontière ?",
  "Jusqu’au site là où la destination le permet, sous un incoterm rendu, le "
  "trajet intérieur chiffré en ligne séparée pour que vous voyiez ce qu’il "
  "coûte. Là où seul l’importateur peut dédouaner, nous livrons au point "
  "convenu avant dédouanement et remettons le jeu de documents complet."),
 ("Qui s’occupe du dédouanement ?",
  "En général l’importateur, parce que dans la plupart de ces pays "
  "l’enregistrement et la conformité pèsent sur l’acheteur et ne peuvent pas "
  "être transférés à un vendeur étranger. Nous fournissons les documents "
  "qu’exige le dédouanement, dans la langue exigée, et nous vérifions le jeu "
  "contre la liste de la destination avant le départ."),
 ("Transportez-vous des produits chimiques dangereux sur ce corridor ?",
  "Là où le classement le permet et où les transporteurs l’acceptent. Le "
  "numéro ONU, la classe et le groupe d’emballage décident du "
  "conditionnement, de l’étiquetage, du wagon et des documents, et ils sont "
  "arrêtés avant la production. Là où un produit ne peut pas circuler en "
  "conformité sur cette route, nous le disons et proposons celle où il le "
  "peut."),
 ("Quelles conditions de paiement pratiquez-vous ?",
  "Un crédit documentaire payable à vue contre le jeu de documents, qui est "
  "la structure que nous préférons avec un acheteur avec lequel nous n’avons "
  "pas d’historique. Le jeu comprend un certificat d’inspection avant "
  "expédition délivré par un organisme que vous nommez, de sorte que "
  "l’argent se déplace contre la marchandise et pas seulement contre du "
  "papier."),
 ("Nous ne sommes pas une compagnie nationale. Coterez-vous quand même ?",
  "Oui. Les distributeurs, les entreprises et les exploitants achètent aussi "
  "sur ce corridor. Le volume qui fait tenir l’économie du dossier est le "
  "conteneur complet ; en dessous, le trajet terrestre à la tonne monte plus "
  "vite que toute économie sur la marchandise, et nous vous le dirons plutôt "
  "que de le coter."),
],
"ca_cta_h": "Envoyez une spécification. Recevez un prix rendu.",
"ca_cta": ("Le produit, la qualité, la quantité et le point de livraison "
           "suffisent pour commencer. Pas de compte, pas d’inscription, pas "
           "de frais."),

"comp": [
 ("Qui nous contrôlons, et quand", [
  "Avant chaque cotation, avant chaque contrat et avant chaque paiement, "
  "nous contrôlons la contrepartie par sa raison sociale et par tout nom "
  "commercial qu’elle utilise, ses propriétaires et toute personne qui la "
  "contrôle, l’utilisateur final de la marchandise lorsqu’il n’est pas la "
  "contrepartie, le destinataire, la partie à notifier et la destination "
  "finale, ainsi que le navire, le transporteur et la banque lorsqu’ils nous "
  "sont connus.",
  "Le contrôle est repris avant le paiement, il n’est pas reporté depuis la "
  "cotation. Les structures de propriété et les listes changent entre une "
  "cotation et une expédition, et un résultat propre obtenu en première "
  "semaine ne prouve rien sur la dixième.",
 ]),
 ("Les listes sur lesquelles nous contrôlons", [
  "La liste des ressortissants spécialement désignés et des personnes "
  "bloquées et la liste consolidée des sanctions de l’OFAC du Trésor "
  "américain ; les listes des personnes refusées, des entités et des entités "
  "non vérifiées du BIS du Département du commerce américain ; la liste "
  "consolidée des sanctions du Conseil de sécurité des Nations unies ; la "
  "liste consolidée de l’Union européenne ; et la liste des sanctions du "
  "Royaume-Uni.",
  "La propriété est appréciée selon la règle des cinquante pour cent. Une "
  "entité détenue, directement ou indirectement, à cinquante pour cent ou "
  "plus au total par une ou plusieurs personnes bloquées est elle-même "
  "traitée comme bloquée, qu’elle figure ou non nommément sur une liste.",
 ]),
 ("Ce que nous ne ferons pas", [
  "Nous ne traitons pas avec des personnes ou des entités visées par des "
  "sanctions, ni avec des territoires sous sanctions globales.",
  "Nous ne déclarons jamais faussement l’origine, la destination ou "
  "l’utilisateur final d’une marchandise, dans un document, dans une "
  "déclaration ou dans une correspondance, et nous n’acceptons pas "
  "d’instruction en ce sens.",
  "Nous ne structurons pas une opération, un itinéraire ou un paiement pour "
  "éviter l’application d’une règle de sanctions ou de contrôle des "
  "exportations, et nous n’aidons aucune autre partie à le faire.",
  "Nous ne fournissons pas de marchandise lorsque nous savons, ou avons des "
  "raisons de croire, qu’elle est destinée à un usage final interdit, y "
  "compris un usage militaire, nucléaire, de missiles ou d’armes chimiques "
  "et biologiques lorsque cet usage est contrôlé.",
 ]),
 ("Ce qui arrête une opération", [
  "Une opération est arrêtée et réexaminée avant de se poursuivre lorsque "
  "l’utilisateur final refuse d’être nommé ou que l’usage déclaré ne "
  "correspond ni à la marchandise ni à la quantité ; lorsque l’adresse de "
  "livraison, le destinataire ou l’itinéraire change après l’accord, ou que "
  "l’itinéraire n’a pas de sens commercial ; lorsque le paiement est proposé "
  "par un tiers, depuis une juridiction sans rapport, ou d’une manière qui "
  "masque son origine ; lorsque la contrepartie demande que les documents "
  "montrent autre chose que les faits ; ou lorsque la contrepartie, ses "
  "propriétaires ou la destination sont liés à un territoire sous sanctions.",
  "Chacun de ces points se résout sur pièces ou l’opération est refusée. Une "
  "assurance verbale n’en résout aucun. Lorsqu’une opération ne peut pas "
  "être mise en conformité, nous la refusons, et aucun montant de commande "
  "ne change cette réponse.",
 ]),
 ("Conservation", [
  "Les résultats de contrôle, les éléments d’identité obtenus, les "
  "informations sur l’utilisateur final et les motifs de toute décision de "
  "refus sont conservés avec le dossier de l’opération pendant au moins cinq "
  "ans à compter de la date de l’opération, conformément aux durées de "
  "conservation prévues par la réglementation américaine sur les sanctions "
  "et le contrôle des exportations.",
  "Toute préoccupation relative à une opération, à une contrepartie ou à "
  "cette politique peut être adressée directement au membre à "
  "info@ispgroupgc.com. Une préoccupation exprimée de bonne foi n’a aucune "
  "conséquence défavorable pour la personne qui l’exprime.",
 ]),
],
}

# =====================================================================
#  ИСПАНСКИЙ
# =====================================================================
ES = {
"tenders_h": "Para licitaciones",
"details_h": "Datos de la empresa",
"cta_btn": "Solicitar cotización",

"chem_steps": {
 "s1": [
  "El nombre de un producto no es una especificación. El ATMP al cincuenta "
  "por ciento en solución y el ATMP al noventa y cinco por ciento en sólido "
  "son la misma molécula y dos compras distintas: distinto flete, distinta "
  "manipulación, distinto precio por kilogramo de lo que realmente actúa. "
  "Nuestra primera pregunta nunca es la cantidad. Es el contenido de materia "
  "activa y el método de ensayo con el que se mide.",
  "Para un inhibidor de incrustaciones o un fosfonato, indique la calidad, "
  "el contenido activo, la forma y los límites que le importan: cloruros, "
  "hierro, fosfato libre, color. Para un coagulante, el contenido de alúmina "
  "y la basicidad, y si debe cumplir una norma de agua potable. Para una "
  "resina de intercambio iónico, el tipo y la matriz, la forma iónica de "
  "entrega, el tamaño de perla y el coeficiente de uniformidad, la retención "
  "de humedad y la capacidad total. Para un tamiz molecular, el tipo, la "
  "forma y el tamaño, la adsorción estática de agua, la resistencia al "
  "aplastamiento y la atrición.",
  "Indique también el uso final, no sólo el producto. El uso decide qué "
  "impureza importa. Una resina para pulido de condensado y una resina para "
  "recuperación de metales pueden llevar la misma designación y fallar cada "
  "una en el servicio de la otra.",
 ],
 "s2": [
  "Enviamos la ficha técnica, la ficha de datos de seguridad y un "
  "certificado de análisis de muestra antes de cualquier precio. No son "
  "formalidades y no son intercambiables. La ficha técnica es lo que el "
  "fabricante se compromete a producir. El certificado de análisis es lo que "
  "un lote realmente fue. Un fabricante que no quiere mostrar un certificado "
  "reciente antes del pedido le está diciendo algo sobre el siguiente.",
  "La ficha de datos de seguridad debe estar en el formato y el idioma que "
  "exige el destino, y lleva los datos que deciden el embarque: número ONU, "
  "clase de peligro, grupo de embalaje y el etiquetado que la terminal va a "
  "mirar. Esas tres líneas deciden si el producto viaja en contenedor "
  "estándar, si el puerto lo acepta y cuánto cuesta el flete. Una cotización "
  "que llega sin ellas todavía no es comparable con nada.",
 ],
 "s3": [
  "Cotizamos sobre una sola base: incoterm y puerto nombrados, envase y peso "
  "neto, plazo desde el pedido hasta la disponibilidad, juego de documentos "
  "que acompaña a la mercancía y cuánto tiempo se mantiene el precio. Lo que "
  "no está en esa línea no está en el precio.",
  "Después convierta antes de comparar. Dos ofertas del mismo fosfonato, una "
  "al cincuenta por ciento de activo y otra al sesenta, no están a quince "
  "por ciento de distancia: llevadas a base activa, la que parecía más "
  "barata puede ser la más cara. Sume el envase: tambores facturados con "
  "depósito, sacos que el destino no acepta y hay que reenvasar, un IBC que "
  "no se devuelve. Sume el incoterm: un precio FOB y un precio CIF son dos "
  "números para la misma carga. Llevamos cada oferta a la misma base activa, "
  "el mismo envase y el mismo incoterm, y esa comparación es la que le "
  "enviamos, con la aritmética a la vista.",
 ],
 "s4": [
  "La producción sigue la especificación acordada, y cada lote sale con su "
  "propio certificado de análisis, fechado y con el número de lote que "
  "aparece en los tambores. Las muestras testigo quedan en el fabricante "
  "durante la vida útil del producto, que es lo único que hace posible un "
  "reclamo posterior.",
  "Cuando el pedido lo justifica, o su licitación lo exige, un inspector "
  "independiente interviene antes del embarque. Usted nombra la entidad, no "
  "nosotros: SGS, Intertek y Bureau Veritas trabajan en los orígenes donde "
  "compramos. El alcance lo fija usted, y el alcance útil cubre el muestreo "
  "y el precintado, la cantidad y el peso neto, el estado y el marcado del "
  "envase, la limpieza del contenedor y el número de precinto. El "
  "certificado de inspección entra en el juego de documentos nombrado en el "
  "crédito, de modo que el dinero se mueve contra la mercancía y no sólo "
  "contra el papel.",
 ],
 "s5": [
  "El envase es una decisión de costo y se toma antes de producir, no "
  "después. Sacos de veinticinco kilogramos, tambores de doscientos cincuenta "
  "kilogramos, contenedores intermedios de una tonelada y, para líquidos en "
  "volumen, un contenedor cisterna. Cada uno cambia el peso que entra en un "
  "contenedor, la mano de obra en destino y el precio por kilogramo puesto. "
  "Los palés de madera viajan bajo la norma internacional de embalaje de "
  "madera y llevan la marca que lo acredita.",
  "La temperatura es parte de la especificación, no un detalle de última "
  "hora. Varios de estos productos cristalizan, se estratifican o se "
  "congelan por debajo de una temperatura determinada, y un embarque de "
  "invierno hacia un destino continental tiene que decirlo en el contrato. "
  "La vida útil también: el reloj corre desde la fecha de fabricación que "
  "figura en el certificado de análisis, no desde la fecha de embarque.",
  "La mercancía viaja por mar, por ferrocarril o por carretera, bajo nuestro "
  "contrato desde la puerta de la planta hasta el punto de entrega acordado, "
  "con los documentos viajando con ella.",
 ],
},
"chem_admis_h": "Qué decide si un producto químico es admisible",
"chem_admis": [
 "Un producto químico es admisible o no lo es, y eso se resuelve antes del "
 "pedido y no en la frontera. Tres cosas lo deciden.",
 "La primera es el régimen en destino. Los productos químicos industriales "
 "se registran, se notifican o se licencian bajo reglas propias de cada "
 "mercado, y la obligación suele recaer en el importador y no en nosotros. "
 "Le diremos qué puede documentar el fabricante; lo que su autoridad le "
 "exija a usted le corresponde confirmarlo, y preferimos plantearlo en la "
 "primera semana antes que encontrarlo en el muelle.",
 "La segunda es el uso. Todo lo que toca agua potable se juzga contra una "
 "norma de agua potable, y el certificado debe nombrar la calidad y la "
 "planta. Una calidad industrial del mismo producto, con el mismo ensayo, no "
 "la sustituye, y ningún papel la convierte en eso.",
 "La tercera es la clasificación de peligro. El número ONU, la clase y el "
 "grupo de embalaje deciden la estiba, los documentos, el etiquetado y a "
 "menudo si la terminal acepta el contenedor. Son propiedades del producto, "
 "decididas en la planta. Un embarque correcto en lo comercial y equivocado "
 "en una etiqueta sigue siendo un embarque que no despacha.",
],
"chem_faq_h": "Lo que preguntan los compradores antes del primer pedido",
"chem_faq": [
 ("¿Pueden cotizar un producto que no está en la tabla?",
  "Por lo general sí. La tabla es lo que cotizamos con más frecuencia, no el "
  "límite de lo que compramos. Envíe el producto, la calidad y el contenido "
  "activo y le diremos si podemos abastecerlo correctamente o no. Si no "
  "podemos, se lo decimos en lugar de enviarle una cotización que no "
  "podríamos sostener."),
 ("¿Cuál es el pedido más pequeño que atienden?",
  "Trabajamos en contenedores completos, porque ahí es donde la economía se "
  "sostiene. Un primer pedido normalmente es uno o dos contenedores en "
  "condiciones plenamente comerciales. Por debajo de eso el flete por "
  "kilogramo sube más rápido que cualquier ahorro en la mercancía, y le "
  "estaríamos vendiendo una operación peor que la que consigue localmente."),
 ("¿Suministran calidad para agua potable?",
  "Cuando el fabricante tiene la certificación correspondiente y puede "
  "mostrarla por planta y por calidad, sí, y el certificado viaja con la "
  "mercancía. Cuando sólo tiene calidad industrial, lo decimos y cotizamos "
  "la calidad industrial por lo que es."),
 ("¿Podemos nombrar nosotros la entidad de inspección?",
  "Sí, y lo preferimos. Usted nombra la entidad y el alcance, la inspección "
  "ocurre antes del embarque y el certificado entra en el juego de "
  "documentos nombrado en el crédito. Un inspector elegido por nosotros le "
  "probaría menos."),
 ("¿Pueden presentarse a nuestra licitación?",
  "Sí. Para una licitación aportamos la carta de autorización del "
  "fabricante, los certificados de origen y calidad y los documentos de "
  "producto que exija su comité. Envíe el número y la fecha de cierre junto "
  "con la consulta y el expediente se arma para esa fecha."),
 ("¿Cómo estamos protegidos si la mercancía no es la correcta?",
  "Por la estructura, no por una promesa. La especificación se acuerda por "
  "escrito antes de producir, cada lote lleva su certificado de análisis, un "
  "inspector que usted nombra interviene antes del embarque y el pago se "
  "hace contra el juego de documentos nombrado en el crédito. Cada uno de "
  "esos puntos es un lugar donde una partida equivocada se detiene en lugar "
  "de llegar."),
],

"ca_steps": [
 ("s1", "Estar sin salida al mar cambia la aritmética", [
  "En una ruta marítima el flete es una línea de la cotización. Aquí es casi "
  "toda la cotización. No hay puerto de descarga en destino, así que cada "
  "tonelada termina su viaje sobre rieles o sobre un camión, y en mercancía "
  "pesada en relación con su valor, que es lo que son los productos químicos "
  "y los materiales industriales, el tramo terrestre decide si el negocio "
  "existe.",
  "Eso cambia lo que una cotización tiene que contener. Una tarifa de flete "
  "marítimo aquí no dice casi nada. Lo que importa es la tarifa ferroviaria "
  "del vagón o del contenedor, la espera en el paso fronterizo, el costo de "
  "mover la mercancía entre dos sistemas ferroviarios y quién paga el "
  "contenedor mientras espera. Cotizamos esos cuatro como líneas con nombre "
  "en lugar de fundirlos en una cifra única que usted no podría interrogar.",
 ]),
 ("s2", "El ancho de vía cambia en la frontera", [
  "Los ferrocarriles chinos circulan en trocha estándar. Kazajistán y sus "
  "vecinos circulan en la trocha ancha que se usa en la región. Las dos no "
  "se encuentran, así que en Khorgos y en Dostyk cada carga cambia de vagón "
  "o el vagón cambia de bogies. No es un trámite. Es una operación física, "
  "con un costo, una cola y un modo de falla.",
  "El modo de falla importa más que el costo. Los líquidos en tambores y los "
  "sólidos en sacos manipulados sueltos en una terminal de transbordo llegan "
  "con sacos rotos, tambores abollados y faltante. El contenedor lo evita: "
  "la caja se transfiere en un solo movimiento y la mercancía de adentro no "
  "se toca nunca. Por eso cotizamos en contenedor siempre que el producto y "
  "el volumen lo permiten, y por eso lo decimos cuando un producto no lo "
  "permite.",
 ]),
 ("s3", "El cruce del Caspio es un riesgo de calendario", [
  "Para la carga que cruza el Caspio el agua es la parte corta. Aktau y "
  "Kuryk están en la orilla este, Alat en la oeste, y la travesía en sí se "
  "mide en horas. La espera no. Las salidas se asignan más que se programan "
  "como lo hace una naviera, el clima cierra los puertos y un cupo perdido "
  "se mide en días.",
  "Por eso no cotizamos un tiempo de tránsito que supone que todas las "
  "conexiones se cumplen. Damos una ventana, decimos qué puede moverla y le "
  "anticipamos el costo de la demora en lugar de descubrirlo con usted "
  "después. Si una fecha es realmente firme de su lado, dígalo en la "
  "consulta: cambia la ruta que recomendamos y a veces cambia el envase.",
 ]),
 ("s4", "Qué pide la aduana, país por país", [
  "El juego comercial es el mismo en todas partes: factura, lista de "
  "empaque, certificado de origen y documento de transporte. Para productos "
  "químicos viajan dos piezas más con la mercancía y se leen con atención: "
  "la ficha de datos de seguridad, con el número ONU, la clase de peligro y "
  "el grupo de embalaje, y el certificado de análisis del lote que "
  "efectivamente está en los tambores.",
  "La conformidad es donde los países difieren. En Kazajistán y Kirguistán "
  "la mercancía que entra en el alcance de los reglamentos técnicos de la "
  "unión aduanera lleva la marca de conformidad, y la declaración o el "
  "certificado se emite antes de que la mercancía salga, no después de que "
  "llegue. Uzbekistán, Turkmenistán y Azerbaiyán aplican cada uno su propio "
  "régimen. En la mayoría de ellos la obligación de registro recae en el "
  "importador y no en el vendedor, y precisamente por eso lo planteamos la "
  "primera semana: le diremos qué puede documentar el fabricante, y lo que "
  "le corresponde a usted queda a usted confirmarlo.",
  "El idioma es parte del expediente. Un documento que la oficina no puede "
  "leer es un documento que falta, y una traducción hecha en la frontera "
  "cuesta más que una hecha en la planta.",
 ]),
 ("s5", "El invierno es parte de la especificación", [
  "El clima es continental y la carga pasa semanas dentro de él. Los vagones "
  "no son calefaccionados y los contenedores no son aislados. Varios de los "
  "productos que bajan por este corredor cristalizan, se estratifican o se "
  "congelan por debajo de una temperatura determinada, y un líquido en "
  "tambor que se ha congelado rara vez es el mismo producto después.",
  "La respuesta no es una nota en un correo. El contrato indica la "
  "temperatura más baja que la carga va a encontrar, el envase se elige para "
  "ella, y cuando el producto realmente no soporta la estación, la respuesta "
  "honesta es embarcarlo en otra. Un embarque liberado en noviembre cruza en "
  "pleno invierno, y eso se decide en el pedido, no en la frontera.",
 ]),
],
"ca_tender_h": "Licitaciones en la región",
"ca_tender": [
 "Las compañías nacionales de petróleo, gas, electricidad, minería y agua de "
 "estos países compran por licitación, y el expediente decide el resultado "
 "con más frecuencia que el precio.",
 "Para una licitación aportamos la carta de autorización del fabricante que "
 "nombra la licitación, los certificados de origen y calidad, los documentos "
 "de producto que su comité enumere y las condiciones comerciales en la "
 "forma en que se piden. Cuando la licitación exige una garantía de oferta, "
 "un representante local o un registro que sólo el oferente puede tener, lo "
 "decimos al principio y no en la presentación. Envíe el número y la fecha "
 "de cierre con la consulta y el expediente se arma para esa fecha.",
],
"ca_faq_h": "Lo que preguntan los compradores de este corredor",
"ca_faq_lede": ("Las preguntas que deciden si un embarque por este corredor "
                "funciona, respondidas como las respondemos en la primera "
                "llamada."),
"ca_faq": [
 ("¿Cuánto tarda desde China hasta Kazajistán?",
  "Depende del paso y del cupo, y quien responda con un solo número está "
  "cotizando el mejor caso. Damos una ventana para el embarque concreto, "
  "decimos qué puede moverla y la actualizamos cuando se asigna el vagón. "
  "Una cifra que sólo se cumple si nada sale mal no es una cifra con la que "
  "se pueda planificar."),
 ("¿Entregan en nuestra planta o sólo en la frontera?",
  "En la planta donde el destino lo permite, bajo un incoterm de entrega, "
  "con el tramo interior cotizado como línea propia para que vea cuánto "
  "cuesta. Donde sólo el importador puede despachar, entregamos en el punto "
  "acordado antes del despacho y entregamos el juego completo de documentos."),
 ("¿Quién se ocupa del despacho aduanero?",
  "Normalmente el importador, porque en la mayoría de estos países el "
  "registro y la conformidad recaen en el comprador y no pueden transferirse "
  "a un vendedor extranjero. Nosotros aportamos los documentos que el "
  "despacho necesita, en el idioma que necesita, y verificamos el juego "
  "contra la lista del destino antes de que la mercancía salga."),
 ("¿Mueven productos químicos peligrosos por este corredor?",
  "Donde la clasificación lo permite y los transportistas lo aceptan. El "
  "número ONU, la clase y el grupo de embalaje deciden el envase, el "
  "etiquetado, el vagón y los documentos, y se resuelven antes de producir. "
  "Donde un producto no puede moverse en conformidad por esta ruta lo "
  "decimos y proponemos la ruta por la que sí puede."),
 ("¿Con qué condiciones de pago trabajan?",
  "Un crédito documentario pagadero a la vista contra el juego de "
  "documentos, que es la estructura que preferimos con un comprador con el "
  "que no tenemos historial. El juego incluye un certificado de inspección "
  "previa al embarque de una entidad que usted nombra, de modo que el dinero "
  "se mueve contra la mercancía y no sólo contra el papel."),
 ("No somos una compañía nacional. ¿Cotizarán igual?",
  "Sí. Distribuidores, contratistas y operadores de planta también compran "
  "en este corredor. El volumen que hace que la economía funcione es el "
  "contenedor completo; por debajo, el tramo terrestre por tonelada sube más "
  "rápido que cualquier ahorro en la mercancía, y se lo diremos en lugar de "
  "cotizarlo."),
],
"ca_cta_h": "Envíe una especificación. Reciba un precio puesto.",
"ca_cta": ("Producto, calidad, cantidad y punto de entrega bastan para "
           "empezar. Sin cuenta, sin registro, sin cargo."),

"comp": [
 ("A quién verificamos, y cuándo", [
  "Antes de cada cotización, antes de cada contrato y antes de cada pago "
  "verificamos a la contraparte por su razón social y por cualquier nombre "
  "comercial que use, a sus propietarios y a cualquier persona que la "
  "controle, al usuario final de la mercancía cuando no es la contraparte, "
  "al consignatario, a la parte a notificar y al destino final, y al buque, "
  "al transportista y al banco cuando los conocemos.",
  "La verificación se repite antes del pago, no se arrastra desde la "
  "cotización. La propiedad y las listas cambian entre una cotización y un "
  "embarque, y un resultado limpio obtenido en la primera semana no prueba "
  "nada sobre la décima.",
 ]),
 ("Las listas contra las que verificamos", [
  "La lista de nacionales especialmente designados y personas bloqueadas y "
  "la lista consolidada de sanciones de la OFAC del Tesoro de los Estados "
  "Unidos; las listas de personas denegadas, de entidades y de entidades no "
  "verificadas del BIS del Departamento de Comercio; la lista consolidada de "
  "sanciones del Consejo de Seguridad de las Naciones Unidas; la lista "
  "consolidada de la Unión Europea; y la lista de sanciones del Reino Unido.",
  "La propiedad se evalúa según la regla del cincuenta por ciento. Una "
  "entidad cuya propiedad, directa o indirecta, corresponda en un cincuenta "
  "por ciento o más en conjunto a una o varias personas bloqueadas se trata "
  "ella misma como bloqueada, figure o no nominalmente en una lista.",
 ]),
 ("Lo que no haremos", [
  "No operamos con personas o entidades sujetas a sanciones, ni con "
  "territorios bajo sanciones integrales.",
  "Nunca declaramos falsamente el origen, el destino o el usuario final de "
  "una mercancía, ni en un documento, ni en una declaración, ni en "
  "correspondencia, y no aceptamos instrucciones en ese sentido.",
  "No estructuramos una operación, una ruta o un pago para evitar la "
  "aplicación de una norma de sanciones o de control de exportaciones, ni "
  "ayudamos a ninguna otra parte a hacerlo.",
  "No suministramos mercancía cuando sabemos, o tenemos motivos para creer, "
  "que está destinada a un uso final prohibido, incluido un uso militar, "
  "nuclear, de misiles o de armas químicas y biológicas cuando ese uso está "
  "controlado.",
 ]),
 ("Qué detiene una operación", [
  "Una operación se detiene y se revisa antes de continuar cuando el usuario "
  "final no quiere ser nombrado o el uso declarado no encaja con la "
  "mercancía ni con la cantidad; cuando la dirección de entrega, el "
  "consignatario o la ruta cambian después de acordado el contrato, o la "
  "ruta no tiene sentido comercial; cuando el pago se ofrece desde un "
  "tercero, desde una jurisdicción sin relación, o de una manera que oculta "
  "su origen; cuando la contraparte pide que los documentos muestren algo "
  "distinto de los hechos; o cuando la contraparte, sus propietarios o el "
  "destino están vinculados a un territorio bajo sanciones.",
  "Cada uno de esos puntos se resuelve con pruebas o la operación se "
  "rechaza. Una garantía verbal no resuelve ninguno. Cuando una operación no "
  "puede hacerse conforme, la rechazamos, y ningún importe de pedido cambia "
  "esa respuesta.",
 ]),
 ("Conservación de registros", [
  "Los resultados de verificación, las pruebas de identidad obtenidas, la "
  "información sobre el usuario final y los motivos de cualquier decisión de "
  "rechazo se conservan con el expediente de la operación durante al menos "
  "cinco años desde la fecha de la operación, conforme a los plazos de "
  "conservación de la normativa estadounidense de sanciones y control de "
  "exportaciones.",
  "Cualquier inquietud sobre una operación, una contraparte o esta política "
  "puede plantearse directamente al miembro en info@ispgroupgc.com. Una "
  "inquietud planteada de buena fe no tiene consecuencia adversa para quien "
  "la plantea.",
 ]),
],
}


# =====================================================================
#  НЕМЕЦКИЙ
# =====================================================================
DE = {
"tenders_h": "Für Ausschreibungen",
"details_h": "Unternehmensangaben",
"cta_btn": "Angebot anfordern",

"chem_steps": {
 "s1": [
  "Ein Produktname ist keine Spezifikation. ATMP zu fünfzig Prozent in "
  "Lösung und ATMP zu fünfundneunzig Prozent als Feststoff sind dasselbe "
  "Molekül und zwei verschiedene Einkäufe: andere Fracht, andere Handhabung, "
  "anderer Preis je Kilogramm des Stoffes, der tatsächlich wirkt. Unsere "
  "erste Frage ist nie die Menge. Es ist der Wirkstoffgehalt und die "
  "Prüfmethode, mit der er bestimmt wird.",
  "Für einen Scale-Inhibitor oder ein Phosphonat nennen Sie die Qualität, "
  "den Wirkstoffgehalt, die Form und die Grenzwerte, auf die es Ihnen "
  "ankommt: Chlorid, Eisen, freies Phosphat, Farbe. Für ein "
  "Koagulationsmittel den Aluminiumoxidgehalt und die Basizität, und ob das "
  "Produkt eine Trinkwassernorm erfüllen muss. Für ein Ionenaustauscherharz "
  "Typ und Matrix, die Ionenform bei Lieferung, Korngröße und "
  "Gleichmäßigkeitskoeffizient, Wasserrückhalt und Gesamtkapazität. Für ein "
  "Molekularsieb Typ, Form und Größe, statische Wasseradsorption, "
  "Druckfestigkeit und Abrieb.",
  "Nennen Sie auch den Verwendungszweck, nicht nur das Produkt. Der Zweck "
  "entscheidet, welche Verunreinigung zählt. Ein Harz für die "
  "Kondensatreinigung und ein Harz für die Metallrückgewinnung können "
  "dieselbe Typbezeichnung tragen und in der Aufgabe des jeweils anderen "
  "versagen.",
 ],
 "s2": [
  "Wir senden das technische Datenblatt, das Sicherheitsdatenblatt und ein "
  "Muster-Analysenzertifikat vor jedem Preis. Das sind keine Formalitäten "
  "und sie sind nicht austauschbar. Das Datenblatt ist das, was der "
  "Hersteller zu produzieren zusagt. Das Analysenzertifikat ist das, was "
  "eine Charge tatsächlich war. Ein Hersteller, der vor der Bestellung kein "
  "aktuelles Zertifikat zeigen will, sagt Ihnen etwas über die nächste.",
  "Das Sicherheitsdatenblatt muss in Format und Sprache des Bestimmungslands "
  "vorliegen und trägt die Angaben, die über die Sendung entscheiden: "
  "UN-Nummer, Gefahrklasse, Verpackungsgruppe und die Kennzeichnung, auf die "
  "das Terminal schaut. Diese drei Zeilen entscheiden, ob ein Produkt im "
  "Standardcontainer reist, ob der Hafen es annimmt und was die Fracht "
  "kostet. Ein Angebot, das ohne sie kommt, ist mit nichts vergleichbar.",
 ],
 "s3": [
  "Wir bieten auf einer einzigen Grundlage an: benannte Incoterm-Klausel und "
  "benannter Hafen, Gebinde und Nettogewicht, Frist von der Bestellung bis "
  "zur Bereitstellung, der Dokumentensatz, der mit der Ware reist, und wie "
  "lange der Preis gilt. Was nicht in dieser Zeile steht, steckt auch nicht "
  "im Preis.",
  "Rechnen Sie dann um, bevor Sie vergleichen. Zwei Angebote für dasselbe "
  "Phosphonat, eines mit fünfzig Prozent Wirkstoff und eines mit sechzig, "
  "liegen nicht fünfzehn Prozent auseinander: auf Wirkstoffbasis kann das "
  "scheinbar günstigere das teurere sein. Rechnen Sie das Gebinde hinzu: "
  "Fässer mit Pfand, Säcke, die das Bestimmungsland nicht annimmt und die "
  "umgepackt werden müssen, ein IBC ohne Rücknahme. Rechnen Sie die "
  "Incoterm-Klausel hinzu: ein FOB-Preis und ein CIF-Preis sind zwei Zahlen "
  "für dieselbe Ladung. Wir bringen jedes Angebot auf dieselbe "
  "Wirkstoffbasis, dasselbe Gebinde und dieselbe Klausel, und diesen "
  "Vergleich senden wir Ihnen, mit offengelegter Rechnung.",
 ],
 "s4": [
  "Die Produktion läuft gegen die vereinbarte Spezifikation, und jede Charge "
  "verlässt das Werk mit ihrem eigenen Analysenzertifikat, datiert und mit "
  "der Chargennummer, die auf den Fässern steht. Rückstellmuster bleiben "
  "über die Haltbarkeit des Produkts beim Hersteller, und das allein macht "
  "eine spätere Reklamation überhaupt möglich.",
  "Wo die Bestellung es rechtfertigt oder Ihre Ausschreibung es verlangt, "
  "prüft eine unabhängige Stelle vor dem Versand. Sie benennen die Stelle, "
  "nicht wir: SGS, Intertek und Bureau Veritas arbeiten an allen Ursprüngen, "
  "an denen wir einkaufen. Den Umfang legen Sie fest; der sinnvolle Umfang "
  "deckt Probenahme und Versiegelung, Menge und Nettogewicht, Zustand und "
  "Kennzeichnung der Gebinde, Sauberkeit des Containers und die "
  "Siegelnummer ab. Das Inspektionszertifikat gehört in den im Akkreditiv "
  "genannten Dokumentensatz, damit das Geld gegen die Ware fließt und nicht "
  "nur gegen Papier.",
 ],
 "s5": [
  "Das Gebinde ist eine Kostenentscheidung, und sie fällt vor der "
  "Produktion, nicht danach. Fünfundzwanzig-Kilogramm-Säcke, "
  "Zweihundertfünfzig-Kilogramm-Fässer, Ein-Tonnen-Großpackmittel und, für "
  "Flüssigkeiten in Menge, ein Tankcontainer. Jedes verändert das Gewicht, "
  "das in einen Container geht, den Arbeitsaufwand am Zielort und den Preis "
  "je Kilogramm frei Haus. Holzpaletten reisen unter dem internationalen "
  "Standard für Holzverpackungen und tragen die Marke, die das belegt.",
  "Die Temperatur gehört zur Spezifikation und ist kein Nachgedanke. Mehrere "
  "dieser Produkte kristallisieren, entmischen sich oder gefrieren unterhalb "
  "einer genannten Temperatur, und eine Wintersendung in ein kontinentales "
  "Zielgebiet muss das im Vertrag sagen. Die Haltbarkeit ebenso: Es zählt "
  "das Herstelldatum im Analysenzertifikat, nicht das Versanddatum.",
  "Die Ware reist über See, Schiene oder Straße, unter unserem Vertrag vom "
  "Werkstor bis zum vereinbarten Lieferort, und die Dokumente reisen mit.",
 ],
},
"chem_admis_h": "Was darüber entscheidet, ob eine Chemikalie zulässig ist",
"chem_admis": [
 "Eine Chemikalie ist zulässig oder sie ist es nicht, und das klärt sich vor "
 "der Bestellung und nicht an der Grenze. Drei Dinge entscheiden darüber.",
 "Das erste ist die Regelung am Bestimmungsort. Industriechemikalien werden "
 "je Markt nach eigenen Regeln registriert, angemeldet oder lizenziert, und "
 "die Pflicht liegt meist beim Importeur und nicht bei uns. Wir sagen Ihnen, "
 "was der Hersteller belegen kann; was Ihre Behörde von Ihnen verlangt, "
 "bleibt Ihnen zu bestätigen, und wir sprechen es lieber in der ersten Woche "
 "an, als es am Kai zu finden.",
 "Das zweite ist die Verwendung. Alles, was mit Trinkwasser in Berührung "
 "kommt, wird an einer Trinkwassernorm gemessen, und das Zertifikat muss "
 "Qualität und Werk benennen. Eine Industriequalität desselben Produkts mit "
 "demselben Gehalt ersetzt sie nicht, und kein Papier macht sie dazu.",
 "Das dritte ist die Gefahreinstufung. UN-Nummer, Klasse und "
 "Verpackungsgruppe entscheiden über Stauung, Dokumente, Kennzeichnung und "
 "oft darüber, ob ein Terminal den Container überhaupt annimmt. Sie sind "
 "Eigenschaften des Produkts und werden im Werk festgelegt. Eine Sendung, "
 "die kaufmännisch stimmt und bei einem Etikett falsch ist, ist immer noch "
 "eine Sendung, die nicht abgefertigt wird.",
],
"chem_faq_h": "Was Käufer vor der ersten Bestellung fragen",
"chem_faq": [
 ("Können Sie ein Produkt anbieten, das nicht in der Tabelle steht?",
  "In der Regel ja. Die Tabelle ist das, was wir am häufigsten anbieten, "
  "nicht die Grenze dessen, was wir einkaufen. Senden Sie Produkt, Qualität "
  "und Wirkstoffgehalt, und wir sagen Ihnen, ob wir es sauber beschaffen "
  "können oder nicht. Wenn wir es nicht können, sagen wir das, statt ein "
  "Angebot zu senden, zu dem wir nicht stehen könnten."),
 ("Was ist die kleinste Bestellung, die Sie bearbeiten?",
  "Wir arbeiten in vollen Containerladungen, weil die Rechnung nur dort "
  "aufgeht. Eine erste Bestellung sind normalerweise ein oder zwei Container "
  "zu voll kaufmännischen Bedingungen. Darunter steigt die Fracht je "
  "Kilogramm schneller als jede Ersparnis an der Ware, und wir würden Ihnen "
  "ein schlechteres Geschäft verkaufen, als Sie vor Ort bekommen."),
 ("Liefern Sie Trinkwasserqualität?",
  "Wo der Hersteller die entsprechende Zertifizierung hält und sie nach Werk "
  "und Qualität vorlegen kann, ja, und das Zertifikat reist mit der Ware. "
  "Wo er nur eine Industriequalität hält, sagen wir das und bieten die "
  "Industriequalität als das an, was sie ist."),
 ("Dürfen wir die Prüfstelle benennen?",
  "Ja, und uns ist das lieber. Sie benennen Stelle und Umfang, die "
  "Inspektion findet vor dem Versand statt, und das Zertifikat gehört in den "
  "im Akkreditiv genannten Dokumentensatz. Ein von uns selbst gewählter "
  "Prüfer würde Ihnen weniger beweisen."),
 ("Können Sie an unserer Ausschreibung teilnehmen?",
  "Ja. Für eine Ausschreibung liefern wir das Autorisierungsschreiben des "
  "Herstellers, Ursprungs- und Qualitätszeugnisse und die "
  "Produktdokumente, die Ihr Gremium verlangt. Senden Sie Nummer und "
  "Schlusstermin mit der Anfrage, dann wird die Akte auf dieses Datum hin "
  "zusammengestellt."),
 ("Wie sind wir geschützt, wenn die Ware nicht stimmt?",
  "Durch die Struktur, nicht durch ein Versprechen. Die Spezifikation wird "
  "vor der Produktion schriftlich vereinbart, jede Charge trägt ihr eigenes "
  "Analysenzertifikat, ein von Ihnen benannter Prüfer ist vor dem Versand "
  "dabei, und gezahlt wird gegen den im Akkreditiv genannten "
  "Dokumentensatz. Jeder dieser Punkte ist eine Stelle, an der eine falsche "
  "Sendung anhält, statt anzukommen."),
],

"ca_steps": [
 ("s1", "Ohne Meereszugang ändert sich die Rechnung", [
  "Auf einer Seestrecke ist die Fracht eine Zeile im Angebot. Hier ist sie "
  "fast das ganze Angebot. Am Ziel gibt es keinen Löschhafen, also legt jede "
  "Tonne das letzte Stück auf der Schiene oder auf dem Lkw zurück, und bei "
  "Ware, die im Verhältnis zum Wert schwer ist, und das sind "
  "Industriechemikalien und Baustoffe, entscheidet der Landweg darüber, ob "
  "das Geschäft überhaupt zustande kommt.",
  "Das ändert, was ein Angebot enthalten muss. Eine Seefrachtrate sagt hier "
  "fast nichts. Es zählen der Bahntarif für Waggon oder Container, die "
  "Standzeit am Grenzübergang, die Kosten des Übergangs zwischen zwei "
  "Bahnsystemen und wer den Container bezahlt, während er wartet. Wir "
  "weisen diese vier als benannte Zeilen aus, statt sie in eine einzige Zahl "
  "zu legen, die Sie nicht hinterfragen können.",
 ]),
 ("s2", "An der Grenze wechselt die Spurweite", [
  "Die chinesische Bahn fährt auf Normalspur. Kasachstan und seine Nachbarn "
  "fahren auf der in der Region üblichen Breitspur. Beide treffen sich "
  "nicht, also wechselt in Khorgos und in Dostyk jede Ladung den Waggon oder "
  "der Waggon wechselt das Fahrwerk. Das ist keine Formalität. Es ist ein "
  "physischer Vorgang mit Kosten, Warteschlange und einem Fehlerbild.",
  "Das Fehlerbild wiegt schwerer als die Kosten. Flüssigkeiten in Fässern "
  "und Feststoffe in Säcken, die an einem Umschlagterminal lose gehandhabt "
  "werden, kommen mit aufgerissenen Säcken, verbeulten Fässern und "
  "Mindermenge an. Der Container vermeidet das: die Box wird in einem Zug "
  "hinübergehoben und die Ware darin nie angefasst. Deshalb bieten wir "
  "containerisiert an, wo Produkt und Menge es zulassen, und deshalb sagen "
  "wir es, wenn ein Produkt es nicht zulässt.",
 ]),
 ("s3", "Die Kaspi-Querung ist ein Terminrisiko, keine Entfernung", [
  "Für Ladung über das Kaspische Meer ist das Wasser der kurze Teil. Aktau "
  "und Kuryk liegen am Ostufer, Alat am Westufer, und die Überfahrt selbst "
  "dauert Stunden. Das Warten nicht. Abfahrten werden zugeteilt und nicht so "
  "geplant, wie eine Reederei plant, das Wetter schließt die Häfen, und ein "
  "verpasster Slot zählt in Tagen.",
  "Wir nennen deshalb keine Transitzeit, die unterstellt, dass jeder "
  "Anschluss hält. Wir nennen ein Zeitfenster, sagen, was es verschieben "
  "kann, und nennen Ihnen die Kosten der Verzögerung, statt sie später "
  "gemeinsam zu entdecken. Wenn bei Ihnen ein Termin wirklich fest ist, "
  "sagen Sie es bei der Anfrage: das ändert die empfohlene Route und "
  "manchmal das Gebinde.",
 ]),
 ("s4", "Was der Zoll verlangt, Land für Land", [
  "Der kaufmännische Satz ist überall gleich: Rechnung, Packliste, "
  "Ursprungszeugnis und Transportdokument. Bei Chemikalien reisen zwei "
  "weitere Papiere mit und werden genau gelesen: das Sicherheitsdatenblatt "
  "mit UN-Nummer, Gefahrklasse und Verpackungsgruppe, und das "
  "Analysenzertifikat der Charge, die tatsächlich in den Fässern ist.",
  "Bei der Konformität unterscheiden sich die Länder. In Kasachstan und "
  "Kirgisistan tragen Waren im Anwendungsbereich der technischen Regelwerke "
  "der Zollunion das Konformitätszeichen, und die Erklärung oder das "
  "Zertifikat wird vor dem Versand ausgestellt, nicht nach der Ankunft. "
  "Usbekistan, Turkmenistan und Aserbaidschan haben jeweils eigene "
  "Regelungen. In den meisten liegt die Registrierungspflicht beim Importeur "
  "und nicht beim Verkäufer, und genau deshalb sprechen wir es in der ersten "
  "Woche an: wir sagen Ihnen, was der Hersteller belegen kann, und was bei "
  "Ihnen liegt, bleibt Ihnen zu bestätigen.",
  "Die Sprache gehört zur Akte. Ein Dokument, das die Behörde nicht lesen "
  "kann, ist ein fehlendes Dokument, und eine Übersetzung an der Grenze "
  "kostet mehr als eine im Werk.",
 ]),
 ("s5", "Der Winter gehört zur Spezifikation", [
  "Das Klima ist kontinental, und die Ware ist wochenlang darin. Waggons "
  "sind nicht beheizt und Container nicht isoliert. Mehrere der Produkte, "
  "die über diesen Korridor laufen, kristallisieren, entmischen sich oder "
  "gefrieren unterhalb einer genannten Temperatur, und eine gefrorene "
  "Flüssigkeit im Fass ist danach selten dasselbe Produkt.",
  "Die Antwort darauf ist keine Zeile in einer E-Mail. Der Vertrag nennt die "
  "tiefste Temperatur, der die Ware ausgesetzt sein wird, das Gebinde wird "
  "dafür gewählt, und wo ein Produkt die Jahreszeit wirklich nicht verträgt, "
  "ist die ehrliche Antwort, es in einer anderen zu verschiffen. Eine im "
  "November freigegebene Sendung quert im tiefen Winter, und das wird bei "
  "der Bestellung entschieden, nicht an der Grenze.",
 ]),
],
"ca_tender_h": "Ausschreibungen in der Region",
"ca_tender": [
 "Die staatlichen Öl-, Gas-, Strom-, Bergbau- und Wasserunternehmen dieser "
 "Länder kaufen über Ausschreibungen, und über den Ausgang entscheidet die "
 "Akte häufiger als der Preis.",
 "Für eine Ausschreibung liefern wir das Autorisierungsschreiben des "
 "Herstellers, das die Ausschreibung benennt, Ursprungs- und "
 "Qualitätszeugnisse, die von Ihrem Gremium aufgeführten Produktdokumente "
 "und die kaufmännischen Bedingungen in der verlangten Form. Wo die "
 "Ausschreibung eine Bietungsgarantie, eine lokale Vertretung oder eine "
 "Registrierung verlangt, die nur der Bieter halten kann, sagen wir das am "
 "Anfang und nicht bei der Abgabe. Senden Sie Nummer und Schlusstermin mit "
 "der Anfrage, dann wird die Akte auf dieses Datum hin zusammengestellt.",
],
"ca_faq_h": "Was Käufer zu diesem Korridor fragen",
"ca_faq_lede": ("Die Fragen, die darüber entscheiden, ob eine Sendung auf "
                "diesem Korridor funktioniert, so beantwortet, wie wir sie im "
                "ersten Gespräch beantworten."),
"ca_faq": [
 ("Wie lange dauert es von China nach Kasachstan?",
  "Das hängt vom Übergang und vom Slot ab, und wer mit einer einzigen Zahl "
  "antwortet, nennt den besten Fall. Wir nennen ein Zeitfenster für die "
  "konkrete Sendung, sagen, was es verschieben kann, und aktualisieren es, "
  "sobald der Waggon zugeteilt ist. Eine Zahl, die nur hält, wenn nichts "
  "schiefgeht, ist keine Zahl, mit der man planen kann."),
 ("Liefern Sie bis zu unserem Standort oder nur bis zur Grenze?",
  "Bis zum Standort, wo das Zielland es zulässt, unter einer "
  "Lieferklausel, mit dem Inlandsabschnitt als eigener Zeile, damit Sie "
  "sehen, was er kostet. Wo nur der Importeur verzollen kann, liefern wir "
  "bis zum vereinbarten Punkt vor der Abfertigung und übergeben den "
  "vollständigen Dokumentensatz."),
 ("Wer übernimmt die Zollabfertigung?",
  "Üblicherweise der Importeur, weil in den meisten dieser Länder "
  "Registrierung und Konformität beim Käufer liegen und nicht auf einen "
  "ausländischen Verkäufer übertragen werden können. Wir liefern die "
  "Dokumente, die die Abfertigung braucht, in der Sprache, die sie braucht, "
  "und prüfen den Satz vor dem Versand gegen die Liste des Ziellands."),
 ("Befördern Sie Gefahrgut auf diesem Korridor?",
  "Wo die Einstufung es zulässt und die Frachtführer es annehmen. "
  "UN-Nummer, Klasse und Verpackungsgruppe entscheiden über Gebinde, "
  "Kennzeichnung, Waggon und Dokumente, und sie stehen vor der Produktion "
  "fest. Wo ein Produkt auf dieser Route nicht rechtskonform laufen kann, "
  "sagen wir das und schlagen die Route vor, auf der es läuft."),
 ("Mit welchen Zahlungsbedingungen arbeiten Sie?",
  "Mit einem Dokumentenakkreditiv, zahlbar bei Sicht gegen den "
  "Dokumentensatz; das ist die Struktur, die wir bei einem Käufer ohne "
  "gemeinsame Vorgeschichte bevorzugen. Zum Satz gehört ein "
  "Vorversandinspektionszertifikat einer von Ihnen benannten Stelle, damit "
  "das Geld gegen die Ware fließt und nicht nur gegen Papier."),
 ("Wir sind kein staatliches Unternehmen. Bieten Sie trotzdem an?",
  "Ja. Händler, Auftragnehmer und Anlagenbetreiber kaufen auf diesem "
  "Korridor ebenfalls. Die Menge, bei der die Rechnung aufgeht, ist die "
  "volle Containerladung; darunter steigt der Landweg je Tonne schneller als "
  "jede Ersparnis an der Ware, und wir sagen Ihnen das, statt es "
  "anzubieten."),
],
"ca_cta_h": "Senden Sie eine Spezifikation. Erhalten Sie einen Preis frei Haus.",
"ca_cta": ("Produkt, Qualität, Menge und Lieferort genügen für den Anfang. "
           "Kein Konto, keine Registrierung, keine Gebühr."),

"comp": [
 ("Wen wir prüfen, und wann", [
  "Vor jedem Angebot, vor jedem Vertrag und vor jeder Zahlung prüfen wir die "
  "Gegenpartei nach Firmenname und nach jedem verwendeten Handelsnamen, ihre "
  "Eigentümer und jede Person, die sie kontrolliert, den Endverwender der "
  "Ware, wenn er nicht die Gegenpartei ist, den Empfänger, die zu "
  "benachrichtigende Partei und den endgültigen Bestimmungsort sowie "
  "Schiff, Frachtführer und Bank, soweit sie uns bekannt sind.",
  "Die Prüfung wird vor der Zahlung wiederholt und nicht aus dem Angebot "
  "übernommen. Eigentumsverhältnisse und Listen ändern sich zwischen Angebot "
  "und Versand, und ein sauberes Ergebnis aus der ersten Woche beweist "
  "nichts über die zehnte.",
 ]),
 ("Die Listen, gegen die wir prüfen", [
  "Die Liste der speziell benannten Staatsangehörigen und gesperrten "
  "Personen und die konsolidierte Sanktionsliste des OFAC des US-"
  "Finanzministeriums; die Denied-Persons-, Entity- und Unverified-Listen "
  "des BIS des US-Handelsministeriums; die konsolidierte Sanktionsliste des "
  "Sicherheitsrats der Vereinten Nationen; die konsolidierte Liste der "
  "Europäischen Union; und die Sanktionsliste des Vereinigten Königreichs.",
  "Eigentum wird nach der Fünfzig-Prozent-Regel beurteilt. Ein "
  "Unternehmen, das unmittelbar oder mittelbar zu fünfzig Prozent oder mehr "
  "insgesamt einer oder mehreren gesperrten Personen gehört, gilt selbst als "
  "gesperrt, gleich ob es namentlich auf einer Liste steht oder nicht.",
 ]),
 ("Was wir nicht tun", [
  "Wir handeln nicht mit Personen oder Unternehmen, die Sanktionen "
  "unterliegen, und nicht mit umfassend sanktionierten Gebieten.",
  "Wir machen niemals falsche Angaben zu Ursprung, Bestimmungsort oder "
  "Endverwender einer Ware, weder in einem Dokument noch in einer Erklärung "
  "noch im Schriftverkehr, und wir nehmen eine solche Weisung nicht an.",
  "Wir gestalten kein Geschäft, keine Route und keine Zahlung so, dass die "
  "Anwendung einer Sanktions- oder Exportkontrollvorschrift vermieden wird, "
  "und wir helfen keiner anderen Partei dabei.",
  "Wir liefern keine Ware, wenn wir wissen oder Grund zu der Annahme haben, "
  "dass sie für eine verbotene Endverwendung bestimmt ist, einschließlich "
  "einer militärischen, nuklearen, Raketen- oder chemisch-biologischen "
  "Endverwendung, soweit diese kontrolliert ist.",
 ]),
 ("Was ein Geschäft anhält", [
  "Ein Geschäft wird angehalten und geprüft, bevor es weitergeht, wenn der "
  "Endverwender nicht genannt werden will oder die angegebene Verwendung "
  "weder zur Ware noch zur Menge passt; wenn Lieferanschrift, Empfänger oder "
  "Route nach Vertragsschluss wechseln oder die Route kaufmännisch keinen "
  "Sinn ergibt; wenn die Zahlung von einem Dritten, aus einer "
  "unzusammenhängenden Jurisdiktion oder auf eine Weise angeboten wird, die "
  "ihren Ursprung verschleiert; wenn die Gegenpartei verlangt, dass "
  "Dokumente etwas anderes als die Tatsachen zeigen; oder wenn Gegenpartei, "
  "Eigentümer oder Bestimmungsort mit einem sanktionierten Gebiet verbunden "
  "sind.",
  "Jeder dieser Punkte wird anhand von Belegen geklärt, oder das Geschäft "
  "wird abgelehnt. Eine Zusicherung allein klärt keinen davon. Wo ein "
  "Geschäft nicht rechtskonform gestaltet werden kann, lehnen wir es ab, und "
  "kein Auftragswert ändert diese Antwort.",
 ]),
 ("Aufbewahrung", [
  "Prüfergebnisse, erhaltene Identitätsnachweise, Angaben zum Endverwender "
  "und die Gründe für jede Ablehnung werden mit der Geschäftsakte mindestens "
  "fünf Jahre ab dem Datum des Geschäfts aufbewahrt, entsprechend den "
  "Aufbewahrungsfristen der US-Sanktions- und Exportkontrollvorschriften.",
  "Ein Hinweis zu einem Geschäft, einer Gegenpartei oder zu dieser Richtlinie "
  "kann unmittelbar an das Mitglied unter info@ispgroupgc.com gerichtet "
  "werden. Ein in gutem Glauben vorgebrachter Hinweis hat für die "
  "hinweisgebende Person keine nachteiligen Folgen.",
 ]),
],
}


LOCALES = {"fr": FR, "es": ES, "de": DE}


# ---------------------------------------------------------------------
def add_css(s):
    if CSS.strip() in s:
        return s
    return s.replace("</head>", "<style>%s</style>\n</head>" % CSS, 1)


def faq_schema(s, faq):
    if '"@type": "FAQPage"' in s:
        return s
    data = {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}}
                           for q, a in faq]}
    return s.replace("</body>", '<script type="application/ld+json">%s</script>\n'
                     % json.dumps(data, ensure_ascii=False) + "</body>", 1)


def do_chemicals(lg, L):
    p = SITE / lg / "chemicals.html"
    s = b = p.read_text()
    for sid, paras in L["chem_steps"].items():
        m = re.search(r'(?s)(<h2 id="%s">.*?</h2><div class="ptext">)(.*?)(</div>)'
                      % sid, s)
        if not m:
            print("  ВНИМАНИЕ: %s/chemicals, шаг %s не найден" % (lg, sid))
            continue
        body = "".join("<p>%s</p>" % x for x in paras)
        if m.group(2) == body:
            continue
        s = s[:m.start(2)] + body + s[m.end(2):]
    if L["chem_admis_h"] not in s:
        block = ('<div class="lede" style="margin-top:56px"><h2>%s</h2>'
                 '<p class="intro">%s</p></div>%s'
                 % (L["chem_admis_h"], L["chem_admis"][0],
                    "".join('<p class="chem-a">%s</p>' % x
                            for x in L["chem_admis"][1:])))
        anchor = ('<div class="lede" style="margin-top:56px"><h2>%s</h2>'
                  % L["tenders_h"])
        if anchor in s:
            s = s.replace(anchor, block + anchor, 1)
        else:
            print("  ВНИМАНИЕ: %s/chemicals, якорь тендеров не найден" % lg)
    if L["chem_faq_h"] not in s:
        qa = "".join('<p class="chem-q">%s</p><p class="chem-a">%s</p>' % (q, a)
                     for q, a in L["chem_faq"])
        block = ('<div class="lede" style="margin-top:56px"><h2>%s</h2></div>%s'
                 % (L["chem_faq_h"], qa))
        anchor = '<div class="lede" id="rfq">'
        if anchor in s:
            s = s.replace(anchor, block + anchor, 1)
        else:
            print("  ВНИМАНИЕ: %s/chemicals, якорь формы не найден" % lg)
    s = faq_schema(s, L["chem_faq"])
    s = add_css(s)
    if s != b:
        p.write_text(s)
        return True
    return False


def do_central_asia(lg, L):
    p = SITE / lg / "central-asia.html"
    s = b = p.read_text()
    if 'id="s1"' not in s:
        toc = ('<nav class="toc"><ol>%s</ol></nav>'
               % "".join('<li><a href="#%s"><span>%02d</span>%s</a></li>'
                         % (sid, i + 1, h)
                         for i, (sid, h, _) in enumerate(L["ca_steps"])))
        prose = '<div class="prose">%s</div>' % "".join(
            '<div class="pblock"><span class="k">%02d</span><h2 id="%s">%s</h2>'
            '<div class="ptext">%s</div></div>'
            % (i + 1, sid, h, "".join("<p>%s</p>" % x for x in paras))
            for i, (sid, h, paras) in enumerate(L["ca_steps"]))
        tender = ('<div class="lede" style="margin-top:56px"><h2>%s</h2>'
                  '<p class="intro">%s</p></div>%s'
                  % (L["ca_tender_h"], L["ca_tender"][0],
                     "".join('<p class="ca-a">%s</p>' % x
                             for x in L["ca_tender"][1:])))
        qa = "".join("<details><summary>%s</summary><p>%s</p></details>"
                     % (q, a) for q, a in L["ca_faq"])
        faq = ('<div class="lede" style="margin-top:56px"><h2>%s</h2>'
               '<p class="intro">%s</p></div><div style="margin-top:34px">%s</div>'
               % (L["ca_faq_h"], L["ca_faq_lede"], qa))
        cta = ('<div class="lede" style="margin-top:56px"><h2>%s</h2>'
               '<p class="intro">%s</p><p style="margin-top:18px">'
               '<a class="btn" href="/contact#enquiry">%s</a></p></div>'
               % (L["ca_cta_h"], L["ca_cta"], L["cta_btn"]))
        anchor = '<div class="lanelinks" style="margin-top:48px">'
        if anchor not in s:
            print("  ВНИМАНИЕ: %s/central-asia, якорь не найден" % lg)
            return False
        s = s.replace(anchor, toc + prose + tender + faq + cta + anchor, 1)
    s = faq_schema(s, L["ca_faq"])
    s = add_css(s)
    if s != b:
        p.write_text(s)
        return True
    return False


def do_compliance(lg, L):
    p = SITE / lg / "compliance.html"
    s = b = p.read_text()
    if L["comp"][0][0] not in s:
        out = "".join('<h2 class="comp-h">%s</h2>%s'
                      % (h, "".join('<p class="comp-p">%s</p>' % x
                                    for x in paras))
                      for h, paras in L["comp"])
        anchor = ('<div class="lede" style="margin-top:56px"><h2>%s</h2>'
                  % L["details_h"])
        if anchor not in s:
            print("  ВНИМАНИЕ: %s/compliance, якорь не найден" % lg)
            return False
        s = s.replace(anchor, out + anchor, 1)
    s = add_css(s)
    if s != b:
        p.write_text(s)
        return True
    return False


def main():
    n = 0
    for lg, L in LOCALES.items():
        n += do_chemicals(lg, L)
        n += do_central_asia(lg, L)
        n += do_compliance(lg, L)
    print("страниц дополнено: %d" % n)
    for lg in LOCALES:
        for name in ("chemicals", "central-asia", "compliance"):
            s = (SITE / lg / ("%s.html" % name)).read_text()
            t = re.sub(r"<[^>]+>", " ",
                       re.sub(r"(?s)<(script|style|nav|footer|head).*?</\1>", "", s))
            print("  %s/%-13s примерно %d слов" % (lg, name, len(t.split())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
