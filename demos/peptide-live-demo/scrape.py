#!/usr/bin/env python3
"""
Live proof-of-concept: scrape 10 of Brandon's real vendors via the public
WooCommerce Store API, land it in SQLite, and fan out to a site + an Excel sheet.

The point being demonstrated: these storefronts publish price, sale price and
stock status as JSON. No headless browser, no dropdown clicking. His SOW assumed
Playwright for all of it; 11 of 12 vendors probed don't need it.

  python3 demos/peptide-live-demo/scrape.py --db demos/peptide-live-demo/prices.db

Polite by construction: 1 request/sec/domain, honest UA, small concurrency.
These are small shops his tracker sends buyers to -- getting banned would cost
him the affiliate relationships, not just the data.
"""

import argparse
import json
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

# All confirmed to expose /wp-json/wc/store/products.
VENDORS = [
    ("Bulk Peptide Wholesale", "bulkpeptidewholesale.com"),
    ("Modern Aminos",          "modernaminos.com"),
    ("SwissChems",             "swisschems.is"),
    ("Core Peptides",          "www.corepeptides.com"),
    ("Ascension Peptides",     "ascensionpeptides.com"),
    ("Nexaph",                 "nexaph.com"),
    ("Welli Labs",             "wellilabs.com"),
    ("Peptidology",            "peptidology.co"),
    ("Umbrella Labs",          "umbrellalabs.is"),
    ("Simple Peptides",        "simplepeptide.com"),
]

# Brandon's canonical compounds (SCRAPE.md). Order matters only for reporting;
# matching is longest-alias-wins so blends beat their components.
COMPOUNDS = [
    "5-Amino-1MQ", "Adamax", "AOD9604", "ARA-290", "Bacteriostatic Water", "BPC-157",
    "BPC157+TB500 Blend (Wolverine)", "BPC157+TB500+Cartalax Blend (Deadpool)",
    "BPC157+TB500+KPV Blend (Wolverine 2)", "Bromantane", "Cagrilintide", "Cartalax",
    "Cerebrolysin", "CJC-1295 No DAC", "CJC-1295 No DAC + Ipamorelin Blend",
    "CJC-1295 w/DAC", "Dihexa", "DSIP", "Eloralintide", "Epitalon", "Follistatin-344",
    "FOXO4", "GHK-CU", "GHK-CU+TB500+BPC157 Blend (GLOW)",
    "GHK-CU+TB500+BPC157+KPV Blend (KLOW)", "GHRP-2", "GHRP-6", "Glutathione",
    "HCG (IUs)", "Hexarelin", "HGH Fragment 176-191", "Humanin", "IGF-1LR3",
    "Ipamorelin", "KissPeptin-10", "KPV", "KPV+GHK-CU Blend", "L-Carnitine", "LL37",
    "MOTS-C", "MT-1", "MT-2", "NAD+", "NAD++Mots-C+5-Amino-1MQ Blend (Triple Helix)",
    "Oxytocin", "P-21", "Pinealon", "PT-141", "Retatrutide (GLP3-R)",
    "Retatrutide + Cagrilintide Blend", "Selank", "Selank+Semax Blend",
    "Semaglutide (GLP1-S)", "Semax", "Sermorelin", "SLU-PP-332", "SLU-PP-915",
    "SNAP-8", "SS-31", "TB-500", "Tesamorelin", "Tesamorelin+Ipamorelin Blend",
    "Tesofensine", "Testagen", "Thymalin", "Thymosin Alpha-1",
    "Thymosin Alpha-1+Thymalin Blend", "Tirzepatide (GLP2-T)", "Vilon",
    "VIP (Vasoactive Intestinal Peptide)",
]

# Aliases from SCRAPE.md's name-mapping tables (GLP code names, Zesty Rat
# nomenclature, blend trade names). Matched longest-first.
ALIASES = {
    "Semaglutide (GLP1-S)": ["semaglutide", "glp-1", "glp1", "glps", "sema"],
    "Tirzepatide (GLP2-T)": ["tirzepatide", "glp-2", "glp2", "glpt", "tirz", "trizeppy"],
    "Retatrutide (GLP3-R)": ["retatrutide", "glp-3", "glp3", "glpr", "reta", "ly3437943"],
    "Cagrilintide": ["cagrilintide", "cagri", "am833"],
    "Tesamorelin": ["tesamorelin", "th9507"],
    "Ipamorelin": ["ipamorelin", "nnc 26-0161"],
    "Sermorelin": ["sermorelin", "ghrh 1-29"],
    "Hexarelin": ["hexarelin", "ep-23905"],
    "GHRP-2": ["ghrp-2", "ghrp2", "kp-102"],
    "MT-2": ["mt-2", "mt2", "mt-ii", "melanotan 2", "melanotan-2", "melanotan ii"],
    "MT-1": ["mt-1", "mt1", "melanotan 1", "melanotan-1"],
    "Oxytocin": ["oxytocin", "ot 9 amino"],
    "Selank": ["selank", "tp-7"],
    "Semax": ["semax", "actch (4-7)"],
    "KissPeptin-10": ["kisspeptin-10", "kisspeptin", "kp-10"],
    "GHK-CU": ["ghk-cu", "ghk cu", "ghkcu", "ghk-copper"],
    "BPC-157": ["bpc-157", "bpc157", "bpc 157"],
    "TB-500": ["tb-500", "tb500", "tb 500"],
    "NAD+": ["nad+", "nad plus", "nad"],
    "HCG (IUs)": ["hcg"],
    "AOD9604": ["aod9604", "aod-9604"],
    "IGF-1LR3": ["igf-1 lr3", "igf-1lr3", "igf1 lr3", "igf-1 des"],
    "HGH Fragment 176-191": ["hgh fragment", "frag 176-191", "hgh frag"],
    "Thymosin Alpha-1": ["thymosin alpha-1", "thymosin alpha 1", "ta-1", "taa-1"],
    "Epitalon": ["epitalon", "epithalon"],
    "L-Carnitine": ["l-carnitine", "carnitine"],
    "Glutathione": ["glutathione", "gsh"],
    "Bacteriostatic Water": ["bacteriostatic water", "bac water", "bacteriostatic"],
    "P-21": ["p-21", "p21"],
    "SS-31": ["ss-31", "ss31", "elamipretide"],
    "MOTS-C": ["mots-c", "motsc", "mots c"],
    "5-Amino-1MQ": ["5-amino-1mq", "5 amino 1mq", "5amino1mq"],
    "CJC-1295 No DAC + Ipamorelin Blend": [
        "cjc-1295 no dac + ipamorelin", "cjc1295/ipamorelin", "cjc-1295/ipamorelin",
        "cjc 1295 ipamorelin", "cjc-1295 without dac + ipamorelin", "cjc/ipa"],
    "CJC-1295 No DAC": ["cjc-1295 no dac", "cjc-1295 without dac", "cjc1295 no dac"],
    "CJC-1295 w/DAC": ["cjc-1295 with dac", "cjc-1295 w/dac", "cjc1295 dac"],
    "GHK-CU+TB500+BPC157 Blend (GLOW)": ["glow"],
    "GHK-CU+TB500+BPC157+KPV Blend (KLOW)": ["klow"],
    "BPC157+TB500 Blend (Wolverine)": [
        "wolverine", "bpc-157/ tb-500", "bpc-157/tb-500", "bpc157/tb500",
        "bpc-157 + tb-500", "bpc/tb"],
    "BPC157+TB500+KPV Blend (Wolverine 2)": ["wolverine 2", "wolverine2"],
    "BPC157+TB500+Cartalax Blend (Deadpool)": ["deadpool"],
    "NAD++Mots-C+5-Amino-1MQ Blend (Triple Helix)": [
        "triple helix", "trinity", "mitochondrial powerhouse"],
    "Selank+Semax Blend": ["selank + semax", "selank/semax", "semax + selank"],
    "Tesamorelin+Ipamorelin Blend": ["tesamorelin + ipamorelin", "tesamorelin/ipamorelin"],
    "Thymosin Alpha-1+Thymalin Blend": ["thymosin alpha-1 + thymalin"],
    "KPV+GHK-CU Blend": ["kpv + ghk-cu", "ghkpv", "kpv/ghk"],
    "Retatrutide + Cagrilintide Blend": ["retatrutide + cagrilintide", "reta/cagri", "reta + cagri"],
    "VIP (Vasoactive Intestinal Peptide)": ["vasoactive intestinal", "vip"],
}

# Anything matching these is not a tracked compound (SCRAPE.md R10).
JUNK = re.compile(
    r"t-?shirt|hoodie|hat|sticker|apparel|syringe|needle|swab|alcohol pad|"
    r"gift card|shipping|insurance|bundle builder|sample pack|book|guide|"
    r"test kit|scale|vial rack|cap|stopper", re.I)

_alias_index = None


def alias_index():
    """(needle, canonical) sorted longest-first so blends win over components."""
    global _alias_index
    if _alias_index is None:
        pairs = []
        for c in COMPOUNDS:
            pairs.append((c.split(" (")[0].casefold(), c))
            pairs.append((c.casefold(), c))
        for canon, names in ALIASES.items():
            for n in names:
                pairs.append((n.casefold(), canon))
        _alias_index = sorted(set(pairs), key=lambda p: -len(p[0]))
    return _alias_index


BLEND_TRADE = {
    "glow": "GHK-CU+TB500+BPC157 Blend (GLOW)",
    "klow": "GHK-CU+TB500+BPC157+KPV Blend (KLOW)",
    "wolverine 2": "BPC157+TB500+KPV Blend (Wolverine 2)",
    "wolverine": "BPC157+TB500 Blend (Wolverine)",
    "deadpool": "BPC157+TB500+Cartalax Blend (Deadpool)",
    "triple helix": "NAD++Mots-C+5-Amino-1MQ Blend (Triple Helix)",
}

# Component set -> canonical blend. SCRAPE.md: "Match on composition, not just
# the trade name. Any three-compound blend containing NAD+, MOTS-C and
# 5-Amino-1MQ is Triple Helix regardless of what the vendor calls it."
BLEND_BY_COMPOSITION = {
    frozenset({"GHK-CU", "TB-500", "BPC-157"}): "GHK-CU+TB500+BPC157 Blend (GLOW)",
    frozenset({"GHK-CU", "TB-500", "BPC-157", "KPV"}): "GHK-CU+TB500+BPC157+KPV Blend (KLOW)",
    frozenset({"BPC-157", "TB-500"}): "BPC157+TB500 Blend (Wolverine)",
    frozenset({"BPC-157", "TB-500", "KPV"}): "BPC157+TB500+KPV Blend (Wolverine 2)",
    frozenset({"BPC-157", "TB-500", "Cartalax"}): "BPC157+TB500+Cartalax Blend (Deadpool)",
    frozenset({"NAD+", "MOTS-C", "5-Amino-1MQ"}): "NAD++Mots-C+5-Amino-1MQ Blend (Triple Helix)",
    frozenset({"CJC-1295 No DAC", "Ipamorelin"}): "CJC-1295 No DAC + Ipamorelin Blend",
    frozenset({"Selank", "Semax"}): "Selank+Semax Blend",
    frozenset({"Tesamorelin", "Ipamorelin"}): "Tesamorelin+Ipamorelin Blend",
    frozenset({"Thymosin Alpha-1", "Thymalin"}): "Thymosin Alpha-1+Thymalin Blend",
    frozenset({"KPV", "GHK-CU"}): "KPV+GHK-CU Blend",
    frozenset({"Retatrutide (GLP3-R)", "Cagrilintide"}): "Retatrutide + Cagrilintide Blend",
}


def match_compound(name):
    """Resolve a vendor product name to one canonical compound.

    Order matters. A blend must never resolve to one of its components -- naive
    longest-string matching labels 'GLOW (GHK-CU, TB-500, BPC-157)' as BPC-157,
    because 'bpc-157' is a longer string than 'glow'.
    """
    hay = re.sub(r"\s+", " ", name.casefold())

    # 1. Blend trade name wins outright.
    for trade, canon in BLEND_TRADE.items():
        if re.search(r"(?<![a-z])" + re.escape(trade) + r"(?![a-z])", hay):
            return canon

    # 2. Collect every single compound mentioned, then resolve by composition.
    found, spans = set(), []
    for needle, canon in alias_index():
        if "blend" in canon.casefold() or "(" in needle:
            continue
        m = re.search(r"(?<![a-z0-9])" + re.escape(needle) + r"(?![a-z0-9])", hay)
        if m and not any(s <= m.start() < e for s, e in spans):
            found.add(canon)
            spans.append((m.start(), m.end()))

    if len(found) > 1:
        if frozenset(found) in BLEND_BY_COMPOSITION:
            return BLEND_BY_COMPOSITION[frozenset(found)]
        # A multi-compound product we can't name: flag, don't guess (INGEST.md).
        return None
    if len(found) == 1:
        return next(iter(found))

    # 3. Fall back to full-alias matching for anything left.
    for needle, canon in alias_index():
        if re.search(r"(?<![a-z0-9])" + re.escape(needle) + r"(?![a-z0-9])", hay):
            return canon
    return None


def parse_units(*texts):
    """Pull a vial/bottle count out of a product or variation label."""
    for t in texts:
        if not t:
            continue
        t = str(t)
        m = re.search(r"(?:kit\s*)?\(?\s*(\d+)\s*(?:x\s*)?(?:vials?|bottles?|pack|ct)\b", t, re.I)
        if m:
            return int(m.group(1))
        m = re.search(r"\b(\d+)\s*[-x]\s*pack\b", t, re.I)
        if m:
            return int(m.group(1))
    return 1


SLUGGY = re.compile(r"batch|purity|lot\b|\d{4}-\d{2}", re.I)


def parse_mg(*texts):
    """Total mg per vial.

    The trap: vendors state the blend split AND the total in one string --
    'GLOW GHK-CU/TB-500/BPC-157 (70MG/10MG/10MG) 90MG VIAL'. Summing everything
    gives 180mg for a 90mg vial. This is the same double-count that corrupted
    his v50 sheet ('54mg (27mg+27mg)' read as 108mg), so guard it explicitly:
    if one figure equals the sum of the others, that figure IS the total.
    """
    for t in texts:
        if not t or SLUGGY.search(str(t)):
            continue
        t = str(t)

        # Concentration x volume. Order varies: '30ML (1MG/ML, ...)' puts the
        # volume first, so match the two independently rather than in sequence.
        conc = re.search(r"(\d+(?:\.\d+)?)\s*mg\s*/\s*ml", t, re.I)
        if conc:
            vol = re.search(r"(\d+(?:\.\d+)?)\s*ml\b(?!\s*\))", t, re.I) or \
                  re.search(r"(\d+(?:\.\d+)?)\s*ml\b", t, re.I)
            if vol:
                return float(conc.group(1)) * float(vol.group(1))

        # Some vendors spell it out in the variant label ('2-milligram'), which is
        # the authoritative size when the parent name lists every option
        # ('TB-500 2MG/5MG/10MG VIAL'). Summing those options gives 17mg for a
        # 2mg vial, so the spelled-out form has to be recognised.
        m = re.search(r"(\d+(?:\.\d+)?)\s*[-\s]?milligram", t, re.I)
        if m:
            return float(m.group(1))
        m = re.search(r"(\d+(?:\.\d+)?)\s*[-\s]?microgram", t, re.I)
        if m:
            return float(m.group(1)) / 1000

        vals = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s*mg\b", t, re.I)]
        if len(vals) > 1:
            for i, v in enumerate(vals):
                rest = vals[:i] + vals[i + 1:]
                # Must be STRICTLY the largest, else two equal components
                # ('10mg/10mg') look like a total and halve the real figure.
                if abs(v - sum(rest)) < 0.01 and v > max(rest):
                    return v                      # explicit total, don't re-add
            return sum(vals)                      # split only -> sum it
        if vals:
            return vals[0]

        m = re.search(r"(\d+(?:\.\d+)?)\s*mcg\b", t, re.I)
        if m:
            return float(m.group(1)) / 1000
    return None


def http_json(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as f:
        return json.loads(f.read().decode("utf8", "ignore")), f.headers


def money(minor, unit=2):
    try:
        return round(int(minor) / (10 ** unit), 2)
    except (TypeError, ValueError):
        return None


def collect(vendor, domain, verbose=True):
    """Tier A collector: WooCommerce Store API."""
    base = f"https://{domain}/wp-json/wc/store/products"
    rows, page, pages = [], 1, 1
    products = []
    while page <= pages and page <= 6:
        try:
            data, hdrs = http_json(f"{base}?per_page=100&page={page}")
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            if page == 1:
                return [], f"catalog fetch failed: {type(e).__name__}"
            break
        pages = int(hdrs.get("X-WP-TotalPages") or 1)
        products.extend(data)
        page += 1
        time.sleep(1.0)

    variable = [p for p in products if p.get("type") == "variable"]
    for p in products:
        name = p.get("name") or ""
        if JUNK.search(name):
            continue
        compound = match_compound(name)
        if not compound:
            continue
        unit = p["prices"].get("currency_minor_unit", 2)
        url = p.get("permalink")

        if p.get("type") == "variable" and p.get("variations"):
            for v in p["variations"][:12]:
                label = " ".join(a.get("value", "") for a in v.get("attributes", []))
                try:
                    vd, _ = http_json(f"https://{domain}/wp-json/wc/store/products/{v['id']}")
                except Exception:
                    continue
                time.sleep(0.35)
                vp = vd.get("prices", {})
                price = money(vp.get("price"), vp.get("currency_minor_unit", unit))
                if not price:
                    continue
                rows.append({
                    "vendor": vendor, "compound": compound,
                    "product": name, "variant": label,
                    "mg": parse_mg(label, name), "units": parse_units(label, name),
                    "price": price,
                    "regular": money(vp.get("regular_price"), vp.get("currency_minor_unit", unit)),
                    "in_stock": bool(vd.get("is_in_stock")),
                    "url": vd.get("permalink") or url,
                })
        else:
            pr = p["prices"]
            price = money(pr.get("price"), unit)
            if not price:
                continue
            rows.append({
                "vendor": vendor, "compound": compound,
                "product": name, "variant": "",
                "mg": parse_mg(name), "units": parse_units(name),
                "price": price, "regular": money(pr.get("regular_price"), unit),
                "in_stock": bool(p.get("is_in_stock")),
                "url": url,
            })

    if verbose:
        print(f"  {vendor:<24} {len(products):>4} products → {len(rows):>4} tracked SKUs")
    return rows, None


SCHEMA = """
CREATE TABLE IF NOT EXISTS sweeps (
  id INTEGER PRIMARY KEY, started_at TEXT, vendors INT, skus INT);
CREATE TABLE IF NOT EXISTS skus (
  id INTEGER PRIMARY KEY, vendor TEXT, compound TEXT, product TEXT, variant TEXT,
  method TEXT, mg REAL, units INT, url TEXT,
  UNIQUE(vendor, compound, product, variant, mg, units));
CREATE TABLE IF NOT EXISTS price_snapshots (
  id INTEGER PRIMARY KEY, sku_id INT, sweep_id INT, price REAL, regular REAL,
  on_sale INT, in_stock INT, scraped_at TEXT,
  FOREIGN KEY(sku_id) REFERENCES skus(id));
CREATE INDEX IF NOT EXISTS ix_snap ON price_snapshots(sku_id, scraped_at DESC);
CREATE TABLE IF NOT EXISTS price_changes (
  id INTEGER PRIMARY KEY, sku_id INT, old_price REAL, new_price REAL,
  pct_delta REAL, kind TEXT, detected_at TEXT);
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="demos/peptide-live-demo/prices.db")
    ap.add_argument("--workers", type=int, default=5)
    args = ap.parse_args()

    db_path = Path(args.db)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(db_path)
    db.executescript(SCHEMA)

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    print(f"sweeping {len(VENDORS)} vendors via WooCommerce Store API...")
    t0 = time.time()
    all_rows, errors = [], []
    with ThreadPoolExecutor(args.workers) as ex:
        for rows, err in ex.map(lambda v: collect(*v), VENDORS):
            all_rows.extend(rows)
            if err:
                errors.append(err)
    elapsed = time.time() - t0

    cur = db.cursor()
    cur.execute("INSERT INTO sweeps(started_at,vendors,skus) VALUES(?,?,?)",
                (now, len(VENDORS), len(all_rows)))
    sweep_id = cur.lastrowid

    changes = 0
    for r in all_rows:
        method = "Inj"  # every tracked SKU on these 10 vendors is a lyophilised vial
        cur.execute(
            """INSERT OR IGNORE INTO skus(vendor,compound,product,variant,method,mg,units,url)
               VALUES(?,?,?,?,?,?,?,?)""",
            (r["vendor"], r["compound"], r["product"], r["variant"], method,
             r["mg"], r["units"], r["url"]))
        cur.execute(
            """SELECT id FROM skus WHERE vendor=? AND compound=? AND product=?
               AND variant=? AND IFNULL(mg,-1)=IFNULL(?,-1) AND units=?""",
            (r["vendor"], r["compound"], r["product"], r["variant"], r["mg"], r["units"]))
        sku_id = cur.fetchone()[0]

        cur.execute("""SELECT price FROM price_snapshots WHERE sku_id=?
                       ORDER BY scraped_at DESC LIMIT 1""", (sku_id,))
        prev = cur.fetchone()
        on_sale = 1 if (r["regular"] and r["price"] < r["regular"]) else 0
        cur.execute(
            """INSERT INTO price_snapshots(sku_id,sweep_id,price,regular,on_sale,in_stock,scraped_at)
               VALUES(?,?,?,?,?,?,?)""",
            (sku_id, sweep_id, r["price"], r["regular"], on_sale, int(r["in_stock"]), now))

        if prev and prev[0] != r["price"]:
            pct = (r["price"] - prev[0]) / prev[0] * 100
            cur.execute(
                """INSERT INTO price_changes(sku_id,old_price,new_price,pct_delta,kind,detected_at)
                   VALUES(?,?,?,?,?,?)""",
                (sku_id, prev[0], r["price"], round(pct, 2),
                 "drop" if pct < 0 else "rise", now))
            changes += 1

    db.commit()
    n_sales = sum(1 for r in all_rows if r["regular"] and r["price"] < r["regular"])
    n_oos = sum(1 for r in all_rows if not r["in_stock"])
    n_sweeps = db.execute("SELECT COUNT(*) FROM sweeps").fetchone()[0]

    print(f"\n{len(all_rows)} SKUs · {len({r['compound'] for r in all_rows})} compounds "
          f"· {len({r['vendor'] for r in all_rows})} vendors  in {elapsed:.0f}s")
    print(f"on sale: {n_sales} · out of stock: {n_oos} · "
          f"price changes vs last sweep: {changes} · sweeps in db: {n_sweeps}")
    if errors:
        print("errors:", errors)
    print(f"db: {db_path}")
    db.close()


if __name__ == "__main__":
    sys.exit(main())
