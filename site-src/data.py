"""Parsers that lift structured content out of the old site's pages."""
import re, html, os
from core import read_crawl, text_of, thumb, ORIG, esc


def _cells(row):
    parts = re.split(r'<td[^>]*>', row)[1:]
    return [text_of(p) for p in parts]


def _img(row):
    m = re.search(r'<img[^>]+src="([^"]+)"', row)
    return m.group(1).replace('../', '') if m else None


def parse_staff():
    """Return {section: [dict(name, role, qual, joined, photo)]} — omits DOB and employee codes."""
    s = re.sub(r'<!--.*?-->', '', read_crawl('staff.html'), flags=re.S)
    out = {}
    secs = [('Administration', 'admin'), ('Teachers', 'teachers'), ('Office Staff', 'office'), ('Sub Staff', 'support')]
    idx = [(s.find(f'>{n}</b>'), key) for n, key in secs]
    idx.append((s.find('</article>'), None))
    for (a, key), (b, _) in zip(idx, idx[1:]):
        chunk = s[a:b]
        rows = re.findall(r'<tr>(.*?)(?=<tr>|</tbody>|</table>)', chunk, flags=re.S)
        people = []
        for r in rows:
            if '<th' in r:
                continue
            c = _cells(r)
            photo = _img(r)
            c = [x for x in c]
            # first cell after img td is name (img td has empty text)
            if c and c[0] == '':
                c = c[1:]
            if not c or not c[0]:
                continue
            name, role = c[0], (c[1] if len(c) > 1 else '')
            if key in ('admin', 'office'):
                joined, qual = (c[3] if len(c) > 3 else ''), (c[4] if len(c) > 4 else '')
            else:
                qual = c[3] if len(c) > 3 else ''
                joined = c[5] if len(c) > 5 else ''
            people.append(dict(name=name.title().replace(' Of ', ' of '), role=role, qual=qual, joined=joined, photo=photo))
        out[key] = people
    return out


def staff_photo(p):
    if p['photo'] and os.path.isfile(os.path.join(ORIG, p['photo'])):
        return thumb(p['photo'], w=360)
    return None


def initials(name):
    w = [x for x in re.split(r'\s+', name.replace('Dr ', '').replace('Dr. ', '')) if x]
    return (w[0][0] + (w[-1][0] if len(w) > 1 else '')).upper()


def parse_org():
    """Governing body and managing committee: [(name, role, photo)]"""
    s = re.sub(r'<!--.*?-->', '', read_crawl('org_structure.html'), flags=re.S)
    i = s.find('Members of the School Managing Committee')
    out = []
    for chunk in (s[:i], s[i:]):
        grp = []
        for r in re.findall(r'<tr>(.*?)</tr>', chunk, flags=re.S):
            m = re.search(r'<img[^>]+src="([^"]+)"', r)
            cells = re.findall(r'<td[^>]*>(.*?)</td>', r, flags=re.S)
            if not cells:
                continue
            t = html.unescape(re.sub(r'<br\s*/?>', '|', cells[-1]))
            t = re.sub(r'<[^>]+>', '', t)
            parts = [x.strip(' ,\n\t') for x in t.split('|') if x.strip(' ,\n\t')]
            if len(parts) >= 2:
                grp.append((parts[0], ' '.join(parts[1:]), m.group(1).replace('../', '') if m else None))
        out.append(grp)
    return out
