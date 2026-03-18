// shared.js — footer injection, cursor, reveal animations

(function() {
    // ── CURSOR ──
    const cur = document.createElement('div'); cur.className = 'cursor'; cur.id = 'cursor';
    const ring = document.createElement('div'); ring.className = 'cursor-ring'; ring.id = 'cursor-ring';
    document.body.appendChild(cur); document.body.appendChild(ring);
    let mx = 0, my = 0, rx = 0, ry = 0;
    document.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; });
    (function animCursor() {
        cur.style.cssText = `left:${mx-5}px;top:${my-5}px`;
        rx += (mx - rx) * 0.14; ry += (my - ry) * 0.14;
        ring.style.cssText = `left:${rx-17}px;top:${ry-17}px`;
        requestAnimationFrame(animCursor);
    })();
    document.querySelectorAll('a,button,.card,.division-card,.event-card,.shop-item,.comp-item').forEach(el => {
        el.addEventListener('mouseenter', () => { ring.style.transform = 'scale(2)'; ring.style.opacity = '0.25'; });
        el.addEventListener('mouseleave', () => { ring.style.transform = 'scale(1)'; ring.style.opacity = '0.5'; });
    });

    // ── REVEAL ON SCROLL ──
    const io = new IntersectionObserver(entries => {
        entries.forEach((e, i) => {
            if (e.isIntersecting) {
                setTimeout(() => e.target.classList.add('visible'), i * 80);
                io.unobserve(e.target);
            }
        });
    }, { threshold: 0.08 });
    document.querySelectorAll('.reveal').forEach(el => io.observe(el));

    // ── FOOTER ──
    const footerHTML = `
    <div class="ticker-wrap">
        <div class="ticker-track">
            <span class="ticker-item">Shell Eco-Marathon 2026 ◆</span>
            <span class="ticker-item">Monaco Energy Boat Challenge ◆</span>
            <span class="ticker-item">University of Glasgow ◆</span>
            <span class="ticker-item">Hydrogen Fuel Cell Technology ◆</span>
            <span class="ticker-item">Zero Emission Motorsport ◆</span>
            <span class="ticker-item">Applications Open 2026 ◆</span>
            <span class="ticker-item">Shell Eco-Marathon 2026 ◆</span>
            <span class="ticker-item">Monaco Energy Boat Challenge ◆</span>
            <span class="ticker-item">University of Glasgow ◆</span>
            <span class="ticker-item">Hydrogen Fuel Cell Technology ◆</span>
            <span class="ticker-item">Zero Emission Motorsport ◆</span>
            <span class="ticker-item">Applications Open 2026 ◆</span>
        </div>
    </div>
    <footer class="site-footer">
        <div class="footer-inner">
            <div class="footer-top">
                <div class="footer-brand">
                    <div class="logo-text">UG<span>HFR</span></div>
                    <p>UG Hydrogen Fuel Racing — pioneering zero-emission motorsport at the University of Glasgow. Competing at Shell Eco-Marathon and the Monaco Energy Boat Challenge.</p>
                </div>
                <div class="footer-col">
                    <h5>Navigate</h5>
                    <ul>
                        <li><a href="index.html">Home</a></li>
                        <li><a href="about.html">About</a></li>
                        <li><a href="divisions.html">Divisions</a></li>
                        <li><a href="competitions.html">Competitions</a></li>
                        <li><a href="events.html">Events</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h5>Team</h5>
                    <ul>
                        <li><a href="about.html#team">Meet the Team</a></li>
                        <li><a href="register.html">Join Us</a></li>
                        <li><a href="sponsors.html">Sponsors</a></li>
                        <li><a href="shop.html">Shop</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h5>Contact</h5>
                    <ul>
                        <li><a href="mailto:hfr@glasgow.ac.uk">hfr@glasgow.ac.uk</a></li>
                        <li><a href="#">Instagram</a></li>
                        <li><a href="#">LinkedIn</a></li>
                        <li><a href="https://www.gla.ac.uk" target="_blank">University of Glasgow</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>© 2026 UG Hydrogen Fuel Racing · University of Glasgow · All rights reserved.</p>
                <div class="footer-socials">
                    <a href="#" class="social-link">in</a>
                    <a href="#" class="social-link">ig</a>
                    <a href="#" class="social-link">tw</a>
                </div>
            </div>
        </div>
    </footer>`;
    document.body.insertAdjacentHTML('beforeend', footerHTML);
})();
