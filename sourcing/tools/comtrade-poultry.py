#!/usr/bin/env python3
"""UN Comtrade: фактические цены сделок по мясу птицы.

Таможенная статистика показывает не котировку, а то, почём товар реально
пересёк границу: сумма FOB делится на фактический нетто-вес. Для вопроса
«где дешевле купить» это ближе к истине, чем любой прайс, потому что
в цифре уже сидят все скидки, которые продавец реально дал.
"""
import json, subprocess, os, sys, time

BASE = "https://comtradeapi.un.org/public/v1/preview/C/A/HS"
CACHE = "ctcache"

REP = {76: "Бразилия", 616: "Польша", 276: "Германия", 250: "Франция",
       842: "США", 643: "Россия", 792: "Турция", 528: "Нидерланды",
       380: "Италия", 724: "Испания", 152: "Чили"}
AFR = {768: "Того", 204: "Бенин", 566: "Нигерия", 288: "Гана",
       384: "Кот-д'Ивуар", 562: "Нигер", 854: "Буркина-Фасо", 686: "Сенегал",
       266: "Габон", 178: "Конго", 180: "ДР Конго", 120: "Камерун",
       226: "Экв. Гвинея", 24: "Ангола", 710: "ЮАР", 270: "Гамбия",
       694: "Сьерра-Леоне", 430: "Либерия", 324: "Гвинея", 140: "ЦАР",
       148: "Чад", 466: "Мали", 478: "Мавритания", 0: "ВЕСЬ МИР"}
CMD = {"020714": "курица, части мороженые",
       "020727": "индейка, части мороженые",
       "020712": "курица, тушка мороженая",
       "020725": "индейка, тушка мороженая"}


def get(rep, cmd, year):
    os.makedirs(CACHE, exist_ok=True)
    p = f"{CACHE}/{rep}_{cmd}_{year}.json"
    if not os.path.exists(p):
        url = (f"{BASE}?reporterCode={rep}&period={year}&cmdCode={cmd}&flowCode=X")
        out = subprocess.run(["curl", "-s", "--max-time", "90", url],
                             capture_output=True).stdout
        if len(out) < 100:
            return []
        open(p, "wb").write(out)
        time.sleep(1)
    try:
        return json.load(open(p)).get("data") or []
    except Exception:
        return []


def rows(rep, cmd, year):
    out = {}
    for x in get(rep, cmd, year):
        if x.get("customsCode") != "C00" or x.get("partner2Code") != 0:
            continue
        w = x.get("netWgt") or 0
        v = x.get("primaryValue") or 0
        if w > 0:
            pc = x["partnerCode"]
            a, b = out.get(pc, (0, 0))
            out[pc] = (a + w, b + v)
    return out


def show(rep, cmd, year, only=None, top=14):
    r = rows(rep, cmd, year)
    if not r:
        print(f"\n{REP.get(rep, rep)} · {CMD.get(cmd, cmd)} · {year}: нет данных")
        return
    world = r.get(0)
    print(f"\n### {REP.get(rep, rep)} · {CMD.get(cmd, cmd)} · {year}")
    if world:
        print(f"   {'весь мир':22} {world[0]/1000:>10,.0f} т  {world[1]/world[0]:>6.2f} $/кг")
    lst = [(p, w, v) for p, (w, v) in r.items() if p != 0 and w >= 100_000]
    if only:
        lst = [x for x in lst if x[0] in only]
    lst.sort(key=lambda x: x[1] / x[1] and (x[2] / x[1]))   # по цене, от дешёвых
    for p, w, v in lst[:top]:
        name = AFR.get(p) or REP.get(p) or f"код {p}"
        print(f"   {name:22} {w/1000:>10,.0f} т  {v/w:>6.2f} $/кг")


if __name__ == "__main__":
    for cmd in ("020727", "020714"):
        for year in (2024, 2025):
            show(76, cmd, year, only=set(AFR))
    print("\n" + "=" * 70)
    for rep in (616, 276, 842, 643, 792):
        for cmd in ("020727", "020714"):
            show(rep, cmd, 2024, only=set(AFR), top=8)
