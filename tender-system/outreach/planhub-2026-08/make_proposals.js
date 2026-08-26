const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, BorderStyle, HeadingLevel,
  Table, TableRow, TableCell, WidthType, ShadingType,
} = require(path.join('/home/user/Supply-of-Goods/sourcing/concentrate/node_modules/docx'));

const BRAND = '2E4A62', GREY = '555555', ACCENT = 'B23A2E';
const P = (children, opts = {}) => new Paragraph({ children, spacing: { after: 120, ...(opts.spacing || {}) }, ...opts });
const T = (text, opts = {}) => new TextRun({ text, font: 'Calibri', size: 22, ...opts });
const mono = (text, opts = {}) => new TextRun({ text, font: 'Consolas', size: 20, ...opts });
const H = (text, lvl = HeadingLevel.HEADING_1) => new Paragraph({ heading: lvl, spacing: { before: 240, after: 120 }, children: [new TextRun({ text, font: 'Calibri', bold: true, color: BRAND })] });
const rule = () => new Paragraph({ spacing: { after: 160 }, border: { bottom: { color: 'CCCCCC', space: 1, style: BorderStyle.SINGLE, size: 6 } } });

// ---- paste-ready message block (monospace, boxed) ----
function msgBox(lines) {
  const cell = new TableCell({
    width: { size: 9600, type: WidthType.DXA },
    shading: { type: ShadingType.CLEAR, fill: 'F5F7FA', color: 'auto' },
    margins: { top: 120, bottom: 120, left: 160, right: 160 },
    children: lines.map((l) => new Paragraph({ spacing: { after: 60 }, children: [mono(l)] })),
  });
  return new Table({ columnWidths: [9600], width: { size: 9600, type: WidthType.DXA }, rows: [new TableRow({ children: [cell] })] });
}

// ---- master message text ----
const MASTER = (proj, gc, sf) => ([
  `Subject: Final / Post-Construction Cleaning — ${proj}`,
  ``,
  `Hello,`,
  ``,
  `Thank you for the invitation to bid on ${proj}. ISP Group LLC would like to`,
  `submit for the FINAL / POST-CONSTRUCTION CLEANING scope (rough clean,`,
  `final clean, interior/exterior window cleaning, and construction debris`,
  `haul-off) for this project${sf ? ` (~${sf} SF)` : ''}.`,
  ``,
  `We are a Florida-based cleaning & light-finishing subcontractor (Aventura,`,
  `FL). Cleaning is self-performed and requires no state license in Florida.`,
  `We carry General Liability insurance and can provide a Certificate of`,
  `Insurance naming ${gc} as additional insured before we set foot on site.`,
  ``,
  `Budget pricing for final/rough clean typically runs $0.28-$0.38 / SF`,
  `depending on finish level and phasing. We will hold a firm number the same`,
  `day you share the plans or the cleanable square footage and target turnover`,
  `date. We are flexible on scheduling and can phase to your punch-list.`,
  ``,
  `Could you share: (1) cleanable SF, (2) target turnover / substantial`,
  `completion date, (3) whether windows and exterior are in scope? I will`,
  `return a line-item quote right away.`,
  ``,
  `Best regards,`,
  `[Your name]`,
  `ISP Group LLC  ·  16395 Biscayne Blvd, Aventura, FL 33160`,
  `estimating@ispgroupgc.com  ·  info@ispgroupgc.com`,
]);

// ---- targets ----
const targets = [
  { proj: 'Logistics Warehouse & Office (Tenant Build-Out)', gc: 'Thatch Construction Group', city: 'Hialeah, FL 33018', due: '09/04/2026', sf: '53,456', scope: 'Final clean', est: '$15k-$20k' },
  { proj: 'Yeti Warehouse (Ground-Up)', gc: 'RE Crawford Construction', city: 'Palmetto, FL', due: 'см. PlanHub', sf: '45,200', scope: 'Final clean', est: '$13k-$17k' },
  { proj: "Chili's Port St Lucie (Ground-Up Restaurant)", gc: 'RE Crawford Construction', city: 'Port St Lucie, FL', due: 'см. PlanHub', sf: '5,760', scope: 'Final clean', est: '$1.6k-$2.2k' },
  { proj: 'LivSmart & WSS (2 hotels)', gc: 'Path Construction', city: 'Ellenton, FL', due: 'см. PlanHub', sf: '2 bldgs', scope: 'Final clean (hotels — heavy)', est: 'по SF' },
  { proj: 'Gaines Park Aquatic Center Renovations (City of WPB)', gc: 'West Construction, Inc.', city: 'West Palm Beach, FL', due: 'см. PlanHub', sf: '—', scope: 'Final clean + paint', est: 'по SF' },
  { proj: 'Southshore Sportsplex — Phase 2', gc: 'Kingdom Construction', city: 'Apollo Beach, FL', due: 'см. PlanHub', sf: '—', scope: 'Final clean', est: 'по SF' },
  { proj: 'Collier Senior Center Expansion (26-8672)', gc: 'Nujack Companies', city: 'Naples, FL', due: 'см. PlanHub', sf: '2,710+7,120', scope: 'Final clean + paint', est: 'по SF' },
  { proj: 'Flamingo Park Baseball Field Facilities Reno (RE-BID)', gc: 'LEGO Construction Co.', city: 'Miami Beach, FL', due: 'см. PlanHub', sf: '49,577', scope: 'Final clean', est: '$14k-$18k' },
  { proj: 'EcoSteris Central FL Treatment Facility', gc: 'The Highland Group, LLC', city: 'Wauchula, FL', due: 'см. PlanHub', sf: '35,316', scope: 'Final clean', est: '$10k-$13k' },
  { proj: 'Chloe — Royal Poinciana Plaza #M313B (retail remodel)', gc: 'Sullivan Construction', city: 'Palm Beach, FL', due: '~27.08 (1 день)', sf: '1,894', scope: 'Final clean + demo/paint prep', est: 'по SF' },
  { proj: 'Glades Road Library Creation Station Reno', gc: 'Innovative Interiors, Inc', city: 'Boca Raton, FL', due: 'см. PlanHub', sf: '240', scope: 'Final clean + paint/floor', est: 'мелкий — $0.35/SF' },
  { proj: 'AutoZone #9300 (Ground-Up) — несколько GC бидят', gc: 'Hanna Design / MEC / Triad / P&C', city: 'Nokomis/Osprey, FL', due: 'см. PlanHub', sf: '~6,400', scope: 'Final clean + EIFS/paint/floor', est: 'по SF' },
];

const children = [];
children.push(new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text: 'ISP GROUP LLC', font: 'Calibri', size: 30, bold: true, color: BRAND })] }));
children.push(new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text: 'PlanHub / BuildingConnected — предложения к отправке (26.08.2026)', font: 'Calibri', size: 22, color: GREY })] }));
children.push(rule());

// How to submit
children.push(H('Как отправить предложение в PlanHub (3 шага)'));
[
  '1. Открой письмо ITB → кнопка «View Project» (или войди на app.planhub.com). После входа откроется страница проекта и контакт GC.',
  '2. Нажми «Intend to Bid» (в письме или в портале) — это переводит тебя в список бидеров, и GC видит, что ты в игре.',
  '3. В проекте есть поле сообщения GC / загрузка квоты — вставь текст из этого файла (мастер-шаблон или готовый под проект), заполни [имя] и цифры. Прикрепи COI/W-9 если просят.',
].forEach((s) => children.push(P([T(s)])));
children.push(P([T('BuildingConnected (напр. KITH ROM) — там контакт эстиматора в письме, можно ответить прямым email (см. §4).', { italics: true, color: GREY })]));

// Master template
children.push(H('§1. Мастер-шаблон (вставляй в любой проект, меняй [проект]/[GC]/SF)'));
children.push(P([T('Один универсальный текст под final clean. Меняй название проекта, GC и метраж — остальное готово.')]));
children.push(msgBox(MASTER('[PROJECT NAME]', '[GC NAME]', '[SF]')));

// Per-target
children.push(H('§2. Готовые предложения по проектам (топ-12 FL)'));
children.push(P([T('По каждому: заголовок с данными проекта + готовый текст. Дедлайн уточняй в PlanHub при клике.')]));
targets.forEach((tg, i) => {
  children.push(new Paragraph({ spacing: { before: 200, after: 40 }, children: [new TextRun({ text: `${i + 1}. ${tg.proj}`, font: 'Calibri', size: 24, bold: true, color: ACCENT })] }));
  children.push(P([
    new TextRun({ text: 'GC: ', font: 'Calibri', size: 20, bold: true }), T(tg.gc + '   ', { size: 20 }),
    new TextRun({ text: 'Город: ', font: 'Calibri', size: 20, bold: true }), T(tg.city + '   ', { size: 20 }),
    new TextRun({ text: 'Дедлайн: ', font: 'Calibri', size: 20, bold: true }), T(tg.due + '   ', { size: 20 }),
    new TextRun({ text: 'SF: ', font: 'Calibri', size: 20, bold: true }), T(tg.sf + '   ', { size: 20 }),
    new TextRun({ text: 'Наш scope: ', font: 'Calibri', size: 20, bold: true }), T(tg.scope + '   ', { size: 20 }),
    new TextRun({ text: 'Оценка: ', font: 'Calibri', size: 20, bold: true }), T(tg.est, { size: 20 }),
  ]));
  children.push(msgBox(MASTER(tg.proj, tg.gc, tg.sf.match(/\d/) ? tg.sf : '')));
});

// Direct email
children.push(H('§3. Прямой email (BuildingConnected) — KITH ROM: Venetian Plaster'));
children.push(P([
  new TextRun({ text: 'Кому: ', bold: true, font: 'Calibri', size: 22 }), T('Antonio Favasoli — antonio@downsmcgovern.com   '),
  new TextRun({ text: 'Тел: ', bold: true, font: 'Calibri', size: 22 }), T('+1 438-238-1960 x215   '),
  new TextRun({ text: 'Проект: ', bold: true, font: 'Calibri', size: 22 }), T('1931 Collins Ave, Miami Beach   '),
  new TextRun({ text: 'Bid due: ', bold: true, font: 'Calibri', size: 22 }), T('09/09/2026'),
]));
children.push(P([T('⚠️ Venetian plaster — специализированная отделка. Для новой компании бери ТОЛЬКО если найдёшь плаща-мастера/партнёра. Иначе предложи по этому же GC final clean (ниже — вариант письма это учитывает).', { color: ACCENT })]));
children.push(msgBox([
  `To: antonio@downsmcgovern.com`,
  `Subject: KITH ROM — Venetian Plaster / Final Clean (ISP Group LLC)`,
  ``,
  `Hi Antonio,`,
  ``,
  `Thank you for the budget-pricing request on KITH ROM (1931 Collins Ave,`,
  `Miami Beach). ISP Group LLC is a Florida finishing & cleaning subcontractor.`,
  ``,
  `We can support this project two ways — please tell me which is useful:`,
  `  1) Venetian / decorative plaster finish — we quote per plans and the`,
  `     specified system (Veneziano / Marmorino). Send the finish schedule and`,
  `     wall SF and I will return budget pricing.`,
  `  2) Final / post-construction cleaning for the space at turnover`,
  `     ($0.28-$0.38/SF), if a cleaning sub is still open.`,
  ``,
  `We are insured (COI on request, GC named additional insured) and based`,
  `minutes away in Aventura. Happy to walk the space this week.`,
  ``,
  `Best regards,`,
  `[Your name]`,
  `ISP Group LLC  ·  estimating@ispgroupgc.com  ·  info@ispgroupgc.com`,
]));

// Tracker note
children.push(H('§4. Дальше'));
[
  'Приоритет по дедлайну: сначала Chloe (Royal Poinciana, ~27.08) и Thatch (04.09), потом остальные.',
  'На каждый — «Intend to Bid» в PlanHub, вставь текст, попроси у GC метраж/дату сдачи → пришлёшь твёрдую цену.',
  'Dade Construction Corp. прислал ~8 ITB — им отдельно предложи рамочно final clean на все их объекты (одно письмо = отношения с активным GC).',
].forEach((s) => children.push(P([T(s)])));

const doc = new Document({
  creator: 'ISP Group LLC',
  styles: { default: { document: { run: { font: 'Calibri', size: 22 } } } },
  sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1080, bottom: 1080, left: 1200, right: 1200 } } }, children }],
});
Packer.toBuffer(doc).then((b) => {
  const out = path.join('/home/user/Supply-of-Goods/tender-system/outreach/planhub-2026-08/planhub-proposals-2026-08-26.docx');
  fs.writeFileSync(out, b);
  console.log('wrote', out, '·', targets.length, 'targets');
});
