# -*- coding: utf-8 -*-
"""Перенести правку текста руководства из источника на готовую страницу.

Зачем отдельный инструмент. Тексты руководств живут в `content_guides.py`,
а на сайте лежит готовый HTML, через который прошло полтора десятка
доводочных проходов: версии файлов в именах, размеры картинок, шрифты,
снятые надбровия, подрезанные srcset. Полная пересборка `run_build.py`
всё это сотрёт, и вдобавок затянет на другие страницы старые тексты из
`content_core.py`, где ещё не учтены правки внешнего аудита. Поэтому
пересобирать нельзя, а править HTML руками нельзя тем более: оглавление
нумеруется, и ручная вставка раздела разъедется с нумерацией.

Что делает этот инструмент. Берёт версию `content_guides.py` из последнего
коммита и версию из рабочего дерева, рендерит из обеих одни и те же куски
теми же функциями, что и сборщик, и меняет на странице старый кусок на
новый. Куски три: оглавление, основной текст, блок вопросов вместе с его
разметкой FAQPage.

Главное здесь не замена, а проверка. Прежде чем что-то менять, инструмент
убеждается, что старый кусок лежит на странице дословно. Если не лежит,
значит страница с источником разошлась, и тогда тихая замена затёрла бы
чужую правку. В этом случае инструмент ничего не трогает и говорит, что
именно не сошлось. Молчаливой порчи быть не должно.

Запуск:
    python3 tools/guide-sync.py                 все руководства
    python3 tools/guide-sync.py letter-of-credit bill-of-lading
    python3 tools/guide-sync.py --dry           только показать, что изменится
"""
import importlib.util, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = os.path.join(ROOT, "site")
sys.path.insert(0, HERE)

import gen_pages as G  # noqa: E402

# Надбровия со страниц сняты отдельным проходом, оглавление на сайте идёт
# без них. Рендерим как сборщик и снимаем так же, иначе дословного
# совпадения не будет и инструмент справедливо откажется работать.
EYEBROW = re.compile(r'<span class="eyebrow">[^<]*</span>')

# Ссылки на страницах уже без .html: Cloudflare Pages отдаёт /page.html
# редиректом на /page, и сборщик это подчищает отдельным проходом. Повторяем
# то же правило над свежим куском, иначе дословного совпадения не выйдет.
HREF = re.compile(r'href=(")([a-z0-9][a-z0-9\-]*\.html)((?:#[^"]*)?)\1')


def pretty(text):
    known = {os.path.basename(p) for p in os.listdir(SITE) if p.endswith(".html")}

    def one(m):
        q, name, rest = m.group(1), m.group(2), m.group(3)
        if name not in known:
            return m.group(0)
        if name == "index.html":
            return 'href=%s/%s%s' % (q, rest, q)
        return 'href=%s%s%s%s' % (q, name[:-5], rest, q)

    return HREF.sub(one, text)


def head_version():
    """content_guides.py из последнего коммита, как отдельный модуль."""
    src = subprocess.run(["git", "show", "HEAD:tools/content_guides.py"],
                         cwd=ROOT, capture_output=True, text=True)
    if src.returncode:
        sys.exit("не достать content_guides.py из HEAD: " + src.stderr.strip())
    fd, path = tempfile.mkstemp(suffix=".py", prefix="cg_head_")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(src.stdout)
    spec = importlib.util.spec_from_file_location("cg_head", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    os.unlink(path)
    return mod


def by_slug(mod):
    return {s["slug"]: s for s in mod.GUIDES_PAGES}


def pieces(spec):
    """Три куска страницы ровно в том виде, в каком они на ней лежат."""
    faq = spec.get("faq") or []
    out = {
        "оглавление": (EYEBROW.sub("", G.toc(spec["body"])) if G.toc(spec["body"]) else ""),
        "текст": G.prose(spec["body"]),
        "вопросы": G.faq_html(faq) if faq else "",
        "разметка вопросов": json.dumps(G.faq_ld(faq), ensure_ascii=False) if faq else "",
    }
    return {k: pretty(v) for k, v in out.items()}


def sync(slug, old, new, dry):
    path = os.path.join(SITE, slug + ".html")
    if not os.path.exists(path):
        return "нет файла " + path, False
    html = open(path, encoding="utf-8").read()
    a, b = pieces(old), pieces(new)

    changed, notes = [], []
    for name in a:
        if not a[name] or a[name] == b[name]:
            continue
        # Сначала ищем НОВЫЙ кусок, а не старый. Когда правка это дописанный
        # вопрос, старый кусок оказывается началом нового и находится внутри
        # него: замена по старому пришила бы хвост второй раз. Если новый
        # кусок уже на странице, работа сделана раньше, и трогать нечего.
        if b[name] and b[name] in html:
            continue
        if a[name] not in html:
            return ("%s: кусок «%s» на странице не найден дословно, "
                    "страница разошлась с источником, не трогаю" % (slug, name)), False
        if html.count(a[name]) != 1:
            return ("%s: кусок «%s» встречается %d раза, не трогаю"
                    % (slug, name, html.count(a[name]))), False
        html = html.replace(a[name], b[name])
        changed.append(name)
        notes.append("    %-18s %+d символов" % (name, len(b[name]) - len(a[name])))

    if not changed:
        return "%s: без изменений" % slug, False
    if not dry:
        open(path, "w", encoding="utf-8").write(html)
    head = "%s: %s%s" % (slug, ", ".join(changed), " (только показ)" if dry else "")
    return head + "\n" + "\n".join(notes), True


def main(argv):
    dry = "--dry" in argv
    want = [a for a in argv if not a.startswith("-")]
    old, new = by_slug(head_version()), by_slug(__import__("content_guides"))
    slugs = want or [s for s in new if s in old]
    bad = [s for s in slugs if s not in new]
    if bad:
        sys.exit("нет таких руководств: " + ", ".join(bad))

    touched = 0
    for slug in slugs:
        if slug not in old:
            print("%s: новое руководство, его собирает сборщик, пропускаю" % slug)
            continue
        msg, did = sync(slug, old[slug], new[slug], dry)
        print(msg)
        touched += did
    print("\nизменено страниц: %d" % touched)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
