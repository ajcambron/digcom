# Overview, scope & sequence, change log, and the custom 2.1 exit ticket for the PDD revision.
import os
import gen
from gen import (UNIT, LESSONS, SUMMATIVES, EX, ACP, q, write, slug, lessons_in, summ_in, unit_of, TOP, DRAFT,
                 ALLROWS, status, rev_cover)

GMS = {1: "None (setup in 2.1)", 2: "Pre-test, then Module 1", 3: "Module 1", 4: "Module 1 (finish)", 5: "Module 2", 6: "Module 3",
       7: "Module 4", 8: "Module 4 finish, Module 5 start", 9: "Module 5 finish, Module 6 start; Module 8 as homework"}

def s_periods(u):
    return UNIT[u]["days"] / 2 - 4

def fmt(x):
    return str(int(x)) if x == int(x) else str(x)

TOP_DRAFT = DRAFT.replace("../../processes", "../processes").replace("../index.md", "index.md")

def scope():
    fm = ["---", "layout: default", "title: \"PDD Revision: Scope & Sequence\"", f"parent: {q(TOP)}", "nav_order: 1",
          "nav_exclude: true", "search_exclude: true", "---"]
    b = ["# Scope & Sequence: Processes of Digital Design (2026–27 draft)", "", TOP_DRAFT, "",
         "Built backward from the ACP Photoshop exam as its own Unit 10 (Apr 20 – May 3, 2027), on the same calendar math as FDD and ADD: Units 1–9 are 4 formative lessons + 1 summative block each, the A/B schedule gives each section half of each unit's school days, and Units 11–12 are post-certification Extra Units. Competition skills both events judge most (studio lighting, B&W, still life, macro, the Photoshop editing task) get a first, rudimentary pass in Units 1–4, before winter break.", "",
         "## Year at a glance", "",
         "| Unit | Dates | Periods per section (F + S) | Lessons (NEW in bold) | Summative | BrainBuffet strand |", "|---|---|---|---|---|---|"]
    for u in range(1, 10):
        U = UNIT[u]
        ls = ", ".join(f"**{L['n']} NEW**" if L["st"] == "NEW" else L["n"] for L in lessons_in(u))
        b.append(f"| [{u}. {U['title']}](pdd{u}/index.md) | {U['dates']} | 4 + {fmt(s_periods(u))} | {ls} | S{u} {summ_in(u)['title']} | {GMS[u]} |")
    b += ["| [10. ACP Review & Exam](pdd10/index.md) | Apr 20 – May 3, 2027 | 4 review + 1 exam | 10.1–10.4 review, practice exams | ACP Photoshop exam | Module 8 + GMetrix practice exams |",
          "| [11. Photojournalism Profile & Nationals Prep](pdd11/index.md) | May 4 – 17, 2027 | 4 + 1 | Teacher/Staff Profile (EX15) | Published profile | — |",
          "| [12. Portfolio Polish & Deconstructed Identity](pdd12/index.md) | May 18 – Jun 4, 2027 | 4 + 1 | BrainBuffet Modules 6–7, portfolio | Final web portfolio | Modules 6–7 |", "",
          f"**Totals, Units 1–9:** 36 formative lessons ({sum(L['st']=='NEW' for L in LESSONS)} NEW, "
          f"{sum(L['st']=='EDIT' for L in LESSONS)} existing with light edits, {sum(L['st']=='EX' for L in LESSONS)} existing unchanged) "
          f"and 9 summatives (0 NEW, {sum(S['st']=='EDIT' for S in SUMMATIVES)} with light edits). 44 of the 45 existing lessons/projects are used in Units 1–9 (several one-period decks and tutorials are merged into single lessons); EX15 moves to Unit 11 (see the [change log](change-log.md)).", "",
          "## Unit by unit", ""]
    for u in range(1, 10):
        U, S = UNIT[u], summ_in(u)
        b += [f"### Unit {u} | {U['title']} ({U['dates']})", "", U["intro"], "",
              "| | |", "|---|---|",
              f"| **Exam objectives** | {U['acp']} |", f"| **Competition skills** | {U['comp']} |",
              f"| **Existing lessons used** | {U['existing']} |",
              f"| **Class periods** | {fmt(UNIT[u]['days']/2)} per section: 4 formative + {fmt(s_periods(u))} for S{u} |",
              f"| **Assessment** | {U['assess']} |", f"| **GMetrix/BrainBuffet** | {U['gm']} |",
              f"| **Core (everyone)** | {U['core']} |", f"| **Competition track** | {U['track']} |",
              f"| **Literacy** | {U['literacy']} |", f"| **Numeracy** | {U['numeracy']} |", "",
              "| Lesson | Status | Existing source | ACP | Competition | Periods |", "|---|---|---|---|---|---|"]
        for L in lessons_in(u) + [S]:
            src = ", ".join(L["ex"]) if L["ex"] else "—"
            st = {"NEW": "**NEW**", "EDIT": "Existing, light edit", "EX": "Existing"}[L["st"]]
            per = fmt(s_periods(u)) if L["n"].startswith("S") else "1"
            name = f"S{u}" if L["n"].startswith("S") else L["n"]
            b.append(f"| [{name} {L['title']}](pdd{u}/{slug(L['n'])}.md) | {st} | {src} | {', '.join(L['acp']) or '—'} | {', '.join(L.get('comp', [])) or '—'} | {per} |")
        b.append("")
    b += ["### Unit 10 | ACP Review, Practice Exams & Certification", "",
          "No new content. Four review meetings per section (diagnostic, domain stations, two GMetrix practice exams, targeted re-teach) and the exam meeting. See [Unit 10](pdd10/index.md).", "",
          "### Units 11–12 | Extra Units", "",
          "Post-certification: the Teacher/Staff Profile (moved from the journalism unit), TSA and SkillsUSA nationals prep, BrainBuffet Modules 6–7, and the final web portfolio. Outline pages: [Unit 11](pdd11/index.md), [Unit 12](pdd12/index.md).", "",
          "## Period-budget flags", "",
          "| Item | Estimated need | Allotted | Plan |", "|---|---|---|---|",
          "| S1 Portrait Photography (EX05) | ~2 periods | 1 per section | Start the portrait shoot in the last 20 minutes of 1.4; S1 day is shooting the remaining frames and selecting. |",
          "| S6 Magazine Cover (EX31) | ~3 | 2.5 | Cover photo is shot as 6.2/6.4 homework or chosen from earlier units. |",
          "| Merged Didact tutorials (3.2, 5.3, 5.4, 8.2) | 2 tutorials each | 1 period | Teach the core steps of both in the 23-minute guided block; the remaining tutorial steps become early-finisher work. |",
          "| BrainBuffet Photoshop course | ~22 h of class time (Modules 1–6, 8) | ~17.5 h of strand time (Units 2–9) + Unit 10 | Module 6 (Echo Hart) finishes in Unit 12; Module 8 starts as homework during S9; Module 7 is Unit 12 enrichment. |", ""]
    write("scope-and-sequence.md", "\n".join(fm) + "\n" + "\n".join(b))

def changelog():
    fm = ["---", "layout: default", "title: \"PDD Revision: Change Log\"", f"parent: {q(TOP)}", "nav_order: 3",
          "nav_exclude: true", "search_exclude: true", "---"]
    b = ["# Change Log", "", TOP_DRAFT, "",
         "Compared with the existing PDD course (Drive folder *Processes of Digital Production*, the 2023 course outline, and the current syllabus's 8-unit list).", "",
         "## Structure", "", "| Change | Reason |", "|---|---|",
         "| 8 topic units → 9 core units + Unit 10 (ACP exam) + 2 Extra Units | Matches the FDD/ADD calendar math and puts the exam in its own unit with review and practice-exam time before it. |",
         "| Every unit is 4 formative lessons + 1 summative, with `lesson:` front matter and paired teacher pages | Same format as FDD and ADD, so teacher pages, exit tickets, the vocab quiz, and the calendar all work automatically. |",
         "| GMetrix/BrainBuffet strand added from Unit 2 on (30 min per formative lesson) | The current PDD course has no ACP practice structure; FDD and ADD do. |",
         "| Lighting, B&W, still life, and macro moved before winter break (Unit 4) | Competition skills both events judge are covered in rudimentary form before Christmas. |", "",
         "## Moved", "", "| Lesson | From | To | Reason |", "|---|---|---|---|",
         "| Double Exposure (EX16) | Art-photography unit | 6.2 | It depends on masks, blend modes, and clipping masks, which are now taught in 6.1. |",
         "| Teacher/Staff Profile (EX15) | Journalism unit | Unit 11 | 4–5 periods of writing with no ACP coverage; it fits after the exam, and it's a strong portfolio piece. |",
         "| Framing (EX07) | Its own lesson | 3.1 | Merged with Planning your Shoot and Good News Photo (each ~1 period of slides). |",
         "| Composition (EX09, two copies in the 2023 outline) | Units 1 and 4 | 1.4 | One lesson; the duplicate was dropped. |",
         "| Lighting, Shaping Light, Ansel Adams, Mood Shoot (EX17–EX20) | Later units | Unit 4 | Before winter break, for competition prep. |",
         "| Didact Lesson05 tutorials (EX21–EX27) | Scattered | Unit 5 | Grouped as one image-correction unit with Panorama as its summative. |",
         "| Light Painting (EX43) | Art photography | 8.3 | Pairs with the painting unit and gives a strong TSA student-choice image. |",
         "| Magnum Opus Portfolio (EX44) | Final project | S9 | Rebuilt to TSA's current 5-category format and finished before the exam. |", "",
         "## Edited (light edits to existing lessons)", "", "| Revision lesson | Existing source | What changed |", "|---|---|---|"]
    for L in LESSONS + SUMMATIVES:
        if L["st"] == "EDIT":
            what = L["source"].split("Light edit:", 1)[1].strip() if "Light edit:" in L["source"] else L["source"]
            n = f"S{L['unit']}" if L["n"].startswith("S") else L["n"]
            b.append(f"| {n} {L['title']} | {', '.join(L['ex'])} | {what} |")
    b += ["", "## Added (NEW lessons)", "", f"{sum(L['st']=='NEW' for L in LESSONS)} of 36 formative lessons; no NEW summatives.", "",
          "| Lesson | Why it's needed |", "|---|---|"]
    for L in LESSONS:
        if L["st"] == "NEW":
            b.append(f"| [{L['n']} {L['title']}](pdd{unit_of(L['n'])}/{slug(L['n'])}.md) | {L['source'].replace('NEW. ', '')} |")
    b += ["", "## Cut", "", "| Item | Reason |", "|---|---|",
          "| Duplicate Composition lesson (2023 outline, Unit 4) | Same content as Unit 1's; merged into 1.4. |",
          "| Lightroom as a requirement (Event Photography) | Not assumed on the lab Macs; Camera Raw does the same job and is ACP-tested (2.3.a). |",
          "| Typography Unit subfolder (C. Hess copy) | Overlaps Typographic Design 1 & 2 (EX30), which is kept as 6.4. Still in Drive if wanted for Unit 11–12 enrichment. |",
          "| PDP 1.1 Syllabus (2021) and the earlier 9-unit PDD draft in `_planning/2026-27-scope-and-sequence.md` | Superseded by this revision. Neither file was edited; update the planning doc once this draft is approved. |",
          "| Separate Paragraphs lesson (2023 outline) | Merged into 6.4 with the Character and Paragraph panels. |", ""]
    write("change-log.md", "\n".join(fm) + "\n" + "\n".join(b))

def overview(counts):
    fm = ["---", "layout: default", f"title: {q(TOP)}", "nav_order: 31", "nav_exclude: true", "search_exclude: true",
          "has_children: true", "has_toc: false",
          "description: \"First-draft revision of Processes of Digital Design, built backward from the ACP Photoshop exam, with SkillsUSA and TSA photography prep.\"", "---"]
    b = ["# Processes of Digital Design: Revision Draft 1", "",
         "{: .warning }", "**Unlisted draft.** Nothing here replaces the live [Processes of Digital Design](../processes/index.md) pages, which are unchanged, and nothing in Drive was edited. These pages are hidden from the site navigation and search.", "",
         "**Goal:** by April 30, 2027, students are prepared to (1) pass the Adobe Certified Professional exam in Visual Design Using Adobe Photoshop, (2) compete in SkillsUSA Photography, and (3) submit a TSA Photographic Technology portfolio. Not every student competes: each unit separates the core for everyone from optional competition-track enrichment.", "",
         "## Deliverables", "",
         f"1. [Coverage matrix](coverage-matrix.md): {len(ALLROWS)} rows (ACP objectives + TSA + SkillsUSA criteria) × 45 existing lessons. {counts['covered']} rows covered by an existing lesson, {counts['partial']} partial, {counts['gap']} gaps; every row is covered in the revision.",
         "2. [Scope & sequence](scope-and-sequence.md), unit by unit, with exam objectives, competition skills, existing lessons, class periods, assessment, core vs competition track, and literacy/numeracy.",
         "3. The draft course, in the build format (`lesson:` front matter, paired teacher pages, calendar, exit tickets):",
         ""]
    for u in range(1, 10):
        b.append(f"   - [Unit {u}: {UNIT[u]['title']}](pdd{u}/index.md)")
    b += ["   - [Unit 10: ACP Review, Practice Exams & Certification](pdd10/index.md)",
          "   - [Unit 11: Photojournalism Profile & Nationals Prep](pdd11/index.md)",
          "   - [Unit 12: Portfolio Polish & Deconstructed Identity](pdd12/index.md)",
          "4. [Change log](change-log.md): moved, edited, added, and cut, with reasons.", "",
          "## By the numbers", "",
          f"- **36 formative lessons:** {sum(L['st']=='EX' for L in LESSONS)} existing unchanged, {sum(L['st']=='EDIT' for L in LESSONS)} existing with light edits, **{sum(L['st']=='NEW' for L in LESSONS)} NEW** ({', '.join(L['n'] for L in LESSONS if L['st']=='NEW')}).",
          "- **9 summatives:** all existing projects, 0 NEW.",
          "- **NEW lesson stubs** say what's missing in their teacher notes (start files, station cards, a spec sheet).", "",
          "## Promoting the draft", "",
          "When it's approved: move `processes-revision/pddN/` into `processes/pddN/`, change `parent:` from \"PDD Draft | Unit N\" to \"PDD | Unit N\" and `grandparent:` to \"Processes of Digital Design\", and remove `nav_exclude`/`search_exclude` from student pages (teacher pages keep `nav_exclude: true`).", "",
          "## Assumptions", "",
          "1. **ACP objectives** are from the official *Visual Design Using Adobe Photoshop* exam objectives, 2025 exam version (Photoshop v26.x), the PDF in Drive. Adobe's and Certiport's sites were blocked from this session, so check for a newer version before the testing window.",
          "2. **SkillsUSA Photography** national technical standards are members-only (Pathful). The criteria K1–K12 were compiled from published state and national summaries; check them against the current national standards when you log in.",
          "3. **TSA Photographic Technology** rules are from the 2025 & 2026 high school guide in Drive (*TSA Rules 26*). The 2026–27 theme (\"Behind the Scenes\" per a web search) is unverified. TSA's honor statement bans generative AI, so 7.4's AI work is ACP-only.",
          "4. **Calendar:** the same `_data/calendar.yml` as FDD and ADD, A/B schedule. On that calendar the S10 exam meeting falls on 4/30 for one section and 5/3 for the other; the draft recommends testing both by 4/30.",
          "5. **Period estimates** for existing lessons come from the materials themselves (slide counts, tutorial length). Most decks are image-only, so they were inventoried by title.",
          "6. **Software:** Photoshop 26.11 (GMetrix's top supported version), run in Rosetta for GMetrix. Lightroom is not assumed; Camera Raw and Bridge replace it.",
          "7. **Equipment:** Canon Rebel (T6-class, APS-C, ~1.6 crop) DSLRs with 18–55 mm kit lenses, tripods, and the Godox X Pro-C / X1R-C / Canon 600EX-RT flash kits. No dedicated macro lens; 4.4 uses the kit lens at closest focus, and extension tubes are an optional purchase.",
          "8. **No Jamf:** practice files, Classroom in a Book files, and GMetrix files are copied by hand to `/Users/Shared/` on all 24 Macs (the same pattern ADD uses), with a master copy in Drive.",
          "9. **BrainBuffet Photoshop** needs about 22 hours of class time for Modules 1–6 and 8; the strand provides about 17.5 hours in Units 2–9. Module 6 finishes in Unit 12, Module 8 starts as homework during S9, and Module 7 is Unit 12 enrichment.",
          "10. **Vocabulary includes** (`_includes/vocab/pdd-*.md`) don't exist yet, so lessons have no `vocab:` lists and the F5 quiz button stays hidden until they're written.",
          "11. **Prints and mounting** (11×14 on 16×20) cost money, so they are competition-track only; everyone else submits digital.",
          "12. **Generative AI** in Photoshop is assumed enabled for student Adobe IDs; if the district disables it, 7.4 is a teacher demo.", ""]
    write("index.md", "\n".join(fm) + "\n" + "\n".join(b))

def exit_tickets(repo):
    d = os.path.join(repo, "_includes", "exit-ticket")
    open(os.path.join(d, "pdd2-1-score.md"), "w").write(
"""📤 **Exit Ticket: Pre-Test Score.** In the discussion board below, post:

* your **score**, exactly as it appears on the results screen,
* your **results screenshot** (attach the file you took with ⌘ Command + Shift + 3), and
* a reflection in **at least 3 sentences (aim for 5)**: which part of the exam felt most
  unfamiliar, and one Photoshop skill you want to learn first.

*Stuck on how to start? Try: "I scored ___. The part that felt most unfamiliar was ___ because
___. One skill I want to learn first is ___."*
""")
    open(os.path.join(d, "pdd2-1-score-teacher.md"), "w").write(
"""**Exit Ticket: Pre-Test Score (PDD 2.1 only).** In the last few minutes, have students post to the
discussion board their Photoshop practice-exam score as shown on the results screen, the results
screenshot attached, and a reflection of at least 3 sentences (aim for 5) naming the part of the
exam that felt most unfamiliar and one Photoshop skill they want to learn first. The score itself
is not graded; it's the class baseline. Grade with the check system (see Resources > Rubrics): ✓
for score + screenshot + an on-topic reflection meeting the sentence count, ✓+ for a reflection
that names a specific exam task or tool, ✓− for a missing score or screenshot, or a one-line
reflection. Then use the posts: record each score as the student's baseline before Module 1, and
note which unfamiliar areas come up most.
""")
