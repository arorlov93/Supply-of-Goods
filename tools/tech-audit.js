/* Сплошная техническая проверка сайта.
 *
 * Смысл не в том, чтобы получить красивую оценку чужого сервиса, а в том,
 * чтобы каждый дефект был назван файлом и строкой и его можно было
 * починить. Поэтому проверки измеряют, а не угадывают:
 *
 *   ссылки      каждая внутренняя ссылка запрашивается, смотрим код ответа
 *   картинки    сравниваем натуральный размер с отрисованным при DPR 2
 *   разметка    повторяющиеся id, пустой alt, порядок заголовков, lang
 *   мета        длина title и description, их уникальность, canonical
 *   доступность поля без подписи, кнопки без имени, мелкие цели нажатия
 *   скорость    вес страницы, LCP, сдвиг макета
 *
 * Запуск:  node tools/tech-audit.js [адрес]
 * По умолчанию проверяется живой сайт.
 */
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const BASE = (process.argv[2] || "https://ispgroupgc.com").replace(/\/$/, "");
const SITE = path.join(__dirname, "..", "site");

const pages = fs
  .readdirSync(SITE)
  .filter((f) => f.endsWith(".html") && f !== "crm.html")
  .map((f) => "/" + f.replace(/\.html$/, "").replace(/^index$/, ""))
  .concat(["/fr/", "/es/", "/de/"]);

const problems = [];
const add = (page, kind, detail) => problems.push({ page, kind, detail });

(async () => {
  const browser = await chromium.launch();
  const linkStatus = new Map();
  const titles = new Map();
  const descs = new Map();
  let totalBytes = 0;

  for (const p of pages) {
    const ctx = await browser.newContext({
      viewport: { width: 1440, height: 900 },
      deviceScaleFactor: 2,
    });
    const pg = await ctx.newPage();

    let bytes = 0;
    const failed = [];
    pg.on("response", async (r) => {
      const len = Number(r.headers()["content-length"] || 0);
      bytes += len;
      if (r.status() >= 400) failed.push(r.status() + " " + r.url().replace(BASE, ""));
    });
    pg.on("console", (m) => {
      if (m.type() === "error") add(p, "js", m.text().slice(0, 150));
    });
    pg.on("pageerror", (e) => add(p, "js", String(e.message).slice(0, 150)));

    const resp = await pg.goto(BASE + p, { waitUntil: "networkidle" }).catch(() => null);
    if (!resp) {
      add(p, "страница", "не открылась");
      await ctx.close();
      continue;
    }
    if (resp.status() !== 200) add(p, "страница", "код ответа " + resp.status());

    // ленивые картинки до замера надо заставить загрузиться
    await pg.evaluate(() =>
      document.querySelectorAll('img[loading="lazy"]').forEach((i) => (i.loading = "eager"))
    );
    await pg.waitForTimeout(700);

    const data = await pg.evaluate(() => {
      const out = {
        ids: {}, imgs: [], links: [], labels: 0, nameless: 0, small: [],
        title: document.title || "",
        desc: (document.querySelector('meta[name="description"]') || {}).content || "",
        canonical: (document.querySelector('link[rel="canonical"]') || {}).href || "",
        lang: document.documentElement.lang || "",
        h1: document.querySelectorAll("h1").length,
        headings: [...document.querySelectorAll("h1,h2,h3,h4")].map((h) => +h.tagName[1]),
        viewport: !!document.querySelector('meta[name="viewport"]'),
        jsonld: [...document.querySelectorAll('script[type="application/ld+json"]')].map(
          (s) => s.textContent
        ),
      };
      document.querySelectorAll("[id]").forEach((e) => {
        out.ids[e.id] = (out.ids[e.id] || 0) + 1;
      });
      document.querySelectorAll("img").forEach((i) => {
        const r = i.getBoundingClientRect();
        out.imgs.push({
          src: (i.currentSrc || i.src || "").split("/").pop(),
          nat: [i.naturalWidth, i.naturalHeight],
          box: [Math.round(r.width), Math.round(r.height)],
          alt: i.alt,
          hasAlt: i.hasAttribute("alt"),
          dims: !!(i.getAttribute("width") && i.getAttribute("height")),
        });
      });
      document.querySelectorAll("a[href]").forEach((a) => {
        const h = a.getAttribute("href");
        if (!h || h.startsWith("#") || h.startsWith("mailto:") || h.startsWith("tel:")) return;
        out.links.push(new URL(h, location.href).href);
        if (!(a.textContent || "").trim() && !a.getAttribute("aria-label")) out.nameless++;
      });
      document.querySelectorAll("input, select, textarea").forEach((f) => {
        if (f.type === "hidden") return;
        const ok =
          (f.id && document.querySelector(`label[for="${CSS.escape(f.id)}"]`)) ||
          f.closest("label") ||
          f.getAttribute("aria-label") ||
          f.getAttribute("aria-labelledby");
        if (!ok) out.labels++;
      });
      document.querySelectorAll("a, button, input, select").forEach((e) => {
        const r = e.getBoundingClientRect();
        if (r.width === 0 || r.height === 0) return;
        if (r.height < 24 || r.width < 24)
          out.small.push(((e.textContent || e.tagName).trim() || e.tagName).slice(0, 22) +
            ` ${Math.round(r.width)}x${Math.round(r.height)}`);
      });
      return out;
    });

    const vitals = await pg.evaluate(
      () =>
        new Promise((res) => {
          let lcp = 0, cls = 0;
          try {
            new PerformanceObserver((l) => {
              for (const e of l.getEntries()) lcp = Math.max(lcp, e.startTime);
            }).observe({ type: "largest-contentful-paint", buffered: true });
            new PerformanceObserver((l) => {
              for (const e of l.getEntries()) if (!e.hadRecentInput) cls += e.value;
            }).observe({ type: "layout-shift", buffered: true });
          } catch {}
          setTimeout(() => res({ lcp: Math.round(lcp), cls: +cls.toFixed(3) }), 900);
        })
    );

    totalBytes += bytes;
    failed.forEach((f) => add(p, "ресурс", f));

    // --- разметка
    Object.entries(data.ids).forEach(([id, n]) => {
      if (n > 1) add(p, "разметка", `id "${id}" встречается ${n} раза`);
    });
    if (!data.lang) add(p, "разметка", "нет lang у <html>");
    if (!data.viewport) add(p, "разметка", "нет meta viewport");
    if (data.h1 !== 1) add(p, "разметка", `заголовков h1: ${data.h1}`);
    let prev = 0;
    data.headings.forEach((lvl) => {
      if (prev && lvl > prev + 1) add(p, "разметка", `скачок заголовков h${prev} -> h${lvl}`);
      prev = lvl;
    });

    // --- мета
    if (!data.title) add(p, "мета", "нет title");
    else if (data.title.length > 65) add(p, "мета", `title ${data.title.length} знаков`);
    if (!data.desc) add(p, "мета", "нет description");
    else if (data.desc.length > 160) add(p, "мета", `description ${data.desc.length} знаков`);
    else if (data.desc.length < 70) add(p, "мета", `description всего ${data.desc.length} знаков`);
    if (!data.canonical) add(p, "мета", "нет canonical");
    if (titles.has(data.title)) add(p, "мета", `title повторяет ${titles.get(data.title)}`);
    else titles.set(data.title, p);
    if (data.desc && descs.has(data.desc)) add(p, "мета", `description повторяет ${descs.get(data.desc)}`);
    else if (data.desc) descs.set(data.desc, p);
    data.jsonld.forEach((s, i) => {
      try {
        JSON.parse(s);
      } catch (e) {
        add(p, "мета", `разметка данных ${i} не разбирается: ${String(e.message).slice(0, 60)}`);
      }
    });

    // --- картинки
    data.imgs.forEach((i) => {
      if (!i.hasAlt) add(p, "картинка", `${i.src}: нет alt`);
      if (!i.dims) add(p, "картинка", `${i.src}: нет width/height, это сдвиг макета`);
      if (i.box[0] && i.nat[0]) {
        const k = (i.box[0] * 2) / i.nat[0];
        if (k > 1.15) add(p, "картинка", `${i.src}: растянута в ${k.toFixed(2)} раза при DPR 2`);
      }
      if (i.nat[0] === 0) add(p, "картинка", `${i.src}: не загрузилась`);
    });

    // --- доступность
    if (data.labels) add(p, "доступность", `полей без подписи: ${data.labels}`);
    if (data.nameless) add(p, "доступность", `ссылок без текста: ${data.nameless}`);
    [...new Set(data.small)].forEach((s) => add(p, "доступность", `мелкая цель нажатия: ${s}`));

    // --- скорость
    if (vitals.lcp > 2500) add(p, "скорость", `LCP ${vitals.lcp} мс`);
    if (vitals.cls > 0.1) add(p, "скорость", `сдвиг макета ${vitals.cls}`);
    if (bytes > 2_000_000) add(p, "скорость", `вес ${(bytes / 1048576).toFixed(2)} МБ`);

    for (const l of data.links) if (l.startsWith(BASE)) linkStatus.set(l, null);

    await ctx.close();
  }

  // --- ссылки проверяем один раз на адрес, а не на каждое вхождение
  const ctx = await browser.newContext();
  const pg = await ctx.newPage();
  for (const url of linkStatus.keys()) {
    const r = await pg.request.get(url).catch(() => null);
    const st = r ? r.status() : 0;
    linkStatus.set(url, st);
    if (st >= 400 || st === 0) add("(ссылки)", "ссылка", `${st} ${url.replace(BASE, "")}`);
  }
  await browser.close();

  const byKind = {};
  problems.forEach((p) => (byKind[p.kind] = (byKind[p.kind] || 0) + 1));
  console.log("страниц проверено:", pages.length, "| ссылок:", linkStatus.size);
  console.log("найдено замечаний:", problems.length);
  Object.entries(byKind)
    .sort((a, b) => b[1] - a[1])
    .forEach(([k, n]) => console.log(`   ${k.padEnd(14)} ${n}`));
  fs.writeFileSync(
    path.join(__dirname, "..", "audit-tech.json"),
    JSON.stringify({ base: BASE, when: new Date().toISOString(), problems }, null, 1)
  );
  console.log("подробности: audit-tech.json");
})();
