const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, BorderStyle,
  Table, TableRow, TableCell, WidthType, ShadingType,
} = require('docx');

const BRAND = '2E4A62';
const GREY = '555555';
const p = (children, opts = {}) => new Paragraph({ children, spacing: { after: 150, ...(opts.spacing || {}) }, ...opts });
const t = (text, opts = {}) => new TextRun({ text, font: 'Calibri', size: 22, ...opts });
const ph = (text) => new TextRun({ text, font: 'Calibri', size: 22, color: BRAND, bold: true });
const rule = () => new Paragraph({ spacing: { after: 200 }, border: { bottom: { color: 'CCCCCC', space: 1, style: BorderStyle.SINGLE, size: 6 } } });

// assay table
const cell = (txt, opts = {}) => new TableCell({
  width: { size: opts.w, type: WidthType.DXA },
  shading: opts.head ? { type: ShadingType.CLEAR, fill: 'EDF1F5', color: 'auto' } : undefined,
  margins: { top: 40, bottom: 40, left: 90, right: 90 },
  children: [new Paragraph({ children: [new TextRun({ text: txt, font: 'Calibri', size: 20, bold: !!opts.head })] })],
});
const assayRows = [
  ['Element', 'Typical', 'Element', 'Typical'],
  ['Cu', '18.0–28.0% (min 16%)', 'Pb', '< 0.15%'],
  ['Au', '0.8 g/t', 'Zn', '0.2%'],
  ['Ag', '70 g/t', 'Sb', '< 0.003%'],
  ['As', '< 0.03%', 'Fe', '28%'],
  ['S', '32%', 'SiO₂', '6.3%'],
  ['Co', '0.015%', 'Moisture', '≤ 10%'],
];
const COLW = [1550, 2450, 1550, 2450];
const assayTable = new Table({
  columnWidths: COLW,
  width: { size: 8000, type: WidthType.DXA },
  rows: assayRows.map((r, i) => new TableRow({
    children: r.map((c, j) => cell(c, { w: COLW[j], head: i === 0 })),
  })),
});

const bullet = (lead, rest) => new Paragraph({
  numbering: { reference: 'q', level: 0 }, spacing: { after: 90 },
  children: [new TextRun({ text: lead, font: 'Calibri', size: 22, bold: true }), t(rest)],
});

const doc = new Document({
  creator: 'ISP Group LLC',
  styles: { default: { document: { run: { font: 'Calibri', size: 22 } } } },
  numbering: { config: [{ reference: 'q', levels: [{ level: 0, format: 'decimal', text: '%1.', alignment: AlignmentType.START, style: { paragraph: { indent: { left: 460, hanging: 320 } } } }] }] },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1080, bottom: 1080, left: 1440, right: 1440 } } },
    children: [
      p([new TextRun({ text: 'ISP GROUP LLC', font: 'Calibri', size: 30, bold: true, color: BRAND })], { spacing: { after: 20 } }),
      p([new TextRun({ text: 'International Trading & Supply', font: 'Calibri', size: 20, color: GREY })], { spacing: { after: 20 } }),
      p([new TextRun({ text: '16395 Biscayne Blvd, Aventura, FL 33160, USA  ·  estimating@ispgroupgc.com', font: 'Calibri', size: 18, color: GREY })], { spacing: { after: 120 } }),
      rule(),

      p([t('Date: '), ph('[DD Month 2026]')]),
      p([t('To: '), ph('[Seller / Trader / Company]'), t('   Attn: '), ph('[Name, title]')]),

      p([new TextRun({ text: 'RFQ — Copper Concentrate (Cu 18–28%, silver-bearing), ', font: 'Calibri', size: 22, bold: true }), new TextRun({ text: '[tonnage] MT', font: 'Calibri', size: 22, bold: true, color: BRAND }), new TextRun({ text: ', ', font: 'Calibri', size: 22, bold: true }), new TextRun({ text: '[CIF/FOB] [port]', font: 'Calibri', size: 22, bold: true, color: BRAND })], { spacing: { before: 120, after: 160 } }),

      p([t('Dear '), ph('[Name]'), t(',')]),
      p([t('ISP Group LLC is a ready buyer for copper concentrate. We are seeking a firm offer for material to the following typical specification, and would move quickly on competitive terms:')]),
      assayTable,
      p([t('')], { spacing: { after: 40 } }),
      p([t('Quantity: '), ph('[tonnage] MT'), t(' as a first / trial lot, with intended recurring offtake of '), ph('[monthly tonnage] MT'), t(' per month. Delivery basis: '), ph('[CIF / FOB] [port]'), t('. Loading window sought: '), ph('[month/quarter]'), t('.')]),

      p([new TextRun({ text: 'Please quote a firm offer covering:', font: 'Calibri', size: 22, bold: true })], { spacing: { after: 90 } }),
      bullet('Your role. ', 'Producer, current title-holder, or broker (if broker, chain to title-holder).'),
      bullet('Lot assay & tonnage. ', 'Assay of the actual parcel (lab, report no., date) and exact tonnage available now.'),
      bullet('Origin & location. ', 'Mine / plant and country of origin; where the material physically sits today (warehouse / port).'),
      bullet('Payable terms. ', 'Payable Cu (%); silver & gold payables (g/t threshold and %); TC/RC (USD/dmt and c/lb); any penalties (As, etc.); moisture basis (paid on dry metric tonne).'),
      bullet('Pricing & QP. ', 'LME reference and quotation period (QP); Incoterm and named port.'),
      bullet('Weighing, sampling & assay. ', 'At load and discharge by SGS or Alfred H. Knight, with umpire — confirm acceptance.'),
      bullet('Payment & security. ', 'Terms via documentary LC or escrow (e.g., 90% provisional against shipping documents, balance on final outturn). We do not remit advance payment to personal accounts.'),
      bullet('Proof of product. ', 'Lot assay, dated stock photos, packing list / weighbridge tickets, and warehouse receipt or holding certificate.'),

      p([t('For reference, we price against '), new TextRun({ text: 'LME copper less prevailing TC/RC and standard payables', font: 'Calibri', size: 22, bold: true }), t(', with proper credit for the silver and gold content. Offers that reflect the current market on those terms will get a firm response from us within '), ph('[24–48] hours'), t('.')], { spacing: { before: 120 } }),
      p([t('If this exact parcel is no longer available, please quote your current stock of the same or comparable copper concentrate — we are an active, repeat buyer.')]),
      p([t('Kindly reply to '), new TextRun({ text: 'estimating@ispgroupgc.com', font: 'Calibri', size: 22, bold: true }), t('. Thank you — I look forward to your offer.')]),

      p([t('Best regards,')], { spacing: { before: 180, after: 220 } }),
      p([new TextRun({ text: 'Estimating Department', font: 'Calibri', size: 22, bold: true })], { spacing: { after: 20 } }),
      p([t('ISP Group LLC')], { spacing: { after: 20 } }),
      p([t('estimating@ispgroupgc.com')]),
    ],
  }],
});

Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(process.argv[2] || 'copper-concentrate-rfq.docx', buf); console.log('written'); });
