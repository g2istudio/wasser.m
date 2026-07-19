(()=>{
  const key='wasserProfessionalReviews';
  const read=()=>{try{return JSON.parse(localStorage.getItem(key)||'{}')}catch(error){return {}}};
  const save=value=>{try{localStorage.setItem(key,JSON.stringify(value))}catch(error){}}
  const escape=value=>String(value||'').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  let activeId='';

  function render(id){
    const list=document.querySelector(`[data-professional-reviews="${id}"]`);if(!list)return;
    const reviews=read()[id]||[];
    list.querySelectorAll('.professional-review.is-local').forEach(item=>item.remove());
    reviews.forEach(review=>{
      const article=document.createElement('article');article.className='professional-review is-local';
      article.innerHTML=`<header><strong>${escape(review.name||'Anonym')}</strong><span>${'★'.repeat(review.rating)}${'☆'.repeat(5-review.rating)} ${review.rating},0</span></header><p>${escape(review.comment)}</p><small>Lokale Bewertung · in diesem Browser gespeichert · ${new Date(review.date).toLocaleDateString('de-DE')}</small>`;
      list.appendChild(article);
    });
  }

  function ensureModal(){
    let modal=document.querySelector('.professional-review-modal');if(modal)return modal;
    modal=document.createElement('div');modal.className='professional-review-modal';
    modal.innerHTML=`<div class="professional-review-dialog" role="dialog" aria-modal="true" aria-labelledby="professional-review-title"><button class="professional-review-close" type="button" aria-label="Schließen">×</button><h2 id="professional-review-title">Fachbetrieb bewerten</h2><p data-professional-dialog-name></p><form><label>Ihr Name<input name="name" maxlength="60" placeholder="Optional"></label><label>Bewertung<select name="rating" required><option value="">Bitte wählen</option><option value="5">5 – Ausgezeichnet</option><option value="4">4 – Gut</option><option value="3">3 – In Ordnung</option><option value="2">2 – Verbesserungswürdig</option><option value="1">1 – Schlecht</option></select></label><label>Ihre Erfahrung<textarea name="comment" rows="5" maxlength="1000" required placeholder="Wie waren Beratung, Termin, Ausführung und Preis?"></textarea></label><label class="review-consent"><input type="checkbox" required> Ich bestätige, dass diese Bewertung auf meiner eigenen Erfahrung basiert.</label><button class="btn primary" type="submit">Bewertung speichern</button><p class="professional-review-note">Demoversion: Die Bewertung wird nur in diesem Browser gespeichert und nicht öffentlich übertragen.</p></form></div>`;
    document.body.appendChild(modal);
    modal.querySelector('.professional-review-close').addEventListener('click',()=>modal.classList.remove('show'));
    modal.addEventListener('click',event=>{if(event.target===modal)modal.classList.remove('show')});
    modal.querySelector('form').addEventListener('submit',event=>{
      event.preventDefault();const form=event.currentTarget;const store=read();store[activeId]=store[activeId]||[];
      store[activeId].push({name:form.name.value.trim(),rating:Number(form.rating.value),comment:form.comment.value.trim(),date:new Date().toISOString()});
      save(store);render(activeId);form.reset();modal.classList.remove('show');
    });
    return modal;
  }

  document.querySelectorAll('[data-professional-reviews]').forEach(list=>render(list.dataset.professionalReviews));
  document.addEventListener('click',event=>{
    const button=event.target.closest('[data-professional-review]');if(!button)return;
    activeId=button.dataset.professionalReview;const modal=ensureModal();
    modal.querySelector('[data-professional-dialog-name]').textContent=button.dataset.professionalName;
    modal.classList.add('show');modal.querySelector('[name="rating"]').focus();
  });
})();
