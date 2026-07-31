(function () {
  if (document.getElementById('hfr-rail')) return;

  const sections = {
    divisions: { label: 'Divisions', cards: [
      { title: 'LAND', href: '/divisions/#land' },
      { title: 'SEA',  href: '/divisions/#sea' },
      { title: 'AIR',  href: '/divisions/#air' }
    ]},
    partners: { label: 'Partners', cards: [
      { title: '2026 PARTNERS', href: '/sponsors/' },
      { title: 'SUPPORT US',    href: '/sponsors/#support' }
    ]},
    discover: { label: 'Discover', cards: [
      { title: 'OUR MISSION', href: '/about/#mission' },
      { title: 'EVENTS',      href: '/events/' },
      { title: 'HISTORY',     href: '/about/#history' }
    ]},
    join: { label: 'Join Us', cards: [
      { title: 'JOINING THE TEAM', href: '/register/#why' },
      { title: 'CREATE ACCOUNT',   href: '/accounts/signup/' },
      { title: 'LOG IN',           href: '/accounts/login/' },
      { title: 'MY APPLICATION',   href: '/apply/' }
    ]}
  };
  const rail = document.createElement('aside');
  rail.id = 'hfr-rail';
  rail.className = 'hfr-rail';
  rail.innerHTML = `
    <button class="hfr-burger" type="button" aria-label="Toggle menu">
      <span></span><span></span><span></span>
    </button>
    <nav class="hfr-rail-nav">
      ${Object.entries(sections).map(([key, s]) =>
        `<a href="#" data-key="${key}">${s.label}</a>`).join('')}
    </nav>
  `;

  const panel = document.createElement('div');
  panel.id = 'hfr-panel';
  panel.className = 'hfr-panel';
  panel.setAttribute('aria-hidden', 'true');
  panel.innerHTML = `
    <button class="hfr-panel-close" type="button" aria-label="Close">&times;</button>
    <div class="hfr-cards" id="hfr-cards"></div>
    <div class="hfr-wash" aria-hidden="true"><span class="hfr-wash-text"></span></div>
  `;

  document.body.appendChild(panel);
  document.body.appendChild(rail);
  document.body.classList.add('hfr-has-rail');

  const navLinks = rail.querySelectorAll('.hfr-rail-nav a');
  const burger   = rail.querySelector('.hfr-burger');
  const closeBtn = panel.querySelector('.hfr-panel-close');
  const cardsBox = panel.querySelector('#hfr-cards');
  const wash     = panel.querySelector('.hfr-wash');
  const washText = panel.querySelector('.hfr-wash-text');
  let washTimer  = null;

  function renderCards(key) {
    cardsBox.innerHTML = sections[key].cards.map(c =>
      `<a class="hfr-card" href="${c.href}">
         <span class="hfr-card-title">${c.title}</span>
       </a>`).join('');
  }

  function openPanel() {
    panel.classList.add('open');
    panel.setAttribute('aria-hidden', 'false');
    document.body.classList.add('hfr-panel-open');
  }

  function closePanel() {
    panel.classList.remove('open');
    panel.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('hfr-panel-open');
    navLinks.forEach(a => a.classList.remove('active'));
  }

  function selectSection(key) {
    navLinks.forEach(a => a.classList.toggle('active', a.dataset.key === key));
    openPanel();
    washText.textContent = sections[key].label;
    wash.classList.add('show');
    clearTimeout(washTimer);
    washTimer = setTimeout(() => {
      renderCards(key);
      wash.classList.remove('show');
    }, 420);
  }

  navLinks.forEach(a => a.addEventListener('click', e => {
    e.preventDefault();
    selectSection(a.dataset.key);
  }));

  burger.addEventListener('click', () => {
    if (panel.classList.contains('open')) closePanel();
  });
  closeBtn.addEventListener('click', closePanel);
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && panel.classList.contains('open')) closePanel();
  });
})();