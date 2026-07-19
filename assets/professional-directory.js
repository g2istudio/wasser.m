(()=>{
  const city=document.querySelector('[data-professional-city]');
  const specialty=document.querySelector('[data-professional-specialty]');
  const cards=[...document.querySelectorAll('[data-professional-directory-card]')];
  const count=document.querySelector('[data-professional-result-count]');
  const empty=document.querySelector('[data-professional-empty]');
  if(!cards.length)return;
  function apply(){
    const cityQuery=(city?.value||'').trim().toLowerCase();
    const specialtyQuery=(specialty?.value||'').toLowerCase();
    let visible=0;
    cards.forEach(card=>{
      const show=(!cityQuery||card.dataset.city.includes(cityQuery))&&(!specialtyQuery||card.dataset.specialties.includes(specialtyQuery));
      card.hidden=!show;if(show)visible++;
    });
    if(count)count.textContent=String(visible);if(empty)empty.hidden=visible!==0;
  }
  city?.addEventListener('input',apply);specialty?.addEventListener('change',apply);
  document.querySelector('[data-professional-reset]')?.addEventListener('click',()=>{if(city)city.value='';if(specialty)specialty.value='';apply();city?.focus()});
})();
