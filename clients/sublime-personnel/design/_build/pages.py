#!/usr/bin/env python3
"""Generates every page except index.html, so header/footer never drift.
Run from design/:  python3 _build/pages.py && python3 _build/bust.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from industries import INDUSTRIES, STANDARD_FAQ
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4"/></svg>'
PHONE = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.5 11.3v2a1.3 1.3 0 0 1-1.5 1.3 13 13 0 0 1-5.7-2 12.8 12.8 0 0 1-4-4 13 13 0 0 1-2-5.8A1.3 1.3 0 0 1 2.7 1.3h2A1.3 1.3 0 0 1 6 2.5c.1.6.2 1.3.5 1.9a1.3 1.3 0 0 1-.3 1.4l-.9.8a10.7 10.7 0 0 0 4 4l.8-.8a1.3 1.3 0 0 1 1.4-.3c.6.2 1.2.4 1.9.4a1.3 1.3 0 0 1 1.1 1.4z"/></svg>'
CHECK = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m4 10.4 4 4 8-9"/></svg>'
LOCK  = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="8.6" width="12" height="8.4" rx="2"/><path d="M6.9 8.6V6.4a3.1 3.1 0 0 1 6.2 0v2.2"/></svg>'
CLOCK = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="10" cy="10" r="7.4"/><path d="M10 5.8V10l2.8 1.7"/></svg>'
SHIELD= '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 2.2 3.8 4.7v4.6c0 3.9 2.6 7.1 6.2 8.5 3.6-1.4 6.2-4.6 6.2-8.5V4.7z"/><path d="m7.6 9.9 1.8 1.8 3.3-3.5"/></svg>'
SEARCH= '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="9" r="5.6"/><path d="m13.2 13.2 3.6 3.6"/></svg>'
DOC   = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11.5 2.5H6a1.5 1.5 0 0 0-1.5 1.5v12A1.5 1.5 0 0 0 6 17.5h8a1.5 1.5 0 0 0 1.5-1.5V6.5z"/><path d="M11.5 2.5v4h4M7.5 11h5M7.5 14h3"/></svg>'
USER  = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="10" cy="6.8" r="3"/><path d="M4 16.6a6 6 0 0 1 12 0"/></svg>'

# Order is the published order: the "practice area NN of 07" numbering, the nav,
# the footer and the related-practice cards all read off this one list.
VERTICALS = [
    ("hoa-property-management",   "HOA &amp; Property Management", "Community managers, portfolio &amp; high-rise"),
    ("hospitality-restaurant",    "Hospitality &amp; Restaurant",  "GMs, multi-unit leaders, chefs, F&amp;B"),
    ("commercial-lines-insurance","Commercial Lines Insurance",    "Producers, underwriters, account managers"),
    ("personal-lines-insurance",  "Personal Lines Insurance",      "Account managers, producers, service"),
    ("accounting-finance",        "Accounting &amp; Finance",      "Controllers, CFOs, senior accountants"),
    ("commercial-construction",   "Commercial Construction",       "PMs, superintendents, estimators"),
    ("qsr-franchise",             "QSR &amp; Franchise",           "Area coaches, FBCs, multi-unit leadership"),
]
IND_NUM = {slug: f"{n+1:02d}" for n, (slug, _, _) in enumerate(VERTICALS)}

# d = directory depth below the site root, so industries/ pages get "../".
def head(title, desc, d=0):
    r = "../" * d
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#0C1A2E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/styles.css?v=94e67a65">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""

def header(d=0):
    r = "../" * d
    # practice pages are siblings at depth 1, so they take no prefix at all
    ind = f"{r}industries/" if d == 0 else ""
    items = "".join(
        f'<a href="{ind}{slug}.html"><strong>{name}</strong><span>{sub}</span></a>'
        for slug, name, sub in VERTICALS)
    drawer = "".join(
        f'<a href="{ind}{slug}.html">{name}</a>' for slug, name, _ in VERTICALS)
    return f"""<div class="util">
  <div class="wrap">
    <span class="util-tag">Greater Houston &middot; Recruiting nationwide</span>
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

def footer(d=0):
    r = "../" * d
    ind_dir = f"{r}industries/" if d == 0 else ""
    ind = "".join(
        f'<li><a href="{ind_dir}{slug}.html">{name}</a></li>'
        for slug, name, _ in VERTICALS)
    return f"""<footer class="ftr">
  <div class="wrap">
    <div class="ftr-top">
      <div>
        <a class="brand" href="{r}index.html">
          <img src="{r}assets/logo-flat-light.png" alt="Sublime Personnel" width="460" height="176">
        </a>
        <p class="blurb">A boutique executive search and recruiting firm in the Greater Houston Area, placing leadership across hospitality, property management, insurance, accounting, construction and franchise operations since 2010.</p>
      </div>
      <div><h3 class="minor-head">Industries</h3><ul>{ind}</ul></div>
      <div><h3 class="minor-head">Company</h3><ul>
        <li><a href="{r}clients.html">For Employers</a></li>
        <li><a href="{r}candidates.html">For Candidates</a></li>
        <li><a href="{r}start-a-search.html">Start a Search</a></li>
        <li><a href="{r}cost-of-vacancy.html">What It Costs</a></li>
        <li><a href="{r}blog.html">Insights</a></li>
        <li><a href="{r}index.html#partners">About</a></li>
      </ul></div>
      <div><h3 class="minor-head">Contact</h3><ul>
        <li><a href="tel:+17133960944">713-396-0944</a></li>
        <li><a href="mailto:pete@sublimepersonnel.com">pete@sublimepersonnel.com</a></li>
        <li><a href="mailto:terry@sublimepersonnel.com">terry@sublimepersonnel.com</a></li>
        <li>Greater Houston Area<br>Recruiting nationwide</li>
      </ul></div>
    </div>
    <div class="ftr-bot">
      <p>&copy; <span data-year>2026</span> Sublime Personnel LLC. All rights reserved.</p>
      <ul><li><a href="#">Privacy Policy</a></li><li><a href="#">Sitemap</a></li></ul>
    </div>
  </div>
</footer>

<div class="callbar">
  <a href="tel:+17133960944">Call 713-396-0944</a>
  <a href="{r}start-a-search.html">Start a search</a>
</div>

<script src="{r}assets/main.js?v=b0564b64" defer></script>
<script src="{r}assets/funnel.js?v=3696a58f" defer></script>
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
      <a class="btn btn-out" href="tel:+17133960944">Call 713-396-0944</a>
    </div>
  </div>
</section>
'''

def write(path, body):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(body)
    print("  wrote", path, f"({len(body)//1024} KB)")

# ============================================================ 1. START A SEARCH
def build_intake():
    tiles = "".join(
        f'<label class="choice"><input type="radio" name="industry" value="{name.replace("&amp;","and")}"><span>{name}<small>{sub}</small></span></label>'
        for _, name, sub in VERTICALS
    ) + '<label class="choice"><input type="radio" name="industry" value="Something else"><span>Something else<small>Describe it and we will tell you candidly whether we can fill it</small></span></label>'

    body = head("Start a Search | Sublime Personnel",
                "Tell us the role you are hiring for. Four short questions, and Pete or Terry come back within one business day on whether we can fill it and what it costs.")
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
def build_calc():
    body = head("What Does a Vacancy Cost? | Sublime Personnel",
                "Work out what an empty seat costs you per day and what a placement fee is against it. Adjustable inputs, transparent assumptions, no email required.")
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

        <div class="calc-field" style="margin-bottom:0">
          <div class="rangewrap">
            <label class="flabel" for="multiplier">Value of the role against its salary</label>
            <span class="rangeval" data-out="mult">1.0&times;</span>
          </div>
          <input id="multiplier" type="range" min="0.5" max="3" step="0.1" value="1">
          <div class="ticks"><span>0.5&times;</span><span>3&times;</span></div>
          <p class="hint">The default of 1.0&times; assumes the role generates exactly what it is paid &mdash; deliberately conservative. For a producer or revenue role, increase it.</p>
        </div>
      </div>

      <div class="calc-out on-dark">
        <p class="eyebrow">Running total</p>
        <div class="bignum" data-out="vacancy">$19,038</div>
        <p style="margin-top:10px">is what this vacancy has cost so far.</p>

        <div style="margin-top:32px">
          <div class="calc-row"><span>Every further day it stays open</span><b data-out="daily">$423</b></div>
          <div class="calc-row"><span>Our fee for this placement (15&ndash;20%)</span><b data-out="fee">$16,500 &ndash; $22,000</b></div>
          <div class="calc-row"><span>At this volume, annually</span><b data-out="annual">$66,000 &ndash; $88,000</b></div>
          <div class="calc-row"><span>Days of vacancy that equal the fee</span><b data-out="breakeven">52 days</b></div>
        </div>

        <div class="verdict" data-out="verdict"></div>

        <div class="btns" style="margin-top:30px">
          <a class="btn btn-green" href="start-a-search.html">Begin the search {ARROW}</a>
          <a class="btn btn-out" href="tel:+17133960944">Call 713-396-0944</a>
        </div>

        <details class="assump">
          <summary>How we calculate this</summary>
          <p>Daily cost = (salary &times; multiplier) &divide; 260 working days. Cost so far = daily cost &times; days open. Our fee range is 15&ndash;20% of first-year compensation, which is the band Pete quotes on the phone &mdash; where you land inside it depends on role level and how many searches you run a year.</p>
          <p>This is a planning estimate, not a quote. It deliberately ignores overtime, the cost of the work not getting done, and manager time spent covering &mdash; so if anything it reads low. Your actual fee is agreed in writing before any search begins.</p>
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
      </div>
      <div>
        <form class="form-card" data-simple="vacancy_report" novalidate style="background:#fff;border:1px solid var(--line);padding:clamp(26px,3.4vw,40px)">
          <p class="eyebrow">Take it with you</p>
          <h3 style="margin-bottom:12px">Send me these figures</h3>
          <p style="font-size:.94rem;margin-bottom:24px">We will send the figures you have built, together with the compensation range we are currently seeing for this role in the Houston market.</p>
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
</main>
"""
    body += footer()
    write("cost-of-vacancy.html", body)

# ============================================================ 3. TALENT NETWORK
def build_talent():
    opts = "".join(f"<option>{name.replace('&amp;','&')}</option>" for _, name, _ in VERTICALS) + "<option>Something else</option>"
    body = head("Join the Talent Network | Sublime Personnel",
                "A confidential conversation with a Houston executive recruiter. Free for candidates, always. Your r&eacute;sum&eacute; never reaches a company without your approval.")
    body += header()
    body += f"""
<main id="main">
<section class="phead">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><i>/</i>Talent Network</nav>
    <p class="eyebrow center">For candidates</p>
    <h1 class="phead-display"><span class="fill">Represented</span>, not listed</h1>
    <p class="lede">We do not run a job board and we do not post r&eacute;sum&eacute;s. Tell us what would make a move worthwhile, and when something genuine appears in your field you will hear about it before it is advertised &mdash; if it is advertised at all.</p>
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
            <input id="tloc" name="location" type="text" placeholder="Houston, open to relocate">
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
    body = head("Executive Search for Houston Employers | Sublime Personnel",
                "How we run a search: a proper briefing, a mapped market, a short assessed slate, fees agreed in writing, and a thirty-day guarantee on every direct hire.")
    body += header()
    body += f"""
<main id="main">
<section class="phead">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><i>/</i>For Employers</nav>
    <p class="eyebrow center">For employers</p>
    <h1 class="phead-display">Executive search for <span class="fill">Houston employers</span></h1>
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
      <div class="card rv"><h3 class="minor-head">Direct hire</h3><p>Permanent placement, contingency or retained. A percentage of first-year compensation, and every placement carries the thirty-day guarantee.</p></div>
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
      <div class="step rv"><div class="step-n">03</div><div><h3>The slate &mdash; typically inside two weeks</h3><p>Three to five candidates with written assessment of each: the fit, the risk, the motivation, and what it will take to close them. No volume submissions. If the market produced only two genuine candidates, you receive two and an explanation.</p></div></div>
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
        <div class="card rv"><div class="icn">{SHIELD}</div><h3 class="minor-head">Thirty-day guarantee</h3><p>Should a direct-hire placement leave within thirty days, we conduct the search again at no further fee.</p></div>
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
  "A percentage of the candidate's first-year compensation, structured to the level of the role and the volume of work, and agreed in writing before the search begins. We would rather have that conversation on the first call than at offer stage."),
 ("Are you retained or contingency?",
  "Mostly contingency, with retained or engaged arrangements for confidential and executive searches where the work has to happen quietly and thoroughly. We recommend the structure that fits the role, not the one that pays us best."),
 ("How many candidates will I see?",
  "Three to five, with written assessment of each. If only two genuinely qualify, you receive two and an explanation of why the market is thin. Padding a slate wastes your interview time and ours."),
 ("What do you need from us to start?",
  "Roughly an hour: a proper briefing, the compensation band you can defend, and one named decision maker who can move candidates through the process. Searches stall on scheduling far more often than on sourcing."),
 ("What is the guarantee?",
  "Direct-hire placements carry a thirty-day guarantee. Should the placement leave within that period, we conduct the search again at no further fee."),
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
 ("Do you have roles outside Houston?",
  "Yes. We are Houston-based and recruit nationwide, with the deepest reach across Texas and the Gulf Coast."),
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
                "Confidential representation for Houston professionals in hospitality, property management, insurance, accounting and construction. Never a cost to you.")
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
  "A series exploring why Texas organizations across HOA and community management, hospitality, insurance, accounting and construction choose Sublime Personnel as their recruiting partner."),
 ("2026-08-18", "August 18, 2026", "Hiring strategy",
  "Why Choose Sublime Personnel as Your Texas Recruiting Partner",
  "why-choose-sublime-personnel-as-your-texas-recruiting-partner",
  "Nine specific, practical reasons Texas organizations choose us: targeted candidates, real industry expertise, faster placements, culture fit and reduced hiring risk."),
 ("2026-08-13", "August 13, 2026", "Market data",
  "Texas Hiring Market Trends: What Employers Need to Know Right Now",
  "texas-hiring-market-trends-what-employers-need-to-know-right-now",
  "Hiring decisions made without current market context tend to cost more in the long run &mdash; through offers that miss the market, or searches that drag because expectations are out of date."),
 ("2026-08-11", "August 11, 2026", "Fees",
  "Contingent, Retained, or Hourly? A Guide to Recruiting Pricing",
  "contingent-retained-or-hourly-a-guide-to-recruiting-pricing",
  "A single leadership hire, a confidential executive search and ongoing volume hiring each call for a different kind of engagement &mdash; and a different fee structure."),
 ("2026-08-06", "August 6, 2026", "Working with us",
  "Why a Dedicated Recruiting Partner Beats Call-Center Staffing",
  "why-a-dedicated-recruiting-partner-beats-call-center-staffing",
  "When you hire a recruiting firm you are trusting someone to represent your organization in the marketplace. That is a different relationship to submitting a request and hoping the right r&eacute;sum&eacute; arrives."),
 ("2026-08-04", "August 4, 2026", "Track record",
  "Sublime Personnel's Track Record: 187 Hires in 22 Months",
  "sublime-personnels-track-record-187-hires-in-22-months",
  "Most agencies talk about their process. Fewer share their numbers. For employers evaluating a recruiting partner, results rather than promises are the better measure."),
 ("2026-07-30", "July 30, 2026", "Hiring risk",
  "How Replacement Guarantees Reduce Hiring Risk for Texas Employers",
  "how-replacement-guarantees-reduce-hiring-risk-for-texas-employers",
  "Every hiring decision carries risk. However thorough the interview process, nobody can predict every challenge that surfaces after someone joins a team."),
 ("2026-07-28", "July 28, 2026", "Assessment",
  "Why the Most Qualified Candidate Isn't Always the Best Hire",
  "why-the-most-qualified-candidate-isnt-always-the-best-hire",
  "A r&eacute;sum&eacute; shows what someone has done. An interview shows what they know. Neither reliably predicts how a person will lead, collaborate or adapt over the next three years."),
 ("2026-07-23", "July 23, 2026", "Cost of vacancy",
  "The Real Cost of a Vacant Position, and How to Reduce It",
  "real-cost-of-a-vacant-position-and-how-tx-employers-can-reduce-it",
  "An open position does not sit quietly on an org chart. It shows up in overtime, in customer service delays, and in the stress absorbed by everyone covering the gap."),
 ("2026-07-18", "July 2026", "Practice areas",
  "Why Industry-Specific Recruiting Expertise Matters",
  "why-industry-specific-recruiting-expertise-matters-for-tx-hiring",
  "A recruiter who has not worked inside your industry is assessing candidates against a job description. One who has is assessing them against the job."),
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
      </article>""" for iso, shown, tag, title, slug, excerpt in rest)

    body = head("Insights | Hiring Intelligence for Employers | Sublime",
                "Hiring intelligence for Texas employers: market trends, the real cost of a vacant seat, fee structures, guarantees and how to assess beyond the résumé.")
    body += header()
    body += f"""
<main id="main">
<section class="phead">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><i>/</i>Insights</nav>
    <p class="eyebrow center">Insights</p>
    <h1 class="phead-display">Hiring intelligence for <span class="fill">Texas employers</span></h1>
    <p class="lede">What a vacancy actually costs. How fee structures differ and when each one is right. What the Texas market is paying now. Written by the partners who run the searches.</p>
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

    body  = head(i["title"], i["desc"], d=1)
    body += header(d=1)
    body += f"""
<main id="main">

<section class="phead">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><i>/</i><a href="../index.html#industries">Industries</a><i>/</i>{i['nav']}</nav>
    <p class="eyebrow center">Practice area {num} of 07</p>
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
        <div class="card rv"><div class="icn">{CLOCK}</div><h3 class="minor-head">First slate in about two weeks</h3><p>Three to five candidates with written assessment of fit, risk and what it will take to close them.</p></div>
        <div class="card rv"><div class="icn">{SHIELD}</div><h3 class="minor-head">30-day guarantee</h3><p>Direct-hire placements are replaced at no further fee should they leave within thirty days.</p></div>
      </div>
    </div>
  </div>
</section>

{faq_block(i['faq'] + STANDARD_FAQ, "Common questions.")}
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
    body += footer(d=1)
    write(f"industries/{slug}.html", body)

# ============================================================ entry point
if __name__ == "__main__":
    print("Building ->", ROOT)
    build_intake(); build_calc(); build_talent()
    build_clients(); build_candidates(); build_blog()
    for i in INDUSTRIES:
        build_industry(i)
    print("Done.")
