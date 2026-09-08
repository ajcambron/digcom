## Embedding lesson pages in Schoology

**Reverted to a plain `<iframe>` (Sep 2026).** The earlier approach — a `<script>`-based
fetch-and-inject into a shadow root, avoiding an iframe entirely — worked when tested locally
(see git history for that writeup) but this Schoology instance rejects `<script>` tags pasted
into Page HTML, same as the caveat below flagged as the main risk. Since the script never runs,
there's nothing to fall back to but the iframe.

### Schoology-side snippet

Every page's footer has a **📋 Copy Schoology Embed Code** button that copies this for the exact
page you're on. In the Page material's editor, switch to the HTML/source view and paste it:

```html
<iframe src="https://digcom.cambron.cc/foundations/fdd1/1_1.html" style="width: 100%; height: 1000px; border: 1px solid #ccc; border-radius: 6px;" loading="lazy"></iframe>
```

It still re-fetches the live page on every load — edits pushed to this site show up in Schoology
the next time a student opens the page, nothing to re-paste. What it doesn't get from the old
approach: style isolation (the iframe's content uses its own stylesheet inside the frame
boundary, same as any iframe — this was never actually a problem specific to the injection
approach) and a custom failure state if the page is unreachable (an iframe just shows its own
browser error, not a "open it directly" link).

Adjust the `height` in the pasted snippet if a specific lesson runs much longer or shorter than
the 1000px default — it's plain HTML, safe to hand-edit per page.

### Caveats

- **If iframes are "unreliable" here for a reason other than script-blocking** (e.g. the
  Schoology instance's own CSP or an admin-configured domain allowlist for framed content), an
  iframe pointed at `digcom.cambron.cc` may still not render. Test with one real Page first.
- **Schoology's mobile app** has historically had rougher iframe support than its desktop/browser
  view — verify there too before depending on this for mobile-heavy classes.
- No fixed height is right for every lesson — long lessons will scroll inside the frame, short
  ones will leave empty space below. There's no reliable cross-origin auto-resize without the
  embedded page's own JS cooperating (postMessage), which runs into the same script-rejection
  problem this reverted away from.
