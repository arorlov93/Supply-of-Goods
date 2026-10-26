// Ищет текст, который не помещается в свою ячейку и вылезает на соседей.
//
// getBoundingClientRect возвращает коробку элемента, а не чернила: заголовок
// в колонке 76px отдаёт ширину 76px, даже когда слово занимает 210px и лежит
// поверх абзаца. Поэтому сравниваем scrollWidth с clientWidth: расхождение и
// есть вылезший текст. Проверка дешёвая, гонять её стоит после каждой правки
// разметки или типографики.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');

const ROOT = path.resolve(__dirname, '..', 'site');
const BASE = process.env.BASE || 'http://127.0.0.1:8899';
const WIDTHS = [1680, 1440, 1180, 980, 860, 760, 420];

function pages(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const f = path.join(dir, e.name);
    if (e.isDirectory()) { if (!['media', 'css', 'fonts', 'js'].includes(e.name)) pages(f, out); }
    else if (e.name.endsWith('.html')) out.push(path.relative(ROOT, f));
  }
  return out;
}

const probe = () => {
  const out = [];
  for (const el of document.querySelectorAll('h1,h2,h3,h4,p,li,td,th,b,a,button,label')) {
    if (!el.firstChild) continue;
    const cs = getComputedStyle(el);
    if (cs.overflow !== 'visible' || cs.position === 'absolute') continue;
    // строчные элементы не имеют собственной ширины, а у скрытых для
    // скринридера подписей она равна пикселю: и то и другое не наложение
    if (cs.display.startsWith('inline') && cs.display !== 'inline-block') continue;
    if (cs.whiteSpace === 'nowrap' || cs.textOverflow === 'ellipsis') continue;
    const over = el.scrollWidth - el.clientWidth;
    if (over > 2 && el.clientWidth >= 40) {
      out.push({ tag: el.tagName, cls: el.className || '', over,
                 w: el.clientWidth, text: (el.textContent || '').trim().slice(0, 40) });
    }
  }
  return out;
};

(async () => {
  const list = pages(ROOT).sort();
  let bad = 0;
  const br = await chromium.launch();
  for (const w of WIDTHS) {
    const ctx = await br.newContext({ viewport: { width: w, height: 900 } });
    const pg = await ctx.newPage();
    for (const rel of list) {
      await pg.goto(`${BASE}/${rel.split(path.sep).join('/')}`, { waitUntil: 'networkidle' });
      for (const r of await pg.evaluate(probe)) {
        bad++;
        console.log(`${rel} @${w}px  <${r.tag}.${r.cls}> ячейка ${r.w}px, текст шире на ${r.over}px  «${r.text}»`);
      }
    }
    await ctx.close();
  }
  await br.close();
  console.log(`страниц ${list.length}, ширин ${WIDTHS.length}, вылезаний: ${bad}`);
  process.exit(bad ? 1 : 0);
})();
