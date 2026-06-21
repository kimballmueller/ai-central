// Tiny renderer for both pages. Detects which root container is present
// and loads the matching JSON file. No deps, no build.

const ICONS = {
  gift:     '<path d="M20 12v10H4V12"/><path d="M2 7h20v5H2z"/><path d="M12 22V7"/><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"/><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/>',
  youtube:  '<path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.25 29 29 0 0 0-.46-5.33z"/><polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02" fill="currentColor" stroke="none"/>',
  calendar: '<rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
  building: '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M12 6h.01"/><path d="M8 10h.01"/><path d="M16 10h.01"/><path d="M12 10h.01"/><path d="M8 14h.01"/><path d="M16 14h.01"/><path d="M12 14h.01"/>',
  mail:     '<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>',
  users:    '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
  instagram:'<rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/>',
  tiktok:   '<path d="M9 12a4 4 0 1 0 4 4V4c0 3 2 5 5 5"/>',
  chevron:  '<polyline points="9 18 15 12 9 6"/>',
  arrowLeft:'<line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/>'
};

function svg(name, opts = {}) {
  const path = ICONS[name];
  if (!path) return '';
  const cls = opts.class ? ` class="${opts.class}"` : '';
  return `<svg${cls} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${path}</svg>`;
}

function el(html) {
  const t = document.createElement('template');
  t.innerHTML = html.trim();
  return t.content.firstElementChild;
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}

// Pull the 11-char video id out of any YouTube URL form.
function youtubeId(url) {
  const m = String(url || '').match(/(?:v=|youtu\.be\/|embed\/)([\w-]{11})/);
  return m ? m[1] : '';
}

// ---------- Homepage ----------
function renderHomepage(root, data) {
  // Probe the image: only swap in the photo if it actually loads.
  // Until then (or if it 404s), the gradient .avatar div is shown.
  const avatar = `<div class="avatar" role="img" aria-label="${escapeHtml(data.name)}"></div>`;
  if (data.avatar) {
    const probe = new Image();
    probe.onload = () => {
      const el = root.querySelector('.avatar');
      if (el) el.style.backgroundImage = `url("${data.avatar}")`;
    };
    probe.src = data.avatar;
  }

  const buttons = data.buttons.map(b => {
    const classes = ['btn'];
    if (b.primary) classes.push('primary');
    if (b.comingSoon) classes.push('coming-soon');
    const target = (/^https?:/i.test(b.url)) ? ' target="_blank" rel="noopener"' : '';
    const trailing = b.comingSoon
      ? `<span class="badge">Coming Soon</span>`
      : svg('chevron', { class: 'chevron' });
    return `
      <a class="${classes.join(' ')}" href="${escapeHtml(b.url)}"${target}>
        <span class="icon">${svg(b.icon)}</span>
        <span class="label">${escapeHtml(b.label)}</span>
        ${trailing}
      </a>`;
  }).join('');

  const socials = (data.socials || []).map(s => `
    <a href="${escapeHtml(s.url)}" target="_blank" rel="noopener" aria-label="${escapeHtml(s.platform)}">
      ${svg(s.platform)}
    </a>`).join('');

  const taglineHtml = (() => {
    if (!data.tagline) return '';
    const lines = Array.isArray(data.tagline) ? data.tagline : [data.tagline];
    return `<p class="tagline">${lines.map(escapeHtml).join('<br>')}</p>`;
  })();

  root.innerHTML = `
    ${avatar}
    <h1 class="name">${escapeHtml(data.name)}</h1>
    ${data.role ? `<p class="role">${escapeHtml(data.role)}</p>` : ''}
    ${taglineHtml}
    <div class="stack">${buttons}</div>
    ${socials ? `<div class="socials">${socials}</div>` : ''}
  `;
}

// ---------- Resources page ----------
function renderResources(root, data) {
  const videos = [...(data.videos || [])].sort((a, b) => {
    return String(b.publishedAt || '').localeCompare(String(a.publishedAt || ''));
  });

  if (videos.length === 0) {
    root.innerHTML = `<p class="empty">No resources posted yet. Check back soon.</p>`;
    return;
  }

  const cards = videos.map(v => {
    const items = (v.resources || []).map(r => `
      <li>
        <a href="${escapeHtml(r.url)}" target="_blank" rel="noopener">
          <span class="r-label">${escapeHtml(r.label)}</span>
          ${r.type ? `<span class="r-type">${escapeHtml(r.type)}</span>` : ''}
        </a>
      </li>`).join('');

    const yt = v.youtubeUrl
      ? `<a class="yt-link" href="${escapeHtml(v.youtubeUrl)}" target="_blank" rel="noopener">${svg('youtube')}Watch</a>`
      : (v.comingSoon ? `<span class="yt-link soon">${svg('youtube')}Coming Soon</span>` : '');

    const meta = v.publishedAt ? `<p class="video-meta">Posted ${escapeHtml(v.publishedAt)}</p>` : '';
    const desc = v.description ? `<p class="video-desc">${escapeHtml(v.description)}</p>` : '';

    const embedId = v.embed ? youtubeId(v.youtubeUrl) : '';
    const embed = embedId
      ? `<div class="video-embed"><iframe src="https://www.youtube.com/embed/${escapeHtml(embedId)}" title="${escapeHtml(v.title)}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>`
      : '';

    const list = items
      ? `<div class="divider"></div><ul class="resource-list">${items}</ul>`
      : '';

    return `
      <article class="video-card">
        <div class="video-head">
          <div style="flex:1">
            <h2 class="video-title">${escapeHtml(v.title)}</h2>
            ${meta}
          </div>
          ${embed ? '' : yt}
        </div>
        ${desc}
        ${embed}
        ${list}
      </article>`;
  }).join('');

  root.innerHTML = `<div class="videos">${cards}</div>`;
}

// ---------- Bootstrap ----------
async function loadJson(path) {
  const res = await fetch(path, { cache: 'no-cache' });
  if (!res.ok) throw new Error(`Failed to load ${path}: ${res.status}`);
  return res.json();
}

(async function init() {
  const home = document.getElementById('home-root');
  const resources = document.getElementById('resources-root');

  try {
    if (home) {
      const data = await loadJson('data/links.json');
      renderHomepage(home, data);
    } else if (resources) {
      const data = await loadJson('data/resources.json');
      renderResources(resources, data);
    }
  } catch (err) {
    console.error(err);
    const target = home || resources;
    if (target) {
      target.innerHTML = `<p class="empty">Couldn't load content. If you're opening this file directly, run a local server: <code>python3 -m http.server</code></p>`;
    }
  }
})();
