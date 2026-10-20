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
    nav.querySelectorAll('.has-sub > button').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var li = btn.parentElement;
        var open = li.classList.toggle('is-open');
        btn.setAttribute('aria-expanded', open);
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
