---
title: Custom macOS Dock for the Lab Image
parent: Notes for IT
grandparent: Teacher Resources
nav_order: 1
---

# Custom macOS Dock for the Lab Image
{: .no_toc }

Pin Chrome, Google Drive, and the Adobe apps this course needs into every student's Dock the
first time they log in, using [bluemoosegoose/Build-a-Custom-MacOS-Dock](https://github.com/bluemoosegoose/Build-a-Custom-MacOS-Dock),
a small script-based tool deployed through Jamf Pro.
{: .fs-5 .fw-300 }

<details open markdown="block">
  <summary>On this page</summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

---

{: .note }
> This tool is a third-party GitHub project, not something Apple, Google, Adobe, or Jamf ships or
> supports. It's a plain shell script plus a LaunchAgent, verified by its author on macOS Sonoma
> and back-compatible to Catalina. Read it before you deploy it — it's short.

## How it works

Three packages, all pushed through Jamf Pro (the same MDM already used to deploy the
BrainBuffet Premiere assets — see the GMetrix accountability notes in
`_planning/2026-27-scope-and-sequence.md` — so no new deployment channel to set up):

| Package | What it does |
|:--------|:--------------|
| `dockutil` binary | A command-line tool (from its own GitHub releases, separate from this repo) that adds, removes, and reorders Dock items. Installs to `/usr/local/bin/dockutil`. |
| `BuildtheDockScript.pkg` | Installs `BuildtheDock.sh` to `/Library/Scripts/`. This is the one file you actually edit. |
| `buildadockagent.pkg` | Installs a LaunchAgent (`/Library/LaunchAgents/com.matt.buildadock.plist`) that runs the script at every login. |

**The dock builds once per user, then leaves it alone.** The script's first real action is to
check for a marker file, `~/dockscrap.txt`. If that file exists, the script exits immediately and
touches nothing — so a student who's rearranged their own Dock never gets it silently reset on a
later login. If the marker is missing, the script wipes the Dock (`dockutil --remove all`) and
rebuilds it from a fixed list of items, then creates the marker so it won't run again.

That means: to push an *updated* default (say, a new Adobe app this year), you have to delete
`dockscrap.txt` and re-trigger the LaunchAgent — see [Re-running after an update](#re-running-after-an-update)
below — not just edit the script and wait.

## Step 1: Edit `BuildtheDock.sh`

The stock script (from the repo's `BuildtheDock.sh`) builds the Dock like this, one `dockutil`
call per item, in the order they should appear:

```bash
#Clear the Dock
echo Removing all Dock Items
$DOCKUTIL_BINARY --remove all --no-restart

#sleep for 2 seconds
$sleep 2

#Build the Dock
$DOCKUTIL_BINARY --add '/System/Applications/Launchpad.app' --allhomes --no-restart
$DOCKUTIL_BINARY --add '/System/Applications/System Settings.app' --allhomes --no-restart
$DOCKUTIL_BINARY --add '/Applications/Self Service.app' --allhomes --no-restart
$DOCKUTIL_BINARY --add '/System/Cryptexes/App/System/Applications/Safari.app' --allhomes --no-restart
$DOCKUTIL_BINARY --add '/Applications/Firefox.app' --allhomes --no-restart
$DOCKUTIL_BINARY --add '/Applications/Google Chrome.app' --allhomes --no-restart
$DOCKUTIL_BINARY --add '/Library/Application Support/Dock Icons/Office 365.webloc' --label 'Office 365' --no-restart
$DOCKUTIL_BINARY --add '~/Downloads' --view fan --display stack
echo Added Downloads-Fan View-Stack Display
```

**Chrome is already in the stock list** (`/Applications/Google Chrome.app`) — nothing to add
there. Drop or keep `Self Service.app`, `Firefox.app`, and the `Office 365.webloc` line depending
on what's actually relevant to this lab; they're the original author's defaults, not required by
the tool itself.

To add **Google Drive** and **the Adobe apps**, insert one `--add` line per app, right after the
Chrome line and before the `~/Downloads` stack:

```bash
$DOCKUTIL_BINARY --add '/Applications/Google Chrome.app' --allhomes --no-restart
$DOCKUTIL_BINARY --add '/Applications/Google Drive.app' --allhomes --no-restart
$DOCKUTIL_BINARY --add '/Applications/Adobe Illustrator 2025/Adobe Illustrator.app' --allhomes --no-restart
$DOCKUTIL_BINARY --add '/Applications/Adobe Premiere Pro 2025/Adobe Premiere Pro 2025.app' --allhomes --no-restart
$DOCKUTIL_BINARY --add '/Applications/Adobe Photoshop 2025/Adobe Photoshop 2025.app' --allhomes --no-restart
$DOCKUTIL_BINARY --add '~/Downloads' --view fan --display stack
```

Only add a line for whichever Adobe app(s) this specific lab image actually has installed — a
Premiere-only Mac lab doesn't need the Illustrator or Photoshop lines, and vice versa. Items
appear in the Dock in the exact order you `--add` them, so put the app each course actually uses
first if you want it closest to the Applications side.

{: .important }
> **Confirm the exact path on a real test Mac before you trust it.** Adobe's folder name changes
> with the release line (`Adobe Illustrator 2025` this year, a different year next year), and the
> Google Drive client has been renamed by Google before. Don't guess from this page — on a Mac
> that already has the app installed, either right-click the app in **Applications → Get Info**
> and read the path, or drag the app icon onto an open Terminal window; Terminal prints its full
> path. Use that exact string.

## Step 2: Package and deploy through Jamf

1. Build/import the three packages (`dockutil`, `BuildtheDockScript.pkg` with your edited script
   inside, `buildadockagent.pkg`) as Jamf Pro packages, same as any other software deployment.
2. Scope them to the lab's Smart Group or the specific machines, same as the BrainBuffet asset
   packages already pushed to the ADD Mac lab.
3. If any app you're adding is itself a **web shortcut** rather than an installed application
   (the repo's example is an Office 365 `.webloc`), the process is: create the `.webloc` file on a
   test Mac (drag a URL from the browser's address bar to the desktop, or use **File → Save As
   Webloc** where the browser supports it), package it with Jamf Composer into
   `/Library/Application Support/Dock Icons/`, then reference that path with a `--label` flag,
   exactly like the Office 365 line above.

## Re-running after an update

Because the script only fires once per user (per the `dockscrap.txt` check), editing and
re-pushing `BuildtheDock.sh` alone does **nothing** for a Mac that's already built its Dock. The
repo ships two small helper scripts for this:

| Script | What it does |
|:-------|:--------------|
| `A_Delete Dockscrap.sh` | Deletes `~/dockscrap.txt` for whoever's currently logged in, clearing the "already built" marker. |
| `BuildtheDock_ReLoad LaunchAgent.sh` | Unloads and reloads the LaunchAgent, forcing `BuildtheDock.sh` to run again immediately. |

To push an updated default Dock (a new Adobe app, a dropped item) to Macs that already have one
built: run `A_Delete Dockscrap.sh` first, then `BuildtheDock_ReLoad LaunchAgent.sh`, both as a
Jamf policy (or `sudo` locally on one machine while testing). Running the reload script without
first deleting the marker just reloads the LaunchAgent — the script still sees `dockscrap.txt`
and exits without changing anything.

{: .warning }
> Deleting `dockscrap.txt` throws away that student's own Dock customizations along with the old
> default — the rebuild is a full wipe (`dockutil --remove all`), not a merge. Only push a
> re-build when you actually intend to reset the Dock, e.g. lab re-image day or the start of a
> new school year, not as a casual fix.

## Verifying an install

- `dockutil` present at `/usr/local/bin/dockutil`
- `BuildtheDock.sh` present at `/Library/Scripts/`
- LaunchAgent plist present at `/Library/LaunchAgents/com.matt.buildadock.plist`
- A log of the last build at `/Users/<username>/docklog.txt` — the script redirects all its own
  output there, so this is the first place to check if a Dock didn't build as expected.

## Source

[bluemoosegoose/Build-a-Custom-MacOS-Dock](https://github.com/bluemoosegoose/Build-a-Custom-MacOS-Dock)
on GitHub. Commands and file names on this page are taken directly from that repo's
`BuildtheDock.sh`, `A_Delete Dockscrap.sh`, and `BuildtheDock_ReLoad LaunchAgent.sh` as of
September 2026 — check the repo itself if something here stops matching what you see.
