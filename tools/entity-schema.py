# -*- coding: utf-8 -*-
"""Опознавательные признаки компании в разметке данных.

Зачем. И поисковику, и языковой модели мало знать, что на странице
написано «ISP Group». Названий, похожих на наше, в мире десятки: по
запросу «ISP Group» первым выходит швейцарская финансовая компания
ispgroup.com. Чтобы нас не путали, машине нужны признаки, которые
принадлежат только нам и проверяются в чужом реестре.

У нас такие есть и они открытые:

    UEI  WA46PAMTYMQ7   единый идентификатор в системе SAM
    CAGE 217F4          код поставщика в государственных закупках США

Оба проверяются в SAM.gov по номеру. Для государственного покупателя,
который ищет поставщика, это прямое попадание, а для языковой модели
это якорь: по такому номеру компания определяется однозначно.

Добавляется заодно то, чего в разметке просто не было: телефон,
логотип и точка контакта.

Ничего не выдумано: все значения взяты из карточки компании.

Запуск: python3.13 tools/entity-schema.py
Повторный запуск ничего не дублирует.
"""
import json, pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
HOST = "https://ispgroupgc.com"

ADD = {
    "telephone": "+1-929-830-0038",
    "logo": f"{HOST}/brand/favicon-512.png",
    "image": f"{HOST}/brand/favicon-512.png",
    "identifier": [
        {
            "@type": "PropertyValue",
            "name": "Unique Entity ID (SAM.gov)",
            "propertyID": "UEI",
            "value": "WA46PAMTYMQ7",
        },
        {
            "@type": "PropertyValue",
            "name": "CAGE Code",
            "propertyID": "CAGE",
            "value": "217F4",
        },
    ],
    "contactPoint": [
        {
            "@type": "ContactPoint",
            "contactType": "sales",
            "email": "info@ispgroupgc.com",
            "telephone": "+1-929-830-0038",
            "availableLanguage": ["en", "fr", "es", "de", "ru"],
        }
    ],
}

BLOCK = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)


def enrich(obj):
    """Дополняет узел Organization, не трогая то, что там уже есть."""
    if not isinstance(obj, dict):
        return False
    hit = False
    if obj.get("@type") == "Organization" and obj.get("name") == "ISP GROUP LLC":
        for k, v in ADD.items():
            if k not in obj:
                obj[k] = v
                hit = True
    for v in obj.values():
        if isinstance(v, dict):
            hit = enrich(v) or hit
        elif isinstance(v, list):
            for it in v:
                hit = enrich(it) or hit
    return hit


def main():
    touched = 0
    for p in sorted(SITE.rglob("*.html")):
        if p.name == "crm.html":
            continue
        s = p.read_text()
        out, last, changed = [], 0, False

        for m in BLOCK.finditer(s):
            try:
                d = json.loads(m.group(1))
            except Exception:
                continue
            if not enrich(d):
                continue
            new = json.dumps(d, ensure_ascii=False, indent=1)
            out.append(s[last : m.start(1)] + new)
            last = m.end(1)
            changed = True

        if changed:
            p.write_text("".join(out) + s[last:])
            touched += 1

    print(f"страниц с опознавательными признаками: {touched}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
