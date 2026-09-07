// Adds a "Download Vocabulary (CSV)" button after every vocab callout (<dl class="vocab">)
// on the page. Reads the term/definition pairs directly from the rendered list, so there's
// no separate data source to keep in sync with the _includes/vocab/*.md files.
(function () {
  function csvField(value) {
    var s = String(value).replace(/\s+/g, ' ').trim();
    if (/[",\n]/.test(s)) {
      s = '"' + s.replace(/"/g, '""') + '"';
    }
    return s;
  }

  function dlToCsv(dl) {
    var rows = [['Term', 'Definition']];
    var terms = dl.querySelectorAll('dt');
    terms.forEach(function (dt) {
      var term = dt.textContent;
      var dd = dt.nextElementSibling;
      var defs = [];
      while (dd && dd.tagName === 'DD') {
        defs.push(dd.textContent);
        dd = dd.nextElementSibling;
      }
      rows.push([term, defs.join(' ')]);
    });
    return rows.map(function (row) {
      return row.map(csvField).join(',');
    }).join('\r\n');
  }

  function slugify(text) {
    return String(text)
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/(^-|-$)/g, '') || 'vocabulary';
  }

  function addButtons() {
    var lists = document.querySelectorAll('dl.vocab');
    lists.forEach(function (dl, index) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'vocab-csv-btn';
      btn.textContent = '⬇ Download Vocabulary (CSV)';
      btn.addEventListener('click', function () {
        var csv = dlToCsv(dl);
        var blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        var base = slugify(document.title || 'vocabulary');
        var suffix = lists.length > 1 ? '-' + (index + 1) : '';
        a.href = url;
        a.download = base + suffix + '-vocab.csv';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      });
      dl.insertAdjacentElement('afterend', btn);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', addButtons);
  } else {
    addButtons();
  }
})();
