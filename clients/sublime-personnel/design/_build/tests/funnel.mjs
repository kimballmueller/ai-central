// The conversion paths: the four-step employer intake, the vacancy calculator,
// and the two simple forms. These are the pages the SOW is judged on, so they
// get driven end to end rather than eyeballed.
import { go, ev, wait, realErrs, close } from './_cdp.mjs';
let pass = 0, fail = 0;
const check = (label, got, want) => {
  const ok = JSON.stringify(got) === JSON.stringify(want);
  ok ? pass++ : fail++;
  console.log(`${ok?'PASS':'FAIL'}  ${label}` + (ok ? '' : `\n        got ${JSON.stringify(got)}  want ${JSON.stringify(want)}`));
};

// ---------------------------------------------------------- multi-step intake
console.log('--- start-a-search: four-step intake ---');
await go('start-a-search.html');
await ev(`sessionStorage.clear()`);
await go('start-a-search.html');
const step = `(() => {
  const ps = [...document.querySelectorAll('.step-panel')];
  return { step: ps.findIndex(p => !p.hidden),
           counter: document.querySelector('[data-count]').textContent,
           bar: document.querySelector('.wiz-bar i').style.width,
           doneShown: !document.querySelector('.wiz-done').hidden };
})()`;
check('starts on step 1', await ev(step), { step: 0, counter: 'Step 1 of 4', bar: '25%', doneShown: false });

await ev(`document.querySelector('input[name=industry]').click()`); await wait(400);
check('choosing a practice auto-advances', (await ev(step)).step, 1);

await ev(`document.querySelector('[data-next]').click()`); await wait(250);
check('empty required field blocks advance', (await ev(step)).step, 1);
check('field flagged .bad', await ev(`document.querySelector('[data-required=role]').classList.contains('bad')`), true);
check('aria-invalid set', await ev(`document.querySelector('#role').getAttribute('aria-invalid')`), 'true');

await ev(`(()=>{const e=document.querySelector('#role');e.value='Portfolio Manager';
         e.dispatchEvent(new Event('input',{bubbles:true}));})()`);
await ev(`document.querySelector('[data-next]').click()`); await wait(350);
check('valid field advances to step 3', (await ev(step)).step, 2);
check('progress bar tracks the step', (await ev(step)).bar, '75%');
check('progress persisted to sessionStorage',
      await ev(`!!JSON.parse(sessionStorage.getItem('sp_intake')||'{}').role`), true);

await ev(`document.querySelector('.back').click()`); await wait(300);
check('back returns to step 2', (await ev(step)).step, 1);
check('answer survives going back', await ev(`document.querySelector('#role').value`), 'Portfolio Manager');

// walk the rest of the wizard, filling whatever the visible panel requires
const fillPanel = `(() => {
  const p = [...document.querySelectorAll('.step-panel')].find(x => !x.hidden);
  let filled = 0;
  p.querySelectorAll('[data-required]').forEach(g => {
    const name = g.getAttribute('data-required');
    const els = p.querySelectorAll('[name="' + name + '"]');
    const el = els[0]; if (!el) return;
    if (el.type === 'radio' || el.type === 'checkbox') { el.click(); filled++; return; }
    if (String(el.value).trim() !== '') return;
    el.value = el.type === 'email' ? 'pete@example.com'
             : el.type === 'tel'   ? '7133960944' : 'Test value';
    el.dispatchEvent(new Event('input', { bubbles: true }));
    filled++;
  });
  return filled;
})()`;
for (let i = 0; i < 3; i++) {
  const cur = (await ev(step)).step;
  if (cur === 3) break;
  await ev(fillPanel); await wait(150);
  await ev(`document.querySelector('[data-next]').click()`); await wait(400);
}
check('reaches the final step', (await ev(step)).step, 3);
check('final step is labelled', (await ev(step)).counter, 'Step 4 of 4');

await ev(`(()=>{for(const [sel,v] of [['#name','Pete Proctor'],['#email','not-an-email'],['#phone','7133960944']]){
         const e=document.querySelector(sel); if(e){e.value=v; e.dispatchEvent(new Event('input',{bubbles:true}));}}})()`);
await ev(fillPanel);
await ev(`(()=>{const e=document.querySelector('#email');e.value='not-an-email';
         e.dispatchEvent(new Event('input',{bubbles:true}));})()`);
await ev(`document.querySelector('[data-wizard] [data-next]').click()`); await wait(400);
check('malformed email blocks submit', (await ev(step)).doneShown, false);
check('email field flagged', await ev(`document.querySelector('[data-required=email]').classList.contains('bad')`), true);

await ev(`(()=>{const e=document.querySelector('#email');e.value='pete@example.com';
         e.dispatchEvent(new Event('input',{bubbles:true}));})()`);
await ev(`document.querySelector('[data-wizard] [data-next]').click()`); await wait(900);
check('valid submit shows the confirmation', (await ev(step)).doneShown, true);
// assert on the interpolated name node, not on the panel text — the static copy
// mentions Pete either way, so a textContent check here would pass vacuously
check('confirmation interpolates the first name',
      await ev(`(document.querySelector('.wiz-done [data-name]')?.textContent||'').trim()`), 'Pete');
check('sessionStorage cleared after submit', await ev(`sessionStorage.getItem('sp_intake')`), null);

// ------------------------------------------------------------- the calculator
console.log('\n--- cost-of-vacancy: the calculator ---');
await go('cost-of-vacancy.html');
const nums = `(() => {
  const t = s => (document.querySelector(s)?.textContent || '');
  const num = s => t(s).replace(/[^0-9.]/g,'');
  return { daily: num('[data-out=daily]'), vacancy: num('[data-out=vacancy]'),
           fee: t('[data-out=fee]'), annual: t('[data-out=annual]'),
           breakeven: num('[data-out=breakeven]'), verdict: t('[data-out=verdict]'),
           salary: num('[data-out=salary]'), days: num('[data-out=days]') };
})()`;
const set = async (id, v) => ev(`(()=>{const e=document.querySelector('#${id}');
  if(e){e.value='${v}'; e.dispatchEvent(new Event('input',{bubbles:true}));}})()`);
const money = n => Math.round(n).toLocaleString('en-US');

await set('salary', 120000); await set('daysopen', 45);
await set('hires', 4); await set('multiplier', 2); await wait(400);
const D1 = 120000*2/260, V1 = D1*45;
const a = await ev(nums);
check('echoes the salary back', a.salary, '120,000'.replace(/,/g,''));
check('daily value = salary x multiplier / 260', a.daily, String(Math.round(D1)));
check('vacancy cost = daily x days open', a.vacancy, String(Math.round(V1)));
check('fee range is 15-20% of salary', a.fee.replace(/\s/g,''), '$18,000–$24,000');
check('annual fee = range x hires per year', a.annual.replace(/\s/g,''), '$72,000–$96,000');
check('break-even = high fee / daily value', a.breakeven, String(Math.round(24000/D1)));
check('verdict speaks when the seat has outrun the fee',
      V1 > 24000 ? a.verdict.includes('more') : a.verdict.includes('overtakes'), true);

await set('salary', 65000); await set('daysopen', 90); await wait(400);
const D2 = 65000*2/260;
const b = await ev(nums);
check('recalculates daily value on new inputs', b.daily, String(Math.round(D2)));
check('vacancy follows the new day count', b.vacancy, String(Math.round(D2*90)));
check('fees follow the new salary', b.fee.replace(/\s/g,''), '$9,750–$13,000');
check('no email gate on the result',
      await ev(`!document.querySelector('.calc-out input[type=email]')`), true);

// ----------------------------------------------------------------- the forms
for (const page of ['talent-network.html', 'cost-of-vacancy.html']) {
  console.log(`\n--- ${page}: simple form ---`);
  await go(page);
  const name = await ev(`document.querySelector('form[data-simple]')?.getAttribute('data-simple')`);
  if (!name) { check(`${page} has a simple form`, false, true); continue; }

  await ev(`document.querySelector('form[data-simple] [type=submit]')?.click()`); await wait(300);
  check(`${name}: empty submit is blocked and flagged`,
        await ev(`!!document.querySelector('form[data-simple] .bad')`), true);

  await ev(`(()=>{document.querySelectorAll('form[data-simple] [data-required] [name]').forEach(e=>{
      e.value = e.type === 'email' ? 'candidate@example.com' : 'Test value';
      e.dispatchEvent(new Event('input',{bubbles:true}));});})()`);
  await ev(`document.querySelector('form[data-simple] [type=submit]')?.click()`); await wait(800);
  check(`${name}: confirmation shown on valid submit`,
        await ev(`(()=>{const b=document.querySelector('form[data-simple] .form-ok');
                  return !!b && b.hidden === false;})()`), true);
  check(`${name}: fields hidden after submit`,
        await ev(`[...document.querySelectorAll('form[data-simple] .field')].every(f=>f.hidden)`), true);
}

// ------------------------------------------------------------------- console
console.log('\n--- console health ---');
for (const p of ['start-a-search.html','cost-of-vacancy.html','talent-network.html','clients.html','index.html']) {
  await go(p, 1800);
  const e = realErrs();
  check(`${p}: no uncaught errors`, e, []);
}
console.log(`\n${pass} passed, ${fail} failed`);
close(fail ? 1 : 0);
