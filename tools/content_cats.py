# -*- coding: utf-8 -*-
"""Этап 2: страницы товарных групп."""
from content_core import HOST, ORG, CORRIDOR_LINKS, CATEGORY_LINKS

def rel(slug, extra=None):
    """Три следующие категории по кругу, а не первые три из списка:
    иначе последние в списке никогда не получают входящих ссылок."""
    order = [x[0] for x in CATEGORY_LINKS]
    i = order.index(slug + ".html") if slug + ".html" in order else 0
    items = [CATEGORY_LINKS[(i + k) % len(CATEGORY_LINKS)] for k in range(1, 4)]
    items.append(extra or ("contact.html", "Send a requirement",
                           "Product, quantity and destination port is enough to start."))
    return ("Other categories", "The same method, applied to different goods.", items)

def ld(name, desc, slug, items):
    return [{"@context": "https://schema.org", "@type": "Service", "name": name,
             "description": desc, "provider": ORG, "url": HOST + slug + ".html",
             "hasOfferCatalog": {"@type": "OfferCatalog", "name": name,
               "itemListElement": [{"@type": "Offer", "itemOffered":
                 {"@type": "Product", "name": i}} for i in items]}}]

CATS = [
{
 "slug": "building-materials",
 "title": "Building and finishing materials | import and supply",
 "desc": "Natural stone, porcelain and ceramic tile, cement, insulation, dry mixes, sanitary "
         "ware and cable, bought against EN and ISO standards with the certificates named.",
 "trail": [("ISP Group","index.html"),("What we supply","supply.html"),
           ("Building materials",None)],
 "h1": "Building and <em>finishing materials</em>",
 "sub": "Stone, tile, cement products, insulation, dry mixes, sanitary ware and cable. "
        "Bought against a named standard with the test certificate attached, not against a "
        "photograph in a catalogue.",
 "chips": ["EN &middot; ISO &middot; ASTM &middot; GOST", "FCL and consolidated LCL",
           "T&uuml;rkiye &middot; China &middot; EU"],
 "hero_right": None,
 "img": ("pipe.jpg", 922, 691, "Stacked construction material seen end on",
         "Materials bought to a named standard, with the certificate attached"),
 "lede": ("Finishing materials fail on tolerance, not on price",
   "A tile that is two millimetres out of square, a batch of slabs from three different "
   "blocks, a cable that does not carry the reaction-to-fire class the building needs. None "
   "of these shows in a quotation, and all of them are discovered on site."),
 "body": [
  ("h2","What we buy in this category"),
  ("ul",["<b>Natural stone</b> in blocks, slabs cut to 2 cm or 3 cm, and finished pieces. "
         "Polished, honed or brushed, bundled by block so a run matches.",
         "<b>Porcelain and ceramic tile</b> to ISO 13006 and EN 14411, specified by water "
         "absorption group and by abrasion class rather than by trade name.",
         "<b>Cement products and dry mixes</b>, cement to EN 197-1 class, adhesives and "
         "screeds with the batch certificate.",
         "<b>Insulation</b> to the EN 13162 to 13171 family, specified by declared thermal "
         "conductivity and by thickness, not by brand.",
         "<b>Sanitary ware</b>, ceramics and fittings, with the pressure and flush tests "
         "stated.",
         "<b>Cable and electrical goods</b>, with the reaction-to-fire classification the "
         "destination building code requires."]),
  ("h2","The specification that makes offers comparable"),
  ("p","Tile is the clearest example. “600 by 600 porcelain, grey” is not a "
       "specification: it leaves out the water absorption group, which decides whether the "
       "tile can go outside; the abrasion class, which decides whether it survives a "
       "commercial floor; the rectification, which decides the joint width; the surface "
       "slip rating; and the calibre and shade batch, which decide whether two pallets laid "
       "side by side look like one floor."),
  ("p","We write those into the order before asking for a price, and we ask for the shade "
       "and calibre batch to be held across the whole quantity. A second shipment from the "
       "same factory in a different batch will not match the first, and no discount fixes it."),
  ("h2","Natural stone is three different purchases"),
  ("p","A quarry sells blocks by the cubic metre. A factory sells slabs by the square metre, "
       "bundled by block. A fabricator sells pieces cut to a drawing. Different prices, "
       "different packing, different waste and different people to argue with."),
  ("p","If the buyer intends to fabricate, bundle integrity matters more than the unit price, "
       "because slabs from different blocks will not match across a run. Most commercial "
       "travertine and much marble is resin treated and often mesh backed, which is normal "
       "and has to be declared. Stone sold as unfilled that arrives resin filled is a claim. "
       "The detail is on the <a href=\"turkiye.html\">Türkiye corridor page</a>."),
  ("h2","Packing decides what arrives saleable"),
  ("p","Tile travels on pallets and is lost to corner damage; the pallet has to be strapped "
       "and corner-protected and the stretch wrap has to be real wrap, not three turns. "
       "Stone travels on A-frames or in wooden bundles with the faces separated, and a sealed "
       "crate that cannot breathe marks light material with trapped moisture."),
  ("p","Cement products and dry mixes are hygroscopic: they want a liner and they want to be "
       "loaded last and discharged first. We write the breakage and moisture allowance into "
       "both contracts in the same words, with the same inspection window and the same "
       "evidence standard."),
  ("h2","What the destination will ask for"),
  ("p","Which certificates matter depends entirely on where the goods are going, and this is "
       "settled before the order rather than at the border. In the European Union, "
       "construction products in scope carry a declaration of performance and CE marking. In "
       "the Eurasian customs union the equivalent is the EAC conformity regime. In the United "
       "States the question is usually the HTS classification and whether a trade remedy "
       "order touches the product."),
  ("note","We agree the classification in writing before the order is placed, because the "
          "importer of record is liable for a wrong one and the seller is not."),
 ],
 "facts": [("Typical cargo","Stone, porcelain and ceramic tile, cement products, dry mixes, insulation, sanitary ware, cable"),
           ("Standards","EN 14411 and ISO 13006 for tile, EN 197-1 for cement, EN 13162 to 13171 for insulation"),
           ("Bought by","Water absorption group, abrasion class, calibre and shade batch, declared conductivity"),
           ("Pack","Pallets strapped and corner protected; stone on A-frames or bundled by block"),
           ("Corridors","Tükiye to the United States, China to worldwide, EU"),
           ("Terms","FOB, CIF, DAP")],
 "faq": [("Can you match a tile we already have?",
          "Usually, from a sample or from the original manufacturer's reference. What cannot "
          "be promised is a shade match across batches, because shade is a batch property. If "
          "matching matters, the whole quantity has to come from one batch and that has to be "
          "in the order."),
         ("Do you supply stone by the block or by the slab?",
          "Both, but they are different purchases with different economics. If you are not "
          "running your own saw, buy slabs bundled by block. If you are, blocks can be "
          "cheaper per square metre and you carry the yield risk."),
         ("Who certifies that the material meets the standard?",
          "The producer issues the test report or declaration; we check that the document "
          "names the standard the destination actually requires, which is not always the one "
          "the producer is used to issuing. Where the value justifies it we add third-party "
          "testing before shipment.")],
},
{
 "slug": "industrial-equipment",
 "title": "Industrial equipment and machinery | sourcing and supply",
 "desc": "Production lines, compressors, pumps, generators and material handling, new and "
         "factory refurbished, with the certification mark, voltage and spares pack specified.",
 "trail": [("ISP Group","index.html"),("What we supply","supply.html"),
           ("Industrial equipment",None)],
 "h1": "Industrial equipment <em>and machinery</em>",
 "sub": "Production lines, compressors, pumps, generators, material handling and workshop "
        "equipment. New and factory refurbished, with spares and commissioning arranged "
        "before the machine ships, not after it arrives.",
 "chips": ["New and refurbished", "CE &middot; EAC &middot; UL", "Spares and commissioning",
           "China &middot; EU &middot; T&uuml;rkiye"],
 "img": ("machinery.jpg", 910, 683, "Industrial drive assembly and chain gearing",
         "A machine is bought on its drive, its controller and its spares, not on its price"),
 "lede": ("A machine is the one purchase where the cheapest offer is usually the most expensive",
   "Equipment is bought once and run for ten years. The price difference between two offers "
   "is almost always smaller than the cost of a single week of unplanned downtime in year "
   "three, and the thing that decides which you get is the specification, not the invoice."),
 "body": [
  ("h2","What has to be in the specification"),
  ("p","A purchase order that says “machine, 50 kW, 380 V” leaves the motor brand, the "
       "controller, the duty cycle, the finish, the spares pack and the manual language "
       "entirely to the seller, and the seller resolves every one of them in the direction of "
       "cost. These are the lines we insist on before asking for a price."),
  ("ul",["<b>Drive and controller by make and model.</b> Two machines with identical output "
         "figures and different controllers are different machines when a board fails.",
         "<b>Electrical supply.</b> Voltage and frequency at the destination, and whether "
         "that means 380 to 400 V at 50 Hz or 480 V at 60 Hz. Conversion after the fact costs "
         "more than specifying it.",
         "<b>Certification mark the destination requires.</b> CE for the European Union, EAC "
         "for the Eurasian customs union, UL or CSA where the insurer or the inspector asks "
         "for it.",
         "<b>Ingress protection and ambient.</b> An IP rating and the design ambient "
         "temperature. Equipment specified for a temperate workshop fails in a West African "
         "one.",
         "<b>Duty cycle.</b> Continuous, intermittent or short-time. The single most commonly "
         "omitted line, and the one that decides service life.",
         "<b>Spares pack and consumables</b> for the first period of operation, priced "
         "separately so it can be compared.",
         "<b>Documentation language</b> and whether the electrical schematic is included."]),
  ("h2","New or factory refurbished"),
  ("p","Refurbished equipment is a real market and it is not a lesser one, but it has to be "
       "bought differently. What matters is who refurbished it, what was replaced, what was "
       "only cleaned, whether the control system was updated or merely made to work, and "
       "whether there is a warranty attached to the refurbishment rather than to the original "
       "manufacture."),
  ("p","We ask for the refurbishment report line by line and for a witnessed run before "
       "payment. On a machine with a known service history, that combination is often better "
       "value than a new machine from an unfamiliar producer."),
  ("h2","Inspection means a witnessed run"),
  ("p","For a commodity, inspection is a sampling plan. For a machine it is a factory "
       "acceptance test: the equipment is run under load, against the specification, with "
       "someone present who is not the seller, and the result is recorded with photographs "
       "and readings."),
  ("p","That is also the moment to confirm the spares pack is physically in the crate and "
       "that the schematic is in the document folder, because both are routinely promised and "
       "occasionally shipped."),
  ("h2","Commissioning and what happens after"),
  ("p","Machinery arrives in pieces and the gap between delivery and production is where most "
       "of the disappointment lives. Before the order we settle who assembles it, who "
       "commissions it, whether the producer sends an engineer or supplies instructions, who "
       "pays for the visa and the flights, and what the response time is on a warranty call."),
  ("note","Deliverable on this category: a specification the producer has signed, a witnessed "
          "run report, a spares list priced separately, and a written commissioning "
          "arrangement with named responsibilities."),
  ("h2","Packing and the inland leg"),
  ("p","Heavy equipment is out-of-gauge more often than buyers expect, and an item that does "
       "not fit a standard container changes the freight cost by a multiple rather than a "
       "percentage. Dimensions and weights are confirmed from the drawing before we quote, "
       "not from the brochure. Wood packaging is heat treated and marked under ISPM 15, "
       "checked at loading rather than at arrival."),
 ],
 "facts": [("Typical cargo","Production lines, compressors, pumps, generators, material handling, workshop equipment"),
           ("Condition","New and factory refurbished, with the refurbishment report line by line"),
           ("Specified by","Drive and controller by make, voltage and frequency, certification mark, IP rating, duty cycle"),
           ("Before payment","Factory acceptance test under load, witnessed, with readings and photographs"),
           ("Included","Spares pack priced separately, schematic, manual in the agreed language"),
           ("Corridors","China to worldwide, European Union, Tükiye")],
 "faq": [("Can you arrange commissioning at our site?",
          "We arrange it with the producer and write it into the contract: who travels, who "
          "pays for the travel, how long they stay and what the warranty response time is. "
          "That is settled before the order, because afterwards it is a negotiation with no "
          "leverage."),
         ("What voltage will the machine be built for?",
          "Whatever you specify, if it is specified before the order. Say the voltage and the "
          "frequency at the destination. Converting after delivery costs more than the "
          "difference ever did."),
         ("Is refurbished equipment worth the risk?",
          "It can be clearly better value, but only against a refurbishment report that says "
          "what was replaced rather than what was serviced, a warranty attached to the "
          "refurbishment, and a witnessed run before payment.")],
},
{
 "slug": "tools-hardware",
 "title": "Tools, hardware and fasteners | import and supply",
 "desc": "Power and hand tools, abrasives, measuring instruments, fixings and consumables, "
         "supplied to specification or to brand with the safety marks the destination needs.",
 "trail": [("ISP Group","index.html"),("What we supply","supply.html"),
           ("Tools and hardware",None)],
 "h1": "Tools, hardware <em>and fasteners</em>",
 "sub": "Power and hand tools, abrasives, measuring instruments, fixings and consumables. "
        "To your specification or to a named brand, with the safety marking the destination "
        "requires rather than the one the factory usually prints.",
 "chips": ["To spec or to brand", "IEC &middot; EN &middot; ISO", "Own-brand packaging",
           "China &middot; T&uuml;rkiye"],
 "img": ("machinery.jpg", 910, 683, "Workshop tooling and drive components",
         "Tooling is bought on the grade of its consumable, not on the body"),
 "lede": ("The cheap part of the tool is the tool",
   "On almost everything in this category the purchase price is a small fraction of the "
   "running cost. An abrasive that lasts two thirds as long is not thirty per cent cheaper, "
   "it is fifty per cent more expensive, and nothing in a product photograph shows which one "
   "you are being offered."),
 "body": [
  ("h2","Three different ways to buy the same box"),
  ("ul",["<b>To a named brand.</b> You know what you are getting and you pay for it. Our job "
         "is authenticity and landed cost, and the first check is whether the seller is an "
         "authorised channel.",
         "<b>To specification, unbranded.</b> A factory builds to your written specification "
         "and your packaging. Cheaper per unit, slower to set up, and only works if the "
         "specification is real.",
         "<b>Own brand.</b> The same as above with your mark, your carton and your manual. "
         "Minimum quantities rise, and the artwork and the safety text become part of the "
         "order."]),
  ("p","Most disappointments in this category come from buying the second while thinking "
       "about the first: a specification that says “equivalent to” a brand, with nothing "
       "measurable after it."),
  ("h2","What makes a tool specification measurable"),
  ("p","For power tools: input power and, more usefully, output power; no-load speed; the "
       "bearing type; the switch and brush assembly by make; the cable length and plug type "
       "for the destination; the voltage and frequency; the insulation class; and the "
       "electrical safety standard the destination enforces, which for most of the world is "
       "the IEC 62841 family."),
  ("p","For abrasives: the grit, the bond, the maximum operating speed and the safety "
       "standard, because a cutting disc is a safety-critical product and EN 12413 exists "
       "for a reason. For measuring instruments: the accuracy class and whether a calibration "
       "certificate is supplied and traceable."),
  ("p","For fixings: the grade and the coating, which together decide both the strength and "
       "the service life. A property class 8.8 bolt and a 4.6 bolt look identical in a "
       "photograph and are not interchangeable in a structure."),
  ("h2","Personal protective equipment is a legal product"),
  ("p","Gloves, footwear, eye protection and hearing protection are not ordinary consumables. "
       "They are sold against harmonised standards, they carry a mark, and in most "
       "destinations supplying them without valid conformity documentation is an offence "
       "rather than a commercial problem."),
  ("p","We ask for the test report from a named laboratory, not a certificate image, and we "
       "check the standard cited is the one in force at the destination. This is the single "
       "most counterfeited document category in the hardware trade."),
  ("h2","Assortment, minimums and the consolidated container"),
  ("p","Hardware is bought as an assortment, and an assortment rarely fills a container from "
       "one factory. We consolidate several producers into one container at the port of "
       "loading, which keeps a mixed order on full container economics and produces one bill "
       "of lading instead of six."),
  ("p","Consolidation adds about a week to the schedule and it has to be in the plan rather "
       "than discovered. It also means one packing list has to reconcile against several "
       "suppliers' cartons, which is exactly the kind of discrepancy customs resolves by "
       "inspecting, so the counting is done at the consolidation warehouse and photographed."),
  ("note","Deliverable on this category: a written specification per line, the conformity "
          "documents checked against the destination's standard, and a consolidated packing "
          "list reconciled carton by carton before the container is sealed."),
 ],
 "facts": [("Typical cargo","Power and hand tools, abrasives, measuring instruments, fixings and fasteners, PPE and consumables"),
           ("Bought as","Named brand through an authorised channel, to specification unbranded, or own brand"),
           ("Standards","IEC 62841 for power tools, EN 12413 for bonded abrasives, property class for fasteners"),
           ("PPE","Test report from a named laboratory, standard checked against the destination"),
           ("Load","Consolidated LCL into one FCL, packing list reconciled at the warehouse"),
           ("Corridors","China to worldwide, Tükiye")],
 "faq": [("Can you make it under our own brand?",
          "Yes. Minimum quantities rise and the artwork, the manual and the safety text "
          "become part of the order rather than an afterthought. We ask for a pre-production "
          "sample of the printed carton, not just of the product."),
         ("How do we know PPE certificates are genuine?",
          "By asking for the test report from the named laboratory and checking the "
          "laboratory exists and issued it, rather than accepting an image of a certificate. "
          "This category is the most counterfeited in the trade."),
         ("Our order is small and mixed. Is that a problem?",
          "No, it is the normal case. We consolidate several producers into one container at "
          "the port of loading. It adds roughly a week to the schedule and keeps the "
          "economics of a full container.")],
},
{
 "slug": "metals-pipe",
 "title": "Metals and pipe | sections, plate, seamless and welded",
 "desc": "Structural sections, sheet and plate, seamless and welded pipe, fittings and "
         "flanges to EN, ASTM or GOST, with EN 10204 mill certificates.",
 "trail": [("ISP Group","index.html"),("What we supply","supply.html"),("Metals and pipe",None)],
 "h1": "Metals <em>and pipe</em>",
 "sub": "Structural sections, sheet and plate, seamless and welded pipe, fittings and flanges. "
        "To EN, ASTM or GOST, with the mill certificate that proves it.",
 "chips": ["EN &middot; ASTM &middot; GOST", "EN 10204 3.1 certificates",
           "Seamless and welded", "Mill direct"],
 "img": ("pipe.jpg", 922, 691, "Stacked steel pipe seen end on",
         "Pipe is bought on the certificate as much as on the dimension"),
 "lede": ("In metals the document is half the product",
   "Two lengths of pipe can be dimensionally identical and commercially worth very different "
   "money, because one has a mill test certificate traceable to the heat it was rolled from "
   "and the other has a piece of paper. On anything that will be welded, pressurised or "
   "inspected, the certificate is the product."),
 "body": [
  ("h2","What we buy"),
  ("ul",["<b>Structural sections</b>: beams, channels, angles and hollow sections to EN "
         "10025 grades or the ASTM equivalents, in the profile series the design actually "
         "calls for.",
         "<b>Sheet and plate</b>, hot and cold rolled, by grade, thickness tolerance and "
         "surface condition.",
         "<b>Seamless and welded pipe</b>, by outside diameter and wall thickness or by "
         "schedule, to the pressure standard the application requires.",
         "<b>Fittings and flanges</b> to ANSI or ASME B16.5, EN 1092-1 or the GOST series, "
         "matched to the pipe standard rather than assumed to fit.",
         "<b>Fasteners and structural bolting</b> by property class and coating."]),
  ("h2","The certificate, and why 3.1 is the line"),
  ("p","EN 10204 defines the inspection documents. A type 2.2 test report is the producer's "
       "own statement of general conformity. A type 3.1 certificate is issued by the "
       "producer's own inspection function, independent of the manufacturing department, and "
       "states the actual test results for the material supplied, traceable to the heat "
       "number. A type 3.2 adds a third party."),
  ("p","On anything structural or pressure-bearing, 3.1 is normally the minimum that an "
       "engineer, an insurer or a customs authority will accept. Asking for “a certificate” "
       "and receiving a 2.2 is the commonest quiet downgrade in this trade, and it is "
       "invisible until the material is already on site."),
  ("note","We state the required document type in the order, we check the heat numbers on the "
          "certificate against the markings on the material at loading, and we photograph "
          "both."),
  ("h2","Three standards families that do not map one to one"),
  ("p","EN, ASTM and GOST are not translations of each other. Grades that are commonly treated "
       "as equivalent differ in chemistry, in impact testing temperature and in permitted "
       "tolerance. A material sold as “analogue of” a grade is not that grade, and if the "
       "destination's inspector works to one family, that is the family the certificate has "
       "to be issued under."),
  ("p","Where a project genuinely needs cross-standard supply, the right move is to name the "
       "standard in the purchase order and have the mill certify to it, which most mills of "
       "reasonable size can do if it is agreed before rolling rather than after."),
  ("h2","Tolerance, length and what arrives bent"),
  ("p","Thickness tolerance, straightness, ovality on pipe and end condition are all "
       "negotiable and all routinely unstated. Mill lengths differ by producer, and a "
       "specification that asks for exact lengths carries a cutting cost and a yield loss "
       "that has to be priced rather than discovered."),
  ("p","Pipe and sections are loaded in bundles and damaged on the ends. Bundles are strapped, "
       "end caps are specified where the application needs clean ends, and dunnage is "
       "written into the order because a container of steel that has shifted in transit is "
       "both a claim and a discharge problem."),
  ("h2","Weight, not pieces"),
  ("p","Metals are invoiced by weight and a container fills on weight long before it fills on "
       "volume. A 20ft container is usually the right box for dense cargo even when it looks "
       "half empty, and the theoretical weight against actual weighbridge weight is a line "
       "that has to be agreed in the contract, because the two are never identical."),
 ],
 "facts": [("Typical cargo","Structural sections, sheet and plate, seamless and welded pipe, fittings, flanges, structural bolting"),
           ("Standards","EN 10025 and the EN series, ASTM, GOST. Named in the purchase order, not assumed"),
           ("Documents","EN 10204 type 3.1 as the normal minimum; 3.2 where a third party is required"),
           ("Checked at loading","Heat numbers on the certificate against the markings on the material, photographed"),
           ("Pack","Bundled and strapped, dunnage specified, end caps where the application needs them"),
           ("Invoiced","By weight, with theoretical against weighbridge agreed in the contract")],
 "faq": [("What is the difference between a 2.2 and a 3.1 certificate?",
          "A 2.2 is the producer's general statement of conformity. A 3.1 states the actual "
          "test results for the material supplied, is issued by an inspection function "
          "independent of manufacturing, and is traceable to the heat number. On structural "
          "and pressure work, 3.1 is normally the minimum anyone will accept."),
         ("Can you supply GOST material against an EN design?",
          "We can have a mill certify to the standard named in the purchase order, if it is "
          "agreed before rolling. What we will not do is supply an “analogue” grade and "
          "let the buyer discover at inspection that the chemistry and the impact testing "
          "are different."),
         ("Is a 20ft or a 40ft container better for steel?",
          "Usually 20ft. Dense cargo reaches the weight limit long before it fills the "
          "volume, so a 40ft box ships mostly air and costs more per tonne.")],
},
{
 "slug": "paper-packaging",
 "title": "Paper, packaging and consumables | reels and corrugated",
 "desc": "Newsprint, kraft and containerboard in reels, corrugated packaging, cleaning and "
         "facility consumables, workwear and protective equipment.",
 "trail": [("ISP Group","index.html"),("What we supply","supply.html"),
           ("Paper and packaging",None)],
 "h1": "Paper, packaging <em>and consumables</em>",
 "sub": "Newsprint, kraft and containerboard in reels, corrugated packaging, cleaning and "
        "facility consumables, workwear and protective equipment. Bought on grammage and "
        "strength, handled on reel weight.",
 "chips": ["Reels and sheets", "Grammage &middot; ECT &middot; burst",
           "Schedule supply", "Durban &middot; EU &middot; Americas"],
 "img": ("crane.jpg", 834, 625, "Quayside crane against an open sky",
         "Paper is bought by the tonne and lost on the edge of a reel"),
 "lede": ("Reels are a handling specification before they are a product",
   "A reel with a crushed edge is downgraded or scrapped, and most of that damage happens in "
   "handling rather than in transit. Which means the right questions are about the receiving "
   "end, not about the mill."),
 "body": [
  ("h2","What the grade actually means"),
  ("p","Paper is specified by grammage in grams per square metre and by the strength property "
       "that matters for its use. For containerboard that is usually burst strength or edge "
       "crush resistance, measured to ISO methods, and for anything that will be printed or "
       "glued it is also the surface sizing, measured by the Cobb test."),
  ("p","A quotation that gives only the grammage is giving one of three numbers. Two reels at "
       "the same grammage with different edge crush values make boxes with different stacking "
       "strength, and the box is where the customer notices."),
  ("ul",["<b>Newsprint</b> by grammage and brightness.",
         "<b>Kraft and containerboard</b> by grammage, burst or edge crush, and Cobb.",
         "<b>Corrugated packaging</b> by flute, board combination and box compression, with "
         "a sample board specified rather than described.",
         "<b>Cleaning and facility consumables</b> on a schedule, because they fail on "
         "stockout rather than on price.",
         "<b>Workwear and protective equipment</b> on a standard mark, which is worthless "
         "without a traceable test report."]),
  ("h2","Reel diameter, core and weight"),
  ("p","Three dimensions decide whether a reel can be used at all: the width, which has to "
       "match the machine; the core diameter, which has to match the shaft; and the reel "
       "diameter and weight, which have to match the lifting equipment at the receiving end."),
  ("p","The last one is the one that gets missed. A mill will happily supply a reel at its "
       "standard diameter, and a buyer whose site has no clamp truck will then be unable to "
       "move it off the vehicle. Clamp handling also needs a reel that can take clamp "
       "pressure without ovalising, and a facility without clamps needs reels on pallets, "
       "which changes both the price and the loading plan."),
  ("note","We ask three questions before quoting reels: what lifts it at your end, what is "
          "the maximum weight that equipment handles, and is there a dock or is it a ground "
          "level discharge."),
  ("h2","Moisture is the whole risk in transit"),
  ("p","Paper is hygroscopic and a container crossing the tropics condenses on its roof at "
       "night. Reels loaded against a bare steel wall arrive with a wet edge. The pack has to "
       "include a liner or desiccant and the loading plan has to keep product off the walls "
       "and the floor, which means dunnage and a loading photograph showing it."),
  ("p","Corrugated packaging arrives flat and is ruined by the same mechanism, with the added "
       "problem that nobody discovers it until the boxes are being erected weeks later. The "
       "inspection window in the contract has to be long enough to be real and short enough "
       "to be provable."),
  ("h2","Consumables are a schedule, not a purchase"),
  ("p","Cleaning and facility supply has a different failure mode from everything else on "
       "this page: the cost of being out of stock is far higher than any price difference. "
       "The useful structure is a standing programme with an agreed call-off and a safety "
       "stock held either at origin or at destination, priced accordingly."),
  ("p","On the <a href=\"southern-africa.html\">Durban corridor</a> we usually quote this "
       "category DAP at the buyer's own gate, because on a long inland leg the port price "
       "tells the buyer very little."),
 ],
 "facts": [("Typical cargo","Newsprint, kraft and containerboard in reels, corrugated packaging, cleaning and facility consumables, workwear and PPE"),
           ("Specified by","Grammage, burst strength or edge crush, Cobb, flute and board combination"),
           ("Reels","Width, core diameter, reel diameter and weight matched to the receiving equipment"),
           ("Handling","Clamp or pallet, confirmed before quoting, with dunnage in the loading plan"),
           ("Moisture","Liner or desiccant, product off the walls and floor, loading photographed"),
           ("Corridors","Durban into SADC, European Union, Americas")],
 "faq": [("What do you need to know before quoting reels?",
          "The machine width, the core diameter, and what lifts the reel at your end with its "
          "maximum weight. The third question is the one most often skipped, and it is the "
          "one that strands a container on a vehicle."),
         ("How is moisture damage prevented?",
          "A liner or desiccant in the container, product kept off the walls and the floor "
          "with dunnage, and a loading photograph that shows it. The mechanism is condensation "
          "on the container roof at night, not rain."),
         ("Can you hold stock for a consumables programme?",
          "Yes, either at origin or at destination, with an agreed call-off. On consumables "
          "the cost of a stockout is usually larger than any price difference, so the safety "
          "stock is worth paying for and we price it openly.")],
},
{
 "slug": "food-agricultural",
 "title": "Food and agricultural goods | frozen protein and staples",
 "desc": "Frozen and chilled protein, bulk staples and food ingredients, handled under "
         "veterinary and sanitary certification for the destination country.",
 "trail": [("ISP Group","index.html"),("What we supply","supply.html"),
           ("Food and agricultural goods",None)],
 "h1": "Food and <em>agricultural goods</em>",
 "sub": "Frozen and chilled protein, bulk staples and food ingredients. The price is the last "
        "question on this category, because an offer from an establishment that cannot legally "
        "ship to the destination is not an offer.",
 "chips": ["40ft reefer, 25 t net", "Block frozen, 10 kg cartons",
           "Establishment approval first", "CIF &middot; CFR"],
 "img": ("vessel2.jpg", 774, 581, "Container vessel alongside with boxes loaded",
         "Reefer programmes run to a schedule, not to a spot booking"),
 "lede": ("Admissibility, nomenclature, cold chain, then price",
   "Those four, in that order. Most of the cheap offers in this trade fail one of the first "
   "three, and a buyer who starts at the fourth will spend a month discovering it."),
 "body": [
  ("h2","Admissibility comes before price"),
  ("p","Frozen meat does not enter a country on a commercial invoice. It enters on a "
       "veterinary health certificate issued for a specific producing establishment, in a "
       "form the destination accepts. An establishment approved for one country is not "
       "automatically approved for its neighbour, and the requirements change."),
  ("p","The first question to any seller is the establishment number and written "
       "confirmation that it is cleared for the destination, before price is discussed. "
       "How certification works for United States and European Union origin, which form "
       "is issued and who signs it, is in the "
       "<a href=\"veterinary-certificate.html\">veterinary certificate guide</a>, and the "
       "lane itself on the <a href=\"west-africa.html\">West Africa corridor page</a>."),
  ("h2","Specify the cut by anatomy, not by category"),
  ("p","Every enquiry we send names the anatomy explicitly, names the pack and asks for "
       "the price per line on the same Incoterm, because a category name covers several "
       "products at several prices. The same discipline applies to grading on staples "
       "and to piece weight on anything portioned."),
  ("p","The full nomenclature, and why two offers using the same word are not "
       "comparable, is in <a href=\"poultry-cuts.html\">the cuts guide</a>."),
  ("h2","Pack and cold chain are part of the specification"),
  ("p","Many destination markets buy block frozen product in 10 kg cartons, which is not the "
       "standard pack in the United States or in the European Union. Repacking is possible "
       "and it costs money, so the price has to be asked for in the producer's own pack as "
       "well; the difference is what the non-standard format is actually worth."),
  ("p","A 40ft reefer carries about 25 tonnes net. The temperature is set at loading, recorded "
       "throughout and read at discharge, and the recorder tape belongs in the document set "
       "rather than in a drawer. Plug time at the transhipment port and at the destination is "
       "the part of the chain nobody books and everybody assumes."),
  ("h2","Bulk staples and ingredients"),
  ("p","Rice, sugar, pulses, flour and oils move on specification and on sanitary "
       "documentation rather than on veterinary certification, which makes them simpler to "
       "originate and no simpler to land. The lines that decide a claim are moisture, "
       "broken percentage or equivalent grading, foreign matter, packing weight tolerance and "
       "the sampling method at discharge. Those are agreed in the contract or they are "
       "argued about afterwards."),
  ("h2","Compare the market, not the quotations"),
  ("p","A quotation is what a seller would like to receive. Customs statistics show what the "
       "goods actually crossed a border at, because the declared value is divided by the "
       "declared net weight and every discount the seller really gave is already inside that "
       "number. Before we negotiate a lane we pull the destination's import values by origin "
       "and by commodity code for the most recent full periods and negotiate against that."),
  ("note","On this category that exercise regularly moves the target by a fifth or more, and "
          "it changes which origin we approach first. The method is set out in "
          "<a href=\"customs-data-pricing.html\">how customs data shows the real price</a>."),
 ],
 "facts": [("Typical cargo","Frozen and chilled poultry and protein, bulk staples, food ingredients"),
           ("First question","Establishment number and written confirmation of admissibility at the destination"),
           ("Equipment","40ft reefer, about 25 t net, temperature recorded and read at discharge"),
           ("Pack","Block frozen in 10 kg cartons where the market needs it, producer pack priced in parallel"),
           ("Specification","Anatomy named per line, tom or hen for turkey, grading agreed for staples"),
           ("Corridors","Americas and EU into West Africa, with Lomé and Cotonou priced separately")],
 "faq": [("Why do you ask for the establishment number before discussing price?",
          "Because an establishment that is not approved for the destination cannot ship, "
          "whatever it quotes. Approval for one country does not carry to its neighbour, and "
          "the requirements change, so we want the number and written confirmation before "
          "anything else."),
         ("Can you supply in our own pack format?",
          "Usually, but ask for both prices. Repacking from the producer's standard format "
          "costs money, and seeing the two numbers side by side tells you what the "
          "non-standard pack is really worth."),
         ("How is the cold chain evidenced?",
          "The temperature is set at loading, recorded throughout and read at discharge, and "
          "the recorder output is part of the document set. Plug time at transhipment and at "
          "the destination is booked rather than assumed.")],
},
]
