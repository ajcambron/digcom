#!/usr/bin/env python3
"""Generate the FMLA DFM section: DFM 200 during leave, on the same unit calendar and grading math as FMLA FDD/ADD.

Run from the repo root:  python3 scripts/fmla/gen_dfm.py
Re-running overwrites fmla-dfm/ and the DFM exit-ticket includes.

Source: "DFM 200 Course Syllabus – Scheduled", Extended Continuity Plan (Weeks 8–22): every team writes and preps
a script for the All American High School Film Festival (AAHSFF), to shoot in DFM 300. That content is mapped
onto the district unit calendar (_data/calendar.yml), Units 4–6 (MP2): four formative days (F | u.1–u.4) and an
S block (S | u) per unit, F before S. DFM meets on B-days only, so each F label is one class and each S block is
three. The college 7-week session (Units 1–3) ends Oct 23 with the DFM 200 Final Presentation.

Grading math (internal planning only, never printed on a page), matching FMLA FDD: every formative is worth
10 points and the unit summatives total 300 — 12 formatives = 120 points, 3 summatives x 100 = 300 points.
"""
import json, os, shutil, textwrap

ROOT = os.getcwd()
FOLDER = "fmla-dfm"
TOP = "FMLA DFM"
q = lambda s: json.dumps(s, ensure_ascii=False)
FORMATIVE_PTS, SUMMATIVE_PTS = 10, 100
DFM_SCHEMA = dict(formatives=12, formative_pts=120, summative_pts=300)

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
AAHSFF_RULES = "https://www.hsfilmfest.com/rulesandcategories"
CATEGORIES = [("Drama (recommended default)", "20 min"), ("Comedy", "15 min"), ("Documentary", "15 min"),
              ("Horror / Sci-Fi / Fantasy", "10 min"), ("Animation", "10 min"), ("Experimental", "10 min"),
              ("Video Podcast", "10 min"), ("Storyblocks: Representation Through Storytelling", "15 min"),
              ("Broadcast Journalism: Feature Story", "5 min"), ("Sports Feature", "5 min"), ("Music Video", "5 min"),
              ("Micro Movie", "1 min")]

# B-day class dates from _data/calendar.yml (A/B rotation anchored on the syllabus's B-days).
# Each formative is due before the next class; each summative on the last S day.
UNITS = {
 4: dict(title="Writing the Script", dates="Nov 4 – Dec 1, 2026",
         f_dates=["Wed, Nov 4", "Fri, Nov 6", "Tue, Nov 10", "Fri, Nov 13"], s_dates=["Tue, Nov 17", "Thu, Nov 19", "Mon, Nov 30"],
         intro="Your team picks an AAHSFF category, then takes the story from a one-sentence logline to a locked, properly formatted script.",
         F=[dict(title="AAHSFF Target & Logline", obj="A1, B5, B6",
                 reading=[("AAHSFF Rules & Categories", AAHSFF_RULES)],
                 focus="Your category's runtime cap, the content rules (every song, image and clip must be licensed) and what past winners in your category have in common.",
                 steps=["As a team, pick one AAHSFF category from the table on the [FMLA DFM overview](../index.md#aahsff-categories). Drama is the default if you can't agree.",
                        "Write a **logline**: one sentence that names the main character, what they want, and what stands in the way.",
                        "Find **3–5 past nominees or winners** in your category on the festival site. For each, note the title, runtime, and one thing it does well.",
                        "Write your **length target**: about one script page per minute of screen time, under your category's cap.",
                        "Draft a **location and talent wishlist**: every place your story might happen and every role you'll need."],
                 deliver=["Category + length target", "Logline", "3–5 comparable past winners with notes", "Location/talent wishlist"]),
            dict(title="Outline & Beat Sheet", obj="A1, B1, C2",
                 reading=[("StudioBinder: Save the Cat Beat Sheet Explained", SB + "save-the-cat-beat-sheet/")],
                 focus="How the beats map onto a short film. A 10-minute film still needs a catalyst, a midpoint and a finale, just compressed.",
                 steps=["Use the Save the Cat beats as a checklist. Give every beat 1–3 sentences.",
                        "Next to each beat, write the **page it lands on**, scaled to your length target.",
                        "Cut or merge beats until the total fits under your category's cap.",
                        "Narrow your location wishlist to a **shortlist of 2–3** real places."],
                 deliver=["Beat sheet with page targets", "Location shortlist (2–3)"]),
            dict(title="Screenplay Format & First Draft", obj="A3, B1, C2",
                 reading=[("StudioBinder: How to Format a Screenplay", SB + "brilliant-script-screenplay-format/")],
                 focus="Scene headings (INT./EXT., location, time of day), action lines in present tense, character cues and dialogue.",
                 steps=["Split the beat sheet between teammates, one section each.",
                        "Write your section in screenplay format: Courier 12 pt, scene headings, action, character cues, dialogue.",
                        "Combine the sections into one draft and check the page count against your length target.",
                        "Reach out to your top-choice location about access and permission, and log who you contacted."],
                 deliver=["First draft (PDF)", "Location outreach log"]),
            dict(title="Table Read & Revision", obj="B3, C1, C2",
                 reading=[("StudioBinder: What is a Table Read and Why Are They Important?", SB + "table-read-through/")],
                 focus="Hearing the script out loud to catch weak dialogue, pacing problems and confusing moments before you shoot.",
                 steps=["Assign every role, plus one reader for action lines. Read the whole script out loud without stopping.",
                        "One teammate takes notes: lines that stumbled, scenes that dragged, anything confusing.",
                        "Revise the script from those notes and cut until it fits your length target.",
                        "Draft a **costume and prop list, scene by scene**."],
                 deliver=["Table-read notes", "Revised draft (PDF)", "Costume/prop list"])],
         S=dict(title="Locked Script & Actor Notes", obj="A4, B3, B5, C2",
                reading=[("Judith Weston, *Directing Actors*: the opening chapters (acting as doing; playing an intention)", None)],
                focus="Why directors give actors intentions and actions to play instead of line readings.",
                steps=["Make final fixes to your revised draft. Check it fits your length target, then label it **LOCKED** with the date.",
                       "Pick **3 key lines**. For each, write the character's **intention**: what they're trying to do to the other person (to warn, to win over, to shut down…).",
                       "Write the direction you'd give the actor for each line: intentions and actions, never a line reading.",
                       "Write and post your **casting call**: the project, each role, the shoot dates and how to audition."],
                deliver=["Locked script (PDF)", "Actor-direction notes for 3 key lines", "Casting call (posted)"])),
 5: dict(title="Casting & Locations", dates="Dec 2, 2026 – Jan 4, 2027",
         f_dates=["Wed, Dec 2", "Fri, Dec 4", "Tue, Dec 8", "Thu, Dec 10"], s_dates=["Mon, Dec 14", "Wed, Dec 16", "Fri, Dec 18"],
         intro="Your team casts the film and locks where it will be shot, so DFM 300 can start shooting on day one.",
         F=[dict(title="Casting Breakdown", obj="B3, C2",
                 reading=[("StudioBinder: Indie Film Casting Explained", SB + "indie-short-film-casting-pointers/")],
                 focus="Casting breakdowns, writing a clear casting call, and running auditions.",
                 steps=["Write a **casting breakdown** for each role: age range, personality, and anything the actor must be able to do.",
                        "Pick a short audition scene (1–2 pages) from your locked script.",
                        "List candidate actors for each role, and reach out to at least two per lead role."],
                 deliver=["Casting breakdown", "Audition scene", "Candidate list with outreach"]),
            dict(title="Auditions", obj="B3, C1",
                 reading=[],
                 focus="No new reading: use the casting article from 5.1.",
                 steps=["Hold auditions. Each actor reads the audition scene; record it if they agree.",
                        "Take notes on each actor right after they read: fit for the role, how they took direction.",
                        "Rank your choices for each role."],
                 deliver=["Audition notes and rankings"]),
            dict(title="Location Scouting", obj="A1, B4",
                 reading=[("StudioBinder: 11 Essential Location Scouting Tips for Any Budget", SB + "essential-film-location-scouting-tips/")],
                 focus="Scouting with people you already know, using one location for several scenes, and getting permission in writing.",
                 steps=["Visit your top 2–3 locations (or study photos if you can't visit during class).",
                        "Take photos from where the camera would go.",
                        "Check sound (fridges, HVAC, traffic), power outlets, light at your shoot time, and where the crew can wait."],
                 deliver=["Scouting photos and notes for each location"]),
            dict(title="Permissions & Sourcing", obj="B4",
                 reading=[],
                 focus="No new reading: use the location article from 5.3.",
                 steps=["Ask your top location's owner or manager for **written permission**, and pick a **backup** location.",
                        "Turn your costume/prop list into a **sourcing list**: who brings what, for which scene.",
                        "Offer your lead roles to your first choices and confirm a backup for each."],
                 deliver=["Permission request (sent) + backup location", "Costume/prop sourcing list", "Role offers sent"])],
         S=dict(title="Cast & Location Lock", obj="A1, B3, B4",
                reading=[], focus="No new reading: this block finishes and checks everything from 5.1–5.4.",
                steps=["**Cast list:** every role with the actor's name and contact, plus a backup for each lead, all confirmed in writing.",
                       "**Location list:** primary and backup locations with contact info, scouting photos and written permission.",
                       "**Costume/prop list:** final, with who is bringing each item.",
                       "Check all three lists match your locked script: same scenes, same characters."],
                deliver=["Cast list (leads + backups confirmed)", "Location list with written permission", "Final costume/prop list"])),
 6: dict(title="Visual Plan & Director's Prep Packet", dates="Jan 5 – 22, 2027",
         f_dates=["Tue, Jan 5", "Thu, Jan 7", "Mon, Jan 11", "Wed, Jan 13"], s_dates=["Fri, Jan 15", "Wed, Jan 20", "Fri, Jan 22"],
         intro="Your team plans every shot and the look of the film, then assembles the Director's Prep Packet you'll shoot from in DFM 300.",
         F=[dict(title="Blocking & Shot List", obj="A4, A5, B1",
                 reading=[("StudioBinder: 50+ Types of Camera Shots, Angles, and Techniques", SB + "ultimate-guide-to-camera-shots/"),
                          ("StudioBinder: Film Coverage and Efficient Shot Listing", SB + "film-coverage/")],
                 focus="Shot sizes and angles, what each one says about a character, and how coverage gives your editor choices.",
                 steps=["For every scene, write the **blocking**: where the actors stand and move.",
                        "Build a **shot list**: scene number, shot number, shot size, angle, movement and a one-line description."],
                 deliver=["Blocking notes", "Shot list for the whole script"]),
            dict(title="Storyboard", obj="A4, A5",
                 reading=[],
                 focus="No new reading: use the camera-shots article from 6.1.",
                 steps=["Pick your most important scene.",
                        "Storyboard every shot in it, matching your shot list. Stick figures are fine; show framing and movement.",
                        "Fix anything in the shot list the storyboard showed you was missing."],
                 deliver=["Storyboard for one key scene", "Updated shot list"]),
            dict(title="Director–Editor: Alternate Cuts", obj="A6, C2",
                 reading=[("Walter Murch, *In the Blink of an Eye*, Ch. 1 (\"The Rule of Six\")", None)],
                 focus="Murch's six criteria for a cut, and why emotion comes first.",
                 steps=["Pick one key moment from your script.",
                        "Describe **3 different ways** it could be cut: which shots, in what order, and where each cut lands.",
                        "Choose one and justify it with Murch's Rule of Six in 3–5 sentences.",
                        "Add any shots your chosen cut needs to the shot list."],
                 deliver=["3 alternate cuts + justification"]),
            dict(title="Lookbook & Lighting", obj="A4, A5",
                 reading=[("StudioBinder: Film Lookbook Examples & How to Make a Lookbook", SB + "film-lookbook-examples/"),
                          ("StudioBinder: Film Lighting, The Ultimate Guide", SB + "film-lighting/")],
                 focus="How a lookbook shows mood, color and composition, and the basic lighting setups (three-point, high-key, low-key).",
                 steps=["Collect reference images for mood, color, lighting and composition, each with a short caption.",
                        "Arrange them into a lookbook, organized by scene or by category.",
                        "Add a **lighting and camera note** to each shot on your shot list."],
                 deliver=["Lookbook / mood board", "Shot list with lighting and camera notes"])],
         S=dict(title="Director's Prep Packet", obj="A1, B5, C2",
                reading=[("AAHSFF Rules & Categories (re-check the current cycle)", AAHSFF_RULES)],
                focus="Your category's rules and runtime cap for the 2026–27 cycle.",
                steps=["Draft a **shoot-day calendar** for the start of DFM 300: which scenes, where, and who's needed each day.",
                       "Put everything in one folder, in this order: **script, shot list, blocking, storyboard, lookbook, cast list, location list, costume/prop list, shoot calendar**.",
                       "Check every piece is the latest version and matches the others (same scene numbers, same cast).",
                       "List anything unresolved for Day 1 of DFM 300."],
                deliver=["Director's Prep Packet (all 9 pieces)", "Unresolved-items list for DFM 300"])),
}

F_TIMING = [("Stinger", 10, "Today's stinger from the DFM stinger deck; take attendance"),
            ("Team Check-In", 5, "Teams open today's page and split today's steps"),
            ("Reading", 15, "Today's reading, or review of the last one"),
            ("Team Work Time", 43, "Today's formative steps"),
            ("Save & Wrap-Up", 5, "Save to the team folder; note what's left before the due date")]
S_TIMING = [("Stinger", 10, "Today's stinger from the DFM stinger deck; take attendance"),
            ("Team Check-In", 5, "Teams check the summative checklist"),
            ("Finish the Summative", 58, "Finish, check and assemble the unit's summative"),
            ("Save & Wrap-Up", 5, "Save to the team folder; submit on the last S day")]
for t in (F_TIMING, S_TIMING):
    assert sum(x[1] for x in t) == 78

FORMATIVE_CHECK = ("Check system: ✓+ every deliverable is complete and specific to the team's film; ✓ every deliverable is "
                   "submitted; ✓− a deliverable is missing.")
SUMMATIVE_CHECK = ("Check system for the summative: ✓+ every piece is complete, matches the team's earlier work (same scenes, cast and "
                   "category) and shows revision; ✓ every piece is complete and usable for DFM 300; ✓− a piece is missing or doesn't "
                   "match the rest of the team's work.")

def reading_md(item):
    if not item["reading"]:
        return [item["focus"], ""]
    out = [f"- [{label}]({url})" if url else f"- {label} (in the course materials)" for label, url in item["reading"]]
    return out + ["", f"**Look for:** {item['focus']}", ""]

def lesson_front(unit, num, title, item, timing, summative, due, prev):
    L = ["---", "layout: default", f"title: {q(title)}", f"parent: {q(TOP + ' | Unit ' + str(unit))}", "nav_exclude: false", "lesson:",
         f"  course: {q(TOP)}", f"  unit: {unit}", f"  number: {q(num)}"]
    if summative:
        L.append("  is_summative: true")
    L += [f"  standard: {q('DFM 200 objectives ' + item['obj'] + ' (Wilmington University syllabus)')}",
          folded("source", "DFM 200 syllabus, Extended Continuity Plan: self-directed pre-production for an AAHSFF film to shoot in DFM 300, mapped onto the district unit calendar (B-days)."),
          "  timing:"]
    for seg, m, note in timing:
        L += [f"    - segment: {q(seg)}", f"      minutes: {m}", f"      note: {q(note)}"]
    kind = "summative" if summative else "formative"
    L += ["  the_seven:",
          f"    organization: {q('The page lists today’s reading, numbered steps and a deliverables checklist. Graded: the ' + kind + ', due ' + due + '.')}",
          f"    connection: {q(prev)}",
          f"    target: {q('SWBAT ' + item['title'][0].lower() + item['title'][1:] + ' for their team’s AAHSFF film, shown by the submitted ' + kind + ': ' + '; '.join(item['deliver']) + '.')}",
          f"    collaboration: {q('Teams split the steps at the Team Check-In and work together; each teammate owns at least one deliverable.')}",
          f"    evidence: {q('The submitted ' + kind + ': ' + '; '.join(item['deliver']) + '.')}",
          f"    summarization: {q('At wrap-up each team notes what is done and what is left before the due date.')}",
          "  organize:", "    binder:", "      - \"your Stinger Response Sheet\"", "    drive:",
          "      - item: \"today's deliverables\"", "        folder: \"your team's DFM folder\"",
          "  differentiation:",
          f"    iep504: {q('Work the numbered steps one at a time with the deliverables checklist; readings can be listened to with text-to-speech; extended time per IEP/504.')}",
          f"    ell: {q('Readings can be translated in the browser; a teammate can pair-read; sentence frame for notes: This scene needs ___ because ___.')}",
          f"    gt: {q('Take a lead role (producer, director or AD) for the day, and compare your work to one more past AAHSFF winner in your category.')}",
          "  materials:", "    - \"Chromebook or lab computer\"", "    - \"Team's shared DFM folder\"", "    - \"Stinger Response Sheet\""]
    sub = ("For the sub: project today's stinger from the DFM stinger deck and take attendance, then project this page. Teams work "
           "on their own; circulate and check each team has the page open and someone working on each deliverable. ")
    sub += (f"Summative: submitted on the last S day, {due}. Teacher grading (on return): {SUMMATIVE_CHECK} " if summative else
            f"Formative: due {due}. Teacher grading (on return): {FORMATIVE_CHECK} ")
    L += [folded("notes", sub + "No live instruction is needed."), "---", ""]
    return "\n".join(L)

def body(title, item, timing, head, extra=None):
    b = [f"# {title}", "", "{: .highlight }", head, ""]
    if extra:
        b += extra
    b += ["## Today's Plan", "", "| Time | What you do |", "|---|---|"] + [f"| {m} min | {seg} |" for seg, m, _ in timing]
    b += ["", "## Stinger (~10 min)", "", "{% include lesson-parts/stinger.md %}", "", "## Reading", ""] + reading_md(item)
    b += ["## Steps", ""] + [f"{i}. {st}" for i, st in enumerate(item["steps"], 1)] + [""]
    b += ["## Before You Submit", ""] + [f"- [ ] {d}" for d in item["deliver"]]
    b += ["- [ ] Everything is saved in your team's DFM folder", "- [ ] Submitted", ""]
    b += ["## Wrap-Up", "", "Save to your team folder and note what's left before the due date.", "",
          "{% include lesson-parts/organize.html %}", ""]
    return "\n".join(b)

def teacher(unit, slug, title):
    write(f"{FOLDER}/fmla{unit}/{slug}-teacher.md", "\n".join([
        "---", "layout: default", f"title: {q(title + ' (Teacher)')}", f"parent: {q(TOP + ' | Unit ' + str(unit))}",
        f"grandparent: {q(TOP)}", "nav_exclude: true", "has_toc: false", "---",
        f"# {title} | Teacher Plan", "", "{% include teacher-plan.html %}", ""]))

def unit_pages(unit, U):
    for i, item in enumerate(U["F"], 1):
        num = f"{unit}.{i}"
        title = f"{num} | {item['title']}"
        nxt = U["f_dates"][i] if i < 4 else U["s_dates"][0]
        due = f"the start of your next class ({nxt})"
        prev = (f"Builds on {unit}.{i - 1} ({U['F'][i - 2]['title']})" if i > 1 else
                f"Builds on the team's Unit {unit - 1} work" if unit > 4 else "Starts the team’s AAHSFF film after the DFM 200 Final Presentation")
        head = f"Today's graded assignment ({U['f_dates'][i - 1]}): **{item['title']} (formative)**, due {due}."
        write(f"{FOLDER}/fmla{unit}/{unit}_{i}.md",
              lesson_front(unit, num, title, item, F_TIMING, False, due, prev + "; it feeds this unit’s summative.") + body(title, item, F_TIMING, head))
        teacher(unit, f"{unit}_{i}", title)
    S = U["S"]
    title = f"S | {unit} | {S['title']}"
    due = U["s_dates"][-1]
    head = f"Graded assignment: **{S['title']} (summative)**. Submit it by the end of the last S day, **{due}**."
    extra = ["{: .important }", f"**S days:** {'; '.join(U['s_dates'])}. This summative pulls together {unit}.1–{unit}.4, so most of it "
             "is already done: finish it, check every piece matches, and submit.", ""]
    write(f"{FOLDER}/fmla{unit}/s{unit}.md",
          lesson_front(unit, f"S{unit}", title, S, S_TIMING, True, due, f"Pulls together {unit}.1–{unit}.4 into one finished product.")
          + body(title, S, S_TIMING, head, extra))
    teacher(unit, f"s{unit}", title)
    # unit index
    rows = [f"| [{unit}.{i}]({unit}_{i}.md) | {U['f_dates'][i - 1]} | {it['title']} (formative) |" for i, it in enumerate(U["F"], 1)]
    rows.append(f"| [S{unit}](s{unit}.md) | {'; '.join(U['s_dates'])} | {S['title']} (summative) |")
    write(f"{FOLDER}/fmla{unit}/index.md", "\n".join([
        "---", "layout: default", f"title: {q(TOP + ' | Unit ' + str(unit))}", f"nav_order: {unit}", f"parent: {q(TOP)}",
        f"description: {q(U['title'])}", "has_children: true", "has_toc: false", "---",
        f"# Unit {unit} | {U['title']} ({U['dates']})", "", "## Introduction", "", U["intro"], "",
        "DFM meets on **B-days**, so each formative day below is one class and the S block is three.", "",
        "## Graded Assignments", "", "| Day | Class (B-day) | Graded assignment |", "|---|---|---|"] + rows + [
        "", "## Calendar of Events for This Unit", "", "Your class meets on the B-day of each pair.", "",
        f"{{% include calendar-of-events.html unit={unit} %}}", ""]))

def index():
    rows = [f"| [Unit {u}](fmla{u}/index.md) | {U['dates']} | {U['title']} | {U['S']['title']} |" for u, U in UNITS.items()]
    graded = ["| Unit | .1 | .2 | .3 | .4 | S (summative) |", "|---|---|---|---|---|---|"]
    graded += [f"| {u} | " + " | ".join(f["title"] for f in U["F"]) + f" | {U['S']['title']} |" for u, U in UNITS.items()]
    write(f"{FOLDER}/index.md", "\n".join([
        "---", "layout: default", f"title: {q(TOP)}", "parent: \"FMLA\"", "nav_order: 3", "has_children: true", "has_toc: false",
        f"description: {q('DFM 200 Units 4–6 while the teacher is on leave: pre-production for an AAHSFF film to shoot in DFM 300.')}", "---",
        "# FMLA DFM: Introduction to Digital Filmmaking During Leave", "",
        "DFM 200's college session ends **Oct 23, 2026** with the Final Presentation. While your teacher is on leave, Units 4–6 keep your "
        "team working toward one goal: **writing and prepping a script for the All American High School Film Festival (AAHSFF)**, which "
        "you'll shoot in DFM 300 and submit to the festival.", "",
        "| Unit | Dates | Focus | Summative |", "|---|---|---|---|"] + rows + [
        "", "## Every Class", "",
        "DFM meets on **B-days**. Every class follows the same routine:", "",
        "1. **Stinger (10 min).** Answer the day's stinger on your Stinger Response Sheet.",
        "2. **Team check-in (5 min).** Open the day's page and split the steps.",
        "3. **Reading and team work time.** Do the reading, then the day's steps together.",
        "4. **Save and wrap up** before you leave.", "",
        "## How You're Graded", "",
        "Each unit has four formatives (one per class, due by the start of the next class) and one summative that pulls them together, "
        "submitted on the last S day.", ""] + graded + [
        "", "## Before Unit 4 (Oct 27 and 29)", "",
        "The S | 3 days after the Final Presentation are a head start, with nothing graded: form your team and watch past AAHSFF "
        "nominees and winners on the [festival site](https://www.hsfilmfest.com/) so you're ready to lock a category on 4.1.", "",
        "## AAHSFF Categories", "",
        "Lock one on 4.1. It sets your script's length from then on: about **one script page per minute** of screen time.", "",
        "| Category | Max length |", "|---|---|"] + [f"| {c} | {m} |" for c, m in CATEGORIES] + [
        "", f"Check the [current rules and categories]({AAHSFF_RULES}) once the 2026–27 cycle opens (expected around November 2026): "
        "the categories and dates can change.", "",
        "## For the Substitute", "",
        "- Start class by projecting today's stinger from the [DFM stinger deck](bellringers.md) and taking attendance. Then project the day's page (find it on the unit page).",
        "- Teams work on their own. Circulate and check each team has the page open and someone working on each deliverable.",
        "- Each day's teacher page has the full plan and grading notes. Add `-teacher` to the end of the page's address, for example `4_1-teacher.html`.", ""]))

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

def schema_check():
    n_form = sum(len(U["F"]) for U in UNITS.values())
    got = dict(formatives=n_form, formative_pts=n_form * FORMATIVE_PTS, summative_pts=len(UNITS) * SUMMATIVE_PTS)
    print(f"DFM schema: {got['formatives']} formatives / {got['formative_pts']} pts, {got['summative_pts']} summative pts")
    for k, v in DFM_SCHEMA.items():
        if got[k] != v:
            print(f"WARNING: DFM schema {k}: planned {v}, got {got[k]}")

def main():
    shutil.rmtree(os.path.join(ROOT, FOLDER), ignore_errors=True)
    for old in ("_includes/exit-ticket/fmla-dfm.md", "_includes/exit-ticket/fmla-dfm-teacher.md"):
        if os.path.exists(os.path.join(ROOT, old)):
            os.remove(os.path.join(ROOT, old))
    stingers()
    index()
    for u, U in UNITS.items():
        assert len(U["F"]) == 4 and len(U["f_dates"]) == 4 and len(U["s_dates"]) == 3
        unit_pages(u, U)
    schema_check()

if __name__ == "__main__":
    main()
