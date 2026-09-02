#!/usr/bin/env python3
"""Holds the nationwide re-optimization in place.

The site used to target "executive search firm Houston". It now targets
vertical+role terms with no geographic modifier, and the local terms are
quarantined on locations/houston.html so the local pack is not lost.

Nothing else in the suite asserts on titles, descriptions or areaServed, so a
stray "Houston" could reappear in a title and nothing would notice. This is that
test. It checks the surfaces that actually carry ranking weight, and deliberately
tolerates the places a geographic word is simply the truth.

Run:  python3 _build/tests/geo.py
"""
import io, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GEO = re.compile(r"\b(Houston|Texas|TX)\b", re.I)

# Geographic claims allowed to survive anywhere. Each is a factual statement
# about where the firm's network physically is, not a keyword. Adding to this
# list should be a deliberate act, not a way to make the test go quiet.
ALLOWED_PHRASES = [
    "Gulf Coast",       # the industrial / subsea / ROV network — a real claim
    "deepwater Gulf",   # industry vocabulary, not geo-SEO
    "Permian",          # basin name; how energy hiring is actually discussed
]

# Lines that legitimately contain a place name. These are not keyword surfaces.
TOLERATED_LINE = re.compile(
    r"locations/houston\.html"          # links to the local page itself
    r"|sublimepersonnel\.com/blog/"     # real published posts, off-site URLs
    r"|addressLocality|addressRegion|PostalAddress"   # the real registered address
    r"|data-state=|<option value=\"[A-Z]{2}\">"       # job board state filter
    r"|job-meta"                        # real listings in real cities, incl. Texas ones
)

LOCAL_PAGES = {"locations/houston.html"}

def scrub(t):
    for a in ALLOWED_PHRASES:
        t = t.replace(a, "")
    return t

def blog_titles():
    """The real titles of their live posts. We render them verbatim — rewriting a
    published post's title to drop 'Texas' would misrepresent their own content."""
    sys.path.insert(0, os.path.join(ROOT, "_build"))
    import pages
    out = set()
    for p in pages.POSTS:
        out.update(str(x) for x in p if isinstance(x, str))
    return out

def main():
    os.chdir(ROOT)
    titles = blog_titles()
    files = [f for f in sorted(glob.glob("**/*.html", recursive=True))
             if not f.startswith("_build/")]
    files += [f for f in ("llms.txt", "sitemap.xml", "robots.txt") if os.path.exists(f)]
    fails = []

    # ---- 1. the head of every page must be geographically neutral -------------
    for f in files:
        if not f.endswith(".html") or f in LOCAL_PAGES:
            continue
        s = io.open(f, encoding="utf-8").read()
        head = s.split("</head>")[0]
        for tag, pat in (("title", r"<title>(.*?)</title>"),
                         ("description", r'<meta name="description" content="(.*?)"'),
                         ("og:title", r'<meta property="og:title" content="(.*?)"')):
            m = re.search(pat, head, re.S)
            if m and GEO.search(scrub(m.group(1))):
                fails.append(f"{f}  <{tag}> carries a geo term: {m.group(1)[:80]}")
        if re.search(r'"areaServed"\s*:\s*"[^"]*(Houston|Texas)', s):
            fails.append(f"{f}  Service schema areaServed is still local")

    # ---- 2. no geo in an H1, H2 or eyebrow ------------------------------------
    for f in files:
        if not f.endswith(".html") or f in LOCAL_PAGES:
            continue
        s = io.open(f, encoding="utf-8").read()
        for m in re.finditer(r"<(h1|h2)[^>]*>(.*?)</\1>", s, re.S):
            txt = re.sub(r"<[^>]+>", "", m.group(2))
            if txt in titles:          # a real published post title
                continue
            if GEO.search(scrub(txt)):
                fails.append(f"{f}  <{m.group(1)}> carries a geo term: {txt.strip()[:70]}")

    # ---- 3. body copy, minus the tolerated cases -----------------------------
    for f in files:
        if f in LOCAL_PAGES:
            continue
        for n, line in enumerate(io.open(f, encoding="utf-8"), 1):
            if TOLERATED_LINE.search(line):
                continue
            stripped = re.sub(r"<[^>]+>", " ", scrub(line))
            for t in titles:
                stripped = stripped.replace(t, "")
            if GEO.search(stripped):
                fails.append(f"{f}:{n}  {line.strip()[:100]}")

    # ---- 4. the local page must still be doing its job ------------------------
    if not os.path.exists("locations/houston.html"):
        fails.append("locations/houston.html is missing — the local cluster is gone")
    else:
        s = io.open("locations/houston.html", encoding="utf-8").read()
        if s.count("Houston") < 6:
            fails.append("locations/houston.html has lost its local terms")
        if "LocalBusiness" not in s:
            fails.append("locations/houston.html has no LocalBusiness schema")
    # and the Organization node must still carry the real address
    idx = io.open("index.html", encoding="utf-8").read()
    if "EmploymentAgency" not in idx or '"addressLocality":"Houston"' not in idx:
        fails.append("index.html lost its Organization node or its real address")

    if fails:
        print(f"geo: FAIL ({len(fails)})")
        for f in fails:
            print("   ", f)
        return 1
    print(f"geo: pass — {len(files)} files checked; heads, headings and body copy "
          "are geographically neutral, local terms contained to locations/houston.html")
    return 0

if __name__ == "__main__":
    sys.exit(main())
