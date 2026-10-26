# -*- coding: utf-8 -*-
"""Убрать из библиотеки кадры, которые больше нигде не стоят.

После замены неподходящих снимков в media осталось несколько файлов,
на которые не ссылается ни одна страница: кузова, сборочная линия, карьер,
офицеры таможни, пляж. Лежать им там незачем: они попадают в выкладку, и,
что хуже, остаются в титрах, где выглядят как используемые.

Страница титров собирается из CREDITS.json, поэтому чистится и он.
Оригиналы в media-src остаются: вернуть кадр дешевле, чем искать заново.

Запуск: python3.13 tools/media-prune.py          показать, что лишнее
        python3.13 tools/media-prune.py --delete  удалить
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
MEDIA = SITE / "media"


def used():
    names = set()
    for p in SITE.rglob("*.html"):
        if p.name == "credits.html":        # титры ссылаются на всё подряд
            continue
        for m in re.finditer(r"media/([A-Za-z0-9_-]+)\.(?:jpg|webp)", p.read_text()):
            names.add(m.group(1))
    return names


def main(delete=False):
    keep = used()
    have = {p.stem for p in MEDIA.glob("*.jpg")}
    extra = sorted(have - keep)
    if not extra:
        print("лишних кадров нет")
        return
    print(f"не используется нигде: {len(extra)}")
    for n in extra:
        print("   ", n)
    if not delete:
        print("\nудалить: python3.13 tools/media-prune.py --delete")
        return
    cred = json.loads((MEDIA / "CREDITS.json").read_text())
    for n in extra:
        for ext in ("jpg", "webp"):
            f = MEDIA / f"{n}.{ext}"
            if f.exists():
                f.unlink()
        cred.pop(f"{n}.jpg", None)
    (MEDIA / "CREDITS.json").write_text(json.dumps(cred, ensure_ascii=False, indent=1))
    print(f"\nудалено файлов: {len(extra)}, в титрах осталось записей: {len(cred)}")


if __name__ == "__main__":
    main("--delete" in sys.argv)
