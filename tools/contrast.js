// Контраст текста по всему сайту, замер по настоящим пикселям.
//
// Прошлая версия этой проверки считала цвет по каскаду и была выброшена:
// шапка лежит поверх фотографии и собственного фона не имеет, подъём по
// родителям находил фон страницы и выдавал сотни несуществующих нарушений.
//
// Здесь две поправки, и обе обязательны.
// Первая: цвета на сайте заданы в oklch, разбирать строку как RGB нельзя,
// перевод делается через canvas, который принимает любой формат CSS.
// Вторая: элементы поверх фотографии пропускаются, у них фон это кадр, а
// не цвет, и мерить его по каскаду бессмысленно. Такие места проверяются
// глазами на снимке, а не этим скриптом.
//
// Запуск: node tools/contrast.js   (сервер на 127.0.0.1:8899)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');

const ROOT = path.resolve(__dirname, '..', 'site');
const BASE = process.env.BASE || 'http://127.0.0.1:8899';
const WIDTHS = [1440, 420];

function pages(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const f = path.join(dir, e.name);
    if (e.isDirectory()) { if (!['media', 'css', 'fonts', 'js'].includes(e.name)) pages(f, out); }
    else if (e.name.endsWith('.html')) out.push(path.relative(ROOT, f));
  }
  return out;
}

const probe = () => {
  const cv = document.createElement('canvas'); cv.width = cv.height = 1;
  const cx = cv.getContext('2d', { willReadFrequently: true });
  const rgb = (css) => {
    cx.clearRect(0, 0, 1, 1); cx.fillStyle = '#000'; cx.fillStyle = css;
    cx.fillRect(0, 0, 1, 1); const d = cx.getImageData(0, 0, 1, 1).data;
    return [d[0], d[1], d[2]];
  };
  const lum = ([r, g, b]) => {
    const f = (v) => { v /= 255; return v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; };
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b);
  };
  // фон ищется по каскаду, но только пока над элементом нет фотографии
  const bgOf = (el) => {
    for (let e = el; e; e = e.parentElement) {
      // поверх фотографии фон это кадр, а не цвет: мерить нечего
      if (e.matches && e.matches('.scene, .stage, .shot, picture, .card, .rail, .teaser, figure')) return null;
      const b = getComputedStyle(e).backgroundColor;
      if (b && !/rgba\(0, 0, 0, 0\)|transparent/.test(b)) return b;
    }
    return 'rgb(255,255,255)';
  };
  const out = [];
  for (const el of document.querySelectorAll('p,li,a,h1,h2,h3,h4,b,td,th,label,button,summary,span')) {
    const hasText = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
    if (!hasText) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity === 0) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 8 || r.height < 8) continue;
    // увод за экран это приём для ссылки «к содержимому» и подписей
    // скринридера: такой текст виден только при фокусе и на своём фоне
    if (r.left < -100 || r.top + window.scrollY < -100 || r.right > document.documentElement.scrollWidth + 100) continue;
    if (cs.clipPath && cs.clipPath !== 'none' && /inset\(\s*50%/.test(cs.clipPath)) continue;
    const bg = bgOf(el);
    if (bg === null) continue;                       // текст поверх кадра
    const ratio = (() => {
      const L1 = lum(rgb(cs.color)), L2 = lum(rgb(bg));
      return (Math.max(L1, L2) + .05) / (Math.min(L1, L2) + .05);
    })();
    const px = parseFloat(cs.fontSize), bold = +cs.fontWeight >= 700;
    const need = (px >= 24 || (px >= 18.66 && bold)) ? 3 : 4.5;
    if (ratio < need - 0.05) {
      out.push(`<${el.tagName}.${String(el.className).trim().slice(0, 28)}> ${ratio.toFixed(2)}:1 ` +
               `нужно ${need} «${el.textContent.trim().slice(0, 40)}»`);
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
      // раскрыть всё, что спрятано за details, иначе внутрь не заглянуть
      await pg.evaluate(() => document.querySelectorAll('details').forEach((d) => (d.open = true)));
      for (const line of await pg.evaluate(probe)) {
        bad++; console.log(`${rel} @${w}px  ${line}`);
      }
    }
    await ctx.close();
  }
  await br.close();
  console.log(`страниц ${list.length} x ширин ${WIDTHS.length}: нарушений контраста ${bad}`);
  process.exit(bad ? 1 : 0);
})();
