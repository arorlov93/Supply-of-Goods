# -*- coding: utf-8 -*-
"""Перенос шрифтов на свой домен.

Было: все 45 страниц тянули три семейства с fonts.googleapis.com. Это
отдельное соединение к чужому домену до того, как покажется первый текст,
и во внешнем аудите именно оно держало отрисовку первого экрана на телефоне.
Файлы маленькие, повод держать их у себя очевидный.

Берутся только наборы latin и latin-ext: сайт на английском, французском,
испанском и немецком, кириллица и вьетнамский ему не нужны и весят зря.

Запуск: python3.13 tools/fonts-local.py
"""
import pathlib, re, urllib.request

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
FONTS = SITE / "fonts"
CSS_URL = ("https://fonts.googleapis.com/css2"
           "?family=Newsreader:ital,wght@0,400;1,400"
           "&family=Schibsted+Grotesk:wght@400;500;700"
           "&family=IBM+Plex+Mono:wght@400;500&display=swap")
# без браузерного User-Agent Google отдаёт устаревший формат вместо woff2
BROWSER_UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/124.0 Safari/537.36")
KEEP = ("latin", "latin-ext")

LINK_RE = re.compile(
    r'<link[^>]*fonts\.googleapis\.com[^>]*>|'
    r'<link[^>]*rel="preconnect"[^>]*fonts\.gstatic\.com[^>]*>|'
    r'<link[^>]*rel="preconnect"[^>]*fonts\.googleapis\.com[^>]*>\s*')
LOCAL = ('<link rel="preload" href="/fonts/fonts.css" as="style">\n'
         '<link rel="stylesheet" href="/fonts/fonts.css">')


def get(url, ua=BROWSER_UA):
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read()


def main():
    FONTS.mkdir(exist_ok=True)
    css = get(CSS_URL).decode("utf-8")

    out, kept, skipped = [], 0, 0
    # каждый блок @font-face идёт со своим комментарием о наборе знаков
    for block in re.split(r"(?=/\*\s*[a-z-]+\s*\*/)", css):
        m = re.search(r"/\*\s*([a-z-]+)\s*\*/", block)
        if not m:
            continue
        subset = m.group(1)
        if subset not in KEEP:
            skipped += 1
            continue
        u = re.search(r"url\((https://fonts\.gstatic\.com/[^)]+\.woff2)\)", block)
        fam = re.search(r"font-family:\s*'([^']+)'", block)
        wght = re.search(r"font-weight:\s*(\d+)", block)
        ital = "italic" in block
        if not (u and fam):
            continue
        name = (fam.group(1).replace(" ", "-").lower() + "-" + (wght.group(1) if wght else "400")
                + ("-italic" if ital else "") + "-" + subset + ".woff2")
        (FONTS / name).write_bytes(get(u.group(1)))
        out.append(block.replace(u.group(1), "/fonts/" + name).strip())
        kept += 1

    (FONTS / "fonts.css").write_text(
        "/* Шрифты лежат на своём домене: чужое соединение до первого текста\n"
        "   держало отрисовку первого экрана на телефоне. */\n\n"
        + "\n\n".join(out) + "\n")

    done = 0
    for p in sorted(SITE.rglob("*.html")):
        s = s0 = p.read_text()
        if "fonts.googleapis.com" not in s:
            continue
        s = LINK_RE.sub("", s)
        s = s.replace("</head>", LOCAL + "\n</head>", 1)
        if s != s0:
            p.write_text(s)
            done += 1

    size = sum(f.stat().st_size for f in FONTS.glob("*.woff2"))
    print(f"файлов шрифтов: {kept}, пропущено наборов: {skipped}, "
          f"вес: {size / 1024:.0f} КБ")
    print(f"страниц переключено: {done}")


if __name__ == "__main__":
    main()
