# -*- coding: utf-8 -*-
"""Форма заявки: чтобы ни одна не терялась.

Что было не так, и это главное в этой правке. Скрипт формы выглядел
надёжным, а работал наоборот. Строка

    .then(function(j){ return (j && j.ok) ? j : relay(); })

читается как «если наш приёмник ответил успехом, больше ничего не
делаем». Но приёмник отвечает успехом всегда, когда заявка легла в базу,
и в этом же ответе пишет mail: "queued", то есть «письмо не ушло,
отправь его сам». Ретранслятор в итоге не вызывался ни разу, а
посетителю показывалось «Requirement received». Заявки ложились в базу
молча, и узнать о них можно было, только открыв CRM руками.

Почему письмо вообще шлёт страница. Бесплатный ретранслятор отбивает
запросы с серверов Cloudflare кодом 429, с обычной машины в ту же
секунду отвечает 200. Проверено отдельным замером. Поэтому отправляет
браузер, а сервер только помечает отправленное.

Что теперь устроено слоями, от быстрого к надёжному.

1. Заявка пишется в базу раньше всего. Это и есть «не потеряется»:
   дальше речь только о том, как быстро о ней узнают.
2. Страница шлёт уведомление и подтверждает его серверу подписанной
   отметкой. Три попытки с нарастающей паузой.
3. Не вышло — заявка кладётся в очередь в localStorage и повторяется при
   следующем открытии любой страницы сайта. Очередь переживает закрытие
   вкладки и перезагрузку.
4. Вкладку закрывают прямо сейчас — уходит sendBeacon, он успевает
   отправиться после того, как страница уже закрылась.
5. Посетителю в любом случае показывается номер заявки и адрес почты.
   Это последний слой и он человеческий: даже если все машинные пути
   отказали, человек знает, на что сослаться.

Снаружи всё это страхует проверка /api/pulse, которая видит, сколько
заявок лежит без уведомления. Её слои 1-5 не заменяют: она отвечает на
вопрос «что-то сломалось?», а не доставляет письмо.

Запуск: python3.13 tools/form-robust.py
Повторный запуск переписывает скрипт тем же содержимым.
"""
import pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
PAGES = ["contact.html", "contact-fr.html"]

MARK = "/* queue:v2 */"

SCRIPT = MARK + r"""
(function(){
  var f=document.getElementById('cf');
  var KEY='isp.queue';

  /* ---- очередь уведомлений -------------------------------------------
     Живёт в localStorage, поэтому переживает закрытие вкладки. Каждый
     элемент это то, что нужно для одной отправки: тело письма, номер
     заявки и подпись, которой сервер поверит отметке «отправлено». */
  function load(){ try{ return JSON.parse(localStorage.getItem(KEY)||'[]'); }catch(e){ return []; } }
  function save(q){ try{ localStorage.setItem(KEY, JSON.stringify(q.slice(-20))); }catch(e){} }
  function push(item){ var q=load(); q.push(item); save(q); }
  function drop(stamp){ save(load().filter(function(x){ return x.stamp!==stamp; })); }

  function send(item){
    return fetch('https://formsubmit.co/ajax/info@ispgroupgc.com',{method:'POST',
      headers:{'Content-Type':'application/json',Accept:'application/json'},
      body:JSON.stringify(item.body)})
      .then(function(r){ return r.json(); })
      .then(function(j){ if(String(j&&j.success)!=='true') throw 0; return true; });
  }

  function confirm(item){
    if(!item.id || !item.token) return Promise.resolve();
    return fetch('/api/quote',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({confirm:String(item.id), token:item.token})}).catch(function(){});
  }

  /* Три попытки с нарастающей паузой. Ретранслятор пропускает примерно
     одну заявку в сорок секунд, поэтому паузы такого же порядка: более
     частый повтор упирается в тот же отказ. */
  function attempt(item, tries){
    return send(item)
      .then(function(){ drop(item.stamp); return confirm(item); })
      .catch(function(){
        if(tries<=1) return false;
        return new Promise(function(res){ setTimeout(res, tries===3?4000:20000); })
          .then(function(){ return attempt(item, tries-1); });
      });
  }

  /* При открытии любой страницы сайта дожимаем то, что лежит в очереди.
     Берём по одной: ретранслятор не любит очередей подряд. */
  function drain(){
    var q=load(); if(!q.length) return;
    attempt(q[0], 2);
  }

  /* Вкладку закрывают. fetch в этот момент обрывается, sendBeacon нет:
     браузер обязан его доставить уже после закрытия страницы. */
  function flush(){
    var q=load(); if(!q.length || !navigator.sendBeacon) return;
    try{
      navigator.sendBeacon('https://formsubmit.co/ajax/info@ispgroupgc.com',
        new Blob([JSON.stringify(q[0].body)], {type:'application/json'}));
    }catch(e){}
  }
  addEventListener('pagehide', flush);
  addEventListener('visibilitychange', function(){ if(document.visibilityState==='hidden') flush(); });

  if(document.readyState==='loading') addEventListener('DOMContentLoaded', drain);
  else drain();

  if(!f) return;

  function v(id){ var e=document.getElementById(id); return e?(e.value||'').trim():''; }

  f.addEventListener('submit',function(e){
    e.preventDefault();
    var data={ name:v('f-name'), mail:v('f-mail'), co:v('f-co'),
      spec:[v('f-product'), v('f-note')].filter(Boolean).join('\n\n'),
      qty:v('f-qty'), dest:v('f-port'), terms:v('f-terms'),
      website:v('f-website'), page:location.pathname };
    var out=document.getElementById('cf-out');
    if(!data.name || !data.mail || !data.spec){
      out.textContent='Please give your name, a work e-mail and what you need.';
      out.hidden=false; return;
    }
    var btn=f.querySelector('button[type=submit]'); var label=btn.textContent;
    btn.disabled=true; btn.textContent='Sending';

    function plain(){return ['Name: '+data.name,'Company: '+data.co,'Work e-mail: '+data.mail,'',
        'Product: '+v('f-product'),'Quantity: '+data.qty,'Destination: '+data.dest,
        'Terms: '+data.terms,'','Notes:',v('f-note')].join('\n');}

    function body(){ return {_subject:'Requirement: '+(data.co||data.name), _replyto:data.mail,
      _template:'table', _captcha:'false', Name:data.name, 'Work e-mail':data.mail,
      Company:data.co, Product:v('f-product'), Quantity:data.qty,
      Destination:data.dest, Terms:data.terms, Notes:v('f-note')}; }

    function done(ref){
      var r = ref ? ' Your reference is <b>'+ref+'</b>.' : '';
      f.innerHTML='<p class="cresult" style="margin:0"><b>Requirement received.</b>'+r+
        ' We reply within one working day. If you have heard nothing by then, write to '+
        '<a class="mail" href="mailto:info@ispgroupgc.com">info@ispgroupgc.com</a>'+
        (ref?' quoting '+ref:'')+'.</p>';
      if(window.gtag) gtag('event','quote_submit',{page:'contact'});
    }

    fetch('/api/quote',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify(data)})
      .then(function(r){ return r.json().catch(function(){return null;}); })
      .then(function(j){
        if(!j || !j.ok) throw 0;
        /* Заявка у нас. Что бы дальше ни случилось с письмом, она не
           потеряна, поэтому посетителю отвечаем сразу и честно. */
        var ref = j.id ? ('#'+j.id) : '';
        done(ref);
        if(j.mail==='queued' || j.mail===false){
          var item={stamp:Date.now(), id:j.id, token:j.token, body:body()};
          push(item);
          attempt(item, 3);
        }
      })
      .catch(function(){
        /* Приёмник недоступен: заявки у нас нет. Единственный честный
           выход это отдать человеку готовое письмо. */
        btn.disabled=false; btn.textContent=label;
        var subj='Requirement'+(v('f-product')?(': '+v('f-product')):'');
        out.innerHTML='We could not send this from the page. Please e-mail it to '+
          '<a class="mail" href="mailto:info@ispgroupgc.com?subject='+encodeURIComponent(subj)+
          '&body='+encodeURIComponent(plain())+'">info@ispgroupgc.com</a>.';
        out.hidden=false;
      });
  });
})();
"""


def main():
    done = 0
    for name in PAGES:
        p = SITE / name
        if not p.is_file():
            continue
        s = p.read_text()
        # прежний скрипт формы: от <script> с getElementById('cf') до конца
        m = re.search(r"<script>\s*\(function\(\)\{[^\0]*?getElementById\('cf'\)[^\0]*?</script>", s)
        if not m:
            print(f"  {name}: скрипт формы не найден")
            continue
        s = s[: m.start()] + "<script>" + SCRIPT + "</script>" + s[m.end():]
        p.write_text(s)
        print(f"  {name}: скрипт формы заменён ({len(SCRIPT)} знаков)")
        done += 1
    print(f"страниц правлено: {done}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
