#!/usr/bin/env python3
"""Вскрыть выбранные лоты: вложения, срок исполнения, аванс, объём, цена за единицу.

Карточка лота на rostender прячет организатора, но ссылки на документацию лежат
открытыми в var tendersData -> files_by_date. Их и качаем.
"""
import json, re, os, sys, io, zipfile, subprocess, html as H

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")
DOCS = "docs"


def get(url, binary=True):
    r = subprocess.run(["curl", "-sL", "--max-time", "90", "-A", UA, url],
                       capture_output=True)
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


def plain(h):
    t = re.sub(r"<script.*?</script>", " ", h, flags=re.S)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return " ".join(H.unescape(t).split())


def files_of(h):
    m = re.search(r"var tendersData = (\{.*)", h)
    if not m:
        return []
    blob = m.group(1)
    depth, end = 0, None
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
        return []
    out = []
    for t in d.values():
        for day, lst in (t.get("files_by_date") or {}).items():
            for f in lst:
                if f.get("link"):
                    out.append((f.get("title", ""), f.get("fsid", ""), f["link"]))
    return out


def office_text(data):
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
            out.append(re.sub(r"<[^>]+>", " ", x))
    return " ".join(" ".join(out).split())


def archive_text(data, ext):
    """Архив: распаковать во временную папку и собрать текст из всего внутри."""
    import tempfile, shutil
    d = tempfile.mkdtemp()
    try:
        p = os.path.join(d, "a." + ext)
        open(p, "wb").write(data)
        subprocess.run(["unar", "-q", "-o", d, p], capture_output=True, timeout=180)
        out = []
        for root, _, fs in os.walk(d):
            for f in fs:
                if f == "a." + ext:
                    continue
                fp = os.path.join(root, f)
                try:
                    inner = open(fp, "rb").read()
                except Exception:
                    continue
                t = any_text(inner, f)
                if t:
                    out.append(f"[{f}] " + t)
        return " ".join(out)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def ru_words(t):
    return len(re.findall(r"[А-Яа-яЁё]{4,}", t))


def doc_text(data):
    """Старый бинарный .doc. Берём тот конвертер, который дал больше русских слов:
    antiword часто «успешно» выдаёт мусор, и по длине его не отличить."""
    import tempfile
    best = ""
    with tempfile.NamedTemporaryFile(suffix=".doc", delete=True) as f:
        f.write(data)
        f.flush()
        for cmd in (["catdoc", "-d", "utf-8", f.name],
                    ["antiword", "-m", "cp1251.txt", f.name]):
            try:
                r = subprocess.run(cmd, capture_output=True, timeout=180)
            except Exception:
                continue
            t = " ".join(r.stdout.decode("utf-8", "replace").split())
            if ru_words(t) > ru_words(best):
                best = t
    return best if ru_words(best) > 50 else ""


def any_text(data, name):
    """Текст из чего угодно: архив, docx/xlsx, doc, rtf, pdf, html, plain."""
    if data[:4] == b"Rar!":
        return archive_text(data, "rar")
    if data[:2] == b"PK":
        # OOXML или обычный zip с документами внутри
        t = office_text(data)
        return t if len(t) > 200 else archive_text(data, "zip")
    if data[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1":
        t = doc_text(data)
        if t:
            return t
    if data[:5] == b"%PDF-":
        try:
            import pypdf
            r = pypdf.PdfReader(io.BytesIO(data))
            return " ".join(" ".join((p.extract_text() or "").split())
                            for p in r.pages[:60])
        except Exception:
            return ""
    head = data[:4000].decode("utf-8", "replace").lower()
    if "<html" in head or "<?xml" in head or "<w:" in head:
        return plain(data.decode("utf-8", "replace"))
    if data[:5] == b"{\\rtf":
        t = data.decode("cp1251", "replace")
        t = re.sub(r"\\'([0-9a-f]{2})", lambda m: bytes([int(m.group(1), 16)]).decode("cp1251", "replace"), t)
        t = re.sub(r"\\[a-z]+-?\d* ?", " ", t)
        return " ".join(re.sub(r"[{}]", " ", t).split())
    # старый бинарный .doc — выдираем читаемые куски в cp1251 и utf-16
    for enc in ("cp1251", "utf-16-le"):
        try:
            t = data.decode(enc, "replace")
        except Exception:
            continue
        words = re.findall(r"[А-Яа-яЁё0-9][А-Яа-яЁё0-9 .,:;%()«»/\-]{6,}", t)
        if len(words) > 20:
            return " ".join(" ".join(words).split())
    return ""


# срок исполнения: только то, где рядом с «поставк/исполнен» стоит число дней или дата
TERM = re.compile(
    r"[^.;|]{0,90}"
    r"(?:срок\w*\s+(?:поставк\w+|исполнен\w+|оказан\w+|выполнен\w+|действия\s+(?:договора|контракта))"
    r"|период\w*\s+поставк\w+|поставк\w+\s+(?:товара\s+)?осуществляется)"
    r"[^.;|]{0,140}", re.I)
NUMDAY = re.compile(r"\b\d{1,3}\s*\(?[а-я ]{0,20}\)?\s*(?:календарн\w+|рабоч\w+)?\s*дн", re.I)
DATES = re.compile(r"\b(?:до|по|с)\s+\d{1,2}[.\s][\d]{1,2}[.\s]20\d{2}", re.I)
ADV = re.compile(r"[^.;|]{0,70}(?:аванс\w*|предоплат\w*)\s*[^.;|]{0,30}?\d{1,3}\s*%[^.;|]{0,60}", re.I)
QTY = re.compile(r"(итого|всего|общее\s+количество|количество\s+товара)[^А-Яа-я0-9]{0,20}"
                 r"([\d  ]{2,12}(?:[.,]\d+)?)\s*(шт|компл|пар|кг|т\b|тонн\w*|м2|м3|м\b)", re.I)
UNIT = re.compile(r"(цена\s+за\s+ед\w*|цена\s+единицы|за\s+1\s*(?:шт|кг|т\b))[^|]{0,80}", re.I)


def is_real_term(s):
    """Отсечь юридическую воду: оставить только фразы с числом дней или датой."""
    if re.search(r"заключения\s+договор|подписать|протокол|коллективн|рабочим\s+днем", s, re.I):
        return False
    return bool(NUMDAY.search(s) or DATES.search(s))


def squeeze(s, n=200):
    return " ".join(s.split())[:n]


def main(nums):
    short = {x["no"]: x for x in json.load(open("short.json"))}
    os.makedirs(DOCS, exist_ok=True)
    res = []
    for n in nums:
        lot = short[n]
        print(f"\n{'='*78}\n№{n}  {lot['nmck']:,} ₽  {lot['law']}  {lot['region']}"
              f"\n{lot['title'][:110]}", flush=True)
        page = get(lot["url"], binary=False)
        pt = plain(page)
        adv = re.search(r"Аванс:\s*([\d.,]+)\s*%", pt)
        rec = {"no": n, "nmck": lot["nmck"], "law": lot["law"],
               "title": lot["title"], "url": lot["url"],
               "advance": adv.group(1) if adv else None,
               "files": [], "terms": [], "qty": [], "unit": [], "advance_doc": []}
        print("  аванс по карточке:", rec["advance"] or "не указан")
        fl = files_of(page)
        print(f"  вложений: {len(fl)}")
        for title, fsid, link in fl:
            data = get(link)
            ext = (re.search(r"\.([a-z0-9]{2,5})$", fsid or title, re.I) or [None, "?"])[1]
            size = len(data)
            rec["files"].append({"title": title, "ext": ext, "size": size})
            print(f"   - {title[:60]:60} {ext:5} {size:>9,} б")
            if size < 400:
                continue
            t = any_text(data, title)
            if not t:
                continue
            fn = re.sub(r"[^A-Za-zА-Яа-я0-9.]", "_", f"{n}_{title}")[:90]
            open(f"{DOCS}/{fn}.txt", "w").write(t)
            for m in TERM.finditer(t):
                s = squeeze(m.group(0))
                if is_real_term(s) and s not in rec["terms"]:
                    rec["terms"].append(s)
            for m in ADV.finditer(t):
                s = squeeze(m.group(0), 160)
                if s not in rec["advance_doc"]:
                    rec["advance_doc"].append(s)
            for m in QTY.finditer(t):
                rec["qty"].append(squeeze(m.group(0), 90))
            for m in UNIT.finditer(t):
                rec["unit"].append(squeeze(m.group(0), 90))
        for k, lbl in (("terms", "СРОК"), ("advance_doc", "АВАНС"),
                       ("qty", "КОЛИЧЕСТВО"), ("unit", "ЦЕНА/ЕД")):
            for s in rec[k][:5]:
                print(f"     {lbl}: {s}")
        res.append(rec)
        json.dump(rec, open(f"{DOCS}/dig_{n}.json", "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main([int(x) for x in sys.argv[1:]])
