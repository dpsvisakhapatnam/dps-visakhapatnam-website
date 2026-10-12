/* Renders the school-editable content (content/*.json, managed through /admin).
   Every container ships with a static fallback in the HTML, so the page still reads if this fails. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const live = !/^(localhost|127\.|\[::1\]|)$/.test(location.hostname);
  const rel = p => String(p || '').replace(/^\/+/, '');
  // Photos uploaded through the admin may be large: let Netlify's image CDN shrink them on the live site.
  const pic = (p, w) => { p = rel(p); return live && /^uploads\//i.test(p) ? `/.netlify/images?url=/${encodeURI(p)}&w=${w}` : encodeURI(p); };
  const fix = e => { const im = e.target; if (im.tagName === 'IMG' && im.dataset.raw && !im.dataset.tried) { im.dataset.tried = 1; im.src = im.dataset.raw; } };
  document.addEventListener('error', fix, true);
  const imgTag = (p, w, alt, extra = '') => `<img ${extra} loading="lazy" src="${pic(p, w)}" data-raw="${encodeURI(rel(p))}" alt="${esc(alt)}">`;
  const get = n => fetch(`content/${n}.json`, { cache: 'no-cache' }).then(r => r.ok ? r.json() : Promise.reject(n)).catch(() => null);
  const fmt = d => { if (!d) return ''; const x = new Date(d + (String(d).length <= 10 ? 'T00:00:00' : '')); return isNaN(x) ? '' : x.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }); };
  const byDate = (a, b) => (b.date ? Date.parse(b.date) : -1) - (a.date ? Date.parse(a.date) : -1);
  const ext = f => (String(f).split('?')[0].split('.').pop() || '').toLowerCase();
  const badge = f => ['jpg', 'jpeg', 'png', 'webp'].includes(ext(f)) ? '<span class="ft img">IMG</span>' : `<span class="ft">${esc(ext(f).toUpperCase() || 'FILE').slice(0, 4)}</span>`;
  const docLi = (title, file, sub, cat) => `<li data-cat="${esc(cat || '')}"><a href="${encodeURI(rel(file))}" target="_blank" rel="noopener">${badge(file)}<span><b>${esc(title)}</b><small>${esc(sub)}</small></span></a></li>`;

  window.DPS = window.DPS || {};
  const cache = {};
  const data = {};
  const need = n => cache[n] || (cache[n] = get(n).then(d => (data[n] = d)));
  const jobs = [];
  const job = (sel, names, fn) => { if ($(sel)) jobs.push(Promise.all(names.map(need)).then(r => { try { fn(...r); } catch (e) { console.warn('content render', sel, e); } })); };

  /* notice ticker (every page) */
  job('.ticker', ['notices'], n => {
    if (!n || !n.items || !n.items.length) return;
    const h = n.items.map(i => `<a href="${esc(i.link || '#')}"${/^https?:/.test(i.link || '') ? ' target="_blank" rel="noopener"' : ''}>${esc(i.text)}</a>`).join('');
    $('.ticker').innerHTML = `<div>${h}${h}</div>`;
  });

  /* circulars */
  const circ = c => {
    const items = ((c && c.items) || []).slice().sort(byDate);
    return items;
  };
  job('#circularList', ['circulars'], c => {
    const items = circ(c); if (!items.length) return;
    $('#circularList').innerHTML = items.map(i => docLi(i.title, i.file, i.date ? fmt(i.date) : 'Download', 'circular')).join('');
  });
  job('#latestCirc', ['circulars'], c => {
    const items = circ(c).slice(0, 4); if (!items.length) return;
    $('#latestCirc').innerHTML = items.map(i => docLi(i.title, i.file, i.date ? fmt(i.date) : 'Download', 'circular')).join('');
  });

  /* assignments, syllabus, book list, magazine */
  const list = (id, d, sub, cat) => {
    if (!d) return;
    const el = $(id); if (d.items && d.items.length) el.innerHTML = d.items.map(i => docLi(i.label, i.file, sub, cat)).join('');
  };
  job('#assignList', ['assignments'], a => { if (!a) return; if (a.heading && $('#assignH')) $('#assignH').textContent = a.heading; if (a.note && $('#assignNote')) $('#assignNote').textContent = a.note; list('#assignList', a, 'Assignment · Download', 'assignments'); });
  job('#syllabusList', ['syllabus'], a => { if (!a) return; if (a.heading && $('#sylH')) $('#sylH').textContent = a.heading; if (a.note && $('#sylNote')) $('#sylNote').textContent = a.note; list('#syllabusList', a, 'Syllabus break-up · Download', 'syllabus'); });
  job('#bookFrame', ['booklist'], b => { if (!b || !b.file) return; $('#bookFrame').src = encodeURI(rel(b.file)); $('#bookDl').href = encodeURI(rel(b.file)); if (b.title && $('#bookH')) $('#bookH').textContent = b.title; });
  job('#magFrame', ['magazine'], m => { if (!m || !m.file) return; $('#magFrame').src = encodeURI(rel(m.file)); $('#magDl').href = encodeURI(rel(m.file)); if (m.title && $('#magH')) $('#magH').textContent = m.title; if (m.subtitle && $('#magSub')) $('#magSub').textContent = m.subtitle; });

  /* news */
  const newsItems = n => ((n && n.items) || []).slice().sort(byDate);
  job('#newsList', ['news'], n => {
    const it = newsItems(n); if (!it.length) return;
    $('#newsList').innerHTML = it.map(i => `<article class="newscard">${i.image ? `<button class="newsimg" data-zoom="${encodeURI(rel(i.image))}" data-cap="${esc(i.title)}">${imgTag(i.image, 700, i.title)}</button>` : ''}<div><div class="meta">${i.category ? `<span class="pill">${esc(i.category)}</span>` : ''}${i.date ? `<span>${esc(fmt(i.date))}</span>` : ''}</div><h3>${esc(i.title)}</h3>${i.summary ? `<p>${esc(i.summary)}</p>` : ''}${i.link ? `<p><a href="${esc(i.link)}" target="_blank" rel="noopener">Read more →</a></p>` : ''}</div></article>`).join('');
  });
  job('#latestNews', ['news'], n => {
    const it = newsItems(n).slice(0, 3); if (!it.length) return;
    $('#latestNews').innerHTML = it.map(i => `<a class="nitem" href="news.html#achievements">${i.image ? imgTag(i.image, 200, i.title) : '<span class="ph"></span>'}<span><b>${esc(i.title)}</b><small>${[i.category, i.date ? fmt(i.date) : ''].filter(Boolean).map(esc).join(' · ')}</small></span></a>`).join('');
  });

  /* results */
  job('#resultsDyn', ['results'], r => {
    if (!r) return;
    const card = (cls, c) => !c ? '' : `<article class="res"><header><span>${cls}</span><b>100% result</b></header><div class="big">${esc(c.percent)}<small>%</small></div><p class="who">${esc(c.name)} <em>· school topper</em></p><ul><li><span>Class average</span><b>${esc(c.average)}</b></li><li><span>Students appeared</span><b>${esc(c.appeared)}</b></li><li><span>Students passed</span><b>${esc(c.passed)}</b></li></ul>${c.poster ? `<p style="margin:18px 0 0"><button class="btn btn-gold btn-sm" data-zoom="${encodeURI(rel(c.poster))}" data-cap="${esc(cls + ' results')}">View result poster</button></p>` : ''}</article>`;
    const ch = (r.chart || []);
    $('#resultsDyn').innerHTML = `<div class="section-head light"><p class="eyebrow">Session ${esc(r.session)}</p><h2>Results that speak</h2><p>${esc(r.tagline || '')}</p></div><div class="res-grid">${card('Class X', r.classX)}${card('Class XII', r.classXII)}</div>` +
      (ch.length ? `<div class="chart" style="margin-top:24px"><h3>${esc(r.chart_title || 'Results over the years')}</h3><p class="note" style="margin:0">Percent.</p><div class="bars" data-bars>${ch.map(c => `<div class="bar-col"><b>${esc(c.average)}</b><i style="--h:${Math.min(100, parseFloat(c.average) || 0)}%"></i></div>`).join('')}</div><div class="bar-labels">${ch.map(c => `<span>${esc(c.year)}</span>`).join('')}</div></div>` : '');
  });

  /* gallery + albums */
  job('#gallery', ['gallery'], g => {
    const el = $('#gallery'); let it = (g && g.items) || []; if (!it.length) return;
    const lim = +el.dataset.limit; if (lim) it = it.slice(0, lim);
    el.innerHTML = it.map(i => `<button data-c="${esc(i.category || 'culture')}" data-cap="${esc(i.caption || '')}" class="g${i.wide ? ' wide' : ''}">${imgTag(i.image, 900, i.alt || i.caption || 'School photo')}</button>`).join('');
  });
  job('#albumsList', ['albums'], a => {
    const al = (a && a.items) || []; if (!al.length) return;
    const P = x => (x.photos || []).map(p => (typeof p === 'string' ? p : (p && p.image) || '')).filter(Boolean);
    window.DPS.albums = al.map(x => ({ title: x.title, photos: P(x).map(p => ({ src: encodeURI(rel(p)), cap: x.title })) }));
    $('#albumsList').innerHTML = al.map((x, k) => { const ph = P(x); return ph.length ? `<button class="album" data-album="${k}">${imgTag(ph[0], 520, x.title)}<div><b>${esc(x.title)}</b><span>${ph.length} photo${ph.length === 1 ? '' : 's'}${x.year ? ' · ' + esc(x.year) : ''}</span></div></button>` : ''; }).join('');
  });

  window.DPS = Object.assign(window.DPS || {}, {
    data,
    // entries for the site search so newly published items are findable immediately
    searchEntries: () => Promise.all(['circulars', 'assignments', 'syllabus', 'news'].map(need)).then(() => {
      const out = [];
      ((data.circulars || {}).items || []).forEach(i => out.push({ t: i.title, u: rel(i.file), d: 'Circular' + (i.date ? ' · ' + fmt(i.date) : ''), k: 'Download' }));
      ((data.assignments || {}).items || []).forEach(i => out.push({ t: i.label, u: rel(i.file), d: 'Assignment · Download', k: 'Download' }));
      ((data.syllabus || {}).items || []).forEach(i => out.push({ t: i.label, u: rel(i.file), d: 'Syllabus · Download', k: 'Download' }));
      ((data.news || {}).items || []).forEach(i => out.push({ t: i.title, u: 'news.html#achievements', d: [i.category, i.date ? fmt(i.date) : ''].filter(Boolean).join(' · ') || 'News', k: 'News' }));
      return out;
    }),
  });
  window.DPS_READY = Promise.all(jobs);
})();
