# DPS Visakhapatnam Steel Plant — new website

Static site (HTML/CSS/JS, no framework). Open `index.html` or serve the folder:

    python3 -m http.server 5173

Deploy by uploading everything except `site-src/` to any static host (Netlify, GitHub Pages, cPanel).

## Editing
Pages are generated from `site-src/` (Python + Pillow):

    cd site-src && python3 build.py

- `pages_home.py`, `pages_a.py`, `pages_b.py` — page content
- `layout.py` — header, menu, footer, modals
- `styles.css`, `script.js` — copied to the site root on build
- `orig/` and `crawl/` — snapshot of the old site (images, PDFs, HTML) used as the source of truth; safe to delete after launch to save ~300 MB

Before launch: replace `https://example.org/` in `site-src/build.py` with the real domain (sitemap/robots).
