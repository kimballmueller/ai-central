// The seven practice pages must stay structurally identical — they are generated
// from one template, so any drift here means the generator broke.
import { go, ev, SLUGS, close } from './_cdp.mjs';
let fail = 0;
console.log('practice                     roles screen faq related fill band darkCTA  number');
for (const s of SLUGS) {
  await go(`industries/${s}.html`);
  const r = await ev(`(()=>({
    roles: document.querySelectorAll('.roles li').length,
    screen: document.querySelectorAll('.steps .step').length,
    faq: document.querySelectorAll('.faq details').length,
    related: document.querySelectorAll('.sec.tint .g3 .card').length,
    fill: !!document.querySelector('.phead-display .fill'),
    band: (()=>{ const i = document.querySelector('.band .shot img');
                 return !!i && i.naturalWidth > 0; })(),
    dark: !!document.querySelector('.sec.dark .btn-green') && !!document.querySelector('.sec.cta'),
    ghost: [...document.querySelectorAll('.sec.dark .btn-out, .sec.cta .btn-out')]
             .every(b => getComputedStyle(b).color === 'rgb(255, 255, 255)'),
    num: (document.querySelector('.phead .eyebrow')||{}).textContent||''
  }))()`);
  const ok = r.roles===9 && r.screen===4 && r.faq===4 && r.related===3 && r.fill && r.band
             && r.dark && r.ghost && new RegExp(`^Practice area \\d{2} of ${String(SLUGS.length).padStart(2,'0')}$`).test(r.num.trim());
  if (!ok) fail++;
  console.log(`${ok?'PASS':'FAIL'} ${s.padEnd(26)} ${String(r.roles).padStart(4)} ${String(r.screen).padStart(6)} ${String(r.faq).padStart(3)} ${String(r.related).padStart(7)} ${String(r.fill).padStart(5)} ${String(r.band).padStart(4)} ${String(r.dark&&r.ghost).padStart(7)}  ${r.num.trim().slice(-8)}`);
}
console.log(fail ? `\n${fail} failed` : `\nAll ${SLUGS.length} practice pages pass.`);
close(fail ? 1 : 0);
