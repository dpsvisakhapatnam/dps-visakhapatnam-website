"""Point the site's settings at a custom domain.   Usage:
    python3 site-src/switch_domain.py https://www.dpsvisakhapatnam.org [--dry-run]
Updates admin/config.yml (site_url, display_url) and the sitemap/robots address in build.py, then rebuilds."""
import os, re, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
args = [a for a in sys.argv[1:] if not a.startswith('--')]
dry = '--dry-run' in sys.argv
if not args or not re.match(r'^https://[a-z0-9.-]+$', args[0].rstrip('/')):
    sys.exit('Give the new address, e.g. https://www.dpsvisakhapatnam.org')
new = args[0].rstrip('/')
cfg = os.path.join(ROOT, 'admin', 'config.yml'); bld = os.path.join(HERE, 'build.py')
c = open(cfg).read(); b = open(bld).read()
c2 = re.sub(r'^(site_url|display_url): \S+', lambda m: f'{m.group(1)}: {new}', c, flags=re.M)
b2 = re.sub(r"^base = '[^']+'", f"base = '{new}/'", b, flags=re.M)
print('admin/config.yml:', 'changed' if c2 != c else 'already set'); print('build.py       :', 'changed' if b2 != b else 'already set')
if dry: sys.exit('dry run, nothing written')
open(cfg, 'w').write(c2); open(bld, 'w').write(b2)
subprocess.check_call([sys.executable, bld], cwd=HERE)
print('\nDone. Now commit and push (GitHub Desktop: Commit to main, then Push origin).')
