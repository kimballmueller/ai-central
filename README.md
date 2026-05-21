# kimballmueller.github.io

My personal link hub. Static HTML/CSS/JS — no build step, no framework, deploys straight to GitHub Pages.

- **Homepage** (`index.html`) — name, tagline, link buttons, social row.
- **Free Resource Guide** (`resources.html`) — downloadables grouped by the video they came from.

---

## Editing content

Everything you'll change day-to-day lives in `data/`. Markup is untouched.

### Update a homepage button

Open `data/links.json` and edit the entry. Example — paste in your real YouTube URL:

```json
{ "label": "YouTube", "url": "https://youtube.com/@kimballmueller", "icon": "youtube" }
```

Placeholders to replace once you have the real URLs:

- `YOUR_YOUTUBE_URL`
- `YOUR_BOOKING_URL`
- `YOUR_IG_URL`
- `YOUR_TIKTOK_URL`

### Add a new video's resources (the main loop)

Open `data/resources.json`. Add one object to the `videos` array — newest first:

```json
{
  "title": "How I Set Up an AI Cold Caller in 20 Minutes",
  "youtubeUrl": "https://youtube.com/watch?v=xxxxxx",
  "publishedAt": "2026-05-21",
  "description": "One-line hook for the resources page.",
  "resources": [
    { "label": "GHL workflow JSON", "url": "https://...", "type": "Template" },
    { "label": "Cold call script",  "url": "https://...", "type": "PDF" }
  ]
}
```

Commit, push — live within ~1 minute.

Valid `type` values are anything you want; common ones: `PDF`, `Template`, `Tool`, `Script`, `Workflow`, `Link`.

### Headshot

Drop a square JPG at `assets/headshot.jpg`. Until you do, the page shows a clean gradient circle.

### Tagline / name

Edit `name` and `tagline` in `data/links.json`.

---

## Local preview

From the project root:

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>. (Opening the HTML files directly with `file://` won't work because the JSON fetch is blocked — that's why the local server.)

---

## Deploying to GitHub Pages

One-time setup:

```bash
git init
git add .
git commit -m "Initial site"
gh repo create kimballmueller.github.io --public --source=. --remote=origin --push
```

That special repo name (`<username>.github.io`) means GitHub serves it at `https://kimballmueller.github.io` automatically. Enable Pages in repo Settings → Pages → "Deploy from a branch" → `main` / `/ (root)` if it's not on by default.

After that, every push to `main` updates the live site within ~60 seconds.

### Custom domain later

Add a file named `CNAME` at the repo root containing just the domain (e.g. `kimballmueller.com`). Point an `A` record at GitHub Pages' IPs (185.199.108.153, etc. — see GitHub docs) or a `CNAME` record at `kimballmueller.github.io`.

---

## File layout

```
index.html                                Homepage
resources.html                            Resource Guide page
guides/
  claude-code-quickstart.html             First published guide
  <future-guide>.html                     Add more guides here
assets/
  styles.css                              Mesh gradient, glassmorphism, responsive
  guide.css                               Long-form prose, OS tabs, callouts (guide pages only)
  app.js                                  Renders index/resources from data/*.json
  guide.js                                OS tab + copy-to-clipboard (guide pages only)
  favicon.svg                             Gradient "K" mark
  headshot.png                            Avatar shown on the homepage
  disruptors-logo.png                     On hand for future use
  guides/
    hero.png                              Hero image for the Claude Code guide
data/
  links.json                              Homepage config
  resources.json                          Resource library
.nojekyll                                 Tells GH Pages not to run Jekyll
```

## Adding a new guide

1. Write the guide as a new HTML file in `guides/` — copy `claude-code-quickstart.html` as a template.
2. (Optional) drop a hero image at `assets/guides/<slug>.png`.
3. Open `data/resources.json` and add an entry whose `resources[]` link points to `guides/<slug>.html`.
4. Commit, push.
