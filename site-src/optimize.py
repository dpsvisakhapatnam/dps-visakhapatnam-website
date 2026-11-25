"""Post-build image optimiser. Run after the pages are built (build.py calls it).

1. Writes WebP versions of the big photos at phone/tablet/desktop widths into assets/rs/.
2. Adds srcset / sizes / width / height to every matching <img> in the built pages, so a phone
   downloads ~40-80 KB instead of the 300-400 KB original, and the page does not jump while loading.
3. Preloads the first hero photo on the home page (it is the largest thing on screen).

Naming rule (also used by content.js for photos chosen in the editor):
    assets/gallery/g9.jpg  ->  assets/rs/gallery-g9-<width>.webp
Originals stay in place as the fallback `src`, so nothing breaks if a variant is missing.
"""
import glob
import os
import re
from html import escape

from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'rs')
WIDTHS = (480, 720, 960, 1440)
MIN_SOURCE = 560  # smaller pictures (staff photos, badges) are already light enough
SIZES_DEFAULT = '(max-width:900px) 92vw, 600px'


def rsname(rel, w):
    base = re.sub(r'\.\w+$', '', re.sub(r'^assets/', '', rel)).replace('/', '-')
    return f'assets/rs/{base}-{w}.webp'


def candidates():
    pats = ['assets/gallery/*', 'assets/img/*', 'assets/hero*.jpg', 'assets/principal1.jpeg']
    for pat in pats:
        for f in sorted(glob.glob(os.path.join(ROOT, pat))):
            if re.search(r'\.(jpe?g|png)$', f, re.I):
                yield os.path.relpath(f, ROOT).replace(os.sep, '/')


def make_variants():
    os.makedirs(OUT, exist_ok=True)
    info = {}
    made = 0
    for rel in candidates():
        src = os.path.join(ROOT, rel)
        try:
            im = Image.open(src)
            im = ImageOps.exif_transpose(im)
        except Exception as e:  # noqa: BLE001
            print('  ! skip', rel, e)
            continue
        w0, h0 = im.size
        if w0 < MIN_SOURCE:
            continue
        sizes = []
        for w in WIDTHS:
            # never upscale: the first width at or above the photo's own width becomes its full-size copy
            tw = min(w, w0)
            if sizes and sizes[-1][0] == w0:
                break
            out_rel = rsname(rel, w)
            dst = os.path.join(ROOT, out_rel)
            if not (os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src)):
                th = round(h0 * tw / w0)
                v = im.resize((tw, th), Image.LANCZOS) if tw != w0 else im
                has_alpha = v.mode in ('RGBA', 'LA') or (v.mode == 'P' and 'transparency' in v.info)
                v = v.convert('RGBA' if has_alpha else 'RGB')
                v.save(dst, 'WEBP', quality=68, method=6)
                made += 1
            sizes.append((tw, out_rel))
        info[rel] = (w0, h0, sizes)
    print(f'  image variants: {len(info)} photos, {made} files written')
    return info


def srcset(sizes):
    return ', '.join(f'{p} {w}w' for w, p in sizes)


def pick_sizes(before, tag):
    """`sizes` tells the browser how wide the picture is on screen, from the wrapper just before it."""
    wrapper = re.search(r'<(\w+)[^>]*class="([^"]*)"[^>]*>\s*$', before)
    classes = wrapper.group(2).split() if wrapper else []
    if 'data-hero' in tag or 'slide' in classes:
        return '100vw'
    if wrapper and wrapper.group(1) == 'button' and 'g' in classes:
        return '(max-width:700px) 100vw, 50vw' if 'wide' in classes else '(max-width:700px) 50vw, 25vw'
    return SIZES_DEFAULT


def enhance(tag, sizes, info):
    sm = re.search(r'\b(data-src|src)="(assets/[^"]+)"', tag)
    if not sm or 'srcset=' in tag or sm.group(2) not in info:
        return tag
    w0, h0, variants = info[sm.group(2)]
    add = f' data-srcset="{srcset(variants)}"' if 'data-hero' in tag else f' srcset="{srcset(variants)}" sizes="{sizes}"'
    if 'width=' not in tag:
        add += f' width="{w0}" height="{h0}"'
    if 'decoding=' not in tag:
        add += ' decoding="async"'
    return tag[:-1].rstrip('/').rstrip() + add + '>'


def process_html(info):
    changed = 0
    for page in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
        s = open(page, encoding='utf8').read()
        orig = s
        out, pos = [], 0
        for m in re.finditer(r'<img\b[^>]*>', s):
            out.append(s[pos:m.start()])
            out.append(enhance(m.group(0), pick_sizes(s[max(0, m.start() - 400):m.start()], m.group(0)), info))
            pos = m.end()
        out.append(s[pos:])
        s = ''.join(out)

        if os.path.basename(page) == 'index.html':
            hm = re.search(r'<div class="slide on">\s*<img[^>]*\bsrc="(assets/[^"]+)"', s)
            if hm and hm.group(1) in info and 'rel="preload" as="image"' not in s:
                sz = info[hm.group(1)][2]
                pre = (f'<link rel="preload" as="image" href="{hm.group(1)}" imagesrcset="{escape(srcset(sz))}" '
                       f'imagesizes="100vw" fetchpriority="high">\n')
                s = s.replace('<link rel="stylesheet" href="styles.css">', pre + '<link rel="stylesheet" href="styles.css">', 1)

        if s != orig:
            open(page, 'w', encoding='utf8').write(s)
            changed += 1
    print(f'  pages updated with responsive images: {changed}')


def make_logo():
    """The school crest is shown at ~46px but shipped at 146px: make a light 2x copy for the header/footer."""
    src, dst = os.path.join(ROOT, 'assets', 'dpslogo.png'), os.path.join(ROOT, 'assets', 'dpslogo-sm.png')
    if os.path.exists(src) and not (os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src)):
        im = Image.open(src).convert('RGBA')
        im = im.resize((92, round(im.height * 92 / im.width)), Image.LANCZOS)
        im.quantize(colors=128, method=Image.FASTOCTREE).save(dst, optimize=True)
        print('  logo: dpslogo-sm.png', os.path.getsize(dst) // 1024, 'KB')


def minify():
    """Shrink the three site files in place (the readable sources stay in site-src/). Skipped if esbuild is unavailable."""
    import shutil
    import subprocess
    if not shutil.which('npx'):
        print('  (npx not found, skipping minify)')
        return
    for f in ('styles.css', 'script.js', 'content.js'):
        p = os.path.join(ROOT, f)
        before = os.path.getsize(p)
        r = subprocess.run(['npx', '--yes', 'esbuild@0.24.2', p, '--minify', '--allow-overwrite', '--outfile=' + p, '--log-level=error'],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print('  ! minify failed for', f, r.stderr[:200])
            continue
        print(f'  minified {f}: {before // 1024} KB -> {os.path.getsize(p) // 1024} KB')


if __name__ == '__main__':
    process_html(make_variants())
