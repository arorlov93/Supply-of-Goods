# -*- coding: utf-8 -*-
"""Содержимое видно по умолчанию, скрывает его скрипт, а не наоборот.

Правило Hallmark 62 и пункт 7 его «пола». Блоки с появлением при прокрутке
стояли в CSS с opacity:0 и ждали, пока скрипт повесит класс. Пока скрипт
не отработал, страница пустая: при медленной сети, при ошибке в скрипте и
у поисковых роботов, которые не ждут. Заплатка через <noscript> закрывала
только случай «скрипт выключен», но не случай «скрипт ещё не выполнился»
и не случай «скрипт упал».

Правильный порядок обратный: разметка видна, а скрытое состояние живёт под
классом, который скрипт ставит на <html> первым делом. Не выполнился
скрипт - содержимое просто осталось на месте.

Запуск: python3.13 tools/slop-reveal.py
"""
import pathlib, re

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

# селекторы, у которых скрытое состояние: правило начинается ровно с них
HIDDEN = [".fade", ".jsteps li", ".steps li", ".svc-list li", "[data-reveal]",
          ".ln>span", ".ln > span"]

FLAG = ('<script>document.documentElement.classList.add("js")</script>')
NOSCRIPT = re.compile(r"<noscript><style>[^<]*</style></noscript>\s*", re.S)


def scope(s):
    """Приписать .js скрытым правилам, не трогая правила видимого состояния."""
    out, n = s, 0
    for sel in HIDDEN:
        # только объявление скрытого состояния: с opacity:0 внутри
        pat = re.compile(r"(?<![\w.\-\[])" + re.escape(sel) + r"\{([^}]*opacity:0[^}]*)\}")
        def rep(m):
            nonlocal n
            n += 1
            return f".js {sel}{{{m.group(1)}}}"
        out = pat.sub(rep, out)
    return out, n


def main():
    pages, rules = 0, 0
    for p in sorted(SITE.rglob("*.html")):
        s = s0 = p.read_text()

        s, n = scope(s)
        rules += n

        # заплатка больше не нужна: видимость теперь состояние по умолчанию
        s = NOSCRIPT.sub("", s)

        # класс ставится до первой отрисовки, иначе блоки мигнут
        if 'classList.add("js")' not in s:
            s = re.sub(r"(<head[^>]*>)", r"\1\n" + FLAG, s, count=1)

        if s != s0:
            p.write_text(s)
            pages += 1
    print(f"страниц изменено: {pages}, правил скрытого состояния: {rules}")


if __name__ == "__main__":
    main()
