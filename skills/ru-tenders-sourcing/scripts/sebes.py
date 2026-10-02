#!/usr/bin/env python3
"""Себестоимость по позициям спецификаций: поиск закупочной цены у поставщиков.

Жёсткое ограничение среды: исходящий IP американский, и большинство российских
магазинов его режут (403) либо рисуют цены в браузере. Работают те сайты, где
выдача поиска приходит с сервера уже с ценами. Для каждой такой площадки свой
адаптер; остальные позиции честно помечаются как «цена не получена», а не
придумываются.
"""
import re, sys, json, html, subprocess, urllib.parse, os, csv, time

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")
CACHE = "pricecache"


def get(url, headers=()):
    os.makedirs(CACHE, exist_ok=True)
    key = os.path.join(CACHE, re.sub(r"\W+", "_", url)[-120:] + ".html")
    if os.path.exists(key) and os.path.getsize(key) > 500:
        return open(key, encoding="utf-8", errors="replace").read()
    cmd = ["curl", "-sL", "--max-time", "45", "-A", UA]
    for h in headers:
        cmd += ["-H", h]
    out = subprocess.run(cmd + [url], capture_output=True).stdout.decode("utf-8", "replace")
    if len(out) > 500:
        open(key, "w").write(out)
    return out


def lines_of(h):
    h = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", "\n", h))
    return [" ".join(x.split()) for x in t.split("\n") if x.strip()]


MONEY = re.compile(r"^(\d[\d  ]{2,})\s*(?:р\.|₽|руб)")


def num(s):
    return int(re.sub(r"\D", "", s))


# ------------------------------------------------------------- СОЮЗСПЕЦОДЕЖДА

def soyuz(query, limit=12):
    """Выдача поиска приходит с сервера и содержит оптовую цену. -> [(имя, опт, розн)]"""
    u = ("https://www.specodegda.ru/search/catalog/?q="
         + urllib.parse.quote(query))
    ls = lines_of(get(u, ["X-Requested-With: XMLHttpRequest"]))
    out, i = [], 0
    while i < len(ls):
        if ls[i] == "Оптом:":
            # имя — ближайшая осмысленная строка выше
            name = ""
            for j in range(i - 1, max(-1, i - 6), -1):
                if len(ls[j]) > 12 and not MONEY.match(ls[j]) and ls[j] not in (
                        "Распродажа", "Новинка", "Хит", "В розницу:"):
                    name = ls[j]
                    break
            opt = roz = None
            k = i + 1
            vals = []
            while k < len(ls) and k < i + 7:
                if MONEY.match(ls[k]):
                    vals.append(num(ls[k]))
                elif ls[k] == "В розницу:":
                    pass
                elif len(ls[k]) > 12:
                    break
                k += 1
            if vals:
                opt = min(vals)          # опт со скидкой — самая низкая из показанных
                roz = max(vals)
            if name and opt:
                out.append((name, opt, roz))
            i = k
        else:
            i += 1
    uniq, seen = [], set()
    for n, o, r in out:
        if n in seen:
            continue
        seen.add(n)
        uniq.append((n, o, r))
    return uniq[:limit]


ADAPTERS = {"СОЮЗСПЕЦОДЕЖДА": soyuz}


# ----------------------------------------------------------------- сопоставление

STOP = set("""для и с из на по не или аналог шт компл пар кг или т мм см м
защиты от тип вид цвет размер гост ту серия модель""".split())


def tokens(s):
    s = s.lower().replace("ё", "е")
    s = re.sub(r"\(.*?\)", " ", s)
    return [w for w in re.findall(r"[а-яa-z0-9]{3,}", s) if w not in STOP]


def score(spec_name, cand_name):
    a, b = set(tokens(spec_name)), set(tokens(cand_name))
    if not a or not b:
        return 0.0
    return len(a & b) / len(a)


def query_for(name):
    """Короткий запрос: первые значимые слова, без характеристик в скобках."""
    t = tokens(name)
    return " ".join(t[:4])


def run(no, adapter="СОЮЗСПЕЦОДЕЖДА", minscore=0.34):
    d = json.load(open(f"spec/{no}.json"))
    fn = ADAPTERS[adapter]
    rows = []
    for it in d["items"]:
        q = query_for(it["name"])
        try:
            cands = fn(q)
        except Exception as e:
            cands = []
            print(f"   ! {q}: {e}", file=sys.stderr)
        scored = sorted(((score(it["name"], cn), cn, opt, roz)
                         for cn, opt, roz in cands), key=lambda x: -x[0])
        ok = [x for x in scored if x[0] >= minscore]
        # из подходящих берём самую дешёвую: на тендере считать надо по минимуму,
        # а не по первому попавшемуся совпадению
        best = min(ok, key=lambda x: x[2]) if ok else None
        rows.append({**it, "q": q, "match": best[1] if best else None,
                     "score": round(best[0], 2) if best else None,
                     "cost": best[2] if best else None,
                     "retail": best[3] if best else None,
                     "source": adapter if best else None,
                     "alts": [{"name": c, "opt": o, "roz": r, "score": round(s, 2)}
                              for s, c, o, r in scored[:6]]})
        time.sleep(0.4)
    return d, rows


def report(no, d, rows):
    nmck = d["nmck"]
    got = [r for r in rows if r["cost"]]
    print(f"\n{'='*92}\n№{no}  НМЦК {nmck:,} ₽  позиций {len(rows)}, "
          f"цена поставщика найдена по {len(got)}")
    print(f"   {'позиция':48} {'кол':>7} {'НМЦ/ед':>10} {'закуп':>9} {'марж%':>7}")
    for r in rows:
        m = ""
        if r["cost"] and r["price"]:
            m = f"{(r['price'] - r['cost']) / r['price'] * 100:5.1f}%"
        print(f"   {r['name'][:48]:48} {r['qty'] if r['qty'] is not None else '':>7} "
              f"{r['price'] if r['price'] is not None else '':>10} "
              f"{r['cost'] if r['cost'] else '':>9} {m:>7}")
        for a in r.get("alts", [])[:4]:
            mark = "→" if a["name"] == r["match"] else " "
            print(f"     {mark} {a['opt'] if a['opt'] else '':>8} опт | "
                  f"{a['score']:.2f} | {a['name'][:66]}")
    tot_n = sum(r["qty"] * r["price"] for r in rows if r["qty"] and r["price"])
    tot_c = sum(r["qty"] * r["cost"] for r in rows if r["qty"] and r["cost"])
    cov = sum(r["qty"] * r["price"] for r in rows if r["qty"] and r["price"] and r["cost"])
    if tot_c:
        print(f"\n   покрыто ценами поставщика: {cov:,.0f} ₽ из {tot_n:,.0f} ₽ НМЦ "
              f"({cov / tot_n * 100:.0f} %)")
        print(f"   закупка по покрытой части: {tot_c:,.0f} ₽, маржа {cov - tot_c:,.0f} ₽ "
              f"({(cov - tot_c) / cov * 100:.1f} %)")
    os.makedirs("sebes", exist_ok=True)
    json.dump({"no": no, "nmck": nmck, "rows": rows},
              open(f"sebes/{no}.json", "w"), ensure_ascii=False, indent=1)
    with open(f"sebes/{no}.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["#", "позиция", "ед", "кол-во", "НМЦ за ед", "закупка за ед",
                    "маржа за ед", "маржа %", "что нашли", "совпадение", "источник"])
        for i, r in enumerate(rows, 1):
            mg = (r["price"] - r["cost"]) if r["cost"] and r["price"] else ""
            mp = (round((r["price"] - r["cost"]) / r["price"] * 100, 1)
                  if r["cost"] and r["price"] else "")
            w.writerow([i, r["name"], r["unit"], r["qty"], r["price"], r["cost"],
                        mg, mp, r["match"], r["score"], r["source"]])


if __name__ == "__main__":
    for a in sys.argv[1:]:
        no = int(a)
        d, rows = run(no)
        report(no, d, rows)
