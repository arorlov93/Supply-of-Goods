# -*- coding: utf-8 -*-
"""Поиск по сайту: индекс собирается при сборке, грузится по первому открытию."""
import re, json, os, glob, html as H

def build_index(site="site", out="site/search.json"):
    rows = []
    for f in sorted(glob.glob(os.path.join(site, "*.html"))):
        slug = os.path.basename(f)[:-5]
        if slug in ("404",):
            continue
        s = open(f, encoding="utf-8").read()
        t = re.search(r"<title>(.*?)</title>", s, re.S)
        d = re.search(r'name="description" content="(.*?)"', s, re.S)
        heads = re.findall(r"<h[23][^>]*>(.*?)</h[23]>", s, re.S)
        clean = lambda x: " ".join(H.unescape(re.sub("<[^>]+>", "", x)).split())
        rows.append({
            "u": "/" if slug == "index" else "/" + slug,
            "t": clean(t.group(1)).split(" | ")[0] if t else slug,
            "d": clean(d.group(1)) if d else "",
            "h": " · ".join(clean(h) for h in heads[:9]),
        })
    json.dump(rows, open(out, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    return len(rows), os.path.getsize(out)


BUTTON = ('    <button class="navsearch" id="navsearch" type="button" aria-label="Search" '
          'aria-expanded="false" aria-controls="searchpanel">'
          '<svg viewBox="0 0 20 20" width="17" height="17" aria-hidden="true">'
          '<circle cx="8.5" cy="8.5" r="5.6" fill="none" stroke="currentColor" stroke-width="1.7"/>'
          '<path d="M12.8 12.8 17 17" stroke="currentColor" stroke-width="1.7" '
          'stroke-linecap="round"/></svg></button>\n')

PANEL = '''<div class="searchpanel" id="searchpanel" hidden>
  <div class="wrap">
    <label class="sr" for="searchinput">Search the site</label>
    <input id="searchinput" type="search" autocomplete="off" spellcheck="false"
      placeholder="Search guides, corridors, categories&hellip;">
    <p class="searchhint">Type at least two letters. Press Escape to close.</p>
    <ul class="searchres" id="searchres"></ul>
  </div>
</div>
'''

CSS = '''
/* поиск */
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.navsearch{display:inline-flex;align-items:center;justify-content:center;width:38px;height:38px;
  margin-left:4px;padding:0;border:1px solid var(--rule);background:var(--surface);
  color:var(--ink-2);cursor:pointer;border-radius:1px;box-shadow:var(--shadow-s);
  transition:border-color .18s,color .18s}
.navsearch:hover{border-color:var(--brand);color:var(--brand)}
.searchpanel{position:sticky;top:68px;z-index:39;background:var(--surface);
  border-bottom:1px solid var(--rule);box-shadow:var(--shadow-m);padding:22px 0 26px}
.searchpanel[hidden]{display:none}
.searchpanel input{width:100%;background:var(--paper);border:1px solid var(--rule);
  color:var(--ink);font-family:var(--fs);font-size:clamp(1.3rem,2.6vw,1.9rem);
  padding:14px 16px;transition:border-color .18s,box-shadow .18s}
.searchpanel input:focus{outline:none;border-color:var(--brand);box-shadow:0 0 0 3px var(--brand-wash)}
.searchhint{margin-top:10px;font-family:var(--fm);font-size:.55rem;letter-spacing:.12em;
  text-transform:uppercase;color:var(--ink-3)}
.searchres{list-style:none;margin:16px 0 0;padding:0;max-height:52vh;overflow:auto}
.searchres li{border-top:1px solid var(--rule)}
.searchres a{display:block;padding:14px 0;text-decoration:none;color:var(--ink)}
.searchres a:hover,.searchres a:focus-visible{background:var(--surface-2)}
.searchres b{display:block;font-family:var(--fs);font-weight:400;font-size:1.18rem;margin-bottom:4px}
.searchres span{display:block;color:var(--ink-2);font-size:.92rem}
.searchres mark{background:var(--gold-soft);color:inherit;padding:0 2px}
@media(max-width:940px){.searchpanel{top:68px}}
'''

JS = '''<script>
(function(){
  var btn=document.getElementById('navsearch'), panel=document.getElementById('searchpanel');
  if(!btn||!panel) return;
  var input=document.getElementById('searchinput'), out=document.getElementById('searchres');
  var idx=null, loading=false, opener=null;
  function load(){
    if(idx||loading) return;
    loading=true;
    fetch('/search.json').then(function(r){return r.json();})
      .then(function(j){ idx=j; loading=false; run(); })
      .catch(function(){ loading=false;
        out.innerHTML='<li><a href="/guides"><b>Search is unavailable</b>'+
          '<span>Browse the guides instead.</span></a></li>'; });
  }
  function esc(s){ return s.replace(/[&<>"]/g,function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];}); }
  function hl(s,q){ if(!s) return '';
    var i=s.toLowerCase().indexOf(q);
    if(i<0) return esc(s.slice(0,118));
    var a=Math.max(0,i-40), t=(a?'… ':'')+s.slice(a,i)+'\\u0000'+s.slice(i,i+q.length)+'\\u0001'+s.slice(i+q.length,i+q.length+70);
    return esc(t).replace('\\u0000','<mark>').replace('\\u0001','</mark>'); }
  function run(){
    var q=(input.value||'').trim().toLowerCase();
    if(q.length<2){ out.innerHTML=''; return; }
    if(!idx){ load(); return; }
    var hits=[];
    for(var i=0;i<idx.length;i++){
      var r=idx[i], t=r.t.toLowerCase(), d=(r.d||'').toLowerCase(), h=(r.h||'').toLowerCase();
      var sc=0;
      if(t.indexOf(q)>=0) sc+=10;
      if(h.indexOf(q)>=0) sc+=4;
      if(d.indexOf(q)>=0) sc+=3;
      if(sc) hits.push([sc,r]);
    }
    hits.sort(function(a,b){return b[0]-a[0];});
    if(!hits.length){
      out.innerHTML='<li><a href="/contact"><b>Nothing matched &ldquo;'+esc(q)+'&rdquo;</b>'+
        '<span>Ask us directly and we will answer.</span></a></li>'; return; }
    out.innerHTML=hits.slice(0,8).map(function(x){
      var r=x[1], ctx=(r.d&&r.d.toLowerCase().indexOf(q)>=0)?r.d:(r.h||r.d);
      return '<li><a href="'+r.u+'"><b>'+hl(r.t,q)+'</b><span>'+hl(ctx,q)+'</span></a></li>';
    }).join('');
  }
  function open_(){
    opener=document.activeElement;
    panel.hidden=false; btn.setAttribute('aria-expanded','true');
    load(); input.focus(); input.select();
  }
  function close_(){
    panel.hidden=true; btn.setAttribute('aria-expanded','false');
    if(opener&&opener.focus) opener.focus();
  }
  btn.addEventListener('click',function(){ panel.hidden?open_():close_(); });
  input.addEventListener('input',run);
  document.addEventListener('keydown',function(e){
    if(e.key==='Escape'&&!panel.hidden){ close_(); return; }
    if(e.key==='/'&&panel.hidden){
      var a=document.activeElement, tag=a?a.tagName:'';
      if(tag==='INPUT'||tag==='TEXTAREA'||tag==='SELECT'||(a&&a.isContentEditable)) return;
      e.preventDefault(); open_();
    }
  });
})();
</script>
'''
