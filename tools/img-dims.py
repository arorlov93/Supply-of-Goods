# -*- coding: utf-8 -*-
"""Проставляет width и height картинкам, у которых их нет.

Зачем. Пока браузер не скачал картинку, он не знает её пропорций и
отводит под неё нулевую высоту. Картинка приезжает, занимает место, и всё
под ней съезжает вниз. Это сдвиг макета, он считается в Core Web Vitals и
он же раздражает человека, который уже начал читать.

Атрибуты width и height решают это полностью: браузер резервирует место
заранее. Числа нужны натуральные, из самого файла, а не выдуманные:
масштабирование потом сделает CSS, а пропорция берётся отсюда.

Замер до правки: 52 случая на 13 файлах.

Запуск: python3.13 tools/img-dims.py
Повторный запуск ничего не меняет.
"""
import pathlib, re, sys
from PIL import Image

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
IMG = re.compile(r"<img\b[^>]*>", re.I)
SRC = re.compile(r'\bsrc="([^"]+)"')
HAS = re.compile(r'\b(width|height)=')

size_cache = {}


def natural(src, page):
    """Натуральный размер файла, на который ссылается src."""
    if src.startswith("http") or src.startswith("data:"):
        return None
    rel = src.lstrip("/")
    for base in (page.parent, SITE):
        f = (base / rel).resolve()
        if f.is_file():
            if f not in size_cache:
                try:
                    size_cache[f] = Image.open(f).size
                except Exception:
                    size_cache[f] = None
            return size_cache[f]
    return None


def main():
    fixed = pages = 0
    missing = []
    for p in sorted(SITE.rglob("*.html")):
        if p.name == "crm.html":
            continue
        s = p.read_text()
        out, last, changed = [], 0, 0

        for m in IMG.finditer(s):
            tag = m.group(0)
            if HAS.search(tag):
                continue
            sm = SRC.search(tag)
            if not sm:
                continue
            dim = natural(sm.group(1), p)
            if not dim:
                missing.append(f"{p.name}: {sm.group(1)}")
                continue
            new = tag[:-1].rstrip() + f' width="{dim[0]}" height="{dim[1]}">'
            out.append(s[last:m.start()] + new)
            last = m.end()
            changed += 1

        if changed:
            p.write_text("".join(out) + s[last:])
            fixed += changed
            pages += 1

    print(f"размеры проставлены: {fixed} картинок на {pages} страницах")
    for x in missing[:10]:
        print("  файл не найден:", x)
    return 0


if __name__ == "__main__":
    sys.exit(main())
