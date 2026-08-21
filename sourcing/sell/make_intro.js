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
const bullet = (text) => new Paragraph({ numbering: { reference: 'i', level: 0 }, spacing: { after: 80 }, children: [t(text)] });

function buildIntro({ subject, product, table }) {
  return new Document({
    creator: 'ISP Group LLC',
    styles: { default: { document: { run: { font: 'Calibri', size: 22 } } } },
    numbering: { config: [{ reference: 'i', levels: [{ level: 0, format: 'bullet', text: '•', alignment: AlignmentType.START, style: { paragraph: { indent: { left: 460, hanging: 260 } } } }] }] },
    sections: [{
      properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1080, bottom: 1080, left: 1440, right: 1440 } } },
      children: [
        p([new TextRun({ text: 'ISP GROUP LLC', font: 'Calibri', size: 30, bold: true, color: BRAND })], { spacing: { after: 20 } }),
        p([new TextRun({ text: 'International Trading & Supply', font: 'Calibri', size: 20, color: GREY })], { spacing: { after: 20 } }),
        p([new TextRun({ text: '16395 Biscayne Blvd, Aventura, FL 33160, USA  ·  estimating@ispgroupgc.com', font: 'Calibri', size: 18, color: GREY })], { spacing: { after: 120 } }),
        rule(),
        p([t('Date: '), ph('[DD Month 2026]')]),
        p([t('To: '), ph('[Buyer / Company]'), t('   Attn: '), ph('[Name / Procurement]')]),
        p([new TextRun({ text: subject, font: 'Calibri', size: 22, bold: true })], { spacing: { before: 120, after: 160 } }),
        p([t('Dear '), ph('[Name]'), t(',')]),
        p([t('I am reaching out from ISP Group LLC, an international trading and supply company. We hold regular availability of ' + product + ' to the specification below, and we are selectively expanding our long-term buyer relationships.')]),
        table,
        p([t('')], { spacing: { after: 40 } }),
        p([t('Rather than lead with a quotation, we prefer to understand your requirement first so any proposal we make genuinely fits your operation. Could you kindly share:')]),
        bullet('Your typical monthly / annual purchase volume of this material;'),
        bullet('The grades and specifications you buy, and the packing you prefer;'),
        bullet('Your delivery destination(s) and usual Incoterms;'),
        bullet('Whether you are currently open to qualifying an additional reliable supplier.'),
        p([t('On that basis we will tailor a proposal to your needs. We are glad to provide a current SGS certificate of analysis, samples, and trade references under NCND at the appropriate stage.')], { spacing: { before: 100 } }),
        p([t('I would welcome a short introductory call or your reply to '), new TextRun({ text: 'estimating@ispgroupgc.com', font: 'Calibri', size: 22, bold: true }), t('. Thank you for your time — I look forward to the possibility of working together.')]),
        p([t('Best regards,')], { spacing: { before: 180, after: 220 } }),
        p([new TextRun({ text: 'Trading Desk', font: 'Calibri', size: 22, bold: true })], { spacing: { after: 20 } }),
        p([t('ISP Group LLC')], { spacing: { after: 20 } }),
        p([t('estimating@ispgroupgc.com')]),
      ],
    }],
  });
}

const sulphur = buildIntro({
  subject: 'Sulphur supply — ISP Group LLC (introduction & your requirement)',
  product: 'high-purity elemental sulphur (technical, granular / lump, GOST 127.1-93)',
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
});

const feColw = [1450, 900, 1000, 900, 900, 900, 1300];
const ferro = buildIntro({
  subject: 'Ferrochrome supply — ISP Group LLC (introduction & your requirement)',
  product: 'ferrochrome — High Carbon (HCFeCr) and Low Carbon (LCFeCr), grade to requirement',
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
});

Promise.all([
  Packer.toBuffer(sulphur).then((b) => fs.writeFileSync('sulphur-intro.docx', b)),
  Packer.toBuffer(ferro).then((b) => fs.writeFileSync('ferrochrome-intro.docx', b)),
]).then(() => console.log('written both'));
