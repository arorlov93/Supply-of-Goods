/* Поисковая техничка: карта сайта, канонические адреса, языковые связи.
 *
 * Эти вещи не видно глазом и они не ломают страницу, поэтому ломаются
 * тихо и живут годами. Проверяется то, что поисковик действительно
 * читает:
 *
 *   карта сайта    все ли страницы в ней и все ли адреса из неё живы
 *   canonical      совпадает ли с настоящим адресом страницы
 *   hreflang       взаимны ли ссылки между языками
 *   robots         не закрыта ли страница от обхода случайно
 *   структура      разбирается ли разметка данных
 *
 * Запуск: node tools/seo-check.js [адрес]
 */
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const BASE = (process.argv[2] || "https://ispgroupgc.com").replace(/\/$/, "");
const SITE = path.join(__dirname, "..", "site");
const bad = [];
const say = (what) => bad.push(what);

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext();
  const pg = await ctx.newPage();

  // --- карта сайта
  const smRes = await pg.request.get(BASE + "/sitemap.xml");
  if (!smRes.ok()) say("карта сайта не отдаётся: " + smRes.status());
  const sm = smRes.ok() ? await smRes.text() : "";
  const urls = [...sm.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
  console.log("адресов в карте сайта:", urls.length);

  const files = fs
    .readdirSync(SITE)
    .filter((f) => f.endsWith(".html") && !["crm.html", "404.html", "home-classic.html"].includes(f))
    .map((f) => BASE + "/" + f.replace(/\.html$/, "").replace(/^index$/, ""));

  for (const f of files) {
    const want = f.endsWith("/") ? f : f;
    if (!urls.some((u) => u.replace(/\/$/, "") === want.replace(/\/$/, ""))) {
      say("страницы нет в карте сайта: " + want.replace(BASE, ""));
    }
  }

  // --- каждый адрес из карты должен открываться без переадресации
  for (const u of urls) {
    const r = await pg.request.get(u, { maxRedirects: 0 }).catch(() => null);
    if (!r) say("адрес из карты не открылся: " + u.replace(BASE, ""));
    else if (r.status() !== 200) say(`адрес из карты отвечает ${r.status()}: ${u.replace(BASE, "")}`);
  }

  // --- страницы по одной
  const robots = await (await pg.request.get(BASE + "/robots.txt")).text();
  if (!/Sitemap:/i.test(robots)) say("в robots.txt нет ссылки на карту сайта");

  const langs = {};
  for (const u of urls.slice(0, 60)) {
    const r = await pg.goto(u, { waitUntil: "domcontentloaded" }).catch(() => null);
    if (!r) continue;
    const d = await pg.evaluate(() => ({
      canonical: (document.querySelector('link[rel="canonical"]') || {}).href || "",
      robots: (document.querySelector('meta[name="robots"]') || {}).content || "",
      alts: [...document.querySelectorAll('link[rel="alternate"][hreflang]')].map((l) => [
        l.getAttribute("hreflang"),
        l.href,
      ]),
      jsonld: [...document.querySelectorAll('script[type="application/ld+json"]')].map((s) => s.textContent),
      title: document.title,
    }));
    const here = pg.url().replace(/\/$/, "");
    if (!d.canonical) say("нет canonical: " + u.replace(BASE, ""));
    else if (d.canonical.replace(/\/$/, "") !== here) {
      say(`canonical не совпадает с адресом: ${u.replace(BASE, "")} -> ${d.canonical.replace(BASE, "")}`);
    }
    if (/noindex/i.test(d.robots)) say("страница закрыта от индексации: " + u.replace(BASE, ""));
    d.jsonld.forEach((s, i) => {
      try {
        JSON.parse(s);
      } catch (e) {
        say(`разметка данных ${i} не разбирается на ${u.replace(BASE, "")}`);
      }
    });
    if (d.alts.length) langs[here] = d.alts;
  }

  // --- взаимность языковых связей
  for (const [from, alts] of Object.entries(langs)) {
    for (const [code, to] of alts) {
      if (code === "x-default") continue;
      const back = langs[to.replace(/\/$/, "")];
      if (!back) {
        say(`языковая связь в одну сторону: ${from.replace(BASE, "")} -> ${to.replace(BASE, "")}`);
        continue;
      }
      if (!back.some(([, u]) => u.replace(/\/$/, "") === from)) {
        say(`нет обратной языковой связи: ${to.replace(BASE, "")} не ссылается на ${from.replace(BASE, "")}`);
      }
    }
  }

  await browser.close();
  console.log("замечаний:", bad.length);
  bad.slice(0, 40).forEach((b) => console.log("  ", b));
})();
