// Loads a live lesson page from this site into a Schoology "Page" material, without an
// <iframe>. Schoology's Page editor allows a <script src="..."> pointed at this file plus a
// placeholder <div data-digcom-embed="https://digcom.cambron.cc/..."> — see
// _planning/schoology-embed.md for the exact snippet. Because this file is fetched fresh on
// every page view (and itself fetches the lesson page fresh), edits pushed to this site show
// up in Schoology on the next load with no re-pasting required.
//
// Uses a shadow root so the lesson's own stylesheet can't leak into Schoology's chrome (or the
// other way around) the way it would with a plain innerHTML injection.
(function () {
  'use strict';

  function absolutize(html, baseUrl) {
    var doc = new DOMParser().parseFromString(html, 'text/html');
    doc.querySelectorAll('[href], [src]').forEach(function (node) {
      ['href', 'src'].forEach(function (attr) {
        var val = node.getAttribute(attr);
        if (val) {
          try {
            node.setAttribute(attr, new URL(val, baseUrl).href);
          } catch (e) {
            // leave malformed URLs (e.g. "javascript:") untouched
          }
        }
      });
    });
    return doc;
  }

  function render(container, src) {
    var shadow = container.shadowRoot || container.attachShadow({ mode: 'open' });
    shadow.innerHTML = '<p class="digcom-embed-status">Loading lesson…</p>';

    var cacheBustedUrl = src + (src.indexOf('?') === -1 ? '?' : '&') + 'embed=' + Date.now();

    fetch(cacheBustedUrl, { cache: 'no-store', mode: 'cors' })
      .then(function (res) {
        if (!res.ok) {
          throw new Error('the page responded with HTTP ' + res.status);
        }
        return res.text();
      })
      .then(function (html) {
        var doc = absolutize(html, src);
        var main = doc.querySelector('main');
        if (!main) {
          throw new Error('could not find lesson content in the fetched page');
        }

        var styleLinks = '';
        doc.querySelectorAll('link[rel="stylesheet"]').forEach(function (link) {
          styleLinks += '<link rel="stylesheet" href="' + link.getAttribute('href') + '">';
        });

        shadow.innerHTML =
          styleLinks +
          '<style>:host{display:block;} .digcom-embed-wrap{max-width:800px;margin:0 auto;padding:1rem 0;}</style>' +
          '<div class="digcom-embed-wrap main-content">' + main.innerHTML + '</div>';
      })
      .catch(function (err) {
        shadow.innerHTML =
          '<p class="digcom-embed-status digcom-embed-error">' +
          "This lesson couldn't be loaded here (" + err.message + '). ' +
          '<a href="' + src + '" target="_blank" rel="noopener">Open it in a new tab →</a></p>';
      });
  }

  function init() {
    document.querySelectorAll('[data-digcom-embed]').forEach(function (container) {
      var src = container.getAttribute('data-digcom-embed');
      if (src) render(container, src);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
