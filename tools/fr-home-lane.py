# -*- coding: utf-8 -*-
"""Переводит французскую главную на одну полосу: допустимость груза и
франкоязычная Западная Африка.

Чем это обосновано, по порядку доказательной силы.

**Замер.** Search Console за 28 дней до 7 ноября 2026: весь сайт это
1 095 показов, 6 кликов, 0,55 процента, средняя позиция 23,5. Внутри
этого уже есть выбравший себя рынок: afrique-ouest на позиции **1,0**,
west-africa с CTR 14,3 процента, decoupes-volaille 9,1,
veterinary-certificate 6,2, contact-fr на позиции 5,5. Главный экран при
этом вёл шестью категориями, ни одна из которых не та, откуда идут
клики. Предложение и покупатель находились на разных страницах одного
сайта.

**Совет директоров.** Три рамки из трёх поставили отсутствие выбранного
рынка первым пунктом. Рамка Monopoly: позиция 1,0 это единственный
монопольный факт во всём разборе. Рамка Offers: предложение идёт после
рынка, а рынок не был выбран.

**Панель.** Из ста смоделированных покупателей «Admissibility before
price» оказалась единственной строчкой сайта, которую назвали
работающей, и назвали её те, у кого груз когда-то задержали. Остальные
три утверждения либо не упоминались, либо, как «Principal, not a
broker», сработали против.

Что меняется. Заголовок «DITES-NOUS LE PRODUIT. NOUS LE LIVRONS.»
уступает место утверждению, которое сработало. Лид говорит, чем мы
закрываем недоверие: собственное имя в контракте, документы на нас,
платёж против документов. Ниже первого экрана появляется полоса из трёх
стран ввоза, со ссылками на разбор документного комплекта каждой.

Чего не делаем. Шесть категорий остаются на месте, ниже. Английскую
главную не трогаем: просили переписать французскую.

Запуск: python3.13 tools/fr-home-lane.py
Повторный запуск ничего не дублирует.
"""
import pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
HOME = SITE / "fr" / "index.html"

# Отступ в собранной странице двенадцать пробелов, а не десять: образец
# должен совпадать с файлом побайтно, иначе замена молча не срабатывает.
IND = "\n" + " " * 12
H1_OLD = IND.join(['<span class="ln"><span>DITES-NOUS</span></span>',
                   '<span class="ln"><span>LE PRODUIT.</span></span>',
                   '<span class="ln"><span>NOUS LE LIVRONS.</span></span>'])

H1_NEW = IND.join(['<span class="ln"><span>L’ADMISSIBILITÉ</span></span>',
                   '<span class="ln"><span>AVANT</span></span>',
                   '<span class="ln"><span>LE PRIX.</span></span>'])

LEAD_OLD = ("Biens industriels, matériaux de construction, équipements, "
            "emballages et denrées. Nous trouvons le producteur, le "
            "vérifions, achetons en notre propre nom et livrons à votre "
            "port. Négociant pour compte propre, pas courtier.")

LEAD_NEW = ("Une offre d’un producteur qui ne peut pas légalement "
            "expédier vers votre pays n’est pas une offre, quel que soit "
            "le chiffre dessus. Nous achetons en notre propre nom, nous portons "
            "le dossier documentaire jusqu’à votre port, et quand votre "
            "banque l’exige nous travaillons contre documents.")

CARDS = [
 ("/admissibilite-cote-divoire", "01", "Côte d’Ivoire",
  "Abidjan, San Pedro", "port-cma",
  "/media/port-cma-349.c4f1b5ba.webp 349w, /media/port-cma.20962826.webp 552w",
  "/media/port-cma-349.c4f1b5ba.webp",
  "Porte-conteneurs à quai sur un terminal"),
 ("/admissibilite-senegal", "02", "Sénégal", "Dakar", "crane-red",
  "/media/crane-red-349.c878dd74.webp 349w, /media/crane-red.03cec0d1.webp 531w",
  "/media/crane-red-349.c878dd74.webp",
  "Portiques au-dessus d’un poste à conteneurs"),
 ("/admissibilite-cameroun", "03", "Cameroun", "Douala, Kribi",
  "containers-wall",
  "/media/containers-wall-349.5186aa08.webp 349w, "
  "/media/containers-wall.17942d5c.webp 546w",
  "/media/containers-wall-349.5186aa08.webp",
  "Conteneurs empilés sur un terre-plein portuaire"),
]

MARK = "<!-- admissibilite:lane -->"

SIZES = "(max-width: 480px) 351px, (max-width: 900px) 731px, 509px"


def card(href, n, title, sub, _key, srcset, src, alt):
    return (
      '<a class="card" href="%s">\n'
      '  <picture><source srcset="%s" sizes="%s" type="image/webp">'
      '<img srcset="%s" sizes="%s" src="%s" alt="%s" loading="lazy" '
      'decoding="async" width="1040" height="1300"></picture>\n'
      '  <span class="n">%s</span>\n'
      '  <span class="cap"><b>%s</b><span>%s</span></span>\n'
      '</a>' % (href, srcset, SIZES, srcset, SIZES, src, alt, n, title, sub))


# Секцию намеренно НЕ объявляем сценой. Разметка сцены (class="scene"
# плюс data-scene) обслуживается скриптом прокрутки страницы, который
# перебирает сцены при загрузке и ведёт их прозрачность по положению в
# окне. Новая сцена в этот перебор не попадает и остаётся приглушённой:
# замерено, заголовок и подпись рисуются вполсилы рядом с #s-cats,
# который на том же фоне graphite выглядит нормально. Обычная секция
# такого обслуживания не требует, а полоса карточек .rail работает и
# без сцены.
SECTION = (MARK + """
<section id="s-lane" data-reveal aria-labelledby="h-lane">
  <div class="stage">
    <div class="rail-head">
      <h2 class="display sm" id="h-lane" style="color:var(--black)">
        <span class="ln"><span>LE DOSSIER, PAYS PAR PAYS.</span></span>
      </h2>
      <p class="lead muted fade" style="margin-top:18px;color:var(--steel-2)">Ce
        qui bloque un conteneur au port, ce n’est presque jamais le prix.
        C’est une pièce manquante que personne n’a réclamée à
        l’origine. Voici qui délivre quoi, et à quel moment.</p>
    </div>
    <div class="rail">
%s
    </div>
  </div>
</section>
""" % "\n".join(card(*c) for c in CARDS))

ANCHOR = "<!-- ============ ПУТЬ ГРУЗА ============ -->"

# Меню французской главной вело шестью пунктами на английские страницы:
# /services, /supply, /corridors, /guides, /about, /contact. То есть
# читатель, которого мы зовём по-французски, из меню попадал в
# английский текст. Плюс строка перестала помещаться: замерено
# переполнение 91 px при окне 1280 после добавления седьмого пункта.
# Заменяем список целиком на французские адреса, которые у сайта есть.
# Доступ к английской версии остаётся через переключатель языка справа.
NAV_NEW = ('<a href="/afrique-ouest">Afrique de l’Ouest</a>\n'
           '    <a href="/admissibilite-cote-divoire">Côte d’Ivoire</a>\n'
           '    <a href="/admissibilite-senegal">Sénégal</a>\n'
           '    <a href="/admissibilite-cameroun">Cameroun</a>\n'
           '    <a href="/decoupes-volaille">Découpes</a>\n'
           '    <a href="/contact-fr">Contact</a>')

# Берём весь список ссылок между открывающим тегом меню и переключателем
# языка, а не конкретную строку: так замена переживает и прежний состав
# меню, и промежуточное состояние, в которое я его уже один раз привёл.
NAV_RE = re.compile(
    r'(<nav class="top-nav"[^>]*>\s*)(.*?)(\s*<div class="langsw")', re.S)

TITLE_OLD = "<title>ISP Group LLC : sourcing et livraison à votre port</title>"
TITLE_NEW = ("<title>Admissibilité avant le prix : importer vers "
             "l’Afrique de l’Ouest</title>")

DESC_OLD = ('<meta name="description" content="ISP GROUP LLC achète la '
            'marchandise en son propre nom et la livre à votre port. '
            'Matériaux, équipements, outillage, métaux, papier et '
            'alimentaire.">')
DESC_NEW = ('<meta name="description" content="Le dossier documentaire qui '
            'décide si un conteneur sort du port, pays par pays : '
            'Côte d’Ivoire, Sénégal, Cameroun. Nous achetons en '
            'notre propre nom et travaillons contre documents.">')


def main():
    s = HOME.read_text()
    orig = s
    steps = []

    if H1_NEW.split("\n")[0] in s:
        steps.append("заголовок уже был")
    elif H1_OLD in s:
        s = s.replace(H1_OLD, H1_NEW, 1)
        steps.append("заголовок")
    else:
        print("  ВНИМАНИЕ: прежний заголовок не найден")

    if LEAD_NEW in s:
        steps.append("лид уже был")
    elif LEAD_OLD in s:
        s = s.replace(LEAD_OLD, LEAD_NEW, 1)
        steps.append("лид")
    else:
        print("  ВНИМАНИЕ: прежний лид не найден")

    if MARK in s:
        steps.append("полоса стран уже была")
    elif ANCHOR in s:
        s = s.replace(ANCHOR, SECTION + ANCHOR, 1)
        steps.append("полоса стран")
    else:
        print("  ВНИМАНИЕ: место для полосы стран не найдено")

    if NAV_NEW in s:
        steps.append("меню уже было")
    elif NAV_RE.search(s):
        s = NAV_RE.sub(lambda m: m.group(1) + NAV_NEW + m.group(3), s, count=1)
        steps.append("меню")
    else:
        print("  ВНИМАНИЕ: меню не найдено, правка не применена")

    if TITLE_OLD in s:
        s = s.replace(TITLE_OLD, TITLE_NEW, 1)
        steps.append("заголовок вкладки")
    if DESC_OLD in s:
        s = s.replace(DESC_OLD, DESC_NEW, 1)
        steps.append("описание")

    if s != orig:
        HOME.write_text(s)
    print("fr/index.html: " + ", ".join(steps))
    return 0


if __name__ == "__main__":
    sys.exit(main())
