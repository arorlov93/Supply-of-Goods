# -*- coding: utf-8 -*-
"""Счётчик без cookie: режим согласия вместо client_storage.

Сначала тег ставился с настройкой `client_storage: 'none'`. На живом
сайте замер показал, что она не действует: GA4 всё равно писал _ga и
_ga_8HDRVVXJFF. Проверены четыре варианта на отдельных страницах, cookie
после загрузки:

    client_storage: 'none'                 2 cookie
    storage: 'none'                        2 cookie
    client_storage + свой client_id        2 cookie
    consent default analytics_storage      0 cookie

Значит, единственный работающий запрет хранилища это режим согласия, и
объявлять его нужно до config, иначе тег успевает поставить cookie.

Чем платим. Без cookie GA не отличает вернувшегося человека от нового,
поэтому число посетителей будет завышено. Посещения страниц, источники
переходов и события заявки считаются по-прежнему, а именно они и нужны,
чтобы понимать, какие страницы приводят заказчиков. Политика сайта при
этом остаётся правдой, а она опубликована.

Запуск: python3.13 tools/analytics-consent.py
Повторный запуск ничего не дублирует.
"""
import pathlib, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
GA = "G-8HDRVVXJFF"

OLD = (f"  gtag('config', '{GA}', {{ client_storage: 'none', anonymize_ip: true }});")

NEW = (
    "  /* Запрет хранилища объявляется до config: иначе тег успевает\n"
    "     поставить cookie. Настройка client_storage в GA4 не действует,\n"
    "     это проверено замером. */\n"
    "  gtag('consent', 'default', { analytics_storage: 'denied', ad_storage: 'denied' });\n"
    f"  gtag('config', '{GA}', {{ anonymize_ip: true }});"
)


def main():
    done = skipped = 0
    for p in sorted(SITE.rglob("*.html")):
        s = p.read_text()
        if "analytics_storage" in s:
            skipped += 1
            continue
        if OLD not in s:
            if GA in s:
                print(f"  ВНИМАНИЕ: тег есть, но строка config не та: {p.relative_to(SITE)}")
            skipped += 1
            continue
        p.write_text(s.replace(OLD, NEW, 1))
        done += 1
    print(f"переведено на режим согласия: {done}, пропущено: {skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
