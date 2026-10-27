# -*- coding: utf-8 -*-
"""Страница поставочных референсов: объекты, в которые ушёл наш товар.

Зачем она нужна. Внешний аудит поставил доказательствам 5,8 из 10 и был
прав: на сайте не было ни одного объекта, ни одного снимка, ничего, что
нельзя написать про любую торговую компанию. Это самая дорогая дыра,
потому что покупателя до первого заказа убеждает не каталог.

Где проходит граница, и почему она важнее самой страницы. Объекты
построили подрядчики, которые у нас покупали. Мы не строили ничего. Сайт
только что чистили от завышений: аудит нашёл и «двадцать лет» у компании,
которой столько нет, и «на пятую часть и больше» без источника, и
«пошлина включена» там, где по DAP её платит покупатель. Поставить теперь
чужие объекты как свои значит вернуть всё обратно и в худшем виде, потому
что проверяется это одним звонком. Поэтому формулировка на странице везде
одна: мы купили и привезли, построил другой.

Снимки взяты из презентаций, которые дал владелец: подрядной по объектам
в России и девелоперской по Бали. Второй комплект это визуализации, а не
фотографии готовых вилл, и на странице так и написано: выдать рендер за
снимок объекта это то же завышение, только картинкой.

Цифры в подписях взяты из презентации подрядчика и отнесены к объекту, а
не к нашей поставке. Сколько именно поставили мы, не публикуется: это
принадлежит покупателю, а не нам.

Как собирается. Не общим сборщиком. Сборщик берёт тексты из content_*.py,
а там лежат версии до правок аудита: запуск вернул бы на about «in your
own jurisdiction», а на services «на пятую часть и больше». Поэтому
скелет страницы, шапка, подвал, шрифты и поиск берутся из готовой
about.html, а меняется только голова и содержимое.

Запуск: python3.13 tools/projects-page.py
Повторный запуск перезаписывает страницу тем же содержимым.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
os.chdir(ROOT)

import search_mod as SRCH

SITE = "site"
HOST = "https://ispgroupgc.com/"
SLUG = "projects"
DONOR = os.path.join(SITE, "about.html")
OUT = os.path.join(SITE, SLUG + ".html")

TITLE = "Supply references: steel, formwork and plant from China"
OG_TITLE = "Goods we bought, and the sites they went into"
DESC = ("Projects our team supplied into: structural steel, formwork, inert materials "
        "and the machinery fleet from China, bridge equipment from the European Union, "
        "finishes and pool plant to Bali.")
OG_IMG = "ref-bridge.jpg"
OG_ALT = "Steel truss railway bridge standing on new concrete abutments"

# ─── снимки ────────────────────────────────────────────────────────────────
# Ширины файлов, которые нарезал tools/ref-photos.py. Верхняя ступень лежит
# под именем без суффикса, остальные с суффиксом ширины.
STEPS = [390, 760]
# Замер сетки: во всю полосу колонок выходит три, плитка около 380 точек, на
# планшете две, на телефоне одна во всю ширину за вычетом полей. Ширина
# показа здесь указана честно: браузер сам возьмёт ступень 760 на экране
# двойной плотности и 390 на обычном, а завышенный sizes заставил бы его
# качать крупный файл всегда.
SIZES_GRID = "(max-width: 620px) 92vw, (max-width: 1040px) 46vw, 390px"
SIZES_WIDE = "(max-width: 900px) 94vw, 1180px"


def shot(name, w, h, alt, sizes, eager=False):
    """Снимок с набором ширин и жёстко заданными размерами.

    Размеры в разметке стоят обязательно: без них браузер не знает высоту
    до загрузки файла и страница прыгает. Сдвиг макета на сайте сведён к
    нулю замером, терять это из-за галереи не хочется."""
    srcset = ", ".join([f"media/{name}-{s}.webp {s}w" for s in STEPS]
                       + [f"media/{name}.webp {w}w"])
    load = ('fetchpriority="high" decoding="async"' if eager
            else 'loading="lazy" decoding="async"')
    return (f'<div class="shot"><span class="pz">'
            f'<img src="media/{name}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{alt}" {load}></span></div>')


def figure(name, w, h, alt, cap):
    return (f'<figure>{shot(name, w, h, alt, SIZES_GRID)}'
            f"<figcaption>{cap}</figcaption></figure>")


def grid(items):
    return '<div class="refgrid">%s</div>' % "".join(figure(*i) for i in items)


HERO = ("ref-bridge", 1170, 731, OG_ALT,
        "Railway bridge at Nakhodka, designed span 35 metres. The structural steel for "
        "this programme came in from China.")

RUSSIA = [
 ("ref-resort", 1240, 775,
  "Concrete frame under construction with formwork and shoring in place",
  "<b>Primorsky Entertainment Resort City, Artyom.</b> The contractor puts the project "
  "at ten thousand cubic metres of monolithic concrete and 498 tonnes of steelwork, "
  "built between 2017 and 2024."),
 ("ref-moscow", 1130, 706,
  "City construction site with a tower crane and foundation formwork",
  "<b>Myasnitskaya 21, Moscow.</b> Regeneration of the listed School of Painting, "
  "Sculpture and Architecture: 4,394 square metres over six floors."),
 ("ref-ferry", 1240, 775,
  "Mobile crane working on a quay in a port town",
  "<b>Kholmsk, Sakhalin.</b> Shore works for the Vanino to Kholmsk rail ferry: berth "
  "superstructure, the lifting bridge and its counterweights."),
 ("ref-moles", 1043, 652,
  "Concrete tetrapods stacked on the shore before placement",
  "<b>Port of Kholmsk.</b> Reconstruction of the entrance moles: 1,980 tetrapods and "
  "3,655 cylindrical gabions placed."),
 ("ref-shore", 1171, 732,
  "Excavator working rock armour at the water&rsquo;s edge",
  "<b>Nikolskoye, Kamchatka.</b> Coastal works on an open shore, where the plant has to "
  "be on site because there is nothing to hire within reach."),
 ("ref-plant", 1240, 775,
  "Large industrial building under construction above a bay",
  "<b>Fish plant, Petropavlovsk-Kamchatsky.</b> A pollock processing plant of 9,695 "
  "square metres with its own boiler house and treatment works."),
]

BALI = [
 ("ref-villa", 1240, 775,
  "Villa exterior with full height glazing and a pool",
  "<b>Sun on the Hill, Nusa Dua.</b> Six villas. Glazing, external finishes and the "
  "pools."),
 ("ref-villa-pool", 1240, 775,
  "Double height living space glazed onto a pool",
  "<b>Living space and pool.</b> The pool plant was bought from European manufacturers "
  "and shipped in through Denpasar."),
 ("ref-villa-in", 1240, 775,
  "Villa living space with a stair and double height glazing",
  "<b>Interiors.</b> Finishing materials shipped from China: tile, stone, joinery and "
  "sanitary ware."),
]

# ─── тексты ────────────────────────────────────────────────────────────────
H1 = "Goods we bought, and <em>the sites they went into</em>"
SUB = ("Supply references, not construction credits. Every object below was built by its "
       "own contractor. Our part was upstream: finding the producers, buying in our own "
       "name and landing the goods on site.")
CHIPS = ["China &rarr; Russia", "European Union &rarr; Russia",
         "China &amp; EU &rarr; Indonesia", "Steel &middot; formwork &middot; plant"]

LEDE = ("What a reference from a trading company can honestly show",
        "Not that we can build. That we have bought the awkward items, cleared them into "
        "a difficult country and had them standing on site when the programme said they "
        "had to be there. That part of these projects is ours to claim.")

# Страница идёт кусками: текст в узкой колонке прозы, галерея во всю ширину
# полосы. Снимок на триста восемьдесят точек это ещё доказательство, на
# двести восемьдесят уже иллюстрация, а ради доказательства страница и
# делалась. Нумерация разделов при этом сквозная, см. prose(start=...).
BLOCKS_1 = [
 ("h2", "What we supplied, and where it came from"),
 ("p", "Three programmes: two running into Russia, one into Indonesia. The pattern was the "
       "same in each. The contractor needed goods that were either not made locally at a "
       "workable price or not available in the quantity the programme demanded, and we "
       "bought them abroad and brought them in."),
 ("ul", [
  "<b>Structural steel and formwork, out of China.</b> Section and plate for fabricated "
  "structures, and the formwork and shoring the monolithic work was poured against.",
  "<b>Part of the inert materials, out of China.</b> Aggregate and fill for the marine "
  "and earthwork packages.",
  "<b>The machinery fleet, out of China.</b> Cranes, excavators, loaders and site trucks, "
  "imported rather than hired. On a site a thousand kilometres from the nearest rental "
  "yard that is not a preference, it is the only version that works.",
  "<b>Bridge equipment, out of the European Union.</b> The running hardware a bridge needs "
  "to work properly, bought in Europe because the specification and the service life "
  "decided it rather than the price.",
  "<b>Finishes from China, pool plant from the European Union.</b> For the villa project "
  "on Bali, shipped into Indonesia from two continents against one fit-out programme.",
 ]),
 ("note", "Quantities, contract values and the names of the buying companies are not "
          "published here. They belong to the contractors who bought the goods. A "
          "reference can be arranged on request, with their agreement."),

 ("h2", "Russia: Sakhalin, Kamchatka, Primorye and Moscow"),
 ("p", "Marine works in the port of Kholmsk and on the Kamchatka coast, a railway bridge "
       "at Nakhodka, a resort at Artyom and listed buildings in central Moscow. Different "
       "packages on one import channel."),
 ("p", "What makes this group worth showing is not the architecture. It is that a good "
       "part of it stands where the sea freezes, the road ends and the navigation window "
       "is counted in weeks. Goods that arrive late there do not arrive at all until the "
       "following year."),
]

BLOCKS_2 = [
 ("h2", "Bali: finishes and pool plant into a villa project"),
 ("p", "Sun on the Hill, a complex of six villas at Nusa Dua. The finishes came from "
       "China, the pool equipment from the European Union, both landed in Indonesia "
       "against the developer&rsquo;s fit-out programme."),
 ("note", "The three images below are the developer&rsquo;s visualisations of the villas "
          "rather than photographs of finished buildings, which is why they are marked "
          "as such."),
]

BLOCKS_3 = [
 ("h2", "Why a trading company publishes other people&rsquo;s buildings"),
 ("p", "Because the questions that decide a first order are not about catalogues. They "
       "are whether we have actually moved steel across a border, whether we know what a "
       "crane costs to land rather than to buy, and whether we have supplied a site that "
       "could not wait. These projects are the answer."),
 ("p", "What they are not is a construction capability. We do not build. We buy, we "
       "verify, we ship and we hand over the documents, and on every site above somebody "
       "else did the building. If a quotation from us ever reads as though we are offering "
       "more than that, it is wrong and we would rather be told."),
]

FAQ = [
 ("Did ISP Group build these objects?",
  "No. They were built by their own contractors. Our team's part was the supply: finding "
  "the producers, buying the goods in our own name and delivering them to site. Anything "
  "past that point is somebody else's credit and we do not claim it."),
 ("Can you supply the same goods somewhere else?",
  "Steel, formwork, plant and finishes are the same purchase wherever they land. What "
  "changes is the route and the clearance: admissibility at the destination, a broker who "
  "has cleared this product there, and a document set that has actually passed. We say how "
  "long building that takes before quoting rather than after."),
 ("Why import machinery instead of renting it?",
  "On a remote site there is nothing to rent. Once plant has to be mobilised several "
  "thousand kilometres and held for the length of a programme, buying it abroad and "
  "importing it is usually cheaper than hiring locally, and it is always more certain."),
 ("Will you give the contract value or the buyer's name?",
  "No. Those belong to the counterparties rather than to us, and a supplier who publishes "
  "them is telling you what he will publish about you. A reference can be arranged on "
  "request, with the buyer's agreement."),
]

RELATED = [
 ("/supply", "What we supply",
  "Six categories where producer relationships and a documented lane already exist."),
 ("/china", "Sourcing from China",
  "Factory or trader, inspection, payment, and the checks that separate them."),
 ("/experience", "Twenty years of supply work",
  "China, the Russian north and the European Union: three regimes, one method."),
 ("/corridors", "Trade corridors",
  "What has to exist on a route before anything can be quoted honestly."),
]


# ─── сборка разметки ───────────────────────────────────────────────────────
def plain(s):
    return re.sub("<[^>]+>", "", s).replace("&rsquo;", "’").replace("&amp;", "&")


def prose(blocks, start=0):
    """Разметка текстового куска. start продолжает сквозную нумерацию
    разделов: куски разделены галереями, а счёт у читателя один."""
    out, n, opened = [], start, False
    for kind, text in blocks:
        if kind == "h2":
            if opened:
                out.append("</div></div>")
            n += 1
            out.append('<div class="pblock"><span class="k">%02d</span>'
                       '<h2 id="s%d">%s</h2><div class="ptext">' % (n, n, text))
            opened = True
        elif kind == "raw":
            out.append(text)
        elif kind == "ul":
            out.append('<ul class="plist">%s</ul>'
                       % "".join("<li>%s</li>" % x for x in text))
        elif kind == "note":
            out.append('<p class="pnote">%s</p>' % text)
        else:
            out.append("<p>%s</p>" % text)
    if opened:
        out.append("</div></div>")
    return "".join(out), n


def toc(blocks):
    heads = [t for k, t in blocks if k == "h2"]
    items = "".join('<li><a href="#s%d"><span>%02d</span>%s</a></li>' % (i, i, h)
                    for i, h in enumerate(heads, 1))
    return ('<nav class="toc" aria-label="On this page">'
            '<span class="eyebrow">On this page</span><ol>%s</ol></nav>' % items)


def body_html():
    p1, n = prose(BLOCKS_1)
    p2, n = prose(BLOCKS_2, n)
    p3, n = prose(BLOCKS_3, n)
    crumbs = ('<nav class="crumbs" aria-label="Breadcrumb">'
              '<a href="/">ISP Group</a> <span>/</span> <b>References</b></nav>')
    chips = "".join('<span class="chip">%s</span>' % c for c in CHIPS)
    out = [
     '<header class="hero chero" id="top">',
     '  <div class="wrap chero-g chero-1">',
     "    <div>",
     "      " + crumbs,
     "      <h1>%s</h1>" % H1,
     '      <p class="sub">%s</p>' % SUB,
     '      <div class="chips">%s</div>' % chips,
     '      <div class="ctarow" style="margin-top:28px">'
     '<a class="btn" href="/contact#enquiry">Request a quote</a></div>',
     "    </div>",
     "  </div>",
     "</header>",
     "",
     '<main id="main" tabindex="-1">',
     '<section data-reveal><div class="wrap">',
     '<figure class="mediafig" style="margin-bottom:44px">'
     + shot(HERO[0], HERO[1], HERO[2], HERO[3], SIZES_WIDE, eager=True)
     + "<figcaption>%s</figcaption></figure>" % HERO[4],
     '<div class="lede"><h2>%s</h2><p class="intro">%s</p></div>' % LEDE,
     toc(BLOCKS_1 + BLOCKS_2 + BLOCKS_3),
     '<div class="prose">%s</div>' % p1,
     grid(RUSSIA),
     '<div class="prose">%s</div>' % p2,
     grid(BALI),
     '<div class="prose">%s</div>' % p3,
     "</div></section>",
     '<section data-reveal id="faq"><div class="wrap"><span class="eyebrow">Questions</span>'
     '<div class="lede"><h2>What buyers ask about these references</h2>'
     '<p class="intro">The four that come up as soon as the pictures load.</p></div>'
     '<div style="margin-top:34px">%s</div></div></section>'
     % "".join("<details><summary>%s</summary><p>%s</p></details>" % q for q in FAQ),
     '<section data-reveal><div class="wrap"><span class="eyebrow">Keep reading</span>'
     '<div class="lede"><h2>Where this turns into a price for you</h2>'
     '<p class="intro">The same work, described from the buying side rather than from '
     'the site.</p></div><div class="lanelinks">%s</div></div></section>'
     % "".join('<a class="lanelink" href="%s"><b>%s</b><span>%s</span></a>' % r
               for r in RELATED),
    ]
    return "\n".join(out)


def ld_blocks():
    faq = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q,
                           "acceptedAnswer": {"@type": "Answer", "text": a}}
                          for q, a in FAQ]}
    crumb = {"@context": "https://schema.org", "@type": "BreadcrumbList",
             "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "ISP Group", "item": HOST},
              {"@type": "ListItem", "position": 2, "name": "References",
               "item": HOST + SLUG}]}
    # Разметка коллекции: страница это перечень объектов, а не статья. Имена
    # объектов в ней те же, что видны в подписях, выдуманного нет.
    coll = {"@context": "https://schema.org", "@type": "CollectionPage",
            "url": HOST + SLUG, "name": plain(H1), "description": DESC,
            "about": {"@type": "Organization", "name": "ISP GROUP LLC",
                      "url": HOST},
            "hasPart": [{"@type": "CreativeWork", "name": plain(c.split("</b>")[0]),
                         "description": plain(c)}
                        for *_, c in RUSSIA + BALI]}
    return "".join('<script type="application/ld+json">%s</script>\n'
                   % json.dumps(d, ensure_ascii=False) for d in (coll, faq, crumb))


HEAD_META = """<meta name="description" content="{desc}">
<link rel="canonical" href="{host}{slug}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="ISP Group Global Commerce">
<meta property="og:url" content="{host}{slug}">
<meta property="og:title" content="{ogt}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{host}media/{ogi}">
<meta property="og:image:alt" content="{oga}">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#0b0e12">
<title>{title}</title>
"""


def main():
    donor = open(DONOR, encoding="utf-8").read()

    # 1. голова: всё от первой meta description до </title> заменяется целиком,
    #    остальное (шрифты, стили, иконка, счётчик) остаётся донорским
    head_end = donor.index("</head>")
    head = donor[:head_end]
    a = head.index('<meta name="description"')
    b = head.index("</title>") + len("</title>") + 1
    head = head[:a] + HEAD_META.format(
        desc=DESC, host=HOST, slug=SLUG, ogt=OG_TITLE, ogi=OG_IMG, oga=OG_ALT,
        title=TITLE) + head[b:]

    # 2. тело: от шапки до конца основного блока
    prefix = donor[donor.index("<body>"):donor.index('<header class="hero')]
    suffix = donor[donor.index("<footer"):]
    # разметка данных у донора своя, её снимаем и ставим свою
    suffix = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', "",
                    suffix, flags=re.S)
    suffix = suffix.replace("<!--/email_off-->", ld_blocks() + "<!--/email_off-->", 1)

    page = head + "</head>\n" + prefix + body_html() + "\n\n" + suffix

    # 3. текущий пункт меню донора на новой странице неверен
    page = page.replace(' aria-current="page"', "")

    open(OUT, "w", encoding="utf-8").write(page)
    print("   собрана страница:", OUT, len(page), "знаков")

    # 4. ссылка в подвале всех страниц: иначе новую страницу находит только
    #    поиск, а внутренних ссылок на неё нет ни одной
    #    Ссылки в подвале лежат без ведущей косой черты, относительными, и
    #    только на английских страницах: у языковых версий подвал свой.
    old = '<a href="guides" style="display:block">Guides</a>'
    new = old + '<a href="projects" style="display:block">Projects we supplied</a>'
    touched = 0
    for root, _, files in os.walk(SITE):
        for f in sorted(files):
            if not f.endswith(".html"):
                continue
            p = os.path.join(root, f)
            t = open(p, encoding="utf-8").read()
            if old in t and '"projects"' not in t:
                open(p, "w", encoding="utf-8").write(t.replace(old, new, 1))
                touched += 1
    print("   ссылка в подвале добавлена на страницах:", touched)

    # 5. карта сайта и индекс поиска
    sm = os.path.join(SITE, "sitemap.xml")
    t = open(sm, encoding="utf-8").read()
    if HOST + SLUG + "<" not in t:
        row = ('  <url><loc>%s%s</loc><lastmod>2026-10-27</lastmod>'
               '<changefreq>monthly</changefreq><priority>0.9</priority></url>\n'
               % (HOST, SLUG))
        open(sm, "w", encoding="utf-8").write(t.replace("</urlset>", row + "</urlset>"))
        print("   адрес добавлен в карту сайта")

    credits()
    llms()

    n, size = SRCH.build_index()
    print(f"   индекс поиска пересобран: {n} страниц, {size/1024:.0f} КБ")
    return 0


# Титры. В подвале стояло «все прочие снимки CC0 или общественное достояние».
# После этой страницы это неправда: девять кадров принадлежат владельцам
# объектов. Строку приходится менять вместе со страницей, иначе сайт, который
# только что чистили от завышений, начинает врать в подвале.
CREDIT_OLD = ("All other images CC0 or public domain. Full list with links in "
              "media/CREDITS.json.")
CREDIT_NEW = ("Photographs and visualisations on the references page belong to the "
              "owners of those projects. All other images CC0 or public domain. "
              "Full list with links in media/CREDITS.json.")


def credits():
    path = os.path.join(SITE, "media", "CREDITS.json")
    data = json.load(open(path, encoding="utf-8"))
    for name, _w, _h, _alt, cap in [HERO] + RUSSIA + BALI:
        data[name + ".jpg"] = {
            "title": plain(cap.split("</b>")[0]).split(". ")[0],
            "license": "all rights reserved",
            # source это адрес, из которого страница титров делает ссылку.
            # У этих снимков адреса нет: они пришли от владельца объекта, а
            # не из открытой библиотеки, и подставлять туда фразу значит
            # получить ссылку в никуда.
            "author": "project owner, supplied to ISP GROUP LLC",
            "source": None,
        }
    json.dump(data, open(path, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    touched = 0
    for root, _, files in os.walk(SITE):
        for f in sorted(files):
            if not f.endswith(".html"):
                continue
            p = os.path.join(root, f)
            t = open(p, encoding="utf-8").read()
            if CREDIT_OLD in t and CREDIT_NEW not in t:
                open(p, "w", encoding="utf-8").write(t.replace(CREDIT_OLD, CREDIT_NEW))
                touched += 1
    print("   титры в подвале поправлены на страницах:", touched)


def llms():
    """Файл для языковых моделей: страницу нужно перечислить и там, иначе
    модель её просто не увидит, а именно ради цитирования она и писалась."""
    path = os.path.join(SITE, "llms.txt")
    t = open(path, encoding="utf-8").read()
    row = ("- [%s](%s%s): %s\n" % (OG_TITLE, HOST, SLUG, DESC))
    if HOST + SLUG + ")" in t:
        return
    anchor = "- [About ISP Group]"
    i = t.index(anchor)
    open(path, "w", encoding="utf-8").write(t[:i] + row + t[i:])
    print("   страница добавлена в llms.txt")


if __name__ == "__main__":
    sys.exit(main())
