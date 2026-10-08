# -*- coding: utf-8 -*-
"""Снимок в шапке: slug -> (файл, alt).

Каждая страница открывается кадром, а не одним текстом. Держим карту в одном
месте, чтобы сборщики страниц и коридоров брали её из общего источника.
"""

HERO = {
    # ядро
    "about":        ("miami-dusk.webp",   "Miami waterfront at dusk from the air"),
    "contact":      ("miami-bay.webp",    "North Miami Beach seen from Biscayne Bay"),
    "services":     ("robots-wide.webp",  "Robot arms on an automated assembly line"),
    "supply":       ("port-wide.webp",    "Container vessel alongside a working terminal"),
    "corridors":    ("ship-aerial.webp",  "Loaded container vessel seen from above"),
    "guides":       ("crane-dusk.webp",   "Ship-to-shore cranes against an evening sky"),
    "experience":   ("port-noir.webp",    "Harbour cranes under a heavy sky"),
    "incoterms":    ("ship-sea.webp",     "Container ship under way in open water"),
    "privacy":      ("crane-lift.webp",   "Cargo being lifted on a quayside"),
    "terms":        ("stamp.webp",        "A shipping document being stamped"),
    "404":          ("ship-dusk.webp",    "Container ship at dusk"),

    # коридоры
    "china":            ("port-cma.webp",      "Container vessel loading at an Asian terminal"),
    "turkiye":          ("bosphorus.webp",     "Bulk carrier passing through the Bosphorus"),
    "west-africa":      ("chart-west.webp",    "Early Portuguese nautical chart of the West African coast"),
    "southern-africa":  ("durban-sunset.webp", "Ship's bow at a southern African harbour at sunset"),

    # товарные группы
    "building-materials":  ("quarry-stone.webp", "Working face of a stone quarry"),
    "industrial-equipment": ("robots.webp",      "Industrial robots on a production line"),
    "tools-hardware":      ("tools-flat.webp",   "Hand tools laid out on a work surface"),
    "metals-pipe":         ("steel-tubes.webp",  "Square steel sections stacked end on"),
    "paper-packaging":     ("pallets-wall.webp", "Wall of stacked wooden pallets"),
    "food-agricultural":   ("silos.webp",        "Grain terminal silos"),

    # руководства
    "landed-price":         ("crane-red.webp",      "Gantry cranes over a container berth"),
    "verify-supplier":      ("machinery.webp",      "Industrial drive assembly in a workshop"),
    "letter-of-credit":     ("signing.webp",        "A contract being signed"),
    "customs-data-pricing": ("containers-wall.webp", "Stacked containers in a port yard"),
    "hs-code":              ("yard-dusk.webp",      "Container yard at dusk"),
    "ispm-15":              ("pallets-stack.webp",  "Stacks of wooden pallets"),
    "container-loading":    ("loading-truck.webp",  "A twenty foot container loaded on a truck"),
    "veterinary-certificate": ("stamp.webp",        "A health certificate being stamped"),
    "poultry-cuts":         ("coldstore.webp",      "Chilled store at a meat plant"),
    "reefer-cold-chain":    ("container-gold.webp", "Refrigerated container in evening light"),
    "antidumping-check":    ("quarry-cut.webp",     "Cut stone at a marble quarry"),
    "bill-of-lading":       ("ship-dusk.webp",      "Container ship at dusk"),
    "demurrage-detention":  ("truck-road.webp",     "Container trucks on a highway"),
    "certificate-of-origin": ("chart-old.webp",     "Early nautical chart"),
    "proforma-invoice":     ("signing.webp",        "A document being signed"),

    # французская версия
    "fr":                    ("port-wide.webp",  "Porte-conteneurs à quai"),
    "afrique-ouest":         ("chart-west.webp", "Carte marine portugaise de la côte ouest-africaine"),
    "decoupes-volaille":     ("coldstore.webp",  "Chambre froide dans un abattoir"),
    "certificat-veterinaire": ("stamp.webp",     "Un certificat sanitaire tamponné"),
    "contact-fr":            ("miami-bay.webp",  "North Miami Beach vu de la baie de Biscayne"),
}
