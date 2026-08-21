const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  BorderStyle, PositionalTab, PositionalTabAlignment, PositionalTabLeader,
} = require('docx');

const BRAND = '2E4A62';
const GREY = '555555';

const p = (children, opts = {}) => new Paragraph({ children, spacing: { after: 160, ...(opts.spacing||{}) }, ...opts });
const t = (text, opts = {}) => new TextRun({ text, font: 'Calibri', size: 22, ...opts });
const ph = (text) => new TextRun({ text, font: 'Calibri', size: 22, color: BRAND, bold: true }); // placeholder

const rule = () => new Paragraph({
  spacing: { after: 200 },
  border: { bottom: { color: 'CCCCCC', space: 1, style: BorderStyle.SINGLE, size: 6 } },
});

const doc = new Document({
  creator: 'ISP Group LLC',
  styles: { default: { document: { run: { font: 'Calibri', size: 22 } } } },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1080, bottom: 1080, left: 1440, right: 1440 } } },
    children: [
      // Letterhead
      p([new TextRun({ text: 'ISP GROUP LLC', font: 'Calibri', size: 30, bold: true, color: BRAND })], { spacing: { after: 20 } }),
      p([new TextRun({ text: 'International Trading & Supply', font: 'Calibri', size: 20, color: GREY })], { spacing: { after: 20 } }),
      p([new TextRun({ text: '16395 Biscayne Blvd, Apt 818, Aventura, FL 33160, USA  ·  info@ispgroupgc.com  ·  +1 (929) 707-5551', font: 'Calibri', size: 18, color: GREY })], { spacing: { after: 120 } }),
      rule(),

      // Date + recipient
      p([t('Date: '), ph('[DD Month 2026]')]),
      p([t('To: '), ph('[Seller / Company name]')], { spacing: { after: 20 } }),
      p([t('Attn: '), ph('[Contact name, title]')], { spacing: { after: 20 } }),
      p([t('Via: '), ph('[email / platform]')]),

      // Subject
      p([new TextRun({ text: 'Re: Firm buying interest — ', font: 'Calibri', size: 22, bold: true }), new TextRun({ text: '[commodity & grade, e.g. Copper Concentrate 25% Cu]', font: 'Calibri', size: 22, bold: true, color: BRAND }), new TextRun({ text: ', ', font: 'Calibri', size: 22, bold: true }), new TextRun({ text: '[tonnage] MT', font: 'Calibri', size: 22, bold: true, color: BRAND })], { spacing: { before: 120, after: 200 } }),

      // Body
      p([t('Dear '), ph('[Contact name]'), t(',')]),

      p([
        t('I am writing on behalf of ISP Group LLC, a U.S.-based trading and supply company. We reviewed your offer for '),
        ph('[commodity / grade]'),
        t(' and are a ready, funded buyer for this material. I will be direct so we do not waste each other’s time: we move quickly when the parcel is real, the counterparty is the title-holder or a mandated seller, and the numbers are transparent.'),
      ]),

      p([
        t('Our interest is a first purchase of '),
        ph('[tonnage] MT'),
        t(' of '),
        ph('[commodity, grade / assay, e.g. 25% Cu min]'),
        t(', with the intent of a recurring monthly offtake of '),
        ph('[monthly tonnage] MT'),
        t(' should the first shipment perform. Delivery basis of interest: '),
        ph('[FOB / CIF / DDP — destination]'),
        t('.'),
      ]),

      p([new TextRun({ text: 'To proceed to a firm offer, please confirm the following in writing:', font: 'Calibri', size: 22, bold: true })], { spacing: { after: 100 } }),

      ...[
        ['Your role. ', 'Are you the producer, the current title-holder, or a broker for this parcel? If broker, please state the chain to the title-holder.'],
        ['Material & assay. ', 'Latest independent assay (lab, report no., date) — full element breakdown, moisture, and penalty elements. We will require re-assay by SGS / Alfred H. Knight at loading.'],
        ['Origin. ', 'Mine / plant name and country of origin, plus export licence or certificate of origin.'],
        ['Current location & availability. ', 'Where the material physically sits today (warehouse / port), who holds title now, and the exact tonnage currently unsold and available.'],
        ['Proof of product. ', 'Dated stock photos, packing list / weighbridge tickets, and warehouse receipt or holding certificate.'],
        ['Commercials. ', 'Your price on the stated basis, payment terms, and readiness to transact under independent inspection with payment via LC or escrow against shipping documents.'],
      ].map(([lead, rest]) => new Paragraph({
        numbering: { reference: 'reqs', level: 0 },
        spacing: { after: 100 },
        children: [new TextRun({ text: lead, font: 'Calibri', size: 22, bold: true }), t(rest)],
      })),

      p([
        t('On our side, you are dealing with a serious counterparty: we are prepared to provide proof of funds, appoint and pay for independent inspection, and settle through '),
        ph('[LC at sight / escrow]'),
        t(' against clean shipping documents. We do not send advance payment to personal accounts, and we expect the same professionalism in return — that protects both of us.'),
      ], { spacing: { before: 120 } }),

      p([
        t('If the original parcel is no longer available, I would welcome your current stock of the same or comparable material — we are an active buyer, not a one-time enquiry.'),
      ]),

      p([
        t('Please reply to '),
        new TextRun({ text: 'info@ispgroupgc.com', font: 'Calibri', size: 22, bold: true }),
        t('. On receipt of the assay and confirmation of availability, I will respond with a firm target and a proposed path to contract within '),
        ph('[24–48] hours'),
        t('. I look forward to doing good business with you.'),
      ]),

      // Sign-off
      p([t('Best regards,')], { spacing: { before: 200, after: 240 } }),
      p([new TextRun({ text: 'Aleksandr Orlov', font: 'Calibri', size: 22, bold: true })], { spacing: { after: 20 } }),
      p([t('Managing Member — ISP Group LLC')], { spacing: { after: 20 } }),
      p([t('info@ispgroupgc.com  ·  +1 (929) 707-5551')], { spacing: { after: 20 } }),
      p([new TextRun({ text: '[Add: proof-of-funds available on NCNDA · SGS/AHK inspection · LC/escrow settlement]', font: 'Calibri', size: 18, italics: true, color: GREY })]),
    ],
  }],
  numbering: {
    config: [{
      reference: 'reqs',
      levels: [{ level: 0, format: 'decimal', text: '%1.', alignment: AlignmentType.START,
        style: { paragraph: { indent: { left: 460, hanging: 320 } } } }],
    }],
  },
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(process.argv[2] || 'concentrate-inquiry-letter.docx', buf);
  console.log('written');
});
