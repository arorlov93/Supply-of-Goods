# -*- coding: utf-8 -*-
"""Search Console: по каким запросам нас уже показывают.

Зачем. 28.10 выяснилось, что сайт в индексе и собирает показы, а я до
этого утверждал обратное на основании выдачи поискового инструмента.
Вывод был неверный, проверка негодная. Чтобы это не повторялось, данные
надо брать у самого Google, а не у посредника.

И это меняет порядок работы. Средняя позиция 19,3 это вторая страница
выдачи: показы есть, кликов почти нет. Вытащить на первую страницу то,
что уже висит на второй, дешевле и быстрее, чем писать новые страницы.
Но для этого надо знать, какие именно это запросы.

Ключ. Сервисный аккаунт Google, ключ в переменной окружения
GSC_SA_KEY, целиком JSON или он же в base64. В репозиторий ключ не
попадает и в переписке не передаётся, см. CLAUDE.md, пункт 5. Скрипт
ключ не печатает никогда, даже в отладке.

Доступ. Сервисному аккаунту должен быть выдан доступ к ресурсу в самой
Search Console: Настройки, Пользователи и разрешения, добавить почту
вида имя@проект.iam.gserviceaccount.com. Прав «Ограниченный» достаточно
для чтения.

Запуск:
    python3.13 tools/gsc.py              отчёт за 28 дней
    python3.13 tools/gsc.py 7            за 7 дней
    python3.13 tools/gsc.py 28 pages     разрез по страницам
"""
import base64, collections, datetime, json, os, sys

SITE = "sc-domain:ispgroupgc.com"
API = "https://searchconsole.googleapis.com/webmasters/v3/sites/%s/searchAnalytics/query"
SCOPE = ["https://www.googleapis.com/auth/webmasters.readonly"]


def creds():
    raw = os.environ.get("GSC_SA_KEY", "").strip()
    if not raw:
        print("нет переменной окружения GSC_SA_KEY.")
        print("Положить туда JSON сервисного аккаунта целиком или его base64.")
        print("В репозиторий ключ не класть и в переписку не присылать.")
        return None
    if not raw.lstrip().startswith("{"):
        try:
            raw = base64.b64decode(raw).decode("utf-8")
        except Exception:
            print("GSC_SA_KEY не похож ни на JSON, ни на base64 от него.")
            return None
    try:
        info = json.loads(raw)
    except Exception as e:
        print("GSC_SA_KEY не разбирается как JSON:", type(e).__name__)
        return None
    try:
        from google.oauth2 import service_account
    except ImportError:
        print("нет библиотеки google-auth. Поставить:")
        print("    pip install --break-system-packages google-auth requests")
        return None
    # почту аккаунта печатаем: по ней видно, какому адресу выдавать доступ
    print("  сервисный аккаунт:", info.get("client_email", "?"))
    return service_account.Credentials.from_service_account_info(info, scopes=SCOPE)


def query(cr, start, end, dims, limit=250, filters=None):
    import requests
    from google.auth.transport.requests import Request as GReq

    cr.refresh(GReq())
    body = {
        "startDate": start, "endDate": end,
        "dimensions": dims, "rowLimit": limit,
        "dataState": "all",
    }
    if filters:
        body["dimensionFilterGroups"] = [{"filters": filters}]
    r = requests.post(API % SITE.replace(":", "%3A"),
                      headers={"Authorization": "Bearer " + cr.token,
                               "Content-Type": "application/json"},
                      json=body, timeout=60)
    if r.status_code == 403:
        print("  403: у сервисного аккаунта нет доступа к ресурсу.")
        print("  Search Console, Настройки, Пользователи и разрешения,")
        print("  добавить почту аккаунта с правами «Ограниченный».")
        return None
    if not r.ok:
        print("  ошибка", r.status_code, r.text[:300])
        return None
    return r.json().get("rows", [])


def table(rows, head, n=25):
    if not rows:
        print("   нет данных")
        return
    print(f"   {head:52s} {'показы':>7s} {'клики':>6s} {'CTR':>6s} {'позиция':>8s}")
    for r in rows[:n]:
        k = " / ".join(r["keys"])[:52]
        print(f"   {k:52s} {r['impressions']:7.0f} {r['clicks']:6.0f} "
              f"{r['ctr']*100:5.1f}% {r['position']:8.1f}")


def main(argv):
    days = int(argv[0]) if argv and argv[0].isdigit() else 28
    mode = argv[1] if len(argv) > 1 else "all"

    cr = creds()
    if not cr:
        return 1

    end = datetime.date.today() - datetime.timedelta(days=1)
    start = end - datetime.timedelta(days=days - 1)
    s, e = start.isoformat(), end.isoformat()
    print(f"  период: {s} .. {e}\n")

    tot = query(cr, s, e, [])
    if tot is None:
        return 1
    if tot:
        t = tot[0]
        print(f"  ИТОГО: показов {t['impressions']:.0f}, кликов {t['clicks']:.0f}, "
              f"CTR {t['ctr']*100:.2f}%, средняя позиция {t['position']:.1f}\n")
    else:
        print("  за период данных нет\n")

    if mode in ("all", "queries"):
        print("— ЗАПРОСЫ —")
        q = query(cr, s, e, ["query"]) or []
        table(q, "запрос")
        # то, ради чего всё: что висит на второй странице выдачи
        near = [r for r in q if 10 < r["position"] <= 25 and r["impressions"] >= 3]
        near.sort(key=lambda r: -r["impressions"])
        print(f"\n— БЛИЗКО К ПЕРВОЙ СТРАНИЦЕ (позиция 11-25, показов от 3): {len(near)} —")
        table(near, "запрос", 20)

    if mode in ("all", "pages"):
        print("\n— СТРАНИЦЫ —")
        p = query(cr, s, e, ["page"]) or []
        table(p, "страница", 25)

    if mode == "all":
        print("\n— СТРАНЫ —")
        table(query(cr, s, e, ["country"]) or [], "страна", 10)

    # сырые данные рядом, для разбора
    out = os.path.join(os.environ.get("TMPDIR", "/tmp"), "gsc-last.json")
    try:
        with open(out, "w", encoding="utf-8") as f:
            json.dump({"period": [s, e],
                       "queries": query(cr, s, e, ["query"], 500) or [],
                       "pages": query(cr, s, e, ["page"], 500) or []},
                      f, ensure_ascii=False, indent=1)
        print("\n  сырые данные:", out)
    except Exception as ex:
        print("  сырые данные не записал:", type(ex).__name__)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
