(function() {
  const langSwitch = document.querySelector('.language-switch');
  if (!langSwitch) return;

  const buttons = langSwitch.querySelectorAll('button');
  const langBlocks = document.querySelectorAll('.lang-block');
  const langInlines = document.querySelectorAll('.lang-inline');

  function switchLang(lang) {
    buttons.forEach(btn => {
      btn.classList.toggle('is-active', btn.dataset.switchLang === lang);
    });

    langBlocks.forEach(block => {
      block.classList.toggle('is-active', block.dataset.lang === lang);
    });

    langInlines.forEach(inline => {
      inline.classList.toggle('is-active', inline.dataset.lang === lang);
    });

    localStorage.setItem('orion-lang', lang);
  }

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      switchLang(btn.dataset.switchLang);
    });
  });

  const savedLang = localStorage.getItem('orion-lang') || 'en';
  switchLang(savedLang);

  const yearEl = document.querySelector('[data-year]');
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }
})();

(function createConstellation() {
  function initConstellation() {
    if (!document.body) {
      setTimeout(initConstellation, 10);
      return;
    }

    // Verificar se já existe uma layer (evitar duplicatas)
    const existing = document.querySelector('.constellation-layer');
    if (existing) {
      existing.remove();
    }

    const layer = document.createElement('div');
    layer.className = 'constellation-layer';
    document.body.insertBefore(layer, document.body.firstChild);

    const numStars = 200;
    const stars = [];
    const constellationGroups = 10;

    for (let i = 0; i < numStars; i++) {
      const star = document.createElement('div');
      const rand = Math.random();
      star.className = 'star';
      
      if (rand > 0.88) {
        star.className += ' bright';
      } else if (rand < 0.35) {
        star.className += ' faint';
      }

      const x = Math.random() * 100;
      const y = Math.random() * 100;
      
      star.style.left = x + '%';
      star.style.top = y + '%';
      star.style.animationDelay = Math.random() * 3 + 's';
      
      layer.appendChild(star);
      stars.push({ element: star, x, y });
    }

    for (let g = 0; g < constellationGroups; g++) {
      const groupSize = 4 + Math.floor(Math.random() * 5);
      const groupStars = [];
      const centerX = Math.random() * 80 + 10;
      const centerY = Math.random() * 80 + 10;

      for (let s = 0; s < groupSize; s++) {
        const x = centerX + (Math.random() - 0.5) * 20;
        const y = centerY + (Math.random() - 0.5) * 20;
        
        if (x >= 0 && x <= 100 && y >= 0 && y <= 100) {
          groupStars.push({ x, y });
        }
      }

      for (let i = 0; i < groupStars.length - 1; i++) {
        const start = groupStars[i];
        const end = groupStars[i + 1];
        
        if (Math.random() > 0.3) {
          const line = document.createElement('div');
          line.className = 'constellation-line';
          
          const dx = end.x - start.x;
          const dy = end.y - start.y;
          const distance = Math.sqrt(dx * dx + dy * dy);
          const angle = Math.atan2(dy, dx) * 180 / Math.PI;
          
          line.style.width = distance + '%';
          line.style.left = start.x + '%';
          line.style.top = start.y + '%';
          line.style.transform = `rotate(${angle}deg)`;
          line.style.animationDelay = Math.random() * 6 + 's';
          
          layer.appendChild(line);
        }
      }
    }

    console.log('Constellation layer created with', numStars, 'stars and', constellationGroups, 'constellation groups');
  }

  // Garantir que execute quando o DOM estiver pronto
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initConstellation);
  } else {
    // Se já carregou, executar imediatamente
    setTimeout(initConstellation, 100);
  }
})();
