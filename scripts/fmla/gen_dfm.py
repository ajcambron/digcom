#!/usr/bin/env python3
"""Generate the FMLA DFM section: DFM 200 Weeks 8–22, the self-directed leave extension in the syllabus.

Run from the repo root:  python3 scripts/fmla/gen_dfm.py
Re-running overwrites fmla-dfm/ and the DFM exit-ticket includes.

Source: "DFM 200 Course Syllabus – Scheduled", Extended Continuity Plan (Weeks 8–22). Every team writes and
preps a script for the All American High School Film Festival (AAHSFF), to shoot in DFM 300. Weeks release
Monday and are due Sunday 11:59 PM in Canvas. B-day class periods follow one routine, run by the sub.
"""
import json, os, textwrap

ROOT = os.getcwd()
FOLDER = "fmla-dfm"
TOP = "FMLA DFM"
q = lambda s: json.dumps(s, ensure_ascii=False)

def write(rel, text):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(text)

def folded(key, text, indent=2):
    pad = " " * indent
    lines = textwrap.wrap(text, 94 - indent, break_on_hyphens=False, break_long_words=False)
    return f"{pad}{key}: >\n" + "\n".join(f"{pad}  {l}" for l in lines)

SB = "https://www.studiobinder.com/blog/"
CATEGORIES = [("Drama (recommended default)", "20 min"), ("Comedy", "15 min"), ("Documentary", "15 min"),
              ("Horror / Sci-Fi / Fantasy", "10 min"), ("Animation", "10 min"), ("Experimental", "10 min"),
              ("Video Podcast", "10 min"), ("Storyblocks: Representation Through Storytelling", "15 min"),
              ("Broadcast Journalism: Feature Story", "5 min"), ("Sports Feature", "5 min"), ("Music Video", "5 min"),
              ("Micro Movie", "1 min")]

# week: title, dates, objectives, reading [(label, url or None)], reading focus, task title, task steps, logistics, deliverables
WEEKS = {
 8: dict(title="AAHSFF Target & Studying Previous Winners", dates="Oct 26 – Nov 1, 2026", due="Sun, Nov 1",
         obj="A1, B5, B6",
         reading=[("AAHSFF Rules & Categories", "https://www.hsfilmfest.com/rulesandcategories"),
                  ("AAHSFF past nominees and winners (on the festival site)", "https://www.hsfilmfest.com/")],
         focus="Find your category's runtime cap, the content rules (every song, image and clip must be licensed) and what past winners in your category have in common.",
         task="Lock your target category and logline; research 3–5 comparable past winners",
         steps=["As a team, pick one AAHSFF category from the table on the [FMLA DFM overview](index.md#aahsff-categories). Drama is the default if you can't agree.",
                "Write a **logline**: one sentence that names the main character, what they want, and what stands in the way.",
                "Find **3–5 past nominees or winners** in your category. For each, note the title, runtime, and one thing it does well that your film could learn from.",
                "Write your **length target**: about one script page per minute of screen time, under your category's cap."],
         logistics="Draft a **location and talent wishlist**: every place your story might happen and every role you'll need to cast.",
         deliver=["Category + length target", "Logline", "3–5 comparable past winners with notes", "Location/talent wishlist"]),
 9: dict(title="Right-Sizing the Story: Outline & Beat Sheet", dates="Nov 2 – 8, 2026", due="Sun, Nov 8", obj="A1, B1, C2",
         reading=[("StudioBinder: Save the Cat Beat Sheet Explained", SB + "save-the-cat-beat-sheet/")],
         focus="How the beats map onto a short film. A 10-minute film still needs a catalyst, a midpoint and a finale, just compressed.",
         task="Write a full outline / beat sheet sized to your category's runtime cap",
         steps=["Use the Save the Cat beats as a checklist. Every beat gets 1–3 sentences.",
                "Next to each beat, write the **page it lands on** in your script, scaled to your length target.",
                "Cut or merge beats until the total fits under your category's cap."],
         logistics="Narrow your **location shortlist to 2–3** real places, and **start the talent wishlist** with names.",
         deliver=["Beat sheet with page targets", "Location shortlist (2–3)", "Talent wishlist started"]),
 10: dict(title="Screenplay Format & First Draft", dates="Nov 9 – 15, 2026", due="Sun, Nov 15", obj="A3, B1, C2",
          reading=[("StudioBinder: How to Format a Screenplay", SB + "brilliant-script-screenplay-format/")],
          focus="Scene headings (INT./EXT., location, time of day), action lines in present tense, character cues and dialogue.",
          task="Write a complete first draft in proper screenplay format",
          steps=["Turn your beat sheet into scenes, in order.",
                 "Use screenplay format: Courier 12 pt, scene headings, action, character cues, dialogue.",
                 "Check the page count against your length target. Being a little long is fine; you'll cut in Week 11."],
          logistics="**Reach out to your top-choice location(s)** to ask about access and permission. Keep a record of who you contacted and what they said.",
          deliver=["First draft (PDF)", "Location outreach log"]),
 11: dict(title="Table Read & Revision", dates="Nov 16 – 22, 2026", due="Sun, Nov 22", obj="B3, C1, C2",
          reading=[("StudioBinder: What is a Table Read and Why Are They Important?", SB + "table-read-through/")],
          focus="What a table read is for: hearing the script out loud to catch weak dialogue, pacing problems and confusing moments before you shoot.",
          task="Hold a table read and complete a revised draft",
          steps=["Assign every role, plus one reader for action lines. Read the whole script out loud without stopping.",
                 "One teammate takes notes: lines that stumbled, scenes that dragged, anything confusing.",
                 "Revise the script from those notes. Cut until it fits your length target."],
          logistics="Draft a **costume and prop list, scene by scene**.",
          deliver=["Table-read notes", "Revised draft (PDF)", "Costume/prop list"]),
 13: dict(title="Directing Actors I: Communication & Intention", dates="Nov 30 – Dec 6, 2026", due="Sun, Dec 6", obj="A4, B3, C2",
          reading=[("Judith Weston, *Directing Actors*: the opening chapters (acting as doing; playing an intention)", None)],
          focus="Why directors give actors intentions and actions to play instead of line readings.",
          task="Write actor-direction notes for 3 key lines",
          steps=["Pick **3 key lines** from your revised script.",
                 "For each, write the character's **intention**: what they're trying to do to the other person (to warn, to win over, to shut down…).",
                 "Write the direction you'd give the actor. Use intentions and actions, never a line reading (\"say it like this\")."],
          logistics="**Post your casting call** and start reaching out to candidate actors.",
          deliver=["Actor-direction notes for 3 lines", "Casting call (posted)"]),
 14: dict(title="Casting Your Film", dates="Dec 7 – 13, 2026", due="Sun, Dec 13", obj="B3, B4",
          reading=[("StudioBinder: Indie Film Casting Explained", SB + "indie-short-film-casting-pointers/")],
          focus="Casting breakdowns, writing a clear casting call, and running auditions.",
          task="Hold auditions; lock your lead role(s) and backups",
          steps=["Write a short **casting breakdown** for each role: age range, personality, anything the actor must be able to do.",
                 "Hold auditions. Have each actor read a short scene from your script, and record it if they agree.",
                 "Choose your lead(s) and a **backup** for each. Confirm with them in writing."],
          logistics="**Milestone: leads cast.** Record each lead's and backup's name and contact in your cast list.",
          deliver=["Casting breakdown", "Cast list with leads + backups confirmed"]),
 15: dict(title="Locking Locations", dates="Dec 14 – 20, 2026", due="Sun, Dec 20", obj="A1, B4",
          reading=[("StudioBinder: 11 Essential Location Scouting Tips for Any Budget", SB + "essential-film-location-scouting-tips/")],
          focus="Scouting with people you already know, using one location for several scenes, and getting permission in writing.",
          task="Scout and lock your primary location and a backup",
          steps=["Visit your top location(s). Take photos from where the camera would go.",
                 "Check sound (fridges, HVAC, traffic), power outlets, light at your shoot time, and where the crew can wait.",
                 "Get **written permission** from the owner or manager, and lock a **backup** location."],
          logistics="**Milestone: location locked.** Add the primary and backup to your location list with contact info and scouting photos.",
          deliver=["Scouting photos and notes", "Location list with written permission (primary + backup)"]),
 18: dict(title="Blocking, Coverage & Shot Lists for Your Script", dates="Jan 4 – 10, 2027", due="Sun, Jan 10", obj="A4, A5, B1",
          reading=[("StudioBinder: 50+ Types of Camera Shots, Angles, and Techniques", SB + "ultimate-guide-to-camera-shots/"),
                   ("StudioBinder: Film Coverage and Efficient Shot Listing", SB + "film-coverage/")],
          focus="Shot sizes and angles, what each one says about a character, and how coverage gives your editor choices.",
          task="Storyboard and shot-list your locked script at your locked location",
          steps=["For every scene, write the **blocking**: where the actors stand and move.",
                 "Build a **shot list**: scene number, shot number, shot size, angle, movement and a one-line description.",
                 "Storyboard the most important scene. Stick figures are fine."],
          logistics="**Finalize costume and prop sourcing**: who brings what, for which scene.",
          deliver=["Shot list for the whole script", "Storyboard for one key scene", "Final costume/prop sourcing list"]),
 19: dict(title="The Director–Editor Relationship", dates="Jan 11 – 17, 2027", due="Sun, Jan 17", obj="A6, C2",
          reading=[("Walter Murch, *In the Blink of an Eye*, Ch. 1 (\"The Rule of Six\")", None)],
          focus="Murch's six criteria for a cut, and why emotion comes first.",
          task="Plan 3 alternate ways to cut one key moment, and justify your choice",
          steps=["Pick one key moment from your script.",
                 "Describe **3 different ways** it could be cut: which shots, in what order, and where each cut lands.",
                 "Choose one. Justify it with Murch's Rule of Six in 3–5 sentences."],
          logistics="**Confirm remaining supporting cast and extras.**",
          deliver=["3 alternate cuts + justification", "Updated cast list (supporting + extras confirmed)"]),
 20: dict(title="Visual References & Director–DP Collaboration", dates="Jan 18 – 24, 2027", due="Sun, Jan 24", obj="A4, A5",
          reading=[("StudioBinder: Film Lookbook Examples & How to Make a Lookbook", SB + "film-lookbook-examples/"),
                   ("StudioBinder: Film Lighting, The Ultimate Guide", SB + "film-lighting/")],
          focus="How a lookbook shows mood, color and composition, and the basic lighting setups (three-point, high-key, low-key).",
          task="Build a lookbook / mood board, and annotate your shot list with lighting and camera notes",
          steps=["Collect reference images for mood, color, lighting and composition, with a short caption on each.",
                 "Arrange them into a lookbook, organized by scene or by category (lighting, color, framing).",
                 "Add a **lighting and camera note** to each shot on your shot list."],
          logistics="Draft a **shoot-day calendar** for the start of DFM 300: which scenes, where, and who's needed each day.",
          deliver=["Lookbook / mood board", "Annotated shot list", "Draft shoot-day calendar"]),
 21: dict(title="Director's Prep Packet: Integration & AAHSFF Submission Readiness", dates="Jan 25 – 31, 2027", due="Sun, Jan 31",
          obj="A1, B5, C2", reading=[],
          focus="No new reading: review your Weeks 8–20 work.",
          task="Assemble the full Director's Prep Packet",
          steps=["Put everything in one folder, in this order: **script, shot list, blocking, lookbook, cast list, location list, costume/prop list, draft shoot calendar**.",
                 "Check each piece is the latest version and matches the others (same scene numbers, same cast).",
                 "Re-check the current AAHSFF rules and your category's runtime cap."],
          logistics="**Final lock-check.** List anything unresolved for Day 1 of DFM 300.",
          deliver=["Director's Prep Packet (all 8 pieces)", "Unresolved-items list for DFM 300"]),
 22: dict(title="Return from Leave", dates="Feb 1 – 2, 2027", due="Feb 1–2", obj="B5",
          reading=[], focus="No reading.",
          task="Turn in the Director's Prep Packet",
          steps=["Turn in your team's Director's Prep Packet.",
                 "DFM 300 shooting begins with your locked script, cast and locations."],
          logistics="None: you're ready to shoot.",
          deliver=["Director's Prep Packet"]),
}
BREAKS = {12: ("Thanksgiving Break", "Nov 23 – 29, 2026"), 16: ("Winter Break", "Dec 21 – 27, 2026"),
          17: ("Winter Break (continued)", "Dec 28, 2026 – Jan 3, 2027")}

TIMING = [("Stinger", 10, "Today's stinger from the DFM stinger deck; take attendance"),
          ("Weekly Check-In", 5, "Teams open this week's page and split the week's tasks"),
          ("Team Work Time", 58, "Reading, Producing Task and Pre-Production Logistics"),
          ("Team Check-In", 5, "Exit ticket: what the team finished today, what's next, who's doing it")]
assert sum(t[1] for t in TIMING) == 78

def reading_md(w):
    if not w["reading"]:
        return [w["focus"], ""]
    out = []
    for label, url in w["reading"]:
        out.append(f"- [{label}]({url})" if url else f"- {label} (in the course materials)")
    return out + ["", f"**Look for:** {w['focus']}", ""]

def week_page(n, w):
    title = f"Week {n} | {w['title']}"
    b = ["---", "layout: default", f"title: {q(title)}", f"parent: {q(TOP)}", f"nav_order: {n}", "nav_exclude: false", "lesson:",
         f"  course: {q(TOP)}", f"  unit: {n}", f"  number: {q('Week ' + str(n))}",
         f"  standard: {q('DFM 200 objectives ' + w['obj'] + ' (Wilmington University syllabus)')}",
         folded("source", "DFM 200 syllabus, Extended Continuity Plan (Weeks 8–22): self-directed pre-production for an AAHSFF film to shoot in DFM 300. Weeks release Monday and are due Sunday 11:59 PM in Canvas."),
         "  timing:"]
    for seg, mins, note in TIMING:
        b += [f"    - segment: {q(seg)}", f"      minutes: {mins}", f"      note: {q(note)}"]
    prev = f"Builds on the team's Week {n - 1 if n - 1 not in BREAKS else max(k for k in WEEKS if k < n)} work" if n > 8 else "Starts the leave extension: DFM 200's graded weeks ended Oct 23"
    b += ["  the_seven:",
          f"    organization: {q('The week page lists the reading, the Producing Task steps, the logistics milestone and a deliverables checklist, all due ' + w['due'] + '.')}",
          f"    connection: {q(prev + '; every week moves the team’s AAHSFF film one step closer to DFM 300.')}",
          f"    target: {q('SWBAT ' + w['task'][0].lower() + w['task'][1:] + ', shown by the team’s Canvas submission for Producing Task ' + str(n) + '.')}",
          f"    collaboration: {q('Teams split the week’s tasks at the Weekly Check-In and work together in Team Work Time; the Team Check-In names who owns each next step.')}",
          f"    evidence: {q('The Team Check-In exit ticket each class, and the week’s Canvas submission: ' + '; '.join(w['deliver']) + '.')}",
          f"    summarization: {q('Each Team Check-In states what the team finished, what’s next and who’s doing it.')}",
          "  exit_ticket: fmla-dfm",
          "  organize:", "    binder:", "      - \"your Stinger Response Sheet\"", "    drive:",
          "      - item: \"this week's Producing Task and logistics files\"", "        folder: \"your team's DFM 200 folder\"",
          "  differentiation:",
          f"    iep504: {q('Use the page’s deliverables checklist to work one step at a time; the reading can be listened to with text-to-speech; extended time per IEP/504 within the week.')}",
          f"    ell: {q('Sentence frames for the Team Check-In (Today we finished ___. Next, ___ will ___.); readings can be translated in the browser; a teammate can pair-read.')}",
          f"    gt: {q('Take a lead role (producer, director or AD) for the week, and compare your work to one more past AAHSFF winner in your category.')}",
          "  materials:", "    - \"Chromebook or lab computer with Canvas\"", "    - \"Team's shared DFM 200 folder\"",
          "    - \"Stinger Response Sheet\""]
    sub = ("For the sub: project today's stinger from the DFM stinger deck and take attendance, then project this page. "
           "Teams work on this week's tasks for most of the period; circulate and check each team has the page open and "
           "someone working on each deliverable. In the last 5 minutes, each team posts the Team Check-In in Canvas. "
           f"Everything for the week is due {w['due']} at 11:59 PM in Canvas. No live instruction is needed.")
    b += [folded("notes", sub), "---", ""]
    s = [f"# {title} ({w['dates']})", "", "{: .highlight }",
         f"**Due {w['due']}, 11:59 PM in Canvas:** {'; '.join(w['deliver'])}.", "",
         "## In Class (B-days)", "", "| Time | What you do |", "|---|---|"]
    s += [f"| {m} min | {seg} |" for seg, m, _ in TIMING]
    s += ["", "## Stinger (~10 min)", "", "{% include lesson-parts/stinger.md %}", "", "## This Week's Reading", ""] + reading_md(w)
    s += [f"## Producing Task {n}: {w['task']}", ""] + [f"{i}. {st}" for i, st in enumerate(w["steps"], 1)] + [""]
    s += ["## Pre-Production Logistics", "", w["logistics"], "", "## Before You Submit", ""]
    s += [f"- [ ] {d}" for d in w["deliver"]] + ["- [ ] Everything is saved in your team's DFM 200 folder", "- [ ] Submitted in Canvas", ""]
    s += ["## Team Check-In (last ~5 min)", "", "{% include lesson-parts/organize.html %}", "", "{% include exit-ticket/fmla-dfm.md %}", ""]
    write(f"{FOLDER}/week{n}.md", "\n".join(b) + "\n".join(s))
    write(f"{FOLDER}/week{n}-teacher.md", "\n".join([
        "---", "layout: default", f"title: {q(title + ' (Teacher)')}", f"parent: {q(TOP)}", "nav_exclude: true", "has_toc: false", "---",
        f"# {title} | Teacher Plan", "", "{% include teacher-plan.html %}", ""]))

def index():
    rows = []
    for n in range(8, 23):
        if n in BREAKS:
            rows.append(f"| {n} | {BREAKS[n][1]} | {BREAKS[n][0]} | No new material |")
        else:
            w = WEEKS[n]
            rows.append(f"| [{n}](week{n}.md) | {w['dates']} | {w['title']} | Producing Task {n}, due {w['due']} |")
    b = ["---", "layout: default", f"title: {q(TOP)}", "parent: \"FMLA\"", "nav_order: 3", "has_children: true", "has_toc: false",
         f"description: {q('DFM 200 Weeks 8–22: self-directed pre-production for an AAHSFF film while the instructor is on leave.')}", "---",
         "# FMLA DFM: Introduction to Digital Filmmaking During Leave", "",
         "DFM 200's graded weeks end **Oct 23, 2026**. While your instructor is on leave (through **Feb 2, 2027**), your team keeps "
         "going on one goal: **writing and prepping a script for the All American High School Film Festival (AAHSFF)**, which you'll "
         "shoot in DFM 300 next semester and submit to the festival.", "",
         "## How Each Week Works", "",
         "- A new week opens every **Monday**. Everything for that week is due **Sunday at 11:59 PM in Canvas**.",
         "- Each week has a **reading**, a **Producing Task** and a **Pre-Production Logistics** step. They build on each other into your Director's Prep Packet.",
         "- In class on B-days: stinger, a quick team check-in, team work time, then a Team Check-In before you leave.",
         "- This work is separate from DFM 200's graded assignments. It's graded for completion in Canvas.", "",
         "## Schedule", "", "| Week | Dates | Topic | Due |", "|---|---|---|---|"] + rows + [
         "", "## AAHSFF Categories", "",
         "Lock one in Week 8. It sets your script's length for every week after: about **one script page per minute** of screen time.", "",
         "| Category | Max length |", "|---|---|"] + [f"| {c} | {m} |" for c, m in CATEGORIES] + [
         "", "Check the [current rules and categories](https://www.hsfilmfest.com/rulesandcategories) once the 2026–27 cycle opens "
         "(expected around November 2026): the categories and dates can change.", "",
         "## For the Substitute", "",
         "- Start class by projecting today's stinger from the [DFM stinger deck](bellringers.md) and taking attendance. Then project the current week's page.",
         "- Teams work on their own. Circulate and check each team has the week's page open and someone working on each deliverable.",
         "- In the last 5 minutes, each team posts its Team Check-In in Canvas.",
         "- Each week's teacher page has the full plan. Add `-teacher` to the end of the page's address, for example `week8-teacher.html`.", ""]
    write(f"{FOLDER}/index.md", "\n".join(b))

def stingers():
    write(f"{FOLDER}/bellringers.md", "\n".join([
        "---", "layout: default", "title: Daily Stingers", f"parent: {q(TOP)}", "nav_order: 1", "nav_exclude: false",
        "embed_extra: bellringer", "---", "# Daily Stingers", "",
        "Every class begins with the same 10-minute routine, using the deck below:", "",
        "1. **Rewrite** today's question in your own words, on your own line.",
        "2. **Write your response.** At least 3 sentences, aim for 5. *Stuck on how to start? Try: \"I think ___ because ___. One example of this is ___.\"*",
        "3. **Share** your response with a classmate.", "4. **Copy** their response underneath yours.",
        "5. **Synthesize** what the two responses had in common, in 1 to 2 sentences.", "",
        "## Stinger Deck", "", "<div class=\"presentation-embed\">",
        " <iframe class=\"presentation-embed-fill\" src=\"https://docs.google.com/presentation/d/1ahg761Fp8akGa_0s0bGynTu5FVwnpd4-ZLspv5dQwCY/embed?start=false&loop=false&delayms=3000\" allowfullscreen loading=\"lazy\"></iframe>",
        "</div>", ""]))

def exit_ticket():
    write("_includes/exit-ticket/fmla-dfm.md",
"""📤 **Team Check-In.** One teammate posts for the team in this week's Canvas Team Check-In:

* **what your team finished today** (name the deliverable),
* **what's next**, and
* **who's doing it**, by name.

*Stuck on how to start? Try: "Today we finished ___. Next, ___ will ___ by ___."*
""")
    write("_includes/exit-ticket/fmla-dfm-teacher.md",
"""**Team Check-In (FMLA DFM).** In the last 5 minutes, one teammate posts for the team in this week's
Canvas Team Check-In: what the team finished today, what's next, and who's doing it. Completion
credit in Canvas. Use the posts to see which teams are stalled before each Sunday deadline.
""")

def main():
    exit_ticket()
    stingers()
    index()
    for n, w in WEEKS.items():
        week_page(n, w)

if __name__ == "__main__":
    main()
