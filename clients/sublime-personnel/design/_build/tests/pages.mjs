// Structure of every page: exactly one H1, the kicker and display heading at the
// right sizes, no skipped heading levels, and a clean console.
import { go, ev, realErrs, PAGES, close } from './_cdp.mjs';
let fail = 0;
console.log('page                                     H1  kicker  display  skips  console');
for (const p of PAGES) {
  await go(`${p}.html`);
  const r = await ev(`(()=>{
    const kick = document.querySelector('.hero .eyebrow, .phead .eyebrow');
    const disp = document.querySelector('.hero-display, .phead-display');
    const hs = [...document.querySelectorAll('h1,h2,h3,h4')].map(h => +h.tagName[1]);
    let sk = 0; for (let i = 1; i < hs.length; i++) if (hs[i] - hs[i-1] > 1) sk++;
    return { n: document.querySelectorAll('h1').length,
             k: kick ? Math.round(parseFloat(getComputedStyle(kick).fontSize)) : null,
             d: disp ? Math.round(parseFloat(getComputedStyle(disp).fontSize)) : null, sk };
  })()`);
  const e = realErrs();
  const ok = r.n === 1 && r.k === 11 && r.d > 28 && r.sk === 0 && e.length === 0;
  if (!ok) fail++;
  console.log(`${ok?'PASS':'FAIL'} ${p.padEnd(38)} ${String(r.n).padStart(2)}  ${String(r.k).padStart(6)}  ${String(r.d).padStart(7)}  ${String(r.sk).padStart(5)}  ${e.length?e[0].slice(0,44):'clean'}`);
}
console.log(fail ? `\n${fail} page(s) failed` : `\nAll ${PAGES.length} pages pass.`);
close(fail ? 1 : 0);
