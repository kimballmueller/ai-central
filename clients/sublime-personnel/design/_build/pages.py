#!/usr/bin/env python3
"""Generates every page except index.html, so header/footer never drift.
Run from design/:  python3 _build/pages.py && python3 _build/bust.py"""
import os, sys, re, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from industries import INDUSTRIES, STANDARD_FAQ
from roles import ROLES
from glossary import GLOSSARY, RECRUITING_TERMS
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Production origin. Canonicals, og:url and sitemap.xml are all absolute URLs, which
# means they must point at where the site will actually live — not at the staging
# link. If the domain changes, this is the only line to edit.
SITE = "https://sublimepersonnel.com"

ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4"/></svg>'
PHONE = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.5 11.3v2a1.3 1.3 0 0 1-1.5 1.3 13 13 0 0 1-5.7-2 12.8 12.8 0 0 1-4-4 13 13 0 0 1-2-5.8A1.3 1.3 0 0 1 2.7 1.3h2A1.3 1.3 0 0 1 6 2.5c.1.6.2 1.3.5 1.9a1.3 1.3 0 0 1-.3 1.4l-.9.8a10.7 10.7 0 0 0 4 4l.8-.8a1.3 1.3 0 0 1 1.4-.3c.6.2 1.2.4 1.9.4a1.3 1.3 0 0 1 1.1 1.4z"/></svg>'
CHECK = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m4 10.4 4 4 8-9"/></svg>'
LOCK  = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="8.6" width="12" height="8.4" rx="2"/><path d="M6.9 8.6V6.4a3.1 3.1 0 0 1 6.2 0v2.2"/></svg>'
CLOCK = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="10" cy="10" r="7.4"/><path d="M10 5.8V10l2.8 1.7"/></svg>'
SHIELD= '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 2.2 3.8 4.7v4.6c0 3.9 2.6 7.1 6.2 8.5 3.6-1.4 6.2-4.6 6.2-8.5V4.7z"/><path d="m7.6 9.9 1.8 1.8 3.3-3.5"/></svg>'
SEARCH= '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="9" r="5.6"/><path d="m13.2 13.2 3.6 3.6"/></svg>'
DOC   = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11.5 2.5H6a1.5 1.5 0 0 0-1.5 1.5v12A1.5 1.5 0 0 0 6 17.5h8a1.5 1.5 0 0 0 1.5-1.5V6.5z"/><path d="M11.5 2.5v4h4M7.5 11h5M7.5 14h3"/></svg>'
USER  = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="10" cy="6.8" r="3"/><path d="M4 16.6a6 6 0 0 1 12 0"/></svg>'

# Derived from _build/industries.py so the nav, the footer, the practice grid and
# the "NN of NN" numbering cannot drift from the practice content. One list, one
# source — this used to be a second hardcoded copy and it went stale immediately.
VERTICALS = [(i["slug"], i["nav"], i["navsub"]) for i in INDUSTRIES]
IND_NUM = {slug: f"{n+1:02d}" for n, (slug, _, _) in enumerate(VERTICALS)}

# d = directory depth below the site root, so industries/ pages get "../".
# path = this page's URL relative to the site root ("clients.html",
# "industries/healthcare.html"). It drives the canonical and og:url, both of which
# must be absolute, so it cannot be derived from the "../" prefix. PAGES registers
# it once per page and the sitemap reads the same list — see build_sitemap().
def head(title, desc, d=0, schema="", path=""):
    r = "../" * d
    url = f"{SITE}/{path}"
    # Strip entities out of the title for og/twitter: those are plain-text fields and
    # a raw &amp; renders literally in a link preview.
    plain = html.unescape(re.sub(r"<[^>]+>", "", title)).replace("‑", "-")
    pdesc = html.unescape(re.sub(r"<[^>]+>", "", desc)).replace("‑", "-")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Sublime Personnel">
<meta property="og:title" content="{html.escape(plain, quote=True)}">
<meta property="og:description" content="{html.escape(pdesc, quote=True)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#0C1A2E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/styles.css?v=19271c0c">
{schema}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""

def header(d=0, in_industries=False):
    r = "../" * d
    # Practice pages are siblings of each other, so they link with no prefix at
    # all. Everything else needs the full path. This used to be inferred from
    # d == 1, which was fine until roles/ and locations/ arrived at depth 1 and
    # were not siblings — that inference broke 56 links at once. Pass it.
    ind = "" if in_industries else f"{r}industries/"
    items = (f'<a href="{r}industries.html"><strong>All practice areas</strong>'
             f'<span>The eight industries we recruit for</span></a>'
             + "".join(
        f'<a href="{ind}{slug}.html"><strong>{name}</strong><span>{sub}</span></a>'
        for slug, name, sub in VERTICALS))
    drawer = (f'<a href="{r}industries.html">All practice areas</a>'
              + "".join(
        f'<a href="{ind}{slug}.html">{name}</a>' for slug, name, _ in VERTICALS))
    return f"""<div class="util">
  <div class="wrap">
    <span class="util-tag">Executive search &middot; Recruiting nationwide</span>
    <span class="util-right">
      <a class="quiet" href="{r}candidates.html">Looking for a role?</a>
      <a href="tel:+17133960944">{PHONE} 713-396-0944</a>
    </span>
  </div>
</div>

<header class="hdr">
  <div class="wrap">
    <a class="brand" href="{r}index.html" aria-label="Sublime Personnel — home">
      <img src="{r}assets/logo-flat.png" alt="Sublime Personnel" width="460" height="176">
    </a>
    <nav class="nav" aria-label="Primary">
      <div class="has-menu">
        <button type="button" aria-expanded="false">Industries <svg viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="m2 4 3 3 3-3"/></svg></button>
        <div class="menu">{items}</div>
      </div>
      <a href="{r}clients.html">For Employers</a>
      <a href="{r}candidates.html">For Candidates</a>
      <a href="{r}jobs.html">Open Roles</a>
      <a href="{r}blog.html">Insights</a>
      <a href="{r}index.html#partners">About</a>
    </nav>
    <div class="hdr-cta">
      <a class="btn btn-blue btn-sm" href="{r}start-a-search.html">Start a search</a>
      <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="drawer"><span></span></button>
    </div>
  </div>
</header>

<div class="drawer" id="drawer">
  <div class="wrap" style="padding:0">
    <a href="{r}clients.html">For Employers</a>
    <a href="{r}candidates.html">For Candidates</a>
    <a href="{r}jobs.html">Open Roles</a>
    <a href="{r}cost-of-vacancy.html">What It Costs</a>
    <a href="{r}blog.html">Insights</a>
    <a href="{r}index.html#partners">About</a>
    <p class="grp">Industries</p>
    <div class="sub">{drawer}</div>
    <div class="btns">
      <a class="btn btn-blue" href="{r}start-a-search.html">Start a search</a>
      <a class="btn btn-out" href="tel:+17133960944">713-396-0944</a>
    </div>
  </div>
</div>
"""

def footer(d=0, in_industries=False):
    r = "../" * d
    ind_dir = "" if in_industries else f"{r}industries/"
    ind = (f'<li><a href="{r}industries.html"><b>All practice areas</b></a></li>'
           + "".join(
        f'<li><a href="{ind_dir}{slug}.html">{name}</a></li>'
        for slug, name, _ in VERTICALS))
    # Role pages are the national ranking layer — they need a crawlable link from
    # every page, not only from their own practice.
    rle = "".join(
        f'<li><a href="{r}roles/{x["slug"]}.html">{x["nav"]}</a></li>' for x in ROLES)
    return f"""<footer class="ftr">
  <div class="wrap">
    <div class="ftr-top">
      <div>
        <a class="brand" href="{r}index.html">
          <img src="{r}assets/logo-flat-light.png" alt="Sublime Personnel" width="460" height="176">
        </a>
        <p class="blurb">A boutique executive search and recruiting firm placing leadership nationwide across hospitality, property management, insurance, healthcare, accounting, construction and franchise operations since 2010.</p>
      </div>
      <div><h3 class="minor-head">Industries</h3><ul>{ind}</ul></div>
      <div><h3 class="minor-head">Roles we recruit</h3><ul>{rle}</ul></div>
      <div><h3 class="minor-head">Company</h3><ul>
        <li><a href="{r}clients.html">For Employers</a></li>
        <li><a href="{r}candidates.html">For Candidates</a></li>
        <li><a href="{r}jobs.html">Open Roles</a></li>
        <li><a href="{r}start-a-search.html">Start a Search</a></li>
        <li><a href="{r}cost-of-vacancy.html">What It Costs</a></li>
        <li><a href="{r}blog.html">Insights</a></li>
        <li><a href="{r}index.html#partners">About</a></li>
        <li><a href="{r}locations/houston.html">Houston</a></li>
      </ul></div>
      <div><h3 class="minor-head">Contact</h3><ul>
        <li><a href="tel:+17133960944">713-396-0944</a></li>
        <li><a href="mailto:pete@sublimepersonnel.com">pete@sublimepersonnel.com</a></li>
        <li><a href="mailto:terry@sublimepersonnel.com">terry@sublimepersonnel.com</a></li>
        <li>Recruiting nationwide<br>Every search run by a partner</li>
      </ul></div>
    </div>
    <div class="ftr-bot">
      <p>&copy; <span data-year>2026</span> Sublime Personnel LLC. All rights reserved.</p>
      <ul><li><a href="{r}sitemap.xml">Sitemap</a></li></ul>
    </div>
  </div>
</footer>

<div class="callbar">
  <a href="tel:+17133960944">Call 713-396-0944</a>
  <a href="{r}start-a-search.html">Start a search</a>
</div>

<script src="{r}assets/main.js?v=b0564b64" defer></script>
<script src="{r}assets/funnel.js?v=3658b600" defer></script>
</body>
</html>
"""


def faq_block(items, heading):
    rows = "".join(
        f'''<details{" open" if n == 0 else ""}>
          <summary>{q}</summary>
          <div class="ans"><p>{a}</p></div>
        </details>''' for n, (q, a) in enumerate(items))
    return f'''<section class="sec">
  <div class="wrap">
    <div class="split-hd">
      <div><p class="eyebrow rv">FAQ</p><h2 class="rv">{heading}</h2></div>
      <div class="faq rv">{rows}</div>
    </div>
  </div>
</section>
'''

def cta_band(heading="Let us discuss the role.", d=0,
             body="Twenty minutes on the phone and you will have a clear view of what the search involves, what it will cost, and how long it should take."):
    r = "../" * d
    return f'''<section class="sec cta">
  <div class="wrap">
    <p class="eyebrow center rv">Next step</p>
    <h2 class="rv">{heading}</h2>
    <p class="lede mx-auto rv" style="margin-top:22px;color:rgba(255,255,255,.68)">{body}</p>
    <div class="btns center rv" style="margin-top:36px">
      <a class="btn btn-green" href="{r}start-a-search.html">Begin a search {ARROW}</a>
      <a class="btn btn-out" href="{r}cost-of-vacancy.html">What is this seat costing you?</a>
    </div>
  </div>
</section>
'''

def write(path, body):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(body)
    print("  wrote", path, f"({len(body)//1024} KB)")


# ============================================================ SCHEMA + CLUSTERS
def esc_json(t):
    """Strip the HTML entities and tags our copy carries so JSON-LD stays valid."""
    import re, html
    return html.unescape(re.sub(r"<[^>]+>", "", t)).replace("\u2011", "-").replace('"', "'")

def faq_schema(items):
    """FAQPage JSON-LD. The FAQ blocks are already question-shaped, so this is the
    cheapest real AEO win on the site — it is what answer engines read when deciding
    whether to quote a page."""
    qs = ",".join(
        '{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
        % (esc_json(q), esc_json(a)) for q, a in items)
    return ('<script type="application/ld+json">'
            '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}</script>\n' % qs)

def service_schema(name, desc, area="United States"):
    return ('<script type="application/ld+json">'
            '{"@context":"https://schema.org","@type":"Service",'
            '"serviceType":"%s","provider":{"@type":"EmploymentAgency","name":"Sublime Personnel",'
            '"telephone":"+1-713-396-0944","areaServed":"%s"},"description":"%s"}</script>\n'
            % (esc_json(name), area, esc_json(desc)))

def posts_for(slug, limit=3):
    """Articles for one practice: practice-specific first, then the universal ones.
    Today every published post is universal — none of their ten is vertical-specific —
    so the clusters start general and tighten as per-practice content is written."""
    specific = [p for p in POSTS if slug in p[6]]
    universal = [p for p in POSTS if not p[6]]
    if universal:
        off = (IND_NUM.get(slug, "01") and int(IND_NUM[slug]) - 1) * limit
        universal = [universal[(off + k) % len(universal)] for k in range(len(universal))]
    return (specific + universal)[:limit]

def post_cards(posts, d=0):
    r = "../" * d
    return "".join(
        f'<article class="post rv"><a class="post-link" href="{LIVE}{p[4]}" target="_blank" rel="noopener">'
        f'<div class="post-meta"><time datetime="{p[0]}">{p[1]}</time><span class="tag">{p[2]}</span></div>'
        f'<h3>{p[3]}</h3><p>{p[5]}</p>'
        f'<span class="tlink">Read {ARROW}</span></a></article>' for p in posts)

def cluster_block(slug, nav, d=1):
    """Hub and spoke: the practice page is the pillar, its articles are the spokes,
    linked both ways. One Insights section, eight authority surfaces — rather than
    eight thin blogs or a blog page that merely links out."""
    r = "../" * d
    cards = post_cards(posts_for(slug), d)
    if not cards:
        return ""
    return f'''<section class="sec">
  <div class="wrap">
    <div class="split-hd" style="margin-bottom:40px">
      <div><p class="eyebrow rv">Reading</p><h2 class="rv">Written for people<br>hiring in {nav}.</h2></div>
      <div><p class="lede rv">Where a vacancy actually costs you money, how fee structures differ, and what the market is paying now. <a class="tlink" href="{r}blog.html" style="margin-top:14px">All insights {ARROW}</a></p></div>
    </div>
    <div class="post-grid rv">{cards}</div>
  </div>
</section>

'''

def gallery_block(slug, related, d=1):
    """A static three-up, deliberately below the primary CTA so it cannot compete
    with it. Not a carousel: most visitors never advance past slide one, it costs
    page weight, and on a phone it pushes the call to action off screen.
    Swap the `photo` values for the client's own images when they arrive."""
    r = "../" * d
    import industries as _I
    by = {i["slug"]: i for i in _I.INDUSTRIES}
    picks = [slug] + [o for o, _ in related]
    cells = "".join(
        f'<a class="gal-cell rv" href="{r}industries/{sg}.html">'
        f'<div class="shot"><img src="{r}assets/img/{by[sg]["photo"].replace(".jpg", "-card.jpg")}" alt="" '
        f'width="760" height="320" loading="lazy" decoding="async"></div>'
        f'<span class="gal-cap">{by[sg]["nav"]}</span></a>' for sg in picks if sg in by)
    return f'''<section class="sec-tight gal-sec">
  <div class="wrap">
    <div class="gallery">{cells}</div>
  </div>
</section>

'''

# ============================================================ 1. START A SEARCH
def build_intake():
    tiles = "".join(
        f'<label class="choice"><input type="radio" name="industry" value="{name.replace("&amp;","and")}"><span>{name}<small>{sub}</small></span></label>'
        for _, name, sub in VERTICALS
    ) + '<label class="choice"><input type="radio" name="industry" value="Something else"><span>Something else<small>Describe it and we will tell you candidly whether we can fill it</small></span></label>'

    body = head("Start a Search | Sublime Personnel",
                "Tell us the role you are hiring for. Four short questions, and Pete or Terry come back within one business day on whether we can fill it and what it costs.",
                path="start-a-search.html")
    body += header()
    body += f"""
<main id="main">
<section class="phead">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><i>/</i>Start a Search</nav>
    <p class="eyebrow center">For employers</p>
    <h1 class="phead-display">Start a <span class="fill">Search</span></h1>
    <p class="lede">Four questions, about ninety seconds. A partner will then call you back with a clear view of whether we can fill the role, what it will cost, and how long it should take.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="split" style="align-items:start;gap:clamp(32px,5vw,64px)">

      <div class="wizard" data-wizard>
        <div class="wiz-bar"><i></i></div>
        <div class="wiz-inner">
          <div class="wiz-meta">
            <span data-count>Step 1 of 4</span>
            <span class="save">Your progress is saved</span>
          </div>
          <form novalidate>

            <div class="step-panel" data-advance>
              <h2>What is the role?</h2>
              <p class="sub">Select the closest practice. If the role sits between two, choose either &mdash; most engagements cross a line.</p>
              <div class="field" data-required="industry">
                <div class="choices">{tiles}</div>
                <p class="err">Pick one to continue.</p>
              </div>
            </div>

            <div class="step-panel" hidden>
              <h2>The brief, and the timing.</h2>
              <p class="sub">A title and a band is enough. If the figure is not settled, give us the range you could defend internally.</p>
              <div class="field" data-required="role">
                <label for="role">Role title <span class="req">*</span></label>
                <input id="role" name="role" type="text" placeholder="e.g. Portfolio Manager, high-rise">
                <p class="err">Please add a title.</p>
              </div>
              <div class="field-row">
                <div class="field">
                  <label for="comp">Compensation band</label>
                  <input id="comp" name="comp" type="text" placeholder="e.g. $95k&ndash;$115k + bonus">
                </div>
                <div class="field">
                  <label for="when">Need them by</label>
                  <select id="when" name="when">
                    <option value="">Select&hellip;</option>
                    <option>Yesterday</option>
                    <option>Within 30 days</option>
                    <option>Within 90 days</option>
                    <option>Planning ahead</option>
                  </select>
                </div>
              </div>
              <div class="field">
                <label for="location">Location</label>
                <input id="location" name="location" type="text" placeholder="City, state &mdash; or remote">
              </div>
            </div>

            <div class="step-panel" hidden>
              <h2>How often do you hire at this level?</h2>
              <p class="sub">This determines your rate. A continuing relationship is not priced like a single engagement &mdash; and if we are not the right firm for your volume, we would rather establish that now.</p>
              <div class="field" data-required="volume">
                <div class="choices one">
                  <label class="choice"><input type="radio" name="volume" value="1"><span>A single engagement<small>One role to fill at present</small></span></label>
                  <label class="choice"><input type="radio" name="volume" value="2-3"><span>Two or three a year<small>Occasional, typically replacements</small></span></label>
                  <label class="choice"><input type="radio" name="volume" value="4-6"><span>Four to six a year<small>Where our rate structure begins to work in your favour</small></span></label>
                  <label class="choice"><input type="radio" name="volume" value="7+"><span>Seven or more a year<small>Growth, a new market, or building a bench</small></span></label>
                </div>
                <p class="err">Pick one to continue.</p>
              </div>
              <div class="field">
                <label for="notes">Anything else we should know</label>
                <textarea id="notes" name="notes" placeholder="Why the seat is open, what went wrong last time, what a great hire looks like."></textarea>
              </div>
            </div>

            <div class="step-panel" hidden>
              <h2>Where can we reach you?</h2>
              <p class="sub">You will hear back within one business day. Nothing you send is shared outside the two partners.</p>
              <div class="field-row">
                <div class="field" data-required="name">
                  <label for="name">Your name <span class="req">*</span></label>
                  <input id="name" name="name" type="text" autocomplete="name">
                  <p class="err">Please add your name.</p>
                </div>
                <div class="field" data-required="company">
                  <label for="company">Company <span class="req">*</span></label>
                  <input id="company" name="company" type="text" autocomplete="organization">
                  <p class="err">Please add your company.</p>
                </div>
              </div>
              <div class="field-row">
                <div class="field" data-required="email">
                  <label for="email">Work email <span class="req">*</span></label>
                  <input id="email" name="email" type="email" autocomplete="email">
                  <p class="err">Please check the email address.</p>
                </div>
                <div class="field">
                  <label for="phone">Phone</label>
                  <input id="phone" name="phone" type="tel" autocomplete="tel">
                  <p class="hint">The quickest route to a direct answer.</p>
                </div>
              </div>
            </div>

            <div class="hp" aria-hidden="true"><label for="cw">Leave blank</label><input id="cw" name="company_website" type="text" tabindex="-1" autocomplete="off"></div>

            <div class="wiz-nav">
              <button class="back" type="button" hidden>&larr; Back</button>
              <button class="btn btn-blue" type="submit" data-next><span>Continue</span> {ARROW}</button>
            </div>
          </form>
        </div>

        <div class="wiz-done" hidden>
          <div class="tick">{CHECK}</div>
          <h2>Received, <span data-name>thank you</span>.</h2>
          <p class="lede mx-auto" style="margin-top:12px">A partner will come back to you within one business day. If the matter is urgent, call directly &mdash; you will reach Pete or Terry, not a queue.</p>
          <div class="btns center" style="margin-top:30px">
            <a class="btn btn-green" href="tel:+17133960944">Call 713-396-0944 {ARROW}</a>
            <a class="btn btn-out" href="cost-of-vacancy.html">What an open seat costs</a>
          </div>
        </div>
      </div>

      <div>
        <p class="eyebrow">What happens next</p>
        <h2 style="margin-bottom:26px">What happens after you send this.</h2>
        <ul class="trust">
          <li>{CLOCK}<div><strong>A reply within one business day</strong>From a partner, not an auto-responder and not a coordinator.</div></li>
          <li>{USER}<div><strong>You deal with a principal</strong>The person who takes your brief is the person who runs the search.</div></li>
          <li>{SHIELD}<div><strong>A candid assessment</strong>If we cannot fill the role well, or the compensation will not clear the market, you hear it on the first call.</div></li>
          <li>{LOCK}<div><strong>Handled in confidence</strong>What you tell us stays between you and the two partners. Confidential searches are routine.</div></li>
        </ul>
        <div class="callout" style="margin-top:30px">
          <h3 class="minor-head">Prefer to speak first?</h3>
          <p>Many of our engagements begin with a twenty-minute conversation rather than a form. <a class="tlink" style="display:inline-flex;margin-top:8px" href="tel:+17133960944">Call 713-396-0944 {ARROW}</a></p>
        </div>
      </div>

    </div>
  </div>
</section>
</main>
"""
    body += footer()
    write("start-a-search.html", body)

# ============================================================ 2. CALCULATOR
# The national head terms nobody in this field answers. Every competitor page we
# looked at — Blue Castle, Horizon, GSI, Executive Property Staffing — states a
# guarantee in the abstract and no fee at all, so the query "what do recruiters
# charge" is answered today by recruiting-SaaS blogs and job boards rather than by
# any recruiting firm. Sublime publishes the actual numbers, which is the one
# differentiator a competitor will not copy: publishing a price costs them their
# negotiating position. These answers must stay numerically identical to the tiers
# in assets/funnel.js and in llms.txt.
FEE_FAQ = [
 ("What do recruiters charge?",
  "Most contingency recruiters charge 15–30% of the hire's first-year compensation, and retained executive search typically runs 25–33% with a minimum. Our own band is 15–25%, published rather than withheld until a sales call, and the percentage you pay is tied to the length of the replacement guarantee you want."),
 ("What is a placement fee?",
  "A one-time fee paid by the hiring company when a candidate you hire starts. It is calculated as a percentage of that candidate's first-year compensation, so a 20% fee on a $120,000 role is $24,000. Candidates never pay anything, at any stage."),
 ("What is a replacement guarantee?",
  "A contractual window during which, if the placement leaves, the firm runs the search again at no further fee. Ours is tied to the fee tier: 60 days at 15%, 90 days at 20%, 120 days at 25%. The tier is written into your contract rather than negotiated after something goes wrong."),
 ("Why would I pay more for a longer guarantee?",
  "Because the risk moves with it. A new hire is most likely to fail between day 60 and day 90 — a 120-day guarantee carries them through onboarding, the first quarter and the first time they are genuinely under pressure. If you want the lower fee we will write the shorter guarantee; we would simply rather you chose it knowingly."),
 ("How long should a search take?",
  "Our first slate reaches you in under 10 days from the briefing: three candidates with written assessment, then a tighter four once you have given feedback. Time to offer after that depends far more on your interview process than on ours."),
 ("Do you charge a retainer or an upfront fee?",
  "Mostly no — our work is contingency, so the fee is due when someone starts. We use retained or engaged arrangements for confidential and executive searches where the work has to happen quietly and thoroughly, and we will tell you which structure fits the role rather than which one pays us best."),
 ("Is a recruiting fee worth it?",
  "That depends on what the seat is costing you empty, which is what the calculator on this page works out. A role paying $120,000 that drives revenue typically costs more per day open than the fee amortised across the year — the calculator shows you the day on which the vacancy has cost you more than the placement would have."),
]

def build_calc():
    body = head("What Does a Recruiter Cost? Fees, Guarantees &amp; Vacancy Calculator",
                "Our recruiting fees in full: 15% with a 60-day guarantee, 20% with 90 days, 25% with 120 days. Plus a calculator for what an empty seat costs you per day. No email required.",
                schema=faq_schema(FEE_FAQ), path="cost-of-vacancy.html")
    body += header()
    body += f"""
<main id="main">
<section class="phead">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><i>/</i>What It Costs</nav>
    <p class="eyebrow center">Cost of vacancy</p>
    <h1 class="phead-display">What an open seat <span class="fill">costs you</span></h1>
    <p class="lede">Most firms will not discuss fees until you are several conversations in. We would rather you had the figures now. Adjust the inputs below &mdash; no email required.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="calc" data-calc>

      <div class="calc-in">
      <div class="calc-field">
          <label class="flabel" for="jobtitle">What is the role</label>
          <input id="jobtitle" class="titlein" type="text" list="commonroles" autocomplete="off"
                 placeholder="Director of Operations" value="">
          <datalist id="commonroles">
            <option value="Chief Executive Officer"><option value="Chief Financial Officer">
            <option value="Chief Operating Officer"><option value="Vice President of Operations">
            <option value="Regional Vice President"><option value="Director of Operations">
            <option value="General Manager"><option value="Multi-Unit / District Manager">
            <option value="Controller"><option value="Portfolio / Community Manager">
            <option value="Commercial Lines Producer"><option value="Project Executive">
            <option value="Project Manager"><option value="Superintendent">
            <option value="Director of Nursing"><option value="Drilling Engineer">
          </datalist>
          <p class="hint">Optional. It sharpens the comparables if you ask us for the figures.</p>
        </div>

        <div class="calc-field">
          <div class="rangewrap">
            <label class="flabel" for="salary">Annual salary for the role</label>
            <span class="rangeval" data-out="salary">$110,000</span>
          </div>
          <input id="salary" type="range" min="45000" max="300000" step="5000" value="110000">
          <div class="ticks"><span>$45k</span><span>$300k</span></div>
        </div>

        <div class="calc-field">
          <div class="rangewrap">
            <label class="flabel" for="daysopen">How long has it been open</label>
            <span class="rangeval" data-out="days">45 days</span>
          </div>
          <input id="daysopen" type="range" min="0" max="180" step="5" value="45">
          <div class="ticks"><span>Today</span><span>6 months</span></div>
        </div>

        <div class="calc-field">
          <div class="rangewrap">
            <label class="flabel" for="hires">Roles at this level per year</label>
            <span class="rangeval" data-out="hires">4 hires / year</span>
          </div>
          <input id="hires" type="range" min="1" max="12" step="1" value="4">
          <div class="ticks"><span>1</span><span>12</span></div>
        </div>

        <div class="calc-field">
          <div class="rangewrap">
            <label class="flabel" for="multiplier">Value of the role against its salary</label>
            <span class="rangeval" data-out="mult">1.0&times;</span>
          </div>
          <input id="multiplier" type="range" min="0.5" max="3" step="0.1" value="1">
          <div class="ticks"><span>0.5&times;</span><span>3&times;</span></div>
          <p class="hint">The default of 1.0&times; assumes the role generates exactly what it is paid &mdash; deliberately conservative. For a producer or revenue role, increase it.</p>
        </div>

        <div class="calc-field tier-field">
          <span class="flabel" id="tierlab">Fee and replacement guarantee</span>
          <div class="tiers" role="radiogroup" aria-labelledby="tierlab">
            <label class="tier"><input type="radio" name="tier" value="0"><span><b>15%</b><i>60&#8209;day guarantee</i></span></label>
            <label class="tier"><input type="radio" name="tier" value="1" checked><span><b>20%</b><i>90&#8209;day guarantee</i></span></label>
            <label class="tier"><input type="radio" name="tier" value="2"><span><b>25%</b><i>120&#8209;day guarantee</i></span></label>
          </div>
          <p class="hint">Where you land in our fee band is your choice, not ours. A lower fee carries a shorter guarantee on the placement; a higher one carries longer cover. Most clients sit at 20%.</p>
        </div>
      </div>

      <div class="calc-out on-dark">
        <h2 class="eyebrow">Running total</h2>
        <div class="bignum" data-out="vacancy">$19,038</div>
        <p style="margin-top:10px">is what this vacancy has cost so far.</p>

        <div style="margin-top:32px">
          <div class="calc-row"><span>Your cost every day it stays open</span><b data-out="daily">$423</b></div>
          <div class="calc-row lost"><span>Lost revenue this quarter</span><b data-out="quarter">$38,077</b></div>
          <div class="calc-row"><span data-out="feelabel">Our fee at 20% &middot; 90&#8209;day guarantee</span><b data-out="fee">$22,000</b></div>
          <div class="calc-row"><span>Days of vacancy that equal the fee</span><b data-out="breakeven">52 days</b></div>
        </div>

        <div class="verdict" data-out="verdict"></div>

        <form class="calc-capture" data-simple="vacancy_snapshot" data-calc-context novalidate>
          <div class="field" data-required="email">
            <label for="snapemail">Send this to yourself</label>
            <div class="inline-in">
              <input id="snapemail" name="email" type="email" autocomplete="email" placeholder="Work email">
              <button class="btn btn-green" type="submit">Send</button>
            </div>
            <p class="err">Please check the email address.</p>
          </div>
          <div class="hp" aria-hidden="true"><label for="snapw">Leave blank</label><input id="snapw" name="company_website" type="text" tabindex="-1" autocomplete="off"></div>
          <p class="form-note hint">Your figures, plus the compensation range we are currently seeing for this role. One email &mdash; no sequence.</p>
          <div class="form-ok" hidden><h3>On its way.</h3><p>Check your inbox shortly.</p></div>
        </form>

        <div class="btns" style="margin-top:30px">
          <a class="btn btn-green" href="start-a-search.html">Begin the search {ARROW}</a>
          <a class="btn btn-out" href="tel:+17133960944">Call 713-396-0944</a>
        </div>

        <details class="assump">
          <summary>How we calculate this</summary>
          <p>Daily cost = (salary &times; multiplier) &divide; 260 working days. Cost so far = daily cost &times; days open. Lost revenue this quarter = daily cost &times; 90 days. Our fee is 15%, 20% or 25% of first&#8209;year compensation depending on the replacement guarantee you want behind the placement.</p>
          <p>This is a planning estimate, not a quote. It deliberately ignores overtime, the cost of the work not getting done, and manager time spent covering &mdash; so if anything it reads low. It also ignores the largest compounding risk: an open seat absorbed by one person who then leaves as well, which costs you the training already invested, a second search, and the team&rsquo;s rhythm on top. Your actual fee is agreed in writing before any search begins.</p>
        </details>
      </div>

    </div>
  </div>
</section>

<section class="sec tint">
  <div class="wrap">
    <div class="split" style="align-items:start;gap:clamp(32px,5vw,64px)">
      <div>
        <p class="eyebrow">Why we publish this</p>
        <h2>Why we publish our fees.</h2>
        <p class="lede" style="margin-top:22px">Look at the largest hospitality, insurance and construction recruiters. Not one publishes a fee. You are expected to sit through a sales conversation before anyone will name a figure.</p>
        <p style="margin-top:16px">We take the opposite view. Tell us what you are able to invest in hiring across a year and we will tell you whether we can work within it. Sometimes the answer is no &mdash; which is a five-minute conversation rather than a wasted quarter.</p>

        <table class="feetable">
          <caption class="hint">Sublime Personnel direct-hire fees, as written into your contract.</caption>
          <thead>
            <tr><th scope="col">Fee</th><th scope="col">Replacement guarantee</th><th scope="col">When it fits</th></tr>
          </thead>
          <tbody>
            <tr><th scope="row">15%</th><td>60 days</td><td>You need the lower fee and will carry the shorter cover.</td></tr>
            <tr><th scope="row">20%</th><td>90 days</td><td>Standard. Where most clients sit.</td></tr>
            <tr><th scope="row">25%</th><td>120 days</td><td>Premium search. Cover through onboarding and the first quarter.</td></tr>
          </tbody>
        </table>
        <p class="hint" style="margin-top:14px">Percentage of the candidate&rsquo;s first&#8209;year compensation, agreed in writing before a search begins. Candidates are never charged, at any stage.</p>
      </div>
      <div>
        <form class="form-card" data-simple="vacancy_report" data-calc-context novalidate style="background:#fff;border:1px solid var(--line);padding:clamp(26px,3.4vw,40px)">
          <p class="eyebrow">Take it with you</p>
          <h3 style="margin-bottom:12px">Send me these figures</h3>
          <p style="font-size:.94rem;margin-bottom:24px">We will send the figures you have built, together with the compensation range we are currently seeing for this role in your market.</p>
          <div class="field" data-required="email">
            <label for="cemail">Work email <span class="req">*</span></label>
            <input id="cemail" name="email" type="email" autocomplete="email">
            <p class="err">Please check the email address.</p>
          </div>
          <div class="field">
            <label for="cname">Name</label>
            <input id="cname" name="name" type="text" autocomplete="name">
          </div>
          <div class="hp" aria-hidden="true"><label for="cw2">Leave blank</label><input id="cw2" name="company_website" type="text" tabindex="-1" autocomplete="off"></div>
          <button class="btn btn-blue" type="submit" style="width:100%">Send the figures</button>
          <p class="form-note hint" style="margin-top:14px">One email with the figures. No sequence and no newsletter &mdash; we follow up only if you ask.</p>
          <div class="form-ok" hidden>
            <h3>On its way.</h3>
            <p>It will reach your inbox shortly. If the matter is urgent, call 713-396-0944 and you will reach a partner directly.</p>
          </div>
        </form>
      </div>
    </div>
  </div>
</section>

{faq_block(FEE_FAQ, "Recruiting fees, answered.")}
</main>
"""
    body += footer()
    write("cost-of-vacancy.html", body)

# ============================================================ 3. TALENT NETWORK
def build_talent():
    opts = "".join(f"<option>{name.replace('&amp;','&')}</option>" for _, name, _ in VERTICALS) + "<option>Something else</option>"
    body = head("Join the Talent Network | Sublime Personnel",
                "A confidential conversation with an executive recruiter who runs the search personally. Free for candidates, always. Your r&eacute;sum&eacute; never reaches a company without your approval.",
                path="talent-network.html")
    body += header()
    body += f"""
<main id="main">
<section class="phead">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><i>/</i>Talent Network</nav>
    <p class="eyebrow center">For candidates</p>
    <h1 class="phead-display"><span class="fill">Represented</span>, not listed</h1>
    <p class="lede">Our board carries only the roles a client has cleared for posting; most of what we fill never reaches it, and we never post r&eacute;sum&eacute;s. Tell us what would make a move worthwhile, and when something genuine appears in your field you will hear about it before it is advertised &mdash; if it is advertised at all.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="split" style="align-items:start;gap:clamp(32px,5vw,64px)">

      <form class="wizard" data-simple="talent_network" novalidate style="padding:clamp(28px,4vw,48px)">
        <p class="eyebrow">Confidential</p>
        <h2 style="margin-bottom:10px">Start a conversation</h2>
        <p class="sub" style="font-size:.96rem;margin-bottom:28px">Two minutes. Nothing leaves this office without your approval, company by company.</p>

        <div class="field-row">
          <div class="field" data-required="name">
            <label for="tname">Your name <span class="req">*</span></label>
            <input id="tname" name="name" type="text" autocomplete="name">
            <p class="err">Please add your name.</p>
          </div>
          <div class="field" data-required="email">
            <label for="temail">Email <span class="req">*</span></label>
            <input id="temail" name="email" type="email" autocomplete="email">
            <p class="err">Please check the email address.</p>
          </div>
        </div>
        <div class="field-row">
          <div class="field">
            <label for="tphone">Phone</label>
            <input id="tphone" name="phone" type="tel" autocomplete="tel">
          </div>
          <div class="field">
            <label for="ttitle">Current title</label>
            <input id="ttitle" name="current_title" type="text" autocomplete="organization-title">
          </div>
        </div>
        <div class="field-row">
          <div class="field">
            <label for="tfield">Your field</label>
            <select id="tfield" name="field"><option value="">Select&hellip;</option>{opts}</select>
          </div>
          <div class="field">
            <label for="tloc">Where you are &mdash; and would you move?</label>
            <input id="tloc" name="location" type="text" placeholder="City, state &mdash; or open to relocate">
          </div>
        </div>
        <div class="field">
          <label for="tcomp">What would make a move worth it?</label>
          <input id="tcomp" name="comp" type="text" placeholder="Target compensation, or what's missing where you are">
        </div>
        <div class="field">
          <label for="tlink">LinkedIn or r&eacute;sum&eacute; link</label>
          <input id="tlink" name="profile_url" type="url" placeholder="https://linkedin.com/in/&hellip;">
          <p class="hint">Prefer to send a file? Email it to <a href="mailto:pete@sublimepersonnel.com" style="color:var(--blue);font-weight:600">pete@sublimepersonnel.com</a>.</p>
        </div>
        <div class="hp" aria-hidden="true"><label for="cw3">Leave blank</label><input id="cw3" name="company_website" type="text" tabindex="-1" autocomplete="off"></div>
        <button class="btn btn-blue" type="submit" style="width:100%">Send in confidence</button>
        <p class="form-note hint" style="margin-top:14px">Candidates are never charged, at any stage.</p>

        <div class="form-ok" hidden>
          <h3>Received, and held in confidence.</h3>
          <p>A partner will read this personally and be in touch within a business day. If we have nothing suitable at present we will say so plainly, and keep you in mind.</p>
        </div>
      </form>

      <div>
        <p class="eyebrow">How this works</p>
        <h2 style="margin-bottom:26px">How we work with candidates.</h2>
        <ul class="trust">
          <li>{LOCK}<div><strong>Nothing moves without your approval</strong>You are told the company, the compensation, the manager and the reservations. Only then, and only if you agree, does anything proceed.</div></li>
          <li>{CHECK}<div><strong>There is no cost to you</strong>The hiring company pays our fee. If a recruiter asks you for money, walk away.</div></li>
          <li>{USER}<div><strong>Proper preparation</strong>Who is in the room, why the role is open, what went wrong previously, and what this manager genuinely values.</div></li>
          <li>{SHIELD}<div><strong>We will advise against a move</strong>If it is wrong for you we say so, even where it costs us the fee. It is the reason people return to us.</div></li>
        </ul>
        <div class="callout" style="margin-top:30px">
          <h3 class="minor-head">Not currently looking?</h3>
          <p>Most of the people we place were not. A twenty-minute conversation costs nothing and means that when the right role appears, you hear about it first.</p>
        </div>
      </div>

    </div>
  </div>
</section>
</main>
"""
    body += footer()
    write("talent-network.html", body)


# ============================================================ 4. FOR EMPLOYERS
def build_clients():
    body = head("Executive Search for Employers | Nationwide | Sublime Personnel",
                "How we run a search: a proper briefing, a mapped market, a short assessed slate, fees agreed in writing, and a replacement guarantee of 60, 90 or 120 days on every direct hire, tied to the fee tier you choose.",
                schema=faq_schema(CLIENT_FAQ), path="clients.html")
    body += header()
    body += f"""
<main id="main">
<section class="phead">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><i>/</i>For Employers</nav>
    <p class="eyebrow center">For employers</p>
    <h1 class="phead-display">Executive search, <span class="fill">run by a partner</span></h1>
    <p class="lede">You are not short of r&eacute;sum&eacute;s. You are short of the judgement to know which three are worth your time &mdash; and the hours to find them while the seat sits empty.</p>
    <div class="btns center">
      <a class="btn btn-blue" href="start-a-search.html">Begin a search {ARROW}</a>
    </div>
    <a class="alt-path" href="cost-of-vacancy.html">First, <b>see what the open seat is costing you</b> {ARROW}</a>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="split-hd" style="margin-bottom:48px">
      <div><p class="eyebrow rv">Engagements</p><h2 class="rv">Three ways<br>to work with us.</h2></div>
      <div><p class="lede rv">Most of our work is direct hire. Forcing every requirement into one model is how firms end up selling you the wrong thing, so we will tell you which of these your situation actually calls for.</p></div>
    </div>
    <div class="grid g3">
      <div class="card rv"><h3 class="minor-head">Direct hire</h3><p>Permanent placement, contingency or retained. A percentage of first-year compensation &mdash; 15% to 25% &mdash; and every placement carries a replacement guarantee of 60, 90 or 120 days, tied to the tier you choose and set in your contract.</p></div>
      <div class="card rv"><h3 class="minor-head">Temp&#8209;to&#8209;hire</h3><p>Bring someone in on our payroll, see the work, convert when you are certain. Useful for accounting and back-office roles where fit is hard to read in an interview.</p></div>
      <div class="card rv"><h3 class="minor-head">Interim &amp; temporary</h3><p>Cover for a leave, a close, a build-out, or the gap between leaders &mdash; including interim controllers and fractional finance leadership.</p></div>
    </div>
  </div>
</section>

<section class="sec tint">
  <div class="wrap">
    <p class="eyebrow rv">The process</p>
    <h2 class="rv" style="max-width:18ch">What actually happens after you call.</h2>
    <div class="steps" style="margin-top:46px">
      <div class="step rv"><div class="step-n">01</div><div><h3>The briefing &mdash; about forty minutes</h3><p>What the role genuinely requires, who it reports to, the compensation you can defend, the interview process and who owns it, and what has gone wrong in this seat before. If the role as written cannot be filled at that number, you hear it on this call and we will tell you what would need to change.</p></div></div>
      <div class="step rv"><div class="step-n">02</div><div><h3>The market map &mdash; days one to five</h3><p>We identify who holds this role across comparable organisations, who is credentialed, and who is quietly open. Then we approach them personally. The strongest people in our practices are not applying to anything; they are employed, busy, and take the call because they know one of us.</p></div></div>
      <div class="step rv"><div class="step-n">03</div><div><h3>The slate &mdash; in under 10 days</h3><p>Three to five candidates with written assessment of each: the fit, the risk, the motivation, and what it will take to close them. No volume submissions. If the market produced only two genuine candidates, you receive two and an explanation.</p></div></div>
      <div class="step rv"><div class="step-n">04</div><div><h3>Interviews and offer</h3><p>We coordinate scheduling, debrief both sides after each round, and hold candidates engaged through the slow weeks. At offer we manage the compensation conversation and pre-empt the counter-offer &mdash; a candidate surprised by one is a candidate you lose.</p></div></div>
      <div class="step rv"><div class="step-n">05</div><div><h3>Thirty days on</h3><p>We check in with both parties at week one and week four. If it is not working the guarantee applies and we return to the market. If it is working, we ask who else you need.</p></div></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="split">
      <div>
        <p class="eyebrow rv">Fit</p>
        <h2 class="rv">We are not the right firm for everyone.</h2>
        <p class="lede rv" style="margin-top:22px">Establishing this early saves both parties a quarter.</p>
        <div class="callout rv" style="margin-top:28px">
          <h3 class="minor-head">A good fit</h3>
          <p>An organisation hiring several professional or leadership roles a year, with a real onboarding programme, that can move a candidate from first interview to offer inside three weeks.</p>
        </div>
        <div class="callout rv" style="margin-top:18px;border-left-color:var(--muted)">
          <h3 class="minor-head">A poor fit</h3>
          <p>High-volume hourly hiring, no structure to retain the person once placed, or a compensation band well under market with no flexibility. In those cases the placement does not hold, and we would rather say so at the briefing.</p>
        </div>
      </div>
      <div class="grid" style="gap:20px">
        <div class="card rv"><div class="icn">{SEARCH}</div><h3 class="minor-head">We screen on the work</h3><p>Each practice page sets out exactly what we ask candidates in that field. It is the clearest picture of how we assess &mdash; read the one that matches your role.</p><a class="tlink" style="margin-top:auto;padding-top:22px" href="index.html#industries">See the practices {ARROW}</a></div>
        <div class="card rv"><div class="icn">{LOCK}</div><h3 class="minor-head">Confidential searches</h3><p>Replacing someone who still holds the seat is delicate. We run those quietly and never approach a candidate through a channel their employer can see.</p></div>
        <div class="card rv"><div class="icn">{SHIELD}</div><h3 class="minor-head">A guarantee you choose</h3><p>Every direct hire carries a replacement guarantee, and its length is tied to the fee tier you choose: 60 days at 15%, 90 days at 20%, 120 days at 25%. The tier is set in your contract. Should the placement leave inside that window, we run the search again at no further fee.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="sec dark">
  <div class="wrap">
    <div class="split">
      <div>
        <p class="eyebrow rv">Fees</p>
        <h2 class="rv">We will tell you the number on the first call.</h2>
        <p class="lede rv" style="margin-top:22px;color:rgba(255,255,255,.7)">A percentage of first-year compensation, structured to the level of the role and the volume of work, agreed in writing before the search begins. Most firms in this market will not name a figure until you are several conversations in.</p>
        <div class="btns rv" style="margin-top:30px">
          <a class="btn btn-green" href="cost-of-vacancy.html">Work out the numbers {ARROW}</a>
          <a class="btn btn-out" href="start-a-search.html">Begin a search</a>
        </div>
      </div>
      <div class="grid" style="gap:20px">
        <div class="card rv"><h3 class="minor-head">Agreed before we begin</h3><p>In writing, at the briefing. The number is never a surprise at offer stage.</p></div>
        <div class="card rv"><h3 class="minor-head">Structured to the role</h3><p>A continuing relationship is not priced like a single engagement.</p></div>
      </div>
    </div>
  </div>
</section>

{faq_block(CLIENT_FAQ, "Employer questions.")}
{cta_band()}
</main>
"""
    body += footer()
    write("clients.html", body)

CLIENT_FAQ = [
 ("What does a placement cost?",
  "A percentage of the candidate's first-year compensation, agreed in writing before the search begins. Our band is 15–25%, and where you land inside it is your choice: a lower fee carries a shorter replacement guarantee, a higher one carries longer cover. Most clients sit at 20% with a 90-day guarantee. We would rather have that conversation on the first call than at offer stage."),
 ("Are you retained or contingency?",
  "Mostly contingency, with retained or engaged arrangements for confidential and executive searches where the work has to happen quietly and thoroughly. We recommend the structure that fits the role, not the one that pays us best."),
 ("How many candidates will I see?",
  "Three to five, with written assessment of each. If only two genuinely qualify, you receive two and an explanation of why the market is thin. Padding a slate wastes your interview time and ours."),
 ("What do you need from us to start?",
  "Roughly an hour: a proper briefing, the compensation band you can defend, and one named decision maker who can move candidates through the process. Searches stall on scheduling far more often than on sourcing."),
 ("What is the guarantee?",
  "Every direct hire carries a replacement guarantee, and its length is tied to the fee tier you choose: 60 days at 15%, 90 days at 20%, 120 days at 25%. The tier is set in your contract. Should the placement leave inside that window, we run the search again at no further fee. We have written about why replacement guarantees matter <a href=\"https://sublimepersonnel.com/blog/f/how-replacement-guarantees-reduce-hiring-risk-for-texas-employers\" target=\"_blank\" rel=\"noopener\">here</a>."),
 ("Will you sign our NDA or vendor agreement?",
  "Yes. Send it across with the role and we will turn it around quickly."),
]

# ============================================================ 5. FOR CANDIDATES
CAND_FAQ = [
 ("Does it cost me anything?",
  "No, at any stage. Our fees are paid entirely by the hiring company. If a recruiter asks you for money, walk away."),
 ("Will my employer find out I am talking to you?",
  "Not from us. Your résumé is never sent anywhere without your approval of that specific company, and we do not approach you through channels your employer can see. For insurance producers and senior operators, discretion is the entire engagement."),
 ("What if I am not actively looking?",
  "Most of the people we place were not. A twenty-minute conversation costs nothing and means that when the right role appears you hear about it first, rather than reading about it once it is filled."),
 ("Where do you place people?",
  "Nationwide. We run searches across the United States and place wherever our clients operate — our HOA and property management work alone spans ten states. Relocation is settled early rather than discovered at offer stage."),
 ("How will you prepare me for an interview?",
  "You get the real context before you walk in: who you are meeting, why the role is open, what went wrong previously, what the organisation is genuinely paying, and the two or three things this manager values most."),
 ("What happens to my information?",
  "It stays with the two partners. We do not sell, publish or post candidate data, and we do not add you to a mailing list you did not ask for."),
]

def build_candidates():
    fields = "".join(
        (f'<li><a class="tlink" href="industries/{slug}.html">' if slug != "#" else '<li><a class="tlink" href="#">')
        + name + f" {ARROW}</a></li>" for slug, name, _ in VERTICALS)
    body = head("For Candidates | Confidential Career Conversations | Sublime",
                "Confidential representation for professionals in hospitality, property management, insurance, healthcare, accounting and construction. Never a cost to you.",
                schema=faq_schema(CAND_FAQ), path="candidates.html")
    body += header()
    body += f"""
<main id="main">
<section class="phead">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><i>/</i>For Candidates</nav>
    <p class="eyebrow center">For candidates</p>
    <h1 class="phead-display">Recruiters who <span class="fill">represent you</span>, not list you</h1>
    <p class="lede">We do not run a job board and we do not circulate r&eacute;sum&eacute;s. Your name reaches a company only after you have approved that company &mdash; and you are told the reservations as well as the pitch.</p>
    <div class="btns center">
      <a class="btn btn-blue" href="talent-network.html">Speak with us in confidence {ARROW}</a>
    </div>
    <a class="alt-path" href="clients.html">Hiring instead? <b>See how we run a search</b> {ARROW}</a>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="split">
      <div>
        <p class="eyebrow rv">What is different</p>
        <h2 class="rv">The posting never tells you the part that matters.</h2>
        <p class="lede rv" style="margin-top:22px">Why the role is open. What happened to the last person. Whether the owner genuinely lets a controller close the books, or whether the board removes a manager every second year.</p>
        <p class="rv" style="margin-top:16px">We know because we have worked in these industries, and because we speak to the hiring manager rather than an inbox. You get that context before your first interview &mdash; along with an honest view on whether you should take the meeting at all.</p>
      </div>
      <div class="grid" style="gap:20px">
        <div class="card rv"><div class="icn">{LOCK}</div><h3 class="minor-head">Confidential by default</h3><p>Particularly for insurance producers and senior operators. Nothing moves without your approval, company by company.</p></div>
        <div class="card rv"><div class="icn">{CHECK}</div><h3 class="minor-head">No cost to you</h3><p>The hiring company pays our fee. Candidates are never charged, at any stage.</p></div>
        <div class="card rv"><div class="icn">{USER}</div><h3 class="minor-head">A principal reads it</h3><p>Not a coordinator and not a keyword filter. Pete or Terry reads what you send and replies personally.</p></div>
        <!-- Pete's own candidate-facing site. The only outbound link on the site,
             and it sits on the candidate path deliberately: it helps someone
             preparing for a move, and it keeps every employer page exit-free. -->
        <div class="card rv"><div class="icn">{SEARCH}</div><h3 class="minor-head">Check your r&eacute;sum&eacute; first</h3><p>Pete runs a free ATS r&eacute;sum&eacute; review at Influence of Your 7 &mdash; it shows you how an applicant tracking system reads your r&eacute;sum&eacute; before a person ever sees it.</p><a class="tlink" style="margin-top:auto;padding-top:22px" href="https://influenceofyour7.com" target="_blank" rel="noopener">Run the review {ARROW}</a></div>
      </div>
    </div>
  </div>
</section>

<section class="sec tint">
  <div class="wrap">
    <p class="eyebrow rv">How it works</p>
    <h2 class="rv" style="max-width:18ch">Four stages, and you can stop at any of them.</h2>
    <div class="steps" style="margin-top:46px">
      <div class="step rv"><div class="step-n">01</div><div><h3>A real conversation</h3><p>Twenty minutes on where you are, what you actually want next, what you are paid now and what would make a move worthwhile. No pitch. If we have nothing suitable today we will say so and keep you in mind.</p></div></div>
      <div class="step rv"><div class="step-n">02</div><div><h3>You approve every introduction</h3><p>When a role fits we tell you the company, the compensation, the manager and the reservations. Only after you agree to that specific company does your name leave this office.</p></div></div>
      <div class="step rv"><div class="step-n">03</div><div><h3>Preparation worth having</h3><p>Who is in the room, what they are worried about, what the last person got wrong, and the questions you should ask that will make you the obvious choice.</p></div></div>
      <div class="step rv"><div class="step-n">04</div><div><h3>Offer, counter-offer and after</h3><p>We negotiate on your behalf and prepare you for the counter-offer your employer will make. We then check in at week one and week four, because a placement that does not hold helps nobody.</p></div></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="split-hd" style="margin-bottom:40px">
      <div><p class="eyebrow rv">Where we place people</p><h2 class="rv">Find your field.</h2></div>
      <div><p class="lede rv">Each page sets out the roles we fill and exactly what a hiring manager in that field will be assessing you on.</p></div>
    </div>
    <ul class="grid g2 rv" style="gap:16px 44px">{fields}</ul>
  </div>
</section>

<section class="sec dark">
  <div class="wrap">
    <div class="pull mx-auto center rv">
      <p class="eyebrow center">Our commitment</p>
      <blockquote>&ldquo;If the move is wrong for you we will say so, even where it costs us the fee. It is the reason people come back to us a second time.&rdquo;</blockquote>
      <cite>Sublime Personnel</cite>
    </div>
  </div>
</section>

{faq_block(CAND_FAQ, "Candidate questions.")}

<section class="sec cta">
  <div class="wrap">
    <p class="eyebrow center rv">Next step</p>
    <h2 class="rv">Send it in confidence.</h2>
    <p class="lede mx-auto rv" style="margin-top:22px;color:rgba(255,255,255,.68)">A partner will read it personally and be in touch within a business day. Nothing moves without your approval.</p>
    <div class="btns center rv" style="margin-top:36px">
      <a class="btn btn-green" href="talent-network.html">Join the talent network {ARROW}</a>
      <a class="btn btn-out" href="tel:+17133960944">Call 713-396-0944</a>
    </div>
  </div>
</section>
</main>
"""
    body += footer()
    write("candidates.html", body)

# ============================================================ 6. INSIGHTS (BLOG)
# Real posts, scraped from sublimepersonnel.com/blog on 2026-08-24.
# See _build/blog-posts.md. Excerpts are the client's own copy, trimmed.
LIVE = "https://sublimepersonnel.com/blog/f/"
POSTS = [
 ("2026-08-21", "August 21, 2026", "Hiring strategy",
  "10 Reasons Texas Organizations Choose Sublime Personnel",
  "10-reasons-texas-organizations-choose-sublime-personnel",
  "A series exploring why Texas organizations across HOA and community management, hospitality, insurance, accounting and construction choose Sublime Personnel as their recruiting partner.",
  ()),
 ("2026-08-18", "August 18, 2026", "Hiring strategy",
  "Why Choose Sublime Personnel as Your Texas Recruiting Partner",
  "why-choose-sublime-personnel-as-your-texas-recruiting-partner",
  "Nine specific, practical reasons Texas organizations choose us: targeted candidates, real industry expertise, faster placements, culture fit and reduced hiring risk.",
  ()),
 ("2026-08-13", "August 13, 2026", "Market data",
  "Texas Hiring Market Trends: What Employers Need to Know Right Now",
  "texas-hiring-market-trends-what-employers-need-to-know-right-now",
  "Hiring decisions made without current market context tend to cost more in the long run &mdash; through offers that miss the market, or searches that drag because expectations are out of date.",
  ()),
 ("2026-08-11", "August 11, 2026", "Fees",
  "Contingent, Retained, or Hourly? A Guide to Recruiting Pricing",
  "contingent-retained-or-hourly-a-guide-to-recruiting-pricing",
  "A single leadership hire, a confidential executive search and ongoing volume hiring each call for a different kind of engagement &mdash; and a different fee structure.",
  ()),
 ("2026-08-06", "August 6, 2026", "Working with us",
  "Why a Dedicated Recruiting Partner Beats Call-Center Staffing",
  "why-a-dedicated-recruiting-partner-beats-call-center-staffing",
  "When you hire a recruiting firm you are trusting someone to represent your organization in the marketplace. That is a different relationship to submitting a request and hoping the right r&eacute;sum&eacute; arrives.",
  ()),
 ("2026-08-04", "August 4, 2026", "Track record",
  "Sublime Personnel's Track Record: 187 Hires in 22 Months",
  "sublime-personnels-track-record-187-hires-in-22-months",
  "Most agencies talk about their process. Fewer share their numbers. For employers evaluating a recruiting partner, results rather than promises are the better measure.",
  ()),
 ("2026-07-30", "July 30, 2026", "Hiring risk",
  "How Replacement Guarantees Reduce Hiring Risk for Texas Employers",
  "how-replacement-guarantees-reduce-hiring-risk-for-texas-employers",
  "Every hiring decision carries risk. However thorough the interview process, nobody can predict every challenge that surfaces after someone joins a team.",
  ()),
 ("2026-07-28", "July 28, 2026", "Assessment",
  "Why the Most Qualified Candidate Isn't Always the Best Hire",
  "why-the-most-qualified-candidate-isnt-always-the-best-hire",
  "A r&eacute;sum&eacute; shows what someone has done. An interview shows what they know. Neither reliably predicts how a person will lead, collaborate or adapt over the next three years.",
  ()),
 ("2026-07-23", "July 23, 2026", "Cost of vacancy",
  "The Real Cost of a Vacant Position, and How to Reduce It",
  "real-cost-of-a-vacant-position-and-how-tx-employers-can-reduce-it",
  "An open position does not sit quietly on an org chart. It shows up in overtime, in customer service delays, and in the stress absorbed by everyone covering the gap.",
  ()),
 ("2026-07-18", "July 2026", "Practice areas",
  "Why Industry-Specific Recruiting Expertise Matters",
  "why-industry-specific-recruiting-expertise-matters-for-tx-hiring",
  "A recruiter who has not worked inside your industry is assessing candidates against a job description. One who has is assessing them against the job.",
  ()),
]

def build_blog():
    lead = POSTS[0]
    rest = POSTS[1:]
    cards = "".join(f"""      <article class="post rv">
        <a class="post-link" href="{LIVE}{slug}" target="_blank" rel="noopener">
          <div class="post-meta"><time datetime="{iso}">{shown}</time><span class="tag">{tag}</span></div>
          <h3>{title}</h3>
          <p>{excerpt}</p>
          <span class="tlink">Read {ARROW}</span>
        </a>
      </article>""" for iso, shown, tag, title, slug, excerpt, _pr in rest)

    prac_links = "".join(
        f'<a href="industries/{slug}.html">{name}</a>' for slug, name, _ in VERTICALS)
    body = head("Insights | Hiring Intelligence for Employers | Sublime",
                "Hiring intelligence for employers: market trends, the real cost of a vacant seat, fee structures, guarantees and how to assess beyond the résumé.",
                path="blog.html")
    body += header()
    body += f"""
<main id="main">
<section class="phead">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><i>/</i>Insights</nav>
    <p class="eyebrow center">Insights</p>
    <h1 class="phead-display">Hiring intelligence for <span class="fill">employers</span></h1>
    <p class="lede">What a vacancy actually costs. How fee structures differ and when each one is right. What the market is paying now. Written by the partners who run the searches.</p>
  </div>
</section>

<section class="sec-tight">
  <div class="wrap">
    <a class="lead-post rv" href="{LIVE}{lead[4]}" target="_blank" rel="noopener">
      <div class="lead-body">
        <div class="post-meta"><span class="latest">Latest</span><time datetime="{lead[0]}">{lead[1]}</time><span class="tag">{lead[2]}</span></div>
        <h2 class="lead-title">{lead[3]}</h2>
        <p>{lead[5]}</p>
        <span class="tlink">Read the article {ARROW}</span>
      </div>
      <div class="lead-mark" aria-hidden="true">
        <img src="assets/mark.svg" alt="" width="200" height="200">
      </div>
    </a>
  </div>
</section>

<section class="sec-tight">
  <div class="wrap">
    <p class="eyebrow rv" style="margin-bottom:18px">Browse by practice</p>
    <div class="prac-row rv">{prac_links}</div>
  </div>
</section>

<section class="sec" style="padding-top:clamp(30px,3vw,44px)">
  <div class="wrap">
    <div class="post-grid">
{cards}
    </div>
    <p class="rv" style="margin-top:44px;font-size:.9rem;color:var(--muted)">
      Articles open on our current site while the new one is in build.
      <a class="tlink" style="margin-left:10px" href="https://sublimepersonnel.com/blog" target="_blank" rel="noopener">See all articles {ARROW}</a>
    </p>
  </div>
</section>

<section class="sec tint">
  <div class="wrap">
    <div class="split">
      <div>
        <p class="eyebrow rv">Put it to use</p>
        <h2 class="rv">Reading about the cost of a vacancy is one thing.</h2>
        <p class="lede rv" style="margin-top:22px">Knowing what yours is costing is another. The calculator uses your own numbers &mdash; salary, days open, hires per year &mdash; and shows the figure against what a search would cost. No email required to see it.</p>
        <div class="btns rv" style="margin-top:30px">
          <a class="btn btn-blue" href="cost-of-vacancy.html">Open the calculator {ARROW}</a>
          <a class="btn btn-out" href="start-a-search.html">Begin a search</a>
        </div>
      </div>
      <div class="grid" style="gap:20px">
        <div class="card rv"><div class="icn">{DOC}</div><h3 class="minor-head">Written by the partners</h3><p>Not outsourced. Pete and Terry write from the searches they are actually running.</p></div>
        <div class="card rv"><div class="icn">{CLOCK}</div><h3 class="minor-head">Roughly weekly</h3><p>Short, practical, and aimed at the decision rather than the algorithm.</p></div>
      </div>
    </div>
  </div>
</section>

{cta_band()}
</main>
"""
    body += footer()
    write("blog.html", body)

# ============================================================ 7. PRACTICE AREAS
NAV_BY_SLUG = {slug: name for slug, name, _ in VERTICALS}
SUB_BY_SLUG = {slug: sub for slug, _, sub in VERTICALS}

def build_industry(i):
    """One practice-area page. Everything is driven off _build/industries.py, so
    the seven pages cannot drift apart in structure — only in copy."""
    slug, num = i["slug"], IND_NUM[i["slug"]]
    total = f"{len(VERTICALS):02d}"

    roles  = "".join(f"<li>{r}</li>" for r in i["roles"])
    screen = "".join(
        f'<div class="step rv"><div class="step-n">{n+1:02d}</div>'
        f'<div><h3>{t}</h3><p>{b}</p></div></div>'
        for n, (t, b) in enumerate(i["screen"]))
    why    = "".join(f'<p class="rv">{para}</p>' for para in i["why"])

    related = "".join(
        f'<a class="card rv" href="{o}.html"><span class="num">{IND_NUM[o]}</span>'
        f'<h3>{NAV_BY_SLUG[o]}</h3><p>{blurb}</p>'
        f'<span class="tlink">View practice {ARROW}</span></a>'
        for o, blurb in i["related"])
    related += ('<a class="card rv" href="../index.html#industries"><span class="num">&mdash;</span>'
                '<h3>All practice areas</h3><p>How the practices overlap, and where your role sits.</p>'
                f'<span class="tlink">View all {ARROW}</span></a>')

    schema = (faq_schema(i["faq"] + STANDARD_FAQ)
              + service_schema(f'{i["nav"]} recruiting', i["desc"]))
    body  = head(i["title"], i["desc"], d=1, schema=schema,
                 path=f'industries/{i["slug"]}.html')
    body += header(d=1, in_industries=True)
    body += f"""
<main id="main">

<section class="phead">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><i>/</i><a href="../index.html#industries">Industries</a><i>/</i>{i['nav']}</nav>
    <p class="eyebrow center">Practice area {num} of {total}</p>
    <h1 class="phead-display">{i['h1_main']} <span class="fill">{i['h1_fill']}</span></h1>
    <p class="lede">{i['lede']}</p>
    <div class="btns center">
      <a class="btn btn-blue" href="../start-a-search.html">Start a search {ARROW}</a>
    </div>
    <a class="alt-path" href="../talent-network.html">I work in this field &mdash; <b>speak with us in confidence</b> {ARROW}</a>
  </div>
</section>

<section class="band">
  <div class="shot"><img src="../assets/img/{i['photo']}" alt="" width="1800" height="620" loading="lazy" decoding="async"></div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="split-hd">
      <div><p class="eyebrow rv">Why us for this</p><h2 class="rv">{i['why_head']}</h2></div>
      <div>{why}</div>
    </div>
  </div>
</section>

<section class="sec tint">
  <div class="wrap">
    <div class="split-hd" style="margin-bottom:44px">
      <div><p class="eyebrow rv">Roles we fill</p><h2 class="rv">{i['roles_head']}</h2></div>
      <div><p class="lede rv">Management level and above &mdash; direct hire, temp&#8209;to&#8209;hire or interim. If your role is adjacent to one of these but not listed, call us; the answer is usually yes.</p></div>
    </div>
    <ul class="roles rv">{roles}</ul>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <p class="eyebrow rv">What we screen for</p>
    <h2 class="rv" style="max-width:20ch">{i['screen_head']}</h2>
    <div class="steps" style="margin-top:46px">{screen}</div>
  </div>
</section>

<section class="sec dark" id="contact">
  <div class="wrap">
    <div class="split">
      <div>
        <p class="eyebrow rv">{i['dark_eyebrow']}</p>
        <h2 class="rv">Let us discuss the role.</h2>
        <p class="lede rv" style="margin-top:22px;color:rgba(255,255,255,.7)">Forty minutes on the phone and you will know whether we can fill the role, what it will cost and how long it should take. If we are not the right firm for this one, we will say so and point you elsewhere.</p>
        <div class="btns rv" style="margin-top:32px">
          <a class="btn btn-green" href="tel:+17133960944">Call 713-396-0944 {ARROW}</a>
          <a class="btn btn-out" href="../cost-of-vacancy.html">What will it cost?</a>
        </div>
      </div>
      <div class="grid" style="gap:20px">
        <div class="card rv"><div class="icn">{CLOCK}</div><h3 class="minor-head">First slate in under 10 days</h3><p>Three to five candidates with written assessment of fit, risk and what it will take to close them.</p></div>
        <div class="card rv"><div class="icn">{SHIELD}</div><h3 class="minor-head">A guarantee you choose</h3><p>Every direct hire carries a replacement guarantee &mdash; 60, 90 or 120 days, tied to the fee tier you choose and set in your contract. Leave inside that window and we run the search again at no further fee.</p></div>
      </div>
    </div>
  </div>
</section>

{faq_block(i['faq'] + STANDARD_FAQ, "Common questions.")}
{cluster_block(slug, i['nav'])}{gallery_block(slug, i['related'])}
<section class="sec tint">
  <div class="wrap">
    <p class="eyebrow rv">Related practices</p>
    <h2 class="rv" style="margin-bottom:42px">Most clients hire across two practices.</h2>
    <div class="grid g3">{related}</div>
  </div>
</section>

{cta_band(d=1)}
</main>
"""
    body += footer(d=1, in_industries=True)
    write(f"industries/{slug}.html", body)


# ============================================================ JOB BOARD
# Sample rows. Pete asked for a board the old site promised and never delivered:
# open/close control, sanitized descriptions, search by region, salary, practice.
# These are ILLUSTRATIVE and the page says so in a banner — the prototype is on a
# public URL and a plausible-looking fake opening is a job someone would apply to.
# Replace wholesale when Pete sends real cleared roles, then set JOBS_LIVE = True.
JOBS_LIVE = False

# (title, practice-slug, city, state, salary_low, salary_high, benefits, brief)
JOBS = [
 ("Portfolio Manager, High&#8209;Rise", "hoa-property-management", "Nashville", "TN", 95, 115,
  "Health, dental, 401(k) match, vehicle allowance",
  "Mixed-use high-rise with commercial on the back of the property. Governance experience and board meeting facilitation are non-negotiable; the board interviews the shortlist."),
 ("Community Association Manager", "hoa-property-management", "Denver", "CO", 72, 88,
  "Health, dental, 401(k), mileage reimbursement",
  "Portfolio of six associations for a national management company. CMCA held or in progress."),
 ("Director of Operations", "hospitality-restaurant", "Las Vegas", "NV", 130, 160,
  "Health, dental, bonus to 20%, vehicle allowance",
  "Multi-unit group opening four locations over eighteen months. Reports to the principal; owns P&amp;L across the portfolio."),
 ("Executive Chef", "hospitality-restaurant", "Austin", "TX", 95, 120,
  "Health, dental, 401(k), quarterly bonus",
  "Chef-driven independent doing 180 covers a night. Scratch kitchen, seasonal menu, full authority over the line."),
 ("Commercial Lines Producer", "insurance", "Charlotte", "NC", 90, 140,
  "Health, dental, 401(k), uncapped commission",
  "Established agency with a book to inherit alongside new business. Property and casualty licence required."),
 ("Commercial Lines Account Manager", "insurance", "Chicago", "IL", 68, 85,
  "Health, dental, 401(k), licence sponsorship",
  "Middle-market book, roughly forty accounts. Applied Epic experience preferred."),
 ("Director of Nursing", "healthcare", "Scottsdale", "AZ", 115, 140,
  "Health, dental, 401(k), CEU allowance",
  "Multi-site outpatient group. Active RN licence and prior multi-site clinical leadership required."),
 ("Controller", "accounting-finance", "Atlanta", "GA", 125, 150,
  "Health, dental, 401(k) match, bonus",
  "Privately held company approaching $80M revenue. Month-end close, audit liaison, and a team of four. CPA preferred, not required."),
 ("Project Executive", "commercial-construction", "Houston", "TX", 160, 200,
  "Health, dental, 401(k), vehicle, bonus",
  "Ground-up commercial general contractor. Owns two to three concurrent projects in the $20&ndash;60M range."),
 ("Superintendent", "commercial-construction", "The Woodlands", "TX", 110, 135,
  "Health, dental, 401(k), truck and fuel",
  "Interior and ground-up commercial. Self-perform concrete background is an advantage."),
 ("Area Coach, Multi&#8209;Unit", "qsr-franchise", "Phoenix", "AZ", 78, 95,
  "Health, dental, 401(k), vehicle allowance, bonus",
  "Franchisee operating eleven units across two brands. Twelve to fourteen restaurant span of control."),
 ("Drilling Engineer", "oil-gas", "Midland", "TX", 145, 185,
  "Health, dental, 401(k) match, rotation schedule",
  "Permian operator, horizontal programme. Well planning through execution; some field presence expected."),
]


def build_jobs():
    prac = {slug: nav for slug, nav, _ in VERTICALS}
    states = sorted({j[3] for j in JOBS})

    rows = []
    for title, slug, city, st, lo, hi, benefits, brief in JOBS:
        band = "under100" if hi <= 100 else ("100to150" if hi <= 150 else "over150")
        rows.append(f"""      <article class="job" data-state="{st}" data-practice="{slug}" data-band="{band}">
        <div class="job-hd">
          <h3 class="minor-head">{title}</h3>
          <p class="job-pay">${lo}k &ndash; ${hi}k</p>
        </div>
        <p class="job-meta"><span>{city}, {st}</span><i>&middot;</i><a href="industries/{slug}.html">{prac[slug]}</a></p>
        <p class="job-brief">{brief}</p>
        <p class="job-ben">{benefits}</p>
        <a class="tlink" href="talent-network.html">Ask us about this role {ARROW}</a>
      </article>""")

    state_opts = "".join(f'<option value="{st}">{st}</option>' for st in states)
    prac_opts = "".join(f'<option value="{slug}">{nav}</option>' for slug, nav, _ in VERTICALS)

    banner = "" if JOBS_LIVE else """
    <div class="notice" role="status">
      <strong>Preview.</strong> Sample roles are shown here so you can see the board work &mdash;
      the filters, the counts and the enquiry route are all live. Real openings replace them
      as soon as Sublime publishes them, and nothing below is currently recruiting.
    </div>
"""

    body = head("Open Roles | Sublime Personnel",
                "Leadership and professional roles Sublime Personnel is currently recruiting across HOA, hospitality, insurance, healthcare, accounting, construction, franchise and energy. Most of our work is never advertised.",
                path="jobs.html")
    body += header()
    body += f"""
<main id="main">
<section class="phead">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><i>/</i>Open Roles</nav>
    <p class="eyebrow center">Currently recruiting</p>
    <h1 class="phead-display">The roles we can <span class="fill">talk about</span></h1>
    <p class="lede">Most of what we fill is confidential and never reaches a board. These are the searches our clients have cleared for posting. If none of them is yours, speak to us anyway &mdash; the right role usually arrives before it is advertised.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap">{banner}
    <h2 class="sec-head">Currently open</h2>
    <div class="job-filters" data-jobs>
      <div class="jf">
        <label for="f-state">Location</label>
        <select id="f-state" data-filter="state"><option value="">Any state</option>{state_opts}</select>
      </div>
      <div class="jf">
        <label for="f-practice">Practice</label>
        <select id="f-practice" data-filter="practice"><option value="">All practices</option>{prac_opts}</select>
      </div>
      <div class="jf">
        <label for="f-band">Salary</label>
        <select id="f-band" data-filter="band">
          <option value="">Any salary</option>
          <option value="under100">Up to $100k</option>
          <option value="100to150">$100k &ndash; $150k</option>
          <option value="over150">$150k and above</option>
        </select>
      </div>
      <p class="jf-count"><b data-jobs-count>{len(JOBS)}</b> <span data-jobs-noun>roles</span> shown</p>
    </div>

    <div class="jobs" data-jobs-list>
{chr(10).join(rows)}
    </div>

    <p class="jobs-empty" data-jobs-empty hidden>Nothing open under those filters at the moment. Most of our searches never reach this page &mdash; <a href="talent-network.html">tell us what you are looking for</a> and we will come to you when it appears.</p>
  </div>
</section>

{cta_band("Not seeing your role?",
          body="The strongest opportunities we run are confidential. A twenty-minute conversation puts you in front of them before they are advertised, and it costs you nothing.")}
</main>
"""
    body += footer()
    write("jobs.html", body)


def build_llms():
    """llms.txt — a plain-text brief for AI crawlers.

    Two jobs. It states the facts a model needs to answer a question about
    Sublime correctly (practices, fees, guarantee, geography, contact), and it
    carries the HOA glossary that Pete did not want as a page for humans. Models
    will happily read a wall of definitions; visitors will not.
    """
    def clean(t):
        return re.sub(r"<[^>]+>", "", html.unescape(t)).replace("\u2011", "-")

    L = []
    L.append("# Sublime Personnel")
    L.append("")
    L.append("> Boutique executive search and recruiting firm, founded 2010, placing leadership "
             "and professional talent nationwide across the United States. Every search is run "
             "personally by one of the two partners.")
    L.append("")
    L.append("Contact: Pete Proctor, Vice President of Operations - pete@sublimepersonnel.com - 713-396-0944")
    L.append("Terry Stevenson, Partner - terry@sublimepersonnel.com")
    L.append("")

    L.append("## How the firm works")
    L.append("")
    L.append("- Fees are a percentage of first-year compensation and are published rather than "
             "withheld until a sales call. The band is 15% to 25%.")
    L.append("- The fee is tied to the replacement guarantee: 15% carries a 60-day guarantee, "
             "20% carries 90 days, 25% carries 120 days. The tier is set in the client's contract. "
             "If a placement leaves inside the window the search is run again at no further fee.")
    L.append("- The first slate reaches a client in under 10 days from the briefing: three "
             "candidates, then a tighter four after feedback. Three to five candidates with a "
             "written assessment of fit, risk, motivation and what it will take to close them.")
    L.append("- Engagement types: direct hire (contingency or retained), temp-to-hire, and "
             "interim or temporary placement.")
    L.append("- Candidates are never charged, at any stage. A resume is never sent to a company "
             "without the candidate's approval of that specific company.")
    L.append("- Client names are not published. Candidates who learn a client's identity go "
             "direct, so confidentiality is a condition of the work rather than a preference.")
    L.append("- Searches are run nationwide across the United States. The firm's HOA and "
             "property management practice alone covers ten states. Its deepest regional "
             "network is the Gulf Coast, which is where the industrial, subsea and ROV "
             "technical roles come from.")
    L.append("")

    L.append("## Practices")
    L.append("")
    for i in INDUSTRIES:
        L.append(f"- [{clean(i['nav'])}](industries/{i['slug']}.html): {clean(i['desc'])}")
    L.append("")

    L.append("## Pages")
    L.append("")
    for path, title, desc in [
        ("index.html", "Home", "The firm, the practices, the partners."),
        ("clients.html", "For Employers", "How a search is run, engagement types, fees and guarantee."),
        ("candidates.html", "For Candidates", "How candidates are represented, and what it costs them (nothing)."),
        ("jobs.html", "Open Roles", "Roles cleared for posting. Most searches are confidential and never appear here."),
        ("cost-of-vacancy.html", "What It Costs", "A calculator for the cost of an open seat, and the published fee and guarantee tiers."),
        ("start-a-search.html", "Start a Search", "Employer intake."),
        ("talent-network.html", "Talent Network", "Confidential candidate intake."),
        ("blog.html", "Insights", "Hiring intelligence: market trends, fee structures, guarantees, assessment."),
        ("industries.html", "Industries", "Hub page for all eight practice areas."),
        ("locations/houston.html", "Houston", "The firm's home market and its Gulf Coast and Permian network. The firm recruits nationwide; this page covers the local practice only."),
    ]:
        L.append(f"- [{title}]({path}): {desc}")
    L.append("")

    L.append("## Roles")
    L.append("")
    L.append("One page per role, covering what the role owns, how the firm screens "
             "for it, and the compensation range currently seen nationally.")
    L.append("")
    for x in ROLES:
        lo, hi = x["salary"]
        L.append(f"- [{clean(x['nav'])}](roles/{x['slug']}.html): {clean(x['desc'])} "
                 f"Range currently seen: ${lo},000-${hi},000.")
    L.append("")

    L.append("## HOA and community association management glossary")
    L.append("")
    L.append("Sublime Personnel's deepest practice is HOA and property management recruiting. "
             "These are the firm's own published definitions of the terms used in that field.")
    L.append("")
    for term, definition in GLOSSARY:
        L.append(f"- **{term}**: {definition}")
    L.append("")

    L.append("## Recruiting terms")
    L.append("")
    for term, definition in RECRUITING_TERMS:
        L.append(f"- **{term}**: {definition}")
    L.append("")

    write("llms.txt", "\n".join(L) + "\n")



# ============================================================ 9. INDUSTRIES HUB
def build_industries_hub():
    """The crawlable pillar the site never had.

    Before this, the practice pages' "All practice areas" card pointed at
    index.html#industries — a fragment, which cannot rank, cannot be linked to and
    cannot appear in a sitemap. With the site targeting vertical+role terms rather
    than a city, the hub is the page that collects that internal link equity."""
    cards = "".join(
        f'<a class="card rv" href="industries/{slug}.html">'
        f'<span class="num">{IND_NUM[slug]}</span><h3>{name}</h3>'
        f'<p>{sub}</p><span class="tlink">View practice {ARROW}</span></a>'
        for slug, name, sub in VERTICALS)

    rows = "".join(
        f'''<div class="hub-row rv">
          <div><p class="eyebrow">{IND_NUM[i["slug"]]}</p>
            <h3 class="minor-head"><a class="tlink" href="industries/{i["slug"]}.html">{i["nav"]} {ARROW}</a></h3></div>
          <div><p>{i["lede"]}</p>
            <p class="hint" style="margin-top:12px"><b>Roles we place:</b> {", ".join(r.replace("&#8209;", "-") for r in i["roles"][:6])}.</p></div>
        </div>''' for i in INDUSTRIES)

    body = head("Recruiting by Industry | 8 Practice Areas | Sublime Personnel",
                "The eight industries Sublime Personnel recruits for nationwide &mdash; HOA and property management, hospitality, insurance, healthcare, accounting, construction, franchise and energy. Each practice is led by a partner with operating experience in it.",
                schema=service_schema("Executive search and recruiting",
                                      "Executive search and professional recruiting across eight industry practices, placed nationwide across the United States."),
                path="industries.html")
    body += header()
    body += f"""
<main id="main">
<section class="phead">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><i>/</i>Industries</nav>
    <p class="eyebrow center">Practice areas</p>
    <h1 class="phead-display">Eight industries, <span class="fill">recruited nationwide</span></h1>
    <p class="lede">We do not recruit for everything. We recruit for eight industries our partners have actually worked inside &mdash; and we say so plainly when a role sits outside them.</p>
    <div class="btns center"><a class="btn btn-green" href="start-a-search.html">Start a search {ARROW}</a></div>
    <a class="alt-path" href="cost-of-vacancy.html">Not sure yet? <b>See what the seat is costing you</b> {ARROW}</a>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="split-hd" style="margin-bottom:44px">
      <div><p class="eyebrow rv">The practices</p><h2 class="rv">Where we<br>actually work.</h2></div>
      <div><p class="lede rv">Each practice is led by a partner with direct operating experience in it &mdash; thirty years of restaurant operations, an insurance desk since 2006, two years recruiting inside a high&#8209;rise property management firm.</p></div>
    </div>
    <div class="grid g3">{cards}</div>
  </div>
</section>

<section class="sec tint">
  <div class="wrap">
    <div class="split-hd" style="margin-bottom:44px">
      <div><p class="eyebrow rv">In detail</p><h2 class="rv">What each<br>practice covers.</h2></div>
      <div><p class="lede rv">Every practice page carries the roles we place, how we screen for them, and the questions employers in that industry actually ask.</p></div>
    </div>
    <div class="hub-rows">{rows}</div>
  </div>
</section>
{cta_band()}
</main>
"""
    body += footer()
    write("industries.html", body)


# ============================================================ 10. SITEMAP + ROBOTS
# Derived from the same lists everything else reads, so a new practice or role page
# cannot be missing from the sitemap. README's standing warning applies: three
# hardcoded copies of the practice list have drifted here already — never type a
# fourth.
def site_urls():
    urls = [("", "1.0"), ("clients.html", "0.9"), ("industries.html", "0.9"),
            ("cost-of-vacancy.html", "0.9"), ("start-a-search.html", "0.8"),
            ("candidates.html", "0.7"), ("jobs.html", "0.7"),
            ("talent-network.html", "0.6"), ("blog.html", "0.6"),
            ("locations/houston.html", "0.6")]
    urls += [(f'industries/{i["slug"]}.html', "0.8") for i in INDUSTRIES]
    urls += [(f'roles/{r["slug"]}.html', "0.7") for r in ROLES]
    return urls

def build_sitemap():
    from datetime import date
    today = date.today().isoformat()
    entries = "".join(
        f"  <url><loc>{SITE}/{path}</loc><lastmod>{today}</lastmod>"
        f"<priority>{pri}</priority></url>\n" for path, pri in site_urls())
    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          f"{entries}</urlset>\n")

def build_robots():
    write("robots.txt",
          "User-agent: *\n"
          "Allow: /\n"
          "\n"
          "# Answer engines: llms.txt carries the firm's facts in full — practices,\n"
          "# published fees, guarantee tiers, and the HOA glossary.\n"
          f"Sitemap: {SITE}/sitemap.xml\n")


# ============================================================ 11. ROLE PAGES
def build_role(r):
    """One role page. See _build/roles.py for why these exist: the geographic
    modifier is gone, so the role name is what makes the page narrow enough to
    rank. Links up to its practice (the pillar) and down into the calculator."""
    prac = next(i for i in INDUSTRIES if i["slug"] == r["practice"])
    lo, hi = r["salary"]

    does = "".join(f"<li>{d}</li>" for d in r["does"])
    screen = "".join(
        f'<div class="step rv"><div class="step-n">{n+1:02d}</div>'
        f'<div><h3>{t}</h3><p>{b}</p></div></div>'
        for n, (t, b) in enumerate(r["screen"]))

    # Sibling roles, capped at three so the block reads as a suggestion rather
    # than a second nav. Rotated by position so the eight pages do not all point
    # at the same three — same reasoning as posts_for() on the practice pages.
    others = [o for o in ROLES if o["slug"] != r["slug"]]
    start = ROLES.index(r)
    picks = [others[(start + n) % len(others)] for n in range(3)]
    siblings = "".join(
        f'<a class="card rv" href="{o["slug"]}.html"><span class="num">&mdash;</span>'
        f'<h3>{o["nav"]}</h3><p>{NAV_BY_SLUG[o["practice"]]}</p>'
        f'<span class="tlink">View role {ARROW}</span></a>' for o in picks)

    schema = (faq_schema(r["faq"] + STANDARD_FAQ)
              + service_schema(f'{r["nav"]} recruiting', r["desc"]))
    body  = head(r["title"], r["desc"], d=1, schema=schema,
                 path=f'roles/{r["slug"]}.html')
    body += header(d=1)
    body += f"""
<main id="main">
<section class="phead">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><i>/</i><a href="../industries.html">Industries</a><i>/</i><a href="../industries/{prac['slug']}.html">{prac['nav']}</a><i>/</i>{r['nav']}</nav>
    <p class="eyebrow center">{prac['nav']} &middot; Recruiting nationwide</p>
    <h1 class="phead-display">{r['h1_main']} <span class="fill">{r['h1_fill']}</span></h1>
    <p class="lede">{r['lede']}</p>
    <div class="btns center"><a class="btn btn-green" href="../start-a-search.html">Start a search {ARROW}</a></div>
    <a class="alt-path" href="../cost-of-vacancy.html">First, <b>see what this seat is costing you</b> {ARROW}</a>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="split-hd">
      <div><p class="eyebrow rv">The role</p><h2 class="rv">{r['does_head']}</h2></div>
      <div><ul class="ticks-list rv">{does}</ul></div>
    </div>
  </div>
</section>

<section class="sec tint">
  <div class="wrap">
    <p class="eyebrow center rv">Our screen</p>
    <h2 class="center rv" style="margin-bottom:52px">{r['screen_head']}</h2>
    <div class="steps">{screen}</div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="split" style="align-items:start;gap:clamp(32px,5vw,64px)">
      <div>
        <p class="eyebrow">Compensation</p>
        <h2>What this role pays.</h2>
        <p class="lede" style="margin-top:22px">The range we are currently seeing nationally for this role is <b>${lo},000&ndash;${hi},000</b>. It moves with market, scope and credentials &mdash; and we will tell you plainly when the band you have set will not attract the person you have described.</p>
        <p style="margin-top:16px">Our fee against that hire is 15%, 20% or 25% of first&#8209;year compensation, and the percentage you choose sets the length of the replacement guarantee. <a class="tlink" href="../cost-of-vacancy.html" style="margin-top:14px">Work out the numbers {ARROW}</a></p>
      </div>
      <div>
        <div class="card" style="background:var(--paper-2);border:1px solid var(--line);padding:clamp(26px,3.4vw,40px)">
          <p class="eyebrow">Part of our {prac['nav']} practice</p>
          <h3 class="minor-head" style="margin-top:10px">{prac['nav']}</h3>
          <p style="margin-top:14px">{prac['lede']}</p>
          <a class="tlink" style="margin-top:20px" href="../industries/{prac['slug']}.html">View the full practice {ARROW}</a>
        </div>
      </div>
    </div>
  </div>
</section>

{faq_block(r['faq'] + STANDARD_FAQ, "Common questions.")}

<section class="sec tint">
  <div class="wrap">
    <p class="eyebrow center rv">Other roles we recruit</p>
    <h2 class="center rv" style="margin-bottom:52px">Hiring for something else?</h2>
    <div class="grid g3">{siblings}</div>
  </div>
</section>
{cta_band(d=1)}
</main>
"""
    body += footer(d=1)
    write(f'roles/{r["slug"]}.html', body)


# ============================================================ 12. HOUSTON / LOCAL
def build_houston():
    """The local cluster, contained to one page.

    The rest of the site went national, which is right for the eight practices and
    wrong for the local pack — the one surface a two-partner firm ranks on
    immediately. Rather than lose that, every Houston/Texas term is quarantined
    here, together with the only LocalBusiness node on the site. Pete's "Texas is
    a big enough market to get us running" and Terry's "not limited to Texas" are
    both true at once this way."""
    local_faq = [
      ("Are you a Houston-based recruiting firm?",
       "Yes. Sublime Personnel was founded in Houston in 2010 and both partners are here. We recruit nationwide &mdash; our HOA and property management practice alone spans ten states &mdash; but the firm is Houston-based and our deepest regional network is the Gulf Coast."),
      ("What industries do you recruit for in Houston?",
       "All eight of our practices: HOA and property management, hospitality and restaurant, insurance, healthcare, accounting and finance, commercial construction, QSR and franchise, and energy. The Gulf Coast industrial and energy work &mdash; including subsea and ROV roles &mdash; is specifically a Houston-network practice."),
      ("Do you recruit in the Permian Basin and West Texas?",
       "Yes. Midland and Odessa are an active market for us on the drilling, completions and production side, and the screen there is different from the offshore and downstream work on the coast."),
      ("How much does a Houston recruiter charge?",
       "The same as everywhere else we work, because we publish it: 15% of first-year compensation with a 60-day replacement guarantee, 20% with 90 days, or 25% with 120 days. The tier is written into your contract before the search begins."),
    ]
    schema = (faq_schema(local_faq) + '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"LocalBusiness",
 "@id":"https://sublimepersonnel.com/locations/houston.html#local",
 "parentOrganization":{"@id":"https://sublimepersonnel.com/#organization"},
 "name":"Sublime Personnel",
 "url":"https://sublimepersonnel.com/locations/houston.html",
 "telephone":"+1-713-396-0944",
 "email":"pete@sublimepersonnel.com",
 "priceRange":"15-25% of first-year compensation",
 "address":{"@type":"PostalAddress","addressLocality":"Houston","addressRegion":"TX","addressCountry":"US"},
 "areaServed":[{"@type":"City","name":"Houston"},{"@type":"State","name":"Texas"},{"@type":"Country","name":"United States"}]}
</script>
''')
    body = head("Houston Executive Recruiters &amp; Search Firm | Sublime Personnel",
                "Houston-based executive search and recruiting since 2010, placing nationwide. Fees published: 15/20/25% tied to a 60, 90 or 120-day guarantee. Both partners recruit; nobody sits between you and the work.",
                d=1, schema=schema, path="locations/houston.html")
    body += header(d=1)
    body += f"""
<main id="main">
<section class="phead">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><i>/</i>Houston</nav>
    <p class="eyebrow center">Houston, Texas &middot; Since 2010</p>
    <h1 class="phead-display">Houston executive <span class="fill">recruiters</span></h1>
    <p class="lede">Sublime Personnel was founded in Houston in 2010 and has been run the same way since: two partners, both of whom recruit, and nobody between you and the work. We place nationwide &mdash; but this is where the firm is, and where its deepest network sits.</p>
    <div class="btns center"><a class="btn btn-green" href="../start-a-search.html">Start a search {ARROW}</a>
      <a class="btn btn-out" href="tel:+17133960944">Call 713-396-0944</a></div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="split" style="align-items:start;gap:clamp(32px,5vw,64px)">
      <div>
        <p class="eyebrow">The local network</p>
        <h2>Where being here<br>actually matters.</h2>
        <p class="lede" style="margin-top:22px">For most of our practices, location is irrelevant &mdash; a controller search runs the same way in Atlanta as in Houston. For two of them it is the entire advantage.</p>
        <p style="margin-top:16px">The Gulf Coast industrial and energy network is ours because we are on it. That includes the hard&#8209;to&#8209;fill technical roles &mdash; subsea and ROV operators among them &mdash; where the candidate pool is a set of relationships rather than a job board. The same people who know which superintendent can hold a jobsite know which turnaround lead can hold a shutdown.</p>
        <p style="margin-top:16px">West Texas is the other one. Midland and Odessa are an active market for us on the drilling, completions and production side, and Permian unconventional is a different screen from deepwater work on the coast.</p>
      </div>
      <div>
        <div class="card" style="background:var(--paper-2);border:1px solid var(--line);padding:clamp(26px,3.4vw,40px)">
          <p class="eyebrow">Local, not limited</p>
          <h3 class="minor-head" style="margin-top:10px">We place nationwide</h3>
          <p style="margin-top:14px">Our HOA and property management practice alone covers ten states. Clients bring us wherever they need us, and we build networks in their markets ahead of the search rather than after it.</p>
          <a class="tlink" style="margin-top:20px" href="../industries.html">All eight practices {ARROW}</a>
        </div>
      </div>
    </div>
  </div>
</section>

{faq_block(local_faq, "Houston questions.")}
{cta_band(d=1)}
</main>
"""
    body += footer(d=1)
    write("locations/houston.html", body)


# ============================================================ entry point
if __name__ == "__main__":
    print("Building ->", ROOT)
    build_intake(); build_calc(); build_talent()
    build_clients(); build_candidates(); build_blog(); build_jobs()
    build_industries_hub(); build_houston()
    for i in INDUSTRIES:
        build_industry(i)
    for r in ROLES:
        build_role(r)
    # llms.txt and the sitemap enumerate everything above, so they go last.
    build_llms(); build_sitemap(); build_robots()
    print("Done.")
