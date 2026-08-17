#!/usr/bin/env python3
"""SAM.gov ежедневный скан по NAICS-категориям ISP. Дельта к прошлому скану."""
import json, os, sys, urllib.request, datetime, glob

CATS = {
    "materials":   ["212319", "212321", "423320"],
    "equipment":   ["423810", "333120"],
    "furniture":   ["337127", "337214", "337215"],
    "janitorial":  ["561720", "561740"],
    "landscaping": ["561730"],
    "painting":    ["238320"],
    "flooring":    ["238330", "238340"],
    "debris":      ["562111", "562119", "562910"],
}
DISC = os.path.join(os.path.dirname(__file__), "..", "discovery")
REP = os.path.join(os.path.dirname(__file__), "..", "reports")

def fetch(naics, size=100):
    url = (f"https://sam.gov/api/prod/sgs/v1/search/?index=opp&is_active=true"
           f"&naics={naics}&sort=-modifiedDate&page=0&size={size}")
    req = urllib.request.Request(url, headers={"Accept": "application/hal+json"})
    d = json.load(urllib.request.urlopen(req, timeout=60))
    return d.get("_embedded", {}).get("results", []) if isinstance(d.get("_embedded"), dict) else []

def norm(r, naics, cat):
    sa = ""
    sol = r.get("solicitation") or {}
    if isinstance(sol, dict):
        sao = sol.get("setAside") or {}
        sa = sao.get("value", "") if isinstance(sao, dict) else ""
    pw = r.get("placeOfPerformance") or {}
    state = ""
    if isinstance(pw, dict):
        st = pw.get("state") or {}
        state = st.get("code", "") if isinstance(st, dict) else ""
    dl = r.get("responseDate") or ""
    if isinstance(dl, str) and "T" in dl: dl = dl.split("T")[0]
    pd = r.get("publishDate") or ""
    if isinstance(pd, str) and "T" in pd: pd = pd.split("T")[0]
    return {
        "id": r.get("_id") or r.get("id", ""),
        "title": (r.get("title") or "").strip(),
        "sol": r.get("solicitationNumber", "") or "",
        "naics": naics, "type": (r.get("type") or {}).get("value", "") if isinstance(r.get("type"), dict) else "",
        "posted": pd, "deadline": dl, "state": state, "setaside": sa, "cat": cat,
        "link": f"https://sam.gov/opp/{r.get('_id') or r.get('id','')}/view",
    }

def main():
    today = datetime.date.today().isoformat()
    seen, out = {}, []
    for cat, codes in CATS.items():
        for naics in codes:
            try:
                for r in fetch(naics):
                    o = norm(r, naics, cat)
                    if not o["id"]: continue
                    if o["id"] in seen:
                        if cat not in seen[o["id"]]["cats"]: seen[o["id"]]["cats"].append(cat)
                        continue
                    o2 = dict(o); o2["cats"] = [cat]; del o2["cat"]
                    seen[o["id"]] = o2; out.append(o2)
            except Exception as e:
                print(f"WARN {naics}: {repr(e)[:80]}", file=sys.stderr)
    # прошлый скан
    prior = sorted(glob.glob(os.path.join(DISC, "sam-2026-*.json")))
    prior = [p for p in prior if today not in p]
    prev_ids = set()
    if prior:
        try: prev_ids = {x["id"] for x in json.load(open(prior[-1]))}
        except Exception: pass
    new = [o for o in out if o["id"] not in prev_ids]
    # запись json
    jpath = os.path.join(DISC, f"sam-{today}.json")
    json.dump(out, open(jpath, "w"), ensure_ascii=False)
    # разбивка
    from collections import Counter
    by_cat = Counter(c for o in out for c in o["cats"])
    new_by_cat = Counter(c for o in new for c in o["cats"])
    print(f"TOTAL active: {len(out)} | NEW vs {os.path.basename(prior[-1]) if prior else 'n/a'}: {len(new)}")
    print("by_cat:", dict(by_cat))
    print("new_by_cat:", dict(new_by_cat))
    # markdown отчёт
    lines = [f"# SAM.gov скан {today}", "",
             f"Активных по категориям ISP: **{len(out)}** · Новых со прошлого скана "
             f"({os.path.basename(prior[-1]) if prior else 'n/a'}): **{len(new)}**", "",
             "## По категориям (активно / новых)", ""]
    for c in CATS:
        lines.append(f"- **{c}**: {by_cat.get(c,0)} / +{new_by_cat.get(c,0)}")
    # TOP supply новинки (materials/furniture/equipment)
    supply_new = [o for o in new if any(c in ("materials","furniture","equipment") for c in o["cats"])]
    lines += ["", f"## Новые SUPPLY (материалы/мебель/техника) — {len(supply_new)}", ""]
    for o in sorted(supply_new, key=lambda x: x["deadline"] or "9999")[:40]:
        lines.append(f"- `{o['deadline'] or '—'}` [{'/'.join(o['cats'])}] **{o['title'][:70]}** "
                     f"({o['naics']}, {o['state'] or '—'}, {o['setaside'] or 'open'}) — {o['link']}")
    # прочие новые услуги
    svc_new = [o for o in new if o not in supply_new]
    lines += ["", f"## Новые УСЛУГИ (painting/flooring/janitorial/landscape/debris) — {len(svc_new)}", ""]
    for o in sorted(svc_new, key=lambda x: x["deadline"] or "9999")[:30]:
        lines.append(f"- `{o['deadline'] or '—'}` [{'/'.join(o['cats'])}] {o['title'][:70]} "
                     f"({o['state'] or '—'}, {o['setaside'] or 'open'}) — {o['link']}")
    open(os.path.join(REP, f"{today}-sam-scan.md"), "w").write("\n".join(lines))
    print("wrote", jpath, "and report")

if __name__ == "__main__":
    main()
