"""Seed content/page-<name>.json from the built pages.
Every element carrying data-text / data-md / data-docimg / data-list is lifted out of the static HTML, so the
JSON starts out identical to what is on the page. Existing JSON files are never overwritten (the school edits them)."""
import os, re, json
from bs4 import BeautifulSoup
from markdownify import markdownify as mdify
from core import ROOT
from layout import ICON

CONTENT = os.path.join(ROOT, 'content')
SVG2KEY = {v: k for k, v in ICON.items()}
PAGES = ['index', 'about', 'academics', 'admissions', 'campus']


_sig = lambda x: tuple(sorted(re.findall(r'(?:d|cx|cy|r|x|y|width|height|rx)="([^"]*)"', str(x))))
SIG2KEY = {_sig(v): k for k, v in ICON.items()}


def icon_key(el):
    svg = el.find('svg')
    return SIG2KEY.get(_sig(svg), '') if svg else ''


def txt(el):
    return re.sub(r'\s+', ' ', el.get_text(' ', strip=True)) if el else ''


def md(el):
    inner = ''.join(str(c) for c in el.children)
    inner = re.sub(r'\s*<br\s*/?>\s*', '  \n', inner)
    out = mdify(inner, heading_style='ATX', bullets='-', strip=['a'] if False else None)
    out = re.sub(r'\n{3,}', '\n\n', out).strip()
    return out


def parse_list(el, tpl):
    out = []
    kids = [c for c in el.find_all(recursive=False)]
    if tpl == 'stat':
        for k in kids: out.append({'number': txt(k.find('b')), 'label': txt(k.find('span'))})
    elif tpl == 'why':
        for k in kids: out.append({'icon': icon_key(k), 'title': txt(k.find('h3')), 'text': txt(k.find('p'))})
    elif tpl == 'step':
        for k in kids: out.append({'when': txt(k.find('small')), 'title': txt(k.find('h3')), 'text': txt(k.find('p'))})
    elif tpl == 'house':
        for k in kids: out.append({'name': txt(k.find('b'))})
    elif tpl in ('pill', 'pill2'):
        out = [txt(k) for k in kids]
    elif tpl == 'dcard':
        for k in kids:
            color = re.search(r'border-top:\s*6px solid (#[0-9a-fA-F]+)', k.get('style', ''))
            ps = [p for p in k.find_all('p', recursive=False)]
            note = next((txt(p) for p in ps if 'note' in (p.get('class') or [])), '')
            intro = next((txt(p) for p in ps if 'note' not in (p.get('class') or [])), '')
            out.append({'title': txt(k.find('h3')), 'color': color.group(1) if color else '#0e4a2c', 'intro': intro, 'items': [txt(li) for li in k.find_all('li')], 'note': note})
    elif tpl == 'faq':
        for k in kids: out.append({'question': txt(k.find('summary')), 'answer': txt(k.find(class_='ans'))})
    elif tpl == 'mentor':
        for k in kids:
            im = k.find('img'); src = im.get('src') if im else ''
            out.append({'name': txt(k.find('b')), 'role': txt(k.find('span')), **({'photo': src} if src else {})})
    elif tpl == 'pcard':
        for k in kids:
            body = BeautifulSoup('', 'html.parser'); box = body.new_tag('div')
            for p in k.find_all('p'): box.append(BeautifulSoup(str(p), 'html.parser'))
            out.append({'icon': icon_key(k), 'title': txt(k.find('h3')), 'body': md(box)})
    elif tpl == 'doclink':
        for k in kids:
            a = k.find('a'); out.append({'title': txt(a.find('b')), 'file': a.get('href')})
    elif tpl == 'calendars':
        tabs = el.select('[role=tab]'); panels = el.select('[role=tabpanel]')
        for t, p in zip(tabs, panels):
            z = p.find(attrs={'data-zoom': True}); out.append({'title': txt(t), 'image': z.get('data-zoom') if z else ''})
    elif tpl == 'day':
        for k in kids:
            d = {'title': txt(k.find('p')), 'month': k.get('data-m')}
            if k.get('data-n'):
                d.update({'nth': k.get('data-n'), 'weekday': k.get('data-w')})
            else:
                d['day'] = k.get('data-d')
            out.append(d)
    return out


AWARDS_MD = """### Encouragement Systems

DPS Visakhapatnam believes in encouraging the achievers in all fields by giving prizes and awards. These prizes / awards are given not only in the field of academics but also in sports and co-curricular activities.

#### Academics

- **100% Attendance** – Students who have 100% attendance in the session are presented with trophies.
- **Class Toppers**
    - III to X: Students scoring first three positions according to the overall percentage of marks will receive mementos.
    - XI: Rank prizes will be given to the students securing first three positions in the class in all three streams separately.
    - XII: The board class toppers in the school will be awarded Chairman’s Trophies.
- **Subject Toppers** – Principal’s Trophies will be given to students who score the highest marks in each subject in school in class XII.
- **Scholars** – Criteria for awarding scholar ties / blazer / medal: in order to encourage the bright students the school awards ‘Scholar Ties’ to the deserving students. The criteria for the same is as follows:
    - Classes III to V: Students scoring A1 grades in English, II Language, Mathematics, Science and Social Science individually.
    - Classes VI to X: Students scoring A2 & A1 grades in English, II Language, Mathematics, Science and Social Science individually.
    - Classes XI & XII: Students scoring B1 grade and above in all subjects individually.

*Note: It is mandatory for a student to appear in all HYE and AE to be qualified for Scholar Award.*

#### Sports

**Inter House Track and Field Events:** The first, second and third place holders are given Gold, Silver and Bronze medals respectively for each track and field event.

**Best Athlete (Boy and Girl):** The student winning maximum number of prizes in each group as per the following details is adjudged as the best athlete and given a trophy.

| Medal | Gold | Silver | Bronze |
| --- | --- | --- | --- |
| Marks | 5 | 3 | 2 |

In case of a tie the student winning more number of Golds will be adjudged as the best athlete.

**Open Game / Sports Meet:** Students taking part and winning prizes in these meets are also given awards as per the following table.

| Position | Level | Award |
| --- | --- | --- |
| 1st or 2nd | State | Track Suit |
| 1st or 2nd for 3 consecutive years | State | Track Suit & Maroon Blazer |
| 1st, 2nd or 3rd | National | Track Suit & Maroon Blazer |

**CBSE Games / Sports Meet:** The students winning a medal / prize in the National Games / Sports competitions conducted by CBSE will be awarded a TRACK SUIT from the school.

*Note: The school will bear the whole participation expenses of students taking part in the National Games / Sports competitions whether open or conducted by CBSE.*

#### Co-curricular

Trophies are given to the 1st, 2nd and 3rd position winners of the various Inter House and Intra Class competitions held from time to time in the school. The trophies are given at the time of the competition itself.

**Best Student:** The best student is selected from each group (III–V), (VI–VIII) and (IX–XII) on the basis of his/her performance in academics, sports, Inter House & outside competitions. The marks calculation is done as per the tables below.

| Class toppers | A1 | A2 | B1 |
| --- | --- | --- | --- |
| 1. Class toppers | 20 | 15 | 10 |

| Other performance | I | II | III |
| --- | --- | --- | --- |
| 2. Other individual performance | 10 | 7 | 5 |
| 3. Team performance | 5 | 3 | 2 |
| 4. Group performance | 3 | 2 | 1 |
| 5. 100% attendance | 10 | – | – |

**Best House:** The best House award is given to the House scoring maximum points in the co-curricular competitions, sports & academics as per the following table.

| Points for | I | II | III | IV |
| --- | --- | --- | --- | --- |
| 1. Individual performance | 3 | 2 | 1 | – |
| 2. Team performance | 5 | 3 | 2 | – |
| 3. Group performance | 20 | 15 | 10 | 5 |
| 4. 100% attendance | 2 | – | – | – |

*Notes: In the tables above, a team is 4 or fewer participants, whereas a group is more than 4. Outside competitions are the ones recognised by the school. Students aspiring for the Best Student Award have to apply in the format available in the school’s office.*
"""


def run():
    for name in PAGES:
        path = os.path.join(CONTENT, f'page-{name}.json')
        if os.path.exists(path):
            continue
        soup = BeautifulSoup(open(os.path.join(ROOT, name + '.html'), encoding='utf8').read(), 'html.parser')
        data = {}
        for el in soup.select('[data-text]'):
            if not el.get('data-src'): data[el['data-text']] = txt(el)
        for el in soup.select('[data-md]'):
            data[el['data-md']] = AWARDS_MD if el['data-md'] == 'awards_md' else md(el)
        for el in soup.select('[data-docimg]'):
            z = el.find(attrs={'data-zoom': True}); data[el['data-docimg']] = z.get('data-zoom') if z else ''
        for el in soup.select('[data-list]'):
            if el.get('data-src'): continue
            data[el['data-list']] = parse_list(el, el.get('data-tpl'))
        json.dump(data, open(path, 'w', encoding='utf8'), indent=2, ensure_ascii=False)
        print('  seeded content/page-' + name + '.json', {k: (len(v) if isinstance(v, list) else 'text') for k, v in data.items()})
