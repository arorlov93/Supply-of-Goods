# -*- coding: utf-8 -*-
"""Ежедневная часть индекса: валюта, в которой выставлен счёт.

Почему именно курс, а не что-нибудь ещё. Страницу просили обновлять
каждый день, и обновлять её надо тем, что действительно меняется каждый
день. Таможенная статистика так не меняется: у неё годовой и месячный
шаг. А вот курс валюты, в которой продавец выставляет счёт, меняется
ежедневно, и для импортёра это не украшение, а прямая статья: счёт в
евро, подписанный в понедельник и оплаченный через месяц, стоит других
денег.

Источник: Европейский центральный банк, справочные курсы. Публикуются
каждый рабочий день около 16:00 по Центральной Европе, бесплатно, без
ключа, и это тот источник, на который ссылаются банки. Берётся файл за
последние 90 дней, чтобы считать не только сегодняшнее значение, но и
движение за месяц: одна цифра без движения ничего не говорит.

Что считается. ЕЦБ публикует, сколько единиц валюты даёт один евро.
Нам нужно обратное и в долларах: сколько долларов стоит единица валюты
продавца. Это курс доллара к евро, делённый на курс нужной валюты к
евро. Для самого евро это просто курс доллара.

Выходные и праздники. ЕЦБ в эти дни не публикует, файл остаётся
вчерашним. Это не ошибка, и подменять дату нельзя: на странице стоит та
дата, которой данные, а не та, когда мы их взяли.

Запуск: python3.13 tools/fx-daily.py
Результат: data/fx.json. Дальше tools/offer-pages.py вставляет блок на
страницу индекса.
"""
import json, pathlib, subprocess, sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data"
URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml"
NS = {"e": "http://www.ecb.int/vocabulary/2002-08-01/eurofxref"}

# Валюты, в которых продавцы на наших коридорах выставляют счёт.
# Подпись это не название валюты, а ответ на вопрос «кто этим платит».
WANT = [
    ("EUR", "European Union, Poland in euro contracts"),
    ("CNY", "China"),
    ("TRY", "Türkiye"),
    ("PLN", "Poland"),
    ("INR", "India"),
    ("KRW", "Korea"),
]

BACK = 22          # торговых дней в месяце, примерно


def main():
    r = subprocess.run(["curl", "-sS", "-m", "60", URL], capture_output=True, text=True)
    if r.returncode != 0:
        print("не скачалось:", r.stderr[:200])
        return 1

    days = ET.fromstring(r.stdout).findall(".//e:Cube[@time]", NS)
    if not days:
        print("в файле нет дней")
        return 1
    # в файле ЕЦБ первым идёт самый свежий день
    def table(node):
        return {c.get("currency"): float(c.get("rate")) for c in node}

    today, tdate = table(days[0]), days[0].get("time")
    back_i = min(BACK, len(days) - 1)
    past, pdate = table(days[back_i]), days[back_i].get("time")

    rows = []
    for code, who in WANT:
        def usd(t):
            if code == "EUR":
                return t.get("USD")
            if not t.get("USD") or not t.get(code):
                return None
            return t["USD"] / t[code]
        a, b = usd(today), usd(past)
        if not a or not b:
            continue
        rows.append({
            "code": code, "who": who,
            "usd": round(a, 6),
            "change": round((a - b) / b * 100, 2),
        })

    doc = {"source": "European Central Bank reference rates",
           "source_url": "https://www.ecb.europa.eu/stats/eurofxref/",
           "date": tdate, "compared_to": pdate, "rows": rows}
    OUT.mkdir(exist_ok=True)
    (OUT / "fx.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1))

    print(f"курсы на {tdate}, сравнение с {pdate}")
    for r_ in rows:
        print(f"   1 {r_['code']} = ${r_['usd']:.6f}  за месяц {r_['change']:+.2f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
