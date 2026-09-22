"""Idempotent importer for the two reviewed pilot records. No mass-import mode.

Run from any directory: python scripts/import-agent-test.py
Delivery uses the authenticated GitHub API and existing FTPS deployment.
"""
import copy
import html
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
EXPECTED = {('Waterdrop','G3P800'):'waterdrop-umkehrosmoseanlage-g3p800',
            ('OsmoFresh','Fusion Pro 2'):'osmofresh-fusion-pro-2'}
def read(path): return (ROOT/path).read_text(encoding='utf-8')
def write(path, value): (ROOT/path).write_text(value,encoding='utf-8')
def dump(path, value): write(path,json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def esc(value): return html.escape(str(value),quote=True)
def js(value): return json.dumps(value,ensure_ascii=False).replace('<','\\u003c')
def public_image(path): return path if path.startswith('https://') else '../'+path
def price(p): return f"{p['price']:,.0f}".replace(',','.')+' €' if p.get('price') is not None else '—'
LABELS = dict(zip(
    ['identity.model','system.technology','system.installation_type','system.tankless','filtration.advertised_stage_count','performance.rated_capacity_gpd','smart_features.display','smart_features.filter_life_indicator','smart_features.smart_faucet','performance.dispensing_flow_lpm','performance.minimum_inlet_pressure','performance.maximum_inlet_pressure','performance.maximum_feed_temperature','electrical.standby_power_w','electrical.cooling_power_w','electrical.maximum_power_w','physical.dimensions_raw','physical.width_mm','physical.depth_mm','physical.height_mm','commercial.current_price','commercial.currency'],
    ['Modell','Technologie','Installation','Tanklos','Filterstufen','Membranleistung','Display','Filterstatusanzeige','Intelligenter Wasserhahn','Durchfluss','Min. Eingangsdruck','Max. Eingangsdruck','Max. Eingangstemperatur','Standby','Kühlleistung','Max. Leistungsaufnahme','Abmessungen','Breite','Tiefe','Höhe','Herstellerpreis','Währung']))

batch=json.loads(read('data/agent-test-products.json'))
assert batch.get('schema_version')==1 and batch.get('reviewed') is True
records=batch['products']
assert len(records)==2 and {(r['brand'],r['model']) for r in records}==set(EXPECTED)
for r in records:
    assert r['target_id']==EXPECTED[r['brand'],r['model']]
    assert urlparse(r['source_url']).scheme=='https'
    for path,field in r['fields'].items():
        assert field.get('value') is not None and field.get('evidence'), path
        assert all(e['source_url']==r['source_url'] for e in field['evidence']),path

products=json.loads(read('data/products.json')); before=copy.deepcopy(products)
assert len({p['id'] for p in products})==len(products)
assert len({p['slug'] for p in products})==len(products)
for r in records:
    existing=[p for p in products if p['id']==r['target_id']]
    assert len(existing)<=1
    if r['model']=='G3P800':
        assert len(existing)==1, 'Existing German G3P800 required; refuse to guess identity'
        p=existing[0]
        assert p['brand']=='Waterdrop' and 'mineralien' not in p['slug']
        assert p['currency']=='EUR' and urlparse(p['source']).hostname=='www.waterdropfilter.de'
        p['specs']['Agent-Abgleich']='G3P800 · 800 GPD · 10 Filterstufen (US-Herstellerseite)'
    else:
        p=existing[0] if existing else {'id':r['target_id'],'slug':r['target_id'],'brand':'OsmoFresh','brandSlug':'osmofresh','name':'Fusion Pro 2','category':'Countertop RO','rating':None,'reviews':0,'featured':False}
        if not existing: products.append(p)
        f=r['fields']; val=lambda path:f[path]['value']
        p.update(price=val('commercial.current_price'),currency=val('commercial.currency'),image=r['image']['url'],source=r['source_url'],summary='Umkehrosmoseanlage mit 7-Zoll-Display. Technische Herstellerdaten mit nachvollziehbaren Quellen.')
        assert p['currency']=='EUR'
        p['specs']={'Technologie':val('system.technology'), 'Durchfluss':f"{val('performance.dispensing_flow_lpm')} L/min", 'Display':val('smart_features.display'),
            'Eingangsdruck':f"{val('performance.minimum_inlet_pressure')}–{val('performance.maximum_inlet_pressure')} bar",
            'Max. Eingangstemperatur':f"{val('performance.maximum_feed_temperature')} °C",
            'Standby':f"{val('electrical.standby_power_w')} W",'Kühlleistung':f"{val('electrical.cooling_power_w')} W",
            'Max. Leistungsaufnahme':f"{val('electrical.maximum_power_w')} W",'Maße (L × B × H)':val('physical.dimensions_raw'),
            'Membranleistung (GPD)':'—','Rohwassertank':'—'}
    p['agent_import']={'batch':batch['batch'],'identity':{'brand':r['brand'],'model':r['model']},'checked_at':r['checked_at'],'source_url':r['source_url'],'fields':r['fields'],'publication_status':'PUBLISHABLE_PARTIAL'}

assert len(products)==len(before)+(0 if any(p['id']=='osmofresh-fusion-pro-2' for p in before) else 1)
for old in before:
    if old['id'] not in EXPECTED.values(): assert old==next(p for p in products if p['id']==old['id'])
dump('data/products.json',products)

# Retain the site's header, footer, analytics and styles using its existing page.
template=read('products/osmofresh-fusion-pro.html')
header=template[template.index('<body'):template.index('<main')]
footer=template[template.index('</main>')+7:]
for r in records:
    p=next(p for p in products if p['id']==r['target_id'])
    title=p['brand']+' '+r['model']; url='https://wasser.market/products/'+p['slug']
    brand_slug='waterdrop' if r['brand']=='Waterdrop' else 'osmofresh'
    schema={'@context':'https://schema.org','@type':'Product','name':title,'brand':{'@type':'Brand','name':p['brand']},'url':url,'image':p['image'] if p['image'].startswith('https://') else 'https://wasser.market/'+p['image']}
    if p.get('price') is not None: schema['offers']={'@type':'Offer','price':p['price'],'priceCurrency':p['currency'],'url':p['source']}
    head=template[:template.index('<body')]
    head=re.sub(r'<title>.*?</title>',f'<title>{esc(title)} – Daten &amp; Quellen</title>',head)
    head=re.sub(r'<script type="application/ld\+json">.*?</script>','',head,flags=re.S)
    head=re.sub(r'<meta (?:name="(?:description|twitter:[^"]+)"|property="og:[^"]+")[^>]*>','',head)
    head=re.sub(r'<link rel="canonical"[^>]*>',f'<link rel="canonical" href="{url}">',head)
    head=head.replace('</head>',f'<meta name="description" content="{esc(title)}: technische Daten und Herstellerquellen."><script type="application/ld+json">{js(schema)}</script></head>')
    rows=''.join(f'<tr><th scope="row">{esc(k)}</th><td>{esc(v)}</td></tr>' for k,v in p['specs'].items())
    evidence=''
    for path,field in r['fields'].items():
        e=field['evidence'][0]
        shown='Ja' if field['value'] is True else 'Nein' if field['value'] is False else field['value']
        evidence+=f'<details><summary>{esc(LABELS[path])}: {esc(shown)} {esc(field.get("unit",""))}</summary><p>ℹ Herstellerangabe · {esc(r["checked_at"])}</p><blockquote>{esc(e["original_text"])}</blockquote><a href="{esc(e["source_url"])}" target="_blank" rel="noopener nofollow">Quelle beim Hersteller</a></details>'
    note='Die Preise und regionalen Angaben beziehen sich auf das deutsche Angebot. Der ergänzende Datenabgleich stammt von der US-Herstellerseite; US-Preis, Gewicht und Zertifizierungen wurden nicht auf das deutsche Angebot übertragen.' if r['model']=='G3P800' else 'Nicht ausreichend belegte Werte sind mit — gekennzeichnet. Abbildung: Jet Black; die Modellseite umfasst mehrere Farben. Herstellerangaben sind keine unabhängigen Laborprüfungen.'
    main=f'''<main><div class="container"><div class="breadcrumbs"><a href="../products">Produkte</a> / {esc(title)}</div><section class="device-layout"><div class="device-photo"><img src="{esc(public_image(p['image']))}" alt="{esc(title)}" loading="eager"></div><div class="device-info"><a href="../brands/{brand_slug}"><img src="../assets/brands/{brand_slug}.png" alt="{esc(p['brand'])}" style="max-width:150px;max-height:55px;object-fit:contain"></a><h1>{esc(title)}</h1><span class="badge">{esc(p['category'])}</span><p class="lead">{esc(p.get('summary',''))}</p><div class="price">{price(p)}</div><p>Hersteller-/Shoppreis bei Recherche. Datenabgleich: {esc(r['checked_at'])}.</p><a class="btn primary" href="{esc(p['source'])}" target="_blank" rel="noopener nofollow">Herstellerangebot ↗</a> <button class="btn" data-compare="{esc(p['id'])}">+ Compare</button></div></section><section class="panel"><h2>Technische Daten</h2><table class="spec-table">{rows}</table><p>{esc(note)}</p></section><section class="panel"><h2>Quellen und Datenprüfung</h2><p>ℹ Herstellerangabe · — kein ausreichend belegter Wert. Zertifizierungsangaben wurden nicht unabhängig bestätigt.</p>{evidence}</section></div></main>'''
    write('products/'+p['slug']+'.html',head+header+main+footer)

def card(p,prefix=''):
    image=p['image'] if p['image'].startswith('https://') else prefix+p['image']
    specs=''.join(f'<span>{esc(k)}: {esc(v)}</span>' for k,v in list(p['specs'].items())[:3])
    return f'<div class="product-card" data-product-id="{esc(p["id"])}"><a class="photo" href="{prefix}products/{esc(p["slug"])}"><img src="{esc(image)}" alt="{esc(p["brand"]+" "+p["name"])}" loading="lazy"></a><div class="brand">{esc(p["brand"])}</div><h3>{esc(p["name"])}</h3><div class="rating">Herstellerdaten</div><div class="price">{price(p)}</div><div class="specs">{specs}</div><div class="actions"><a class="btn small" href="{prefix}products/{esc(p["slug"])}">Alle Daten</a><button class="btn small" data-compare="{esc(p["id"])}">+ Compare</button></div></div>'

def replace_card(page,p,prefix=''):
    pattern=r'<div class="product-card"[^>]*data-product-id="'+re.escape(p['id'])+r'"[^>]*>'
    match=re.search(pattern,page)
    if not match: return page,False
    depth=1; end=None
    for token in re.finditer(r'<div\b[^>]*>|</div\s*>',page[match.end():]):
        depth+=-1 if token.group().startswith('</') else 1
        if depth==0: end=match.end()+token.end();break
    assert end
    return page[:match.start()]+card(p,prefix)+page[end:],True

catalog=read('products.html')
for r in records:
    p=next(p for p in products if p['id']==r['target_id'])
    catalog,found=replace_card(catalog,p)
    if not found:
        marker=re.search(r'<div class="product-grid"[^>]*>',catalog[catalog.index('id="productResultText"'):])
        assert marker
        position=catalog.index('id="productResultText"')+marker.end()
        catalog=catalog[:position]+card(p)+catalog[position:]
catalog=re.sub(r'(<h2 id="productResultCount">).*?(</h2>)',rf'\g<1>{len(products)} Modelle\2',catalog)
catalog=re.sub(r'(<p id="productResultText">).*?(</p>)',rf'\g<1>{len(products)} Produkte in der Datenbank\2',catalog)
write('products.html',catalog)

brands=json.loads(read('data/brands.json'))
for slug in ('osmofresh','waterdrop'):
    page=read('brands/'+slug+'.html'); brand=next(b for b in brands if b['slug']==slug)
    count=sum(p['brand'].casefold()==brand['name'].casefold() for p in products)
    brand['products_count']=count
    page=re.sub(r'(<dt>Modelle</dt><dd>)\d+(</dd>)',rf'\g<1>{count}\2',page)
    for r in records:
        if r['brand'].casefold()!=brand['name'].casefold():continue
        p=next(p for p in products if p['id']==r['target_id'])
        page,found=replace_card(page,p,'../')
        if not found: page=page.replace('<div class="product-grid">','<div class="product-grid">'+card(p,'../'),1)
    write('brands/'+slug+'.html',page)
dump('data/brands.json',brands)

app=read('assets/app.js')
for r in records:
    p=next(p for p in products if p['id']==r['target_id'])
    if r['model']=='G3P800':continue  # Existing regional comparison data stays intact.
    record={k:'—' for k in ('flow','maint','liter','membrane','pfas','viruses','bacteria','nitrates','lead','arsenic','micro','tds','remin','noise','power','warranty','country')}
    record.update(id=p['id'],brand=p['brand'],name=p['name'],cat=p['category'],price=price(p),priceValue=p['price'],features=['display'],ppb=None,flow=p['specs']['Durchfluss'],power=p['specs']['Max. Leistungsaufnahme'],image=p['image'],url='products/'+p['slug'])
    line=js(record)
    pattern=r'^\{[^\n]*"id": "'+re.escape(p['id'])+r'"[^\n]*\},?[ \t]*\n?'
    app=re.sub(pattern,'',app,flags=re.M)
    app=app.replace('const products=[','const products=[\n'+line+',',1)
write('assets/app.js',app)

sitemap=read('sitemap.xml'); url='https://wasser.market/products/osmofresh-fusion-pro-2'
if f'<loc>{url}</loc>' not in sitemap:sitemap=sitemap.replace('</urlset>',f'<url><loc>{url}</loc></url>\n</urlset>')
write('sitemap.xml',sitemap)
index=read('index.html');index=re.sub(r'(<b id="overviewProducts">)\d+(</b>)',rf'\g<1>{len(products)}\2',index);write('index.html',index)
print(json.dumps({'batch':batch['batch'],'targets':list(EXPECTED.values()),'catalog_count':len(products),'other_products_unchanged':True}))
