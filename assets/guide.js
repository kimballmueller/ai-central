// OS tabs + copy-to-clipboard. Tiny, no deps.

(function () {
  const STORAGE_KEY = 'preferred-os';

  function activateOs(os) {
    document.querySelectorAll('.os-tabs').forEach(group => {
      group.querySelectorAll('.tab').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.os === os);
        btn.setAttribute('aria-selected', btn.dataset.os === os);
      });
      group.querySelectorAll('.os-content').forEach(panel => {
        panel.classList.toggle('active', panel.dataset.os === os);
      });
    });
    try { localStorage.setItem(STORAGE_KEY, os); } catch (_) {}
  }

  function initOsTabs() {
    const saved = (() => { try { return localStorage.getItem(STORAGE_KEY); } catch (_) { return null; } })();
    const initial = saved
      || (/Win/i.test(navigator.platform) ? 'windows' : 'mac');
    activateOs(initial);

    document.querySelectorAll('.os-tabs .tab').forEach(btn => {
      btn.addEventListener('click', () => activateOs(btn.dataset.os));
    });
  }

  function initCopyButtons() {
    document.querySelectorAll('.code').forEach(block => {
      if (block.querySelector('.copy')) return;
      const pre = block.querySelector('pre');
      if (!pre) return;
      const btn = document.createElement('button');
      btn.className = 'copy';
      btn.type = 'button';
      btn.textContent = 'Copy';
      btn.addEventListener('click', async () => {
        try {
          await navigator.clipboard.writeText(pre.textContent.trim());
          btn.textContent = 'Copied';
          btn.classList.add('copied');
          setTimeout(() => {
            btn.textContent = 'Copy';
            btn.classList.remove('copied');
          }, 1600);
        } catch (err) {
          btn.textContent = 'Press ⌘C';
          setTimeout(() => { btn.textContent = 'Copy'; }, 1600);
        }
      });
      block.appendChild(btn);
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    initOsTabs();
    initCopyButtons();
  });
})();
