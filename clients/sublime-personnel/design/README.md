# Sublime Personnel — design prototype (Phase 1)

**This is not the shipped site.** It's a throwaway static shell whose only job is to
lock the aesthetic and the conversion path before we build the WordPress block theme
(Phase 3 of the plan). Fourteen pages — enough to approve a design system, a funnel and
the site's shape.

- `index.html` — homepage (the only hand-maintained page; everything else is generated)
- `clients.html` — For Employers
- `candidates.html` — For Candidates
- `blog.html` — Insights, built from their real live posts
- `start-a-search.html` — four-step employer intake (the primary conversion path)
- `cost-of-vacancy.html` — live fee/vacancy calculator
- `talent-network.html` — candidate capture
- `industries/*.html` — all seven practice areas

Everything except `index.html` is generated:

```bash
python3 _build/pages.py && python3 _build/bust.py
```

`_build/pages.py` owns the markup, `_build/industries.py` owns the practice-area copy
(that file is the one Pete edits). Both `head()`/`header()`/`footer()`/`cta_band()` take
`d=` — the directory depth — so pages inside `industries/` get `../` prefixes. Practice
pages link to each other with no prefix at all, since they are siblings; that was a real
bug the link crawler caught, so if you add a depth-2 directory, re-run the crawler.

## Previewing

**Use the no-cache server, not `python3 -m http.server`.**

```bash
cd clients/sublime-personnel/design
python3 _build/serve.py          # http://localhost:8901
```

Plain `http.server` lets the browser cache `styles.css`. When a change renames a CSS
selector *and* the markup at the same time — as the H1/H2 swap did — a stale stylesheet
against new markup renders the hero with no colours and no layout at all. It looks like
the design broke; nothing is wrong on disk. This cost us a review cycle once already.

Belt and braces: `_build/bust.py` stamps every asset link with a content hash
(`styles.css?v=c496def0`). **Re-run it after editing anything in `assets/`:**

```bash
python3 _build/bust.py
```

## The direction

Type-led, after **[retsusa.com](https://retsusa.com)**. The headline *is* the design —
which is what lets this look expensive with no photography budget. Supporting moves:
the authority bar from [Jacobson](https://jacobsononline.com), the activity stat band
from [Kimmel](https://www.kimmel.com), the audience-fork panels from
[Goodwin](https://goodwinrecruiting.com) (their structure, not their stock photos), and
the operator-credibility copy angle that [Gecko](https://www.geckohospitality.com)
leads with — because it's Pete's actual biography.

## Brand

Colors sampled off the existing logo, kept per the Aug 13 call ("original logo retained
with a modern update"):

| | |
|---|---|
| `--blue` `#174591` | logo blue, unchanged |
| `--green` `#6EB43B` | logo green, unchanged |
| `--green-deep` `#4E8A28` | the modern-update tone, used for anything that carries text |
| `--ink` `#0C1A2E` | near-black navy derived from the blue |

**`#6EB43B` is 2.5:1 on white and can never carry text** — only hairline rules, chevron
bullets, icon strokes, and text on dark surfaces. Every text use is `--green-deep`
(4.2:1) or darker. This is enforced by hand, so check it on any new component.

The mark in `assets/mark.svg` is a **flat redraw** of the existing petal burst — the
plaque, bevel and drop shadow are gone. It's an approximation generated from a
screenshot; **replace it with the real vector when Pete sends the logo files.**

Type: **Archivo** (display, width axis pushed to ~110) + **Inter** (UI). We started on
Bodoni Moda for the RETS look and dropped it — a Didone's hairlines are the whole design
*and* the whole legibility problem. Every top converter in this niche uses a sans.

## The hero fill

The middle line uses `background-clip: text` over a layered gradient. Every declared
stop is ≥3:1 on white (verified — the large-text bar), and there's a solid-blue
`@supports` fallback.

Swapping in real photography later is **one line** — replace the `background-image` on
`.hero h1 .fill` with a `url()`. A letterform mask hides ~90% of the source image, which
is why even mediocre stock reads as intentional here.

## Positioning & voice

The site sells one thing: **lead generation for employers who are deciding whether to
use a recruiting firm.** Everything else is subordinate to that.

**What we do not lead with:** the number of industries. "Seven industries" is not a
search term and nobody buys on breadth — it reads as a firm spread thin rather than a
firm that is the best at anything. The industry *names* carry real search volume, so
they live in the meta description, the practice cards and the vertical pages. The
homepage targets the head term (*executive search firm Houston*) through the subhead,
the authority bar and the title tag.

**The hero** follows one rule: three seconds to learn what we do and why it matters,
and exactly one obvious next step.

- **H1 — "The hire you can't afford to get wrong."** The buyer's stakes, not our
  biography. It positions Sublime as the firm you use when the consequence is real,
  which is how a boutique claims "best" without saying it.
- **Subhead carries the head term** — "Sublime Personnel is an executive search firm in
  Houston" — so the SEO work is done by the sentence that also does the selling.
- **One button.** `Start a search`. The header CTA points at the same place.
- **Candidates get a quiet text link**, not a competing button. Pete's bottleneck is
  clients, not candidates — he has 12,000 people in his network and told us sourcing is
  the easy part. A candidate button of equal weight splits attention away from the only
  action that generates revenue.
- Nav cut from five items to three; the "For Employers"/"For Candidates" anchor jumps
  were pulling against the primary action.

**Heading semantics.** The kicker is the `<h1>` and the giant display line is an `<h2>`.
The head terms therefore sit in the H1 ("Executive Search & Recruiting · Greater Houston
· Since 2010") while the visual hook stays visually dominant. Nothing is hidden — the
text is fully visible, just small, which is a legitimate pattern rather than cloaking.
Be realistic about the size of the win: Google weights H1 far less than it once did, and
the title tag, page copy and internal links do more work. It costs nothing, so it is
worth doing.

Because the styling was tied to tag names, this needed decoupling: the display rules now
hang off `.hero-display`, and `.eyebrow` resets the heading defaults itself so it renders
as a small Inter kicker even as an `<h1>`.

Promoting the display line to `<h2>` exposed six pre-existing `h2 -> h4` level skips in
card and callout titles across the site. Those are now `<h3 class="minor-head">`, which
keeps the appearance and gives every page a clean outline with no skipped levels.

Before this pass the opening had **11 distinct destinations** and two equal-weight hero
buttons pointing in opposite directions.

**Voice:** assured and precise, not chatty. The first draft was too knowing — "no
form-fill purgatory", "we'd rather tell you now", "that's in, thanks". A firm that
charges for judgement should sound like it has some. Directness stays; the winking
does not.

> The hero line sizes are **measured, not guessed**: for the current headline the three
> lines render 911 / 962 / 1031px at a common size, so each is scaled to match the
> narrowest — verified to 0.01% spread. **If the headline wording changes, re-measure**
> or the type block stops justifying. See Tests below for how.

## The funnel

Five pages now, not two — the brochure pages plus three conversion surfaces:

| Page | What it does |
|---|---|
| `start-a-search.html` | Four-step employer intake. Step 3 asks hires-per-year, which qualifies against Pete's ICP ("clients who can digest our services four times a year"). Partial data POSTs at every step, so an abandon is still a lead. Progress survives a refresh via sessionStorage. |
| `cost-of-vacancy.html` | Live calculator: what the empty seat costs per day vs. the fee. Email capture is *after* the number, not in front of it. |
| `talent-network.html` | Candidate capture, replacing job applications. |

Every `mailto:` and bare `tel:` primary CTA is gone; the hero, the fork, the industry
cards and the closing band all route into the funnel. CTAs escalate by scroll depth:
book/start at the top, calculator mid-page.

**Calculator math** (`assets/funnel.js`): daily cost = (salary × multiplier) ÷ 260
working days. The 15–20% fee band is Pete's own from the transcript — *"not all those
clients are going to come in at 20%, so I'm going to come in at 15."* The multiplier
defaults to a conservative 1.0× and is user-adjustable, and the assumptions are printed
on the page under "How we calculate this". No invented statistics.

**Wiring it up:** one constant, `CFG.ENDPOINT` at the top of `assets/funnel.js`. Every
form and every partial step POSTs there as JSON. Until it's set, submissions log to the
console and the UI still completes so the prototype is testable.

**Analytics:** `track()` fires a GA4 event on every step view, step completion, submit,
and calculator adjustment — so you can see *where* people drop, not just that they did.
Required by SOW §2.3e; §4 promises attributed leads by month 4.

## Partner portraits

`assets/img/pete.jpg` and `assets/img/terry.jpg` — pulled from the client's own About
page on their wsimg CDN, at the crop framing their existing site uses, re-rendered at
600px and optimised to 440px / ~40KB each.

They sit in a square frame with a brand-green hairline underneath, sized 136px so two
partners read as a real firm rather than an afterthought. The two source crops sit
differently in frame, so Terry's carries `.crop-high` to stop the top of his head being
clipped — check both if either image is ever replaced.

**Source note:** these came off the live site, not from Pete directly. Worth confirming
he is happy with them before launch; his is captioned "No Edit" in the filename.

## What's deliberately not here

About, Privacy, sitemap, and JSON-LD schema. There is no `industries.html` hub either —
the nav dropdown and the homepage practices grid (`index.html#industries`) do that job,
and the crumbs point there. Add a hub only if Pete wants one.

The practice-page copy was rewritten into the design voice in `_build/industries.py`.
The research behind it came from `../website/_build/build.py`, which also still holds the
JSON-LD, the About copy and the utility pages — carry those into the WordPress build
rather than rebuilding them.

No job board (v1 decision). RETS, Gecko, Goodwin and Patrice all lead with live jobs —
it's the biggest candidate-conversion and fresh-content SEO lever, and skipping it is a
real tradeoff worth revisiting at v2.

Not built, and worth doing: gated vertical salary guides for lower-intent visitors
(Jacobson's whole content engine is their Labor Market Study), and speed-to-lead
automation — form → GHL → instant SMS to Pete. That last one lives outside the website
and is probably the single highest-leverage thing on this list.

## Tests

`_build/tests/` — run the lot with `./_build/tests/run.sh` (start `serve.py` first;
the runner launches and cleans up its own headless browser).

| Suite | What it holds down |
|---|---|
| `links.py` | Every internal `href`/`src` and every CSS `url()` resolves; every practice page is linked from every page. **The only check that catches a bad `../`** — run it after any change to page depth. |
| `pages.mjs` | All 14 pages: exactly one H1, correct kicker and display sizing, no skipped heading levels, clean console. |
| `industries.mjs` | The 7 practice pages are structurally identical — 9 roles, 4 screening steps, 4 FAQs, 3 related cards, gradient fill in the H1, a loaded photograph in the band, correct `NN of 07`, no ghost button dark-on-dark. |
| `images.mjs` | Every `<img>` resolves with lazy images forced to load, and every page stays inside its weight budget (600KB; 1100KB for the homepage, which carries the practice-card set). |
| `funnel.mjs` | 39 assertions driving the conversion paths end to end: step advance, per-step validation, back-navigation retaining answers, email format, the confirmation state, sessionStorage clearing, every calculator output at two input sets, and both simple forms. |

They drive headless Chrome over CDP on Node 22's built-in WebSocket — no dependencies
(Playwright was locked by another session when this was written). `_cdp.mjs` is the
shared driver; `CDP_PORT` and `BASE` override the defaults.

Two traps worth knowing, both of which produced silently passing tests here:

- **The wizard restores sessionStorage.** Clear it before asserting on step state or
  every step assertion is meaningless.
- **Assert on the interpolated node, not the panel text.** The confirmation copy
  mentions Pete either way, so `textContent.includes('Pete')` passes whether or not
  the name was ever filled in. Assert on `[data-name]`.

## Insights (blog)

Their blog is live and posting roughly weekly. `blog.html` is built from the ten real
posts captured in `_build/blog-posts.md`; articles currently link out to the live site
since we do not have post bodies.

Their version is a bare reverse-chron list — date, title, truncated excerpt, "Continue
Reading", and no way out of the page. Ours adds a featured lead post, a practice tag per
article, a three-up card grid, and a hand-off into the calculator and the intake form, so
the blog feeds the funnel instead of dead-ending. Deliberately no read-time estimates: we
do not have the post bodies, and inventing them would be fabrication.

**Still worth doing:** their blog publishes **"187 hires in 22 months"** — a real, public,
client-owned figure that is stronger than anything currently in the homepage stat band.

## Heading pattern

The homepage is the one exception: its kicker is the `<h1>` (so the head terms sit in it)
and the display line is an `<h2 class="hero-display">`. Every interior page does the
conventional thing — kicker is a `<p class="eyebrow">`, and the descriptive line is the
`<h1 class="phead-display">`, which is both better for keywords and matches the practice
pages. Sizing is class-scoped, never tag-scoped; tag-scoped rules were what broke twice.

## The redrawn mark (superseded)

`assets/mark.svg` was redrawn from a screenshot before the real logo was available:
the elements are **people** (tapered torso, flat shoulders, separate round head) fanned
across a half circle. It is now only the favicon — see **Logo** below for what the header
and footer actually use.

## Still blocked

See the plan at `~/.claude/plans/go-find-the-best-velvety-sonnet.md`. The big one:
the **Aug 13 onboarding transcript is not in the repo**, so the medical vertical, the
parallel recruiting site, and the logo direction all rest on a six-bullet email recap.
Export it before Phase 3.

**The practice list is still unconfirmed and it is now load-bearing** — seven pages, the
`NN of 07` numbering, the nav, the footer and the cross-links all read off one list in
`_build/pages.py`. Three sources disagree: the SOW says seven including QSR/franchise,
their live homepage says "07 Oil and Gas", and their blog says five (HOA, hospitality,
insurance, accounting, construction). The Aug 13 recap adds a medical vertical as an
eighth. Pete has to settle this. Changing it later is cheap — edit `VERTICALS` and
`INDUSTRIES` and rebuild — but every number on every page moves with it.

## Interior page heads

`.phead` is deliberately a scaled-down copy of `.hero`, not its own composition:
centred, same blue radial wash, same rule-flanked eyebrow, same `.fill` gradient
on the emphasis phrase. The `.fill` rule is unscoped for exactly this reason — the
homepage and every interior page share one mechanic, which is what stops the
interior pages reading as a different site. `box-decoration-break: clone` is on it
so a phrase that wraps gets the full ramp per line instead of one sliced box.

When adding a page head: `<p class="eyebrow center">` + `<h1 class="phead-display">`
with `<span class="fill">` around the phrase that carries the promise, then
`<div class="btns center">` and one quiet `.alt-path`. Spacing comes from the
stylesheet — no inline `margin-top`.

## Photography

Ten licensed stock photographs (Unsplash — free for commercial use, no attribution
required), in `assets/img/`. Sources and picks are deliberate: a working kitchen line
rather than a plated dish, a rebar deck with field leaders on it rather than a crane
at sunset, a packed trailer yard for commercial lines. The brief was *the work*, not
people smiling in a meeting room — that stock cliché is the exact failure the plan
called out on Goodwin.

**They are all treated the same way, and that is the whole trick.** Each image is
desaturated, then a blue-to-green brand gradient is multiplied over it. One duotone
across ten unrelated photographs is what makes them read as a commissioned shoot
rather than a picture library. Retune `.shot::after` in the stylesheet and every
photograph on the site follows.

| Where | Files | Notes |
|---|---|---|
| Practice page bands | `<practice>.jpg`, 1800×620 | Full-bleed, between the page head and "why us" |
| Homepage practice cards | `<practice>-card.jpg`, 760×320 | Sized to what actually renders (376×158 CSS px at 2×) |
| Homepage cost section | `houston.jpg`, 2000×760 | Behind Pete's quote at ~38% under a near-opaque overlay — texture, not an image, so the text contrast does not move |
| Audience fork | `employers.jpg`, `candidates.jpg` | CSS backgrounds under a 92–97% flat colour |

All are decorative and carry empty `alt` — the copy says everything the photographs
would. Total 1.8MB across the site; `images.mjs` holds the per-page budget.

## Logo

**Temporary, and it is the client's real one.** Lifted from the live GoDaddy site
(`img1.wsimg.com/isteam/ip/5562da6e…/blob.png`) at 1600px:

- `logo-original-source.png` — untouched original, plaque and all
- `logo.png` — trimmed plaque lockup, exactly as it appears on their site today
- `logo-flat.png` — **in use in the header.** Same artwork with the glass plaque
  knocked out, because at 46px the plaque renders as a grey box on a white header
  and "PERSONNEL" becomes unreadable
- `logo-flat-light.png` — **in use in the footer.** Knockout for dark surfaces:
  wordmark to white, mark to the lighter brand green
- `mark.svg` / `favicon.svg` — the redrawn mark, still the favicon; a 16px crop of
  the plaque is unreadable

To go back to the full plaque, point the header `<img>` at `logo.png` in
`_build/pages.py` and `index.html` and rebuild — one line in each.

**Still needed from Pete: the logo as a vector.** Everything above is a raster lift
from a 1600px PNG, which is fine for the prototype and not fine for the WordPress
build or for print.
