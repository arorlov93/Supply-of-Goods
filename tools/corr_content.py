# -*- coding: utf-8 -*-
"""Тексты страниц коридоров. Вынесены отдельно, чтобы генератор остался читаемым."""

PAGES = [
{
 "slug": "china",
 "title": "China sourcing and container shipping",
 "desc": "How we buy in China: separating a factory from a trading company, writing a specification that binds, pre-shipment inspection, consolidated loading and staged payment.",
 "h1": "China: the gap between a <em>price</em> and a shipment",
 "sub": "Equipment, tools, hardware and building materials out of Ningbo, Qingdao and Shenzhen. The quote is the easy part. Everything between the quote and a container on the water is the work.",
 "chips": [("FOB &middot; CIF &middot; DAP", None), ("Ningbo &middot; Qingdao &middot; Shenzhen", None),
           ("30 / 50 / 20", "staged payment"), ("FCL and LCL", None)],
 "photo": ("machinery.jpg", 910, 683, "Industrial drive assembly and chain gearing",
           "Equipment and machinery sourced to specification"),
 "lede": ("Why a Chinese quote is not yet a price",
   "Almost every first enquiry comes back with a number that looks excellent and cannot be "
   "compared with anything. It is quoted EXW on an unstated specification, by a company that "
   "may never have made the product. Our first job is to turn that number into something a "
   "buyer can actually act on."),
 "body": [
  ("h2", "The supplier is a factory or it is not"),
  ("p", "China exports through two very different kinds of counterparty. A factory owns a "
        "production line and a business licence that names what it manufactures. A trading "
        "company owns a WeChat account and a relationship with several factories. Both will "
        "answer your enquiry within an hour, and both will send photographs of a plant."),
  ("p", "The difference matters when something goes wrong. A factory can re-run a batch. A "
        "trading company has to persuade someone else to re-run it, at its own cost, with no "
        "leverage. The check is not difficult: the business licence shows the registered scope "
        "of business, the export licence shows whether the entity can ship in its own name, and "
        "the bank account on the proforma has to carry the same name as the licence. If the "
        "beneficiary name differs from the seller name, that is not a detail, that is the whole "
        "question."),
  ("p", "We do not refuse to work with trading companies. For small quantities or for an "
        "assortment across several plants they are often the right answer. We refuse to work "
        "with one that presents itself as a factory."),
  ("h2", "The specification is the only thing that binds"),
  ("p", "The commonest failure in this corridor is not fraud. It is that the buyer and the "
        "seller each had a clear picture in mind and the pictures were different. A purchase "
        "order that says “machine, 50 kW, 380 V” leaves the motor brand, the controller, "
        "the duty cycle, the finish, the spares pack and the manual language entirely to the "
        "seller, and the seller will resolve every one of them in the direction of cost."),
  ("p", "We write the specification before we ask for a price, not after. For equipment that "
        "means the drive and controller by make, the electrical standard, the certification "
        "mark required at destination, the voltage and frequency, the spares pack and the "
        "commissioning arrangement. For materials it means grade, dimension and tolerance "
        "against a named standard, the mill or batch certificate, the surface finish and the "
        "pack. For anything that has an appearance, it means a sealed reference sample held by "
        "both sides."),
  ("p", "Once the specification exists, three quotes against it are comparable and a fourth "
        "supplier can be added without starting again."),
  ("h2", "Inspection is cheap compared with a container of the wrong thing"),
  ("p", "Production is inspected before the goods are paid for in full and before they are "
        "loaded. For a commodity that means a sampling plan against the specification and a "
        "dimensional check. For equipment it means a witnessed run. For everything it means "
        "photographs of the goods, the carton, the pallet and the loaded container, taken by "
        "someone who is not the seller."),
  ("p", "Wood packaging has to be heat treated and marked under ISPM 15, and a container that "
        "arrives with untreated pallets can be refused at the destination port at the "
        "importer’s expense. That check belongs at loading, not at arrival."),
  ("h2", "Consolidation, documents and the customs line"),
  ("p", "A full container is simpler and cheaper per unit, but a first order rarely fills one. "
        "We consolidate several suppliers into one container at the port of loading, which keeps "
        "a trial order on full container economics and produces one bill of lading instead of "
        "four. The trade-off is time: consolidation adds a week to the schedule, and that week "
        "has to be in the plan rather than discovered."),
  ("p", "The document set is where the money is actually lost. The HS code decides the duty "
        "rate at destination and it is the importer who is liable for a wrong one, not the "
        "Chinese seller who typed it. The certificate of origin decides whether a preference "
        "applies. The packing list has to agree with the invoice, the bill of lading and the "
        "physical container, down to the carton count, because customs anywhere in the world "
        "resolves a discrepancy by inspecting."),
  ("h2", "Payment is staged against events, not dates"),
  ("p", "We do not prepay in full, and we do not ask a buyer to. A deposit releases production, "
        "a second instalment falls due against inspection and the final balance against the "
        "document set. Where the value justifies the bank charges, an irrevocable letter of "
        "credit does the same job with the bank holding the trigger instead of us."),
  ("p", "Every stage is tied to something observable. “Fifty per cent on 15 March” pays for "
        "a date. “Fifty per cent against a passed inspection report” pays for goods."),
 ],
 "facts": [("Typical cargo", "Industrial equipment and machinery, tools and hardware, building and finishing materials, consumables"),
           ("Gateways", "Ningbo, Qingdao, Shenzhen, Shanghai"),
           ("Terms we quote", "FOB, CIF, DAP"),
           ("Load type", "FCL 20ft and 40ft, consolidated LCL for trial orders"),
           ("Verification", "Business licence, export licence, beneficiary name match, factory check"),
           ("Before loading", "Pre-shipment inspection, loading photographs, ISPM 15 wood packaging"),
           ("Settlement", "Staged transfer against events, or irrevocable letter of credit")],
 "kw": ["sourcing from China", "factory verification", "pre-shipment inspection",
        "container consolidation", "ISPM 15", "letter of credit", "FOB Ningbo"],
},
{
 "slug": "turkiye",
 "title": "Stone and building materials from Türkiye",
 "desc": "Buying natural stone and building materials in Türkiye for the United States: block against slab, grading and resin, crating and breakage, HTS classification and the trade remedy check.",
 "h1": "Türkiye: stone and building materials into the <em>United States</em>",
 "sub": "Marble, travertine, porcelain and finishing materials out of Izmir and Istanbul to New York, Savannah and Houston. A short ocean leg, a long list of things that decide whether the pallet arrives saleable.",
 "chips": [("FOB &middot; CIF", None), ("Izmir &middot; Istanbul", None),
           ("New York &middot; Savannah &middot; Houston", None), ("2 cm and 3 cm", "slab")],
 "photo": ("pipe.jpg", 922, 691, "Stacked material seen end on",
           "Materials bought to a named standard, not to a photograph"),
 "lede": ("A short lane with an expensive failure mode",
   "Tükiye is close to the United States by sea and deep in stone, tile and finishing "
   "materials. That makes the corridor attractive and slightly deceptive: the freight is "
   "manageable, so buyers relax, and the money is lost on grading, on breakage and on a "
   "customs classification nobody checked before the order."),
 "body": [
  ("h2", "Block, slab or finished: three different purchases"),
  ("p", "“Marble” is not a product. A quarry sells blocks by the cubic metre. A factory "
        "sells slabs by the square metre, cut to 2 cm or 3 cm, polished or honed, sold in "
        "bundles that came from one block and therefore match. A fabricator sells finished "
        "pieces cut to a drawing. The three have different prices, different packing, different "
        "waste and different people to argue with."),
  ("p", "If the buyer is going to fabricate, bundles matter more than price. Slabs from "
        "different blocks will not match across a run, and a job that needs twelve matching "
        "slabs cannot be filled from a mixed pallet at any discount. That has to be written "
        "into the order: block number, bundle integrity, sequence preserved."),
  ("h2", "Grading and resin are where the margin hides"),
  ("p", "Natural stone is graded commercially, not by a public standard, which means grade A "
        "from one supplier can be grade B at the next. The honest way to buy is against a "
        "sealed reference sample plus a written tolerance for veining, colour variation and "
        "filled defects, with photographs of the actual bundles before shipment."),
  ("p", "Most commercial travertine and much marble is resin treated and often mesh backed on "
        "the reverse. That is normal and it is not a defect, but it changes what the material "
        "can be used for and it has to be declared. A slab sold as unfilled that arrives "
        "resin filled is a claim; a slab sold as resin filled is a product."),
  ("h2", "Crating decides whether you receive what you bought"),
  ("p", "Stone travels badly and arrives expensively. Slabs ship on A-frames or in wooden "
        "bundles, strapped, with the faces separated. A crate that is well built costs a few "
        "dollars per square metre and a crate that is not costs the value of the stone. "
        "Moisture trapped in a sealed crate marks the surface of light material, so the pack "
        "has to breathe."),
  ("p", "We write the breakage allowance into both contracts in the same words, with the same "
        "inspection window and the same evidence standard: photographs at the time of "
        "discharge, before the crate leaves the port. A claim raised three weeks later against "
        "a seller who has already been paid is a conversation, not a remedy."),
  ("h2", "Classify before you order, not at the border"),
  ("p", "The importer of record is liable for the classification, the duty and anything that "
        "follows from getting it wrong, and the seller in Izmir is not. Two things have to be "
        "settled before the order rather than at entry."),
  ("p", "The first is the ordinary HTS heading and duty rate for the exact product. The second "
        "is whether the product falls inside the scope of a trade remedy order. Quartz surface "
        "products from Türkiye have carried antidumping and countervailing duty orders since "
        "2020, while quarried stone such as granite, marble, soapstone and quartzite is "
        "excluded from that scope. Rates are reviewed, so the live rate has to be confirmed at "
        "the time of entry, and a cash deposit on a subject product can exceed the value of the "
        "goods. This is the single check in this corridor that turns a good purchase into a loss."),
  ("h2", "What the short ocean leg is worth"),
  ("p", "The practical advantage of this lane over a far eastern one is the schedule. A shorter "
        "transit means the working capital is tied up for less time, a replacement for a damaged "
        "consignment arrives inside the same season, and a sample shipment can be judged before "
        "the main order rather than after it. We quote FOB and CIF side by side so the buyer can "
        "see exactly what that schedule costs."),
 ],
 "facts": [("Typical cargo", "Marble, travertine and other natural stone, porcelain and ceramic tile, building and finishing materials"),
           ("Gateways", "Izmir, Istanbul to New York, Savannah, Houston"),
           ("Terms we quote", "FOB, CIF"),
           ("Slab formats", "2 cm and 3 cm, polished or honed, bundled by block"),
           ("Before shipment", "Sealed reference sample, bundle photographs, crate specification"),
           ("US entry", "HTS classification agreed in advance, trade remedy scope checked, importer of record liability understood"),
           ("Claims", "Inspection window and evidence standard mirrored on both contracts")],
 "kw": ["marble import United States", "travertine supplier Türkiye", "natural stone slabs",
        "HTS classification", "antidumping duty", "CIF Savannah", "building materials import"],
},
{
 "slug": "west-africa",
 "title": "Frozen food into Lomé and Cotonou",
 "desc": "Shipping frozen poultry, bulk staples and consumables into Togo and Benin: veterinary admissibility, cut nomenclature, reefer cold chain and what the buyer's payment terms do to the cash cycle.",
 "h1": "West Africa: frozen food and consumables into <em>Lomé and Cotonou</em>",
 "sub": "Reefer programmes out of the Americas and the European Union. The product is simple, the admissibility and the payment terms are not, and those two decide whether the lane makes money.",
 "chips": [("CIF &middot; CFR", None), ("40ft reefer", "25 t net"),
           ("10 kg cartons", "block frozen"), ("Lomé &middot; Cotonou", None)],
 "photo": ("vessel2.jpg", 774, 581, "Container vessel alongside with boxes loaded",
           "Reefer programmes run to a schedule, not to a spot booking"),
 "lede": ("The cheapest offer in this trade is usually the one that cannot ship",
   "Frozen poultry and bulk staples into West Africa look like a pure price business and they "
   "are not. An offer is only real if the producing establishment is admissible in the "
   "destination country, if the cut is the one the market actually buys and if the payment "
   "terms survive a forty day voyage. Most of the cheap offers fail one of the three."),
 "body": [
  ("h2", "Admissibility comes before price"),
  ("p", "Frozen meat does not enter on a commercial invoice. It enters on a veterinary health "
        "certificate issued for a specific producing establishment, in a form the destination "
        "country accepts. An establishment approved for one West African country is not "
        "automatically approved for its neighbour, and the requirements change."),
  ("p", "For United States origin, export certification runs through the Food Safety and "
        "Inspection Service, and the certificate requirements for a given destination are "
        "published in its export library. Some destinations are handled electronically and some "
        "still require a paper certificate, which changes the lead time at the loading end. For "
        "European Union origin the equivalent is the competent authority of the member state. "
        "The question to put to any seller, before discussing a price, is the establishment "
        "number and written confirmation that it is cleared for the destination."),
  ("p", "We do not treat a seller’s assurance on this as an answer. The establishment number "
        "is checked, and where the destination is ambiguous we get the certificate form "
        "identified in writing before any money moves."),
  ("h2", "A cut is three products, not one"),
  ("p", "The commonest reason two offers cannot be compared is that they are not for the same "
        "thing. A whole wing with three joints, a two joint wing, a drumette and a mid joint "
        "flat are four different products with four different prices and four different buyers. "
        "Turkey is sold as tom or hen, and the lines are not interchangeable for a processor. "
        "Tails, backs and paws each have their own market and their own seasonality."),
  ("p", "Every enquiry we send names the anatomy explicitly, names the pack, and asks for the "
        "price on the same Incoterm for each line separately. An offer that quotes “wings” "
        "is not an offer."),
  ("h2", "Pack and cold chain are part of the specification"),
  ("p", "The West African standard is block frozen product in 10 kg cartons, which is not the "
        "standard pack in the United States or in the European Union. Repacking is possible and "
        "it costs money, so the price has to be asked for in both the producer’s own pack and "
        "in the destination pack. The difference tells you what the non-standard format is "
        "really worth."),
  ("p", "A 40ft reefer carries about 25 tonnes net. The temperature is set at loading, recorded "
        "throughout and read at discharge, and the recorder tape is part of the document set, "
        "not an optional extra. Plug time at the transhipment port and at the destination is the "
        "part of the chain nobody books and everybody assumes."),
  ("h2", "Compare the market, not the quotations"),
  ("p", "A quotation is what a seller would like to receive. Customs statistics are what the "
        "goods actually crossed a border at, because the declared value is divided by the "
        "declared net weight and every discount the seller really gave is already inside that "
        "number. Before we negotiate a lane we pull the destination country’s import values by "
        "origin and by commodity code for the most recent full periods, and we negotiate "
        "against that rather than against the first offer."),
  ("p", "On this corridor that exercise regularly moves the target by twenty per cent or more, "
        "and it changes which origin we approach first. It is also the only way to tell a "
        "genuinely competitive offer from one that is simply the lowest of three bad ones."),
  ("h2", "The payment terms decide the return, not the margin"),
  ("p", "This is the part buyers and sellers both underestimate. The margin per kilogram is set "
        "in the negotiation; the return on the money is set by how long the money is out. A "
        "letter of credit payable at sight against shipping documents releases the cash while "
        "the vessel is still at sea. Thirty day terms after arrival add the full voyage plus a "
        "month to the cycle, and on a multi container programme that is the difference between "
        "financing one shipment and financing four at once."),
  ("p", "We price the two cases separately and we say so. A buyer who wants extended terms is "
        "asking for a credit facility, and a credit facility has a price. That conversation "
        "belongs before the first shipment, not after it."),
 ],
 "facts": [("Typical cargo", "Frozen poultry parts, frozen and chilled protein, bulk staples and food ingredients, cleaning and facility consumables"),
           ("Gateways", "Santos, Gdańsk, Houston and other Atlantic ports to Lomé and Cotonou"),
           ("Terms we quote", "CIF and CFR, each port priced separately"),
           ("Equipment", "40ft reefer, about 25 t net, temperature recorded and read at discharge"),
           ("Pack", "Block frozen in 10 kg cartons, producer pack priced in parallel"),
           ("Before any money moves", "Establishment number, written confirmation of admissibility, certificate form identified"),
           ("Settlement", "Irrevocable letter of credit at sight preferred; extended terms priced as credit")],
 "kw": ["frozen poultry West Africa", "CIF Lome", "CIF Cotonou", "reefer container",
        "veterinary health certificate", "FSIS export library", "turkey wings supplier"],
},
{
 "slug": "southern-africa",
 "title": "Durban to Gaborone and SADC supply",
 "desc": "Supplying landlocked Southern Africa through Durban: why SACU is not SADC, road transit paperwork on the corridor, handling paper reels, and why DAP suits this lane.",
 "h1": "Southern Africa: industrial supply out of <em>Durban</em>",
 "sub": "Paper and packaging, cleaning and facility consumables and industrial supply into Botswana and the wider SADC region. A short sea leg and a long road leg, where the road leg is the risk.",
 "chips": [("DAP", None), ("Durban &rarr; Gaborone", None),
           ("Reels and corrugated", None), ("SACU", "common external tariff")],
 "photo": ("crane.jpg", 834, 625, "Quayside crane against an open sky",
           "Durban is the gateway for landlocked Southern Africa"),
 "lede": ("The sea leg is the easy half",
   "For a landlocked buyer in Southern Africa the ocean freight is a solved problem. What "
   "decides the delivered cost and the delivered date is the road leg out of Durban, the "
   "paperwork that travels with the truck and whether anyone checked which trade regime the "
   "consignment is actually moving under."),
 "body": [
  ("h2", "SACU is not SADC, and the difference changes the paperwork"),
  ("p", "This is the most common and most expensive confusion on the lane. Botswana, Namibia, "
        "Eswatini and Lesotho form a customs union with South Africa, with a common external "
        "tariff applied at the first point of entry into the union. Goods moving between members "
        "of that union are not in the same position as goods moving under the wider Southern "
        "African Development Community preference, where a certificate of origin and a rule of "
        "origin have to be satisfied."),
  ("p", "The practical consequence is that the document a consignment needs depends on where "
        "the goods originate and which borders they cross, not on where the truck is going. A "
        "SADC certificate of origin obtained for a movement that never leaves the customs union "
        "is wasted effort; the same certificate missing on a movement that does leave it is a "
        "duty bill. Requirements change, so we confirm the position per consignment with the "
        "revenue authority or a licensed clearing agent rather than relying on how the last one "
        "went."),
  ("h2", "The transit declaration travels with the load"),
  ("p", "On the regional corridors the customs administrations work from a common transit "
        "declaration completed at the office of departure, with continuation and transit control "
        "sheets, and copies move with the consignment to each border post until the destination. "
        "The document set is prepared once and then has to survive the journey."),
  ("p", "That is a different discipline from ocean freight. There is no second chance to correct "
        "a declaration at a land border at two in the morning, and a truck held at a post is "
        "costing demurrage on the trailer and shelf space at the buyer. We route this lane "
        "through a clearing agent who is physically present at the border posts the load will "
        "cross, not one who is excellent in Johannesburg."),
  ("h2", "Paper reels are a handling specification, not a product"),
  ("p", "Newsprint, kraft and containerboard in reels are bought by weight and lost by edge "
        "damage. A reel with a crushed edge is downgraded or scrapped, and most of that damage "
        "happens in handling rather than in transit. Reel diameter and core size have to match "
        "the buyer’s machine, reel weight has to match the lifting equipment at the receiving "
        "end, and the handling method has to be specified: clamp trucks need a reel that can "
        "take clamp pressure, and a facility without them needs reels on pallets."),
  ("p", "The same thinking applies to the rest of the basket. Corrugated packaging arrives flat "
        "and is ruined by moisture; cleaning and facility consumables are bought on a schedule "
        "and fail on stockout, not on price; workwear and protective equipment is bought on a "
        "standard mark and is worthless without it."),
  ("h2", "Why we quote this lane DAP"),
  ("p", "On a corridor where the inland leg carries most of the risk, a port price tells the "
        "buyer very little. DAP puts the ocean freight, the port charges, the transit "
        "documentation and the road leg into one number at the buyer’s own gate, and it puts "
        "the risk of the road leg on the party that selected the transporter, which is us."),
  ("p", "Buyers who want to run their own inland leg can have the price at Durban instead. We "
        "quote both, with the difference shown, because the gap between them is the honest cost "
        "of the part of the journey that most quotations quietly leave out."),
 ],
 "facts": [("Typical cargo", "Newsprint, kraft and containerboard in reels, corrugated packaging, cleaning and facility consumables, workwear and protective equipment, industrial supply"),
           ("Gateway", "Durban to Gaborone and the wider SADC region"),
           ("Terms we quote", "DAP at the buyer’s gate, and the port price at Durban alongside it"),
           ("Trade regime", "SACU and SADC are different regimes; position confirmed per consignment"),
           ("Transit", "Common transit declaration prepared at departure, travels with the load to each border post"),
           ("Reels", "Diameter, core, reel weight and handling method specified against the receiving equipment"),
           ("Clearing", "Agent physically present at the border posts the load will cross")],
 "kw": ["Durban to Gaborone freight", "SADC supply", "SACU customs union", "containerboard reels",
        "DAP delivery Botswana", "industrial supply Southern Africa"],
},
]

# ── описания ровно под обрезку выдачи и вопросы для FAQPage ────────────────
SHORTDESC = {
 "china": "Sourcing from China: how we separate a factory from a trading company, write a "
          "specification that binds, inspect before loading and stage the payment.",
 "turkiye": "Natural stone, tile and building materials from Türkiye to the United States: "
            "block against slab, grading, crating, HTS classification and the duty check.",
 "west-africa": "Frozen poultry, staples and consumables into Lomé and Cotonou: veterinary "
                "admissibility, cut nomenclature, reefer cold chain and payment terms.",
 "southern-africa": "Paper, packaging and industrial supply through Durban into Botswana and "
                    "SADC: why SACU is not SADC, transit paperwork, reels and DAP pricing.",
}

FAQ = {
 "china": [
  ("How do I know a Chinese supplier is a factory and not a trading company?",
   "The business licence shows the registered scope of business and the export licence shows "
   "whether the entity can ship in its own name. The decisive check is the bank account: the "
   "beneficiary on the proforma has to carry the same name as the licence. A mismatch between "
   "the seller name and the beneficiary name is the question, not a detail."),
  ("What should a specification contain before I ask for a price?",
   "For equipment: the drive and controller by make, the electrical standard, the certification "
   "mark required at destination, voltage and frequency, the spares pack and the commissioning "
   "arrangement. For materials: grade, dimension and tolerance against a named standard, the "
   "mill or batch certificate, the finish and the pack. For anything with an appearance, a "
   "sealed reference sample held by both sides."),
  ("Can a trial order be shipped as a full container?",
   "We consolidate several suppliers into one container at the port of loading, which keeps a "
   "trial order on full container economics and produces one bill of lading instead of several. "
   "Consolidation adds about a week to the schedule, and that week belongs in the plan."),
  ("Who is liable if the HS code is wrong?",
   "The importer of record, not the Chinese seller who typed it on the invoice. The code decides "
   "the duty rate at destination, so it is agreed before the order rather than at entry."),
 ],
 "turkiye": [
  ("What is the difference between buying blocks, slabs and finished stone?",
   "A quarry sells blocks by the cubic metre, a factory sells slabs by the square metre cut to "
   "2 cm or 3 cm and bundled by block, and a fabricator sells pieces cut to a drawing. The three "
   "have different prices, packing, waste and counterparties. If you intend to fabricate, bundle "
   "integrity matters more than the unit price, because slabs from different blocks will not "
   "match across a run."),
  ("Is resin treated stone a defect?",
   "No. Most commercial travertine and much marble is resin treated and often mesh backed, which "
   "is normal and has to be declared. Stone sold as unfilled that arrives resin filled is a "
   "claim; stone sold as resin filled is a product."),
  ("Do antidumping duties apply to stone from Türkiye?",
   "Quartz surface products from Türkiye have carried antidumping and countervailing duty "
   "orders since 2020, while quarried stone such as granite, marble, soapstone and quartzite is "
   "excluded from that scope. Rates are reviewed, so the live position must be confirmed at the "
   "time of entry. A cash deposit on a subject product can exceed the value of the goods."),
  ("How is breakage handled?",
   "The allowance, the inspection window and the evidence standard are written into the supply "
   "contract and the sale contract in the same words: photographs at discharge, before the crate "
   "leaves the port. A claim raised weeks later against a seller who has been paid is a "
   "conversation, not a remedy."),
 ],
 "west-africa": [
  ("What has to be checked before a frozen meat offer is real?",
   "The producing establishment has to be admissible in the destination country. Frozen meat "
   "enters on a veterinary health certificate issued for a specific establishment, in a form the "
   "destination accepts, and approval for one West African country does not carry to its "
   "neighbour. We ask for the establishment number and written confirmation before discussing "
   "price."),
  ("Why can two poultry offers not be compared?",
   "Because they are usually not the same product. A whole wing with three joints, a two joint "
   "wing, a drumette and a mid joint flat are four products with four prices. Turkey is sold as "
   "tom or hen and the lines are not interchangeable. Every enquiry has to name the anatomy, the "
   "pack and the Incoterm for each line separately."),
  ("What is the standard pack and container for this lane?",
   "Block frozen product in 10 kg cartons, in a 40ft reefer carrying about 25 tonnes net. That is "
   "not the standard pack in the United States or the European Union, so we ask for the price in "
   "the producer's own pack as well; the difference is what the non-standard format really costs."),
  ("How do the buyer's payment terms change the economics?",
   "A letter of credit payable at sight against shipping documents releases the cash while the "
   "vessel is still at sea. Thirty day terms after arrival add the voyage plus a month to the "
   "cycle, which on a multi container programme is the difference between financing one shipment "
   "and financing four at once. Extended terms are a credit facility and are priced as one."),
 ],
 "southern-africa": [
  ("Is a SADC certificate of origin needed for a delivery from Durban to Gaborone?",
   "Not necessarily. Botswana, Namibia, Eswatini and Lesotho form a customs union with South "
   "Africa with a common external tariff, and that is a different regime from the wider SADC "
   "preference, where a certificate and a rule of origin have to be satisfied. The document a "
   "consignment needs depends on the origin of the goods and the borders crossed, so we confirm "
   "the position per consignment with the revenue authority or a licensed clearing agent."),
  ("What paperwork travels with the truck?",
   "A common transit declaration completed at the office of departure, with continuation and "
   "transit control sheets, copied to each border post until the destination. There is no second "
   "chance to correct it at a land border at night, so it is prepared once and correctly."),
  ("How should paper reels be specified?",
   "By diameter, core size and reel weight matched to the buyer's machine and to the lifting "
   "equipment at the receiving end, plus the handling method. Clamp trucks need a reel that can "
   "take clamp pressure; a site without them needs reels on pallets. Most reel damage happens in "
   "handling, not in transit."),
  ("Why quote DAP instead of a port price?",
   "Because on this lane the inland leg carries most of the risk, and a price at Durban tells the "
   "buyer very little. DAP puts freight, port charges, transit documentation and the road leg "
   "into one number at the buyer's gate and leaves the road risk with the party that chose the "
   "transporter. We show the Durban price alongside it so the difference is visible."),
 ],
}
