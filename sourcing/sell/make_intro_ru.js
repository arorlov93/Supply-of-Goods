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

function buildIntroRu({ subject, product, table }) {
  return new Document({
    creator: 'ISP Group LLC',
    styles: { default: { document: { run: { font: 'Calibri', size: 22 } } } },
    numbering: { config: [{ reference: 'i', levels: [{ level: 0, format: 'bullet', text: '•', alignment: AlignmentType.START, style: { paragraph: { indent: { left: 460, hanging: 260 } } } }] }] },
    sections: [{
      properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1080, bottom: 1080, left: 1440, right: 1440 } } },
      children: [
        p([new TextRun({ text: 'ISP GROUP LLC', font: 'Calibri', size: 30, bold: true, color: BRAND })], { spacing: { after: 20 } }),
        p([new TextRun({ text: 'Международная торговля и поставки', font: 'Calibri', size: 20, color: GREY })], { spacing: { after: 20 } }),
        p([new TextRun({ text: '16395 Biscayne Blvd, Aventura, FL 33160, USA  ·  estimating@ispgroupgc.com', font: 'Calibri', size: 18, color: GREY })], { spacing: { after: 120 } }),
        rule(),
        p([t('Дата: '), ph('[ДД месяц 2026]')]),
        p([t('Кому: '), ph('[Покупатель / Компания]'), t('   Вниманию: '), ph('[Имя / Отдел закупок]')]),
        p([new TextRun({ text: subject, font: 'Calibri', size: 22, bold: true })], { spacing: { before: 120, after: 160 } }),
        p([t('Уважаемый(ая) '), ph('[Имя]'), t(',')]),
        p([t('Обращаюсь от ISP Group LLC, международной торгово-снабженческой компании. Мы располагаем регулярным наличием ' + product + ' по спецификации ниже и выборочно расширяем круг долгосрочных покупателей.')]),
        table,
        p([t('')], { spacing: { after: 40 } }),
        p([t('Прежде чем давать цену, мы предпочитаем сначала понять вашу потребность — чтобы предложение действительно подошло под вашу работу. Не могли бы вы сообщить:')]),
        bullet('типичный объём закупки этого материала в месяц / год;'),
        bullet('марки и спецификации, которые вы берёте, и предпочтительную упаковку;'),
        bullet('порт(ы) назначения и обычные Incoterms;'),
        bullet('открыты ли вы сейчас к квалификации ещё одного надёжного поставщика.'),
        p([t('На этой основе подготовим адресное предложение под ваши нужды. На соответствующем этапе с готовностью предоставим актуальный сертификат анализа SGS, образцы и торговые референсы под NCND.')], { spacing: { before: 100 } }),
        p([t('Буду рад короткому ознакомительному звонку или вашему ответу на '), new TextRun({ text: 'estimating@ispgroupgc.com', font: 'Calibri', size: 22, bold: true }), t('. Благодарю за уделённое время — надеюсь на возможное сотрудничество.')]),
        p([t('С уважением,')], { spacing: { before: 180, after: 220 } }),
        p([new TextRun({ text: 'Trading Desk', font: 'Calibri', size: 22, bold: true })], { spacing: { after: 20 } }),
        p([t('ISP Group LLC')], { spacing: { after: 20 } }),
        p([t('estimating@ispgroupgc.com')]),
      ],
    }],
  });
}

const sulphur = buildIntroRu({
  subject: 'Поставка серы — ISP Group LLC (знакомство и ваша потребность)',
  product: 'серы элементарной высокой чистоты (техническая, гранула / комовая, ГОСТ 127.1-93)',
  table: specTable(
    ['Показатель', 'Норма ГОСТ 127.1-93', 'Факт (типовое)'],
    [
      ['Сера (S), % не менее', '99,98', '99,99'],
      ['Зола, % не более', '0,02', '0,002'],
      ['Органические вещества, % не более', '0,01', '0,005'],
      ['Кислоты (в пересч. на H₂SO₄), % не более', '0,0015', '0,0002'],
      ['Влага (вода), % не более', '0,2', '0,008'],
      ['Механические примеси', 'не допускаются', 'отсутствуют'],
    ],
    [3600, 2500, 2300]
  ),
});

const feColw = [1450, 900, 1000, 900, 900, 900, 1300];
const ferro = buildIntroRu({
  subject: 'Поставка феррохрома — ISP Group LLC (знакомство и ваша потребность)',
  product: 'феррохрома — высокоуглеродистого (HCFeCr) и низкоуглеродистого (LCFeCr), марка под требование',
  table: specTable(
    ['Продукт', 'Cr %', 'Si %', 'C %', 'P %', 'S %', 'Фракция, мм'],
    [
      ['HCFeCr', '65-67', '1,5 макс', '6-8', '0,03', '0,05', '10-100'],
      ['HCFeCr', '64-65', '1-2', '6-8', '0,03', '0,05', '10-100'],
      ['HCFeCr', '62-64', '2', '6-8', '0,03', '0,05', '10-100'],
      ['HCFeCr', '60-62', '2-4', '6-8', '0,03', '0,05', '10-100'],
      ['HCFeCr', '55-60', '5 макс', '8', '0,03', '0,05', '-10'],
      ['HCFeCr', '50-55', '5 макс', '8', '0,03', '0,05', '-10'],
      ['LCFeCr', '60', '1', '0,1', '0,04', '0,04', '10-50'],
      ['LCFeCr', '65', '1', '0,1', '0,04', '0,04', '10-50'],
      ['LCFeCr', '65', '1', '0,05', '0,04', '0,04', '10-50'],
    ],
    feColw
  ),
});

Promise.all([
  Packer.toBuffer(sulphur).then((b) => fs.writeFileSync('sulphur-intro-ru.docx', b)),
  Packer.toBuffer(ferro).then((b) => fs.writeFileSync('ferrochrome-intro-ru.docx', b)),
]).then(() => console.log('written both RU'));
