// Adds a "Download Schoology Vocab Quiz" button to unit overview pages. It reads the unit's
// combined vocab list (<dl class="vocab"> rendered by _includes/unit-vocab.html), builds one
// auto-graded multiple-choice question per term, and downloads a QTI 2.1 package (.zip) that
// Schoology can import as an assessment.
//
// Randomization, per click: each term is asked in a random direction (term -> pick the
// definition, or definition -> pick the term), wrong answers are drawn at random from the
// unit's other terms, and both the question order and the answer order are shuffled. Every
// download is stamped with a short version code so different versions can be told apart.
// Because it reads the rendered page, an updated vocab list is picked up on the next click.
(function () {
  // ---------- helpers ----------
  function shuffle(list) {
    var a = list.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function versionCode() {
    var chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    var s = '';
    for (var i = 0; i < 4; i++) s += chars[Math.floor(Math.random() * chars.length)];
    return s;
  }

  function xml(value) {
    return String(value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function clean(text) {
    return String(text).replace(/\s+/g, ' ').trim();
  }

  function escapeRegex(s) {
    return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  // Blank out a term (and the parts of a compound term like "Source/Program Monitor" or
  // "Raster (Bitmap)") inside its own definition, so the definition doesn't give the answer away.
  function maskTerm(definition, term) {
    var parts = [term].concat(term.split(/[\/()]/));
    var out = definition;
    parts
      .map(clean)
      .filter(function (p) { return p.length >= 4; })
      .reduce(function (all, p) {   // "Toolbars" should also blank out "toolbar"
        return all.concat(/s$/i.test(p) && p.length > 4 ? [p, p.slice(0, -1)] : [p]);
      }, [])
      .sort(function (a, b) { return b.length - a.length; })
      .forEach(function (p) {
        out = out.replace(new RegExp('\\b' + escapeRegex(p) + '(e?s)?\\b', 'gi'), '_____');
      });
    return out;
  }

  function readVocab(dl) {
    var items = [];
    dl.querySelectorAll('dt').forEach(function (dt) {
      var defs = [];
      var dd = dt.nextElementSibling;
      while (dd && dd.tagName === 'DD') {
        defs.push(dd.textContent);
        dd = dd.nextElementSibling;
      }
      var term = clean(dt.textContent);
      var definition = clean(defs.join(' '));
      if (term && definition) items.push({ term: term, definition: maskTerm(definition, term) });
    });
    return items;
  }

  // ---------- QTI 2.1 ----------
  var QTI_NS = 'xmlns="http://www.imsglobal.org/xsd/imsqti_v2p1" ' +
    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' +
    'xsi:schemaLocation="http://www.imsglobal.org/xsd/imsqti_v2p1 ' +
    'http://www.imsglobal.org/xsd/qti/qtiv2p1/imsqti_v2p1.xsd"';
  var LETTERS = ['A', 'B', 'C', 'D'];

  function buildQuestions(vocab) {
    return shuffle(vocab).map(function (entry, n) {
      var others = shuffle(vocab.filter(function (v) { return v !== entry; })).slice(0, 3);
      var askForDefinition = Math.random() < 0.5;
      var options = shuffle([entry].concat(others));
      return {
        id: 'item' + (n + 1),
        title: 'Question ' + (n + 1) + ': ' + entry.term,
        prompt: askForDefinition
          ? 'Which definition best matches the term <strong>' + xml(entry.term) + '</strong>?'
          : 'Which term matches this definition?<br/><em>' + xml(entry.definition) + '</em>',
        choices: options.map(function (o) { return askForDefinition ? o.definition : o.term; }),
        correct: LETTERS[options.indexOf(entry)]
      };
    });
  }

  function itemXml(q) {
    var choices = q.choices.map(function (c, i) {
      return '      <simpleChoice identifier="' + LETTERS[i] + '">' + xml(c) + '</simpleChoice>';
    }).join('\n');
    return '<?xml version="1.0" encoding="UTF-8"?>\n' +
      '<assessmentItem ' + QTI_NS + ' identifier="' + q.id + '" title="' + xml(q.title) + '" ' +
      'adaptive="false" timeDependent="false">\n' +
      '  <responseDeclaration identifier="RESPONSE" cardinality="single" baseType="identifier">\n' +
      '    <correctResponse><value>' + q.correct + '</value></correctResponse>\n' +
      '  </responseDeclaration>\n' +
      '  <outcomeDeclaration identifier="SCORE" cardinality="single" baseType="float">\n' +
      '    <defaultValue><value>0</value></defaultValue>\n' +
      '  </outcomeDeclaration>\n' +
      '  <itemBody>\n' +
      '    <choiceInteraction responseIdentifier="RESPONSE" shuffle="false" maxChoices="1">\n' +
      '      <prompt>' + q.prompt + '</prompt>\n' +
      choices + '\n' +
      '    </choiceInteraction>\n' +
      '  </itemBody>\n' +
      '  <responseProcessing template="http://www.imsglobal.org/question/qti_v2p1/rptemplates/match_correct"/>\n' +
      '</assessmentItem>\n';
  }

  function testXml(title, questions) {
    var refs = questions.map(function (q) {
      return '      <assessmentItemRef identifier="' + q.id + '" href="' + q.id + '.xml"/>';
    }).join('\n');
    return '<?xml version="1.0" encoding="UTF-8"?>\n' +
      '<assessmentTest ' + QTI_NS + ' identifier="vocab_quiz" title="' + xml(title) + '">\n' +
      '  <testPart identifier="part1" navigationMode="nonlinear" submissionMode="simultaneous">\n' +
      '    <assessmentSection identifier="section1" title="' + xml(title) + '" visible="true">\n' +
      refs + '\n' +
      '    </assessmentSection>\n' +
      '  </testPart>\n' +
      '</assessmentTest>\n';
  }

  function manifestXml(title, questions) {
    var deps = questions.map(function (q) {
      return '      <dependency identifierref="' + q.id + '"/>';
    }).join('\n');
    var items = questions.map(function (q) {
      return '    <resource identifier="' + q.id + '" type="imsqti_item_xmlv2p1" href="' + q.id + '.xml">\n' +
        '      <file href="' + q.id + '.xml"/>\n' +
        '    </resource>';
    }).join('\n');
    return '<?xml version="1.0" encoding="UTF-8"?>\n' +
      '<manifest xmlns="http://www.imsglobal.org/xsd/imscp_v1p1" ' +
      'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' +
      'xsi:schemaLocation="http://www.imsglobal.org/xsd/imscp_v1p1 http://www.imsglobal.org/xsd/imscp_v1p1.xsd" ' +
      'identifier="MANIFEST-' + title.replace(/[^A-Za-z0-9]+/g, '-').replace(/-$/, '') + '">\n' +
      '  <metadata>\n' +
      '    <schema>QTIv2.1 Package</schema>\n' +
      '    <schemaversion>1.0.0</schemaversion>\n' +
      '  </metadata>\n' +
      '  <organizations/>\n' +
      '  <resources>\n' +
      '    <resource identifier="vocab_quiz" type="imsqti_test_xmlv2p1" href="assessment.xml">\n' +
      '      <file href="assessment.xml"/>\n' +
      deps + '\n' +
      '    </resource>\n' +
      items + '\n' +
      '  </resources>\n' +
      '</manifest>\n';
  }

  // ---------- minimal ZIP writer (stored, no compression) ----------
  var CRC_TABLE = (function () {
    var t = [];
    for (var n = 0; n < 256; n++) {
      var c = n;
      for (var k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1;
      t[n] = c >>> 0;
    }
    return t;
  })();

  function crc32(bytes) {
    var c = 0xFFFFFFFF;
    for (var i = 0; i < bytes.length; i++) c = CRC_TABLE[(c ^ bytes[i]) & 0xFF] ^ (c >>> 8);
    return (c ^ 0xFFFFFFFF) >>> 0;
  }

  function zip(files) {
    var enc = new TextEncoder();
    var parts = [];
    var central = [];
    var offset = 0;
    files.forEach(function (f) {
      var name = enc.encode(f.name);
      var data = enc.encode(f.content);
      var crc = crc32(data);
      var local = new DataView(new ArrayBuffer(30));
      local.setUint32(0, 0x04034b50, true);
      local.setUint16(4, 20, true);
      local.setUint16(6, 0x0800, true);   // UTF-8 names
      local.setUint16(8, 0, true);        // stored
      local.setUint32(14, crc, true);
      local.setUint32(18, data.length, true);
      local.setUint32(22, data.length, true);
      local.setUint16(26, name.length, true);
      parts.push(local.buffer, name, data);

      var cd = new DataView(new ArrayBuffer(46));
      cd.setUint32(0, 0x02014b50, true);
      cd.setUint16(4, 20, true);
      cd.setUint16(6, 20, true);
      cd.setUint16(8, 0x0800, true);
      cd.setUint16(10, 0, true);
      cd.setUint32(16, crc, true);
      cd.setUint32(20, data.length, true);
      cd.setUint32(24, data.length, true);
      cd.setUint16(28, name.length, true);
      cd.setUint32(42, offset, true);
      central.push(cd.buffer, name);
      offset += 30 + name.length + data.length;
    });
    var cdSize = central.reduce(function (s, p) { return s + p.byteLength; }, 0);
    var end = new DataView(new ArrayBuffer(22));
    end.setUint32(0, 0x06054b50, true);
    end.setUint16(8, files.length, true);
    end.setUint16(10, files.length, true);
    end.setUint32(12, cdSize, true);
    end.setUint32(16, offset, true);
    return new Blob(parts.concat(central, [end.buffer]), { type: 'application/zip' });
  }

  // ---------- page wiring ----------
  function findVocabList(marker) {
    var el = marker.previousElementSibling;
    while (el && !(el.tagName === 'DL' && el.classList.contains('vocab'))) el = el.previousElementSibling;
    return el;
  }

  function download(marker, dl) {
    var vocab = readVocab(dl);
    var course = marker.getAttribute('data-course');
    var unit = marker.getAttribute('data-unit');
    var version = versionCode();
    var title = course + ' Unit ' + unit + ' Vocabulary Quiz (Version ' + version + ')';
    var questions = buildQuestions(vocab);
    var files = [
      { name: 'imsmanifest.xml', content: manifestXml(title, questions) },
      { name: 'assessment.xml', content: testXml(title, questions) }
    ].concat(questions.map(function (q) { return { name: q.id + '.xml', content: itemXml(q) }; }));

    var url = URL.createObjectURL(zip(files));
    var a = document.createElement('a');
    a.href = url;
    a.download = (course + '-unit-' + unit + '-vocab-quiz-' + version).toLowerCase() + '-qti.zip';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  function init() {
    document.querySelectorAll('.vocab-quiz').forEach(function (marker) {
      var dl = findVocabList(marker);
      if (!dl || dl.querySelectorAll('dt').length < 2) return;
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'vocab-csv-btn vocab-quiz-btn';
      btn.textContent = '⬇ Download Schoology Vocab Quiz (QTI)';
      btn.addEventListener('click', function () { download(marker, dl); });
      var note = document.createElement('p');
      note.className = 'vocab-quiz-note';
      note.textContent = 'Teacher tool: one auto-graded multiple-choice question per term, ' +
        'randomized on every click. Import the .zip into Schoology as a QTI 2.1 package.';
      marker.appendChild(btn);
      marker.appendChild(note);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
