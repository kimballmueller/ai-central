// Every <img> resolves and every page stays inside its weight budget, with lazy
// images forced to load by scrolling to the bottom first.
import { go, ev, wait, send, PAGES, close } from './_cdp.mjs';
await send('Network.enable');
const BUDGET_KB = { index: 1100 };      // homepage carries the practice-card set
let fail = 0;
console.log('page                                     imgs  broken   weight');
for (const p of PAGES) {
  await go(`${p}.html`, 1200);
  await ev('window.scrollTo(0, document.body.scrollHeight)'); await wait(1500);
  const r = await ev(`(()=>{const im=[...document.images];
    return { n: im.length,
             broken: im.filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.currentSrc||i.src),
             bytes: performance.getEntriesByType('resource').reduce((a,b)=>a+(b.transferSize||0),0) };})()`);
  const kb = r.bytes/1024, cap = BUDGET_KB[p] ?? 600;
  const ok = r.broken.length === 0 && kb <= cap;
  if (!ok) fail++;
  console.log(`${ok?'PASS':'FAIL'} ${p.padEnd(38)} ${String(r.n).padStart(3)}  ${String(r.broken.length).padStart(6)}  ${kb.toFixed(0).padStart(5)}KB / ${cap}KB`);
  r.broken.forEach(b => console.log('      broken:', b));
}
console.log(fail ? `\n${fail} page(s) failed` : '\nEvery image loads and every page is inside budget.');
close(fail ? 1 : 0);
