/* Lumière du Soleil — moteur de prototype (navigation + interactions)
   Délégation d'événements globale : robuste au rendu des Design Components. */
(function () {
  var FILES = {
    'synthèse': 'Dashboard principal.dc.html',
    'projets': 'Liste des projets.dc.html',
    'saisie réalisation': 'Formulaire rapport.dc.html',
    'calendrier': 'Calendrier Gantt.dc.html'
  };
  function go(url) {
    if (!url) return;
    // En version autonome téléchargée (.html), pointer vers les fichiers .html
    if (!/\.dc\.html$/.test(window.location.pathname)) {
      url = url.replace(/\.dc\.html$/, '.html');
    }
    window.location.href = url;
  }

  // ---------- clics ----------
  document.addEventListener('click', function (e) {
    var t = e.target;

    var nav = t.closest('[data-nav]');
    if (nav) { e.preventDefault(); go(nav.getAttribute('data-nav')); return; }

    var sf = t.closest('[data-statusfilter]');
    if (sf) { filterStatus(sf); return; }

    var tab = t.closest('[data-tab]');
    if (tab) { switchTab(tab); return; }

    var role = t.closest('[data-role]');
    if (role) { switchRole(role); return; }

    var side = t.closest('.navd');
    if (side) {
      var key = side.textContent.trim().toLowerCase();
      if (FILES[key]) { e.preventDefault(); go(FILES[key]); }
      return;
    }

    var row = t.closest('.prow');
    if (row) { go('Fiche projet.dc.html'); return; }
  });

  // ---------- Liste : filtres de statut ----------
  function filterStatus(el) {
    var group = el.parentElement.querySelectorAll('[data-statusfilter]');
    group.forEach(function (g) {
      var active = g === el;
      g.style.background = active ? 'var(--surface-cream-strong)' : 'transparent';
      g.style.color = active ? 'var(--ink)' : 'var(--muted)';
      g.style.fontWeight = active ? '600' : '500';
    });
    var val = el.getAttribute('data-statusfilter');
    var rows = document.querySelectorAll('.prow');
    var shown = 0;
    rows.forEach(function (r) {
      var ok = val === 'all' || r.getAttribute('data-status') === val;
      r.style.display = ok ? '' : 'none';
      if (ok) shown++;
    });
    var counter = document.querySelector('[data-rowcount]');
    if (counter) counter.textContent = shown + ' projet' + (shown > 1 ? 's' : '') + ' sur 5';
  }

  // ---------- Fiche : onglets ----------
  function switchTab(el) {
    var tabs = document.querySelectorAll('[data-tab]');
    tabs.forEach(function (tb) {
      var active = tb === el;
      tb.style.color = active ? 'var(--ink)' : 'var(--muted)';
      tb.style.fontWeight = active ? '600' : '500';
      tb.style.borderBottom = active ? '2px solid var(--coral)' : '2px solid transparent';
      tb.style.marginBottom = '-1px';
    });
    var key = el.getAttribute('data-tab');
    var target = key === 'apercu' || key === 'rapports'
      ? null
      : document.querySelector('[data-section="' + key + '"]');
    var y = target ? target.getBoundingClientRect().top + window.scrollY - 90 : 0;
    window.scrollTo({ top: y, behavior: 'smooth' });
  }

  // ---------- Dashboard : rôle ----------
  function switchRole(el) {
    var group = el.parentElement.querySelectorAll('[data-role]');
    group.forEach(function (g) {
      var active = g === el;
      g.style.background = active ? '#fff' : 'transparent';
      g.style.color = active ? 'var(--ink)' : 'var(--muted)';
      g.style.fontWeight = active ? '600' : '400';
      g.style.boxShadow = active ? '0 1px 2px rgba(0,0,0,.05)' : 'none';
    });
  }

  // ---------- Formulaire : recalcul automatique du taux ----------
  function colorFor(taux) {
    if (taux >= 90) return { txt: '#2f7d44', dot: '#5db872', key: 'green' };
    if (taux >= 70) return { txt: '#9a6a1f', dot: '#e8a55a', key: 'amber' };
    return { txt: '#b23b3b', dot: '#c64545', key: 'red' };
  }
  function num(v) { return parseFloat(String(v).replace(',', '.').replace(/\s/g, '')); }

  function recompute() {
    var inputs = document.querySelectorAll('input.num[data-cible]');
    if (!inputs.length) return;
    var counts = { green: 0, amber: 0, red: 0 };
    var sum = 0, n = 0;
    inputs.forEach(function (inp) {
      var cible = num(inp.getAttribute('data-cible'));
      var real = num(inp.value);
      if (!isFinite(cible) || cible === 0 || !isFinite(real)) return;
      var taux = Math.round((real / cible) * 100);
      var c = colorFor(taux);
      var span = inp.nextElementSibling; // cellule "Taux"
      if (span) { span.textContent = taux + ' %'; span.style.color = c.txt; }
      var row = inp.parentElement;
      if (row) row.style.background = taux < 70 ? 'rgba(198,69,69,.035)' : '';
      inp.style.borderColor = taux < 70 ? '#d99' : '';
      counts[c.key]++; sum += taux; n++;
    });
    var avg = n ? Math.round(sum / n) : 0;
    var avgEl = document.querySelector('[data-avg]');
    if (avgEl) avgEl.textContent = avg + ' %';
    var total = n || 1;
    ['green', 'amber', 'red'].forEach(function (k) {
      var cEl = document.querySelector('[data-count="' + k + '"]');
      if (cEl) cEl.textContent = counts[k];
      var bEl = document.querySelector('[data-bar="' + k + '"]');
      if (bEl) bEl.style.width = (counts[k] / total * 100) + '%';
    });
  }
  document.addEventListener('input', function (e) {
    if (e.target.closest('input.num[data-cible]')) recompute();
  });
  // calcul initial (après rendu du Design Component)
  var tries = 0;
  (function init() {
    if (document.querySelector('input.num[data-cible]')) { recompute(); return; }
    if (tries++ < 40) setTimeout(init, 100);
  })();
})();
