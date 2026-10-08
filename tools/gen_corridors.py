# -*- coding: utf-8 -*-
"""Страницы коридоров + общий модуль 3D-эффектов при скролле.

Голову, стили, шапку и подвал берём из index.html, чтобы страницы не разошлись
с главной по оформлению и чтобы правка стиля не требовала правки в пяти местах.
"""
import re, json, html, os
from corr_content import PAGES, FAQ, SHORTDESC

SITE = "site"
HOST = "https://ispgroupgc.com/"
IDX = os.path.join(SITE, "index.html")
src = open(IDX, encoding="utf-8").read()

ASSETS = src[src.index('<link rel="preconnect"'):src.index("</head>")]
NAV    = src[src.index("<nav>"):src.index("</nav>") + 6]
FOOT   = src[src.index("<footer>"):src.index("</footer>") + 9]

# ── 1. дополнительные стили: страницы коридоров и 3D-эффекты ────────────────
FX = '''
/* страницы коридоров */
.crumbs{font-family:var(--fm);font-size:.57rem;letter-spacing:.13em;text-transform:uppercase;
  color:var(--ink-3);margin-bottom:18px;
  /* сбрасываем глобальные правила для nav: это крошки, а не шапка */
  position:static;z-index:auto;background:none;backdrop-filter:none;border:0;top:auto}
.crumbs a{color:var(--brand);text-decoration:none;border-bottom:1px solid transparent;
  transition:border-color .2s}
.crumbs a:hover{border-color:var(--gold)}
.crumbs span{padding:0 7px;color:var(--rule)}
.crumbs b{font-weight:400;color:var(--ink-2)}
.chero-g{display:grid;grid-template-columns:minmax(0,1.12fr) minmax(0,.88fr);
  gap:clamp(28px,5vw,64px);align-items:start;padding-block:clamp(48px,7vw,92px)}
@media(max-width:900px){.chero-g{grid-template-columns:1fr}}
.chero h1{font-size:clamp(2.3rem,5.2vw,4rem);max-width:16ch;letter-spacing:-.02em}
.chero h1 em{font-style:italic;color:var(--brand)}
.chero .sub{margin-top:22px;max-width:48ch;font-size:clamp(1rem,1.7vw,1.14rem);color:var(--ink-2)}
.factcard{background:var(--surface);border:1px solid var(--rule);padding:26px 24px;
  box-shadow:var(--shadow-m)}
.facts{width:100%;border-collapse:collapse;font-size:.92rem;margin-top:4px}
.facts th{text-align:left;font-family:var(--fm);font-weight:500;font-size:.56rem;
  letter-spacing:.13em;text-transform:uppercase;color:var(--ink-3);
  padding:14px 14px 14px 0;vertical-align:top;width:9.5rem}
.facts td{padding:14px 0;color:var(--ink-2);vertical-align:top}
.facts tr+tr th,.facts tr+tr td{border-top:1px solid var(--rule)}
@media(max-width:560px){
  .facts th,.facts td{display:block;width:auto;padding:0}
  .facts th{padding-top:15px}
  .facts td{padding:5px 0 15px}
  .facts tr+tr td{border-top:0}
}
.prose{margin-top:6px}
.pblock{display:grid;grid-template-columns:4.4rem minmax(0,.92fr) minmax(0,1.28fr);
  gap:0 30px;padding:34px 0;border-top:1px solid var(--rule);align-items:start}
.pblock:last-child{border-bottom:1px solid var(--rule)}
.pblock .k{font-family:var(--fm);font-size:.6rem;color:var(--gold);letter-spacing:.12em;padding-top:10px}
.pblock h2{font-size:clamp(1.5rem,2.3vw,1.92rem);max-width:20ch}
.pblock .ptext p{color:var(--ink-2);font-size:1rem}
.pblock .ptext p+p{margin-top:15px}
@media(max-width:900px){.pblock{grid-template-columns:4.4rem minmax(0,1fr);gap:0 24px}
  .pblock .ptext{grid-column:2;margin-top:16px}}
@media(max-width:620px){.pblock{grid-template-columns:1fr}
  .pblock .ptext{grid-column:1}}
.lanelinks{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin-top:34px}
.lanelink{display:block;text-decoration:none;background:var(--surface);border:1px solid var(--rule);
  padding:20px 20px 18px;box-shadow:var(--shadow-s);
  transition:transform .22s ease,box-shadow .22s ease,border-color .22s ease}
.lanelink:hover{transform:translateY(-4px);box-shadow:var(--shadow-l);border-color:var(--brand)}
.lanelink b{display:block;font-family:var(--fs);font-weight:400;font-size:1.22rem;margin-bottom:6px}
.lanelink span{font-size:.9rem;color:var(--ink-2)}
.lanes td a{color:var(--ink);text-decoration:none;border-bottom:1.5px solid var(--gold-soft);
  transition:border-color .2s}
.lanes td a:hover{border-color:var(--gold)}

/* параллакс: картинка живёт в обёртке выше кадра, чтобы было куда ехать */
.pz{position:absolute;inset:-8% 0;display:block;will-change:transform}
.pz img{width:100%;height:100%;object-fit:cover}
@media (prefers-reduced-motion:reduce){.pz{inset:0}}
'''

FXJS = '''<script>
(function(){
  /* Глубина при скролле. Всё делается инлайновыми стилями: без JS страница
     остаётся полностью видимой, и поисковик видит обычный документ. */
  if (!('IntersectionObserver' in window)) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var EASE='cubic-bezier(.16,.74,.22,1)';
  var SEL='.cap,.cat,.step,figure,.lede>*,.band .wrap>*,details,.scroller,.factcard,'+
          '.pblock,.lanelink,.teaser>*,.ask,.steps,.fgrid>div';
  var items=[].slice.call(document.querySelectorAll(SEL)).filter(function(e){
    return !e.closest('.pz');
  });
  items.forEach(function(el){
    var p=el.parentNode;
    if(p.__g===undefined) p.__g=0;
    el.__d=Math.min(p.__g++,5)*70;
    el.style.willChange='transform,opacity';
    el.style.opacity='0';
    el.style.transform='perspective(1300px) rotateX(7deg) translate3d(0,36px,-70px)';
  });
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(!e.isIntersecting) return;
      var el=e.target; io.unobserve(el);
      el.style.transition='opacity .75s '+EASE+' '+el.__d+'ms, transform .95s '+EASE+' '+el.__d+'ms';
      el.style.opacity=''; el.style.transform='';
      setTimeout(function(){ el.style.transition=''; el.style.willChange=''; }, el.__d+1200);
    });
  },{rootMargin:'0px 0px -9% 0px', threshold:0.05});
  items.forEach(function(el){ io.observe(el); });

  /* параллакс фотографий */
  var live=[];
  var pio=new IntersectionObserver(function(es){
    es.forEach(function(e){
      var i=live.indexOf(e.target);
      if(e.isIntersecting){ if(i<0) live.push(e.target); }
      else if(i>=0) live.splice(i,1);
    });
  },{rootMargin:'30% 0px 30% 0px'});
  [].forEach.call(document.querySelectorAll('.pz'), function(e){ pio.observe(e); });
  var queued=false;
  function par(){
    queued=false;
    var h=window.innerHeight||1;
    for(var i=0;i<live.length;i++){
      var e=live[i], r=e.getBoundingClientRect();
      var p=((r.top+r.height/2)-h/2)/h;
      if(p>1.3)p=1.3; if(p<-1.3)p=-1.3;
      e.style.transform='translate3d(0,'+(p*-5.6).toFixed(2)+'%,0)';
    }
  }
  function kick(){ if(!queued){ queued=true; requestAnimationFrame(par); } }
  window.addEventListener('scroll',kick,{passive:true});
  window.addEventListener('resize',kick,{passive:true});
  par();
})();
</script>
'''

NAVJS = '''<script>
(function(){
  var nt=document.getElementById('navtoggle'), nm=document.getElementById('navmenu');
  if(!nt||!nm) return;
  nt.addEventListener('click',function(){
    var open=nm.classList.toggle('open');
    nt.setAttribute('aria-expanded', open?'true':'false');
  });
  nm.addEventListener('click',function(e){
    if(e.target.tagName==='A'){ nm.classList.remove('open'); nt.setAttribute('aria-expanded','false'); }
  });
})();
</script>
'''

ICON = ("<link rel=\"icon\" href=\"data:image/svg+xml,"
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'>"
        "<rect width='64' height='64' rx='12' fill='%230b4a40'/>"
        "<text x='32' y='43' font-family='Georgia,serif' font-size='30' font-weight='400'"
        " fill='%23e8d9b4' text-anchor='middle'>IG</text></svg>\">")

LANES = [(p["slug"], p["h1"], p["sub"]) for p in PAGES]
SHORT = {"china":"China &rarr; worldwide", "turkiye":"T&uuml;rkiye &rarr; United States",
         "west-africa":"Americas &amp; EU &rarr; West Africa", "southern-africa":"Intra-Africa"}


def plain(s):
    return html.unescape(re.sub("<[^>]+>", "", s)).replace("&rarr;", "to")


def nav_for(page):
    """Шапка та же, но ссылки-якоря ведут на главную."""
    n = NAV
    for a in ("#capabilities", "#categories", "#corridors", "#faq", "#enquiry", "#top"):
        n = n.replace('href="%s"' % a, 'href="index.html%s"' % a)
    return n


def footer_for(page):
    f = FOOT
    links = "".join('<a href="%s.html" style="display:block">%s</a>' % (s, SHORT[s])
                    for s, _, _ in LANES)
    col = ('<div><dt>Corridors</dt><dd style="line-height:1.95">%s</dd></div>' % links)
    if "<dt>Corridors</dt>" not in f:                 # index.html уже мог получить колонку
        f = f.replace('<div><dt>Reading</dt>', col + '\n      <div><dt>Reading</dt>')
    if page != "index":
        f = f.replace('href="experience.html"', 'href="experience.html"')
    return f


def build(p):
    url = HOST + p["slug"] + ".html"
    img, w, h, alt, cap = p["photo"]
    import heroes as H
    hero, heroalt = H.HERO.get(p["slug"], (img, alt))
    facts = "".join("<tr><th scope=\"row\">%s</th><td>%s</td></tr>" % (k, v) for k, v in p["facts"])
    chips = "".join('<span class="chip">%s%s</span>' %
                    (("<b>%s</b> " % a) if b else a, b or "") for a, b in p["chips"])

    prose, n, open_block = "", 0, False
    for kind, text in p["body"]:
        if kind == "h2":
            if open_block:
                prose += "</div></div>\n"
            n += 1
            prose += ('<div class="pblock"><span class="k">%02d</span><h2>%s</h2>'
                      '<div class="ptext">' % (n, text))
            open_block = True
        else:
            prose += "<p>%s</p>" % text
    if open_block:
        prose += "</div></div>"

    others = "".join(
        '<a class="lanelink" href="%s.html"><b>%s</b><span>%s</span></a>' %
        (s, SHORT[s], plain(sub).split(".")[0] + ".")
        for s, _, sub in LANES if s != p["slug"])

    faqhtml = "".join(
        "<details><summary>%s</summary><p>%s</p></details>" % (q, a) for q, a in FAQ[p["slug"]])

    ld = [
      {"@context":"https://schema.org","@type":"Service",
       "name": plain(p["h1"]), "serviceType":"International sourcing, trading and supply",
       "description": p["desc"],
       "provider":{"@type":"Organization","name":"ISP GROUP LLC","url":HOST,
                   "address":{"@type":"PostalAddress","streetAddress":"16395 Biscayne Blvd",
                              "addressLocality":"North Miami Beach","addressRegion":"FL",
                              "postalCode":"33160","addressCountry":"US"}},
       "areaServed":[{"@type":"Place","name":x} for x in p["kw"][:1]],
       "url": url},
      {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,
         "acceptedAnswer":{"@type":"Answer","text":a}} for q, a in FAQ[p["slug"]]]},
      {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"ISP Group Global Commerce","item":HOST},
        {"@type":"ListItem","position":2,"name":"Corridors","item":HOST+"#corridors"},
        {"@type":"ListItem","position":3,"name":SHORT[p["slug"]].replace("&rarr;","to")
            .replace("&amp;","and").replace("&uuml;","ü"),"item":url}]},
    ]
    ldjs = "".join('<script type="application/ld+json">%s</script>\n'
                   % json.dumps(d, ensure_ascii=False) for d in ld)

    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{sdesc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="ISP Group Global Commerce">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{otitle}">
<meta property="og:description" content="{sdesc}">
<meta property="og:image" content="{host}media/{ogimg}">
<meta property="og:image:alt" content="{alt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#eef1ef">
{icon}
<title>{title} | ISP Group</title>
{assets}
<style>{fx}</style>
</head>
<body>
{nav}

<header class="hero chero" id="top">
  <div class="wrap chero-g">
    <div>
      <nav class="crumbs" aria-label="Breadcrumb">
        <a href="index.html">ISP Group</a> <span>/</span>
        <a href="index.html#corridors">Corridors</a> <span>/</span>
        <b>{crumb}</b>
      </nav>
      <h1>{h1}</h1>
      <p class="sub">{sub}</p>
      <div class="chips">{chips}</div>
      <div class="ctarow" style="margin-top:28px">
        <a class="btn" href="index.html#enquiry">Request a quote</a>
        <a class="btn btn-ghost" href="index.html#corridors">All corridors</a>
      </div>
    </div>
    <div class="heroside">
      <div class="shot"><span class="pz"><img src="media/{hero}" width="1040" height="1300"
        alt="{heroalt}" fetchpriority="high" decoding="async"></span></div>
      <aside class="factcard">
        <span class="eyebrow">Lane at a glance</span>
        <table class="facts"><tbody>{facts}</tbody></table>
      </aside>
    </div>
  </div>
</header>

<main>
<section>
  <div class="wrap">
    <figure class="mediafig" style="margin-bottom:44px">
      <div class="shot"><span class="pz"><img src="media/{img}" width="{w}" height="{h}"
        loading="lazy" alt="{alt}"></span></div>
      <figcaption>{cap}</figcaption>
    </figure>
    <div class="lede">
      <h2>{ledeh}</h2>
      <p class="intro">{ledep}</p>
    </div>
    <div class="prose">{prose}</div>
  </div>
</section>

<section id="faq">
  <div class="wrap">
    <span class="eyebrow">Questions</span>
    <div class="lede">
      <h2>What buyers ask about this lane</h2>
      <p class="intro">The four questions that decide whether a shipment on this corridor
        works, answered the way we answer them on a first call.</p>
    </div>
    <div style="margin-top:34px">{faqhtml}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="eyebrow">Other corridors</span>
    <div class="lede">
      <h2>A lane is the asset, the product travelling down it can change</h2>
      <p class="intro">Once the producers, the forwarder, the customs broker and the document
        set work on a route, the same route carries a different product next time. These are
        the routes we already run.</p>
    </div>
    <div class="lanelinks">{others}
      <a class="lanelink" href="experience.html"><b>Twenty years of supply work</b>
        <span>China, the Russian north and the European Union: three regimes, one method.</span></a>
    </div>
  </div>
</section>

<section class="cta">
  <div class="wrap">
    <span class="eyebrow">Get started</span>
    <div class="lede">
      <h2>Send a specification. Get a landed price.</h2>
      <p class="intro">Product, quantity and destination port is enough to start. If you only
        have a problem, describe it and we will write the specification with you.</p>
    </div>
    <div class="ctarow">
      <a class="btn" href="index.html#enquiry">Request a quote</a>
      <span class="mail">info@ispgroupgc.com</span>
    </div>
  </div>
</section>
</main>

{foot}
{ldjs}{navjs}{fxjs}</body>
</html>
""".format(desc=p["desc"], url=url, host=HOST, img=img, alt=alt, cap=cap, w=w, h=h,
           hero=hero, heroalt=heroalt, ogimg=hero.replace(".webp", ".jpg"),
           otitle=plain(p["h1"]), title=p["title"], icon=ICON, assets=ASSETS, fx=FX,
           nav=nav_for(p["slug"]), h1=p["h1"], sub=p["sub"], chips=chips, facts=facts,
           ledeh=p["lede"][0], ledep=p["lede"][1], prose=prose, others=others,
           sdesc=SHORTDESC[p["slug"]], faqhtml=faqhtml,
           crumb=SHORT[p["slug"]].replace("&amp;","&amp;"),
           foot=footer_for(p["slug"]), ldjs=ldjs, navjs=NAVJS, fxjs=FXJS)


# ── сборка страниц коридоров ────────────────────────────────────────────────
for p in PAGES:
    out = os.path.join(SITE, p["slug"] + ".html")
    open(out, "w", encoding="utf-8").write(build(p))
    print("собрано", out, len(open(out, encoding="utf-8").read()), "байт")


# ── правки на главной и в статье ────────────────────────────────────────────
def upgrade(path, is_index):
    s = open(path, encoding="utf-8").read()
    # обёртка для параллакса вокруг каждой фотографии
    s, k = re.subn(r'(<div class="shot">)(\s*<img\b[^>]*>)(\s*</div>)',
                   r'\1<span class="pz">\2</span>\3', s, flags=re.S)
    # общие стили и скрипт эффектов
    if ".pz{" not in s:
        i = s.rindex("</style>"); s = s[:i] + FX + s[i:]
    if "perspective(1300px)" not in s:
        s = s.replace("</body>", FXJS + "</body>", 1)
    # подвал получает колонку коридоров
    if "<dt>Corridors</dt>" not in s:
        links = "".join('<a href="%s.html" style="display:block">%s</a>' % (sl, SHORT[sl])
                        for sl, _, _ in LANES)
        s = s.replace('<div><dt>Reading</dt>',
                      '<div><dt>Corridors</dt><dd style="line-height:1.95">%s</dd></div>\n'
                      '      <div><dt>Reading</dt>' % links, 1)
    if is_index:
        # первая ячейка таблицы коридоров становится ссылкой
        for sl in SHORT:
            lab = SHORT[sl]
            s = s.replace("<tr><td>%s</td>" % lab,
                          '<tr><td><a href="%s.html">%s</a></td>' % (sl, lab), 1)
    open(path, "w", encoding="utf-8").write(s)
    print("обновлено", path, "| обёрнуто фото:", k)


upgrade(IDX, True)
upgrade(os.path.join(SITE, "experience.html"), False)

# ── sitemap ─────────────────────────────────────────────────────────────────
rows = [(HOST, "1.0", "monthly"), (HOST + "experience.html", "0.8", "yearly")]
rows += [(HOST + p["slug"] + ".html", "0.9", "monthly") for p in PAGES]
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
sm += ['  <url><loc>%s</loc><lastmod>2026-10-08</lastmod>'
       '<changefreq>%s</changefreq><priority>%s</priority></url>' % (u, c, pr)
       for u, pr, c in rows]
sm.append("</urlset>")
open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm) + "\n")
print("sitemap:", len(rows), "адресов")
