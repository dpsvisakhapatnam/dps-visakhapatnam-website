from core import img, thumb, doc, esc
from layout import ICON, page, ERP, FEES, PHONE, PHONE_TEL, EMAIL

# (month, day) or (month, nth, weekday[0=Sun]) -> title
DAYS = [
    ((1, 1), 'New Year Day'), ((1, 12), 'National Youth Day (Swami Vivekananda’s birthday)'), ((1, 15), 'Army Day'),
    ((1, 25), 'National Tourism Day'), ((1, 26), 'Republic Day'), ((1, 28), 'Martyrs’ Day (Mahatma Gandhi’s martyrdom day)'),
    ((2, 18), 'RINL Formation Day'), ((2, 26), 'National Science Day'), ((3, 8), 'Women’s Day'),
    ((5, 1), 'May Day, Labour’s Day'), ((5, 2, 0), 'Mother’s Day'), ((6, 5), 'Environment Day'),
    ((6, 21), 'International Yoga Day'), ((6, 3, 0), 'Father’s Day'), ((7, 1), 'Doctor’s Day'),
    ((7, 15), 'DPS VSP Formation Day'), ((7, 27), 'Parents’ Day'), ((8, 1, 0), 'Friendship Day'),
    ((8, 15), 'Independence Day'), ((8, 29), 'National Sports Day (Major Dhyan Chand’s birthday)'),
    ((9, 5), 'Teachers’ Day'), ((9, 14), 'Hindi Day (Bhartendu Harishchandra’s birthday)'),
    ((10, 2), 'International Non-Violence Day (Gandhi Jayanti)'), ((10, 24), 'United Nations Day'),
    ((11, 14), 'Children’s Day (Jawaharlal Nehru’s birthday)'), ((12, 10), 'World Human Rights Day'),
]
MON = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
WD = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
ORD = ['', '1st', '2nd', '3rd']


def days_html(limit=None):
    out = []
    for k, t in DAYS[:limit] if limit else DAYS:
        if len(k) == 2:
            m, d = k
            lab, attrs = f'<b>{d}</b><span>{MON[m]}</span>', f'data-m="{m}" data-d="{d}"'
        else:
            m, n, w = k
            lab, attrs = f'<b>{ORD[n]}</b><span>{WD[w][:3]} · {MON[m]}</span>', f'data-m="{m}" data-n="{n}" data-w="{w}"'
        out.append(f'<div class="day" {attrs}><div class="d">{lab}</div><p>{esc(t)}</p></div>')
    return ''.join(out)


GAL = [
    ('sports', 'International Yoga Day', 'g1', 'Students and staff pose with International Yoga Day banners', True),
    ('ceremony', 'Investiture Ceremony', 'g9', 'House captains and prefects at the Investiture Ceremony', False),
    ('culture', 'Annual celebrations', 'g7', 'Students perform a folk dance in red costumes', False),
    ('sports', 'Annual Sports Day', 'g18', 'Students form a human pyramid on Sports Day', False),
    ('culture', 'Annual celebrations', 'g5', 'A large group of performers in traditional dress', True),
    ('ceremony', 'Annual Awards & Investiture', 'g12', 'Award winners with guests of honour', False),
    ('sports', 'Annual Sports Day', 'g19', 'Children with colourful umbrellas on the field', False),
    ('culture', 'Annual celebrations', 'g10', 'Children in traditional outfits on stage', False),
    ('sports', '23rd Annual Sports Day', 'g17', 'Sports Day podium with medal winners', False),
    ('culture', 'Annual celebrations', 'g13', 'Students in colourful costumes on stage', False),
    ('ceremony', 'Scholar Badge presentation', 'g4', 'Students holding certificates with teachers', False),
    ('sports', 'March past', 'g14', 'March past with a house flag', False),
    ('culture', 'Pedda Panduga Celebrations', 'g21', 'Guests and students at Pedda Panduga celebrations', True),
    ('culture', 'Grandparents’ Day', 'g16', 'Children light a lamp at Grandparents’ Day', False),
    ('sports', 'Yoga session', 'g3', 'Students seated for a yoga session', False),
    ('ceremony', 'Annual Sports Day', 'g22', 'Young athletes with certificates on the field', False),
]


def gallery_html(items=GAL, limit=None):
    out = []
    for c, cap, g, alt, wide in items[:limit] if limit else items:
        out.append(f'<button data-c="{c}" data-cap="{esc(cap)}" class="g{" wide" if wide else ""}"><img loading="lazy" src="assets/gallery/{g}.jpg" alt="{esc(alt)}"></button>')
    return ''.join(out)


def results_chart():
    data = [('2020-21', 83.0), ('2021-22', 85.1), ('2022-23', 78.3), ('2023-24', 83.7), ('2024-25', 85.2), ('2025-26', 86.2)]
    cols = ''.join(f'<div class="bar-col"><b>{v}</b><i style="--h:{v}%"></i></div>' for _, v in data)
    labs = ''.join(f'<span>{y}</span>' for y, _ in data)
    return f'<div class="bars" data-bars>{cols}</div><div class="bar-labels">{labs}</div>'


def build_index():
    ed = img('img/ED 1.jpeg', 600, name='award-education-today')
    ew = img('img/Mag-1.png', 600, fmt='png', name='award-educationworld')
    dl = img('img/mag-3.png', 600, fmt='png', name='award-digital-learning')
    uc = img('img/mag-5.png', 600, fmt='png', name='award-unified-council')
    sof = img('img/Mag-4.png', 600, fmt='png', name='award-sof')
    c360 = img('img/career 2026.jpeg', 1400, name='award-careers360')
    rids = img('img/RIDS.jpeg', 1200, name='rids-2026-2029')
    ed_full = img('img/ED 1.jpeg', 1200, name='award-education-today-full')
    px = img('img/principal1.jpeg', 900, name='principal')
    res_x = img('img/1.jpeg', 1200, name='result-class-x-2025-26')
    res_xii = img('img/3.jpeg', 1200, name='result-class-xii-2025-26')

    stats = [('1991', 'Founded under the DPS Society, New Delhi', None), ('13', 'Acres of campus', None), ('100%', 'Board pass rate, five years running', None),
             ('4', 'Houses: Chenab, Ganges, Jhelum, Krishna', None), ('59', 'Teachers', None), ('16+', 'Clubs & activities', None)]
    stat_html = ''.join(f'<div><b>{n}</b><span>{t}</span></div>' for n, t, _ in stats)

    why = [
        ('trophy', 'Consistent academic excellence', '100% pass in Classes X and XII every year from 2020-21 to 2025-26, with toppers scoring 98.8% and 96.8%.'),
        ('flask', 'Well-equipped laboratories', 'Separate Physics, Chemistry, Biology, Maths and Computer Science labs for hands-on learning.'),
        ('monitor', 'Digital classrooms', 'Technology and automation built into the school system, equipping students with 21st-century skills.'),
        ('lib', 'A library that is always growing', 'Over 6,000 reference books, 12 magazines, 4 periodicals and 5 dailies — replenished regularly.'),
        ('run', 'Sprawling playground', 'More than 32,000 sq. m of playground, indoor games, and a full calendar of sports and Inter-House events.'),
        ('palette', 'Arts, music & dance', 'Dedicated music and dance rooms, art and painting, dramatics, creative writing and public speaking.'),
        ('globe', 'International dimension', 'Recognised by the British Council for an International Dimension in Schools (2026–2029).'),
        ('heart', 'Character first', 'Service before Self: assemblies, house system, scholar awards and a clear, fair discipline policy.'),
    ]
    why_html = ''.join(f'<article class="card hover reveal"><div class="ico">{ICON[i]}</div><h3>{t}</h3><p>{d}</p></article>' for i, t, d in why)

    steps = [('Dec – Jan', 'Registration', 'Names are registered from the second half of December to January.'),
             ('Feb – Mar', 'Test & interview', 'Written test in English, Hindi and Maths. Nursery: a meeting with teachers and the Principal.'),
             ('After tests', 'Selection list', 'The final list of selected candidates is displayed on the School Notice Board.'),
             ('April', 'Session begins', 'An orientation programme is held for new parents; school starts on the first working day of April.')]
    steps_html = ''.join(f'<div class="step reveal"><small>{a}</small><h3>{b}</h3><p>{c}</p></div>' for a, b, c in steps)

    body = f'''
<section class="hero" aria-label="Welcome">
  <div class="slides" aria-hidden="true">
    <div class="slide on" style="background-image:url(assets/gallery/g9.jpg)"></div>
    <div class="slide" style="background-image:url(assets/gallery/g7.jpg)"></div>
    <div class="slide" style="background-image:url(assets/gallery/g13.jpg)"></div>
    <div class="slide" style="background-image:url(assets/gallery/g18.jpg)"></div>
    <div class="slide" style="background-image:url(assets/gallery/g21.jpg)"></div>
  </div>
  <div class="wrap hero-inner">
    <p class="eyebrow">Established 1991 · Under the aegis of the DPS Society, New Delhi</p>
    <h1>Service <em>before</em> Self.</h1>
    <p class="lead">For over three decades we have nurtured the body, mind, heart and soul of every child — so they can excel in academics and leave a legacy.</p>
    <div class="hero-cta">
      <a class="btn btn-gold" href="admissions.html#process">Admissions</a>
      <a class="btn btn-ghost" href="contact.html#visit">Plan a campus visit</a>
      <a class="btn btn-ghost" href="#life">See life at DPS</a>
    </div>
  </div>
  <a class="hero-badge" href="#recognition" style="text-decoration:none;color:#fff"><b>No. 1 in Visakhapatnam</b><span>No. 1 in Andhra Pradesh · India’s Top 20 CBSE Schools (Education Today)</span></a>
  <div class="dots" role="tablist" aria-label="Choose background photo"></div>
</section>

<section class="stats" aria-label="School highlights"><div class="wrap stat-grid">{stat_html}</div></section>

<section class="section tight"><div class="wrap">
  <div class="quick reveal">
    <a href="admissions.html#process"><b>Admissions</b><span>Process, dates &amp; application form</span></a>
    <a href="{FEES}" target="_blank" rel="noopener"><b>Pay School Fees</b><span>Online via SBI Collect</span></a>
    <a href="{ERP}" target="_blank" rel="noopener"><b>ERP Portal</b><span>Parent &amp; student login</span></a>
    <a href="resources.html#assignments"><b>Assignments</b><span>Aug–Sep 2026-27, all classes</span></a>
    <a href="news.html"><b>Circulars</b><span>Notices for parents</span></a>
    <a href="resources.html#booklist"><b>Book List 2026-27</b><span>Download the PDF</span></a>
    <a href="academics.html#calendar"><b>School Calendar</b><span>Academic &amp; assessment dates</span></a>
    <a href="disclosure.html"><b>Mandatory Disclosure</b><span>As per CBSE directive</span></a>
  </div>
</div></section>

<section class="section tight" id="latest"><div class="wrap">
  <div class="split top">
    <div class="reveal"><p class="eyebrow dark">Latest news</p><h2 style="font-size:1.8rem">What’s happening at DPS</h2><div class="newslist" id="latestNews"><p class="note">Loading…</p></div><p><a class="btn btn-line btn-sm" href="news.html#achievements">All news →</a></p></div>
    <div class="reveal"><p class="eyebrow dark">Circulars</p><h2 style="font-size:1.8rem">Latest circulars</h2><ul class="doclist" id="latestCirc" style="grid-template-columns:1fr"><li><span class="note">Loading…</span></li></ul><p><a class="btn btn-line btn-sm" href="news.html#circulars">All circulars →</a></p></div>
  </div>
</div></section>

<section class="section" id="about" style="padding-top:30px"><div class="wrap">
  <div class="split">
    <div class="reveal">
      <p class="eyebrow dark">About the school</p>
      <h2>A place where learning is a joy</h2>
      <p>Delhi Public School Visakhapatnam was established in 1991 and imparts quality education with the most modern teaching techniques, so its students can compete with the world. It provides a congenial atmosphere for the total development of the whole personality and its integration with society.</p>
      <p>The school inculcates personal hygiene, neatness, cleanliness, graceful manners and discipline, in an environment that fosters a spirit of enquiry and keen competition — with personal attention to every child and a competent, supportive staff.</p>
      <p><a class="btn btn-green" href="about.html">Read our story</a></p>
    </div>
    <div class="photo reveal" style="aspect-ratio:4/3"><img src="assets/gallery/g12.jpg" alt="Annual Awards and Investiture ceremony" loading="lazy"></div>
  </div>
  <div class="four reveal" style="margin:56px 0 40px" aria-label="Our four dimensions">
    <article><span class="ico">◆</span><h3>Body</h3><p>to live</p></article>
    <article><span class="ico">◆</span><h3>Mind</h3><p>to learn</p></article>
    <article><span class="ico">◆</span><h3>Heart</h3><p>to love</p></article>
    <article><span class="ico">◆</span><h3>Soul</h3><p>to leave a legacy</p></article>
  </div>
  <div class="tabs reveal" data-tabs>
    <div class="tablist" role="tablist" aria-label="Our approach">
      <button role="tab" aria-selected="true" aria-controls="p1" id="t1">Philosophy</button>
      <button role="tab" aria-selected="false" aria-controls="p2" id="t2" tabindex="-1">Aim</button>
      <button role="tab" aria-selected="false" aria-controls="p3" id="t3" tabindex="-1">International Policy</button>
    </div>
    <div class="panel" role="tabpanel" id="p1" aria-labelledby="t1">
      <p class="motto">Motto: <strong>Service before Self</strong></p>
      <p>To develop all four human dimensions — Body, Mind, Heart and Soul.</p>
      <p>Our objective is to enable students to excel in academics, recognise their full potential and develop good habits so that they can contribute to the progress of the world — using the three great gifts given to every human being: the <strong>Power of Choice</strong>, the <strong>Power of Intelligence</strong> and the <strong>Power of Conscience</strong>.</p>
    </div>
    <div class="panel" role="tabpanel" id="p2" aria-labelledby="t2" hidden>
      <p>Our aim is to impart sound and liberal education to boys and girls during their impressionable years — an education that lays stress on character building, team work, esprit-de-corps and physical development, and infuses a spirit of adventure, fair play and justice.</p>
      <p>We aim to develop among our students a feeling of pride in Indian culture, and to produce citizens who are truly Indian and above social, communal, religious or provincial prejudices.</p>
    </div>
    <div class="panel" role="tabpanel" id="p3" aria-labelledby="t3" hidden>
      <p>To encourage young minds to develop understanding, tolerance and appreciation of the diverse cultures of the world.</p>
      <p>To nurture global citizens who play a responsible role in sustainable development in a changing world.</p>
    </div>
  </div>
</div></section>

<section class="section alt" id="why"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Why DPS Visakhapatnam</p><h2>Everything a child needs to grow</h2><p>From classrooms and labs to playgrounds and stages — a campus built for the whole child.</p></div>
  <div class="grid g4">{why_html}</div>
</div></section>

<section class="section" id="recognition"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Recognition</p><h2>Adjudged “The Best School”</h2><p>Honours and rankings earned by the school community. Tap any card to enlarge the certificate.</p></div>
  <div class="awards reveal">
    <button class="award" data-zoom="{ed_full}" data-cap="Education Today — India’s Top 20 CBSE Schools"><img src="{ed}" alt="Education Today certificate" loading="lazy"><b>India’s Top 20 CBSE Schools</b><span class="rank">No. 19</span><span>No. 1 in Visakhapatnam &amp; Andhra Pradesh · Education Today</span></button>
    <button class="award" data-zoom="{c360}" data-cap="Careers360 — India’s Best Schools 2026"><img src="{thumb('img/career 2026.jpeg', 500, name='award-careers360')}" alt="Careers360 certificate" loading="lazy"><b>India’s Best Schools 2026</b><span class="rank">AAA+</span><span>Day School category, 2025-26 · Careers360</span></button>
    <button class="award" data-zoom="{ew}" data-cap="EducationWorld rankings"><img src="{ew}" alt="EducationWorld ranks" loading="lazy"><b>EducationWorld</b><span class="rank">AIR 168</span><span>City Rank 1 · State Rank 1</span></button>
    <button class="award" data-zoom="{dl}" data-cap="Digital Learning — Rank #1"><img src="{dl}" alt="Digital Learning" loading="lazy"><b>Digital Learning</b><span class="rank">Rank #1</span><span>Digital Learning magazine</span></button>
    <button class="award" data-zoom="{uc}" data-cap="Unified Council — Best District School"><img src="{uc}" alt="Unified Council" loading="lazy"><b>Best District School</b><span class="rank">Unified Council</span><span>Foundation for Success</span></button>
    <button class="award" data-zoom="{sof}" data-cap="Science Olympiad Foundation — Best AP Zone School"><img src="{sof}" alt="Science Olympiad Foundation" loading="lazy"><b>Best AP Zone School</b><span class="rank">SOF</span><span>Science Olympiad Foundation</span></button>
    <button class="award" data-zoom="{rids}" data-cap="British Council — Recognition of an International Dimension in Schools 2026–2029"><img src="{thumb('img/RIDS.jpeg', 400, name='rids-2026-2029')}" alt="RIDS 2026–2029" loading="lazy"><b>International Dimension</b><span class="rank">RIDS</span><span>British Council · 2026–2029</span></button>
  </div>
</div></section>

<section class="section principal alt" id="principal"><div class="wrap p-grid">
  <figure class="reveal"><img src="{px}" alt="Mr. Samir Kumar Pandey, Principal" width="852" height="965" loading="lazy"></figure>
  <div class="reveal">
    <p class="eyebrow dark">Principal speaks</p>
    <blockquote><p>“The will to win, the desire to succeed, the urge to reach your full potential… these are the keys that will unlock the door to personal excellence.”</p></blockquote>
    <p class="sig"><strong>Samir Kumar Pandey</strong><br>Principal</p>
    <p><a class="btn btn-green" href="about.html#principal">Read the full message</a></p>
  </div>
</div></section>

<section class="section results" id="results"><div class="wrap" id="resultsDyn">
  <div class="section-head reveal light"><p class="eyebrow">Session 2025–26</p><h2>Results that speak</h2><p>Consistently setting benchmarks in academic excellence.</p></div>
  <div class="res-grid">
    <article class="res reveal"><header><span>Class X</span><b>100% result</b></header><div class="big">98.8<small>%</small></div><p class="who">Cheruku Anvith Raj <em>· school topper</em></p>
      <ul><li><span>Class average</span><b>86.2</b></li><li><span>Students appeared</span><b>158</b></li><li><span>Students passed</span><b>158</b></li></ul>
      <p style="margin:18px 0 0"><button class="btn btn-gold btn-sm" data-zoom="{res_x}" data-cap="Class X results 2025-26">View result poster</button></p></article>
    <article class="res reveal"><header><span>Class XII</span><b>100% result</b></header><div class="big">96.8<small>%</small></div><p class="who">Bikash Kumar Barik <em>· school topper</em></p>
      <ul><li><span>Class average</span><b>80.5</b></li><li><span>Students appeared</span><b>17</b></li><li><span>Students passed</span><b>17</b></li></ul>
      <p style="margin:18px 0 0"><button class="btn btn-gold btn-sm" data-zoom="{res_xii}" data-cap="Class XII results 2025-26">View result poster</button></p></article>
  </div>
  <div class="chart reveal" style="margin-top:24px"><h3>Class X average, last six years</h3><p class="note" style="margin:0">Percent. Every year has produced a 100% pass result in Classes X and XII.</p>{results_chart()}</div>
</div></section>

<section class="section life" id="life"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Glimpses of our latest activities</p><h2>Life at DPS</h2></div>
  <div class="filters reveal" role="group" aria-label="Filter photos">
    <button class="chip on" data-f="all">All</button><button class="chip" data-f="ceremony">Ceremonies</button><button class="chip" data-f="culture">Culture</button><button class="chip" data-f="sports">Sports &amp; wellness</button>
  </div>
  <div class="gallery" id="gallery" data-limit="16">{gallery_html()}</div>
  <p style="margin-top:26px"><a class="btn btn-line" href="gallery.html">Explore the full gallery →</a></p>
</div></section>

<section class="section alt" id="admissions"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Admissions</p><h2>Join the DPS family</h2><p>Simple, transparent and personal. Here is how a year of admissions flows.</p></div>
  <div class="steps">{steps_html}</div>
  <p style="margin-top:28px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-green" href="admissions.html">Admission details</a><button class="btn btn-line" data-open="enquiry">Send an enquiry</button><a class="btn btn-line" href="{doc('docs/Std_ApplicationForm.pdf')}">Application form (PDF)</a></p>
</div></section>

<section class="section"><div class="wrap">
  <div class="split top">
    <div class="reveal"><p class="eyebrow dark">Important days</p><h2>Our school year at a glance</h2><p>The school observes national and international days throughout the year. The next upcoming one is highlighted for you.</p>
      <p><a class="btn btn-line" href="academics.html#calendar">Full calendars</a></p></div>
    <div class="days reveal" id="daysHome" style="grid-template-columns:1fr">{days_html()}</div>
  </div>
</div></section>

<section class="section alt" id="resources"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">For students &amp; parents</p><h2>Everything in one place</h2></div>
  <div class="quick reveal">
    <a href="news.html"><b>Circulars &amp; News</b><span>Notices and media</span></a>
    <a href="resources.html#syllabus"><b>Syllabus Breakup</b><span>Class-wise PDFs</span></a>
    <a href="resources.html#magazine"><b>School Magazine</b><span>Aurora Australis</span></a>
    <a href="resources.html#careers"><b>Careers</b><span>Join our team</span></a>
    <a href="staff.html"><b>Faculty &amp; Staff</b><span>Meet our people</span></a>
    <a href="campus.html#council"><b>Student Council</b><span>Our flag bearers</span></a>
    <a href="campus.html#rids"><b>RIDS</b><span>International dimension</span></a>
    <a href="contact.html#alumni"><b>Alumni</b><span>Stay connected</span></a>
  </div>
</div></section>

<section class="section" id="contact"><div class="wrap c-grid">
  <div class="reveal">
    <p class="eyebrow dark">Get in touch</p><h2>Visit us or write to us</h2>
    <div class="ci">
      <div><span class="ico">{ICON['pin']}</span><p><small>Address</small>Delhi Public School, Sector VIII, Ukkunagaram,<br>Visakhapatnam, Andhra Pradesh – 530032</p></div>
      <a href="tel:{PHONE_TEL}"><span class="ico">{ICON['phone']}</span><p><small>Phone</small>{PHONE} · 0891 2886880</p></a>
      <a href="mailto:{EMAIL}"><span class="ico">{ICON['mail']}</span><p><small>Email</small>{EMAIL}</p></a>
    </div>
    <form class="form" data-mailto="{EMAIL}" data-subject="Message from website">
      <div class="row"><label>Your name<input name="Name" required autocomplete="name"></label><label>Email or phone<input name="Contact" required></label></div>
      <label>Message<textarea name="Message" rows="3" required></textarea></label>
      <button class="btn btn-green" type="submit">Send message</button><p class="note" style="margin:0">Opens your email app, addressed to the school office.</p>
    </form>
  </div>
  <div class="map reveal"><iframe title="Map to Delhi Public School Visakhapatnam" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=Delhi%20Public%20School%20Visakhapatnam%20Steel%20Plant&output=embed"></iframe></div>
</div></section>
'''
    ld = '''<script type="application/ld+json">{"@context":"https://schema.org","@type":"School","name":"Delhi Public School Visakhapatnam Steel Plant","foundingDate":"1991","telephone":"+91-891-2510686","email":"dpsvisakhapatnam@gmail.com","address":{"@type":"PostalAddress","streetAddress":"Sector VIII, Ukkunagaram","addressLocality":"Visakhapatnam","addressRegion":"Andhra Pradesh","postalCode":"530032","addressCountry":"IN"},"parentOrganization":{"@type":"Organization","name":"Delhi Public School Society"}}</script>'''
    return page('index.html', 'Home', 'Delhi Public School, Visakhapatnam Steel Plant — educating the body, mind, heart and soul since 1991. Admissions, results, gallery, assignments, circulars and more.', None, body, extra_head=ld)
