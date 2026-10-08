# -*- coding: utf-8 -*-
import os, glob, importlib
import build as B, gen_pages as G, content_core as C
import heroes as H

mods = []
try:
    import content_cats as CAT; mods.append("cats")
except Exception as e: CAT = None; print("категории пропущены:", e)
try:
    import content_guides as GU; mods.append("guides")
except Exception: GU = None
try:
    import content_fr as FR; mods.append("fr")
except Exception: FR = None

# ── этап 1 и хабы
UPD = ('<p class="upd"><time datetime="2026-10-08">Updated 8 October 2026</time>'
       ' &middot; ISP Group</p>')
for spec in [C.CONTACT, C.ABOUT, C.SERVICES, C.INCOTERMS, C.NOTFOUND,
             C.SUPPLY, C.CORRIDORS_HUB, C.GUIDES, C.PRIVACY, C.TERMS]:
    sp = dict(spec)
    if sp["slug"] in ("incoterms", "privacy", "terms"):
        sp["updated"] = UPD
    if sp["slug"] == "incoterms" and GU:
        sp["ld"] = GU.article_ld(sp)
    sp["hero_img"] = H.HERO.get(sp["slug"])
    B.write(sp, extra_js=C.CONTACT_JS if sp["slug"] == "contact" else "")

# ── этап 2: товарные группы
if CAT:
    for spec in CAT.CATS:
        s = dict(spec)
        s["hero_right"] = G.factcard("Category at a glance", spec["facts"])
        s["hero_img"] = H.HERO.get(spec["slug"])
        s["related"] = CAT.rel(spec["slug"])
        s["faq_h2"] = "What buyers ask about this category"
        s["faq_sub"] = "The three that come up before a first order."
        s["ld"] = CAT.ld(G.plain(spec["h1"]), spec["desc"], spec["slug"],
                         [r[1] for r in spec["facts"][:1]])
        B.write(s)

# ── этап 3: руководства
if GU:
    for spec in GU.GUIDES_PAGES:
        s = dict(spec)
        s["hero_img"] = H.HERO.get(spec["slug"])
        s.setdefault("faq_h2", "Questions on this")
        s.setdefault("faq_sub", "The ones we are asked most often.")
        s["related"] = GU.rel(spec["slug"])
        s["ld"] = GU.article_ld(spec)
        s["updated"] = ('<p class="upd"><time datetime="%s">Updated 8 October 2026</time>'
                        ' &middot; ISP Group</p>' % GU.UPDATED)
        B.write(s)

# ── этап 4: французская версия
if FR:
    for spec in FR.PAGES_FR:
        spec = dict(spec); spec["hero_img"] = H.HERO.get(spec["slug"])
        B.write(spec, lang="fr", extra_js=C.CONTACT_JS if "contact" in spec["slug"] else "")

print("собрано страниц:", len(B.built))

if FR:
    B.hreflang(FR.HREFLANG, G.HOST)

B.retrofit_nav(["site/index.html", "site/experience.html", "site/china.html",
                "site/turkiye.html", "site/west-africa.html", "site/southern-africa.html"])

import nums
NUMCSS = """
.nums{display:grid;grid-template-columns:repeat(auto-fit,minmax(142px,1fr));
  gap:clamp(16px,2.6vw,34px);margin-top:40px}
.num{border-top:1px solid var(--rule);padding-top:17px}
.num b{display:block;font-family:var(--fs);font-weight:400;letter-spacing:-.02em;
  font-size:clamp(2.5rem,5vw,4rem);line-height:.9;color:var(--brand)}
.num span{display:block;margin-top:11px;font-family:var(--fm);font-size:.57rem;
  letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3);line-height:1.85}
.num a{color:inherit;text-decoration:none;border-bottom:1px solid transparent;
  transition:border-color .2s,color .2s}
.num a:hover{color:var(--brand);border-color:var(--gold)}
"""
nums.inject("site/index.html", nums.EN, NUMCSS)
nums.inject("site/fr.html", nums.FR)
print("числовая полоса добавлена на главные")

B.pretty_urls(G.HOST)

allslugs = sorted({os.path.basename(p)[:-5] for p in glob.glob("site/*.html")})
print("в sitemap адресов:", B.sitemap(allslugs))

import search_mod
n, size = search_mod.build_index()
print(f"индекс поиска: {n} страниц, {size//1024} КБ")
