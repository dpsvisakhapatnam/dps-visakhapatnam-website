(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const store = { get: k => { try { return localStorage.getItem(k); } catch (e) { return null; } }, set: (k, v) => { try { localStorage.setItem(k, v); } catch (e) {} } };

  /* ---------- header, menu, dropdowns ---------- */
  const header = $('.site-header');
  const tb = $('.topbar');
  const setTb = () => document.documentElement.style.setProperty('--tb', (tb ? Math.max(0, tb.getBoundingClientRect().bottom) : 0) + 'px');
  const onScroll = () => {
    header.classList.toggle('solid', scrollY > 10);
    const t = $('#toTop'); if (t) t.classList.toggle('show', scrollY > 700);
    setTb();
  };
  addEventListener('scroll', onScroll, { passive: true }); addEventListener('resize', setTb); onScroll();

  const btn = $('#menuBtn'), nav = $('#nav');
  const setMenu = open => {
    nav.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', open);
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    document.body.style.overflow = open ? 'hidden' : '';
  };
  btn.addEventListener('click', () => setMenu(!nav.classList.contains('open')));
  $$('.item', nav).forEach(it => {
    const b = $('button', it);
    if (!b) return;
    b.addEventListener('click', e => {
      e.stopPropagation();
      const was = it.classList.contains('open');
      $$('.item.open', nav).forEach(x => { x.classList.remove('open'); $('button', x).setAttribute('aria-expanded', 'false'); });
      if (!was) { it.classList.add('open'); b.setAttribute('aria-expanded', 'true'); }
    });
  });
  document.addEventListener('click', e => {
    if (!e.target.closest('.nav')) $$('.item.open', nav).forEach(x => x.classList.remove('open'));
  });
  $$('.drop a, .nav > .item > a', nav).forEach(a => a.addEventListener('click', () => setMenu(false)));

  /* ---------- theme ---------- */
  const themeBtn = $('#themeBtn');
  if (themeBtn) themeBtn.addEventListener('click', () => {
    const d = document.documentElement, next = d.dataset.theme === 'dark' ? 'light' : 'dark';
    d.dataset.theme = next; store.set('theme', next);
  });

  /* ---------- to top ---------- */
  const tt = $('#toTop'); if (tt) tt.addEventListener('click', () => scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }));

  /* ---------- modals ---------- */
  let lastFocus = null;
  const openModal = m => { lastFocus = document.activeElement; m.hidden = false; document.body.style.overflow = 'hidden'; const f = $('input,select,textarea,button.btn', m); f && setTimeout(() => f.focus(), 30); };
  const closeModal = m => { m.hidden = true; document.body.style.overflow = ''; lastFocus && lastFocus.focus && lastFocus.focus(); };
  document.addEventListener('click', e => {
    const o = e.target.closest('[data-open]');
    if (o) { e.preventDefault(); const m = document.getElementById(o.dataset.open); if (m) openModal(m); return; }
    if (e.target.closest('[data-close]')) { const m = e.target.closest('.modal'); if (m) closeModal(m); return; }
    if (e.target.classList && e.target.classList.contains('modal')) closeModal(e.target);
  });

  /* ---------- search ---------- */
  const sm = $('#search'), q = $('#q'), res = $('#qres');
  let idx = null, sel = 0, hits = [];
  const load = () => idx ? Promise.resolve(idx) : Promise.all([
    fetch('assets/search.json').then(r => r.json()).catch(() => []),
    (window.DPS && DPS.searchEntries ? DPS.searchEntries() : Promise.resolve([])).catch(() => []),
  ]).then(([a, b]) => (idx = a.concat(b)));
  const render = () => {
    const term = q.value.trim().toLowerCase();
    if (!term) { hits = (idx || []).filter(x => x.k === 'Page').slice(0, 8); }
    else {
      const w = term.split(/\s+/);
      hits = (idx || []).map(x => {
        const hay = (x.t + ' ' + x.d).toLowerCase(); let s = 0;
        for (const t of w) { if (!hay.includes(t)) return null; s += x.t.toLowerCase().includes(t) ? 3 : 1; if (x.t.toLowerCase().startsWith(t)) s += 2; }
        s += x.k === 'Page' ? 2 : 0; return { x, s };
      }).filter(Boolean).sort((a, b) => b.s - a.s).slice(0, 30).map(o => o.x);
    }
    sel = 0;
    res.innerHTML = hits.length ? hits.map((h, i) => `<a href="${h.u}" class="${i ? '' : 'sel'}"><b>${h.t.replace(/</g, '&lt;')}</b><small>${h.k} · ${h.d.replace(/</g, '&lt;').slice(0, 90)}</small></a>`).join('') : '<div class="empty">No results — try another word.</div>';
  };
  const openSearch = () => { openModal(sm); load().then(render); q.select(); };
  $('#searchBtn') && $('#searchBtn').addEventListener('click', openSearch);
  q.addEventListener('input', () => load().then(render));
  const move = d => { const a = $$('a', res); if (!a.length) return; a[sel] && a[sel].classList.remove('sel'); sel = (sel + d + a.length) % a.length; a[sel].classList.add('sel'); a[sel].scrollIntoView({ block: 'nearest' }); };
  q.addEventListener('keydown', e => {
    if (e.key === 'ArrowDown') { e.preventDefault(); move(1); }
    if (e.key === 'ArrowUp') { e.preventDefault(); move(-1); }
    if (e.key === 'Enter') { const a = $$('a', res)[sel]; if (a) location.href = a.getAttribute('href'); }
  });
  addEventListener('keydown', e => {
    const typing = /input|textarea|select/i.test((e.target.tagName || ''));
    if ((e.key === '/' && !typing) || ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k')) { e.preventDefault(); openSearch(); }
    if (e.key === 'Escape') { $$('.modal').forEach(m => !m.hidden && closeModal(m)); setMenu(false); }
  });

  /* ---------- forms -> mailto ---------- */
  $$('form[data-mailto]').forEach(f => f.addEventListener('submit', e => {
    e.preventDefault();
    const lines = [...new FormData(f).entries()].map(([k, v]) => `${k}: ${v}`);
    location.href = `mailto:${f.dataset.mailto}?subject=${encodeURIComponent(f.dataset.subject || 'Website enquiry')}&body=${encodeURIComponent(lines.join('\n') + '\n\n— sent from the school website')}`;
  }));

  /* ---------- hero slideshow ---------- */
  const slides = $$('.slide'), dots = $('.dots');
  if (slides.length && dots) {
    let cur = 0, timer;
    slides.forEach((_, i) => { const b = document.createElement('button'); b.setAttribute('role', 'tab'); b.setAttribute('aria-label', 'Photo ' + (i + 1)); b.addEventListener('click', () => { show(i); start(); }); dots.appendChild(b); });
    const show = i => { cur = (i + slides.length) % slides.length; slides.forEach((s, k) => s.classList.toggle('on', k === cur)); $$('button', dots).forEach((d, k) => d.setAttribute('aria-selected', k === cur)); };
    const start = () => { clearInterval(timer); if (!reduce) timer = setInterval(() => show(cur + 1), 6000); };
    show(0); start();
  }

  /* ---------- tabs ---------- */
  $$('[data-tabs]').forEach(tabs => {
    const tb = $$('[role=tab]', tabs), pn = $$('[role=tabpanel]', tabs);
    const pick = (i, focus) => { tb.forEach((t, k) => { t.setAttribute('aria-selected', k === i); t.tabIndex = k === i ? 0 : -1; }); pn.forEach((p, k) => p.hidden = k !== i); if (focus) tb[i].focus(); };
    tb.forEach((t, i) => { t.addEventListener('click', () => pick(i)); t.addEventListener('keydown', e => { if (e.key === 'ArrowRight') pick((i + 1) % tb.length, 1); if (e.key === 'ArrowLeft') pick((i - 1 + tb.length) % tb.length, 1); }); });
  });

  /* ---------- reveal & bars ---------- */
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: .1 });
  $$('.reveal').forEach(el => io.observe(el));
  const ready = window.DPS_READY || Promise.resolve();
  ready.then(() => $$('[data-bars]').forEach(b => { const o = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { $$('.bar-col', b).forEach((c, i) => setTimeout(() => c.classList.add('in'), i * 90)); o.disconnect(); } }), { threshold: .3 }); o.observe(b); }));

  /* ---------- gallery filter ---------- */
  const gItems = () => $$('#gallery .g');
  $$('.filters .chip[data-f]').forEach(c => c.addEventListener('click', () => {
    $$('.filters .chip[data-f]').forEach(x => x.classList.toggle('on', x === c));
    gItems().forEach(g => g.classList.toggle('hide', c.dataset.f !== 'all' && g.dataset.c !== c.dataset.f));
  }));

  /* ---------- lightbox ---------- */
  const lb = $('#lb'), lbImg = $('img', lb), lbCap = $('figcaption', lb);
  let list = [], li = 0, opener = null;
  const show = () => { const it = list[li]; lbImg.src = it.src; lbImg.alt = it.cap || ''; lbCap.textContent = it.cap || ''; lb.classList.toggle('single', list.length < 2); };
  const openLb = (l, i, from) => { list = l; li = i; opener = from; show(); lb.hidden = false; document.body.style.overflow = 'hidden'; $('.lb-x', lb).focus(); };
  const closeLb = () => { lb.hidden = true; document.body.style.overflow = ''; opener && opener.focus && opener.focus(); };
  const step = d => { li = (li + d + list.length) % list.length; show(); };
  document.addEventListener('click', e => {
    const z = e.target.closest('[data-zoom]');
    if (z) { e.preventDefault(); openLb([{ src: z.dataset.zoom, cap: z.dataset.cap }], 0, z); return; }
    const g = e.target.closest('#gallery .g');
    if (g) {
      const vis = gItems().filter(x => !x.classList.contains('hide'));
      openLb(vis.map(x => ({ src: ($('img', x).dataset.raw || $('img', x).src), cap: x.dataset.cap })), vis.indexOf(g), g); return;
    }
    const a = e.target.closest('[data-album]');
    if (a && window.DPS && DPS.albums) openLb(DPS.albums[+a.dataset.album].photos, 0, a);
  });
  $('.lb-x', lb).addEventListener('click', closeLb);
  $('.prev', lb).addEventListener('click', () => step(-1));
  $('.next', lb).addEventListener('click', () => step(1));
  lb.addEventListener('click', e => { if (e.target === lb) closeLb(); });
  addEventListener('keydown', e => { if (lb.hidden) return; if (e.key === 'Escape') closeLb(); if (e.key === 'ArrowLeft') step(-1); if (e.key === 'ArrowRight') step(1); });

  /* ---------- staff filter ---------- */
  const sq = $('#staffQ'), grid = $('#staffGrid');
  if (grid) {
    let role = '';
    const cards = $$('.person', grid);
    const apply = () => {
      const t = (sq.value || '').toLowerCase().trim(); let n = 0;
      cards.forEach(c => { const ok = (!t || c.dataset.name.includes(t)) && (!role || c.dataset.role === role); c.hidden = !ok; if (ok) n++; });
      $('#staffEmpty').hidden = n > 0;
    };
    sq.addEventListener('input', apply);
    $$('#roleF .chip').forEach(c => c.addEventListener('click', () => { $$('#roleF .chip').forEach(x => x.classList.toggle('on', x === c)); role = c.dataset.role; apply(); }));
  }

  /* ---------- downloads search ---------- */
  const dq = $('#docQ');
  if (dq) {
    const cnt = $('#docCount');
    const run = () => { const t = dq.value.toLowerCase().trim(); let n = 0; $$('[data-docs] li').forEach(l => { const ok = !t || l.textContent.toLowerCase().includes(t) || (l.dataset.cat || '').includes(t); l.hidden = !ok; if (ok) n++; }); cnt.textContent = t ? n + ' result' + (n === 1 ? '' : 's') : ''; };
    dq.addEventListener('input', run);
  }

  /* ---------- important days: highlight the next one ---------- */
  const dayLists = $$('.days[id^=days]');
  if (dayLists.length) {
    const now = new Date(); now.setHours(0, 0, 0, 0);
    const nth = (y, m, n, w) => { const d = new Date(y, m - 1, 1); const off = (7 + w - d.getDay()) % 7; return new Date(y, m - 1, 1 + off + 7 * (n - 1)); };
    const dateOf = (el, y) => el.dataset.n ? nth(y, +el.dataset.m, +el.dataset.n, +el.dataset.w) : new Date(y, +el.dataset.m - 1, +el.dataset.d);
    dayLists.forEach(list => {
      let best = null, bd = null;
      $$('.day', list).forEach(el => {
        let d = dateOf(el, now.getFullYear()); if (d < now) d = dateOf(el, now.getFullYear() + 1);
        el._d = d; if (!bd || d < bd) { bd = d; best = el; }
      });
      if (best) {
        best.classList.add('next');
        const diff = Math.round((bd - now) / 864e5);
        const p = $('p', best); p.innerHTML += ` <span class="pill" style="margin-left:6px">${diff === 0 ? 'Today' : diff === 1 ? 'Tomorrow' : 'in ' + diff + ' days'}</span>`;
        if (list.id === 'daysHome') {
          // on the home page show only the next six days, in date order
          const all = $$('.day', list).sort((a, b) => a._d - b._d);
          all.forEach((el, i) => { list.appendChild(el); el.hidden = i >= 6; });
        }
      }
    });
  }

  /* ---------- subnav highlight ---------- */
  const sn = $$('.subnav a');
  if (sn.length && 'IntersectionObserver' in window) {
    const map = new Map(sn.map(a => [a.getAttribute('href').slice(1), a]));
    const so = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { sn.forEach(a => a.classList.remove('on')); const a = map.get(e.target.id); a && a.classList.add('on'); } }), { rootMargin: '-35% 0px -60% 0px' });
    map.forEach((_, id) => { const el = document.getElementById(id); el && so.observe(el); });
  }
})();
