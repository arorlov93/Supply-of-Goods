# -*- coding: utf-8 -*-
"""Страница титров к фотографиям.

В подвале стояло «Photography licensed CC0 or public domain; see media
credits». Обе половины фразы были неправдой: из 46 снимков 18 под CC BY,
которая требует указания автора, а никаких титров на сайте не было, и
«media credits» даже не было ссылкой.

Лицензию нельзя соблюсти наполовину: либо авторы названы, либо снимок
нельзя использовать. Поэтому страница собирается из media/CREDITS.json,
то есть из тех же данных, которыми подписаны файлы, и обновляется вместе
с библиотекой.

Страница строится по образцу privacy.html: оттуда берутся шапка, подвал и
оформление, заменяется только содержимое. Так она не отстаёт от остального
сайта по виду и не требует отдельной вёрстки.

Запуск: python3.13 tools/credits-page.py
"""
import html, json, pathlib, re

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
SRC = SITE / "privacy.html"
DST = SITE / "credits.html"

LIC = {
    "cc0": ("CC0 1.0", "https://creativecommons.org/publicdomain/zero/1.0/"),
    "pdm": ("Public Domain Mark", "https://creativecommons.org/publicdomain/mark/1.0/"),
    "public domain": ("Public domain", ""),
    "by": ("CC BY", "https://creativecommons.org/licenses/by/4.0/"),
    "cc by 2.0": ("CC BY 2.0", "https://creativecommons.org/licenses/by/2.0/"),
    "cc by 3.0": ("CC BY 3.0", "https://creativecommons.org/licenses/by/3.0/"),
    "cc by 4.0": ("CC BY 4.0", "https://creativecommons.org/licenses/by/4.0/"),
    "cc by-sa 2.0": ("CC BY-SA 2.0", "https://creativecommons.org/licenses/by-sa/2.0/"),
    "cc by-sa 3.0": ("CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0/"),
    "cc by-sa 4.0": ("CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0/"),
}


def lic_html(raw):
    key = (raw or "").strip().lower()
    name, url = LIC.get(key, (raw or "not recorded", ""))
    if url:
        return f'<a href="{url}" rel="license noopener" target="_blank">{html.escape(name)}</a>'
    return html.escape(name)


def main():
    shell = SRC.read_text()
    cred = json.loads((SITE / "media" / "CREDITS.json").read_text())

    rows = []
    for fn in sorted(cred):
        v = cred[fn]
        title = html.escape(str(v.get("title") or fn))
        author = html.escape(str(v.get("author") or "not recorded"))
        src = v.get("source") or ""
        name = (f'<a href="{html.escape(src)}" rel="noopener" target="_blank">{title}</a>'
                if src else title)
        rows.append(
            f"<tr><td><code>{html.escape(fn)}</code></td><td>{name}</td>"
            f"<td>{author}</td><td>{lic_html(v.get('license'))}</td></tr>")

    body = (
        '<div class="prose"><div class="pblock"><span class="k">01</span>'
        '<h2 id="s1">Why this page exists</h2><div class="ptext">'
        "<p>Every photograph on this site is someone else's work, used under a licence "
        "that lets us publish it. Several of those licences are only satisfied if the "
        "author is named. This page names them. It is generated from the same file that "
        "records the licence of each image, so it cannot drift out of date while the "
        "pictures change.</p>"
        "<p>No photograph here shows our own goods, our own premises or our own staff. "
        "They illustrate the kind of trade described in the text, nothing more. Nothing "
        "on this page should be read as a claim that we own, operate or are connected to "
        "anything shown.</p></div></div>"
        '<div class="pblock wide"><span class="k">02</span>'
        f'<h2 id="s2">The photographs, {len(rows)} in all</h2><div class="ptext">'
        '<div class="tablewrap"><table class="credits"><thead><tr>'
        "<th>File</th><th>Title and source</th><th>Author</th><th>Licence</th>"
        "</tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>"
        "</div></div></div>"
    )

    toc = ('<nav class="toc" aria-label="On this page"><span class="eyebrow">On this page</span>'
           '<ol><li><a href="#s1"><span>01</span>Why this page exists</a></li>'
           '<li><a href="#s2"><span>02</span>The photographs</a></li></ol></nav>')

    s = shell
    # оглавление и содержимое идут в таком порядке: сначала nav.toc, потом
    # prose. Резать по индексам нельзя, они смещаются друг относительно
    # друга, поэтому каждый кусок меняется своей подстановкой.
    s = re.sub(r'<nav class="toc".*?</nav>', toc, s, count=1, flags=re.S)
    s = re.sub(r'<div class="prose">.*?(?=\n*<(?:footer|section|script|div class="foot))',
               body, s, count=1, flags=re.S)

    s = re.sub(r"<title>[^<]*</title>",
               "<title>Photo credits and licences | ISP Group LLC</title>", s, count=1)
    s = re.sub(r'<meta name="description" content="[^"]*"',
               '<meta name="description" content="Author, source and licence for every '
               'photograph used on this site."', s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*"',
               '<link rel="canonical" href="https://ispgroupgc.com/credits"', s, count=1)
    # заголовок страницы и хлебные крошки. Сплошная замена слова Privacy
    # переименовала бы и ссылку на политику в подвале, поэтому точечно.
    s = s.replace("<b>Privacy</b>", "<b>Photo credits</b>", 1)
    s = re.sub(r"<h1>.*?</h1>",
               "<h1>Whose photographs <em>these are</em></h1>", s, count=1, flags=re.S)
    s = re.sub(r'<p class="sub">.*?</p>',
               '<p class="sub">Every picture here was taken by someone else and is used '
               'under a licence. Some of those licences require the author to be named. '
               'This page names them.</p>', s, count=1, flags=re.S)
    s = re.sub(r'<div class="chips">.*?</div>',
               '<div class="chips"><span class="chip">CC0</span>'
               '<span class="chip">Public domain</span><span class="chip">CC BY</span>'
               '<span class="chip">Author named</span></div>', s, count=1, flags=re.S)

    # таблица титров: в оформлении сайта её нет, она нужна только здесь
    s = s.replace("</body>", """<style>/* титры */
/* обычный раздел прозы держит текст в правой колонке, таблице там тесно:
   название лицензии переносилось на три строки */
.pblock.wide{display:block}
.pblock.wide .ptext{margin-top:18px}
.tablewrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
table.credits{width:100%;border-collapse:collapse;font-size:.88rem;margin-top:10px}
table.credits th{text-align:left;font-family:var(--mono);font-size:10px;
  letter-spacing:.16em;text-transform:uppercase;font-weight:400;
  padding:0 14px 10px 0;border-bottom:1px solid var(--rule)}
table.credits td{padding:11px 14px 11px 0;border-bottom:1px solid var(--rule);
  vertical-align:top}
table.credits code{font-family:var(--mono);font-size:.8rem;opacity:.75}
@media (max-width:760px){
  table.credits{font-size:.82rem}
  /* ссылок в таблице много, и по умолчанию они высотой в строку текста:
     пальцем в такое не попасть */
  table.credits a{display:inline-flex;align-items:center;min-height:44px;
    min-width:44px;line-height:1.3}
  table.credits td{padding-block:4px}
}
</style>
</body>""", 1)

    DST.write_text(s)
    print(f"собрано титров: {len(rows)} -> {DST}")


if __name__ == "__main__":
    main()
