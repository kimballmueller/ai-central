# PowerHouse Estimator & Proposal Maker

Single self-contained HTML file. No build step, no dependencies, no server. Double-click `index.html`
or host it at a private URL. Works offline (Google Fonts degrade to system fallbacks).

White paper, black ink, red accent — matched to the PowerHouse brand. Both logos are embedded as
base64 data URIs (the red **PH** monogram for white surfaces, the full white/red wordmark for black
ones), so the file stays portable with no asset folder to keep alongside it. If the logo files in
`website/assets/` ever change, re-embed them.

Built from `KIMBALL_Powerhouse Estimator .xlsx` (Yasir, 2026-07-28).

## Two modes

**Build** — the rep's cockpit. Enter the nine measurements off an EagleView/Hover report, pick up to
three systems, see cost / price / profit / margin live. Every line item is editable.

**Proposal** — what the homeowner sees. Three tiers side by side, middle one highlighted, scope of
work, process, signature block. `Save as PDF` prints it clean. No cost or margin data ever appears
in this mode.

Keyboard: `1`–`7` toggle systems, `P` proposal, `B` build.

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

## Data

Autosaves to browser `localStorage` (key `phx-estimator-v1`) — one job at a time. `Export` dumps a
CSV of all seven systems. `New job` clears.

## Before this goes to a homeowner

- Warranty copy is generic and conservative on purpose. Confirm exact GAF / CertainTeed terms.
- The tool is internal — it exposes cost and margin. Do not put it on the public site.
