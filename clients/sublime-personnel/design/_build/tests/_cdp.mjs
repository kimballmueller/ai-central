// Minimal CDP driver — no dependencies, uses Node 22's built-in WebSocket.
// Start a browser first:
//   chrome-headless-shell --headless --disable-gpu --hide-scrollbars \
//     --window-size=1440,900 --remote-debugging-port=9352 --user-data-dir=/tmp/sp about:blank
export const PORT = Number(process.env.CDP_PORT || 9352);
export const BASE = process.env.BASE || 'http://localhost:8901';

const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
const target = list.find(t => t.type === 'page');
if (!target) { console.error('no page target on port ' + PORT); process.exit(1); }
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise(r => ws.addEventListener('open', r, { once: true }));

let id = 0; const pend = new Map();
export let errs = [];
export const resetErrs = () => { errs = []; };
ws.addEventListener('message', e => {
  const m = JSON.parse(e.data);
  if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); return; }
  if (m.method === 'Runtime.exceptionThrown') errs.push('EXC ' + (m.params.exceptionDetails?.text || ''));
  if (m.method === 'Log.entryAdded' && m.params.entry.level === 'error') errs.push('LOG ' + m.params.entry.text);
});
export const send = (method, params = {}) => new Promise(res => {
  const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params }));
});
export const ev = async expr => (await send('Runtime.evaluate',
  { expression: expr, returnByValue: true, awaitPromise: true })).result?.result?.value;
export const wait = ms => new Promise(r => setTimeout(r, ms));
export const go = async (path, settle = 1600) => {
  resetErrs();
  await send('Page.navigate', { url: `${BASE}/${path}` });
  await wait(settle);
};
export const realErrs = () => errs.filter(t => !/favicon|fonts\.g/.test(t));
export const close = code => { ws.close(); process.exit(code); };
await send('Runtime.enable'); await send('Log.enable');

export const PAGES = ['index','clients','candidates','blog','start-a-search','cost-of-vacancy','talent-network',
  'industries/hoa-property-management','industries/hospitality-restaurant','industries/commercial-lines-insurance',
  'industries/personal-lines-insurance','industries/accounting-finance','industries/commercial-construction',
  'industries/qsr-franchise','industries/oil-gas'];
export const SLUGS = PAGES.filter(p => p.startsWith('industries/')).map(p => p.split('/')[1]);
