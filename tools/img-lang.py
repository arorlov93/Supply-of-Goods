# -*- coding: utf-8 -*-
"""Снимки на языковых версиях: webp вместо jpg и адаптивный набор.

Что нашлось. Французская, испанская и немецкая главные весили по 2.92 МБ
против 1.29 у английской. Причина простая: там снимки подключены не теми
файлами. Вместо webp стоят исходные jpg, и набора под разные экраны нет
вовсе. Получалось, что посетитель из Франции качает втрое больше
англоязычного за ту же страницу.

Что делается. Для каждого снимка берётся его webp и набор ступеней,
уже нарезанный для английской версии: раскладка у этих страниц та же,
значит и ширины показа те же. Запасной jpg не оставляем: webp понимают
все браузеры, которыми сегодня пользуются, а вторая копия каждого файла
это лишний вес в выкладке.

Запуск: python3.13 tools/img-lang.py
Повторный запуск ничего не меняет.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
MEDIA = SITE / "media"
LANGS = ["fr", "es", "de"]


def main():
    sizes = json.loads((ROOT / "img-sizes.json").read_text())
    en = (SITE / "index.html").read_text()

    def stem_of(fname):
        """Имя снимка без ступени и без версии.

        Файлы называются «имя[-ширина].версия.webp», а в имени самом
        бывают дефисы: j-works, crane-dusk. Поэтому сначала снимаем два
        последних куска через точку, потом хвост из дефиса и цифр."""
        base = fname.split("/")[-1]
        parts = base.split(".")
        name = ".".join(parts[:-2]) if len(parts) > 2 else parts[0]
        return re.sub(r"-\d+$", "", name)

    # стебель -> готовый набор с английской главной
    sets = {}
    for m in re.finditer(r'<source srcset="([^"]+)" sizes="([^"]+)" type="image/webp">', en):
        srcset, sz = m.group(1), m.group(2)
        first = srcset.split(",")[0].strip().split(" ")[0]
        stem = stem_of(first)
        sets[stem] = (srcset, sz)

    # запасной случай: снимок есть, набора для него не делали
    plain = {}
    for f in MEDIA.glob("*.webp"):
        # только исходные файлы, без нарезанных ступеней
        if re.search(r"-\d+\.[0-9a-f]{8}\.webp$", f.name):
            continue
        plain.setdefault(stem_of(f.name), f.name)

    changed = 0
    for lang in LANGS:
        p = SITE / lang / "index.html"
        if not p.is_file():
            continue
        s = p.read_text()
        before = s

        def fix(m):
            whole, path = m.group(0), m.group(1)
            stem = stem_of(path)
            if "srcset=" in whole:
                return whole
            if stem in sets:
                srcset, sz = sets[stem]
                srcset = re.sub(r'(^|, )media/', r"\1/media/", srcset)
                new_src = "/" + srcset.split(",")[0].strip().split(" ")[0].lstrip("/")
                return (whole.replace(path, new_src.lstrip("/") if path.startswith("media/") else new_src)
                        .replace("<img", f'<img srcset="{srcset}" sizes="{sz}"', 1))
            if stem in plain:
                return whole.replace(path, "/media/" + plain[stem])
            return whole

        s = re.sub(r'<img\b[^>]*?\bsrc="(/?media/[^"]+\.jpg)"[^>]*>', fix, s)

        # внутри <picture> решает <source>, а не <img>: пока там стоит
        # один файл без набора, браузер берёт именно его, и вся правка
        # <img> оказывается напрасной. На это и напоролся.
        def fix_source(m):
            path = m.group(1)
            stem = stem_of(path)
            if stem not in sets:
                return m.group(0)
            srcset, sz = sets[stem]
            srcset = re.sub(r'(^|, )media/', r"\1/media/", srcset)
            return f'<source srcset="{srcset}" sizes="{sz}" type="image/webp">'

        s = re.sub(r'<source srcset="(/?media/[^" ]+\.webp)" type="image/webp">', fix_source, s)
        if s != before:
            p.write_text(s)
            changed += 1
            print(f"  {lang}: снимки переведены на webp с набором")

    print(f"языковых страниц поправлено: {changed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
