"""Create content/*.json from the original site content — ONLY if a file does not exist yet.
After launch the school edits these files through /admin, so a rebuild must never overwrite them."""
import os, json
from core import ROOT, img, thumb, doc, size_of

CONTENT = os.path.join(ROOT, 'content')
os.makedirs(CONTENT, exist_ok=True)


def write(name, data):
    p = os.path.join(CONTENT, name + '.json')
    if os.path.exists(p):
        return
    json.dump(data, open(p, 'w', encoding='utf8'), indent=2, ensure_ascii=False)
    print('  seeded content/' + name + '.json')


def run():
    from pages_home import GAL
    from pages_b import ALBUMS, EXTRA_GAL, ASSIGN, SYL
    from layout import TICKER

    write('notices', {'items': [{'text': t, 'link': u} for t, u in TICKER]})

    write('circulars', {'items': [
        {'title': t, 'file': doc(r)} for t, r in [
            ('Circulars for Parents', 'docs/Circulars_for_Parents.pdf'), ('Circulars for Parents — Class VIII', 'docs/Circulars_for_Parents_VIII.pdf'),
            ('Circulars for Parents of Classes VI & VII', 'docs/Circulars_for_Parents_of_VI_and_VII.pdf'), ('Circular for Classes Nursery to II', 'docs/CIRCULAR_FOR_CLASSES_NUR_to_II.pdf'),
            ('Consent Form 2021-22', 'docs/Consent Form 2021-22.pdf'), ('CBSE notification regarding Class X & XII board exams', 'docs/CBSE CE Notification.pdf'), ('Notification', 'docs/Notification.pdf')]]})

    write('assignments', {'heading': 'Assignments for all classes', 'note': 'Aug – Sep Assignments 2026-27 · Please click on the class to download the assignment.',
                          'items': [{'label': l, 'file': doc('docs/assignments/' + f)} for l, f in ASSIGN]})
    write('syllabus', {'heading': 'Syllabus for all classes', 'note': 'Syllabus break-up for academic year 2023-24 · Please click on the class to download.',
                       'items': [{'label': l, 'file': doc('docs/syllabus/' + f)} for l, f in SYL]})
    write('booklist', {'title': 'Book list — academic year 2026-27', 'file': doc('docs/Book List 2026-27.pdf')})
    write('magazine', {'title': 'Aurora Australis — The Southern Lights', 'subtitle': 'Annual magazine for academic year 2024-25', 'file': doc('docs/MAGAZINE 2025.pdf')})

    news = [
        ('Class X board results 2025-26: 100% pass, school topper 98.8%', 'Achievement', 'Cheruku Anvith Raj topped the school with 98.8%. Class average 86.2; all 158 students appeared and passed.', 'img/1.jpeg', 'result-class-x-2025-26'),
        ('Class XII board results 2025-26: 100% pass, school topper 96.8%', 'Achievement', 'Bikash Kumar Barik topped the school with 96.8%. Class average 80.5; all 17 students appeared and passed.', 'img/3.jpeg', 'result-class-xii-2025-26'),
        ('Careers360: India’s Best Schools 2026 — AAA+', 'Achievement', 'DPS Visakhapatnam was rated AAA+ in the Day School category for the academic year 2025-26.', 'img/career 2026.jpeg', 'award-careers360'),
        ('RIDS recognition 2026–2029 from the British Council', 'Achievement', 'Recognition of an International Dimension in Schools, awarded for 2026–2029.', 'img/RIDS.jpeg', 'rids-2026-2029'),
        ('Education Today: India’s Top 20 CBSE Schools', 'Achievement', 'Ranked No. 1 in Visakhapatnam, No. 1 in Andhra Pradesh and No. 19 in India.', 'img/ED 1.jpeg', 'award-education-today-full'),
    ]
    write('news', {'items': [{'title': t, 'category': c, 'summary': s, 'image': img(r, 1200, name=n)} for t, c, s, r, n in news]})

    write('results', {
        'session': '2025–26', 'tagline': 'Consistently setting benchmarks in academic excellence.',
        'classX': {'percent': '98.8', 'name': 'Cheruku Anvith Raj', 'average': '86.2', 'appeared': '158', 'passed': '158', 'poster': img('img/1.jpeg', 1200, name='result-class-x-2025-26')},
        'classXII': {'percent': '96.8', 'name': 'Bikash Kumar Barik', 'average': '80.5', 'appeared': '17', 'passed': '17', 'poster': img('img/3.jpeg', 1200, name='result-class-xii-2025-26')},
        'chart_title': 'Class X average, last six years',
        'chart': [{'year': '2020-21', 'average': '83.0'}, {'year': '2021-22', 'average': '85.1'}, {'year': '2022-23', 'average': '78.3'},
                  {'year': '2023-24', 'average': '83.7'}, {'year': '2024-25', 'average': '85.2'}, {'year': '2025-26', 'average': '86.2'}]})

    from data import parse_staff, staff_photo
    from pages_a import FEE_ROWS
    st = parse_staff()
    def person(x):
        d = {'name': x['name'], 'role': x['role'], 'qualification': x['qual'] if x['qual'] != '-' else ''}
        ph = staff_photo(x)
        if ph:
            d['photo'] = ph
        return d
    lead = [x for x in st['teachers'] if x['role'].lower().startswith('co-ordinator')]
    write('staff', {'leadership': [person(x) for x in st['admin'] + lead], 'teachers': [person(x) for x in st['teachers'] if x not in lead],
                    'office': [person(x) for x in st['office']], 'support': [person(x) for x in st['support']]})
    groups = []
    for r in FEE_ROWS:
        if r[0] == 'h':
            groups.append({'heading': r[1], 'rows': []})
        else:
            groups[-1]['rows'].append({'item': r[1], 'vsp': f'{r[2]:,}', 'nvsp': f'{r[3]:,}'})
    write('fees', {'session': 'Session 2026-27', 'col1': 'VSP (₹)', 'col2': 'NVSP (₹)', 'groups': groups,
                   'note': 'Transcribed from the official fee structure dated 16-02-2026 (VSP / NVSP columns as published by the school). The signed document is the authority — see the scan alongside. Items marked “at admission” are payable once; annual fees every year at the start of the session; monthly heads are payable quarterly.',
                   'scan': doc('docs/Fee Structure 2026-27.jpeg')})


    # ---------- mandatory public disclosure ----------
    from pages_b import INFO_KV, SMC, COMM, PTA
    kv = lambda rows: [{'item': a, 'detail': b} for a, b in rows]
    D = lambda f: doc('docs/' + f)
    write('disclosure', {
        'title': 'Appendix-IX', 'subtitle': 'Mandatory Public Disclosure as per CBSE directive',
        'general': kv([('Name of the School', 'Delhi Public School Visakhapatnam Steel Plant'), ('Affiliation No. (if applicable)', '130110'), ('School Code (if applicable)', '57034'),
                       ('Complete address with pin code', 'Sector-VIII, Ukkunagaram, Visakhapatnam Steel Plant, Visakhapatnam, Andhra Pradesh - 530032'),
                       ('Principal Name & Qualification', 'Shri Samir Kumar Pandey, M.Phil, B.Ed'), ('School Email ID', 'dpsvisakhapatnam@gmail.com'), ('Contact Details (Landline / Mobile)', '0891 2510686, 0891 2886880')]),
        'documents': [
            {'item': 'Copies of affiliation / upgradation letter and recent extension of affiliation, if any', 'file': D('Affiliation Certificate.pdf')},
            {'item': 'Copies of societies / trust / company registration / renewal certificate, as applicable', 'file': D('SESU RC.pdf')},
            {'item': 'Copy of No Objection Certificate (NOC) issued, if applicable, by the State Govt. / UT', 'file': D('NOC SCANED COPY.pdf')},
            {'item': 'Copies of Recognition Certificate under RTE Act, 2009, and its renewal if applicable', 'note': 'N.A.'},
            {'item': 'Copy of Valid Building Safety Certificate as per the National Building Code', 'file': D('Building Safety.pdf')},
            {'item': 'Copy of Valid Fire Safety Certificate issued by the Competent Authority', 'file': D('Fire Safety1.PDF')},
            {'item': 'Copy of the DEO Certificate Submitted by the School for Affiliation / Upgradation / Extension of Affiliation or Self Certification by School', 'file': D('school affidivit.pdf')},
            {'item': 'Copies of valid Water, Health and Sanitation Certificates', 'file': D('Water, Health and Sanitation Cert.pdf')}],
        'academics_docs': [
            {'item': 'Fee Structure of the School', 'file': D('Fee Structure 2026-27.jpeg')}, {'item': 'Annual School Calendar', 'file': D('SC 2025-26.jpg')},
            {'item': 'List of the School Board of Management', 'file': D('LMC 2025-26.pdf')}, {'item': 'List of Parents Teachers Association (PTA) Members', 'file': D('PTA Members 2026-27.pdf')},
            {'item': 'Last three-year result of the board examination as per applicability', 'note': 'Listed below'}],
        'results_x': [dict(year=y, registered=r, passed=p, percent='100%', average=a, distinctions=d, ratio=ra, remarks='--') for y, r, p, a, d, ra in [
            ('2020-21', '169', '169', '83.0%', '651', '3.9'), ('2021-22', '151', '151', '85.1%', '626', '4.1'), ('2022-23', '144', '144', '78.3%', '470', '3.3'),
            ('2023-24', '148', '148', '83.7%', '534', '3.6'), ('2024-25', '167', '167', '85.2%', '626', '3.7')]],
        'results_xii': [dict(year=y, registered=r, passed=r, percent='100%', remarks='----') for y, r in [('2020-21', '13'), ('2021-22', '18'), ('2022-23', '20'), ('2023-24', '19'), ('2024-25', '20')]],
        'staff': kv([('Principal', 'Shri Samir Kumar Pandey'), ('Total No. of Teachers', '59'), ('   * PGT', '1'), ('   * TGT', '7'), ('   * PRT', '30'), ('Teachers Section Ratio', '1.4'),
                     ('Details of Special Educator', 'Smt P Nirmala'), ('Details of Counsellor and Wellness Teacher', 'Smt K V Ranganayaki')]),
        'infrastructure': kv([('Total Campus Area of the School (in square mtrs)', '52609 Sq.Mtrs'), ('No. and size of the Class Rooms (in square mtrs)', 'No.-63, Area-107.02 Sq.Mtrs'),
                              ('No. and size of the Laboratories including the Computer Labs (in square mtrs)', 'No.-5, Area-98.11 Sq.Mtrs'), ('Internet Facility (Yes / No)', 'Yes'),
                              ('No. of Girls Toilets', '5'), ('No. of Boys Toilets', '7'), ('Link of YouTube video of the inspection of school covering the infrastructure of the school', 'N.A.')]),
        'school_info': kv(INFO_KV),
        'smc': [{'name': n, 'post': r, 'address': a, 'tenure': t} for n, r, a, t in SMC],
        'committees_note': 'In accordance with CBSE Circular No. 19/2017 dated 12th September 2017, the following committees have been constituted:',
        'committees': [{'committee': c, 'members': m} for c, m in COMM],
        'pta': [{'class': c, 'name': n} for c, n in PTA],
        'pta_file': D('PTA Members 2026-27.pdf'), 'affiliation_file': D('aff_doc.pdf')})

    # ---------- uniform ----------
    G = lambda title, *items: {'title': title, 'items': list(items)}
    bal, c3 = 'Balvatika - II to Class II', 'Class III to XII'
    write('uniform', {
        'intro': 'All students from class I upwards must wear the following school uniform at school, during examinations and on organized tours and even on days when an extra class or any activity is conducted by the school.',
        'sets': [
            {'heading': 'Boys · Summer', 'groups': [
                G(bal, 'Pink half sleeve shirt with pointed small collars and school emblem.', 'Blue half pant of denim cloth and bottle green school belt.', 'Pink socks with two green stripes on the top, 3" below the knees.', 'Black all-purpose school shoes with medium toes and Velcro.'),
                G('Class III to VII', 'Half sleeve white shirt with pointed small collars and school emblem.', 'White shorts not more than 2½” above the knees.', 'White socks with two green stripes on the top 3" below the knees.', 'Black all-purpose school shoes with medium toes and laces.', 'Bottle green school tie and belt.', 'House T-Shirts and black track lower with white piping and school emblem on Thursdays.'),
                G('Class VIII to XII', 'White trousers with minimum 18” flares.', 'Rest same as class III to VII.')]},
            {'heading': 'Boys · Winter', 'groups': [
                G(bal, '“V” necked pink pullover and pink cap.', 'Rest same as summer uniform.'),
                G(c3, 'Full sleeve white shirt with pointed small collars and school emblem.', '“V” necked pullover of bottle green colour (sleeves optional) / Single breasted bottle green colour blazer with school emblem affixed on the chest pocket.', 'Rest same as summer uniform.')]},
            {'heading': 'Girls · Summer', 'groups': [
                G(bal, 'Pink half sleeve shirt with pointed small collars and school emblem.', 'Blue tunic of denim cloth and bottle green school belt.', 'Pink nylon socks with two green stripes on the top, 3" below the knees.', 'Black all-purpose school shoes with medium toes and Velcro.', 'Pink ribbon, hairband and clips.'),
                G(c3, 'White half sleeve blouse with pointed small collars and school emblem.', 'White box pleated skirt not more than 1” above the knees and 1” below the knees. From class V onwards divided skirts to be worn.', 'White nylon socks with two green stripes on the top 3" below the knees.', 'Black all-purpose school shoes with medium toes and laces.', 'Bottle green school tie and belt.', 'Bottle green ribbon, hairband and clips.', 'House T-Shirts and black track lower with white piping and school emblem on Thursdays.')]},
            {'heading': 'Girls · Winter', 'groups': [
                G(bal, '“V” necked pink pullover and pink cap / scarf.', 'Rest same as summer uniform.'),
                G(c3, 'Full sleeve white blouse / shirt with pointed small collars and school emblem.', '“V” necked pullover of bottle green colour (sleeves optional) / Single breasted bottle green colour blazer with school emblem affixed on the chest pocket.', 'Rest same as summer uniform.')]}],
        'notes': ['Wearing tie is compulsory for all students from Class III onwards.', 'Fancy sport shoes, fancy hair clips or jewellery is not allowed.',
                  'Turbans or Daster if worn should be of pink (up to class II) or bottle green colour (for other classes) for Sikh students.', 'Students from Balvatika to class II can wear full pants of the blue denim colour in winters.']})

    gal = []
    for c, cap, g, alt, wide in GAL + EXTRA_GAL:
        gal.append({'image': f'assets/gallery/{g}.jpg', 'caption': cap, 'category': c, 'wide': wide, 'alt': alt})
    write('gallery', {'items': gal})

    albums = []
    for d, name in ALBUMS:
        folder = os.path.join(ROOT, 'site-src', 'orig', 'pages', 'photogallery', d, 'images')
        files = sorted([f for f in os.listdir(folder) if f.endswith('.jpg')], key=lambda x: int(x.split('.')[0])) if os.path.isdir(folder) else []
        if not files:
            continue
        albums.append({'title': name, 'year': '2018-19', 'photos': ['assets/img/' + f'album-{d.lower()}-{f.split(".")[0]}.jpg' for f in files]})
    write('albums', {'items': albums})
