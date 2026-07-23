#!/usr/bin/env python3
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TMP = Path("/tmp")

def clean(value):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", str(value or ""))).split())

def money(value):
    if value is None:
        return "Preis auf Anfrage"
    return f"{value:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")

def esc(value):
    return html.escape(str(value or ""), quote=True)

def waterdrop_specs(handle, title, description):
    model_match = re.search(r"\b(X12|X16|X8|G3P800|G3P600|G5P700A|G2P600|G5P500A|K6|A2G|A1|K19-HG|C1SL|C1H)\b", title, re.I)
    model = model_match.group(1).upper() if model_match else title
    gpd = {"X12":1200,"X16":1600,"X8":800,"G3P800":800,"G3P600":600,"G5P700A":700,
           "G2P600":600,"G5P500A":500,"K6":600,"A1":100,"K19-HG":75,"C1SL":75,"C1H":75}.get(model)
    countertop = any(x in title.lower() for x in ["auftisch", "arbeitsplatte", "k19", "c1sl", "c1h", "a1 ", "a2g"])
    mineral = any(x in title.lower() for x in ["alkal", "mineral", "mz", "a2g"])
    hot = any(x in title.lower() for x in ["heiß", "heiss", "hot", "k6", "k19"])
    cold = any(x in title.lower() for x in ["kalt", "a1", "a2g"])
    ratios = {"X12":"3:1","X16":"3:1","X8":"2:1","G3P800":"3:1","G3P600":"2:1",
              "K6":"2:1","A2G":"3:1","A1":"2:1","K19-HG":"3:1","C1SL":"3:1","C1H":"3:1"}
    stages = {"X12":"11-stufig","X16":"11-stufig","X8":"9-stufig","G3P800":"10-stufig",
              "G3P600":"8-stufig","G5P700A":"8-stufig","G5P500A":"8-stufig",
              "A2G":"6-stufig","A1":"7-stufig"}
    dims = {"X12":"46,2 × 15,9 × 42,5 cm","X16":"46,2 × 15,9 × 42,5 cm","X8":"46,2 × 15,9 × 42,5 cm",
            "G3P800":"45,9 × 14,4 × 45,0 cm","G3P600":"45,9 × 14,4 × 45,0 cm",
            "K6":"17,0 × 44,5 × 42,2 cm","A2G":"29,0 × 47,2 × 49,0 cm",
            "A1":"46,5 × 19,8 × 43,3 cm","K19-HG":"35,1 × 20,1 × 41,5 cm",
            "C1SL":"29,7 × 21,1 × 34,8 cm","C1H":"39,6 × 27,7 × 43,2 cm",
            "G2P600":"43,9 × 15,0 × 35,3 cm"}
    specs = {
        "Modell": model,
        "Bauart": "Auftisch-Umkehrosmoseanlage ohne Festinstallation" if countertop else "Tanklose Untertisch-Umkehrosmoseanlage",
        "Filtration": stages.get(model, "Mehrstufige Umkehrosmose-Filtration"),
        "RO-Leistung": f"{gpd} GPD" if gpd else "Nicht separat veröffentlicht",
        "Mineralisierung": "Ja, alkalische/mineralische Nachbehandlung" if mineral else "Nein / nicht Bestandteil dieses Sets",
        "Heißwasser": "Ja" if hot else "Nein",
        "Kaltwasser": "Ja" if cold else "Nein",
        "Reinwasser-Abwasser-Verhältnis": ratios.get(model, "Nicht separat veröffentlicht"),
        "Bedienung": "Display mit Filterstatus und Wassereinstellungen" if countertop else "Intelligenter Wasserhahn mit Filterstatusanzeige",
        "Filterwechsel": "Vor-/Nachfilter ca. 6–12 Monate; RO-Membran modellabhängig bis 24 Monate",
        "Tank": "Integrierte Tanks" if countertop else "Tanklos",
        "Installation": "Aufstellen, befüllen und an Strom anschließen" if countertop else "Untertisch an Wasser, Abfluss und Strom",
        "Zertifizierung": "NSF/ANSI 372 (bleifreie wasserberührte Komponenten)",
        "Abmessungen": dims.get(model, "Nicht separat veröffentlicht"),
        "Garantie": "1 Jahr laut Vergleichstabelle des Herstellers",
    }
    exact = {
        "X12":{"Filtration":"11-stufig, RO-Membran 0,0001 µm, UV und alkalische Remineralisierung",
            "Durchfluss":"Becherfüllung in ca. 3 Sekunden","Reinwasser-Abwasser-Verhältnis":"3:1",
            "Wasserhahn":"Touchscreen: Echtzeit-TDS, Filterstatus und Mengenvorwahl",
            "Filterlebensdauer":"F1A bis 12 Monate / 4.164 l; F2 bis 6 Monate / 2.082 l; F3 bis 24 Monate / 8.328 l",
            "Gewicht":"16,75 kg","Zertifizierung":"NSF/ANSI 42, 58 und 372; IAPMO-geprüfte Angaben",
            "Material":"BPA-freie und bleifreie wasserberührte Materialien"},
        "X16":{"Filtration":"11-stufig, RO-Membran 0,0001 µm und alkalische Remineralisierung",
            "Reinwasser-Abwasser-Verhältnis":"3:1","Wasserhahn":"Touchscreen: Echtzeit-TDS, Filterstatus und Mengenvorwahl",
            "Gewicht":"16,76 kg","Zertifizierung":"NSF/ANSI 58 und 372"},
        "X8":{"Filtration":"9-stufig, RO-Membran 0,0001 µm","Durchfluss":"0,56 GPM (ca. 2,12 l/min)",
            "Reinwasser-Abwasser-Verhältnis":"2:1","Wasserhahn":"Smart Display mit TDS- und Filterstatusanzeige",
            "Gewicht":"16,50 kg","Zertifizierung":"NSF/ANSI 58 und 372","Modellnummer":"WD-X8"},
        "G3P800":{"Filtration":"10-stufige tanklose Umkehrosmose-Filtration",
            "Reinwasser-Abwasser-Verhältnis":"3:1","Wasserhahn":"Smart Display mit TDS- und Filterstatusanzeige",
            "Filterlebensdauer":"CF ca. 6 Monate; CB ca. 12 Monate; RO ca. 24 Monate",
            "Gewicht":"16,33 kg","Zertifizierung":"NSF/ANSI 42, 58 und 372"},
        "G3P600":{"Filtration":"8-stufige tanklose Umkehrosmose-Filtration",
            "Reinwasser-Abwasser-Verhältnis":"2:1","Wasserhahn":"Smart Display mit TDS- und Filterstatusanzeige",
            "Filterlebensdauer":"CF ca. 6 Monate; CB ca. 12 Monate; RO ca. 24 Monate",
            "Gewicht":"14,7 kg","Zulaufdruck":"1,0–6,0 bar (14,5–87 psi)",
            "Zertifizierung":"NSF/ANSI 42, 58 und 372"},
        "G5P700A":{"Filtration":"8-stufig, RO-Membran 0,0001 µm und alkalische Mineralisierung",
            "Mineralien":"Calcium, Magnesium, Natrium und Kalium","Filterlebensdauer":"Je nach Kartusche ca. 6–12 Monate",
            "Schadstoffreduktion":"Unter anderem Chlor, Blei, Fluorid, Schwermetalle sowie PFOA/PFOS",
            "Installation":"Tanklose Untertischanlage; DIY-Wechselkartuschen","Platzbedarf":"Tankloses Design, laut Hersteller bis zu 70 % weniger Platz"},
        "G5P500A":{"Filtration":"8-stufig, RO-Membran 0,0001 µm und alkalische Mineralisierung",
            "Mineralien":"Calcium, Magnesium, Natrium und Kalium","Filterlebensdauer":"Je nach Kartusche ca. 6–12 Monate",
            "Schadstoffreduktion":"Unter anderem Chlor, Blei, Fluorid, Schwermetalle sowie PFOA/PFOS",
            "Wasserhahn":"Smart Display","Platzbedarf":"Tankloses Design, laut Hersteller bis zu 70 % weniger Platz"},
        "G2P600":{"Filtration":"MRO: RO-Membran, PP-Sediment, Aktivkohle und PET-Faltenfilter; CF: PP-Sediment und Aktivkohle",
            "Gewicht":"9,50 kg","Zulaufdruck":"1,0–6,0 bar (14,5–87 psi)","Netzkabel":"Ca. 150 cm",
            "Wasserhahn":"Metallarmatur; Filterlebensdaueranzeige am Gerät",
            "Filterlebensdauer":"CF ca. 12 Monate; MRO ca. 24 Monate","Material":"BPA-freies Gehäuse"},
        "K6":{"Filtration":"5-stufige Umkehrosmose-Filtration","Reinwasser-Abwasser-Verhältnis":"2:1",
            "Durchfluss":"600 GPD","Zulaufdruck":"1,0–6,0 bar (14,5–87 psi)","Zulauftemperatur":"5–38 °C",
            "Heißwassertemperatur":"40–95 °C einstellbar","Wasserhahn":"Smart LED, gebürstetes Nickel",
            "Filterlebensdauer":"KJF ca. 12 Monate","Anzeige":"TDS, Filterstatus und Temperatur",
            "Funktionen":"Selbstreinigung und Urlaubsmodus","Gewicht":"14,47 kg","Modellnummer":"WD-K6-W / WD-KJ-600"},
        "A2G":{"Filtration":"6-stufige RO-Filtration mit alkalischer Remineralisierung",
            "Reinwasser-Abwasser-Verhältnis":"3:1","Temperaturbereich":"15–95 °C; 6 Temperaturstufen",
            "Ausgabemengen":"5 voreingestellte Mengen","Tankvolumen":"Rohwasser 4,7 l; Reinwasser 1,0 l",
            "Filterlebensdauer":"A2RF ca. 12 Monate","Anzeige":"Favoriten, Temperatur und Filterstatus",
            "Gewicht":"Ca. 10 kg","UV-Hygiene":"Integrierte UV-Behandlung","Installation":"Keine Festinstallation"},
        "A1":{"Filtration":"Mehrstufige RO-Filtration mit dualer UV-Behandlung","Reinwasser-Abwasser-Verhältnis":"2:1",
            "Temperaturbereich":"Kalt bis 5 °C; heiß bis 95 °C; 6 Temperaturstufen","Ausgabemengen":"5 voreingestellte Mengen",
            "Tankvolumen":"Rohwasser ca. 4,0 l; Kaltwassertank ca. 1,0 l","Anzeige":"TDS, Menge, Temperatur und Filterstatus",
            "Filterlebensdauer":"CF ca. 6 Monate; RO ca. 12 Monate","UV-Hygiene":"Duale UV-Einheit; Herstellerangabe 99,9 %",
            "Installation":"Keine Festinstallation"},
        "K19-HG":{"Filtration":"5-in-1-Filter mit RO, Erhitzung und Mineralisierung","Reinwasser-Abwasser-Verhältnis":"3:1",
            "Rohwassertank":"5 Liter","Reinwassertank":"Herausnehmbar","Heißwassertemperatur":"Bis 95 °C",
            "Anzeige":"TDS, Ausgabemenge und Filterstatus","Filterlebensdauer":"K19RFG ca. 12 Monate",
            "Installation":"Keine Festinstallation"},
        "C1SL":{"Filtration":"Umkehrosmose mit alkalischer Mineralisierung","Reinwasser-Abwasser-Verhältnis":"3:1",
            "Rohwassertank":"3,25 Liter","Reinwassertank":"Herausnehmbar","Wassertemperatur":"Raumtemperatur",
            "Anzeige":"TDS, Ausgabemenge und Filterstatus","Filterlebensdauer":"C1RFG ca. 12 Monate",
            "Installation":"Keine Festinstallation"},
        "C1H":{"Filtration":"6-stufig, RO-Membran 0,0001 µm","Reinwasser-Abwasser-Verhältnis":"3:1",
            "Rohwassertank":"3,2 Liter","Reinwassertank":"1 Liter","Heißwassertemperatur":"Bis 95 °C",
            "Leistungsaufnahme":"1.700 W; 110–120 V, 50–60 Hz","Anzeige":"Filterstatus, Wassermenge und Temperatur",
            "Filterlebensdauer":"C1RF ca. 12 Monate","Installation":"Keine Festinstallation"},
    }
    specs.update(exact.get(model, {}))
    if "f2" in handle: specs["Set-Inhalt"] = "X8-System mit F2-Filter"
    if "f3-ersatzfilter" in handle: specs["Set-Inhalt"] = "X8-System mit zusätzlichem F3-Ersatzfilter"
    if "mz" in handle: specs["Set-Inhalt"] = f"{model}-System mit MNR35-Mineralfilter"
    return specs

products = []
for source_file in sorted(TMP.glob("wd-*.json")):
    try:
        raw = json.loads(source_file.read_text())
    except Exception:
        continue
    handle = raw["handle"]
    if any(item["source"].endswith(f"/{handle}") for item in products):
        continue
    title = raw["title"]
    name = re.sub(r"^Waterdrop\s+", "", title).strip()
    image = f"assets/products/waterdrop-{handle}.webp"
    products.append({
        "id": f"waterdrop-{handle}", "slug": f"waterdrop-{handle}", "brand": "Waterdrop",
        "brandSlug": "waterdrop", "name": name,
        "category": "Countertop RO" if any(x in title.lower() for x in ["auftisch","arbeitsplatte","k19","c1sl","c1h","a1 ","a2g"]) else "Direct Flow RO",
        "price": raw["price"]/100, "currency": "EUR", "rating": None, "reviews": 0,
        "image": image, "source": f"https://www.waterdropfilter.de/products/{handle}",
        "summary": f"{name}: aktuelle Umkehrosmoseanlage aus dem deutschen Waterdrop-Sortiment mit den auf der Herstellerseite dokumentierten Leistungs-, Filter- und Bedienmerkmalen.",
        "specs": waterdrop_specs(handle, title, clean(raw.get("description"))),
        "_remote_image": "https:" + raw["featured_image"] if raw.get("featured_image","").startswith("//") else raw.get("featured_image")
    })

arktis_raw = json.loads((TMP/"arktis.json").read_text())
products.append({
    "id":"arktisquelle-wasserfilter","slug":"arktisquelle-wasserfilter","brand":"Arktisquelle","brandSlug":"arktisquelle",
    "name":"Wasserfilter","category":"Countertop RO","price":arktis_raw["price"]/100,"currency":"EUR",
    "rating":None,"reviews":0,"image":"assets/products/arktisquelle-wasserfilter.webp",
    "source":"https://arktisquelle.de/products/arktisquelle-wasserfilter",
    "summary":"Premium-Auftisch-Umkehrosmoseanlage mit siebenstufiger SeptaTech®-Filtration, DoubleUV-Protect®, Edelstahl-Wassertank, Touchdisplay und Heißwasserfunktion.",
    "specs":{"Bauart":"Auftischsystem ohne Festwasseranschluss","Filtration":"7-Stufen SeptaTech®","Membran":"Molekularmembran / Umkehrosmose, 0,0001 µm","UV-Schutz":"DoubleUV-Protect® mit zwei UVC-Keimsperren","Rohwassertank":"3,5 Liter","Material":"Interner Wassertank und Auslauf aus Edelstahl","Temperaturen":"35–100 °C einstellbar; vier Ausgabemodi","Bedienung":"Touchdisplay, Wasserqualität sensorüberwacht","Filterwechsel":"In weniger als 5 Minuten durch den Nutzer","Installation":"Keine Festinstallation; aufstellen, befüllen, einstecken","Betriebskosten":"Herstellerbeispiel ca. 2–3 € pro Monat","Garantie/Test":"30 Tage Geld-zurück-Garantie","Lieferumfang":"Gerät, vorinstallierter Filtersatz, Glaskaraffen-Set, Auffangschale, Filtertool, Anleitung"},
    "_remote_image":"https:"+arktis_raw["featured_image"]
})

products.append({
    "id":"ho3-home-one","slug":"ho3-home-one","brand":"HO3 Filter","brandSlug":"ho3-filter","name":"Home One",
    "category":"Countertop RO","price":None,"currency":"EUR","rating":None,"reviews":0,
    "image":"assets/products/ho3-home-one.webp","source":"https://ho3filter.de/products/home-one-bundle",
    "summary":"Auftisch-Umkehrosmoseanlage mit nach NSF/ANSI 58 geprüft beschriebener Filterleistung, optionaler Mineralisierung, Heißwasser, doppelter Luma-UV-Lampe und internem Reinwassertank.",
    "specs":{"Bauart":"Auftisch-Umkehrosmoseanlage","Filtration":"Umkehrosmose; Filterleistung laut Hersteller nach NSF/ANSI 58 geprüft","Mineralisierung":"Einsetzbarer Mineralfilter","UV-Schutz":"Doppelte Luma-UV-Lampe","Heißwasser":"Integriertes Heizmodul","Rohwassertank":"5 Liter","Reinwassertank":"1 Liter","Abmessungen":"24 × 43,5 × 38,5 cm","Gewicht":"7,2 kg","Standby-Leistung":"1 W","Filterbetrieb":"30 W","Heizleistung":"2.200 W","Installation":"Keine Festinstallation erforderlich","Wartung":"Wechselbare Filtermodule laut Herstellerplan","Lieferumfang":"Home-One-Gerät, Filtermodule und Mineralisierung gemäß gewähltem Bundle"},
    "_remote_image":"https://ho3filter.de/cdn/shop/files/21_167efdab-b367-41f1-8354-11e042a2374a_1200x1200.png?v=1777475344"
})

aqua_info = {
    "1189":("Mini Touch",795.00,"Mini-silver.jpg","Countertop RO"),
    "1457":("Mini Touch PRO – Black",1195.00,"MiniTouch-PRO-black.jpg","Countertop RO"),
    "1221":("Basic",895.00,"basic.jpg","Direct Flow RO"),
    "1231":("Sparkling",1795.00,"sparkling_button.jpg","Water Dispenser"),
    "1237":("Sparkling Pro",2295.00,"sparkling-pro.jpg","Water Dispenser"),
    "1193":("Hydrogenflasche Glas schwarz",169.00,"hydrogen-schwarz.jpg","Hydrogen Bottles"),
}
for detailid,(name,price,image_name,category) in aqua_info.items():
    source = f"https://aqua-global.com/?mode=artikel&detailid={detailid}&wg_id=1098"
    page = (TMP/f"aqua-{detailid}.html").read_text(errors="ignore")
    specs = {}
    for target, label in re.findall(r'<button[^>]+data-bs-target="#([^"]+)"[^>]*>(.*?)</button>', page, re.I|re.S):
        body_match = re.search(r'id="'+re.escape(target)+r'"[\s\S]*?<div class="accordion-body">(.*?)</div>', page, re.I|re.S)
        key, value = clean(label), clean(body_match.group(1)) if body_match else ""
        if key in {"Filterwechsel","Temperaturen","Tankgröße","Filterleistung","Elektrische Parameter","Abmessungen und Gewicht","Abwasserverhältnis","Filtrationsverfahren","Tankvolumen"} and value:
            specs[key] = value
    if not specs:
        specs = {"Produktart":category,"Technologie":"Herstellerangaben auf der offiziellen Produktseite","Preisstatus":"Offizieller Shoppreis bei Recherche"}
    aqua_exact = {
        "1189":{"Filterwechsel":"Composite 6–12 Monate; Postfilter 6–12 Monate; RO-Membran 12–24 Monate; UV 60 Monate",
            "Temperaturen":"Baby ca. 50 °C; Tee ca. 85 °C; Heiß ca. 95 °C; Raumtemperatur",
            "Tankvolumen":"2,5 Liter","Filterleistung":"10–15 l/h; Zulaufwasser 10–38 °C",
            "Elektrische Parameter":"220–240 V / 50 Hz; Heizung 2.180 W; Standby 0–0,1 kWh/24 h",
            "Abmessungen und Gewicht":"183 × 388 × 300 mm; 6,5 kg","Abwasserverhältnis":"1:1","Filtrationsverfahren":"Umkehrosmose"},
        "1457":{"Filterwechsel":"Composite 6–12 Monate; RO-Membran 12–24 Monate; UV 60 Monate",
            "Temperaturen":"Baby 45–50 °C; Tee 80–85 °C; Heiß 90–95 °C; Raumtemperatur; Kalt 6–12 °C",
            "Tankvolumen":"Nutzbares Reinwasser ca. 0,8–1,0 Liter","Filterleistung":"15–25 l/h; Zulaufwasser 10–38 °C",
            "Elektrische Parameter":"220–240 V / 50 Hz; Heizung 2.100 W; Standby 1 W/h",
            "Abmessungen und Gewicht":"225 × 376 × 329 mm; 6,5 kg","Abwasserverhältnis":"1:1","Filtrationsverfahren":"Umkehrosmose"},
        "1221":{"Filterwechsel":"PC-C 6–12 Monate; RO-Membran 18–36 Monate","Temperaturen":"Raumtemperatur",
            "Tankvolumen":"Tankloses Direct-Flow-System","Filterleistung":"Ca. 1 l/min",
            "Elektrische Parameter":"220–240 V / 50 Hz; 64 W","Abmessungen und Gewicht":"Ø 240 × 395 mm; 7,84 kg",
            "Abwasserverhältnis":"1:1","Filtrationsverfahren":"Umkehrosmose"},
        "1231":{"Filterwechsel":"Nano-Silver-Carbon 6–12 Monate; UV 6–12 Monate",
            "Temperaturen":"Sprudel, gekühlt, still gekühlt und Raumtemperatur","Tankvolumen":"Tankloses Direct-Flow-System",
            "Filterleistung":"Ca. 1 l/min","Elektrische Parameter":"220–240 V / 50 Hz",
            "Abmessungen und Gewicht":"230 × 380 × 380 mm; 18 kg","Filtrationsverfahren":"Nano-Silver-Carbon und UV; keine integrierte RO-Membran"},
        "1237":{"Filterwechsel":"PC-C 6–12 Monate; RO-Membran 18–36 Monate; UV 6–12 Monate",
            "Temperaturen":"Sprudel, gekühlt, still, Raumtemperatur und heiß","Tankvolumen":"Tankloses Direct-Flow-System",
            "Filterleistung":"Ca. 1 l/min","Elektrische Parameter":"220–240 V / 50 Hz",
            "Abmessungen und Gewicht":"Basic: Ø 240 × 395 mm / 7,84 kg; Sparkling Pro: 230 × 380 × 380 mm / 19 kg",
            "Abwasserverhältnis":"1:1","Filtrationsverfahren":"Umkehrosmose im Basic-Modul, Kühlung, Karbonisierung und UV"},
        "1193":{"Produktart":"Tragbare Wasserstoffflasche","Wasserstoffkonzentration":"Bis zu 1.200 ppb",
            "ORP":"Bis zu −600 mV","Flaschenkapazität":"400 ml","Leistung":"USB 3,7 V / 2 A; Ausgang ≤ 5 W",
            "Abmessungen":"Ø 70 × 230 mm","Gewicht":"405 g","Flaschenmaterial":"Borosilikatglas",
            "Geeignetes Wasser":"Stilles, reines Osmosewasser; laut Hersteller aus Mini Touch, Flexible Touch, Basic, Sparkling oder Sparkling Pro",
            "Gewährleistung":"24 Monate"},
    }
    specs.update(aqua_exact.get(detailid, {}))
    products.append({
        "id":f"aqua-global-{detailid}","slug":f"aqua-global-{re.sub('[^a-z0-9]+','-',name.lower()).strip('-')}",
        "brand":"Aqua Global","brandSlug":"aqua-global","name":name,"category":category,"price":price,"currency":"EUR",
        "rating":None,"reviews":0,"image":f"assets/products/aqua-global-{detailid}.webp","source":source,
        "summary":f"Aqua Global {name}: Wasseraufbereitungssystem aus dem aktuellen Hersteller-Shop mit offiziell veröffentlichten technischen Daten und Zubehörangaben.",
        "specs":specs,
        "_remote_image":f"https://aqua-global.com/admin1/_files/_artikelbilder/{detailid}/{image_name}"
    })

brands_updates = {
    "arktisquelle":{"description_de":"Deutscher Anbieter von Auftisch-Umkehrosmoseanlagen mit SeptaTech®-Filtration, UV-Hygieneschutz, Heißwasserfunktion und eigenem Servicekonzept.","description_en":"German supplier of countertop reverse-osmosis systems with multi-stage filtration, UV hygiene protection and hot-water functions.","website":"https://arktisquelle.de"},
    "waterdrop":{"description_de":"Internationale Wasserfiltermarke mit tanklosen Untertisch-RO-Systemen, intelligenten Wasserhähnen sowie Auftischanlagen für heißes, kaltes und mineralisiertes Wasser.","description_en":"International water-filtration brand offering tankless under-sink RO systems, smart faucets and countertop hot, cold and mineralized-water dispensers.","website":"https://www.waterdropfilter.de"},
    "aqua-global":{"description_de":"Deutscher Anbieter von Umkehrosmoseanlagen, Wasserbars, Heiß-/Kaltwasserspendern, Sprudelsystemen und Wasserstoffflaschen für Haushalt und Büro.","description_en":"German supplier of reverse-osmosis systems, water bars, hot/cold dispensers, sparkling-water systems and hydrogen bottles.","website":"https://aqua-global.com"},
}

brands_path = ROOT/"data/brands.json"
brands = json.loads(brands_path.read_text())
for brand in brands:
    if brand["slug"] in brands_updates:
        brand.update(brands_updates[brand["slug"]])
if not any(b["slug"]=="ho3-filter" for b in brands):
    brands.append({"slug":"ho3-filter","name":"HO3 Filter","country":"Germany","website":"https://ho3filter.de",
        "founded":None,"description_de":"Deutsche Wasserfiltermarke für Auftisch-Umkehrosmoseanlagen mit UV-Hygieneschutz, Heißwasserfunktion und optionaler Mineralisierung.",
        "description_en":"German water-filter brand for countertop reverse-osmosis systems with UV hygiene protection, hot water and optional remineralization.",
        "products_count":1,"rating":None,"logo":"assets/brands/ho3-filter.png"})

products_path = ROOT/"data/products.json"
existing = json.loads(products_path.read_text())
# Replace the old generic Arktisquelle record rather than duplicating it.
existing = [p for p in existing if p.get("slug")!="arktisquelle-direct-flow-premium"]
for product in products:
    product.pop("_remote_image", None)
    index = next((i for i,p in enumerate(existing) if p.get("slug")==product["slug"] or p.get("source")==product["source"]), -1)
    if index < 0: existing.append(product)
    else: existing[index] = {**existing[index], **product}
for brand in brands:
    brand["products_count"] = sum(1 for p in existing if p.get("brandSlug")==brand["slug"] or p.get("brand_slug")==brand["slug"] or p.get("brand")==brand["name"])
brands_path.write_text(json.dumps(brands,ensure_ascii=False,indent=2)+"\n")
products_path.write_text(json.dumps(existing,ensure_ascii=False,indent=2)+"\n")

def header(depth=".."):
    return f'''<div class="topbar"><div class="container"><span>Unabhängige Datenbank für Wassertechnologie</span><span>Erfahrungen · Vergleiche · Labordaten</span></div></div><header class="site-header"><div class="header-shell container"><a aria-label="WASSER.MARKET Startseite" class="site-brand" href="{depth}/index.html"><img alt="WASSER.MARKET" src="{depth}/assets/img/wasser-market-logo.jpg" loading="eager"></a><nav class="desktop-nav"><a href="{depth}/products.html">Produkte</a><a href="{depth}/brands.html">Marken</a><a href="{depth}/compare.html">Vergleichen</a><a href="{depth}/community.html">Community</a><div class="nav-more"><button class="nav-more-btn" type="button">Wissen</button><div class="nav-more-menu"><a href="{depth}/knowledge.html">Wasserwissen</a><a href="{depth}/technologies.html">Technologien</a></div></div></nav><div class="header-tools"><a class="btn primary compact-compare" href="{depth}/compare.html">⇄ <span>Vergleichen</span></a><button aria-expanded="false" aria-label="Menü öffnen" class="icon-btn mobile-menu-btn" type="button">☰</button></div></div><div aria-hidden="true" class="mobile-nav-panel"><div class="container mobile-nav-inner"><a href="{depth}/products.html">Produkte</a><a href="{depth}/brands.html">Marken</a><a href="{depth}/compare.html">Vergleichen</a><a href="{depth}/community.html">Community</a><a href="{depth}/knowledge.html">Wasserwissen</a></div></div></header>'''

def footer(depth=".."):
    return f'''<footer class="site-footer"><div class="footer-bottom"><div class="container"><span>© WASSER.MARKET</span><span>Unabhängige Datenbank für Wassertechnologie</span></div></div></footer><script defer src="{depth}/assets/i18n.js"></script><script defer src="{depth}/assets/app.js"></script>'''

def card(p, depth="../"):
    specs = list((p.get("specs") or {}).items())[:3]
    return f'''<div class="product-card" data-product-id="{esc(p["id"])}"><a class="photo" href="{depth}products/{esc(p["slug"])}.html"><img alt="{esc(p["brand"])} {esc(p["name"])}" src="{depth}{esc(p["image"])}" loading="lazy"></a><div class="brand">{esc(p["brand"])}</div><h3>{esc(p["name"])}</h3><div class="rating">Herstellerdaten</div><div class="price">{esc(money(p.get("price")))}</div><div class="specs">{''.join(f"<span>{esc(k)}: {esc(v)}</span>" for k,v in specs)}</div><div class="actions"><a class="btn small" href="{depth}products/{esc(p["slug"])}.html">Alle Daten</a><button class="btn small" data-compare="{esc(p["id"])}">+ Compare</button></div></div>'''

for p in products:
    schema={"@context":"https://schema.org","@type":"Product","name":f'{p["brand"]} {p["name"]}',"image":f'https://wasser.market/{p["image"]}',"brand":{"@type":"Brand","name":p["brand"]},"category":p["category"],"description":p["summary"]}
    if p["price"] is not None: schema["offers"]={"@type":"Offer","priceCurrency":"EUR","price":str(p["price"]),"url":p["source"]}
    rows="".join(f"<tr><td>{esc(k)}</td><td>{esc(v)}</td></tr>" for k,v in p["specs"].items())
    page=f'''<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(p["brand"])} {esc(p["name"])} – Daten & Eigenschaften</title><meta name="description" content="{esc(p["summary"])}"><link rel="stylesheet" href="../assets/css/core.css?v=20260723-catalog1"><link rel="stylesheet" href="../assets/css/product.css?v=20260723-catalog1"><link rel="canonical" href="https://wasser.market/products/{esc(p["slug"])}.html"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head><body class="wm-v2">{header()}<main><div class="container"><div class="breadcrumbs"><a href="../index.html">Home</a> / <a href="../products.html">Produkte</a> / {esc(p["name"])}</div><section class="device-layout"><div class="device-photo"><img alt="{esc(p["brand"])} {esc(p["name"])}" src="../{esc(p["image"])}" loading="eager"></div><div class="device-info"><span class="badge">{esc(p["category"])}</span><h1>{esc(p["brand"])} {esc(p["name"])}</h1><p class="lead">{esc(p["summary"])}</p><div class="price">{esc(money(p["price"]))}</div><p><a class="btn primary" href="{esc(p["source"])}" target="_blank" rel="nofollow noopener">Offizielle Produktseite ↗</a></p></div></section><div class="content-grid"><section class="panel"><h2>Technische Daten</h2><table class="spec-table">{rows}</table><h2>Datenhinweis</h2><p>Preis, Bild und technische Angaben stammen von der verlinkten offiziellen Produktseite. Varianten und Verfügbarkeit können sich ändern.</p></section><aside><div class="panel"><h3>Einordnung</h3><table class="spec-table"><tr><td>Marke</td><td><a href="../brands/{esc(p["brandSlug"])}.html">{esc(p["brand"])}</a></td></tr><tr><td>Kategorie</td><td>{esc(p["category"])}</td></tr><tr><td>Preisstatus</td><td>Offizieller Shoppreis bei Recherche</td></tr></table></div></aside></div></div></main>{footer()}</body></html>'''
    (ROOT/"products"/f'{p["slug"]}.html').write_text(page)

for slug in ["arktisquelle","waterdrop","aqua-global","ho3-filter"]:
    brand=next(b for b in brands if b["slug"]==slug)
    items=[p for p in existing if p.get("brandSlug")==slug or p.get("brand_slug")==slug or p.get("brand")==brand["name"]]
    page=f'''<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(brand["name"])} – Marke und Produkte</title><meta name="description" content="{esc(brand["description_de"])}"><link rel="stylesheet" href="../assets/css/core.css?v=20260723-catalog1"><link rel="stylesheet" href="../assets/css/brand.css?v=20260723-catalog1"><link rel="stylesheet" href="../assets/css/product.css?v=20260723-catalog1"><link rel="canonical" href="https://wasser.market/brands/{slug}.html"></head><body class="wm-v2">{header()}<main><div class="container"><div class="breadcrumbs"><a href="../index.html">Home</a> / <a href="../brands.html">Marken</a> / {esc(brand["name"])}</div><section class="brand-hero"><div class="brand-hero-primary"><div class="brand-hero-logo"><img src="../{esc(brand["logo"])}" alt="{esc(brand["name"])} Logo"></div><div class="brand-hero-copy"><span class="badge">Wasserfiltration</span><h1>{esc(brand["name"])}</h1><p class="lead">{esc(brand["description_de"])}</p></div></div><aside class="brand-hero-details"><h2>Markenprofil</h2><dl><div><dt>Land</dt><dd>{esc(brand.get("country","—"))}</dd></div><div><dt>Modelle</dt><dd>{len(items)}</dd></div></dl><a class="btn primary" href="{esc(brand["website"])}" target="_blank" rel="nofollow noopener">Offizielle Website ↗</a></aside></section><section class="panel"><h2>Produkte in der Datenbank</h2><div class="product-grid">{''.join(card(p) for p in items)}</div></section></div></main>{footer()}</body></html>'''
    (ROOT/"brands"/f"{slug}.html").write_text(page)

# Add HO3 to directory once and refresh brand metadata.
brands_html=(ROOT/"brands.html").read_text()
if 'brands/ho3-filter.html' not in brands_html:
    ho3=next(b for b in brands if b["slug"]=="ho3-filter")
    card_html=f'''<a class="brand-directory-card" href="brands/ho3-filter.html" data-brand-name="ho3 filter" data-brand-country="germany"><div class="brand-logo-wrap"><img src="assets/brands/ho3-filter.png" alt="HO3 Filter Logo" loading="lazy"></div><div class="brand-card-body"><span class="badge">Umkehrosmose</span><h3>HO3 Filter</h3><p>{esc(ho3["description_de"])}</p><span class="brand-meta">Germany · 1 Modell</span><span class="brand-link">Profil ansehen →</span></div></a>'''
    marker='<div class="panel brand-empty"'
    pos=brands_html.find(marker)
    grid_end=brands_html.rfind("</div>",0,pos)
    brands_html=brands_html[:grid_end]+card_html+brands_html[grid_end:]
brands_html=re.sub(r'\d+ bekannte Hersteller',f'{len(brands)} bekannte Hersteller',brands_html)
brands_html=re.sub(r'<span id="brandDirectoryCount" class="brand-count-badge">\d+ Marken</span>',f'<span id="brandDirectoryCount" class="brand-count-badge">{len(brands)} Marken</span>',brands_html)
(ROOT/"brands.html").write_text(brands_html)

# Remove obsolete Arktisquelle page and product references from app, add current batch.
app_path=ROOT/"assets/app.js"
app=app_path.read_text()
app=re.sub(r"\{id:'arktisquelle-direct-flow-premium'[^\n]*\},?\n?","",app)
for p in products:
    line="{id:"+json.dumps(p["id"])+",brand:"+json.dumps(p["brand"],ensure_ascii=False)+",name:"+json.dumps(p["name"],ensure_ascii=False)+",cat:"+json.dumps(p["category"])+",price:"+json.dumps(money(p["price"]),ensure_ascii=False)+",priceValue:"+(str(p["price"]) if p["price"] is not None else "null")+",features:[],ppb:null,flow:"+json.dumps(p["specs"].get("RO-Leistung","Not published"))+",maint:"+json.dumps(p["specs"].get("Filterwechsel","Not published"),ensure_ascii=False)+",liter:'—',membrane:"+json.dumps(p["specs"].get("Membran",p["specs"].get("Filtration","Not published")),ensure_ascii=False)+",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"+json.dumps(p["specs"].get("Mineralisierung","Not published"),ensure_ascii=False)+",noise:'Not published',power:"+json.dumps(p["specs"].get("Heizleistung","Not published"),ensure_ascii=False)+",warranty:"+json.dumps(p["specs"].get("Garantie","Not published"),ensure_ascii=False)+",country:'Not published',image:"+json.dumps(p["image"])+",url:"+json.dumps("products/"+p["slug"]+".html")+"}"
    pattern=re.compile(r"\{id:[\"']"+re.escape(p["id"])+r"[\"'][^\n]*\}")
    if pattern.search(app): app=pattern.sub(lambda _: line,app)
    else: app=app.replace("\n];",",\n"+line+"\n];")
app_path.write_text(app)

sitemap_path=ROOT/"sitemap.xml"
sitemap=sitemap_path.read_text()
sitemap=re.sub(r'<url><loc>https://wasser.market/products/arktisquelle-direct-flow-premium.html</loc></url>\s*','',sitemap)
for url in ["https://wasser.market/brands/ho3-filter.html"]+[f'https://wasser.market/products/{p["slug"]}.html' for p in products]:
    if f"<loc>{url}</loc>" not in sitemap:
        sitemap=sitemap.replace("</urlset>",f"<url><loc>{url}</loc></url>\n</urlset>")
sitemap_path.write_text(sitemap)

# Store current batch in additions as well, so later catalog imports preserve it.
add_path=ROOT/"data/catalog-additions.json"
additions=json.loads(add_path.read_text())
ho3_record={"slug":"ho3-filter","name":"HO3 Filter","country":"Germany","website":"https://ho3filter.de","group":"Water Filtration","description":"Deutsche Wasserfiltermarke für Auftisch-Umkehrosmoseanlagen mit UV-Hygieneschutz, Heißwasser und optionaler Mineralisierung."}
idx=next((i for i,b in enumerate(additions["brands"]) if b["slug"]=="ho3-filter"),-1)
if idx<0:additions["brands"].append(ho3_record)
else:additions["brands"][idx]=ho3_record
additions["products"]=[p for p in additions["products"] if p.get("slug")!="arktisquelle-direct-flow-premium"]
for p in products:
    record={k:v for k,v in p.items() if not k.startswith("_")}
    record["specs"]=list(record["specs"].items())
    idx=next((i for i,x in enumerate(additions["products"]) if x.get("slug")==p["slug"]),-1)
    if idx<0:additions["products"].append(record)
    else:additions["products"][idx]=record
add_path.write_text(json.dumps(additions,ensure_ascii=False,indent=2)+"\n")

print(f"Imported {len(products)} official products; total catalog: {len(existing)} products, {len(brands)} brands")
