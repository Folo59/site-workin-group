// Workin Group — scripts communs (menu mobile, carrousels, cookies + Google Analytics)
(function () {
  // Menu mobile
  var burger = document.querySelector('.burger');
  var nav = document.querySelector('.nav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', open);
      document.body.style.overflow = open ? 'hidden' : '';
    });
    // sur téléphone, le premier appui ouvre le sous-menu au lieu de changer de page
    nav.querySelectorAll('.has-sub > .nav__top').forEach(function (a) {
      a.addEventListener('click', function (e) {
        if (window.innerWidth > 960) return;
        e.preventDefault();
        var li = a.parentElement;
        var open = li.classList.toggle('is-open');
        a.setAttribute('aria-expanded', open);
      });
    });
  }

  // Carrousels
  document.querySelectorAll('[data-carousel]').forEach(function (root) {
    var track = root.querySelector('.carousel__track');
    var prev = root.querySelector('.carousel__btn--prev');
    var next = root.querySelector('.carousel__btn--next');
    function step() { var c = track.firstElementChild; return c ? c.getBoundingClientRect().width + 20 : 300; }
    function update() {
      prev.disabled = track.scrollLeft < 5;
      next.disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 5;
    }
    prev.addEventListener('click', function () { track.scrollBy({ left: -step(), behavior: 'smooth' }); });
    next.addEventListener('click', function () { track.scrollBy({ left: step(), behavior: 'smooth' }); });
    track.addEventListener('scroll', update, { passive: true });
    update();
  });

  // Cookies : Google Analytics ne se charge qu'après accord (RGPD)
  var GA_ID = 'GT-NMKV8NB';
  var KEY = 'workin-cookies';
  function loadGA() {
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag('js', new Date());
    gtag('config', GA_ID);
  }
  var choice = null;
  try { choice = localStorage.getItem(KEY); } catch (e) {}
  var banner = document.querySelector('.cookies');
  if (choice === 'yes') loadGA();
  if (banner && !choice) {
    banner.hidden = false;
    banner.addEventListener('click', function (e) {
      var v = e.target.getAttribute('data-consent');
      if (!v) return;
      try { localStorage.setItem(KEY, v); } catch (err) {}
      banner.hidden = true;
      if (v === 'yes') loadGA();
    });
  }
})();

// Formulaire de contact : envoi sans recharger la page
(function () {
  var form = document.getElementById('formulaire');
  if (!form || form.tagName !== 'FORM') return;
  var msg = form.querySelector('.form__msg');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!form.checkValidity()) { form.reportValidity(); return; }
    var btn = form.querySelector('button[type=submit]');
    btn.disabled = true; btn.textContent = 'Envoi en cours…';
    fetch(form.action, { method: 'POST', body: new FormData(form) })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function () {
        form.reset();
        msg.hidden = false;
        msg.textContent = 'Merci, votre demande est bien envoyée. Un conseiller vous rappelle sous 24 heures ouvrées.';
        btn.textContent = 'Demande envoyée';
        if (window.gtag) gtag('event', 'generate_lead', { form: 'contact_entreprises' });
      })
      .catch(function () {
        msg.hidden = false;
        msg.textContent = "L'envoi n'a pas fonctionné. Écrivez-nous à loic@workin-group.com ou appelez le +1 438 788 2995.";
        btn.disabled = false; btn.textContent = 'Envoyer ma demande';
      });
  });
})();

// Mouvements discrets : en-tête qui s'ombre au défilement, apparitions, compteurs
(function () {
  var header = document.querySelector('.header');
  if (header) {
    var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 10); };
    window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  }
  var root = document.querySelector('.has-motion');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!root || reduce || !window.requestAnimationFrame) return;

  var groups = [
    '.section-head', '.section .wrap > .eyebrow', '.section .wrap > h2', '.section .wrap > .lead',
    '.stat', '.compare__card', '.cards-2 > .card', '.pledge', '.step', '.carousel__track > .sector',
    '.permit', '.review', '.candidates', '.faq details', '.final .btn-row', '.final p', '.reviews-foot', '.carousel-foot',
    '.grid > .box', '.split__media', '.split .prose > *', '.stack > .prose > *', '.stack > .checklist', '.stack > .chips',
    '.toc', '.quote', '.sources', '.logo-grid', '.contact-grid > *', '.hero--plain .hero__text'
  ];
  var items = [];
  groups.forEach(function (sel) {
    root.querySelectorAll(sel).forEach(function (el) {
      if (el.closest('.hero') || el.hasAttribute('data-reveal') || el.closest('[data-reveal]')) return;
      var sib = Array.prototype.indexOf.call(el.parentNode.children, el);
      el.setAttribute('data-reveal', '');
      el.style.setProperty('--d', Math.min(sib, 6));
      items.push(el);
    });
  });
  var steps = root.querySelector('.steps');
  if (steps) items.push(steps);
  document.documentElement.classList.add('motion-ready');

  // compteurs des chiffres clés
  function countUp(el) {
    var raw = el.textContent.trim();
    if (!/^\d{1,4}$/.test(raw) || el.dataset.counted) return;
    var target = parseInt(raw, 10);
    if (!target) return;
    el.dataset.counted = '1';
    var from = target > 1000 ? target - 25 : 0, start = null, dur = 1400;
    function tick(t) {
      if (!start) start = t;
      var p = Math.min((t - start) / dur, 1), e = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(from + (target - from) * e);
      if (p < 1) requestAnimationFrame(tick); else el.textContent = target;
    }
    requestAnimationFrame(tick);
  }

  // dans les rangées qui défilent horizontalement, on suit la rangée entière
  var ROWS = '.carousel__track, .cards-2, .pledges, .grid, .stats, .reviews, .compare';
  var watched = [];
  items.forEach(function (el) {
    var row = el.parentElement && el.parentElement.matches(ROWS) ? el.parentElement : null;
    var target = row || el;
    if (watched.indexOf(target) === -1) watched.push(target);
  });

  function reveal(target) {
    var els = target.hasAttribute('data-reveal') ? [target] : Array.prototype.slice.call(target.children).filter(function (c) { return c.hasAttribute('data-reveal'); });
    els.forEach(function (el) {
      el.classList.add('is-in');
      var n = el.matches('.stat') && el.querySelector('strong');
      if (n) countUp(n);
    });
  }
  // tout ce qui est passé au-dessus du bas de l'écran apparaît (même après un défilement rapide)
  var ticking = false;
  function check() {
    ticking = false;
    var limit = window.innerHeight - 30;
    for (var i = watched.length - 1; i >= 0; i--) {
      if (watched[i].getBoundingClientRect().top < limit) { reveal(watched[i]); watched.splice(i, 1); }
    }
    if (!watched.length) { window.removeEventListener('scroll', onScrollReveal); window.removeEventListener('resize', onScrollReveal); }
  }
  function onScrollReveal() { if (!ticking) { ticking = true; requestAnimationFrame(check); } }
  window.addEventListener('scroll', onScrollReveal, { passive: true });
  window.addEventListener('resize', onScrollReveal);
  requestAnimationFrame(check);

  // filet de sécurité : tout s'affiche même si un élément n'a pas été détecté
  setTimeout(function () { items.forEach(function (el) { el.classList.add('is-in'); }); }, 6000);
})();

// Cartes entièrement cliquables quand elles ne mènent qu'à une seule page
(function () {
  document.querySelectorAll('.card, .box, .sector, .review').forEach(function (card) {
    var links = card.querySelectorAll('a[href]');
    var hrefs = {};
    links.forEach(function (a) { hrefs[a.getAttribute('href')] = a; });
    var keys = Object.keys(hrefs);
    if (keys.length !== 1) return;
    var main = card.querySelector('h3 a') || hrefs[keys[0]];
    card.classList.add('is-clickable');
    main.classList.add('stretched');
  });
})();
