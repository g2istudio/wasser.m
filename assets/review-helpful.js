(()=>{
  const storageKey='wasserHelpfulReviews';
  const read=()=>{try{return JSON.parse(localStorage.getItem(storageKey)||'{}')}catch(error){return {}}};
  const write=value=>{try{localStorage.setItem(storageKey,JSON.stringify(value))}catch(error){}}
  const votes=read();

  function render(){
    document.querySelectorAll('[data-review-helpful]').forEach(button=>{
      const id=button.dataset.reviewHelpful;
      const active=Boolean(votes[id]);
      const count=button.querySelector('[data-helpful-count]');
      button.classList.toggle('is-active',active);
      button.setAttribute('aria-pressed',String(active));
      if(count)count.textContent=active?'1':'0';
    });
    document.querySelectorAll('.sample-review-grid').forEach(grid=>{
      [...grid.querySelectorAll('[data-review-card]')]
        .sort((a,b)=>Number(Boolean(votes[b.dataset.reviewCard]))-Number(Boolean(votes[a.dataset.reviewCard])))
        .forEach(card=>grid.appendChild(card));
    });
  }

  document.addEventListener('click',event=>{
    const button=event.target.closest('[data-review-helpful]');
    if(!button)return;
    const id=button.dataset.reviewHelpful;
    if(votes[id])delete votes[id];else votes[id]=true;
    write(votes);
    render();
  });
  render();
})();
