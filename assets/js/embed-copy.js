// Footer button (see _includes/footer_custom.html) that copies the two-line snippet a teacher
// pastes into a Schoology Page to embed the current page via assets/js/schoology-embed.js.
(function () {
  function init() {
    document.querySelectorAll('.embed-copy-btn').forEach(function (btn) {
      var source = btn.previousElementSibling;
      if (!source) return;
      var label = btn.textContent;

      btn.addEventListener('click', function () {
        function show(text) {
          btn.textContent = text;
          setTimeout(function () { btn.textContent = label; }, 2000);
        }
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(source.textContent).then(
            function () { show('✅ Copied!'); },
            function () { show('⚠ Copy failed — select the text manually'); }
          );
        } else {
          show('⚠ Copy failed — select the text manually');
        }
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
