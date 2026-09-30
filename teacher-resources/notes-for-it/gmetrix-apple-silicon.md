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

## Which Adobe version to install

GMetrix publishes an exact supported-version range per application per exam year, on the same
[SMS Compatibility: Adobe Creative Cloud](https://support.gmetrix.net/support/solutions/articles/67000746490-sms-compatibility-adobe-creative-cloud)
page. For the **2025 Exam Version** column — the one that matches this district's FDD
(Illustrator), ADD (Premiere Pro), and PDD (Photoshop) courses — as of this table's last check:

| App | 2025 Exam Version |
|:----|:-------------------|
| **Illustrator** (FDD) | 29.0–29.8.1 |
| **Premiere Pro** (ADD) | 25.1–25.5 |
| **Photoshop** (PDD) | 26.0–26.11 |
| InDesign | 20.0–20.5 |
| After Effects | 25.0–25.5 |
| Animate | *not listed for 2025 at last check* |
| Dreamweaver | N/A (no longer covered) |

{: .important }
> Install a version **inside** the listed range, not just "whatever's current" — Creative Cloud's
> auto-update can walk an app past the top of that range without anyone noticing until a test
> won't launch. Pin the exact version by packaging it through the Adobe Admin Console (see
> [Step 1](#step-1-build-the-adobe-package-in-the-admin-console)) rather than leaving apps on
> auto-update, and re-check the live compatibility page before each testing window — GMetrix
> revises these ranges as new Adobe point releases ship and gets re-tested, so a range that's
> correct today can narrow later in the year.

{: .note }
> Adobe removed CEP extension support from Photoshop starting with the 2025 release line
> (v26+) — the framework GMetrix's LITA plugin depends on — which is why 2025 Photoshop had real
> reported compatibility problems for a stretch (see the Sources below). GMetrix's own table
> confirms 26.0–26.11 is supported now, so this isn't a live blocker if you're inside that range,
> but it's the reason the range has an upper bound instead of just "latest" — don't manually
> update past 26.11 assuming a newer Photoshop will keep working.

## Step 1: Build the Adobe package in the Admin Console

Install the lab's Adobe apps from a managed package built at
[adminconsole.adobe.com](https://adminconsole.adobe.com/) (**Packages → Create a package**)
instead of letting each Mac install whatever Creative Cloud currently offers. A package is how you
pick a version inside GMetrix's supported range (the table above) and put that same version on
every lab Mac through Jamf.

1. **Licensing method: Shared device licensing.** This is the lab option. Apps are licensed to
   the machine through the district's K-12 shared device license, and students sign in with their
   own school identity when they open an app. Named user licensing is for a single person's own
   machine, like a teacher laptop.

   ![Admin Console licensing method choice, with Shared device licensing selected]({{ '/assets/images/notes-for-it/adobe-package-1-licensing.png' | relative_url }})

2. **Entitlements:** check **Creative Cloud All Apps for K-12 - Shared Device**.

   ![Entitlements step, with Creative Cloud All Apps for K-12 - Shared Device selected]({{ '/assets/images/notes-for-it/adobe-package-2-entitlements.webp' | relative_url }})

3. **Configure:** set the platform to **macOS (Intel)** and leave **Use OS Locale** on (it falls
   back to English (North America)).

   ![Configure step, with platform set to macOS (Intel) and Use OS Locale turned on]({{ '/assets/images/notes-for-it/adobe-package-3-configure.webp' | relative_url }})

   The Intel builds matter on Apple Silicon Macs: an Intel-only app always runs under Rosetta,
   which is exactly what GMetrix's plugin panel needs. Apps from this package won't show the
   **Open using Rosetta** checkbox in [Step 3](#step-3-make-an-adobe-app-work-with-gmetrix-on-apple-silicon)
   at all, because macOS only offers that checkbox for apps that also have an Apple Silicon build.

4. **Choose apps:** click **Other versions**, keep **Latest versions** checked, and check **Older
   versions** (leave long-term supported, beta, and pre-release unchecked). Without Older versions
   the list only offers each app's newest release, which may be past the top of GMetrix's
   supported range. Then add the specific version of each app this lab needs from the table above
   (Illustrator 29.x for FDD, Premiere Pro 25.x for ADD, Photoshop 26.x for PDD). The **License
   File** is added to the package automatically.

   ![Choose apps step, with the Other versions menu open and Latest versions and Older versions checked]({{ '/assets/images/notes-for-it/adobe-package-4-choose-apps.webp' | relative_url }})

5. **Choose plugins, Options, Finalize:** GMetrix's plugin panel isn't added here; GMetrix SMS
   installs it into each Adobe app itself. Finish the remaining steps, name the package, and let
   Adobe build it. When it's ready, download it from the Packages list and deploy it through Jamf
   like the lab's other packages.

## Step 2: Install GMetrix SMSe on macOS

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

## Step 3: Make an Adobe app work with GMetrix on Apple Silicon

Do this for **every** Adobe application this lab runs GMetrix practice exams through — it's a
per-application setting, not a one-time system setting.

1. Open the **Applications** folder in Finder and locate the Adobe app (for example,
   `/Applications/Adobe Photoshop 2025`).
2. Right-click the application and select **Get Info**.
3. Check the box labeled **Open using Rosetta**. If there's no such checkbox, the app is an
   Intel-only build (the macOS (Intel) package from Step 1) and already runs under Rosetta, so
   skip to the next step.
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
| Plugin panel never appears in the Adobe app | Confirm the Adobe app is running under Rosetta: either it came from the macOS (Intel) package in Step 1, or **Open using Rosetta** is checked on the app itself (not just GMetrix SMSe). This is the single most common miss. |
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
> (network restriction). The version-compatibility table above is the real thing, pasted in
> directly from that page, and the Admin Console packaging steps come from screenshots of this
> district's own console. Everything else on this page (the GMetrix installation and
> Rosetta/Legacy Extensions steps) is reconstructed from search-indexed summaries of GMetrix's own published
> articles, cross-checked against an independent Jamf Nation admin thread describing the same fix
> in practice. Re-verify the procedural steps against the live pages before relying on this for a
> real deployment.
