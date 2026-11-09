# -*- coding: utf-8 -*-
"""Три страницы допустимости по странам ввоза: Кот-д'Ивуар, Сенегал,
Камерун.

Зачем. Из ста смоделированных покупателей 44 попросили не рассуждение о
документах вообще, а **комплект под свою страну**: какой документ, кем
выпускается, на чьём риске. В группе «нужны правильные бумаги» это 14 из
14. При этом три документных руководства сайта уже дают 305 показов в
Search Console и ноль кликов: текст написан про документ в общем виде,
а человек ищет свой порт. Эти страницы и есть мост.

Откуда взята фактура. Только проверенные источники, и там, где
источники расходятся, на странице стоит оговорка, а не число.

* Сенегал. Всемирная торговая организация, обзор торговой политики
  WT/TPR/S/362, приложение по Сенегалу: BESC обязателен с 2008 года по
  межведомственному приказу № 04350 от 26 мая 2008, выпускается
  Сенегальским советом грузоотправителей (COSEC), требуется для любого
  морского ввоза для местного потребления; программа проверки импорта
  распространяется на все контейнеры и на партии стоимостью от 3 млн
  франков КФА по ФОБ. Оператор программы и пороги в этом обзоре
  зафиксированы на момент его составления, поэтому на странице они
  названы как предмет письменного подтверждения по каждой отгрузке, а
  не как текущая данность.
* Камерун. Официальный сайт Агентства по стандартам и качеству (ANOR):
  программа оценки соответствия до отгрузки учреждена декретом
  № 2015/1875/PM от 1 июля 2015, изменена декретом № 2021/3306/PM от
  31 мая 2021; аттестацию соответствия выдают SGS, Intertek и TÜV
  Rheinland, сертификат соответствия выдаёт и отвечает за него сама
  ANOR; перечень товаров усиленного контроля взят с той же страницы.
  Приостановка BESC для транзита по коридорам Дуала - Нджамена и
  Дуала - Банги объявлена сообщением Национального совета
  грузоотправителей Камеруна от 15 июня 2026; на ввоз в сам Камерун
  приостановка не распространяется.
* Кот-д'Ивуар. Номера декрета и таможенного циркуляра **не ставим**:
  источники дают разные даты одного и того же циркуляра, а
  первоисточник недоступен. Названы только то, что подтверждается:
  орган, выпускающий бордеро (Ивуарийское управление грузоотправителей),
  роль бордеро как условия приемлемости таможенной декларации,
  программа проверки соответствия с сертификатом или отчётом о
  несоответствии, и национальный орган по стандартам CODINORM.

Почему на страницах нет ни цен, ни сроков в днях. По всем трём странам
коммерческие сайты называют разные сроки подачи и разные тарифы, а
первоисточники их не подтверждают. Поставить такое число значит сделать
ровно то, за что покупатель перестаёт верить странице, когда проверит.
Вместо числа на странице стоит обещание подтвердить его письменно по
конкретной отгрузке, и это и есть то, что продаётся.

Как устроено. Страницы собираются из уже собранной afrique-ouest.html:
она французская, у неё верная шапка, подвал, стили и разметка. Меняется
голова, шапка статьи и содержимое main. Полная пересборка не
запускается.

Запуск: python3.13 tools/admissibility-pages.py
Повторный запуск переписывает страницы тем же содержимым.
"""
import pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
SHELL = SITE / "afrique-ouest.html"
HOST = "https://ispgroupgc.com"

HERO_IMG = {
 "admissibilite-cote-divoire": (
   'media/port-cma.20962826.webp',
   'media/port-cma-349.c4f1b5ba.webp 349w, media/port-cma.20962826.webp 552w',
   "Porte-conteneurs à quai sur un terminal"),
 "admissibilite-senegal": (
   'media/crane-red.03cec0d1.webp',
   'media/crane-red-349.c878dd74.webp 349w, media/crane-red.03cec0d1.webp 531w',
   "Portiques au-dessus d’un poste à conteneurs"),
 "admissibilite-cameroun": (
   'media/containers-wall.17942d5c.webp',
   'media/containers-wall-349.5186aa08.webp 349w, media/containers-wall.17942d5c.webp 546w',
   "Conteneurs empilés sur un terre-plein portuaire"),
}

# Общий для трёх страниц разбор: кто несёт риск и как платим. Текст
# одинаковый намеренно: это обязательство компании, и оно не может
# звучать по-разному в зависимости от страны.
RISK = ("Qui porte le risque, et jusqu’où", [
 "<p>Nous achetons la marchandise en notre nom propre et nous la revendons. "
 "Vous avez un contrat, un interlocuteur et une facture. Concrètement, "
 "constituer le dossier à l’origine, relancer le producteur sur les "
 "attestations et vérifier que le connaissement, la facture et les "
 "certificats disent la même chose est notre travail, pas le vôtre.</p>",
 "<p>Ce que nous ne promettons pas : la décision d’une administration. "
 "Personne ne peut la garantir, et un vendeur qui la garantit vous apprend "
 "quelque chose sur lui. Ce que nous engageons, c’est que le dossier parte "
 "complet et conforme à ce que la destination exige au moment du "
 "chargement, et que vous le voyiez avant que la marchandise ne bouge.</p>",
 "<p class=\"pnote\">La société est enregistrée aux États-Unis sous "
 "les références UEI WA46PAMTYMQ7 et CAGE 217F4, et vos demandes sont traitées par "
 "Aleksandr Orlov, Member. Ces numéros sont publics : vérifiez-les "
 "vous-même plutôt que de nous croire sur parole.</p>"])

PAY = ("Le paiement contre documents", [
 "<p>Nous ne facturons pas la cotation et nous ne demandons pas d’acompte "
 "pour étudier un dossier.</p>",
 "<p>Sur la transaction elle-même, quand votre banque l’exige, nous "
 "travaillons sous crédit documentaire payable à vue contre "
 "présentation du jeu de documents, ou en remise documentaire. "
 "L’argent ne quitte votre banque que lorsque les documents sont "
 "présentés et conformes.</p>",
 "<p>Nous le proposons pour une raison précise. Nous n’avons pas encore "
 "d’acheteur dans votre pays que vous puissiez appeler, et nous ne "
 "fabriquerons pas de référence pour en avoir une. Une structure de "
 "paiement que votre propre banque contrôle est la seule garantie qu’un "
 "vendeur sans historique chez vous puisse honnêtement offrir.</p>"])

# Предотгрузочная инспекция внутри комплекта по аккредитиву.
# Панель: аккредитив обсуждают 76 процентов и 100 процентов из 38 обожжённых
# трейдером, но 26 процентов обожжённых говорят одно и то же: **аккредитив
# платит против документов, а не против товара.** Комплект чистый, контейнер
# не тот. Сами покупатели называют решение, 18 процентов панели назвали SGS,
# Intertek или TÜV поимённо.
# Правка стоит ноль, потому что инспекция уже в цепочке у всех трёх стран.
# Органы названы поимённо только там, где это подтверждено первоисточником,
# то есть по Камеруну. По Кот-д'Ивуару и Сенегалу названа программа и
# обещано письменное подтверждение органа до открытия аккредитива.
INSPECT_COMMON = (
 "<p>Reste l’objection qui vient ensuite, et elle est juste : un crédit "
 "documentaire paie contre des documents, pas contre la marchandise. Le "
 "jeu peut être propre et le conteneur mauvais. C’est pourquoi nous "
 "faisons figurer dans le jeu exigé par le crédit un certificat "
 "d’inspection avant expédition délivré par un tiers nommé, et nous en "
 "faisons une condition de paiement. L’organisme est désigné dans le "
 "crédit avant le chargement, pas discuté après l’arrivée.</p>")

INSPECT = {
 "admissibilite-cote-divoire":
   "<p>Cela ne rajoute pas une étape à votre dossier : le contrôle avant "
   "embarquement décrit plus haut est déjà prévu pour les produits "
   "réglementés. Nous ne faisons que l’attacher au paiement. L’organisme "
   "mandaté et le champ exact du contrôle vous sont confirmés par écrit "
   "pour votre expédition avant l’ouverture du crédit.</p>",
 "admissibilite-senegal":
   "<p>Cela ne rajoute pas une étape à votre dossier : la vérification des "
   "importations décrite plus haut couvre déjà les conteneurs et les "
   "cargaisons à partir du seuil FOB rappelé ci-dessus. Nous ne faisons que "
   "l’attacher au paiement. L’organisme retenu et le champ exact du "
   "contrôle vous sont confirmés par écrit pour votre expédition avant "
   "l’ouverture du crédit.</p>",
 "admissibilite-cameroun":
   "<p>Cela ne rajoute pas une étape à votre dossier : l’évaluation de la "
   "conformité avant embarquement est déjà obligatoire, et l’attestation "
   "de conformité est délivrée par SGS, Intertek ou TÜV Rheinland. Nous ne "
   "faisons que nommer l’organisme dans le crédit et attacher son "
   "certificat au paiement.</p>",
}

PAGES = [
{
 "slug": "admissibilite-cote-divoire",
 "crumb": "Côte d’Ivoire",
 "title": "Côte d’Ivoire : le dossier à l’import | Abidjan, San Pedro",
 "desc": "Bordereau de suivi des cargaisons, certificat de conformité avant "
         "embarquement, documents sanitaires. Qui délivre quoi, et à quel "
         "moment, pour un conteneur à destination d’Abidjan.",
 "ogtitle": "Côte d’Ivoire : le dossier documentaire à l’import",
 "h1": "Côte d’Ivoire : ce qui décide <em>si le conteneur sort du port</em>",
 "sub": "Un prix se renégocie, un conditionnement se change, une date glisse. "
        "Un dossier incomplet à l’arrivée ne se rattrape pas : la "
        "marchandise reste au port, et le stationnement est pour vous.",
 "chips": ["Abidjan", "San Pedro", "BSC", "Certificat de conformité",
           "Principal, <b>pas courtier</b>"],
 "lede": ("Ce n’est pas la facture qui fait entrer la marchandise",
   "Trois dossiers distincts décident de l’entrée : le suivi de "
   "cargaison, la conformité vérifiée avant embarquement et, pour les "
   "denrées animales, l’agrément de l’établissement. Trois "
   "organismes différents, et aucun des trois ne se rattrape une fois le "
   "navire parti."),
 "brief": [
  ("Le bordereau conditionne la déclaration.",
   "Le bordereau de suivi des cargaisons est géré par l’Office "
   "ivoirien des chargeurs. Sans lui au dossier, la déclaration en détail "
   "n’est pas recevable, quelle que soit la facture."),
  ("La conformité se prouve avant l’embarquement.",
   "Les produits réglementés entrent sur un certificat de conformité "
   "établi avant le départ du navire. Un dossier refusé donne un "
   "rapport de non-conformité, qui ne remplace rien."),
  ("Pour les denrées animales, l’agrément passe avant le prix.",
   "Il est accordé établissement par établissement et pays par pays. "
   "Un établissement agréé pour le voisin ne l’est pas ici."),
  ("Les délais et les barèmes changent.",
   "Nous les faisons confirmer par écrit pour chaque expédition plutôt "
   "que de les recopier d’une page web, la nôtre comprise."),
 ],
 "prose": [
  ("Le bordereau de suivi des cargaisons", [
   "<p>Le bordereau de suivi des cargaisons est géré par l’Office "
   "ivoirien des chargeurs et couvre les mouvements maritimes à l’import "
   "comme à l’export. Son numéro doit figurer au dossier "
   "d’importation, et la douane en fait une condition de recevabilité de "
   "la déclaration en détail. La nuance compte : une déclaration "
   "déposée sans lui n’est pas rejetée sur le fond, elle "
   "n’est pas reçue.</p>",
   "<p>Ce qui en découle en pratique : le bordereau ne se règle pas "
   "à l’arrivée. Il s’ouvre à l’origine, sur la base du "
   "connaissement, de la facture et de la liste de colisage, donc il "
   "dépend de pièces que le producteur doit fournir à temps. "
   "C’est la raison pour laquelle nous réclamons ces trois pièces "
   "avant de confirmer une date de chargement, et non après.</p>"]),
  ("La conformité vérifiée avant embarquement", [
   "<p>Les produits réglementés relèvent du programme de "
   "vérification de la conformité. Le contrôle a lieu avant "
   "l’embarquement, il est conduit par des sociétés mandatées par "
   "le ministère en charge du commerce, et il se conclut de deux "
   "façons : un certificat de conformité, ou un rapport de "
   "non-conformité. Le certificat fait partie des pièces exigées au "
   "dédouanement. Le rapport, lui, ne remplace rien.</p>",
   "<p>Deux conséquences. La charge documentaire repose sur "
   "l’exportateur : c’est lui qui produit les rapports d’essai et les "
   "attestations qualité. Et un producteur qui n’a jamais expédié "
   "vers la Côte d’Ivoire n’a pas ce réflexe, ce qui est "
   "précisément le moment où un programme déraille. La "
   "normalisation nationale relève de CODINORM.</p>"]),
  ("Les denrées animales et l’agrément", [
   "<p>Pour la viande et les produits de la pêche, la pièce qui décide "
   "est le certificat sanitaire vétérinaire, délivré par "
   "l’autorité compétente du pays exportateur pour un établissement "
   "précis. Ce n’est pas un document commercial et le vendeur ne peut "
   "pas l’émettre.</p>",
   "<p>Le détail figure sur la page <a href=\"certificat-veterinaire\">"
   "certificat vétérinaire</a>, la nomenclature des découpes sur "
   "<a href=\"decoupes-volaille\">découpes de volaille</a>, et la ligne "
   "frigorifique complète sur <a href=\"afrique-ouest\">Afrique de "
   "l’Ouest</a>.</p>"]),
  RISK, PAY,
 ],
},
{
 "slug": "admissibilite-senegal",
 "crumb": "Sénégal",
 "title": "Sénégal : le dossier à l’import | port de Dakar",
 "desc": "Bordereau électronique de suivi des cargaisons du COSEC, programme de "
         "vérification des importations, normes de l’ASN. Qui délivre "
         "quoi pour un conteneur à destination de Dakar.",
 "ogtitle": "Sénégal : le dossier documentaire à l’import",
 "h1": "Sénégal : le dossier qui <em>précède le navire</em>",
 "sub": "Le bordereau est exigible pour toute importation maritime destinée "
        "à la mise à la consommation, et il conditionne la recevabilité "
        "de la déclaration. Il s’établit avant, pas après.",
 "chips": ["Dakar", "BESC", "COSEC", "Vérification des importations",
           "Principal, <b>pas courtier</b>"],
 "lede": ("Le texte est public, et il est plus précis que la plupart des pages "
   "qui le commentent",
   "Le bordereau électronique de suivi des cargaisons est obligatoire depuis "
   "2008. Il est établi par le Conseil sénégalais des chargeurs et "
   "exigible pour toute importation par voie maritime destinée à la mise "
   "à la consommation locale. Le transit en est exempté."),
 "brief": [
  ("Obligatoire depuis 2008, par arrêté.",
   "L’arrêté interministériel n° 04350 du 26 mai 2008 institue le "
   "bordereau de suivi des cargaisons. Le bordereau est établi par le "
   "Conseil sénégalais des chargeurs."),
  ("Il vise la mise à la consommation, pas le transit.",
   "Exigible pour toute importation par voie maritime destinée à la "
   "consommation locale ; les marchandises en transit en sont exemptées."),
  ("La vérification des importations s’applique à tous les conteneurs.",
   "Et aux cargaisons dont la valeur FOB atteint 3 millions de francs CFA. "
   "Elle porte sur la qualité, la quantité, les documents, le classement "
   "tarifaire et la valeur en douane."),
  ("Opérateur et barèmes se vérifient à la date de l’expédition.",
   "La société chargée du programme et les seuils figurent dans des "
   "textes qui évoluent. Nous les faisons confirmer par écrit, par "
   "expédition."),
 ],
 "prose": [
  ("Le bordereau électronique de suivi des cargaisons", [
   "<p>L’arrêté interministériel n° 04350 du 26 mai 2008 institue le "
   "bordereau de suivi des cargaisons et impose au chargeur, ou à son "
   "mandataire, de l’établir et de le faire valider auprès du Conseil "
   "sénégalais des chargeurs. Il est exigible pour toute importation "
   "par voie maritime destinée à la mise à la consommation locale ; "
   "les marchandises en transit en sont exemptées.</p>",
   "<p>Deux points que les pages commerciales rendent mal. Le bordereau "
   "conditionne la recevabilité de la déclaration en douane, ce qui en "
   "fait une pièce du dossier et non une formalité annexe. Et le "
   "Conseil peut refuser de valider un bordereau dont les mentions lui "
   "paraissent peu crédibles, ce qui vise directement les factures "
   "sous-évaluées : un dossier incohérent se paie à "
   "l’établissement du bordereau, avant même la douane.</p>"]),
  ("La vérification des importations", [
   "<p>Le Sénégal maintient un programme de vérification des "
   "importations applicable à tous les conteneurs, ainsi qu’aux "
   "cargaisons dont la valeur FOB atteint 3 millions de francs CFA. "
   "L’inspection porte notamment sur la qualité et la quantité, la "
   "vérification documentaire, le classement tarifaire et la valeur en "
   "douane.</p>",
   "<p>Pour un acheteur, la conséquence pratique n’est pas le "
   "contrôle lui-même : c’est que le classement et la valeur retenus "
   "à ce stade déterminent les droits. Une désignation approximative "
   "sur la facture coûte plus cher qu’une remise obtenue à la "
   "négociation.</p>",
   "<p>La société chargée du programme, les seuils et les pièces "
   "exigées relèvent d’un contrat et de textes qui se renouvellent. "
   "Nous ne les recopions pas : nous les faisons confirmer par écrit "
   "pour l’expédition en cours.</p>"]),
  ("Les normes nationales et les denrées", [
   "<p>Pour un produit couvert par une norme sénégalaise, la "
   "certification relève de l’Association sénégalaise de "
   "normalisation, sur dossier technique et rapports d’essai. Le fer "
   "à béton, la farine de blé, l’huile raffinée, le concentré "
   "de tomate et le sel iodé figurent parmi les produits "
   "concernés.</p>",
   "<p>Pour la viande et les produits de la pêche, le document qui "
   "décide reste le certificat sanitaire vétérinaire délivré "
   "pour un établissement agréé pour la destination. Voir "
   "<a href=\"certificat-veterinaire\">certificat vétérinaire</a> et "
   "<a href=\"afrique-ouest\">Afrique de l’Ouest</a>.</p>"]),
  RISK, PAY,
 ],
},
{
 "slug": "admissibilite-cameroun",
 "crumb": "Cameroun",
 "title": "Cameroun : le dossier à l’import | Douala, Kribi",
 "desc": "Bordereau électronique de suivi des cargaisons du CNCC et programme "
         "d’évaluation de la conformité avant embarquement de l’ANOR. "
         "Qui délivre quoi pour un conteneur à destination de Douala.",
 "ogtitle": "Cameroun : le dossier documentaire à l’import",
 "h1": "Cameroun : la conformité <em>se prouve avant le chargement</em>",
 "sub": "Le certificat de conformité s’obtient en deux temps et par deux "
        "organismes distincts. Il s’attache aux documents d’embarquement, "
        "ce qui veut dire qu’il ne se rattrape pas en mer.",
 "chips": ["Douala", "Kribi", "BESC", "PECAE", "ANOR",
           "Principal, <b>pas courtier</b>"],
 "lede": ("Deux organismes, deux documents, un seul ordre possible",
   "Un organisme accrédité délivre l’attestation de conformité, "
   "puis l’Agence des normes et de la qualité émet le certificat de "
   "conformité et en répond. L’ordre n’est pas administratif : "
   "l’attestation s’obtient avant l’embarquement, donc avant que la "
   "marchandise ne quitte le pays d’origine."),
 "brief": [
  ("Le programme a une base réglementaire datée.",
   "Décret n° 2015/1875/PM du 1er juillet 2015, modifié par le décret "
   "n° 2021/3306/PM du 31 mai 2021."),
  ("Deux étapes, deux organismes.",
   "SGS, Intertek ou TÜV Rheinland délivrent l’attestation de "
   "conformité ; l’ANOR émet le certificat de conformité et en est "
   "entièrement responsable."),
  ("Les denrées sont en contrôle renforcé.",
   "Produits animaux et de la pêche, produits laitiers, céréales et "
   "dérivés, huiles alimentaires, sucre, produits agricoles frais, "
   "engrais et intrants, cosmétiques, électroménager et "
   "électronique, biens d’occasion."),
  ("Le bordereau reste exigé à l’import.",
   "Sa suspension annoncée le 15 juin 2026 vise le transit sur les "
   "corridors Douala - Ndjamena et Douala - Bangui, pas les marchandises "
   "dont la destination finale est le Cameroun."),
 ],
 "prose": [
  ("L’évaluation de la conformité avant embarquement", [
   "<p>Le programme a été institué par le décret n° 2015/1875/PM du "
   "1er juillet 2015, modifié par le décret n° 2021/3306/PM du 31 mai "
   "2021. Il se déroule en deux temps : un organisme accrédité par "
   "l’Agence des normes et de la qualité, SGS, Intertek ou TÜV "
   "Rheinland, délivre l’attestation de conformité ; l’Agence "
   "émet ensuite le certificat de conformité, dont elle est "
   "entièrement responsable.</p>",
   "<p>Le certificat s’attache aux documents d’embarquement. C’est "
   "le point que les acheteurs découvrent trop tard : l’attestation "
   "doit être obtenue avant le chargement, donc le producteur doit "
   "avoir ses rapports d’essai prêts avant la date de départ, et "
   "non au moment où la marchandise est déjà en mer.</p>"]),
  ("Les produits en contrôle renforcé", [
   "<p>L’Agence place en inspection renforcée, entre autres, le sucre, "
   "les céréales et produits dérivés, les engrais et intrants "
   "agricoles, les produits animaux et de la pêche, les produits "
   "laitiers, les produits agricoles frais, les biens d’occasion, les "
   "équipements électriques et électroniques, les huiles "
   "alimentaires et les cosmétiques et produits d’hygiène.</p>",
   "<p>Autrement dit : la quasi-totalité de ce qui se commande en "
   "conteneur alimentaire est dans la catégorie la plus contrôlée. "
   "Pour la viande et la pêche, le certificat sanitaire "
   "vétérinaire délivré pour un établissement agréé "
   "s’ajoute à ce dispositif, il ne s’y substitue pas. Voir "
   "<a href=\"certificat-veterinaire\">certificat vétérinaire</a>.</p>"]),
  ("Le bordereau électronique de suivi des cargaisons", [
   "<p>Le bordereau est en vigueur au Cameroun depuis le 11 juillet 2006 "
   "et relève du Conseil national des chargeurs du Cameroun. Il sert "
   "à l’identification de la marchandise, au contrôle du coût du "
   "transport et à la traçabilité.</p>",
   "<p>Une précision d’actualité, parce qu’elle circule mal. Le "
   "Conseil a annoncé le 15 juin 2026 la suspension du bordereau pour "
   "les marchandises <b>en transit</b> sur les corridors "
   "Douala - Ndjamena et Douala - Bangui, à la suite des "
   "recommandations du forum tripartite Tchad - Cameroun - RCA. Une "
   "marchandise dont la destination finale est le Cameroun n’est pas "
   "concernée par cette suspension.</p>"]),
  RISK, PAY,
 ],
},
]

OTHERS = {
 "admissibilite-cote-divoire": [("admissibilite-senegal", "Sénégal"),
                                ("admissibilite-cameroun", "Cameroun")],
 "admissibilite-senegal": [("admissibilite-cote-divoire", "Côte d’Ivoire"),
                           ("admissibilite-cameroun", "Cameroun")],
 "admissibilite-cameroun": [("admissibilite-cote-divoire", "Côte d’Ivoire"),
                            ("admissibilite-senegal", "Sénégal")],
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") \
            .replace('"', "&quot;")


def build_main(p):
    out = ['<main id="main" tabindex="-1">', '<section data-reveal><div class="wrap">']
    h2, intro = p["lede"]
    out.append('<div class="lede"><h2>%s</h2><p class="intro">%s</p></div>' % (h2, intro))

    out.append('<div class="answer">\n<h2>En bref</h2>\n<ol class="alist">')
    for b, t in p["brief"]:
        out.append("<li><b>%s</b> %s</li>" % (b, t))
    out.append("</ol>\n</div>")

    out.append('<nav class="toc" aria-label="Sur cette page"><ol>')
    for i, (head, _) in enumerate(p["prose"], 1):
        out.append('<li><a href="#s%d"><span>%02d</span>%s</a></li>' % (i, i, head))
    out.append("</ol></nav>")

    out.append('<div class="prose">')
    for i, (head, paras) in enumerate(p["prose"], 1):
        if head == PAY[0]:
            paras = paras[:2] + [INSPECT_COMMON, INSPECT[p["slug"]]] + paras[2:]
        out.append('<div class="pblock"><span class="k">%02d</span>'
                   '<h2 id="s%d">%s</h2><div class="ptext">%s</div></div>'
                   % (i, i, head, "".join(paras)))
    out.append("</div>")

    out.append('<div class="lede" style="margin-top:56px"><h2>Les autres destinations</h2>'
               '<p class="intro">Le dossier change avec le pays, pas avec le produit.</p></div>'
               '<div class="lanelinks">')
    for slug, name in OTHERS[p["slug"]]:
        out.append('<a class="lanelink" href="%s"><b>%s</b>'
                   '<span>Le dossier documentaire à l’import.</span></a>' % (slug, name))
    out.append('<a class="lanelink" href="afrique-ouest"><b>Afrique de l’Ouest</b>'
               '<span>La ligne frigorifique, de bout en bout.</span></a></div>')

    out.append("</div></section>")
    out.append('<section data-reveal class="cta"><div class="wrap"><div class="lede">'
               '<h2>Dites-nous le produit et le port. Vous recevez le dossier exigé.</h2>'
               '<p class="intro">Avant toute discussion de prix : la liste des pièces '
               'pour votre destination, qui les délivre, et ce qui reste à votre '
               'charge.</p></div><div class="ctarow">'
               '<a class="btn" href="contact-fr#enquiry">Demander un devis</a>'
               '<span class="mail">info@ispgroupgc.com</span></div></div></section>')
    out.append("</main>")
    return "\n".join(out)


def build_hero(p):
    img, srcset, alt = HERO_IMG[p["slug"]]
    chips = "".join('<span class="chip">%s</span>' % c for c in p["chips"])
    return (
      '<header class="hero chero" id="top">\n  <div class="wrap chero-g">\n    <div>\n'
      '      <nav class="crumbs" aria-label="Breadcrumb"><a href="/fr/">ISP Group</a> '
      '<span>/</span> <b>%s</b></nav>\n\n'
      '      <h1>%s</h1>\n'
      '      <p class="sub">%s</p>\n'
      '      <div class="chips">%s</div>\n'
      '      <div class="ctarow" style="margin-top:28px">'
      '<a class="btn" href="contact-fr#enquiry">Demander un devis</a></div>\n'
      '    </div>\n'
      '    <div class="heroside"><div class="shot"><span class="pz">'
      '<img src="%s" srcset="%s" sizes="(max-width: 480px) 349px, '
      '(max-width: 900px) 731px, 509px" width="1040" height="1300" alt="%s" '
      'fetchpriority="high" decoding="async"></span></div></div>\n'
      '  </div>\n  <span class="scroll-cue" aria-hidden="true">Scroll</span>\n</header>'
      % (p["crumb"], p["h1"], p["sub"], chips, img, srcset, esc(alt)))


def build_page(shell, p):
    s = shell
    url = "%s/%s" % (HOST, p["slug"])

    # Голова
    s = re.sub(r'<meta name="description" content="[^"]*">',
               '<meta name="description" content="%s">' % esc(p["desc"]), s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">',
               '<link rel="canonical" href="%s">' % url, s, count=1)
    # Английской версии у этих страниц нет: самоссылка вместо чужого x-default
    s = re.sub(r'(?s)<link rel="alternate" hreflang="en"[^>]*>\s*'
               r'<link rel="alternate" hreflang="fr"[^>]*>\s*'
               r'<link rel="alternate" hreflang="x-default"[^>]*>',
               '<link rel="alternate" hreflang="fr" href="%s">' % url, s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*">',
               '<meta property="og:url" content="%s">' % url, s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">',
               '<meta property="og:title" content="%s">' % esc(p["ogtitle"]), s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">',
               '<meta property="og:description" content="%s">' % esc(p["desc"]), s, count=1)
    s = re.sub(r'<meta property="og:image" content="[^"]*">',
               '<meta property="og:image" content="%s/%s">'
               % (HOST, HERO_IMG[p["slug"]][0]), s, count=1)
    s = re.sub(r'(?s)<title>.*?</title>', '<title>%s</title>' % p["title"], s, count=1)

    # Шапка статьи и содержимое
    s = re.sub(r'(?s)<header class="hero chero".*?</header>', lambda m: build_hero(p), s, count=1)
    s = re.sub(r'(?s)<main id="main".*?</main>', lambda m: build_main(p), s, count=1)

    # Текущий пункт меню снимаем: этих страниц в меню нет
    s = s.replace(' aria-current="page"', '')

    # Разметка данных страницы-образца описывает другую статью. Снимаем её
    # целиком: ложная разметка хуже отсутствующей.
    s = re.sub(r'(?s)<script type="application/ld\+json">.*?</script>\s*', '', s)
    return s


# В собранных страницах французские буквы стоят html-сущностями, а не
# символами. Образец должен совпадать с файлом, а не с тем, как текст
# читается на экране, иначе замена молча не находит ничего.
FOOT_OLD = ('<a href="certificat-veterinaire" style="display:block">'
            'Certificat v&eacute;t&eacute;rinaire</a>')
FOOT_NEW = (FOOT_OLD
            + '<a href="admissibilite-cote-divoire" style="display:block">'
              'C&ocirc;te d&rsquo;Ivoire : le dossier</a>'
              '<a href="admissibilite-senegal" style="display:block">'
              'S&eacute;n&eacute;gal : le dossier</a>'
              '<a href="admissibilite-cameroun" style="display:block">'
              'Cameroun : le dossier</a>')


def sitemap():
    """Карта сайта собирается отдельным шагом полной сборки, которую
    запускать нельзя. Поэтому новые адреса вносим сюда сами: без них
    страницы не уходят ни в IndexNow (он читает этот же список), ни в
    обход поисковика."""
    f = SITE / "sitemap.xml"
    if not f.exists():
        print("  ВНИМАНИЕ: sitemap.xml не найден")
        return 0
    s = f.read_text()
    today = __import__("datetime").date.today().isoformat()
    added = 0
    for p in PAGES:
        loc = "%s/%s" % (HOST, p["slug"])
        if "<loc>%s</loc>" % loc in s:
            continue
        row = ('  <url><loc>%s</loc><lastmod>%s</lastmod>'
               '<changefreq>monthly</changefreq><priority>0.8</priority></url>\n'
               % (loc, today))
        s = s.replace("</urlset>", row + "</urlset>", 1)
        added += 1
    if added:
        f.write_text(s)
    return added


def main():
    shell = SHELL.read_text()
    for p in PAGES:
        out = SITE / (p["slug"] + ".html")
        out.write_text(build_page(shell, p))
        print("  %s" % out.name)

    foot = 0
    for p in sorted(SITE.rglob("*.html")):
        s = p.read_text()
        if FOOT_OLD not in s or "admissibilite-senegal" in s.split("<footer")[-1]:
            continue
        p.write_text(s.replace(FOOT_OLD, FOOT_NEW, 1))
        foot += 1

    sm = sitemap()
    print("страниц собрано: %d, подвалов со ссылками: %d, в карту сайта: %d"
          % (len(PAGES), foot, sm))
    return 0


if __name__ == "__main__":
    sys.exit(main())
