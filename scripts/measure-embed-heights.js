// Measures the full rendered height of every page in a built Jekyll site (_site/) and writes
// _data/embed_heights.json, mapping each page's url (matching Liquid's `page.url`, e.g.
// "/foundations/fdd2/2_2.html") to a height in px. _includes/footer_custom.html reads this map
// to size each page's "Copy Embed for Schoology" iframe snippet to the page's real content
// height, so the exit ticket (or any other content near the bottom) is never cut off by a
// fixed guess that's wrong for most pages.
//
// Pages are served over a local HTTP server rather than opened as file:// URLs: the site's
// stylesheets, fonts, and scripts use root-relative paths (/assets/...), which resolve against
// the filesystem root under file://, so the page renders unstyled and measures 2-3x taller than
// it really is -- which is exactly how the iframes ended up with thousands of pixels of blank
// space below the content.
//
// Each page is measured at several widths spanning a plausible Schoology content column, and
// the tallest wins: text reflows taller as the iframe narrows, and a small overshoot is far
// better than cutting off the exit ticket at the bottom.
//
// Run this after `bundle exec jekyll build` (the _site/ directory must be current), any time
// lesson content changes enough to shift page heights materially:
//
//   bundle exec jekyll build && node scripts/measure-embed-heights.js
//
// This does not run as part of the Cloudflare Pages build (Ruby-only there) -- like the
// worksheet PDFs and syllabus PDFs, _data/embed_heights.json is generated locally and checked
// into the repo.

const fs = require('fs');
const http = require('http');
const path = require('path');

const PLAYWRIGHT_BIN = '/opt/node22/lib/node_modules/playwright';
const CHROMIUM_EXECUTABLE = '/opt/pw-browsers/chromium';
const ROOT = path.resolve(__dirname, '..');
const SITE_DIR = path.join(ROOT, '_site');
const OUT_PATH = path.join(ROOT, '_data', 'embed_heights.json');

const WIDTHS = [700, 800, 900, 1000];
const PADDING = 40; // small buffer so the iframe isn't a pixel-exact, hairline-clipped fit
const MIN_HEIGHT = 400;

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css',
  '.js': 'text/javascript',
  '.json': 'application/json',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.pdf': 'application/pdf',
};

function walk(dir, out) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walk(full, out);
    } else if (entry.isFile() && entry.name.endsWith('.html')) {
      out.push(full);
    }
  }
  return out;
}

function startServer() {
  const server = http.createServer((req, res) => {
    let rel = decodeURIComponent(req.url.split('?')[0]);
    let file = path.join(SITE_DIR, rel);
    if (!file.startsWith(SITE_DIR)) {
      res.writeHead(403).end();
      return;
    }
    if (fs.existsSync(file) && fs.statSync(file).isDirectory()) {
      file = path.join(file, 'index.html');
    }
    fs.readFile(file, (err, data) => {
      if (err) {
        res.writeHead(404).end();
        return;
      }
      res.writeHead(200, { 'Content-Type': MIME[path.extname(file)] || 'application/octet-stream' });
      res.end(data);
    });
  });
  return new Promise((resolve) => server.listen(0, '127.0.0.1', () => resolve(server)));
}

(async () => {
  if (!fs.existsSync(SITE_DIR)) {
    console.error(`${SITE_DIR} not found -- run "bundle exec jekyll build" first.`);
    process.exit(1);
  }

  // Reveal.js decks and other raw HTML under /assets/ never carry the embed footer.
  const files = walk(SITE_DIR, []).filter(
    (f) => !path.relative(SITE_DIR, f).startsWith('assets' + path.sep)
  );

  const server = await startServer();
  const base = `http://127.0.0.1:${server.address().port}`;

  const { chromium } = require(PLAYWRIGHT_BIN);
  const browser = await chromium.launch({ executablePath: CHROMIUM_EXECUTABLE });
  // Short viewport so a short page's scrollHeight isn't floored at the viewport height.
  const page = await browser.newPage({ viewport: { width: WIDTHS[0], height: 300 } });

  const heights = {};
  for (const file of files) {
    let url = '/' + path.relative(SITE_DIR, file).split(path.sep).join('/');
    const fetchUrl = url;
    // Jekyll serves foo/index.html as page.url == "/foo/", not "/foo/index.html".
    if (url === '/index.html') {
      url = '/';
    } else if (url.endsWith('/index.html')) {
      url = url.slice(0, -'index.html'.length);
    }

    await page.setViewportSize({ width: WIDTHS[0], height: 300 });
    // Same ?embed=1 content-only layout the Schoology iframe loads (see head_custom.html).
    await page.goto(base + fetchUrl + '?embed=1', { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);

    let tallest = 0;
    for (const width of WIDTHS) {
      await page.setViewportSize({ width, height: 300 });
      const h = await page.evaluate(
        () => new Promise((resolve) =>
          requestAnimationFrame(() => resolve(document.documentElement.scrollHeight))
        )
      );
      tallest = Math.max(tallest, h);
    }
    heights[url] = Math.max(MIN_HEIGHT, Math.ceil((tallest + PADDING) / 50) * 50);
  }

  await browser.close();
  server.close();

  const sorted = Object.keys(heights).sort().reduce((acc, k) => {
    acc[k] = heights[k];
    return acc;
  }, {});
  fs.writeFileSync(OUT_PATH, JSON.stringify(sorted, null, 2) + '\n');
  console.log(`Wrote ${Object.keys(sorted).length} page heights to ${path.relative(ROOT, OUT_PATH)}`);
})();
