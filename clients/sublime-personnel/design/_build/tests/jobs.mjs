/* Job board: the filters have to actually narrow, the count has to agree with
   what is on screen, and while the rows are illustrative the page has to say so.
   That last one is not cosmetic — the board is on a public URL and a convincing
   fake opening is a job a real candidate would apply to. */
import { go, ev, wait, realErrs, close } from './_cdp.mjs';
let pass = 0, fail = 0;
const check = (label, got, want) => {
  const ok = JSON.stringify(got) === JSON.stringify(want);
  ok ? pass++ : fail++;
  console.log(`${ok?'PASS':'FAIL'}  ${label}` + (ok ? '' : `\n        got ${JSON.stringify(got)}  want ${JSON.stringify(want)}`));
};

await go('jobs.html');

const state = `(() => {
  const rows = [...document.querySelectorAll('.job')];
  return {
    total:   rows.length,
    visible: rows.filter(r => !r.hidden).length,
    count:   +(document.querySelector('[data-jobs-count]')?.textContent || -1),
    noun:    document.querySelector('[data-jobs-noun]')?.textContent || '',
    empty:   document.querySelector('[data-jobs-empty]')?.hidden !== false,
    banner:  !!document.querySelector('.notice')
  };
})()`;

const pick = async (id, v) => ev(`(()=>{const e=document.querySelector('#${id}');
  if(e){e.value='${v}'; e.dispatchEvent(new Event('change',{bubbles:true}));}})()`);

const a = await ev(state);
check('the board has roles on it', a.total > 0, true);
check('every role is visible before filtering', a.visible, a.total);
check('the count agrees with what is on screen', a.count, a.visible);
check('the empty state is hidden while rows show', a.empty, true);
check('sample rows carry a preview banner', a.banner, true);

// one filter
await pick('f-practice', 'hoa-property-management'); await wait(250);
const b = await ev(state);
check('a practice filter narrows the board', b.visible < a.total && b.visible > 0, true);
check('the count follows the filter', b.count, b.visible);
check('only matching rows survive',
  await ev(`[...document.querySelectorAll('.job')].filter(r=>!r.hidden)
             .every(r => r.getAttribute('data-practice') === 'hoa-property-management')`), true);

// two filters compose
await pick('f-band', 'over150'); await wait(250);
const c = await ev(state);
check('filters compose rather than replace', c.visible <= b.visible, true);
// Guard against the empty-state checks below going vacuous if the sample data moves.
check('this filter pair genuinely empties the board', c.visible, 0);
check('no matches shows the empty state', c.visible === 0 ? c.empty === false : true, true);
check('singular noun when one role matches', c.visible === 1 ? c.noun === 'role' : true, true);

// clearing restores
await pick('f-practice', ''); await pick('f-band', ''); await wait(250);
const d = await ev(state);
check('clearing the filters restores every role', d.visible, a.total);

// every row routes somewhere real
check('every role links onward',
  await ev(`[...document.querySelectorAll('.job')].every(r => {
    const a = r.querySelector('a.tlink');
    return !!a && !!a.getAttribute('href');
  })`), true);
check('every role names its practice page',
  await ev(`[...document.querySelectorAll('.job')].every(r =>
    !!r.querySelector('.job-meta a[href^="industries/"]'))`), true);

check('jobs.html: no uncaught errors', realErrs(), []);
console.log(`\n${pass} passed, ${fail} failed`);
close(fail ? 1 : 0);
