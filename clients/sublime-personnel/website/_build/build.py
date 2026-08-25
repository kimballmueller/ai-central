#!/usr/bin/env python3
"""
Sublime Personnel — static site builder.

Emits plain HTML into the parent directory. Shared chrome (head, header,
footer, CTA band, schema) lives here so twelve pages can't drift apart.
Run:  python3 _build/build.py     (from the website root)
"""
import os, re, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE = {
    "name":    "Sublime Personnel",
    "legal":   "Sublime Personnel LLC",
    "tagline": "We Take Recruiting Personally",
    "domain":  "https://sublimepersonnel.com",
    "phone":   "713-396-0944",
    "phone_href": "+17133960944",
    "email":   "pete@sublimepersonnel.com",
    "email2":  "terry@sublimepersonnel.com",
    "city":    "Houston",
    "region":  "TX",
    "area":    "Greater Houston Area",
    "founded": "2010",
    "linkedin": "https://www.linkedin.com/company/sublime-personnel",
    # --- PASTE the booking link here (Calendly / GHL calendar) ---
    "booking": "",
}

# ---------------------------------------------------------------- icons
ICONS = {
    "arrow":  '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4"/></svg>',
    "phone":  '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.5 11.3v2a1.3 1.3 0 0 1-1.5 1.3 13 13 0 0 1-5.7-2 12.8 12.8 0 0 1-4-4 13 13 0 0 1-2-5.8A1.3 1.3 0 0 1 2.7 1.3h2a1.3 1.3 0 0 1 1.3 1.2c.1.6.2 1.3.5 1.9a1.3 1.3 0 0 1-.3 1.4l-.9.8a10.7 10.7 0 0 0 4 4l.8-.8a1.3 1.3 0 0 1 1.4-.3c.6.2 1.2.4 1.9.4a1.3 1.3 0 0 1 1.1 1.4z"/></svg>',
    "mail":   '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="16" height="12" rx="2"/><path d="m2.5 5.5 7.5 5.5 7.5-5.5"/></svg>',
    "pin":    '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16 8.3c0 4.4-6 10-6 10s-6-5.6-6-10a6 6 0 1 1 12 0z"/><circle cx="10" cy="8.2" r="2.2"/></svg>',
    "clock":  '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="10" cy="10" r="7.4"/><path d="M10 5.8V10l2.8 1.7"/></svg>',
    "search": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="9" r="5.6"/><path d="m13.2 13.2 3.6 3.6"/></svg>',
    "shield": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 2.2 3.8 4.7v4.6c0 3.9 2.6 7.1 6.2 8.5 3.6-1.4 6.2-4.6 6.2-8.5V4.7z"/><path d="m7.6 9.9 1.8 1.8 3.3-3.5"/></svg>',
    "users":  '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="7.6" cy="6.6" r="2.9"/><path d="M2.6 16.4a5 5 0 0 1 10 0"/><path d="M13.4 4a2.9 2.9 0 0 1 0 5.5M14.6 11.9a5 5 0 0 1 2.9 4.5"/></svg>',
    "chart":  '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.8 17h14.4"/><path d="M5.6 17V9.4M10 17V4.2M14.4 17v-5.4"/></svg>',
    "lock":   '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="8.6" width="12" height="8.4" rx="2"/><path d="M6.9 8.6V6.4a3.1 3.1 0 0 1 6.2 0v2.2"/></svg>',
    "handshake": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.6 7.4 6 4.6l2.6 1.8 2.8-1.8 3.9 2.8"/><path d="M6 12.4 8.2 14l1.6-1.4L11.6 14l1.8-1.6"/><path d="M2.6 7.4v4.2l3.4 3M17.4 7.4v4.2l-3.2 2.9"/></svg>',
    "linkedin": '<svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M3.2 1.6a1.6 1.6 0 1 0 0 3.2 1.6 1.6 0 0 0 0-3.2zM1.8 6h2.8v8.4H1.8zM6.5 6h2.7v1.2h.04a3 3 0 0 1 2.7-1.4c2.9 0 3.4 1.8 3.4 4.2v4.4h-2.8v-3.9c0-.9 0-2.1-1.3-2.1s-1.5 1-1.5 2v4H6.5z"/></svg>',
}

# ---------------------------------------------------------------- industries
INDUSTRIES = [
{
 "slug": "hospitality-restaurant",
 "nav":  "Hospitality &amp; Restaurant",
 "short":"Hospitality",
 "h1":   "Hospitality &amp; restaurant recruiting",
 "navdesc": "GMs, multi-unit leaders, chefs, F&amp;B directors",
 "title": "Hospitality &amp; Restaurant Recruiting | Houston &amp; Nationwide",
 "desc": "Restaurant and hospitality recruiters who ran the floor first. GM, multi-unit, executive chef, and F&B leadership searches out of Houston, placing nationwide.",
 "lede": "Thirty years of restaurant operations sit behind every hospitality search we run. We know the difference between a résumé that looks like a general manager and a person who can actually hold a building together on a Saturday night.",
 "why": [
   "Pete Proctor spent more than thirty years in restaurant operations before he ever recruited for it — walking into units in the low nineties and taking them past one-thirty. That background is the screen. When a candidate talks about how they fixed a labor line or turned a kitchen culture around, we know within a few minutes whether the story is real.",
   "Hospitality hiring fails in predictable places: a strong operator who has never run more than one unit, a chef who can cook but cannot cost, a district manager who has only ever inherited healthy stores. We ask the questions that expose those gaps before you spend three months finding out."
 ],
 "roles": ["General Manager","Multi-Unit / District Manager","Director of Operations","Executive Chef","Food &amp; Beverage Director","Regional Vice President","Catering &amp; Events Director","Hotel &amp; Resort Leadership"],
 "screen": [
   ("Unit economics, not anecdotes","We ask for the numbers they owned — food cost, labor, COGS, AUV, flow-through — and how they moved them. Operators who ran the P&L answer in seconds."),
   ("Span of control","A five-unit district and a twenty-unit district are different jobs. We map what they actually supervised, including whether they built the bench under them."),
   ("Turnover and retention","Anyone can open a store. We look at whether their teams stayed, and what they did in the first ninety days when they inherited a broken one."),
   ("Culture and hours","Hospitality burns people who did not know what they were signing up for. We are direct about schedule, travel, and expectations before the first interview.")
 ],
 "faq": [
   ("Do you recruit for independents or only large groups?","Both. Our client profile is a company that can support roughly four searches a year, which is usually a multi-unit group, a growing regional brand, or a hospitality management company — but we take strong independent operators when the role is senior enough to justify a retained-style search."),
   ("Can you fill hourly or line-level roles?","Our work is management and above. For hourly volume hiring you are better served by a staffing agency, and we will say so rather than take the engagement.")
 ],
},
{
 "slug": "hoa-property-management",
 "nav":  "HOA &amp; Property Management",
 "short":"HOA &amp; Property Mgmt",
 "h1":   "HOA &amp; property management recruiting",
 "navdesc": "Community managers, portfolio &amp; high-rise leadership",
 "title": "HOA &amp; Property Management Recruiting | Community Association Talent",
 "desc": "HOA and property management recruiters who understand governance. Community association managers, portfolio managers, high-rise GMs, and regional directors — CMCA, AMS, PCAM.",
 "lede": "In community association management, governance is everything. A manager who cannot run a board meeting, read the CC&amp;Rs, and keep a volatile board calm is a liability no matter how good the résumé reads.",
 "why": [
   "We learned this vertical from the inside — two years as a corporate recruiter for a high-rise property management firm, where the entire business turned on whether a manager could handle a board. Boards do not fire managers over spreadsheets. They fire them over meetings, minutes, and tone.",
   "So our screen goes past portfolio size. We look at how a candidate handles an owner who shows up angry, whether they have run a reserve study conversation, how they document decisions, and whether they have survived a board turnover without losing the account."
 ],
 "roles": ["Community Association Manager","Portfolio Manager","On-Site / High-Rise General Manager","Director of Community Management","Regional Director","Assistant Community Manager","Association Accounting &amp; AR Manager","Maintenance &amp; Facilities Director"],
 "screen": [
   ("Governance literacy","Can they read governing documents, run an annual meeting, and hold a quorum together? We ask for specifics from real meetings, not job descriptions."),
   ("Portfolio math","Doors, associations, and complexity are three different numbers. Twelve small HOAs and two high-rises are not the same workload, and we price the candidate accordingly."),
   ("Credentials and trajectory","CMCA, AMS, and PCAM matter to boards. We track where a candidate is in that ladder and whether their employer supported it."),
   ("Board temperament","The single biggest predictor of a manager surviving year two. We reference-check this directly with people who watched them in a room.")
 ],
 "faq": [
   ("Do you place licensed and credentialed managers?","Yes. We recruit CMCA, AMS, and PCAM holders as well as strong managers working toward those designations, and we confirm credential status before presenting anyone."),
   ("Can you support a management company opening a new market?","Yes. Market entry is one of the places we do our best work, because it needs a portfolio manager and a bench at the same time. Bring us the timeline and we will build the search around it.")
 ],
},
{
 "slug": "commercial-lines-insurance",
 "nav":  "Commercial Lines Insurance",
 "short":"Commercial Insurance",
 "h1":   "Commercial lines insurance recruiting",
 "navdesc": "Producers, account managers, underwriters, claims",
 "title": "Commercial Lines Insurance Recruiting | Producers, Underwriters, Account Managers",
 "desc": "Commercial lines insurance recruiting for agencies, brokers, and carriers. Producers with a book, account managers, underwriters, and claims professionals. CIC, CPCU, CRM.",
 "lede": "Commercial insurance is a relationship business with a technical floor. We screen for both — the book and the book of knowledge — because agencies that hire on charm alone spend the next year cleaning up the file.",
 "why": [
   "Terry Richards has recruited insurance talent since 2006 and knows the difference between a producer with a portable book and a producer with a story about one. We ask about renewal retention, carrier appointments, class concentration, and non-competes early, so nobody wastes a quarter on a hire that cannot legally bring anything with them.",
   "On the service side, the gap is usually technical. An account manager who can quote, endorse, and handle a certificate crunch in a hard market is worth two who cannot, and the résumés look identical until you ask the right five questions."
 ],
 "roles": ["Commercial Lines Producer","Commercial Lines Account Manager","Account Executive","Underwriter","Claims Adjuster / Examiner","Risk Advisor","Marketing / Placement Specialist","Agency &amp; Branch Leadership"],
 "screen": [
   ("Book, retention, and portability","Size of book, renewal retention, class mix, and — critically — what their agreement actually allows them to move."),
   ("Systems fluency","AMS360, Applied Epic, EZLynx, Sagitta. The wrong system is a real ramp cost and we flag it up front."),
   ("Designations","CIC, CPCU, CRM, ARM. We note who holds what and who is mid-track, because it tells you how they invest in themselves."),
   ("Market conditions","How they performed in a hard market says more than how they performed in a soft one. We ask about both.")
 ],
 "faq": [
   ("Do you recruit producers with a book of business?","Yes — and we handle those conversations with real discretion. Producer searches are confidential by default, and we never approach someone through a channel their current agency can see."),
   ("Do you work with carriers as well as agencies?","Yes. Retail agencies, wholesalers, MGAs, and carriers. The screen changes for each; the discipline does not.")
 ],
},
{
 "slug": "personal-lines-insurance",
 "nav":  "Personal Lines Insurance",
 "short":"Personal Insurance",
 "h1":   "Personal lines insurance recruiting",
 "navdesc": "Account managers, producers, service &amp; agency leadership",
 "title": "Personal Lines Insurance Recruiting | Account Managers &amp; Agency Staff",
 "desc": "Personal lines insurance recruiting — account managers, producers, service representatives, and agency leadership. Licensed talent screened for retention, not just volume.",
 "lede": "Personal lines lives or dies on service. A book bleeds one policy at a time when the person answering the phone is competent but cold, or warm but slow — and neither shows up on a résumé.",
 "why": [
   "We screen personal lines candidates on the two things that actually drive retention: how fast they close the loop, and how they talk to a policyholder who just got a rate increase. Both are testable in an interview if you know what to listen for.",
   "Licensing is the other place searches stall. We confirm the license, the state, the appointment status, and the CE standing before a candidate reaches your calendar, so an offer is never held up by paperwork nobody checked."
 ],
 "roles": ["Personal Lines Account Manager","Personal Lines Producer","Customer Service Representative","Claims Support Specialist","High-Net-Worth / Private Client Advisor","Agency Manager","Team Lead / Service Supervisor"],
 "screen": [
   ("License verification","State, line, standing, and CE. Confirmed before presentation, not after the offer."),
   ("Book size and mix","Number of households serviced, average premium, and whether they carried high-net-worth accounts, which is a different discipline entirely."),
   ("Retention behaviour","What they do at renewal, how they handle a rate increase call, and whether they proactively re-market."),
   ("Carrier and system exposure","Which carriers and which agency management system — the two biggest drivers of ramp time.")
 ],
 "faq": [
   ("Do you handle high-net-worth / private client roles?","Yes. Private client service is a distinct skill set — Chubb, PURE, Cincinnati experience, comfort with complex schedules — and we screen for it specifically rather than treating it as ordinary personal lines."),
   ("Can you fill a full service team, not just one seat?","Yes. Team builds are common in this vertical and usually cheaper per seat than one-off searches. Tell us the headcount and the runway.")
 ],
},
{
 "slug": "accounting-finance",
 "nav":  "Accounting &amp; Finance",
 "short":"Accounting &amp; Finance",
 "h1":   "Accounting &amp; finance recruiting",
 "navdesc": "Controllers, CFOs, staff and senior accountants",
 "title": "Accounting &amp; Finance Recruiting | Controllers, CFOs, Accountants",
 "desc": "Accounting and finance recruiting for private companies — controllers, assistant controllers, staff and senior accountants, AP/AR leadership, FP&A, and fractional CFO placements.",
 "lede": "Accounting runs through every other vertical we work in. Restaurants, HOAs, agencies, and contractors all need someone who can close the month and tell the owner the truth about the numbers.",
 "why": [
   "Because we recruit accounting inside industries we already know, we can screen for context and not just credentials. Association accounting is not restaurant accounting. Percentage-of-completion for a commercial contractor is not the same job as agency trust accounting.",
   "That context is what stops the classic bad hire: a technically sound accountant who has never worked in your industry, takes six months to get comfortable, and leaves in month nine because the work was not what they pictured."
 ],
 "roles": ["Controller","Assistant Controller","Staff &amp; Senior Accountant","Accounting Manager","AP / AR Manager","FP&amp;A Analyst","Payroll Manager","CFO &amp; Fractional CFO"],
 "screen": [
   ("Close ownership","Do they own the close or support it? How many days, how many entities, and what did they inherit?"),
   ("Industry accounting","Percentage-of-completion, association reserves, trust accounting, multi-unit consolidations — whichever applies to you."),
   ("Systems","QuickBooks, Sage Intacct, NetSuite, Yardi, Vantaca, restaurant back-office platforms. Ramp time is a system question."),
   ("Business partnership","Whether they can sit in front of an owner or a board and explain the number, or whether they can only produce it.")
 ],
 "faq": [
   ("Do you place fractional or interim finance leadership?","Yes. We handle direct hire, temp-to-hire, and interim placements, and for smaller companies an experienced fractional controller is often the right first move."),
   ("Are candidates CPA-verified?","Where CPA status is claimed, we verify licence status before presentation. We will also tell you plainly when a strong candidate is not a CPA and it does not matter for the role.")
 ],
},
{
 "slug": "commercial-construction",
 "nav":  "Commercial Construction",
 "short":"Commercial Construction",
 "h1":   "Commercial construction recruiting",
 "navdesc": "PMs, superintendents, estimators, project executives",
 "title": "Commercial Construction Recruiting | PMs, Superintendents, Estimators",
 "desc": "Commercial construction recruiting for general contractors and specialty trades — project managers, superintendents, estimators, preconstruction, safety, and project executives.",
 "lede": "Construction hiring is judged in the field, not the interview. We screen on project type, delivery method, and dollar value, because a twelve-million-dollar tilt-wall superintendent and a ninety-million-dollar healthcare superintendent are not interchangeable.",
 "why": [
   "This vertical is Terry's home ground, and Pete grew up around the trades — his father was a welder — which is why our conversations with field leaders sound like conversations rather than screenings. Superintendents can tell inside a minute whether a recruiter has ever stood on a jobsite.",
   "We also work the adjacent industrial and energy niches around Houston, including hard-to-fill technical roles like subsea and ROV operators, where the candidate pool is a network rather than a job board."
 ],
 "roles": ["Project Manager","Senior Project Manager","Superintendent","Estimator","Preconstruction Manager","Project Executive","Safety Director","MEP &amp; Specialty Trade Leadership"],
 "screen": [
   ("Project profile","Sector, square footage, dollar value, and delivery method — CM at risk, design-build, hard bid. The résumé rarely says; we always ask."),
   ("Self-perform vs. subcontract","Whether they managed their own crews or coordinated subs changes what they can do on day one."),
   ("Software","Procore, Bluebeam, Sage 300 CRE, HeavyBid, On-Screen Takeoff. Field leaders who cannot use your stack cost you a quarter."),
   ("Travel and geography","Construction candidates move for the right project. We settle relocation and per-diem expectations before the first interview, not after the offer.")
 ],
 "faq": [
   ("Do you recruit for specialty trades and industrial work?","Yes — mechanical, electrical, roofing, and industrial contractors, plus energy-adjacent technical roles through our Gulf Coast network."),
   ("Can you support a bid-driven hiring spike?","Yes. Tell us the award timeline and we will pipeline ahead of it so you are not starting a search the week the contract is signed.")
 ],
},
{
 "slug": "qsr-franchise",
 "nav":  "QSR &amp; Franchise",
 "short":"QSR &amp; Franchise",
 "h1":   "QSR &amp; franchise recruiting",
 "navdesc": "Area coaches, FBCs, multi-unit franchise leadership",
 "title": "QSR &amp; Franchise Recruiting | Multi-Unit &amp; Franchise Operations Leaders",
 "desc": "QSR and franchise recruiting — area coaches, franchise business consultants, directors of operations, and multi-unit leadership for franchisees and franchisors.",
 "lede": "Franchise operations is its own discipline. Running units you own and coaching units somebody else owns require two different personalities, and hiring the wrong one produces a year of quiet friction.",
 "why": [
   "We recruit for both sides of the franchise relationship — multi-unit franchisees building an ops bench, and franchisors staffing field support. The screen differs: franchisee leadership needs P&amp;L ownership and speed; franchisor field roles need influence without authority, which is a rarer skill.",
   "Brand-standard discipline is the other filter. Some operators thrive inside a playbook. Others quietly rewrite it, which works until the audit. We find out which one you are hiring."
 ],
 "roles": ["Area Coach / Area Supervisor","Franchise Business Consultant","Director of Operations","Multi-Unit Manager","Training &amp; Development Manager","New Store Opening Manager","Franchise Development Manager","Regional Director"],
 "screen": [
   ("Units and AUV","Number of units supervised, average unit volume, and whether growth came from new builds or from fixing existing stores."),
   ("Franchisee vs. franchisor","Which side they have operated on, and whether they can influence an owner they do not employ."),
   ("Speed and scale","New-store opening experience, remodel cycles, and how many openings they have personally led."),
   ("Brand standards","How they handle an audit, a failing store, and an owner who does not want to hear it.")
 ],
 "faq": [
   ("Do you work with franchisees or franchisors?","Both. A multi-unit franchisee building a district manager bench and a franchisor staffing field consultants are different searches, and we run them differently."),
   ("Can you support new market entry?","Yes. New market openings need leadership hired ahead of the build schedule. Give us the opening dates and we will work backwards from them.")
 ],
},
]
IND_BY_SLUG = {i["slug"]: i for i in INDUSTRIES}

# ---------------------------------------------------------------- shared FAQ
CORE_FAQ = [
 ("What industries does Sublime Personnel recruit for?",
  "Seven: hospitality and restaurant, HOA and property management, commercial lines insurance, personal lines insurance, accounting and finance, commercial construction, and QSR and franchise operations. We are deliberately multi-vertical — a recruiting firm concentrated in one industry gets shut down when that industry does, which is exactly what happened to single-vertical hospitality recruiters in 2020."),
 ("Where do you recruit?",
  "We are based in the Greater Houston Area and recruit nationwide. Most searches are Texas and the Gulf Coast, but our networks in insurance, construction, and community association management extend across the country."),
 ("How do your fees work?",
  "Sliding-scale search and placement fees, quoted as a percentage of first-year compensation and agreed in writing before we start. Rates flex with volume and role level. If you tell us the annual budget you have for hiring, we will tell you honestly whether we can work inside it."),
 ("Do you offer a guarantee?",
  "Yes. Direct-hire placements carry a 30-day guarantee — if the person leaves within their first thirty days, we replace them at no additional fee."),
 ("Do you handle temporary and temp-to-hire placements?",
  "Yes. Direct hire, temp-to-hire, and temporary placement, depending on what the role actually calls for."),
 ("How long does a search usually take?",
  "For most roles we present a first slate within two weeks of the intake call. Time to offer depends more on your interview process than on ours — clients who can move candidates through in two rounds close far faster than clients who take a month to schedule."),
 ("Is there any cost for candidates?",
  "Never. Candidates are never charged. Our fees are paid by the hiring company."),
]

# ================================================================ helpers
def plain(s):
    """HTML-with-entities -> plain text, safe for JSON-LD and attributes."""
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s)

def jstr(s):
    """JSON string literal, escaped for embedding in <script type=ld+json>."""
    out = plain(s).replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
    return out.replace("</", "<\\/")

def rel(depth):
    return "../" * depth

# ================================================================ chrome
NAV_MAIN = [
    ("For Employers", "clients.html"),
    ("For Candidates", "candidates.html"),
    ("About", "about.html"),
]

def head(title, desc, canonical, depth=0, schema="", og_type="website"):
    r = rel(depth)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(plain(desc), quote=True)}">
<link rel="canonical" href="{SITE['domain']}/{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="author" content="{SITE['legal']}">
<meta name="geo.region" content="US-TX">
<meta name="geo.placename" content="Houston, Texas">

<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:title" content="{html.escape(plain(title), quote=True)}">
<meta property="og:description" content="{html.escape(plain(desc), quote=True)}">
<meta property="og:url" content="{SITE['domain']}/{canonical}">
<meta property="og:image" content="{SITE['domain']}/assets/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(plain(title), quote=True)}">
<meta name="twitter:description" content="{html.escape(plain(desc), quote=True)}">

<link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{r}assets/favicon.svg">
<meta name="theme-color" content="#10141a">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/styles.css">
{schema}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""

def header(active="", depth=0):
    r = rel(depth)
    ind_items = "".join(
        f'<a href="{r}industries/{i["slug"]}.html"><strong>{i["nav"]}</strong><span>{i["navdesc"]}</span></a>'
        for i in INDUSTRIES)
    nav = "".join(
        f'<a href="{r}{href}"{" class=\"active\"" if active == href else ""}>{label}</a>'
        for label, href in NAV_MAIN)
    drawer_ind = "".join(
        f'<a href="{r}industries/{i["slug"]}.html">{i["nav"]}</a>' for i in INDUSTRIES)
    drawer_nav = "".join(f'<a href="{r}{href}">{label}</a>' for label, href in NAV_MAIN)
    ind_active = ' class="active"' if active.startswith("industries") else ""
    return f"""<header class="hdr">
  <div class="wrap">
    <a class="brand" href="{r}index.html" aria-label="{SITE['name']} — home">
      <svg class="brand-mark" viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="#10141a"/><path d="M22 42.5c2.6 2.3 6.1 3.5 9.9 3.5 6.6 0 10.6-3 10.6-7.6 0-4.2-2.9-6.3-9-7.6l-3.1-.7c-3.1-.7-4.4-1.7-4.4-3.4 0-2.1 1.9-3.5 5.2-3.5 3 0 5.6 1 7.6 2.6l3-4.3C39.3 19.2 35.6 18 31.4 18c-6.2 0-10.2 3.1-10.2 7.7 0 4.1 2.7 6.3 8.5 7.5l3.1.7c3.4.7 4.8 1.7 4.8 3.5 0 2.2-2.1 3.6-5.6 3.6-3.3 0-6.2-1.1-8.5-3.1z" fill="#d98d63"/></svg>
      <span class="brand-txt"><span class="brand-name">Sublime Personnel</span><span class="brand-sub">We take recruiting personally</span></span>
    </a>
    <nav class="nav" aria-label="Primary">
      <div class="has-menu">
        <button type="button" aria-expanded="false"{ind_active}>Industries <svg viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="m2 4 3 3 3-3"/></svg></button>
        <div class="menu" role="menu">{ind_items}<a href="{r}industries.html"><strong>All seven industries</strong><span>How our verticals fit together</span></a></div>
      </div>
      {nav}
    </nav>
    <div class="hdr-cta">
      <a class="hdr-phone" href="tel:{SITE['phone_href']}">{ICONS['phone']} {SITE['phone']}</a>
      <a class="btn btn-ink btn-sm" href="{r}contact.html">Start a search</a>
      <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="drawer"><span></span></button>
    </div>
  </div>
</header>
<div class="drawer" id="drawer">
  <div class="wrap" style="padding:0">
    {drawer_nav}
    <p class="grp-label">Industries</p>
    <div class="sub">{drawer_ind}<a href="{r}industries.html">All seven industries</a></div>
    <div class="btns">
      <a class="btn btn-primary" href="{r}contact.html">Start a search</a>
      <a class="btn btn-ghost" href="tel:{SITE['phone_href']}">{SITE['phone']}</a>
    </div>
  </div>
</div>
"""

def cta_band(depth=0, heading="Tell us what you are trying to hire.", body="One call, twenty minutes. We will tell you whether we can fill it, roughly what it costs, and how fast — and if we are not the right firm, we will say so."):
    r = rel(depth)
    return f"""<section class="sec cta-band">
  <div class="wrap center">
    <p class="eyebrow center rv">Next step</p>
    <h2 class="mx-auto rv" style="margin:0 auto">{heading}</h2>
    <p class="lede mx-auto rv" style="margin:22px auto 0;color:rgba(255,255,255,.68)">{body}</p>
    <div class="btns rv" style="justify-content:center;margin-top:34px">
      <a class="btn btn-primary" href="{r}contact.html">Book an intake call {ICONS['arrow']}</a>
      <a class="btn btn-ghost" href="tel:{SITE['phone_href']}">Call {SITE['phone']}</a>
    </div>
  </div>
</section>
"""

def footer(depth=0):
    r = rel(depth)
    ind = "".join(f'<li><a href="{r}industries/{i["slug"]}.html">{i["nav"]}</a></li>' for i in INDUSTRIES)
    return f"""<footer class="ftr">
  <div class="wrap">
    <div class="ftr-top">
      <div>
        <a class="brand" href="{r}index.html">
          <svg class="brand-mark" viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="#1a2029"/><path d="M22 42.5c2.6 2.3 6.1 3.5 9.9 3.5 6.6 0 10.6-3 10.6-7.6 0-4.2-2.9-6.3-9-7.6l-3.1-.7c-3.1-.7-4.4-1.7-4.4-3.4 0-2.1 1.9-3.5 5.2-3.5 3 0 5.6 1 7.6 2.6l3-4.3C39.3 19.2 35.6 18 31.4 18c-6.2 0-10.2 3.1-10.2 7.7 0 4.1 2.7 6.3 8.5 7.5l3.1.7c3.4.7 4.8 1.7 4.8 3.5 0 2.2-2.1 3.6-5.6 3.6-3.3 0-6.2-1.1-8.5-3.1z" fill="#d98d63"/></svg>
          <span class="brand-txt"><span class="brand-name">Sublime Personnel</span><span class="brand-sub">We take recruiting personally</span></span>
        </a>
        <p class="ftr-blurb">A boutique executive search and recruiting firm in the Greater Houston Area, placing leadership across seven industries since {SITE['founded']}.</p>
        <div class="ftr-social">
          <a href="{SITE['linkedin']}" aria-label="Sublime Personnel on LinkedIn" rel="noopener" target="_blank">{ICONS['linkedin']}</a>
          <a href="tel:{SITE['phone_href']}" aria-label="Call Sublime Personnel">{ICONS['phone']}</a>
          <a href="mailto:{SITE['email']}" aria-label="Email Sublime Personnel">{ICONS['mail']}</a>
        </div>
      </div>
      <div>
        <h4>Industries</h4>
        <ul>{ind}</ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="{r}clients.html">For Employers</a></li>
          <li><a href="{r}candidates.html">For Candidates</a></li>
          <li><a href="{r}about.html">About</a></li>
          <li><a href="{r}industries.html">All Industries</a></li>
          <li><a href="{r}contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="tel:{SITE['phone_href']}">{SITE['phone']}</a></li>
          <li><a href="mailto:{SITE['email']}">{SITE['email']}</a></li>
          <li><a href="mailto:{SITE['email2']}">{SITE['email2']}</a></li>
          <li>{SITE['area']}<br>Recruiting nationwide</li>
        </ul>
      </div>
    </div>
    <div class="ftr-bot">
      <p>&copy; <span data-year>2026</span> {SITE['legal']}. All rights reserved.</p>
      <ul>
        <li><a href="{r}privacy.html">Privacy Policy</a></li>
        <li><a href="{r}sitemap.html">Sitemap</a></li>
      </ul>
    </div>
  </div>
</footer>
<div class="callbar">
  <a href="tel:{SITE['phone_href']}">Call {SITE['phone']}</a>
  <a class="alt" href="{r}contact.html">Start a search</a>
</div>
<script src="{r}assets/main.js" defer></script>
</body>
</html>
"""

def faq_block(items, heading="Common questions", eyebrow="FAQ"):
    rows = "".join(
        f"""<details{' open' if n == 0 else ''}>
      <summary>{q}</summary>
      <div class="ans"><p>{a}</p></div>
    </details>""" for n, (q, a) in enumerate(items))
    return f"""<section class="sec">
  <div class="wrap">
    <div class="split-hd">
      <div>
        <p class="eyebrow rv">{eyebrow}</p>
        <h2 class="rv">{heading}</h2>
      </div>
      <div class="faq rv">{rows}</div>
    </div>
  </div>
</section>
"""

def faq_schema(items):
    q = ",".join(
        '{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}' % (jstr(a), jstr(b))
        for a, b in items)
    return '<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}</script>\n' % q

ORG_SCHEMA = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":["EmploymentAgency","LocalBusiness","Organization"],
"@id":"%(domain)s/#organization","name":"%(legal)s","alternateName":"Sublime Personnel","slogan":"%(tagline)s",
"url":"%(domain)s/","telephone":"%(phone)s","email":"%(email)s","foundingDate":"%(founded)s","priceRange":"$$",
"logo":{"@type":"ImageObject","url":"%(domain)s/assets/favicon.svg"},
"image":"%(domain)s/assets/og-image.jpg",
"description":"Boutique executive search and recruiting firm in the Greater Houston Area placing leadership talent across hospitality, HOA and property management, commercial and personal lines insurance, accounting, commercial construction, and QSR and franchise operations.",
"address":{"@type":"PostalAddress","addressLocality":"Houston","addressRegion":"TX","addressCountry":"US"},
"areaServed":[{"@type":"City","name":"Houston"},{"@type":"State","name":"Texas"},{"@type":"Country","name":"United States"}],
"sameAs":["%(linkedin)s"],
"knowsAbout":["Executive search","Hospitality recruiting","HOA management recruiting","Insurance recruiting","Accounting recruiting","Commercial construction recruiting","Franchise operations recruiting"],
"founder":[{"@type":"Person","name":"Terry Richards","jobTitle":"Owner"},{"@type":"Person","name":"Pete Proctor","jobTitle":"Senior Recruiting Partner"}]}
</script>
""" % SITE

def breadcrumb_schema(trail):
    items = ",".join(
        '{"@type":"ListItem","position":%d,"name":"%s","item":"%s/%s"}' % (n + 1, jstr(name), SITE["domain"], href)
        for n, (name, href) in enumerate(trail))
    return '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[%s]}</script>\n' % items

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("  wrote", path, f"({len(content)//1024} KB)")

# ================================================================ home
def build_home():
    ind_cards = "".join(f"""<a class="card ind-card rv" href="industries/{i['slug']}.html">
        <span class="card-num">{n+1:02d}</span>
        <h3>{i['nav']}</h3>
        <p>{i['navdesc']}.</p>
        <span class="tlink">Explore this practice {ICONS['arrow']}</span>
      </a>""" for n, i in enumerate(INDUSTRIES))

    schema = ORG_SCHEMA + faq_schema(CORE_FAQ[:5]) + """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebSite","url":"%s/","name":"Sublime Personnel","publisher":{"@id":"%s/#organization"}}
</script>
""" % (SITE["domain"], SITE["domain"])

    body = f"""{head("Sublime Personnel | Executive Recruiting in Houston, TX", "Boutique executive recruiting firm in the Greater Houston Area. Hospitality, HOA and property management, insurance, accounting, commercial construction, and franchise operations. Recruiting since 2010.", "", 0, schema)}
{header("index.html", 0)}
<main id="main">

<section class="hero">
  <div class="wrap">
    <p class="eyebrow rv">Boutique executive search &middot; Houston, Texas &middot; Since {SITE['founded']}</p>
    <h1 class="rv">We recruit for seven industries because we <em>worked</em> in them first.</h1>
    <p class="lede rv">Sublime Personnel places leadership talent for employers who cannot afford a bad hire &mdash; in hospitality, community association management, insurance, accounting, commercial construction, and franchise operations. Two partners. Thirty years of recruiting between them. Every search run personally.</p>
    <div class="btns rv">
      <a class="btn btn-primary" href="contact.html">I need to hire someone {ICONS['arrow']}</a>
      <a class="btn btn-ghost" href="candidates.html">I'm looking for a role</a>
    </div>
    <div class="hero-figures">
      <div class="fig rv"><div class="fig-n">{SITE['founded']}</div><div class="fig-l">Recruiting under the Sublime name since</div></div>
      <div class="fig rv"><div class="fig-n">7</div><div class="fig-l">Industries, each one worked from the inside</div></div>
      <div class="fig rv"><div class="fig-n">30&#8209;day</div><div class="fig-l">Replacement guarantee on direct hire placements</div></div>
      <div class="fig rv"><div class="fig-n">12,000+</div><div class="fig-l">Professionals in our direct network</div></div>
    </div>
  </div>
</section>

<section class="sec-tight">
  <div class="wrap">
    <div class="paths rv">
      <div class="path">
        <p class="kicker">For employers</p>
        <h3>You have a seat to fill and no time to fill it.</h3>
        <p>We run the search end to end &mdash; scoping the role honestly, working our own network instead of a job board, and putting three or four people in front of you who could actually do the job.</p>
        <ul>
          <li>Direct hire, temp&#8209;to&#8209;hire, and temporary placement</li>
          <li>Sliding&#8209;scale fees, agreed in writing before we start</li>
          <li>30&#8209;day replacement guarantee on direct hire</li>
          <li>You talk to Pete or Terry &mdash; never a handoff</li>
        </ul>
        <a class="btn btn-ink" href="clients.html">How we run a search {ICONS['arrow']}</a>
      </div>
      <div class="path">
        <p class="kicker">For candidates</p>
        <h3>You want the next move to be the right one.</h3>
        <p>We do not blast your r&eacute;sum&eacute; anywhere. Your name goes to a company only after you have said yes to that company, and we tell you the parts of the job the posting left out.</p>
        <ul>
          <li>Always free &mdash; the hiring company pays our fee</li>
          <li>Confidential by default, especially for producers</li>
          <li>Real prep before every interview</li>
          <li>Straight answers on compensation and culture</li>
        </ul>
        <a class="btn btn-ghost" href="candidates.html">Start a confidential conversation {ICONS['arrow']}</a>
      </div>
    </div>
  </div>
</section>

<section class="sec tint">
  <div class="wrap">
    <div class="split-hd" style="margin-bottom:52px">
      <div>
        <p class="eyebrow rv">Practice areas</p>
        <h2 class="rv">Seven industries. One standard.</h2>
      </div>
      <div>
        <p class="lede rv">A recruiting firm concentrated in a single industry disappears when that industry does. We watched it happen to hospitality recruiters in 2020. Breadth is not a lack of focus &mdash; it is how a boutique firm stays standing, and how we keep a candidate network that spans the whole org chart of a mid&#8209;market company.</p>
      </div>
    </div>
    <div class="grid g3">{ind_cards}
      <a class="card ind-card rv" href="industries.html" style="background:var(--ink);border-color:transparent">
        <span class="card-num" style="color:var(--copper-l)">&mdash;</span>
        <h3 style="color:#fff">Not sure where your role fits?</h3>
        <p style="color:rgba(255,255,255,.62)">Most of our searches cross two verticals. Tell us the role and we will tell you straight whether it is one we can fill well.</p>
        <span class="tlink" style="color:var(--copper-l);border-color:rgba(217,141,99,.4)">See how the practices overlap {ICONS['arrow']}</span>
      </a>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="split">
      <div>
        <p class="eyebrow rv">Why a boutique</p>
        <h2 class="rv">Big firms send you r&eacute;sum&eacute;s. We send you people we have already vetted.</h2>
        <p class="lede rv" style="margin-top:24px">The large agencies solve for throughput. A junior recruiter runs a keyword search, forwards nine profiles, and hopes one sticks. You do the screening they billed you for.</p>
        <p class="rv" style="margin-top:16px">We are two partners with three decades of recruiting behind us, and we work each search ourselves. That caps how many we take at once &mdash; which is the point. When we present someone, we have already had the hard conversation about compensation, commute, counter&#8209;offers, and the thing they did not want to explain on their r&eacute;sum&eacute;.</p>
        <div class="btns rv" style="margin-top:30px"><a class="btn btn-ink" href="about.html">Meet Pete and Terry {ICONS['arrow']}</a></div>
      </div>
      <div class="grid" style="gap:20px">
        <div class="card rv"><div class="icn">{ICONS['users']}</div><h4>Operators, then recruiters</h4><p>Thirty years running restaurants. Two decades in insurance and construction. Two years inside high&#8209;rise property management. We screen from experience, not a keyword list.</p></div>
        <div class="card rv"><div class="icn">{ICONS['shield']}</div><h4>We turn down bad fits</h4><p>If a company has no training program and no way to retain the person we place, the hire falls off and everyone loses. We would rather say no at the intake call.</p></div>
        <div class="card rv"><div class="icn">{ICONS['handshake']}</div><h4>Fees you can plan around</h4><p>Sliding scale, quoted up front. Tell us what four placements a year need to cost you and we will tell you honestly if we can work in that space.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="sec sage">
  <div class="wrap">
    <div class="split-hd" style="margin-bottom:14px">
      <div>
        <p class="eyebrow rv">How a search runs</p>
        <h2 class="rv">Define the reach. Build the strategy. Deliver.</h2>
      </div>
      <div><p class="lede rv" style="color:rgba(255,255,255,.72)">The same three steps every time, whether it is a staff accountant or a regional vice president. What changes is the depth of the map we build in step two.</p></div>
    </div>
    <div class="steps">
      <div class="step rv"><div class="step-n">01</div><div>
        <h3>Define the reach</h3>
        <p>A real intake call, not a form. What the role actually does, who it reports to, the compensation band you can defend, the three things that would make you say yes on the spot, and the two that are quietly non&#8209;negotiable. We will push back here if the role as written cannot be filled at that number &mdash; better now than in month three.</p>
      </div></div>
      <div class="step rv"><div class="step-n">02</div><div>
        <h3>Create the strategy</h3>
        <p>We map the market: who holds this job today at the companies around you, who is credentialed and quietly open, and who we already know. Most of our best placements are people who were not looking. Sourcing is the part of this business we find easy &mdash; the network is already built.</p>
      </div></div>
      <div class="step rv"><div class="step-n">03</div><div>
        <h3>Deliver</h3>
        <p>A short slate with written notes on each person &mdash; why they fit, what the risk is, what they want. We coordinate the interviews, keep candidates warm through your process, and handle the offer and the counter&#8209;offer conversation. Direct hire placements carry a 30&#8209;day replacement guarantee.</p>
      </div></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="quote mx-auto center rv">
      <blockquote>&ldquo;Cost is always what you want to know up front. So tell me what you can afford to pay annually for four placements &mdash; and I'll tell you honestly whether I can work in that space.&rdquo;</blockquote>
      <cite>Pete Proctor &mdash; Senior Recruiting Partner, Sublime Personnel</cite>
    </div>
  </div>
</section>

<section class="sec tint">
  <div class="wrap">
    <div class="split-hd" style="margin-bottom:52px">
      <div><p class="eyebrow rv">The partners</p><h2 class="rv">Two people. Both of them recruit.</h2></div>
      <div><p class="lede rv">You will not be handed to a coordinator. The person who takes your intake call is the person who works your search and calls you when there is news &mdash; good or bad.</p></div>
    </div>
    <div class="grid g2">
      <div class="person rv">
        <div class="person-photo" aria-hidden="true">TR</div>
        <div>
          <h3>Terry Richards</h3>
          <p class="role">Owner</p>
          <p>Founded Sublime Personnel in {SITE['founded']} and has recruited since 2006 across insurance, engineering, information technology, and commercial construction. President of the Game Day Soccer League since 2016 &mdash; teamwork on and off the field, as he puts it.</p>
        </div>
      </div>
      <div class="person rv">
        <div class="person-photo" aria-hidden="true">PP</div>
        <div>
          <h3>Pete Proctor</h3>
          <p class="role">Senior Recruiting Partner</p>
          <p>Thirty&#8209;plus years in restaurant operations before recruiting, plus two years as a corporate recruiter inside a high&#8209;rise property management firm. Runs the hospitality, HOA, franchise, and Gulf Coast industrial practices. Treats every hire as an investment in tomorrow.</p>
        </div>
      </div>
    </div>
  </div>
</section>

{faq_block(CORE_FAQ[:5], "Questions we get before the first call.")}
{cta_band(0)}
</main>
{footer(0)}"""
    write("index.html", body)

# ================================================================ for employers
CLIENT_FAQ = [
 ("What does a placement cost?",
  "Fees are a sliding-scale percentage of the candidate's first-year compensation, agreed in writing before the search begins. The rate moves with role level and with volume — a company running four searches a year does not pay the same rate as a company running one. We would rather have the money conversation on the first call than at the offer stage."),
 ("What is the guarantee?",
  "Direct-hire placements carry a 30-day guarantee. If the person leaves inside their first thirty days, we run the search again at no additional fee."),
 ("Are you retained or contingency?",
  "Mostly contingency, with retained or engaged arrangements for confidential and executive searches where the work has to happen quietly and thoroughly. We will recommend the structure that fits the role rather than the one that pays us best."),
 ("How many candidates will I see?",
  "Three to five, with written notes on each. If we can only find two who genuinely qualify, we send two and tell you why the market is thin — padding a slate wastes your interview time and ours."),
 ("What do you need from us to start?",
  "Roughly an hour: a proper intake call, the compensation band you can actually defend, and one named decision maker who can move candidates through the process. Searches stall on scheduling far more often than on sourcing."),
 ("Will you sign our NDA or vendor agreement?",
  "Yes. Send it over with the role and we will turn it around quickly."),
]

def build_clients():
    schema = faq_schema(CLIENT_FAQ) + breadcrumb_schema([("Home", ""), ("For Employers", "clients.html")]) + """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Service","serviceType":"Executive search and recruiting","provider":{"@id":"%s/#organization"},
"areaServed":{"@type":"Country","name":"United States"},
"hasOfferCatalog":{"@type":"OfferCatalog","name":"Placement services","itemListElement":[
{"@type":"Offer","itemOffered":{"@type":"Service","name":"Direct hire placement"}},
{"@type":"Offer","itemOffered":{"@type":"Service","name":"Temp-to-hire placement"}},
{"@type":"Offer","itemOffered":{"@type":"Service","name":"Temporary placement"}},
{"@type":"Offer","itemOffered":{"@type":"Service","name":"Confidential executive search"}}]}}
</script>
""" % SITE["domain"]

    body = f"""{head("For Employers | Executive Search &amp; Recruiting | Sublime Personnel", "How Sublime Personnel runs a search for employers: honest intake, a mapped market, a short vetted slate, sliding-scale fees, and a 30-day guarantee on direct hire placements.", "clients.html", 0, schema)}
{header("clients.html", 0)}
<main id="main">

<section class="phead">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span>For Employers</nav>
    <p class="eyebrow">For employers</p>
    <h1>A short slate of people who can actually do the job.</h1>
    <p class="lede">You do not have a sourcing problem. You have a screening problem &mdash; and the fastest way to solve it is to hire recruiters who have held the job they are hiring for.</p>
    <div class="btns" style="margin-top:32px">
      <a class="btn btn-primary" href="contact.html">Start a search {ICONS['arrow']}</a>
      <a class="btn btn-ghost" href="tel:{SITE['phone_href']}">Call {SITE['phone']}</a>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="split-hd" style="margin-bottom:48px">
      <div><p class="eyebrow rv">What you get</p><h2 class="rv">Three ways to engage.</h2></div>
      <div><p class="lede rv">Most of our work is direct hire, but forcing every need into one model is how agencies end up selling the wrong thing. We will tell you which of these your situation calls for.</p></div>
    </div>
    <div class="grid g3">
      <div class="card rv"><div class="icn">{ICONS['users']}</div><h4>Direct hire</h4><p>Permanent placement, contingency or retained. Fee is a percentage of first&#8209;year compensation and carries the 30&#8209;day replacement guarantee.</p></div>
      <div class="card rv"><div class="icn">{ICONS['clock']}</div><h4>Temp&#8209;to&#8209;hire</h4><p>Bring someone in on our payroll, see them work, convert when you are sure. Useful for accounting and back&#8209;office roles where fit is hard to read in an interview.</p></div>
      <div class="card rv"><div class="icn">{ICONS['chart']}</div><h4>Temporary &amp; interim</h4><p>Coverage for a leave, a close, a build&#8209;out, or a gap between leaders. Includes interim controllers and fractional finance leadership.</p></div>
    </div>
  </div>
</section>

<section class="sec tint">
  <div class="wrap">
    <p class="eyebrow rv">The process</p>
    <h2 class="rv" style="max-width:20ch">What actually happens after you call us.</h2>
    <div class="steps" style="margin-top:44px">
      <div class="step rv"><div class="step-n">01</div><div>
        <h3>Intake &mdash; roughly forty minutes</h3>
        <p>We scope the role properly: responsibilities, reporting line, the compensation band you can defend, the interview process and who owns it, and what has gone wrong in this seat before. We will tell you on this call if the role as written cannot be filled at that number, and what would need to change.</p>
      </div></div>
      <div class="step rv"><div class="step-n">02</div><div>
        <h3>Market map &mdash; days one to five</h3>
        <p>We identify who holds this job at comparable companies, who is credentialed, and who is quietly open. Then we reach out personally. The best candidates in our verticals are not applying to anything &mdash; they are employed, busy, and only take the call because they know one of us.</p>
      </div></div>
      <div class="step rv"><div class="step-n">03</div><div>
        <h3>Slate &mdash; usually inside two weeks</h3>
        <p>Three to five candidates with written notes: why they fit, what the risk is, what they want, and what it will take to close them. No volume dumps. If the market only produced two real candidates, you get two and an explanation.</p>
      </div></div>
      <div class="step rv"><div class="step-n">04</div><div>
        <h3>Interviews and offer</h3>
        <p>We coordinate scheduling, debrief both sides after every round, and keep candidates engaged through slow weeks. When you are ready to make an offer we handle the compensation conversation and pre&#8209;empt the counter&#8209;offer, because a candidate who is surprised by a counter is a candidate you lose.</p>
      </div></div>
      <div class="step rv"><div class="step-n">05</div><div>
        <h3>Thirty days out</h3>
        <p>We check in with both of you at week one and week four. If it is not working, the guarantee applies and we go back out. If it is working, we ask who else you need &mdash; that is usually where the second search comes from.</p>
      </div></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="split">
      <div>
        <p class="eyebrow rv">Who we work best with</p>
        <h2 class="rv">We are not the right firm for everyone.</h2>
        <p class="lede rv" style="margin-top:22px">Being direct about this saves both of us a quarter.</p>
        <div class="callout rv">
          <h4>A good fit looks like</h4>
          <p>A medium to large company that hires roughly four professional or leadership roles a year, has a real onboarding and training program, and can move a candidate from first interview to offer inside three weeks.</p>
        </div>
        <div class="callout rv" style="border-color:var(--muted);background:var(--paper-2)">
          <h4>A poor fit looks like</h4>
          <p>High&#8209;volume hourly hiring, no training program to retain the person once placed, or a comp band well under market with no flexibility. In those cases the placement falls off, we end up in an endless warranty cycle, and nobody is better off. We will say so at the intake call.</p>
        </div>
      </div>
      <div class="grid" style="gap:20px">
        <div class="card rv"><div class="icn">{ICONS['search']}</div><h4>We screen on the job, not the r&eacute;sum&eacute;</h4><p>Every vertical page on this site lists exactly what we ask candidates in that field. Read the one that matches your role &mdash; it is the clearest picture of how we work.</p></div>
        <div class="card rv"><div class="icn">{ICONS['lock']}</div><h4>Confidential searches</h4><p>Replacing someone who still holds the seat is delicate. We run those quietly, and we never approach a candidate through a channel their current employer can see.</p></div>
        <div class="card rv"><div class="icn">{ICONS['shield']}</div><h4>30&#8209;day guarantee</h4><p>If a direct&#8209;hire placement leaves inside thirty days, we replace them at no additional fee. It has kept us honest about who we present for fifteen years.</p></div>
      </div>
    </div>
  </div>
</section>

<!-- TODO(client): swap this band for two real case studies once Pete and Terry
     confirm which engagements we can describe publicly (SOW §2.2c). -->
<section class="sec dark">
  <div class="wrap center">
    <p class="eyebrow center rv">Proof</p>
    <h2 class="rv mx-auto" style="margin:0 auto;max-width:22ch">Ask us for references in your industry.</h2>
    <p class="lede mx-auto rv" style="margin:22px auto 0;color:rgba(255,255,255,.68)">We would rather put you on the phone with a hiring manager who has used us than publish a testimonial you cannot verify. Tell us the vertical and we will make the introduction.</p>
    <div class="btns rv" style="justify-content:center;margin-top:32px"><a class="btn btn-primary" href="contact.html">Request references {ICONS['arrow']}</a></div>
  </div>
</section>

{faq_block(CLIENT_FAQ, "Employer questions, answered plainly.")}
{cta_band(0)}
</main>
{footer(0)}"""
    write("clients.html", body)

# ================================================================ for candidates
CAND_FAQ = [
 ("Does it cost me anything?",
  "No. Never. Our fees are paid entirely by the hiring company. If a recruiter ever asks you for money, walk away."),
 ("Will my current employer find out I'm talking to you?",
  "Not from us. We never send your résumé anywhere without your explicit approval of that specific company, and we do not approach you through channels your employer can see. For insurance producers and senior operators, discretion is the whole engagement."),
 ("What if I'm not actively looking?",
  "Most of the people we place were not. A twenty-minute call costs you nothing and means that when the right role appears, you hear about it first instead of reading about it after it is filled."),
 ("Do you have roles outside Houston?",
  "Yes. We are Houston-based and recruit nationwide, with the deepest reach in Texas and the Gulf Coast."),
 ("How will you prep me for an interview?",
  "You get the real context before you walk in: who you are meeting, why the seat is open, what went wrong with the last person, what the company is actually paying, and the two or three things this hiring manager cares about most. You should never be the least-informed person in the room."),
 ("What happens to my information?",
  "It stays with Pete and Terry. We do not sell, publish, or post candidate data, and we do not add you to a mailing list you did not ask for."),
]

def build_candidates():
    schema = faq_schema(CAND_FAQ) + breadcrumb_schema([("Home", ""), ("For Candidates", "candidates.html")])
    ind_links = "".join(f'<li><a class="tlink" href="industries/{i["slug"]}.html">{i["nav"]}</a></li>' for i in INDUSTRIES)
    body = f"""{head("For Candidates | Confidential Career Conversations | Sublime Personnel", "Free, confidential recruiting for professionals in hospitality, HOA management, insurance, accounting, commercial construction, and franchise operations. Your résumé never goes anywhere without your approval.", "candidates.html", 0, schema)}
{header("candidates.html", 0)}
<main id="main">

<section class="phead">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span>For Candidates</nav>
    <p class="eyebrow">For candidates</p>
    <h1>You are represented here, not listed.</h1>
    <p class="lede">Your r&eacute;sum&eacute; does not go anywhere until you say yes to that specific company. No blasting, no posting, no surprises getting back to your boss. That is not a policy we advertise &mdash; it is the only way this works.</p>
    <div class="btns" style="margin-top:32px">
      <a class="btn btn-primary" href="contact.html#candidates">Start a confidential conversation {ICONS['arrow']}</a>
      <a class="btn btn-ghost" href="tel:{SITE['phone_href']}">Call {SITE['phone']}</a>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="split">
      <div>
        <p class="eyebrow rv">What we do differently</p>
        <h2 class="rv">The posting never tells you the part that matters.</h2>
        <p class="lede rv" style="margin-top:22px">Why the seat is open. What happened to the last person. Whether the owner actually lets a controller close the books, or whether the board runs the manager out every two years.</p>
        <p class="rv" style="margin-top:16px">We know because we have worked in these industries and because we talk to the hiring manager, not an HR inbox. You get that context before your first interview, and you get an honest read on whether we think you should take the meeting at all.</p>
      </div>
      <div class="grid" style="gap:20px">
        <div class="card rv"><div class="icn">{ICONS['lock']}</div><h4>Confidential by default</h4><p>Especially for insurance producers and senior operators. Nothing moves without your explicit approval, company by company.</p></div>
        <div class="card rv"><div class="icn">{ICONS['handshake']}</div><h4>Free, always</h4><p>The hiring company pays the fee. You are never charged, for anything, at any stage.</p></div>
        <div class="card rv"><div class="icn">{ICONS['chart']}</div><h4>Straight compensation talk</h4><p>We know the bands in these markets. If what you want is not realistic, you will hear it from us early rather than find out in a final round.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="sec tint">
  <div class="wrap">
    <p class="eyebrow rv">How it goes</p>
    <h2 class="rv" style="max-width:18ch">Four steps, and you can stop at any of them.</h2>
    <div class="steps" style="margin-top:44px">
      <div class="step rv"><div class="step-n">01</div><div><h3>A real conversation</h3><p>Twenty minutes on where you are, what you actually want next, what you are paid now and what would make a move worth it. No pitch. If we have nothing for you today, we will say so and keep you in mind.</p></div></div>
      <div class="step rv"><div class="step-n">02</div><div><h3>You approve every introduction</h3><p>When a role fits, we tell you the company, the comp, the manager, and the catch. Only after you say yes to that company does your name leave our office.</p></div></div>
      <div class="step rv"><div class="step-n">03</div><div><h3>Prep that is worth something</h3><p>Who is in the room, what they are worried about, what the last person got wrong, and the questions you should ask that will make you the obvious choice.</p></div></div>
      <div class="step rv"><div class="step-n">04</div><div><h3>Offer, counter&#8209;offer, and after</h3><p>We negotiate on your behalf and we prepare you for the counter&#8209;offer your current employer will make. Then we check in at week one and week four, because a placement that does not stick helps nobody.</p></div></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="split-hd" style="margin-bottom:40px">
      <div><p class="eyebrow rv">Where we place people</p><h2 class="rv">Find your field.</h2></div>
      <div><p class="lede rv">Each page lists the roles we fill and exactly what a hiring manager in that field will be screening you on.</p></div>
    </div>
    <ul class="grid g2 rv" style="gap:18px 40px">{ind_links}</ul>
  </div>
</section>

<section class="sec sage">
  <div class="wrap">
    <div class="quote mx-auto center rv">
      <blockquote>&ldquo;Every hire is an investment in tomorrow &mdash; for the company and for the person. We take that personally on both sides of the table.&rdquo;</blockquote>
      <cite>Pete Proctor &mdash; Senior Recruiting Partner</cite>
    </div>
  </div>
</section>

{faq_block(CAND_FAQ, "Candidate questions, answered plainly.")}
{cta_band(0, "Send us your r&eacute;sum&eacute;. Nothing happens without your say-so.", "We will read it, tell you honestly what we are seeing in your market, and only reach out when something real comes up.")}
</main>
{footer(0)}"""
    write("candidates.html", body)

# ================================================================ about
def build_about():
    schema = breadcrumb_schema([("Home", ""), ("About", "about.html")]) + """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"AboutPage","mainEntity":{"@id":"%s/#organization"}}
</script>
""" % SITE["domain"]
    body = f"""{head("About Sublime Personnel | Houston Recruiting Firm Since 2010", "Sublime Personnel is a boutique recruiting firm founded in Houston in 2010 by Terry Richards. Meet the partners and read how the firm's seven-vertical model came about.", "about.html", 0, schema)}
{header("about.html", 0)}
<main id="main">

<section class="phead">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span>About</nav>
    <p class="eyebrow">About the firm</p>
    <h1>We take recruiting personally.</h1>
    <p class="lede">Sublime Personnel was founded in Houston in {SITE['founded']} on a simple idea: staffing done with integrity, by people who understand the work they are hiring for.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap wrap-sm prose">
    <p class="rv" style="font-size:1.14rem;color:var(--head)">Most recruiting firms sell reach. We sell judgment.</p>
    <p class="rv">Terry Richards started Sublime Personnel in {SITE['founded']} after four years recruiting insurance, engineering, and technology talent. Pete Proctor joined after three decades running restaurants and two years as a corporate recruiter inside a high&#8209;rise property management company. Between them they have placed leadership across seven industries, and in every one of them they have done the job or worked beside people who did.</p>
    <p class="rv">That is the whole thesis. A recruiter who has never run a P&amp;L cannot tell whether a general manager is describing a turnaround or describing luck. A recruiter who has never sat through a hostile HOA board meeting cannot tell whether a community manager will survive their second year. We can, because we have.</p>

    <h2 class="rv">Why seven verticals</h2>
    <p class="rv">Specialisation is conventional wisdom in recruiting, and it is a trap for a small firm. Pete was recruiting in hospitality when COVID arrived and the keys got turned off overnight &mdash; every search, every client, gone in a week. Firms that had only ever placed restaurant managers did not survive that.</p>
    <p class="rv">Seven verticals is not scattered. It is deliberately diversified, and the verticals reinforce each other: accounting runs through every one of them, insurance and construction share a client base, and hospitality and franchise operations are two dialects of the same language. When a client in one vertical needs a controller or a safety director, we are not starting from zero.</p>

    <div class="callout rv">
      <h4>What has never changed</h4>
      <p>Every search is worked by a partner. Fees are quoted before the work starts. Direct hire placements carry a 30&#8209;day guarantee. And if we do not think we can fill your role well, we tell you at the intake call instead of taking the engagement and hoping.</p>
    </div>
  </div>
</section>

<section class="sec tint">
  <div class="wrap">
    <p class="eyebrow rv">The partners</p>
    <h2 class="rv" style="margin-bottom:52px">Who you will actually be working with.</h2>
    <div class="grid g2" style="gap:44px">
      <div class="person rv">
        <div class="person-photo" aria-hidden="true">TR</div>
        <div>
          <h3>Terry Richards</h3>
          <p class="role">Owner &middot; Founded {SITE['founded']}</p>
          <p>Terry has recruited since 2006, with a practice built on executive search across insurance, engineering, information technology, commercial construction, and business development. He founded Sublime Personnel on a commitment to quality staffing delivered with integrity and purpose&#8209;driven leadership, and he has run it that way ever since.</p>
          <p>Outside the firm he has served as President of the Game Day Soccer League since 2016 &mdash; a fair summary of how he thinks about teams, on the field and off it.</p>
          <p style="margin-top:16px"><a class="tlink" href="mailto:{SITE['email2']}">{SITE['email2']} {ICONS['arrow']}</a></p>
        </div>
      </div>
      <div class="person rv">
        <div class="person-photo" aria-hidden="true">PP</div>
        <div>
          <h3>Pete Proctor</h3>
          <p class="role">Senior Recruiting Partner</p>
          <p>Pete spent more than thirty years in restaurant operations before he recruited for it &mdash; the kind of operator who walked into units doing ninety and left them past one&#8209;thirty. He then spent two years as a corporate recruiter for a high&#8209;rise property management firm, where he learned that in community association management, governance is everything.</p>
          <p>He runs the hospitality, HOA and property management, franchise, and Gulf Coast industrial practices, and he approaches every placement the same way: integrity, care, and the belief that a hire is an investment in tomorrow.</p>
          <p style="margin-top:16px"><a class="tlink" href="mailto:{SITE['email']}">{SITE['email']} {ICONS['arrow']}</a></p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec dark">
  <div class="wrap">
    <p class="eyebrow rv">How we work</p>
    <h2 class="rv" style="max-width:20ch;margin-bottom:48px">Four commitments we will not trade away.</h2>
    <div class="grid g4">
      <div class="card rv"><span class="card-num">01</span><h4>Partner&#8209;run searches</h4><p>No coordinators, no handoffs. The person on your intake call works your search.</p></div>
      <div class="card rv"><span class="card-num">02</span><h4>Honest at the start</h4><p>If the role cannot be filled at that comp, or the company cannot retain the hire, we say so before taking the engagement.</p></div>
      <div class="card rv"><span class="card-num">03</span><h4>Candidates are people</h4><p>No r&eacute;sum&eacute; leaves this office without the candidate approving that specific company. Ever.</p></div>
      <div class="card rv"><span class="card-num">04</span><h4>We stand behind it</h4><p>A 30&#8209;day replacement guarantee on direct hire, and a check&#8209;in with both sides at week one and week four.</p></div>
    </div>
  </div>
</section>

{cta_band(0)}
</main>
{footer(0)}"""
    write("about.html", body)

# ================================================================ industries hub
def build_industries_hub():
    cards = "".join(f"""<a class="card ind-card rv" href="industries/{i['slug']}.html">
        <span class="card-num">{n+1:02d}</span>
        <h3>{i['nav']}</h3>
        <p>{i['lede'][:150].rsplit(' ',1)[0]}&hellip;</p>
        <ul class="roles">{''.join(f'<li>{r}</li>' for r in i['roles'][:4])}</ul>
        <span class="tlink">View this practice {ICONS['arrow']}</span>
      </a>""" for n, i in enumerate(INDUSTRIES))
    schema = breadcrumb_schema([("Home", ""), ("Industries", "industries.html")])
    body = f"""{head("Industries We Recruit For | Sublime Personnel", "Seven recruiting practices: hospitality and restaurant, HOA and property management, commercial and personal lines insurance, accounting and finance, commercial construction, and QSR and franchise operations.", "industries.html", 0, schema)}
{header("industries.html", 0)}
<main id="main">

<section class="phead">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span>Industries</nav>
    <p class="eyebrow">Practice areas</p>
    <h1>Seven industries we know from the inside.</h1>
    <p class="lede">Each of these is a practice, not a keyword. The pages below list the roles we fill and the specific questions we ask candidates in that field &mdash; which is the fastest way to judge whether we know your business.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="grid g3">{cards}</div>
  </div>
</section>

<section class="sec tint">
  <div class="wrap">
    <div class="split">
      <div>
        <p class="eyebrow rv">How they connect</p>
        <h2 class="rv">Most searches cross two of these.</h2>
        <p class="lede rv" style="margin-top:22px">A restaurant group needs a controller. A property management company needs an association accountant and a maintenance director. A commercial contractor needs a safety director and a risk advisor, and their insurance agency needs a producer who understands contractors.</p>
        <p class="rv" style="margin-top:16px">That overlap is the practical argument for a multi&#8209;vertical firm. When you have hired us once, the second search rarely starts from zero &mdash; we already know your business, your comp philosophy, and the kind of person who lasts there.</p>
        <div class="btns rv" style="margin-top:30px"><a class="btn btn-ink" href="contact.html">Tell us what you need {ICONS['arrow']}</a></div>
      </div>
      <div class="grid" style="gap:20px">
        <div class="card rv"><div class="icn">{ICONS['users']}</div><h4>Leadership and professional roles</h4><p>Management through executive. We do not do high&#8209;volume hourly staffing, and we will tell you when that is what you actually need.</p></div>
        <div class="card rv"><div class="icn">{ICONS['pin']}</div><h4>Houston&#8209;based, nationwide reach</h4><p>Deepest in Texas and the Gulf Coast, with insurance, construction, and community association networks across the country.</p></div>
        <div class="card rv"><div class="icn">{ICONS['search']}</div><h4>Hard&#8209;to&#8209;fill technical niches</h4><p>Including energy&#8209;adjacent roles like subsea and ROV operators, where the candidate pool is a personal network rather than a job board.</p></div>
      </div>
    </div>
  </div>
</section>

{cta_band(0)}
</main>
{footer(0)}"""
    write("industries.html", body)

# ================================================================ industry pages
def build_industry(idx, i):
    nxt = INDUSTRIES[(idx + 1) % len(INDUSTRIES)]
    prv = INDUSTRIES[(idx - 1) % len(INDUSTRIES)]
    roles = "".join(f'<li class="rv">{r}</li>' for r in i["roles"])
    screen = "".join(f"""<div class="step rv"><div class="step-n">{n+1:02d}</div><div><h3>{t}</h3><p>{d}</p></div></div>"""
                     for n, (t, d) in enumerate(i["screen"]))
    why = "".join(f'<p class="rv">{p}</p>' for p in i["why"])
    allfaq = i["faq"] + [CORE_FAQ[2], CORE_FAQ[3], CORE_FAQ[5]]
    others = "".join(
        f'<a class="card ind-card rv" href="{o["slug"]}.html"><h4>{o["nav"]}</h4><p>{o["navdesc"]}.</p><span class="tlink">View practice {ICONS["arrow"]}</span></a>'
        for o in (prv, nxt))
    schema = (faq_schema(allfaq)
              + breadcrumb_schema([("Home", ""), ("Industries", "industries.html"), (plain(i["nav"]), f"industries/{i['slug']}.html")])
              + """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Service","name":"%s","serviceType":"Recruiting and executive search",
"provider":{"@id":"%s/#organization"},"areaServed":[{"@type":"City","name":"Houston"},{"@type":"Country","name":"United States"}],
"description":"%s","url":"%s/industries/%s.html"}
</script>
""" % (jstr(i["h1"]), SITE["domain"], jstr(i["desc"]), SITE["domain"], i["slug"]))

    body = f"""{head(f"{i['title']} | Sublime Personnel", i["desc"], f"industries/{i['slug']}.html", 1, schema)}
{header("industries/" + i["slug"], 1)}
<main id="main">

<section class="phead">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><span>/</span><a href="../industries.html">Industries</a><span>/</span>{i['nav']}</nav>
    <p class="eyebrow">Practice area {idx+1:02d} of 07</p>
    <h1>{i['h1']}</h1>
    <p class="lede">{i['lede']}</p>
    <div class="btns" style="margin-top:32px">
      <a class="btn btn-primary" href="../contact.html">Start a search {ICONS['arrow']}</a>
      <a class="btn btn-ghost" href="../candidates.html">I work in this field</a>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="split-hd">
      <div>
        <p class="eyebrow rv">Why us for this</p>
        <h2 class="rv">Experience, not keywords.</h2>
      </div>
      <div class="prose">{why}</div>
    </div>
  </div>
</section>

<section class="sec tint">
  <div class="wrap">
    <div class="split-hd" style="margin-bottom:44px">
      <div><p class="eyebrow rv">Roles we fill</p><h2 class="rv">{i['short']} placements.</h2></div>
      <div><p class="lede rv">Management level and above, direct hire, temp&#8209;to&#8209;hire, or interim. If your role is close to one of these but not on the list, call us &mdash; the answer is usually yes.</p></div>
    </div>
    <ul class="grid g3" style="gap:14px">{roles}</ul>
    <style>
      .grid > li {{ background:var(--white); border:1px solid var(--line); border-radius:6px; padding:15px 18px; font-size:.95rem; color:var(--head); font-weight:500; }}
    </style>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <p class="eyebrow rv">What we screen for</p>
    <h2 class="rv" style="max-width:22ch">The questions that separate a r&eacute;sum&eacute; from a hire.</h2>
    <div class="steps" style="margin-top:44px">{screen}</div>
  </div>
</section>

<section class="sec sage">
  <div class="wrap">
    <div class="split">
      <div>
        <p class="eyebrow rv">Hiring in {plain(i['short']).lower()}?</p>
        <h2 class="rv">Tell us the seat and the number.</h2>
        <p class="lede rv" style="margin-top:20px;color:rgba(255,255,255,.72)">Forty minutes on the phone and you will know whether we can fill it, what it costs, and roughly how long it takes. If we are not the right firm for this one, we will say so and point you somewhere better.</p>
        <div class="btns rv" style="margin-top:30px">
          <a class="btn btn-primary" href="../contact.html">Book an intake call {ICONS['arrow']}</a>
          <a class="btn btn-ghost" href="tel:{SITE['phone_href']}">{SITE['phone']}</a>
        </div>
      </div>
      <div class="grid" style="gap:20px">
        <div class="card rv"><div class="icn">{ICONS['clock']}</div><h4>First slate in about two weeks</h4><p>Three to five candidates with written notes on fit, risk, and what it takes to close them.</p></div>
        <div class="card rv"><div class="icn">{ICONS['shield']}</div><h4>30&#8209;day guarantee</h4><p>Direct hire placements are replaced at no additional fee if they leave inside thirty days.</p></div>
      </div>
    </div>
  </div>
</section>

{faq_block(allfaq, f"{i['short']} recruiting questions.")}

<section class="sec tint">
  <div class="wrap">
    <p class="eyebrow rv">Related practices</p>
    <h2 class="rv" style="margin-bottom:40px">Most clients hire across two of these.</h2>
    <div class="grid g3">{others}
      <a class="card ind-card rv" href="../industries.html"><h4>All seven practices</h4><p>See how the verticals overlap and where your role fits.</p><span class="tlink">View all {ICONS['arrow']}</span></a>
    </div>
  </div>
</section>

{cta_band(1)}
</main>
{footer(1)}"""
    write(f"industries/{i['slug']}.html", body)

# ================================================================ contact
def build_contact():
    ind_opts = "".join(f'<option>{plain(i["nav"])}</option>' for i in INDUSTRIES) + '<option>Something else</option>'
    booking = ""
    if SITE["booking"]:
        booking = f"""<section class="sec-tight tint" id="book">
  <div class="wrap">
    <p class="eyebrow rv">Or book directly</p>
    <h2 class="rv" style="margin-bottom:30px">Pick a time on the calendar.</h2>
    <div class="rv" style="border:1px solid var(--line);border-radius:8px;overflow:hidden;background:#fff">
      <iframe src="{SITE['booking']}" title="Book a call with Sublime Personnel" style="width:100%;min-height:720px;border:0" loading="lazy"></iframe>
    </div>
  </div>
</section>"""
    else:
        booking = """<!-- TODO(setup): paste the Calendly / GHL booking link into SITE["booking"]
     in _build/build.py and re-run the build to drop a live calendar in here. -->"""

    schema = breadcrumb_schema([("Home", ""), ("Contact", "contact.html")]) + """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ContactPage","mainEntity":{"@id":"%s/#organization"}}
</script>
""" % SITE["domain"]

    body = f"""{head("Contact Sublime Personnel | Houston Recruiting Firm", "Start a search or a confidential career conversation with Sublime Personnel. Call 713-396-0944 or send us the role — Pete or Terry responds within one business day.", "contact.html", 0, schema)}
{header("contact.html", 0)}
<main id="main">

<section class="phead">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span>Contact</nav>
    <p class="eyebrow">Contact</p>
    <h1>Two doors. Pick the one that's you.</h1>
    <p class="lede">Either way you are writing to Pete or Terry directly, and either way you will hear back within one business day.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="split" style="align-items:start;gap:clamp(32px,5vw,68px)">

      <div class="form-card rv">
        <div class="tabs" data-tabs role="tablist" aria-label="Who are you?">
          <button class="tab" type="button" role="tab" id="tab-employer" aria-controls="panel-employer" aria-selected="true">I'm hiring</button>
          <button class="tab" type="button" role="tab" id="tab-candidate" aria-controls="panel-candidate" aria-selected="false">I'm looking</button>
        </div>

        <div id="panel-employer" role="tabpanel" aria-labelledby="tab-employer">
          <form data-form="employer" novalidate>
            <div class="form-msg" role="status" aria-live="polite"></div>
            <div class="field-row">
              <div class="field"><label for="e-name">Your name <span class="req">*</span></label><input id="e-name" name="name" type="text" autocomplete="name" required></div>
              <div class="field"><label for="e-co">Company <span class="req">*</span></label><input id="e-co" name="company" type="text" autocomplete="organization" required></div>
            </div>
            <div class="field-row">
              <div class="field"><label for="e-email">Work email <span class="req">*</span></label><input id="e-email" name="email" type="email" autocomplete="email" required></div>
              <div class="field"><label for="e-phone">Phone</label><input id="e-phone" name="phone" type="tel" autocomplete="tel"></div>
            </div>
            <div class="field"><label for="e-role">Role you're hiring for <span class="req">*</span></label><input id="e-role" name="role" type="text" placeholder="e.g. Portfolio Manager, high-rise" required></div>
            <div class="field-row">
              <div class="field"><label for="e-ind">Industry</label><select id="e-ind" name="industry"><option value="">Select&hellip;</option>{ind_opts}</select></div>
              <div class="field"><label for="e-loc">Location</label><input id="e-loc" name="location" type="text" placeholder="City, state or remote"></div>
            </div>
            <div class="field-row">
              <div class="field"><label for="e-comp">Compensation range</label><input id="e-comp" name="compensation" type="text" placeholder="e.g. $95k&ndash;$115k + bonus"></div>
              <div class="field"><label for="e-when">Need them by</label><select id="e-when" name="timeline"><option value="">Select&hellip;</option><option>Yesterday</option><option>Within 30 days</option><option>Within 90 days</option><option>Planning ahead</option></select></div>
            </div>
            <div class="field"><label for="e-notes">Anything else we should know</label><textarea id="e-notes" name="notes" placeholder="Why the seat is open, what went wrong last time, what a great hire looks like."></textarea></div>
            <div class="hp" aria-hidden="true"><label for="e-hp">Leave blank</label><input id="e-hp" name="company_website" type="text" tabindex="-1" autocomplete="off"></div>
            <button class="btn btn-primary" type="submit">Send the role {ICONS['arrow']}</button>
            <p class="form-note">We reply within one business day. Nothing you send here is shared outside Pete and Terry.</p>
          </form>
        </div>

        <div id="panel-candidate" role="tabpanel" aria-labelledby="tab-candidate" hidden>
          <form data-form="candidate" novalidate>
            <div class="form-msg" role="status" aria-live="polite"></div>
            <div class="field-row">
              <div class="field"><label for="c-name">Your name <span class="req">*</span></label><input id="c-name" name="name" type="text" autocomplete="name" required></div>
              <div class="field"><label for="c-email">Email <span class="req">*</span></label><input id="c-email" name="email" type="email" autocomplete="email" required></div>
            </div>
            <div class="field-row">
              <div class="field"><label for="c-phone">Phone</label><input id="c-phone" name="phone" type="tel" autocomplete="tel"></div>
              <div class="field"><label for="c-title">Current title</label><input id="c-title" name="current_title" type="text" autocomplete="organization-title"></div>
            </div>
            <div class="field-row">
              <div class="field"><label for="c-ind">Field</label><select id="c-ind" name="industry"><option value="">Select&hellip;</option>{ind_opts}</select></div>
              <div class="field"><label for="c-loc">Where you are / will go</label><input id="c-loc" name="location" type="text" placeholder="Houston, open to relocate"></div>
            </div>
            <div class="field"><label for="c-link">LinkedIn or r&eacute;sum&eacute; link</label><input id="c-link" name="profile_url" type="url" placeholder="https://linkedin.com/in/&hellip;"><p class="hint">Prefer to send a file? Email it to <a href="mailto:{SITE['email']}" style="color:var(--copper)">{SITE['email']}</a>.</p></div>
            <div class="field"><label for="c-want">What you want next</label><textarea id="c-want" name="notes" placeholder="Target role, compensation, and what would make a move worth it."></textarea></div>
            <div class="hp" aria-hidden="true"><label for="c-hp">Leave blank</label><input id="c-hp" name="company_website" type="text" tabindex="-1" autocomplete="off"></div>
            <button class="btn btn-primary" type="submit">Start the conversation {ICONS['arrow']}</button>
            <p class="form-note">Confidential. Your r&eacute;sum&eacute; never goes to a company without your approval of that specific company, and we never charge candidates.</p>
          </form>
        </div>
      </div>

      <div>
        <p class="eyebrow rv">Direct lines</p>
        <h2 class="rv" style="margin-bottom:12px">Prefer to just call?</h2>
        <p class="rv" style="margin-bottom:22px">Most of our best engagements started with a twenty&#8209;minute phone call rather than a form.</p>
        <div class="rv">
          <div class="crow"><div class="icn">{ICONS['phone']}</div><div><div class="lbl">Phone</div><div class="val"><a href="tel:{SITE['phone_href']}">{SITE['phone']}</a></div><div class="sub">Monday&ndash;Friday, 8am&ndash;6pm Central</div></div></div>
          <div class="crow"><div class="icn">{ICONS['mail']}</div><div><div class="lbl">Pete Proctor &mdash; Senior Recruiting Partner</div><div class="val"><a href="mailto:{SITE['email']}">{SITE['email']}</a></div><div class="sub">Hospitality, HOA &amp; property management, franchise, industrial</div></div></div>
          <div class="crow"><div class="icn">{ICONS['mail']}</div><div><div class="lbl">Terry Richards &mdash; Owner</div><div class="val"><a href="mailto:{SITE['email2']}">{SITE['email2']}</a></div><div class="sub">Insurance, construction, engineering, accounting</div></div></div>
          <div class="crow"><div class="icn">{ICONS['pin']}</div><div><div class="lbl">Where we are</div><div class="val">{SITE['area']}, Texas</div><div class="sub">Recruiting nationwide</div></div></div>
          <div class="crow"><div class="icn">{ICONS['clock']}</div><div><div class="lbl">Response time</div><div class="val">One business day</div><div class="sub">Usually a lot faster</div></div></div>
        </div>
        <div class="callout rv" style="margin-top:34px">
          <h4>Already know it's confidential?</h4>
          <p>Say so in the notes, or just call. We run producer and executive searches quietly as a matter of course &mdash; nothing gets posted, nothing gets forwarded.</p>
        </div>
      </div>

    </div>
  </div>
</section>

{booking}
</main>
{footer(0)}"""
    write("contact.html", body)

# ================================================================ utility pages
def build_utility():
    # ---- privacy
    body = f"""{head("Privacy Policy | Sublime Personnel", "How Sublime Personnel collects, uses, and protects the information you share with us as a client or candidate.", "privacy.html", 0, "")}
{header("privacy.html", 0)}
<main id="main">
<section class="phead"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span>Privacy Policy</nav>
  <h1>Privacy policy</h1>
  <p class="lede">Short version: we do not sell your data, and a candidate r&eacute;sum&eacute; never leaves this office without that candidate's approval.</p>
</div></section>
<section class="sec"><div class="wrap wrap-sm prose">
  <p><em>Last updated: <span data-year>2026</span>. This is a working draft for the new site &mdash; have counsel review before launch.</em></p>
  <h2>What we collect</h2>
  <p>When you submit a form on this site we collect the information you enter: your name, contact details, employer or current role, and anything you type into the notes field. Like most websites we also collect basic technical data through analytics &mdash; pages viewed, approximate location, browser and device type, and the site that referred you.</p>
  <h2>How we use it</h2>
  <ul>
    <li>To respond to your inquiry and run the search or job conversation you asked for.</li>
    <li>To present candidates to employers &mdash; only after the candidate has approved that specific employer.</li>
    <li>To improve the website and understand which pages help people find us.</li>
  </ul>
  <h2>What we never do</h2>
  <ul>
    <li>We do not sell, rent, or trade personal information to anyone.</li>
    <li>We do not post, publish, or distribute r&eacute;sum&eacute;s.</li>
    <li>We do not add you to a marketing list you did not ask to join.</li>
    <li>We never charge candidates for anything.</li>
  </ul>
  <h2>Cookies and analytics</h2>
  <p>This site uses cookies for basic functionality and for analytics (Google Analytics 4 and Google Search Console). You can block or delete cookies in your browser settings; the site will still work.</p>
  <h2>Third parties</h2>
  <p>Form submissions are transmitted to our customer relationship management system so that an inquiry does not get lost in an inbox. Those providers process the data on our behalf and are not permitted to use it for their own purposes.</p>
  <h2>Your choices</h2>
  <p>You can ask us at any time to tell you what we hold about you, correct it, or delete it. Email <a class="tlink" href="mailto:{SITE['email']}">{SITE['email']}</a> or call <a class="tlink" href="tel:{SITE['phone_href']}">{SITE['phone']}</a> and we will handle it.</p>
  <h2>Contact</h2>
  <p>{SITE['legal']}<br>{SITE['area']}, Texas<br><a class="tlink" href="tel:{SITE['phone_href']}">{SITE['phone']}</a></p>
</div></section>
</main>
{footer(0)}"""
    write("privacy.html", body)

    # ---- html sitemap
    ind = "".join(f'<li><a class="tlink" href="industries/{i["slug"]}.html">{i["nav"]}</a></li>' for i in INDUSTRIES)
    body = f"""{head("Sitemap | Sublime Personnel", "Every page on the Sublime Personnel website.", "sitemap.html", 0, "")}
{header("sitemap.html", 0)}
<main id="main">
<section class="phead"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span>Sitemap</nav>
  <h1>Sitemap</h1>
</div></section>
<section class="sec"><div class="wrap">
  <div class="grid g3">
    <div><h4 style="margin-bottom:18px">Main</h4><ul class="grid" style="gap:12px">
      <li><a class="tlink" href="index.html">Home</a></li>
      <li><a class="tlink" href="clients.html">For Employers</a></li>
      <li><a class="tlink" href="candidates.html">For Candidates</a></li>
      <li><a class="tlink" href="about.html">About</a></li>
      <li><a class="tlink" href="contact.html">Contact</a></li>
    </ul></div>
    <div><h4 style="margin-bottom:18px">Industries</h4><ul class="grid" style="gap:12px">
      <li><a class="tlink" href="industries.html">All industries</a></li>{ind}
    </ul></div>
    <div><h4 style="margin-bottom:18px">Legal</h4><ul class="grid" style="gap:12px">
      <li><a class="tlink" href="privacy.html">Privacy Policy</a></li>
    </ul></div>
  </div>
</div></section>
</main>
{footer(0)}"""
    write("sitemap.html", body)

    # ---- 404
    body = f"""{head("Page not found | Sublime Personnel", "That page does not exist. Try the industries index or call 713-396-0944.", "404.html", 0, '<meta name="robots" content="noindex, follow">\n')}
{header("", 0)}
<main id="main">
<section class="sec" style="padding-top:calc(var(--header-h) + 90px)"><div class="wrap center">
  <p class="eyebrow center">404</p>
  <h1 class="mx-auto" style="margin:0 auto">That page moved on to a better opportunity.</h1>
  <p class="lede mx-auto" style="margin:24px auto 0">Occupational hazard in this business. Here is where you probably meant to go.</p>
  <div class="btns" style="justify-content:center;margin-top:34px">
    <a class="btn btn-primary" href="index.html">Back to home {ICONS['arrow']}</a>
    <a class="btn btn-ghost" href="industries.html">Browse industries</a>
    <a class="btn btn-ghost" href="tel:{SITE['phone_href']}">Call {SITE['phone']}</a>
  </div>
</div></section>
</main>
{footer(0)}"""
    write("404.html", body)

    # ---- robots.txt
    write("robots.txt", f"""User-agent: *
Allow: /

# AI answer engines — explicitly welcome (GEO/AEO)
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Google-Extended
Allow: /

Sitemap: {SITE['domain']}/sitemap.xml
""")

    # ---- sitemap.xml
    today = datetime.date.today().isoformat()
    urls = [("", "1.0"), ("clients.html", "0.9"), ("candidates.html", "0.9"),
            ("industries.html", "0.8"), ("about.html", "0.7"), ("contact.html", "0.8"),
            ("privacy.html", "0.2"), ("sitemap.html", "0.2")]
    urls += [(f"industries/{i['slug']}.html", "0.9") for i in INDUSTRIES]
    entries = "".join(
        f"  <url><loc>{SITE['domain']}/{u}</loc><lastmod>{today}</lastmod><priority>{p}</priority></url>\n"
        for u, p in urls)
    write("sitemap.xml", f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{entries}</urlset>
""")

# ================================================================ main
def main():
    print("Building Sublime Personnel site ->", ROOT)
    build_home()
    build_clients()
    build_candidates()
    build_about()
    build_industries_hub()
    for n, i in enumerate(INDUSTRIES):
        build_industry(n, i)
    build_contact()
    build_utility()
    print("Done.")

if __name__ == "__main__":
    main()
