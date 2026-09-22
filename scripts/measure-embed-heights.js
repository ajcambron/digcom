// Measures the full rendered height of every page in a built Jekyll site (_site/) and writes
// _data/embed_heights.json, mapping each page's url (matching Liquid's `page.url`, e.g.
// "/foundations/fdd2/2_2.html") to a height in px. _includes/footer_custom.html reads this map
// to size each page's "Copy Embed for Schoology" iframe snippet to the page's real content
// height, so the exit ticket (or any other content near the bottom) is never cut off by a
// fixed guess that's wrong for most pages.
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
const path = require('path');

const PLAYWRIGHT_BIN = '/opt/node22/lib/node_modules/playwright';
const CHROMIUM_EXECUTABLE = '/opt/pw-browsers/chromium';
const ROOT = path.resolve(__dirname, '..');
const SITE_DIR = path.join(ROOT, '_site');
const OUT_PATH = path.join(ROOT, '_data', 'embed_heights.json');

const PADDING = 40; // small buffer so the iframe isn't a pixel-exact, hairline-clipped fit
const MIN_HEIGHT = 400;

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

(async () => {
  if (!fs.existsSync(SITE_DIR)) {
    console.error(`${SITE_DIR} not found -- run "bundle exec jekyll build" first.`);
    process.exit(1);
  }

  const files = walk(SITE_DIR, []);
  const { chromium } = require(PLAYWRIGHT_BIN);
  const browser = await chromium.launch({ executablePath: CHROMIUM_EXECUTABLE });
  const page = await browser.newPage({ viewport: { width: 1100, height: 800 } });

  const heights = {};
  for (const file of files) {
    let url = '/' + path.relative(SITE_DIR, file).split(path.sep).join('/');
    // Jekyll serves foo/index.html as page.url == "/foo/", not "/foo/index.html".
    if (url === '/index.html') {
      url = '/';
    } else if (url.endsWith('/index.html')) {
      url = url.slice(0, -'index.html'.length);
    }
    await page.goto('file://' + file, { waitUntil: 'networkidle' });
    const height = await page.evaluate(() => {
      const main = document.querySelector('#main-content');
      return main ? main.scrollHeight : document.documentElement.scrollHeight;
    });
    heights[url] = Math.max(MIN_HEIGHT, Math.ceil((height + PADDING) / 50) * 50);
  }

  await browser.close();

  const sorted = Object.keys(heights).sort().reduce((acc, k) => {
    acc[k] = heights[k];
    return acc;
  }, {});
  fs.writeFileSync(OUT_PATH, JSON.stringify(sorted, null, 2) + '\n');
  console.log(`Wrote ${Object.keys(sorted).length} page heights to ${path.relative(ROOT, OUT_PATH)}`);
})();
