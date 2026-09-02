#!/usr/bin/env python3
"""Re-splice index.html's header and footer from pages.py.

index.html is the one hand-maintained page, which means it carried hand-copied
twins of the util bar, the nav dropdown, the mobile drawer and all four footer
columns. Those twins drifted every single time the generated pages changed —
README records three separate silent drifts of the practice list alone.

This replaces the twins with the real thing. The hero, stats, practice grid,
partners and FAQ between them stay hand-maintained; only the two chrome blocks
are machine-written.

Run it after pages.py, before bust.py:
    python3 _build/pages.py && python3 _build/sync_index.py && python3 _build/bust.py
"""
import io, os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pages

ROOT = pages.ROOT
p = os.path.join(ROOT, "index.html")
s = io.open(p, encoding="utf-8").read()

# --- header: <div class="util"> .. </header> ---------------------------------
start = s.index('<div class="util">')
end = s.index("</header>") + len("</header>")
s = s[:start] + pages.header().rstrip("\n") + s[end:]

# --- footer: <footer class="ftr"> .. </html> ---------------------------------
start = s.index('<footer class="ftr">')
s = s[:start] + pages.footer()

io.open(p, "w", encoding="utf-8").write(s)

# The homepage is the only page whose chrome is spliced rather than generated, so
# assert the splice actually took rather than trusting it.
chk = io.open(p, encoding="utf-8").read()
for must in ['href="industries.html"', 'href="locations/houston.html"',
             'href="roles/community-association-manager-recruiters.html"',
             'href="sitemap.xml"', 'Executive search &middot; Recruiting nationwide']:
    assert must in chk, f"splice lost: {must}"
assert 'href="#">Sitemap' not in chk and 'href="#">Privacy' not in chk
print("  index.html header + footer re-synced from pages.py")
