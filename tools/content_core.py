# -*- coding: utf-8 -*-
"""Этап 1: контакты, о компании, услуги, Инкотермс, 404 и три страницы-хаба."""

HOST = "https://ispgroupgc.com/"
ORG = {"@type": "Organization", "name": "ISP GROUP LLC", "url": HOST,
       "email": "info@ispgroupgc.com",
       "address": {"@type": "PostalAddress", "streetAddress": "16395 Biscayne Blvd",
                   "addressLocality": "North Miami Beach", "addressRegion": "FL",
                   "postalCode": "33160", "addressCountry": "US"}}

CORRIDOR_LINKS = [
 ("china.html", "China &rarr; worldwide",
  "Equipment, tools, hardware and building materials out of Ningbo, Qingdao and Shenzhen."),
 ("turkiye.html", "T&uuml;rkiye &rarr; United States",
  "Stone, tile and building materials to New York, Savannah and Houston."),
 ("west-africa.html", "Americas &amp; EU &rarr; West Africa",
  "Frozen food and consumables into Lom&eacute; and Cotonou."),
 ("southern-africa.html", "Intra-Africa",
  "Paper, packaging and industrial supply out of Durban into Botswana and SADC."),
]

CATEGORY_LINKS = [
 ("building-materials.html", "Building and finishing materials",
  "Stone, tile, cement products, insulation, dry mixes, sanitary ware, cable."),
 ("industrial-equipment.html", "Industrial equipment and machinery",
  "Production lines, compressors, pumps, generators, material handling."),
 ("tools-hardware.html", "Tools, hardware and fasteners",
  "Power and hand tools, abrasives, measuring instruments, fixings."),
 ("metals-pipe.html", "Metals and pipe",
  "Sections, sheet and plate, seamless and welded pipe, fittings and flanges."),
 ("paper-packaging.html", "Paper, packaging and consumables",
  "Newsprint, kraft and containerboard in reels, corrugated, PPE and workwear."),
 ("food-agricultural.html", "Food and agricultural goods",
  "Frozen and chilled protein, bulk staples and ingredients under veterinary certification."),
]

# ───────────────────────────────────────────────────────── контакты
CONTACT_FORM = """<aside class="cform" id="enquiry">
  <span class="eyebrow">Send a requirement</span>
  <form id="cf" novalidate>
    <label for="f-product">Product or equipment</label>
    <input id="f-product" type="text" autocomplete="off" placeholder="What you need, in your own words">
    <label for="f-qty">Quantity</label>
    <input id="f-qty" type="text" autocomplete="off" placeholder="Containers, tonnes, pieces">
    <label for="f-port">Destination port or city</label>
    <input id="f-port" type="text" autocomplete="off" placeholder="Where it has to arrive">
    <label for="f-terms">Terms you want quoted</label>
    <select id="f-terms">
      <option>Not sure, advise</option><option>FOB</option><option>CFR</option>
      <option>CIF</option><option>FCA</option><option>DAP</option>
    </select>
    <label for="f-note">Anything else</label>
    <textarea id="f-note" placeholder="Specification, standard, certification, deadline"></textarea>
    <button class="btn" type="submit">Compose the email</button>
    <p class="cresult" id="cf-out" hidden></p>
  </form>
</aside>"""

CONTACT_JS = """<script>
(function(){
  /* Бэкенда нет, и это честнее: форма собирает письмо и открывает почтовый
     клиент, поэтому у отправителя остаётся копия в «Отправленных». */
  var f=document.getElementById('cf'); if(!f) return;
  function v(id){ var e=document.getElementById(id); return e?(e.value||'').trim():''; }
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var p=v('f-product'), q=v('f-qty'), po=v('f-port'), t=v('f-terms'), n=v('f-note');
    var lines=['Product: '+(p||'(not stated)'),'Quantity: '+(q||'(not stated)'),
               'Destination: '+(po||'(not stated)'),'Terms: '+t];
    if(n) lines.push('','Notes:',n);
    lines.push('','Sent from ispgroupgc.com');
    var subj='Requirement'+(p?(': '+p):'')+(po?(' to '+po):'');
    var href='mailto:info@ispgroupgc.com?subject='+encodeURIComponent(subj)+
             '&body='+encodeURIComponent(lines.join('\\n'));
    var out=document.getElementById('cf-out');
    out.innerHTML='Opening your email client. If nothing happens, write to '+
      '<span class="mail">info@ispgroupgc.com</span> with the same details.';
    out.hidden=false;
    window.location.href=href;
  });
})();
</script>"""

CONTACT = {
 "slug": "contact",
 "title": "Contact ISP Group | sourcing enquiries",
 "desc": "Send a requirement to ISP GROUP LLC: product, quantity and destination port is "
         "enough to start. Office at 16395 Biscayne Blvd, North Miami Beach, Florida.",
 "trail": [("ISP Group", "index.html"), ("Contact", None)],
 "h1": "Tell us what you need and <em>where it has to arrive</em>",
 "sub": "Product, quantity and destination port is enough to start a quotation. No account, "
        "no registration, no fee. We reply within one working day.",
 "chips": ["<b>1</b> working day to reply", "<b>10</b> working days to a landed price",
           "FOB &middot; CFR &middot; CIF &middot; FCA &middot; DAP"],
 "hero_right": CONTACT_FORM,
 "lede": ("What to put in the first message",
   "The faster a requirement becomes a specification, the faster it becomes a price. "
   "You do not need all of this to write to us, but each line you can answer removes "
   "a round trip."),
 "body": [
  ("h2", "The four lines that start a quotation"),
  ("p", "Everything else we can work out together. These four decide whether we can go "
        "straight to producers or have to come back with questions first."),
  ("ul", ["<b>What the product is</b>, in whatever words you use for it. A photograph, a "
          "drawing, a competitor's part number or a sample are all better than a category.",
          "<b>How much</b>, per shipment and per month if it repeats. A one-off container "
          "and a monthly programme are priced differently and sourced differently.",
          "<b>Where it has to arrive.</b> Port, city or the gate of your own warehouse. "
          "The inland leg is often the largest single line in a landed price.",
          "<b>On what terms</b>, if you already know. If you do not, say so and we will "
          "quote two bases side by side so the logistics portion is visible."]),
  ("h2", "What happens after you write"),
  ("p", "Within one working day you get an acknowledgement with the questions we still "
        "need answered. Those questions are the specification taking shape, and they are "
        "the part that decides whether the shipment works."),
  ("p", "Within about ten working days you get a landed price: at least three comparable "
        "offers from verified producers on one basis, with freight, insurance, port charges, "
        "duty and certification added, and with the rate validity stated. If a lane is new "
        "to us it takes longer, and we say so at the start rather than at the end."),
  ("note", "We do not ask for a fee to quote, and we do not take a commission on a "
           "producer's invoice. We buy in our own name and resell, so our price is our price."),
  ("h2", "If you are a producer, not a buyer"),
  ("p", "Write to the same address. We are interested in producers who can hold a "
        "specification and a loading date, in any of the categories we supply, and "
        "particularly in frozen protein, paper and packaging, stone and industrial equipment."),
  ("p", "Send the establishment or licence number, the product range with pack formats, the "
        "ports you normally load, and the countries you are already approved to ship to. "
        "That is enough for us to tell you within a day whether we have a buyer for it."),
  ("h2", "Where we are"),
  ("p", "ISP GROUP LLC is a United States company. The registered office is at 16395 Biscayne "
        "Blvd, North Miami Beach, Florida 33160. Correspondence in English and Russian; "
        "written enquiries are answered faster than any other channel."),
 ],
 "faq_h2": "Before you write",
 "faq_sub": "Four things people check before sending a first enquiry.",
 "faq": [
  ("Do you charge for a quotation?",
   "No. There is no fee for a quotation and no commission added on top of a producer's "
   "invoice. We buy the goods in our own name and resell them, so the price we quote is "
   "the price you pay."),
  ("What is the smallest order you will handle?",
   "We work in full container loads, because that is where the economics hold. A first order "
   "is normally one or two containers on full commercial terms before a monthly programme "
   "starts. For a trial we can consolidate several suppliers into one container."),
  ("How fast can you reply?",
   "An acknowledgement with the open questions within one working day. A landed price in "
   "about ten working days on a lane we already run. On a new lane it is longer, and we say "
   "how much longer at the start."),
  ("Which languages do you work in?",
   "English and Russian in correspondence. Our producer side also works in Chinese, Turkish, "
   "Portuguese and French through local partners, which is usually where a specification "
   "gets lost in translation."),
 ],
 "related": ("Where to go next",
   "If you already know what you need, these are the pages that answer it fastest.",
   [("supply.html", "What we supply", "Six categories, with a page for each."),
    ("corridors.html", "Corridors", "Four routes we already run end to end."),
    ("guides.html", "Guides", "Incoterms, landed cost, certificates, supplier checks."),
    ("about.html", "About ISP Group", "Who we are and how we work.")]),
 "ld": [{"@context": "https://schema.org", "@type": "ContactPage",
         "url": HOST + "contact.html", "mainEntity": ORG}],
 "tail": "",
}

# ───────────────────────────────────────────────────────── о компании
ABOUT = {
 "slug": "about",
 "title": "About ISP Group | international sourcing and trading",
 "desc": "ISP GROUP LLC is a United States trading company. We buy in our own name, verify "
         "producers before quoting and deliver on agreed Incoterms. Twenty years of supply work.",
 "trail": [("ISP Group", "index.html"), ("About", None)],
 "h1": "A trading company, <em>not an agency</em>",
 "sub": "ISP GROUP LLC buys goods in its own name and resells them. One contract with the "
        "producer, one contract with the buyer, one counterparty to hold responsible.",
 "chips": ["<b>20</b> years of supply work", "Principal, <b>not a broker</b>",
           "United States entity", "FOB &middot; CFR &middot; CIF &middot; FCA &middot; DAP"],
 "img": ("terminal.jpg", 1023, 438, "Ship-to-shore gantry cranes working a container vessel",
         "We carry the goods on our own balance sheet until they are yours"),
 "lede": ("What the difference between a trader and an agent actually means",
   "An agent introduces you to a factory and takes a percentage. If the factory fails, the "
   "agent is a witness. We are the buyer on one contract and the seller on the next, which "
   "means the failure is ours to fix and ours to pay for."),
 "body": [
  ("h2", "Who we are"),
  ("p", "ISP GROUP LLC is a United States company with its registered office in North Miami "
        "Beach, Florida. We source materials, products and industrial equipment from verified "
        "producers and deliver them to the buyer's port or gate on agreed Incoterms."),
  ("p", "Behind the company are twenty years of supply work across four continents: container "
        "programmes out of China, delivery to unequipped shorelines in the Russian north where "
        "there is no quay and the navigation window is measured in weeks, and food and "
        "equipment into the European Union under its own certification regime. Different "
        "cargo, different continents, the same discipline. That account is written out in "
        "full on <a href=\"experience.html\">twenty years of supply work</a>."),
  ("h2", "How we work"),
  ("p", "Our work splits into four things we do on every shipment, in this order."),
  ("ul", ["<b>We verify before we quote.</b> Establishment and licence numbers are checked "
          "against the registers of the importing country, not taken from the seller's "
          "website. Lookalike exporter domains are common in this trade and we screen for them.",
          "<b>We price from customs data.</b> We benchmark what comparable goods actually "
          "cleared customs at on your lane before we negotiate, so an offer can be judged "
          "against the market rather than against itself.",
          "<b>We take title.</b> We are the buyer on one contract and the seller on the next. "
          "You deal with one counterparty, one invoice and one currency, in your own "
          "jurisdiction.",
          "<b>We mirror the terms.</b> Inspection windows, weight tolerances, claim periods "
          "and bank charges are matched on both contracts, so nothing falls into the gap "
          "between supplier and buyer."]),
  ("h2", "Why we are not tied to one commodity"),
  ("p", "Because the asset is not the product, it is the lane. A trade lane is the set of "
        "verified producers, the forwarder, the customs broker and the document set on a "
        "given route. Once a lane works, the product travelling down it can change, and the "
        "second shipment costs a fraction of the first to set up."),
  ("p", "That is why our pages are organised by <a href=\"corridors.html\">corridor</a> rather "
        "than by catalogue, and why a product outside our usual categories is a sourcing "
        "project rather than a refusal. What transfers between products is the method: "
        "specification, producer verification, landed costing, documents and settlement. What "
        "has to be rebuilt each time is the producer shortlist."),
  ("h2", "What we do not do"),
  ("p", "We do not quote on a specification we have not read, we do not prepay a producer in "
        "full, and we do not put a commission on top of someone else's invoice and call it a "
        "service."),
  ("p", "We also do not claim capability we have not got. If a lane is new to us we say so, "
        "we say what we will have to build, and we say how long that takes. A buyer who is "
        "told the truth about a twelve week lead time plans around it. A buyer who is told "
        "six and gets twelve does not come back."),
  ("h2", "Where to find the detail"),
  ("p", "The <a href=\"services.html\">services page</a> sets out each step as a separate "
        "piece of work with a named deliverable. The <a href=\"corridors.html\">corridor "
        "pages</a> go into what is specific to each route. The "
        "<a href=\"guides.html\">guides</a> answer the questions that come up before a first "
        "order, from Incoterms to what a landed price has to include."),
 ],
 "faq_h2": "What buyers ask about the company",
 "faq_sub": "The questions that come before the commercial ones.",
 "faq": [
  ("Are you a broker or an agent?",
   "Neither. We buy the goods in our own name and resell them. There is no commission on top "
   "of a producer's invoice, and the producer is not asked to manage a triangular billing "
   "arrangement."),
  ("Where is ISP Group registered?",
   "ISP GROUP LLC is a United States company. The registered office is 16395 Biscayne Blvd, "
   "North Miami Beach, Florida 33160."),
  ("Can you source a product you have never traded?",
   "Yes, and most of our lanes started that way. What transfers between products is the "
   "method. What has to be built each time is the producer shortlist, and that is the part we "
   "quote a timeline for honestly."),
  ("Who carries the risk if the factory does not ship?",
   "We do, because we are the seller on your contract. That is the practical difference "
   "between a trader and an agent, and it is why we never prepay a producer in full and stage "
   "payment against production milestones and documents instead."),
 ],
 "related": ("Keep reading",
   "The pages that go behind this one.",
   [("experience.html", "Twenty years of supply work",
     "China, the Russian north and the European Union: three regimes, one method."),
    ("services.html", "What we actually do", "Each step as a named piece of work."),
    ("corridors.html", "Corridors", "The four routes we run end to end."),
    ("contact.html", "Contact", "Send a requirement and get a landed price.")]),
 "ld": [{"@context": "https://schema.org", "@type": "AboutPage", "url": HOST + "about.html",
         "mainEntity": dict(ORG, **{
           "alternateName": "ISP Group Global Commerce",
           "description": "United States trading company sourcing materials, products and "
                          "industrial equipment from verified producers worldwide."})}],
}

# ───────────────────────────────────────────────────────── услуги
SERVICES = {
 "slug": "services",
 "title": "What we do | sourcing, verification, landed pricing",
 "desc": "Each step of a cross-border purchase as a named piece of work: specification, "
         "producer verification, landed costing, contracting, inspection and documents.",
 "trail": [("ISP Group", "index.html"), ("What we do", None)],
 "h1": "Six pieces of work between an idea <em>and a delivered container</em>",
 "sub": "Most of what goes wrong in international trade goes wrong in a specific place. "
        "These are those places, and what we do at each of them.",
 "chips": ["Specification", "Verification", "Landed price", "Contract",
           "Inspection", "Documents"],
 "hero_right": "",
 "lede": ("Why we describe the work and not the goods",
   "Any trader can list products. What a buyer is actually paying for is the sequence below, "
   "because that is where a purchase survives or fails. We can run the whole sequence or "
   "step in at any point in it."),
 "body": [
  ("h2", "Specification"),
  ("p", "We turn a request into something a factory can quote against and a laboratory can "
        "test against: grade, dimension or cut, pack, tolerance, standard and the "
        "certificates the destination country requires."),
  ("p", "Most failed imports fail here, before anyone has quoted. A purchase order that says "
        "“machine, 50 kW, 380 V” leaves the motor brand, the controller, the duty cycle, "
        "the finish, the spares pack and the manual language to the seller, and the seller "
        "resolves every one of them in the direction of cost. Once a specification exists, "
        "three quotes against it are comparable and a fourth supplier can be added without "
        "starting again."),
  ("note", "Deliverable: a specification sheet and the list of certificates the destination "
           "requires, in a form you can send to any producer, including ones we did not find."),
  ("h2", "Producer verification"),
  ("p", "We approach producers directly rather than through intermediaries, and we check each "
        "one against the register of the importing country rather than against its own "
        "website. For food that means the establishment number and written confirmation of "
        "admissibility. For manufactured goods it means the business licence, the export "
        "licence and the certification mark the destination requires."),
  ("p", "One check catches more fraud than all the others combined: the beneficiary name on "
        "the proforma invoice has to match the name on the licence. Lookalike exporter domains "
        "are endemic in this trade, and a mismatch between the seller and the bank account is "
        "the whole question, not a detail."),
  ("note", "Deliverable: at least three comparable offers from verified producers, quoted on "
           "one basis, with the registration evidence attached."),
  ("h2", "Landed price"),
  ("p", "A factory price is not a price. Freight, insurance, port charges, duty, certification "
        "and the inland leg are added so you see one number at your own door, with the rate "
        "validity stated on it."),
  ("p", "We benchmark that number against what comparable goods actually cleared customs at on "
        "your lane. Customs statistics show the transacted value divided by the net weight, "
        "which means every discount the seller really gave is already inside the figure. "
        "A quotation is what a seller would like to receive; customs data is what the market "
        "paid. Negotiating against the second rather than the first regularly moves a target "
        "by a fifth or more."),
  ("note", "Deliverable: one landed number per option, with the cost build-up shown and the "
           "validity date stated."),
  ("h2", "Contract and settlement"),
  ("p", "We contract with the producer in our own name and with the buyer on a mirrored set of "
        "terms. Inspection windows, weight tolerances, claim periods and bank charges are "
        "written the same way on both legs, so nothing falls into the gap between them."),
  ("p", "Settlement is by irrevocable letter of credit, documentary collection or staged "
        "transfer. Every stage is tied to something observable: a deposit releases production, "
        "a second instalment falls due against a passed inspection, the balance against the "
        "document set. A date pays for a date. An event pays for goods."),
  ("note", "Deliverable: two mirrored contracts and a payment schedule in which every stage "
           "has an observable trigger."),
  ("h2", "Inspection and loading"),
  ("p", "Where the value justifies it, production is inspected before full payment and before "
        "loading: a sampling plan against the specification for a commodity, a witnessed run "
        "for equipment, photographs of the goods, the carton, the pallet and the loaded "
        "container in every case, taken by someone who is not the seller."),
  ("p", "Wood packaging is checked for heat treatment and ISPM 15 marking at loading, not at "
        "arrival, because a container that reaches the destination port with untreated pallets "
        "is refused there at the importer's expense."),
  ("note", "Deliverable: an inspection report with photographs, and confirmation of pack and "
           "marking before the container is sealed."),
  ("h2", "Documents and delivery"),
  ("p", "The document set is where the money is quietly lost. The HS code decides the duty rate "
        "and the importer of record is liable for a wrong one, not the seller who typed it. "
        "The certificate of origin decides whether a preference applies. The packing list has "
        "to agree with the invoice, the bill of lading and the physical container down to the "
        "carton count, because customs anywhere resolves a discrepancy by inspecting."),
  ("p", "We issue the set through a nominated forwarder, agree the classification before the "
        "order rather than at entry, and hand over a file that a customs broker can clear "
        "without calling anyone."),
  ("note", "Deliverable: a complete document set issued before arrival, and a classification "
           "agreed in writing before the order was placed."),
 ],
 "faq_h2": "How the work is bought",
 "faq_sub": "You do not have to take the whole sequence.",
 "faq": [
  ("Can we use you for only part of this?",
   "Yes. Buyers who already have a producer often use us for verification, inspection and the "
   "document set. Buyers who have a product idea and no supplier use the whole sequence. We "
   "price the parts separately so you can see what each one costs."),
  ("Do you charge a fee for sourcing?",
   "No separate sourcing fee and no commission on a producer's invoice. We buy in our own "
   "name and resell, so our margin is inside the price we quote and you can compare it with "
   "any other offer on the same basis."),
  ("What if the specification is the thing we do not have?",
   "That is the normal case and it is the first piece of work on this page. Describe the "
   "problem rather than the product and we will write the specification with you."),
  ("How long does a first quotation take?",
   "About ten working days to a landed price on a lane we already run, from the moment the "
   "specification is agreed. On a new lane it is longer because the producer shortlist has to "
   "be built, and we say how much longer before we start."),
 ],
 "related": ("Keep reading",
   "Where this work is applied.",
   [("corridors.html", "Corridors", "The four routes we run end to end."),
    ("supply.html", "What we supply", "Six categories, a page for each."),
    ("guides.html", "Guides", "Incoterms, landed cost, certificates, supplier checks."),
    ("contact.html", "Contact", "Send a requirement and get a landed price.")]),
 "ld": [{"@context": "https://schema.org", "@type": "Service",
         "serviceType": "International sourcing, verification and supply",
         "provider": ORG, "url": HOST + "services.html",
         "hasOfferCatalog": {"@type": "OfferCatalog", "name": "What we do",
           "itemListElement": [{"@type": "Offer", "itemOffered":
             {"@type": "Service", "name": n}} for n in
             ("Specification", "Producer verification", "Landed pricing",
              "Contract and settlement", "Inspection and loading",
              "Documents and delivery")]}}],
}

# ───────────────────────────────────────────────────────── Инкотермс
INCOTERMS_TABLE = """<div class="scroller"><table class="ptable">
<thead><tr><th scope="col">Rule</th><th scope="col">Seller pays to</th>
<th scope="col">Risk passes</th><th scope="col">Export / import clearance</th>
<th scope="col">Mode</th></tr></thead><tbody>
<tr><td>EXW</td><td>Nothing. Goods available at the works</td>
<td>At the seller's premises</td><td>Buyer does both</td><td>Any</td></tr>
<tr><td>FCA</td><td>Delivery to the carrier at the named place</td>
<td>On handover to the carrier</td><td>Seller exports, buyer imports</td><td>Any</td></tr>
<tr><td>FOB</td><td>Loading on board at the port of shipment</td>
<td>When goods are on board</td><td>Seller exports, buyer imports</td><td>Sea only</td></tr>
<tr><td>CFR</td><td>Freight to the destination port</td>
<td><b>On board at origin</b>, not on arrival</td><td>Seller exports, buyer imports</td>
<td>Sea only</td></tr>
<tr><td>CIF</td><td>Freight plus minimum insurance to destination port</td>
<td><b>On board at origin</b>, not on arrival</td><td>Seller exports, buyer imports</td>
<td>Sea only</td></tr>
<tr><td>CPT</td><td>Carriage to the named destination</td>
<td>On handover to the first carrier</td><td>Seller exports, buyer imports</td><td>Any</td></tr>
<tr><td>CIP</td><td>Carriage plus all-risks insurance to destination</td>
<td>On handover to the first carrier</td><td>Seller exports, buyer imports</td><td>Any</td></tr>
<tr><td>DAP</td><td>Arrival at the named place, ready for unloading</td>
<td>At the named place</td><td>Seller exports, buyer imports</td><td>Any</td></tr>
<tr><td>DPU</td><td>Arrival and unloading at the named place</td>
<td>After unloading</td><td>Seller exports, buyer imports</td><td>Any</td></tr>
<tr><td>DDP</td><td>Arrival, cleared for import, duty paid</td>
<td>At the named place</td><td>Seller does both</td><td>Any</td></tr>
</tbody></table></div>"""

INCOTERMS = {
 "slug": "incoterms",
 "title": "Incoterms 2020 explained | who pays for what",
 "desc": "FOB, CFR, CIF, FCA, DAP and the rest in plain language: who pays, where risk "
         "passes, which rules are sea-only, and why CFR and CIF split cost from risk.",
 "trail": [("ISP Group", "index.html"), ("Guides", "guides.html"), ("Incoterms", None)],
 "h1": "Incoterms, and the two columns <em>people confuse</em>",
 "sub": "An Incoterm says who pays for what and where the risk passes. Those are two "
        "different questions, and on CFR and CIF the answers are in different countries.",
 "chips": ["Incoterms 2020", "11 rules", "4 sea-only", "Cost &ne; risk"],
 "lede": ("Why this matters before the price, not after",
   "Two quotes cannot be compared until both carry the same Incoterm and the same named "
   "place. A FOB price and a CIF price for the same goods can differ by a third, and neither "
   "seller is wrong. The buyer who treats them as the same number is."),
 "body": [
  ("h2", "The whole set on one page"),
  ("p", "Eleven rules in the 2020 edition. Each one answers three questions: how far the "
        "seller pays, where the risk transfers, and who handles clearance. Read the risk "
        "column before the cost column."),
  ("raw", INCOTERMS_TABLE),
  ("p", "Every rule has to be written with a named place after it. “CIF” means nothing; "
        "“CIF Lomé, Incoterms 2020” means something. The named place is where the "
        "seller's obligation ends, and on the C rules it is not where the risk ends."),
  ("h2", "The mistake that costs the most: CFR and CIF"),
  ("p", "On CFR and CIF the seller pays the freight all the way to the destination port, but "
        "the risk passes to the buyer when the goods are on board at the origin port. The two "
        "columns are deliberately in different places, and it is the only family of rules "
        "where that is true."),
  ("p", "In practice: if the vessel is lost mid-voyage on a CFR shipment, the goods were "
        "already the buyer's, and the buyer still owes the seller for them. The freight being "
        "prepaid changes nothing about that. This is why CIF exists, and why the insurance "
        "clause in a CIF contract deserves more attention than the price."),
  ("note", "Under Incoterms 2020, CIF requires only minimum cover, Institute Cargo Clauses "
           "(C), while CIP requires all-risks cover, Institute Cargo Clauses (A). A buyer who "
           "assumes CIF means fully insured is assuming something the rule does not say."),
  ("h2", "FOB is being used for containers, and it should not be"),
  ("p", "FOB, CFR and CIF are sea and inland waterway rules written for cargo handed over the "
        "ship's side. For a container the seller loses physical control days earlier, at the "
        "container terminal, and has no practical way to affect anything between the gate and "
        "the vessel."),
  ("p", "The correct container equivalents are FCA, CPT and CIP, where the risk passes on "
        "handover to the carrier. The trade has used FOB for containers for decades out of "
        "habit, and most of the time nothing goes wrong. When something does go wrong in the "
        "terminal, the contract does not say who owns it."),
  ("h2", "Which rule to ask for, by situation"),
  ("ul", ["<b>You have your own forwarder and good rates.</b> Ask for FCA at the named "
          "terminal, or FOB if the seller will not move off it. You control the main carriage.",
          "<b>You want one number and no logistics.</b> Ask for CIF or CFR at your port, and "
          "read the insurance clause. You still clear the import.",
          "<b>You want it at your own gate.</b> Ask for DAP. The seller carries the inland leg "
          "and its risk; you still clear the import and pay the duty.",
          "<b>You want nothing to do with customs.</b> DDP, and expect to pay for it. The "
          "seller is taking on an import clearance in a country where it may not be "
          "established, and prices that risk accordingly.",
          "<b>You are collecting from the factory yourself.</b> EXW, and understand that "
          "export clearance is now yours, which in some countries a foreign buyer cannot do."]),
  ("h2", "What we quote and why"),
  ("p", "We quote FOB, CFR, CIF, FCA and DAP, and we prefer to show at least two bases side "
        "by side. The gap between a FOB number and a DAP number is the honest cost of the "
        "logistics portion, and a buyer who can see it is in a far better position than one "
        "looking at a single landed figure."),
  ("p", "On corridors where the inland leg carries most of the risk, such as "
        "<a href=\"southern-africa.html\">Durban into landlocked SADC</a>, we lead with DAP. "
        "On <a href=\"west-africa.html\">reefer programmes into West Africa</a> we lead with "
        "CIF or CFR per port, because the ports price differently. On "
        "<a href=\"china.html\">China</a> we usually show FOB and CIF together."),
 ],
 "faq_h2": "Incoterms questions we get",
 "faq_sub": "The four that come up on almost every first contract.",
 "faq": [
  ("Does CIF mean my goods are insured for their full value?",
   "Not automatically. Under Incoterms 2020 the seller's obligation on CIF is minimum cover, "
   "Institute Cargo Clauses (C), which is a restricted named-perils cover. CIP requires "
   "Institute Cargo Clauses (A), which is all risks. If you want full cover on a CIF "
   "shipment, it has to be written into the contract."),
  ("Who pays the duty on DAP?",
   "The buyer. DAP means delivered at the named place ready for unloading, with import "
   "clearance and duty still on the buyer. Only DDP puts the import clearance and duty on the "
   "seller."),
  ("Is FOB wrong for containers?",
   "Technically yes. FOB is written for goods placed on board a vessel, and with a container "
   "the seller hands over at the terminal days earlier. FCA is the correct rule. In practice "
   "FOB is used constantly for containers, and the problem only surfaces when something "
   "happens between the terminal gate and the ship."),
  ("Can I compare a FOB price with a CIF price?",
   "Not directly. You have to add freight, insurance and origin charges to the FOB number "
   "first, and those depend on the route, the season and the carrier. We quote two bases side "
   "by side precisely so the difference is visible rather than assumed."),
 ],
 "related": ("Keep reading",
   "The guides that follow from this one.",
   [("landed-price.html", "What a landed price must include",
     "Every line between a factory price and your gate."),
    ("letter-of-credit.html", "A letter of credit at sight",
     "How it protects both sides and what it costs."),
    ("guides.html", "All guides", "Everything we have written down."),
    ("corridors.html", "Corridors", "Which terms we lead with on each route.")]),
 "ld": [],
}

# ───────────────────────────────────────────────────────── 404
NOTFOUND = {
 "slug": "404",
 "title": "Page not found | ISP Group",
 "desc": "That page does not exist. The corridors, categories and guides are all linked here.",
 "robots": "noindex,follow",
 "eyebrow": "404",
 "h1": "That page <em>does not exist</em>",
 "sub": "The address may have changed, or the link may be wrong. Everything on the site is "
        "reachable from the four groups below.",
 "related": ("Where you probably wanted to go",
   "The four parts of the site.",
   [("supply.html", "What we supply", "Six categories, a page for each."),
    ("corridors.html", "Corridors", "Four routes we run end to end."),
    ("guides.html", "Guides", "Incoterms, landed cost, certificates, supplier checks."),
    ("contact.html", "Contact", "Send a requirement and get a landed price.")]),
 "ld": [],
}

# ───────────────────────────────────────────────────────── список руководств
GUIDE_LINKS = [
 ("incoterms.html", "Incoterms 2020 explained",
  "Who pays for what, where risk passes, and why CFR splits the two."),
 ("landed-price.html", "What a landed price must include",
  "Every line between a factory price and your own gate."),
 ("verify-supplier.html", "How to verify a supplier is a factory",
  "Licence, export right and the bank account name that gives it away."),
 ("letter-of-credit.html", "A letter of credit at sight",
  "What it protects, what it costs and where it fails."),
 ("customs-data-pricing.html", "How customs data shows the real price",
  "Why a quotation and a transacted value are different numbers."),
 ("hs-code.html", "Who is liable for the HS code",
  "The importer of record, and what that means in money."),
 ("ispm-15.html", "ISPM 15: how a pallet stops a container",
  "Heat treatment, the mark, and where the check belongs."),
 ("container-loading.html", "FCL, LCL and consolidation",
  "What fits, what it costs, and when to share a box."),
 ("veterinary-certificate.html", "Veterinary certificates for frozen meat",
  "Establishment approval, the certificate form and who issues it."),
 ("poultry-cuts.html", "Wing, drumette, flat: four different products",
  "The cut nomenclature that makes two offers incomparable."),
 ("reefer-cold-chain.html", "What a reefer programme requires",
  "Temperature, recorders, plug time and the pack nobody checks."),
 ("antidumping-check.html", "The trade remedy check before you order",
  "Why a deposit can exceed the value of the goods."),
 ("bill-of-lading.html", "Bill of lading and telex release",
  "Receipt, contract and title in one document, and how to release cargo."),
 ("demurrage-detention.html", "Demurrage and detention",
  "The two clocks that run after arrival, and who stops them."),
 ("certificate-of-origin.html", "Certificates of origin",
  "Preferential and non-preferential, who issues them, what breaks them."),
 ("proforma-invoice.html", "The proforma invoice",
  "An offer, not an accounting document. What it has to contain."),
]

# ───────────────────────────────────────────────────────── хабы
SUPPLY = {
 "slug": "supply",
 "title": "What we supply | materials, equipment, food",
 "desc": "Six categories where we already have producer relationships and a documented lane: "
         "building materials, industrial equipment, tools, metals and pipe, paper, food.",
 "trail": [("ISP Group", "index.html"), ("What we supply", None)],
 "h1": "Materials, products <em>and equipment</em>",
 "sub": "We are not tied to one commodity. These six categories are where we already have "
        "producer relationships and a documented lane. A product outside them is a sourcing "
        "project, not a refusal.",
 "chips": ["6 categories", "FCL and consolidated LCL", "To specification or to brand"],
 "img": ("pipe.jpg", 922, 691, "Stacked steel pipe seen end on",
         "Bought to a named standard, with the mill certificate attached"),
 "lede": ("Why a category list is the least interesting thing about a trader",
   "Everyone publishes one. What decides whether a purchase works is whether the specification "
   "was written properly, whether the producer was checked and whether the documents match "
   "the container. The categories below are simply where we have already done that."),
 "body": [
  ("h2", "How to read these pages"),
  ("p", "Each category page says the same four things: what we actually buy within it, the "
        "standard or grade it is bought against, the certificates the destination usually "
        "requires, and how it is packed and loaded. Those four are what turn a shopping list "
        "into a quotation."),
  ("p", "If your product is not here, that is not a refusal. "
        "Most of our lanes began with a product we had never traded, because what transfers "
        "between products is the method rather than the catalogue. What has to be rebuilt each "
        "time is the producer shortlist, and we say honestly how long that takes."),
  ("h2", "What is common to all six"),
  ("ul", ["Bought against a written specification and a named standard, never against a "
          "photograph or a category name.",
          "Producer checked against the register of the importing country before a price is "
          "quoted, not after an order is placed.",
          "Priced landed, with freight, insurance, port charges, duty and certification "
          "included and the rate validity stated.",
          "Inspected and photographed before the container is sealed, where the value "
          "justifies it.",
          "Delivered under one contract with us, in one currency, with one counterparty to "
          "hold responsible."]),
 ],
 "related": ("The six categories",
   "A page for each, with the standards, certificates and pack that each one needs.",
   CATEGORY_LINKS),
 "ld": [],
}

CORRIDORS_HUB = {
 "slug": "corridors",
 "title": "Trade corridors we run | China, Türkiye, West Africa, SADC",
 "desc": "Four routes we run end to end, with the producers, forwarder, customs broker and "
         "document set already in place on each one.",
 "trail": [("ISP Group", "index.html"), ("Corridors", None)],
 "h1": "We run lanes, <em>not a catalogue</em>",
 "sub": "A trade lane is the real asset: the producers, the forwarder, the customs broker and "
        "the document set on a given route. Once a lane works, the product travelling down it "
        "can change.",
 "chips": ["4 active corridors", "FOB &middot; CFR &middot; CIF &middot; DAP",
           "FCL and consolidated LCL"],
 "img": ("vessel.jpg", 1023, 575, "Container vessel under way",
         "Cargo moves under our contract from the plant gate to the discharge port"),
 "lede": ("Why we organise the business by route and not by product",
   "Setting up a first shipment on a new route is most of the work: finding producers that "
   "survive a check, finding a forwarder who actually calls back, learning which customs "
   "office wants which paper. The second shipment on the same route costs a fraction of that. "
   "So the asset is the route."),
 "body": [
  ("h2", "What a working corridor contains"),
  ("ul", ["<b>Producers that have been checked</b>, with licence or establishment numbers "
          "verified against the importing country's register rather than their own websites.",
          "<b>A forwarder with real rates</b> on that specific leg, not a quote desk that "
          "sends a number three days later.",
          "<b>A customs broker physically present</b> at the office or border post the cargo "
          "will actually cross.",
          "<b>A document set that has already cleared</b> at that destination, so the next "
          "one is a copy rather than an experiment.",
          "<b>A settlement route</b> the banks on both ends already accept."]),
  ("h2", "The four we run now"),
  ("p", "Each corridor page goes into what is specific to that route: the cargo that moves "
        "well on it, the terms we lead with, the documents, and the one check on that lane "
        "that turns a good purchase into a loss."),
  ("p", "They are deliberately different in character. China is about specification and "
        "verification. Türkiye is about grading, crating and a customs classification. "
        "West Africa is about veterinary admissibility and payment terms. Southern Africa is "
        "about a road leg and which trade regime the goods are moving under."),
  ("h2", "A route that is not here"),
  ("p", "We open new lanes, and most of the four below started as one. What we will tell you "
        "at the start is how long it takes to build the producer shortlist and whether the "
        "destination has a certification regime we have not worked under before. A buyer who "
        "is told the truth about a twelve week lead time plans around it."),
 ],
 "related": ("The four corridors", "Each with its own facts, documents and failure modes.",
             CORRIDOR_LINKS),
 "ld": [],
}

GUIDES = {
 "slug": "guides",
 "title": "Guides to importing | Incoterms, landed cost, certificates",
 "desc": "Plain answers to the questions that come up before a first order: Incoterms, landed "
         "price, supplier verification, letters of credit, HS codes, certificates and packing.",
 "trail": [("ISP Group", "index.html"), ("Guides", None)],
 "h1": "The questions that come <em>before the first order</em>",
 "sub": "Written down once, properly, because we were answering them on the phone over and "
        "over. No registration, no email gate, nothing to download.",
 "chips": ["12 guides", "No email gate", "Updated as rules change"],
 "lede": ("Why a trading company publishes this",
   "Half of what goes wrong in a first import goes wrong because nobody explained the rule "
   "before the order was placed. A buyer who understands where risk passes and who is liable "
   "for a classification is a better counterparty, and a better counterparty is cheaper for "
   "us too."),
 "body": [
  ("h2", "Start here if you have never imported"),
  ("p", "Read <a href=\"incoterms.html\">Incoterms</a> first, then "
        "<a href=\"landed-price.html\">what a landed price must include</a>. Between them "
        "they cover the two things that make quotations incomparable: the terms they are "
        "quoted on and the costs they leave out."),
  ("h2", "If you already have a supplier"),
  ("p", "Read <a href=\"verify-supplier.html\">how to verify a supplier is a factory</a> and "
        "<a href=\"letter-of-credit.html\">the letter of credit at sight</a>. The first "
        "catches the counterparty problem, the second is how you stop paying for a promise."),
  ("h2", "If you are buying food"),
  ("p", "Read <a href=\"veterinary-certificate.html\">veterinary certificates</a> before "
        "anything else, because an inadmissible establishment makes the price irrelevant. "
        "Then <a href=\"poultry-cuts.html\">cut nomenclature</a> and "
        "<a href=\"reefer-cold-chain.html\">the cold chain</a>."),
 ],
 "related": ("All guides", "Twelve, in the order we would read them.", GUIDE_LINKS),
 "ld": [{"@context": "https://schema.org", "@type": "CollectionPage",
         "url": HOST + "guides.html", "name": "Guides to importing",
         "hasPart": [{"@type": "Article", "name": t, "url": HOST + h}
                     for h, t, _ in GUIDE_LINKS]}],
}
