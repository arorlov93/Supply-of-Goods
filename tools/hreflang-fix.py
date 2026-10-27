# -*- coding: utf-8 -*-
"""Языковые связи: указывать на перевод этой страницы, а не на главную.

Что было. Все 46 страниц несли один и тот же набор:

    hreflang="en" -> /
    hreflang="fr" -> /fr/
    hreflang="es" -> /es/
    hreflang="de" -> /de/

То есть страница про Китай заявляла поисковику, что её английская
версия это главная, французская это французская главная и так далее.
Это неправда, и правила это прямо запрещают: связь должна указывать на
равнозначную страницу и быть взаимной. Непарные связи в лучшем случае
не учитываются, в худшем поисковик показывает не ту страницу.

Как правильно. Набор остаётся только там, где переводы действительно
есть:

  * четыре главные, они переведены целиком;
  * четыре пары внутренних страниц, у которых есть французский близнец:
    контакты, куски птицы, Западная Африка, ветеринарный сертификат.

У остальных страниц перевода нет, и честный ответ это отсутствие
связей вовсе. Страница без hreflang не становится хуже в выдаче, а
страница с ложным hreflang становится.

Запуск: python3.13 tools/hreflang-fix.py
Повторный запуск ничего не меняет.
"""
import pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
HOST = "https://ispgroupgc.com"

# главные: переведены целиком
HOMES = {
    "index.html": "en",
    "fr/index.html": "fr",
    "es/index.html": "es",
    "de/index.html": "de",
}
HOME_URL = {"en": f"{HOST}/", "fr": f"{HOST}/fr/", "es": f"{HOST}/es/", "de": f"{HOST}/de/"}

# внутренние пары: английская страница и её французский близнец
PAIRS = [
    ("contact.html", "contact-fr.html"),
    ("poultry-cuts.html", "decoupes-volaille.html"),
    ("west-africa.html", "afrique-ouest.html"),
    ("veterinary-certificate.html", "certificat-veterinaire.html"),
]

BLOCK = re.compile(r'[ \t]*<link rel="alternate" hreflang="[^"]*"[^>]*>\n?')


def url_of(rel):
    slug = rel.replace(".html", "")
    if slug.endswith("index"):
        slug = slug[: -len("index")]
    return f"{HOST}/{slug}" if slug else f"{HOST}/"


def links_for(pairs):
    """pairs: список (код языка, адрес). Первый считается основным."""
    out = [f'<link rel="alternate" hreflang="{c}" href="{u}">' for c, u in pairs]
    en = dict(pairs).get("en")
    if en:
        out.append(f'<link rel="alternate" hreflang="x-default" href="{en}">')
    return "\n".join(out) + "\n"


def main():
    want = {}

    for rel, code in HOMES.items():
        want[rel] = links_for([(c, HOME_URL[c]) for c in ("en", "fr", "es", "de")])

    for en_file, fr_file in PAIRS:
        pair = [("en", url_of(en_file)), ("fr", url_of(fr_file))]
        want[en_file] = links_for(pair)
        want[fr_file] = links_for(pair)

    changed = cleared = same = 0
    for p in sorted(SITE.rglob("*.html")):
        if p.name == "crm.html":
            continue
        rel = str(p.relative_to(SITE))
        s = p.read_text()
        has = BLOCK.search(s)
        new = want.get(rel, "")

        if not has and not new:
            same += 1
            continue

        # вырезаем прежний набор целиком
        first = has.start() if has else None
        cleaned = BLOCK.sub("", s)

        if new:
            if first is None:
                m = re.search(r'<link rel="canonical"[^>]*>\n?', cleaned)
                if not m:
                    print(f"  ОШИБКА: некуда вставить в {rel}")
                    return 1
                at = m.end()
            else:
                at = first
            cleaned = cleaned[:at] + new + cleaned[at:]
            changed += 1
        else:
            cleared += 1

        p.write_text(cleaned)

    print(f"набор исправлен: {changed}, ложные связи убраны: {cleared}, без изменений: {same}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
