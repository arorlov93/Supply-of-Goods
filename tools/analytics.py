# -*- coding: utf-8 -*-
"""Счётчик Google Analytics на все страницы сайта.

Крючки под него в разметке уже были: `if (window.gtag) gtag('event',
'quote_submit', ...)` на главной и на странице контактов. Пока тега не
было, они молчали. Теперь заработают.

Кроме отправки заявки считается нажатие на призыв к действию: без этого
видно только посещения, а нужно видеть путь до заявки.

Тег ставится перед </head>. Он загружается асинхронно, поэтому выше
поднимать его незачем, а так он не задерживает отрисовку.

Страница /crm служебная, её в счёт не берём.

Запуск: python3.13 tools/analytics.py
Повторный запуск ничего не дублирует.
"""
import pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
GA = "G-8HDRVVXJFF"
SKIP = {"crm.html"}

SNIPPET = f"""<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  /* Без cookie. Запрет хранилища объявляется до config, иначе тег успевает
     его поставить. Настройка client_storage в GA4 не действует, проверено
     замером, подробности в tools/analytics-consent.py. */
  gtag('consent', 'default', {{ analytics_storage: 'denied', ad_storage: 'denied' }});
  gtag('config', '{GA}', {{ anonymize_ip: true }});
  /* Нажатие на призыв к действию. Посещения без этого события не
     показывают главного: сколько человек дошло до намерения оставить
     заявку. Само отправление заявки считается отдельно, в обработчике
     формы. */
  addEventListener('click', function (e) {{
    var a = e.target.closest && e.target.closest('.btn, .btn-lg, .cta, a[href*="contact"], a[href*="#request"]');
    if (!a) return;
    gtag('event', 'cta_click', {{
      label: (a.textContent || '').trim().slice(0, 48),
      page: location.pathname
    }});
  }}, {{passive: true}});
</script>
"""


def main():
    done = skipped = 0
    for p in sorted(SITE.rglob("*.html")):
        if p.name in SKIP:
            skipped += 1
            continue
        s = p.read_text()
        if GA in s:
            skipped += 1
            continue
        if "</head>" not in s:
            print(f"  ОШИБКА: нет </head> в {p.relative_to(SITE)}")
            return 1
        p.write_text(s.replace("</head>", SNIPPET + "</head>", 1))
        done += 1
    print(f"страниц со счётчиком: {done}, пропущено: {skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
