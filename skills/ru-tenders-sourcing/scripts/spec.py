#!/usr/bin/env python3
"""Вытащить спецификации лотов построчно: позиция, ед., количество, цена за единицу.

Текстовый дамп XML тут не годится: спецификация — это таблица, и без строк и
столбцов числа теряют привязку к позициям. Поэтому:
  xlsx/xls -> openpyxl (xls сначала через libreoffice)
  docx/doc/rtf/odt -> libreoffice в html, затем разбор <table>
  pdf -> pypdf построчно
  rar/zip -> распаковка и рекурсия
"""
import os, re, sys, json, io, csv, zipfile, subprocess, tempfile, shutil, html as H
from html.parser import HTMLParser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dig

RAW, OUT = "raw", "spec"
LO_PROFILE = "/tmp/loprofile"


# ---------------------------------------------------------------- конвертеры

def lo(path, to, outdir):
    """libreoffice --convert-to. Возвращает путь результата или None."""
    try:
        subprocess.run(
            ["soffice", f"-env:UserInstallation=file://{LO_PROFILE}",
             "--headless", "--norestore", "--convert-to", to,
             "--outdir", outdir, path],
            capture_output=True, timeout=300)
    except Exception:
        return None
    stem = os.path.splitext(os.path.basename(path))[0]
    p = os.path.join(outdir, stem + "." + to.split(":")[0])
    return p if os.path.exists(p) else None


class Tables(HTMLParser):
    """Таблицы из html: список таблиц, каждая — список строк, строка — список ячеек."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tables, self.stack, self.row, self.cell = [], [], None, None

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.stack.append([])
        elif tag == "tr" and self.stack:
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.cell = []

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.cell is not None:
            self.row.append(" ".join("".join(self.cell).split()))
            self.cell = None
        elif tag == "tr" and self.row is not None:
            if self.stack:
                self.stack[-1].append(self.row)
            self.row = None
        elif tag == "table" and self.stack:
            t = self.stack.pop()
            if t:
                self.tables.append(t)

    def handle_data(self, d):
        if self.cell is not None:
            self.cell.append(d)


def xlsx_rows(path):
    import openpyxl
    out = []
    try:
        wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    except Exception:
        return out
    for ws in wb.worksheets:
        rows = []
        for r in ws.iter_rows(values_only=True):
            cells = ["" if c is None else str(c).strip() for c in r]
            if any(cells):
                rows.append(cells)
        if rows:
            out.append((ws.title, rows))
    return out


TBL = re.compile(rb"<w:tbl[ >].*?</w:tbl>", re.S)
TR = re.compile(rb"<w:tr[ >].*?</w:tr>", re.S)
TC = re.compile(rb"<w:tc[ >].*?</w:tc>", re.S)
WT = re.compile(rb"<w:t(?:\s[^>]*)?>(.*?)</w:t>", re.S)


def docx_tables(path):
    """Таблицы прямо из word/document.xml. LibreOffice на больших docx падает,
    а разметка таблиц в OOXML простая: w:tbl > w:tr > w:tc > w:t."""
    try:
        z = zipfile.ZipFile(path)
        xml = z.read("word/document.xml")
    except Exception:
        return []
    out = []
    for i, tb in enumerate(TBL.finditer(xml)):
        rows = []
        for tr in TR.finditer(tb.group(0)):
            cells = []
            for tc in TC.finditer(tr.group(0)):
                txt = b"".join(m.group(1) for m in WT.finditer(tc.group(0)))
                cells.append(" ".join(H.unescape(txt.decode("utf-8", "replace")).split()))
            if any(cells):
                rows.append(cells)
        if len(rows) > 1:
            out.append((f"tbl{i+1}", rows))
    return out


def tables_of(path, ext, tmp):
    """-> [(имя листа/таблицы, [строки])]"""
    ext = ext.lower()
    if ext in ("xlsx", "xlsm"):
        return xlsx_rows(path)
    if ext == "xls":
        # xlrd читает старый бинарный xls напрямую; libreoffice в этой сборке
        # отказывается открывать любые OLE-файлы, на него полагаться нельзя
        try:
            import xlrd
            b = xlrd.open_workbook(path)
            out = []
            for sh in b.sheets():
                rows = []
                for i in range(sh.nrows):
                    cells = [("" if c.value is None else str(c.value)).strip()
                             for c in sh.row(i)]
                    cells = [re.sub(r"\.0$", "", c) if re.match(r"^\d+\.0$", c) else c
                             for c in cells]
                    if any(cells):
                        rows.append(cells)
                if rows:
                    out.append((sh.name, rows))
            if out:
                return out
        except Exception:
            pass
        p = lo(path, "xlsx", tmp)
        return xlsx_rows(p) if p else []
    if ext == "docx":
        t = docx_tables(path)
        if t:
            return t
    if ext in ("doc", "rtf", "odt"):
        p = lo(path, "docx", tmp)
        if p:
            t = docx_tables(p)
            if t:
                return t
    if ext in ("docx", "doc", "rtf", "odt", "html", "htm"):
        src = path
        if ext in ("docx", "doc", "rtf", "odt"):
            src = lo(path, "html", tmp) or path
        try:
            data = open(src, "rb").read()
        except Exception:
            return []
        for enc in ("utf-8", "cp1251"):
            try:
                txt = data.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        else:
            txt = data.decode("utf-8", "replace")
        p = Tables()
        p.feed(txt)
        return [(f"table{i+1}", t) for i, t in enumerate(p.tables)]
    if ext == "pdf":
        # pdfplumber видит сетку таблицы; у техзаданий спецификация почти всегда
        # разбита по страницам, поэтому таблицы с одинаковой шириной склеиваем
        try:
            import pdfplumber
        except Exception:
            pdfplumber = None
        if pdfplumber:
            try:
                out, buf = [], {}
                with pdfplumber.open(path) as pdf:
                    for pi, pg in enumerate(pdf.pages):
                        for t in pg.extract_tables() or []:
                            rows = [["" if c is None else " ".join(str(c).split())
                                     for c in r] for r in t]
                            rows = [r for r in rows if any(r)]
                            if len(rows) < 2:
                                continue
                            w = max(len(r) for r in rows)
                            buf.setdefault(w, []).extend(rows)
                for w, rows in buf.items():
                    out.append((f"pdf{w}col", rows))
                if out:
                    return out
            except Exception:
                pass
        try:
            import pypdf
            rd = pypdf.PdfReader(path)
        except Exception:
            return []
        rows = []
        for pg in rd.pages:
            for ln in (pg.extract_text() or "").splitlines():
                ln = " ".join(ln.split())
                if ln:
                    rows.append([ln])
        return [("pdf", rows)] if rows else []
    return []


# ------------------------------------------------------- распознавание спеки

# Порядок важен: колонки назначаются по очереди и повторно не используются,
# иначе «Наименование каждой единицы продукции» съедает колонку «Ед. изм.»,
# а цена за единицу теряется, потому что в шапке стоит «НМЦ», а не «цена».
COLS = [
    ("unit",  re.compile(r"^\W*ед(?:\.|иница|иницы)?\s*(?:изм|измер)|ед\.\s*изм", re.I)),
    ("qty",   re.compile(r"кол[-\s]*во|количеств|объ[её]м\s*(?:поставк|работ)?", re.I)),
    # «Средн. Стоимость» в обоснованиях НМЦК — это и есть принятая цена за единицу,
    # а соседние колонки КП1/КП2/КП3 это цены из коммерческих предложений, их брать нельзя
    ("price", re.compile(r"средн\w*\.?\s*(?:стоимост|цена)|НМЦ\s*(?:каждой\s+)?единиц"
                         r"|цена\s*(?:за\s*)?(?:1\s*)?ед|цена\s+единиц|стоимост\w*\s+единиц"
                         r"|цена\s*\*?\s*за\s*ед|ед\.\s*стоимост", re.I)),
    ("sum",   re.compile(r"^\W*(?:сумма|итого|общая\s+стоимост|стоимост\w*\s+позиц"
                         r"|всего\s+стоимост)", re.I)),
    ("name",  re.compile(r"наименован|предмет\s+закупк|описание\s+объекта|^\W*товар\b"
                         r"|продукц|позиц", re.I)),
    ("price2", re.compile(r"\bцена\b|\bНМЦ\b", re.I)),     # запасной вариант цены
    ("num",   re.compile(r"^\W*№|^\W*n\s*п/п|^\W*п/п", re.I)),
]
NUM = re.compile(r"^[\d  ]{1,15}(?:[.,]\d+)?$")
# колонки, которые выглядят как цена, но ею не являются
BADPRICE = re.compile(r"\bКП\s*\d|источник\s*№|предложени\w*\s*№|откл|коэффициент"
                      r"|с\s*учетом\s*%\s*снижен|вариац", re.I)


def tofloat(s):
    s = str(s).replace(" ", "").replace(" ", "").replace(" ", "")
    s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def header_map(rows, look=45):
    """Найти шапку и индексы колонок.

    Шапка часто занимает несколько строк: «Объем» сверху, а «Ед. изм.» и «Кол-во»
    строкой ниже, и по одной строке карту не собрать. Поэтому для каждой строки
    пробуем склейку её самой и до трёх следующих.
    """
    cand = []
    for i in range(min(look, len(rows))):
        for h in range(1, 5):
            block = rows[i:i + h]
            if not block:
                continue
            w = max(len(r) for r in block)
            comp = [" ".join(r[j] for r in block if j < len(r) and r[j]) for j in range(w)]
            cand.append((i + h - 1, comp))
    best = None
    for last, r in cand:
        i = last
        taken, m = set(), {}
        for key, pat in COLS:
            if key in m or (key == "price2" and "price" in m):
                continue
            for j, c in enumerate(r):
                if j in taken or not c:
                    continue
                if key in ("price", "price2") and BADPRICE.search(c):
                    continue
                if pat.search(c):
                    m["price" if key == "price2" else key] = j
                    taken.add(j)
                    break
        if "name" not in m or ("qty" not in m and "price" not in m):
            continue
        score = len(m) + (2 if "price" in m else 0) + (1 if "qty" in m else 0)
        if best is None or score > best[0]:
            best = (score, i, m)
    return best


def extract(rows):
    """-> список позиций [{name, unit, qty, price, sum}]"""
    hm = header_map(rows)
    if not hm:
        return []
    _, hi, m = hm
    items = []
    for r in rows[hi + 1:]:
        def g(k):
            j = m.get(k)
            return r[j] if j is not None and j < len(r) else ""
        name = g("name")
        if not name or len(name) < 3 or not re.search(r"[А-Яа-яA-Za-z]{3}", name):
            continue
        if re.match(r"^(итого|всего|в том числе|х{1,3})$", name.strip(), re.I):
            continue
        qty, price, tot = tofloat(g("qty")), tofloat(g("price")), tofloat(g("sum"))
        if qty is None and price is None and tot is None:
            continue
        items.append({"name": " ".join(name.split())[:140], "unit": g("unit")[:14],
                      "qty": qty, "price": price, "sum": tot})
    return items


# ------------------------------------------------------------------- прогон

def sniff(data, ext):
    """Расширение по содержимому. Rostender часто отдаёт docx под именем .doc,
    а libreoffice в таком случае просто отказывается открывать файл."""
    if data[:4] == b"Rar!":
        return "rar"
    if data[:2] == b"PK":
        try:
            names = zipfile.ZipFile(io.BytesIO(data)).namelist()
        except Exception:
            return "zip"
        if any(n.startswith("word/") for n in names):
            return "docx"
        if any(n.startswith("xl/") for n in names):
            return "xlsx"
        if any(n.startswith("ppt/") for n in names):
            return "pptx"
        if "mimetype" in names:
            return "odt"
        return "zip"
    if data[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1":
        # OLE: doc или xls. Отличаем по именам потоков.
        head = data[:200000]
        if b"W\x00o\x00r\x00k\x00b\x00o\x00o\x00k" in head or b"Book" in head[:4000]:
            return "xls"
        return "doc"
    if data[:5] == b"%PDF-":
        return "pdf"
    if data[:5] == b"{\\rtf":
        return "rtf"
    if data[:6].lower().startswith(b"<html") or b"<html" in data[:200].lower():
        return "html"
    return ext or "bin"


def download(no, lot):
    os.makedirs(RAW, exist_ok=True)
    # карточка иногда отдаётся без блока tendersData — просто повторяем
    fl = []
    for attempt in range(5):
        fl = dig.files_of(dig.get(lot["url"], binary=False))
        if fl:
            break
        print(f"   попытка {attempt+1}: вложений не видно, повтор", flush=True)
    got = []
    for title, fsid, link in fl:
        data = dig.get(link)
        if len(data) < 400:
            continue
        ext = (re.search(r"\.([a-z0-9]{2,5})$", fsid or title, re.I) or [None, ""])[1].lower()
        ext = sniff(data, ext)
        name = re.sub(r"[^A-Za-zА-Яа-я0-9.]", "_", f"{no}__{title}")[:80] + "." + ext
        p = os.path.join(RAW, name)
        open(p, "wb").write(data)
        got.append((p, ext, title))
    return got


def expand(files, tmp, depth=0):
    """Развернуть архивы в плоский список (путь, ext, подпись).

    Архивы бывают вложенными: в карточке лежит rar, внутри него ещё один rar
    с проектом договора и спецификацией. Поэтому рекурсия, но не глубже трёх.
    """
    out = []
    for p, ext, title in files:
        if ext in ("rar", "zip", "7z") and depth < 3:
            d = tempfile.mkdtemp(dir=tmp)
            subprocess.run(["unar", "-q", "-o", d, p], capture_output=True, timeout=300)
            inner = []
            for root, _, fs in os.walk(d):
                for f in fs:
                    fp = os.path.join(root, f)
                    e = (re.search(r"\.([a-z0-9]{2,5})$", f, re.I) or [None, ""])[1].lower()
                    try:
                        e = sniff(open(fp, "rb").read(200000), e)
                    except Exception:
                        pass
                    if not f.lower().endswith("." + e):
                        fp2 = fp + "." + e
                        try:
                            os.rename(fp, fp2)
                            fp = fp2
                        except Exception:
                            pass
                    inner.append((fp, e, f"{title} / {f}"))
            out += expand(inner, tmp, depth + 1)
        else:
            out.append((p, ext, title))
    return out


def run(nums):
    short = {x["no"]: x for x in json.load(open("short.json"))}
    os.makedirs(OUT, exist_ok=True)
    for no in nums:
        lot = short[no]
        print(f"\n{'='*80}\n№{no}  {lot['nmck']:,} ₽  {lot['title'][:80]}", flush=True)
        tmp = tempfile.mkdtemp()
        try:
            files = expand(download(no, lot), tmp)
            found = []
            for p, ext, title in files:
                for sheet, rows in tables_of(p, ext, tmp):
                    items = extract(rows)
                    if items:
                        found.append((title, sheet, items))
            if not found:
                print("   спецификация не распознана; файлов просмотрено:", len(files))
                for p, ext, title in files:
                    print("     -", ext, title[:70])
                continue
            # лучшая таблица — та, где есть и количество, и цена за единицу,
            # а уже потом та, где больше строк
            def rank(f):
                it = f[2]
                return (sum(1 for x in it if x["price"] is not None) > 0,
                        sum(1 for x in it if x["qty"] is not None) > 0,
                        len(it))
            found.sort(key=rank, reverse=True)
            title, sheet, items = found[0]
            print(f"   источник: {title[:70]} [{sheet}] · позиций {len(items)}")
            with open(f"{OUT}/{no}.csv", "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["#", "наименование", "ед", "кол-во", "цена за ед", "сумма"])
                for i, it in enumerate(items, 1):
                    w.writerow([i, it["name"], it["unit"], it["qty"], it["price"], it["sum"]])
            json.dump({"no": no, "nmck": lot["nmck"], "src": title, "items": items},
                      open(f"{OUT}/{no}.json", "w"), ensure_ascii=False, indent=1)
            qs = [it["qty"] for it in items if it["qty"]]
            ps = [it["price"] for it in items if it["price"]]
            ss = [it["sum"] for it in items if it["sum"]]
            qp = sum(it["qty"] * it["price"] for it in items
                     if it["qty"] and it["price"])
            print(f"   кол-во задано у {len(qs)}, цена за ед. у {len(ps)}, сумма у {len(ss)}")
            if qp:
                print(f"   Σ кол-во × цена = {qp:,.2f} ₽   против НМЦК {lot['nmck']:,} ₽"
                      f"   ({qp / lot['nmck'] * 100:.1f} %)")
            if ss:
                print(f"   Σ сумм по строкам = {sum(ss):,.2f} ₽")
            for it in items[:10]:
                print(f"     {it['name'][:52]:52} {it['unit'][:7]:7} "
                      f"{it['qty'] if it['qty'] is not None else '':>9} "
                      f"{it['price'] if it['price'] is not None else '':>12}")
            if len(found) > 1:
                print("   прочие таблицы:", [(t[:30], len(i)) for t, _, i in found[1:4]])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    run([int(x) for x in sys.argv[1:]])
