# Sublime Personnel — new website (first draft)

Static site. No framework, no build dependency beyond Python 3. Every page is
plain HTML that any host can serve and any developer can edit by hand.

Built against the signed SOW (`sow_sublime_personnel_search.txt`, §2.2) and the
2026-08-05 discovery call with Pete.

---

## What's here

| Page | File | Purpose |
|---|---|---|
| Home | `index.html` | Positioning, two-path split, 7 verticals, process, partners, FAQ |
| For Employers | `clients.html` | Engagement models, 5-step search process, fit/non-fit, employer FAQ |
| For Candidates | `candidates.html` | Confidentiality promise, 4-step process, candidate FAQ |
| About | `about.html` | Firm story, why seven verticals, Terry + Pete bios, commitments |
| Industries hub | `industries.html` | All seven practices + how they overlap |
| 7 vertical pages | `industries/*.html` | Roles filled, what we screen for, per-vertical FAQ |
| Contact | `contact.html` | Dual employer/candidate tabbed form, direct lines |
| Privacy | `privacy.html` | Draft policy — **have counsel review before launch** |
| Sitemap | `sitemap.html` | Human sitemap |
| 404 | `404.html` | |

Plus `robots.txt` (AI crawlers explicitly allowed, for the GEO/AEO work) and
`sitemap.xml`.

## Editing

Shared chrome (header, footer, CTA band, schema) is generated so twelve pages
can't drift apart. Content lives in `_build/build.py`.

```bash
cd clients/sublime-personnel/website
python3 _build/build.py       # regenerates every HTML file
```

Editing a generated `.html` directly works fine for a one-off tweak, but the
next build overwrites it. Put real changes in `_build/build.py`.

CSS and JS are hand-written and **not** generated: `assets/styles.css`,
`assets/main.js`.

## Before this goes live

Three things need Pete/Terry or an account, marked `TODO` in the source:

1. **Form endpoint** — `assets/main.js`, `SITE.FORM_ENDPOINT`. Paste a GHL
   inbound webhook, Zapier catch hook, or Formspree URL. Until then the form
   falls back to opening a `mailto:` draft to `pete@sublimepersonnel.com`, so
   the staging link is never a dead end.
2. **Booking link** — `_build/build.py`, `SITE["booking"]`. Paste the Calendly /
   GHL calendar URL and rebuild; a live calendar section appears on `contact.html`.
3. **Case studies** — `clients.html` currently offers references instead of
   testimonials (SOW §2.2c calls for two written case studies). Needs Pete and
   Terry to confirm which engagements can be described publicly.

Nice to have, not blocking:

- **Real headshots** for Terry and Pete — currently monogram circles. Drop
  `assets/img/terry.jpg` and `assets/img/pete.jpg` in and swap the
  `.person-photo` divs for `<img>`.
- **Google reviews + video embed** (SOW §2.2e) — needs the GBP review widget and
  the HOA video URLs Pete mentioned ranking on the call.
- **Logo file** — the wordmark is set in Fraunces with a generated `S` mark.
  If there's a real logo, it replaces `assets/favicon.svg` and the inline SVG
  in `header()` / `footer()`.

## SEO / GEO notes already implemented

- Unique title + meta description + canonical on every page.
- JSON-LD: `EmploymentAgency`/`LocalBusiness`/`Organization` sitewide,
  `Service` per vertical, `FAQPage` on 10 pages, `BreadcrumbList` on interiors.
  FAQ answers are written as direct, quotable answers — that's the AEO play.
- Semantic heading order, skip link, breadcrumbs, alt/aria on interactive bits.
- `robots.txt` explicitly allows GPTBot, OAI-SearchBot, PerplexityBot,
  ClaudeBot, and Google-Extended.
- No render-blocking JS, one stylesheet, one deferred script, SVG favicon,
  system-fallback font stacks.

**Not yet done:** the 301 redirect map off the GoDaddy site (SOW §2.3a) — that
needs a crawl of the current site's live URLs before cutover.

## Local preview

```bash
cd clients/sublime-personnel/website
python3 -m http.server 8899
# http://localhost:8899
```

## Facts sourced from the client (do not invent more)

Founded 2010 by Terry Richards · Terry recruiting since 2006 · Pete Proctor,
30+ yrs restaurant operations, 2 yrs corporate recruiter at a high-rise property
management firm · 713-396-0944 · Greater Houston Area, recruits nationwide ·
sliding-scale fees · 30-day guarantee on direct hire · direct hire, temp-to-hire,
temp · ~12,000 LinkedIn network · seven verticals per SOW §2.2b.

No placement counts, revenue figures, client names, or testimonials appear
anywhere on the site — nothing we can't back up.
