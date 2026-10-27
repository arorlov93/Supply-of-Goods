# -*- coding: utf-8 -*-
"""Адаптивные наборы снимков: каждому экрану свой файл.

Задача. Замер показал перекос в обе стороны. Снимки маршрута лежат
шириной 1700 точек, а показываются на 342: в них впятеро больше точек,
чем нужно даже экрану с удвоенной плотностью. Главная страница весила
2.92 МБ, из них 2.66 МБ снимки. При этом шапка-заставка, наоборот,
растянута: файл 543 точки на 1440 показа.

Что делает. Для каждого снимка берёт замеренную ширину показа на трёх
окнах (tools/img-measure.js), готовит несколько файлов под эти ширины с
запасом на удвоенную плотность и собирает srcset с точным sizes. Браузер
дальше сам берёт то, что ему нужно: телефон маленький файл, большой
экран крупный.

Чего не делает. Не выдумывает резкость. Если исходник меньше, чем нужно,
крупный размер просто не создаётся: растянуть снимок программой значит
сделать его мыльным, а не чётким. Такие случаи печатаются списком, их
лечат только настоящим исходником.

Имена файлов версионные, по содержимому, как и остальные: так их можно
кэшировать навсегда, а при изменении имя меняется само.

Запуск:
    node tools/img-measure.js      # сначала замер
    python3.13 tools/img-srcset.py # потом нарезка и разметка
Повторный запуск ничего не дублирует.
"""
import hashlib, json, pathlib, re, sys
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
MEDIA = SITE / "media"
SIZES = ROOT / "img-sizes.json"

# Плотность экрана: на двойную берём запас, на тройную нет. Тройная
# встречается на телефонах, а там и окно узкое, и мобильный трафик дорог.
DPR = 2
# Ступени не плодим: каждая лишняя это ещё один файл в выкладке, а
# выигрыш между близкими ширинами копеечный.
MIN_STEP = 1.35
QUALITY = 80


def variants(nat_w, shown):
    """Нужные ширины файлов для снимка с такими показами.

    Ступени берутся и под обычную плотность экрана, и под удвоенную.
    Только под удвоенную нельзя: телефон с обычным экраном тогда качает
    вдвое больший файл, чем ему нужен, и весь смысл теряется. Проверено
    замером: после первой нарезки вес на окне 390 точек почти не упал."""
    want = sorted({min(nat_w, round(w * k)) for w in shown.values() if w for k in (1, DPR)})
    want = [w for w in want if w >= 200]
    out = []
    for w in want:
        if not out or w / out[-1] >= MIN_STEP:
            out.append(w)
        else:
            out[-1] = max(out[-1], w)
    # исходник целиком добавляем, только если он заметно крупнее верхней
    # ступени: иначе это тот же файл под другим именем
    if out and nat_w / out[-1] >= MIN_STEP:
        out.append(nat_w)
    return out or [nat_w]


def sizes_attr(shown):
    """Точный sizes из замеров, без догадок."""
    w390 = shown.get("390") or shown.get(390)
    w768 = shown.get("768") or shown.get(768)
    w1440 = shown.get("1440") or shown.get(1440)
    parts = []
    if w390:
        parts.append(f"(max-width: 480px) {w390}px")
    if w768:
        parts.append(f"(max-width: 900px) {w768}px")
    parts.append(f"{w1440 or w768 or w390}px")
    return ", ".join(parts)


def main():
    if not SIZES.exists():
        print("нет img-sizes.json, сначала: node tools/img-measure.js")
        return 1
    measured = json.loads(SIZES.read_text())

    html = {p: p.read_text() for p in SITE.rglob("*.html") if p.name != "crm.html"}
    made = skipped = 0
    too_small = []

    for name, shown in sorted(measured.items()):
        src = MEDIA / name
        if not src.is_file() or src.suffix != ".webp":
            continue
        joined = "".join(html.values())
        if f"media/{name} " in joined or f"-{name.split('.')[0]}-" in joined:
            skipped += 1
            continue

        im = Image.open(src)
        nat_w, nat_h = im.size
        need = max(round(w * DPR) for w in shown.values() if w)
        if nat_w < need * 0.9:
            too_small.append(f"{name}: есть {nat_w}, нужно {need}")

        widths = variants(nat_w, shown)
        if len(widths) < 2:
            skipped += 1
            continue

        entries = []
        for w in widths:
            if w >= nat_w:
                entries.append((f"media/{name}", nat_w))
                continue
            out = im.resize((w, round(nat_h * w / nat_w)), Image.LANCZOS)
            stem = name.split(".")[0]
            tmp = MEDIA / f"{stem}-{w}.tmp.webp"
            out.save(tmp, "WEBP", quality=QUALITY, method=6)
            h = hashlib.sha256(tmp.read_bytes()).hexdigest()[:8]
            final = MEDIA / f"{stem}-{w}.{h}.webp"
            if final.exists():
                tmp.unlink()
            else:
                tmp.rename(final)
            entries.append((f"media/{final.name}", w))
            made += 1

        entries = sorted(set(entries), key=lambda e: e[1])
        srcset = ", ".join(f"{u} {w}w" for u, w in entries)
        sz = sizes_attr(shown)

        for p, s in html.items():
            if f"media/{name}" not in s:
                continue
            # внутри <picture> набор вешается на <source>
            s = s.replace(
                f'<source srcset="media/{name}" type="image/webp">',
                f'<source srcset="{srcset}" sizes="{sz}" type="image/webp">')
            # на страницах без <picture> снимок стоит простым <img>
            s = re.sub(
                r'(<img\b[^>]*?\bsrc="media/' + re.escape(name) + r'")(?![^>]*\bsrcset=)',
                lambda m: m.group(1) + f' srcset="{srcset}" sizes="{sz}"',
                s)
            html[p] = s

    for p, s in html.items():
        if s != p.read_text():
            p.write_text(s)

    print(f"новых файлов: {made}, пропущено снимков: {skipped}")
    if too_small:
        print("исходник мельче, чем нужно (лечится только новым исходником):")
        for t in too_small:
            print("   ", t)
    return 0


if __name__ == "__main__":
    sys.exit(main())
