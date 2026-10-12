import os, re, json
from core import img, thumb, doc, esc, main_of, rewrite_links, text_of, size_of, ORIG, read_crawl, clean_html
from layout import ICON, page, hero_page, subnav, ERP, FEES, PHONE, PHONE_TEL, EMAIL
from pages_a import prose, docimg
from pages_home import GAL, gallery_html

REG = 'https://forms.edunexttechnologies.com/forms/dps-visakhapatnam/registration/'
REC = 'https://forms.edunexttechnologies.com/forms/dps-visakhapatnam/Recruitment/'


# ---------------------------------------------------------------- CAMPUS
def build_campus():
    infra = rewrite_links(main_of('infrastructure.html'))
    facilities = [
        ('flask', 'Science laboratories', 'Physics, Chemistry and Biology labs (22 × 48 ft each) for practical learning.'),
        ('book', 'Maths lab', 'A dedicated Mathematics laboratory (22 × 45 ft).'),
        ('monitor', 'Computer science lab', 'A 27 × 45 ft computer lab, plus digital classrooms.'),
        ('lib', 'Library', '48 × 32 ft with 6,080 reference books, 12 magazines, 4 periodicals and 5 dailies.'),
        ('run', 'Playground & indoor games', 'A 32,375 sq. m playground and indoor games facilities.'),
        ('music', 'Music & dance rooms', 'Dedicated rooms for music and dance.'),
        ('bus', 'Transport', 'School’s own and outsourced buses.'),
        ('shield', 'Health care', 'Health and medical check-ups are done by VSGH.'),
    ]
    fh = ''.join(f'<article class="card hover reveal"><div class="ico">{ICON[i]}</div><h3>{t}</h3><p>{d}</p></article>' for i, t, d in facilities)
    clubs = ['Quiz Club', 'Music', 'Dance', 'Public Speaking', 'Sports', 'Science', 'Yoga & Health Club', 'Art and Painting', 'Handwriting', 'Maths', 'Martial Art', 'Creative Writing', 'Environment', 'Dramatics', 'Gardening', 'First Aid Club']
    extra = ['Home Science', 'Information Technology', 'Library', 'Arabic Language', 'YESS Club', 'Sanskrit']
    ch = ''.join(f'<span class="pill" style="font-size:.85rem;padding:.4em 1em">{esc(c)}</span> ' for c in clubs)
    ex = ''.join(f'<span class="pill" style="font-size:.85rem;padding:.4em 1em;background:#fbefd0;color:#6b4a00">{esc(c)}</span> ' for c in extra)
    rids = img('img/RIDS.jpeg', 1200, name='rids-2026-2029')
    body = hero_page('Campus Life', 'A 13-acre campus, sixteen clubs, four houses and a calendar full of celebrations.') + subnav([
        ('infrastructure', 'Infrastructure'), ('houses', 'Houses & Clubs'), ('assembly', 'Morning Assembly'), ('council', 'Student Council'), ('discipline', 'Discipline'), ('rids', 'RIDS')]) + f'''
<section class="section" id="infrastructure"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Infrastructure</p><h2>A campus built for learning</h2><p>Spread over 13 acres (52,609 sq. m) in the Steel Township, Ukkunagaram.</p></div>
  <div class="grid g4" style="margin-bottom:46px">{fh}</div>
  <div class="prose" style="max-width:none"><div class="reveal">{infra}</div></div>
</div></section>

<section class="section alt" id="houses"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Functioning of the school</p><h2>House system &amp; clubs</h2><p>The house system forms the basis of all competitions in the school. It promotes team spirit, group loyalty and healthy competition. The school is divided into four houses named after rivers; students compete in Inter-House competitions, demonstrating their talents and skills to bring glory to their houses.</p></div>
  <div class="houses reveal"><div class="house h-chenab"><b>Chenab</b><span>House</span></div><div class="house h-ganges"><b>Ganges</b><span>House</span></div><div class="house h-jhelum"><b>Jhelum</b><span>House</span></div><div class="house h-krishna"><b>Krishna</b><span>House</span></div></div>
  <div class="reveal" style="margin-top:40px"><h3>Clubs &amp; activities</h3><p class="note">Activities for Classes II to XII</p><p style="line-height:2.4">{ch}</p>
  <p class="note" style="margin-top:20px">Additional activities for Classes VI onwards</p><p style="line-height:2.4">{ex}</p></div>
</div></section>

<section class="section" id="assembly"><div class="wrap split top">
  <div class="reveal prose"><p class="eyebrow dark">Various activities</p><h2>Conducting morning assemblies</h2>
    <p>Morning Assembly is conducted by one particular class for the whole week. It is held on Mondays, Wednesdays and Fridays. On Mondays and Wednesdays it is held in English and on Fridays in Telugu / Hindi / Sanskrit.</p>
    <p>The Morning Assembly begins with ‘Vande Mataram’ and is followed by prayers, then mass PT, Patriotic Song, Scripture, Reading News, Speeches, Recitation of Poetry, a few creative demonstrations, and ends with the ‘National Anthem’. This provides the school with an excellent opportunity to develop the overall personality of the students and helps them shed their stage fear.</p></div>
  <div class="photo reveal" style="aspect-ratio:4/3"><img src="assets/gallery/g10.jpg" alt="Children on stage" loading="lazy"></div>
</div></section>

<section class="section alt" id="council"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Academic year 2025-26</p><h2>Student Council — our flag bearers</h2><p>The Student Council of DPS Visakhapatnam includes the Senior School council, House Prefects and Vice House Prefects, installed at the annual Investiture Ceremony.</p></div>
  <div class="grid g3 reveal"><div class="card"><div class="ico">{ICON['users']}</div><h3>Senior School</h3><p>Head Boy, Head Girl and senior council members.</p></div><div class="card"><div class="ico">{ICON['trophy']}</div><h3>House Prefects</h3><p>One for each of the four houses.</p></div><div class="card"><div class="ico">{ICON['heart']}</div><h3>Vice House Prefects</h3><p>Supporting prefects in each house.</p></div></div>
  <div class="grid g2" style="margin-top:20px"><div class="photo reveal" style="aspect-ratio:4/3"><img src="assets/gallery/g9.jpg" alt="Investiture ceremony group" loading="lazy"></div><div class="photo reveal" style="aspect-ratio:4/3"><img src="assets/gallery/g12.jpg" alt="Investiture ceremony awards" loading="lazy"></div></div>
</div></section>

<section class="section" id="discipline"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Punishment policy</p><h2>A clear, fair disciplinary system</h2></div>
  <div class="grid g3 reveal">
    <article class="card" style="border-top:6px solid #e3b505"><h3>Yellow card</h3><p>Issued in an academic year for:</p><ul><li>Three late comings to school</li><li>Use of abusive language</li><li>Unruly &amp; indisciplined behaviour in class</li><li>Pilfering, forging signatures</li></ul></article>
    <article class="card" style="border-top:6px solid #8a8f98"><h3>Grey card</h3><ul><li>Three yellow cards issued to a student in one academic year</li><li>Damage to school property</li><li>Physically hurting or injuring fellow mates</li></ul></article>
    <article class="card" style="border-top:6px solid #c0392b"><h3>Red card</h3><ul><li>Three grey cards issued to a student in his entire tenure at school</li><li>Use of vulgar language (oral or written)</li></ul><p class="note">If a student is issued a red card, it amounts to issuing of T.C.</p></article>
  </div>
</div></section>

<section class="section alt" id="rids"><div class="wrap split">
  <div class="reveal"><button class="docimg" data-zoom="{rids}" data-cap="RIDS 2026–2029"><img src="{rids}" alt="Recognition of an International Dimension in Schools 2026–2029" loading="lazy"></button></div>
  <div class="reveal prose"><p class="eyebrow dark">RIDS 2025-26</p><h2>Recognition of an International Dimension in Schools</h2>
    <p>DPS Visakhapatnam has been recognised by the British Council under the <strong>Recognition of an International Dimension in Schools (RIDS) 2026–2029</strong> — a mark of the school’s commitment to global citizenship.</p>
    <p>Our International Policy: to encourage young minds to develop understanding, tolerance and appreciation of the diverse cultures of the world, and to nurture global citizens who play a responsible role for sustainable development in a changing world.</p></div>
</div></section>'''
    return page('campus.html', 'Campus Life', 'Infrastructure, labs, library, house system, clubs, morning assembly, student council, discipline policy and RIDS recognition at DPS Visakhapatnam.', 'Campus Life', body)


# ---------------------------------------------------------------- GALLERY
ALBUMS = [('AntiCrackerRally', 'Anti Cracker Rally'), ('CapacityBuildingProgramme', 'Capacity Building Programme'), ('Exhibition', 'Exhibition'), ('GandhiJayanti', 'Gandhi Jayanti'),
          ('IHD', 'Inter House Dance'), ('Investiture', 'Investiture Ceremony'), ('RepublicDay', 'Republic Day Ceremony'), ('Sankranti', 'Sankranti Celebrations'),
          ('SportsDay', 'Sports Day Celebrations'), ('Swaranjali', 'Swaranjali Inter DPS Competitions')]
EXTRA_GAL = [('ceremony', 'Investiture Ceremony', 'g8', 'Chief guests present a memento at the Investiture Ceremony', False),
             ('culture', 'Annual celebrations', 'g6', 'Performers in colourful traditional costume', False),
             ('culture', 'Grandparents’ Day', 'g11', 'Children in pastel outfits on stage', False),
             ('ceremony', 'Scholar Badge presentation', 'g15', 'Students in blazers on the field', False),
             ('ceremony', 'Pedda Panduga Celebrations', 'g20', 'Guests receive mementos on stage', False),
             ('ceremony', 'Workshop', 'g2', 'A speaker addresses a gathering in the hall', False)]


def build_gallery():
    albums, data = [], {}
    for d, name in ALBUMS:
        folder = os.path.join(ORIG, 'pages', 'photogallery', d, 'images')
        files = sorted([f for f in os.listdir(folder) if f.endswith('.jpg')], key=lambda x: int(x.split('.')[0])) if os.path.isdir(folder) else []
        urls = [img(f'pages/photogallery/{d}/images/{f}', 1400, name=f'album-{d.lower()}-{f.split(".")[0]}') for f in files]
        if not urls:
            continue
        cover = thumb(f'pages/photogallery/{d}/images/{files[0]}', 520, name=f'album-{d.lower()}-{files[0].split(".")[0]}')
        data[d] = [dict(src=u, cap=name) for u in urls]
        albums.append(f'<button class="album" data-album="{d}"><img src="{cover}" alt="{esc(name)}" loading="lazy"><div><b>{esc(name)}</b><span>{len(urls)} photos · 2018-19</span></div></button>')
    all_items = GAL + EXTRA_GAL
    body = hero_page('Photo Gallery', 'Celebrations, competitions and everyday moments from DPS Visakhapatnam.') + subnav([('latest', 'Latest activities'), ('albums', 'Event albums')]) + f'''
<section class="section" id="latest"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Glimpses of our latest activities</p><h2>Latest activities</h2></div>
  <div class="filters reveal" role="group" aria-label="Filter photos"><button class="chip on" data-f="all">All</button><button class="chip" data-f="ceremony">Ceremonies</button><button class="chip" data-f="culture">Culture</button><button class="chip" data-f="sports">Sports &amp; wellness</button></div>
  <div class="gallery" id="gallery">{gallery_html(all_items)}</div>
</div></section>
<section class="section alt" id="albums"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Events in 2018-19</p><h2>Event albums</h2><p>Tap an album to browse its photos.</p></div>
  <div class="albums" id="albumsList">{''.join(albums)}</div>
</div></section>
<script type="application/json" id="albumData">{json.dumps(data)}</script>'''
    return page('gallery.html', 'Gallery', 'Photo gallery of events and activities at Delhi Public School Visakhapatnam: investiture, sports day, cultural programmes and more.', 'Gallery', body)


# ---------------------------------------------------------------- NEWS
def build_news():
    px = lambda f, w=1200, n=None: img(f, w, name=n)
    res_x = img('img/1.jpeg', 1200, name='result-class-x-2025-26')
    res_xii = img('img/3.jpeg', 1200, name='result-class-xii-2025-26')
    c360 = img('img/career 2026.jpeg', 1400, name='award-careers360')
    ed = img('img/ED 1.jpeg', 1200, name='award-education-today-full')
    ew = img('img/Mag-1.png', 800, fmt='png', name='award-educationworld')
    sof = img('img/Mag-4.png', 600, fmt='png', name='award-sof')
    dl = img('img/mag-3.png', 600, fmt='png', name='award-digital-learning')
    uc = img('img/mag-5.png', 600, fmt='png', name='award-unified-council')
    rids = img('img/RIDS.jpeg', 1200, name='rids-2026-2029')
    circ = [('Circulars for Parents', 'docs/Circulars_for_Parents.pdf'), ('Circulars for Parents — Class VIII', 'docs/Circulars_for_Parents_VIII.pdf'), ('Circulars for Parents of Classes VI & VII', 'docs/Circulars_for_Parents_of_VI_and_VII.pdf'),
            ('Circular for Classes Nursery to II', 'docs/CIRCULAR_FOR_CLASSES_NUR_to_II.pdf'), ('Consent Form 2021-22', 'docs/Consent Form 2021-22.pdf'), ('CBSE notification regarding Class X & XII board exams', 'docs/CBSE CE Notification.pdf'), ('Notification', 'docs/Notification.pdf')]
    cl = ''.join(f'<li><a href="{doc(r)}" target="_blank" rel="noopener"><span class="ft">PDF</span><span><b>{esc(t)}</b><small>PDF · {size_of(doc(r))}</small></span></a></li>' for t, r in circ)
    aw = lambda src, big, cap, t, s: f'<button class="award" data-zoom="{big}" data-cap="{esc(cap)}"><img src="{src}" alt="{esc(cap)}" loading="lazy"><b>{t}</b><span>{s}</span></button>'
    body = hero_page('News & Circulars', 'Notices for parents, achievements by the school and its children, and DPS in the news.') + subnav([('circulars', 'Circulars'), ('achievements', 'Achievements'), ('news', 'DPS in News')]) + f'''
<section class="section" id="circulars"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Important information to parents and students</p><h2>Circulars</h2><p>Current notices are shared through the school ERP portal and the notice board. Earlier circulars are archived here.</p>
    <p><a class="btn btn-green" href="{ERP}" target="_blank" rel="noopener">Open ERP portal</a></p></div>
  <h3 class="reveal">Circular archive</h3><ul class="doclist" id="circularList">{cl}</ul>
</div></section>

<section class="section alt" id="achievements"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Academic year 2025-26</p><h2>Achievements by school and children</h2></div>
  <div class="newsgrid" id="newsList" style="margin-bottom:40px"></div>
  <h3 class="reveal">Recognition &amp; awards</h3>
  <div class="grid g2" style="margin-bottom:32px;display:none"><button class="docimg reveal" data-zoom="{res_x}" data-cap="Class X — 98.8% — Cheruku Anvith Raj"><img src="{res_x}" alt="Class X result poster" loading="lazy"></button><button class="docimg reveal" data-zoom="{res_xii}" data-cap="Class XII — 96.8% — Bikash Kumar Barik"><img src="{res_xii}" alt="Class XII result poster" loading="lazy"></button></div>
  <div class="awards reveal">
    {aw(img('img/career 2026.jpeg', 500, name='award-careers360-500'), c360, 'Careers360 — India’s Best Schools 2026 (AAA+)', 'India’s Best Schools 2026', 'AAA+ · Careers360')}
    {aw(img('img/ED 1.jpeg', 500, name='award-education-today'), ed, 'Education Today — India’s Top 20 CBSE Schools', 'India’s Top 20 CBSE Schools', 'No. 1 in Vizag · No. 19 in India')}
    {aw(ew, ew, 'EducationWorld rankings', 'EducationWorld', 'City 1 · State 1 · AIR 168')}
    {aw(dl, dl, 'Digital Learning Rank #1', 'Digital Learning', 'Rank #1')}
    {aw(uc, uc, 'Unified Council — Best District School', 'Best District School', 'Unified Council')}
    {aw(sof, sof, 'Science Olympiad Foundation — Best AP Zone School', 'Best AP Zone School', 'Science Olympiad Foundation')}
    {aw(img('img/RIDS.jpeg', 400, name='rids-2026-2029-400'), rids, 'RIDS 2026–2029', 'International Dimension', 'British Council · RIDS 2026–2029')}
  </div>
</div></section>

<section class="section" id="news"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Print &amp; electronic media</p><h2>DPS in the news</h2><p>Important activities covered by print and electronic media will appear here. Follow the school’s Facebook page for the latest updates.</p>
    <p><a class="btn btn-line" href="https://www.facebook.com/profile.php?id=100074407933164" target="_blank" rel="noopener">DPS on Facebook →</a></p></div>
</div></section>'''
    return page('news.html', 'News & Circulars', 'Circulars, achievements, awards and news from Delhi Public School Visakhapatnam.', 'Updates', body)


# ---------------------------------------------------------------- RESOURCES
ASSIGN = [('Balvatika II', 'cl- Bal II Aug - Sep Assignment 2026.pdf'), ('Balvatika III', 'cl-Bal III  Aug- Sep Assignment 2026.pdf'), ('Class 1', 'cl-  I  Aug- Sep Assignment 2026.pdf'),
          ('Class 2', 'cl- II Aug - Sep Assignment 2026.pdf'), ('Class 3', 'cl- III HYE Revision Assignment 2026.pdf'), ('Class 4', 'cl-IV HYE Revision Assignment 2026.pdf'),
          ('Class 5', 'cl-V HYE Revision Assignment 2026.pdf'), ('Class 6', 'cl- VI   HYE Revision Assignment 2026.pdf'), ('Class 7', 'cl-VII HYE Revision Assignment 2026.pdf'),
          ('Class 8', 'cl-VIII HYE Revision Assignment 2026.pdf'), ('Class 9', 'cl-IX HYE Revision Assignment 2026.pdf'), ('Class 10', 'cl-X  HYE Revision Assignment 2026.pdf'),
          ('Class 11 Science', 'cl- XI Science HYE Revision Assignment 2026.pdf'), ('Class 11 Commerce', 'cl- XI Commerce HYE Revision Assignment 2026.pdf'),
          ('Class 12 Science', 'cl- XII Science HYE Revision Assignment 2026.pdf'), ('Class 12 Commerce', 'cl-XII Commerce  HYE Revision Assignment 2026.pdf')]
SYL = [('Nursery', 'Class Nursery  Syllabus 2023-24.pdf'), ('Prep', 'Class Prep.  Syllabus 2023-24.pdf'), ('Class I', 'Class I Syllabus 2023-24.pdf'), ('Class II', 'Class II Syllabus 2023-24.pdf'),
       ('Class III', 'Class III Syllabus 2023-24.pdf'), ('Class IV', 'Class IV Syllabus 2023-24.pdf'), ('Class V', 'Class V Syllabus 2023-24.pdf'), ('Class VI', 'Class VI Syllabus 2023-24.pdf'),
       ('Class VII', 'Class VII Syllabus 2023-24.pdf'), ('Class VIII', 'Class VIII Syllabus 2023-24.pdf'), ('Class IX', 'Class IX Syllabus 2023-24.pdf'), ('Class X', 'Class X Syllabus 2023-24.pdf'),
       ('Class XI', 'Class XI Syllabus 2023-24.pdf'), ('Class XII', 'Class XII Syllabus 2023-24.pdf')]


def build_resources():
    ach = ''.join(f'<li data-cat="assignments"><a href="{doc("docs/assignments/" + f)}" target="_blank" rel="noopener"><span class="ft">PDF</span><span><b>{l}</b><small>Assignment 2026-27 · PDF · {size_of(doc("docs/assignments/" + f))}</small></span></a></li>' for l, f in ASSIGN)
    syl = ''.join(f'<li data-cat="syllabus"><a href="{doc("docs/syllabus/" + f)}" target="_blank" rel="noopener"><span class="ft">PDF</span><span><b>{l}</b><small>Syllabus break-up 2023-24 · PDF · {size_of(doc("docs/syllabus/" + f))}</small></span></a></li>' for l, f in SYL)
    book, mag = doc('docs/Book List 2026-27.pdf'), doc('docs/MAGAZINE 2025.pdf')
    forms = [('Student enrolment form', 'docs/Std_ApplicationForm.pdf'), ('Application form', 'docs/Application Form.pdf'), ('Transfer certificate sample', 'docs/tc sample.pdf'), ('Consent form 2021-22', 'docs/Consent Form 2021-22.pdf')]
    fm = ''.join(f'<li data-cat="forms"><a href="{doc(r)}" target="_blank" rel="noopener"><span class="ft">PDF</span><span><b>{t}</b><small>Form · PDF · {size_of(doc(r))}</small></span></a></li>' for t, r in forms)
    body = hero_page('Resources & Downloads', 'Assignments, syllabus break-ups, book lists, the school magazine and forms — all downloadable.') + subnav([
        ('assignments', 'Assignments'), ('booklist', 'Book List'), ('syllabus', 'Syllabus'), ('magazine', 'Magazine'), ('forms', 'Forms'), ('careers', 'Careers')]) + f'''
<section class="section tight"><div class="wrap">
  <div class="docbar reveal"><input type="search" id="docQ" placeholder="Search all downloads — e.g. “class 7”, “syllabus”, “form”…" aria-label="Search downloads"><span class="note" id="docCount"></span></div>
</div></section>
<section class="section" id="assignments" style="padding-top:0"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Aug – Sep Assignments 2026-27</p><h2 id="assignH">Assignments for all classes</h2><p id="assignNote">Classes Balvatika to II: August–September assignments. Classes 3 to 12: half-yearly exam (HYE) revision assignments. Please click on the class to download the assignment.</p></div>
  <ul class="doclist" data-docs id="assignList">{ach}</ul>
</div></section>

<section class="section alt" id="booklist"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Book list</p><h2 id="bookH">Book list — academic year 2026-27</h2></div>
  <div class="reveal"><iframe id="bookFrame" class="pdf-frame" src="{book}" title="Book list" loading="lazy"></iframe><p style="margin-top:14px"><a id="bookDl" class="btn btn-green btn-sm" href="{book}" download>Download PDF ({size_of(book)})</a></p></div>
</div></section>

<section class="section" id="syllabus"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Syllabus break-up for academic year 2023-24</p><h2 id="sylH">Syllabus for all classes</h2><p id="sylNote">Please click on the class to download the syllabus break-up.</p></div>
  <ul class="doclist" data-docs id="syllabusList">{syl}</ul>
</div></section>

<section class="section alt" id="magazine"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark" id="magSub">Annual magazine for academic year 2024-25</p><h2 id="magH">Aurora Australis — The Southern Lights</h2></div>
  <div class="reveal"><iframe id="magFrame" class="pdf-frame" src="{mag}" title="Annual magazine" loading="lazy"></iframe><p style="margin-top:14px"><a id="magDl" class="btn btn-green btn-sm" href="{mag}" download>Download magazine ({size_of(mag)})</a></p></div>
</div></section>

<section class="section" id="forms"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Forms &amp; formats</p><h2>Forms</h2></div>
  <ul class="doclist reveal" data-docs>{fm}</ul>
  <p style="margin-top:20px"><a class="btn btn-line btn-sm" href="{REG}" target="_blank" rel="noopener">Online registration form →</a> <span class="note">Availability depends on the admission season.</span></p>
</div></section>

<section class="section alt" id="careers"><div class="wrap split">
  <div class="reveal"><p class="eyebrow dark">Current openings</p><h2>Join our team</h2><p>DPS Visakhapatnam is always glad to hear from passionate educators and professionals. Job openings are announced on this page and on the school notice board.</p>
    <p><a class="btn btn-green" href="{REC}" target="_blank" rel="noopener">Apply online →</a> <a class="btn btn-line" href="mailto:{EMAIL}?subject=Job%20application">Email your CV</a></p></div>
  <div class="card reveal"><div class="ico">{ICON['cap']}</div><h3>Why teach at DPS?</h3><p>Be part of a school of the Delhi Public School Society that invests in in-service teacher education, workshops and professional growth — see our <a href="academics.html#training">staff training records</a>.</p></div>
</div></section>
<script type="application/json" id="docIndex">{json.dumps([])}</script>'''
    return page('resources.html', 'Resources & Downloads', 'Download class-wise assignments, syllabus break-ups, the 2026-27 book list, school magazine and forms from DPS Visakhapatnam.', 'Updates', body)


# ---------------------------------------------------------------- DISCLOSURE
PTA = [('Balvatika – II', 'Gutta Sireesha'), ('Balvatika – III', 'Himanshu Raj'), ('I', 'Abhishek Kumar'), ('II', 'Prabhat Chandra'), ('III', 'Krishnadeo Yadav'), ('IV', 'Chandan Sarkar'),
       ('V', 'Biswabandhu Mohapatra'), ('VI', 'P Arjun Kumar'), ('VII', 'Divecha Prabhakar M'), ('VIII', 'Saraswati Kallo'), ('IX', 'Satish Kumar Singh'), ('X', 'Ajay Vikram S'),
       ('XI', 'Muralidhar Banu'), ('XII', 'G Usha')]
SMC = [('Shri Rahul Singh', 'Chairperson', 'Colaba, Mumbai – 400005', 'Three years'), ('Dr (Mrs) Malini Vijay Shankar', 'Vice Chairperson', 'Uthadi, Chennai – 600119', 'Three years'),
       ('Shri Shantanu Consul', 'Member', 'BTM 2nd Stage, Bangalore – 560076', 'Three years'), ('Shri Rakesh Kacker', 'Member', 'Defence Colony, New Delhi – 110024', 'Three years'),
       ('Shri Pravin Srivastava', 'Member', 'Eldeco Utopia Expressway, Noida – 201301, UP', 'Three years'), ('Mrs N Bhanu', 'Pro Vice Chairperson', 'GM (HR), RINL VSP', 'Until further posting'),
       ('Shri J Rahul', 'Member', 'DGM (TA) I/c, RINL VSP', 'Until further posting'), ('Shri Ch Leela Srinivas', 'Member', 'DGM (F&A), RINL VSP', 'Until further posting'),
       ('Shri Padma Ranjan Roy', 'Member', 'Sr Manager (TA)', 'Until further posting'), ('Shri Samir Kumar Pandey', 'Secretary', 'Principal, DPS Visakhapatnam Steel Plant, Sector-VIII, Ukkunagaram, Visakhapatnam – 530032', 'Until further posting')]
COMM = [('Redressal of Public Grievance', 'Ms K V R S Madhuri (TGT) · Mr B Mutyala Rao (Office Superintendent) · Mr T Srinivas Rao (LDC)'),
        ('Redressal of Staff Grievances', 'Ms T Nagini (PGT) · Mr N V S V N Murthy (TGT) · Ms K V R S Madhuri (TGT)'),
        ('Redressal of Parents’ Grievances', 'Ms A Sreedevi (TGT) · Ms P Sarada (PRT) · Ms N D Sasiprabha (PRT)'),
        ('Redressal of Students’ Grievances', 'Ms Kavita Pandey (PGT) · Mr P Naagendra (PRT) · Ms Sridevi Vasantha Rao (PRT)'),
        ('Internal Complaints Committee', 'Ms G S Rajyalakshmi (TGT) · Ms J X Juliana Nirmala (TGT) · Ms V Sreedevi (PRT)'),
        ('Sexual Harassment Committee', 'Ms C B Jeevakala (TGT) · Ms Sibani Patnaik (TGT) · Mr N V S V N Murthy (TGT) · Ms Sushree Samantaray (PRT) · Mr Navin Kumar Karan (PRT)'),
        ('Protection of Children from Sexual Offence', 'Ms Vijayalaxmi Naidu (TGT) · Ms L Maruti Devi (PRT) · Ms K V Ranganayaki (PRT) · Mr U Rama Krishna (PRT)')]


def school_info():
    kv = [('Name & address', 'DELHI PUBLIC SCHOOL Visakhapatnam Steel Plant, Sector-VIII, Ukkunagaram, Visakhapatnam Steel Plant, Visakhapatnam, Andhra Pradesh – 530032'),
          ('E-mail', EMAIL), ('Phone / Fax', '0891 2510686, 0891 2886880 · Fax 0891-2510686'), ('Year of establishment', '1991'),
          ('NOC from State / UT', 'Secretary to Govt A.P · Ltr. No. 1836/EE2/92-Edn · dated 21-09-1992'), ('Recognition', 'Recognised by the Central Board of Secondary Education'),
          ('Affiliation', 'Provisional · Affiliation No. 130110 · with the Board since 1992 · extension of affiliation up to 31.03.2023'),
          ('Trust / Society', 'DPS Society, registered under the Societies Registration Act 1860. Registration is on a permanent basis.'),
          ('Manager / Principal', 'Shri Samir Kumar Pandey, Principal · dpsvisakhapatnam@gmail.com · +91 94931 93753'),
          ('Grievance / Redressal Officer', 'Smt. Kavita Pandey, Delhi Public School, Visakhapatnam Steel Plant · +91 94251 80099 · kavitapandeydps@gmail.com')]
    t1 = ''.join(f'<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td></tr>' for a, b in kv)
    t2 = ''.join(f'<tr><td>{i}</td><td>{esc(n)}</td><td>{esc(r)}</td><td>{esc(a)}</td><td>{esc(t)}</td></tr>' for i, (n, r, a, t) in enumerate(SMC, 1))
    t3 = ''.join(f'<tr><td>{i}</td><td>{esc(n)}</td><td>{esc(m)}</td></tr>' for i, (n, m) in enumerate(COMM, 1))
    t4 = ''.join(f'<tr><td>{esc(c)}</td><td>{esc(n)}</td></tr>' for c, n in PTA)
    W = lambda h: f'<div class="tbl-wrap">{h}</div>'
    return (f'<h3>School information</h3>' + W(f'<table class="t"><tbody>{t1}</tbody></table>') +
            '<h3>Members of the School Managing Committee</h3>' + W(f'<table class="t"><thead><tr><th>Sl.</th><th>Name</th><th>Post held</th><th>Address</th><th>Tenure</th></tr></thead><tbody>{t2}</tbody></table>') +
            '<h3>Committees</h3><p>In accordance with CBSE Circular No. 19/2017 dated 12th September 2017, the following committees have been constituted:</p>' + W(f'<table class="t"><thead><tr><th>Sl.</th><th>Committee</th><th>Members</th></tr></thead><tbody>{t3}</tbody></table>') +
            '<h3>Members of PTA</h3>' + W(f'<table class="t"><thead><tr><th>Class</th><th>Member</th></tr></thead><tbody>{t4}</tbody></table>') +
            f'<p class="note">Full list with contact details: <a href="{doc("docs/PTA Members 2026-27.pdf")}" target="_blank" rel="noopener">PTA Members 2026-27 (PDF)</a>. Affiliation letter: <a href="{doc("docs/aff_doc.pdf")}" target="_blank" rel="noopener">PDF</a>.</p>')


def build_disclosure():
    mpd = rewrite_links(main_of('mpd.html'))
    for key, i in [('A. General Information:', 'mpd-a'), ('B. Documents and Information:', 'mpd-b'), ('C. Result and Academics:', 'mpd-c'), ('D. Staff (Teaching):', 'mpd-d'), ('E. School Infrastructure:', 'mpd-e')]:
        mpd = mpd.replace(f'<h4>{key}</h4>', f'<h3 id="{i}">{key.rstrip(":")}</h3>')
    mpd = mpd.replace('<h4>', '<h4 style="margin-top:1.4em">')
    body = hero_page('Mandatory Public Disclosure', 'As per CBSE directive — Appendix IX. General information, documents, results, staff and infrastructure.', ['<a href="about.html">About</a>']) + subnav([
        ('mpd-a', 'General'), ('mpd-b', 'Documents'), ('mpd-c', 'Results'), ('mpd-d', 'Staff'), ('mpd-e', 'Infrastructure'), ('school-information', 'School information')]) + f'''
<section class="section" id="mpd"><div class="wrap">
  <div class="prose reveal" style="max-width:none">{mpd}</div>
</div></section>
<section class="section alt" id="school-information"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">About DPS VSP</p><h2>School information &amp; committees</h2></div>
  <div class="prose reveal" style="max-width:none">{school_info()}</div>
</div></section>'''
    return page('disclosure.html', 'Mandatory Public Disclosure', 'CBSE mandatory public disclosure for Delhi Public School Visakhapatnam Steel Plant: affiliation, certificates, results, staff and infrastructure.', 'More', body)


# ---------------------------------------------------------------- CONTACT
def build_contact():
    body = hero_page('Contact Us', 'We would love to hear from you — visit, call or write.') + f'''
<section class="section"><div class="wrap c-grid">
  <div class="reveal">
    <h2>Get in touch</h2>
    <div class="ci">
      <div><span class="ico">{ICON['pin']}</span><p><small>Address</small>Delhi Public School<br>Sector VIII, Ukkunagaram, Visakhapatnam Steel Plant<br>Visakhapatnam, Andhra Pradesh, India – 530032</p></div>
      <a href="tel:{PHONE_TEL}"><span class="ico">{ICON['phone']}</span><p><small>Phone</small>{PHONE} · 0891 2886880</p></a>
      <a href="mailto:{EMAIL}"><span class="ico">{ICON['mail']}</span><p><small>Email</small>{EMAIL}</p></a>
      <a href="https://www.facebook.com/profile.php?id=100074407933164" target="_blank" rel="noopener"><span class="ico">{ICON['globe']}</span><p><small>Facebook</small>DPS Visakhapatnam</p></a>
    </div>
    <p><a class="btn btn-green" href="https://www.google.com/maps/dir/?api=1&destination=Delhi+Public+School+Visakhapatnam+Steel+Plant" target="_blank" rel="noopener">Get directions →</a></p>
    <form class="form" data-mailto="{EMAIL}" data-subject="Message from website" style="margin-top:28px">
      <div class="row"><label>Your name<input name="Name" required autocomplete="name"></label><label>Email or phone<input name="Contact" required></label></div>
      <label>Message<textarea name="Message" rows="4" required></textarea></label>
      <button class="btn btn-green" type="submit">Send message</button><p class="note" style="margin:0">Opens your email app, addressed to the school office.</p>
    </form>
  </div>
  <div class="map reveal"><iframe title="Map to Delhi Public School Visakhapatnam" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=Delhi%20Public%20School%20Visakhapatnam%20Steel%20Plant&output=embed"></iframe></div>
</div></section>

<section class="section alt" id="visit"><div class="wrap split top">
  <div class="reveal"><p class="eyebrow dark">Campus visit</p><h2>Schedule a visit</h2><p>See the classrooms, labs, library and playground first-hand and meet the people who will teach your child. Pick a preferred date and we’ll confirm.</p></div>
  <form class="form card reveal" data-mailto="{EMAIL}" data-subject="Campus visit request">
    <div class="row"><label>Parent’s name<input name="Parent" required autocomplete="name"></label><label>Mobile<input name="Mobile" type="tel" required autocomplete="tel"></label></div>
    <div class="row"><label>Preferred date<input name="Date" type="date" required></label><label>Class of interest<input name="Class"></label></div>
    <button class="btn btn-green" type="submit">Request a visit</button><p class="note" style="margin:0">Opens your email app, addressed to the school office.</p>
  </form>
</div></section>

<section class="section" id="alumni"><div class="wrap split">
  <div class="reveal"><p class="eyebrow dark">Alumni</p><h2>Once a DPSian, always a DPSian</h2><p>Our alumni carry the spirit of “Service before Self” into every field. Graduates are welcome to reconnect with the school, mentor current students and visit campus.</p>
    <p><a class="btn btn-green" href="mailto:{EMAIL}?subject=Alumni%20connect">Write to the alumni desk</a></p></div>
  <div class="photo reveal" style="aspect-ratio:4/3"><img src="assets/gallery/g15.jpg" alt="Students on the school field" loading="lazy"></div>
</div></section>'''
    return page('contact.html', 'Contact Us', 'Contact Delhi Public School Visakhapatnam Steel Plant: address, phone, email, map and campus visit request.', 'More', body)


def build_404():
    body = f'''<section class="section"><div class="wrap" style="text-align:center;padding:60px 0"><p class="eyebrow dark">Error 404</p><h1 style="font-size:clamp(2.4rem,6vw,4rem);color:var(--green)">This page has taken a study break.</h1><p>The page you’re looking for isn’t here — but everything else at DPS is.</p><p><a class="btn btn-green" href="index.html">Back to home</a> <a class="btn btn-line" href="contact.html">Contact the school</a></p></div></section>'''
    return page('404.html', 'Page not found', 'Page not found', None, body)
