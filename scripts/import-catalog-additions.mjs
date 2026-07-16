import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const additions = JSON.parse(fs.readFileSync(path.join(root, 'data/catalog-additions.json'), 'utf8'));
const brandsPath = path.join(root, 'data/brands.json');
const productsPath = path.join(root, 'data/products.json');
const brands = JSON.parse(fs.readFileSync(brandsPath, 'utf8'));
const products = JSON.parse(fs.readFileSync(productsPath, 'utf8'));

const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const priceText = value => value == null ? 'Preis auf Anfrage' : new Intl.NumberFormat('de-DE',{style:'currency',currency:'EUR',maximumFractionDigits:0}).format(value);

for (const brand of additions.brands) {
  if (!brands.some(item => item.slug === brand.slug)) {
    const count = additions.products.filter(product => product.brandSlug === brand.slug).length;
    const ext = brand.slug === 'wasserwelt' ? 'svg' : 'png';
    brands.push({...brand, founded:null, description_de:brand.description, description_en:brand.description, products_count:count, rating:null, logo:`assets/brands/${brand.slug}.${ext}`});
  }
}

for (const product of additions.products) {
  if (!products.some(item => item.slug === product.slug)) {
    products.push({id:product.slug, slug:product.slug, brand:product.brand, name:product.name, category:product.category, price:product.price, currency:'EUR', rating:null, reviews:0, image:product.image, featured:false, specs:Object.fromEntries(product.specs.map(([key,value]) => [key,value])), source:product.source});
  }
}

for (const brand of brands) {
  const added = additions.products.filter(product => product.brandSlug === brand.slug).length;
  if (added && !additions.brands.some(item => item.slug === brand.slug)) brand.products_count = (brand.products_count || 0) + added;
}

fs.writeFileSync(brandsPath, JSON.stringify(brands,null,2)+'\n');
fs.writeFileSync(productsPath, JSON.stringify(products,null,2)+'\n');

const header = (depth='..') => `<div class="topbar"><div class="container"><span>Independent water technology database</span><span>Reviews · Comparisons · Laboratory data</span></div></div><header class="site-header"><div class="header-shell container"><a class="site-brand" href="${depth}/index.html"><img alt="WASSER.MARKET" src="${depth}/assets/img/wasser-market-logo.jpg"></a><nav class="desktop-nav"><a href="${depth}/products.html">Produkte</a><a href="${depth}/brands.html">Marken</a><a href="${depth}/compare.html">Vergleichen</a><a href="${depth}/community.html">Community</a><a href="${depth}/knowledge.html">Wissen</a></nav></div></header>`;
const footer = depth => `<footer class="site-footer"><div class="footer-bottom"><div class="container"><span>© WASSER.MARKET</span><span>Unabhängige Datenbank für Wassertechnologie</span></div></div></footer><script src="${depth}/assets/i18n.js"></script><script src="${depth}/assets/app.js"></script>`;

const productCard = (product, depth='') => `<div class="product-card" data-product-id="${esc(product.slug)}"><div class="photo"><img alt="${esc(product.brand)} ${esc(product.name)}" src="${depth}${esc(product.image)}"></div><div class="brand">${esc(product.brand)}</div><h3>${esc(product.name)}</h3><div class="rating">Herstellerdaten</div><div class="price">${esc(priceText(product.price))}</div><div class="specs">${product.specs.slice(0,3).map(([key,value])=>`<span>${esc(key)}: ${esc(value)}</span>`).join('')}</div><div class="actions"><a class="btn small" href="${depth}products/${esc(product.slug)}.html">Alle Daten</a><button class="btn small" data-compare="${esc(product.slug)}">+ Compare</button></div></div>`;

for (const brand of additions.brands) {
  const logoExt = brand.slug === 'wasserwelt' ? 'svg' : 'png';
  const items = additions.products.filter(product => product.brandSlug === brand.slug);
  const website = brand.website ? `<a class="btn primary" href="${esc(brand.website)}" target="_blank" rel="noopener nofollow">Offizielle Website ↗</a>` : '<span class="meta">Offizielle Website nicht bestätigt</span>';
  const html = `<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(brand.name)} – Marke und Produkte</title><meta name="description" content="${esc(brand.description)}"><link rel="stylesheet" href="../assets/styles.css"><link rel="icon" href="../assets/favicon/favicon.ico"><link rel="canonical" href="https://hitmoda.ru/brands/${esc(brand.slug)}.html"></head><body class="wm-v2">${header()}<main><div class="container"><div class="breadcrumbs">Home / Marken / ${esc(brand.name)}</div><section class="brand-hero"><div class="brand-hero-primary"><div class="brand-hero-logo"><img src="../assets/brands/${esc(brand.slug)}.${logoExt}" alt="${esc(brand.name)} Logo"></div><div class="brand-hero-copy"><span class="badge">${esc(brand.group)}</span><h1>${esc(brand.name)}</h1><p class="lead">${esc(brand.description)}</p></div></div><aside class="brand-hero-details"><h2>Markenprofil</h2><dl><div><dt>Land</dt><dd>${esc(brand.country)}</dd></div><div><dt>Bereich</dt><dd>${esc(brand.group)}</dd></div><div><dt>Modelle</dt><dd>${items.length}</dd></div></dl>${website}</aside></section><section class="panel"><h2>Produkte in der Datenbank</h2><div class="product-grid">${items.map(item=>productCard(item,'../')).join('')}</div></section></div></main>${footer('..')}</body></html>`;
  fs.writeFileSync(path.join(root,'brands',`${brand.slug}.html`),html+'\n');
}

for (const product of additions.products) {
  const price = priceText(product.price);
  const source = product.source ? `<a class="btn primary" href="${esc(product.source)}" target="_blank" rel="nofollow noopener">Datenquelle / Hersteller ↗</a>` : '<span class="meta">Keine öffentlich indexierte Herstellerseite gefunden.</span>';
  const schema = {"@context":"https://schema.org","@type":"Product",name:`${product.brand} ${product.name}`,brand:{"@type":"Brand",name:product.brand},category:product.category,description:product.summary};
  if (product.price != null) schema.offers={"@type":"Offer",priceCurrency:'EUR',price:String(product.price),url:product.source};
  const html = `<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(product.brand)} ${esc(product.name)} – Daten & Eigenschaften</title><meta name="description" content="${esc(product.summary)}"><link rel="stylesheet" href="../assets/styles.css"><link rel="icon" href="../assets/favicon/favicon.ico"><link rel="canonical" href="https://hitmoda.ru/products/${esc(product.slug)}.html"><script type="application/ld+json">${JSON.stringify(schema)}</script></head><body class="wm-v2">${header()}<main><div class="container"><div class="breadcrumbs">Home / Produkte / ${esc(product.brand)} ${esc(product.name)}</div><section class="device-layout"><div class="device-photo"><img alt="${esc(product.brand)} ${esc(product.name)}" src="../${esc(product.image)}"></div><div class="device-info"><span class="badge">${esc(product.category)}</span><h1>${esc(product.brand)} ${esc(product.name)}</h1><p class="lead">${esc(product.summary)}</p><div class="price">${esc(price)}</div><p>${source}</p></div></section><div class="content-grid"><section class="panel"><h2>Technische Daten</h2><table class="spec-table">${product.specs.map(([key,value])=>`<tr><td>${esc(key)}</td><td>${esc(value)}</td></tr>`).join('')}</table><h2>Datenhinweis</h2><p>Die Angaben stammen aus öffentlich zugänglichen Hersteller- und Produktunterlagen. Nicht veröffentlichte Werte wurden nicht geschätzt. Änderungen und Modellvarianten sind möglich.</p></section><aside><div class="panel"><h3 style="margin-top:0">Einordnung</h3><table class="spec-table"><tr><td>Marke</td><td><a href="../brands/${esc(product.brandSlug)}.html">${esc(product.brand)}</a></td></tr><tr><td>Kategorie</td><td>${esc(product.category)}</td></tr><tr><td>Preisstatus</td><td>${product.price == null ? 'Nicht veröffentlicht' : 'Hersteller-/Shoppreis bei Recherche'}</td></tr></table></div></aside></div></div></main>${footer('..')}</body></html>`;
  fs.writeFileSync(path.join(root,'products',`${product.slug}.html`),html+'\n');
}

let brandsHtml = fs.readFileSync(path.join(root,'brands.html'),'utf8');
const newBrandCards = additions.brands.filter(brand => !brandsHtml.includes(`href="brands/${brand.slug}.html"`)).map(brand => {
  const ext = brand.slug === 'wasserwelt' ? 'svg' : 'png';
  return `<a class="brand-directory-card" href="brands/${esc(brand.slug)}.html" data-brand-name="${esc(brand.name.toLowerCase())}" data-brand-country="${esc(brand.country.toLowerCase())}"><div class="brand-logo-wrap"><img src="assets/brands/${esc(brand.slug)}.${ext}" alt="${esc(brand.name)} Logo" loading="lazy"></div><div class="brand-card-body"><span class="badge">${esc(brand.group)}</span><h3>${esc(brand.name)}</h3><p>${esc(brand.description)}</p><span class="brand-meta">${esc(brand.country)} · ${additions.products.filter(product=>product.brandSlug===brand.slug).length} Modelle</span><span class="brand-link">Profil ansehen →</span></div></a>`;
}).join('\n');
brandsHtml = brandsHtml.replace('</div>\n<div class="panel brand-empty"',`${newBrandCards}</div>\n<div class="panel brand-empty"`);
fs.writeFileSync(path.join(root,'brands.html'),brandsHtml);

let app = fs.readFileSync(path.join(root,'assets/app.js'),'utf8');
const appItems = additions.products.filter(product=>!app.includes(`id:'${product.slug}'`)).map(product=>`{id:'${product.slug}',brand:${JSON.stringify(product.brand)},name:${JSON.stringify(product.name)},cat:${JSON.stringify(product.category)},price:${JSON.stringify(priceText(product.price))},priceValue:${product.price ?? 'null'},features:[],ppb:null,flow:'Not published',maint:'Not published',liter:'—',membrane:${JSON.stringify(product.specs.find(([key])=>/Membran/.test(key))?.[1] || 'Not published')},pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:'Not published',warranty:'Not published',country:'Germany',image:${JSON.stringify(product.image)},url:'products/${product.slug}.html'}`).join(',\n');
app = app.replace('\n];',`,\n${appItems}\n];`);
fs.writeFileSync(path.join(root,'assets/app.js'),app);
await import('./rebuild-products-page.mjs');
