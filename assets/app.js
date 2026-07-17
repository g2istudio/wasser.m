const products=[
{id:'biella',brand:'WERTACH',name:'Biella',cat:'Countertop RO',price:'from €1,994',priceValue:1994,features:['remineralization','display','cooling','instant-heater'],ppb:null,flow:'0.34 L/min',maint:'Filter-dependent',liter:'—',membrane:'100 GPD Filmtec® RO',pfas:'Manufacturer claim',viruses:'RO + UV protection',bacteria:'4-fold; 5-fold Medical',nitrates:'RO filtration',lead:'RO filtration',arsenic:'RO filtration',micro:'RO filtration',tds:'Real-time display',remin:'Yes',noise:'Not specified',power:'2,093 W max.',warranty:'5 years',country:'Germany',image:'assets/img/wertach-biella.webp',url:'products/wertach-biella.html'},
{id:'pearl',brand:'BLACKWATER',name:'Pearl',cat:'Countertop RO',price:'€1,497',priceValue:1497,features:['remineralization','display','cooling','instant-heater'],ppb:null,flow:'0.34 L/min',maint:'Filter-dependent',liter:'—',membrane:'100 GPD Filmtec® RO',pfas:'RO filtration',viruses:'RO + dual UV',bacteria:'3-fold protection',nitrates:'RO filtration',lead:'RO filtration',arsenic:'RO filtration',micro:'0.0001 µm membrane',tds:'Input display',remin:'Yes',noise:'Not specified',power:'2,150 W max.',warranty:'Not specified',country:'Germany',image:'assets/img/blackwater-pearl.jpg',url:'products/blackwater-pearl.html'},
{id:'dwm',brand:'Aquaphor',name:'DWM-202S Pro',cat:'Under Sink RO',price:'€699',priceValue:699,features:['remineralization','pump'],ppb:null,flow:'15 L/h',maint:'€130/year',liter:'€0.10',membrane:'100 GPD',pfas:'Claimed',viruses:'99%',bacteria:'99.9%',nitrates:'90%',lead:'98%',arsenic:'90%',micro:'99%',tds:'15–50 ppm',remin:'Yes',noise:'42 dB',power:'55 W',warranty:'2 years',country:'Estonia',image:'assets/img/device-ro.svg',url:'products/blackwater-pearl.html'},
{id:'spirit',brand:"Bluewater",name:"Spirit 300CP",cat:"Under Sink RO",price:"€1,910",priceValue:1910,features:[],ppb:null,flow:"bis 99–99,7 % laut Händlerseite",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Nein",noise:'Not published',power:"350 W / 6 A",warranty:"1 Jahr",country:"Sweden",image:"assets/products/bluewater-spirit-300cp.jpg",url:'products/bluewater-spirit-300.html'},
{id:'hydro',brand:'WALUTEC',name:'H2 Bottle Pro',cat:'Hydrogen Bottles',price:'€199',priceValue:199,features:['pem-spe','usb-c','display','self-cleaning'],ppb:3000,flow:'260 ml',maint:'€0/year',liter:'—',membrane:'PEM/SPE',pfas:'No',viruses:'No',bacteria:'No',nitrates:'No',lead:'No',arsenic:'No',micro:'No',tds:'Unchanged',remin:'No',noise:'Silent',power:'USB-C',warranty:'2 years',country:'Germany',image:'assets/img/bottle.svg',url:'products/blackwater-pearl.html'},
{id:'truu-fountain-3',brand:"truu",name:"fountain 3",cat:"Commercial Water System",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:"Not published",image:"assets/products/truu-fountain-3.png",url:'products/truu-fountain-3.html'},
{id:'mrwater-premium-ro',brand:"misterwater®",name:"Wasserfilteranlagen (Puria / Arctica / Silver Star / Futura)",cat:"Reverse Osmosis",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:"Not published",image:"assets/products/mrwater-premium-ro.png",url:'products/mrwater-premium-ro.html'},
{id:'wertach-pantera',brand:"WERTACH",name:"Pantera",cat:"Direct Flow RO",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"WERTGARANTIE laut Hersteller",country:"Not published",image:"assets/products/wertach-pantera.webp",url:'products/wertach-pantera.html'},
{id:'osmofresh-fusion-pro',brand:"OsmoFresh",name:"Fusion Pro",cat:"Countertop RO",price:"1.290 €",priceValue:1290,features:[],ppb:null,flow:"120 W",maint:"Alle 12 Monate",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"ca. 2,6 W Standby; bis 2.400 W Betrieb",warranty:"Not published",country:"Not published",image:"assets/products/osmofresh-fusion-pro.webp",url:'products/osmofresh-fusion-pro.html'},
{id:'greifenstein-direct-flow-premium',brand:"Greifenstein Wasserveredelung",name:"INOX",cat:"Direct Flow RO",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"TFC, 0,0001 Mikron",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"2 Jahre; Verlängerung unter Herstellerbedingungen",country:"Not published",image:"assets/products/greifenstein-inox.jpg",url:'products/greifenstein-direct-flow-premium.html'},
{id:'gewapur-ro-comfort-direct-flow',brand:"Gewapur",name:"Osmo Star 2.0",cat:"Direct Flow RO",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Not published",maint:"Schnellwechselsystem",liter:'—',membrane:"800 GPD",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:"Not published",image:"assets/products/gewapur-osmo-star-2.webp",url:'products/gewapur-ro-comfort-direct-flow.html'},
{id:'aqmos-aq-ro-800-gpd',brand:"Aqmos",name:"AQ-RO 800 GPD",cat:"Direct Flow RO",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"800 GPD",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:"Not published",image:"assets/brands/aqmos.png",url:'products/aqmos-aq-ro-800-gpd.html'},
{id:'wasserhaus-zen-flow',brand:"Wasserhaus",name:"ZEN FLOW",cat:"Direct Flow RO",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"bis ca. 2,1 L/min unter optimalen Bedingungen",maint:"Not published",liter:'—',membrane:"800 GPD",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Magnesium, Kalium und Calcium",noise:'Not published',power:"Not published",warranty:"Not published",country:"Not published",image:"assets/products/wasserhaus-zen-flow.jpg",url:'products/wasserhaus-zen-flow.html'},
{id:'arktisquelle-direct-flow-premium',brand:"Arktisquelle",name:"Direct Flow Premium",cat:"Countertop RO",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:"Not published",image:"assets/products/arktisquelle-direct-flow-premium.png",url:'products/arktisquelle-direct-flow-premium.html'},
{id:'myaqua-1900',brand:"myAqua",name:"myAQUA 1900",cat:"Aquarium RO",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"bis 1.900 Liter",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"70 W; Standby 1–2 W",warranty:"Not published",country:"Not published",image:"assets/products/myaqua-1900.jpg",url:'products/myaqua-1900.html'},
{id:'purway-pur-booster-quick',brand:"Purway",name:"PUR Booster Quick",cat:"Direct Flow RO",price:"309 €",priceValue:309,features:[],ppb:null,flow:"bis ca. 1,1 L/min",maint:"Twist-Change-System",liter:'—',membrane:"400 GPD",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:"Not published",image:"assets/products/purway-pur-booster-quick.jpg",url:'products/purway-pur-booster-quick.html'},
{id:'osmounity-direct-flow',brand:"Osmounity",name:"Direct Flow",cat:"Direct Flow RO",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Variantenabhängig",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:"Not published",image:"assets/products/osmounity-direct-flow.jpg",url:'products/osmounity-direct-flow.html'},
{id:'wasserwelt-ww-premium-direct-flow',brand:"WasserWelt",name:"WW Premium Direct Flow",cat:"Direct Flow RO",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:"Not published",image:"assets/brands/wasserwelt.svg",url:'products/wasserwelt-ww-premium-direct-flow.html'},
{id:'bwt-aqa-drink-pro-20',brand:"BWT",name:"AQA drink PRO 20",cat:"Water Dispenser",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:"Not published",image:"assets/products/bwt-aqa-drink-pro-20.png",url:'products/bwt-aqa-drink-pro-20.html'},
{id:'bwt-bestaqua-roc',brand:"BWT",name:"bestaqua ROC",cat:"Commercial RO",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Modellabhängig, bis 180 L/h dokumentiert",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:"Not published",image:"assets/products/bwt-bestaqua-roc.png",url:'products/bwt-bestaqua-roc.html'},
{id:'gruenbeck-geno-osmo-x',brand:"Grünbeck",name:"GENO-OSMO-X",cat:"Industrial RO",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:"Not published",image:"assets/products/gruenbeck-geno-osmo-x.png",url:'products/gruenbeck-geno-osmo-x.html'},
{id:'judo-i-fill',brand:"JUDO",name:"i-fill",cat:"Heating Water Filling",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:"Not published",image:"assets/brands/judo.png",url:'products/judo-i-fill.html'},
{id:'alfiltra-ro-professional',brand:"Alfiltra",name:"RO Professional",cat:"Commercial RO",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:"Not published",image:"assets/products/alfiltra-ro-professional.jpg",url:'products/alfiltra-ro-professional.html'},
{id:'aquion-premium-7',brand:"AQUION",name:"Premium 7",cat:"Water Ionizer",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:"Not published",image:"assets/products/aquion-premium-7.jpg",url:'products/aquion-premium-7.html'},
{id:'quooker-front-cube',brand:"Quooker",name:"Front + CUBE",cat:"Kitchen Water System",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:"Not published",image:"assets/products/quooker-front-cube.webp",url:'products/quooker-front-cube.html'},
{id:'brita-mypure-p1',brand:"BRITA",name:"mypure P1",cat:"Under Sink Filter",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Not published",maint:"Abhängig von Wasserhärte und Verbrauch",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:"Not published",image:"assets/products/brita-mypure-p1.jpg",url:'products/brita-mypure-p1.html'},
{id:'grohe-blue-home',brand:"GROHE Blue",name:"GROHE Blue Home",cat:"Kitchen Water System",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:"Not published",image:"assets/brands/grohe-blue.png",url:'products/grohe-blue-home.html'},
{id:'franke-mythos-water-hub',brand:"Franke",name:"Mythos Water Hub",cat:"Kitchen Water System",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:"Not published",image:"assets/products/franke-mythos-water-hub.jpg",url:'products/franke-mythos-water-hub.html'},
{id:'blanco-unit-drink-systems',brand:"BLANCO",name:"BLANCO UNIT / DRINK.SYSTEMS",cat:"Kitchen Water System",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:"Not published",image:"assets/products/blanco-unit-drink-systems.webp",url:'products/blanco-unit-drink-systems.html'},
{id:'aqua-global-flexible-touch',brand:"Aqua Global",name:"Flexible Touch",cat:"Countertop RO",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"ca. 10–15 L/h",maint:"Composite/Nachfilter 6–12 Monate; Membran 12–24 Monate; UV-Lampe 60 Monate",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"2.180 W",warranty:"Not published",country:"Not published",image:"assets/brands/aqua-global.svg",url:'products/aqua-global-flexible-touch.html'},
{id:'bela-aqua-oblige-directflow',brand:"Bela Aqua",name:"OBLIGE Directflow",cat:"Direct Flow RO",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"bis zu 2,1 L/min",maint:"Not published",liter:'—',membrane:"800 GPD High Performance RO",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Optionaler BIO-3+-Filter bei OBLIGE MINERALE",noise:'Not published',power:"Not published",warranty:"Not published",country:"Not published",image:"assets/products/bela-aqua-oblige-directflow.jpg",url:'products/bela-aqua-oblige-directflow.html'},
{id:'aquapro-high-flow-800-gpd',brand:"AQUAPRO",name:"High Flow 800 GPD Reverse Osmosis System",cat:"Commercial RO",price:"€907",priceValue:907,features:[],ppb:null,flow:'Not published',maint:'Not published',liter:'—',membrane:"0,0001 Mikron",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:'Not published',warranty:'Not published',country:"United Arab Emirates",image:"assets/products/aquapro-high-flow-800-gpd.jpg",url:'products/aquapro-high-flow-800-gpd.html'},
{id:"culligan-c2-firewall-ro",brand:"Culligan",name:"C2 Firewall® RO Water Dispenser",cat:"Mains-Fed Water Cooler",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Not published",maint:'Not published',liter:'—',membrane:"Direct-Flow-Umkehrosmose",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:"United States",image:"assets/products/culligan-c2-firewall-ro.webp",url:"products/culligan-c2-firewall-ro.html"},
{id:"blackwater-drop",brand:"BLACKWATER",name:"Drop",cat:"Direct Flow RO",price:"1.490 €",priceValue:1490,features:[],ppb:null,flow:"bis 2,2 L/min",maint:'Not published',liter:'—',membrane:"Hochleistungs-RO-Kompakteinheit, 800 GPD",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"1,4 W Standby; 84 W Betrieb",warranty:"2 Jahre",country:"Germany",image:"assets/products/blackwater-drop.png",url:"products/blackwater-drop.html"},
{id:"walutec-el-nero-smart-medic-s",brand:"WALUTEC",name:"eL-Neró® smart + medic S",cat:"Countertop RO",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"ca. 0,13 L/min",maint:'Not published',liter:'—',membrane:"FILMTEC® TFC, 100 GPD, 0,0001 µm",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Alkaline pH+; pH-Stabilisierung",noise:'Not published',power:"1,5 W Standby; 38 W Produktion; 65 W Kühlung; 2.000 W Heizung",warranty:"3 Jahre; unter Herstellerbedingungen bis 10 Jahre verlängerbar",country:"Germany",image:"assets/products/walutec-el-nero-smart.png",url:"products/walutec-el-nero-smart-medic-s.html"},
{id:"walutec-el-nero-speedflow-medic-s",brand:"WALUTEC",name:"eL-Neró® speedflow medic S",cat:"Direct Flow RO",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"ca. 1,7 L/min",maint:'Not published',liter:'—',membrane:"700 GPD Hochleistungsmembran",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Ca, Mg, K und Na; pH-Stabilisierung",noise:'Not published',power:"1,4 W Standby; 84 W Produktion",warranty:"36 Monate; unter Herstellerbedingungen bis 10 Jahre verlängerbar",country:"Germany",image:"assets/products/walutec-el-nero-speedflow-medic-s.jpg",url:"products/walutec-el-nero-speedflow-medic-s.html"}
];

function storageGet(key,fallback){try{const v=localStorage.getItem(key);return v===null?fallback:v}catch(e){return fallback}}
function storageSet(key,value){try{localStorage.setItem(key,value)}catch(e){}}
let selected=[];
try{selected=JSON.parse(storageGet('wasserCompare','[]'))||[]}catch(e){selected=[]}
const lang=()=>storageGet('wasserLang','de');
const tr=(de,en)=>lang()==='de'?de:en;
function basePrefix(){return /\/(products|brands|articles)\//.test(location.pathname)?'../':''}
function save(){storageSet('wasserCompare',JSON.stringify(selected));renderDock()}
function addCompare(id){if(selected.includes(id)){selected=selected.filter(x=>x!==id)}else{if(selected.length>=3){alert(tr('Es können maximal 3 Geräte verglichen werden','You can compare a maximum of 3 devices'));return}selected.push(id)}save()}
function renderDock(){const dock=document.querySelector('.compare-dock');if(!dock)return;if(!selected.length){dock.classList.remove('show');return}dock.classList.add('show');dock.querySelector('.compare-items').innerHTML=selected.map(id=>{const p=products.find(x=>x.id===id);return p?`<div class="compare-mini">${p.brand} ${p.name}</div>`:''}).join('');dock.querySelector('.count').textContent=`${selected.length}/3`}
function goCompare(){location.href=basePrefix()+'compare.html'}
function productMatches(q){q=(q||'').trim().toLowerCase();if(!q)return products;return products.filter(p=>`${p.brand} ${p.name} ${p.cat}`.toLowerCase().includes(q)).slice(0,8)}
function suggestionHTML(p){return `<div class="autocomplete-item" role="option" tabindex="0" data-id="${p.id}"><img src="${basePrefix()}${p.image}" alt=""><div><b>${p.brand} ${p.name}</b><span>${p.cat} · ${p.price}</span></div></div>`}
function navigateToProduct(p){if(p) location.href=basePrefix()+p.url}

function setupGeneralAutocomplete(){
  document.querySelectorAll('.product-search:not(.compare-search)').forEach(input=>{
    if(input.dataset.searchReady==='1')return;
    input.dataset.searchReady='1';
    const parent=input.closest('.searchbar')||input.parentElement;
    let box=parent.querySelector('.autocomplete-results');
    if(!box){box=document.createElement('div');box.className='autocomplete-results';box.setAttribute('role','listbox');parent.appendChild(box)}
    const button=parent.querySelector('button');
    let currentMatches=[];
    function draw(force=false){
      const q=input.value.trim();
      currentMatches=productMatches(q);
      box.innerHTML=currentMatches.length?currentMatches.map(suggestionHTML).join(''):`<div class="search-no-results">${tr('Keine passenden Produkte gefunden','No matching products found')}</div>`;
      box.classList.toggle('show',force||q.length>0);
      box.querySelectorAll('.autocomplete-item').forEach(el=>{
        const choose=()=>navigateToProduct(products.find(x=>x.id===el.dataset.id));
        el.addEventListener('click',choose);
        el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();choose()}});
      });
    }
    function submit(){
      const q=input.value.trim();
      const exact=productMatches(q)[0];
      if(exact){navigateToProduct(exact);return}
      if(q) location.href=basePrefix()+'products.html?q='+encodeURIComponent(q);
      else draw(true);
    }
    input.addEventListener('input',()=>draw(false));
    input.addEventListener('focus',()=>{if(input.value.trim())draw(false)});
    input.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();submit()}else if(e.key==='Escape'){box.classList.remove('show')}});
    if(button)button.addEventListener('click',e=>{e.preventDefault();submit()});
    document.addEventListener('click',e=>{if(!parent.contains(e.target))box.classList.remove('show')});
  });
}

function setupBrandSearch(){
  const page=document.querySelector('input[placeholder="Search manufacturer"],input[placeholder="Hersteller suchen"]');
  if(!page)return;
  const grid=page.closest('.container')?.querySelector('.article-grid');
  if(!grid)return;
  const cards=[...grid.querySelectorAll('.article-card')];
  const button=page.closest('.searchbar')?.querySelector('button');
  function filter(){
    const q=page.value.trim().toLowerCase();
    let visible=0;
    cards.forEach(card=>{const match=!q||card.textContent.toLowerCase().includes(q);card.style.display=match?'':'none';if(match)visible++});
    let empty=grid.parentElement.querySelector('.brand-search-empty');
    if(!empty){empty=document.createElement('div');empty.className='brand-search-empty panel';empty.style.display='none';grid.after(empty)}
    empty.textContent=tr('Keine passende Marke gefunden.','No matching brand found.');
    empty.style.display=visible?'none':'block';
  }
  page.classList.remove('product-search');
  page.addEventListener('input',filter);
  page.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();filter()}});
  if(button)button.addEventListener('click',e=>{e.preventDefault();filter()});
}

function setupProductsQueryFilter(){
  if(!/products\.html$/.test(location.pathname))return;
  const q=new URLSearchParams(location.search).get('q');
  if(!q)return;
  const cards=[...document.querySelectorAll('.product-card')];
  cards.forEach(card=>{card.style.display=card.textContent.toLowerCase().includes(q.toLowerCase())?'':'none'});
}

function initComparePage(){
  const slots=[0,1,2].map(i=>document.getElementById('slot'+i));if(!slots[0])return;

  const syncClearButton=input=>{
    const clear=input.parentElement.querySelector('.search-clear-btn');
    if(!clear)return;
    const hasValue=input.value.trim().length>0;
    clear.classList.toggle('show',hasValue);
    clear.tabIndex=hasValue?0:-1;
    clear.setAttribute('aria-hidden',hasValue?'false':'true');
  };

  const refreshSlotValues=()=>{
    slots.forEach((slot,index)=>{
      const product=products.find(p=>p.id===selected[index]);
      slot.value=product?`${product.brand} ${product.name}`:'';
      syncClearButton(slot);
    });
  };

  slots.forEach((input,i)=>{
    const box=input.parentElement.querySelector('.autocomplete-results');
    const current=products.find(p=>p.id===selected[i]);
    if(current)input.value=`${current.brand} ${current.name}`;
    syncClearButton(input);

    function draw(){
      const matches=productMatches(input.value);
      box.innerHTML=matches.length?matches.map(suggestionHTML).join(''):`<div class="search-no-results">${tr('Keine passenden Produkte gefunden','No matching products found')}</div>`;
      box.classList.add('show');
      box.querySelectorAll('.autocomplete-item').forEach(el=>el.onclick=()=>{
        const id=el.dataset.id;
        if(selected.includes(id)&&selected[i]!==id)return;
        selected[i]=id;
        selected=selected.filter(Boolean).slice(0,3);
        save();
        refreshSlotValues();
        box.classList.remove('show');
        renderCompareTable();
      });
    }

    input.addEventListener('input',()=>{
      if(!input.value.trim()&&selected[i]){
        selected.splice(i,1);
        save();
        refreshSlotValues();
        renderCompareTable();
        box.classList.remove('show');
        return;
      }
      syncClearButton(input);
      draw();
    });
    input.addEventListener('focus',draw);
    input.addEventListener('keydown',e=>{if(e.key==='Escape')box.classList.remove('show')});
  });

  document.addEventListener('click',e=>{
    document.querySelectorAll('.compare-slot .autocomplete-results').forEach(box=>{
      if(!box.parentElement.contains(e.target))box.classList.remove('show');
    });
  });
  refreshSlotValues();
  renderCompareTable();
}
function renderCompareTable(){const table=document.getElementById('comparison');if(!table)return;const ps=selected.map(id=>products.find(p=>p.id===id)).filter(Boolean);if(ps.length<2){table.innerHTML=`<div style="padding:25px">${tr('Fügen Sie mindestens zwei Geräte zum Vergleich hinzu.','Add at least two products to compare.')}</div>`;return}const rows=[[tr('Allgemein','General'),null],[tr('Kategorie','Category'),'cat'],[tr('Preis','Price'),'price'],[tr('Markenland','Brand country'),'country'],[tr('Leistung','Performance'),null],[tr('Durchfluss','Flow rate'),'flow'],[tr('Jährliche Wartung','Annual maintenance'),'maint'],[tr('Kosten pro Liter','Cost per liter'),'liter'],[tr('Membran','Membrane'),'membrane'],[tr('Filtration','Filtration'),null],['PFAS','pfas'],[tr('Viren','Viruses'),'viruses'],[tr('Bakterien','Bacteria'),'bacteria'],[tr('Nitrate','Nitrates'),'nitrates'],[tr('Blei','Lead'),'lead'],[tr('Arsen','Arsenic'),'arsenic'],[tr('Mikroplastik','Microplastics'),'micro'],[tr('Wasserqualität','Water quality'),null],['TDS','tds'],[tr('Remineralisierung','Remineralization'),'remin'],[tr('Betrieb','Operation'),null],[tr('Geräuschpegel','Noise'),'noise'],[tr('Stromverbrauch','Power'),'power'],[tr('Garantie','Warranty'),'warranty']];table.innerHTML=`<table class="compare-table"><thead><tr><th>${tr('Parameter','Parameter')}</th>${ps.map(p=>`<th>${p.brand}<br><strong>${p.name}</strong></th>`).join('')}</tr></thead><tbody>${rows.map(r=>r[1]?`<tr><td>${r[0]}</td>${ps.map(p=>`<td>${p[r[1]]}</td>`).join('')}</tr>`:`<tr class="group-row"><td colspan="${ps.length+1}">${r[0]}</td></tr>`).join('')}</tbody></table>`}



function setupSearchClearButtons(){
  const inputs=[...document.querySelectorAll('.product-search, input[placeholder="Search manufacturer"], input[placeholder="Hersteller suchen"], input[type="search"]')];
  inputs.forEach(input=>{
    if(input.dataset.clearReady==='1')return;
    const parent=input.parentElement;
    if(!parent)return;
    if(input.id==='brandDirectorySearch' || parent.querySelector('.field-clear')){
      input.dataset.clearReady='1';
      return;
    }
    input.dataset.clearReady='1';
    const clear=document.createElement('button');
    clear.type='button';
    clear.className='search-clear-btn';
    clear.setAttribute('aria-label',tr('Suchfeld leeren','Clear search field'));
    clear.setAttribute('title',tr('Suchfeld leeren','Clear search field'));
    clear.innerHTML='×';
    input.insertAdjacentElement('afterend',clear);
    const update=()=>{
      const hasValue=input.value.length>0;
      clear.classList.toggle('show',hasValue);
      clear.tabIndex=hasValue?0:-1;
      clear.setAttribute('aria-hidden',hasValue?'false':'true');
    };
    clear.addEventListener('click',e=>{
      e.preventDefault();
      e.stopPropagation();
      input.value='';
      input.dispatchEvent(new Event('input',{bubbles:true}));
      input.dispatchEvent(new Event('change',{bubbles:true}));
      parent.querySelectorAll('.autocomplete-results').forEach(box=>box.classList.remove('show'));
      update();
      input.focus();
    });
    input.addEventListener('input',update);
    input.addEventListener('change',update);
    update();
  });
}

document.addEventListener('DOMContentLoaded',()=>{
  renderDock();
  setupSearchClearButtons();
  setupBrandSearch();
  initComparePage();
  setupGeneralAutocomplete();
  setupProductsQueryFilter();
  document.querySelectorAll('[data-compare]').forEach(b=>b.addEventListener('click',()=>addCompare(b.dataset.compare)));
});


const productRatingSeed={
 pearl:{average:5,count:5},dwm:{average:4.4,count:81},hydro:{average:4.5,count:22}
};
function getReviewStore(){try{return JSON.parse(storageGet('wasserProductReviews','{}'))||{}}catch(e){return {}}}
function saveReviewStore(data){storageSet('wasserProductReviews',JSON.stringify(data))}
function getProductReviews(id){return getReviewStore()[id]||[]}
function calculateProductRating(id){const seed=productRatingSeed[id]||{average:0,count:0};const reviews=getProductReviews(id);const total=seed.average*seed.count+reviews.reduce((s,r)=>s+Number(r.rating||0),0);const count=seed.count+reviews.length;return {average:count?total/count:0,count}}
function starText(value){const full=Math.round(value);return '★★★★★'.slice(0,full)+'☆☆☆☆☆'.slice(0,5-full)}
function ratingStars(value){const percent=Math.max(0,Math.min(100,(Number(value)||0)/5*100));return `<span class="rating-stars" style="--rating-fill:${percent}%" aria-label="${(Number(value)||0).toFixed(2)} von 5 Sternen"><span>★★★★★</span></span>`}
function getRatingDimensions(id){
 const keys=['quality','usability','service','price'];
 const reviews=getProductReviews(id);
 return Object.fromEntries(keys.map(key=>{const values=reviews.map(review=>Number(review.scores?.[key])).filter(value=>value>=1&&value<=5);return [key,values.length?values.reduce((sum,value)=>sum+value,0)/values.length:null]}));
}
function getFrequentFeedback(id,key){
 const counts=new Map();
 getProductReviews(id).flatMap(review=>review[key]||[]).forEach(item=>{const clean=String(item).trim();if(clean)counts.set(clean,(counts.get(clean)||0)+1)});
 return [...counts.entries()].sort((a,b)=>b[1]-a[1]).slice(0,4).map(([text,count])=>({text,count}));
}
function ratingDimensionHTML(label,value){
 const score=value==null?'—':value.toFixed(2);
 const width=value==null?0:value/5*100;
 return `<div class="rating-dimension"><div><span>${label}</span><strong>${score}</strong></div><div class="rating-track"><i style="width:${width}%"></i></div></div>`;
}
function renderRatingExperience(){
 document.querySelectorAll('.product-card[data-product-id]').forEach(card=>{
   const id=card.dataset.productId;
   const result=calculateProductRating(id);
   const photo=card.querySelector('.photo');
   if(photo){let badge=photo.querySelector('.product-rating-badge');if(!badge){badge=document.createElement('span');badge.className='product-rating-badge';photo.appendChild(badge)}badge.innerHTML=result.count?`★ <b>${result.average.toFixed(2)}</b>`:`☆ <span>${tr('Keine Bewertung','No rating')}</span>`;badge.classList.toggle('is-empty',!result.count)}
   const summary=card.querySelector('.rating');
   if(summary){summary.classList.add('rating-line');summary.innerHTML=result.count?`${ratingStars(result.average)} <strong>${result.average.toFixed(2)}</strong><span>${result.count}</span>`:`<span class="rating-empty">${tr('Noch keine Nutzerbewertung','No user ratings yet')}</span>`}
 });

 const layout=document.querySelector('.device-layout');
 if(!layout)return;
 const file=location.pathname.split('/').pop();
 const product=products.find(item=>item.url?.split('/').pop()===file);
 if(!product)return;
 const result=calculateProductRating(product.id);
 const dimensions=getRatingDimensions(product.id);
 const pros=getFrequentFeedback(product.id,'pros');
 const cons=getFrequentFeedback(product.id,'cons');
 const photo=layout.querySelector('.device-photo');
 if(photo){let badge=photo.querySelector('.product-rating-badge');if(!badge){badge=document.createElement('span');badge.className='product-rating-badge product-rating-badge-large';photo.appendChild(badge)}badge.innerHTML=result.count?`★ <b>${result.average.toFixed(2)}</b><small>${result.count} ${tr('Bewertungen','reviews')}</small>`:`☆ <span>${tr('Noch keine Bewertung','No rating yet')}</span>`}
 let section=document.querySelector('[data-product-rating-panel]');
 if(!section){section=document.createElement('section');section.className='product-rating-panel';section.dataset.productRatingPanel=product.id;layout.insertAdjacentElement('afterend',section)}
 const feedback=(items,type)=>items.length?items.map(item=>`<span><i>${type==='pro'?'✓':'−'}</i>${escapeReview(item.text)}${item.count>1?` <small>×${item.count}</small>`:''}</span>`).join(''):`<p>${tr('Noch nicht genügend strukturierte Nutzerangaben.','Not enough structured user feedback yet.')}</p>`;
 section.innerHTML=`<div class="rating-overview"><span class="eyebrow">${tr('Nutzerbewertung','User rating')}</span><div class="rating-score">${result.count?result.average.toFixed(2):'—'}</div>${ratingStars(result.average)}<strong>${result.count} ${tr('Bewertungen','reviews')}</strong><button class="btn primary small" type="button" data-review-product="${product.id}">${tr('Produkt bewerten','Rate product')}</button></div><div class="rating-breakdown"><h2>${tr('Bewertung im Detail','Rating details')}</h2>${ratingDimensionHTML(tr('Qualität','Quality'),dimensions.quality)}${ratingDimensionHTML(tr('Bedienkomfort','Ease of use'),dimensions.usability)}${ratingDimensionHTML(tr('Service','Service'),dimensions.service)}${ratingDimensionHTML(tr('Preis-Leistung','Value for money'),dimensions.price)}</div><div class="rating-feedback"><div class="rating-feedback-list is-pro"><h3>${tr('Häufig genannte Vorteile','Frequently mentioned pros')}</h3>${feedback(pros,'pro')}</div><div class="rating-feedback-list is-con"><h3>${tr('Häufig genannte Nachteile','Frequently mentioned cons')}</h3>${feedback(cons,'con')}</div></div>`;
 section.querySelector('[data-review-product]')?.addEventListener('click',()=>openReviewModal(product.id));
}
function refreshProductRatings(){
 document.querySelectorAll('[data-rating-summary]').forEach(el=>{const id=el.dataset.ratingSummary,r=calculateProductRating(id);el.textContent=`${starText(r.average)} ${r.average.toFixed(1)} (${r.count})`});
 document.querySelectorAll('[data-rating-value]').forEach(el=>{const r=calculateProductRating(el.dataset.ratingValue);el.textContent=r.average.toFixed(1)});
 document.querySelectorAll('[data-rating-stars]').forEach(el=>{const r=calculateProductRating(el.dataset.ratingStars);el.textContent=starText(r.average)});
 document.querySelectorAll('[data-rating-count]').forEach(el=>{const r=calculateProductRating(el.dataset.ratingCount);el.textContent=`${r.count} ${tr('Bewertungen','reviews')}`});
 document.querySelectorAll('[data-review-list]').forEach(renderReviewList);
 renderRatingExperience();
}
function renderReviewList(el){const id=el.dataset.reviewList,reviews=getProductReviews(id);if(!reviews.length){el.innerHTML=`<div class="review-empty">${tr('Noch keine zusätzlichen Nutzerbewertungen in diesem Browser.','No additional user reviews in this browser yet.')}</div>`;return}el.innerHTML=reviews.slice().reverse().map((r,i)=>`<article class="rich-review-card"><div class="user-review-head"><strong>${escapeReview(r.name||tr('Anonym','Anonymous'))}</strong><span class="review-stars-display">${starText(r.rating)}</span></div><p>${escapeReview(r.comment)}</p>${(r.pros||[]).length||(r.cons||[]).length?`<div class="pros-cons"><div><b>${tr('Vorteile','Pros')}</b>${(r.pros||[]).map(x=>`<span>✓ ${escapeReview(x)}</span>`).join('')}</div><div><b>${tr('Nachteile','Cons')}</b>${(r.cons||[]).map(x=>`<span>− ${escapeReview(x)}</span>`).join('')}</div></div>`:''}<div class="review-footer"><button class="helpful-btn" data-helpful-id="local-${id}-${i}" data-helpful-count="${r.helpful||0}">👍 <span>${r.helpful||0}</span> ${tr('hilfreich','helpful')}</button><time>${new Date(r.date).toLocaleDateString(lang()==='de'?'de-DE':'en-US')}</time></div></article>`).join('');setupHelpfulButtons(el)}
function escapeReview(v){const d=document.createElement('div');d.textContent=v||'';return d.innerHTML}
function openReviewModal(id){const p=products.find(x=>x.id===id);let modal=document.getElementById('review-modal');if(!modal){modal=document.createElement('div');modal.id='review-modal';modal.className='review-modal';modal.innerHTML=`<div class="review-dialog" role="dialog" aria-modal="true"><button class="review-close" aria-label="Close">×</button><h2 class="review-dialog-title"></h2><form id="review-form"><input type="hidden" name="productId"><label>${tr('Ihr Name','Your name')}<input name="name" maxlength="60" placeholder="${tr('Optional','Optional')}"></label><fieldset><legend>${tr('Gesamtbewertung','Overall rating')}</legend><div class="star-picker">${[1,2,3,4,5].map(n=>`<button type="button" data-star="${n}" aria-label="${n} ${tr('Sterne','stars')}">☆</button>`).join('')}</div><input type="hidden" name="rating" required></fieldset><fieldset class="review-score-fields"><legend>${tr('Einzelbewertungen','Detailed ratings')}</legend>${[['quality','Qualität','Quality'],['usability','Bedienkomfort','Ease of use'],['service','Service','Service'],['price','Preis-Leistung','Value for money']].map(([name,de,en])=>`<label>${tr(de,en)}<select name="score_${name}" required><option value="">—</option>${[5,4,3,2,1].map(value=>`<option value="${value}">${value} / 5</option>`).join('')}</select></label>`).join('')}</fieldset><label>${tr('Kommentar','Comment')}<textarea name="comment" rows="5" maxlength="1200" required placeholder="${tr('Beschreiben Sie Ihre Erfahrung mit dem Produkt.','Describe your experience with the product.')}"></textarea></label><label>${tr('Vorteile (eine Zeile pro Punkt)','Pros (one item per line)')}<textarea name="pros" rows="3" maxlength="600" placeholder="${tr('Leise\nHoher Durchfluss','Quiet\nHigh flow rate')}"></textarea></label><label>${tr('Nachteile (eine Zeile pro Punkt)','Cons (one item per line)')}<textarea name="cons" rows="3" maxlength="600" placeholder="${tr('Ersatzfilter teuer','Expensive replacement filters')}"></textarea></label><label class="review-consent"><input type="checkbox" required> ${tr('Ich bestätige, dass diese Bewertung auf meiner eigenen Erfahrung basiert.','I confirm this review is based on my own experience.')}</label><button class="btn primary" type="submit">${tr('Bewertung veröffentlichen','Publish review')}</button><p class="review-storage-note">${tr('Demoversion: Speicherung nur in diesem Browser.','Demo: stored only in this browser.')}</p></form></div>`;document.body.appendChild(modal);modal.querySelector('.review-close').onclick=()=>modal.classList.remove('show');modal.addEventListener('click',e=>{if(e.target===modal)modal.classList.remove('show')});const form=modal.querySelector('#review-form');modal.querySelectorAll('[data-star]').forEach(btn=>btn.onclick=()=>{const n=Number(btn.dataset.star);form.rating.value=n;modal.querySelectorAll('[data-star]').forEach(b=>b.textContent=Number(b.dataset.star)<=n?'★':'☆')});form.onsubmit=e=>{e.preventDefault();if(!form.rating.value){alert(tr('Bitte wählen Sie eine Sternebewertung.','Please choose a star rating.'));return}const store=getReviewStore(),pid=form.productId.value;store[pid]=store[pid]||[];store[pid].push({name:form.name.value.trim(),rating:Number(form.rating.value),scores:{quality:Number(form.score_quality.value),usability:Number(form.score_usability.value),service:Number(form.score_service.value),price:Number(form.score_price.value)},comment:form.comment.value.trim(),pros:form.pros.value.split(/\n+/).map(x=>x.trim()).filter(Boolean),cons:form.cons.value.split(/\n+/).map(x=>x.trim()).filter(Boolean),helpful:0,date:new Date().toISOString()});saveReviewStore(store);modal.classList.remove('show');form.reset();modal.querySelectorAll('[data-star]').forEach(b=>b.textContent='☆');refreshProductRatings()}}
 modal.querySelector('.review-dialog-title').textContent=`${tr('Bewertung für','Review for')} ${p?p.brand+' '+p.name:id}`;modal.querySelector('[name="productId"]').value=id;modal.classList.add('show')}

function setupHelpfulButtons(root=document){root.querySelectorAll('.helpful-btn').forEach(btn=>{if(btn.dataset.ready)return;btn.dataset.ready='1';const id=btn.dataset.helpfulId;let count=Number(btn.dataset.helpfulCount||0);if(storageGet('wasserHelpful_'+id,'0')==='1'){btn.classList.add('voted');count+=1;btn.querySelector('span').textContent=count}btn.addEventListener('click',()=>{if(storageGet('wasserHelpful_'+id,'0')==='1')return;storageSet('wasserHelpful_'+id,'1');btn.classList.add('voted');btn.querySelector('span').textContent=count+1})})}
function setupReviewSystem(){document.querySelectorAll('[data-review-product]').forEach(btn=>btn.addEventListener('click',()=>openReviewModal(btn.dataset.reviewProduct)));refreshProductRatings()}
document.addEventListener('DOMContentLoaded',()=>{setupReviewSystem();setupHelpfulButtons()});


function setupProductsLiveFilters(){
  if(!/products\.html$/.test(location.pathname)) return;

  const category = document.getElementById('filterCategory');
  const brandInput = document.getElementById('filterBrand');
  const brandClear = document.getElementById('filterBrandClear');
  const brandSuggestions = document.getElementById('filterBrandSuggestions');
  const price = document.getElementById('filterPrice');
  const featuresBox = document.getElementById('dynamicFeatures');
  const reset = document.getElementById('resetProductFilters');
  const count = document.getElementById('productResultCount');
  const resultText = document.getElementById('productResultText');
  if(!category || !brandInput || !price || !featuresBox) return;

  const cards = [...document.querySelectorAll('.product-card')];
  const brands = [...new Set(products.map(p=>p.brand))].sort((a,b)=>a.localeCompare(b));
  const featureDefinitions = {
    'Under Sink RO': [
      {id:'remineralization',de:'Remineralisierung',en:'Remineralization'},
      {id:'certified',de:'Geprüfte Filterleistung',en:'Certified claims'},
      {id:'tankless',de:'Tanklos',en:'Tankless'},
      {id:'pump',de:'Integrierte Pumpe',en:'Integrated pump'}
    ],
    'Hydrogen Bottles': [
      {id:'ppb1500',de:'Mindestens 1.500 PPB',en:'At least 1,500 PPB',test:p=>(p.ppb||0)>=1500},
      {id:'ppb3000',de:'Bis 3.000 PPB',en:'Up to 3,000 PPB',test:p=>(p.ppb||0)>=3000},
      {id:'pem-spe',de:'PEM/SPE-Technologie',en:'PEM/SPE technology'},
      {id:'usb-c',de:'USB-C',en:'USB-C'},
      {id:'display',de:'Display',en:'Display'},
      {id:'self-cleaning',de:'Selbstreinigung',en:'Self-cleaning'}
    ],
    'Shower Filters': [
      {id:'chlorine',de:'Chlorreduzierung',en:'Chlorine reduction'},
      {id:'universal',de:'Universalanschluss',en:'Universal connection'},
      {id:'replaceable',de:'Wechselkartusche',en:'Replaceable cartridge'}
    ],
    '': [
      {id:'remineralization',de:'Remineralisierung',en:'Remineralization'},
      {id:'certified',de:'Geprüfte Filterleistung',en:'Certified claims'},
      {id:'tankless',de:'Tanklos',en:'Tankless'},
      {id:'pem-spe',de:'PEM/SPE-Technologie',en:'PEM/SPE technology'}
    ]
  };

  function localText(item){ return lang()==='de' ? item.de : item.en; }

  function renderFeatures(){
    const defs = featureDefinitions[category.value] || featureDefinitions[''];
    featuresBox.innerHTML = defs.map(item=>`
      <label class="feature-option">
        <input type="checkbox" value="${item.id}">
        <span>${localText(item)}</span>
      </label>`).join('');
    featuresBox.querySelectorAll('input').forEach(el=>el.addEventListener('change',applyFilters));
  }

  function selectedFeatureDefs(){
    const defs = featureDefinitions[category.value] || featureDefinitions[''];
    const checked = [...featuresBox.querySelectorAll('input:checked')].map(x=>x.value);
    return defs.filter(d=>checked.includes(d.id));
  }

  function productForCard(card){
    return products.find(p=>p.id===card.dataset.productId);
  }

  function matchesFeatures(p){
    return selectedFeatureDefs().every(def=>{
      if(def.test) return def.test(p);
      return (p.features||[]).includes(def.id);
    });
  }

  function applyFilters(){
    const selectedCategory = category.value;
    const brandQuery = brandInput.value.trim().toLowerCase();
    const selectedPrice = price.value;
    let visible = 0;

    cards.forEach(card=>{
      const p = productForCard(card);
      if(!p){ card.style.display='none'; return; }

      const categoryMatch = !selectedCategory || p.cat===selectedCategory;
      const brandMatch = !brandQuery || p.brand.toLowerCase().includes(brandQuery);
      const priceMatch = !selectedPrice ||
        (selectedPrice==='under1500' && p.priceValue != null && p.priceValue < 1500) ||
        (selectedPrice==='from1500' && p.priceValue != null && p.priceValue >= 1500);
      const featureMatch = matchesFeatures(p);
      const show = categoryMatch && brandMatch && priceMatch && featureMatch;

      card.style.display = show ? '' : 'none';
      if(show) visible++;
    });

    if(count) count.textContent = `${visible} ${visible===1 ? tr('Modell','model') : tr('Modelle','models')}`;
    if(resultText) resultText.textContent = visible
      ? tr('Die Auswahl wird automatisch aktualisiert.','Results update automatically.')
      : tr('Keine Produkte entsprechen den gewählten Filtern.','No products match the selected filters.');

    brandClear.classList.toggle('show', brandInput.value.length>0);
  }

  function drawBrandSuggestions(){
    const q = brandInput.value.trim().toLowerCase();
    const matches = brands.filter(b=>!q || b.toLowerCase().includes(q));
    brandSuggestions.innerHTML = matches.length
      ? matches.map(b=>`<button type="button" class="brand-suggestion" role="option">${b}</button>`).join('')
      : `<div class="brand-suggestion-empty">${tr('Keine Marke gefunden','No brand found')}</div>`;
    brandSuggestions.classList.add('show');
    brandSuggestions.querySelectorAll('.brand-suggestion').forEach(btn=>{
      btn.addEventListener('click',()=>{
        brandInput.value = btn.textContent;
        brandSuggestions.classList.remove('show');
        applyFilters();
        brandInput.focus();
      });
    });
  }

  category.addEventListener('change',()=>{
    renderFeatures();
    applyFilters();
  });
  price.addEventListener('change', applyFilters);
  brandInput.addEventListener('input',()=>{
    drawBrandSuggestions();
    applyFilters();
  });
  brandInput.addEventListener('focus', drawBrandSuggestions);
  brandInput.addEventListener('keydown',e=>{
    if(e.key==='Escape') brandSuggestions.classList.remove('show');
    if(e.key==='Enter'){
      e.preventDefault();
      const first = brandSuggestions.querySelector('.brand-suggestion');
      if(first) first.click();
      else applyFilters();
    }
  });
  brandClear.addEventListener('click',()=>{
    brandInput.value='';
    brandSuggestions.classList.remove('show');
    applyFilters();
    brandInput.focus();
  });
  reset.addEventListener('click',()=>{
    category.value='';
    brandInput.value='';
    price.value='';
    renderFeatures();
    brandSuggestions.classList.remove('show');
    applyFilters();
  });
  document.addEventListener('click',e=>{
    if(!brandInput.closest('.filter-autocomplete').contains(e.target)){
      brandSuggestions.classList.remove('show');
    }
  });

  renderFeatures();
  applyFilters();
}


document.addEventListener('DOMContentLoaded', setupProductsLiveFilters);


// Sprint 1.1 global UI behaviours
(function(){
  function initV2Navigation(){
    document.querySelectorAll('.mobile-menu-btn').forEach(btn=>{
      const header=btn.closest('.site-header');
      const panel=header && header.querySelector('.mobile-nav-panel');
      if(!panel) return;
      btn.addEventListener('click',()=>{
        const open=panel.classList.toggle('open');
        panel.setAttribute('aria-hidden',String(!open));
        btn.setAttribute('aria-expanded',String(open));
        btn.textContent=open?'×':'☰';
      });
    });
    document.querySelectorAll('.nav-more-btn').forEach(btn=>{
      btn.addEventListener('click',()=>btn.setAttribute('aria-expanded',btn.getAttribute('aria-expanded')==='true'?'false':'true'));
    });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',initV2Navigation); else initV2Navigation();
})();

function setupBrandDirectory(){const input=document.getElementById('brandDirectorySearch');if(!input)return;const clear=document.getElementById('brandDirectoryClear');const cards=[...document.querySelectorAll('.brand-directory-card')];const count=document.getElementById('brandDirectoryCount');const empty=document.getElementById('brandDirectoryEmpty');const normalize=value=>(value||'').normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').trim().toLowerCase();function run(){const q=normalize(input.value);let n=0;cards.forEach(c=>{const haystack=normalize([c.dataset.brandName,c.dataset.brandCountry,c.querySelector('h3')?.textContent,c.querySelector('.brand-meta')?.textContent].join(' '));const show=!q||haystack.includes(q);c.hidden=!show;c.style.display=show?'':'none';if(show)n++});if(count)count.textContent=`${n} ${lang()==='de'?'Marken':'brands'}`;if(clear)clear.classList.toggle('show',!!q);if(empty)empty.hidden=n>0}input.addEventListener('input',run);input.addEventListener('search',run);if(clear)clear.addEventListener('click',()=>{input.value='';run();input.focus()});run()}
document.addEventListener('DOMContentLoaded',setupBrandDirectory);

async function setupDatabaseOverview(){
  const root=document.getElementById('databaseOverview');
  if(!root)return;
  try{
    const prefix=basePrefix();
    const [productResponse,brandResponse]=await Promise.all([
      fetch(prefix+'data/products.json',{cache:'no-store'}),
      fetch(prefix+'data/brands.json',{cache:'no-store'})
    ]);
    if(!productResponse.ok||!brandResponse.ok)throw new Error('Catalog data unavailable');
    const [catalogProducts,catalogBrands]=await Promise.all([productResponse.json(),brandResponse.json()]);
    const values={
      overviewProducts:catalogProducts.length,
      overviewBrands:catalogBrands.length,
      overviewTechnologies:new Set(catalogProducts.map(item=>item.category).filter(Boolean)).size,
      overviewReviews:catalogProducts.reduce((sum,item)=>sum+(Number(item.reviews)||0),0)
    };
    Object.entries(values).forEach(([id,value])=>{const node=document.getElementById(id);if(node)node.textContent=new Intl.NumberFormat(lang()==='de'?'de-DE':'en-US').format(value)});
  }catch(error){
    root.dataset.syncStatus='fallback';
  }
}
document.addEventListener('DOMContentLoaded',setupDatabaseOverview);

async function setupCatalogCardSync(){
  const cards=[...document.querySelectorAll('.product-card[data-product-id]')];
  if(!cards.length)return;
  try{
    const response=await fetch(basePrefix()+'data/products.json',{cache:'no-store'});
    if(!response.ok)throw new Error('Catalog data unavailable');
    const catalog=await response.json();
    const byId=new Map(catalog.map(item=>[String(item.id),item]));
    const locale=lang()==='de'?'de-DE':'en-US';
    cards.forEach(card=>{
      const product=byId.get(String(card.dataset.productId));
      if(!product)return;
      const image=card.querySelector('.photo img');
      const brand=card.querySelector('.brand');
      const name=card.querySelector('h3');
      const price=card.querySelector('.price');
      if(image&&product.image){
        image.src=basePrefix()+product.image;
        image.alt=`${product.brand} ${product.name}`;
      }
      if(brand)brand.textContent=product.brand||'';
      if(name)name.textContent=product.name||'';
      if(price&&product.price!=null){
        try{price.textContent=new Intl.NumberFormat(locale,{style:'currency',currency:product.currency||'EUR',maximumFractionDigits:0}).format(product.price)}
        catch(error){price.textContent=`${product.currency||''} ${product.price}`.trim()}
      }
    });
  }catch(error){
    document.documentElement.dataset.catalogCardSync='fallback';
  }
}
document.addEventListener('DOMContentLoaded',setupCatalogCardSync);
