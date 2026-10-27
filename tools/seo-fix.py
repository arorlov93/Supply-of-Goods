# -*- coding: utf-8 -*-
"""Правки под поисковую и машинную выдачу.

Делает четыре вещи.

1. robots.txt: явный список краулеров языковых моделей. Строки
   `User-agent: *` им формально достаточно, но часть из них читает только
   собственное имя, а защитные настройки у провайдеров всё чаще по
   умолчанию блокируют именно их. Явное разрешение снимает двусмысленность
   и переживёт смену настроек на стороне Cloudflare.

2. Описания страниц: шесть штук выходили за 70-165 знаков. Короткое
   описание теряет место в выдаче, длинное обрезается на середине фразы, и
   в обоих случаях в ответ машины попадает не то, что мы хотели сказать.

3. Заголовки немецкой и французской главных: 67 и 69 знаков, обрезаются.

4. sitemap: языковые версии главной не были связаны между собой через
   hreflang. Без этого поисковик считает их четырьмя конкурирующими
   страницами об одном и том же, а не одной страницей на четырёх языках.

Запуск: python3.13 tools/seo-fix.py
"""
import pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

ROBOTS = """# ISP GROUP LLC, https://ispgroupgc.com
# Индексирование и использование в ответах разрешено всем.
# Имена ниже перечислены явно: часть краулеров читает только собственную
# секцию, а не общую, и явное разрешение переживает смену настроек у
# провайдера, где блокировка таких ботов всё чаще включена по умолчанию.

User-agent: *
Allow: /

# Поисковые системы
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: DuckDuckBot
Allow: /

User-agent: YandexBot
Allow: /

# Ответные машины и языковые модели
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: Amazonbot
Allow: /

User-agent: meta-externalagent
Allow: /

User-agent: CCBot
Allow: /

User-agent: cohere-ai
Allow: /

User-agent: YouBot
Allow: /

Sitemap: https://ispgroupgc.com/sitemap.xml

# Plain-text map of this site for language models
# https://ispgroupgc.com/llms.txt
"""

# файл -> новое описание
DESC = {
    "index.html":
        "ISP GROUP LLC buys goods in its own name and delivers to your port. "
        "Building materials, industrial equipment, tools, metals and pipe, paper, food.",
    "food-agricultural.html":
        "Frozen and chilled protein, bulk staples, ingredients and branded beverages, "
        "handled under veterinary and sanitary certification for the destination country.",
    "credits.html":
        "Author, source and licence for every photograph used on this site, "
        "each with a link to the original file.",
    "de/index.html":
        "ISP GROUP LLC kauft Ware im eigenen Namen und liefert an Ihren Hafen. "
        "Baustoffe, Industrieanlagen, Werkzeuge, Metalle, Papier, Lebensmittel.",
    "es/index.html":
        "ISP GROUP LLC compra la mercancía en nombre propio y la entrega en su puerto. "
        "Materiales, equipos, herramientas, metales, papel y alimentación.",
    "fr/index.html":
        "ISP GROUP LLC achète la marchandise en son propre nom et la livre à votre port. "
        "Matériaux, équipements, outillage, métaux, papier et alimentaire.",
}

# файл -> (старый заголовок, новый заголовок)
TITLE = {
    "de/index.html": ("ISP Group LLC: Beschaffung, Lieferung und Zustellung an Ihren Hafen",
                      "ISP Group LLC: Beschaffung und Lieferung an Ihren Hafen"),
    "fr/index.html": ("ISP Group LLC : sourcing, approvisionnement et livraison à votre port",
                      "ISP Group LLC : sourcing et livraison à votre port"),
}

# языковые версии главной, связываются между собой
ALT = {
    "https://ispgroupgc.com/": "en",
    "https://ispgroupgc.com/fr/": "fr",
    "https://ispgroupgc.com/es/": "es",
    "https://ispgroupgc.com/de/": "de",
}


def set_meta(text, name, value, kind="name"):
    """Заменить значение мета-тега, вернуть (текст, сработало ли)."""
    pat = re.compile(rf'(<meta {kind}="{re.escape(name)}" content=")([^"]*)(")', re.I)
    out, n = pat.subn(lambda m: m.group(1) + value + m.group(3), text)
    return out, n


def main():
    bad = 0

    (SITE / "robots.txt").write_text(ROBOTS)
    print("robots.txt: краулеров разрешено явно:", ROBOTS.count("User-agent:") - 1)

    for rel, desc in DESC.items():
        if not 70 <= len(desc) <= 165:
            print(f"  ОШИБКА {rel}: описание {len(desc)} знаков, нужно 70-165"); bad += 1; continue
        p = SITE / rel
        s = p.read_text()
        for kind, name in (("name", "description"), ("property", "og:description"),
                           ("name", "twitter:description")):
            s, _ = set_meta(s, name, desc, kind)
        p.write_text(s)
        print(f"  описание {rel}: {len(desc)} знаков")

    for rel, (old, new) in TITLE.items():
        if len(new) > 62:
            print(f"  ОШИБКА {rel}: заголовок {len(new)} знаков"); bad += 1; continue
        p = SITE / rel
        s = p.read_text()
        if old not in s:
            print(f"  ОШИБКА {rel}: прежний заголовок не найден"); bad += 1; continue
        p.write_text(s.replace(old, new))
        print(f"  заголовок {rel}: {len(new)} знаков")

    # hreflang в sitemap
    sm = SITE / "sitemap.xml"
    s = sm.read_text()
    if "xmlns:xhtml" not in s:
        s = s.replace(
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            '        xmlns:xhtml="http://www.w3.org/1999/xhtml">')
    links = "".join(
        f'<xhtml:link rel="alternate" hreflang="{lang}" href="{href}"/>'
        for href, lang in ALT.items()
    ) + '<xhtml:link rel="alternate" hreflang="x-default" href="https://ispgroupgc.com/"/>'

    done = 0
    for href in ALT:
        # вставить ссылки внутрь соответствующего <url>, если их там ещё нет
        pat = re.compile(r"(<url><loc>" + re.escape(href) + r"</loc>)(.*?)(</url>)")
        m = pat.search(s)
        if not m:
            print(f"  ОШИБКА sitemap: {href} не найден"); bad += 1; continue
        if "xhtml:link" in m.group(2):
            continue
        s = s[:m.start()] + m.group(1) + m.group(2) + links + m.group(3) + s[m.end():]
        done += 1
    sm.write_text(s)
    print(f"sitemap: языковых версий связано {done}, всего ссылок hreflang {s.count('xhtml:link')}")

    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
