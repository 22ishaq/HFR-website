// nav.js — shared navigation injected into every page
(function() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navHTML = `
    <nav id="navbar">
        <a href="index.html" class="nav-logo-link">
            <img src="hfr.jpg" alt="HFR Logo" class="nav-logo-img">
        </a>
        <ul class="nav-links" id="nav-links">
            <li><a href="index.html" class="${currentPage === 'index.html' ? 'active' : ''}">Home</a></li>
            <li class="has-dropdown">
                <a href="about.html" class="${currentPage === 'about.html' ? 'active' : ''}">About <span class="arrow">▾</span></a>
                <ul class="dropdown">
                    <li><a href="about.html#mission">Our Mission</a></li>
                    <li><a href="about.html#achievements">Achievements</a></li>
                    <li><a href="about.html#timeline">Timeline</a></li>
                    <li><a href="about.html#team">The Team</a></li>
                </ul>
            </li>
            <li class="has-dropdown">
                <a href="divisions.html" class="${currentPage === 'divisions.html' ? 'active' : ''}">Divisions <span class="arrow">▾</span></a>
                <ul class="dropdown">
                    <li><a href="divisions.html#land">Land Division</a></li>
                    <li><a href="divisions.html#sea">Sea Division</a></li>
                    <li><a href="competitions.html">Competitions</a></li>
                </ul>
            </li>
            <li class="has-dropdown">
                <a href="events.html" class="${currentPage === 'events.html' ? 'active' : ''}">Events <span class="arrow">▾</span></a>
                <ul class="dropdown">
                    <li><a href="events.html#lectures">Lecture Series</a></li>
                    <li><a href="events.html#outreach">Outreach</a></li>
                    <li><a href="events.html#socials">Socials</a></li>
                    <li><a href="events.html#tours">Site Tours</a></li>
                </ul>
            </li>
            <li><a href="sponsors.html" class="${currentPage === 'sponsors.html' ? 'active' : ''}">Sponsors</a></li>
            <li><a href="shop.html" class="${currentPage === 'shop.html' ? 'active' : ''}">Shop</a></li>
            <li><a href="register.html" class="nav-cta ${currentPage === 'register.html' ? 'active' : ''}">Join Us</a></li>
        </ul>
        <div class="hamburger" id="hamburger">
            <span></span><span></span><span></span>
        </div>
    </nav>
    `;

    // Insert at top of body
    document.body.insertAdjacentHTML('afterbegin', navHTML);

    // Hamburger toggle
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('nav-links');
    hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('open');
        hamburger.classList.toggle('open');
    });

    // Scroll effect
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        navbar.classList.toggle('scrolled', window.scrollY > 50);
    });

    // Close dropdown on outside click
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.has-dropdown')) {
            document.querySelectorAll('.dropdown').forEach(d => d.classList.remove('show'));
        }
    });

    // Dropdown toggle on click (mobile) / hover handled by CSS
    document.querySelectorAll('.has-dropdown > a').forEach(link => {
        link.addEventListener('click', (e) => {
            if (window.innerWidth <= 768) {
                e.preventDefault();
                const dropdown = link.nextElementSibling;
                dropdown.classList.toggle('show');
            }
        });
    });
})();
