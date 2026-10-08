# -*- coding: utf-8 -*-
"""Числовая полоса под героем. Конкуренты выносят объёмы (Interra: 4 300 товаров,
45 стран, 112 назначений). Мы выносим то, что посетитель может проверить кликом,
и ни одной придуманной цифры."""

EN = """
<section id="numbers">
  <div class="wrap">
    <span class="eyebrow">In numbers</span>
    <div class="lede">
      <h2>Everything here is checkable on this site</h2>
      <p class="intro">We do not publish tonnage or client names we cannot evidence. Each
        figure below links to the pages it is counted from, so you can verify it yourself
        before you write to us.</p>
    </div>
    <div class="nums">
      <div class="num"><b>20</b><span>Years of<br><a href="experience.html">supply work</a></span></div>
      <div class="num"><b>4</b><span><a href="corridors.html">Corridors</a><br>run end to end</span></div>
      <div class="num"><b>14</b><span>Gateway ports<br><a href="corridors.html">on those lanes</a></span></div>
      <div class="num"><b>6</b><span><a href="supply.html">Categories</a><br>supplied</span></div>
      <div class="num"><b>3</b><span>Verified producers<br>per enquiry</span></div>
    </div>
  </div>
</section>
"""

FR = """
<section id="numbers">
  <div class="wrap">
    <span class="eyebrow">En chiffres</span>
    <div class="lede">
      <h2>Tout ce qui suit est v&eacute;rifiable sur ce site</h2>
      <p class="intro">Nous ne publions ni tonnages ni noms de clients que nous ne pouvons
        pas prouver. Chaque chiffre renvoie aux pages d&rsquo;o&ugrave; il est compt&eacute;.</p>
    </div>
    <div class="nums">
      <div class="num"><b>20</b><span>Ans<br>d&rsquo;exp&eacute;rience</span></div>
      <div class="num"><b>4</b><span>Lignes exploit&eacute;es<br>de bout en bout</span></div>
      <div class="num"><b>14</b><span>Ports<br>sur ces lignes</span></div>
      <div class="num"><b>6</b><span>Cat&eacute;gories<br>fournies</span></div>
      <div class="num"><b>3</b><span>Producteurs v&eacute;rifi&eacute;s<br>par demande</span></div>
    </div>
  </div>
</section>
"""


NUMS_JS = """<script>
(function(){
  /* Цифры выезжают из глубины и досчитываются, затем переходят на лёгкий
     параллакс. Без JS и при prefers-reduced-motion блок просто виден. */
  var wrap=document.querySelector('.nums'); if(!wrap) return;
  var nums=[].slice.call(wrap.querySelectorAll('.num'));
  if(!nums.length) return;
  var EASE='cubic-bezier(.16,.74,.22,1)';
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  nums.forEach(function(n){
    var b=n.querySelector('b'); if(!b) return;
    b.setAttribute('data-to', b.textContent.trim());
  });
  if(reduce || !('IntersectionObserver' in window)) return;
  nums.forEach(function(n){
    n.style.opacity='0';
    n.style.transform='rotateX(-74deg) translate3d(0,30px,-70px)';
  });
  function run(n,i){
    var b=n.querySelector('b');
    var to=parseInt(b.getAttribute('data-to'),10);
    if(isNaN(to)) to=null; else b.textContent='0';
    setTimeout(function(){
      n.style.transition='opacity .55s '+EASE+', transform .95s '+EASE;
      n.style.opacity=''; n.style.transform='';
      if(to!==null){
        var t0=performance.now(), dur=760+i*70;
        (function tick(now){
          var p=Math.min(1,(now-t0)/dur), e=1-Math.pow(1-p,3);
          b.textContent=Math.round(to*e);
          if(p<1) requestAnimationFrame(tick); else b.textContent=to;
        })(t0);
      }
      setTimeout(function(){ n.style.transition=''; n.__ready=1; }, 1100);
    }, i*105);
  }
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(!e.isIntersecting) return;
      io.unobserve(e.target); run(e.target, nums.indexOf(e.target));
    });
  },{threshold:0.35});
  nums.forEach(function(n){ io.observe(n); });
  /* страховка: если наблюдатель промолчал, всё равно показать */
  setTimeout(function(){
    nums.forEach(function(n,i){ if(n.style.opacity==='0' &&
      n.getBoundingClientRect().top < (window.innerHeight||0)+140){ io.unobserve(n); run(n,i); } });
  }, 2600);
  var q=false;
  function par(){
    q=false;
    var r=wrap.getBoundingClientRect(), h=window.innerHeight||1;
    var p=((r.top+r.height/2)-h/2)/h;
    if(p>1.5||p<-1.5) return;
    for(var i=0;i<nums.length;i++){
      var n=nums[i]; if(!n.__ready) continue;
      var k=1+(i-(nums.length-1)/2)*0.17;
      n.style.transform='translate3d(0,'+(p*-9*k).toFixed(2)+'px,0) rotateX('+(p*2.6).toFixed(2)+'deg)';
    }
  }
  window.addEventListener('scroll',function(){ if(!q){q=true;requestAnimationFrame(par);} },{passive:true});
})();
</script>
"""


def inject(path, block, css=None):
    s = open(path, encoding="utf-8").read()
    if 'id="numbers"' in s:
        import re
        s = re.sub(r'\n<section id="numbers">.*?</section>\n', "\n", s, flags=re.S)
    s = s.replace("</header>\n\n<main>", "</header>\n\n<main>\n" + block.strip() + "\n", 1)
    if css and ".nums{" not in s:
        i = s.rindex("</style>")
        s = s[:i] + css + s[i:]
    if "perspective:1300px" not in s:
        i = s.rindex("</style>")
        s = s[:i] + '\n/* числовая полоса: объём и счётчик */\n.nums{perspective:1300px;perspective-origin:50% 40%}\n.num{transform-style:preserve-3d;will-change:transform,opacity}\n.num b{display:block;transform-origin:50% 90%;\n  text-shadow:0 1px 0 rgba(255,255,255,.65), 0 10px 26px rgba(11,74,64,.16);\n  font-variant-numeric:tabular-nums}\n@media (prefers-reduced-motion:reduce){.num{transform:none!important;opacity:1!important}}\n' + s[i:]
    if "data-to" not in s:
        s = s.replace("</body>", NUMS_JS + "</body>", 1)
    open(path, "w", encoding="utf-8").write(s)
