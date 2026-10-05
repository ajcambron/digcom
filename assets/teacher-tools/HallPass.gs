/**
 * Hall Pass: Google Docs generator (container-bound Apps Script)
 *
 * Rebuilds this Doc as a one-page letter bathroom pass with today's date
 * microprinted through every section, in three formats. Two entry points:
 *
 *   Hall Pass > Issue pass now   Rebuilds with the date AND the current time
 *                                pre-filled in TIME OUT. Use right before printing.
 *   Daily 6 AM trigger           Rebuilds with the new date and a blank TIME OUT
 *                                (a time stamped at 6 AM would be wrong by 8 AM).
 *
 * Setup: Extensions > Apps Script, paste this file, save, run setup() once
 * and approve the permissions prompt.
 */

const CFG = {
  school: 'NEWARK HIGH SCHOOL',
  tz: 'America/New_York',
  triggerHour: 6,
  gold: '#FFCC00',
  micro: '#BDBDBD',
  microOnGold: '#8F7300',
  cols: 185            // monospace characters per microprint line at 5 pt
};

function onOpen() {
  DocumentApp.getUi().createMenu('Hall Pass')
    .addItem('Issue pass now (stamps time out)', 'issuePass')
    .addItem('Refresh date only (blank time out)', 'refreshDate')
    .addItem('Install daily refresh', 'installTrigger')
    .addToUi();
}

function setup() {
  PropertiesService.getScriptProperties()
    .setProperty('DOC_ID', DocumentApp.getActiveDocument().getId());
  installTrigger();
  refreshDate();
}

function installTrigger() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'refreshDate') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('refreshDate').timeBased()
    .everyDays(1).atHour(CFG.triggerHour).inTimezone(CFG.tz).create();
}

function issuePass() { build_(true); }
function refreshDate() { build_(false); }

function getDoc_() {
  const id = PropertiesService.getScriptProperties().getProperty('DOC_ID');
  return id ? DocumentApp.openById(id) : DocumentApp.getActiveDocument();
}

/* ---------- helpers ---------- */

function para_(c, text) {
  const n = c.getNumChildren();
  const last = n ? c.getChild(n - 1) : null;
  let p;
  if (last && last.getType() === DocumentApp.ElementType.PARAGRAPH &&
      last.asParagraph().getText() === '') {
    p = last.asParagraph();
    p.setText(text);
  } else {
    p = c.appendParagraph(text);
  }
  return p;
}

function style_(p, o) {
  p.setFontFamily(o.font || 'Roboto');
  p.setFontSize(o.size || 10);
  p.setBold(!!o.bold);
  p.setForegroundColor(o.color || '#000000');
  p.setSpacingBefore(o.before || 0);
  p.setSpacingAfter(o.after || 0);
  p.setLineSpacing(o.line || 1);
  p.setAlignment(o.align || DocumentApp.HorizontalAlignment.LEFT);
  return p;
}

function micro_(c, n, color, tokens, seed) {
  for (let i = 0; i < n; i++) {
    const k = seed + i;
    const tok = tokens[k % tokens.length] + ' ';
    const off = (k * 11) % tok.length;
    const s = tok.repeat(Math.ceil(CFG.cols / tok.length) + 2).substr(off, CFG.cols);
    style_(para_(c, s), { font: 'Roboto Mono', size: 5, color: color });
  }
}

function band_(body, color) {
  const t = body.appendTable([['']]);
  t.setBorderWidth(0);
  const cell = t.getCell(0, 0);
  cell.setBackgroundColor(color);
  cell.setPaddingTop(2); cell.setPaddingBottom(2);
  cell.setPaddingLeft(6); cell.setPaddingRight(6);
  return cell;
}

function label_(c, text) {
  style_(para_(c, '// ' + text), { size: 9, bold: true, before: 4 });
}

function line_(c, chars, text, opts) {
  const o = opts || {};
  style_(para_(c, text || '_'.repeat(chars)), {
    font: text ? 'Roboto Slab' : 'Roboto Mono',
    size: text ? 18 : 12, bold: !!text, before: o.before === undefined ? 14 : o.before
  });
}

function pair_(body, l1, v1, l2, v2) {
  const t = body.appendTable([['', '']]);
  t.setBorderWidth(0);
  [[0, l1, v1], [1, l2, v2]].forEach(function (x) {
    const c = t.getCell(0, x[0]);
    c.setPaddingLeft(0); c.setPaddingRight(8);
    label_(c, x[1]);
    line_(c, 36, x[2]);
  });
}

/* ---------- builder ---------- */

function build_(stampTime) {
  const doc = getDoc_();
  const body = doc.getBody();
  const now = new Date();
  const f = function (p) { return Utilities.formatDate(now, CFG.tz, p).toUpperCase(); };
  const d = {
    long: f('EEE, MMM d, yyyy'),
    a: f('EEE MM/dd/yy'),
    b: f('MMMM d yyyy'),
    c: f('MM-dd-yyyy EEE')
  };
  const time = stampTime ? f('h:mm a') : '';
  const tokens = [d.a, d.b, d.c];
  if (time) tokens.push(d.a + ' ' + time);

  body.clear();
  body.setPageWidth(612);
  body.setPageHeight(792);
  body.setMarginTop(18); body.setMarginBottom(18);
  body.setMarginLeft(18); body.setMarginRight(18);

  let seed = 0;
  const m = function (c, n, color) { micro_(c, n, color || CFG.micro, tokens, seed); seed += n; };

  // Header
  m(body, 5);
  style_(para_(body, '// ' + CFG.school), { size: 9, bold: true });
  const h = para_(body, 'HALL PASS');
  style_(h, { size: 52, bold: true, line: 1 });
  h.editAsText().setFontFamily(0, 4, 'Roboto Light').setBold(0, 4, false);
  const rule = band_(body, CFG.gold);
  style_(para_(rule, ' '), { size: 3 });
  m(body, 4);

  // Date band
  const band = band_(body, CFG.gold);
  m(band, 3, CFG.microOnGold);
  style_(para_(band, '// VALID ONLY ON'), { size: 9, bold: true, before: 2 });
  style_(para_(band, d.long), { font: 'Roboto Slab', size: 40, bold: true });
  m(band, 3, CFG.microOnGold);
  m(body, 4);

  // Fields
  label_(body, 'STUDENT NAME');
  line_(body, 76);
  m(body, 3);
  pair_(body, 'PERIOD', '', 'TEACHER', '');
  m(body, 3);
  pair_(body, 'TIME OUT', time, 'TIME IN', '');
  m(body, 3);
  label_(body, 'DESTINATION');
  style_(para_(body, '☐ RESTROOM      ☐ NURSE      ☐ OFFICE      ☐ OTHER'),
    { size: 12, before: 8 });
  m(body, 3);
  label_(body, 'TEACHER SIGNATURE');
  line_(body, 76);
  m(body, 4);

  // Footer band
  const foot = band_(body, CFG.gold);
  m(foot, 2, CFG.microOnGold);
  style_(para_(foot, 'ALTERED OR UNDATED PASSES ARE VOID'), { size: 14, bold: true, before: 2 });
  style_(para_(foot, d.long + (time ? ' | OUT ' + time : '') + ' | RETURN TO CLASS'),
    { font: 'Roboto Slab', size: 11, bold: true });
  m(foot, 2, CFG.microOnGold);
}
