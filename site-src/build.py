import os, re, json, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import ROOT, text_of, doc
import pages_home, pages_a, pages_b, seed
seed.run()

PAGES = {
    'index.html': pages_home.build_index,
    'about.html': pages_a.build_about,
    'staff.html': pages_a.build_staff,
    'academics.html': pages_a.build_academics,
    'admissions.html': pages_a.build_admissions,
    'campus.html': pages_b.build_campus,
    'gallery.html': pages_b.build_gallery,
    'news.html': pages_b.build_news,
    'resources.html': pages_b.build_resources,
    'disclosure.html': pages_b.build_disclosure,
    'contact.html': pages_b.build_contact,
    '404.html': pages_b.build_404,
}
index = []
seen = set()
for fn, builder in PAGES.items():
    print('building', fn)
    h = builder()
    open(os.path.join(ROOT, fn), 'w', encoding='utf8').write(h)
    if fn == '404.html':
        continue
    title = re.search(r'<title>(.*?)</title>', h).group(1).split(' · ')[0]
    desc = html.unescape(re.search(r'<meta name="description" content="(.*?)">', h).group(1))
    index.append({'t': title, 'u': fn, 'd': desc, 'k': 'Page'})
    for m in re.finditer(r'<h([23])[^>]*id="([^"]+)"[^>]*>(.*?)</h\1>', h, flags=re.S):
        t = text_of(m.group(3))
        if t and (fn, t) not in seen:
            seen.add((fn, t)); index.append({'t': t, 'u': f'{fn}#{m.group(2)}', 'd': title, 'k': 'Section'})
    h_static = re.sub(r'<ul class="doclist"[^>]*id="(?:circularList|assignList|syllabusList)">.*?</ul>', '', h, flags=re.S)
    for m in re.finditer(r'<a href="(docs/[^"]+)"[^>]*><span class="ft[^"]*">[^<]*</span><span><b>(.*?)</b><small>(.*?)</small>', h_static):
        key = (m.group(1))
        if key in seen: continue
        seen.add(key); index.append({'t': text_of(m.group(2)), 'u': m.group(1), 'd': text_of(m.group(3)), 'k': 'Download'})
import seed_pages
seed_pages.run()
from layout import ICON
json.dump(ICON, open(os.path.join(ROOT, 'assets', 'icons.json'), 'w'), separators=(',', ':'))
json.dump(index, open(os.path.join(ROOT, 'assets', 'search.json'), 'w'), separators=(',', ':'), ensure_ascii=False)
base = 'https://dpsvisakhapatnam.netlify.app/'
urls = ''.join(f'<url><loc>{base}{fn if fn != "index.html" else ""}</loc></url>' for fn in PAGES if fn != '404.html')
open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
open(os.path.join(ROOT, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nSitemap: ' + base + 'sitemap.xml\n')
import shutil
shutil.copyfile(os.path.join(ROOT, 'site-src', 'styles.css'), os.path.join(ROOT, 'styles.css'))
shutil.copyfile(os.path.join(ROOT, 'site-src', 'script.js'), os.path.join(ROOT, 'script.js'))
shutil.copyfile(os.path.join(ROOT, 'site-src', 'content.js'), os.path.join(ROOT, 'content.js'))
print('search entries', len(index))
