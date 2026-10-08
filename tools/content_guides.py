# -*- coding: utf-8 -*-
"""Этап 3: руководства под длинный хвост запросов."""
from content_core import HOST, ORG, GUIDE_LINKS

def rel(slug):
    """Три следующих руководства по кругу: при выборке «первые три» девять
    страниц из двенадцати оставались с одной входящей ссылкой."""
    order = [x[0] for x in GUIDE_LINKS]
    i = order.index(slug + ".html") if slug + ".html" in order else 0
    items = [GUIDE_LINKS[(i + k) % len(GUIDE_LINKS)] for k in range(1, 4)]
    items.append(("contact.html", "Send a requirement",
                  "Product, quantity and destination port is enough to start."))
    return ("Related guides", "The ones that usually get read next.", items)

UPDATED = "2026-10-08"

def article_ld(spec):
    return [{"@context": "https://schema.org", "@type": "Article",
             "headline": spec["title"].split(" | ")[0],
             "description": spec["desc"],
             "author": ORG, "publisher": ORG,
             "datePublished": UPDATED, "dateModified": UPDATED,
             "inLanguage": "en",
             "mainEntityOfPage": HOST + spec["slug"]}]

def t(slug, extra=None):
    return [("ISP Group", "index.html"), ("Guides", "guides.html"), (extra or slug, None)]

GUIDES_PAGES = [
{
 "slug": "landed-price",
 "title": "What a landed price must include | ISP Group",
 "desc": "Every line between a factory price and your own gate: freight, surcharges, "
         "insurance, terminal handling, duty, broker, inland leg and the costs that only "
         "appear when something goes wrong.",
 "trail": t("Landed price"),
 "h1": "What a landed price <em>has to include</em>",
 "sub": "A factory price is not a price. These are the lines between it and your gate, in "
        "the order they fall due, and the ones that are routinely left out.",
 "chips": ["12 cost lines", "Validity date", "Duty and broker", "Demurrage risk"],
 "lede": ("Why two quotations are almost never comparable",
   "Not because anyone is dishonest, but because each quotation stops at a different point "
   "on the journey. Until both are extended to the same point, the cheaper one is simply "
   "the one that stops earlier."),
 "body": [
  ("h2","The full list, origin to gate"),
  ("ul",["<b>Ex-works price</b> of the goods, at the agreed specification and pack.",
         "<b>Origin inland</b>, factory to port or terminal, including waiting time if the "
         "factory loads slowly.",
         "<b>Export clearance</b> and any origin documentation: certificate of origin, "
         "fumigation, inspection, phytosanitary or veterinary certification.",
         "<b>Terminal handling at origin</b>, which is quoted separately from freight far "
         "more often than buyers expect.",
         "<b>Ocean or air freight</b> for the actual equipment type, not a generic rate.",
         "<b>Surcharges</b>: bunker, currency, congestion, peak season, low-sulphur. These "
         "move independently of the base rate and are the usual reason a quoted price and "
         "an invoice disagree.",
         "<b>Insurance</b>, with the cover level stated rather than the word “insured”.",
         "<b>Terminal handling at destination</b> and port charges, which differ by port on "
         "the same lane.",
         "<b>Customs duty</b> at the correct classification, plus any trade remedy deposit.",
         "<b>Import VAT or GST</b>, usually recoverable for a registered importer but still "
         "cash out of the door on the day.",
         "<b>Customs broker</b> and any inspection or examination fee the authority raises.",
         "<b>Inland delivery</b> to your own gate, plus unloading if you have no dock."]),
  ("h2","The three that are always missing"),
  ("p","<b>Demurrage and detention.</b> Free time at the destination is finite, and the clock "
       "runs whether or not your paperwork is ready. On a lane where clearance is slow this "
       "is not an edge case, it is a budget line. Ask how many free days the quoted rate "
       "includes and what the daily rate is afterwards."),
  ("p","<b>Bank charges on both legs.</b> A letter of credit, a documentary collection and "
       "even a plain transfer all carry charges at the issuing bank, the advising bank and "
       "any intermediary. They are small individually and they are allocated in writing or "
       "they are argued about later."),
  ("p","<b>The cost of the specification being wrong.</b> Not a line you can quote, but it "
       "is the largest number on this page when it happens. It is why the specification work "
       "comes before the pricing work and not after it."),
  ("h2","Rate validity is part of the price"),
  ("p","Freight rates are quoted with an expiry and they move sharply. A landed price without "
       "a validity date is a landed price for an unknown day. We state the date the freight "
       "component is good until, and we say which lines are fixed and which float."),
  ("note","On most lanes the goods price is firm for longer than the freight price. Splitting "
          "the two in the quotation lets a buyer lock the part that can be locked instead of "
          "re-tendering the whole thing."),
  ("h2","Where VAT confuses the comparison"),
  ("p","Import VAT or GST is usually recoverable by a registered importer, so it does not "
       "belong in a margin calculation. It absolutely belongs in a cash flow calculation, "
       "because it is paid at clearance and recovered weeks or months later. A buyer who "
       "nets it out of the landed price and forgets the timing runs out of working capital "
       "on the third container rather than the first."),
  ("h2","What we hand over"),
  ("p","One number at your door, the build-up behind it line by line, the validity date on "
       "the freight component, and the Incoterm and named place the number is quoted at. If "
       "we are quoting two bases, the difference between them is the honest cost of the "
       "logistics portion, which is the most useful single figure a buyer can have."),
 ],
 "faq": [("Why does your landed price look higher than a FOB quote I have?",
          "Because a FOB quote stops at the origin port rail and a landed price stops at your "
          "gate. Add freight, surcharges, insurance, destination handling, duty, broker and "
          "the inland leg to the FOB number and then compare."),
         ("Can you fix the price for a whole year?",
          "The goods portion, often. The freight portion, rarely, because carriers do not "
          "offer it on most lanes and anyone who does is pricing in the risk. We split the "
          "two so you can fix what is fixable."),
         ("Is duty included in your quote?",
          "Yes, at the classification we have agreed in writing with you before the order. "
          "If a trade remedy order touches the product, the deposit is shown as a separate "
          "line because it is not an ordinary duty and it may not be the final liability.")],
},
{
 "slug": "verify-supplier",
 "title": "How to verify a supplier is a factory | ISP Group",
 "desc": "Business licence, export right, scope of business and the bank account name: the "
         "checks that separate a manufacturer from a trading company, and the ones that "
         "catch a lookalike domain.",
 "trail": t("Verifying a supplier"),
 "h1": "How to verify a supplier <em>is actually a factory</em>",
 "sub": "Both kinds of counterparty answer your enquiry within an hour and both send "
        "photographs of a plant. Four checks separate them, and one of the four catches "
        "almost every impersonation.",
 "chips": ["Licence", "Export right", "Scope of business", "Beneficiary name"],
 "lede": ("Why it matters, in one sentence",
   "A factory can re-run a batch. A trading company has to persuade someone else to re-run "
   "it, at its own cost, with no leverage, which is why the difference shows up only when "
   "something has already gone wrong."),
 "body": [
  ("h2","Check one: the registration document"),
  ("p","Every registered company has one, and it names the legal entity, the registration "
       "number, the registered capital and the scope of business. In China that is the "
       "business licence with its unified social credit code; elsewhere it has a different "
       "name and the same function."),
  ("p","Read the scope of business rather than the letterhead. A company whose registered "
       "scope is wholesale and import-export is not a manufacturer, whatever the website "
       "says. This is not a hidden fact, it is printed on the document they will send you if "
       "you ask."),
  ("h2","Check two: the right to export"),
  ("p","Manufacturing and exporting are separate permissions in many jurisdictions. A real "
       "factory may have no export right at all and may ship through an agent, which is "
       "legitimate and changes who your contract is with, who issues the invoice and who is "
       "named on the bill of lading."),
  ("p","If the entity that signs your contract is not the entity that manufactures and not "
       "the entity that exports, there are three parties and you are relying on the "
       "relationships between two of them that you cannot see."),
  ("h2","Check three: the beneficiary name on the proforma"),
  ("p","This is the one that catches almost everything. The bank account on the proforma "
       "invoice has to carry the same name as the registration document. Not a similar name, "
       "not the trading name, not the name of a director, not an account in a third country "
       "“because of currency controls”."),
  ("note","A mismatch between the seller name and the beneficiary name is not an "
          "administrative detail to be smoothed over. It is the whole question. Every "
          "payment-diversion fraud in this trade runs through exactly that gap."),
  ("p","The related problem is the lookalike domain. Around well-known exporters there is a "
       "layer of sites that copy the name and offer their own sales addresses. The rule is "
       "simple: write only to the domain published on the company's own official site, and "
       "treat any address on a different domain as unverified until proven otherwise."),
  ("h2","Check four: something only a factory can answer"),
  ("p","Ask a production question that a trader cannot answer without a phone call: the "
       "cycle time on the line that would make your item, the changeover time between sizes, "
       "the name of the controller on the main machine, how many shifts run in a normal week, "
       "and what the minimum run is before a changeover stops being worth it."),
  ("p","A factory answers in one message. A trader answers tomorrow, in different words from "
       "the ones they used yesterday."),
  ("h2","What an audit adds, and when it is worth it"),
  ("p","A physical factory audit by a third party adds what documents cannot: that the plant "
       "exists at the registered address, that the equipment matches the claim, and that the "
       "quality system is operated rather than framed. It costs a fraction of a container and "
       "it is worth it on a first order of any size, on anything safety-critical, and on any "
       "supplier found through a marketplace rather than through a reference."),
  ("p","We do these checks before quoting rather than before ordering, because a price from a "
       "counterparty that will not survive the check is not information."),
 ],
 "faq": [("Is it wrong to buy through a trading company?",
          "No. For a small quantity or an assortment across several plants a trading company "
          "is often the right answer and costs less than dealing with five factories. What is "
          "wrong is a trading company presenting itself as a manufacturer, because then you "
          "are pricing a risk you do not know you are carrying."),
         ("The supplier wants payment to an account in another country. Is that normal?",
          "It is a stop sign. There are legitimate reasons a group banks offshore, and they "
          "can all be evidenced in writing on company letterhead with the group structure. "
          "Until that evidence exists, treat it as the most common pattern in payment fraud."),
         ("How long do these checks take?",
          "The document checks take a day or two. A third-party factory audit takes one to "
          "two weeks to schedule and a day to perform. Both are shorter than the delay caused "
          "by a failed first shipment.")],
},
{
 "slug": "letter-of-credit",
 "title": "A letter of credit at sight | how it works and what it costs",
 "desc": "What a documentary credit protects, why banks deal in documents and not goods, "
         "what a discrepancy costs, and when a letter of credit is the wrong instrument.",
 "trail": t("Letter of credit"),
 "h1": "The letter of credit, <em>and what it actually protects</em>",
 "sub": "It does not guarantee that the goods are good. It guarantees that a bank pays "
        "against documents that comply. Understanding that one sentence prevents most of "
        "the disappointment.",
 "chips": ["UCP 600", "Irrevocable by default", "Documents, not goods", "21 days to present"],
 "lede": ("The instrument solves one problem and only one",
   "A seller does not want to ship before being paid. A buyer does not want to pay before "
   "being shipped to. A documentary credit puts a bank between them so that neither has to "
   "go first. Everything else people expect from it, it does not do."),
 "body": [
  ("h2","Banks deal in documents, not in goods"),
  ("p","This is the governing principle of the rules that almost every credit is issued "
       "under, the ICC Uniform Customs and Practice for Documentary Credits. The bank never "
       "sees the cargo. It examines whether the presented documents comply on their face "
       "with the credit, and if they do it pays, even if the container turns out to hold "
       "the wrong goods."),
  ("p","Which means the protection a credit gives a buyer is exactly as good as the document "
       "list written into it. A credit that calls for an inspection certificate issued by a "
       "named third party protects the buyer. A credit that calls only for an invoice and a "
       "bill of lading protects the seller."),
  ("h2","Sight, usance and what each one costs the other side"),
  ("p","A credit payable <b>at sight</b> pays on presentation of compliant documents, which "
       "in practice is a few banking days after shipment. A <b>usance</b> credit pays a "
       "stated number of days later, typically 30, 60 or 90 from the bill of lading date."),
  ("p","The difference is not a formality, it is the whole financing question. At sight, the "
       "seller is funded while the vessel is at sea. At 90 days, the seller is lending the "
       "buyer the value of the cargo for three months and will price that in, openly or "
       "otherwise. A buyer asking for long usance is asking for credit, and credit has a "
       "price whether or not it appears as a line."),
  ("h2","Confirmed or unconfirmed"),
  ("p","An unconfirmed credit carries the risk of the issuing bank and of its country. A "
       "confirmed credit adds a second bank, usually in the seller's country, which "
       "undertakes to pay independently. Confirmation costs a fee that scales with the "
       "perceived risk of the issuing bank, and on some corridors that fee is the honest "
       "market price of the country risk."),
  ("note","If a seller insists on confirmation and the buyer finds the cost unreasonable, "
          "the disagreement is not really about the fee. It is about what the market thinks "
          "of the issuing bank, and that is worth knowing before the first shipment."),
  ("h2","Discrepancies, which is where credits actually fail"),
  ("p","Compliance is strict. A spelling difference between the invoice and the credit, a "
       "bill of lading dated one day outside the shipment window, a certificate signed by "
       "the wrong function, an amount expressed in a different form of words: any of these "
       "is a discrepancy, and a discrepant presentation can be refused."),
  ("p","In practice most discrepancies are waived by the buyer, but the waiver is the "
       "buyer's to give, which means a discrepant seller has lost the protection they paid "
       "for and is back to trusting the buyer. Each discrepancy also carries a bank fee."),
  ("p","Two mechanical points prevent most of it. The presentation period is finite, "
       "normally 21 calendar days after shipment and always within the credit's expiry, so "
       "documents have to be assembled fast. And the draft of the credit should be reviewed "
       "by the beneficiary before it is issued, not after, because amending a credit costs "
       "money and time and needs both sides to agree."),
  ("h2","When a credit is the wrong instrument"),
  ("ul",["<b>Small shipments.</b> The bank charges on both legs can be a visible share of a "
         "small container's value. A documentary collection is cheaper and gives less "
         "protection; staged transfer against milestones gives different protection again.",
         "<b>Trusted repeat business.</b> After a dozen clean shipments the credit is paying "
         "for a risk neither side believes in.",
         "<b>A counterparty you have not verified.</b> A credit does not make an unverified "
         "producer safe. It only ensures you pay against paper. Verification comes first."]),
  ("h2","What we do"),
  ("p","We contract with the producer in our own name and with the buyer separately, and we "
       "mirror the settlement terms on both legs so the gap between them does not become our "
       "working capital by accident. We review the credit draft before issuance, we allocate "
       "the bank charges on each leg in writing, and we prefer the document list to include "
       "something the buyer actually cares about rather than only what the bank needs."),
 ],
 "faq": [("Does a letter of credit protect me if the goods are defective?",
          "Only indirectly. The bank pays against documents, not goods. You get protection by "
          "writing the right documents into the credit, for example an inspection certificate "
          "from a named third party, so that defective goods cannot produce a compliant "
          "presentation."),
         ("Who pays the bank charges?",
          "Whoever the contract says. The default is that each side pays the charges of banks "
          "in its own country, but it is routinely varied and it should be written down. "
          "Unallocated charges are a predictable argument at the worst moment."),
         ("Is an irrevocable credit really irrevocable?",
          "Under the current ICC rules every credit is irrevocable unless it says otherwise, "
          "and it cannot be amended or cancelled without the agreement of the beneficiary and "
          "any confirming bank. What it can be is discrepant on presentation, which is a "
          "different and far more common problem.")],
},
{
 "slug": "customs-data-pricing",
 "title": "How customs data shows the real price | ISP Group",
 "desc": "A quotation is what a seller wants. A customs unit value is what the market paid. "
         "Where to find the data, how to read it, and the four traps in it.",
 "trail": t("Customs data"),
 "h1": "A quotation is an opinion. <em>Customs data is a record</em>",
 "sub": "Declared value divided by declared net weight gives the price at which goods really "
        "crossed a border, with every discount the seller actually gave already inside the "
        "number.",
 "chips": ["Unit value", "By origin", "By commodity code", "Four traps"],
 "lede": ("Why we benchmark before we negotiate",
   "Three quotations tell you what three sellers hope for. They do not tell you whether the "
   "best of the three is good. Customs statistics do, because they are built from "
   "declarations that someone signed and a customs authority accepted."),
 "body": [
  ("h2","What the number is"),
  ("p","Trade statistics record, for each commodity code and each partner country, the "
       "declared value and the declared net weight of what actually moved in a period. "
       "Dividing one by the other gives a unit value: the average price per kilogram at "
       "which that commodity crossed that border from that origin."),
  ("p","It is an average rather than a quotation, and that is the point. It already contains "
       "the volume discounts, the seasonal softness and the deals that were never published. "
       "A seller quoting well above the running unit value for the same code and the same "
       "lane is asking you to pay for something, and the conversation starts there."),
  ("h2","Where to get it"),
  ("ul",["<b>UN Comtrade</b> covers most countries at the six-digit level and is the fastest "
         "way to compare several origins into one destination.",
         "<b>National sources</b> are more detailed. The United States publishes down to ten "
         "digits, the European Union eight, and several countries, Brazil among them, run "
         "open query tools over their own export data at full code level.",
         "<b>Mirror statistics</b>, meaning the exporter's declaration of what it sent you, "
         "are often published faster than the importer's own figures and are a useful "
         "cross-check when a destination reports slowly."]),
  ("h2","The four traps"),
  ("p","<b>Trap one: CIF against FOB.</b> Most countries record imports at CIF value and "
       "exports at FOB. Comparing an import unit value with an export unit value therefore "
       "compares a delivered price with a factory-gate price, and the gap is the freight, "
       "not the margin. Compare like with like or adjust for it explicitly."),
  ("p","<b>Trap two: the basket inside the code.</b> A six-digit code can hold several "
       "commercial products at very different prices. A code covering frozen poultry cuts "
       "holds wings, legs and tails together, and the average moves with the mix rather than "
       "with the market. Go as deep as the national code allows and read the description."),
  ("p","<b>Trap three: thin flows.</b> A unit value built on fifty tonnes in a year is one "
       "or two shipments and can be anything, including a sample consignment or a gift. We "
       "set a weight floor before we look at a number, and we ignore everything below it."),
  ("p","<b>Trap four: related-party pricing.</b> Shipments between two arms of the same group "
       "are declared at transfer prices that serve a tax purpose, not a market one. On lanes "
       "dominated by a single integrated producer this can pull the whole average."),
  ("note","None of the four makes the data useless. They make it data that has to be read "
          "rather than quoted. Used properly it is still the only published number in this "
          "trade that someone had to sign."),
  ("h2","How we use it in a negotiation"),
  ("p","Before approaching producers on a lane we pull the destination's import unit values "
       "by origin and by code for the most recent full periods, drop the thin flows, and set "
       "a target band rather than a target number. The band is what we negotiate against, "
       "and we say to the seller what it is based on."),
  ("p","That changes the conversation from haggling to arithmetic, and it regularly moves "
       "the achievable price by a fifth or more. It also decides which origin to approach "
       "first, which is often worth more than the discount itself."),
 ],
 "faq": [("Is customs data public?",
          "Yes, in aggregate. Country-to-country flows by commodity code and period are "
          "published by the United Nations and by most national statistics offices at no "
          "cost. Shipment-level records with named companies are a separate, commercial "
          "product in the countries that release them at all."),
         ("How current is it?",
          "Typically one to three months behind for the fastest reporters and longer for "
          "others. On a volatile commodity that lag matters and the data sets the band "
          "rather than the price. On a stable one it is close enough to negotiate against."),
         ("Can a seller argue the data is wrong for their product?",
          "Often, and sometimes they are right, because of the basket problem. The useful "
          "answer is to ask what in their product justifies the gap: a grade, a "
          "certification, a pack, a lead time. If there is a real answer it is worth paying "
          "for. If there is not, the gap is the negotiation.")],
},
{
 "slug": "hs-code",
 "title": "Who is liable for the HS code | classification and duty",
 "desc": "The importer of record is liable for the tariff classification, not the seller who "
         "typed it. How the code is structured, what a wrong one costs, and how to make it "
         "binding in advance.",
 "trail": t("HS codes"),
 "h1": "The HS code is <em>the importer's problem</em>",
 "sub": "The seller types a number on the invoice and has no liability for it. The importer "
        "of record declares it, pays on it and answers for it. That asymmetry is worth "
        "understanding before the order, not at the border.",
 "chips": ["6 digits international", "8 to 10 national", "Binding rulings", "Retroactive"],
 "lede": ("The one line on an invoice nobody negotiates",
   "Buyers negotiate the price to the last cent and accept the tariff code without reading "
   "it, although the code can move the delivered cost by more than any discount ever "
   "achieved."),
 "body": [
  ("h2","How the number is built"),
  ("p","The first six digits are the Harmonized System, maintained by the World Customs "
       "Organization and identical in every country that uses it, which is almost all of "
       "them. Beyond six digits each territory extends the code for its own tariff and "
       "statistics: eight digits in the European Union, ten in the United States, and "
       "various lengths elsewhere."),
  ("p","Which means a six-digit code agreed with a seller is not a classification. It is the "
       "first two thirds of one, and the duty rate lives in the part that was not agreed."),
  ("h2","What a wrong code costs"),
  ("ul",["<b>Underpaid duty</b>, recoverable from the importer with interest, often years "
         "later during an audit rather than at entry.",
         "<b>Penalties</b>, which in most jurisdictions scale with whether the error is "
         "treated as negligence or something worse.",
         "<b>A missed preference.</b> A code that sits outside a trade agreement's coverage "
         "pays full duty on goods that qualified for zero.",
         "<b>An unexpected trade remedy.</b> Antidumping and countervailing scope is defined "
         "by product description and anchored to codes. A classification that lands inside "
         "a scope can carry a deposit larger than the goods.",
         "<b>A licence requirement</b> that applies to one code and not its neighbour, "
         "discovered when the entry is rejected."]),
  ("h2","Classify on what the thing is, not on what it is for"),
  ("p","The system has interpretive rules, and the most common amateur error is classifying "
       "by intended use when the structure classifies by material, function or state. The "
       "second most common is accepting the seller's domestic code, which was chosen for the "
       "seller's export statistics and may have no counterpart at your end."),
  ("p","Sets, kits and goods made of several materials have their own rules, and so do parts, "
       "which are sometimes classified with the machine and sometimes on their own. These "
       "are exactly the cases where a confident guess is expensive."),
  ("h2","Make it binding before you order"),
  ("p","Most customs administrations issue advance rulings that bind them for a period: in "
       "the United States a binding ruling from the customs authority, in the European Union "
       "Binding Tariff Information, with equivalents elsewhere. You describe the product, "
       "they issue the classification, and it holds."),
  ("note","On a repeating programme this is the highest-return paperwork in the whole "
          "transaction. It is free or nearly free, it takes weeks rather than months, and it "
          "converts the largest open variable in the landed cost into a fixed one."),
  ("h2","What we do"),
  ("p","We agree the classification in writing with the buyer before the order, we state it "
       "in the landed price so the duty line can be checked, and on any product near a scope "
       "boundary or a preference threshold we recommend an advance ruling and say why. Where "
       "the seller's code differs from ours we reconcile it before the invoice is issued "
       "rather than after the container has sailed."),
 ],
 "faq": [("The seller gave me a code. Can I just use it?",
          "You can declare it, and you will own the consequences. The seller chose it for "
          "their own export statistics in their own tariff, which beyond six digits is not "
          "your tariff. Treat it as a starting point and confirm it at your end."),
         ("How do I get a binding ruling?",
          "By applying to the customs administration of the importing country with a full "
          "product description and usually a sample. In the United States it is a binding "
          "ruling, in the European Union Binding Tariff Information. It takes weeks and it "
          "holds for years."),
         ("Can a classification change after clearance?",
          "Yes. Customs can review entries after the fact within the statutory period and "
          "reassess, which is why an underpaid duty surfaces as an audit finding with "
          "interest rather than as a problem at the port.")],
},
{
 "slug": "ispm-15",
 "title": "ISPM 15: how a pallet stops a container | wood packaging",
 "desc": "What ISPM 15 covers, the treatment codes, how to read the mark, which wood is "
         "exempt, and why the check belongs at loading rather than at arrival.",
 "trail": t("ISPM 15"),
 "h1": "How a pallet <em>stops a container</em>",
 "sub": "Untreated wood packaging is refused at the border of most countries in the world. "
        "The cargo inside it is irrelevant, the cost falls on the importer, and the whole "
        "thing is preventable with a photograph taken at loading.",
 "chips": ["IPPC mark", "HT &middot; DH &middot; MB", "6 mm exemption",
           "Checked before sealing"],
 "lede": ("A rule about insects that behaves like a rule about money",
   "Solid wood carries pests between continents. The international standard that addresses "
   "it is adopted by most trading nations, and enforcement is at the border, where the only "
   "available remedies are expensive."),
 "body": [
  ("h2","What is covered"),
  ("p","Wood packaging material: pallets, crates, cases, boxes, drums, dunnage, blocking and "
       "bracing. If it is solid wood and it is holding your cargo in place, it is in scope."),
  ("p","Processed wood-based materials are out of scope, because the manufacturing process "
       "already destroys pests. That includes plywood, oriented strand board, particle board "
       "and veneer, and in general thin wood below the thickness threshold the standard "
       "sets. Wood that has been fully stripped of bark and processed into panels is not the "
       "problem the rule addresses."),
  ("h2","The treatments and the mark"),
  ("p","Approved treatments are heat treatment to a specified core temperature and duration, "
       "dielectric heating, and fumigation, with the fumigant in question being phased out in "
       "many jurisdictions on environmental grounds. Heat treatment is the normal commercial "
       "answer."),
  ("p","Treated material carries a stamp with four elements: the IPPC wheat symbol, the "
       "two-letter country code, a unique number identifying the treatment provider, and the "
       "treatment code. The mark must be legible, permanent and on at least two opposite "
       "sides of the item."),
  ("note","A hand-written stamp, a mark on one side only, a mark that is illegible, or a "
          "pallet that has been repaired with untreated timber after being marked: each of "
          "these fails, and each is common."),
  ("h2","What happens when it fails"),
  ("p","The options at the border are all bad and all at the importer's cost: treatment at "
       "the port where that is available, re-export of the packaging, destruction of the "
       "packaging, or in the worst case refusal of the whole consignment. On top of the "
       "direct cost the container sits, and demurrage accrues from the day it lands."),
  ("p","The timing is what makes this expensive. A non-compliant pallet costs a few tens of "
       "dollars to replace at the factory and several thousand to resolve at the destination."),
  ("h2","Where the check belongs"),
  ("ul",["At loading, before the container is sealed, not at arrival.",
         "Photograph the mark on the pallets actually used, not on a sample pallet in the "
         "corner of the warehouse.",
         "Photograph the dunnage and the bracing too, because loose timber used to chock a "
         "machine is wood packaging and is caught by the same rule.",
         "Where a factory repairs pallets in house, confirm that repair timber is also "
         "treated and that the pallet is re-marked.",
         "Put the requirement in the purchase order in writing, with the treatment and the "
         "mark named, so a failure is a breach rather than a misunderstanding."]),
  ("h2","Who actually gets caught"),
  ("p","Not usually the exporters who ship every week on standard pallets. It is first-time "
       "shippers, factories that normally sell domestically, out-of-gauge machinery crated "
       "specially for one shipment, and consolidated loads where one of six suppliers used "
       "its own timber. All four are situations we see at the start of a new lane, which is "
       "exactly when nobody is looking for it."),
 ],
 "faq": [("Does this apply to plywood pallets?",
          "No. Processed wood-based materials such as plywood, OSB and particle board are "
          "out of scope because the manufacturing process destroys pests. The rule targets "
          "solid wood."),
         ("Our supplier says the pallets are treated. Is that enough?",
          "No, because the mark is the evidence and only the mark counts at the border. Ask "
          "for photographs of the stamp on the pallets going into your container, taken at "
          "loading. It costs nothing and it is the only proof that travels."),
         ("What if the container arrives and the pallets are not marked?",
          "The options are treatment at the port where available, re-export or destruction of "
          "the packaging, or refusal of the consignment, all at the importer's cost, with "
          "demurrage running throughout. There is no version of this that is cheap.")],
},
{
 "slug": "container-loading",
 "title": "FCL, LCL and consolidation | what fits and what it costs",
 "desc": "Container capacities, why dense cargo fills on weight and light cargo on volume, "
         "when LCL is false economy, and how consolidation keeps a trial order on full "
         "container economics.",
 "trail": t("Container loading"),
 "h1": "FCL, LCL <em>and consolidation</em>",
 "sub": "A container fills on weight or on volume, almost never on both. Which one it fills "
        "on decides the box, the price per unit and whether sharing it with someone else "
        "makes sense.",
 "chips": ["20ft &middot; 40ft &middot; 40HC", "Weight or volume", "VGM required",
           "Consolidated LCL"],
 "lede": ("The question to answer before asking for a freight rate",
   "Is this cargo heavy or bulky. Steel, tile, cement and paper reach the weight limit with "
   "the box half empty. Packaging, insulation and finished consumer goods run out of space "
   "with tonnes to spare. The two are priced in opposite directions."),
 "body": [
  ("h2","What the boxes hold"),
  ("p","Approximate working figures, which vary by operator, by equipment age and by the "
       "road weight limits at each end. Confirm them against the actual booking rather than "
       "planning to the last kilogram."),
  ("ul",["<b>20ft general purpose</b>: roughly 33 cubic metres of space. Dense cargo "
         "normally reaches its weight limit well before that, which is why a 20ft box that "
         "looks half empty is often the correct and cheaper choice for steel or tile.",
         "<b>40ft general purpose</b>: roughly twice the volume of a 20ft, and not twice the "
         "payload. For heavy cargo two 20ft boxes usually beat one 40ft.",
         "<b>40ft high cube</b>: around nine or ten cubic metres more than a standard 40ft, "
         "for the same payload. The right box for light, bulky cargo.",
         "<b>40ft reefer</b>: less internal volume than a dry box because of the insulation "
         "and the machinery, and about 25 tonnes net on a typical frozen food loading plan."]),
  ("note","Road weight limits at origin and destination often bind before the container's "
          "own rating does. A box that is legal at sea can be illegal on the road at one "
          "end, and that is discovered by the haulier, not by the carrier."),
  ("h2","Verified gross mass is not optional"),
  ("p","Under the international convention on safety of life at sea, the shipper must declare "
       "a verified gross mass for every packed container before it is loaded on a vessel, "
       "obtained either by weighing the packed container or by weighing the cargo and adding "
       "the certified tare. A container without a declared VGM does not get loaded."),
  ("p","In practice this is handled by the forwarder, and in practice it occasionally is not, "
       "with a container rolled to the next vessel as the result. On a new lane we confirm "
       "who is producing the VGM figure before the booking rather than on the cut-off day."),
  ("h2","When LCL is false economy"),
  ("p","Less than container load looks cheaper because you pay for a share. The problem is "
       "what is attached to that share: destination charges on LCL are per cubic metre and "
       "they are high, the consignment is handled at a deconsolidation warehouse at both "
       "ends, and the transit time is longer because the box waits for other cargo."),
  ("p","The rough rule is that below about a third of a container, LCL wins. Above about "
       "half, a full container usually wins even if some of it is air. In between it depends "
       "entirely on the destination charges at that specific port, and those are worth asking "
       "for by name rather than assuming."),
  ("h2","Consolidation: a middle option most buyers do not ask for"),
  ("p","Several suppliers in the same region can be loaded into one container at the port of "
       "loading. The buyer gets full container economics and one bill of lading instead of "
       "four, which also means one customs entry instead of four."),
  ("p","Two costs come with it. Consolidation adds roughly a week to the schedule, because "
       "the box waits for the slowest supplier. And one packing list has to reconcile against "
       "several suppliers' cartons, which is exactly the kind of discrepancy a customs "
       "authority resolves by inspecting, so the counting and the photography at the "
       "consolidation warehouse are not optional."),
  ("h2","Loading practice that prevents claims"),
  ("ul",["Dunnage so the load cannot shift, and a photograph showing it in place.",
         "Product off the walls and the floor on anything hygroscopic, because the "
         "mechanism for wet cargo is condensation on the container roof at night, not rain.",
         "Heavy items low and evenly distributed, not all against one wall; an unbalanced "
         "container is a road safety problem at the far end.",
         "Wood packaging treated and marked, checked and photographed before sealing.",
         "The seal number recorded and photographed, and matched against the bill of lading."]),
 ],
 "faq": [("Should I use a 20ft or a 40ft container?",
          "If the cargo is dense, two 20ft boxes usually beat one 40ft, because payload does "
          "not double with volume. If the cargo is light and bulky, a 40ft high cube is the "
          "cheapest cubic metre you can buy."),
         ("Is LCL cheaper for a small order?",
          "Below roughly a third of a container, usually yes. Above roughly half, usually no, "
          "because LCL destination charges are per cubic metre and high. In between, ask for "
          "the destination charges at that specific port before deciding."),
         ("Can you combine several of our suppliers into one container?",
          "Yes, that is consolidation, and it is how most trial orders should ship. It adds "
          "about a week while the box waits for the slowest supplier, and it needs careful "
          "counting at the warehouse so the packing list reconciles.")],
},
{
 "slug": "veterinary-certificate",
 "title": "Veterinary certificates for frozen meat | ISP Group",
 "desc": "Why an establishment number comes before a price, how export certification works "
         "for United States and European Union origin, and what to ask a seller first.",
 "trail": t("Veterinary certificates"),
 "h1": "The establishment number comes <em>before the price</em>",
 "sub": "Frozen meat does not enter a country on a commercial invoice. It enters on a "
        "veterinary health certificate issued for a specific plant, in a form the "
        "destination accepts. If the plant is not approved, the price is irrelevant.",
 "chips": ["Establishment number", "Certificate form", "Per destination",
           "Written confirmation"],
 "lede": ("The cheapest offer in this trade is usually the one that cannot ship",
   "Approval is granted plant by plant and destination by destination. An establishment "
   "cleared for one West African country is not automatically cleared for its neighbour, "
   "and the lists change."),
 "body": [
  ("h2","What the certificate is"),
  ("p","A veterinary health certificate is an official document issued by the competent "
       "authority of the exporting country, attesting that the consignment comes from an "
       "approved establishment, was produced under official inspection and meets the animal "
       "and public health conditions the importing country has set."),
  ("p","It is not a commercial document and the seller cannot issue it. It travels with the "
       "consignment, it is presented at the border post of entry, and without it the cargo "
       "does not clear, whatever the invoice says."),
  ("h2","United States origin"),
  ("p","Export certification runs through the federal food safety inspection service. The "
       "requirements for each destination country, including the certificate form and any "
       "additional attestations, are published in an export library maintained for that "
       "purpose and updated as destinations change their rules."),
  ("p","Two practical points follow. Some destinations are handled through the electronic "
       "system and some still require a paper certificate, which changes the lead time at "
       "the loading end. And a destination that is not listed is not necessarily closed, "
       "but it does mean the requirements have to be established in writing before anything "
       "is loaded rather than assumed."),
  ("h2","European Union origin"),
  ("p","The equivalent is the competent authority of the member state, with certificates "
       "issued through the Union's own trade control system. The establishment has to hold "
       "the relevant approval, and for third-country export the certificate model is the one "
       "agreed between the Union and the destination."),
  ("h2","What to ask a seller, in this order"),
  ("ul",["<b>The establishment number</b>, as registered, not the company's trading name.",
         "<b>Written confirmation that the establishment is approved for the destination</b>, "
         "not for the region and not for a neighbouring country.",
         "<b>Which certificate form will be issued</b>, and whether it is electronic or "
         "paper, because that sets the lead time.",
         "<b>Who signs it</b> and how long signature normally takes at that plant.",
         "<b>What happens if the destination changes its requirements</b> between the "
         "contract and the loading date, which on some corridors is a live possibility."]),
  ("note","We do not treat a seller's verbal assurance on admissibility as an answer. The "
          "number is checked, and where the destination is ambiguous the certificate form is "
          "identified in writing before any money moves."),
  ("h2","Why this is the first question and not the fifth"),
  ("p","Because it is the only one of the commercial variables that cannot be fixed later. A "
       "price can be renegotiated, a pack can be changed, a shipment date can slip. An "
       "inadmissible establishment cannot be made admissible inside a shipment cycle, and a "
       "container of frozen product sitting at a border post while someone investigates is "
       "the most expensive single failure available on this lane."),
  ("p","The rest of what matters on this corridor, from cut nomenclature to the cold chain, "
       "is on the <a href=\"west-africa.html\">West Africa corridor page</a>."),
 ],
 "faq": [("Can a seller export to any country once it has an export licence?",
          "No. Approval is per establishment and per destination. A plant cleared for one "
          "country may not be cleared for its neighbour, and the lists are revised. That is "
          "why the question is about the specific destination, not about export in general."),
         ("How long does it take to get a plant approved for a new destination?",
          "It is a government-to-government process and it is measured in months or longer, "
          "not weeks. For a shipment you need now, the answer is to find an already-approved "
          "establishment rather than to wait."),
         ("Who pays if the consignment is rejected at the border?",
          "That depends entirely on how the contract allocates it, which is why it is "
          "written down before the first shipment. We mirror the condition on both legs so "
          "the risk does not land in the gap between the supply contract and the sale.")],
},
{
 "slug": "poultry-cuts",
 "title": "Wing, drumette, flat: four different products | poultry cuts",
 "desc": "Why a quotation for wings is not a quotation: whole wing, two-joint, drumette and "
         "mid-joint flat are four products with four prices, and tom is not hen.",
 "trail": t("Poultry cuts"),
 "h1": "“Wings” is <em>not a product</em>",
 "sub": "A whole wing has three sections. Remove the tip and it is a two-joint. Separate the "
        "two remaining sections and you have two more products. Four items, four prices, "
        "four different buyers.",
 "chips": ["3-joint &middot; 2-joint", "Drumette &middot; flat &middot; tip",
           "Tom &middot; hen", "Per line, per Incoterm"],
 "lede": ("The commonest reason two offers cannot be compared",
   "Not the Incoterm, not the pack, not the payment terms. It is that the two sellers are "
   "quoting different parts of the bird and both are calling it the same thing."),
 "body": [
  ("h2","The anatomy, once, clearly"),
  ("p","A whole wing has three sections joined end to end. Closest to the body is the "
       "<b>drumette</b>, the small drumstick-shaped piece with a single bone. In the middle "
       "is the <b>mid-joint</b>, also called the flat or the wingette, with two parallel "
       "bones. At the end is the <b>tip</b>, which has very little meat."),
  ("ul",["<b>Whole wing, three joint</b>: all three sections, intact.",
         "<b>Two joint wing</b>: drumette plus flat, tip removed. This is what most markets "
         "mean by a wing for retail or food service.",
         "<b>Drumette</b> alone: the premium section, priced accordingly.",
         "<b>Mid-joint flat</b> alone: sold separately, strong demand in some markets and "
         "almost none in others.",
         "<b>Tips</b>: a by-product with its own narrow market, mostly for stock and "
         "processing."]),
  ("note","A seller quoting “wings” without naming the configuration can be offering any "
          "of the first four, and the difference between the cheapest and the dearest is "
          "not a rounding error."),
  ("h2","Tom and hen are not grades of the same thing"),
  ("p","In turkey the male and female lines are raised to different weights and give "
       "different piece sizes. For a processor buying to a portion weight, they are not "
       "interchangeable, and a shipment of the wrong one is unusable rather than merely "
       "disappointing. Specify which line, and specify the piece weight range."),
  ("h2","The other parts, and why they have their own markets"),
  ("p","Legs, thighs, drumsticks, backs, necks, tails and paws all trade separately and each "
       "has a geography. A cut that is a by-product in one market is a staple in another, "
       "which is the whole reason the international trade in poultry parts exists: a bird is "
       "disassembled and each part sold where it is worth most."),
  ("p","Two commercial consequences. First, prices for different parts of the same bird move "
       "independently, so a basket quoted as a single average price hides which line is "
       "expensive. Second, availability is driven by what the rest of the world is buying, "
       "which is why a line can be unobtainable in a month when the whole bird is cheap."),
  ("h2","What a usable enquiry looks like"),
  ("ul",["The cut named by anatomy, not by category.",
         "Tom or hen for turkey, and the piece weight range.",
         "The pack: carton weight, block frozen or individually quick frozen, net or gross.",
         "The Incoterm and the named port, per destination port if there is more than one.",
         "Quantity per line, per month, not as a single basket figure.",
         "The establishment number, because an inadmissible plant makes all of the above "
         "irrelevant."]),
  ("p","We send every enquiry on this corridor in that form and ask for the price per line "
       "on the same basis. It takes one extra paragraph to write and it removes two weeks of "
       "correspondence."),
  ("h2","Why the basket matters more than the discount"),
  ("p","On a mixed programme the mix is worth more than the negotiation. Shifting the "
       "proportion of the container towards the lines with the widest spread between the "
       "buying market and the selling market can be worth more per month than every cent "
       "squeezed out of the supplier. That conversation belongs with the buyer at the start, "
       "not after the first shipment."),
 ],
 "faq": [("What is the difference between a wingette and a flat?",
          "Nothing. They are two names for the mid-joint section, the one with two parallel "
          "bones. The confusion is real enough that we write “mid-joint flat” in "
          "enquiries to remove it."),
         ("Can I buy whole wings and have them cut at destination?",
          "Sometimes, and the economics depend entirely on labour cost and yield at your end. "
          "Ask for both prices, whole and separated, and compare after adding your own "
          "cutting cost and waste."),
         ("Why do prices for different cuts move in opposite directions?",
          "Because each cut is sold into a different geography with its own demand. A bird is "
          "disassembled and each part goes where it is worth most, so the parts have "
          "independent markets even though they come off the same line.")],
},
{
 "slug": "reefer-cold-chain",
 "title": "What a reefer programme requires | cold chain and recorders",
 "desc": "Set point, recorders, plug time at transhipment, pack format and the loading "
         "practice that decides whether a frozen consignment arrives saleable.",
 "trail": t("Reefer cold chain"),
 "h1": "The cold chain is <em>a booking problem</em>",
 "sub": "The container keeps the temperature while it is plugged in. Everything that goes "
        "wrong in this trade happens in the hours when it is not, and nobody books those "
        "hours.",
 "chips": ["Set point", "Recorder in the file", "Plug time", "25 t net"],
 "lede": ("Equipment is the easy part",
   "A modern reefer holds its set point reliably for weeks. What it cannot do is hold it "
   "while it is standing on a chassis at a transhipment port waiting for a plug, and that "
   "is a scheduling decision somebody made, not an equipment failure."),
 "body": [
  ("h2","The set point and what it means"),
  ("p","The set point is written into the booking and into the contract, and it is the "
       "temperature the machine maintains for the air it delivers. For block frozen product "
       "the commercial standard is well below freezing with a stated tolerance, and the "
       "tolerance matters as much as the number."),
  ("p","Two mistakes recur. Loading product that is not already at temperature, because a "
       "reefer maintains temperature and does not pull it down from warm, so warm product "
       "arrives warm and everything downstream is a claim. And setting a temperature "
       "appropriate for chilled cargo on a frozen booking, which is a clerical error that "
       "ruins a container."),
  ("h2","The recorder belongs in the document set"),
  ("p","The machine logs its own performance and the data can be downloaded at discharge. On "
       "top of that an independent recorder placed inside the load gives the temperature of "
       "the cargo rather than of the delivery air."),
  ("p","Both outputs belong in the document file, handed over with the bill of lading and "
       "the certificates, not kept in a drawer by whoever happened to download them. A claim "
       "without a temperature record is an argument. A claim with one is arithmetic."),
  ("note","Where the value justifies it, the independent recorder should be placed by someone "
          "who is not the seller, and its position in the load should be photographed."),
  ("h2","Plug time, the part nobody books"),
  ("ul",["<b>At the port of loading</b>, between the arrival of the packed container and "
         "the vessel: is it plugged, and who confirms it.",
         "<b>At transhipment</b>, which on many routes into West Africa and Southern Africa "
         "means a day or more in a hub port. This is where the chain is most often broken "
         "and least often checked.",
         "<b>At the discharge port</b>, between landing and customs release. Clearance delays "
         "and plug availability are separate problems that arrive together.",
         "<b>On the inland leg</b>, if there is one, and whether the vehicle is genset "
         "equipped or the container travels unpowered."]),
  ("p","We ask these four questions at booking rather than at arrival, and on a programme we "
       "ask who at the terminal confirms the plug status and how that confirmation reaches "
       "the file."),
  ("h2","Pack format is part of the cold chain"),
  ("p","Block frozen product in cartons behaves differently from individually frozen product "
       "in bags: the block is thermally slow and forgiving, the loose product is fast and "
       "unforgiving. Carton strength matters because a crushed carton in the middle of a "
       "stack restricts air flow, and restricted air flow is the mechanism behind most "
       "uneven-temperature claims."),
  ("p","Loading practice follows from that. The load has to be stowed so that the delivery "
       "air can travel: product off the floor channels where the design requires it, nothing "
       "blocking the return air path at the top, and the load not stacked above the red line "
       "painted inside the box for exactly this reason."),
  ("h2","What a 40ft reefer actually carries"),
  ("p","Less volume than a dry box of the same length, because of the insulation and the "
       "machinery, and on a typical frozen food loading plan about 25 tonnes net. That "
       "figure is the planning number for a programme: five containers a month is roughly "
       "125 tonnes, ten is roughly 250."),
 ],
 "faq": [("Can a reefer freeze product that is loaded warm?",
          "No. It maintains temperature, it does not pull product down from warm. Product "
          "has to be at temperature before it goes in, and that is a condition in the "
          "contract, not an assumption."),
         ("Who holds the temperature record?",
          "It belongs in the document set handed over with the bill of lading. The machine's "
          "own log can be downloaded at discharge, and an independent recorder in the load "
          "gives the cargo temperature rather than the air temperature. Both should be in "
          "the file."),
         ("Where does the cold chain usually break?",
          "At transhipment, waiting for a plug, and between discharge and customs release. "
          "Both are scheduling problems rather than equipment problems, which is why they "
          "are asked about at booking.")],
},
{
 "slug": "antidumping-check",
 "title": "The trade remedy check before you order | antidumping",
 "desc": "Why a cash deposit can exceed the value of the goods, how scope is defined, and "
         "why in the United States the deposit is not the final liability.",
 "trail": t("Trade remedies"),
 "h1": "The check that turns a good purchase <em>into a loss</em>",
 "sub": "Antidumping and countervailing duties are not ordinary tariffs. The rate can exceed "
        "the value of the goods, the scope is defined by product description rather than by "
        "code alone, and in some systems the amount paid at entry is only a deposit.",
 "chips": ["Scope by description", "Deposit at entry", "Retrospective assessment",
           "Sunset review"],
 "lede": ("Why this deserves its own check",
   "An ordinary duty rate of a few per cent is a line in a cost model. A trade remedy rate "
   "in the hundreds of per cent is not a line in a cost model, it is the end of the "
   "transaction, and it attaches to the importer."),
 "body": [
  ("h2","What the two remedies are"),
  ("p","An <b>antidumping</b> duty answers a finding that goods were sold into the market "
       "below their normal value. A <b>countervailing</b> duty answers a finding that the "
       "production was subsidised. They are imposed per country of origin and usually per "
       "producer, so two factories in the same country can carry very different rates and "
       "one can carry none."),
  ("p","They sit on top of the ordinary tariff, not instead of it, and they are collected "
       "from the importer of record."),
  ("h2","Scope is a description, not a code"),
  ("p","This is the part that catches people. An order defines the subject merchandise in "
       "words: what it is made of, how it is processed, what it is used for, and what is "
       "expressly excluded. Commodity codes are listed for convenience and the text says so; "
       "goods outside the listed codes can still be in scope and goods inside them can be "
       "out of it."),
  ("p","A worked example from a lane we run: quartz surface products from a particular origin "
       "carry orders, while quarried stone such as granite, marble, soapstone and quartzite "
       "is expressly excluded from that scope. Two slabs that a buyer would describe the same "
       "way sit on opposite sides of the line, and the difference is in the material and the "
       "processing, not in the appearance."),
  ("note","Where the answer is genuinely unclear, administrations issue scope rulings. "
          "Asking for one before a programme starts costs a fraction of discovering the "
          "answer at entry."),
  ("h2","In the United States the deposit is not the bill"),
  ("p","Most systems assess the final duty at entry. The United States operates "
       "retrospectively: the amount paid at entry is a cash deposit at the current rate, and "
       "the final liability is determined later in an administrative review covering that "
       "period, which can take years."),
  ("p","The consequence is uncomfortable and frequently missed. If the review sets a higher "
       "rate than the deposit, the importer owes the difference with interest, long after the "
       "goods were sold and the margin was spent. A buyer running a programme under an order "
       "has an open liability on the books, and should know that before the first container, "
       "not during an audit."),
  ("h2","Rates change, so the check has a date on it"),
  ("p","Rates are revised in administrative reviews, new producers can obtain their own "
       "rates, and the orders themselves are reviewed periodically to decide whether they "
       "continue. A rate confirmed six months ago is not a rate confirmed today, and the "
       "only date that matters is the date of entry."),
  ("h2","How we run the check"),
  ("ul",["Identify the classification and read the scope text of any order touching that "
         "product and origin, rather than relying on the code alone.",
         "Identify the specific producer, because rates are producer-specific and a "
         "company-specific rate can be zero where the country-wide rate is not.",
         "Confirm the live rate as at the planned entry date, not as at the enquiry date.",
         "Where the product sits near a scope boundary, recommend a scope ruling and say "
         "what the delay costs against what the exposure is.",
         "Show any deposit as a separate line in the landed price, flagged as a deposit "
         "rather than as a duty, so nobody treats it as final."]),
 ],
 "faq": [("Does an antidumping duty apply to the product or to the supplier?",
          "To both. Scope defines the product and the origin; rates are then set per "
          "producer, so the same goods from two factories in one country can carry very "
          "different rates and one of them may carry none."),
         ("Can I avoid it by shipping through another country?",
          "No, and attempting it is circumvention, which carries its own penalties and "
          "reaches back to the importer. Origin for these purposes is where the goods were "
          "produced, not where they were last loaded."),
         ("Is the duty I pay at entry final?",
          "Not in every system. The United States assesses retrospectively: what you pay at "
          "entry is a deposit, and the final rate is set later in a review, with the "
          "difference payable with interest. That open liability belongs in the decision "
          "before the first order.")],
},
{
 "slug": "bill-of-lading",
 "title": "Bill of lading and telex release | ISP Group",
 "desc": "Receipt, contract of carriage and document of title in one piece of paper. "
         "Originals, seaway bills, telex release and what happens when cargo beats documents.",
 "trail": t("Bill of lading"),
 "h1": "The bill of lading <em>is the cargo</em>",
 "sub": "Whoever holds an original endorsed bill of lading can collect the goods. That one "
        "sentence explains every rule, every delay and every argument around this document.",
 "chips": ["Receipt", "Contract", "Document of title", "Telex release"],
 "lede": ("Three jobs in one piece of paper",
   "A bill of lading is a receipt that the carrier took the goods, the contract of carriage "
   "on which it carries them, and, when it is negotiable, a document of title. The third job "
   "is the one that creates all the drama, because it means the paper controls the steel box."),
 "body": [
  ("h2","Negotiable original or sea waybill"),
  ("p","A negotiable bill of lading is usually issued in a set of three originals, and "
       "surrendering any one of them releases the cargo; the other two then become void. The "
       "set exists because paper used to travel by post on different ships, and the practice "
       "survived the reason for it."),
  ("p","A sea waybill is not a document of title. It names a consignee, the carrier releases "
       "to that named party on identification, and nothing has to travel. It is faster and "
       "safer, and it is the right choice whenever the seller is already paid or is content "
       "to be paid against something other than the document."),
  ("note","The rule of thumb: if payment depends on controlling the goods, you need a "
          "negotiable original. If it does not, a sea waybill removes an entire category of "
          "problem."),
  ("h2","Who is the consignee, and why “to order” matters"),
  ("ul",["<b>Straight consigned</b> to a named buyer: only that buyer can collect. Simple, "
         "and it gives the seller no leverage after shipment.",
         "<b>To order</b> of the shipper: the shipper endorses the bill to transfer control, "
         "which is what makes a documentary credit work.",
         "<b>To order of the issuing bank</b>: the bank holds control until the buyer pays or "
         "accepts. The strongest position for the bank and the most common under a credit.",
         "<b>Notify party</b> is not the consignee. It is who the carrier telephones on "
         "arrival, and it has no rights over the cargo at all."]),
  ("h2","Telex release, which is not a telex"),
  ("p","On a short voyage the vessel arrives before the paperwork, and originals posted from "
       "the origin will not be at the destination in time. A telex release solves it: the "
       "shipper surrenders all originals to the carrier at the origin, and the carrier "
       "instructs its own office at the destination to release without presentation."),
  ("p","Two things follow. The seller gives up control the moment the originals are "
       "surrendered, so it should only be done when payment is secure. And because it is a "
       "carrier process rather than a legal instrument, every line does it slightly "
       "differently, charges differently for it, and takes a different amount of time, which "
       "has to be asked about before the booking rather than during the crisis."),
  ("p","An express release is the same idea built in from the start: the bill is issued "
       "non-negotiable and no original is ever printed."),
  ("h2","House and master bills"),
  ("p","When a freight forwarder consolidates, the ocean carrier issues a master bill to the "
       "forwarder, and the forwarder issues a house bill to each shipper. The house bill is "
       "the document the buyer deals with, and it is only as good as the forwarder behind it."),
  ("p","That matters at the destination: the cargo is released by the forwarder's own agent, "
       "not by the shipping line. A forwarder with no real agent at the discharge port is "
       "the commonest cause of a consignment sitting on the quay while two offices email "
       "each other."),
  ("h2","When the paper goes wrong"),
  ("ul",["<b>Cargo arrives before documents.</b> Either arrange a telex release, or the "
         "buyer provides a bank guarantee to the carrier, which the bank will charge for and "
         "will not love.",
         "<b>Originals lost.</b> Replacement requires an indemnity, usually bank-backed, for "
         "a multiple of the cargo value, held for years. Expensive and slow.",
         "<b>Details differ from the credit.</b> A spelling difference between the bill and "
         "the letter of credit is a discrepancy, and the protection the seller paid for is "
         "gone until the buyer waives it.",
         "<b>A switch bill is requested.</b> Issuing a second set at a different port, "
         "usually to hide the original supplier, is a real commercial practice and also the "
         "mechanism behind a lot of fraud. We only do it with the first set physically "
         "surrendered, and we do not do it to misstate origin."]),
  ("h2","What we put in the contract"),
  ("p","Which document type will be issued, who is consignee and notify, how many originals, "
       "where they are to be couriered and at whose cost, whether telex release is permitted "
       "and who authorises it, and the deadline for the document set to reach the buyer "
       "relative to the vessel's arrival. All five are settled before loading, because none "
       "of them can be fixed while a container accrues demurrage."),
 ],
 "faq": [("What is the difference between a bill of lading and a sea waybill?",
          "A negotiable bill of lading is a document of title: whoever holds an endorsed "
          "original can take the goods. A sea waybill is not; the carrier releases to the "
          "named consignee on identification and nothing has to be presented. Use the first "
          "when payment depends on controlling the cargo, the second when it does not."),
         ("How long does a telex release take?",
          "It is a carrier procedure, not a legal instrument, so it varies by line and by "
          "office, from a few hours to a couple of days. Ask the carrier before the booking "
          "rather than on the day the vessel berths."),
         ("Can I get my cargo without the original bill of lading?",
          "Only with the carrier's agreement, normally against a bank guarantee for a "
          "multiple of the cargo value. It is expensive and the bank will want security. "
          "Preventing the situation costs nothing by comparison.")],
},
{
 "slug": "demurrage-detention",
 "title": "Demurrage and detention | the two clocks after arrival",
 "desc": "Demurrage runs while the container sits in the terminal, detention while you have "
         "it outside. Free time, reefer rates, who pays and how to stop the clock.",
 "trail": t("Demurrage and detention"),
 "h1": "Two clocks start <em>the day the vessel berths</em>",
 "sub": "Demurrage runs while the container is still in the terminal. Detention runs while "
        "you have the container outside it. They are different charges, from different "
        "parties, and almost nobody budgets for either.",
 "chips": ["Demurrage: inside", "Detention: outside", "Free time", "Reefer is shorter"],
 "lede": ("The largest cost that never appears in a quotation",
   "Freight is negotiated to the dollar and these are discovered on an invoice weeks later. "
   "On a lane where clearance is slow they are not an edge case, they are a line in the "
   "budget."),
 "body": [
  ("h2","Which clock is which"),
  ("p","<b>Demurrage</b> is charged for the container occupying space in the terminal after "
       "the free time ends. It is the port's or the carrier's charge for storage, and it "
       "runs whether or not your paperwork is ready."),
  ("p","<b>Detention</b> is charged for the container being away from the terminal, at your "
       "yard, after the free time for unpacking ends. It is the carrier's charge for its box "
       "not being back in circulation."),
  ("p","Some carriers merge the two into a single combined free time, which sounds generous "
       "and is usually shorter in total. Read which model the quotation uses before comparing "
       "two offers."),
  ("note","A third charge, port storage, can run alongside demurrage and is billed by the "
          "terminal rather than the line. On congested ports it is the larger of the two."),
  ("h2","Free time is a negotiated number, not a fact"),
  ("p","Free time varies by carrier, by trade lane, by season and by how much volume you "
       "give the line. It is routinely extendable at the time of booking and almost never "
       "extendable afterwards, which is the whole point: ask for it when you still have "
       "something to trade."),
  ("p","Reefer free time is dramatically shorter than dry, often a small fraction of it, and "
       "reefer demurrage is charged at a higher rate because the box is drawing power. On a "
       "frozen programme this is the single most expensive thing to get wrong, and it is why "
       "the clearance file has to be complete before the vessel arrives rather than after."),
  ("h2","Why the clock usually runs"),
  ("ul",["<b>Documents late.</b> Originals still in the post, a telex release not yet "
         "actioned, a certificate missing a signature.",
         "<b>Classification queried.</b> Customs disagrees with the code and the entry is "
         "held while it is resolved, which is why the code is agreed before the order.",
         "<b>Inspection.</b> A physical examination adds days and is not under anyone's "
         "control; it is a budget line with a probability, not an exception.",
         "<b>No haulier booked.</b> The box is cleared and nobody arranged a truck, which "
         "happens more often than anyone admits.",
         "<b>Receiving site cannot unload.</b> No forklift for the weight, no dock, nobody "
         "on site on Friday afternoon.",
         "<b>Port congestion.</b> Not your fault and still your invoice."]),
  ("h2","Merchant haulage and carrier haulage"),
  ("p","If the carrier arranges the inland leg, the free time and the charges sit inside its "
       "contract and it has an interest in moving the box. If you arrange your own haulier, "
       "the line's detention clock still runs and nobody on the carrier's side is watching "
       "it for you."),
  ("p","Neither is always cheaper. What matters is knowing which one you bought, because the "
       "two put the risk of a slow truck in completely different places."),
  ("h2","How we keep the clock stopped"),
  ("ul",["Negotiate free time at the booking, in writing, as part of the rate rather than as "
         "a favour afterwards.",
         "Have the full document set with the broker before the vessel arrives, not when it "
         "berths.",
         "Agree the tariff classification before the order so a query is unlikely.",
         "Book the haulier against the estimated arrival and re-confirm when the schedule "
         "moves, which it will.",
         "Confirm the receiving site can take the weight and has someone there on the day.",
         "On reefer, treat the shorter free time as the binding constraint on the whole "
         "schedule, because it is."]),
  ("p","Where we quote DAP, as on the "
      "<a href=\"southern-africa.html\">Durban corridor</a>, these risks sit with us rather "
      "than with the buyer, which is the honest reason a DAP price is higher than a port "
      "price."),
 ],
 "faq": [("What is the difference between demurrage and detention?",
          "Demurrage is charged while the container is still inside the terminal after free "
          "time expires. Detention is charged while the container is outside the terminal, "
          "at your premises, after the unpacking free time expires. Different clocks, often "
          "different invoices."),
         ("How much free time should I ask for?",
          "More than the default, and ask at booking. The number depends on the lane and "
          "your volume. What matters is that it is written into the rate, because after "
          "arrival nobody extends it."),
         ("Who pays if the port is congested?",
          "Normally the importer, which feels unfair and is how the contracts are written. "
          "The practical defences are a longer free time negotiated up front and a complete "
          "document set lodged before arrival.")],
},
{
 "slug": "certificate-of-origin",
 "title": "Certificates of origin | preferential and non-preferential",
 "desc": "Who issues a certificate of origin, what preferential and non-preferential mean, "
         "how rules of origin are actually tested, and the mistakes that void one.",
 "trail": t("Certificates of origin"),
 "h1": "Where goods are <em>from</em> is a legal test, not a shipping address",
 "sub": "Origin is not where the container was loaded, not where the seller is registered "
        "and not where the invoice was printed. It is where the goods were produced, or "
        "last substantially transformed, and the test is written down.",
 "chips": ["Preferential", "Non-preferential", "Substantial transformation", "Chamber or authority"],
 "lede": ("Two documents with the same name and different jobs",
   "A non-preferential certificate says where the goods came from. A preferential one claims "
   "a reduced or zero duty under a trade agreement. The second is worth money and is "
   "therefore checked properly."),
 "body": [
  ("h2","Non-preferential: who made it"),
  ("p","This is the ordinary certificate, usually issued by a chamber of commerce in the "
       "exporting country on the exporter's declaration. It is used for customs statistics, "
       "for government procurement rules, for labelling requirements, for quotas and for "
       "establishing whether a trade remedy applies to the goods."),
  ("p","It carries no duty benefit by itself. It is still the document that decides whether "
       "an antidumping order reaches your consignment, which makes it quietly important on "
       "any lane where such an order exists."),
  ("h2","Preferential: why it is worth money"),
  ("p","A preferential certificate claims the reduced duty available under a specific trade "
       "agreement between the exporting and importing countries. Because it has a cash value "
       "it is issued under stricter conditions, often on a prescribed form, and it is the "
       "one customs authorities audit after the fact."),
  ("p","Several modern agreements have moved away from a stamped certificate to "
       "<b>self-certification</b>: the exporter makes a statement of origin on the invoice "
       "or on a separate declaration, sometimes only if registered in an official exporter "
       "system. That shifts the burden entirely onto the exporter's records, and it means a "
       "buyer should ask what evidence sits behind the statement, not just whether the "
       "statement exists."),
  ("h2","How origin is actually decided"),
  ("ul",["<b>Wholly obtained.</b> Mined, grown, harvested, caught or born and raised in one "
         "country. Unambiguous and rare outside agriculture and raw materials.",
         "<b>Substantial transformation.</b> For anything made from imported inputs, origin "
         "is where the last substantial transformation happened. Agreements define that in "
         "one of three ways, and sometimes more than one at once.",
         "<b>Change of tariff classification.</b> The finished good sits under a different "
         "heading from its imported inputs. Mechanical and easy to test.",
         "<b>Value-added threshold.</b> A stated percentage of the value has to originate "
         "locally. Requires a costing the exporter may not want to show.",
         "<b>Specific process rule.</b> A named operation must occur, common in textiles and "
         "chemicals.",
         "<b>Insufficient operations.</b> Repacking, labelling, simple assembly, mixing and "
         "sorting never confer origin, whatever the invoice says."]),
  ("note","Assembling imported parts in a third country to change the stated origin and "
          "escape a duty is circumvention, not planning. It reaches back to the importer, "
          "with penalties, and the goods are usually traceable."),
  ("h2","What voids a certificate in practice"),
  ("ul",["<b>Issued by the wrong body.</b> Preferential forms generally have one competent "
         "authority per country; a chamber certificate will not substitute.",
         "<b>Names the trading company as producer.</b> If the exporter on the certificate "
         "is not the manufacturer, the manufacturer still has to be identifiable and the "
         "origin still has to be theirs.",
         "<b>Details disagree with the other documents.</b> Quantities, marks, container "
         "numbers and invoice references all have to reconcile with the bill of lading and "
         "the packing list.",
         "<b>Issued after shipment without being marked as such.</b> Retrospective issue is "
         "allowed in most schemes but has to be declared on the face of the document.",
         "<b>Nothing behind it.</b> On audit the exporter has to produce the costing or the "
         "bill of materials that supports the claim. A statement with no file behind it is "
         "where self-certification goes wrong."]),
  ("h2","What we do"),
  ("p","We establish before the order which certificate the destination needs, which body "
       "issues it in the country of production, and whether the product meets the rule of "
       "origin as a matter of fact rather than as a matter of assertion. Where a preference "
       "is material to the price, we say in the quotation what the landed cost is with and "
       "without it, so a failed claim is a known risk rather than a surprise."),
  ("p","Where a trade remedy order may be in scope, origin is the first thing we pin down, "
       "for the reason set out in the <a href=\"antidumping-check.html\">trade remedy "
       "guide</a>."),
 ],
 "faq": [("Who issues a certificate of origin?",
          "For non-preferential certificates, usually a chamber of commerce in the exporting "
          "country, on the exporter's declaration. For preferential claims it is the "
          "designated competent authority, or under newer agreements the registered exporter "
          "itself by a statement on the invoice."),
         ("Does repacking in another country change origin?",
          "No. Repacking, relabelling, simple assembly, sorting and mixing are insufficient "
          "operations and do not confer origin under any mainstream rule set, whatever "
          "appears on the invoice."),
         ("What happens if the preference claim is rejected later?",
          "The importer pays the full duty with interest, usually on an audit years after "
          "the goods were sold. This is why we quote the landed cost both with and without "
          "the preference when it materially changes the price.")],
},
{
 "slug": "proforma-invoice",
 "title": "The proforma invoice | what it has to contain",
 "desc": "A proforma invoice is an offer, not an accounting document. What belongs on it, "
         "how it differs from a commercial invoice, and the single line that catches fraud.",
 "trail": t("Proforma invoice"),
 "h1": "A proforma invoice is <em>an offer</em>",
 "sub": "It is not a bill, it does not go into anyone's books, and nothing is owed on it. "
        "It exists so that two parties can agree exactly what is being sold before money "
        "or goods move.",
 "chips": ["Offer, not a bill", "Opens a credit", "Validity date", "Beneficiary name"],
 "lede": ("The document where the deal is actually written",
   "Most of what later goes wrong in a shipment was decided, or left undecided, on the "
   "proforma. It costs nothing to make it complete and it is the cheapest risk control "
   "available in this trade."),
 "body": [
  ("h2","What it is for"),
  ("ul",["<b>Agreeing the deal.</b> Specification, quantity, price, terms and dates in one "
         "place, before a purchase order exists.",
         "<b>Opening a letter of credit.</b> The buyer's bank builds the credit from it, "
         "which is why an incomplete proforma produces a credit the seller cannot comply "
         "with.",
         "<b>Obtaining an import licence or permit</b>, where the destination requires one "
         "before shipment.",
         "<b>Applying for finance</b> or for a foreign currency allocation in countries that "
         "control it.",
         "<b>Customs valuation in advance</b>, for an estimate of duty before the order is "
         "placed."]),
  ("h2","What has to be on it"),
  ("p","A proforma that is missing any of these will cost a round trip, and under a "
       "documentary credit it can cost a discrepancy."),
  ("ul",["Seller and buyer legal names and addresses, as registered, not trading names.",
         "A proforma number and a date, and a <b>validity date</b> for the price.",
         "The goods described the way the specification describes them, with grade, "
         "standard, pack and unit.",
         "Quantity and unit price, and the currency written out.",
         "The <b>Incoterm with the named place and the edition</b>, for example CIF Lomé, "
         "Incoterms 2020.",
         "The <b>HS code</b> the seller believes applies, so it can be checked against the "
         "importing country's tariff before the order.",
         "Country of origin and the producing establishment or plant, where that matters.",
         "Port of loading and port of discharge.",
         "Whether partial shipment and transhipment are allowed.",
         "Lead time, expressed from a trigger rather than from a calendar date: so many days "
         "from receipt of deposit, or from approval of a sample.",
         "Payment terms in full, including who pays which bank charges.",
         "Full bank details, including the beneficiary name."]),
  ("note","That last line is the one that matters most. The beneficiary name on the proforma "
          "must match the seller's registered name exactly. A mismatch is the mechanism "
          "behind almost every payment-diversion fraud in this trade, and it is explained "
          "in <a href=\"verify-supplier.html\">verifying a supplier</a>."),
  ("h2","Proforma, commercial invoice, packing list"),
  ("p","The <b>proforma</b> is the offer, issued before anything happens. The <b>commercial "
       "invoice</b> is the demand for payment, issued when the goods ship, and it is the "
       "document customs values the consignment on. The <b>packing list</b> says what is "
       "physically in each carton and each container and carries no prices."),
  ("p","All three have to agree with each other and with the bill of lading, down to the "
       "carton count and the marks, because a customs authority anywhere in the world "
       "resolves a discrepancy between them by inspecting the container."),
  ("h2","Reading one critically"),
  ("ul",["<b>No validity date.</b> The price is good until the seller says otherwise, which "
         "means it is not a price.",
         "<b>Lead time from a calendar date.</b> It will slip with the deposit and the "
         "argument will be about whose fault that is.",
         "<b>Incoterm without a named place.</b> “CIF” alone means nothing.",
         "<b>Bank in a third country</b> with no explanation on company letterhead.",
         "<b>Specification by model name only.</b> The model will be built down to the "
         "price unless the specification is attached.",
         "<b>No mention of tolerance.</b> On weight, dimension or count, the tolerance is "
         "whatever the seller decides at loading if it is not written."]),
  ("h2","What we issue"),
  ("p","Our proforma to a buyer mirrors our purchase contract with the producer line for "
       "line: the same specification, the same tolerances, the same inspection window and "
       "the same claim period, so nothing falls into the gap between the two contracts. "
       "Where we are quoting more than one Incoterm, each basis is a separate line with its "
       "own total, not a footnote."),
 ],
 "faq": [("Is a proforma invoice legally binding?",
          "It is an offer, and it becomes binding when it is accepted, typically by a "
          "purchase order or by payment of the deposit against it. By itself it creates no "
          "debt and does not belong in anyone's accounts."),
         ("Can customs use a proforma invoice?",
          "For an advance duty estimate or for a licence application, often yes. For the "
          "actual entry, no: customs values the consignment on the commercial invoice issued "
          "when the goods ship."),
         ("What is the single most important line on it?",
          "The bank beneficiary name, which has to match the seller's registered name "
          "exactly. Every payment-diversion fraud in this trade runs through a mismatch "
          "there.")],
},
]
