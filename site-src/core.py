"""Shared helpers for the DPS Visakhapatnam static-site build."""
import os, re, html, json, shutil, urllib.parse
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ORIG = os.path.join(HERE, 'orig')
CRAWL = os.path.join(HERE, 'crawl')
OUT_IMG = os.path.join(ROOT, 'assets', 'img')
OUT_DOC = os.path.join(ROOT, 'docs')
os.makedirs(OUT_IMG, exist_ok=True)
os.makedirs(OUT_DOC, exist_ok=True)

SPAM = re.compile(r'replica|imitaz|faux |fake |falso|dupe|pas cher|tasche|kaufen|louis vuitton|lakers|jersey|hermes|gucci|chanel|goyard|cartier|dior', re.I)


def slug(s):
    s = os.path.splitext(s)[0] if re.search(r'\.\w{2,4}$', s) else s
    s = re.sub(r'[^A-Za-z0-9]+', '-', s).strip('-').lower()
    return s or 'file'


def esc(s):
    return html.escape(s, quote=True)


_img_cache = {}


def img(rel, w=1400, q=76, fmt=None, name=None):
    """Optimise an original image into assets/img and return its site URL.
    `rel` is relative to site-src/orig (e.g. 'img/principal1.jpeg')."""
    key = (rel, w, fmt)
    if key in _img_cache:
        return _img_cache[key]
    src = os.path.join(ORIG, rel)
    if not os.path.exists(src):
        print('  ! missing image', rel)
        return 'assets/img/missing.png'
    im = Image.open(src)
    im = ImageOps.exif_transpose(im)
    has_alpha = im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info)
    ext = fmt or ('png' if has_alpha else 'jpg')
    base = name or slug(rel.replace('/', '-'))
    out = f'{base}.{ext}'
    dst = os.path.join(OUT_IMG, out)
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    if ext == 'png':
        im.convert('RGBA').save(dst, optimize=True)
    else:
        im.convert('RGB').save(dst, quality=q, optimize=True, progressive=True)
    url = 'assets/img/' + out
    _img_cache[key] = url
    return url


def thumb(rel, w=420, name=None):
    return img(rel, w=w, q=72, name=(name or slug(rel.replace('/', '-'))) + f'-{w}')


_doc_cache = {}


def doc(rel):
    """Copy a downloaded document into docs/ with a clean name; return URL."""
    if rel in _doc_cache:
        return _doc_cache[rel]
    src = os.path.join(ORIG, rel)
    if not os.path.exists(src):
        print('  ! missing doc', rel)
        return '#'
    stem, ext = os.path.splitext(os.path.basename(rel))
    ext = ext.lower().replace('.jpeg', '.jpg')
    parent = os.path.basename(os.path.dirname(rel))
    name = slug(stem)
    if parent in ('assignments', 'syllabus'):
        name = parent + '-' + name
    if ext in ('.jpg', '.jpeg', '.png'):
        # keep calendar/fee images zoomable but not enormous
        im = Image.open(src)
        im = ImageOps.exif_transpose(im)
        if im.width > 2600:
            im = im.resize((2600, round(im.height * 2600 / im.width)), Image.LANCZOS)
        dst = os.path.join(OUT_DOC, name + '.jpg')
        im.convert('RGB').save(dst, quality=82, optimize=True)
        url = 'docs/' + name + '.jpg'
    else:
        dst = os.path.join(OUT_DOC, name + ext)
        shutil.copyfile(src, dst)
        url = 'docs/' + name + ext
    _doc_cache[rel] = url
    return url


def size_of(url):
    p = os.path.join(ROOT, url)
    if not os.path.exists(p):
        return ''
    n = os.path.getsize(p)
    return f'{n/1e6:.1f} MB' if n > 1e6 else f'{max(1, round(n/1e3))} KB'


# ---------- cleaning old-site markup ----------

def read_crawl(name):
    return open(os.path.join(CRAWL, name), encoding='utf8', errors='ignore').read()


def main_of(name):
    """Return the cleaned main content of an old-site page (after the banner header)."""
    s = read_crawl(name)
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    m = re.search(r'</header>\s*<!--.*?-->|<img class="arrow-object"[^>]*>\s*</header>', s, flags=re.S)
    i = s.find('arrow-object')
    i = s.find('</header>', i)
    j = s.find('</article>')
    body = s[i + len('</header>'):j]
    return clean_html(body)


def clean_html(b):
    b = re.sub(r'<script.*?</script>|<style.*?</style>', '', b, flags=re.S)
    b = re.sub(r'<i class="icon[^>]*></i>', '', b)
    # drop spam
    b = re.sub(r'<(p|a|li|div|span)[^>]*>[^<]*(%s)[^<]*</\1>' % SPAM.pattern, '', b, flags=re.I)
    # keep only essential attrs
    def attrs(m):
        tag, rest = m.group(1), m.group(2)
        keep = []
        for a in re.finditer(r'(href|src|alt|colspan|rowspan|target)\s*=\s*("[^"]*"|\'[^\']*\'|[^\s>]+)', rest):
            keep.append(f'{a.group(1)}={a.group(2)}')
        return f'<{tag}{" " + " ".join(keep) if keep else ""}>'
    b = re.sub(r'<(?!/)(\w+)([^>]*)>', attrs, b)
    b = re.sub(r'</?(section|center|font|span|article|main|nav|header|footer)[^>]*>', '', b)
    b = re.sub(r'<div>\s*</div>', '', b)
    b = re.sub(r'</?div>', '', b)
    b = re.sub(r'<(h[1-6])>\s*<b>(.*?)</b>\s*</\1>', r'<\1>\2</\1>', b, flags=re.S)
    b = re.sub(r'<b>(.*?)</b>', r'<strong>\1</strong>', b, flags=re.S)
    b = b.replace('<h2>', '<h3>').replace('</h2>', '</h3>')
    b = re.sub(r'&nbsp;', ' ', b)
    b = re.sub(r'<p>\s*</p>', '', b)
    b = re.sub(r'<br>\s*<br>', '</p><p>', b)
    # tables -> styled
    b = re.sub(r'<table>', '<div class="tbl-wrap"><table class="t">', b)
    b = b.replace('</table>', '</table></div>')
    return b


def rewrite_links(b, base_dir='pages'):
    """Point old ../docs/.. and ../img/.. links at the new optimised copies."""
    def d(m):
        attr, path = m.group(1), urllib.parse.unquote(m.group(2))
        rel = path.replace('../', '')
        if rel.startswith('docs/'):
            return f'{attr}="{doc(rel)}"'
        if re.search(r'\.(jpe?g|png|gif)$', rel, re.I):
            return f'{attr}="{img(rel, w=900)}"'
        return m.group(0)
    return re.sub(r'(href|src)="((?:\.\./)(?:docs|img)/[^"]+)"', d, b)


def text_of(h):
    return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h))).strip()
