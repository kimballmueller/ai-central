#!/usr/bin/env python3
"""Every internal href/src must resolve to a file on disk, and every practice
page must be reachable from every page. This is the only check that catches a
bad "../" after a change to page depth — run it after any such change."""
import os, re, glob, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)
bad, n = [], 0
for f in glob.glob("**/*.html", recursive=True):
    base = os.path.dirname(f)
    for href in re.findall(r'(?:href|src)="([^"]+)"', open(f, encoding="utf-8").read()):
        if href.startswith(("http", "mailto:", "tel:", "#", "data:")): continue
        path = href.split("#")[0].split("?")[0]
        if not path: continue
        n += 1
        if not os.path.exists(os.path.normpath(os.path.join(base, path))):
            bad.append((f, href))
css = open("assets/styles.css", encoding="utf-8").read()
css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)          # comments are not references
for u in re.findall(r'url\(([^)]+)\)', css):
    u = u.strip('"\''); n += 1
    if not os.path.exists(os.path.join("assets", u)): bad.append(("assets/styles.css", u))

slugs = sorted(os.path.basename(p)[:-5] for p in glob.glob("industries/*.html"))
orphan = []
for f in sorted(glob.glob("**/*.html", recursive=True)):
    html = open(f, encoding="utf-8").read()
    miss = [s for s in slugs if f"{s}.html" not in html]
    if miss: orphan.append((f, miss))

print(f"{n} internal references checked ->", "all resolve" if not bad else f"{len(set(bad))} BROKEN")
for f, h in sorted(set(bad)): print("   BROKEN", f, "->", h)
for f, m in orphan: print("   ", f, "does not link:", ", ".join(m))
print(f"{len(slugs)} practice pages, all cross-linked" if not orphan else "")
sys.exit(1 if bad or orphan else 0)
