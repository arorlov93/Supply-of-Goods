#!/usr/bin/env python3
"""Вытащить прайсовые позиции «название — цена» с сайтов поставщиков."""
import re, subprocess, sys

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")


def text_nodes(url):
    h = subprocess.run(["curl", "-sL", "--max-time", "45", "-A", UA, url],
                       capture_output=True).stdout.decode("utf-8", "replace")
    h = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S)
    h = re.sub(r"<[^>]+>", "\x00", h)
    for a, b in (("&nbsp;", " "), ("&#8381;", "₽"), ("&quot;", '"'), ("&amp;", "&"),
                 ("&laquo;", "«"), ("&raquo;", "»"), ("&#160;", " ")):
        h = h.replace(a, b)
    return [" ".join(x.split()) for x in h.split("\x00") if x.strip()]


PRICE = re.compile(r"(\d[\d  ]{2,})\s*(?:₽|руб|р\.|/\s*т\b)", re.I)


def prices(url, want=None, limit=25):
    nodes = text_nodes(url)
    seen, out = set(), []
    for i, n in enumerate(nodes):
        m = PRICE.search(n)
        if not m:
            continue
        val = int(re.sub(r"\D", "", m.group(1)))
        if not (50 <= val <= 300000):
            continue
        ctx = " · ".join(nodes[max(0, i - 4):i + 1])[-190:]
        if want and not re.search(want, ctx, re.I):
            continue
        key = (val, ctx[-60:])
        if key in seen:
            continue
        seen.add(key)
        out.append((val, ctx))
        if len(out) >= limit:
            break
    return out


if __name__ == "__main__":
    for url in sys.argv[1:]:
        print(f"\n=== {url}")
        for v, c in prices(url):
            print(f"  {v:>8,} | {c}")
