# -*- coding: utf-8 -*-
"""Форма заявки: короче, понятнее, с призывом по результату.

Что меняется и почему.

Было девять видимых полей. Каждое поле сверх необходимого роняет долю
дошедших до отправки, а первому обращению хватает четырёх: кто пишет,
куда отвечать, куда везти и что нужно. Остальные пять не выброшены, они
убраны под раскрытие: кто готов дать подробности, тот их даст, а
остальные не упрутся в анкету.

Кнопка говорила «начните торговый запрос», то есть описывала действие
посетителя. Теперь она называет результат, и теми же словами, что и
заголовок страницы: отправьте спецификацию, получите цену с доставкой.

Ошибки показывались системным alert: окно поверх страницы, без указания
на поле. Теперь поле подсвечивается и под ним появляется строка, что
именно не так.

Поле спецификации получило живой пример вместо списка слов: человек
видит, какого рода ответ от него ждут.

Запуск: python3.13 tools/form-cta.py
"""
import pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

OLD_FIELDS = """          <div><label for="q-co">Company</label><input id="q-co" name="co" type="text" autocomplete="organization"></div>
          <div><label for="q-country">Country</label><input id="q-country" name="country" type="text" autocomplete="country-name"></div>
          <div><label for="q-cat">Category</label>
            <select id="q-cat" name="cat">
              <option>Building and finishing materials</option>
              <option>Industrial equipment and machinery</option>
              <option>Tools, hardware and fasteners</option>
              <option>Metals and pipe</option>
              <option>Paper, packaging and consumables</option>
              <option>Food, commodities and beverages</option>
              <option>Other</option>
            </select>
          </div>
          <div><label for="q-terms">Terms to quote</label>
            <select id="q-terms" name="terms"><option>Not sure, advise</option><option>EXW</option><option>FCA</option><option>FOB</option><option>CFR</option><option>CIF</option><option>DAP</option><option>DDP</option></select>
          </div>
          <div><label for="q-qty">Quantity</label><input id="q-qty" name="qty" type="text" placeholder="Containers, tonnes, pieces"></div>
          <div><label for="q-dest">Destination port or city</label><input id="q-dest" name="dest" type="text"></div>
          <div class="f-full"><label for="q-spec">Specification</label><textarea id="q-spec" name="spec" required placeholder="Standard, grade, dimensions, certification, deadline"></textarea></div>
"""

NEW_FIELDS = """          <div><label for="q-dest">Destination port or city</label><input id="q-dest" name="dest" type="text" autocomplete="address-level2"></div>
          <div class="f-full"><label for="q-spec">What do you need?</label><textarea id="q-spec" name="spec" required placeholder="For example: 2,000 m2 porcelain tile 600x600 rectified, PEI 4, EN 14411, delivered Miami, needed by March. A rough description is enough to start."></textarea></div>
          <details class="f-full f-more">
            <summary>Add details so we can quote faster</summary>
            <div class="fgrid">
              <div><label for="q-co">Company</label><input id="q-co" name="co" type="text" autocomplete="organization"></div>
              <div><label for="q-country">Country</label><input id="q-country" name="country" type="text" autocomplete="country-name"></div>
              <div><label for="q-cat">Category</label>
                <select id="q-cat" name="cat">
                  <option>Building and finishing materials</option>
                  <option>Industrial equipment and machinery</option>
                  <option>Tools, hardware and fasteners</option>
                  <option>Metals and pipe</option>
                  <option>Paper, packaging and consumables</option>
                  <option>Food, commodities and beverages</option>
                  <option>Other</option>
                </select>
              </div>
              <div><label for="q-terms">Terms to quote</label>
                <select id="q-terms" name="terms"><option>Not sure, advise</option><option>EXW</option><option>FCA</option><option>FOB</option><option>CFR</option><option>CIF</option><option>DAP</option><option>DDP</option></select>
              </div>
              <div><label for="q-qty">Quantity</label><input id="q-qty" name="qty" type="text" placeholder="Containers, tonnes, pieces"></div>
            </div>
          </details>
"""

OLD_BTN = ('<p style="margin:20px 0 0"><button class="btn-lg" type="submit">'
           'Start a trade request</button></p>\n'
           '        <p class="form-note">Sent straight to info@ispgroupgc.com. '
           'We reply within one working day.</p>')

NEW_BTN = ('<p style="margin:20px 0 0"><button class="btn-lg" type="submit">'
           'Get a landed price</button></p>\n'
           '        <p class="form-note">Goes straight to info@ispgroupgc.com. '
           'Within one working day you get either a price, or the questions that '
           'decide it. No brochure, no mailing list.</p>')

OLD_VALIDATE = """    if(!data.name || !data.mail || !data.spec){
      alert('Please give your name, a work e-mail and what you need.');
      return;
    }"""

NEW_VALIDATE = """    /* Ошибка показывается у поля, а не системным окном: человек сразу
       видит, что именно исправить, и не теряет уже введённое. */
    Array.prototype.forEach.call(f.querySelectorAll('.f-err'), function(e){ e.remove(); });
    Array.prototype.forEach.call(f.querySelectorAll('.bad'), function(e){ e.classList.remove('bad'); });
    var first = null;
    function err(id, msg){
      var el = document.getElementById(id);
      if(!el) return null;
      el.classList.add('bad');
      var s = document.createElement('span');
      s.className = 'f-err';
      s.textContent = msg;
      el.parentNode.appendChild(s);
      if(!first) first = el;
      return el;
    }
    if(!data.name) err('q-name', 'Tell us who is writing.');
    if(!data.mail) err('q-mail', 'We need an address to reply to.');
    else if(!/^[^@\\s]+@[^@\\s.]+\\.[^@\\s]+$/.test(data.mail)) err('q-mail', 'That address does not look right.');
    if(!data.spec) err('q-spec', 'A rough description is enough to start.');
    if(first){ first.focus(); return; }"""

CSS = """
/* Форма заявки: короткая по умолчанию, подробности по раскрытию.
   Каждое лишнее видимое поле роняет долю дошедших до отправки, но
   выбрасывать поля нельзя: тот, кто готов дать спецификацию, экономит нам
   переписку. Поэтому они не убраны, а свёрнуты. */
.f-more { grid-column: 1 / -1; border-top: var(--rule-hair) solid var(--color-paper-3); padding-top: 16px; }
.f-more > summary {
  cursor: pointer; list-style: none;
  font: 600 .78rem/1.3 var(--font-body);
  letter-spacing: .08em; text-transform: uppercase;
  color: var(--color-accent-deep);
}
.f-more > summary::-webkit-details-marker { display: none; }
.f-more > summary::before { content: "+ "; }
.f-more[open] > summary::before { content: "\\2212 "; }
.f-more > .fgrid { margin-top: 18px; }

/* Ошибка у поля, а не в системном окне */
.f-err { display: block; margin-top: 6px; font: .78rem/1.35 var(--font-body); color: var(--color-accent-deep); }
input.bad, textarea.bad, select.bad { outline: 2px solid var(--color-accent-deep) !important; outline-offset: -2px; }
"""


def main():
    bad = 0

    p = SITE / "index.html"
    s = p.read_text()

    for name, old, new in (("поля", OLD_FIELDS, NEW_FIELDS),
                           ("кнопка", OLD_BTN, NEW_BTN),
                           ("проверка", OLD_VALIDATE, NEW_VALIDATE)):
        if old not in s:
            print(f"  ОШИБКА: фрагмент «{name}» не найден, разметка изменилась")
            bad += 1
            continue
        s = s.replace(old, new, 1)
        print(f"  {name}: заменено")

    if not bad:
        p.write_text(s)

    css = SITE / "css" / "formwork.css"
    c = css.read_text()
    if ".f-more" not in c:
        css.write_text(c + CSS)
        print("  css: правила формы добавлены")
    else:
        print("  css: правила уже есть")

    # поля должны остаться все: обработчик читает их по id
    s2 = (SITE / "index.html").read_text()
    for fid in ("q-name", "q-mail", "q-co", "q-country", "q-cat",
                "q-terms", "q-qty", "q-dest", "q-spec", "q-website"):
        if f'id="{fid}"' not in s2:
            print(f"  ОШИБКА: поле {fid} потерялось")
            bad += 1
    print("  все поля на месте" if not bad else "")

    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
