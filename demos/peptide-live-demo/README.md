# Live scraper demo — 10 of Brandon's real vendors

Built 2026-08-06 for the Brandon Schubert call. **Nothing here is mock data.**

## Run it

```bash
python3 demos/peptide-live-demo/scrape.py        # ~5 min, hits 10 vendor APIs
python3 demos/peptide-live-demo/export_xlsx.py   # -> Peptide_Prices_LIVE.xlsx
python3 demos/peptide-live-demo/build_site.py    # -> index.html
open demos/peptide-live-demo/index.html
```

## What it proves

One sweep → one database → three outputs. That's the whole architecture, at 1/9th scale.

```
10 vendor APIs ──▶ SQLite ──┬──▶ index.html   (the site)
                            ├──▶ .xlsx        (his sheet, generated)
                            └──▶ price_changes (drives alerts)
```

| Last sweep | |
|---|---|
| SKUs priced | 680 |
| Vendors | 10 of 92 |
| Compounds | 64 |
| On sale right now | 99 |
| Out of stock | 105 |
| Sweep time | **321 seconds** |

**No browser automation.** All 10 vendors run on WooCommerce and publish price,
sale price and stock status through `/wp-json/wc/store/products`. His SOW assumed
Playwright clicking size dropdowns for all 92; 11 of the 12 vendors probed don't
need a browser at all.

## Files

| | |
|---|---|
| `scrape.py` | Tier-A collector, compound matching, size parsing, SQLite writer |
| `export_xlsx.py` | Workbook in his v3 shape + Price History + Changes tabs |
| `build_site.py` | Single self-contained HTML page, data inlined |
| `prices.db` | SQLite. `price_snapshots` is append-only |
| `index.html` | 99 KB, zero external requests — works offline |

The page makes no network calls and loads no webfonts (uses macOS's New York and
SF Mono). It cannot fail on call-day wifi.

## Three bugs found and fixed while building this

Worth knowing, because two are the same class of error found in his v50 sheet.

1. **Blends assigned to a component.** Naive longest-string matching labels
   `GLOW (GHK-CU, TB-500, BPC-157)` as `BPC-157`, because `bpc-157` is a longer
   string than `glow`. 18 blend products were mislabelled. Fixed by resolving
   composition first — his `SCRAPE.md` says *"Match on composition, not just the
   trade name."*

2. **mg double-counted.** `GLOW (70MG/10MG/10MG) 90MG VIAL` summed to 180mg for a
   90mg vial. Identical to the `54mg (27mg+27mg) → 108mg` bug in his own helper
   column. Fixed by treating a figure that equals the sum of the others *and is
   strictly the largest* as the stated total. The "strictly largest" guard matters:
   without it `10mg/10mg` looks like a total and halves the real figure.

3. **Spelled-out units.** `TB-500 ... 2MG/5MG/10MG VIAL` lists three size options
   and the variant label says `2-milligram`. The parser only knew `mg`, so it fell
   back to the parent name and summed the options — 17mg for a 2mg vial, which put
   Umbrella Labs falsely near the top of the TB-500 ranking at $2.00/mg when the
   real figure is $17/mg.

## Honest limits — say these out loud

- **10 vendors, not 92.** The remaining 82 are configuration, not new code.
- **Price history has one timestamp.** Real history needs sweeps across days.
  The `Changes` tab is empty and says so. Nothing was seeded to fake it.
- **Compound matching is good, not perfect.** 680 of 769 SKUs carry a usable mg
  figure; the rest are liquids, capsules and unlabelled blends that need his
  four-METHOD schema and, in a few cases, his decision.
- **Duplicate listings survive.** Some vendors list the same SKU twice; the real
  build dedupes on `(vendor, compound, method, size, units)`.
