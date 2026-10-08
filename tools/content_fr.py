# -*- coding: utf-8 -*-
"""Этап 4: французская версия. Того, Бенин и Кот-д'Ивуар франкоязычные,
и AJC с Interra ведут французский не из вежливости."""
from content_core import HOST, ORG

def tr(last):
    return [("ISP Group", "index-fr.html"), (last, None)]

PAGES_FR = [
{
 "slug": "fr",
 "title": "ISP Group | sourcing et négoce international",
 "desc": "Société de négoce américaine. Nous trouvons des producteurs vérifiés, "
         "achetons en notre nom propre et livrons à votre port au prix rendu.",
 "eyebrow": "Sourcing et négoce international · États-Unis",
 "h1": "Nommez le produit. Nous rendons <em>trois producteurs vérifiés</em> et un prix rendu.",
 "sub": "Nous trouvons l’usine, vérifions qu’elle peut légalement expédier vers votre "
        "pays, achetons la marchandise en notre nom propre et la livrons à votre port.",
 "chips": ["<b>20</b> ans d’expérience", "<b>10</b> jours ouvrés jusqu’au prix rendu",
           "FOB &middot; CFR &middot; CIF &middot; DAP", "Principal, <b>pas courtier</b>"],
 "img": ("terminal.jpg", 1023, 438, "Portiques à conteneurs sur un terminal maritime",
         "Un seul interlocuteur, de la sortie d’usine à votre port"),
 "lede": ("La partie d’un achat transfrontière dont personne ne veut",
   "Trouver une usine est la moitié facile. La moitié difficile consiste à prouver "
   "qu’elle existe, à la faire produire selon votre cahier des charges, à faire passer "
   "les documents par deux douanes et à s’assurer que l’argent arrive. C’est cette "
   "partie que nous prenons."),
 "body": [
  ("h2", "Pourquoi les acheteurs passent par nous"),
  ("ul", ["<b>Nous vérifions avant de coter.</b> Les numéros d’agrément et de licence "
          "sont contrôlés auprès des registres du pays importateur, et non repris du site "
          "du vendeur. Les domaines imitant de vrais exportateurs sont courants dans ce "
          "métier et nous les filtrons.",
          "<b>Nous cotons à partir des statistiques douanières.</b> Nous comparons ce que "
          "des marchandises semblables ont réellement payé au dédouanement sur votre "
          "ligne avant de négocier. Une offre se juge ainsi par rapport au marché et non "
          "par rapport à elle-même.",
          "<b>Nous prenons la propriété de la marchandise.</b> Nous sommes l’acheteur sur "
          "un contrat et le vendeur sur l’autre. Un seul interlocuteur, une seule facture, "
          "une seule devise.",
          "<b>Nous reflétons les conditions.</b> Délais d’inspection, tolérances de "
          "poids, délais de réclamation et frais bancaires sont identiques sur les deux "
          "contrats, pour que rien ne tombe dans l’intervalle."]),
  ("h2", "Ce que nous fournissons"),
  ("p", "Nous ne sommes pas liés à une seule marchandise. Volaille et protéines "
        "congelées, denrées de base et ingrédients alimentaires, matériaux de "
        "construction et de finition, équipements industriels, outillage et quincaillerie, "
        "métaux et tubes, papier, emballage et consommables."),
  ("p", "Notre métier est le sourcing et l’exécution. Un produit hors de ces "
        "catégories est un projet de sourcing, pas un refus."),
  ("h2", "L’Afrique de l’Ouest"),
  ("p", "Nous livrons des programmes de conteneurs frigorifiques depuis les Amériques et "
        "l’Union européenne vers Lomé et Cotonou. Sur cette ligne, trois questions "
        "passent avant le prix : l’agrément de l’établissement pour le pays de "
        "destination, la désignation exacte de la découpe, et la chaîne du froid."),
  ("p", "Le détail figure sur la page "
        "<a href=\"afrique-ouest.html\">Afrique de l’Ouest</a>, et la nomenclature des "
        "découpes sur <a href=\"decoupes-volaille.html\">découpes de volaille</a>."),
  ("note", "« Ailes » n’est pas un produit. L’aile entière à trois phalanges, "
           "l’aile à deux phalanges, le manchon et l’aileron sont quatre produits "
           "différents, à quatre prix différents."),
  ("h2", "Comment commencer"),
  ("p", "Écrivez-nous le produit, la quantité et le port de destination. Vous recevez "
        "sous un jour ouvré un accusé de réception avec les questions restantes, et "
        "sous une dizaine de jours ouvrés un prix rendu : au moins trois offres comparables "
        "de producteurs vérifiés, fret, assurance, frais portuaires, droits et "
        "certification inclus, avec la date de validité indiquée."),
  ("p", "Pas de frais de cotation et pas de commission sur la facture d’un producteur. "
        "Nous achetons en notre nom propre et revendons."),
 ],
 "faq_h2": "Questions fréquentes",
 "faq_sub": "Celles qui reviennent au premier échange.",
 "faq": [
  ("Êtes-vous courtier ou agent ?",
   "Ni l’un ni l’autre. Nous achetons la marchandise en notre nom propre et la "
   "revendons. Aucune commission ne s’ajoute à la facture du producteur, et celui-ci "
   "n’a pas à gérer une facturation triangulaire."),
  ("Traitez-vous de petites quantités ?",
   "Nous travaillons en conteneurs complets, car c’est là que l’économie tient. "
   "Pour une première commande nous faisons généralement un essai d’un ou deux "
   "conteneurs à conditions commerciales complètes."),
  ("Quels Incoterms cotez-vous ?",
   "FOB, CFR, CIF, FCA et DAP. Nous préférons coter au moins deux bases côte à "
   "côte, pour que le coût réel de la partie logistique soit visible."),
  ("Dans quelles langues travaillez-vous ?",
   "Anglais et russe en correspondance directe, et français sur les lignes ouest-"
   "africaines. Côté producteurs, nous travaillons également en chinois, en turc et "
   "en portugais."),
 ],
 "related": ("Pages en français",
   "Le reste du site est en anglais.",
   [("afrique-ouest.html", "Afrique de l’Ouest",
     "Programmes frigorifiques vers Lomé et Cotonou."),
    ("decoupes-volaille.html", "Découpes de volaille",
     "Aile, manchon, aileron : quatre produits distincts."),
    ("certificat-veterinaire.html", "Certificat vétérinaire",
     "L’agrément de l’établissement passe avant le prix."),
    ("contact-fr.html", "Contact", "Envoyez un besoin, recevez un prix rendu.")]),
 "ld": [dict(ORG, **{"@context": "https://schema.org",
         "alternateName": "ISP Group Global Commerce",
         "description": "Société de négoce et de sourcing international basée aux "
                        "États-Unis."})],
},
{
 "slug": "afrique-ouest",
 "title": "Afrique de l’Ouest | volaille congelée, Lomé et Cotonou",
 "desc": "Programmes de conteneurs frigorifiques vers le Togo et le Bénin : agrément de "
         "l’établissement, désignation des découpes, chaîne du froid et conditions "
         "de paiement.",
 "trail": tr("Afrique de l’Ouest"),
 "h1": "Afrique de l’Ouest : denrées congelées vers <em>Lomé et Cotonou</em>",
 "sub": "Programmes frigorifiques depuis les Amériques et l’Union européenne. Le "
        "produit est simple ; l’agrément et les conditions de paiement ne le sont pas, "
        "et ce sont eux qui décident de la rentabilité.",
 "chips": ["CIF &middot; CFR", "Conteneur 40 pieds, 25 t net",
           "Cartons de 10 kg", "Lomé &middot; Cotonou"],
 "img": ("vessel2.jpg", 774, 581, "Porte-conteneurs à quai",
         "Un programme frigorifique se planifie, il ne se réserve pas au coup par coup"),
 "lede": ("L’offre la moins chère est généralement celle qui ne peut pas expédier",
   "Une offre n’est réelle que si l’établissement producteur est agréé pour le "
   "pays de destination, si la découpe est bien celle que le marché achète, et si les "
   "conditions de paiement survivent à une traversée de quarante jours."),
 "body": [
  ("h2", "L’agrément passe avant le prix"),
  ("p", "La viande congelée n’entre pas sur une facture commerciale. Elle entre sur un "
        "certificat sanitaire vétérinaire délivré pour un établissement précis, "
        "dans une forme que le pays de destination accepte. Un établissement agréé pour "
        "un pays ne l’est pas automatiquement pour son voisin."),
  ("p", "La première question à poser à un vendeur, avant toute discussion de prix, "
        "est le numéro d’agrément de l’établissement et la confirmation écrite "
        "qu’il est autorisé pour la destination. Le détail figure sur la page "
        "<a href=\"certificat-veterinaire.html\">certificat vétérinaire</a>."),
  ("h2", "Une découpe, c’est quatre produits"),
  ("p", "La raison la plus fréquente pour laquelle deux offres ne sont pas comparables est "
        "qu’elles ne portent pas sur la même chose. L’aile entière à trois "
        "phalanges, l’aile à deux phalanges, le manchon et l’aileron sont quatre "
        "produits distincts, à quatre prix et pour quatre acheteurs différents. La dinde "
        "se vend en mâle ou en femelle, et les deux lignes ne sont pas interchangeables."),
  ("p", "Chaque demande que nous envoyons nomme l’anatomie explicitement, précise le "
        "conditionnement et demande le prix par ligne sur le même Incoterm. Une offre qui "
        "cote « des ailes » n’est pas une offre. Voir "
        "<a href=\"decoupes-volaille.html\">découpes de volaille</a>."),
  ("h2", "Conditionnement et chaîne du froid"),
  ("p", "Le standard ouest-africain est le produit congelé en bloc en cartons de 10 kg, qui "
        "n’est pas le conditionnement standard aux États-Unis ni dans l’Union "
        "européenne. Le reconditionnement est possible et il coûte, donc le prix se "
        "demande aussi dans le conditionnement d’origine du producteur : l’écart "
        "indique ce que vaut réellement le format non standard."),
  ("p", "Un conteneur frigorifique de 40 pieds transporte environ 25 tonnes nettes. La "
        "température est réglée au chargement, enregistrée pendant tout le trajet et "
        "relevée au déchargement, et l’enregistrement fait partie du dossier "
        "documentaire. Le temps de branchement au port de transbordement et à destination "
        "est la partie que personne ne réserve et que tout le monde suppose acquise."),
  ("h2", "Comparer le marché, pas les cotations"),
  ("p", "Une cotation est ce qu’un vendeur souhaite recevoir. Les statistiques douanières "
        "indiquent à quel prix la marchandise a réellement franchi une frontière, car "
        "la valeur déclarée est divisée par le poids net déclaré et toutes les "
        "remises réellement accordées sont déjà dans ce chiffre."),
  ("p", "Avant de négocier une ligne, nous relevons les valeurs à l’importation du pays "
        "de destination par origine et par code marchandise sur les dernières périodes "
        "complètes, et nous négocions contre cette référence. Sur cette ligne, "
        "l’exercice déplace régulièrement l’objectif de vingt pour cent ou plus."),
  ("h2", "Les conditions de paiement décident du rendement"),
  ("p", "La marge au kilo se fixe dans la négociation ; le rendement du capital se fixe par "
        "la durée pendant laquelle l’argent est sorti. Un crédit documentaire payable "
        "à vue contre documents libère la trésorerie alors que le navire est encore en "
        "mer. Trente jours après arrivée ajoutent toute la traversée plus un mois au "
        "cycle, ce qui sur un programme multi-conteneurs fait la différence entre financer "
        "une expédition et en financer quatre à la fois."),
  ("note", "Un acheteur qui demande des délais de paiement demande une facilité de "
           "crédit, et une facilité de crédit a un prix. Cette conversation a lieu "
           "avant la première expédition, pas après."),
 ],
 "faq_h2": "Questions sur cette ligne",
 "faq_sub": "Les quatre qui décident si une expédition fonctionne.",
 "faq": [
  ("Que faut-il vérifier avant qu’une offre de viande congelée soit réelle ?",
   "L’établissement producteur doit être agréé pour le pays de destination. Nous "
   "demandons le numéro d’agrément et la confirmation écrite avant de discuter du prix."),
  ("Pourquoi deux offres de volaille ne sont-elles pas comparables ?",
   "Parce qu’il ne s’agit généralement pas du même produit. Aile entière, aile "
   "à deux phalanges, manchon et aileron sont quatre produits à quatre prix."),
  ("Quel est le conditionnement standard sur cette ligne ?",
   "Produit congelé en bloc en cartons de 10 kg, dans un conteneur frigorifique de "
   "40 pieds d’environ 25 tonnes nettes. Demandez aussi le prix dans le conditionnement "
   "d’origine du producteur."),
  ("Quels ports desservez-vous ?",
   "Lomé et Cotonou, cotés séparément car les frais portuaires diffèrent. Les "
   "origines habituelles sont Santos, Gdańsk et Houston."),
 ],
 "related": ("À lire ensuite", "Les pages liées à cette ligne.",
   [("decoupes-volaille.html", "Découpes de volaille",
     "Aile, manchon, aileron : la nomenclature qui rend les offres comparables."),
    ("certificat-veterinaire.html", "Certificat vétérinaire",
     "L’agrément de l’établissement et qui le délivre."),
    ("contact-fr.html", "Contact", "Envoyez un besoin, recevez un prix rendu."),
    ("index.html", "Site en anglais", "Le reste du site, y compris les autres lignes.")]),
 "ld": [],
},
{
 "slug": "decoupes-volaille",
 "title": "Découpes de volaille | aile, manchon, aileron",
 "desc": "Pourquoi une cotation pour « des ailes » n’est pas une cotation : aile "
         "entière, aile à deux phalanges, manchon et aileron sont quatre produits.",
 "trail": tr("Découpes de volaille"),
 "h1": "« Ailes » <em>n’est pas un produit</em>",
 "sub": "Une aile entière compte trois phalanges. Retirez la pointe et vous avez une aile "
        "à deux phalanges. Séparez les deux sections restantes et vous obtenez deux "
        "produits de plus. Quatre articles, quatre prix, quatre acheteurs.",
 "chips": ["Trois phalanges", "Manchon &middot; aileron", "Mâle &middot; femelle",
           "Prix par ligne"],
 "lede": ("La raison la plus fréquente pour laquelle deux offres ne se comparent pas",
   "Ni l’Incoterm, ni le conditionnement, ni les conditions de paiement. C’est que les "
   "deux vendeurs cotent des parties différentes de l’animal en leur donnant le même nom."),
 "body": [
  ("h2", "L’anatomie, une fois pour toutes"),
  ("p", "Une aile entière comporte trois sections. La plus proche du corps est le "
        "<b>manchon</b>, en forme de petit pilon, avec un seul os. Au milieu se trouve "
        "l’<b>aileron</b>, plat, avec deux os parallèles. À l’extrémité se "
        "trouve la <b>pointe d’aile</b>, qui porte très peu de chair."),
  ("ul", ["<b>Aile entière, trois phalanges</b> : les trois sections, intactes.",
          "<b>Aile à deux phalanges</b> : manchon et aileron, pointe retirée.",
          "<b>Manchon</b> seul : la section la plus charnue, cotée en conséquence.",
          "<b>Aileron</b> seul : forte demande sur certains marchés, quasi nulle ailleurs.",
          "<b>Pointes d’ailes</b> : sous-produit avec son propre marché étroit."]),
  ("note", "Un vendeur qui cote « des ailes » sans préciser la configuration peut "
           "proposer l’un quelconque des quatre premiers articles, et l’écart entre le "
           "moins cher et le plus cher n’est pas un arrondi."),
  ("h2", "Mâle et femelle ne sont pas deux qualités du même produit"),
  ("p", "Chez la dinde, les lignes mâle et femelle sont élevées à des poids "
        "différents et donnent des calibres différents. Pour un transformateur qui "
        "achète à un poids de portion, elles ne sont pas interchangeables, et une "
        "livraison de la mauvaise ligne est inutilisable plutôt que simplement décevante. "
        "Précisez la ligne et la fourchette de poids à la pièce."),
  ("h2", "Les autres découpes et leurs marchés"),
  ("p", "Cuisses, hauts de cuisse, pilons, dos, cous, croupions et pattes se négocient "
        "séparément et chacun a sa géographie. Une découpe qui est un sous-produit "
        "sur un marché est un produit de base sur un autre : c’est toute la raison "
        "d’être du commerce international des découpes."),
  ("p", "Deux conséquences commerciales. Les prix des différentes parties du même "
        "animal évoluent indépendamment, donc un panier coté à un prix moyen unique "
        "masque la ligne qui coûte cher. Et la disponibilité dépend de ce qu’achète "
        "le reste du monde, ce qui explique qu’une ligne puisse être introuvable un mois "
        "où l’animal entier est bon marché."),
  ("h2", "À quoi ressemble une demande exploitable"),
  ("ul", ["La découpe nommée par son anatomie, pas par sa catégorie.",
          "Mâle ou femelle pour la dinde, avec la fourchette de poids à la pièce.",
          "Le conditionnement : poids du carton, congelé en bloc ou pièce par pièce, "
          "net ou brut.",
          "L’Incoterm et le port nommé, port par port s’il y en a plusieurs.",
          "La quantité par ligne et par mois, pas un chiffre global.",
          "Le numéro d’agrément de l’établissement, sans lequel tout le reste est "
          "sans objet."]),
  ("h2", "Le panier compte plus que la remise"),
  ("p", "Sur un programme mixte, la composition vaut plus que la négociation. Déplacer "
        "la proportion du conteneur vers les lignes où l’écart entre le marché "
        "d’achat et le marché de vente est le plus large peut rapporter davantage par "
        "mois que chaque centime arraché au fournisseur. Cette discussion a lieu avec "
        "l’acheteur au départ, pas après la première expédition."),
 ],
 "faq_h2": "Questions sur les découpes",
 "faq_sub": "Les trois qui reviennent à chaque première commande.",
 "faq": [
  ("Quelle différence entre un manchon et un aileron ?",
   "Le manchon est la section proche du corps, en forme de petit pilon, avec un seul os. "
   "L’aileron est la section médiane, plate, avec deux os parallèles. Ce sont deux "
   "produits distincts à deux prix distincts."),
  ("Puis-je acheter des ailes entières et les faire découper à destination ?",
   "Parfois, et l’économie dépend entièrement du coût de la main-d’œuvre et du "
   "rendement chez vous. Demandez les deux prix, entier et séparé, puis comparez après "
   "avoir ajouté votre coût de découpe et vos pertes."),
  ("Pourquoi les prix des découpes évoluent-ils dans des sens opposés ?",
   "Parce que chaque découpe est vendue dans une géographie différente, avec sa "
   "propre demande. L’animal est désossé et chaque partie part là où elle vaut le "
   "plus cher, donc les parties ont des marchés indépendants."),
 ],
 "related": ("À lire ensuite", "Les pages liées.",
   [("afrique-ouest.html", "Afrique de l’Ouest", "La ligne complète vers Lomé et Cotonou."),
    ("certificat-veterinaire.html", "Certificat vétérinaire",
     "Ce qu’il faut vérifier avant le prix."),
    ("contact-fr.html", "Contact", "Envoyez un besoin par ligne."),
    ("index.html", "Site en anglais", "Le reste du site.")]),
 "ld": [],
},
{
 "slug": "certificat-veterinaire",
 "title": "Certificat vétérinaire | agrément de l’établissement",
 "desc": "Pourquoi le numéro d’agrément passe avant le prix, comment fonctionne la "
         "certification à l’export des États-Unis et de l’Union européenne.",
 "trail": tr("Certificat vétérinaire"),
 "h1": "Le numéro d’agrément passe <em>avant le prix</em>",
 "sub": "La viande congelée n’entre pas dans un pays sur une facture commerciale. Elle "
        "entre sur un certificat sanitaire délivré pour un établissement précis. Si "
        "l’établissement n’est pas agréé, le prix n’a aucune importance.",
 "chips": ["Numéro d’agrément", "Modèle de certificat", "Par destination",
           "Confirmation écrite"],
 "lede": ("L’agrément est accordé usine par usine et pays par pays",
   "Un établissement autorisé pour un pays ouest-africain ne l’est pas "
   "automatiquement pour son voisin, et les listes évoluent."),
 "body": [
  ("h2", "Ce qu’est le certificat"),
  ("p", "Un certificat sanitaire vétérinaire est un document officiel délivré par "
        "l’autorité compétente du pays exportateur, attestant que l’envoi provient "
        "d’un établissement agréé, qu’il a été produit sous inspection "
        "officielle et qu’il répond aux conditions sanitaires fixées par le pays "
        "importateur."),
  ("p", "Ce n’est pas un document commercial et le vendeur ne peut pas l’émettre. Il "
        "accompagne l’envoi, il est présenté au poste frontière d’entrée, et sans "
        "lui la marchandise ne dédouane pas, quelle que soit la facture."),
  ("h2", "Origine États-Unis"),
  ("p", "La certification à l’export passe par le service fédéral d’inspection de la "
        "sécurité alimentaire. Les exigences propres à chaque pays de destination, y "
        "compris le modèle de certificat et les attestations supplémentaires, sont "
        "publiées dans une bibliothèque à l’export tenue à cet effet et mise à "
        "jour lorsque les destinations modifient leurs règles."),
  ("p", "Deux conséquences pratiques. Certaines destinations sont traitées par voie "
        "électronique et d’autres exigent encore un certificat papier, ce qui change le "
        "délai au chargement. Et une destination non répertoriée n’est pas "
        "nécessairement fermée, mais les exigences doivent alors être établies par "
        "écrit avant tout chargement plutôt que supposées."),
  ("h2", "Origine Union européenne"),
  ("p", "L’équivalent est l’autorité compétente de l’État membre, les "
        "certificats étant émis via le système de contrôle des échanges de "
        "l’Union. L’établissement doit détenir l’agrément correspondant, et pour "
        "l’export vers un pays tiers le modèle de certificat est celui convenu entre "
        "l’Union et la destination."),
  ("h2", "Ce qu’il faut demander, dans cet ordre"),
  ("ul", ["<b>Le numéro d’agrément de l’établissement</b>, tel qu’enregistré, "
          "et non la raison commerciale.",
          "<b>La confirmation écrite que l’établissement est agréé pour la "
          "destination</b>, pas pour la région ni pour un pays voisin.",
          "<b>Le modèle de certificat</b> qui sera émis, et s’il est électronique ou "
          "papier, car cela détermine le délai.",
          "<b>Qui le signe</b> et combien de temps prend la signature dans cette usine.",
          "<b>Ce qui se passe si la destination modifie ses exigences</b> entre le contrat "
          "et la date de chargement."]),
  ("note", "Nous ne considérons pas une assurance verbale du vendeur comme une réponse. "
           "Le numéro est vérifié, et lorsque la destination est ambiguë le modèle "
           "de certificat est identifié par écrit avant tout mouvement d’argent."),
  ("h2", "Pourquoi c’est la première question"),
  ("p", "Parce que c’est la seule variable commerciale qui ne peut pas être corrigée "
        "ensuite. Un prix se renégocie, un conditionnement se change, une date glisse. Un "
        "établissement non agréé ne peut pas être rendu agréé dans le temps "
        "d’un cycle d’expédition, et un conteneur de produits congelés immobilisé "
        "à un poste frontière est l’échec le plus coûteux disponible sur cette ligne."),
 ],
 "faq_h2": "Questions sur l’agrément",
 "faq_sub": "Les trois qui reviennent toujours.",
 "faq": [
  ("Un vendeur avec une licence d’export peut-il expédier partout ?",
   "Non. L’agrément est par établissement et par destination. Une usine autorisée "
   "pour un pays peut ne pas l’être pour son voisin, et les listes sont révisées."),
  ("Combien de temps pour agréer une usine vers une nouvelle destination ?",
   "C’est une procédure entre États, qui se compte en mois et non en semaines. Pour "
   "une expédition immédiate, la réponse est de trouver un établissement déjà "
   "agréé."),
  ("Qui paie si l’envoi est refusé à la frontière ?",
   "Cela dépend entièrement de la répartition prévue au contrat, et c’est "
   "pourquoi elle est écrite avant la première expédition. Nous reflétons la "
   "condition sur les deux contrats pour que le risque ne tombe pas dans l’intervalle."),
 ],
 "related": ("À lire ensuite", "Les pages liées.",
   [("afrique-ouest.html", "Afrique de l’Ouest", "La ligne complète vers Lomé et Cotonou."),
    ("decoupes-volaille.html", "Découpes de volaille", "Aile, manchon, aileron."),
    ("contact-fr.html", "Contact", "Envoyez un besoin."),
    ("index.html", "Site en anglais", "Le reste du site.")]),
 "ld": [],
},
{
 "slug": "contact-fr",
 "title": "Contact ISP Group | demandes de cotation",
 "desc": "Envoyez votre besoin : produit, quantité et port de destination suffisent. "
         "Bureau à North Miami Beach, Floride. Réponse sous un jour ouvré.",
 "trail": tr("Contact"),
 "h1": "Dites-nous ce qu’il vous faut <em>et où cela doit arriver</em>",
 "sub": "Le produit, la quantité et le port de destination suffisent pour démarrer une "
        "cotation. Pas de compte, pas d’inscription, pas de frais. Réponse sous un jour "
        "ouvré.",
 "chips": ["<b>1</b> jour ouvré pour répondre",
           "<b>10</b> jours ouvrés jusqu’au prix rendu",
           "FOB &middot; CFR &middot; CIF &middot; DAP"],
 "lede": ("Ce qu’il faut mettre dans le premier message",
   "Plus vite un besoin devient un cahier des charges, plus vite il devient un prix. Vous "
   "n’avez pas besoin de tout cela pour nous écrire, mais chaque ligne que vous pouvez "
   "remplir supprime un aller-retour."),
 "body": [
  ("h2", "Les quatre lignes qui lancent une cotation"),
  ("ul", ["<b>Ce qu’est le produit</b>, avec vos propres mots. Une photo, un plan, une "
          "référence concurrente ou un échantillon valent mieux qu’une catégorie.",
          "<b>Quelle quantité</b>, par expédition et par mois si cela se répète.",
          "<b>Où cela doit arriver.</b> Port, ville ou la porte de votre entrepôt. Le "
          "transport intérieur est souvent le poste le plus lourd d’un prix rendu.",
          "<b>Sur quelles conditions</b>, si vous le savez déjà. Sinon, dites-le et nous "
          "coterons deux bases côte à côte."]),
  ("h2", "Ce qui se passe ensuite"),
  ("p", "Sous un jour ouvré, un accusé de réception avec les questions qui restent. Ces "
        "questions sont le cahier des charges en train de se former, et c’est la partie "
        "qui décide si l’expédition fonctionne."),
  ("p", "Sous une dizaine de jours ouvrés, un prix rendu : au moins trois offres "
        "comparables de producteurs vérifiés sur une même base, fret, assurance, frais "
        "portuaires, droits et certification inclus, avec la date de validité indiquée."),
  ("note", "Pas de frais de cotation, et aucune commission ajoutée à la facture d’un "
           "producteur. Nous achetons en notre nom propre et revendons."),
  ("h2", "Si vous êtes producteur"),
  ("p", "Écrivez à la même adresse. Envoyez le numéro d’agrément ou de licence, la "
        "gamme avec les formats de conditionnement, les ports de chargement habituels et les "
        "pays pour lesquels vous êtes déjà autorisé. Cela nous suffit pour vous dire "
        "sous un jour si nous avons un acheteur."),
  ("h2", "Où nous sommes"),
  ("p", "ISP GROUP LLC est une société américaine. Siège au 16395 Biscayne Blvd, "
        "North Miami Beach, Floride 33160. Correspondance en français, en anglais et en "
        "russe ; une demande écrite reçoit une réponse plus vite que tout autre canal."),
 ],
 "faq_h2": "Avant d’écrire",
 "faq_sub": "Trois points vérifiés avant un premier contact.",
 "faq": [
  ("La cotation est-elle payante ?",
   "Non. Aucun frais de cotation et aucune commission sur la facture du producteur. Nous "
   "achetons en notre nom propre et revendons, donc le prix coté est le prix payé."),
  ("Quelle est la commande minimale ?",
   "Nous travaillons en conteneurs complets. Pour une première commande, un ou deux "
   "conteneurs à conditions commerciales complètes avant le démarrage d’un programme "
   "mensuel."),
  ("En combien de temps répondez-vous ?",
   "Un accusé de réception avec les questions ouvertes sous un jour ouvré. Un prix "
   "rendu sous une dizaine de jours ouvrés sur une ligne que nous exploitons déjà."),
 ],
 "related": ("Pages en français", "Le reste du site est en anglais.",
   [("afrique-ouest.html", "Afrique de l’Ouest", "Programmes frigorifiques vers Lomé et Cotonou."),
    ("decoupes-volaille.html", "Découpes de volaille", "Aile, manchon, aileron."),
    ("certificat-veterinaire.html", "Certificat vétérinaire", "L’agrément avant le prix."),
    ("index.html", "Site en anglais", "Toutes les lignes et tous les guides.")]),
 "ld": [{"@context": "https://schema.org", "@type": "ContactPage",
         "url": HOST + "contact-fr.html", "inLanguage": "fr", "mainEntity": ORG}],
},
]

FORM_FR = """<aside class="cform" id="enquiry">
  <span class="eyebrow">Envoyer un besoin</span>
  <form id="cf" novalidate>
    <label for="f-product">Produit ou &eacute;quipement</label>
    <input id="f-product" type="text" autocomplete="off" placeholder="Ce qu&rsquo;il vous faut, avec vos mots">
    <label for="f-qty">Quantit&eacute;</label>
    <input id="f-qty" type="text" autocomplete="off" placeholder="Conteneurs, tonnes, pi&egrave;ces">
    <label for="f-port">Port ou ville de destination</label>
    <input id="f-port" type="text" autocomplete="off" placeholder="O&ugrave; cela doit arriver">
    <label for="f-terms">Conditions souhait&eacute;es</label>
    <select id="f-terms">
      <option>&Agrave; conseiller</option><option>FOB</option><option>CFR</option>
      <option>CIF</option><option>FCA</option><option>DAP</option>
    </select>
    <label for="f-note">Autres pr&eacute;cisions</label>
    <textarea id="f-note" placeholder="Cahier des charges, norme, certification, d&eacute;lai"></textarea>
    <button class="btn" type="submit">R&eacute;diger le courriel</button>
    <p class="cresult" id="cf-out" hidden></p>
  </form>
</aside>"""

for _p in PAGES_FR:
    if _p["slug"] == "contact-fr":
        _p["hero_right"] = FORM_FR

# пары страниц для hreflang: английская, французская
HREFLANG = [("index.html", "fr.html"),
            ("west-africa.html", "afrique-ouest.html"),
            ("poultry-cuts.html", "decoupes-volaille.html"),
            ("veterinary-certificate.html", "certificat-veterinaire.html"),
            ("contact.html", "contact-fr.html")]
