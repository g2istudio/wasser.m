const fs=require('fs'),path=require('path');
const file=path.resolve(__dirname,'../products/blackwater-pearl.html');
let html=fs.readFileSync(file,'utf8');
html=html.replace(/product\.css\?v=[^"]+/,'product.css?v=20260718-reviews1');
if(!html.includes('class="panel sample-reviews"')){
 const reviews=[
  ['Beispielprofil A','2026-02-12','12.02.2026','Endlich kein Flaschen schleppen mehr','Seit knapp drei Monaten steht die Pearl bei uns in der Küche und wir benutzen sie wirklich jeden Tag. Das kalte Wasser ist angenehm frisch und für Tee nehme ich direkt die heiße Stufe. Bedienung ist sehr einfach und das Wasser schmeckt neutral, sogar die Kinder trinken jetzt mehr. Bis jetzt sind wir sehr zufrieden damit.'],
  ['Beispielprofil B','2026-03-29','29.03.2026','Passt gut in unsere kleine Küche','Ich hatte erst bedenken wegen der Größe, aber das Gerät passt gut neben die Kaffeemaschine. Man muss nichts fest einbauen und wir konnten sofort anfangen. Das Display versteht man schnell und die verschiedenen Mengen sind praktisch. Besonders morgens spart es mir viel Zeit, weil heißes Wasser sofort da ist.'],
  ['Beispielprofil C','2026-05-17','17.05.2026','Teuer, aber im Alltag sehr überzeugend','Der Preis ist schon hoch, das war für mich die einzige schwache Seite und ich habe lange überlegt. Nach einigen Wochen möchte ich die Pearl trotzdem nicht mehr missen. Wasser schmeckt sehr gut, die Kühlung funktioniert ordentlich und beim Kochen ist die Heißwasserfunktion super bequem. Verarbeitung macht auch einen stabilen Eindruck.'],
  ['Beispielprofil D','2026-07-03','03.07.2026','Leise und unkompliziert im täglichen Gebrauch','Wir wollten eine Osmoseanlage ohne Umbau an der Spüle und haben deshalb dieses Modell genommen. Aufstellen, Tank füllen und es ging los. Beim filtern hört man sie natürlich ein bisschen, aber es stört uns nicht. Die Reinigung geht schnell und alle in Familie kommen mit der Bedienung klar. Für uns eine gute Entscheidung.']
 ];
 const cards=reviews.map(([name,date,machineDate,title,text])=>`<article class="sample-review-card"><header><div><strong>${name}</strong><span>Beispielbewertung · nicht verifiziert</span></div><time datetime="${date}">${machineDate}</time></header><div class="sample-stars" aria-label="5 von 5 Sternen">★★★★★ <b>5,0</b></div><h3>${title}</h3><p>${text}</p></article>`).join('');
 const section=`<section class="panel sample-reviews" aria-labelledby="sample-reviews-title"><div class="sample-reviews-head"><div><span class="badge">Beispielinhalte</span><h2 id="sample-reviews-title">Kommentare zur BLACKWATER Pearl</h2><p>Die folgenden Texte sind redaktionell erstellte Beispielbewertungen und keine verifizierten Kundenmeinungen. Der deutsche Originaltext wird in jeder Sprachversion unverändert angezeigt.</p></div><div class="sample-rating-summary"><strong>5,0</strong><span>★★★★★</span><small>4 Beispielbewertungen</small></div></div><div class="sample-review-grid" lang="de" translate="no">${cards}</div></section>`;
 html=html.replace('<section class="panel product-knowledge-links">',section+'<section class="panel product-knowledge-links">');
}
fs.writeFileSync(file,html);
console.log('BLACKWATER Pearl sample reviews added.');
