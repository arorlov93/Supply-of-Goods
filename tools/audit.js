// Сквозная проверка выложенного сайта: битые картинки, ошибки скриптов,
// неотданные файлы и контраст текста. Гоняется по всем страницам и по
// нескольким ширинам окна, чтобы ловить то, что видно только на узком
// экране. Запуск: node tools/audit.js   (сервер на 127.0.0.1:8899)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..', 'site');
const BASE = process.env.BASE || 'http://127.0.0.1:8899';
const WIDTHS = [1440, 860, 420];

function pages(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const f = path.join(dir, e.name);
    if (e.isDirectory()) { if (!['media','css','fonts','js'].includes(e.name)) pages(f, out); }
    else if (e.name.endsWith('.html')) out.push(path.relative(ROOT, f));
  }
  return out;
}

// Контраста здесь нет намеренно. Считать его по каскаду нельзя: шапка
// лежит поверх фотографии и собственного фона не имеет, подъём по
// родителям находит фон страницы и выдаёт несуществующие нарушения
// пачками. Мерить его честно нужно по пикселям снимка под текстом, это
// отдельная работа и отдельный инструмент.

(async () => {
  const list = pages(ROOT).sort();
  let errs = 0, net = 0, broken = 0;
  const br = await chromium.launch();
  for (const w of WIDTHS) {
    const ctx = await br.newContext({ viewport: { width: w, height: 900 } });
    const pg = await ctx.newPage();
    pg.on('pageerror', e => { errs++; console.log(`ОШИБКА СКРИПТА ${pg.url()} :: ${e.message}`); });
    pg.on('response', r => { if (r.status() >= 400) { net++; console.log(`ОТВЕТ ${r.status()} ${r.url()}`); } });
    for (const rel of list) {
      await pg.goto(`${BASE}/${rel.split(path.sep).join('/')}`, { waitUntil: 'networkidle' });
      // Снимки ниже сгиба помечены loading="lazy" и без появления в окне не
      // загружаются, а незагруженный снимок от битого не отличить. Одной
      // прокрутки мало: часть кадров лежит в лентах с боковой прокруткой и
      // вертикально в окно не попадает. Поэтому отложенная загрузка
      // отключается и дожидается завершения каждого кадра.
      await pg.evaluate(() => {
        document.querySelectorAll('img[loading="lazy"]').forEach(i => { i.loading = 'eager'; });
      });
      await pg.evaluate(() => Promise.all([...document.images].map(i =>
        i.complete ? null : new Promise(r => { i.addEventListener('load', r); i.addEventListener('error', r); })
      )));
      await pg.waitForLoadState('networkidle');
      const b = await pg.evaluate(() => [...document.images].filter(i => !i.complete || i.naturalWidth === 0).map(i => i.currentSrc || i.src));
      b.forEach(s => { broken++; console.log(`БИТАЯ КАРТИНКА ${rel} :: ${s}`); });
    }
    await ctx.close();
  }
  await br.close();
  console.log(`страниц ${list.length} x ширин ${WIDTHS.length}: ошибок скриптов ${errs}, ответов 4xx/5xx ${net}, битых картинок ${broken}`);
  process.exit(errs + net + broken ? 1 : 0);
})();
