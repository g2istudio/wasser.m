import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const products = JSON.parse(fs.readFileSync(path.join(root,'data/products.json'),'utf8'));
const file = path.join(root,'products.html');
let html = fs.readFileSync(file,'utf8');
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const price = product => product.price == null ? 'Preis auf Anfrage' : new Intl.NumberFormat('de-DE',{style:'currency',currency:product.currency||'EUR',maximumFractionDigits:0}).format(product.price);
const specLines = product => Object.entries(product.specs||{}).slice(0,3).map(([key,value])=>`<span>${esc(key.replaceAll('_',' '))}: ${esc(value)}</span>`).join('');
const cards = products.map(product=>`<div class="product-card" data-product-id="${esc(product.id)}"><a class="photo" href="products/${esc(product.slug)}.html" aria-label="${esc(product.brand)} ${esc(product.name)} ansehen"><img alt="${esc(product.brand)} ${esc(product.name)}" src="${esc(product.image)}" loading="lazy" decoding="async"></a><div class="brand">${esc(product.brand)}</div><h3>${esc(product.name)}</h3><div class="rating">${product.rating ? `★ ${esc(product.rating)} (${esc(product.reviews||0)} Bewertungen)` : 'Herstellerdaten'}</div><div class="price">${esc(price(product))}</div><div class="specs">${specLines(product)}</div><div class="actions"><a class="btn small" href="products/${esc(product.slug)}.html">Alle Daten</a><button class="btn small" data-compare="${esc(product.id)}">+ Compare</button></div></div>`).join('\n');

const gridStart = html.indexOf('<div class="product-grid"', html.indexOf('id="productResultText"'));
const additionsStart = html.indexOf('<div class="container"><section class="section" id="catalogAdditions">');
if(gridStart < 0) throw new Error('Product grid marker was not found');
if(additionsStart >= 0){
  const additionsEnd = html.indexOf('</section></div></main>', additionsStart);
  if(additionsEnd < 0) throw new Error('Additional catalog closing marker was not found');
  html = html.slice(0,gridStart) + `<div class="product-grid" id="productCatalogGrid">\n${cards}\n</div></section></div></div>` + html.slice(additionsEnd + '</section></div>'.length);
}else{
  const catalogEndMarker = '</div></section></div></div></main>';
  const catalogEnd = html.indexOf(catalogEndMarker,gridStart);
  if(catalogEnd < 0) throw new Error('Catalog closing marker was not found');
  html = html.slice(0,gridStart) + `<div class="product-grid" id="productCatalogGrid">\n${cards}\n</div></section></div></div>` + html.slice(catalogEnd + '</div></section></div></div>'.length);
}

const categories = [...new Set(products.map(product=>product.category).filter(Boolean))];
const options = ['<option data-de="Alle Kategorien" data-en="All categories" value="">Alle Kategorien</option>',...categories.map(category=>`<option value="${esc(category)}">${esc(category)}</option>`)].join('\n');
html = html.replace(/<select id="filterCategory">[\s\S]*?<\/select>/,`<select id="filterCategory">\n${options}\n</select>`);
html = html.replace(/<h2 id="productResultCount">[^<]*<\/h2>/,`<h2 id="productResultCount">${products.length} Modelle</h2>`);
html = html.replace(/<p id="productResultText">[^<]*<\/p>/,`<p id="productResultText">${products.length} Produkte in der Datenbank</p>`);
fs.writeFileSync(file,html);
