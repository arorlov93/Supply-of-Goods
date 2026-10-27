# -*- coding: utf-8 -*-
"""Уведомление о заявке отправляет страница, а не сервер.

Почему так. Ретранслятор принимает письма только из настоящего браузера.
Запросы, уходящие с серверов Cloudflare, он отбивает кодом 429, и это не
предел частоты: в ту же секунду тот же запрос с обычной машины получает
200. Проверено и в журнале Worker, и напрямую.

Поэтому разделение обязанностей. Сервер принимает заявку и кладёт её в
базу, это надёжно и ни от кого не зависит. Страница досылает уведомление
на почту, потому что только у неё это получается. Если не получится и у
неё, заявка всё равно у нас: она в базе и помечена в CRM как ждущая
письма.

Серверный ответ теперь несёт номер заявки и подпись к нему. Отправив
уведомление, страница возвращает их обратно, и отметка в CRM становится
правдивой. Подпись нужна, чтобы посторонний не мог пометить чужие заявки
отправленными и спрятать их.

Ключ RESEND_KEY снимет всю эту конструкцию: тогда письмо уйдёт с нашего
домена прямо с сервера.

Запуск: python3.13 tools/form-relay.py
Повторный запуск ничего не меняет.
"""
import pathlib, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

OLD = """        if (j && j.ok) { if (j.mail === false) { try { relay(); } catch(e){} } return; }"""

NEW = """        if (j && j.ok) {
          /* mail: false или "queued" значит, что с сервера письмо не
             ушло: ретранслятор принимает только браузерные запросы.
             Шлём отсюда и возвращаем отметку, чтобы в CRM было видно,
             что уведомление действительно доставлено. */
          if (j.mail === false || j.mail === 'queued') {
            try {
              relay().then(function(){
                if (!j.id || !j.token) return;
                return fetch('/api/quote', {method:'POST',
                  headers:{'Content-Type':'application/json'},
                  body:JSON.stringify({confirm:j.id, token:j.token})});
              }).catch(function(){});
            } catch(e){}
          }
          return;
        }"""


def main():
    done = skipped = 0
    for p in sorted(SITE.rglob("*.html")):
        s = p.read_text()
        if "j.mail === 'queued'" in s:
            skipped += 1
            continue
        if OLD not in s:
            skipped += 1
            continue
        p.write_text(s.replace(OLD, NEW))
        done += 1
    print(f"страниц с досылкой из браузера: {done}, пропущено: {skipped}")
    return 0 if done else 1


if __name__ == "__main__":
    sys.exit(main())
