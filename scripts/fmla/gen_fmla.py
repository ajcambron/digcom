#!/usr/bin/env python3
"""Generate the FMLA FDD and FMLA ADD sections (Units 3-6): BrainBuffet-module pacing pages.

Run from the repo root:  python3 scripts/fmla/gen_fmla.py
Re-running overwrites fmla-fdd/, fmla-add/ and the fmla vocab/exit-ticket includes.
"""
import json, os, sys, textwrap
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modules import AI, PR, FDD_UNITS, ADD_UNITS, UNIT_DATES

ROOT = os.getcwd()
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

def mmss(sec):
    return f"{sec // 60}:{sec % 60:02d}"

# Minutes of hands-on BrainBuffet time in each kind of class period (see TIMING below).
WORK = {"F1": 58, "F2": 48, "F3": 33, "F4": 55, "S": 58}

COURSES = {
 "fdd": dict(key="FMLA FDD", top="FMLA FDD", folder="fmla-fdd", nav=25, app="Illustrator", course_name="Foundations of Digital Design",
             units=FDD_UNITS, mods=AI, unit_label="GMetrix Illustrator", regular="foundations/fdd"),
 "add": dict(key="FMLA ADD", top="FMLA ADD", folder="fmla-add", nav=45, app="Premiere Pro", course_name="Applications of Digital Design",
             units=ADD_UNITS, mods=PR, unit_label="GMetrix Premiere", regular="applications/add"),
}

def s_days(unit):
    days = UNIT_DATES[unit][1]
    lo = (days - 8) // 2
    hi = days - 8 - lo
    return lo, hi

def plan_days(cid, unit, mod):
    """Return ordered list of (day_key, work_minutes) that carry video lessons."""
    days = [("F1", WORK["F1"]), ("F2", WORK["F2"]), ("F3", WORK["F3"]), ("F4", WORK["F4"])]
    total = sum(v[1] for v in mod["videos"])
    lo, _ = s_days(unit)
    if cid == "fdd":
        if total > 130 * 60:
            days.append(("S1", WORK["S"]))
    elif mod["short"] != "Exam Prep & Practice":
        for k in range(1, lo):           # keep the last S day for export + submit
            days.append((f"S{k}", WORK["S"]))
    return days

def allocate(videos, days):
    total = sum(v[1] for v in videos)
    wtot = sum(d[1] for d in days)
    bounds, acc = [], 0
    for key, w in days:
        acc += w
        bounds.append((key, acc / wtot))
    out = {k: [] for k, _ in days}
    run = 0
    for vid in videos:
        mid = (run + vid[1] / 2) / total
        run += vid[1]
        for key, b in bounds:
            if mid <= b + 1e-9:
                out[key].append(vid)
                break
    return out

def video_table(vs):
    rows = ["| Video | Length | Title |", "|---|---|---|"]
    rows += [f"| {v[0]} | {v[2]} | {v[3]} |" for v in vs]
    return "\n".join(rows)

def pace_text(alloc, key, mod):
    vs = alloc.get(key, [])
    if not vs:
        return None, None
    last = vs[-1]
    return last, f"by the end of class, finish **video {last[0]}: {last[3]}**"

# ---------------------------------------------------------------- daily routine text
def start_steps(c, mod_no):
    if c["app"] == "Illustrator":
        files = ("Save every BrainBuffet file in your Digital Design Drive folder, in **Project Files**, "
                 "named the way the video names it.")
        open_app = "Open **Illustrator**."
    else:
        files = ("The module's footage lives in **`/Users/Shared/GMetrix`** on every lab Mac (Finder › "
                 "**Go › Go to Folder…**). It's read-only: keep your own `.prproj` in your project folder and "
                 "back it up to Drive at the end of class. Lost? See [ADD 2.1, Finding the GMetrix "
                 "Folder]({{% link applications/add2/2_1.md %}}#finding-the-gmetrix-folder).")
        open_app = "Open **Premiere Pro**."
    return (f"1. Open **GMetrix SMS** and log in with Google (school account).\n"
            f"2. Open the BrainBuffet **{c['app']}** course and go to **Module {mod_no}**. Start at the "
            f"first video you haven't finished.\n"
            f"3. {open_app} Put the video on one side of the screen and {c['app']} on the other, and "
            f"pause the video to do each step yourself.\n"
            f"4. {files}\n"
            f"5. Use headphones. Captions and transcripts are available on every video.")

STINGER = ("Answer on your **Stinger Response Sheet** ([download]({{ '/assets/downloads/stinger-response-sheet.pdf' | relative_url }}) "
           "if you need a new one): rewrite the question, answer it in at least 3 sentences, share with a "
           "neighbor, copy their answer, then write 1–2 sentences on what your answers had in common.")

# ---------------------------------------------------------------- page builders
def front(title, parent, top, lesson_lines):
    return "\n".join(["---", "layout: default", f"title: {q(title)}", f"parent: {q(parent)}",
                      f"grandparent: {q(top)}", "nav_exclude: false", "lesson:"] + lesson_lines + ["---", ""])

def teacher_page(folder, unit, slug, title, parent, top):
    write(f"{folder}/fmla{unit}/{slug}-teacher.md", "\n".join([
        "---", "layout: default", f"title: {q(title + ' (Teacher)')}", f"parent: {q(parent)}",
        f"grandparent: {q(top)}", "nav_exclude: true", "has_toc: false", "---",
        f"# {title} | Teacher Plan", "", "{% include teacher-plan.html %}", ""]))

TIMING = {
 "F1": [("Bell Ringer / Stinger", 10, "Stinger prompt on the page; take attendance"),
        ("Pace Check", 5, "Students find today's pace goal and the first video they haven't finished"),
        ("BrainBuffet Module Work", 58, "Self-paced videos, following along in the app"),
        ("Exit Ticket", 5, "Graded: Pace Check Exit Ticket, posted in Schoology")],
 "F2": [("Bell Ringer / Stinger", 10, "Stinger prompt on the page; take attendance"),
        ("Vocabulary Review + Quiz", 15, "Graded: review the term list, then the Schoology vocab quiz"),
        ("BrainBuffet Module Work", 48, "Self-paced videos, following along in the app"),
        ("Save & Wrap-Up", 5, "Save, back up, log out")],
 "F3": [("Bell Ringer / Stinger", 10, "Stinger prompt on the page; take attendance"),
        ("Pace Check", 5, "Students find today's pace goal"),
        ("Module Worksheet", 25, "Graded: the module's worksheet"),
        ("BrainBuffet Module Work", 33, "Self-paced videos, following along in the app"),
        ("Submit & Wrap-Up", 5, "Submit the worksheet, save, back up")],
 "F4": [("Bell Ringer / Stinger", 10, "Stinger prompt on the page; take attendance"),
        ("Pace Check", 5, "Students find today's pace goal"),
        ("BrainBuffet Module Work", 55, "Self-paced videos, following along in the app"),
        ("Stinger Sheet Check", 8, "Graded: the sub checks each student's Stinger Response Sheet")],
 "S":  [("Bell Ringer / Stinger", 10, "Stinger prompt on the page; take attendance"),
        ("Pace Check", 5, "Students check the finished-product checklist"),
        ("Finish the Module Project", 58, "Finish, export and polish the module's final product"),
        ("Submit", 5, "Graded: submit the finished product in Schoology")],
}

def timing_lines(kind):
    out = ["  timing:"]
    for seg, m, note in TIMING[kind]:
        out += [f"    - segment: {q(seg)}", f"      minutes: {m}", f"      note: {q(note)}"]
    assert sum(t[1] for t in TIMING[kind]) == 78
    return out

def seven(kind, mod, c, unit, mod_no, pace):
    graded = {"F1": "the Pace Check Exit Ticket", "F2": "the vocabulary quiz", "F3": "the module worksheet",
              "F4": "the Stinger Sheet Check", "S": "the finished module product"}[kind]
    return {
     "organization": f"The page lists today's videos, their lengths and one pace goal, so every student knows exactly where to stop. Graded today: {graded}.",
     "connection": f"Continues BrainBuffet {c['app']} Module {mod_no} ({mod['name']}) from the last class; today's stinger ties the module's ideas to something students already know.",
     "collaboration": "Stinger share-and-copy with a neighbor; students who are ahead help a neighbor find their place in a video before starting the extension.",
     "summarization": {"F1": "The exit ticket: last video finished, a screenshot, and one skill learned.",
                       "F2": "The vocab quiz summarizes the module's terms.",
                       "F3": "The worksheet applies the module's skills on a fresh file.",
                       "F4": "Students review their unit's stingers while the sheet is checked.",
                       "S": "Students submit the finished product and check it against the checklist."}[kind],
    }

def lesson_page(c, unit, mod_no, mod, kind, alloc, days):
    num = f"{unit}.{kind[1]}" if kind != "S" else f"S{unit}"
    part = {"F1": 1, "F2": 2, "F3": 3, "F4": 4}.get(kind)
    parent = f"{c['top']} | Unit {unit}"
    if kind == "S":
        title = f"S | {unit} | {mod['product_title']}"
    else:
        label = {"F1": "Exit Ticket", "F2": "Vocabulary Quiz", "F3": "Module Worksheet", "F4": "Stinger Sheet Check"}[kind]
        title = f"{num} | {mod['short']}, Part {part}: {label}"
    key = kind if kind != "S" else None
    st = seven(kind, mod, c, unit, mod_no, None)
    # pace goal
    if kind == "S":
        s_keys = [d for d, _ in days if d.startswith("S")]
        s_vids = [v for k in s_keys for v in alloc.get(k, [])]
        target = f"finish {mod['product']}"
    else:
        vids = alloc.get(kind, [])
        last = vids[-1] if vids else None
        target = (f"finish video {last[0]} ({last[3]})" if last else "catch up on any unfinished videos, then start the extension challenge")
    tgt = {"F1": f"follow BrainBuffet {c['app']} Module {mod_no} at pace and {target}, then report progress on an exit ticket",
           "F2": f"define this module's key terms by scoring on the vocabulary quiz, and {target}",
           "F3": f"apply Module {mod_no}'s skills by completing the module worksheet, and {target}",
           "F4": f"{target}, and show a complete Stinger Response Sheet for the unit so far",
           "S": f"{target}"}[kind]
    evidence = {"F1": "The Pace Check Exit Ticket in Schoology: last video finished, a screenshot of it, and a 3-sentence reflection.",
                "F2": "The Schoology vocabulary quiz score (auto-graded).",
                "F3": "The submitted module worksheet.",
                "F4": "The Stinger Response Sheet: every stinger this unit answered, shared, copied and synthesized.",
                "S": f"The finished product submitted in Schoology: {mod['product']}."}[kind]
    acp_note = " (BrainBuffet's mapping; it uses the older Illustrator objective numbers)" if c["app"] == "Illustrator" else ""
    L = ["  course: " + q(c["key"]), f"  unit: {unit}", f"  number: {q(num)}"]
    if kind == "S":
        L.append("  is_summative: true")
    L.append(f"  standard: {q('ACP ' + mod['acp'] + acp_note)}")
    if kind == "F2":
        L += ["  vocab:", f"    - vocab/fmla-{'ai' if c['app']=='Illustrator' else 'pr'}-m{mod_no}.md"]
    L.append(folded("source", f"FMLA plan: this unit follows BrainBuffet {c['app']} Module {mod_no}, {mod['name']}, in GMetrix SMS, instead of the regular {c['course_name']} Unit {unit} lessons. Video list, lengths and objective mapping come from BrainBuffet's teacher lesson plan."))
    if kind == "S":
        lo, hi = s_days(unit)
        span = f"{lo}" if lo == hi else f"{lo}–{hi}"
        L.append(folded("purpose_note", f"The S block is {span} class periods per section on the A/B calendar. Students finish and submit {mod['product']}. Students who finish early do the extension challenge."))
    L += timing_lines(kind if kind != "S" else "S")
    L += ["  the_seven:", f"    organization: {q(st['organization'])}", f"    connection: {q(st['connection'])}",
          f"    target: {q(tgt)}", f"    collaboration: {q(st['collaboration'])}", f"    evidence: {q(evidence)}",
          f"    summarization: {q(st['summarization'])}"]
    if kind == "F1":
        L.append("  exit_ticket: fmla-pace")
    files = "your BrainBuffet project file" if c["app"] == "Illustrator" else "your .prproj project file"
    L += ["  organize:", "    binder:", "      - \"your Stinger Response Sheet\"", "    drive:",
          f"      - item: {q(files)}", "        folder: \"Project Files\""]
    if kind == "S":
        L += ["      - item: \"your exported finished product\"", "        folder: \"Exports\""]
    else:
        L += ["  organize_grading:", f"    plus: {q('the project file is saved and backed up, and the student is at or past today’s pace goal')}",
              f"    minus: {q('no saved project file, or more than one class behind the pace goal')}"]
    L += ["  differentiation:",
          f"    iep504: {q('Turn on video captions and transcripts; the pace goal can stop one video earlier with the remaining video moved to the next class; print the page’s video table to check off.')}",
          f"    ell: {q('Captions and full transcripts are available on every BrainBuffet video; the vocab list with definitions stays open in a second tab; stinger sentence frame: I think ___ because ___.')}",
          f"    gt: {q('Finish today’s videos, then start the extension challenge: ' + mod['ext'])}",
          "  materials:",
          f"    - {q('Lab Mac with GMetrix SMS and ' + c['app'])}",
          f"    - {q('BrainBuffet ' + c['app'] + ' Module ' + str(mod_no) + ' (' + mod['name'] + ')')}",
          "    - \"Headphones\"", "    - \"Stinger Response Sheet\""]
    notes = sub_notes(c, kind, mod, mod_no, unit)
    L.append(folded("notes", notes))
    body = student_body(c, unit, mod_no, mod, kind, alloc, days, title)
    slug = f"{unit}_{kind[1]}" if kind != "S" else f"s{unit}"
    write(f"{c['folder']}/fmla{unit}/{slug}.md", front(title, parent, c["top"], L) + body)
    teacher_page(c["folder"], unit, slug, title, parent, c["top"])
    return title, slug

def sub_notes(c, kind, mod, mod_no, unit):
    base = ("For the sub: project this page, read the stinger aloud, and take attendance. Students work at "
            "their own pace in BrainBuffet; circulate and check that each student's screen shows the video "
            "named in today's pace goal or later. ")
    extra = {
     "F1": "In the last 5 minutes, students post the Pace Check Exit Ticket in Schoology (screenshot + last video + reflection). ",
     "F2": "Open the unit's Schoology vocabulary quiz at the start of the quiz block and close it after 15 minutes. ",
     "F3": f"The worksheet is {mod.get('worksheet', 'the three Critical Thinking questions in the ' + mod.get('handbook', 'module handbook'))}. Collect it in Schoology at the end of class. ",
     "F4": "In the last 8 minutes, walk the room and mark each Stinger Response Sheet on the check system: ✓ every stinger this unit is there with a 3-sentence answer, a copied partner answer and a synthesis; ✓+ answers go beyond 3 sentences; ✓− missing entries. Record marks on the roster. ",
     "S": f"Students submit {mod['product']} in Schoology on the last S day. Teacher grading (on return): {mod['rubric']} ",
    }[kind]
    return base + extra + "Answer keys and BrainBuffet's finished example files stay with the teacher's resources and are not posted."

def student_body(c, unit, mod_no, mod, kind, alloc, days, title):
    b = [f"# {title}", ""]
    graded = {"F1": "**Exit Ticket.** Post your Pace Check Exit Ticket in Schoology at the end of class.",
              "F2": "**Vocabulary Quiz.** Review the key terms below, then take the Schoology vocabulary quiz.",
              "F3": "**Module Worksheet.** Complete and submit this module's worksheet.",
              "F4": "**Stinger Sheet Check.** Your Stinger Response Sheet for this unit gets checked at the end of class.",
              "S": f"**Finished Product.** Submit {mod['product']} in Schoology."}[kind]
    b += ["{: .highlight }", f"Today's graded assignment: {graded}", ""]
    b += ["## Today's Plan", "", "| Time | What you do |", "|---|---|"]
    b += [f"| {m} min | {seg} |" for seg, m, _ in TIMING[kind if kind != "S" else "S"]]
    sk = mod["stingers"][{"F1": 0, "F2": 1, "F3": 2, "F4": 3, "S": 4}[kind]]
    b += ["", "## Bell Ringer: Stinger (~10 min)", "", "{: .discussion }", sk, "", STINGER, ""]
    # pace
    if kind == "S":
        b += ["## Stay on Pace", ""]
        s_keys = [d for d, _ in days if d.startswith("S")]
        s_vids = [v for k in s_keys for v in alloc.get(k, [])]
        lo, hi = s_days(unit)
        if s_vids:
            goals = [f"**S day {k[1:]}:** finish video {alloc[k][-1][0]} ({alloc[k][-1][3]})." for k in s_keys if alloc.get(k)]
            b += ["{: .important }", " ".join(goals) + " **The rest of the S days:** finish, export and submit your project.", "",
                  video_table(s_vids), ""]
        else:
            b += ["{: .important }", "All of this module's videos should be done by now. **S days:** finish, export and submit your project, then start the extension challenge.", ""]
    else:
        vids = alloc.get(kind, [])
        b += ["## Stay on Pace", ""]
        if vids:
            last = vids[-1]
            mins = sum(v[1] for v in vids)
            b += ["{: .important }", f"**Pace goal:** by the end of class, finish **video {last[0]}: {last[3]}**.", "",
                  f"Today's videos ({mmss(mins)} of video):", "", video_table(vids), ""]
        else:
            b += ["{: .important }", "**Pace goal:** all of this module's videos should be finished. Catch up on anything you skipped, then work on the extension challenge.", ""]
    b += ["- **Behind?** Start at the first video you haven't finished and keep going. Watch with captions on and "
          "skip rewatching parts you already did.",
          f"- **Ahead?** Check your work against the video, then try the extension challenge: {mod['ext']}", ""]
    # kind-specific section
    if kind == "F2":
        voc = f"vocab/fmla-{'ai' if c['app']=='Illustrator' else 'pr'}-m{mod_no}.md"
        b += ["## Vocabulary Quiz (~15 min)", "",
              "Review these terms for a few minutes, then take the **Unit vocabulary quiz** in Schoology. It's auto-graded.", "",
              "### Key Terms", "", "{: .vocab }", f"{{% include {voc} %}}", ""]
    if kind == "F3":
        if c["app"] == "Illustrator":
            b += ["## Module Worksheet (~25 min)", "", f"Complete {mod['worksheet']}. Download it from the module's resources in BrainBuffet.", "",
                  "{: .note }", mod["worksheet_note"], "", "Save it in your **Project Files** folder and submit it (or a PDF of it) in Schoology before you leave.", ""]
        else:
            b += ["## Module Worksheet (~25 min)", "",
                  f"Open your **{mod['handbook']}** (in the module's resources in BrainBuffet) and answer its three **Critical Thinking** questions in Schoology. Write 3–5 sentences for each, and use at least one vocabulary term from this module in every answer.", "",
                  "*Stuck on how to start? Try: \"In this module I learned that ___. This matters because ___. For example, ___.\"*", ""]
    if kind == "F4":
        b += ["## Stinger Sheet Check (last ~8 min)", "",
              "Before the check, make sure every stinger from this unit is on your sheet, each with:", "",
              "- [ ] the question rewritten in your own words",
              "- [ ] your answer, at least 3 sentences",
              "- [ ] your neighbor's answer, copied",
              "- [ ] 1–2 sentences on what your answers had in common", ""]
    if kind == "S":
        b += ["## Finished Product Checklist", "", f"Your module project: **{mod['product']}**.", "",
              "- [ ] Every video in the module is finished",
              "- [ ] The project file is saved in **Project Files** and backed up to Drive",
              "- [ ] The final version is exported and saved in **Exports**",
              "- [ ] It's submitted in Schoology", ""]
    b += ["## BrainBuffet Work Time", "", start_steps(c, mod_no), ""]
    if kind == "F1":
        b += ["## Exit Ticket (last ~5 min)", "", "{% include lesson-parts/organize.html %}", "", "{% include exit-ticket/fmla-pace.md %}", ""]
    else:
        b += ["## Wrap-Up", "", "Save, back up your project file, and log out of GMetrix SMS.", "", "{% include lesson-parts/organize.html %}", ""]
    return "\n".join(b)

def unit_index(c, unit, mod_no, mod, alloc, days):
    dates, ndays = UNIT_DATES[unit]
    lo, hi = s_days(unit)
    total = sum(v[1] for v in mod["videos"])
    title = f"{c['top']} | Unit {unit}"
    fm = ["---", "layout: default", f"title: {q(title)}", f"nav_order: {unit}", f"parent: {q(c['top'])}",
          f"description: {q(c['unit_label'] + ' ' + str(mod_no) + ': ' + mod['name'])}", "has_children: true", "has_toc: false", "---"]
    b = [f"# Unit {unit} | {c['unit_label']} {mod_no}: {mod['name']} ({dates})", "",
         "## Introduction", "", mod["overview"], "",
         f"This unit replaces the regular {c['course_name']} Unit {unit} lessons while your teacher is on leave. Every class follows the same routine: a stinger, a pace check, then self-paced work in BrainBuffet {c['app']} Module {mod_no}.", "",
         "| | |", "|---|---|",
         f"| **BrainBuffet module** | {c['app']} Module {mod_no}: {mod['name']} ({len(mod['videos'])} videos, {mmss(total)} of video) |",
         f"| **Class periods** | {ndays} school days on the A/B calendar: 4 formative days plus {lo if lo == hi else f'{lo}–{hi}'} S days per section |",
         f"| **Finished product** | {mod['product']} |", "",
         "## Graded Assignments", "",
         "| Day | Graded assignment |", "|---|---|",
         f"| [{unit}.1]({unit}_1.md) | Exit Ticket (Pace Check) |",
         f"| [{unit}.2]({unit}_2.md) | Vocabulary Quiz |",
         f"| [{unit}.3]({unit}_3.md) | Module Worksheet |",
         f"| [{unit}.4]({unit}_4.md) | Stinger Sheet Check |",
         f"| [S{unit}](s{unit}.md) | Finished product: {mod['product_title']} |", "",
         "## Pacing Guide", "", "Where you should be at the end of each class:", "",
         "| Class | Videos | Finish by the end of class |", "|---|---|---|"]
    names = {"F1": f"{unit}.1", "F2": f"{unit}.2", "F3": f"{unit}.3", "F4": f"{unit}.4"}
    for k, _ in days:
        vs = alloc.get(k, [])
        if not vs:
            continue
        label = names.get(k, f"S{unit}, day {k[1:]}")
        b.append(f"| {label} | {vs[0][0]}–{vs[-1][0]} | {vs[-1][0]} {vs[-1][3]} |")
    for k in ("F1", "F2", "F3", "F4"):
        if not alloc.get(k) and k in dict(days):
            b.append(f"| {names[k]} | — | Catch up, then the extension challenge |")
    b.append(f"| S{unit}, last day(s) | — | Finish, export and submit the finished product |")
    b += ["", "## Calendar of Events for This Unit", "", f"{{% include calendar-of-events.html unit={unit} %}}", "",
          "## Unit Vocabulary", "", f"{{% include unit-vocab.html course=\"{c['key']}\" unit={unit} %}}", ""]
    write(f"{c['folder']}/fmla{unit}/index.md", "\n".join(fm) + "\n" + "\n".join(b))

def section_index(c):
    rows = []
    for unit, m in c["units"].items():
        mod = c["mods"][m]
        rows.append(f"| [Unit {unit}](fmla{unit}/index.md) | {UNIT_DATES[unit][0]} | {c['app']} Module {m}: {mod['name']} | {mod['product_title']} |")
    prep_extra = ("- Copy each module's footage (Modules 2–5, about 5 GB each) to `/Users/Shared/GMetrix` on every lab Mac. There's no Jamf, so this is by hand; one USB-C drive is fastest.\n"
                  "- Confirm Premiere Pro opens each module's starter project from that folder on one test Mac.\n"
                  if c["app"] == "Premiere Pro" else
                  "- Open each module's starter files on one test Mac to make sure fonts activate and files open.\n")
    b = ["---", "layout: default", f"title: {q(c['top'])}", f"nav_order: {c['nav']}", "has_children: true", "has_toc: false",
         f"description: {q('Units 3–6 of ' + c['course_name'] + ' while the teacher is on leave, run entirely through BrainBuffet in GMetrix.')}", "---",
         f"# {c['top']}: {c['course_name']} During Leave", "",
         f"While your teacher is on leave, {c['course_name']} Units 3–6 run entirely through the BrainBuffet {c['app']} course in GMetrix SMS. Each unit is one BrainBuffet module. These pages replace the regular unit pages for those units.", "",
         "| Unit | Dates | BrainBuffet module | Finished product |", "|---|---|---|---|"] + rows + [
         "", "## Every Class", "",
         "1. **Stinger (10 min).** Answer the day's stinger on your Stinger Response Sheet.",
         "2. **Pace check (5 min).** Find today's pace goal on the day's page: the video you should finish by the end of class.",
         "3. **BrainBuffet work.** Watch each video and do every step in " + c["app"] + " as you go.",
         "4. **Save and back up** before you leave.", "",
         "## How You're Graded", "",
         "| Day | Graded assignment |", "|---|---|",
         "| F .1 | Exit Ticket: your progress, a screenshot and one thing you learned |",
         "| F .2 | Vocabulary Quiz on the module's key terms (listed on the .2 page) |",
         "| F .3 | The module's worksheet |",
         "| F .4 | Stinger Sheet Check |",
         "| S | The finished product for the BrainBuffet module |", "",
         "## For the Substitute", "",
         "- Project the day's page (find it on the unit page or the calendar). Read the stinger aloud and take attendance.",
         "- Students work at their own pace. Circulate and check that each screen shows the pace-goal video or later.",
         "- Each day's teacher page (linked from the calendar) has the full plan and the grading notes. Add `-teacher` to the end of the page's address, for example `3_1-teacher.html`.",
         "- Students who are ahead do the extension challenge listed on the page; they don't start the next module early.", "",
         "## Before Leave (teacher checklist)", "",
         "- Build each unit's Schoology vocabulary quiz from the **Download Schoology Vocab Quiz (QTI)** button on the unit page.",
         "- Post the exit ticket, worksheet and finished-product assignments in Schoology for each unit.",
         "- Print a class set of Stinger Response Sheets.", prep_extra]
    write(f"{c['folder']}/index.md", "\n".join(b))

def vocab_include(app_key, mod_no, mod):
    lines = []
    for term, d in sorted(mod["vocab"], key=lambda x: x[0].lower()):
        lines += [f"**{term}**", f": {d}", ""]
    write(f"_includes/vocab/fmla-{app_key}-m{mod_no}.md", "\n".join(lines).rstrip() + "\n")

def exit_tickets():
    write("_includes/exit-ticket/fmla-pace.md",
"""📤 **Exit Ticket: Pace Check.** In the discussion board below, post:

* the **number and title of the last video you finished** today,
* a **screenshot** of your work at that point (⌘ Command + Shift + 3), and
* **at least 3 sentences (aim for 5)**: one skill you learned today, how you used it in your file,
  and whether you're ahead of, on, or behind today's pace goal.

*Stuck on how to start? Try: "I finished video ___. Today I learned how to ___. I used it to ___.
I'm ___ the pace goal because ___."*
""")
    write("_includes/exit-ticket/fmla-pace-teacher.md",
"""**Exit Ticket: Pace Check (FMLA units).** In the last 5 minutes, students post to the discussion
board the last BrainBuffet video they finished, a screenshot of their work at that point, and at
least 3 sentences (aim for 5) on one skill they learned, how they used it, and where they are
against the day's pace goal. Grade with the check system (see Resources > Rubrics): ✓ for all
three parts, ✓+ for a reflection that names a specific tool or setting and shows the student at or
past the pace goal, ✓− for a missing screenshot or a one-line reflection. Use the posts to see who
is falling behind before the S days.
""")

def main():
    exit_tickets()
    for cid, c in COURSES.items():
        section_index(c)
        for unit, m in c["units"].items():
            mod = c["mods"][m]
            vocab_include("ai" if cid == "fdd" else "pr", m, mod)
            days = plan_days(cid, unit, mod)
            alloc = allocate(mod["videos"], days)
            assert sum(len(v) for v in alloc.values()) == len(mod["videos"])
            unit_index(c, unit, m, mod, alloc, days)
            for kind in ("F1", "F2", "F3", "F4", "S"):
                lesson_page(c, unit, m, mod, kind, alloc, days)
            print(cid, unit, {k: f"{v[0][0]}-{v[-1][0]}" if v else "-" for k, v in alloc.items()})

if __name__ == "__main__":
    main()
