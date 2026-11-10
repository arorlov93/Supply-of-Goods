# -*- coding: utf-8 -*-
"""Главная под промышленную химию: пп. 1.1-1.4 брифа от 10.11.2026.

Что делает, по порядку брифа.

1.1 Под заголовком «ADMISSIBILITY BEFORE PRICE» встаёт строка о том, что
    именно компания поставляет и кому. Строка идёт сразу за H1, в левой
    колонке героя, то есть буквально под заголовком, а не в лиде справа.
    Упоминания России с главной снимаются: их там два, оба в разметке
    JSON-LD, в списке areaServed. На /experience и /projects они остаются,
    там они уточняются отдельной правкой.

1.2 В рейле «WHAT WE SUPPLY» становится семь карточек, первая химия,
    остальные шесть сдвигаются на номер вниз. Подзаголовок блока меняется.

1.3 Новый блок «WHO WE SUPPLY»: четыре отрасли с иконками. На телефоне
    сетка 2x2, на широком экране четыре колонки.

1.4 Перед формой заявки строка доверия из четырёх пунктов, последний
    ведёт на /compliance.

Про снимок на карточке химии. Подходящей фотографии в медиатеке нет:
там порты, склад, станки, лес, трубы и холодильник, ни бочек, ни IBC, ни
водоподготовки. Поставлен port-noir, единственный свободный снимок с
нужным набором размеров для рейла. Это заглушка, и её надо заменить
настоящим кадром: отмечено в отчёте.

Запуск: python3.13 tools/chem-home.py
Повторный запуск ничего не меняет. После правки CSS темы нужен
python3.13 tools/css-version.py
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
MERCURY = SITE / "css" / "mercury.css"
PAGES = ("index.html", "fr/index.html", "es/index.html", "de/index.html")
LANG = {"index.html": "en", "fr/index.html": "fr",
        "es/index.html": "es", "de/index.html": "de"}

# Ссылка на страницу, у которой есть языковые версии: с локальной главной
# она должна вести на свою локаль, а не на английскую.
def href(name, path):
    lg = LANG[name]
    return path if lg == "en" else "/%s/%s" % (lg, path)


# ------------------------------------------------------------ 1.1 строка
SUBLINE = {
 "en": "Industrial chemicals, equipment and materials for oil &amp; gas, "
       "power, mining and water utilities. Supplied as principal, from "
       "verified manufacturers to your port.",
 "fr": "Produits chimiques industriels, équipements et matériaux pour le "
       "pétrole et le gaz, l’énergie, les mines et les services d’eau. "
       "Fournis en notre propre nom, de fabricants vérifiés jusqu’à votre "
       "port.",
 "es": "Productos químicos industriales, equipos y materiales para petróleo "
       "y gas, energía, minería y servicios de agua. Suministrados en "
       "nombre propio, de fabricantes verificados hasta su puerto.",
 "de": "Industriechemikalien, Ausrüstung und Materialien für Öl und Gas, "
       "Energie, Bergbau und Wasserwirtschaft. Geliefert im eigenen Namen, "
       "von geprüften Herstellern bis zu Ihrem Hafen.",
}

# ------------------------------------------------------------ 1.2 карточка
CARD = {
 "en": ("Water treatment and oilfield chemicals",
        "Scale inhibitors, coagulants, ion exchange resins"),
 "fr": ("Chimie de l’eau et des champs pétroliers",
        "Inhibiteurs d’entartrage, coagulants, résines échangeuses d’ions"),
 "es": ("Química para agua y campos petroleros",
        "Inhibidores de incrustaciones, coagulantes, resinas de intercambio iónico"),
 "de": ("Chemie für Wasseraufbereitung und Ölfeld",
        "Scale-Inhibitoren, Koagulationsmittel, Ionenaustauscherharze"),
}

RAIL_LEAD_OLD = {
 "en": "These are the categories we quote, food among them.",
 "fr": "Voici les catégories que nous cotons, l’alimentaire compris.",
 "es": "Estas son las categorías que cotizamos, la alimentación entre ellas.",
 "de": "Das sind die Kategorien, die wir anbieten, Lebensmittel eingeschlossen.",
}
RAIL_LEAD_NEW = {
 "en": "These are the categories we quote, chemicals and food among them.",
 "fr": "Voici les catégories que nous cotons, la chimie et l’alimentaire compris.",
 "es": "Estas son las categorías que cotizamos, la química y la alimentación entre ellas.",
 "de": "Das sind die Kategorien, die wir anbieten, Chemie und Lebensmittel eingeschlossen.",
}

IMG = ('<picture><source srcset="%(p)smedia/port-noir-349.2245b88e.webp 349w, '
       '%(p)smedia/port-noir-509.0f2e3096.webp 509w, '
       '%(p)smedia/port-noir-731.effa253f.webp 731w" '
       'sizes="(max-width: 480px) 351px, (max-width: 900px) 731px, 509px" '
       'type="image/webp"><img src="%(p)smedia/port-noir.3ce31aa2.jpg" '
       'alt="%(alt)s" loading="lazy" decoding="async" '
       'width="1280" height="1920"></picture>')

ALT = {
 "en": "Container cranes over a deep-water berth",
 "fr": "Portiques au-dessus d’un poste à conteneurs en eau profonde",
 "es": "Grúas pórtico sobre un atraque de aguas profundas",
 "de": "Containerbrücken über einem Tiefwasserliegeplatz",
}

# ------------------------------------------------------------ 1.3 кому
WHO_H2 = {
 "en": "WHO WE SUPPLY.", "fr": "À QUI NOUS FOURNISSONS.",
 "es": "A QUIÉN SUMINISTRAMOS.", "de": "WEN WIR BELIEFERN.",
}
WHO = {
 "en": [("Oil &amp; gas", "Scale and corrosion inhibitors, demulsifiers, gas dehydration."),
        ("Power and CHP", "Ion exchange resins and chemicals for boiler and cooling water."),
        ("Water utilities", "Coagulants for drinking water and wastewater."),
        ("Mining and metallurgy", "Resins for metal recovery, process water chemicals.")],
 "fr": [("Pétrole et gaz", "Inhibiteurs d’entartrage et de corrosion, désémulsifiants, déshydratation du gaz."),
        ("Électricité et cogénération", "Résines échangeuses d’ions et produits pour l’eau de chaudière et de refroidissement."),
        ("Services d’eau", "Coagulants pour l’eau potable et les eaux usées."),
        ("Mines et métallurgie", "Résines pour la récupération des métaux, produits pour l’eau de procédé.")],
 "es": [("Petróleo y gas", "Inhibidores de incrustaciones y corrosión, desemulsionantes, deshidratación de gas."),
        ("Energía y cogeneración", "Resinas de intercambio iónico y productos para agua de caldera y refrigeración."),
        ("Servicios de agua", "Coagulantes para agua potable y aguas residuales."),
        ("Minería y metalurgia", "Resinas para recuperación de metales, productos para agua de proceso.")],
 "de": [("Öl und Gas", "Scale- und Korrosionsinhibitoren, Demulgatoren, Gastrocknung."),
        ("Strom und KWK", "Ionenaustauscherharze und Chemikalien für Kessel- und Kühlwasser."),
        ("Wasserversorger", "Koagulationsmittel für Trink- und Abwasser."),
        ("Bergbau und Metallurgie", "Harze zur Metallrückgewinnung, Prozesswasserchemikalien.")],
}

# Иконки линейные, в одну краску, наследуют currentColor. Отдельных файлов
# не заводим: четыре коротких пути дешевле четырёх запросов к сети.
ICONS = [
 # нефтяная вышка
 '<path d="M12 3v18M5 21l7-12 7 12M8 13h8"/>',
 # турбина и пар
 '<circle cx="12" cy="12" r="3.2"/><path d="M12 3v5.5M12 15.5V21M3 12h5.5M15.5 12H21M6 6l3.5 3.5M14.5 14.5 18 18M18 6l-3.5 3.5M9.5 14.5 6 18"/>',
 # капля
 '<path d="M12 3s6 6.4 6 10.4A6 6 0 0 1 6 13.4C6 9.4 12 3 12 3Z"/>',
 # кирка
 '<path d="M3 20 14 9M9.5 4.5a9 9 0 0 1 10 10c-2.5-3.5-6.5-7.5-10-10Z"/>',
]


def icon(i):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" '
            'aria-hidden="true">%s</svg>' % ICONS[i])


# ------------------------------------------------------------ 1.4 доверие
TRUST = {
 "en": ["Authorized distributor of the manufacturers we quote",
        "ISO-certified plants, COA, TDS and SDS for every batch",
        "Free samples before the first order",
        "Sanctions screening on every counterparty"],
 "fr": ["Distributeur agréé des fabricants que nous cotons",
        "Usines certifiées ISO, COA, TDS et FDS pour chaque lot",
        "Échantillons gratuits avant la première commande",
        "Contrôle des sanctions sur chaque contrepartie"],
 "es": ["Distribuidor autorizado de los fabricantes que cotizamos",
        "Plantas certificadas ISO, COA, TDS y SDS en cada lote",
        "Muestras gratuitas antes del primer pedido",
        "Control de sanciones sobre cada contraparte"],
 "de": ["Autorisierter Händler der Hersteller, die wir anbieten",
        "ISO-zertifizierte Werke, COA, TDS und SDB zu jeder Charge",
        "Kostenlose Muster vor der ersten Bestellung",
        "Sanktionsprüfung bei jeder Gegenpartei"],
}

CSS = """
/* 01b строка под заголовком, 04b who we supply, 08b строка доверия */
.hero-sub{max-width:34ch;margin:clamp(18px,2.4vh,30px) 0 0;font-size:clamp(.98rem,1.08vw,1.1rem);
  line-height:1.55;color:var(--on-shot)}
@media (max-width:900px){.hero-sub{max-width:46ch}}
#s-who{padding:clamp(70px,11vh,140px) var(--gut);background:var(--graphite)}
#s-who .who-wrap{max-width:var(--maxw);margin:0 auto}
#s-who .who-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));
  gap:1px;background:rgb(var(--paper-rgb) / .14);margin-top:clamp(34px,5vh,64px)}
#s-who .who-grid div{background:var(--graphite);padding:clamp(22px,2.6vw,34px)}
#s-who svg{width:30px;height:30px;display:block;margin-bottom:16px;color:var(--gold)}
#s-who b{display:block;font-weight:500;font-size:1.06rem;margin-bottom:9px}
#s-who p{margin:0;color:var(--steel);font-size:.95rem}
@media (max-width:860px){#s-who .who-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
.trust-row{display:flex;flex-wrap:wrap;gap:10px 26px;margin:clamp(30px,4.5vh,52px) 0 26px;padding:0;list-style:none}
.trust-row li{display:flex;align-items:flex-start;gap:9px;font-size:.92rem;
  line-height:1.45;color:var(--on-shot);max-width:30ch}
.trust-row li::before{content:"";flex:0 0 auto;width:7px;height:7px;margin-top:.45em;
  border-radius:50%;background:var(--gold)}
.trust-row a{color:inherit;text-decoration:underline;text-underline-offset:3px}
"""
CSS_ANCHOR = "/* 07 why */"


def section_who(name):
    lg = LANG[name]
    cells = "\n      ".join(
        '<div class="fade">%s<b>%s</b><p>%s</p></div>' % (icon(i), b, t)
        for i, (b, t) in enumerate(WHO[lg]))
    return """<!-- ============ 04b КОМУ ПОСТАВЛЯЕМ ============ -->
<section id="s-who" aria-labelledby="h-who" data-reveal>
  <div class="who-wrap">
    <h2 class="display sm" id="h-who">
      <span class="ln"><span>%s</span></span>
    </h2>
    <div class="who-grid">
      %s
    </div>
  </div>
</section>

""" % (WHO_H2[lg], cells)


def trust_row(name):
    lg = LANG[name]
    t = TRUST[lg]
    items = "".join("<li>%s</li>" % x for x in t[:3])
    items += '<li><a href="%s">%s</a></li>' % (href(name, "compliance"), t[3])
    return '<ul class="trust-row fade">%s</ul>\n        ' % items


def main():
    pages = 0
    for name in PAGES:
        p = SITE / name
        s = p.read_text()
        orig = s
        lg = LANG[name]
        steps = []

        # --- 1.1 строка под заголовком
        sub = '<p class="hero-sub fade">%s</p>' % SUBLINE[lg]
        if sub not in s:
            m = re.search(r"(?s)(</h1>\s*)", s)
            if not m:
                print("  ВНИМАНИЕ: %s, h1 не найден" % name)
            else:
                s = s[:m.end(1)] + "        " + sub + "\n      " + s[m.end(1):]
                steps.append("строка под заголовком")

        # --- 1.1 Россия из JSON-LD
        n_ru = len(re.findall(r'\{\s*"@type":\s*"Place",\s*"name":\s*"Russia"\s*\},?', s))
        if n_ru:
            s = re.sub(r'\s*\{\s*"@type":\s*"Place",\s*"name":\s*"Russia"\s*\},', "", s)
            s = re.sub(r',\s*\{\s*"@type":\s*"Place",\s*"name":\s*"Russia"\s*\}', "", s)
            steps.append("Россия снята (%d)" % n_ru)

        # --- 1.2 карточка химии и перенумерация
        title, cap = CARD[lg]
        pre = "/" if name != "index.html" else ""
        card = ('      <a class="card" href="%s">\n        %s\n'
                '        <span class="n">01</span>\n'
                '        <span class="cap"><b>%s</b><span>%s</span></span>\n'
                '      </a>\n' % (href(name, "chemicals"),
                                  IMG % {"p": pre, "alt": ALT[lg]}, title, cap))
        if 'href="%s"' % href(name, "chemicals") not in s:
            # Рейл берём не первый попавшийся: на французской главной выше
            # стоит полоса #s-lane со своим рейлом из трёх стран, и карточка
            # химии с перенумерацией уехала бы туда. Ищем рейл внутри
            # секции категорий и правим только её кусок документа.
            sec = re.search(r'(?s)id="s-cats".*?</section>', s)
            m = re.search(r'(<div class="rail">\s*\n)', sec.group(0)) if sec else None
            if not m:
                print("  ВНИМАНИЕ: %s, рейл категорий не найден" % name)
            else:
                a = sec.start() + m.end(1)
                b = sec.end()
                block = s[a:b]
                # сдвигаем номера шести карточек, с конца, чтобы не затереть
                for k in range(6, 0, -1):
                    block = block.replace('<span class="n">%02d</span>' % k,
                                          '<span class="n">%02d</span>' % (k + 1), 1)
                s = s[:a] + card + block + s[b:]
                steps.append("карточка химии")

        if RAIL_LEAD_OLD[lg] in s:
            s = s.replace(RAIL_LEAD_OLD[lg], RAIL_LEAD_NEW[lg], 1)
            steps.append("подзаголовок рейла")

        # --- CSS
        if CSS.strip() not in s:
            if CSS_ANCHOR not in s:
                print("  ВНИМАНИЕ: %s, якорь CSS не найден" % name)
            else:
                s = s.replace(CSS_ANCHOR, CSS.strip() + "\n\n" + CSS_ANCHOR, 1)

        # --- 1.3 блок «кому поставляем», сразу после рейла категорий
        if 'id="s-who"' not in s:
            anchor = '<!-- ============ 06 PROCESS ============ -->'
            if anchor not in s:
                anchor = '<section id="s-proc"'
            if anchor not in s:
                print("  ВНИМАНИЕ: %s, якорь блока не найден" % name)
            else:
                s = s.replace(anchor, section_who(name) + anchor, 1)
                steps.append("блок «кому поставляем»")

        # --- 1.4 строка доверия перед формой
        if 'class="trust-row' not in s:
            m = re.search(r'(\s*)<form class="form-card', s)
            if not m:
                print("  ВНИМАНИЕ: %s, форма не найдена" % name)
            else:
                s = s[:m.start()] + "\n        " + trust_row(name).rstrip() + s[m.start():]
                steps.append("строка доверия")

        if s != orig:
            p.write_text(s)
            pages += 1
            print("  %s: %s" % (name, ", ".join(steps)))

    # Тема красит полосы в графит, новая секция должна попасть в тот же список.
    m = MERCURY.read_text()
    changed = 0
    for old, new in (("#s-cats, #s-proc, #s-why, #s-lane, #s-pay {",
                      "#s-cats, #s-proc, #s-why, #s-lane, #s-pay, #s-who {"),
                     ("#s-lane h2, #s-pay h2, #s-pay h3,",
                      "#s-lane h2, #s-pay h2, #s-pay h3, #s-who h2, #s-who b,"),
                     ("#s-lane p, #s-pay p,", "#s-lane p, #s-pay p, #s-who p,")):
        if new in m:
            continue
        if old not in m:
            print("  ВНИМАНИЕ: mercury.css, не найдено: %s" % old[:46])
            continue
        m = m.replace(old, new, 1)
        changed += 1
    if changed:
        MERCURY.write_text(m)
        print("  mercury.css: правил дополнено %d (нужен css-version.py)" % changed)

    print("главных поправлено: %d" % pages)
    return 0


if __name__ == "__main__":
    sys.exit(main())
