# -*- coding: utf-8 -*-
"""Индекс стоимости доставки: сбор данных.

Что считаем и почему именно это. Таможенная статистика ООН публикует по
каждому направлению и товарной группе две суммы сразу: стоимость товара
на условиях FOB и ту же партию на условиях CIF. Разница между ними это
фрахт и страхование, посчитанные не нами, а таможнями стран-импортёров
по фактическим декларациям.

Эту разницу в процентах почти никто не публикует в пригодном для чтения
виде, а она и есть та самая строка, которую забывают в предложениях: на
керамической плитке из Вьетнама она 26 процентов, из Германии 11. То
есть выбор происхождения меняет цену до ворот сильнее, чем торг по цене
завода, и это видно по открытым данным, а не с наших слов.

Источник: UN Comtrade, открытый просмотровый интерфейс, без ключа.
Отчитывающаяся страна по умолчанию США: сайт обращён к американскому
покупателю, и декларации США это то, что он может проверить сам.

Что отбрасываем и почему. Строки без веса или без одной из двух сумм
считать нечем. Строки, где надбавка меньше процента или больше
шестидесяти, почти всегда артефакт отчётности, а не настоящий фрахт:
такие в таблицу не идут, но их число печатается и указывается на
странице, чтобы отбор был виден.

Запуск: python3.13 tools/lpi-fetch.py [год]
Результат: data/lpi-<год>.json. Повторный запуск перезаписывает файл.
"""
import json, pathlib, subprocess, sys, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data"
API = "https://comtradeapi.un.org/public/v1/preview/C/A/HS"

REPORTER = 842          # США
REPORTER_NAME = "United States"

# Товарные группы по шести категориям сайта. Четыре знака HS: на этом
# уровне данные есть у всех стран, а шесть знаков во многих отчётах
# рассыпаются на нули.
GROUPS = [
    ("Building and finishing materials", [
        ("6802", "Worked stone"),
        ("6907", "Ceramic and porcelain tile"),
        ("2523", "Cement"),
    ]),
    ("Industrial equipment and machinery", [
        ("8413", "Pumps for liquids"),
        ("8414", "Compressors, fans, air pumps"),
        ("8428", "Lifting and handling machinery"),
    ]),
    ("Tools, hardware and fasteners", [
        ("8467", "Hand tools, pneumatic and powered"),
        ("8207", "Interchangeable tool parts"),
        ("7318", "Screws, bolts and fasteners"),
    ]),
    ("Metals and pipe", [
        ("7308", "Structures of iron or steel"),
        ("7304", "Seamless tube and pipe"),
        ("7306", "Welded tube and pipe"),
    ]),
    ("Paper, packaging and consumables", [
        ("4804", "Kraft paper and paperboard"),
        ("4810", "Coated paper and paperboard"),
        ("4819", "Cartons, boxes and cases"),
    ]),
    ("Food and agricultural goods", [
        ("0207", "Poultry meat and offal"),
        ("0303", "Frozen fish"),
    ]),
]

PARTNERS = {
    156: "China", 792: "Türkiye", 276: "Germany", 380: "Italy",
    699: "India", 704: "Viet Nam", 616: "Poland", 410: "Korea, Rep.",
}

MIN_UPLIFT = 1.0        # ниже процента это не фрахт, а особенность отчёта
MAX_UPLIFT = 60.0       # выше шестидесяти тоже
MIN_WEIGHT = 50_000     # килограммы: на мелких партиях удельные цифры скачут


def pull(period, codes):
    """Один запрос на несколько товаров сразу: у просмотрового интерфейса
    есть предел по числу обращений, а не по размеру ответа."""
    url = (f"{API}?reporterCode={REPORTER}&period={period}"
           f"&partnerCode={','.join(str(p) for p in PARTNERS)}"
           f"&cmdCode={','.join(codes)}&flowCode=M")
    # через curl, потому что исходящие запросы идут через прокси, и
    # python-urllib он отбивает кодом 403
    r = subprocess.run(["curl", "-sS", "-m", "90", url],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"curl: {r.stderr[:200]}")
    return json.loads(r.stdout).get("data", [])


def main(argv):
    period = argv[0] if argv else "2024"
    OUT.mkdir(exist_ok=True)

    names = {c: n for _, items in GROUPS for c, n in items}
    rows, dropped = [], 0

    for group, items in GROUPS:
        codes = [c for c, _ in items]
        data = pull(period, codes)
        for r in data:
            w = r.get("netWgt") or 0
            cif = r.get("cifvalue") or 0
            fob = r.get("fobvalue") or 0
            code = str(r.get("cmdCode"))
            partner = PARTNERS.get(r.get("partnerCode"))
            if not (w and cif and fob and partner and code in names):
                dropped += 1
                continue
            if w < MIN_WEIGHT:
                dropped += 1
                continue
            up = (cif - fob) / fob * 100
            if not (MIN_UPLIFT <= up <= MAX_UPLIFT):
                dropped += 1
                continue
            rows.append({
                "group": group, "hs": code, "product": names[code],
                "origin": partner,
                "cif_kg": round(cif / w, 3), "fob_kg": round(fob / w, 3),
                "uplift": round(up, 1), "tonnes": round(w / 1000),
            })
        print(f"  {group}: собрано {len([x for x in rows if x['group']==group])}")
        time.sleep(1.5)

    rows.sort(key=lambda x: (x["group"], x["hs"], x["origin"]))
    doc = {
        "source": "UN Comtrade",
        "source_url": "https://comtradeplus.un.org/",
        "reporter": REPORTER_NAME,
        "period": period,
        "flow": "imports",
        "built": time.strftime("%Y-%m-%d"),
        "dropped": dropped,
        "rows": rows,
    }
    path = OUT / f"lpi-{period}.json"
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=1))
    print(f"строк в индексе: {len(rows)}, отброшено: {dropped}")
    print("записано:", path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
