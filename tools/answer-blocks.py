# -*- coding: utf-8 -*-
"""Блок прямого ответа в начало каждого руководства.

Зачем. Страницы написаны подробно и по делу, но ответ на вопрос из
заголовка собирается только после пяти разделов. Человеку, который
пришёл за этим ответом, приходится читать всё, а машине, которая
подбирает, что процитировать, зацепиться не за что: связный довод на
три экрана в ответ не вынесешь.

Блок решает оба случая сразу. Четыре строки, каждая начинается с сути,
дальше одно уточняющее предложение. Подробности ниже никуда не
деваются, и это не выжимка ради поисковика: тот же блок экономит время
живому читателю.

Содержание не придумано. Каждая строка собрана из самой страницы, из
её разделов, и ничего нового в ней не утверждается.

Французские страницы получают французский блок, заголовок «En bref».

Запуск: python3.13 tools/answer-blocks.py
Повторный запуск ничего не дублирует.
"""
import pathlib, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

# страница -> (заголовок блока, [(суть, уточнение)], сноска или None)
DATA = {

"about.html": ("The short answer", [
 ("Principal, not an agent.", "We buy in our own name, so the contract, the payment and the responsibility sit with one company."),
 ("Verification before the quote.", "Establishment and licence numbers are checked against the registers of the importing country, not taken from the seller's website."),
 ("The asset is the lane, not the product.", "A working route is a set of verified producers, a forwarder, a customs broker and a document set, and the goods travelling down it can change."),
 ("What we do not do.", "We do not quote on a specification we have not read, we do not prepay a producer in full, and we do not put a commission on someone else's invoice and call it a service."),
], "Registered in Florida, United States. UEI WA46PAMTYMQ7, CAGE 217F4."),

"antidumping-check.html": ("The short answer", [
 ("Two separate remedies.", "Antidumping answers a sale below normal value, countervailing answers a subsidy. Both are imposed per country of origin and usually per producer."),
 ("Scope is written in words, not in codes.", "The order describes the subject merchandise. Commodity codes are listed for convenience and they are not the test."),
 ("In the United States what you pay at entry is a deposit.", "The final liability is set later in an administrative review, and it can be higher than the amount deposited."),
 ("A rate has a date on it.", "Rates change in reviews and new producers obtain their own, so a figure confirmed six months ago is not a figure confirmed today."),
], "The check is run against the named producer and the exact origin, before the order rather than at the border."),

"bill-of-lading.html": ("The short answer", [
 ("A negotiable original is title to the cargo.", "It is issued in a set of three, any one of which releases the goods, and the other two then become void."),
 ("The consignee decides who can collect.", "Straight to a named buyer gives the seller no leverage after shipment. To order of the shipper keeps control until the bill is endorsed."),
 ("Telex release is not a telex.", "The shipper surrenders all originals to the carrier at the origin and the carrier releases at the destination without paper."),
 ("A house bill is only as good as the forwarder who issued it.", "The ocean carrier issues the master bill to the forwarder, and the buyer deals with the house bill."),
], "Settle in the contract which type is issued, who is consignee and notify, how many originals, who couriers them and by when."),

"building-materials.html": ("What makes offers comparable", [
 ("Tile needs four figures, not two.", "Water absorption group, abrasion class, rectified or not, and the standard. Six hundred by six hundred grey is not a specification."),
 ("Natural stone is three different purchases.", "A quarry sells blocks by the cubic metre, a factory sells slabs by the square metre bundled by block so a run matches, a fabricator sells pieces cut to a drawing."),
 ("Packing decides what arrives saleable.", "Tile is lost to corner damage and stone to faces touching, so the pallet, the strapping and the face separation are specified rather than assumed."),
 ("The destination decides the certificates.", "In the European Union a construction product in scope carries a declaration of performance, and that is settled before the order."),
], None),

"certificate-of-origin.html": ("The short answer", [
 ("Two different documents under one name.", "A non-preferential certificate says who made the goods. A preferential one claims a reduced duty under a named agreement, which is why it is worth money."),
 ("Origin is not the shipping address.", "For anything made from imported inputs it is decided by substantial transformation, under the rule written into the agreement."),
 ("The wrong issuer voids it.", "Preferential forms generally have one competent authority per country, and a chamber of commerce certificate will not substitute."),
 ("Naming the trader as producer voids it too.", "If the exporter on the certificate is not the manufacturer, the document has to say so."),
], None),

"china.html": ("The short answer", [
 ("A factory and a trading company answer your enquiry the same way.", "The business licence names what the company manufactures, and the registered scope is the test, not the website."),
 ("The specification is the only thing that binds.", "Machine, fifty kilowatts, three eighty volts leaves the motor brand, the controller, the duty cycle and the spares to the seller, and he resolves each one in his own favour."),
 ("Inspect before the balance and before loading.", "A sampling plan against the specification for a commodity, a witnessed run for equipment, photographs of the goods and the container seal number for everything."),
 ("Pay against events, not dates.", "A deposit releases production, the second instalment falls due against inspection, and the balance against the document set."),
], "Several suppliers are consolidated into one container at the port of loading, which keeps a first order on full container economics."),

"container-loading.html": ("The short answer", [
 ("Plan to the booking, not to the last kilogram.", "A twenty foot general purpose box holds roughly thirty three cubic metres, and dense cargo fills it on weight long before it fills on volume."),
 ("Verified gross mass is a legal requirement, not paperwork.", "The shipper declares it before the box is loaded on the vessel, by weighing the packed container or the cargo plus the tare."),
 ("Less than container load is often false economy.", "Destination charges are per cubic metre and they are high, and the consignment is handled at a deconsolidation warehouse."),
 ("Consolidation is the option most buyers never ask for.", "Several suppliers in one container gives full container economics, one bill of lading and one customs entry instead of four."),
], None),

"customs-data-pricing.html": ("The short answer", [
 ("A unit value is a record, not an opinion.", "Declared value divided by declared net weight, for one commodity code and one partner country, is what the goods actually crossed the border at."),
 ("Where to get it.", "UN Comtrade at six digits is the fastest way to compare several origins into one destination. National sources go further: ten digits in the United States."),
 ("The trap that ruins the comparison.", "Most countries record imports at CIF and exports at FOB, so comparing the two compares a delivered price with a factory gate price."),
 ("Use it as a band, not as a number.", "Thin flows are dropped and a target range is set before any producer is approached."),
], None),

"demurrage-detention.html": ("The short answer", [
 ("Two clocks, not one.", "Demurrage is the container occupying space in the terminal. Detention is the container outside the terminal and not yet returned."),
 ("Free time is negotiated at the booking.", "It is routinely extendable before and almost never extendable afterwards, which is the whole point of asking early."),
 ("The clock runs for paperwork, not for cargo.", "Originals still in the post, a telex release not actioned, a tariff code queried by customs."),
 ("Carrier haulage puts the line's own interest on your side.", "With your own haulier the detention clock still runs and nobody at the carrier is in a hurry."),
], None),

"food-agricultural.html": ("The short answer", [
 ("Admissibility comes before price.", "Frozen meat enters a country on a veterinary health certificate issued for a specific establishment, not on a commercial invoice."),
 ("Name the cut by anatomy, not by category.", "A category name covers several products at several prices, so each line is quoted separately and on the same Incoterm."),
 ("Pack is part of the specification.", "Many destination markets buy block frozen product in ten kilogram cartons, which is not the standard pack in the United States or the European Union."),
 ("A brand name is not an article.", "The same brand covers recipes and formats that are not interchangeable and do not trade at the same price, so the article is identified by its EAN."),
], None),

"hs-code.html": ("The short answer", [
 ("The importer of record is liable, not the seller who typed it.", "Underpaid duty is recovered from the importer with interest, often years later in an audit rather than at entry."),
 ("The first six digits are the same everywhere.", "Beyond six each territory extends the code for its own tariff, so the seller's domestic code is not your code."),
 ("Classify on what the thing is, not on what it is for.", "The structure classifies by material, function or state, and classifying by intended use is the commonest amateur error."),
 ("Make it binding before you order.", "Customs administrations issue advance rulings that bind them: a binding ruling in the United States, Binding Tariff Information in the European Union."),
], None),

"incoterms.html": ("The short answer", [
 ("Read the risk column before the cost column.", "Eleven rules in the 2020 edition, each answering how far the seller pays, where risk transfers, and who handles clearance."),
 ("CFR and CIF split cost from risk deliberately.", "The seller pays the freight to the destination port, but the risk passes to the buyer when the goods are on board at the origin."),
 ("FOB is the wrong rule for a container.", "The seller loses physical control at the container terminal, days before the ship's rail that FOB was written around."),
 ("Which to ask for.", "FCA at the named terminal if you have your own forwarder and rates. CIF or CFR at your port if you want one number and no logistics."),
], None),

"industrial-equipment.html": ("The short answer", [
 ("The specification decides who wins every omission.", "Motor brand, controller, duty cycle, finish, spares pack and manual language are resolved in the seller's favour if they are left out."),
 ("Refurbished is a real market, bought differently.", "Who refurbished it, what was replaced, what was only cleaned, and whether the control system was updated or merely repainted."),
 ("Inspection means a witnessed run.", "A factory acceptance test under load, against the specification, with someone present who is not the seller, and the result recorded."),
 ("Commissioning is where the disappointment lives.", "Who assembles it, who commissions it, whether the producer sends an engineer, is settled before the order and not after arrival."),
], "Heavy equipment is out of gauge more often than buyers expect, and that changes the freight cost by a multiple rather than a percentage."),

"ispm-15.html": ("The short answer", [
 ("It covers the wood holding your cargo.", "Pallets, crates, cases, boxes, drums, dunnage, blocking and bracing. Processed wood based materials are out of scope."),
 ("The mark on the wood is the proof.", "Heat treatment to a specified core temperature and duration, or fumigation, applied by an authorised facility and stamped on the timber itself."),
 ("Failure is at the importer's cost.", "Treatment at the port where that is available, re-export or destruction of the packaging, and in the worst case refusal of the whole consignment."),
 ("Check at loading, not at arrival.", "Photograph the mark on the pallets actually used, and the dunnage and bracing too, because loose timber is what usually fails."),
], None),

"landed-price.html": ("The short answer", [
 ("A factory price is not a price.", "Origin inland, export clearance, freight, insurance, terminal handling, duty, the broker and the inland leg all sit between it and your own gate."),
 ("Three lines are always missing.", "Demurrage and detention at the destination, the validity date on the freight, and the inland leg from port to gate."),
 ("A price without a validity date is a price for an unknown day.", "Freight rates are quoted with an expiry and they move sharply."),
 ("VAT belongs in cash flow, not in margin.", "It is recoverable by a registered importer, but it is paid at clearance and recovered weeks or months later."),
], None),

"letter-of-credit.html": ("The short answer", [
 ("Banks deal in documents, not in goods.", "The bank never sees the cargo. It examines whether the presentation complies on its face with the credit."),
 ("Sight or usance decides who finances the shipment.", "A sight credit pays a few banking days after shipment. A usance credit pays thirty, sixty or ninety days later and the seller carries it."),
 ("Confirmation moves the risk.", "An unconfirmed credit carries the issuing bank and its country. A confirmed credit adds a second bank, usually in the seller's country, which undertakes to pay independently."),
 ("Credits fail on discrepancies, not on bad faith.", "A spelling difference, a bill of lading dated one day outside the shipment window, a certificate signed by the wrong function."),
], "On a small shipment the bank charges on both legs are a visible share of the value, and a documentary collection is cheaper and weaker."),

"metals-pipe.html": ("The short answer", [
 ("EN 10204 type 3.1 is the line.", "A type 2.2 report is the producer's own general statement. A 3.1 certificate is issued by an inspection function independent of production."),
 ("EN, ASTM and GOST are not translations of each other.", "Grades commonly treated as equivalent differ in chemistry, in impact testing temperature and in permitted tolerance."),
 ("Tolerance is negotiable and routinely unstated.", "Thickness, straightness, ovality on pipe and the end condition all have to be written into the order."),
 ("Metals are bought by weight.", "A container fills on weight long before it fills on volume, so a twenty foot box is usually the right one even when it looks half empty."),
], None),

"paper-packaging.html": ("The short answer", [
 ("A grade is grammage plus a strength property.", "For containerboard that is usually burst strength or edge crush resistance, measured to ISO methods."),
 ("Three reel dimensions decide whether it can be used at all.", "The width has to match the machine, the core diameter has to match the shaft, and the reel diameter and weight have to match the handling equipment."),
 ("Moisture is the whole risk in transit.", "A container crossing the tropics condenses on its roof at night, and a reel loaded against a bare steel wall arrives with a wet edge."),
 ("Consumables are a schedule, not a purchase.", "Being out of stock costs more than any price difference, so the useful structure is a standing programme rather than a one-off order."),
], None),

"poultry-cuts.html": ("The short answer", [
 ("A whole wing is three sections.", "The drumette closest to the body, the mid joint or flat in the middle, and the tip at the end. Each trades as its own product."),
 ("Tom and hen are not grades of the same thing.", "The male and female turkey lines are raised to different weights and give different piece sizes, and for a processor buying to a portion weight they are not interchangeable."),
 ("Every part has its own market.", "A cut that is a by-product in one country is a staple in another, which is the whole reason this trade exists."),
 ("A usable enquiry names five things.", "The cut by anatomy, tom or hen with the piece weight range, the pack, the Incoterm and named port, and the monthly volume."),
], "On a mixed programme the composition of the basket is usually worth more than the discount."),

"proforma-invoice.html": ("The short answer", [
 ("A proforma is an offer, not a demand for payment.", "The commercial invoice is the demand, issued when the goods ship, and it is the document customs values the consignment on."),
 ("It has to carry the registered names.", "Legal names and addresses as registered rather than trading names, a proforma number and a date, and the bank details of the seller itself."),
 ("No validity date means no price.", "The figure is good until the seller decides otherwise, which is not a price."),
 ("Lead time runs from an event, not from a calendar date.", "From the deposit or from the approved sample, otherwise it slips and the argument is about whose fault that was."),
], None),

"reefer-cold-chain.html": ("The short answer", [
 ("The set point is contractual.", "It is the temperature of the air the machine delivers, and it goes into the booking and into the contract rather than into a conversation."),
 ("The recorder belongs in the document set.", "The machine logs its own performance; an independent recorder placed inside the load gives the temperature of the cargo."),
 ("Plug time is the part nobody books.", "At the port of loading before the vessel, at transhipment, and at the destination before clearance."),
 ("A forty foot reefer carries about twenty five tonnes net.", "Less volume than a dry box of the same length, because of the insulation and the machinery."),
], None),

"services.html": ("The short answer", [
 ("Specification.", "A request turned into something a factory can quote against and a laboratory can test against: grade, dimension or cut, pack, tolerance, standard and the certificates the destination requires."),
 ("Producer verification.", "Producers are approached directly and checked against the register of the importing country rather than against their own website."),
 ("Landed price with a validity date.", "One number at your own door, built up line by line, benchmarked against what the goods actually cross the border at."),
 ("Contract, inspection and documents.", "We contract in our own name on both legs with mirrored terms, inspect before full payment and before loading, and hand over the document set with the goods rather than after them."),
], None),

"southern-africa.html": ("The short answer", [
 ("SACU is not SADC, and the difference changes the paperwork.", "Botswana, Namibia, Eswatini and Lesotho form a customs union with South Africa, with a common external tariff applied at the first point of entry."),
 ("The transit declaration travels with the load.", "It is completed at the office of departure, and the continuation and control sheets move with the consignment rather than by post."),
 ("Paper reels are a handling specification, not a product.", "They are bought by weight and lost to edge damage, and most of that damage happens in handling rather than in transit."),
 ("We quote this lane DAP.", "On a corridor where the inland leg carries most of the risk, a price at the port tells the buyer very little."),
], None),

"tools-hardware.html": ("The short answer", [
 ("Three different ways to buy the same box.", "To a named brand, where the first check is whether the seller is an authorised channel. To specification unbranded. Or against a sealed reference sample."),
 ("What makes a tool specification measurable.", "Output power as well as input, no load speed, bearing type, switch and brush assembly by make, and the cable and plug for the destination."),
 ("Protective equipment is a legal product.", "Gloves, footwear, eye and hearing protection are sold against harmonised standards and in most destinations cannot be supplied without valid conformity documents."),
 ("An assortment rarely fills one factory's container.", "Several producers are consolidated into one container at the port of loading, which keeps a mixed order on full container economics."),
], None),

"turkiye.html": ("The short answer", [
 ("Marble is not a product.", "A quarry sells blocks by the cubic metre, a factory sells slabs by the square metre bundled from one block so they match, a fabricator sells pieces cut to a drawing."),
 ("Grading is commercial, not a public standard.", "Grade A at one supplier is grade B at the next, so the honest way to buy is against a sealed reference sample plus a written tolerance."),
 ("Crating decides whether you receive what you bought.", "A well built crate costs a few dollars per square metre, and a bad one costs the consignment."),
 ("Classify before you order, not at the border.", "The importer of record is liable for the code, the duty and everything that follows from getting it wrong. The seller in Izmir is not."),
], "The short ocean leg is the real advantage of this lane: less working capital tied up, and a replacement arrives inside the same season."),

"veterinary-certificate.html": ("The short answer", [
 ("The establishment number comes before the price.", "The certificate attests that the consignment comes from an approved establishment and was produced under official inspection."),
 ("Approval is destination specific.", "An establishment approved for one country is not approved for its neighbour, and the approval is checked in the register of the importing country."),
 ("Ask in this order.", "The establishment number as registered, written confirmation that it is approved for the destination, the certificate model, and who signs it."),
 ("It is the only variable that cannot be fixed later.", "A price is renegotiated, a pack is changed, a date slips. An inadmissible establishment cannot be made admissible in time."),
], None),

"west-africa.html": ("The short answer", [
 ("Admissibility comes before price.", "Frozen meat enters on a veterinary health certificate issued for a specific establishment, in the form the destination country accepts."),
 ("A cut is three or four products, not one.", "A whole wing with three joints, a two joint wing, a drumette and a mid joint flat are different products at different prices."),
 ("The pack is ten kilogram block frozen cartons.", "That is not the standard pack in the United States or the European Union, and repacking costs money, so it is priced before the order."),
 ("Payment terms decide the return, not the margin.", "The margin per kilogram is set in the negotiation. The return on the money is set by how long the money is out."),
], None),

# --- французские страницы

"afrique-ouest.html": ("En bref", [
 ("L'agrément passe avant le prix.", "La viande congelée entre sur un certificat sanitaire vétérinaire délivré pour un établissement précis, pas sur une facture commerciale."),
 ("Une découpe, c'est quatre produits.", "L'aile entière à trois phalanges, l'aile à deux phalanges, le manchon et l'aileron sont quatre produits à quatre prix différents."),
 ("Le conditionnement fait partie du cahier des charges.", "Le standard ouest-africain est le produit congelé en bloc en cartons de dix kilos, qui n'est pas le conditionnement standard aux États-Unis ni dans l'Union européenne."),
 ("Les conditions de paiement décident du rendement.", "La marge au kilo se fixe dans la négociation. Le rendement du capital se fixe par la durée pendant laquelle l'argent est sorti."),
], None),

"certificat-veterinaire.html": ("En bref", [
 ("Le numéro d'agrément passe avant le prix.", "Le certificat atteste que l'envoi provient d'un établissement agréé et qu'il a été produit sous inspection officielle."),
 ("L'agrément vaut pour une destination, pas pour une région.", "Un établissement agréé pour un pays ne l'est pas pour son voisin, et cela se vérifie dans le registre du pays importateur."),
 ("Ce qu'il faut demander, dans cet ordre.", "Le numéro d'agrément tel qu'enregistré, la confirmation écrite qu'il vaut pour la destination, le modèle de certificat, et qui le signe."),
 ("C'est la seule variable qui ne se corrige pas ensuite.", "Un prix se renégocie, un conditionnement se change, une date glisse. Un établissement non agréé ne peut pas être rendu agréé à temps."),
], None),

"decoupes-volaille.html": ("En bref", [
 ("Une aile entière comporte trois sections.", "Le manchon près du corps, l'aileron plat au milieu, la pointe à l'extrémité. Chacune se négocie comme un produit distinct."),
 ("Mâle et femelle ne sont pas deux qualités du même produit.", "Chez la dinde, les deux lignes sont élevées à des poids différents et donnent des calibres différents, non interchangeables pour un transformateur."),
 ("Chaque découpe a sa géographie.", "Ce qui est un sous-produit sur un marché est un produit de base sur un autre, et c'est toute la raison d'être de ce commerce."),
 ("Une demande exploitable nomme cinq choses.", "La découpe par son anatomie, mâle ou femelle avec la fourchette de poids, le conditionnement, l'incoterm et le port, et le volume mensuel."),
], "Sur un programme mixte, la composition du panier vaut généralement plus que la remise."),

}

ANCHOR = '<nav class="toc" aria-label="On this page">'
ANCHOR_FR = '<nav class="toc" aria-label='


def build(title, items, note):
    out = ['<div class="answer">', f"<h2>{title}</h2>", '<ol class="alist">']
    for lead, rest in items:
        out.append(f"<li><b>{lead}</b> {rest}</li>")
    out.append("</ol>")
    if note:
        out.append(f'<p class="anote">{note}</p>')
    out.append("</div>")
    return "\n".join(out) + "\n"


def main():
    done = skipped = 0
    missing = []
    for name, (title, items, note) in DATA.items():
        p = SITE / name
        if not p.is_file():
            missing.append(name)
            continue
        s = p.read_text()
        if 'class="answer"' in s:
            skipped += 1
            continue
        i = s.find(ANCHOR)
        if i < 0:
            i = s.find(ANCHOR_FR)
        if i < 0:
            missing.append(f"{name}: некуда вставить")
            continue
        p.write_text(s[:i] + build(title, items, note) + s[i:])
        done += 1

    print(f"блоков добавлено: {done}, уже было: {skipped}")
    for m in missing:
        print("  пропущено:", m)
    return 0


if __name__ == "__main__":
    sys.exit(main())
