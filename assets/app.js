const products=[
{id:'biella',brand:'WERTACH',name:'Biella',cat:'Countertop RO',price:'from €1,994',priceValue:1994,features:['remineralization','display','cooling','instant-heater'],ppb:null,flow:'0.34 L/min',maint:'Filter-dependent',liter:'—',membrane:'100 GPD Filmtec® RO',pfas:'Manufacturer claim',viruses:'RO + UV protection',bacteria:'4-fold; 5-fold Medical',nitrates:'RO filtration',lead:'RO filtration',arsenic:'RO filtration',micro:'RO filtration',tds:'Real-time display',remin:'Yes',noise:'Not specified',power:'2,093 W max.',warranty:'5 years',country:'Germany',image:'assets/img/wertach-biella.webp',url:'products/wertach-biella.html'},
{id:'pearl',brand:'BLACKWATER',name:'Pearl',cat:'Countertop RO',price:'€1,497',priceValue:1497,features:['remineralization','display','cooling','instant-heater'],ppb:null,flow:'0.34 L/min',maint:'Filter-dependent',liter:'—',membrane:'100 GPD Filmtec® RO',pfas:'RO filtration',viruses:'RO + dual UV',bacteria:'3-fold protection',nitrates:'RO filtration',lead:'RO filtration',arsenic:'RO filtration',micro:'0.0001 µm membrane',tds:'Input display',remin:'Yes',noise:'Not specified',power:'2,150 W max.',warranty:'Not specified',country:'Germany',image:'assets/img/blackwater-pearl.jpg',url:'products/blackwater-pearl.html'},
{id:'spirit',brand:"Bluewater",name:"Spirit 300CP",cat:"Under Sink RO",price:"€1,910",priceValue:1910,features:[],ppb:null,flow:"bis 99–99,7 % laut Händlerseite",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Nein",noise:'Not published',power:"350 W / 6 A",warranty:"1 Jahr",country:"Sweden",image:"assets/products/bluewater-spirit-300cp.jpg",url:'products/bluewater-spirit-300.html'},
{id:'hydro',brand:'WALUTEC',name:'Hydrogen Water Bottle',cat:'Hydrogen Bottles',price:'€199',priceValue:199,features:['pem-spe','usb-c','display'],ppb:3000,flow:'280 ml',maint:'No filter cartridges',liter:'—',membrane:'SPE/PEM',pfas:'No filtration function',viruses:'No filtration function',bacteria:'No filtration function',nitrates:'No filtration function',lead:'No filtration function',arsenic:'No filtration function',micro:'No filtration function',tds:'Unchanged',remin:'No',noise:'Not specified',power:'USB-C',warranty:'Not specified',country:'UAE / Germany',image:'assets/products/walutec-hydrogen-bottle.png',url:'products/walutec-hydrogen-bottle.html'},
{id:'blackwater-hydrogen',brand:'BLACKWATER',name:'Hydrogen Bottle',cat:'Hydrogen Bottles',price:'€199',priceValue:199,features:['pem-spe','usb-c','display'],ppb:3000,flow:'260 ml',maint:'No filter cartridges',liter:'—',membrane:'DuPont Nafion™ 117 SPE/PEM',pfas:'No filtration function',viruses:'No filtration function',bacteria:'No filtration function',nitrates:'No filtration function',lead:'No filtration function',arsenic:'No filtration function',micro:'No filtration function',tds:'Unchanged',remin:'No',noise:'Not specified',power:'Rechargeable battery',warranty:'Manufacturer information',country:'Germany',image:'assets/products/blackwater-hydrogen-bottle.png',url:'products/blackwater-hydrogen-bottle.html'},
{id:'piurify-hydrogenator-black',brand:'PIURIFY',name:'Hydrogenator® Bottle Black',cat:'Hydrogen Bottles',price:'€120',priceValue:120,features:['pem-spe','usb-c','self-cleaning'],ppb:6300,flow:'280 ml',maint:'No filter cartridges',liter:'—',membrane:'DuPont SPE/PEM, platinum-coated',pfas:'No filtration function',viruses:'No filtration function',bacteria:'No filtration function',nitrates:'No filtration function',lead:'No filtration function',arsenic:'No filtration function',micro:'No filtration function',tds:'Unchanged',remin:'No',noise:'Not specified',power:'USB charging',warranty:'Lifetime limited warranty',country:'USA',image:'assets/products/piurify-hydrogenator-black.png',url:'products/piurify-hydrogenator-black.html'},
{id:'echo-flask',brand:'Echo Water',name:'ECHO Flask',cat:'Hydrogen Bottles',price:'€257',priceValue:257,features:['pem-spe','usb-c','display'],ppb:8250,flow:'360 ml',maint:'Clean cycle; monthly deep cleaning',liter:'—',membrane:'PEM, platinum-coated titanium',pfas:'No filtration function',viruses:'No filtration function',bacteria:'No filtration function',nitrates:'No filtration function',lead:'No filtration function',arsenic:'No filtration function',micro:'No filtration function',tds:'Unchanged',remin:'No',noise:'Not specified',power:'USB-C',warranty:'5 years',country:'USA',image:'assets/products/echo-flask.png',url:'products/echo-flask.html'},
{id:'ionbottles-atom',brand:'ionBottles',name:'ATOM™',cat:'Hydrogen Bottles',price:'€128',priceValue:128,features:['pem-spe','usb-c','display'],ppb:5000,flow:'295 ml',maint:'Descaling as needed',liter:'—',membrane:'Medical-grade DuPont PEM',pfas:'No filtration function',viruses:'No filtration function',bacteria:'No filtration function',nitrates:'No filtration function',lead:'No filtration function',arsenic:'No filtration function',micro:'No filtration function',tds:'Unchanged',remin:'No',noise:'Not specified',power:'USB-C',warranty:'1 year',country:'USA',image:'assets/products/ionbottles-atom.jpg',url:'products/ionbottles-atom.html'},
{id:'levelupway-2-in-1',brand:'Level Up Way',name:'2-in-1 Hydrogen Water Bottle',cat:'Hydrogen Bottles',price:'Preis auf Anfrage',priceValue:null,features:['pem-spe','self-cleaning'],ppb:1300,flow:'325 ml',maint:'Self-cleaning mode',liter:'—',membrane:'SPE/PEM',pfas:'No filtration function',viruses:'No filtration function',bacteria:'No filtration function',nitrates:'No filtration function',lead:'No filtration function',arsenic:'No filtration function',micro:'No filtration function',tds:'Unchanged',remin:'No',noise:'Not specified',power:'Rechargeable battery',warranty:'Not specified',country:'USA',image:'assets/products/levelupway-2-in-1.jpg',url:'products/levelupway-2-in-1.html'},
{id:'alkaviva-hi-output',brand:'AlkaViva',name:'Hi-Output H₂ Bottle',cat:'Hydrogen Bottles',price:'Preis auf Anfrage',priceValue:null,features:['pem-spe','usb-c'],ppb:5000,flow:'210 ml',maint:'Manufacturer instructions',liter:'—',membrane:'Hydrogen electrolysis',pfas:'No filtration function',viruses:'No filtration function',bacteria:'No filtration function',nitrates:'No filtration function',lead:'No filtration function',arsenic:'No filtration function',micro:'No filtration function',tds:'Unchanged',remin:'No',noise:'Not specified',power:'Rechargeable battery',warranty:'Not specified',country:'Australia',image:'assets/products/alkaviva-hi-output.png',url:'products/alkaviva-hi-output.html'},
{id:'truu-fountain-3',brand:"truu",name:"fountain 3",cat:"Commercial Water System",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:"Not published",image:"assets/products/truu-fountain-3.png",url:'products/truu-fountain-3.html'},
{id:'mrwater-premium-ro',brand:"MisterWater",name:"Wasserfilteranlagen (Puria / Arctica / Silver Star / Futura)",cat:"Reverse Osmosis",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:"Not published",image:"assets/products/mrwater-premium-ro.png",url:'products/mrwater-premium-ro.html'},
{id:'wertach-pantera',brand:"WERTACH",name:"Pantera",cat:"Direct Flow RO",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"WERTGARANTIE laut Hersteller",country:"Not published",image:"assets/products/wertach-pantera.webp",url:'products/wertach-pantera.html'},
{id:'osmofresh-fusion-pro',brand:"OsmoFresh",name:"Fusion Pro",cat:"Countertop RO",price:"1.290 €",priceValue:1290,features:[],ppb:null,flow:"120 W",maint:"Alle 12 Monate",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"ca. 2,6 W Standby; bis 2.400 W Betrieb",warranty:"Not published",country:"Not published",image:"assets/products/osmofresh-fusion-pro.webp",url:'products/osmofresh-fusion-pro.html'},
{id:'greifenstein-direct-flow-premium',brand:"Greifenstein Wasserveredelung",name:"INOX",cat:"Direct Flow RO",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"TFC, 0,0001 Mikron",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"2 Jahre; Verlängerung unter Herstellerbedingungen",country:"Not published",image:"assets/products/greifenstein-inox.jpg",url:'products/greifenstein-direct-flow-premium.html'},
{id:'gewapur-ro-comfort-direct-flow',brand:"Gewapur",name:"Osmo Star 2.0",cat:"Direct Flow RO",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Not published",maint:"Schnellwechselsystem",liter:'—',membrane:"800 GPD",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:"Not published",image:"assets/products/gewapur-osmo-star-2.webp",url:'products/gewapur-ro-comfort-direct-flow.html'},
{id:'aqmos-aq-ro-800-gpd',brand:"Aqmos",name:"AQ-RO 800 GPD",cat:"Direct Flow RO",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"800 GPD",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:"Not published",image:"assets/brands/aqmos.png",url:'products/aqmos-aq-ro-800-gpd.html'},
{id:'wasserhaus-zen-flow',brand:"Wasserhaus",name:"ZEN FLOW",cat:"Direct Flow RO",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"bis ca. 2,1 L/min unter optimalen Bedingungen",maint:"Not published",liter:'—',membrane:"800 GPD",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:"Not published",remin:"Magnesium, Kalium und Calcium",noise:'Not published',power:"Not published",warranty:"Not published",country:"Not published",image:"assets/products/wasserhaus-zen-flow.jpg",url:'products/wasserhaus-zen-flow.html'},
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
{id:"walutec-el-nero-speedflow-medic-s",brand:"WALUTEC",name:"eL-Neró® speedflow medic S",cat:"Direct Flow RO",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"ca. 1,7 L/min",maint:'Not published',liter:'—',membrane:"700 GPD Hochleistungsmembran",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Ca, Mg, K und Na; pH-Stabilisierung",noise:'Not published',power:"1,4 W Standby; 84 W Produktion",warranty:"36 Monate; unter Herstellerbedingungen bis 10 Jahre verlängerbar",country:"Germany",image:"assets/products/walutec-el-nero-speedflow-medic-s.jpg",url:"products/walutec-el-nero-speedflow-medic-s.html"},
{id:"waterdrop-alkaline-ro-water-purifier-g5p500a",brand:"Waterdrop",name:"G5P500A Alkalische Umkehrosmoseanlage mit Wasserhahn",cat:"Direct Flow RO",price:"269,99 €",priceValue:269.99,features:[],ppb:null,flow:"500 GPD",maint:"Vor-/Nachfilter ca. 6–12 Monate; RO-Membran modellabhängig bis 24 Monate",liter:'—',membrane:"8-stufig, RO-Membran 0,0001 µm und alkalische Mineralisierung",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Ja, alkalische/mineralische Nachbehandlung",noise:'Not published',power:"Not published",warranty:"1 Jahr laut Vergleichstabelle des Herstellers",country:'Not published',image:"assets/products/waterdrop-alkaline-ro-water-purifier-g5p500a.webp",url:"products/waterdrop-alkaline-ro-water-purifier-g5p500a.html"},
{id:"waterdrop-alkalische-ro-wasserfilter-mit-wasserhahn-g5p700a",brand:"Waterdrop",name:"G5P700A Alkalischer Umkehrosmose Wasserfilter 700 GPD",cat:"Direct Flow RO",price:"369,99 €",priceValue:369.99,features:[],ppb:null,flow:"700 GPD",maint:"Vor-/Nachfilter ca. 6–12 Monate; RO-Membran modellabhängig bis 24 Monate",liter:'—',membrane:"8-stufig, RO-Membran 0,0001 µm und alkalische Mineralisierung",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Ja, alkalische/mineralische Nachbehandlung",noise:'Not published',power:"Not published",warranty:"1 Jahr laut Vergleichstabelle des Herstellers",country:'Not published',image:"assets/products/waterdrop-alkalische-ro-wasserfilter-mit-wasserhahn-g5p700a.webp",url:"products/waterdrop-alkalische-ro-wasserfilter-mit-wasserhahn-g5p700a.html"},
{id:"waterdrop-g3p600-mz-mineralien-wasserfilter",brand:"Waterdrop",name:"G3P600 Mineralien Umkehrosmose Wasserfilter mit MNR35 Ersatzfilter",cat:"Direct Flow RO",price:"458,98 €",priceValue:458.98,features:[],ppb:null,flow:"600 GPD",maint:"Vor-/Nachfilter ca. 6–12 Monate; RO-Membran modellabhängig bis 24 Monate",liter:'—',membrane:"8-stufige tanklose Umkehrosmose-Filtration",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Ja, alkalische/mineralische Nachbehandlung",noise:'Not published',power:"Not published",warranty:"1 Jahr laut Vergleichstabelle des Herstellers",country:'Not published',image:"assets/products/waterdrop-g3p600-mz-mineralien-wasserfilter.webp",url:"products/waterdrop-g3p600-mz-mineralien-wasserfilter.html"},
{id:"waterdrop-g3p600-waterdrop-umkehrosmose-wasserfilteranlage",brand:"Waterdrop",name:"G3P600 Smart Untertisch Umkehrosmose Wasserfilter 600 GPD",cat:"Direct Flow RO",price:"429,00 €",priceValue:429.0,features:[],ppb:null,flow:"600 GPD",maint:"Vor-/Nachfilter ca. 6–12 Monate; RO-Membran modellabhängig bis 24 Monate",liter:'—',membrane:"8-stufige tanklose Umkehrosmose-Filtration",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Nein / nicht Bestandteil dieses Sets",noise:'Not published',power:"Not published",warranty:"1 Jahr laut Vergleichstabelle des Herstellers",country:'Not published',image:"assets/products/waterdrop-g3p600-waterdrop-umkehrosmose-wasserfilteranlage.webp",url:"products/waterdrop-g3p600-waterdrop-umkehrosmose-wasserfilteranlage.html"},
{id:"waterdrop-mineralien-umkehrosmose-wasserfilter-g3p800-mz",brand:"Waterdrop",name:"G3P800 Mineralien Umkehrosmose Wasserfilter mit MNR35 Ersatzfilter",cat:"Direct Flow RO",price:"1.029,98 €",priceValue:1029.98,features:[],ppb:null,flow:"800 GPD",maint:"Vor-/Nachfilter ca. 6–12 Monate; RO-Membran modellabhängig bis 24 Monate",liter:'—',membrane:"10-stufige tanklose Umkehrosmose-Filtration",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Ja, alkalische/mineralische Nachbehandlung",noise:'Not published',power:"Not published",warranty:"1 Jahr laut Vergleichstabelle des Herstellers",country:'Not published',image:"assets/products/waterdrop-mineralien-umkehrosmose-wasserfilter-g3p800-mz.webp",url:"products/waterdrop-mineralien-umkehrosmose-wasserfilter-g3p800-mz.html"},
{id:"waterdrop-ro-heiss-kaltwasserspender-a1",brand:"Waterdrop",name:"A1 Auftisch Umkehrosmose Wasserfilter mit UV",cat:"Countertop RO",price:"599,99 €",priceValue:599.99,features:[],ppb:null,flow:"100 GPD",maint:"Vor-/Nachfilter ca. 6–12 Monate; RO-Membran modellabhängig bis 24 Monate",liter:'—',membrane:"Mehrstufige RO-Filtration mit dualer UV-Behandlung",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Nein / nicht Bestandteil dieses Sets",noise:'Not published',power:"Not published",warranty:"1 Jahr laut Vergleichstabelle des Herstellers",country:'Not published',image:"assets/products/waterdrop-ro-heiss-kaltwasserspender-a1.webp",url:"products/waterdrop-ro-heiss-kaltwasserspender-a1.html"},
{id:"waterdrop-sofortheiss-umkehrosmose-wasserfilter-k6",brand:"Waterdrop",name:"K6 Smart Umkehrosmose Wasserfilter mit Heißwasser",cat:"Direct Flow RO",price:"749,00 €",priceValue:749.0,features:[],ppb:null,flow:"600 GPD",maint:"Vor-/Nachfilter ca. 6–12 Monate; RO-Membran modellabhängig bis 24 Monate",liter:'—',membrane:"5-stufige Umkehrosmose-Filtration",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Nein / nicht Bestandteil dieses Sets",noise:'Not published',power:"Not published",warranty:"1 Jahr laut Vergleichstabelle des Herstellers",country:'Not published',image:"assets/products/waterdrop-sofortheiss-umkehrosmose-wasserfilter-k6.webp",url:"products/waterdrop-sofortheiss-umkehrosmose-wasserfilter-k6.html"},
{id:"waterdrop-umkehrosmose-wasserfilter-corero-c1h",brand:"Waterdrop",name:"C1H Auftisch Umkehrosmose Wasserfilter Heißwasser",cat:"Countertop RO",price:"269,99 €",priceValue:269.99,features:[],ppb:null,flow:"75 GPD",maint:"Vor-/Nachfilter ca. 6–12 Monate; RO-Membran modellabhängig bis 24 Monate",liter:'—',membrane:"6-stufig, RO-Membran 0,0001 µm",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Nein / nicht Bestandteil dieses Sets",noise:'Not published',power:"Not published",warranty:"1 Jahr laut Vergleichstabelle des Herstellers",country:'Not published',image:"assets/products/waterdrop-umkehrosmose-wasserfilter-corero-c1h.webp",url:"products/waterdrop-umkehrosmose-wasserfilter-corero-c1h.html"},
{id:"waterdrop-umkehrosmose-wasserfilter-x12",brand:"Waterdrop",name:"X12 Alkalischer Tankloser Umkehrosmose Wasserfilter 1200 GPD",cat:"Direct Flow RO",price:"1.299,00 €",priceValue:1299.0,features:[],ppb:null,flow:"1200 GPD",maint:"Vor-/Nachfilter ca. 6–12 Monate; RO-Membran modellabhängig bis 24 Monate",liter:'—',membrane:"11-stufig, RO-Membran 0,0001 µm, UV und alkalische Remineralisierung",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Ja, alkalische/mineralische Nachbehandlung",noise:'Not published',power:"Not published",warranty:"1 Jahr laut Vergleichstabelle des Herstellers",country:'Not published',image:"assets/products/waterdrop-umkehrosmose-wasserfilter-x12.webp",url:"products/waterdrop-umkehrosmose-wasserfilter-x12.html"},
{id:"waterdrop-umkehrosmose-wasserfilter-x16",brand:"Waterdrop",name:"X16 Alkalischer Mineralisierender Umkehrosmose Wasserfilter",cat:"Direct Flow RO",price:"1.999,00 €",priceValue:1999.0,features:[],ppb:null,flow:"1600 GPD",maint:"Vor-/Nachfilter ca. 6–12 Monate; RO-Membran modellabhängig bis 24 Monate",liter:'—',membrane:"11-stufig, RO-Membran 0,0001 µm und alkalische Remineralisierung",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Ja, alkalische/mineralische Nachbehandlung",noise:'Not published',power:"Not published",warranty:"1 Jahr laut Vergleichstabelle des Herstellers",country:'Not published',image:"assets/products/waterdrop-umkehrosmose-wasserfilter-x16.webp",url:"products/waterdrop-umkehrosmose-wasserfilter-x16.html"},
{id:"waterdrop-umkehrosmoseanlage-g3p800",brand:"Waterdrop",name:"G3P800 Tankloser Umkehrosmose Wasserfilter 800 GPD",cat:"Direct Flow RO",price:"999,00 €",priceValue:999.0,features:[],ppb:null,flow:"800 GPD",maint:"Vor-/Nachfilter ca. 6–12 Monate; RO-Membran modellabhängig bis 24 Monate",liter:'—',membrane:"10-stufige tanklose Umkehrosmose-Filtration",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Nein / nicht Bestandteil dieses Sets",noise:'Not published',power:"Not published",warranty:"1 Jahr laut Vergleichstabelle des Herstellers",country:'Not published',image:"assets/products/waterdrop-umkehrosmoseanlage-g3p800.webp",url:"products/waterdrop-umkehrosmoseanlage-g3p800.html"},
{id:"waterdrop-umkehrosmoseanlage-wasserfilter-x8",brand:"Waterdrop",name:"X8 Tankloser Untertisch Umkehrosmose Wasserfilter 800 GPD",cat:"Direct Flow RO",price:"799,00 €",priceValue:799.0,features:[],ppb:null,flow:"800 GPD",maint:"Vor-/Nachfilter ca. 6–12 Monate; RO-Membran modellabhängig bis 24 Monate",liter:'—',membrane:"9-stufig, RO-Membran 0,0001 µm",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Nein / nicht Bestandteil dieses Sets",noise:'Not published',power:"Not published",warranty:"1 Jahr laut Vergleichstabelle des Herstellers",country:'Not published',image:"assets/products/waterdrop-umkehrosmoseanlage-wasserfilter-x8.webp",url:"products/waterdrop-umkehrosmoseanlage-wasserfilter-x8.html"},
{id:"waterdrop-untertisch-umkehrosmoseanlage-g2p600",brand:"Waterdrop",name:"G2P600 Umkehrosmose-Wasserfiltrationssystem für Zuhause",cat:"Direct Flow RO",price:"329,99 €",priceValue:329.99,features:[],ppb:null,flow:"600 GPD",maint:"Vor-/Nachfilter ca. 6–12 Monate; RO-Membran modellabhängig bis 24 Monate",liter:'—',membrane:"MRO: RO-Membran, PP-Sediment, Aktivkohle und PET-Faltenfilter; CF: PP-Sediment und Aktivkohle",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Nein / nicht Bestandteil dieses Sets",noise:'Not published',power:"Not published",warranty:"1 Jahr laut Vergleichstabelle des Herstellers",country:'Not published',image:"assets/products/waterdrop-untertisch-umkehrosmoseanlage-g2p600.webp",url:"products/waterdrop-untertisch-umkehrosmoseanlage-g2p600.html"},
{id:"waterdrop-waterdrop-c1sl-alkalisches-tisch-umkehrosmoseanlage",brand:"Waterdrop",name:"C1SL Alkalisches Umkehrosmose-System für die Arbeitsplatte",cat:"Countertop RO",price:"259,00 €",priceValue:259.0,features:[],ppb:null,flow:"75 GPD",maint:"Vor-/Nachfilter ca. 6–12 Monate; RO-Membran modellabhängig bis 24 Monate",liter:'—',membrane:"Umkehrosmose mit alkalischer Mineralisierung",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Ja, alkalische/mineralische Nachbehandlung",noise:'Not published',power:"Not published",warranty:"1 Jahr laut Vergleichstabelle des Herstellers",country:'Not published',image:"assets/products/waterdrop-waterdrop-c1sl-alkalisches-tisch-umkehrosmoseanlage.webp",url:"products/waterdrop-waterdrop-c1sl-alkalisches-tisch-umkehrosmoseanlage.html"},
{id:"waterdrop-waterdrop-k19-hg-instant-hot-mineralisiertes-ro-wassersystem",brand:"Waterdrop",name:"K19-HG Instant Hot Mineralisiertes RO-Wassersystem",cat:"Countertop RO",price:"309,00 €",priceValue:309.0,features:[],ppb:null,flow:"75 GPD",maint:"Vor-/Nachfilter ca. 6–12 Monate; RO-Membran modellabhängig bis 24 Monate",liter:'—',membrane:"5-in-1-Filter mit RO, Erhitzung und Mineralisierung",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Ja, alkalische/mineralische Nachbehandlung",noise:'Not published',power:"Not published",warranty:"1 Jahr laut Vergleichstabelle des Herstellers",country:'Not published',image:"assets/products/waterdrop-waterdrop-k19-hg-instant-hot-mineralisiertes-ro-wassersystem.webp",url:"products/waterdrop-waterdrop-k19-hg-instant-hot-mineralisiertes-ro-wassersystem.html"},
{id:"waterdrop-waterdrop-remineralisierungs-ro-wasserspender-mit-heiss-kaltwasser-a2g",brand:"Waterdrop",name:"A2G Auftisch-Umkehrosmoseanlage mit Heiß- & Kaltwasser",cat:"Countertop RO",price:"509,00 €",priceValue:509.0,features:[],ppb:null,flow:"Nicht separat ver\u00f6ffentlicht",maint:"Vor-/Nachfilter ca. 6–12 Monate; RO-Membran modellabhängig bis 24 Monate",liter:'—',membrane:"6-stufige RO-Filtration mit alkalischer Remineralisierung",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Ja, alkalische/mineralische Nachbehandlung",noise:'Not published',power:"Not published",warranty:"1 Jahr laut Vergleichstabelle des Herstellers",country:'Not published',image:"assets/products/waterdrop-waterdrop-remineralisierungs-ro-wasserspender-mit-heiss-kaltwasser-a2g.webp",url:"products/waterdrop-waterdrop-remineralisierungs-ro-wasserspender-mit-heiss-kaltwasser-a2g.html"},
{id:"waterdrop-waterdrop-x-serie-umkehrosmose-system-x8-f2",brand:"Waterdrop",name:"X-Serie Umkehrosmose-System, X8-F2",cat:"Direct Flow RO",price:"826,99 €",priceValue:826.99,features:[],ppb:null,flow:"800 GPD",maint:"Vor-/Nachfilter ca. 6–12 Monate; RO-Membran modellabhängig bis 24 Monate",liter:'—',membrane:"9-stufig, RO-Membran 0,0001 µm",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Nein / nicht Bestandteil dieses Sets",noise:'Not published',power:"Not published",warranty:"1 Jahr laut Vergleichstabelle des Herstellers",country:'Not published',image:"assets/products/waterdrop-waterdrop-x-serie-umkehrosmose-system-x8-f2.webp",url:"products/waterdrop-waterdrop-x-serie-umkehrosmose-system-x8-f2.html"},
{id:"waterdrop-waterdrop-x8-tankloser-untertisch-umkehrosmose-wasserfilter-800-mit-f3-ersatzfilter",brand:"Waterdrop",name:"X8 Tankloser Untertisch Umkehrosmose Wasserfilter 800 GPD mit F3 Ersatzfilter",cat:"Direct Flow RO",price:"916,99 €",priceValue:916.99,features:[],ppb:null,flow:"800 GPD",maint:"Vor-/Nachfilter ca. 6–12 Monate; RO-Membran modellabhängig bis 24 Monate",liter:'—',membrane:"9-stufig, RO-Membran 0,0001 µm",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Nein / nicht Bestandteil dieses Sets",noise:'Not published',power:"Not published",warranty:"1 Jahr laut Vergleichstabelle des Herstellers",country:'Not published',image:"assets/products/waterdrop-waterdrop-x8-tankloser-untertisch-umkehrosmose-wasserfilter-800-mit-f3-ersatzfilter.webp",url:"products/waterdrop-waterdrop-x8-tankloser-untertisch-umkehrosmose-wasserfilter-800-mit-f3-ersatzfilter.html"},
{id:"arktisquelle-wasserfilter",brand:"Arktisquelle",name:"Wasserfilter",cat:"Countertop RO",price:"1.199,00 €",priceValue:1199.0,features:[],ppb:null,flow:"Not published",maint:"In weniger als 5 Minuten durch den Nutzer",liter:'—',membrane:"Molekularmembran / Umkehrosmose, 0,0001 µm",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/products/arktisquelle-wasserfilter.webp",url:"products/arktisquelle-wasserfilter.html"},
{id:"ho3-home-one",brand:"HO3 Filter",name:"Home One",cat:"Countertop RO",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Umkehrosmose; Filterleistung laut Hersteller nach NSF/ANSI 58 geprüft",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Einsetzbarer Mineralfilter",noise:'Not published',power:"2.200 W",warranty:"Not published",country:'Not published',image:"assets/products/ho3-home-one.webp",url:"products/ho3-home-one.html"},
{id:"aqua-global-1189",brand:"Aqua Global",name:"Mini Touch",cat:"Countertop RO",price:"795,00 €",priceValue:795.0,features:[],ppb:null,flow:"Not published",maint:"Composite 6–12 Monate; Postfilter 6–12 Monate; RO-Membran 12–24 Monate; UV 60 Monate",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/products/aqua-global-1189.webp",url:"products/aqua-global-mini-touch.html"},
{id:"aqua-global-1457",brand:"Aqua Global",name:"Mini Touch PRO – Black",cat:"Countertop RO",price:"1.195,00 €",priceValue:1195.0,features:[],ppb:null,flow:"Not published",maint:"Composite 6–12 Monate; RO-Membran 12–24 Monate; UV 60 Monate",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/products/aqua-global-1457.webp",url:"products/aqua-global-mini-touch-pro-black.html"},
{id:"aqua-global-1221",brand:"Aqua Global",name:"Basic",cat:"Direct Flow RO",price:"895,00 €",priceValue:895.0,features:[],ppb:null,flow:"Not published",maint:"PC-C 6–12 Monate; RO-Membran 18–36 Monate",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/products/aqua-global-1221.webp",url:"products/aqua-global-basic.html"},
{id:"aqua-global-1231",brand:"Aqua Global",name:"Sparkling",cat:"Water Dispenser",price:"1.795,00 €",priceValue:1795.0,features:[],ppb:null,flow:"Not published",maint:"Nano-Silver-Carbon 6–12 Monate; UV 6–12 Monate",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/products/aqua-global-1231.webp",url:"products/aqua-global-sparkling.html"},
{id:"aqua-global-1237",brand:"Aqua Global",name:"Sparkling Pro",cat:"Water Dispenser",price:"2.295,00 €",priceValue:2295.0,features:[],ppb:null,flow:"Not published",maint:"PC-C 6–12 Monate; RO-Membran 18–36 Monate; UV 6–12 Monate",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/products/aqua-global-1237.webp",url:"products/aqua-global-sparkling-pro.html"},
{id:"aqua-global-1193",brand:"Aqua Global",name:"Hydrogenflasche Glas schwarz",cat:"Hydrogen Bottles",price:"169,00 €",priceValue:169.0,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/products/aqua-global-1193.webp",url:"products/aqua-global-hydrogenflasche-glas-schwarz.html"},
{id:"bela-aqua-oblige-minerale-directflow-osmoseanlage",brand:"Bela Aqua",name:"Bela Aqua OBLIGE Minerale | Directflow-Osmoseanlage",cat:"Direct Flow RO",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/bela-aqua-oblige-minerale-directflow-osmoseanlage.webp",url:"products/bela-aqua-oblige-minerale-directflow-osmoseanlage.html"},
{id:"bela-aqua-evolution-classic-osmoseanlage-mit-tank",brand:"Bela Aqua",name:"Bela Aqua Evolution Classic | Osmoseanlage mit Tank",cat:"Direct Flow RO",price:"Preis auf Anfrage",priceValue:null,features:[],ppb:null,flow:"Not published",maint:"Gekapselte Quick-Filter mit Wasserstoppfunktion",liter:'—',membrane:"TFC ST-RO 75; 0,0001 µm",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/bela-aqua-evolution-classic-osmoseanlage-mit-tank.webp",url:"products/bela-aqua-evolution-classic-osmoseanlage-mit-tank.html"},
{id:"bela-aqua-hydrogen-trinkflasche",brand:"Bela Aqua",name:"Hydrogen Trinkflasche",cat:"Hydrogen Bottles",price:"97,00 €",priceValue:97.0,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/bela-aqua-hydrogen-trinkflasche.webp",url:"products/bela-aqua-hydrogen-trinkflasche.html"},
{id:"happyfilter-one-der-wasserspender-fuer-zuhause",brand:"HappyFilter",name:"HappyFilter One - DER Wasserspender für Zuhause",cat:"Water Dispenser",price:"1.090,00 €",priceValue:1090.0,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Heizleistung 2.200 W / Kühlleistung 100 W / 220–240 V / 50 Hz.",warranty:'Not published',country:'Germany',image:"assets/products/happyfilter-one-der-wasserspender-fuer-zuhause.webp",url:"products/happyfilter-one-der-wasserspender-fuer-zuhause.html"},
{id:"sprudelux-power-soda-premium-untertisch-sprudelanlage",brand:"SPRUDELUX",name:"SPRUDELUX® POWER SODA - Premium Untertisch-Sprudelanlage",cat:"Water Dispenser",price:"1.166,63 €",priceValue:1166.63,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"170 W / 0,75 A",warranty:'Not published',country:'Germany',image:"assets/products/sprudelux-power-soda-premium-untertisch-sprudelanlage.webp",url:"products/sprudelux-power-soda-premium-untertisch-sprudelanlage.html"},
{id:"sprudelux-inox-silent-premium-sprudelanlage-hoher-co2-gehalt-geraeuscharm-edelstahl",brand:"SPRUDELUX",name:"SPRUDELUX® INOX SILENT - Premium Sprudelanlage | hoher CO2 Gehalt | geräuscharm | Edelstahl",cat:"Water Dispenser",price:"1.237,90 €",priceValue:1237.9,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/sprudelux-inox-silent-premium-sprudelanlage-hoher-co2-gehalt-geraeuscharm-edelstahl.webp",url:"products/sprudelux-inox-silent-premium-sprudelanlage-hoher-co2-gehalt-geraeuscharm-edelstahl.html"},
{id:"sprudelux-juman-supreme-premium-umkehrosmoseanlage-mit-sprudel-heisswasserfunktion-quick-change",brand:"SPRUDELUX",name:"SPRUDELUX JUMAN SUPREME – Premium Umkehrosmoseanlage mit Sprudel & Heißwasserfunktion | Quick Change Filter & UVC-LED Technologie | mit Festwasseranschluss",cat:"Countertop RO",price:"849,95 €",priceValue:849.95,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/sprudelux-juman-supreme-premium-umkehrosmoseanlage-mit-sprudel-heisswasserfunktion-quick-change.webp",url:"products/sprudelux-juman-supreme-premium-umkehrosmoseanlage-mit-sprudel-heisswasserfunktion-quick-change.html"},
{id:"sprudelux-pro-touch-premium-umkehrosmoseanlage-mit-sprudel-heisswasserfunktion-quick-change",brand:"SPRUDELUX",name:"SPRUDELUX Pro Touch - Premium Umkehrosmoseanlage mit Sprudel & Heißwasserfunktion | Quick Change Filter & UVC-LED Technologie | Tank bzw. Festwasseranschluss",cat:"Countertop RO",price:"1.359,16 €",priceValue:1359.16,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"0,0001 Mikron",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/sprudelux-pro-touch-premium-umkehrosmoseanlage-mit-sprudel-heisswasserfunktion-quick-change.webp",url:"products/sprudelux-pro-touch-premium-umkehrosmoseanlage-mit-sprudel-heisswasserfunktion-quick-change.html"},
{id:"sprudelux-power-soda-premium-auftisch-sprudelanlage",brand:"SPRUDELUX",name:"SPRUDELUX® POWER SODA - Premium Auftisch-Sprudelanlage",cat:"Water Dispenser",price:"1.571,75 €",priceValue:1571.75,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/sprudelux-power-soda-premium-auftisch-sprudelanlage.webp",url:"products/sprudelux-power-soda-premium-auftisch-sprudelanlage.html"},
{id:"sprudelux-power-soda-osmose-premium-untertisch-sprudelanlage",brand:"SPRUDELUX",name:"SPRUDELUX® POWER SODA Osmose - Premium Untertisch-Sprudelanlage",cat:"Water Dispenser",price:"1.643,54 €",priceValue:1643.54,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"170 W / 0,75 A",warranty:'Not published',country:'Germany',image:"assets/products/sprudelux-power-soda-osmose-premium-untertisch-sprudelanlage.webp",url:"products/sprudelux-power-soda-osmose-premium-untertisch-sprudelanlage.html"},
{id:"sprudelux-nuovo-premium-umkehrosmoseanlage-hoher-co2-gehalt-geraeuscharm-edelstahl",brand:"SPRUDELUX",name:"SPRUDELUX® NUOVO - Premium Umkehrosmoseanlage | hoher CO2 Gehalt | geräuscharm | Edelstahl",cat:"Water Dispenser",price:"1.990,43 €",priceValue:1990.43,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/sprudelux-nuovo-premium-umkehrosmoseanlage-hoher-co2-gehalt-geraeuscharm-edelstahl.webp",url:"products/sprudelux-nuovo-premium-umkehrosmoseanlage-hoher-co2-gehalt-geraeuscharm-edelstahl.html"},
{id:"sprudelux-ultra-flat-premium-sprudelanlage-nur-10-5-cm-flach",brand:"SPRUDELUX",name:"SPRUDELUX® ULTRA FLAT - Premium Sprudelanlage | nur 10,5 cm flach | hoher CO2 Gehalt | geräuscharm | Edelstahl",cat:"Water Dispenser",price:"1.316,24 €",priceValue:1316.24,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/sprudelux-ultra-flat-premium-sprudelanlage-nur-10-5-cm-flach.webp",url:"products/sprudelux-ultra-flat-premium-sprudelanlage-nur-10-5-cm-flach.html"},
{id:"aora-gt600-umkehrosmose-wasserfilter-ohne-tank-1-57-l-min",brand:"AORA",name:"AORA GT600 Umkehrosmose Wasserfilter ohne Tank | 1,57 L/Min. Durchfluss | inkl. 3 Wege-Edelstahl- Wasserhahn | Quick Change Filter | geprüfte Qualität",cat:"Direct Flow RO",price:"314,55 €",priceValue:314.55,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/aora-gt600-umkehrosmose-wasserfilter-ohne-tank-1-57-l-min.webp",url:"products/aora-gt600-umkehrosmose-wasserfilter-ohne-tank-1-57-l-min.html"},
{id:"aora-w12-auftisch-osmoseanlage-mit-6-temperaturstufen-15-100-c",brand:"AORA",name:"AORA W12 Auftisch Osmoseanlage mit 6 Temperaturstufen (~15-100°C) | kein Wasseranschluss nötig | 5 stufige Filterung | kalkfreies Trinkwasser | Mobile Umkehrosmoseanlage",cat:"Countertop RO",price:"349,97 €",priceValue:349.97,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/aora-w12-auftisch-osmoseanlage-mit-6-temperaturstufen-15-100-c.webp",url:"products/aora-w12-auftisch-osmoseanlage-mit-6-temperaturstufen-15-100-c.html"},
{id:"aora-w23-auftisch-osmoseanlage-mit-6-temperaturstufen-15-100-c",brand:"AORA",name:"AORA W23 Auftisch Osmoseanlage mit 6 Temperaturstufen (~15-100°C) | mit Tank | 5 stufige Filterung | kalkfreies Trinkwasser | Mobile Umkehrosmoseanlage | Wasserstoff-Generator",cat:"Countertop RO",price:"499,76 €",priceValue:499.76,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/aora-w23-auftisch-osmoseanlage-mit-6-temperaturstufen-15-100-c.webp",url:"products/aora-w23-auftisch-osmoseanlage-mit-6-temperaturstufen-15-100-c.html"},
{id:"stillundlaut-home-soda-premium-untertisch-umkehrosmoseanlage-sprudel-kuehlung-nur-10",brand:"stillundlaut",name:"STILLUNDLAUT HOME SODA – Premium Untertisch-Umkehrosmoseanlage | Sprudel & Kühlung | nur 10 cm hoch | Edelstahl",cat:"Water Dispenser",price:"3.569,94 €",priceValue:3569.94,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/stillundlaut-home-soda-premium-untertisch-umkehrosmoseanlage-sprudel-kuehlung-nur-10.webp",url:"products/stillundlaut-home-soda-premium-untertisch-umkehrosmoseanlage-sprudel-kuehlung-nur-10.html"},
{id:"rowa-4-you-h2o-rowa-select-8-l-tank",brand:"ROWA 4 you",name:"H2O Rowa Select | 8 l Tank",cat:"Direct Flow RO",price:"1.450,00 €",priceValue:1450.0,features:[],ppb:null,flow:"ca. 90 l pro Tag bei 4 bar und 10°C (±15%) bzw. durchschnittlich 4,5 l/h, Verhältnis Konzentrat (Abwasser) zu Permeat (Reinwasser) 2:1 bis 3,5:1 (abhängig von Leitungsdruck)",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/rowa-4-you-h2o-rowa-select-8-l-tank.webp",url:"products/rowa-4-you-h2o-rowa-select-8-l-tank.html"},
{id:"rowa-4-you-h2o-economy-3-blue",brand:"ROWA 4 you",name:"H2O Economy 3+ blue",cat:"Drinking Water Filter",price:"1.150,00 €",priceValue:1150.0,features:[],ppb:null,flow:"ca. 90 l pro Tag bei 4 bar und 10°C (±15%) bzw. durchschnittlich 4,5 l/h, Verhältnis Konzentrat (Abwasser) zu Permeat (Reinwasser) 2:1 bis 3:1 (abhängig von Leitungsdruck)",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/rowa-4-you-h2o-economy-3-blue.webp",url:"products/rowa-4-you-h2o-economy-3-blue.html"},
{id:"wasserladen-wp-a01-all-in-one-umkehr-osmose-auftischfilter",brand:"Wasserladen",name:"WP-A01 | All in One Umkehr Osmose Auftischfilter",cat:"Countertop RO",price:"599,00 €",priceValue:599.0,features:[],ppb:null,flow:"Not published",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/wasserladen-wp-a01-all-in-one-umkehr-osmose-auftischfilter.webp",url:"products/wasserladen-wp-a01-all-in-one-umkehr-osmose-auftischfilter.html"},
{id:"carbonit-sanuno-classic",brand:"CARBONIT",name:"SANUNO Classic",cat:"Water Dispenser",price:"162,00 €",priceValue:162.0,features:[],ppb:null,flow:"ca. 120 Liter pro Stunde bei einem Wasserdruck von 4 bar und einer Wassertemperatur von 10°C. Zur Entnahme von Schadstoffen siehe Datenblatt Filterpatrone NFP Premium",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/carbonit-sanuno-classic.webp",url:"products/carbonit-sanuno-classic.html"},
{id:"carbonit-sanuno-grande-sparset",brand:"CARBONIT",name:"SANUNO Grande Sparset",cat:"Water Dispenser",price:"425,00 €",priceValue:425.0,features:[],ppb:null,flow:"ca. 120 Liter pro Stunde bei einem Wasserdruck von 4 bar und einer Wassertemperatur von 10°C. Zur Entnahme von Schadstoffen siehe Datenblatt Filterpatrone NFP Premium",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/carbonit-sanuno-grande-sparset.webp",url:"products/carbonit-sanuno-grande-sparset.html"},
{id:"osmotech-ultimate-plus-superflow",brand:"Osmotech",name:"Ultimate Plus Superflow",cat:"Direct Flow RO",price:"349,00 €",priceValue:349.0,features:[],ppb:null,flow:"5 Filterstufen",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/osmotech-ultimate-plus-superflow.webp",url:"products/osmotech-ultimate-plus-superflow.html"},
{id:"osmotech-ultimate-plus",brand:"Osmotech",name:"Ultimate Plus",cat:"Direct Flow RO",price:"299,00 €",priceValue:299.0,features:[],ppb:null,flow:"5 Filterstufen",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/osmotech-ultimate-plus.webp",url:"products/osmotech-ultimate-plus.html"},
{id:"osmotech-aquaristik-osmoseanlage-profi-50-gpd",brand:"Osmotech",name:"Aquaristik Osmoseanlage Profi 50 GPD",cat:"Direct Flow RO",price:"69,90 €",priceValue:69.9,features:[],ppb:null,flow:"3 Filterstufen",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/osmotech-aquaristik-osmoseanlage-profi-50-gpd.webp",url:"products/osmotech-aquaristik-osmoseanlage-profi-50-gpd.html"},
{id:"osmotech-aquaristik-osmoseanlage-hobby-50-gpd",brand:"Osmotech",name:"Aquaristik Osmoseanlage Hobby 50 GPD",cat:"Direct Flow RO",price:"49,90 €",priceValue:49.9,features:[],ppb:null,flow:"3 Filterstufen",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/osmotech-aquaristik-osmoseanlage-hobby-50-gpd.webp",url:"products/osmotech-aquaristik-osmoseanlage-hobby-50-gpd.html"},
{id:"sonvita-puraqua-touch",brand:"SONVITA",name:"Puraqua Touch",cat:"Direct Flow RO",price:"549,00 €",priceValue:549.0,features:[],ppb:null,flow:"4 Filterstufen",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/sonvita-puraqua-touch.webp",url:"products/sonvita-puraqua-touch.html"},
{id:"sonvita-aqua-smart-duo",brand:"SONVITA",name:"Aqua Smart Duo",cat:"Direct Flow RO",price:"399,00 €",priceValue:399.0,features:[],ppb:null,flow:"2 Filterstufen",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/sonvita-aqua-smart-duo.webp",url:"products/sonvita-aqua-smart-duo.html"},
{id:"sonvita-pura",brand:"SONVITA",name:"Pura",cat:"Direct Flow RO",price:"429,00 €",priceValue:429.0,features:[],ppb:null,flow:"3 Filterstufen",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/sonvita-pura.webp",url:"products/sonvita-pura.html"},
{id:"sonvita-aqua-quell",brand:"SONVITA",name:"Aqua Quell",cat:"Direct Flow RO",price:"229,00 €",priceValue:229.0,features:[],ppb:null,flow:"4 Filterstufen",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/sonvita-aqua-quell.webp",url:"products/sonvita-aqua-quell.html"},
{id:"sonvita-aqua-tower",brand:"SONVITA",name:"Aqua Tower",cat:"Direct Flow RO",price:"229,00 €",priceValue:229.0,features:[],ppb:null,flow:"2 Filterstufen",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/sonvita-aqua-tower.webp",url:"products/sonvita-aqua-tower.html"},
{id:"osmotech-vista",brand:"Osmotech",name:"Vista",cat:"Direct Flow RO",price:"239,00 €",priceValue:239.0,features:[],ppb:null,flow:"5 Filterstufen",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/osmotech-vista.webp",url:"products/osmotech-vista.html"},
{id:"sonvita-puraqua-max-800",brand:"SONVITA",name:"Puraqua Max 800",cat:"Direct Flow RO",price:"549,00 €",priceValue:549.0,features:[],ppb:null,flow:"2 Filterstufen",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/sonvita-puraqua-max-800.webp",url:"products/sonvita-puraqua-max-800.html"},
{id:"sonvita-aqua-smart-duo-evo-i",brand:"SONVITA",name:"Aqua Smart Duo evo I",cat:"Direct Flow RO",price:"499,00 €",priceValue:499.0,features:[],ppb:null,flow:"2 Filterstufen",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/sonvita-aqua-smart-duo-evo-i.webp",url:"products/sonvita-aqua-smart-duo-evo-i.html"},
{id:"sonvita-aqua-smart-duo-evo-ii",brand:"SONVITA",name:"Aqua Smart Duo evo II",cat:"Direct Flow RO",price:"449,00 €",priceValue:449.0,features:[],ppb:null,flow:"2 Filterstufen",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/sonvita-aqua-smart-duo-evo-ii.webp",url:"products/sonvita-aqua-smart-duo-evo-ii.html"},
{id:"sonvita-aqua-vita-90-gpd-weiss",brand:"SONVITA",name:"Aqua Vita 90 GPD | Weiß",cat:"Countertop RO",price:"379,00 €",priceValue:379.0,features:[],ppb:null,flow:"4 Filterstufen",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/sonvita-aqua-vita-90-gpd-weiss.webp",url:"products/sonvita-aqua-vita-90-gpd-weiss.html"},
{id:"sonvita-pura-up",brand:"SONVITA",name:"Pura Up",cat:"Countertop RO",price:"429,00 €",priceValue:429.0,features:[],ppb:null,flow:"3 Filterstufen",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/sonvita-pura-up.webp",url:"products/sonvita-pura-up.html"},
{id:"sonvita-aqua-vita-90-gpd-b-ware",brand:"SONVITA",name:"Aqua Vita 90 GPD B-Ware",cat:"Countertop RO",price:"279,00 €",priceValue:279.0,features:[],ppb:null,flow:"4 Filterstufen",maint:"Not published",liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:'Not published',noise:'Not published',power:"Not published",warranty:'Not published',country:'Germany',image:"assets/products/sonvita-aqua-vita-90-gpd-b-ware.webp",url:"products/sonvita-aqua-vita-90-gpd-b-ware.html"},
{id:"pentair-freshpoint-gro-350b",brand:"Pentair",name:"FreshPoint GRO-350B",cat:"Under-sink RO",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"50 GPD",maint:'Not published',liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/pentair.png",url:"products/pentair-freshpoint-gro-350b.html"},
{id:"pentek-dura-series-standard-filter-housing",brand:"Pentek",name:"Dura-Series Standard Filter Housing",cat:"Filter Housing",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"Not published",maint:'Not published',liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/pentek.png",url:"products/pentek-dura-series-standard-filter-housing.html"},
{id:"3m-3mro301",brand:"3M",name:"3MRO301",cat:"Under-sink RO",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"Not published",maint:'Not published',liter:'—',membrane:"Umkehrosmose",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/3m.png",url:"products/3m-3mro301.html"},
{id:"ao-smith-ao-us-ro-4000",brand:"A.O. Smith",name:"AO-US-RO-4000",cat:"Under-sink RO",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"50,4 l/Tag",maint:'Not published',liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/ao-smith.png",url:"products/ao-smith-ao-us-ro-4000.html"},
{id:"atlas-filtri-hydra-self-cleaning-1-npt",brand:"Atlas Filtri",name:"HYDRA Self-Cleaning 1″ NPT",cat:"Sediment Filter",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"Not published",maint:'Not published',liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/atlas-filtri.png",url:"products/atlas-filtri-hydra-self-cleaning-1-npt.html"},
{id:"kinetico-k5-drinking-water-station-with-voc-guard",brand:"Kinetico",name:"K5 Drinking Water Station with VOC Guard",cat:"Under-sink RO",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"bis 148 l/Tag",maint:'Not published',liter:'—',membrane:"Nicht-elektrische Umkehrosmose",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/kinetico.png",url:"products/kinetico-k5-drinking-water-station-with-voc-guard.html"},
{id:"aquaphor-ro-101s-morion",brand:"Aquaphor",name:"RO-101S Morion",cat:"Under-sink RO",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"Not published",maint:'Not published',liter:'—',membrane:"Umkehrosmose",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/aquaphor.png",url:"products/aquaphor-ro-101s-morion.html"},
{id:"ispring-rcc7ak",brand:"iSpring",name:"RCC7AK",cat:"Under-sink RO",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"75 GPD",maint:'Not published',liter:'—',membrane:"0,0001 µm",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Alkalische Stufe",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/ispring.png",url:"products/ispring-rcc7ak.html"},
{id:"apec-roes-50",brand:"APEC Water Systems",name:"ROES-50",cat:"Under-sink RO",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"50 GPD",maint:'Not published',liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/apec.png",url:"products/apec-roes-50.html"},
{id:"home-master-tmafc-artesian-full-contact",brand:"Home Master",name:"TMAFC Artesian Full Contact",cat:"Under-sink RO",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"50 GPD",maint:'Not published',liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Full Contact",noise:'Not published',power:"Not published",warranty:"5 Jahre",country:'Not published',image:"assets/brands/home-master.png",url:"products/home-master-tmafc-artesian-full-contact.html"},
{id:"express-water-ro5dx",brand:"Express Water",name:"RO5DX",cat:"Under-sink RO",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"50 GPD",maint:'Not published',liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/express-water.png",url:"products/express-water-ro5dx.html"},
{id:"purepro-ro-105",brand:"PurePro",name:"RO-105",cat:"Under-sink RO",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"50 GPD",maint:'Not published',liter:'—',membrane:"TFC",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/purepro.png",url:"products/purepro-ro-105.html"},
{id:"crystal-quest-thunder-1000c",brand:"Crystal Quest",name:"Thunder 1000C",cat:"Countertop RO",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"Not published",maint:'Not published',liter:'—',membrane:"Umkehrosmose",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/crystal-quest.png",url:"products/crystal-quest-thunder-1000c.html"},
{id:"canature-cro-400ux1",brand:"Canature",name:"CRO-400UX1",cat:"Direct Flow RO",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"400 GPD",maint:'Not published',liter:'—',membrane:"Tanklose Umkehrosmose",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/canature.png",url:"products/canature-cro-400ux1.html"},
{id:"aquatru-classic-countertop-purifier",brand:"AquaTru",name:"Classic Countertop Purifier",cat:"Countertop RO",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"Not published",maint:'Not published',liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/aquatru.png",url:"products/aquatru-classic-countertop-purifier.html"},
{id:"coway-neo-plus-chp-264l",brand:"Coway",name:"Neo Plus CHP-264L",cat:"Water Dispenser",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"Not published",maint:'Not published',liter:'—',membrane:"RO-Membran bis 0,4 nm",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/coway.png",url:"products/coway-neo-plus-chp-264l.html"},
{id:"lg-puricare-self-service-tankless-water-purifier",brand:"LG",name:"PuriCare Self-Service Tankless Water Purifier",cat:"Direct Flow RO",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"Not published",maint:'Not published',liter:'—',membrane:"Mehrstufige Direktfiltration",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/lg.png",url:"products/lg-puricare-self-service-tankless-water-purifier.html"},
{id:"panasonic-tk-as500",brand:"Panasonic",name:"TK-AS500",cat:"Water Ionizer",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"Not published",maint:'Not published',liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/panasonic.png",url:"products/panasonic-tk-as500.html"},
{id:"philips-add6910-ro-water-station",brand:"Philips",name:"ADD6910 RO Water Station",cat:"Countertop RO",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"Not published",maint:'Not published',liter:'—',membrane:"Umkehrosmose",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/philips.png",url:"products/philips-add6910-ro-water-station.html"},
{id:"xiaomi-mijia-smart-water-purifier-n800g",brand:"Xiaomi",name:"Mijia Smart Water Purifier N800G",cat:"Direct Flow RO",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"2 l/min",maint:'Not published',liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"75 W",warranty:"Not published",country:'Not published',image:"assets/brands/xiaomi.png",url:"products/xiaomi-mijia-smart-water-purifier-n800g.html"},
{id:"viomi-kunlun-ai-mineral-water-purifier",brand:"Viomi",name:"Kunlun AI Mineral Water Purifier",cat:"Direct Flow RO",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"Not published",maint:'Not published',liter:'—',membrane:"KI-gestützte Wasseraufbereitung",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Mineralwasser-Funktion",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/viomi.png",url:"products/viomi-kunlun-ai-mineral-water-purifier.html"},
{id:"angel-a7-home-water-purifier",brand:"Angel",name:"A7 Home Water Purifier",cat:"Direct Flow RO",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"Not published",maint:'Not published',liter:'—',membrane:"Mehrstufige Wasseraufbereitung",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/angel.png",url:"products/angel-a7-home-water-purifier.html"},
{id:"qinyuan-krl5006",brand:"Qinyuan",name:"KRL5006",cat:"Direct Flow RO",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"Not published",maint:'Not published',liter:'—',membrane:"Umkehrosmose",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/qinyuan.svg",url:"products/qinyuan-krl5006.html"},
{id:"midea-jetpure-cwrc600-a106",brand:"Midea",name:"JetPure CWRC600-A106",cat:"Direct Flow RO",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"600 GPD",maint:'Not published',liter:'—',membrane:"Umkehrosmose",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/midea.png",url:"products/midea-jetpure-cwrc600-a106.html"},
{id:"haier-hro12h69-su1",brand:"Haier",name:"HRO12H69-SU1",cat:"Direct Flow RO",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"Not published",maint:'Not published',liter:'—',membrane:"Umkehrosmose",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/haier.png",url:"products/haier-hro12h69-su1.html"},
{id:"tyent-hybrid-h2-water-ionizer",brand:"Tyent",name:"Hybrid H2 Water Ionizer",cat:"Water Ionizer",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"Not published",maint:'Not published',liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Lebenslange Herstellergarantie",country:'Not published',image:"assets/brands/tyent.png",url:"products/tyent-hybrid-h2-water-ionizer.html"},
{id:"lourdes-hydrofix-premium-edition",brand:"Lourdes",name:"Hydrofix Premium Edition",cat:"Hydrogen Generator",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"Not published",maint:'Not published',liter:'—',membrane:"Elektrolyse / Wasserstoffwasser",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/lourdes.png",url:"products/lourdes-hydrofix-premium-edition.html"},
{id:"fujiiryoki-hwp-77-water-purifier",brand:"Fujiiryoki",name:"HWP-77 Water Purifier",cat:"Water Ionizer",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"Not published",maint:'Not published',liter:'—',membrane:"Elektrolytische Wasseraufbereitung",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/fujiiryoki.png",url:"products/fujiiryoki-hwp-77-water-purifier.html"},
{id:"dupont-filmtec-bw30-pro-400",brand:"DuPont",name:"FilmTec BW30 PRO-400",cat:"RO Membrane",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"Not published",maint:'Not published',liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/dupont.png",url:"products/dupont-filmtec-bw30-pro-400.html"},
{id:"hydranautics-espa2-ld",brand:"Hydranautics",name:"ESPA2-LD",cat:"RO Membrane",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"Not published",maint:'Not published',liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/hydranautics.png",url:"products/hydranautics-espa2-ld.html"},
{id:"toray-tm720d-400",brand:"Toray",name:"TM720D-400",cat:"RO Membrane",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"Not published",maint:'Not published',liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/toray.png",url:"products/toray-tm720d-400.html"},
{id:"lg-water-solutions-lg-bw-400-r-g2-most",brand:"LG Water Solutions",name:"LG BW 400 R G2 MOST",cat:"RO Membrane",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"Not published",maint:'Not published',liter:'—',membrane:"Not published",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/lg-water-solutions.png",url:"products/lg-water-solutions-lg-bw-400-r-g2-most.html"},
{id:"koch-separation-puron-mp-mbr-module",brand:"Koch Separation Solutions",name:"PURON MP MBR Module",cat:"Membrane Bioreactor",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"Not published",maint:'Not published',liter:'—',membrane:"Hohlfaser-Ultrafiltration",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/koch-separation.png",url:"products/koch-separation-puron-mp-mbr-module.html"},
{id:"veolia-sirion-advanced",brand:"Veolia Water Technologies",name:"Sirion Advanced",cat:"Commercial RO",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"bis 5.000 l/h",maint:'Not published',liter:'—',membrane:"Umkehrosmose",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/veolia.png",url:"products/veolia-sirion-advanced.html"},
{id:"suez-ak4040tm",brand:"SUEZ Water Technologies",name:"AK4040TM",cat:"RO Membrane",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"Not published",maint:'Not published',liter:'—',membrane:"Niederdruck-RO-Membran",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/suez.png",url:"products/suez-ak4040tm.html"},
{id:"grundfos-aqpure",brand:"Grundfos",name:"AQpure",cat:"Ultrafiltration System",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"0,5–2 m³/h",maint:'Not published',liter:'—',membrane:"PVDF-Hohlfaser",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/grundfos.png",url:"products/grundfos-aqpure.html"},
{id:"vontron-ulp21-4040",brand:"Vontron",name:"ULP21-4040",cat:"RO Membrane",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"Not published",maint:'Not published',liter:'—',membrane:"Ultra-Low-Pressure RO",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/vontron.png",url:"products/vontron-ulp21-4040.html"},
{id:"lanxess-lewabrane-b400-hr",brand:"LANXESS",name:"Lewabrane B400 HR",cat:"RO Membrane",price:'Preis auf Anfrage',priceValue:null,features:[],ppb:null,flow:"Not published",maint:'Not published',liter:'—',membrane:"Brackwasser-RO-Membran",pfas:'Not published',viruses:'Not published',bacteria:'Not published',nitrates:'Not published',lead:'Not published',arsenic:'Not published',micro:'Not published',tds:'Not published',remin:"Not published",noise:'Not published',power:"Not published",warranty:"Not published",country:'Not published',image:"assets/brands/lanxess.png",url:"products/lanxess-lewabrane-b400-hr.html"}
];

function storageGet(key,fallback){try{const v=localStorage.getItem(key);return v===null?fallback:v}catch(e){return fallback}}
function storageSet(key,value){try{localStorage.setItem(key,value)}catch(e){}}
let selected=[];
try{selected=JSON.parse(storageGet('wasserCompare','[]'))||[]}catch(e){selected=[]}
selected=selected.filter(id=>products.some(product=>product.id===id));
storageSet('wasserCompare',JSON.stringify(selected));
const isComparePage=/(^|\/)compare(?:\.html)?\/?$/.test(location.pathname);
let compareDockActivated=isComparePage;
let compareDockDismissed=false;
const lang=()=>storageGet('wasserLang','de');
const tr=(de,en)=>lang()==='de'?de:en;
function basePrefix(){const parts=location.pathname.split('/').filter(Boolean);return '../'.repeat(Math.max(0,parts.length-1))}
function save(){storageSet('wasserCompare',JSON.stringify(selected));renderDock()}
function addCompare(id){compareDockActivated=true;compareDockDismissed=false;if(selected.includes(id)){selected=selected.filter(x=>x!==id)}else{if(selected.length>=3){alert(tr('Es können maximal 3 Geräte verglichen werden','You can compare a maximum of 3 devices'));return}selected.push(id)}save()}
function ensureCompareDock(){
 let dock=document.querySelector('.compare-dock');if(!dock){dock=document.createElement('div');dock.className='compare-dock';document.body.appendChild(dock)}dock.setAttribute('aria-live','polite');
 dock.innerHTML=`<button class="compare-dock-close" type="button" data-compare-close aria-label="${tr('Vergleichsleiste schließen','Close comparison bar')}">×</button><div class="compare-dock-summary"><strong>${tr('Vergleich','Compare')} <span class="count">0/3</span></strong><div class="compare-items"></div></div><button class="btn primary small compare-dock-action" type="button" data-go-compare>${tr('Jetzt vergleichen','Compare now')}</button>`;
}
function renderDock(){ensureCompareDock();const dock=document.querySelector('.compare-dock');if(!dock)return;document.querySelectorAll('[data-compare]').forEach(button=>{const active=selected.includes(button.dataset.compare);button.classList.toggle('is-selected',active);button.setAttribute('aria-pressed',String(active))});if(!selected.length||!compareDockActivated||compareDockDismissed){dock.classList.remove('show');return}dock.classList.add('show');dock.querySelector('.compare-items').innerHTML=selected.map(id=>{const p=products.find(x=>x.id===id);return p?`<div class="compare-mini"><span>${p.brand} ${p.name}</span><button type="button" data-compare-remove="${p.id}" aria-label="${tr('Aus Vergleich entfernen','Remove from comparison')}">×</button></div>`:''}).join('');dock.querySelector('.count').textContent=`${selected.length}/3`}
function goCompare(){location.href=basePrefix()+'compare.html'}

function ensureMobileNavigation(){
 document.querySelectorAll('.site-header').forEach(header=>{
  const shell=header.querySelector('.header-shell');if(!shell)return;
  let tools=shell.querySelector('.header-tools');if(!tools){tools=document.createElement('div');tools.className='header-tools';shell.appendChild(tools)}
  let menuButton=shell.querySelector('.mobile-menu-btn');if(!menuButton){menuButton=document.createElement('button');menuButton.className='icon-btn mobile-menu-btn';menuButton.type='button';menuButton.setAttribute('aria-expanded','false');menuButton.setAttribute('aria-label',tr('Menü öffnen','Open menu'));menuButton.textContent='☰'}if(menuButton.parentElement!==tools)tools.appendChild(menuButton)
  if(!header.querySelector('.mobile-nav-panel')){const panel=document.createElement('div');panel.className='mobile-nav-panel';panel.setAttribute('aria-hidden','true');const prefix=basePrefix();panel.innerHTML=`<div class="container mobile-nav-inner"><a href="${prefix}products.html">${tr('Produkte','Products')}</a><a href="${prefix}brands.html">${tr('Marken','Brands')}</a><a href="${prefix}compare.html">${tr('Vergleichen','Compare')}</a><a href="${prefix}hydrogen-bottles.html">Hydrogenflaschen</a><a href="${prefix}community.html">Community</a><a href="${prefix}knowledge.html">${tr('Wissen','Knowledge')}</a></div>`;header.appendChild(panel)}
 });
}
function linkProductCardImages(root=document){
 root.querySelectorAll('.product-card[data-product-id]').forEach(card=>{
  const photo=card.querySelector(':scope > .photo');if(!photo)return;
  const product=products.find(item=>item.id===card.dataset.productId);if(!product?.url)return;
  const link=document.createElement('a');link.className='product-photo-link';link.href=basePrefix()+product.url;link.setAttribute('aria-label',`${product.brand} ${product.name} – ${tr('Produktseite öffnen','Open product page')}`);
  photo.replaceWith(link);link.appendChild(photo);
 });
}
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
  ensureMobileNavigation();
  ensureCompareDock();
  renderDock();
  setupSearchClearButtons();
  setupBrandSearch();
  initComparePage();
  setupGeneralAutocomplete();
  setupProductsQueryFilter();
  linkProductCardImages();
  document.addEventListener('click',event=>{
    const compareButton=event.target.closest('[data-compare]');if(compareButton){event.preventDefault();addCompare(compareButton.dataset.compare);return}
    const removeButton=event.target.closest('[data-compare-remove]');if(removeButton){event.preventDefault();compareDockDismissed=false;selected=selected.filter(id=>id!==removeButton.dataset.compareRemove);save();return}
    if(event.target.closest('[data-compare-close]')){compareDockDismissed=true;renderDock();return}
    if(event.target.closest('[data-go-compare]'))goCompare();
  });
});


const productRatingSeed={
 pearl:{average:5,count:5},hydro:{average:4.5,count:22}
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
   if(summary){summary.classList.add('rating-line');summary.innerHTML=result.count?`${ratingStars(result.average)} <strong>${result.average.toFixed(2)}</strong><span>${result.count} ${tr('Bewertungen','reviews')}</span>`:`<span class="rating-empty">${tr('Noch keine Nutzerbewertung','No user ratings yet')}</span>`}
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
function setupHydrogenProductLayout(){
 const file=location.pathname.split('/').pop();
 const product=products.find(item=>item.url?.split('/').pop()===file&&item.cat==='Hydrogen Bottles');
 if(!product)return;
 const container=document.querySelector('main > .container');
 const details=container?.querySelector(':scope > section.panel');
 if(!container||!details||container.querySelector(':scope > .content-grid'))return;
 const brandLink=document.querySelector('.product-brand-link');
 const grid=document.createElement('div');
 grid.className='content-grid';
 details.insertAdjacentElement('beforebegin',grid);
 grid.appendChild(details);
 const aside=document.createElement('aside');
 const brandValue=brandLink?`<a href="${brandLink.getAttribute('href')}">${product.brand}</a>`:product.brand;
 aside.innerHTML=`<div class="panel"><h3 style="margin-top:0">${tr('Einordnung','Classification')}</h3><table class="spec-table"><tr><td>${tr('Marke','Brand')}</td><td>${brandValue}</td></tr><tr><td>${tr('Kategorie','Category')}</td><td>Hydrogen Bottle</td></tr><tr><td>${tr('Preisstatus','Price status')}</td><td>${product.price}</td></tr></table></div><div class="panel" style="margin-top:14px"><h3 style="margin-top:0">${tr('Hinweis','Note')}</h3><p>${tr('Hydrogenflaschen dienen der Anreicherung von Wasser mit molekularem Wasserstoff und ersetzen keine Trinkwasserfiltration.','Hydrogen bottles enrich water with molecular hydrogen and do not replace drinking-water filtration.')}</p></div>`;
 grid.appendChild(aside);
}
function setupWaterTestBanner(){
 if(!/\/products\/[^/]+\.html$/.test(location.pathname))return;
 const aside=document.querySelector('.content-grid > aside');
 if(!aside||aside.querySelector('.water-test-banner'))return;
 const banner=document.createElement('a');
 banner.className='water-test-banner';
 banner.href='https://wasserfiltercheck.de';
 banner.target='_blank';
 banner.rel='noopener';
 banner.setAttribute('aria-label',tr('Wasser selbst testen – wasserfiltercheck.de öffnen','Test your water – open wasserfiltercheck.de'));
 banner.innerHTML=`<img src="${basePrefix()}assets/img/wasserfiltercheck-banner.png" alt="${tr('Senden Sie eine Anfrage oder testen Sie Ihr Wasser selbst','Send an inquiry or test your water yourself')}" loading="lazy" decoding="async">`;
 aside.appendChild(banner);
}
document.addEventListener('DOMContentLoaded',()=>{setupHydrogenProductLayout();setupReviewSystem();setupHelpfulButtons();setupWaterTestBanner()});


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
    document.addEventListener('click',event=>{
      const btn=event.target.closest('.mobile-menu-btn');
      if(!btn)return;
      const header=btn.closest('.site-header');
      const panel=header && header.querySelector('.mobile-nav-panel');
      if(!panel) return;
      const open=panel.classList.toggle('open');
      panel.setAttribute('aria-hidden',String(!open));
      btn.setAttribute('aria-expanded',String(open));
      btn.setAttribute('aria-label',open?tr('Menü schließen','Close menu'):tr('Menü öffnen','Open menu'));
      btn.textContent=open?'×':'☰';
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

const hydrogenBrandPages={
 'WALUTEC':'walutec','BLACKWATER':'blackwater','PIURIFY':'piurify','Echo Water':'echo-water',
 'ionBottles':'ionbottles','Level Up Way':'level-up-way','AlkaViva':'alkaviva'
};
function hydrogenBrandPage(brand){const slug=hydrogenBrandPages[brand];return slug?`brands/${slug}.html`:''}

function injectHydrogenCatalogCards(){
 const grid=document.querySelector('.filters-layout .product-grid');
 if(!grid)return;
 products.filter(product=>product.cat==='Hydrogen Bottles').forEach(product=>{
  if(grid.querySelector(`[data-product-id="${product.id}"]`))return;
  const card=document.createElement('div');
  card.className='product-card';card.dataset.productId=product.id;
  const brandUrl=hydrogenBrandPage(product.brand);
  card.innerHTML=`<div class="photo"><img alt="${product.brand} ${product.name}" src="${product.image}"></div>${brandUrl?`<a class="brand" href="${brandUrl}">${product.brand}</a>`:`<div class="brand">${product.brand}</div>`}<h3>${product.name}</h3><div class="rating"></div><div class="price">${product.price}</div><div class="specs"><span>${product.flow} · ${product.membrane}</span><span>${product.ppb?`bis ${new Intl.NumberFormat('de-DE').format(product.ppb)} PPB`:'H₂-Wert nicht veröffentlicht'}</span><span>${product.warranty}</span></div><div class="actions"><a class="btn small" href="${product.url}">Alle Daten</a><button class="btn small" data-compare="${product.id}">+ Compare</button></div>`;
  grid.appendChild(card);
 });
}
injectHydrogenCatalogCards();

function injectHydrogenBrands(){
 const grid=document.querySelector('.brand-directory-grid');if(!grid)return;
 [
  {slug:'ionbottles',name:'ionBottles',country:'USA',logo:'assets/brands/ionbottles.svg',text:'Portable PEM-Hydrogenflaschen mit digitalen Funktionen und Labordaten.'},
  {slug:'level-up-way',name:'Level Up Way',country:'USA',logo:'assets/brands/level-up-way.svg',text:'Kompakte Hydrogen-Wassergeräte und Wellnessprodukte.'}
 ].forEach(brand=>{if(grid.querySelector(`[href="brands/${brand.slug}.html"]`))return;const card=document.createElement('a');card.className='brand-directory-card';card.href=`brands/${brand.slug}.html`;card.dataset.brandName=brand.name.toLowerCase();card.dataset.brandCountry=brand.country.toLowerCase();card.innerHTML=`<div class="brand-logo-wrap"><img src="${brand.logo}" alt="${brand.name} Logo" loading="lazy"></div><div class="brand-card-body"><span class="badge">Hydrogen Water</span><h3>${brand.name}</h3><p>${brand.text}</p><span class="brand-meta">${brand.country} · 1 Modell</span><span class="brand-link">Profil ansehen →</span></div>`;grid.appendChild(card)});
}
injectHydrogenBrands();
