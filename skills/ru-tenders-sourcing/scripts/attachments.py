#!/usr/bin/env python3
"""Достать объём в тоннах по конкретным лотам, чтобы посчитать цену за тонну.

Источники объёма, по убыванию надёжности:
  1. приложенный расчёт НМЦК (xlsx)
  2. описание объекта закупки / проект контракта (docx)
  3. само название лота, если объём вынесен туда
"""
import json, re, subprocess, sys, os, zipfile, io

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")


def fetch_bytes(url):
    return subprocess.run(["curl", "-sL", "--max-time", "60", "-A", UA, url],
                          capture_output=True).stdout


def meta(html):
    """tendersData -> {tender_id: [(title, link), ...]}"""
    m = re.search(r'var tendersData = Object\.assign\(PlansData,\s*(\{.*?\})\);', html, re.S)
    if not m:
        return {}
    blob = m.group(1)
    depth = 0
    end = None
    for i, ch in enumerate(blob):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    try:
        d = json.loads(blob[:end])
    except Exception:
        return {}
    return {tid: [(f.get("title", ""), f.get("link", ""))
                  for f in (t.get("files") or []) if f.get("link")]
            for tid, t in d.items() if isinstance(t, dict)}


def office_text(data):
    """Текст из xlsx/docx без внешних библиотек — распаковкой XML."""
    try:
        z = zipfile.ZipFile(io.BytesIO(data))
    except Exception:
        return ""
    out = []
    for n in z.namelist():
        if n.endswith(".xml") and re.search(r"sheet|document|sharedStrings", n):
            try:
                x = z.read(n).decode("utf-8", "replace")
            except Exception:
                continue
            x = re.sub(r"<[^>]+>", " ", x)
            out.append(x)
    return " ".join(" ".join(out).split())


TON = re.compile(
    r"(\d[\d  ]{0,12}(?:[.,]\d+)?)\s*(тонн\w*|т\.?\b|тн\b)", re.I)


def tons_from(text):
    hits = []
    for m in TON.finditer(text):
        v = m.group(1).replace(" ", "").replace(" ", "").replace(",", ".")
        try:
            v = float(v)
        except ValueError:
            continue
        if 10 <= v <= 200000:
            ctx = text[max(0, m.start() - 70):m.end() + 40]
            hits.append((v, " ".join(ctx.split())))
    return hits


if __name__ == "__main__":
    targets = set(sys.argv[1:])
    files = {}
    for pg in range(1, 6):
        url = "https://rostender.info/tendery-tehnicheskie-soli" + (f"?page={pg}" if pg > 1 else "")
        files.update(meta(fetch_bytes(url).decode("utf-8", "replace")))
    print("тендеров с вложениями:", len(files), file=sys.stderr)
    os.makedirs("docs", exist_ok=True)
    for tid, fl in files.items():
        if targets and tid not in targets:
            continue
        for title, link in fl:
            if not re.search(r"\.(xlsx|docx|xls|doc)$", title, re.I):
                continue
            data = fetch_bytes(link)
            if len(data) < 500:
                continue
            open(f"docs/{tid}_{re.sub(r'[^A-Za-zА-Яа-я0-9.]', '_', title)}", "wb").write(data)
            t = office_text(data)
            hits = tons_from(t)
            print(f"\n=== {tid} · {title} · {len(data)} байт")
            for v, ctx in hits[:6]:
                print(f"   {v:>10,.1f} т | {ctx[:130]}")
            for m in re.finditer(r"[^ ]{0,40}(цена за единицу|цена за 1|руб[^ ]{0,6}/\s*т|за тонну)[^|]{0,60}", t, re.I):
                print("   ЦЕНА:", " ".join(m.group(0).split())[:120])
