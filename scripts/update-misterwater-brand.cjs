const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');
const files=['brands.html','brands/mrwater.html','products.html','products/mrwater-premium-ro.html','data/brands.json','data/products.json','data/catalog-additions.json','assets/app.js','scripts/refresh-official-catalog.mjs'];
for(const relative of files){
 const file=path.join(root,relative);let text=fs.readFileSync(file,'utf8');
 text=text.replaceAll('misterwater®','MisterWater').replaceAll('MrWater','MisterWater');
 if(relative==='brands.html'||relative==='brands/mrwater.html'||relative==='data/brands.json')text=text.replaceAll('assets/brands/mrwater.png','assets/brands/misterwater-logo-white.png').replaceAll('../assets/brands/mrwater.png','../assets/brands/misterwater-logo-white.png');
 if(relative==='brands.html')text=text.replace('data-brand-name="mrwater"','data-brand-name="misterwater"').replace('<div class="brand-logo-wrap"><img src="assets/brands/misterwater-logo-white.png"','<div class="brand-logo-wrap misterwater-logo-surface"><img src="assets/brands/misterwater-logo-white.png"');
 if(relative==='brands/mrwater.html')text=text.replace('<div class="brand-hero-logo"><img src="../assets/brands/misterwater-logo-white.png"','<div class="brand-hero-logo misterwater-logo-surface"><img src="../assets/brands/misterwater-logo-white.png"');
 if(relative==='brands.html'||relative==='brands/mrwater.html')text=text.replace(/brand\.css\?v=[^"]+/,'brand.css?v=20260720-misterwater1');
 fs.writeFileSync(file,text);
}
console.log('Updated MisterWater naming and official logo references.');
