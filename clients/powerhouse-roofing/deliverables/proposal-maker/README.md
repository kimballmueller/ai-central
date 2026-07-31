# PowerHouse Estimator & Proposal Maker

Single self-contained HTML file. No build step, no dependencies, no server. Double-click `index.html`
or host it at a private URL. Works offline (Google Fonts degrade to system fallbacks).

White paper, black ink, red accent — matched to the PowerHouse brand. Both logos are embedded as
base64 data URIs (the red **PH** monogram for white surfaces, the full white/red wordmark for black
ones), so the file stays portable with no asset folder to keep alongside it. If the logo files in
`website/assets/` ever change, re-embed them.

Built from `KIMBALL_Powerhouse Estimator .xlsx` (Yasir, 2026-07-28), plus the DOPL license, the
signed Customer Agreement and the warranty certificate in `clients/powerhouse-roofing/Assets/`.

## Two modes

**Build** — the rep's cockpit. Enter the nine measurements off an EagleView/Hover report, pick up to
three systems, see cost / price / profit / margin live. Every line item is editable.

**Proposal** — what the homeowner sees. Three tiers side by side, middle one highlighted, scope of
work, payment and financing, the warranty, process, signature block, license. `Save as PDF` prints it
clean over seven pages. No cost or margin data ever appears in this mode.

Keyboard: `1`–`7` toggle systems, `P` proposal, `B` build.

## Sales tax

**PowerHouse does not charge the homeowner sales tax.** A roof is a real-property improvement, so the
contractor is the end consumer and pays tax at the supplier counter. Tax therefore lives in *cost*,
never on the price — and it always did in this tool. The proposal now says so out loud, in three
places: a badge above the tiers, a line under each price, and the "Paying for it" section.

The workbook baked four different rates (7.5 / 7.6 / 7.7 / 8.5%) into individual unit prices. That is
still a real inconsistency, so the **Supplier tax on materials** panel lets you restate them all at
once: set the rate the sheet assumed and the rate that is actually true, and every material unit cost
is scaled between them. Leave *Actual rate* blank and nothing re-prices. Disposal, roof load, rollout
and kettle are treated as services and left alone. `Match original spreadsheet` ignores the panel
entirely, so the comparison stays honest.

## Financing

PowerHouse finances through **Service Finance Company** (svcfin.com) and **Slice® by FNBO**
(fnbo.com/pos-lending/slice). Both appear in the proposal's payment section with their real published
terms — Slice is up to $150,000, out to 20 years, 8.49%–18.99% APR depending on credit and AutoPay.

The **Payment & financing** panel drives an estimated monthly payment on every tier: pick APR, term
and any amount down. It is a level-payment amortization, shown alongside the amount financed, the APR
and the term, and labelled an estimate rather than an offer — a monthly payment shown without those
figures is a Reg Z problem. Set *Monthly payment estimates* to **Hide** if a rep would rather not show
one. The lender sets the real terms on approval; nothing here is an approval.

## Pricing engine

Seven systems carried over from the workbook tabs. **Unit costs are the workbook's own evaluated
values, including the tax multipliers baked into the formulas — nothing was re-priced.**

The `Engine` dropdown under *Rates & margin* switches between:
- **Corrected math** (default) — the fixes listed below
- **Match original spreadsheet** — prices exactly as the .xlsx would, for comparison

The **Spreadsheet audit** panel at the bottom of the board shows every correction with its dollar
impact on the job currently loaded, plus judgment calls that were deliberately *not* auto-changed.

### Fixed
- Material lines that were priced but never summed (counter flashing, valley metal, ridge vent,
  Quarrix plugs, OSB, 4" galv, ISO insulation, TPO screws) now reach the total
- HDZ / UHDZ measurement refs: starter was reading valleys, ice & water was reading ridge,
  drip edge was reading valleys, L-metal was reading sidewall
- Headwall now reaches HDZ / UHDZ (was pointed at an empty cell, `B18`)
- Flat sq ft now reaches the Natural Shadow TPO kit (was never linked)
- Presidential roof-load total now multiplies by quantity
- Piece counts round up on the piece, not on the linear feet — no more 3.7 sticks of drip edge
- Profit no longer subtracts Company OPS after it was already added to the price
- HydroTech and TPO price off the low-slope area, not the steep-slope field
- Proposal summary refs corrected; TPO included

### Flagged, not changed
Read the audit panel in the app. The two that matter most:

1. **The recovered lines were never validated.** They were priced but never summed, so nobody had a
   reason to check their formulas. Quarrix plugs is the worst offender — it orders one plug per stick
   of ridge vent on three tabs. Check these with Yasir before quoting off them.
2. **Recovering those costs raises price-per-square 20–30% on steep-slope jobs.** That is real cost
   surfacing, not a markup. But validate the new $/sq against jobs actually being won. If it lands
   high, adjust the margin divisor — don't go back to leaking cost.

Also flagged: three definitions of "square" across tabs, four hard-coded tax rates, Presidential has
no ice & water line, disposal priced three ways, TPO runs on different labor/commission rules.

3. **Decking is quoted at cost here and at $100 a sheet in the contract.** The Customer Agreement
   fixes plywood/OSB at $100 per sheet; the estimator carries OSB at $18.67 cost, so a sheet you
   quote up front lands near $29 to the homeowner. Sheets found *after* tear-off are a separate
   transaction billed at contract rate, so this is not automatically wrong — but if a job is expected
   to need decking, override the OSB unit in the drawer.

## Company facts

Everything the proposal asserts about PowerHouse lives in the `CO` object at the top of the script —
license number, address, phone, deposit percentage, card fee, decking rate, warranty term. Change it
there, not in the markup. Current values come from:

- **DOPL license** — Powerhouse Roofing LLC, 1154 S 420 W, Salem UT 84653. License #11494924-5501,
  classifications B100 and S280, active through 11/30/2027.
- **Customer Agreement** — 50% deposit at signing on cash deals, balance at Substantial Completion,
  3% card convenience fee, $100 per added sheet of plywood/OSB, $1,000 threshold for a written change
  order, three-day right to cancel, 10-year workmanship warranty.
- **Warranty certificate** — the 10-year workmanship language is reproduced in its own section.

## Data

Autosaves to browser `localStorage` (key `phx-estimator-v1`) — one job at a time. `Export` dumps a
CSV of all seven systems, now including the estimated monthly payment, term and APR. `New job` clears.
A job saved before the tax and financing settings existed loads fine — `load()` merges one level down
so it picks up the new defaults.

## Before this goes to a homeowner

- Manufacturer warranty copy is still generic and conservative on purpose. Confirm exact GAF /
  CertainTeed terms. Our own workmanship warranty is now the real language from the certificate.
- The default financing illustration is **9.99% APR over 120 months**, which is a placeholder. Get
  the plans Powerhouse is actually enrolled in from each lender and set a real default.
- The tool is internal — it exposes cost and margin. Do not put it on the public site.
