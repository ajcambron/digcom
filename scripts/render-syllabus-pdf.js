// Renders a course's live syllabus page into a printable, fillable PDF: adds an
// "Initial" blank in front of every Parent/Guardian and Student Agreement bullet,
// appends signature/date/printed-name lines for both parties, then scales the print
// layout down (Playwright's page.pdf `scale` option) until it fits exactly 4 pages --
// the largest scale that still does, so it stays as readable as possible.
//
// Every hyperlink in the page (mailto, external, internal, and the self-referential
// "see the PDF version" link) is unwrapped to plain text before printing -- a signed
// paper document has no clickable links, and Chrome's print-to-PDF otherwise bakes in
// both a colored/underlined link style and a real clickable link annotation, neither
// of which makes sense on something meant to be printed and signed.
//
// This replaces the old workflow of hand-maintaining a separate Google Doc copy of
// the syllabus for printing: the PDF is now generated straight from the same
// Markdown that drives the live page, so the two can never drift out of sync.
//
// Requires: Playwright (global install; see PLAYWRIGHT_BIN below) and the `pdfinfo`
// CLI (poppler-utils) for page counting. Requires the Jekyll site to already be
// built and served locally (this script only renders and PDFs an existing URL).
//
// Usage:
//   bundle exec jekyll build
//   npx http-server _site -p 8140 -s &
//   node scripts/render-syllabus-pdf.js fdd http://localhost:8140/foundations/fdd0/syllabus.html assets/syllabus/fdd-syllabus.pdf
//   node scripts/render-syllabus-pdf.js add http://localhost:8140/applications/add0/syllabus.html assets/syllabus/add-syllabus.pdf

const { execFileSync } = require('child_process');
const path = require('path');

const PLAYWRIGHT_BIN = '/opt/node22/lib/node_modules/playwright';
const CHROMIUM_EXECUTABLE = '/opt/pw-browsers/chromium';

const [, , courseLabel, url, outPath] = process.argv;
if (!courseLabel || !url || !outPath) {
  console.error('Usage: node render-syllabus-pdf.js <courseLabel> <syllabusUrl> <outPdfPath>');
  process.exit(1);
}

const FILL_SCRIPT = `
(() => {
  // Unwrap every hyperlink in the printable content to plain text: no color/underline
  // styling, no clickable link annotation in the resulting PDF.
  const links = Array.from(document.querySelectorAll('.main-content a[href]'));
  for (const a of links) {
    const text = document.createTextNode(a.textContent);
    a.replaceWith(text);
  }

  const AGREEMENT_HEADERS = ['Parent/Guardian Agreement', 'Student Agreement'];
  const paragraphs = Array.from(document.querySelectorAll('.main-content p'));

  for (const heading of AGREEMENT_HEADERS) {
    const headerP = paragraphs.find(p => p.textContent.trim() === heading);
    if (!headerP) continue;
    let list = headerP.nextElementSibling;
    while (list && list.tagName !== 'UL') list = list.nextElementSibling;
    if (!list) continue;
    for (const li of list.children) {
      const blank = document.createElement('span');
      blank.className = 'pdf-initial';
      blank.setAttribute('aria-hidden', 'true');
      li.prepend(blank);
    }
  }

  // Signature block: appended after the Student Agreement list (the last one on the page).
  const studentHeaderP = paragraphs.find(p => p.textContent.trim() === 'Student Agreement');
  let anchor = studentHeaderP;
  while (anchor && anchor.nextElementSibling && anchor.nextElementSibling.tagName !== 'UL') anchor = anchor.nextElementSibling;
  if (anchor && anchor.nextElementSibling) anchor = anchor.nextElementSibling; // the UL itself

  if (anchor) {
    const block = document.createElement('div');
    block.className = 'pdf-signature-block';
    block.innerHTML = \`
      <div class="pdf-sign-row">
        <div class="pdf-sign-field pdf-sign-line"><span class="pdf-sign-label">Student Signature</span></div>
        <div class="pdf-sign-field pdf-date-line"><span class="pdf-sign-label">Date</span></div>
      </div>
      <div class="pdf-sign-row">
        <div class="pdf-sign-field pdf-sign-line"><span class="pdf-sign-label">Parent/Guardian Signature</span></div>
        <div class="pdf-sign-field pdf-date-line"><span class="pdf-sign-label">Date</span></div>
      </div>
      <div class="pdf-sign-row">
        <div class="pdf-sign-field pdf-sign-line"><span class="pdf-sign-label">Printed Name (Parent/Guardian)</span></div>
      </div>
    \`;
    anchor.insertAdjacentElement('afterend', block);
  }
})();
`;

const PRINT_CSS = `
  .pdf-initial {
    display: inline-block;
    width: 2.4em;
    height: 1em;
    margin-right: 0.5em;
    border-bottom: 1px solid #2A2118;
    vertical-align: -0.15em;
  }
  .pdf-signature-block {
    margin-top: 1.6em;
    page-break-inside: avoid;
  }
  .pdf-sign-row {
    display: flex;
    gap: 2em;
    margin-bottom: 1.6em;
  }
  .pdf-sign-field {
    display: flex;
    flex-direction: column-reverse;
  }
  .pdf-sign-line { flex: 3; border-top: 1px solid #2A2118; padding-top: 0.3em; }
  .pdf-date-line { flex: 1; border-top: 1px solid #2A2118; padding-top: 0.3em; }
  .pdf-sign-label { font-size: 0.75em; text-transform: uppercase; letter-spacing: 0.05em; color: #6B6255; }
  h2 { page-break-after: avoid; }
  table, .table-wrapper { page-break-inside: avoid; }
  a, a:visited { color: inherit; text-decoration: none; }

  /* Strip just-the-docs callout boxes (highlight/warning/discussion/reflection/good/vocab)
     back to a plain, unstyled paragraph -- no colored box, border, or generated label. */
  .main-content .highlight, .main-content .warning, .main-content .discussion,
  .main-content .reflection, .main-content .good, .main-content .vocab {
    background: none !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 1em 0 !important;
    border-radius: 0 !important;
    color: inherit !important;
  }
  .highlight::before, .warning::before, .discussion::before,
  .reflection::before, .good::before, .vocab::before {
    display: none !important;
  }
`;

function countPages(pdfPath) {
  const out = execFileSync('pdfinfo', [pdfPath]).toString();
  const m = out.match(/^Pages:\s+(\d+)/m);
  return parseInt(m[1], 10);
}

async function renderAt(page, scale, outPath) {
  await page.pdf({
    path: outPath,
    format: 'Letter',
    printBackground: true,
    scale,
    margin: { top: '0.5in', bottom: '0.5in', left: '0.6in', right: '0.6in' },
  });
  return countPages(outPath);
}

(async () => {
  const { chromium } = require(PLAYWRIGHT_BIN);
  const browser = await chromium.launch({ executablePath: CHROMIUM_EXECUTABLE });
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(FILL_SCRIPT);
  await page.addStyleTag({ content: PRINT_CSS });
  await page.emulateMedia({ media: 'print' });

  const TARGET_PAGES = 4;
  let lo = 0.5, hi = 1.0;
  let bestScale = null;
  let bestPages = null;

  // First check scale=1.0 -- if it already fits, we're done (no need to shrink).
  const pagesAtFull = await renderAt(page, hi, outPath);
  if (pagesAtFull <= TARGET_PAGES) {
    console.log(`${courseLabel}: fits in ${pagesAtFull} pages at scale 1.0 -- no scaling needed.`);
    await browser.close();
    return;
  }

  // Binary search for the largest scale that still fits TARGET_PAGES.
  for (let i = 0; i < 9; i++) {
    const mid = (lo + hi) / 2;
    const pages = await renderAt(page, mid, outPath);
    console.log(`${courseLabel}: scale=${mid.toFixed(3)} -> ${pages} pages`);
    if (pages <= TARGET_PAGES) {
      bestScale = mid;
      bestPages = pages;
      lo = mid; // try a larger (less-shrunk) scale
    } else {
      hi = mid; // still too big, shrink more
    }
  }

  if (bestScale === null) {
    console.error(`${courseLabel}: could not fit ${TARGET_PAGES} pages even at scale ${lo.toFixed(3)} (lower bound). Rendering at lower bound anyway.`);
    await renderAt(page, lo, outPath);
  } else {
    await renderAt(page, bestScale, outPath); // final render at the winning scale
    console.log(`${courseLabel}: final scale=${bestScale.toFixed(3)}, ${bestPages} pages -> ${outPath}`);
  }

  await browser.close();
})();
