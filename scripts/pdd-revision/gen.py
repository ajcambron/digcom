#!/usr/bin/env python3
"""Generate the PDD revision draft into <repo>/processes-revision/ (originals in processes/ untouched)."""
import json, os, sys, textwrap
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from units import UNITS, DRIVE_MAIN, DRIVE_DIDACT
from lessons_a import LESSONS_A
from lessons_b import LESSONS_B
from lessons_c import LESSONS_C
from summatives import SUMMATIVES
from matrix import ACP, COMP, EX, EX_PLACEMENT
from patches import P

REPO = sys.argv[1]
OUT = os.path.join(REPO, "processes-revision")
TOP = "PDD Revision (Draft)"
LESSONS = LESSONS_A + LESSONS_B + LESSONS_C
ETNAME = {1: "Stoplight", 2: "Glow & Grow", 3: "Emoji Meter", 4: "3-2-1"}
for _L in LESSONS + SUMMATIVES:
    _L.update(P.get(_L["n"], {}))
for _u in range(1, 10):
    for _pos, _L in enumerate([x for x in LESSONS if int(x["n"].split(".")[0]) == _u], 1):
        if isinstance(_L.get("et", _pos), str):
            continue
        _et = ETNAME[_L.get("et", _pos)]
        if len(_L["summ"]) < 60:
            _L["summ"] = f"{_et} exit ticket on the prompt: \"{_L['refl']}\""
        if len(_L["evid"]) < 45 or _L["evid"].split()[0] in ("Stoplight", "Glow", "Emoji", "3-2-1"):
            base = ("The saved " + _L["files"][0][0].replace("your ", "")) if _L.get("files") else "Today's binder work"
            _L["evid"] = f"{base}, checked against the Organize criteria (✓+ when {_L['plus']}), plus the {_et} exit ticket."
UNIT = {u["n"]: u for u in UNITS}
STATUS_LABEL = {"EX": "EXISTING", "EDIT": "EXISTING, LIGHT EDIT", "NEW": "NEW"}

def q(s):
    return json.dumps(s, ensure_ascii=False)

def folded(key, text, indent):
    pad = " " * indent
    lines = textwrap.wrap(text, 96 - indent - 2, break_on_hyphens=False, break_long_words=False) or [""]
    return f"{pad}{key}: >\n" + "\n".join(f"{pad}  {l}" for l in lines) + "\n"

def write(path, content):
    path = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

def unit_of(n):
    return int(n.split(".")[0]) if not n.startswith("S") else int(n[1:])

def slug(n):
    return n.replace(".", "_").lower()

def drive_note(L):
    names = L.get("drive") or []
    if not names:
        return ""
    didact = any(("Didact" in d) or ("Classroom in a Book" in d) for d in names)
    link = DRIVE_DIDACT if didact else DRIVE_MAIN
    where = "Photoshop tutorial folder" if didact else "Processes of Digital Production"
    return f" Existing materials (unchanged, in Drive's [{where}]({link})): " + "; ".join(names) + "."

def comp_str(ids):
    return ", ".join(ids) if ids else "None directly"

def standard(L):
    if not L["acp"]:
        return "N/A—diagnostic baseline day; no new ACP content introduced"
    s = "ACP " + ", ".join(L["acp"])
    if L.get("comp"):
        s += " · Competition: " + ", ".join(L["comp"])
    return s

def banner(L, kind="lesson"):
    st = L["st"]
    ex = ", ".join(f"{e} {EX[e][0]}" for e in L.get("ex", []))
    if st == "NEW":
        body = f"**NEW {kind} (stub).** No existing PDD {kind} covers this. Written for the draft revision; materials marked \"Stub\" in the teacher notes still need to be built."
        return "{: .highlight }\n" + body + "\n"
    word = "lightly edited" if st == "EDIT" else "reordered, content unchanged"
    return "{: .note }\n" + f"**Existing {kind}, {word}.** From the current PDD course: {ex}. Draft revision page; the original files are untouched.\n"

def gm_note(u, L, pos):
    if u == 1:
        return None
    if u == 2:
        return "BrainBuffet Photoshop Module 1 (Crash Course)"
    return UNIT[u]["gm"]

# ---------------------------------------------------------------- formative pages
def formative(L, pos):
    u = unit_of(L["n"])
    et = L.get("et", pos)
    fm = ["---", "layout: default", f"title: {q(L['n'] + ' | ' + L['title'] + (' (NEW)' if L['st']=='NEW' else ''))}",
          f"parent: {q('PDD Draft | Unit ' + str(u))}", f"grandparent: {q(TOP)}", "nav_exclude: true", "search_exclude: true",
          "lesson:", "  course: PDD", f"  unit: {u}", f"  number: {q(L['n'])}", f"  standard: {q(standard(L))}"]
    fm.append(folded("source", L["source"] + drive_note(L), 2).rstrip("\n"))
    fm.append("  timing:")
    if L.get("special") == "pretest":
        segs = [("Bell Ringer / Hook", 10, "Digital stinger: " + L["bell"]),
                ("GMetrix SMS Login", 10, "Open GMetrix SMS, Login with Google (school account), redeem the class code from the Schoology homepage"),
                ("Pre-Launch Setup", 10, "Open Photoshop in Rosetta from Creative Cloud, confirm the GMetrix extension, quit; then Delete Test Resource Archive, Install Photoshop Plugin, Reinstall Workspace Files (teacher enters the admin password at each machine)"),
                ("ACP Pre-Test", 35, "Launch the Photoshop practice exam from GMetrix SMS and complete it under quiet, test-like conditions"),
                ("Post Results & Reflect", 8, "Screenshot the score/results screen and submit it"),
                ("Exit Ticket / Wrap-Up", 5, "Post score + screenshot + reflection (custom pre-test exit ticket)")]
    elif u == 1:
        segs = [("Bell Ringer / Hook", 10, "Paper stinger: " + L["bell"]),
                ("Direct Instruction", 12, L["di_note"]),
                ("Guided Practice + Shoot", 50, L["gp_note"] + " (no GMetrix in Unit 1; cameras go out once and come back once)"),
                ("Exit Ticket / Wrap-Up", 6, f"Cameras back, cards checked, Exit Ticket {et}")]
    else:
        segs = [("Bell Ringer / Hook", 10, "Digital stinger: " + L["bell"]),
                ("Direct Instruction", 10, L["di_note"]),
                ("Guided Practice", 23, L["gp_note"]),
                ("GMetrix/BrainBuffet Self-Guided Strand", 30, gm_note(u, L, pos)),
                ("Exit Ticket / Wrap-Up", 5, f"Save/submit, Exit Ticket {et}")]
    assert sum(s[1] for s in segs) == 78, L["n"]
    for name, m, note in segs:
        fm += [f"    - segment: {q(name)}", f"      minutes: {m}", f"      note: {q(note)}"]
    fm += ["  the_seven:", f"    organization: {q(L['org'])}", f"    connection: {q(L['conn'])}",
           f"    target: {q(L['target'])}", f"    collaboration: {q(L['collab'])}",
           f"    evidence: {q(L['evid'])}", f"    summarization: {q(L['summ'])}",
           f"  exit_ticket: {et}"]
    fm += organize_fm(L)
    if L.get("plus"):
        fm += ["  organize_grading:", f"    plus: {q(L['plus'])}", f"    minus: {q(L['minus'])}"]
    fm += ["  differentiation:", f"    iep504: {q(L['iep'])}", f"    ell: {q(L['ell'])}", f"    gt: {q(L['gt'])}", "  materials:"]
    fm += [f"    - {q(m)}" for m in L["mats"]]
    notes = L.get("notes", "")
    if L.get("track"):
        notes = (notes + " " if notes else "") + "Competition-track enrichment: " + L["track"]
    if notes:
        fm.append(folded("notes", notes, 2).rstrip("\n"))
    fm.append("---")
    body = [f"# {L['n']} | {L['title']}", "", banner(L), L["intro"], ""]
    if L.get("special") == "pretest":
        body.append(PRETEST_BODY)
    else:
        mins = (12, 50, 6) if u == 1 else (10, 23, 5)
        body += ["## Bell Ringer / Hook (~10 min)", "", "{: .discussion }", L["bell"], "",
                 f"## Direct Instruction (~{mins[0]} min)", "", L["di"], "", f"> \"{L['cue']}\"", "",
                 "**Scaffolded questions. Cold-call through all three:**", "",
                 f"> **Recall:** \"{L['q'][0]}\"", "", f"> **Analysis:** \"{L['q'][1]}\"", "",
                 f"> **Synthesis/Extension:** \"{L['q'][2]}\"", "",
                 f"## Guided Practice{' & Shoot' if u == 1 else ''} (~{mins[1]} min)", ""]
        body += [f"{i}. {s}" for i, s in enumerate(L["gp"], 1)]
        body += ["", "{: .discussion }", L["disc"], ""]
        if u != 1:
            body += ["## GMetrix/BrainBuffet (~30 min)", "", strand_text(u), ""]
        if L.get("track"):
            body += ["{: .important }", f"**Competition track (optional enrichment):** {L['track']}", ""]
        body += [f"## Exit Ticket / Wrap-Up (~{mins[2]} min)", "", "{: .reflection }", L["refl"], "",
                 "{% include lesson-parts/organize.html %}", "", f"{{% include exit-ticket/{et}.md %}}", ""]
    write(f"pdd{u}/{slug(L['n'])}.md", "\n".join(fm) + "\n" + "\n".join(body))
    teacher(L, u)

def organize_fm(L):
    out = ["  organize:"]
    if L.get("binder"):
        out.append("    binder:")
        out += [f"      - {q(b)}" for b in L["binder"]]
    if L.get("files"):
        out.append("    drive:")
        for item, folder in L["files"]:
            out += [f"      - item: {q(item)}", f"        folder: {q(folder)}"]
    return out

def strand_text(u):
    if u == 2:
        return ("Log in and work in **BrainBuffet Photoshop Module 1: Crash Course**, starting where you left off. "
                "Redo Pre-Launch Setup from [2.1](2_1.md#pre-launch-setup) first if this is a new log-on.")
    return f"Log in and keep working in your BrainBuffet module: {UNIT[u]['gm']} Start wherever you left off."

def teacher(L, u):
    t = (L["n"] + " | " + L["title"]) if not L["n"].startswith("S") else f"S | {u} | {L['title']}"
    fm = ["---", "layout: default", f"title: {q(t + ' (Teacher)')}", f"parent: {q('PDD Draft | Unit ' + str(u))}",
          f"grandparent: {q(TOP)}", "nav_exclude: true", "search_exclude: true", "has_toc: false", "---",
          f"# {t} | Teacher Plan", "", "{% include teacher-plan.html %}", ""]
    write(f"pdd{u}/{slug(L['n'])}-teacher.md", "\n".join(fm))

PRETEST_BODY = r"""## Bell Ringer / Hook (~10 min)

{: .discussion }
Before a coach starts a season of training, they usually time every athlete once, without coaching
anything yet. Why would they do that? What does that first time trial tell them?

## GMetrix SMS Login (~10 min)

> "Every ACP course this year runs alongside GMetrix/BrainBuffet. Today's the day we get you
> into it."

1. **Open GMetrix SMS** from the Applications folder (**GmetrixSMSe**).
2. **Click Login with Google** and sign in with your **school Google account**. Don't create a
 new account, and don't use a personal Google account.
3. **Find our class code on Schoology:** open our class's Schoology homepage and scroll down to
 **How to Contact Me**. The code is on the **Gmetrix:** line.
4. **Redeem the code:** in GMetrix SMS, click **Redeem Code** in the left sidebar, type the code
 exactly (including the dash), and click **Redeem Code**. You only do this once.

{: .highlight }
If Login with Google won't take your school account, flag the teacher right away instead of
troubleshooting alone.

## Pre-Launch Setup (~10 min)

Do these steps **every time you log on to a computer**, not just today. They get Photoshop and
GMetrix's plugin ready so the exam actually opens.

{: .important }
**Be patient.** Steps 4, 5, and 6 each ask for an **administrator password**. Raise your hand and
wait: your teacher has to type it on every computer in the room, one at a time. Don't click
Cancel, and don't try to guess a password.

1. **Open Photoshop in Rosetta:** open the **Creative Cloud** app, go to **Apps → Installed
 apps**, click **••• (More actions)** next to Photoshop's **Open** button, and choose **Open in
 Rosetta**.
2. **Confirm the GMetrix extension loaded:** in Photoshop, go to **Window → Extensions (Legacy)** (some
 versions just say **Extensions**) and check that GMetrix is listed. If it isn't, tell
 your teacher.
3. **Quit Photoshop** (**⌘ Command + Q**).
4. **Delete the test resource archive:** in GMetrix SMS, open **Settings**, click the **Tasks**
 tab, and click **Execute** next to **Delete Test Resource Archive**.

   ![GMetrix SMS Tasks tab: Delete Test Resource Archive, with an Execute button]({{ '/assets/images/fdd2/gmetrix-tasks-delete-archive.png' | relative_url }})

5. **Install the Photoshop plugin:** click the **Plugins** tab, choose **Photoshop** in the left
 list, and click **Execute** next to **Install Photoshop Plugin**.
6. **Reinstall the workspace files:** on the same page, click **Execute** next to **Reinstall
 Photoshop Plugin Workspace Files**.

   ![GMetrix SMS Plugins tab, shown with Illustrator selected: Photoshop is in the same left-hand list, with the same Install Plugin and Reinstall Plugin Workspace Files rows]({{ '/assets/images/fdd2/gmetrix-plugins-illustrator.png' | relative_url }})

   *This screenshot shows Illustrator selected. Click **Photoshop** in the same list; its rows
   work the same way.*

## ACP Pre-Test (~35 min)

1. **Launch the Photoshop practice exam** from GMetrix SMS in Testing Mode. GMetrix opens
 Photoshop for you. This is separate from Module 1's regular lessons.
2. **Work quietly and independently.** This isn't graded on correctness, and you haven't been
 taught most of it yet, so guessing is expected. Answer everything you can reason through.
3. **Finish the whole pre-test** before moving on to anything else.

{: .highlight }
If the exam doesn't open properly (Photoshop opens but the GMetrix panel never shows up), quit
Photoshop (⌘Q), redo **Pre-Launch Setup** from step 1, then start the exam again from GMetrix SMS.

{: .discussion }
**Cold call check, once most students finish:** what's one question you genuinely had no idea
about? That's exactly what this test is for.

## Post Results & Reflect (~8 min)

1. **Find your results/score screen** once the pre-test submits.
2. **Take a screenshot** showing your score: press **⌘ Command + Shift + 3**. It saves to your
 Desktop.
3. **Move it to your Digital Design Drive folder**, in the Screenshots folder.

{: .highlight }
A low score today is not a bad grade. It's the whole point. Module 1 exists to teach you
everything this pre-test just asked about.

## Exit Ticket / Wrap-Up (~5 min)

{% include lesson-parts/organize.html %}

{% include exit-ticket/pdd2-1-score.md %}
"""

# ---------------------------------------------------------------- summatives
def summative(S):
    u = S["unit"]
    title = f"S | {u} | {S['title']}"
    fm = ["---", "layout: default", f"title: {q(title)}", f"parent: {q('PDD Draft | Unit ' + str(u))}",
          f"grandparent: {q(TOP)}", "nav_exclude: true", "search_exclude: true", "lesson:", "  course: PDD",
          f"  unit: {u}", f"  number: {q(S['n'])}", "  is_summative: true", f"  standard: {q(standard(S))}"]
    fm.append(folded("source", S["source"] + drive_note(S), 2).rstrip("\n"))
    purpose = S["purpose"] + " No GMetrix/BrainBuffet block today: project days use the full period for the project, the same rule FDD and ADD follow."
    fm.append(folded("purpose_note", purpose, 2).rstrip("\n"))
    fm += ["  timing:",
           "    - segment: \"Bell Ringer / Hook\"", "      minutes: 10", "      note: \"Digital stinger (still runs today—see F5/F6 below)\"",
           "    - segment: \"Project Briefing + Demo\"", "      minutes: 10", f"      note: {q(S['demo'])}",
           "    - segment: \"Project Work Time\"", "      minutes: 53", f"      note: {q(S['work'] + '—no GMetrix block today, the full period is project time')}",
           "    - segment: \"Save, Export & Submit\"", "      minutes: 5", "      note: \"File naming, export, portfolio submission\"",
           "  the_seven:", f"    organization: {q(S['org'])}", f"    connection: {q(S['conn'])}", f"    target: {q(S['target'])}",
           f"    collaboration: {q(S['collab'])}", f"    evidence: {q(S['evid'])}", f"    summarization: {q(S['summ'])}",
           "  formatives:",
           "    - label: \"F5—Cumulative Vocab Quiz\"",
           f"      description: {q('Schoology auto-graded quiz covering all of Unit ' + str(u) + chr(39) + 's vocabulary (once PDD vocab includes exist for ' + str(u) + '.1–' + str(u) + '.4).')}",
           "    - label: \"F6—Stinger Grade\"",
           "      description: \"compiled from this unit's bellringer responses, already collected across the 4 formative lessons—no new work required today, just recorded.\""]
    fm += organize_fm(S)
    fm += ["  differentiation:", f"    iep504: {q(S['iep'])}", f"    ell: {q(S['ell'])}", f"    gt: {q(S['gt'])}", "  materials:"]
    fm += [f"    - {q(m)}" for m in S["mats"]]
    if S.get("track"):
        fm.append(folded("notes", "Competition-track enrichment: " + S["track"], 2).rstrip("\n"))
    fm.append("---")
    body = [f"# {title}", "", banner(S, "project"),
            f"The culmination of this unit. You'll {S['target']}.", "",
            "## Project Briefing (~10 min)", "", f"{S['demo']}, then start your own.", "",
            "## Project Work Time (~53 min)", "", "### Deliverables checklist", ""]
    body += [f"- [ ] {d}" for d in S["deliver"]]
    body += ["", "{: .discussion }", f"**Check-in:** {S['collab']}", ""]
    if S.get("track"):
        body += ["{: .important }", f"**Competition track (optional enrichment):** {S['track']}", ""]
    body += ["## Save, Export & Submit (~5 min)", "", "{: .reflection }", S["summ"], "",
             "{% include portfolio.md %}", "", "{% include lesson-parts/organize.html %}", ""]
    write(f"pdd{u}/s{u}.md", "\n".join(fm) + "\n" + "\n".join(body))
    teacher(S, u)

# ---------------------------------------------------------------- unit pages
def lessons_in(u):
    return [L for L in LESSONS if unit_of(L["n"]) == u]

def summ_in(u):
    return next(S for S in SUMMATIVES if S["unit"] == u)

def tag(st):
    return {"NEW": "**NEW**", "EDIT": "existing, light edit", "EX": "existing"}[st]

def unit_page(U):
    u = U["n"]
    Ls, S = lessons_in(u), summ_in(u)
    new = [L["n"] for L in Ls if L["st"] == "NEW"]
    fm = ["---", "layout: default", f"title: {q('PDD Draft | Unit ' + str(u))}", f"nav_order: {u}", f"parent: {q(TOP)}",
          f"description: {q(U['desc'])}", "has_children: true", "has_toc: false", "nav_exclude: true", "search_exclude: true", "---"]
    b = [f"# Unit {u} | {U['title']} ({U['dates']})", "", DRAFT, "", "## Introduction", "", U["intro"], "",
         "## Unit at a Glance", "", "| | |", "|---|---|",
         f"| **Dates** | {U['dates']}: {U['days']} school days on the A/B calendar, about {U['periods']} class periods per section |",
         f"| **Exam objectives (ACP Photoshop)** | {U['acp']} |",
         f"| **Competition skills supported** | {U['comp']} |",
         f"| **Existing lessons used** | {U['existing']} |",
         f"| **NEW lessons** | {', '.join(new) if new else 'None'} |",
         f"| **Class periods** | 4 formative lessons (1 period each) + the S{u} project block (the rest of the unit) |",
         f"| **Assessment** | {U['assess']} |",
         f"| **GMetrix/BrainBuffet strand** | {U['gm']} |", "",
         "## Core vs. Competition Track", "",
         f"- **Core (everyone):** {U['core']}", f"- **Competition track (enrichment):** {U['track']}", "",
         "## Literacy & Numeracy", "", f"- **Literacy:** {U['literacy']}", f"- **Numeracy:** {U['numeracy']}", "",
         "## Learning Outcomes", "", "Upon successful completion of this unit, you will be able to:", ""]
    b += [f"- {o}" for o in U["outcomes"]]
    b += ["", "## Calendar of Events for This Unit", "", f"{{% include calendar-of-events.html unit={u} %}}", "", "## Lessons", ""]
    for L in Ls:
        b.append(f"- [{L['n']} – {L['title']}]({slug(L['n'])}.md) ({tag(L['st'])}). {', '.join(L['acp']) or 'Baseline pre-test'}")
    b.append(f"- [S{u} – {S['title']}](s{u}.md) ({tag(S['st'])}). Summative project")
    b += ["", "## Unit Vocabulary", "",
          "PDD vocabulary includes haven't been written yet. Once these lessons get `vocab:` lists, the combined list and the F5 quiz download appear here automatically.", "",
          f"{{% include unit-vocab.html course=\"PDD\" unit={u} %}}", ""]
    write(f"pdd{u}/index.md", "\n".join(fm) + "\n" + "\n".join(b))

DRAFT = ("{: .warning }\n**Draft revision (unlisted).** Part of the first-draft PDD course revision. The live "
         "[Processes of Digital Design](../../processes/index.md) pages and the Drive originals are unchanged. "
         "See the [revision overview](../index.md).")

# ---------------------------------------------------------------- unit 10, 11, 12
def domain_units(d):
    us = sorted({unit_of(L["n"]) for L in LESSONS + SUMMATIVES if any(a.startswith(d + ".") for a in L["acp"])})
    return ", ".join(str(x) for x in us)

def unit10():
    fm = ["---", "layout: default", "title: \"PDD Draft | Unit 10\"", "nav_order: 10", f"parent: {q(TOP)}",
          "description: \"No new content: targeted review, GMetrix practice exams, and the ACP Photoshop exam itself.\"",
          "has_children: false", "has_toc: true", "nav_exclude: true", "search_exclude: true", "---"]
    rows = [("10.1", "4/20–4/21", "**Diagnostic + Domains 1 & 2**", "Short diagnostic from the year's exit-ticket and vocab banks, then station review of Domain 1 (design industry, copyright, image terms) and Domain 2 (setup, interface, color)", "Group stations by each student's weakest domain on the diagnostic"),
            ("10.2", "4/22–4/23", "**Domains 3 & 4 + Practice Exam #1**", "Quick station review of layers/masks/adjustments and painting/type/AI tools, then GMetrix Photoshop practice exam #1 in **Training** mode", "Save each student's domain breakdown"),
            ("10.3", "4/26–4/27", "**Domains 5 & 6 + Targeted Re-Teach**", "Selections, retouching, transforms, filters; save/export. Small-group re-teach built from Practice Exam #1", "Group by this week's data, not the Day 1 diagnostic"),
            ("10.4", "4/28–4/29", "**Practice Exam #2 + Study Plan**", "Full GMetrix practice exam in **Testing** mode (timed), then a one-page personal 'double-check' list", "Low-stress, confidence-building"),
            ("S10", "4/30 (A) / 5/3 (B)", "**ACP Photoshop Certification Exam**", "Proctored Certiport exam. Makeups the next available day", "See the scheduling note below")]
    b = ["# Unit 10 | ACP Review, Practice Exams & Certification (Apr 20 – May 3, 2027)", "", DRAFT, "",
         "{: .highlight }", "Unit 10 introduces **no new content**. Every objective on the official ACP *Visual Design Using Adobe Photoshop* (2025, v26.x) list is covered in Units 2–9; see the [coverage matrix](../coverage-matrix.md). This unit gets students from \"has seen it\" to \"certifies on it.\"", "",
         "## Why this page doesn't follow the lesson schema", "",
         "Same reasoning as FDD Unit 10: review days have no new SWBAT or vocabulary, so one planning page replaces five thin lesson pages.", "",
         "## Unit at a Glance", "", "| | |", "|---|---|",
         "| **Dates** | Apr 20 – May 3, 2027: 10 school days, 5 meetings per section |",
         "| **Exam objectives** | All 6 ACP domains (review only) |",
         "| **Competition skills supported** | None directly. TSA and SkillsUSA prep continues in Units 11–12 |",
         "| **Existing lessons used** | Review pulls from every unit (see cross-reference) |",
         "| **Class periods** | 4 review meetings + 1 exam meeting per section |",
         "| **Assessment** | Two GMetrix practice exams (formative) and the ACP Photoshop certification exam |",
         "| **GMetrix/BrainBuffet strand** | BrainBuffet Photoshop Module 8 (Exam Prep, ~2 h, started as homework from S9) + GMetrix practice tests |", "",
         "## The 5 meetings (per section)", "", "| Calendar | Dates | Focus | Format | Notes |", "|---|---|---|---|---|"]
    b += [f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |" for r in rows]
    b += ["", "{: .important }",
          "**Scheduling note.** The goal is certification by **April 30**, but on the A/B calendar the S10 exam meeting falls on 4/30 for one section and **5/3** for the other. Options: (1) book a lab day for the second section on 4/30 (a pull-out or shared period), or (2) accept 5/3 for that section; it's still before AP testing (May 3–7 starts the same day, so check student AP conflicts). This draft assumes option 1.", "",
          "## ACP domain cross-reference", "", "| Domain | Pull review materials from PDD Units |", "|---|---|"]
    for d, name, _ in ACP:
        b.append(f"| {d}. {name} | {domain_units(d)} |")
    b += ["", "## Assessment", "",
          "- **Practice Exam #1 and #2:** recorded as formative scores (not averaged into the summative).",
          "- **ACP exam:** pass/fail from Certiport. Students who don't pass get a retake voucher plan per district policy.", "",
          "## Differentiation", "", "| Cohort | Modification |", "|---|---|",
          "| IEP/504 | Testing accommodations per plan (extended time is supported by Certiport with advance setup); review stations with printed step cards |",
          "| ELL/Multilingual | Certiport language options where available; picture vocabulary review deck |",
          "| Advanced/GT | Peer-coach a station; after passing, start Unit 11 competition prep early |", "",
          "## Materials", "", "- GMetrix SMS with Photoshop practice exams (Photoshop 26.11 in Rosetta)", "- Certiport exam vouchers and proctor login", "- Year's exit-ticket and vocab banks", ""]
    write("pdd10/index.md", "\n".join(fm) + "\n" + "\n".join(b))

def extra_unit(n, title, dates, desc, intro, rows, track):
    fm = ["---", "layout: default", f"title: \"PDD Draft | Unit {n}\"", f"nav_order: {n}", f"parent: {q(TOP)}",
          f"description: {q(desc)}", "has_children: false", "has_toc: true", "nav_exclude: true", "search_exclude: true", "---"]
    b = [f"# Unit {n} | {title} ({dates})", "", DRAFT, "", "## Introduction", "", intro, "", "{: .highlight }",
         "Nothing in this unit is ACP-tested. Outline only in this draft: full lesson pages come after the course plan is approved.", "",
         "## Outline", "", "| Lesson | Focus | Source |", "|---|---|---|"]
    b += [f"| {r[0]} | {r[1]} | {r[2]} |" for r in rows]
    b += ["", "## Core vs. Competition Track", "", f"- **Core (everyone):** {track[0]}", f"- **Competition track (enrichment):** {track[1]}", "",
          "## Calendar of Events for This Unit", "", f"{{% include calendar-of-events.html unit={n} %}}", ""]
    write(f"pdd{n}/index.md", "\n".join(fm) + "\n" + "\n".join(b))

# ---------------------------------------------------------------- coverage
ALLROWS = [(oid, lab, f"ACP {d}") for d, name, objs in ACP for oid, lab in objs] + \
          [(oid, lab, grp) for grp, objs in COMP for oid, lab in objs]

def rev_cover(oid):
    out = []
    for L in LESSONS + SUMMATIVES:
        if oid in L["acp"] or oid in L.get("comp", []):
            out.append(L["n"] + (" NEW" if L["st"] == "NEW" else ""))
    return out

def ex_cover(oid):
    return {e: v[2][oid] for e, v in EX.items() if oid in v[2]}

def status(oid):
    c = ex_cover(oid)
    if any(v == 2 for v in c.values()):
        return "covered"
    return "partial" if c else "gap"

def matrix_page():
    exids = list(EX)
    counts = {"covered": 0, "partial": 0, "gap": 0}
    for oid, _, _ in ALLROWS:
        counts[status(oid)] += 1
    fm = ["---", "layout: default", "title: \"PDD Revision: Coverage Matrix\"", f"parent: {q(TOP)}", "nav_order: 2",
          "nav_exclude: true", "search_exclude: true", "---"]
    h = ["# Coverage Matrix", "", DRAFT.replace("../../processes", "../processes").replace("../index.md", "index.md"), "",
         "Rows: the official ACP *Visual Design Using Adobe Photoshop* objectives (2025 exam, v26.x), then the TSA Photographic Technology and SkillsUSA Photography criteria. Columns: the 45 existing lessons and projects in the current PDD course (EX01–EX45, keyed below), then the revision lesson(s) that cover each row.", "",
         f"**{len(ALLROWS)} rows:** {counts['covered']} covered by an existing lesson, **{counts['partial']} partial** (touched but not taught), **{counts['gap']} gaps** (no existing coverage). Every row is covered in the revision; NEW lessons are marked.", "",
         "<div class=\"cm-legend\"><span class=\"cm-dot\">●</span> primary coverage &nbsp; <span class=\"cm-dot\">◐</span> partial / mentioned &nbsp; <span class=\"cm-swatch cm-gap\"></span> gap: no existing coverage &nbsp; <span class=\"cm-swatch cm-partial\"></span> partial only</div>", "",
         MATRIX_CSS, "<div class=\"cm-wrap\"><table class=\"cm\">", "<thead><tr><th class=\"cm-obj\">Objective / criterion</th>"]
    h[-1] += "".join(f"<th class=\"cm-ex\" title=\"{e}: {EX[e][0]}\"><span>{e[2:]}</span></th>" for e in exids)
    h[-1] += "<th class=\"cm-rev\">Revision coverage</th></tr></thead><tbody>"
    group = None
    for oid, lab, grp in ALLROWS:
        if grp != group:
            group = grp
            gname = grp
            if grp.startswith("ACP"):
                d = grp.split()[1]
                gname = f"ACP Domain {d}: " + next(n for dd, n, _ in ACP if dd == d)
            h.append(f"<tr class=\"cm-group\"><th colspan=\"{len(exids)+2}\">{gname}</th></tr>")
        st = status(oid)
        cov = ex_cover(oid)
        cells = "".join(f"<td>{'●' if cov.get(e)==2 else ('◐' if cov.get(e)==1 else '')}</td>" for e in exids)
        rev = ", ".join(f"<b>{r}</b>" if r.endswith("NEW") else r for r in rev_cover(oid))
        h.append(f"<tr class=\"cm-{st}\"><th class=\"cm-obj\"><b>{oid}</b> {lab}</th>{cells}<td class=\"cm-rev\">{rev}</td></tr>")
    h.append("</tbody></table></div>")
    h += ["", "## Gaps and partials, and what fills them", "", "| Row | Status | Filled in the revision by |", "|---|---|---|"]
    for oid, lab, grp in ALLROWS:
        st = status(oid)
        if st != "covered":
            h.append(f"| **{oid}** {lab} | {'**Gap**' if st=='gap' else 'Partial'} | {', '.join(rev_cover(oid))} |")
    h += ["", "## Existing-lesson key", "",
          "Inventory of the current PDD course (Drive folder *Processes of Digital Production*, plus the Didact/Classroom in a Book tutorials in the Photoshop folder). Period counts are estimates from the materials; most slide decks are image-only, so they were inventoried by title.", "",
          "| ID | Existing lesson / project | Est. periods | Revision placement |", "|---|---|---|---|"]
    for e in exids:
        h.append(f"| {e} | {EX[e][0]} | {EX[e][1]} | {EX_PLACEMENT[e]} |")
    write("coverage-matrix.md", "\n".join(fm) + "\n" + "\n".join(h) + "\n")
    return counts

MATRIX_CSS = """<style>
.cm-wrap{overflow:auto;max-height:80vh;border:1px solid #ccd;margin:1em 0}
table.cm{border-collapse:separate;border-spacing:0;font-size:12px;min-width:0;margin:0}
table.cm th,table.cm td{border-bottom:1px solid #e3e3ea;border-right:1px solid #eee;padding:2px 4px;text-align:center;min-width:0}
table.cm .cm-obj{text-align:left;position:sticky;left:0;background:#fff;min-width:260px;max-width:320px;font-weight:normal;z-index:1}
table.cm thead th{position:sticky;top:0;background:#f4f5fb;z-index:2}
table.cm thead th.cm-obj{z-index:3}
table.cm .cm-ex span{writing-mode:vertical-rl;transform:rotate(180deg);font-weight:600}
table.cm .cm-rev{text-align:left;min-width:150px;white-space:nowrap}
table.cm tr.cm-group th{background:#26318a;color:#fff;text-align:left;position:sticky;left:0}
table.cm tr.cm-gap th.cm-obj,table.cm tr.cm-gap td{background:#fde2e1}
table.cm tr.cm-partial th.cm-obj,table.cm tr.cm-partial td{background:#fff3cd}
.cm-legend{font-size:13px}.cm-swatch{display:inline-block;width:12px;height:12px;vertical-align:middle;border:1px solid #bbb}
.cm-swatch.cm-gap{background:#fde2e1}.cm-swatch.cm-partial{background:#fff3cd}
</style>"""

# ---------------------------------------------------------------- run
def main():
    for u in range(1, 10):
        for pos, L in enumerate(lessons_in(u), 1):
            formative(L, pos)
        summative(summ_in(u))
        unit_page(UNIT[u])
    unit10()
    extra_unit(11, "Photojournalism Profile & Nationals Prep", "May 4 – May 17, 2027",
               "Post-certification: the Teacher/Staff Profile feature story, plus TSA and SkillsUSA nationals prep.",
               "The first Extra Unit returns to the journalism side of the course with the Teacher/Staff Profile, the existing project that was moved out of Unit 3 because it is four to five periods of writing with no ACP coverage. Competition-track students prepare for TSA's semifinal (24-hour shoot, presentation, interview) and SkillsUSA nationals.",
               [("11.1", "Story structure (feature lead, nut graf, kicker)", "EX15 Story Structure deck"),
                ("11.2", "Quotes and the interview", "EX15 Quotes deck"),
                ("11.3", "Environmental portrait of the profile subject", "EX05 skills, Unit 4 lighting"),
                ("11.4", "Group write and edit", "EX15 Group write"),
                ("S11", "Published Teacher/Staff Profile (story + portrait)", "EX15")],
               ("Everyone writes and photographs a staff profile.", "TSA semifinal practice: a mock 24-hour shoot-and-edit prompt with tripod and off-camera flash, a 5-minute presentation, and a 5-minute interview; SkillsUSA mock written test and job interview."))
    extra_unit(12, "Portfolio Polish & Deconstructed Identity", "May 18 – Jun 4, 2027",
               "Post-certification: BrainBuffet's Deconstructed Identity project and a final web portfolio.",
               "The last unit is reflective: students finish BrainBuffet's Echo Hart client project if needed, complete Module 7 (Deconstructed Identity), and publish a final web portfolio of the year's best work.",
               [("12.1", "Echo Hart client project finish (BrainBuffet Module 6)", "BrainBuffet"),
                ("12.2", "Deconstructed Identity, part 1 (BrainBuffet Module 7)", "BrainBuffet"),
                ("12.3", "Deconstructed Identity, part 2", "BrainBuffet"),
                ("12.4", "Portfolio curation and reflection", "EX45 Google Sites portfolio"),
                ("S12", "Final web portfolio and year reflection", "EX45")],
               ("Everyone publishes a final portfolio page.", "SkillsUSA nationals (June) final prep; TSA nationals if qualified."))
    counts = matrix_page()
    import docs
    docs.scope(); docs.changelog(); docs.overview(counts); docs.exit_tickets(REPO)
    for oid, lab, grp in ALLROWS:
        assert rev_cover(oid), f"uncovered row {oid}"
    print("rows", len(ALLROWS), counts)
    print("lessons", len(LESSONS), "NEW", sum(L['st']=='NEW' for L in LESSONS))

if __name__ == "__main__":
    main()
