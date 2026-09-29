---
title: Making a 36"x24" Poster in Canva
parent: Classroom Tool Guides
grandparent: Teacher Resources
nav_order: 1
---

# Making a 36"x24" Poster in Canva
{: .no_toc }

At this school, students reach Canva through the ClassLink Launchpad and sign in with their school
Google account — they never see a Canva password screen. This walks through that login, setting the
canvas to an exact 36"x24" print size (Canva defaults to pixels, not inches), and exporting a
print-ready PDF in CMYK so colors don't shift when it comes off a real printer.
{: .fs-5 .fw-300 }

<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

---

## How students sign in

1. Student opens the ClassLink Launchpad and clicks the **Canva** tile.
2. ClassLink hands the student to Canva already flagged as an SSO login for the district. Canva
   detects this and prompts to continue through the district's identity provider — for a Google
   Workspace district, that's a **Continue with Google** step, landing on the normal Google
   account picker.
3. Student picks their school Google account. Canva creates (first time) or logs into their
   **Canva for Education** account tied to that Google identity.

{: .note }
> The exact click sequence between the ClassLink tile and the Google picker depends on how IT
> configured Canva's SSO app inside ClassLink's Launchpad — confirm it with one real test login
> before relying on this with a full class. If a student ever lands in a personal/free Canva
> account instead (most often because they signed in with a personal Gmail address before SSO was
> set up, or clicked "Sign up" instead of the SSO tile), they won't have the CMYK export option in
> [Export print-ready with CMYK colors](#export-print-ready-with-cmyk-colors) below — Canva for
> Education is what unlocks that.

## Set the canvas to 36"x24"

1. From the Canva home screen, click **Create a design** (top right).
2. Choose **Custom size** from the list of options.
3. In the size dialog, click the unit dropdown and change it from **px** to **in** — this is the
   step that's easy to miss, since Canva opens that dialog in pixels by default.
4. Enter **36** for width and **24** for height (swap them for a portrait-orientation poster).
5. Click **Create new design**.

{: .note }
> Canva's maximum canvas size is roughly 52"x52", so a 36"x24" poster is comfortably inside the
> limit — no workaround needed.

## Export print-ready with CMYK colors

Everything on screen in Canva is RGB (the color model screens use). Printers use CMYK, a smaller
color range — export in CMYK so what prints matches what was designed, instead of Canva or the
print shop guessing at the conversion later.

1. Click **Share** (top right of the editor).
2. Click **Download**.
3. Under **File type**, choose **PDF Print** (not the plain "PDF Standard" option — that one stays
   in RGB).
4. Find the **Color profile** setting on that same download panel and switch it from **RGB** to
   **CMYK**.
5. If the print shop or classroom printer wants bleed (artwork that runs past the trim edge) or
   crop marks, check those boxes here too — otherwise leave them off.
6. Click **Download**.

{: .important }
> If the CMYK option isn't there — only RGB shows on the color profile setting — the signed-in
> account isn't being recognized as Canva for Education. Have the student sign out and back in
> through the **ClassLink tile specifically**, not a bookmarked canva.com login page.

{: .note }
> Colors can shift a little going from RGB to CMYK, especially very saturated blues, greens, and
> neons — CMYK simply can't reproduce those as brightly as a screen can. That's expected color
> science, not a broken export; have students glance at the downloaded PDF before sending it to
> print and nudge any oversaturated color if it looks off.

## Troubleshooting

| Symptom | Likely cause / fix |
|:--------|:--------------------|
| Student never reaches Canva, stuck in a Google login loop | Usually a personal Gmail was entered instead of the school account — redirect them back through the ClassLink tile and have them pick the school account explicitly. |
| Canvas shows an odd size like 3456 x 2304 instead of 36x24 | The unit dropdown was left on **px** when the dimensions were typed in — inches must be selected *before* entering the numbers, not after. |
| CMYK isn't offered on download | Account isn't recognized as Canva for Education (see the callout above) — sign out and back in via ClassLink. |
| Poster looks sharp on screen but blurry once printed | A raster image (photo, downloaded graphic) was scaled up well past its native resolution to fill the 36"x24" canvas — swap in a higher-resolution source image rather than stretching a small one. |

## Sources

- [A guide to design sizes — Canva Design Wiki](https://www.canva.com/sizes/)
- [Poster Sizes — Canva Design Wiki](https://www.canva.com/sizes/poster/)
- [Design with print colors (CMYK) — Canva Help Center](https://www.canva.com/help/cmyk-for-print/)
- [Log in using Single Sign-On (SSO) — Canva Help Center](https://www.canva.com/help/log-in-sso/)
- [ClassLink SAML configuration — Canva Help Center](https://www.canva.com/help/saml-configuration-classlink/)

{: .note }
> This session couldn't reach canva.com directly to quote these pages verbatim (network
> restriction). The steps above are reconstructed from search-indexed summaries of Canva's own
> published help articles rather than a live screenshot walkthrough — the underlying mechanics
> (custom size in inches, PDF Print + CMYK on the download panel, SSO through a school's identity
> provider) are well-documented and consistent across sources, but exact button placement can
> shift as Canva updates its UI. Do one live test login and export before relying on this with a
> full class, and update this page if something no longer matches what's on screen.
