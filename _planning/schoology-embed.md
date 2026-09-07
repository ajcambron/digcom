## Embedding lesson pages in Schoology without an iframe

`assets/js/schoology-embed.js` fetches a live lesson page from this site and injects it into a
Schoology "Page" material, instead of framing it. Two things an `<iframe>` can't reliably give you
that this does:

- It re-fetches the lesson page on every view, so edits pushed to this site show up in Schoology
  immediately — nothing to re-paste.
- It renders into a shadow root, so the lesson's own stylesheet can't leak into Schoology's page
  chrome (or the other way around) — no frame needed for that isolation.

### Schoology-side snippet

In the Page material's editor, switch to the HTML/source view and paste (swap in the lesson's
real URL):

```html
<div data-digcom-embed="https://digcom.cambron.cc/foundations/fdd1/1_1.html"></div>
<script src="https://digcom.cambron.cc/assets/js/schoology-embed.js"></script>
```

That's it — the script does the fetch, pulls the page's own stylesheet links, rewrites relative
links/images to absolute URLs, and drops the lesson's `<main>` content into the shadow root. If the
fetch fails (site down, network blip), the placeholder shows a link to open the lesson directly
instead of a blank/broken frame.

### Verified locally

Tested by building the site (`bundle exec jekyll build`), serving it on one local origin with
`Access-Control-Allow-Origin: *`, and loading a mock "Schoology" page on a second origin — with
deliberately hostile page-wide CSS (`h1 { color: red !important }`) — that pastes in the snippet
above pointed at `foundations/fdd1/1_1.html`. Confirmed: the fetched lesson (title, vocab list,
worksheet links rewritten to absolute URLs, callout boxes) renders with its own styling untouched
by the host page's CSS.

### Caveats to check before relying on this

- **Requires the Schoology instance to allow `<script>` in Page HTML.** Some district admins strip
  script tags from Page content for XSS reasons — the same policy that often makes iframes flaky in
  the first place. Test with one real Page before rolling this out everywhere.
- **Requires CORS on the hosting side.** This assumes GitHub Pages continues serving
  `Access-Control-Allow-Origin: *` on `digcom.cambron.cc` (it does by default at the time of
  writing) — confirm with browser devtools if content stops loading after a Pages config change.
- **Schoology's mobile app** renders Page content in its own native view and may not execute
  injected `<script>` tags the way a desktop/mobile browser does. Verify on the app before
  depending on it for mobile-heavy classes.
- Content only refreshes when the Schoology page is (re)loaded — it isn't push-updated while a
  student has the tab open.
