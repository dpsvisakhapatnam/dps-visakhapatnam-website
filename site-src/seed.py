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
        d = {'name': x['name'], 'role': x['role'], 'qualification': x['qual'] if x['qual'] != '-' else '', 'joined': x['joined']}
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
