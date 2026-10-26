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
# ── Переводы главной ──────────────────────────────────────────────────────────
# Таблица вынесена в tools/i18n.json: держать 140 строк на трёх языках прямо
# в коде неудобно, а главное - прежняя таблица молча устарела. В ней лежали
# строки старой главной («WE BUY», «01 — Origin»), которых на странице уже
# не было, а новые строки в неё никто не добавил. Снаружи это выглядело как
# французская страница, переведённая на четырнадцать процентов.
# Поэтому ниже есть проверка полноты, и она ругается, а не молчит.
HOME = json.loads((pathlib.Path(__file__).parent / "i18n.json").read_text())
HOME.pop("_note", None)


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
.langsw{padding-left:18px;border-left:1px solid rgba(244,243,239,.22)}
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
    """Подстановка по тексту узла, а не по точной строке файла.

    Длинные абзацы в разметке перенесены по строкам с отступами, поэтому
    точное совпадение по ключу для них никогда не срабатывало: именно так
    французская страница и оказалась переведённой наполовину. Здесь текст
    узла сначала сводится к одной строке, и уже он сверяется с таблицей.
    """
    # ключи в нормальном виде: пробелы схлопнуты, типографика развёрнута
    table = {}
    for en, row in HOME.items():
        tr = row.get(lang)
        if tr:
            table[norm(en)] = tr

    def repl(m):
        raw = m.group(1)
        key = norm(html.unescape(raw))
        tr = table.get(key)
        if tr is None:
            return m.group(0)
        # перевод ставится одной строкой: исходные переносы были версткой,
        # а не содержанием
        return ">" + html.escape(tr, quote=False) + "<"

    s = re.sub(r">([^<>]{2,})<", repl, src)

    # значения в атрибутах, которые видит пользователь
    for attr in ("placeholder", "title", "alt", "aria-label"):
        def areps(m, attr=attr):
            tr = table.get(norm(html.unescape(m.group(1))))
            return f'{attr}="{html.escape(tr, quote=True)}"' if tr else m.group(0)
        s = re.sub(attr + r'="([^"]{2,})"', areps, s)
    return s


def norm(t):
    """Текст к сравнимому виду: один пробел, обычные кавычки и тире."""
    t = html.unescape(t)
    t = (t.replace("\u2019", "'").replace("\u2018", "'")
          .replace("\u201c", '"').replace("\u201d", '"')
          .replace("\u2014", "-").replace("\u2013", "-")
          .replace("\u00b7", "-").replace("\u00a0", " "))
    return re.sub(r"\s+", " ", t).strip()


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
    # вставка должна быть идемпотентной: иначе каждый запуск добавляет ещё один
    en = re.sub(r'<div class="langsw" aria-label="Language">.*?</div>\s*', '', en, flags=re.S)
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
        # по образцу, а не точной строкой: перевод атрибутов уже поменял
        # aria-label внутри блока, и точное совпадение срывалось, из-за
        # чего на французской странице подсвечивался английский
        s = re.sub(r'<div class="langsw".*?</div>', switcher(lang), s, count=1, flags=re.S)
        # относительные ссылки становятся абсолютными, иначе внутри /fr/ они ломаются
        for slug in LINKS:
            s = s.replace(f'href="{slug}"', f'href="/{slug}"')
        s = s.replace('href="media/', 'href="/media/')
        s = s.replace('src="media/', 'src="/media/')
        s = s.replace('srcset="media/', 'srcset="/media/')
        (d / "index.html").write_text(s)
        made.append(f"{lang}/index.html")
    return made


def leftovers(page_html, lang):
    """Сколько английского осталось на переведённой странице.

    Это и есть страховка от того, что уже один раз случилось: таблица
    разошлась со страницей, часть строк осталась английской, и никто об
    этом не узнал. Считаются только слова-маркеры, которых во французском,
    испанском и немецком в такой форме не бывает.
    """
    import re as _re
    body = _re.sub(r"<(script|style|noscript)\b.*?</\1>", " ", page_html, flags=_re.S)
    txt = _re.sub(r"<[^>]+>", " ", body)
    txt = _re.sub(r"&[a-z]+;", " ", txt)
    words = _re.findall(r"[A-Za-z']{3,}", txt)
    markers = {
        "the", "and", "with", "your", "from", "that", "this", "what", "where",
        "when", "which", "goods", "supply", "price", "delivery", "contract",
        "quote", "before", "after", "every", "their", "order", "producer",
        "buyer", "request", "trading", "about", "deliver", "works", "into",
        "road", "sea", "start", "stop", "lanes", "among", "them",
        "they", "will", "same", "way", "steps", "process",
    }
    # Слова, которые во французском, испанском или немецком пишутся так же
    # или входят в их словарь: маркерами считать нельзя, иначе проверка
    # ругается на правильный перевод.
    allowed = {"contact", "menu", "incoterms", "standard", "transit", "container",
               "port", "guides", "documents", "source", "name", "terms",
               "import", "export", "service", "cable", "film", "carton",
               "arrive"}   # «la marchandise arrive» это французский, не остаток
    hits = [w.lower() for w in words
            if w.lower() in markers and w.lower() not in allowed]
    return hits


if __name__ == "__main__":
    for f in build():
        print("создано:", f)
    bad = 0
    for lang in LANGS:
        page = (ROOT / lang / "index.html").read_text()
        hits = leftovers(page, lang)
        if hits:
            bad += 1
            from collections import Counter
            top = ", ".join(f"{w} x{n}" for w, n in Counter(hits).most_common(8))
            print(f"  ВНИМАНИЕ {lang}: английских слов осталось {len(hits)} -> {top}")
        else:
            print(f"  {lang}: английского не осталось")
    if bad:
        print("\nДобавьте пропущенные строки в tools/i18n.json и запустите снова.")
        sys.exit(1)
