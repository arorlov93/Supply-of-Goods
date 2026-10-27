// Контраст текста, лежащего поверх фотографии.
//
// Обычная проверка такие места пропускает: фон там кадр, а не цвет, и по
// каскаду его не вычислить. Поэтому меряем по пикселям. Приём простой:
// сначала запоминаем цвет и коробку каждого текста, затем делаем буквы
// прозрачными и снимаем элемент. На снимке остаётся чистый фон, и его
// яркость уже можно сравнить с цветом текста.
//
// Снимки кладутся в каталог, который передаётся первым аргументом;
// яркость по ним считает tools/contrast-photo.py.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');

const OUT = process.argv[2];
const ROOT = path.resolve(__dirname, '..', 'site');
const BASE = process.env.BASE || 'http://127.0.0.1:8899';
const SEL = '.scene .content, .hero .content, .shot, figure, a.card';

function pages(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const f = path.join(dir, e.name);
    if (e.isDirectory()) { if (!['media','css','fonts','js'].includes(e.name)) pages(f, out); }
    else if (e.name.endsWith('.html')) out.push(path.relative(ROOT, f));
  }
  return out;
}

(async () => {
  const meta = [];
  const br = await chromium.launch();
  const pg = await (await br.newContext({ viewport: { width: 1440, height: 900 } })).newPage();
  for (const rel of pages(ROOT).sort()) {
    await pg.goto(`${BASE}/${rel.split(path.sep).join('/')}`, { waitUntil: 'networkidle' });
    await pg.evaluate(() => document.querySelectorAll('img[loading="lazy"]').forEach(i => i.loading = 'eager'));
    await pg.evaluate(() => Promise.all([...document.images].map(i => i.complete ? null :
      new Promise(r => { i.onload = r; i.onerror = r; }))));
    await pg.waitForTimeout(300);

    const items = await pg.evaluate((SEL) => {
      const cv = document.createElement('canvas'); cv.width = cv.height = 1;
      const cx = cv.getContext('2d', { willReadFrequently: true });
      const rgb = (c) => { cx.fillStyle = '#000'; cx.fillStyle = c; cx.fillRect(0,0,1,1);
        const d = cx.getImageData(0,0,1,1).data; return [d[0],d[1],d[2]]; };
      const out = [];
      document.querySelectorAll(SEL).forEach((box, bi) => {
        box.querySelectorAll('h1,h2,h3,h4,p,li,b,span,a').forEach((el, ei) => {
          if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return;
          const cs = getComputedStyle(el);
          if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity === 0) return;
          const r = el.getBoundingClientRect();
          if (r.width < 12 || r.height < 10) return;
          el.setAttribute('data-cp', bi + '-' + ei);
          out.push({ id: bi + '-' + ei, color: rgb(cs.color),
                     px: parseFloat(cs.fontSize), bold: +cs.fontWeight >= 700,
                     text: el.textContent.trim().slice(0, 36), tag: el.tagName });
        });
      });
      return out;
    }, SEL);
    if (!items.length) continue;

    // буквы прозрачны, тени сняты: на снимке остаётся только фон
    await pg.addStyleTag({ content: '*{color:transparent !important;text-shadow:none !important;' +
                                    '-webkit-text-stroke:0 !important}' });
    await pg.waitForTimeout(150);
    for (const it of items) {
      const file = path.join(OUT, `${rel.replace(/[\/\\]/g,'_')}__${it.id}.png`);
      try { await pg.locator(`[data-cp="${it.id}"]`).screenshot({ path: file }); }
      catch { continue; }
      meta.push({ page: rel, file, ...it });
    }
  }
  await br.close();
  fs.writeFileSync(path.join(OUT, 'meta.json'), JSON.stringify(meta));
  console.log('замеров подготовлено:', meta.length);
})();
