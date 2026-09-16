/*
  Shared behavior for every self-hosted reveal.js deck (assets/presentations/*.html).
  Include after reveal.js:
    <script src="/assets/lib/revealjs/dist/reveal.js"></script>
    <script src="/assets/js/revealjs-deck-common.js"></script>
    <script>Reveal.initialize({...});</script>
  Auto-runs on load — no per-deck call needed. Currently: injects a fullscreen
  toggle button, since reveal.js's own controls don't include one and the site's
  embedded iframe is too small to present from directly.
*/
(function () {
  var EXPAND_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="8 3 3 3 3 8"></polyline><polyline points="16 3 21 3 21 8"></polyline><polyline points="3 16 3 21 8 21"></polyline><polyline points="21 16 21 21 16 21"></polyline></svg>';
  var COMPRESS_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 9 9 9 9 4"></polyline><polyline points="20 9 15 9 15 4"></polyline><polyline points="4 15 9 15 9 20"></polyline><polyline points="20 15 15 15 15 20"></polyline></svg>';

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  function isFullscreen() {
    return !!(document.fullscreenElement || document.webkitFullscreenElement);
  }

  function toggleFullscreen() {
    var el = document.documentElement;
    if (!isFullscreen()) {
      var request = el.requestFullscreen || el.webkitRequestFullscreen;
      if (request) request.call(el);
    } else {
      var exit = document.exitFullscreen || document.webkitExitFullscreen;
      if (exit) exit.call(document);
    }
  }

  ready(function () {
    if (!(document.documentElement.requestFullscreen || document.documentElement.webkitRequestFullscreen)) {
      return;
    }
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'deck-fullscreen-btn';
    btn.setAttribute('aria-label', 'Toggle fullscreen');
    btn.title = 'Fullscreen (F)';
    btn.innerHTML = EXPAND_ICON;
    document.body.appendChild(btn);

    function updateIcon() {
      var fs = isFullscreen();
      btn.innerHTML = fs ? COMPRESS_ICON : EXPAND_ICON;
      btn.title = fs ? 'Exit fullscreen (Esc)' : 'Fullscreen (F)';
    }

    btn.addEventListener('click', toggleFullscreen);
    document.addEventListener('fullscreenchange', updateIcon);
    document.addEventListener('webkitfullscreenchange', updateIcon);
    document.addEventListener('keydown', function (e) {
      if ((e.key === 'f' || e.key === 'F') && !e.ctrlKey && !e.metaKey && !e.altKey) {
        var tag = (e.target && e.target.tagName) || '';
        if (tag === 'INPUT' || tag === 'TEXTAREA') return;
        toggleFullscreen();
      }
    });
  });
})();
