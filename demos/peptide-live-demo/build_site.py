#!/usr/bin/env python3
"""
Render the SQLite sweep into a single self-contained HTML page.

Deliberately one file with the data inlined and zero external requests -- no
CDN, no webfont fetch, no server. It opens from disk and cannot fail on
call-day wifi. Fonts are the ones already on macOS (ui-serif = New York,
ui-monospace = SF Mono), so nothing loads over the network.

  python3 demos/peptide-live-demo/build_site.py && open demos/peptide-live-demo/index.html
"""

import argparse
import json
import sqlite3
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Peptide Shaman · live price index</title>
<style>
:root{
  --ink:#0b0b0c; --ink-2:#3d3d42; --ink-3:#78787f;
  --line:#e7e7ea; --line-2:#f2f2f4; --bg:#fff; --wash:#fafafa;
  --best:#07714c; --best-bg:#e8f5ef;
  --sale:#9a4a00; --sale-bg:#fdf0e4;
  --dead:#9a9aa2;
  --serif:ui-serif,"New York",Iowan Old Style,Palatino,Georgia,serif;
  --sans:system-ui,-apple-system,"Helvetica Neue",sans-serif;
  --mono:ui-monospace,"SF Mono",Menlo,monospace;
}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
body{background:var(--bg);color:var(--ink);font-family:var(--sans);
  font-size:15px;line-height:1.5}
.wrap{max-width:1180px;margin:0 auto;padding:0 32px}

/* ── top bar ─────────────────────────────────────────── */
header{border-bottom:1px solid var(--line);position:sticky;top:0;z-index:20;
  background:rgba(255,255,255,.86);backdrop-filter:saturate(180%) blur(20px)}
.bar{display:flex;align-items:center;gap:18px;height:56px}
.mark{font-family:var(--serif);font-size:19px;letter-spacing:-.015em}
.mark i{font-style:italic;color:var(--ink-3)}
.stamp{margin-left:auto;font-family:var(--mono);font-size:11px;color:var(--ink-3);
  letter-spacing:.02em;display:flex;align-items:center;gap:7px}
.pulse{width:6px;height:6px;border-radius:50%;background:var(--best);
  box-shadow:0 0 0 0 rgba(7,113,76,.5);animation:p 2.6s infinite}
@keyframes p{0%{box-shadow:0 0 0 0 rgba(7,113,76,.45)}
  70%{box-shadow:0 0 0 7px rgba(7,113,76,0)}100%{box-shadow:0 0 0 0 rgba(7,113,76,0)}}

/* ── masthead ────────────────────────────────────────── */
.hero{padding:64px 0 40px;border-bottom:1px solid var(--line)}
.kicker{font-family:var(--mono);font-size:11px;letter-spacing:.13em;
  text-transform:uppercase;color:var(--ink-3);margin-bottom:20px}
h1{font-family:var(--serif);font-weight:400;font-size:clamp(38px,5.2vw,64px);
  line-height:1.02;letter-spacing:-.028em;max-width:20ch}
h1 em{font-style:italic;color:var(--ink-3)}
.stats{display:flex;gap:52px;margin-top:44px;flex-wrap:wrap}
.stat b{display:block;font-family:var(--serif);font-size:34px;font-weight:400;
  letter-spacing:-.02em;line-height:1}
.stat span{font-family:var(--mono);font-size:10.5px;letter-spacing:.09em;
  text-transform:uppercase;color:var(--ink-3);margin-top:9px;display:block}

/* ── layout ──────────────────────────────────────────── */
.cols{display:grid;grid-template-columns:236px 1fr;gap:56px;padding:44px 0 96px;
  align-items:start}
@media(max-width:880px){.cols{grid-template-columns:1fr;gap:28px}
  .rail{position:static!important;max-height:none!important}}

/* ── compound rail ───────────────────────────────────── */
.rail{position:sticky;top:80px;max-height:calc(100vh - 120px);overflow-y:auto}
.rail h2,.panel h2{font-family:var(--mono);font-size:10.5px;letter-spacing:.11em;
  text-transform:uppercase;color:var(--ink-3);margin-bottom:14px}
.search{width:100%;border:1px solid var(--line);border-radius:8px;padding:8px 11px;
  font-family:var(--sans);font-size:13.5px;margin-bottom:10px;background:var(--bg);
  color:var(--ink);transition:border-color .15s}
.search:focus{outline:none;border-color:var(--ink-3)}
.search::placeholder{color:var(--ink-3)}
.rail ul{list-style:none}
.rail li{display:flex;align-items:baseline;gap:8px;padding:7px 10px;cursor:pointer;
  border-radius:7px;transition:background .12s}
.rail li:hover{background:var(--wash)}
.rail li[aria-selected=true]{background:var(--ink);color:#fff}
.rail li[aria-selected=true] .n{color:rgba(255,255,255,.55)}
.rail li .t{font-size:13.5px;letter-spacing:-.005em;flex:1;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.rail li .n{font-family:var(--mono);font-size:10.5px;color:var(--ink-3)}

/* ── results ─────────────────────────────────────────── */
.panel>header{border:0;position:static;background:none;backdrop-filter:none;
  display:flex;align-items:flex-end;gap:16px;padding-bottom:20px;
  border-bottom:1px solid var(--line);margin-bottom:4px}
.panel h3{font-family:var(--serif);font-weight:400;font-size:31px;
  letter-spacing:-.022em;line-height:1.1}
.panel .meta{font-family:var(--mono);font-size:11px;color:var(--ink-3);
  margin-left:auto;white-space:nowrap;padding-bottom:5px}

.row{display:grid;grid-template-columns:26px 1fr 118px 96px 104px;gap:16px;
  align-items:center;padding:17px 0;border-bottom:1px solid var(--line-2);
  animation:in .38s both}
@keyframes in{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}
@media(max-width:680px){.row{grid-template-columns:22px 1fr 96px;row-gap:9px}
  .row .size,.row .tot{grid-column:2/-1;text-align:left!important}}
.rank{font-family:var(--mono);font-size:11px;color:var(--ink-3);text-align:right}
.row.best .rank{color:var(--best)}
.vend{min-width:0}
.vend .nm{font-size:15px;letter-spacing:-.008em;white-space:nowrap;
  overflow:hidden;text-overflow:ellipsis}
.vend .sub{font-size:12px;color:var(--ink-3);margin-top:3px;white-space:nowrap;
  overflow:hidden;text-overflow:ellipsis}
.tags{display:flex;gap:5px;margin-top:6px;flex-wrap:wrap}
.tag{font-family:var(--mono);font-size:9.5px;letter-spacing:.06em;
  text-transform:uppercase;padding:2.5px 6px;border-radius:4px}
.tag.b{background:var(--best-bg);color:var(--best)}
.tag.s{background:var(--sale-bg);color:var(--sale)}
.tag.o{background:var(--line-2);color:var(--dead)}
.size,.tot{font-family:var(--mono);font-size:12.5px;color:var(--ink-2);text-align:right}
.tot s{color:var(--ink-3);font-size:11px;display:block;margin-top:2px}
.permg{text-align:right}
.permg b{font-family:var(--mono);font-size:16.5px;letter-spacing:-.02em;
  font-weight:500;font-variant-numeric:tabular-nums}
.row.best .permg b{color:var(--best)}
.permg span{font-family:var(--mono);font-size:9.5px;color:var(--ink-3);
  display:block;margin-top:2px}
.row.oos .vend .nm,.row.oos .permg b{color:var(--dead)}

/* the ladder — the one thing you remember */
.ladder{grid-column:2/4;height:2px;background:var(--line-2);border-radius:2px;
  margin-top:-6px;overflow:hidden}
@media(max-width:680px){.ladder{grid-column:2/-1}}
.ladder i{display:block;height:100%;background:var(--ink);border-radius:2px;
  animation:grow .7s cubic-bezier(.2,.8,.2,1) both}
.row.best .ladder i{background:var(--best)}
.row.oos .ladder i{background:var(--dead)}
@keyframes grow{from{width:0}}

.foot{border-top:1px solid var(--line);padding:28px 0 60px;
  font-size:12.5px;color:var(--ink-3);display:flex;gap:26px;flex-wrap:wrap}
.foot b{color:var(--ink-2);font-weight:500}
.note{background:var(--wash);border:1px solid var(--line);border-radius:10px;
  padding:15px 17px;font-size:13px;color:var(--ink-2);margin-top:26px;line-height:1.55}
.note b{color:var(--ink)}
</style></head><body>

<header><div class="wrap bar">
  <div class="mark">Peptide&nbsp;<i>Shaman</i></div>
  <div class="stamp"><span class="pulse"></span>SWEPT __STAMP__</div>
</div></header>

<div class="wrap">
  <section class="hero">
    <div class="kicker">Live vendor price index · proof of concept</div>
    <h1>Every vendor's real price, <em>normalised to the milligram.</em></h1>
    <div class="stats">
      <div class="stat"><b>__NSKU__</b><span>SKUs priced</span></div>
      <div class="stat"><b>__NVEN__</b><span>vendors swept</span></div>
      <div class="stat"><b>__NCOM__</b><span>compounds</span></div>
      <div class="stat"><b>__NSALE__</b><span>on sale now</span></div>
      <div class="stat"><b>__NOOS__</b><span>out of stock</span></div>
      <div class="stat"><b>__SECS__s</b><span>to sweep all __NVEN__</span></div>
    </div>
  </section>

  <div class="cols">
    <aside class="rail">
      <h2>Compound · vendors</h2>
      <input class="search" id="q" placeholder="Filter compounds…" autocomplete="off">
      <ul id="list"></ul>
    </aside>

    <section class="panel">
      <header>
        <h3 id="title"></h3>
        <div class="meta" id="submeta"></div>
      </header>
      <div id="rows"></div>
      <div class="note">
        <b>Nothing here is typed by hand.</b> Prices, sale flags and stock status come
        straight from each vendor's public product API — the same sweep that writes the
        database, the Excel sheet and the price-drop alerts. Ranked by cost per
        milligram, because a $89 box and a $40 box aren't comparable until you divide
        by what's actually in them.
      </div>
    </section>
  </div>

  <div class="foot">
    <span><b>__NVEN__ of 92</b> vendors — the rest is configuration, not new code</span>
    <span><b>No browser automation.</b> Public JSON endpoints</span>
    <span><b>Append-only history</b> — every sweep kept forever</span>
  </div>
</div>

<script>
const DATA = __DATA__;
const money = n => '$' + n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});
const permg = n => '$' + (n >= 1 ? n.toFixed(2) : n.toFixed(3));
let active = DATA.order[0];

function renderList(filter=''){
  const f = filter.trim().toLowerCase();
  const ul = document.getElementById('list');
  ul.innerHTML = '';
  DATA.order.filter(c => !f || c.toLowerCase().includes(f)).forEach(c => {
    const li = document.createElement('li');
    li.setAttribute('aria-selected', c === active);
    // Show vendor coverage, which is what the rail is ordered by. Showing the
    // listing count while sorting on vendors reads as an arbitrary order.
    const nv = new Set(DATA.byCompound[c].map(r => r.v)).size;
    li.innerHTML = `<span class="t">${c}</span><span class="n">${nv}</span>`;
    li.onclick = () => { active = c; renderList(filter); renderRows(); };
    ul.appendChild(li);
  });
}

function renderRows(){
  const rows = DATA.byCompound[active];
  document.getElementById('title').textContent = active;
  const vend = new Set(rows.map(r => r.v)).size;
  const live = rows.filter(r => r.k).length;
  document.getElementById('submeta').textContent =
    `${rows.length} listings · ${vend} vendors · ${live} in stock`;

  const cheapest = Math.min(...rows.map(r => r.p));
  const dearest  = Math.max(...rows.map(r => r.p));
  const host = document.getElementById('rows');
  host.innerHTML = '';

  rows.forEach((r, i) => {
    const best = i === 0;
    // ladder: cheapest is full width, scaled against the spread
    const span = dearest - cheapest || 1;
    const w = 100 - ((r.p - cheapest) / span) * 82;
    const el = document.createElement('div');
    el.className = 'row' + (best ? ' best' : '') + (r.k ? '' : ' oos');
    el.style.animationDelay = (i * 26) + 'ms';
    const tags = [];
    if (best) tags.push('<span class="tag b">Best / mg</span>');
    if (r.s)  tags.push('<span class="tag s">On sale</span>');
    if (!r.k) tags.push('<span class="tag o">Out of stock</span>');
    el.innerHTML = `
      <div class="rank">${i + 1}</div>
      <div class="vend">
        <div class="nm">${r.v}</div>
        <div class="sub">${r.n}</div>
        ${tags.length ? `<div class="tags">${tags.join('')}</div>` : ''}
      </div>
      <div class="size">${r.mg}mg${r.u > 1 ? ` × ${r.u}` : ''}<br>${r.mg * r.u}mg total</div>
      <div class="tot">${money(r.t)}${r.r && r.s ? `<s>was ${money(r.r)}</s>` : ''}</div>
      <div class="permg"><b>${permg(r.p)}</b><span>per mg</span></div>
      <div class="ladder"><i style="width:${w}%;animation-delay:${i * 26 + 90}ms"></i></div>`;
    host.appendChild(el);
  });
}

document.getElementById('q').addEventListener('input', e => renderList(e.target.value));
renderList(); renderRows();
</script></body></html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="demos/peptide-live-demo/prices.db")
    ap.add_argument("--out", default="demos/peptide-live-demo/index.html")
    ap.add_argument("--secs", default="325", help="sweep duration, for the stat row")
    args = ap.parse_args()

    db = sqlite3.connect(args.db)
    db.row_factory = sqlite3.Row
    sweep = db.execute("SELECT id, started_at FROM sweeps ORDER BY id DESC LIMIT 1").fetchone()

    by = defaultdict(list)
    n_sale = n_oos = 0
    for r in db.execute("""
            SELECT s.compound, s.vendor, s.product, s.variant, s.mg, s.units, s.url,
                   p.price, p.regular, p.on_sale, p.in_stock
            FROM skus s JOIN price_snapshots p ON p.sku_id = s.id
            WHERE p.sweep_id = ? AND s.mg > 0""", (sweep["id"],)):
        n_sale += bool(r["on_sale"])
        n_oos += (not r["in_stock"])
        label = r["product"]
        if r["variant"] and r["variant"].lower() not in label.lower():
            label += f" — {r['variant']}"
        by[r["compound"]].append({
            "v": r["vendor"], "n": label[:96],
            "mg": round(r["mg"], 2) if r["mg"] % 1 else int(r["mg"]),
            "u": r["units"], "t": round(r["price"], 2),
            "r": round(r["regular"], 2) if r["regular"] else None,
            "s": bool(r["on_sale"]), "k": bool(r["in_stock"]),
            "p": r["price"] / (r["mg"] * r["units"]),
        })

    for rows in by.values():
        rows.sort(key=lambda x: x["p"])
    # Rail order: widest vendor coverage first -- that's what makes the point.
    order = sorted(by, key=lambda c: (-len({r["v"] for r in by[c]}), -len(by[c]), c))

    total = sum(len(v) for v in by.values())
    stamp = datetime.fromisoformat(sweep["started_at"]).astimezone(timezone.utc)
    html = (PAGE
            .replace("__DATA__", json.dumps({"byCompound": by, "order": order},
                                            separators=(",", ":")))
            .replace("__STAMP__", stamp.strftime("%d %b %Y · %H:%M UTC").upper())
            .replace("__NSKU__", f"{total:,}")
            .replace("__NVEN__", str(len({r["v"] for v in by.values() for r in v})))
            .replace("__NCOM__", str(len(by)))
            .replace("__NSALE__", str(n_sale))
            .replace("__NOOS__", str(n_oos))
            .replace("__SECS__", args.secs))

    out = Path(args.out)
    out.write_text(html)
    print(f"wrote {out}  ({len(html) / 1024:.0f} KB, self-contained)")
    print(f"  {total} SKUs across {len(by)} compounds · top: {order[0]} "
          f"({len({r['v'] for r in by[order[0]]})} vendors)")
    db.close()


if __name__ == "__main__":
    main()
