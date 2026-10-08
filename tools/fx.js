<script>
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
<script>
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
  function show(el){
    el.style.transition='opacity .75s '+EASE+' '+el.__d+'ms, transform .95s '+EASE+' '+el.__d+'ms';
    el.style.opacity=''; el.style.transform='';
    setTimeout(function(){ el.style.transition=''; el.style.willChange=''; }, el.__d+1200);
  }
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(!e.isIntersecting) return;
      var el=e.target; io.unobserve(el); show(el);
    });
  },{rootMargin:'0px 0px -9% 0px', threshold:0.05});
  items.forEach(function(el){ io.observe(el); });

  /* Подстраховка. Наблюдатель изредка не срабатывает, и тогда блок остаётся
     невидимым навсегда. Раз в полторы секунды показываем всё, что уже в кадре,
     и прекращаем, когда скрытого не осталось. */
  var sweeps=0;
  var timer=setInterval(function(){
    var left=0, h=window.innerHeight||0;
    for(var i=0;i<items.length;i++){
      var el=items[i];
      if(el.style.opacity!=='0') continue;
      left++;
      if(el.getBoundingClientRect().top < h+140){ io.unobserve(el); show(el); }
    }
    if(!left || ++sweeps>40) clearInterval(timer);
  },1500);

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
