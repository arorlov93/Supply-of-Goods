const fs = require('fs');
const path = require('path');
const D = require('/home/user/Supply-of-Goods/sourcing/concentrate/node_modules/docx');
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, BorderStyle, HeadingLevel,
  Table, TableRow, TableCell, WidthType, ShadingType,
} = D;

const BRAND = '2E4A62', GREY = '555555', ACCENT = 'B23A2E';
const P = (ch, o = {}) => new Paragraph({ children: ch, spacing: { after: 120, ...(o.spacing || {}) }, ...o });
const T = (t, o = {}) => new TextRun({ text: t, font: 'Calibri', size: 22, ...o });
const ph = (t) => new TextRun({ text: t, font: 'Calibri', size: 22, bold: true, color: ACCENT });
const H = (t) => new Paragraph({ spacing: { before: 220, after: 100 }, children: [new TextRun({ text: t, font: 'Calibri', bold: true, size: 26, color: BRAND })] });
const rule = () => new Paragraph({ spacing: { after: 160 }, border: { bottom: { color: 'CCCCCC', space: 1, style: BorderStyle.SINGLE, size: 6 } } });

function tbl(rowsArr, widths, head) {
  const cell = (txt, w, isHead, bold) => new TableCell({
    width: { size: w, type: WidthType.DXA },
    shading: isHead ? { type: ShadingType.CLEAR, fill: 'EDF1F5', color: 'auto' } : undefined,
    margins: { top: 50, bottom: 50, left: 90, right: 90 },
    children: [new Paragraph({ children: [new TextRun({ text: String(txt), font: 'Calibri', size: 20, bold: isHead || bold })] })],
  });
  return new Table({
    columnWidths: widths, width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    rows: rowsArr.map((r, i) => new TableRow({ children: r.map((c, j) => cell(c, widths[j], i === 0)) })),
  });
}

const kids = [];
// letterhead
kids.push(P([new TextRun({ text: 'ISP GROUP LLC', font: 'Calibri', size: 32, bold: true, color: BRAND })], { spacing: { after: 20 } }));
kids.push(P([new TextRun({ text: 'Painting · Drywall · Flooring · Post-Construction Cleaning — Subcontractor', font: 'Calibri', size: 20, color: GREY })], { spacing: { after: 20 } }));
kids.push(P([new TextRun({ text: '16395 Biscayne Blvd, Aventura, FL 33160  ·  info@ispgroupgc.com  ·  estimating@ispgroupgc.com', font: 'Calibri', size: 18, color: GREY })], { spacing: { after: 120 } }));
kids.push(rule());

// header block
kids.push(P([T('Date: '), ph('August 27, 2026')]));
kids.push(P([T('To: '), new TextRun({ text: 'Persons Services Corp.', bold: true, font: 'Calibri', size: 22 }), T('  —  Attn: Jermaine Goodman (jgoodman@personsservices.com)')]));
kids.push(P([T('1835 South Perimeter Road, Fort Lauderdale, FL 33309')]));
kids.push(P([T('Project: '), new TextRun({ text: 'Lincoln Road District Enhancement Project', bold: true, font: 'Calibri', size: 22 }), T(' — Lincoln Road, Miami Beach, FL 33139')]));
kids.push(P([T('Bid Due: '), new TextRun({ text: 'September 1, 2026', bold: true, font: 'Calibri', size: 22, color: ACCENT }), T('   |   Scopes: '), new TextRun({ text: 'Div. 9 Painting  &  Div. 9 Mosaic Tile Flooring', bold: true, font: 'Calibri', size: 22 })]));
kids.push(rule());

// cover
kids.push(P([T('Dear Mr. Goodman,')]));
kids.push(P([T('Thank you for the invitation to bid on the Lincoln Road District Enhancement Project. ISP Group LLC is pleased to submit its proposal for the '), new TextRun({ text: 'Division 9 Painting', bold: true, font: 'Calibri', size: 22 }), T(' and '), new TextRun({ text: 'Division 9 Mosaic Tile Flooring', bold: true, font: 'Calibri', size: 22 }), T(' scopes. We are a Florida-based finishing subcontractor and self-perform both trades. The signed Scope of Work Confirmation for each division is included below and will accompany our BuildingConnected submission.')]));
kids.push(P([T('We carry General Liability insurance and will name Persons Services Corp. as additional insured; a Certificate of Insurance and W-9 are available on request. We are prepared to meet the project schedule and coordinate with your superintendent.')]));

// scope confirmation - painting
kids.push(H('Scope of Work Confirmation — Div. 9 Painting'));
kids.push(P([T('ISP Group LLC has reviewed the Division 9 Painting scope, drawings, specifications, and all issued addenda for the Lincoln Road District Enhancement Project, and '), new TextRun({ text: 'confirms it will furnish all labor, material, equipment, surface preparation, priming, and finish coats', bold: true, font: 'Calibri', size: 22 }), T(' required to complete the painting scope in accordance with the contract documents, including:')]));
[
  'Surface preparation (cleaning, patching, sanding, masking, protection of adjacent surfaces).',
  'Primer and finish coating systems per the specified schedule and manufacturer (e.g., Sherwin-Williams / PPG or approved equal).',
  'Exterior/interior coatings as shown, including touch-up and final punch-list.',
  'Daily clean-up and removal of painting-related debris.',
].forEach((s) => kids.push(new Paragraph({ numbering: { reference: 'b', level: 0 }, spacing: { after: 60 }, children: [T(s)] })));
kids.push(P([new TextRun({ text: 'Clarifications / Exclusions: ', bold: true, font: 'Calibri', size: 22 }), T('Price excludes bonds (unless requested as a separate line), permit fees, and hazardous-material abatement. Quantities are as shown on plans; unit prices below govern for adds/deducts.')], { spacing: { before: 80 } }));

// pricing painting
kids.push(H('Pricing Worksheet — Painting (budgetary; unit prices include our margin)'));
kids.push(P([new TextRun({ text: 'Заполнить метраж из чертежей → умножить на юнит-прайс → получить лямп-сум.', italics: true, font: 'Calibri', size: 20, color: GREY })]));
kids.push(tbl([
  ['Item', 'Unit', 'Unit price', 'Qty (из чертежей)', 'Amount'],
  ['Exterior/interior painting (walls, ceilings, structures)', 'per SF', '$4.50', '__________ SF', '$__________'],
  ['High/prep areas, railings, specialty coatings', 'per SF', '$6.00', '__________ SF', '$__________'],
  ['Mobilization / minimum', 'LS', '$1,500', '1', '$1,500'],
  ['', '', '', 'PAINTING TOTAL →', '$__________'],
], [3400, 1000, 1300, 1800, 1600]));

// scope confirmation - tile
kids.push(H('Scope of Work Confirmation — Div. 9 Mosaic Tile Flooring'));
kids.push(P([T('ISP Group LLC has reviewed the Division 9 Tile / Mosaic Flooring scope, drawings, specifications, and all issued addenda, and '), new TextRun({ text: 'confirms it will furnish all labor, material, setting materials, and equipment', bold: true, font: 'Calibri', size: 22 }), T(' required to complete the mosaic tile flooring scope in accordance with the contract documents, including:')]));
[
  'Substrate preparation, crack-isolation / waterproof membrane, and mortar bed as specified.',
  'Furnish and install mosaic tile per pattern, layout, and finish schedule.',
  'Grouting, sealing, movement joints, transitions, and thresholds.',
  'Protection of finished floor and final cleaning of tiled areas.',
].forEach((s) => kids.push(new Paragraph({ numbering: { reference: 'b', level: 0 }, spacing: { after: 60 }, children: [T(s)] })));
kids.push(P([new TextRun({ text: 'Clarifications / Exclusions: ', bold: true, font: 'Calibri', size: 22 }), T('Tile material allowance to be confirmed against spec; premium/imported mosaic may adjust unit price. Excludes bonds (separate line), permit fees, and structural slab work.')], { spacing: { before: 80 } }));

// pricing tile
kids.push(H('Pricing Worksheet — Mosaic Tile Flooring (budgetary; unit prices include our margin)'));
kids.push(tbl([
  ['Item', 'Unit', 'Unit price', 'Qty (из чертежей)', 'Amount'],
  ['Mosaic tile floor — supply & install (standard mosaic)', 'per SF', '$16.00', '__________ SF', '$__________'],
  ['Membrane / substrate prep', 'per SF', '$3.50', '__________ SF', '$__________'],
  ['Premium/imported mosaic (if specified) — add', 'per SF', '$6.00', '__________ SF', '$__________'],
  ['Mobilization / minimum', 'LS', '$1,500', '1', '$1,500'],
  ['', '', '', 'TILE TOTAL →', '$__________'],
], [3400, 1000, 1300, 1800, 1600]));

// how to submit + checklist
kids.push(H('Перед подачей (чек-лист)'));
[
  '1) Скачать в BuildingConnected обе формы: «DIV.9 PAINTING SCOPE CONFIRMATION.pdf» и «DIV.9 TILE SCOPE CONFIRMATION.pdf».',
  '2) Перенести подтверждающий текст из этого файла на их формы, подписать (подпись + дата + компания + лицензия/EIN).',
  '3) Вытащить из чертежей метраж (SF) по покраске и по плитке → вписать в worksheet, посчитать TOTAL.',
  '4) Приложить COI (страховка) и W-9, если требуются.',
  '5) В BuildingConnected нажать «Bidding» → загрузить: (а) заполненные Scope Confirmation, (б) наш proposal с суммами.',
  '6) Дедлайн — 1 сентября 2026. Успеть до времени, указанного в RFP.',
].forEach((s) => kids.push(P([T(s)], { spacing: { after: 60 } })));

kids.push(P([new TextRun({ text: 'ВАЖНО (публичный проект Miami Beach): ', bold: true, color: ACCENT, font: 'Calibri', size: 22 }), T('уточни у GC — нужен ли bid bond / payment&performance bond, применяется ли prevailing wage (Davis-Bacon/местные ставки) и требования по опыту/референсам. Для новой компании это может потребовать со-подписанта по бонду или партнёра. Если бонды обязательны — заложим их отдельной строкой.')], { spacing: { before: 80 } }));

kids.push(P([T('Respectfully submitted,')], { spacing: { before: 200, after: 200 } }));
kids.push(P([new TextRun({ text: '____________________________', font: 'Calibri', size: 22 })]));
kids.push(P([new TextRun({ text: 'Aleksandr Orlov', bold: true, font: 'Calibri', size: 22 })], { spacing: { after: 10 } }));
kids.push(P([T('ISP Group LLC  ·  info@ispgroupgc.com  ·  estimating@ispgroupgc.com')]));

const doc = new Document({
  creator: 'ISP Group LLC',
  styles: { default: { document: { run: { font: 'Calibri', size: 22 } } } },
  numbering: { config: [{ reference: 'b', levels: [{ level: 0, format: 'bullet', text: '•', alignment: AlignmentType.START, style: { paragraph: { indent: { left: 460, hanging: 260 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1080, bottom: 1080, left: 1200, right: 1200 } } }, children: kids }],
});
Packer.toBuffer(doc).then((b) => {
  const out = path.join(__dirname, 'ISP-LincolnRoad-proposal-2026-08-27.docx');
  fs.writeFileSync(out, b);
  console.log('wrote', out);
});
