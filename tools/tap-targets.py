# -*- coding: utf-8 -*-
"""Размер целей нажатия на телефоне.

Замер показал от 14 до 26 элементов на страницу, у которых хотя бы одна
сторона меньше 40 пикселей: ссылки подвала высотой 16-27, хлебные крошки
высотой 13, кнопки меню и поиска шириной 25-28. Пальцем в такое попадают с
второго раза, и это единственное замечание аудита, которое касается каждой
страницы сразу.

Правка только про область нажатия: кегль, цвет и расположение не меняются,
растёт внутренний отступ. Блок дописывается последним перед </body>, потому
что на странице несколько таблиц стилей и побеждает последняя.

Запуск: python3.13 tools/tap-targets.py
"""
import pathlib, re

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
MARK = "/* цели нажатия */"

CSS = f"""<style>{MARK}
@media (max-width:760px){{
  footer a{{display:inline-flex;align-items:center;min-height:44px;
    padding-block:6px;line-height:1.25}}
  .crumbs a{{display:inline-block;padding-block:15px}}
  nav .navtoggle,nav .navsearch,.navtoggle,.navsearch{{min-width:44px;min-height:44px}}
  nav .logo,.wordmark,a.logo{{display:inline-block;padding-block:7px}}
  nav a.btn,.cta{{display:inline-flex;align-items:center;justify-content:center;
    min-width:44px;min-height:44px;padding-block:10px}}
  .skip{{padding:12px 16px}}
}}
</style>
"""

PREV = re.compile(r"<style>" + re.escape(MARK) + r".*?</style>\s*", re.S)


def main():
    done = 0
    for p in sorted(SITE.rglob("*.html")):
        s = s0 = p.read_text()
        s = PREV.sub("", s)                      # чтобы прогон был повторяемым
        if "</body>" in s:
            s = s.replace("</body>", CSS + "</body>", 1)
        else:
            s += CSS
        if s != s0:
            p.write_text(s)
            done += 1
    print(f"страниц поправлено: {done}")


if __name__ == "__main__":
    main()
