// nav.js — wireframe-style top hamburger + centred HFR home logo + two-panel overlay menu
(function () {
  if (document.getElementById('navbar')) return;

  const menuData = {
    fleet: {
      label: 'OUR FLEET',
      items: [
        { text: 'SHELL ECO 27', href: 'divisions.html#land', align: 'left', type: 'media' },
        { text: 'VITAL SPARK', href: 'divisions.html#sea', align: 'right', type: 'media' },
        { text: 'AERO DIVISION CONCEPT', href: 'divisions.html#air', align: 'left', type: 'media' }
      ]
    },
    divisions: {
      label: 'DIVISIONS',
      items: [
        { text: 'AUTOMOTIVE', href: 'divisions.html#automotive', align: 'left', type: 'media' },
        { text: 'AERONAUTICAL', href: 'divisions.html#aeronautical', align: 'right', type: 'media' },
        { text: 'NAUTICAL', href: 'divisions.html#nautical', align: 'left', type: 'media' }
      ]
    },
    partners: {
      label: 'PARTNERS',
      items: [
        { text: '2026 PARTNERS', href: 'sponsors.html', align: 'left', type: 'media' },
        { text: 'SUPPORT US', href: 'sponsors.html#support', align: 'right', type: 'media' }
      ]
    },
    store: {
      label: 'STORE',
      items: [
        { text: '2026 COMPETITION DROP', href: 'shop.html#drop', align: 'left', type: 'media' },
        { text: 'HFR STORE', href: 'shop.html', align: 'right', type: 'media' }
      ]
    },
    discover: {
      label: 'DISCOVER',
      items: [
        { text: 'MISSION', href: 'about.html#mission', align: 'left', type: 'media' },
        { text: 'HISTORY', href: 'about.html#history', align: 'right', type: 'media' },
        { text: 'EVENTS', href: 'events.html', align: 'left', type: 'media' }
      ]
    },
    join: {
      label: 'JOIN US',
      items: [
        { text: 'WHY JOIN HFR?', href: 'register.html#why', align: 'left', type: 'outline' },
        { text: 'REGISTER INTEREST', href: 'register.html', align: 'left', type: 'outline gold' }
      ]
    }
  };

  const nav = document.createElement('nav');
  nav.id = 'navbar';
  nav.innerHTML = `
    <button class="nav-menu-open" type="button" aria-label="Open navigation menu" aria-controls="site-menu-overlay" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>

    <a href="index.html" class="nav-home-logo" aria-label="Hydrogen Fuel Racing home">
      <img src="/static/core/hfr.jpg" alt="HFR">
    </a>

    <a href="register.html" class="nav-avatar-link" aria-label="Register">
      <img src="/static/core/avatar.jpg" alt="Register">
    </a>
  `;

  const overlay = document.createElement('div');
  overlay.id = 'site-menu-overlay';
  overlay.className = 'site-menu-overlay';
  overlay.setAttribute('aria-hidden', 'true');
  overlay.innerHTML = `
    <aside class="menu-main-panel" aria-label="Navigation categories">
      <button class="menu-close" type="button" aria-label="Close navigation menu"><span></span>Close</button>
      <ul class="menu-main-list">
        ${Object.entries(menuData).map(([key, group], index) => `
          <li>
            <button class="menu-main-option ${index === 0 ? 'active' : ''}" type="button" data-menu-key="${key}">
              <span>${group.label}</span><b>›</b>
            </button>
          </li>`).join('')}
      </ul>
    </aside>
    <main class="menu-sub-panel" aria-live="polite">
      <div class="menu-wash" aria-hidden="true"><span class="menu-wash-text"></span></div>
      <div class="menu-sub-inner" id="menu-sub-inner"></div>
    </main>
  `;

  document.body.prepend(overlay);
  document.body.prepend(nav);

  const openBtn = nav.querySelector('.nav-menu-open');
  const closeBtn = overlay.querySelector('.menu-close');
  const optionBtns = overlay.querySelectorAll('.menu-main-option');
  const subInner = overlay.querySelector('#menu-sub-inner');
  const wash = overlay.querySelector('.menu-wash');
  const washText = overlay.querySelector('.menu-wash-text');
  let washTimer = null;

  function renderSubMenu(key) {
    const group = menuData[key];
    subInner.innerHTML = `
      <div class="menu-sub-heading">
        <span>Hydrogen Fuel Racing</span>
        <h2>${group.label}</h2>
      </div>
      <div class="menu-sub-items">
        ${group.items.map(item => `
          <a href="${item.href}" class="menu-sub-card ${item.type || ''}">
            <span class="menu-sub-card-label">${group.label}</span>
            <strong class="${item.align === 'right' ? 'align-right' : ''}">${item.text}</strong>
          </a>`).join('')}
      </div>
    `;
  }

  function setActive(key, animate) {
    optionBtns.forEach(btn => btn.classList.toggle('active', btn.dataset.menuKey === key));
    if (!animate) {
      renderSubMenu(key);
      return;
    }
    washText.textContent = menuData[key].label;
    wash.classList.add('show');
    window.clearTimeout(washTimer);
    washTimer = window.setTimeout(() => {
      renderSubMenu(key);
      wash.classList.remove('show');
    }, 420);
  }

  function openMenu() {
    overlay.classList.add('open');
    overlay.setAttribute('aria-hidden', 'false');
    openBtn.setAttribute('aria-expanded', 'true');
    document.body.classList.add('menu-is-open');
    setActive('fleet', false);
    closeBtn.focus();
  }

  function closeMenu() {
    overlay.classList.remove('open');
    overlay.setAttribute('aria-hidden', 'true');
    openBtn.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('menu-is-open');
    openBtn.focus();
  }

  optionBtns.forEach(btn => btn.addEventListener('click', () => setActive(btn.dataset.menuKey, true)));
  openBtn.addEventListener('click', openMenu);
  closeBtn.addEventListener('click', closeMenu);

  overlay.addEventListener('click', (event) => {
    if (event.target.matches('.menu-sub-card, .menu-sub-card *')) closeMenu();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && overlay.classList.contains('open')) closeMenu();
  });

  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 12);
  });
})();
