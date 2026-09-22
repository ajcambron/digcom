// Renders worksheet-sources/*.html files to assets/worksheets/{name}.pdf plus a
// {name}-preview.png thumbnail, matching the existing worksheet PDF/preview pairs.
//
// Usage:
//   node scripts/render-worksheets.js name1 name2 name3 ...
// (names are the worksheet-sources/*.html basenames, no extension)

const path = require('path');

const PLAYWRIGHT_BIN = '/opt/node22/lib/node_modules/playwright';
const CHROMIUM_EXECUTABLE = '/opt/pw-browsers/chromium';
const ROOT = path.resolve(__dirname, '..');

const names = process.argv.slice(2);
if (names.length === 0) {
  console.error('Usage: node render-worksheets.js name1 name2 ...');
  process.exit(1);
}

(async () => {
  const { chromium } = require(PLAYWRIGHT_BIN);
  const browser = await chromium.launch({ executablePath: CHROMIUM_EXECUTABLE });

  for (const name of names) {
    const srcPath = path.join(ROOT, 'worksheet-sources', `${name}.html`);
    const pdfPath = path.join(ROOT, 'assets', 'worksheets', `${name}.pdf`);
    const previewPath = path.join(ROOT, 'assets', 'worksheets', `${name}-preview.png`);

    const page = await browser.newPage();
    await page.goto(`file://${srcPath}`, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);

    await page.pdf({
      path: pdfPath,
      format: 'Letter',
      printBackground: true,
      margin: { top: '0', bottom: '0', left: '0', right: '0' },
    });

    await page.setViewportSize({ width: 850, height: 1100 });
    await page.screenshot({ path: previewPath });

    await page.close();
    console.log(`Rendered ${name}`);
  }

  await browser.close();
})();
