"""Page shell: top bar, mega-menu header, footer, floating dock, modals."""
import json, re
from core import esc, text_of

SITE = 'Delhi Public School Visakhapatnam Steel Plant'
PHONE = '(0891) 2510686'
PHONE_TEL = '+918912510686'
EMAIL = 'dpsvisakhapatnam@gmail.com'
ERP = 'http://dpsv.edunext5.com/'
FEES = 'https://www.onlinesbi.com/sbicollect/icollecthome.htm?corpID=519243'

ICON = {
    'search': '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
    'moon': '<svg viewBox="0 0 24 24"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
    'menu': '<svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    'close': '<svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18"/></svg>',
    'edit': '<svg viewBox="0 0 24 24"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/></svg>',
    'phone': '<svg viewBox="0 0 24 24"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
    'pin': '<svg viewBox="0 0 24 24"><path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    'mail': '<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
    'cal': '<svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>',
    'login': '<svg viewBox="0 0 24 24"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><path d="m10 17 5-5-5-5M15 12H3"/></svg>',
    'rupee': '<svg viewBox="0 0 24 24"><path d="M6 4h12M6 9h12M9 4c6 0 6 9 0 9H6l8 7"/></svg>',
    'book': '<svg viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5z"/><path d="M4 19.5V21h16"/></svg>',
    'flask': '<svg viewBox="0 0 24 24"><path d="M9 3h6M10 3v6L4.5 19a1.5 1.5 0 0 0 1.3 2.2h12.4a1.5 1.5 0 0 0 1.3-2.2L14 9V3"/><path d="M7.5 15h9"/></svg>',
    'monitor': '<svg viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/></svg>',
    'run': '<svg viewBox="0 0 24 24"><circle cx="13" cy="4" r="2"/><path d="m4 17 5-1 2-4-3-3 4-2 3 3 3 1M11 12l2 4-1 5"/></svg>',
    'music': '<svg viewBox="0 0 24 24"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>',
    'bus': '<svg viewBox="0 0 24 24"><rect x="4" y="3" width="16" height="14" rx="3"/><path d="M4 11h16M8 21v-4M16 21v-4"/><circle cx="8" cy="14" r=".6"/><circle cx="16" cy="14" r=".6"/></svg>',
    'heart': '<svg viewBox="0 0 24 24"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8z"/></svg>',
    'globe': '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20M12 2a15 15 0 0 0 0 20"/></svg>',
    'users': '<svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/></svg>',
    'shield': '<svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>',
    'palette': '<svg viewBox="0 0 24 24"><circle cx="13.5" cy="6.5" r="1.2"/><circle cx="17.5" cy="10.5" r="1.2"/><circle cx="8.5" cy="7.5" r="1.2"/><circle cx="6.5" cy="12.5" r="1.2"/><path d="M12 2a10 10 0 1 0 0 20c1.1 0 2-.9 2-2 0-.6-.2-1-.5-1.4-.3-.4-.5-.8-.5-1.3 0-1.1.9-2 2-2h2.4a4 4 0 0 0 4-4A9.6 9.6 0 0 0 12 2z"/></svg>',
    'trophy': '<svg viewBox="0 0 24 24"><path d="M6 9H4a2 2 0 0 1-2-2V5h4M18 9h2a2 2 0 0 0 2-2V5h-4M6 3h12v6a6 6 0 0 1-12 0zM12 15v4M8 21h8"/></svg>',
    'lib': '<svg viewBox="0 0 24 24"><path d="M3 4h4v16H3zM9 4h4v16H9zM15.5 5.3l3.9-1 3.6 14.4-3.9 1z"/></svg>',
    'cap': '<svg viewBox="0 0 24 24"><path d="m22 10-10-5L2 10l10 5z"/><path d="M6 12v5c3 2.5 9 2.5 12 0v-5M22 10v6"/></svg>',
    'sparkle': '<svg viewBox="0 0 24 24"><path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8zM19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8z"/></svg>',
}

NAV = [
    ('About', 'about.html', [
        ('Our School', 'about.html#school', 'Philosophy, aim & international policy'),
        ("Principal's Message", 'about.html#principal', 'In his own words'),
        ('DPS Society', 'about.html#society', 'A legend in education'),
        ('Mentors & Management', 'about.html#management', 'Governing body & managing committee'),
        ('Faculty & Staff', 'staff.html', 'Meet the people of DPS'),
    ]),
    ('Academics', 'academics.html', [
        ('Teaching Methodology', 'academics.html#methodology', 'Learn, learner, learning'),
        ('Courses & Promotion', 'academics.html#courses', 'Subjects, streams & policy'),
        ('Calendars', 'academics.html#calendar', 'Academic, assessment & events'),
        ('Awards & Rewards', 'academics.html#awards', 'How achievers are recognised'),
        ('Student Strength', 'academics.html#strength', 'Class-wise 2025-26'),
        ('Staff Training', 'academics.html#training', 'Workshop details'),
    ]),
    ('Admissions', 'admissions.html', [
        ('Admission Process', 'admissions.html#process', 'Step by step'),
        ('Fee Structure 2026-27', 'admissions.html#fees', 'Download or view'),
        ('Uniform', 'admissions.html#uniform', 'Summer & winter'),
        ('Application Form', 'admissions.html#forms', 'Registration cum enrolment'),
        ('Withdrawal & TC', 'admissions.html#withdrawal', 'Policy and sample TC'),
        ('FAQs', 'admissions.html#faq', 'Quick answers'),
    ]),
    ('Campus Life', 'campus.html', [
        ('Infrastructure', 'campus.html#infrastructure', '13 acres, labs & library'),
        ('Houses & Clubs', 'campus.html#houses', 'Four rivers, sixteen clubs'),
        ('Morning Assembly', 'campus.html#assembly', 'How the day begins'),
        ('Student Council', 'campus.html#council', 'Our flag bearers'),
        ('Discipline Policy', 'campus.html#discipline', 'Yellow, grey & red cards'),
        ('RIDS Recognition', 'campus.html#rids', 'British Council 2026–2029'),
    ]),
    ('Gallery', 'gallery.html', None),
    ('Updates', 'news.html', [
        ('News & Circulars', 'news.html', 'Notices and media'),
        ('Resources & Downloads', 'resources.html', 'Assignments, syllabus, book list'),
        ('Assignments', 'resources.html#assignments', 'Class-wise PDFs'),
        ('Magazine', 'resources.html#magazine', 'Aurora Australis'),
        ('Careers', 'resources.html#careers', 'Join our team'),
    ]),
    ('More', 'disclosure.html', [
        ('Mandatory Public Disclosure', 'disclosure.html', 'CBSE Appendix-IX'),
        ('Recognition & Awards', 'index.html#recognition', 'Rankings and honours'),
        ('Alumni', 'contact.html#alumni', 'Stay connected'),
        ('Contact Us', 'contact.html', 'Visit or write to us'),
    ]),
]

TICKER = [
    ('Assignments Aug–Sep 2026-27 now available', 'resources.html#assignments'),
    ('Fee structure 2026-27', 'admissions.html#fees'),
    ('Book list 2026-27', 'resources.html#booklist'),
    ('School calendar 2026-27', 'academics.html#calendar'),
    ('Careers360: India’s Best Schools 2026 — AAA+', 'index.html#recognition'),
    ('RIDS recognition 2026–2029 by the British Council', 'campus.html#rids'),
]


def header(active):
    items = []
    for label, href, kids in NAV:
        is_active = ' active' if label == active else ''
        if kids:
            lis = ''.join(f'<a href="{h}"><span>{esc(t)}</span><small>{esc(d)}</small></a>' for t, h, d in kids)
            items.append(
                f'<div class="item{is_active}"><button type="button" aria-haspopup="true" aria-expanded="false">{label}<i class="chev"></i></button><div class="drop">{lis}</div></div>')
        else:
            items.append(f'<div class="item{is_active}"><a href="{href}">{label}</a></div>')
    items.append(f'<div class="item mob-only"><a class="btn btn-gold" href="{ERP}" target="_blank" rel="noopener">Parent Login</a></div>')
    import os
    nj = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'content', 'notices.json')
    notes = [(i['text'], i.get('link') or '#') for i in json.load(open(nj, encoding='utf8'))['items']] if os.path.exists(nj) else TICKER
    ticker = ''.join(f'<a href="{h}">{esc(t)}</a>' for t, h in notes)
    return f'''
<div class="topbar"><div class="wrap">
  <span class="tag">Latest</span>
  <div class="ticker" aria-label="Latest updates"><div>{ticker}{ticker}</div></div>
  <div class="tl"><a href="tel:{PHONE_TEL}">{PHONE}</a><a href="mailto:{EMAIL}">Email us</a></div>
</div></div>
<header class="site-header" id="top"><div class="wrap bar">
  <a class="brand" href="index.html" aria-label="{SITE} — home">
    <img src="assets/dpslogo.png" alt="" width="46" height="51">
    <span><strong>Delhi Public School</strong><small>Visakhapatnam Steel Plant</small></span>
  </a>
  <nav class="nav" id="nav" aria-label="Primary">{''.join(items)}</nav>
  <div class="hdr-actions">
    <button class="icon-btn" id="searchBtn" aria-label="Search the site (press /)" title="Search (/)">{ICON['search']}</button>
    <button class="icon-btn hide-m" id="themeBtn" aria-label="Toggle dark mode" title="Dark mode">{ICON['moon']}</button>
    <a class="btn btn-gold btn-sm hide-m" href="{ERP}" target="_blank" rel="noopener">Parent Login</a>
    <button class="icon-btn menu-btn" id="menuBtn" aria-expanded="false" aria-controls="nav" aria-label="Open menu">{ICON['menu']}</button>
  </div>
</div></header>'''


def footer():
    return f'''
<section class="section tight" style="padding-bottom:0"><div class="wrap">
  <div class="cta reveal">
    <div><h2>Come, see our campus.</h2><p>Admissions open every year from December. Visit our 13-acre campus in Ukkunagaram, meet our teachers and see why learning here is a joy.</p></div>
    <div class="actions"><a class="btn btn-gold" href="contact.html#visit">Plan a campus visit</a><a class="btn btn-ghost" href="admissions.html#process">How admissions work</a></div>
  </div>
</div></section>
<footer class="site-footer" style="margin-top:60px">
  <div class="wrap f-grid">
    <div>
      <div class="brand"><img src="assets/dpslogo.png" alt="" width="46" height="51"><span><strong>Delhi Public School</strong><small>Visakhapatnam Steel Plant</small></span></div>
      <p>Sector VIII, Ukkunagaram,<br>Visakhapatnam, Andhra Pradesh 530032</p>
      <p><a href="tel:{PHONE_TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p class="tiny">Body to live · Mind to learn · Heart to love · Soul to leave a legacy.</p>
    </div>
    <div><h3>The school</h3><ul>
      <li><a href="about.html">About us</a></li><li><a href="staff.html">Faculty &amp; staff</a></li><li><a href="academics.html">Academics</a></li>
      <li><a href="campus.html">Campus life</a></li><li><a href="gallery.html">Gallery</a></li><li><a href="disclosure.html">Mandatory disclosure</a></li></ul></div>
    <div><h3>Parents &amp; students</h3><ul>
      <li><a href="admissions.html">Admissions</a></li><li><a href="resources.html">Downloads</a></li><li><a href="news.html">News &amp; circulars</a></li>
      <li><a href="{ERP}" target="_blank" rel="noopener">ERP portal</a></li><li><a href="{FEES}" target="_blank" rel="noopener">Pay school fees</a></li><li><a href="contact.html">Contact</a></li></ul></div>
    <div><h3>Useful links</h3><ul>
      <li><a href="https://swayam.gov.in/" target="_blank" rel="noopener">Swayam</a></li><li><a href="https://diksha.gov.in/" target="_blank" rel="noopener">Diksha</a></li>
      <li><a href="http://www.cbse.nic.in/" target="_blank" rel="noopener">CBSE</a></li><li><a href="http://www.ncert.nic.in/" target="_blank" rel="noopener">NCERT</a></li>
      <li><a href="http://www.dpsfamily.org/" target="_blank" rel="noopener">DPS Society</a></li><li><a href="https://www.britannica.com/" target="_blank" rel="noopener">Britannica</a></li><li><a href="https://en.wikipedia.org/" target="_blank" rel="noopener">Wikipedia</a></li></ul></div>
  </div>
  <div class="wrap legal"><span>© 2026 Delhi Public School, Visakhapatnam Steel Plant. All rights reserved.</span><span>Affiliated to CBSE · Affiliation No. 130110 · School Code 57034</span></div>
</footer>

<aside class="dock" aria-label="Quick actions">
  <button type="button" data-open="enquiry">{ICON['edit']}Enquire</button>
  <a href="{ERP}" target="_blank" rel="noopener">{ICON['login']}Parent<br>Login</a>
  <a href="{FEES}" target="_blank" rel="noopener">{ICON['rupee']}Pay<br>Fees</a>
  <a href="tel:{PHONE_TEL}" class="gold">{ICON['phone']}Call</a>
</aside>
<button class="to-top" id="toTop" aria-label="Back to top">↑</button>

<div class="modal" id="enquiry" role="dialog" aria-modal="true" aria-labelledby="enqT" hidden>
  <div class="box">
    <button class="x" data-close aria-label="Close">×</button>
    <h2 id="enqT">Admission enquiry</h2>
    <p class="note">Tell us a little and the school office will get back to you. This opens your email app addressed to the school.</p>
    <form class="form" data-mailto="{EMAIL}" data-subject="Admission enquiry">
      <div class="row"><label>Student’s name<input name="Student" required></label>
      <label>Seeking admission to<select name="Class" required><option value="">Select class</option><option>Balvatika II</option><option>Balvatika III</option><option>Class I</option><option>Class II</option><option>Class III</option><option>Class IV</option><option>Class V</option><option>Class VI</option><option>Class VII</option><option>Class VIII</option><option>Class IX</option><option>Class XI</option></select></label></div>
      <div class="row"><label>Parent’s name<input name="Parent" required autocomplete="name"></label>
      <label>Mobile number<input name="Mobile" type="tel" required autocomplete="tel"></label></div>
      <label>Your query<textarea name="Query" rows="3"></textarea></label>
      <button class="btn btn-green" type="submit">Send enquiry</button>
    </form>
  </div>
</div>
<div class="modal" id="search" role="dialog" aria-modal="true" aria-label="Search" hidden>
  <div class="box search-box">
    <input id="q" type="search" placeholder="Search pages, documents, people…" autocomplete="off" aria-label="Search the site">
    <div class="search-res" id="qres"></div>
    <div class="search-hint">↑ ↓ to move · Enter to open · Esc to close</div>
  </div>
</div>
<div class="lightbox" id="lb" role="dialog" aria-modal="true" aria-label="Photo viewer" hidden>
  <button class="lb-x" aria-label="Close">×</button>
  <button class="lb-n prev" aria-label="Previous">‹</button>
  <figure><img alt=""><figcaption></figcaption></figure>
  <button class="lb-n next" aria-label="Next">›</button>
</div>'''


def hero_page(title, sub, crumbs=None):
    cr = '<a href="index.html">Home</a>' + ''.join(f'<span>›</span>{c}' for c in (crumbs or [])) + f'<span>›</span>{esc(title)}'
    return f'''<section class="phero"><div class="wrap"><div class="crumbs">{cr}</div><h1>{esc(title)}</h1><p>{sub}</p></div></section>'''


def subnav(items):
    return '<nav class="subnav" aria-label="On this page"><div class="wrap">' + ''.join(f'<a href="#{i}">{esc(t)}</a>' for i, t in items) + '</div></nav>'


def add_ids(body):
    """Give every h2/h3 an id (if missing) so search & subnav can deep-link."""
    used = set(re.findall(r'id="([^"]+)"', body))

    def rep(m):
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        if 'id=' in attrs:
            return m.group(0)
        base = re.sub(r'[^a-z0-9]+', '-', text_of(inner).lower()).strip('-')[:50] or 'section'
        i, n = base, 2
        while i in used:
            i = f'{base}-{n}'; n += 1
        used.add(i)
        return f'<{tag}{attrs} id="{i}">{inner}</{tag}>'
    return re.sub(r'<(h[23])([^>]*)>(.*?)</\1>', rep, body, flags=re.S)


def page(fname, title, desc, active, body, extra_head='', og_img='assets/gallery/g9.jpg'):
    body = add_ids(body)
    full_title = f'{title} · {SITE}' if fname != 'index.html' else SITE + ' — Service before Self'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#0e4a2c">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(full_title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:image" content="{og_img}">
<link rel="icon" type="image/png" href="assets/dpslogo.png">
<link rel="preload" href="assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="assets/fonts/fraunces-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="styles.css">
<script>try{{var t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}};document.documentElement.classList.add('js')</script>
{extra_head}
</head>
<body data-page="{fname}">
<a class="skip" href="#main">Skip to content</a>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
<script src="content.js" defer></script>
<script src="script.js" defer></script>
</body>
</html>'''
