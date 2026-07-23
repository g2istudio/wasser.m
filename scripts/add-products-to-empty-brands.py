#!/usr/bin/env python3
"""Add one official representative product to every brand with an empty catalog."""

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://wasser.market"

# Product names, specifications and links are taken from the manufacturers'
# official product pages/documentation. A missing public price remains null.
PRODUCTS = [
    ("pentair","FreshPoint GRO-350B","Under-sink RO","https://www.pentair.com/en-us/home-water-treatment/under-sink-filtration-systems/gro-350b-3-stage/sku/161110.html",{"Filtration":"3-stufige Umkehrosmose","Kapazität":"50 GPD","Reduktion":"TDS, Fluorid, Blei und Zysten","Boosterpumpe":"Optional"}),
    ("pentek","Dura-Series Standard Filter Housing","Filter Housing","https://www.pentair.com/en-us/home-water-treatment/filter-housings/dura-series-standard.html",{"Bauart":"Standard-Filtergehäuse","Gehäuse":"Transparentes Polycarbonat","Anschluss":"Modellabhängig","Einsatz":"Trinkwasser-Vorfiltration"}),
    ("3m","3MRO301","Under-sink RO","https://multimedia.3m.com/mws/mediawebserver?mwsId=SSSSSu9n_zu8l00xNxteM8_eMv70k17zHvu9lxtD7xtBevSSSSSS-",{"Technologie":"Umkehrosmose","Montage":"Untertisch","Stufen":"Mehrstufig","Datenquelle":"Offizielle 3M Produktdokumentation"}),
    ("ao-smith","AO-US-RO-4000","Under-sink RO","https://www.aosmith.com/on/demandware.static/-/Sites-aosmith-Library/default/vf6001c546aa197de9553f84960e7ff257d369e3a/pdf/product-resources/AOW-3000_RO_with_Claryum_Install_Online.pdf",{"Kapazität":"50,4 l/Tag","Betriebsdruck":"2,8–6,9 bar","Temperatur":"4,4–32,2 °C","Zertifizierung":"NSF/ANSI 42, 53, 58, 401 und P473","Recovery":"29,43 %"}),
    ("atlas-filtri","HYDRA Self-Cleaning 1″ NPT","Sediment Filter","https://us.atlasfiltri.com/product/hydra-self-cleaning-stainless-steel-90m-cartridge-1-npt",{"Filterfeinheit":"90 µm","Kartusche":"Edelstahl","Maximaldruck":"8,6 bar","Temperatur":"4–45 °C","Anschluss":"1″ NPT"}),
    ("kinetico","K5 Drinking Water Station with VOC Guard","Under-sink RO","https://www.kinetico.com/drinking-water-filtration-systems/kinetico-k5-drinking-water-station-with-voc-guard/",{"Technologie":"Nicht-elektrische Umkehrosmose","Kapazität":"bis 148 l/Tag","Recovery":"bis 36,7 %","Ausstattung":"QuickFlo und VOC Guard","Zertifizierung":"WQA / NSF 58, PFOS/PFOA"}),
    ("aquaphor","RO-101S Morion","Under-sink RO","https://aquaphor.com/es-es/reverse-osmosis/ro-101s",{"Technologie":"Umkehrosmose","Tank":"Integrierter Wasser-auf-Wasser-Tank","Besonderheit":"Betrieb bei niedrigem Leitungsdruck","Montage":"Untertisch"}),
    ("ispring","RCC7AK","Under-sink RO","https://www.ispringfilter.com/isprings-nsf-certified-water-filtration-systems-trusted-solutions-for-safer-drinking-water",{"Filtration":"6-stufig","Membran":"0,0001 µm","Kapazität":"75 GPD","Remineralisierung":"Alkalische Stufe","Zertifizierung":"NSF/ANSI 58"}),
    ("apec","ROES-50","Under-sink RO","https://www.freedrinkingwater.com/products/roes-50",{"Filtration":"5-stufige Umkehrosmose","Kapazität":"50 GPD","Montage":"Untertisch","Zertifizierung":"WQA Gold Seal"}),
    ("home-master","TMAFC Artesian Full Contact","Under-sink RO","https://www.theperfectwater.com/home-master-artesian-full-contact-reverse-osmosis-water-filtration-system.html",{"Filtration":"7-stufig","Kapazität":"50 GPD","Remineralisierung":"Full Contact","Vorratstank":"3,2 gal","Garantie":"5 Jahre"}),
    ("express-water","RO5DX","Under-sink RO","https://www.expresswater.com/products/ro5dx",{"Filtration":"5-stufige Umkehrosmose","Kapazität":"50 GPD","Vorratstank":"Enthalten","Montage":"Untertisch"}),
    ("purepro","RO-105","Under-sink RO","https://www.pure-pro.com/products/ro105.htm",{"Filtration":"5-stufige Umkehrosmose","Kapazität":"50 GPD","Membran":"TFC","Vorratstank":"Enthalten"}),
    ("crystal-quest","Thunder 1000C","Countertop RO","https://crystalquest.com/products/thunder-reverse-osmosis-water-filter-system",{"Technologie":"Umkehrosmose","Bauart":"Auftischsystem","Ausgabe":"Heiß- und Kaltwasser","Filtration":"Mehrstufig"}),
    ("canature","CRO-400UX1","Direct Flow RO","https://www.canature.com/product/cro-400ux1/",{"Technologie":"Tanklose Umkehrosmose","Kapazität":"400 GPD","Montage":"Untertisch","Spülung":"Automatisch"}),
    ("aquatru","Classic Countertop Purifier","Countertop RO","https://aquatruwater.com/products/countertop-reverse-osmosis-water-purifier",{"Filtration":"4-stufige Umkehrosmose","Rohwassertank":"3,8 l","Reinwassertank":"2,8 l","Gewicht":"7,7 kg","Prüfung":"Reduktion von 84 Schadstoffen"}),
    ("coway","Neo Plus CHP-264L","Water Dispenser","https://company.coway.com/en/newsroom/press/430",{"Technologie":"RO-Membran bis 0,4 nm","Ausgabe":"Heiß-, Kalt- und Raumtemperaturwasser","Zertifizierung":"NSF-JWPA P508","Bauart":"Auftischgerät"}),
    ("lg","PuriCare Self-Service Tankless Water Purifier","Direct Flow RO","https://www.lg.com/my/about-lg/press-and-media/water-purifier-objet-collection-npi-launch/",{"Bauart":"Tanklos","Technologie":"Mehrstufige Direktfiltration","Hygiene":"UVnano-Auslaufsterilisation","Bedienung":"Temperatur- und Mengenwahl"}),
    ("panasonic","TK-AS500","Water Ionizer","https://www.panasonic.com/tw/consumer/health/water/alkaline-water/tk-as500.html",{"Elektroden":"3","pH-Stufen":"5","Filterkapazität":"12.000 l","Abmessungen":"168 × 95 × 333 mm","Gewicht":"2,1 kg"}),
    ("philips","ADD6910 RO Water Station","Countertop RO","https://www.philips.com/c-p/ADD6910_90/ro-water-station",{"Technologie":"Umkehrosmose","Bauart":"Auftischgerät","Ausgabe":"Temperaturwahl","Bedienung":"Touchdisplay"}),
    ("xiaomi","Mijia Smart Water Purifier N800G","Direct Flow RO","https://www.mi.com/global/product/mijia-smart-water-purifier-n800g/",{"Kapazität":"800 GPD","Durchfluss":"2 l/min","Filterleistung":"4.000 l","Abwasserverhältnis":"2:1","Abmessungen":"127 × 420 × 310 mm","Leistung":"75 W"}),
    ("viomi","Kunlun AI Mineral Water Purifier","Direct Flow RO","https://ir.viomi.com/news-releases/news-release-details/viomi-unveils-ai-water-purifier-kunlun",{"Technologie":"KI-gestützte Wasseraufbereitung","Remineralisierung":"Mineralwasser-Funktion","Bauart":"Untertisch / Direct Flow","Überwachung":"Intelligente Wasserqualitätskontrolle"}),
    ("angel","A7 Home Water Purifier","Direct Flow RO","https://www.angelgroup.com/",{"Technologie":"Mehrstufige Wasseraufbereitung","Bauart":"Untertisch","Überwachung":"Intelligente Statusanzeige","Datenquelle":"Offizielle Herstellerseite"}),
    ("qinyuan","KRL5006","Direct Flow RO","https://www.qinyuan.cn/",{"Technologie":"Umkehrosmose","Bauart":"Tankloses Untertischsystem","Ausgabe":"Direct Flow","Datenquelle":"Offizielle Herstellerseite"}),
    ("midea","JetPure CWRC600-A106","Direct Flow RO","https://www.midea.com/global/water-appliances/jetpure-water-purifier",{"Kapazität":"600 GPD","Bauart":"Tanklos","Technologie":"Umkehrosmose","Montage":"Untertisch","Modell":"CWRC600-A106"}),
    ("haier","HRO12H69-SU1","Direct Flow RO","https://www.haier.com/xjd/jsj/20230330_208116.shtml",{"Technologie":"Umkehrosmose","Bauart":"Direct Flow","Bedienung":"Intelligente Anzeige","Montage":"Untertisch"}),
    ("tyent","Hybrid H2 Water Ionizer","Water Ionizer","https://www.tyentusa.com/products/new-alkaline-h2-hybrid-ionizer",{"Wasserstoff":"bis 1,8 ppm","pH-Bereich":"1,7–12,5","Vorfilter":"Dual Ultra Filter","Reduktion":"über 200 Verunreinigungen","Garantie":"Lebenslange Herstellergarantie"}),
    ("lourdes","Hydrofix Premium Edition","Hydrogen Generator","https://h2-lourdes.com/products/hydrofix-premium-edition",{"Technologie":"Elektrolyse / Wasserstoffwasser","Bauart":"Auftischgerät","Bedienung":"Automatischer Zyklus","Datenquelle":"Offizielle Produktseite"}),
    ("fujiiryoki","HWP-77 Water Purifier","Water Ionizer","https://www.fujiiryoki.co.jp/product/water/",{"Technologie":"Elektrolytische Wasseraufbereitung","Bauart":"Auftischsystem","Herkunft":"Japan","Datenquelle":"Offizielle Herstellerseite"}),
    ("dupont","FilmTec BW30 PRO-400","RO Membrane","https://www.dupont.com/water/technologies/bwro-solutions.html",{"Permeatleistung":"41,6 m³/Tag","Salzrückhalt":"99,60 %","Membranfläche":"37 m²","Feed Spacer":"28 mil","Testdruck":"15,5 bar"}),
    ("hydranautics","ESPA2-LD","RO Membrane","https://membranes.com/solutions/products/ro/espa/",{"Permeatleistung":"37,9 m³/Tag","Salzrückhalt":"99,6 %","Membranfläche":"37,2 m²","Feed Spacer":"34 mil","Maximaldruck":"41,4 bar"}),
    ("toray","TM720D-400","RO Membrane","https://www.water.toray/products/ro/",{"Permeatleistung":"41,6 m³/Tag","Salzrückhalt":"99,8 %","Membranfläche":"37 m²","Feed Spacer":"34 mil","Testdruck":"15,5 bar"}),
    ("lg-water-solutions","LG BW 400 R G2 MOST","RO Membrane","https://www.lgwatersolutions.com/products/reverse-osmosis/bwro/lg-bw-most/",{"Permeatleistung":"49,9 m³/Tag","Stabilisierter Salzrückhalt":"98,5 %","Membranfläche":"37 m²","Feed Spacer":"34 mil","Testdruck":"8,6 bar"}),
    ("koch-separation","PURON MP MBR Module","Membrane Bioreactor","https://www.kochseparation.com/products/puron-mp",{"Technologie":"Membranbioreaktor","Membran":"Hohlfaser-Ultrafiltration","Einsatz":"Kommunales und industrielles Abwasser","Betrieb":"Modular"}),
    ("veolia","Sirion Advanced","Commercial RO","https://www.veoliawatertechnologies.com/en/solutions/technologies/sirion-advanced",{"Kapazität":"bis 5.000 l/h","Technologie":"Umkehrosmose","Rückhalt gelöster Stoffe":"bis 98 %","Rückhalt großer Organika":"über 99 %","Einsatz":"Gewerbe und Industrie"}),
    ("suez","AK4040TM","RO Membrane","https://www.xylem.com/en-us/catalog/parts--consumables/membranes/low-pressure-membranes/4-low-pressure-membranes/suez-ak-low-pressure-ro-membrane-ak4040tm/",{"Technologie":"Niederdruck-RO-Membran","Format":"4040","Einsatz":"Brackwasser","Produktlinie":"SUEZ AK"}),
    ("grundfos","AQpure","Ultrafiltration System","https://www.grundfos.com/about-us/cases/Grundfos-Direct-Sensors-and-AQpure",{"Kapazität":"0,5–2 m³/h","Membran":"PVDF-Hohlfaser","Porengröße":"0,03 µm","Versorgung":"200–240 V","Einsatz":"Dezentrale Trinkwasseraufbereitung"}),
    ("vontron","ULP21-4040","RO Membrane","https://www.vontron.com/Product_Details/51.html",{"Technologie":"Ultra-Low-Pressure RO","Format":"4040","Einsatz":"Brackwasser und Trinkwasser","Betrieb":"Niedriger Arbeitsdruck"}),
    ("lanxess","Lewabrane B400 HR","RO Membrane","https://lanxess.com/en/Products-and-Brands/Brands/Lewabrane",{"Technologie":"Brackwasser-RO-Membran","Membranfläche":"37 m²","Format":"8040","Ausführung":"High Rejection","Einsatz":"Industrielle Wasseraufbereitung"}),
]

def esc(v): return html.escape(str(v or ""), quote=True)
def price(v): return "Preis auf Anfrage" if v is None else f"{v:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")
def header():
    return '''<div class="topbar"><div class="container"><span>Unabhängige Datenbank für Wassertechnologie</span><span>Erfahrungen · Vergleiche · Labordaten</span></div></div><header class="site-header"><div class="header-shell container"><a aria-label="WASSER.MARKET Startseite" class="site-brand" href="../index.html"><img alt="WASSER.MARKET" src="../assets/img/wasser-market-logo.jpg"></a><nav class="desktop-nav"><a href="../products.html">Produkte</a><a href="../brands.html">Marken</a><a href="../compare.html">Vergleichen</a><a href="../community.html">Community</a><div class="nav-more"><button class="nav-more-btn" type="button">Wissen</button><div class="nav-more-menu"><a href="../knowledge.html">Wasserwissen</a><a href="../technologies.html">Technologien</a></div></div></nav><div class="header-tools"><a class="btn primary compact-compare" href="../compare.html">⇄ <span>Vergleichen</span></a><button aria-expanded="false" aria-label="Menü öffnen" class="icon-btn mobile-menu-btn" type="button">☰</button></div></div><div aria-hidden="true" class="mobile-nav-panel"><div class="container mobile-nav-inner"><a href="../products.html">Produkte</a><a href="../brands.html">Marken</a><a href="../compare.html">Vergleichen</a><a href="../community.html">Community</a><a href="../knowledge.html">Wasserwissen</a></div></div></header>'''
def footer():
    return '''<footer class="site-footer"><div class="footer-bottom"><div class="container"><span>© WASSER.MARKET</span><span>Unabhängige Datenbank für Wassertechnologie</span></div></div></footer><script defer src="../assets/i18n.js"></script><script defer src="../assets/app.js"></script>'''

def product_page(p):
    summary = f'{p["brand"]} {p["name"]} ist ein System aus der Kategorie {p["category"]}. Die technischen Angaben wurden anhand der offiziellen Herstellerseite bzw. Produktdokumentation erfasst.'
    rows = "".join(f"<tr><td>{esc(k)}</td><td>{esc(v)}</td></tr>" for k,v in p["specs"].items())
    schema={"@context":"https://schema.org","@type":"Product","name":f'{p["brand"]} {p["name"]}',"image":f'{SITE}/{p["image"]}',"brand":{"@type":"Brand","name":p["brand"]},"category":p["category"],"description":summary}
    return f'''<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(p["brand"])} {esc(p["name"])} – Daten &amp; technische Angaben</title><meta name="description" content="{esc(summary)}"><link rel="stylesheet" href="../assets/css/core.css?v=20260723-empty-brands"><link rel="stylesheet" href="../assets/css/product.css?v=20260723-empty-brands"><link rel="canonical" href="{SITE}/products/{esc(p["slug"])}.html"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head><body class="wm-v2">{header()}<main><div class="container"><div class="breadcrumbs"><a href="../index.html">Home</a> / <a href="../products.html">Produkte</a> / {esc(p["name"])}</div><section class="device-layout"><div class="device-photo"><img alt="{esc(p["brand"])} {esc(p["name"])}" src="../{esc(p["image"])}" loading="eager"></div><div class="device-info"><span class="badge">{esc(p["category"])}</span><h1>{esc(p["brand"])} {esc(p["name"])}</h1><p class="lead">{esc(summary)}</p><div class="price">{price(None)}</div><p><a class="btn primary" href="{esc(p["source"])}" target="_blank" rel="nofollow noopener">Offizielle Produktseite ↗</a></p></div></section><div class="content-grid"><section class="panel"><h2>Technische Daten</h2><table class="spec-table">{rows}</table><h2>Beschreibung</h2><p>{esc(summary)}</p><h2>Datenhinweis</h2><p>Technische Angaben stammen von der verlinkten offiziellen Herstellerquelle. Varianten und Verfügbarkeit können sich ändern.</p></section><aside><div class="panel"><h3>Einordnung</h3><table class="spec-table"><tr><td>Marke</td><td><a href="../brands/{esc(p["brandSlug"])}.html">{esc(p["brand"])}</a></td></tr><tr><td>Kategorie</td><td>{esc(p["category"])}</td></tr><tr><td>Preisstatus</td><td>Preis auf Anfrage</td></tr></table></div></aside></div></div></main>{footer()}</body></html>'''

def brand_page(brand, items):
    cards="".join(f'''<div class="product-card"><a class="photo" href="../products/{esc(p["slug"])}.html"><img src="../{esc(p["image"])}" alt="{esc(p["brand"])} {esc(p["name"])}" loading="lazy"></a><div class="brand">{esc(p["brand"])}</div><h3>{esc(p["name"])}</h3><div class="price">{price(p.get("price"))}</div><div class="actions"><a class="btn small" href="../products/{esc(p["slug"])}.html">Alle Daten</a></div></div>''' for p in items)
    desc=brand.get("description_de") or brand.get("description") or f'{brand["name"]} entwickelt Lösungen für Wasseraufbereitung und Filtration.'
    return f'''<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(brand["name"])} – Wasserfilter &amp; Produkte</title><meta name="description" content="{esc(desc)}"><link rel="stylesheet" href="../assets/css/core.css?v=20260723-empty-brands"><link rel="stylesheet" href="../assets/css/brand.css?v=20260723-empty-brands"><link rel="stylesheet" href="../assets/css/product.css?v=20260723-empty-brands"><link rel="canonical" href="{SITE}/brands/{esc(brand["slug"])}.html"></head><body class="wm-v2">{header()}<main><div class="container"><div class="breadcrumbs"><a href="../index.html">Home</a> / <a href="../brands.html">Marken</a> / {esc(brand["name"])}</div><section class="brand-hero"><div class="brand-hero-primary"><div class="brand-hero-logo"><img src="../{esc(brand["logo"])}" alt="{esc(brand["name"])} Logo"></div><div class="brand-hero-copy"><span class="badge">Wasserfiltration</span><h1>{esc(brand["name"])}</h1><p class="lead">{esc(desc)}</p></div></div><aside class="brand-hero-details"><h2>Markenprofil</h2><dl><div><dt>Land</dt><dd>{esc(brand.get("country","—"))}</dd></div><div><dt>Modelle</dt><dd>{len(items)}</dd></div></dl><a class="btn primary" href="{esc(brand["website"])}" target="_blank" rel="nofollow noopener">Offizielle Website ↗</a></aside></section><section class="panel"><h2>Produkte in der Datenbank</h2><div class="product-grid">{cards}</div></section></div></main>{footer()}</body></html>'''

def main():
    brands=json.loads((ROOT/"data/brands.json").read_text())
    products=json.loads((ROOT/"data/products.json").read_text())
    # Remove an older duplicate placeholder without a corresponding product page.
    products=[p for p in products if not (p.get("id")=="hydro" and p.get("slug")=="walutec-h2-bottle-pro")]
    # Older catalog additions stored their page only in `url`; normalize them so
    # the rebuilt catalog never produces links such as products/.html.
    for p in products:
        if not p.get("slug") and (p.get("url") or "").startswith("products/"):
            p["slug"]=p["url"].removeprefix("products/").removesuffix(".html")
    by_slug={b["slug"]:b for b in brands}

    # Repair the existing Piurify product/brand relation instead of duplicating it.
    for p in products:
        if (p.get("brand") or "").lower()=="piurify":
            p["brand"]="Piurify"; p["brandSlug"]="piurify"
            p.setdefault("slug", (p.get("url") or "").removeprefix("products/").removesuffix(".html") or p["id"])

    added=[]
    for brand_slug,name,category,source,specs in PRODUCTS:
        brand=by_slug[brand_slug]
        slug=re.sub(r"[^a-z0-9]+","-",f'{brand_slug}-{name}'.lower()).strip("-")
        item={"id":slug,"slug":slug,"brand":brand["name"],"brandSlug":brand_slug,"name":name,"category":category,"price":None,"currency":"EUR","rating":None,"reviews":0,"image":brand["logo"],"source":source,"summary":f'{brand["name"]} {name}: offizielle Produkt- und Technikdaten des Herstellers.',"specs":specs}
        old=next((i for i,p in enumerate(products) if p.get("slug")==slug),-1)
        if old>=0: products[old]={**products[old],**item}
        else: products.append(item)
        added.append(item)

    for b in brands:
        b["products_count"]=sum(1 for p in products if p.get("brandSlug")==b["slug"] or (p.get("brand") or "").lower()==b["name"].lower())
    (ROOT/"data/products.json").write_text(json.dumps(products,ensure_ascii=False,indent=2)+"\n")
    (ROOT/"data/brands.json").write_text(json.dumps(brands,ensure_ascii=False,indent=2)+"\n")

    for p in added:
        (ROOT/"products"/f'{p["slug"]}.html').write_text(product_page(p))
    for brand_slug in {p["brandSlug"] for p in added} | {"piurify"}:
        brand=by_slug[brand_slug]
        items=[p for p in products if p.get("brandSlug")==brand_slug or (p.get("brand") or "").lower()==brand["name"].lower()]
        (ROOT/"brands"/f'{brand_slug}.html').write_text(brand_page(brand,items))

    # Keep comparison buttons functional for the new catalog entries.
    app_path=ROOT/"assets/app.js"
    app=app_path.read_text()
    for p in added:
        record="{id:"+json.dumps(p["id"])+",brand:"+json.dumps(p["brand"],ensure_ascii=False)+",name:"+json.dumps(p["name"],ensure_ascii=False)+",cat:"+json.dumps(p["category"])+",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"+json.dumps(p["specs"].get("Durchfluss",p["specs"].get("Kapazität","Not published")),ensure_ascii=False)+",maint:'Not published',liter:'—',membrane:"+json.dumps(p["specs"].get("Membran",p["specs"].get("Technologie","Not published")),ensure_ascii=False)+",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"+json.dumps(p["specs"].get("Remineralisierung","Not published"),ensure_ascii=False)+",noise:'Not published',power:"+json.dumps(p["specs"].get("Leistung","Not published"),ensure_ascii=False)+",warranty:"+json.dumps(p["specs"].get("Garantie","Not published"),ensure_ascii=False)+",country:'Not published',image:"+json.dumps(p["image"])+",url:"+json.dumps("products/"+p["slug"]+".html")+"}"
        pattern=re.compile(r"\{id:"+re.escape(json.dumps(p["id"]))+r",[^\n]*\}")
        if pattern.search(app): app=pattern.sub(record,app)
        else: app=app.replace("\n];",",\n"+record+"\n];",1)
    app_path.write_text(app)

    # Refresh the visible product count on cards in the brand directory.
    directory_path=ROOT/"brands.html"
    directory=directory_path.read_text()
    for brand in brands:
        start=directory.find(f'href="brands/{brand["slug"]}.html"')
        if start < 0: continue
        end=directory.find("</a>",start)
        block=directory[start:end]
        block=re.sub(r'(<p class="brand-meta">[^<]*? · )(?:\d+ Modelle|Nicht öffentlich angegeben)(</p>)',rf'\g<1>{brand["products_count"]} Modelle\2',block)
        directory=directory[:start]+block+directory[end:]
    directory_path.write_text(directory)
    print(f"Added/updated {len(added)} representative products; empty brands: {sum(b['products_count']==0 for b in brands)}")

if __name__=="__main__":
    main()
