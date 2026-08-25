#!/usr/bin/env python3
"""Stamp every asset link with a content hash so a stale cache can never
render new markup against old CSS. Re-run after touching anything in assets/."""
import hashlib, re, glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def h(path):
    return hashlib.sha1(open(path, "rb").read()).hexdigest()[:8]

vers = {f: h(os.path.join(ROOT, "assets", f))
        for f in ("styles.css", "main.js", "funnel.js")}

n = 0
targets = glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)
targets.append(os.path.join(ROOT, "_build", "pages.py"))
for path in targets:
    t = open(path, encoding="utf-8").read(); o = t
    for f, v in vers.items():
        # match assets/<file> with or without an existing ?v=
        t = re.sub(r'((?:\.\./)*assets/' + re.escape(f) + r')(\?v=[0-9a-f]+)?"',
                   lambda m: f'{m.group(1)}?v={v}"', t)
    if t != o:
        open(path, "w", encoding="utf-8").write(t); n += 1
        print("  stamped", os.path.relpath(path, ROOT))
print("versions:", ", ".join(f"{k}={v}" for k, v in vers.items()), f"| {n} files")
