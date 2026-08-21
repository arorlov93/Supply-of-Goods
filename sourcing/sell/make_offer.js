const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, BorderStyle,
  Table, TableRow, TableCell, WidthType, ShadingType,
} = require('docx');

const BRAND = '2E4A62', GREY = '555555';
const p = (children, opts = {}) => new Paragraph({ children, spacing: { after: 150, ...(opts.spacing || {}) }, ...opts });
const t = (text, opts = {}) => new TextRun({ text, font: 'Calibri', size: 22, ...opts });
const ph = (text) => new TextRun({ text, font: 'Calibri', size: 22, color: BRAND, bold: true });
const rule = () => new Paragraph({ spacing: { after: 200 }, border: { bottom: { color: 'CCCCCC', space: 1, style: BorderStyle.SINGLE, size: 6 } } });

function specTable(headers, rows, colw) {
  const cell = (txt, w, head) => new TableCell({
    width: { size: w, type: WidthType.DXA },
    shading: head ? { type: ShadingType.CLEAR, fill: 'EDF1F5', color: 'auto' } : undefined,
    margins: { top: 40, bottom: 40, left: 80, right: 80 },
    children: [new Paragraph({ children: [new TextRun({ text: txt, font: 'Calibri', size: 18, bold: !!head })] })],
  });
  return new Table({
    columnWidths: colw, width: { size: colw.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    rows: [headers, ...rows].map((r, i) => new TableRow({ children: r.map((c, j) => cell(String(c), colw[j], i === 0)) })),
  });
}

const bullet = (lead, rest) => new Paragraph({
  numbering: { reference: 'o', level: 0 }, spacing: { after: 90 },
  children: [new TextRun({ text: lead, font: 'Calibri', size: 22, bold: true }), t(rest)],
});

function buildOffer({ subject, intro, table, availability, packing }) {
  return new Document({
    creator: 'ISP Group LLC',
    styles: { default: { document: { run: { font: 'Calibri', size: 22 } } } },
    numbering: { config: [{ reference: 'o', levels: [{ level: 0, format: 'decimal', text: '%1.', alignment: AlignmentType.START, style: { paragraph: { indent: { left: 460, hanging: 320 } } } }] }] },
    sections: [{
      properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1080, bottom: 1080, left: 1440, right: 1440 } } },
      children: [
        p([new TextRun({ text: 'ISP GROUP LLC', font: 'Calibri', size: 30, bold: true, color: BRAND })], { spacing: { after: 20 } }),
        p([new TextRun({ text: 'International Trading & Supply', font: 'Calibri', size: 20, color: GREY })], { spacing: { after: 20 } }),
        p([new TextRun({ text: '16395 Biscayne Blvd, Aventura, FL 33160, USA  ·  estimating@ispgroupgc.com', font: 'Calibri', size: 18, color: GREY })], { spacing: { after: 120 } }),
        rule(),
        p([t('Date: '), ph('[DD Month 2026]')]),
        p([t('To: '), ph('[Buyer / Company]'), t('   Attn: '), ph('[Name, title / Procurement]')]),
        p([new TextRun({ text: subject.pre, font: 'Calibri', size: 22, bold: true }), new TextRun({ text: subject.hi, font: 'Calibri', size: 22, bold: true, color: BRAND })], { spacing: { before: 120, after: 160 } }),
        p([t('Dear '), ph('[Name]'), t(',')]),
        p([t(intro)]),
        table,
        p([t('')], { spacing: { after: 40 } }),
        p([new TextRun({ text: 'Commercial outline:', font: 'Calibri', size: 22, bold: true })], { spacing: { after: 90 } }),
        bullet('Quantity. ', availability),
        bullet('Origin & packing. ', packing),
        bullet('Delivery. ', 'Incoterms 2020 — [FOB / CIF / CFR] [named port]; loading window [month/quarter].'),
        bullet('Inspection. ', 'Quality and weight determined at loadport by SGS / CIQ (or mutually agreed inspector); certificate of analysis and origin provided.'),
        bullet('Payment. ', 'Irrevocable LC at sight or [terms to agree]; we work against documentary settlement and do not request advance payment to personal accounts.'),
        bullet('Price. ', 'Firm price on request, indexed to prevailing market (' + subject.bench + '). Confirm destination port and monthly volume and we will issue a firm price and proforma within [24–48] hours.'),
        p([t('We can provide the latest SGS assay, samples on request, and company references under NCND. We are a reliable, repeat supplier and are ready to build a long-term offtake.')], { spacing: { before: 120 } }),
        p([t('Please advise your target destination, monthly requirement and preferred Incoterms, and reply to '), new TextRun({ text: 'estimating@ispgroupgc.com', font: 'Calibri', size: 22, bold: true }), t('. Thank you — we look forward to working with you.')]),
        p([t('Best regards,')], { spacing: { before: 180, after: 220 } }),
        p([new TextRun({ text: 'Trading Desk', font: 'Calibri', size: 22, bold: true })], { spacing: { after: 20 } }),
        p([t('ISP Group LLC')], { spacing: { after: 20 } }),
        p([t('estimating@ispgroupgc.com')]),
      ],
    }],
  });
}

// ---------- SULPHUR ----------
const sulphur = buildOffer({
  subject: { pre: 'OFFER — Granular Sulphur 99.99% (GOST 127.1-93), ', hi: '[tonnage] MT + [monthly] MT/month, [FOB/CIF] [port]', bench: 'e.g. Argus/CRU CFR China or FOB Middle East sulphur' },
  intro: 'ISP Group LLC is pleased to offer elemental sulphur (technical, high-purity) to the following specification (GOST 127.1-93):',
  table: specTable(
    ['Parameter', 'GOST 127.1-93 norm', 'Actual (typical)'],
    [
      ['Sulphur (S), % min', '99.98', '99.99'],
      ['Ash, % max', '0.02', '0.002'],
      ['Organic matter, % max', '0.01', '0.005'],
      ['Acidity as H₂SO₄, % max', '0.0015', '0.0002'],
      ['Moisture (water), % max', '0.2', '0.008'],
      ['Mechanical impurities', 'not permissible', 'none'],
    ],
    [3400, 2600, 2400]
  ),
  availability: '[spot tonnage] MT available now; monthly capacity up to [monthly] MT for recurring supply.',
  packing: 'Origin [country]. Form: granular / lump. Packing: [bulk / 1 MT jumbo bags / 50 kg bags]. Loading port [port].',
});

// ---------- FERROCHROME ----------
const feColw = [1450, 900, 1000, 900, 900, 900, 1300];
const ferro = buildOffer({
  subject: { pre: 'OFFER — Ferrochrome (HC & LC FeCr), ', hi: '[tonnage] MT + [monthly] MT/month, [FOB/CIF] [port]', bench: 'e.g. European benchmark US$/lb Cr or CIF China charge-chrome' },
  intro: 'ISP Group LLC is pleased to offer ferrochrome — High Carbon (HCFeCr) and Low Carbon (LCFeCr) — to the grades below. Priced on chromium content (US$/lb Cr), grade to buyer requirement:',
  table: specTable(
    ['Product', 'Cr %', 'Si %', 'C %', 'P %', 'S %', 'Size mm'],
    [
      ['HCFeCr', '65-67', '1.5 max', '6-8', '0.03', '0.05', '10-100'],
      ['HCFeCr', '64-65', '1-2', '6-8', '0.03', '0.05', '10-100'],
      ['HCFeCr', '62-64', '2', '6-8', '0.03', '0.05', '10-100'],
      ['HCFeCr', '60-62', '2-4', '6-8', '0.03', '0.05', '10-100'],
      ['HCFeCr', '55-60', '5 max', '8', '0.03', '0.05', '-10'],
      ['HCFeCr', '50-55', '5 max', '8', '0.03', '0.05', '-10'],
      ['LCFeCr', '60', '1', '0.1', '0.04', '0.04', '10-50'],
      ['LCFeCr', '65', '1', '0.1', '0.04', '0.04', '10-50'],
      ['LCFeCr', '65', '1', '0.05', '0.04', '0.04', '10-50'],
    ],
    feColw
  ),
  availability: '[spot tonnage] MT available; monthly capacity up to [monthly] MT. Grade/size to buyer specification.',
  packing: 'Origin [country]. Packing: [bulk / 1 MT big bags / steel drums]. Loading port [port].',
});

Promise.all([
  Packer.toBuffer(sulphur).then((b) => fs.writeFileSync('sulphur-offer.docx', b)),
  Packer.toBuffer(ferro).then((b) => fs.writeFileSync('ferrochrome-offer.docx', b)),
]).then(() => console.log('written both'));
