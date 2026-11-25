/* Renders the school-editable content (content/*.json, managed through /admin).
   Every container ships with a static fallback in the HTML, so the page still reads if this fails. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const live = !/^(localhost|127\.|\[::1\]|)$/.test(location.hostname);
  const rel = p => String(p || '').replace(/^\/+/, '');
  // Photos uploaded through the admin may be large: let Netlify's image CDN shrink them on the live site.
  const pic = (p, w) => { p = rel(p); return live && /^uploads\//i.test(p) ? `/.netlify/images?url=/${encodeURI(p)}&w=${w}` : encodeURI(p); };
  const fix = e => { const im = e.target; if (im.tagName === 'IMG' && im.dataset.raw && !im.dataset.tried) { im.dataset.tried = 1; im.removeAttribute('srcset'); im.src = im.dataset.raw; } };
  // Site photos (assets/gallery, assets/img) have phone-sized WebP copies in assets/rs/ - see optimize.py.
  const rs = (p, w) => 'assets/rs/' + p.replace(/^assets\//, '').replace(/\//g, '-').replace(/\.\w+$/, '') + '-' + w + '.webp';
  const cdn = (p, w) => `/.netlify/images?url=/${encodeURI(p)}&w=${w}`;
  const srcsetFor = p => live && /^uploads\//i.test(p) ? ` srcset="${cdn(p, 480)} 480w, ${cdn(p, 960)} 960w" sizes="(max-width:700px) 50vw, 25vw"` : /^assets\/(gallery|img)\/[^/]+\.(jpe?g|png)$/i.test(p) && !/-\d{3}\.\w+$/.test(p) ? ` srcset="${encodeURI(rs(p, 480))} 480w, ${encodeURI(rs(p, 960))} 960w" sizes="(max-width:700px) 50vw, 25vw"` : '';
  document.addEventListener('error', fix, true);
  const imgTag = (p, w, alt, extra = '') => `<img ${extra} loading="lazy" decoding="async" src="${pic(p, w)}" data-raw="${encodeURI(rel(p))}"${srcsetFor(rel(p))} alt="${esc(alt)}">`;
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

  /* Admissions on the home page: hidden by default, switched on from the editor ("Show Admissions on the home page") */
  if (/^index(\.html)?$/.test(document.body.dataset.page || '')) need('page-index').then(d => { if (d && d.show_admissions === true) document.querySelectorAll('[data-adm]').forEach(e => { e.hidden = false; }); });

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

  /* staff */
  const initials = n => { const w = String(n).replace(/^(Dr\.?|Mr\.?|Mrs\.?|Ms\.?|Smt\.?|Shri)\s+/i, '').split(/\s+/).filter(Boolean); return ((w[0] || '?')[0] + (w.length > 1 ? w[w.length - 1][0] : '')).toUpperCase(); };
  const person = p => {
    const media = p.photo ? imgTag(p.photo, 360, p.name) : `<div class="ph">${esc(initials(p.name))}</div>`;
    return `<article class="person" data-name="${esc([p.name, p.role, p.qualification].join(' ').toLowerCase())}" data-role="${esc(String(p.role || '').toUpperCase())}">${media}<div><b>${esc(p.name)}</b><span class="role">${esc(p.role)}</span>${p.qualification ? `<span>${esc(p.qualification)}</span>` : ''}</div></article>`;
  };
  job('#staffGrid', ['staff'], s => {
    if (!s) return;
    const fill = (id, arr) => { if ($(id) && arr && arr.length) $(id).innerHTML = arr.map(person).join(''); };
    fill('#staffLead', s.leadership); fill('#staffGrid', s.teachers); fill('#staffOffice', s.office); fill('#staffSupport', s.support);
    const t = s.teachers || [];
    if ($('#teacherCount')) $('#teacherCount').textContent = t.length + ' teachers';
    const roles = [...new Set(t.map(x => String(x.role || '').toUpperCase()).filter(Boolean))].sort();
    if ($('#roleF')) $('#roleF').innerHTML = '<button class="chip on" data-role="">All</button>' + roles.map(r => `<button class="chip" data-role="${esc(r)}">${esc(r)}</button>`).join('');
  });

  /* fee structure */
  job('#feeTable', ['fees'], f => {
    if (!f) return;
    if (f.session && $('#feeSession')) $('#feeSession').textContent = f.session;
    const rows = (f.groups || []).map(g => `<tr class="sub"><td colspan="3">${esc(g.heading)}</td></tr>` + (g.rows || []).map(r => `<tr><td>${esc(r.item)}</td><td class="num">${esc(r.vsp)}</td><td class="num">${esc(r.nvsp)}</td></tr>`).join('')).join('');
    if (rows) $('#feeTable').innerHTML = `<div class="tbl-wrap"><table class="t"><thead><tr><th>Fee head</th><th class="num">${esc(f.col1 || 'Column 1')}</th><th class="num">${esc(f.col2 || 'Column 2')}</th></tr></thead><tbody>${rows}</tbody></table></div>`;
    if (f.note && $('#feeNote')) $('#feeNote').textContent = f.note;
    if (f.scan && $('#feeScan')) {
      const u = encodeURI(rel(f.scan)); const b = $('#feeScan .docimg'); if (b) { b.dataset.zoom = u; const im = $('img', b); if (im) { im.src = u; } }
      if ($('#feeDl')) $('#feeDl').href = u;
    }
  });

  /* mandatory public disclosure */
  const table = (heads, rows, numCols = []) => `<div class="tbl-wrap"><table class="t"><thead><tr>${heads.map((h, i) => `<th${numCols.includes(i) ? ' class="num"' : ''}>${esc(h)}</th>`).join('')}</tr></thead><tbody>${rows}</tbody></table></div>`;
  const tr = cells => `<tr>${cells.map(c => `<td>${c}</td>`).join('')}</tr>`;
  const kvRows = (a, withNo) => (a || []).map((r, i) => tr((withNo ? [i + 1 + '.'] : []).concat([`<b>${esc(r.item)}</b>`, esc(r.detail)]))).join('');
  const docCell = r => r.file ? `<a href="${encodeURI(rel(r.file))}" target="_blank" rel="noopener">Click here to view</a>` : esc(r.note || 'N.A.');
  const docRows = a => (a || []).map((r, i) => tr([i + 1 + '.', esc(r.item), docCell(r)])).join('');
  job('#mpdDyn', ['disclosure'], d => {
    if (!d) return;
    $('#mpdDyn').innerHTML = `<h3>${esc(d.title || 'Appendix-IX')}</h3><p>${esc(d.subtitle || '')}</p>` +
      `<h3 id="mpd-a">A. General Information</h3>${table(['Sl. No.', 'Information', 'Details'], kvRows(d.general, true))}` +
      `<h3 id="mpd-b">B. Documents and Information</h3>${table(['Sl. No.', 'Documents / Information', 'Upload Documents'], docRows(d.documents))}` +
      `<h3 id="mpd-c">C. Result and Academics</h3>${table(['Sl. No.', 'Documents / Information', 'Upload Documents'], docRows(d.academics_docs))}` +
      `<h4>Result Class: X</h4>${table(['Sl. No.', 'Year', 'No. of Registered Students', 'No. of Students Passed', 'Pass Percentage', 'Class Average', 'Total No. of Distinctions', 'Distinction Ratio', 'Remarks'], (d.results_x || []).map((r, i) => tr([i + 1 + '.', r.year, r.registered, r.passed, r.percent, r.average, r.distinctions, r.ratio, r.remarks].map(esc))).join(''))}` +
      `<h4>Result Class: XII</h4>${table(['Sl. No.', 'Year', 'No. of Registered Students', 'No. of Students Passed', 'Pass Percentage', 'Remarks'], (d.results_xii || []).map((r, i) => tr([i + 1 + '.', r.year, r.registered, r.passed, r.percent, r.remarks].map(esc))).join(''))}` +
      `<h3 id="mpd-d">D. Staff (Teaching)</h3>${table(['Sl. No.', 'Information', 'Details'], kvRows(d.staff, true))}` +
      `<h3 id="mpd-e">E. School Infrastructure</h3>${table(['Sl. No.', 'Information', 'Details'], kvRows(d.infrastructure, true))}`;
    if ($('#schoolInfoDyn')) $('#schoolInfoDyn').innerHTML = `<h3>School information</h3>${table(['Item', 'Details'], kvRows(d.school_info, false))}` +
      `<h3>Members of the School Managing Committee</h3>${table(['Sl.', 'Name', 'Post held', 'Address', 'Tenure'], (d.smc || []).map((r, i) => tr([i + 1, r.name, r.post, r.address, r.tenure].map(esc))).join(''))}` +
      `<h3>Committees</h3><p>${esc(d.committees_note || '')}</p>${table(['Sl.', 'Committee', 'Members'], (d.committees || []).map((r, i) => tr([i + 1, r.committee, r.members].map(esc))).join(''))}` +
      `<h3>Members of PTA</h3>${table(['Class', 'Member'], (d.pta || []).map(r => tr([r.class, r.name].map(esc))).join(''))}` +
      `<p class="note">${d.pta_file ? `Full list with contact details: <a href="${encodeURI(rel(d.pta_file))}" target="_blank" rel="noopener">PTA members (PDF)</a>. ` : ''}${d.affiliation_file ? `Affiliation letter: <a href="${encodeURI(rel(d.affiliation_file))}" target="_blank" rel="noopener">PDF</a>.` : ''}</p>`;
  });

  /* uniform */
  job('#uniformDyn', ['uniform'], u => {
    if (!u || !(u.sets || []).length) return;
    $('#uniformDyn').innerHTML = `${u.intro ? `<p>${esc(u.intro)}</p>` : ''}<div class="grid g2">${u.sets.map(st => `<div class="card"><h3>${esc(st.heading)}</h3>${(st.groups || []).map(g => `<h4>${esc(g.title)}</h4><ul>${(g.items || []).map(i => `<li>${esc(i)}</li>`).join('')}</ul>`).join('')}</div>`).join('')}</div>` +
      ((u.notes || []).length ? `<div class="callout" style="margin-top:24px"><b>Please note</b><ul>${u.notes.map(n => `<li>${esc(n)}</li>`).join('')}</ul></div>` : '');
  });

  /* gallery + albums */
  job('#gallery', ['gallery'], g => {
    const el = $('#gallery'); let it = (g && g.items) || []; if (!it.length) return;
    const lim = +el.dataset.limit; if (lim) it = it.slice(0, lim);
    el.innerHTML = it.map((i, k) => `<button data-c="${esc(i.category || 'culture')}" data-cap="${esc(i.caption || '')}" class="g${i.wide ? ' wide' : ''}">${imgTag(i.image, 640, i.alt || i.caption || 'School photo', k < 4 ? 'loading="eager"' : '')}</button>`).join('');
  });
  job('#albumsList', ['albums'], a => {
    const al = (a && a.items) || []; if (!al.length) return;
    const P = x => (x.photos || []).map(p => (typeof p === 'string' ? p : (p && p.image) || '')).filter(Boolean);
    window.DPS.albums = al.map(x => ({ title: x.title, photos: P(x).map(p => ({ src: encodeURI(rel(p)), cap: x.title })) }));
    $('#albumsList').innerHTML = al.map((x, k) => { const ph = P(x); return ph.length ? `<button class="album" data-album="${k}">${imgTag(ph[0], 520, x.title)}<div><b>${esc(x.title)}</b><span>${ph.length} photo${ph.length === 1 ? '' : 's'}${x.year ? ' · ' + esc(x.year) : ''}</span></div></button>` : ''; }).join('');
  });

  /* editable page content: data-text / data-md / data-docimg / data-list (content/page-<name>.json) */
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const pageName = (document.body.dataset.page || 'index.html').replace(/\.html$/, '');
  const MON = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const WD = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const ORD = ['', '1st', '2nd', '3rd', '4th'];
  let markedP;
  const loadMarked = () => markedP || (markedP = new Promise(res => {
    if (window.marked) return res(window.marked);
    const sc = document.createElement('script'); sc.src = 'https://cdnjs.cloudflare.com/ajax/libs/marked/4.3.0/marked.min.js';
    sc.onload = () => res(window.marked); sc.onerror = () => res(null); document.head.appendChild(sc);
  }));
  const cleanHtml = html => {
    const t = document.createElement('template'); t.innerHTML = html;
    t.content.querySelectorAll('script,iframe,object,embed,style,link,meta,form').forEach(n => n.remove());
    t.content.querySelectorAll('*').forEach(n => [...n.attributes].forEach(a => { if (/^on/i.test(a.name) || (/^(href|src|xlink:href)$/i.test(a.name) && /^\s*javascript:/i.test(a.value))) n.removeAttribute(a.name); }));
    t.content.querySelectorAll('a[href^="http"]').forEach(a => { a.target = '_blank'; a.rel = 'noopener'; });
    t.content.querySelectorAll('table').forEach(tb => {
      const w = document.createElement('div'); w.className = 'tbl-wrap'; tb.classList.add('t'); tb.replaceWith(w); w.appendChild(tb);
      const th = [...tb.querySelectorAll('thead th')]; if (th.length && th.every(x => !x.textContent.trim())) tb.querySelector('thead').remove();
    });
    return t.innerHTML;
  };
  const mdToHtml = (m, mk) => mk ? cleanHtml(mk.parse(String(m), { mangle: false, headerIds: false })) : '<p>' + esc(m) + '</p>';
  const safeColor = c => /^#[0-9a-f]{3,8}$/i.test(c || '') ? c : '#0e4a2c';
  const houseCls = (n, i) => ({ chenab: 'h-chenab', ganges: 'h-ganges', jhelum: 'h-jhelum', krishna: 'h-krishna' }[String(n).toLowerCase().trim()] || ['h-chenab', 'h-ganges', 'h-jhelum', 'h-krishna'][i % 4]);
  const TPL = {
    stat: i => `<div><b>${esc(i.number)}</b><span>${esc(i.label)}</span></div>`,
    why: (i, k, c) => `<article class="card hover"><div class="ico">${(c.icons || {})[i.icon] || ''}</div><h3>${esc(i.title)}</h3><p>${esc(i.text)}</p></article>`,
    step: i => `<div class="step"><small>${esc(i.when)}</small><h3>${esc(i.title)}</h3><p>${esc(i.text)}</p></div>`,
    house: (i, k) => `<div class="house ${houseCls(i.name, k)}"><b>${esc(i.name)}</b><span>House</span></div>`,
    pill: i => `<span class="pill" style="font-size:.85rem;padding:.4em 1em">${esc(i)}</span> `,
    pill2: i => `<span class="pill" style="font-size:.85rem;padding:.4em 1em;background:#fbefd0;color:#6b4a00">${esc(i)}</span> `,
    dcard: i => `<article class="card" style="border-top:6px solid ${safeColor(i.color)}"><h3>${esc(i.title)}</h3>${i.intro ? `<p>${esc(i.intro)}</p>` : ''}<ul>${(i.items || []).map(x => `<li>${esc(x)}</li>`).join('')}</ul>${i.note ? `<p class="note">${esc(i.note)}</p>` : ''}</article>`,
    faq: i => `<details><summary>${esc(i.question)}</summary><div class="ans"><p>${esc(i.answer)}</p></div></details>`,
    mentor: i => `<article class="person">${i.photo ? imgTag(i.photo, 360, i.name) : `<div class="ph">${esc(initials(i.name))}</div>`}<div><b>${esc(i.name)}</b><span>${esc(i.role)}</span></div></article>`,
    pcard: (i, k, c) => `<article class="card"><div class="ico">${(c.icons || {})[i.icon] || ''}</div><h3>${esc(i.title)}</h3>${mdToHtml(i.body || '', c.mk)}</article>`,
    doclink: i => docLi(i.title, i.file, 'Download', ''),
    day: i => i.nth ? `<div class="day" data-m="${esc(i.month)}" data-n="${esc(i.nth)}" data-w="${esc(i.weekday)}"><div class="d"><b>${ORD[+i.nth] || i.nth}</b><span>${WD[+i.weekday] ? WD[+i.weekday].slice(0, 3) : ''} · ${MON[+i.month] || ''}</span></div><p>${esc(i.title)}</p></div>`
      : `<div class="day" data-m="${esc(i.month)}" data-d="${esc(i.day)}"><div class="d"><b>${esc(i.day)}</b><span>${MON[+i.month] || ''}</span></div><p>${esc(i.title)}</p></div>`,
  };
  const calendars = (el, items) => {
    el.innerHTML = `<div class="tablist" role="tablist" aria-label="Calendars">${items.map((c, k) => `<button role="tab" aria-selected="${k === 0}" aria-controls="cal${k}" id="bcal${k}"${k ? ' tabindex="-1"' : ''}>${esc(c.title)}</button>`).join('')}</div>` +
      items.map((c, k) => `<div class="panel" role="tabpanel" id="cal${k}" aria-labelledby="bcal${k}"${k ? ' hidden' : ''}><button class="docimg" data-zoom="${encodeURI(rel(c.image))}" data-cap="${esc(c.title)}"><img src="${encodeURI(rel(c.image))}" alt="${esc(c.title)}" loading="lazy"></button><p style="margin:14px 0 0"><a class="btn btn-line btn-sm" href="${encodeURI(rel(c.image))}" download>Download image</a></p></div>`).join('');
  };
  const pageEls = $$('[data-text],[data-md],[data-docimg],[data-list]');
  if (pageEls.length) {
    const names = [...new Set(pageEls.map(e => e.dataset.src || pageName))];
    const needMd = pageEls.some(e => e.dataset.md !== undefined || e.dataset.tpl === 'pcard');
    const needIcons = pageEls.some(e => ['why', 'pcard'].includes(e.dataset.tpl));
    jobs.push(Promise.all([Promise.all(names.map(n => need('page-' + n))), needMd ? loadMarked() : null, needIcons ? fetch('assets/icons.json').then(r => r.json()).catch(() => ({})) : null]).then(([, mk, icons]) => {
      const ctx = { mk, icons };
      pageEls.forEach(el => {
        try {
          const d = data['page-' + (el.dataset.src || pageName)]; if (!d) return;
          if (el.dataset.text !== undefined) { const v = d[el.dataset.text]; if (v) el.textContent = v; }
          else if (el.dataset.md !== undefined) { const v = d[el.dataset.md]; if (v && String(v).trim()) el.innerHTML = mdToHtml(v, mk); }
          else if (el.dataset.docimg !== undefined) { const v = d[el.dataset.docimg]; if (v) { const b = el.querySelector('.docimg'); if (b) { const u = encodeURI(rel(v)); b.dataset.zoom = u; const im = b.querySelector('img'); if (im) im.src = u; } } }
          else if (el.dataset.list !== undefined) {
            const arr = d[el.dataset.list]; if (!Array.isArray(arr) || !arr.length) return;
            if (el.dataset.tpl === 'calendars') calendars(el, arr);
            else el.innerHTML = arr.map((it, k) => (TPL[el.dataset.tpl] || (() => ''))(it, k, ctx)).join('');
          }
        } catch (e) { console.warn('page content', e); }
      });
    }));
  }

  window.DPS = Object.assign(window.DPS || {}, {
    data,
    // entries for the site search so newly published items are findable immediately
    searchEntries: () => Promise.all(['circulars', 'assignments', 'syllabus', 'news', 'staff'].map(need)).then(() => {
      const out = [];
      const sf = data.staff || {};
      ['leadership', 'teachers', 'office', 'support'].forEach(k => (sf[k] || []).forEach(p => out.push({ t: p.name, u: 'staff.html#' + (k === 'teachers' ? 'teachers' : k === 'leadership' ? 'leadership' : k), d: (p.role || '') + ' · Faculty & Staff', k: 'Person' })));
      ((data.circulars || {}).items || []).forEach(i => out.push({ t: i.title, u: rel(i.file), d: 'Circular' + (i.date ? ' · ' + fmt(i.date) : ''), k: 'Download' }));
      ((data.assignments || {}).items || []).forEach(i => out.push({ t: i.label, u: rel(i.file), d: 'Assignment · Download', k: 'Download' }));
      ((data.syllabus || {}).items || []).forEach(i => out.push({ t: i.label, u: rel(i.file), d: 'Syllabus · Download', k: 'Download' }));
      ((data.news || {}).items || []).forEach(i => out.push({ t: i.title, u: 'news.html#achievements', d: [i.category, i.date ? fmt(i.date) : ''].filter(Boolean).join(' · ') || 'News', k: 'News' }));
      return out;
    }),
  });
  window.DPS_READY = Promise.all(jobs);
})();
