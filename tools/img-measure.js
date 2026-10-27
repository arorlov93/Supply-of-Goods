/* Замеряет, какой ширины на самом деле показывается каждый снимок.
 *
 * Без этого адаптивный набор не собрать: нужно знать не «какой файл у нас
 * есть», а «сколько точек он занимает на телефоне, на планшете и на
 * большом экране». Разница между этими числами и есть лишний вес.
 *
 * Берётся наибольшая ширина по всем страницам: один и тот же снимок
 * где-то стоит карточкой, где-то во весь экран, и набор должен покрывать
 * худший случай.
 *
 * Результат кладётся в img-sizes.json и дальше используется tools/img-srcset.py.
 *
 * Запуск: node tools/img-measure.js [адрес]
 */
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const BASE = (process.argv[2] || "https://ispgroupgc.com").replace(/\/$/, "");
const SITE = path.join(__dirname, "..", "site");
const WIDTHS = [390, 768, 1440];

const pages = fs
  .readdirSync(SITE)
  .filter((f) => f.endsWith(".html") && f !== "crm.html")
  .map((f) => "/" + f.replace(/\.html$/, "").replace(/^index$/, ""));

(async () => {
  const browser = await chromium.launch();
  const data = {}; // файл -> { "390": макс ширина, ... }

  for (const vw of WIDTHS) {
    const ctx = await browser.newContext({ viewport: { width: vw, height: 900 } });
    const pg = await ctx.newPage();
    for (const p of pages) {
      const r = await pg.goto(BASE + p, { waitUntil: "domcontentloaded" }).catch(() => null);
      if (!r) continue;
      await pg.evaluate(() =>
        document.querySelectorAll('img[loading="lazy"]').forEach((i) => (i.loading = "eager"))
      );
      await pg.waitForTimeout(450);
      const got = await pg.evaluate(() =>
        [...document.querySelectorAll("img")]
          .map((i) => {
            const pic = i.closest("picture");
            const src = pic && pic.querySelector("source[type='image/webp']");
            const name = ((src && src.getAttribute("srcset")) || i.getAttribute("src") || "")
              .split(/[ ,]/)[0]
              .split("/")
              .pop();
            return { name, w: Math.round(i.getBoundingClientRect().width) };
          })
          .filter((x) => x.name && x.w > 0)
      );
      for (const g of got) {
        data[g.name] = data[g.name] || {};
        data[g.name][vw] = Math.max(data[g.name][vw] || 0, g.w);
      }
    }
    await ctx.close();
    console.log("ширина окна", vw, "пройдена");
  }
  await browser.close();

  fs.writeFileSync(path.join(__dirname, "..", "img-sizes.json"), JSON.stringify(data, null, 1));
  console.log("снимков замерено:", Object.keys(data).length, "-> img-sizes.json");
})();
