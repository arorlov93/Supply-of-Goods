# -*- coding: utf-8 -*-
"""Оживляет кнопку меню в шапке.

Что было. Кнопка <button class="navtoggle" id="navtoggle"> стоит на всех
65 страницах, у неё размечены aria-expanded и aria-controls, под неё
написан целый блок оформления: выдвижной список, перечёркивание полосок
в крестик при aria-expanded="true". Не написан был только обработчик.
Ни одна страница не вешает на кнопку click. Замер: ширина 700, 900 и
1024, нажатие на кнопку, класс open не появляется, список остаётся
display:none.

Чем это стоило. На телефоне и планшете в шапке остаются логотип, поиск
и кнопка заявки. Разделов сайта нет вообще, и попасть на них можно
только из ссылок в тексте и в подвале. Это не мелкая небрежность
оформления, это отсутствие навигации на половине устройств.

Что делает скрипт. Переключает класс open на списке и aria-expanded на
кнопке. Закрывает меню по Escape, по нажатию вне шапки, по переходу по
ссылке и при расширении окна выше полосы, на которой список снова
становится горизонтальным. Фокус после закрытия по Escape возвращается
на кнопку, иначе человек с клавиатуры теряет место.

Вставляется перед </body>, потому что к этому моменту разметка шапки уже
разобрана и querySelector находит элементы без ожидания события.

Запуск: python3 tools/nav-toggle.py
Повторный запуск ничего не меняет: вставка помечена nav:v1.
"""
import pathlib, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
MARK = "/* nav:v1 */"

# 1090 это верхняя граница полосы, на которой тема держит выдвижное меню
# вместо горизонтального ряда. Значение продублировано в mercury.css,
# в медиазапросе 941-1090, и менять его нужно в обоих местах.
SCRIPT = """<script>
%s
(function(){
  var btn=document.getElementById('navtoggle'), menu=document.getElementById('navmenu');
  if(!btn||!menu) return;
  function set(open){
    menu.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', open?'true':'false');
  }
  btn.addEventListener('click', function(){
    set(btn.getAttribute('aria-expanded')!=='true');
  });
  menu.addEventListener('click', function(e){
    if(e.target.closest('a')) set(false);
  });
  document.addEventListener('keydown', function(e){
    if(e.key==='Escape' && btn.getAttribute('aria-expanded')==='true'){
      set(false); btn.focus();
    }
  });
  document.addEventListener('click', function(e){
    if(btn.getAttribute('aria-expanded')!=='true') return;
    if(!e.target.closest('nav')) set(false);
  });
  var wide=window.matchMedia('(min-width: 1091px)');
  var onwide=function(){ if(wide.matches) set(false); };
  if(wide.addEventListener) wide.addEventListener('change', onwide);
  else if(wide.addListener) wide.addListener(onwide);
})();
</script>
""" % MARK


def main():
    added = already = skipped = 0
    for p in sorted(SITE.rglob("*.html")):
        s = p.read_text()
        if 'id="navtoggle"' not in s or 'id="navmenu"' not in s:
            skipped += 1
            continue
        if MARK in s:
            already += 1
            continue
        i = s.rfind("</body>")
        if i < 0:
            print(f"  ОШИБКА: нет </body> в {p.relative_to(SITE)}")
            return 1
        p.write_text(s[:i] + SCRIPT + s[i:])
        added += 1

    print(f"  кнопка меню оживлена: {added} страниц, "
          f"уже было: {already}, без кнопки: {skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
