#!/usr/bin/env python3
"""Сбор живых тендеров с rostender.info — разбор HTML-таблицы.

Каждый лот — <article class="tender-row" id="...">. Берём: номер, закон (44/223),
название, ссылку, НМЦК, обеспечение контракта и заявки, регион, дату окончания.
Обеспечение важнее всего: для нового юрлица это живые деньги, а не «добросовестность».
"""
import json, re, subprocess, sys, time

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")
BASE = "https://rostender.info"


def fetch(url):
    return subprocess.run(["curl", "-s", "--max-time", "60", "-A", UA, url],
                          capture_output=True).stdout.decode("utf-8", "replace")


def txt(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    for a, b in (("&nbsp;", " "), ("&quot;", '"'), ("&amp;", "&"),
                 ("&#8381;", "₽"), ("&laquo;", "«"), ("&raquo;", "»")):
        s = s.replace(a, b)
    return " ".join(s.split())


def num(s):
    d = re.sub(r"[^\d]", "", txt(s))      # txt() сначала: иначе &#8381; даёт «8381»
    return int(d) if d else None


def one(pat, blk, g=1):
    m = re.search(pat, blk, re.S)
    return m.group(g) if m else ""


def parse(html):
    out = []
    for blk in re.split(r'<article class="tender-row', html)[1:]:
        title = txt(one(r'class="[^"]*tender-info__description[^"]*"[^>]*>(.*?)</a>', blk))
        if not title:
            continue
        href = one(r'class="[^"]*tender-info__description[^"]*"[^>]*href="([^"]+)"', blk)
        out.append({
            "num": txt(one(r'class="tender__number">(.*?)</span>', blk)).replace("Тендер", "").strip(),
            "law": "44-ФЗ" if 'tender__class b-44' in blk else ("223-ФЗ" if 'b-223' in blk else "?"),
            "title": title,
            "url": BASE + href if href.startswith("/") else href,
            "nmck": num(one(r'starting-price__price[^>]*>(.*?)</div>', blk)),
            "sec_contract": txt(one(r'Обеспечение контракта:\s*<span[^>]*>(.*?)</span>', blk)),
            "sec_bid": num(one(r'Обеспечение заявки:\s*<span[^>]*>(.*?)</span>', blk)),
            "region": txt(one(r'class="[^"]*line-clamp[^"]*"[^>]*data-id="address\d+">(.*?)</div>', blk)),
            "end": txt(one(r'class="black">(.*?)</span>', blk)),
            "smp": "СМП" if 'tender__smp-wrap' in blk and 'smp sprite' in blk else "",
        })
    return out


def grab(name, url):
    r = parse(fetch(url))
    print(f"\n### {name} — {len(r)} лотов  <{url}>")
    for x in sorted([y for y in r if y["nmck"]], key=lambda y: -y["nmck"])[:8]:
        print(f"  {x['nmck']:>12,} ₽  {x['law']:6} {x['title'][:70]}")
        print(f"  {'':14} {x['region'][:34]:34} до {x['end']:10} "
              f"обесп.к-та {x['sec_contract'] or '—'}, заявки {x['sec_bid'] or 0:,}")
    return r


CATS = {
    "канцелярские принадлежности": "/tendery-kancelyarskie-prinadlejnosti",
    "соль техническая / галит": "/tendery-tehnicheskie-soli",
    "антигололёдные реагенты": "/category/tendery-antigololednye-reagenty",
    "медрасходка, одноразовый инструмент": "/tendery-medicinskie-rashodnye-materialy-sredstva-reabilitacii-odnorazovyj-medicinskij-instrument",
    "медицинские дезсредства": "/tendery-medicinskie-dezinficiruyushchie-sredstva",
    "хозтовары, бытовая химия": "/tendery-hozyajstvennye-tovary-tovary-shirokogo-potrebleniya-bytovaya-himiya-i-parfyumeriya",
    "спецодежда и спецобувь": "/tendery-obuv-specobuv-odejda-specodejda",
}

if __name__ == "__main__":
    cats = dict(CATS)
    if len(sys.argv) > 1:
        cats = {a.split("=")[0]: a.split("=", 1)[1] for a in sys.argv[1:]}
    res = {}
    for name, path in cats.items():
        res[name] = grab(name, BASE + path if path.startswith("/") else path)
        time.sleep(0.4)
    json.dump(res, open("tenders.json", "w"), ensure_ascii=False, indent=1)
    print("\nитого лотов:", sum(len(v) for v in res.values()))
