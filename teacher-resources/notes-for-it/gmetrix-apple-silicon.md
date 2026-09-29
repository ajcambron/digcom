---
title: Installing GMetrix on Apple Silicon Macs
parent: Notes for IT
grandparent: Teacher Resources
nav_order: 2
---

# Installing GMetrix on Apple Silicon Macs
{: .no_toc }

GMetrix's Adobe-integrated practice exams run through a plugin panel inside the Adobe app itself
(internally named "LITA," visible in the plugin folder names `gmetrix.lita.adobe.illustrator`,
`gmetrix.lita.adobe.photoshop`, and so on). That plugin is built on Adobe's older CEP extension
framework, which was never rebuilt for Apple Silicon — so on an M-series Mac, both GMetrix's own
app and the Adobe application it's plugging into have to run under Rosetta for the plugin to load
at all.
{: .fs-5 .fw-300 }

<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

---

## Which Adobe version to install — confirm before deploying

{: .warning }
> **Don't assume "2025" course content means Adobe's current 2025 release is safe to install.**
> Adobe removed CEP extension support from Photoshop starting with the 2025 release line
> (v26+) — the exact framework GMetrix's LITA plugin depends on. Multiple independent reports
> (Adobe's own community forums, a Jamf Nation admin thread) describe GMetrix's Photoshop plugin
> failing to load on current Photoshop 2025 builds for this reason, not as an Apple-Silicon-only
> issue. The same risk plausibly applies to Illustrator and Premiere Pro as Adobe rolls the same
> CEP-removal forward across the suite, though this page can't confirm that from what's public.

This page could **not** pull GMetrix's live, authoritative "Adobe Creative Cloud Version
Compatibility" table directly — that page is out of this session's network reach — so don't treat
any specific point-release number as confirmed here. Before you image or update lab machines for
a testing window:

1. Check GMetrix's own compatibility pages directly:
   - [Adobe Version Compatibility](https://support.gmetrix.net/support/solutions/articles/67000697496-adobe-creative-cloud-version-compatibility)
   - [SMS Compatibility: Adobe Creative Cloud](https://support.gmetrix.net/support/solutions/articles/67000746490-sms-compatibility-adobe-creative-cloud)
2. If either page doesn't clearly list a supported version for this year's Illustrator,
   Photoshop, or Premiere Pro course, open a ticket with GMetrix support (linked from those
   pages) and ask directly which exact version their current "2025" BrainBuffet content is
   tested against, before touching the lab image.
3. Once you have a confirmed version, install *that* specific version through the Adobe Admin
   Console (Creative Cloud for enterprise/education lets you pin a version per package) rather
   than letting Creative Cloud auto-update to whatever's newest — an unplanned update mid-unit is
   exactly how this breaks.

## Step 1: Install GMetrix SMSe on macOS

1. On the Mac, go to [gmetrix.net/GetGMetrixSMS.aspx](https://www.gmetrix.net/GetGMetrixSMS.aspx)
   and select **Download SMSe**.
2. Open `GmetrixSMSe.dmg` from the Downloads folder.
3. Drag the **GmetrixSMSe** icon onto the **Applications** folder shortcut in the same window.
4. Open the **Applications** folder and double-click **GmetrixSMSe** to launch it. macOS may
   prompt for the local admin password on first launch.

{: .note }
> General macOS system requirements for GMetrix (per GMetrix's own docs): macOS 10.10 or newer,
> a 64-bit machine with hardware-accelerated graphics for simulation-based exams, and a
> high-speed internet connection. None of that is Apple-Silicon-specific — the Rosetta
> requirement below is specifically about the Adobe plugin panel, not GMetrix SMSe itself.

## Step 2: Make an Adobe app work with GMetrix on Apple Silicon

Do this for **every** Adobe application this lab runs GMetrix practice exams through — it's a
per-application setting, not a one-time system setting.

1. Open the **Applications** folder in Finder and locate the Adobe app (for example,
   `/Applications/Adobe Photoshop 2025`).
2. Right-click the application and select **Get Info**.
3. Check the box labeled **Open using Rosetta**.
4. Close the Get Info window, then open the Adobe application itself.
5. Inside the Adobe app, go to **Preferences → Plugins → Legacy Extensions** and enable **both**
   options listed there (GMetrix's own article doesn't name them individually beyond "both
   options" — check the same panel on a test Mac to confirm current wording, since Adobe has
   changed this dialog's exact labels across releases).
6. Quit and relaunch the Adobe application.
7. Launch a practice exam through GMetrix SMS to confirm the plugin panel loads.

{: .important }
> If the plugin still doesn't appear after this, check folder permissions at
> `Macintosh HD → Library → Application Support → Adobe → CEP` — macOS can silently block the
> read/write access GMetrix needs to load new question content mid-test.

## Troubleshooting

| Symptom | Likely cause / fix |
|:--------|:--------------------|
| Plugin panel never appears in the Adobe app | Confirm **Open using Rosetta** is checked on the Adobe app itself, not just GMetrix SMSe — this is the single most common miss. |
| "The GMetrix LITA extension could not be loaded because it was not properly signed" | A known signing/registry issue on Windows; on Mac, try removing and letting GMetrix SMS reinstall the plugin folder (`~/Library/Application Support/Adobe/CEP/extensions/gmetrix.lita.adobe.<app>`) rather than editing it by hand. |
| GMetrix SMS says it can't locate the Adobe application | In GMetrix SMS, open the settings/options wheel, select the affected application, scroll to **Change Filepath**, and point it at the app's actual install path. |
| Premiere Pro: test seems to hang right at start | Some sample project files need to convert on first open — this doesn't count against the test timer, let it finish. |
| After Effects opens the **Render Engine** instead of the full app | Uninstall the After Effects Render Engine component and reopen After Effects normally. |

## Sources

- [How-to Install Adobe Applications (GMetrix)](https://support.gmetrix.net/support/solutions/articles/67000722066-how-to-install-adobe-applications)
- [Issue Loading Photoshop Plugins With Apple Silicon Computers (GMetrix)](https://support.gmetrix.net/support/solutions/articles/67000700785-issue-loading-photoshop-plugins-with-apple-silicon-computers-m1-m2-etc-)
- [If Your SMS Cannot Locate Your Adobe Application (GMetrix)](https://support.gmetrix.net/support/solutions/articles/67000682317-if-your-sms-cannot-locate-your-adobe-application)
- [Adobe LITA Extension Cannot Load (GMetrix)](https://support.gmetrix.net/support/solutions/articles/67000663900-adobe-lita-extension-cannot-load)
- [How to Install GMetrixSMSe on macOS (GMetrix)](https://support.gmetrix.net/support/solutions/articles/67000663190-how-to-install-gmetrixsmse-on-macos)
- [Adobe Version Compatibility (GMetrix)](https://support.gmetrix.net/support/solutions/articles/67000697496-adobe-creative-cloud-version-compatibility)
- [SMS Compatibility: Adobe Creative Cloud (GMetrix)](https://support.gmetrix.net/support/solutions/articles/67000746490-sms-compatibility-adobe-creative-cloud)
- [Gmetrix Adobe Plugins Capture (Solved) — Jamf Nation Community](https://community.jamf.com/t5/jamf-pro/gmetrix-adobe-plugins-capture-solved/td-p/257216)

{: .note }
> This session couldn't reach support.gmetrix.net directly to quote these articles verbatim
> (network restriction), so the steps above are reconstructed from search-indexed summaries of
> GMetrix's own published articles, cross-checked against an independent Jamf Nation admin
> thread describing the same fix in practice. Re-verify against the live pages, especially the
> version-compatibility question above, before relying on this for a real deployment.
