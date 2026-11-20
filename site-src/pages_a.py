import re
from core import img, thumb, doc, esc, main_of, rewrite_links, text_of, size_of, ORIG
from layout import ICON, page, hero_page, subnav, ERP, FEES, PHONE, PHONE_TEL, EMAIL
from data import parse_staff, staff_photo, initials
from pages_home import days_html


def prose(html_):
    return f'<div class="prose">{html_}</div>'


def docimg(rel, cap, alt=None, w=1600):
    url = doc(rel)
    prev = img(rel, w=w, name='view-' + url.split('/')[-1].rsplit('.', 1)[0])
    return f'<button class="docimg" data-zoom="{url}" data-cap="{esc(cap)}"><img src="{prev}" alt="{esc(alt or cap)}" loading="lazy"></button>'


def person_card(p, lead=False):
    ph = staff_photo(p)
    media = f'<img src="{ph}" alt="{esc(p["name"])}" loading="lazy">' if ph else f'<div class="ph">{initials(p["name"])}</div>'
    qual = f'<span>{esc(p["qual"])}</span>' if p['qual'] and p['qual'] != '-' else ''
    return (f'<article class="person" data-name="{esc((p["name"] + " " + p["role"] + " " + p["qual"]).lower())}" data-role="{esc(p["role"].upper())}">'
            f'{media}<div><b>{esc(p["name"])}</b><span class="role">{esc(p["role"])}</span>{qual}</div></article>')


# ---------------------------------------------------------------- ABOUT
GOV = [('Shri V K Shunglu', 'Chairman, DPS Society', 'img/vkshunglu.jpg'), ('Shri B K Chaturvedi', 'Vice Chairman, DPS Society', 'img/Shri B K Chaturvedi.jpg'),
       ('Ms Namita Pradhan', 'Hony. Treasurer, DPS Society', 'img/Ms Namita Pradhan.jpg'), ('Dr Usha K Luthra', 'Member, DPS Society', 'img/Dr Usha K Luthra.jpg'),
       ('Shri Ravi Vira Gupta', 'Member, DPS Society', 'img/Shri Ravi Vira Gupta.jpg'), ('Shri Rahul Singh', 'Member, DPS Society', 'img/Shri Rahul Singh.jpg'),
       ('Dr Kiran Datar', 'Member, DPS Society', 'img/Dr Kiran Datar.jpg'), ('Ms Vrinda Sarup', 'Member, DPS Society', 'img/Ms Vrinda Sarup.jpg')]
MC = [('Shri B K Chaturvedi', 'Chairman – Managing Committee', 'img/Shri B K Chaturvedi.jpg'), ('Dr (Mrs) Malini Vijay Shankar', 'Vice Chairperson – MC', 'img/Dr (Mrs) Malini Vijay Shankar.jpg'),
      ('Shri Shantanu Consul', 'Member – MC', 'img/shantanu.png'), ('Shri Rakesh Kacker', 'Member – MC', 'img/rakesh.png'), ('Shri Pravin Srivastava', 'Member – MC', 'img/Shri Pravin Srivastava.jpg'),
      ('Shri N V S Raju', 'GM (HR) RINL VSP · Pro-Vice Chairman', 'img/Raju.jpeg'), ('Dr S B V S P Sastry', 'DGM (Training) RINL VSP · Member', 'img/sastry.jpeg'),
      ('Shri Ch Leela Srinivas', 'DGM (F&A) RINL VSP · Member', 'img/Shri Ch Leela Srinivas.jpg'), ('Shri Padma Ranjan Roy', 'Sr Manager (TA) RINL VSP · Member', 'img/Roy.jpeg')]


def mentor_cards(lst):
    out = []
    for n, r, p in lst:
        ph = thumb(p, 360) if p and __import__('os').path.isfile(__import__('os').path.join(ORIG, p)) else None
        media = f'<img src="{ph}" alt="{esc(n)}" loading="lazy">' if ph else f'<div class="ph">{initials(n)}</div>'
        out.append(f'<article class="person">{media}<div><b>{esc(n)}</b><span>{esc(r)}</span></div></article>')
    return ''.join(out)


def build_about():
    pm = img('img/principal_msg.jpg', 1400, name='principal-message')
    px = img('img/principal1.jpeg', 900, name='principal')
    body = hero_page('About DPS Visakhapatnam', 'Established in 1991 in the Steel Township, under the aegis of the Delhi Public School Society, New Delhi.') + subnav([
        ('school', 'Our School'), ('philosophy', 'Philosophy'), ('principal', "Principal's Message"), ('society', 'DPS Society'), ('management', 'Management')]) + f'''
<section class="section" id="school"><div class="wrap split top">
  <div class="reveal prose"><p class="eyebrow dark">About the school</p><h2>Brief introduction</h2>
    <div data-md="school_md"><p>Delhi Public School Visakhapatnam was established in the year 1991 and is now imparting quality education with the most modern teaching techniques available to enable its students to compete with the world. It provides a congenial atmosphere for the total development of the whole personality and its integration with the society. It is committed to academic excellence, and appreciation of the worth of the individual student and educational leadership.</p>
    <p>The school tries to inculcate in students the values of personal hygiene, neatness in uniform, cleanliness of surroundings, graceful manners, obedience and discipline. The children are provided with an environment which fosters a spirit of enquiry and keen competition. Personal attention is given to each individual child. A competent and supporting staff takes care of the special needs of the children with full commitment.</p>
    <p>Learning is a joy here and the school provides a very vibrant and inspiring atmosphere for the students to grow in a stress-free environment.</p></div></div>
  <div class="reveal"><div class="photo" style="aspect-ratio:4/3"><img src="assets/gallery/g9.jpg" alt="Prefects at the Investiture Ceremony" loading="lazy"></div>
    <div class="grid g2" style="margin-top:20px"><div class="card"><b style="font:600 2rem var(--serif);color:var(--gold)">1991</b><p class="note" style="margin:0">Year of establishment</p></div><div class="card"><b style="font:600 2rem var(--serif);color:var(--gold)">CBSE</b><p class="note" style="margin:0">Affiliation No. 130110 (since 1992)</p></div></div></div>
</div></section>

<section class="section alt" id="philosophy"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">What we believe</p><h2>Motto, philosophy &amp; aim</h2></div>
  <div class="grid g3" data-list="pcards" data-tpl="pcard">
    <article class="card reveal"><div class="ico">{ICON['heart']}</div><h3>Philosophy</h3><p><strong>Motto: Service before Self.</strong></p><p>To develop all four human dimensions — Body, Mind, Heart and Soul. To teach to learn for: the Body to live, Mind to learn, Heart to love, Soul to leave a legacy.</p><p>To enable students to excel in academics and recognise their full potential and develop good habits so that they can contribute towards the progress of the world — utilising the three great gifts given by God to all human beings: Power of Choice, Power of Intelligence, Power of Conscience.</p></article>
    <article class="card reveal"><div class="ico">{ICON['cap']}</div><h3>Aim</h3><p>Our aim is to impart sound and liberal education to boys and girls during their impressionable years — education that would lay stress on character building, team work, esprit-de-corps, physical development and infuse in them a spirit of adventure, fair play and justice.</p><p>We aim to develop among our students a feeling of pride in Indian culture and produce citizens who will be truly Indian and above social, communal, religious or provincial prejudices.</p></article>
    <article class="card reveal"><div class="ico">{ICON['globe']}</div><h3>International Policy</h3><p>To encourage young minds to develop understanding, tolerance and appreciation of diverse cultures of the world.</p><p>To nurture global citizens who play a responsible role for sustainable development in a changing world.</p></article>
  </div>
  <div class="four reveal" style="margin-top:36px"><article><span class="ico">◆</span><h3>Body</h3><p>to live</p></article><article><span class="ico">◆</span><h3>Mind</h3><p>to learn</p></article><article><span class="ico">◆</span><h3>Heart</h3><p>to love</p></article><article><span class="ico">◆</span><h3>Soul</h3><p>to leave a legacy</p></article></div>
</div></section>

<section class="section" id="principal"><div class="wrap">
  <div class="p-grid" style="align-items:start">
    <figure class="reveal"><img src="{px}" alt="Mr. Samir Kumar Pandey, Principal" width="852" height="965" loading="lazy"></figure>
    <div class="reveal prose"><p class="eyebrow dark">Principal’s message</p><h2>Principal speaks</h2>
      <blockquote><p data-text="principal_quote">“The will to win, the desire to succeed, the urge to reach your full potential… these are the keys that will unlock the door to personal excellence.”</p></blockquote>
      <div data-md="principal_md"><p>Confucius couldn’t have summed up better what we at DPS wish for every student that steps into our portals. DPS Visakhapatnam dates back to 1991 when the school was set up in the Steel Township under the aegis of the Delhi Public School Society, New Delhi. From then onwards, the school has grown in strength with the continuous support of Visakhapatnam Steel Plant Management, who readily lend a helping hand for our upkeep and smooth functioning. The DPS Society too has rendered invaluable support with its guidance, teacher training programmes, Inter DPS Competitions etc.</p>
      <p>The school curriculum provides ample opportunities to go beyond tests and textbooks. Students can foray into numerous activities — be it learning a new language, a new dance form, a new prayer song, a new technique of painting or it could be just witnessing a well orchestrated Morning Assembly — each a new experience, a new joy, all helping to nurture and hone new skills. At DPS, we are ever committed to enable every child to grow to his fullest, which undoubtedly leads to an exhilarating sense of achievement. Added to this, is the spirit of camaraderie and bonhomie fostered through Inter-House competitions and sports activities.</p>
      <p>A well stocked library that is replenished periodically is the DPS way of motivating children to rediscover the pleasure of reading. Books are indeed a “unique portable magic” that transport you from one world to another and thereby open a whole new realm of “Light and Wisdom”.</p>
      <p>“Children are our priority, change is the reality, collaboration is our strategy.” Technology and automation have been incorporated in the school system, ensuring faster and more convenient way of interaction with our stakeholders. Digital classrooms have been introduced to equip teachers and students with 21st century skills, necessary for all to be lifelong learners. Thus, DPS re-affirms that we need to be adaptive and accommodating in this changing world. It is only a collaborative effort of teachers and parents that can lay out the right path, where students are prepared to face all challenges of the world.</p>
      <p class="sig"><strong>S K Pandey</strong><br>Principal, DPS Visakhapatnam</p></div></div>
  </div>
  <div class="photo reveal" style="margin-top:44px;aspect-ratio:21/9"><img src="{pm}" alt="The Principal at his desk" loading="lazy" style="object-position:center 30%"></div>
</div></section>

<section class="section alt" id="society"><div class="wrap split top">
  <div class="reveal"><p class="eyebrow dark">DPS Society</p><h2>A legend in the field of education</h2>
    <div class="grid g2" style="margin-top:24px"><div class="card"><b style="font:600 2.4rem var(--serif);color:var(--gold)">200+</b><p class="note" style="margin:0">Schools under the Society, in India and abroad</p></div><div class="card"><b style="font:600 2.4rem var(--serif);color:var(--gold)">68 yrs</b><p class="note" style="margin:0">Serving the field of education</p></div></div></div>
  <div class="reveal prose">
    <div data-md="society_md"><p>Delhi Public School has been serving the Society in the field of education for the last 68 years. There are presently over 200 Schools under its aegis both in and outside India. The growing number of schools under this society signifies how the need to provide meaningful education to a large number of children desirous of growing into educated and liberated human beings has been fulfilled. Founded and managed by distinguished members and luminaries of society culled from various walks of life, the organisation has always guided its member schools on the path of progress with their visionary approach and lofty ideals. Consequently, Delhi Public Schools have become significant portals of learning and growth of young minds.</p>
    <p>The main aim of this society is to provide an all-round development and sound moral base. Fostering character building and nurturing the inquisitive spirit of children, encouraging scientific temperament and strengthening social bonds, are constant deeds here. Mr. V. K. Shunglu, Chairman, DPS Society is the constant beacon and source of strength.</p>
    <p>From a small beginning in the President’s Estate in 1941 as Church High School to Naveen Bharat School in 1947 and finally in 1949 at its present location of Mathura Road, DPS has traversed a long journey. The birth of a new nation in 1947 was in a way the beginning of DPS (called Naveen Bharat then). A vital time in the history of our nation, when a beginning was made to fulfil a social, national need. DPS was not a silent witness to the trials and tribulations of the growing metropolis but contributed richly to the growth of the capital especially academics. DPS Mathura Road was the only DPS till 1972. But the parent DPS was ready to spread its wings. The many offsprings, 95 schools as on 1st September 2002 that followed from R. K. Puram in 1972 are simple assertions of the strength that is DPS. Yet what has remained unchanged is the zest and spirit to achieve and excel. The society is managing and maintaining a uniform level of excellence, hallmark of a Delhi Public School, with schools set up over vast regions with diverse cultural backgrounds, socio-economic conditions and educational contrasts. This diversity is respected while ensuring that all the schools under the aegis of the society follow a uniform educational practice.</p>
    <p>World famous DPS teachers’ work ethic and dynamism is the bedrock on which rests the DPS edifice. Highly qualified, talented faculty with right skills and positive attitude goes beyond the call of duty to provide appropriately contextual learning experiences to young minds. The DPS faculty boasts of University top rankers and winners of national and international awards. These teachers have committed their working lives to an endeavour centred on building new generations. In-service teacher education programmes, national and international assignments and exposure visits ensure professional and personal growth of these lifelong learners.</p></div>
    <p><a class="btn btn-line" href="http://www.dpsfamily.org/" target="_blank" rel="noopener">Visit the DPS Society →</a></p></div>
</div></section>

<section class="section" id="management"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Organisational structure</p><h2>Meet our mentors</h2></div>
  <h3 class="reveal">Governing Body, DPS Society, New Delhi</h3>
  <div class="mentors" data-list="gov" data-tpl="mentor">{mentor_cards(GOV)}</div>
  <h3 class="reveal" style="margin-top:40px">School Managing Committee, DPS Visakhapatnam Steel Plant</h3>
  <div class="mentors" data-list="mc" data-tpl="mentor">{mentor_cards(MC)}</div>
  <p style="margin-top:26px"><a class="btn btn-line" href="disclosure.html#school-information">Committees &amp; school information →</a></p>
</div></section>'''
    return page('about.html', 'About Us', 'About Delhi Public School Visakhapatnam: philosophy, aim, principal’s message, the DPS Society and our managing committee.', 'About', body)


# ---------------------------------------------------------------- STAFF
def build_staff():
    st = parse_staff()
    lead = [p for p in st['teachers'] if p['role'].lower().startswith('co-ordinator')]
    teachers = [p for p in st['teachers'] if p not in lead]
    roles = sorted({p['role'].upper() for p in teachers})
    chips = '<button class="chip on" data-role="">All</button>' + ''.join(f'<button class="chip" data-role="{esc(r)}">{esc(r)}</button>' for r in roles)
    total = len(st['admin']) + len(st['teachers'])
    body = hero_page('Faculty & Staff', 'The people who make DPS Visakhapatnam what it is — dedicated, qualified and caring.', ['<a href="about.html">About</a>']) + subnav([
        ('leadership', 'Leadership'), ('teachers', 'Teachers'), ('office', 'Office staff'), ('support', 'Support staff')]) + f'''
<section class="section" id="leadership"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Administration</p><h2>School leadership</h2></div>
  <div class="staff-grid" id="staffLead">{''.join(person_card(p) for p in st['admin'] + lead)}</div>
</div></section>
<section class="section alt" id="teachers"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark" id="teacherCount">{len(teachers)} teachers</p><h2>Our teachers</h2><p>PGT: Post Graduate Teacher · TGT: Trained Graduate Teacher · PRT (Pr T): Primary Teacher. All listed teachers are trained.</p></div>
  <div class="table-tools reveal"><input type="search" id="staffQ" placeholder="Search by name, subject or qualification…" aria-label="Search teachers"></div>
  <div class="filters reveal" id="roleF">{chips}</div>
  <div class="staff-grid" id="staffGrid">{''.join(person_card(p) for p in teachers)}</div>
  <p class="note" id="staffEmpty" hidden style="margin-top:20px">No staff match your search.</p>
</div></section>
<section class="section" id="office"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Administration support</p><h2>Office staff</h2></div>
  <div class="staff-grid" id="staffOffice">{''.join(person_card(p) for p in st['office'])}</div>
</div></section>
<section class="section alt" id="support"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Keeping the campus running</p><h2>Support staff</h2></div>
  <div class="staff-grid" id="staffSupport">{''.join(person_card(p) for p in st['support'])}</div>
</div></section>'''
    return page('staff.html', 'Faculty & Staff', 'Meet the principal, coordinators, teachers and staff of Delhi Public School Visakhapatnam.', 'About', body)


# ---------------------------------------------------------------- ACADEMICS
def build_academics():
    promo = rewrite_links(main_of('promotion.html'))
    awards = rewrite_links(main_of('awards.html'))
    train = ''.join(f'<li><a href="{doc(f"docs/Workshop Details {y}.pdf")}" target="_blank" rel="noopener"><span class="ft">PDF</span><span><b>Workshop details {y}</b><small>Staff training · PDF · {size_of(doc(f"docs/Workshop Details {y}.pdf"))}</small></span></a></li>' for y in ['2022', '2020-21', '2019-20', '2018-19', '2017-18'])
    cal = [('c1', 'School Calendar 2026-27', 'docs/School Calendar 2026-27.jpg'), ('c2', 'School Calendar 2025-26', 'docs/SC 2025-26.jpg'),
           ('c3', 'Formative Assessment 2025-26', 'docs/FA 2025-26.jpg'), ('c4', 'Inter House Competitions 2025-26', 'docs/IHC 2025-26.jpg'), ('c5', 'Intra Class Competitions 2025-26', 'docs/ICC 2025-26.jpg')]
    tabs = ''.join(f'<button role="tab" aria-selected="{"true" if i == 0 else "false"}" aria-controls="{k}" id="b{k}"{"" if i == 0 else " tabindex=-1"}>{t}</button>' for i, (k, t, _) in enumerate(cal))
    panels = ''.join(f'<div class="panel" role="tabpanel" id="{k}" aria-labelledby="b{k}"{"" if i == 0 else " hidden"}>{docimg(r, t)}<p style="margin:14px 0 0"><a class="btn btn-line btn-sm" href="{doc(r)}" download>Download image</a></p></div>' for i, (k, t, r) in enumerate(cal))
    body = hero_page('Academics', 'A curriculum that goes beyond tests and textbooks — CBSE, 10+2, taught the “Learn, Learner, Learning” way.') + subnav([
        ('methodology', 'Methodology'), ('courses', 'Courses'), ('promotion', 'Promotion'), ('awards', 'Awards & Rewards'), ('calendar', 'Calendars'), ('days', 'Important Days'), ('strength', 'Student Strength'), ('training', 'Staff Training')]) + f'''
<section class="section" id="methodology"><div class="wrap split top">
  <div class="reveal prose"><p class="eyebrow dark">Academic information</p><h2>Teaching methodology</h2>
    <div data-md="methodology_md"><p>Keeping in mind the fact that for most of the students in our scenario, English is a second language, we at Delhi Public School, Visakhapatnam Steel Plant lay emphasis on developing the oral skills of the little ones who seek admission in pre-primary classes. The best way to pick up the language is to follow the natural way, in which one learns his or her mother tongue, i.e. to develop the skills in the natural order of <strong>Listening, Speaking, Reading and Writing</strong>.</p>
    <p>In higher classes we follow the interactive method. Stress is laid more on “Learn, Learner, Learning” than on “Teach, Teacher, Teaching” for we sincerely believe that it is possible to learn without a teacher but it is not possible to learn without a learner.</p>
    <p>We also believe in giving the optimum homework, which the child should be able to do on his/her own.</p></div></div>
  <div class="grid reveal">
    <div class="card"><div class="ico">{ICON['sparkle']}</div><h3>Listen · Speak · Read · Write</h3><p>Language is built the natural way, starting with oral skills in the pre-primary years.</p></div>
    <div class="card"><div class="ico">{ICON['book']}</div><h3>Learner at the centre</h3><p>Interactive teaching in the higher classes, with optimum homework a child can do independently.</p></div>
  </div>
</div></section>

<section class="section alt" id="courses"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Curriculum</p><h2>Courses offered &amp; promotion policy</h2></div>
  <div class="prose"><div data-md="courses_md">{promo}</div></div>
</div></section>

<section class="section" id="awards"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Encouragement systems</p><h2>Awards &amp; rewards policy</h2><p>DPS Visakhapatnam believes in encouraging achievers in all fields — academics, sports and co-curricular activities.</p></div>
  <div class="prose"><div data-md="awards_md">{awards}</div></div>
</div></section>

<section class="section alt" id="calendar"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Plan your year</p><h2>Calendars</h2><p>Academic calendar, formative assessment schedule and competition schedules. Click any image to enlarge.</p></div>
  <div class="tabs" data-tabs data-list="calendars" data-tpl="calendars"><div class="tablist" role="tablist" aria-label="Calendars">{tabs}</div>{panels}</div>
</div></section>

<section class="section" id="days"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">List of important days</p><h2>Days we celebrate</h2><p>The next upcoming day is highlighted automatically.</p></div>
  <div class="days" id="daysAll" data-list="days" data-tpl="day">{days_html()}</div>
</div></section>

<section class="section alt" id="strength"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">2025-26</p><h2>Class &amp; section-wise student strength</h2></div>
  <div style="max-width:900px" data-docimg="strength_image">{docimg('docs/STUDENT STRENGTH 2025-26.jpg', 'Student strength 2025-26')}</div>
</div></section>

<section class="section" id="training"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Professional growth</p><h2>Staff training details</h2><p>DPS teachers keep learning — workshop records by year.</p></div>
  <ul class="doclist" data-list="training" data-tpl="doclink">{train}</ul>
</div></section>'''
    return page('academics.html', 'Academics', 'Teaching methodology, courses and subject combinations, promotion policy, awards, school calendars and student strength at DPS Visakhapatnam.', 'Academics', body)


# ---------------------------------------------------------------- ADMISSIONS

FEE_ROWS = [
    ('h', 'One-time fees (payable once, at admission)'), ('r', 'Admission fee', 9680, 14210), ('r', 'Development fee', 6710, 13210), ('r', 'Caution money (refundable)', 5000, 6000),
    ('h', 'Annual fee (per year, at the start of the session)'), ('r', 'Balvatika II & III', 1760, 1910), ('r', 'Class I & II', 1760, 2020), ('r', 'Class III to V', 2420, 3280), ('r', 'Class VI to VIII', 3080, 4180),
    ('r', 'Class IX & X', 3300, 4510), ('r', 'Class XI & XII', 7260, 9460), ('r', 'Almanac, magazine, ID card, group photo', 700, 755), ('r', 'Management fund (at admission, then yearly)', 1210, 1300), ('r', 'Workshop, tours, seminars', 390, 420),
    ('h', 'Tuition fee (per month)'), ('r', 'Balvatika II & III', 2035, 2835), ('r', 'Class I & II', 2620, 3720), ('r', 'Class III to V', 2970, 4070), ('r', 'Class VI to VIII', 3315, 4415), ('r', 'Class IX & X', 3500, 4600), ('r', 'Class XI & XII', 3620, 5010),
    ('h', 'Other monthly fees (payable quarterly)'), ('r', 'Activity & assignment fee (per month)', 320, 345), ('r', 'Smart class fee (per month)', 180, 195), ('r', 'Computer fee (per month)', 185, 200),
    ('h', 'Bus fee (per year, optional, payable yearly)'), ('r', 'Stage 1: Old Gajuwaka, KPLM', 24750, 24750), ('r', 'Stage 2: Muralinagar, NAD, Sheela Nagar, BHPV, Auto Nagar, New Gajuwaka', 29700, 29700),
]


def fee_table():
    rows = ''
    for r in FEE_ROWS:
        if r[0] == 'h':
            rows += f'<tr class="sub"><td colspan="3">{esc(r[1])}</td></tr>'
        else:
            rows += f'<tr><td>{esc(r[1])}</td><td class="num">{r[2]:,}</td><td class="num">{r[3]:,}</td></tr>'
    return f'<div class="tbl-wrap"><table class="t"><thead><tr><th>Fee head</th><th class="num">VSP (₹)</th><th class="num">NVSP (₹)</th></tr></thead><tbody>{rows}</tbody></table></div>'

FAQ = [
    ('When does admission begin?', 'Names of those seeking admission are registered from the second half of December each year to January of the next year. Written tests and interviews are held in February/March, and the new session starts from the first working day of April.'),
    ('Is there an entrance test?', 'A written test is conducted for English, Hindi and Mathematics. Children seeking admission to Nursery are instead called for a meeting with the concerned teachers and the Principal, along with their parents.'),
    ('How will I know if my child is selected?', 'The final list of selected candidates is displayed on the School’s Notice Board. An orientation programme is conducted for all new parents.'),
    ('Which board does the school follow?', 'The school prepares students for the All India Secondary School Examination and the All India Senior School Certificate Examination under the 10+2 scheme of the Central Board of Secondary Education (CBSE), New Delhi.'),
    ('Which subject combinations are available in Classes XI–XII?', 'Science (Biology or Maths stream with English, Physics and Chemistry) and Commerce (English, Business Studies, Accountancy, Economics), with optional Physical Education, Informatics Practices and more. See the Academics page for the full table.'),
    ('How do I withdraw my child?', 'A clear calendar month’s notice in writing, or a month’s fee in lieu of notice, is required. Those who leave in May must pay the fee for June. The Transfer Certificate is issued once all dues are settled.'),
    ('How are fees paid?', 'Fees can be paid online through SBI Collect. The fee structure for 2026-27 is available on this page.'),
    ('Is school uniform compulsory?', 'Yes. All students from Class I upwards must wear the prescribed uniform at school, during examinations and on organised tours. A tie is compulsory from Class III onwards.'),
    ('Does the school provide transport?', 'Yes — transport is available through the school’s own and outsourced buses. Health and medical check-ups are done by the Visakhapatnam Steel General Hospital (VSGH).'),
    ('How is promotion decided?', 'Promotion is based on the whole year’s performance. For Classes II–VIII the final marks take 20% of weekly tests, 30% of the half-yearly and 50% of the annual examination into account.'),
]


def build_admissions():
    uni = rewrite_links(main_of('uniform.html'))
    withdraw = main_of('adm_withdraw.html')
    faq = ''.join(f'<details><summary>{esc(q)}</summary><div class="ans"><p>{esc(a)}</p></div></details>' for q, a in FAQ)
    steps = [('Dec – Jan', 'Registration', 'Names are registered from the second half of December to January.'),
             ('Feb – Mar', 'Test & interview', 'Written test in English, Hindi and Maths. Nursery: meeting with teachers and Principal with parents.'),
             ('After tests', 'Selection list', 'The list of selected candidates goes up on the School Notice Board.'),
             ('April', 'Session begins', 'Orientation for new parents; school opens on the first working day of April.')]
    sh = ''.join(f'<div class="step reveal"><small>{a}</small><h3>{b}</h3><p>{c}</p></div>' for a, b, c in steps)
    fee_url = doc('docs/Fee Structure 2026-27.jpeg')
    tc = doc('docs/tc sample.pdf')
    body = hero_page('Admissions', 'Welcome to the DPS family. Here is everything you need to apply, in one place.') + subnav([
        ('process', 'Process'), ('fees', 'Fees 2026-27'), ('uniform', 'Uniform'), ('forms', 'Forms'), ('withdrawal', 'Withdrawal & TC'), ('faq', 'FAQs')]) + f'''
<section class="section" id="process"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Admission process</p><h2>From registration to the first day</h2></div>
  <div class="steps" data-list="steps" data-tpl="step">{sh}</div>
  <div class="callout reveal" style="margin-top:28px"><b>Written test:</b> English, Hindi and Mathematics. For Nursery, a meeting with the concerned teachers and the Principal along with parents. <button class="btn btn-gold btn-sm" data-open="enquiry" style="margin-left:10px">Send an enquiry</button></div>
</div></section>

<section class="section alt" id="fees"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark" id="feeSession">Session 2026-27</p><h2>Fee structure</h2><p>Official fee structure as issued by the school. Click to enlarge or download.</p></div>
  <div class="split top">
    <div class="reveal"><div id="feeTable">{fee_table()}</div><p class="note" id="feeNote" style="margin-top:12px">Transcribed from the official fee structure dated 16-02-2026 (VSP / NVSP columns as published by the school). The signed document is the authority — see the scan alongside. Items marked “at admission” are payable once; annual fees every year at the start of the session; monthly heads are payable quarterly.</p></div>
    <div class="reveal"><div id="feeScan">{docimg('docs/Fee Structure 2026-27.jpeg', 'Fee structure 2026-27 (official scan)')}</div>
      <div class="card" style="margin-top:16px"><div class="ico">{ICON['rupee']}</div><h3>Pay fees online</h3><p>Pay securely through SBI Collect. For clarifications call the school office on {PHONE}.</p><p style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn btn-green" href="{FEES}" target="_blank" rel="noopener">Pay school fees →</a> <a id="feeDl" class="btn btn-line btn-sm" href="{fee_url}" download>Download scan</a></p></div></div>
  </div>
</div></section>

<section class="section" id="uniform"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">What to wear</p><h2>School uniform</h2></div>
  <div class="prose" id="uniformDyn">{uni}</div>
</div></section>

<section class="section alt" id="forms"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow dark">Registration cum enrolment</p><h2>Application form</h2></div>
  <div class="grid g3 reveal">
    <a class="card hover" href="{doc('docs/Std_ApplicationForm.pdf')}" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><div class="ico">{ICON['edit']}</div><h3>Student enrolment form</h3><p>Registration cum enrolment form (PDF, {size_of(doc('docs/Std_ApplicationForm.pdf'))}). Fill, print and submit at the school office.</p></a>
    <a class="card hover" href="{doc('docs/Application Form.pdf')}" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><div class="ico">{ICON['book']}</div><h3>Application form</h3><p>General application form (PDF, {size_of(doc('docs/Application Form.pdf'))}).</p></a>
    <div class="card"><div class="ico">{ICON['pin']}</div><h3>Submit in person</h3><p>Delhi Public School, Sector VIII, Ukkunagaram, Visakhapatnam – 530032.<br>Call {PHONE}</p></div>
  </div>
</div></section>

<section class="section" id="withdrawal"><div class="wrap split top">
  <div class="reveal prose"><p class="eyebrow dark">Policy</p><h2>Withdrawal procedure</h2><div data-md="withdrawal_md">{withdraw.split('Withdrawal Procedure')[-1] if 'Withdrawal Procedure' in withdraw else withdraw}</div></div>
  <div class="reveal"><div class="card"><h3>Transfer certificate</h3><p>Transfer Certificates are issued only when all dues of the school are settled. View the sample format below.</p>
    <p><a class="btn btn-line btn-sm" href="{tc}" target="_blank" rel="noopener">Sample TC (PDF)</a></p></div>
</div>
</div></section>

<section class="section alt" id="faq"><div class="wrap split top">
  <div class="reveal"><p class="eyebrow dark">Quick answers</p><h2>Frequently asked questions</h2><p>Answers are drawn from the school’s published admission, uniform, promotion and withdrawal policies.</p>
    <p><button class="btn btn-green" data-open="enquiry">Still have a question?</button></p></div>
  <div class="acc" data-list="faq" data-tpl="faq">{faq}</div>
</div></section>'''
    return page('admissions.html', 'Admissions', 'Admission process, fee structure 2026-27, school uniform, application forms, withdrawal policy and FAQs for DPS Visakhapatnam.', 'Admissions', body)
