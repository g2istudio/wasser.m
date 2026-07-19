const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..'),dir=path.join(root,'brands');
const topbar=`<div class="topbar"><div class="container"><span>Unabhängige Datenbank für Wassertechnologie</span><span>Erfahrungen · Vergleiche · Labordaten</span></div></div>`;
const header=`<header class="site-header"><div class="header-shell container"><a aria-label="WASSER.MARKET Startseite" class="site-brand" href="../index.html"><img alt="WASSER.MARKET – Datenbank für Wassertechnologie" src="../assets/img/wasser-market-logo.jpg" loading="eager" decoding="async"></a><nav aria-label="Hauptnavigation" class="desktop-nav"><a href="../products.html">Produkte</a><a aria-current="page" href="../brands.html">Marken</a><a href="../compare.html">Vergleichen</a><a href="../community.html">Community</a><div class="nav-more"><button aria-expanded="false" class="nav-more-btn" type="button">Wissen</button><div class="nav-more-menu"><a href="../knowledge.html">Wasserwissen</a><a href="../technologies.html">Technologien</a><a href="../articles/reverse-osmosis.html">Ratgeber</a></div></div></nav><div class="header-tools"><a aria-label="Suche" class="icon-btn header-search-link" href="../index.html#site-search">⌕</a><div aria-label="Sprachauswahl" class="lang-switch compact"><button data-lang="de" type="button">DE</button><button data-lang="en" type="button">EN</button></div><a class="btn primary compact-compare" href="../compare.html">⇄ <span>Vergleichen</span></a><button aria-expanded="false" aria-label="Menü öffnen" class="icon-btn mobile-menu-btn" type="button">☰</button></div></div><div aria-hidden="true" class="mobile-nav-panel"><div class="container mobile-nav-inner"><a href="../products.html">Produkte</a><a href="../brands.html">Marken</a><a href="../compare.html">Vergleichen</a><a href="../community.html">Community</a><a href="../professionals.html">Profis</a><a href="../knowledge.html">Wasserwissen</a><a href="../technologies.html">Technologien</a></div></div></header>`;
let changed=0;
for(const name of fs.readdirSync(dir).filter(name=>name.endsWith('.html'))){
 const file=path.join(dir,name);let html=fs.readFileSync(file,'utf8'),before=html;
 html=html.replace(/<div class="topbar">[\s\S]*?<\/div><\/div>(?=<header class="site-header">)/,topbar);
 html=html.replace(/<header class="site-header">[\s\S]*?<\/header>/,header);
 html=html.replace(/app\.js\?v=[^"]+/g,'app.js?v=20260718-menu1');
 if(html!==before){fs.writeFileSync(file,html);changed++}
}
console.log(`Standardized ${changed} brand page headers.`);
