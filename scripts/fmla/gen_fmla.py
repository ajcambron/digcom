#!/usr/bin/env python3
"""Generate the FMLA FDD and FMLA ADD sections (Units 3-6): BrainBuffet-module pacing pages.

Run from the repo root:  python3 scripts/fmla/gen_fmla.py
Re-running overwrites fmla-fdd/, fmla-add/ and the fmla vocab/exit-ticket includes.

FDD follows FDD_PLAN (modules.py): about 1.5 BrainBuffet Illustrator modules per unit, with each
day's graded item set per unit. ADD runs one Premiere module per unit with a fixed pattern.
"""
import glob, json, os, sys, textwrap
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modules import AI, PR, ADD_UNITS, UNIT_DATES, AI_HOURS, FDD_PLAN, FDD_VOCAB, FORMATIVE_PTS

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

COURSES = {
 "fdd": dict(key="FMLA FDD", top="FMLA FDD", folder="fmla-fdd", nav=25, app="Illustrator", course_name="Foundations of Digital Design",
             mods=AI, unit_label="GMetrix Illustrator", vocab_prefix="ai", form_pts=FORMATIVE_PTS),
 "add": dict(key="FMLA ADD", top="FMLA ADD", folder="fmla-add", nav=45, app="Premiere Pro", course_name="Applications of Digital Design",
             mods=PR, unit_label="GMetrix Premiere", vocab_prefix="pr"),
}

# ---------------------------------------------------------------- per-type class structure (78 min)
TIMING = {
 "exit": [("Stinger", 10, "Today's stinger from the stinger deck; take attendance"),
          ("Pace Check", 5, "Students find today's pace goal and the first video they haven't finished"),
          ("BrainBuffet Module Work", 58, "Self-paced videos, following along in the app"),
          ("Exit Ticket", 5, "Graded: Pace Check Exit Ticket, posted in Schoology")],
 "vocab": [("Stinger", 10, "Today's stinger from the stinger deck; take attendance"),
           ("Vocabulary Review + Quiz", 15, "Graded: review the term list, then the Schoology vocab quiz"),
           ("BrainBuffet Module Work", 48, "Self-paced videos, following along in the app"),
           ("Save & Wrap-Up", 5, "Save, back up, log out")],
 "worksheet": [("Stinger", 10, "Today's stinger from the stinger deck; take attendance"),
               ("Pace Check", 5, "Students find today's pace goal"),
               ("BrainBuffet Module Work", 33, "Self-paced videos, following along in the app"),
               ("Module Worksheet", 25, "Graded: the module worksheet"),
               ("Submit & Wrap-Up", 5, "Submit the worksheet, save, back up")],
 "stinger": [("Stinger", 10, "Today's stinger from the stinger deck; take attendance"),
             ("Pace Check", 5, "Students find today's pace goal"),
             ("BrainBuffet Module Work", 55, "Self-paced videos, following along in the app"),
             ("Stinger Sheet Check", 8, "Graded: the sub checks each student's Stinger Response Sheet")],
 "work": [("Stinger", 10, "Today's stinger from the stinger deck; take attendance"),
          ("Pace Check", 5, "Students find today's pace goal and the first video they haven't finished"),
          ("BrainBuffet Module Work", 58, "Self-paced videos, following along in the app; no graded item today"),
          ("Save & Wrap-Up", 5, "Save, back up, log out")],
 "product": [("Stinger", 10, "Today's stinger from the stinger deck; take attendance"),
             ("Pace Check", 5, "Students check the product checklist"),
             ("BrainBuffet Module Work", 58, "Finish the module's product, then keep going in the videos"),
             ("Submit", 5, "Graded (summative): submit the finished module product in Schoology")],
 "formative": [("Stinger", 10, "Today's stinger from the stinger deck; take attendance"),
               ("Pace Check", 5, "Students check the product checklist"),
               ("BrainBuffet Module Work", 58, "Finish the module's product, then keep going in the videos"),
               ("Submit", 5, "Graded (formative): submit the finished module product in Schoology")],
 "summative": [("Stinger", 10, "Today's stinger from the stinger deck; take attendance"),
               ("Pace Check", 5, "Students check the finished-product checklist"),
               ("Finish the Module Project", 58, "Finish, export and polish the unit's summative product"),
               ("Submit", 5, "Graded (summative): submit the finished product in Schoology")],
}
WORK = {k: next(m for seg, m, _ in v if seg.startswith("BrainBuffet") or seg.startswith("Finish the")) for k, v in TIMING.items()}
for k, v in TIMING.items():
    assert sum(t[1] for t in v) == 78, k

def timing(c, t):
    """TIMING rows for a course; ADD's worksheet is its Handbook's Critical Thinking questions."""
    rows = TIMING[t]
    if c["app"] == "Premiere Pro" and t == "worksheet":
        rows = [("Critical Thinking Questions", m, "Graded: answer the module Handbook's three Critical Thinking questions in Schoology")
                if seg == "Module Worksheet" else (seg, m, n.replace("the worksheet", "your answers")) for seg, m, n in rows]
    return rows

def ws_name(c, m):
    return f"Module {m} Critical Thinking Questions" if c["app"] == "Premiere Pro" else f"Module {m} Worksheet"

# Last video a worksheet depends on (FDD); the worksheet is due no earlier than the day this video is scheduled.
AI_WS_NEEDS = {1: "1.11", 2: "2.15", 3: "3.17", 4: "4.11", 5: "5.06", 6: "6.05"}

def fkeys(P):
    return sorted(k for k in P["slots"] if k.startswith("F"))

def day_keys(P):
    return fkeys(P) + ["S"]

def s_days(unit, P):
    """S days per section: the unit's A/B school days minus two per formative day, split between sections."""
    rest = UNIT_DATES[unit][1] - 2 * len(fkeys(P))
    lo = rest // 2
    return lo, rest - lo

def mod_of(vid):
    return int(vid.split(".")[0])

# ---------------------------------------------------------------- unit plans
def unit_plan(cid, unit):
    if cid == "fdd":
        p = FDD_PLAN[unit]
        seq = [v for m in sorted(AI) for v in AI[m]["videos"]]
        ids = [v[0] for v in seq]
        vids = seq[ids.index(p["start"]):ids.index(p["end"]) + 1]
        tot = {m: sum(v[1] for v in AI[m]["videos"]) for m in AI}
        weight = {v[0]: v[1] * AI_HOURS[mod_of(v[0])] * 3600 / tot[mod_of(v[0])] for v in vids}
        groups = FDD_VOCAB[unit]
        vg = [(lab, terms, f"vocab/fmla-ai-u{unit}.md" if len(groups) == 1 else
               f"vocab/fmla-ai-u{unit}-m{lab.split()[-1]}.md") for lab, terms in groups]
        return dict(title=p["title"], vids=vids, weight=weight, slots=p["slots"], extra=p.get("s_extra", []),
                    vocab_groups=vg,
                    mods=sorted({mod_of(v[0]) for v in vids}), s_videos=True)
    m = ADD_UNITS[unit]
    mod = PR[m]
    return dict(title=f"Premiere Pro Module {m}: {mod['name']}", vids=mod["videos"], weight={v[0]: v[1] for v in mod["videos"]},
                slots={"F1": ("exit",), "F2": ("vocab",), "F3": ("worksheet", m), "F4": ("stinger",), "S": ("summative", m)},
                extra=[], vocab_groups=[(f"Module {m}", mod["vocab"], f"vocab/fmla-pr-m{m}.md")], mods=[m],
                s_videos=(mod["short"] != "Exam Prep & Practice"))

def plan_days(unit, P):
    """Video days in class order: F1–F4, the S block's video days, then F5 (if any). The last S day stays free
    for finishing and submitting, so an F5 worksheet lands after every video it needs but before the summative is due."""
    days = [(k, WORK[P["slots"][k][0]]) for k in fkeys(P) if k != "F5"]
    lo, _ = s_days(unit, P)
    if P["s_videos"]:
        days += [(f"S{k}", WORK["summative"]) for k in range(1, lo)]
    if "F5" in P["slots"]:
        days.append(("F5", WORK[P["slots"]["F5"][0]]))
    return days

def allocate(P, days):
    vids, wt = P["vids"], P["weight"]
    total = sum(wt[v[0]] for v in vids)
    wtot = sum(d[1] for d in days)
    bounds, acc = [], 0
    for key, w in days:
        acc += w
        bounds.append((key, acc / wtot))
    out = {k: [] for k, _ in days}
    run = 0
    for v in vids:
        mid = (run + wt[v[0]] / 2) / total
        run += wt[v[0]]
        out[next(k for k, b in bounds if mid <= b + 1e-9)].append(v)
    return out

def day_of(alloc, vid):
    return next((k for k, vs in alloc.items() if any(v[0] == vid for v in vs)), None)


def check(cid, unit, P, alloc, days):
    """Warn if a graded item is due before the videos it depends on."""
    warn = []
    for day, slot in P["slots"].items():
        if day == "S":
            continue
        need = None
        if slot[0] == "worksheet" and cid == "fdd":
            need = AI_WS_NEEDS[slot[1]]
        if slot[0] in ("formative", "product"):
            need = AI[slot[1]]["videos"][-1][0]
        key = lambda vid: tuple(int(x) for x in vid.split("."))
        if need and key(need) < key(P["vids"][0][0]):
            need = None   # taught in an earlier unit
        if need:
            d = day_of(alloc, need)
            order = [k for k, _ in days]
            if d is None or order.index(d) > order.index(day):
                warn.append(f"{cid} U{unit} {day} {slot} needs {need}, scheduled {d}")
    return warn

PLANS = {}

def P_of(c, unit):
    return PLANS[(c["key"], unit)]

def pts_of(c, slot):
    """Points printed on pages: always None. Point values are internal planning (see raw_pts and schema_check)."""
    return None

def raw_pts(c, slot):
    """Planned points for a graded slot, or None when the course has no point schema (ADD) or nothing is graded."""
    t = slot[0]
    if t in ("summative", "product"):
        return c["mods"][slot[1]].get("points")
    if t == "work":
        return None
    return c.get("form_pts")

def pts_txt(p):
    return f", {p} pts" if p else ""

# ---------------------------------------------------------------- shared text
def start_steps(c, mods):
    mtxt = " and ".join(f"Module {m}" for m in mods)
    if c["app"] == "Illustrator":
        files = ("Save every BrainBuffet file in your Digital Design Drive folder, in **Project Files**, "
                 "named the way the video names it.")
    else:
        files = ("The module's footage lives in **`/Users/Shared/GMetrix`** on every lab Mac (Finder › "
                 "**Go › Go to Folder…**). It's read-only: keep your own `.prproj` in your project folder and "
                 "back it up to Drive at the end of class. Lost? See [ADD 2.1, Finding the GMetrix "
                 "Folder]({% link applications/add2/2_1.md %}#finding-the-gmetrix-folder).")
    return (f"1. Open **GMetrix SMS** and log in with Google (school account).\n"
            f"2. Open the BrainBuffet **{c['app']}** course ({mtxt}). Start at the first video you haven't finished.\n"
            f"3. Open **{c['app']}**. Put the video on one side of the screen and {c['app']} on the other, and "
            f"pause the video to do each step yourself.\n"
            f"4. {files}\n"
            f"5. Use headphones. Captions and transcripts are available on every video.")

def video_table(vs):
    rows = ["| Video | Length | Title |", "|---|---|---|"]
    rows += [f"| {v[0]} | {v[2]} | {v[3]} |" for v in vs]
    return "\n".join(rows)

def slot_label(c, slot, unit):
    t = slot[0]
    if t in ("product", "formative", "summative"):
        return c["mods"][slot[1]]["product_title"]
    if t == "vocab" and len(P_of(c, unit)["vocab_groups"]) > 1:
        return f"{P_of(c, unit)['vocab_groups'][slot[1]][0]} Vocabulary Quiz"
    if t == "worksheet":
        return ws_name(c, slot[1])
    return {"exit": "Exit Ticket", "vocab": "Vocabulary Quiz", "stinger": "Stinger Sheet Check", "work": "Work Day"}[t]

def worksheet_text(c, m):
    mod = c["mods"][m]
    if c["app"] == "Illustrator":
        return (f"Complete {mod['worksheet']}. Download it from Module {m}'s resources in BrainBuffet.\n\n"
                f"{{: .note }}\n{mod['worksheet_note']}\n\n"
                "Save it in your **Project Files** folder and submit it (or a PDF of it) in Schoology before you leave.")
    return (f"Answer the three **Critical Thinking questions** from your **{mod['handbook']}**:\n\n"
            f"1. In BrainBuffet, open Module {m}'s resources and open the **{mod['handbook']}**.\n"
            "2. Find the **Critical Thinking** section. It has three questions.\n"
            "3. Open today's **Critical Thinking Questions** assignment in Schoology and answer all three questions there.\n"
            "4. Write **3–5 sentences** for each answer, and use **at least one vocabulary term** from this module in every answer.\n"
            "5. Submit before you leave.\n\n"
            "*Stuck on how to start? Try: \"In this module I learned that ___. This matters because ___. For example, ___.\"*")

def product_checklist(mod, label):
    return [f"Your {label}: **{mod['product']}**.", "",
            "- [ ] Every video in the module is finished",
            "- [ ] The project file is saved in **Project Files** and backed up to Drive",
            "- [ ] The final version is exported and saved in **Exports**",
            "- [ ] It's submitted in Schoology", ""]

# ---------------------------------------------------------------- pages
def front(title, parent, top, lesson_lines):
    return "\n".join(["---", "layout: default", f"title: {q(title)}", f"parent: {q(parent)}",
                      f"grandparent: {q(top)}", "nav_exclude: false", "lesson:"] + lesson_lines + ["---", ""])

def teacher_page(folder, unit, slug, title, parent, top):
    write(f"{folder}/fmla{unit}/{slug}-teacher.md", "\n".join([
        "---", "layout: default", f"title: {q(title + ' (Teacher)')}", f"parent: {q(parent)}",
        f"grandparent: {q(top)}", "nav_exclude: true", "has_toc: false", "---",
        f"# {title} | Teacher Plan", "", "{% include teacher-plan.html %}", ""]))

def lesson_page(c, unit, P, day, alloc, days):
    slot = P["slots"][day]
    t = slot[0]
    mods = c["mods"]
    num = f"{unit}.{day[1]}" if day != "S" else f"S{unit}"
    parent = f"{c['top']} | Unit {unit}"
    label = slot_label(c, slot, unit)
    if day == "S":
        title = f"S | {unit} | {label}"
    elif c["app"] == "Premiere Pro":   # one module per unit: keep the original "Module, Part n" titles
        old_label = {"exit": "Exit Ticket", "vocab": "Vocabulary Quiz", "worksheet": "Critical Thinking Questions", "stinger": "Stinger Sheet Check"}[t]
        title = f"{num} | {mods[P['mods'][0]]['short']}, Part {day[1]}: {old_label}"
    else:
        title = f"{num} | {label}"
    if day == "S":
        s_keys = [d for d, _ in days if d.startswith("S")]
        today = [v for k in s_keys for v in alloc.get(k, [])]
    else:
        today = alloc.get(day, [])
    today_mods = sorted({mod_of(v[0]) for v in today}) or [P["mods"][-1]]
    ext_mod = mods[today_mods[-1]]
    last = today[-1] if today else None
    reach = f"finish video {last[0]} ({last[3]})" if last else "catch up on any unfinished videos"
    m = slot[1] if len(slot) > 1 else None
    span = slot[1] if t == "stinger" and len(slot) > 1 else "the unit so far"
    if t in ("vocab", "stinger"):
        m = None
    tgt = {"exit": f"follow the BrainBuffet {c['app']} videos at pace and {reach}, then report progress on an exit ticket",
           "vocab": f"define the unit's key terms by scoring on the vocabulary quiz, and {reach}",
           "worksheet": (f"explain Module {m}'s concepts by answering its Handbook's three Critical Thinking questions, and {reach}"
                         if c["app"] == "Premiere Pro" else f"apply Module {m}'s skills by completing its worksheet, and {reach}"),
           "stinger": f"{reach}, and show a complete Stinger Response Sheet for {span}",
           "work": f"follow the BrainBuffet {c['app']} videos at pace and {reach}",
           "product": f"finish and submit {mods[m]['product'] if m else ''}, and {reach}",
           "formative": f"finish and submit {mods[m]['product'] if m else ''}, and {reach}",
           "summative": f"finish and submit {mods[m]['product'] if m else ''}"}[t]
    evidence = {"exit": "The Pace Check Exit Ticket in Schoology: last video finished, a screenshot of it, and a 3-sentence reflection.",
                "vocab": "The Schoology vocabulary quiz score (auto-graded).",
                "worksheet": f"The submitted {ws_name(c, m)}.",
                "stinger": f"The Stinger Response Sheet: every stinger from {span} answered, shared, copied and synthesized.",
                "work": "No collected grade today: the sub's walk-around check that each screen shows today's pace-goal video or later.",
                "product": f"The submitted summative product: {mods[m]['product'] if m else ''}.",
                "formative": f"The submitted formative product: {mods[m]['product'] if m else ''}.",
                "summative": f"The submitted summative product: {mods[m]['product'] if m else ''}."}[t]
    summ = {"exit": "The exit ticket: last video finished, a screenshot, and one skill learned.",
            "vocab": "The vocab quiz summarizes the unit's terms.",
            "worksheet": ("Students explain the module's concepts in their own words, using its vocabulary." if c["app"] == "Premiere Pro"
                          else "The worksheet applies the module's skills on a fresh file."),
            "stinger": "Students review their stingers while the sheet is checked.",
            "work": "Before saving, students compare the last video they finished with today's pace goal.",
            "product": "Students check the product against its checklist before submitting.",
            "formative": "Students check the product against its checklist before submitting.",
            "summative": "Students submit the finished product and check it against the checklist."}[t]
    acp_parts = [f"M{mm}: {mods[mm]['acp']}" for mm in today_mods] if len(P["mods"]) > 1 else [mods[today_mods[0]]["acp"]]
    acp_note = " (BrainBuffet's mapping; Modules 1–4 use the older Illustrator objective numbers)" if c["app"] == "Illustrator" and min(today_mods) <= 4 else ""
    L = ["  course: " + q(c["key"]), f"  unit: {unit}", f"  number: {q(num)}"]
    if day == "S":
        L.append("  is_summative: true")
    L.append(f"  standard: {q('ACP ' + '; '.join(acp_parts) + acp_note)}")
    if t == "vocab":
        L += ["  vocab:", f"    - {P['vocab_groups'][slot[1] if len(slot) > 1 else 0][2]}"]
    mod_names = ", ".join(f"Module {mm} ({mods[mm]['name']})" for mm in P["mods"])
    L.append(folded("source", f"FMLA plan: this unit follows BrainBuffet {c['app']} {mod_names} in GMetrix SMS, instead of the regular {c['course_name']} Unit {unit} lessons. Video list, lengths and objective mapping come from BrainBuffet's teacher lesson plans."))
    if day == "S":
        lo, hi = s_days(unit, P)
        span = f"{lo}" if lo == hi else f"{lo}–{hi}"
        extra = "".join(f" The Module {em} worksheet is also due on the last S day, as a separate formative grade{pts_txt(pts_of(c, ex))}."
                        for ex in P["extra"] for em in [ex[1]])
        sp = pts_of(c, slot)
        sp = f" ({sp} pts)" if sp else ""
        L.append(folded("purpose_note", f"The S block is {span} class periods per section on the A/B calendar. The S block's summative is {mods[m]['product']}{sp}.{extra} Students who finish early do the extension challenge."))
    L.append("  timing:")
    for seg, mins, note in timing(c, t):
        L += [f"    - segment: {q(seg)}", f"      minutes: {mins}", f"      note: {q(note)}"]
    L += ["  the_seven:",
          f"    organization: {q('The page lists today’s videos, their lengths and one pace goal, so every student knows exactly where to stop. ' + ('Nothing is graded today; it’s a work day.' if t == 'work' else 'Graded today: ' + label + '.'))}",
          f"    connection: {q('Continues the BrainBuffet ' + c['app'] + ' videos from the last class; each student starts at the first video they haven’t finished.')}",
          f"    target: {q(tgt)}",
          f"    collaboration: {q('Stinger share-and-copy with a neighbor; students who are ahead help a neighbor find their place in a video before starting the extension.')}",
          f"    evidence: {q(evidence)}", f"    summarization: {q(summ)}"]
    if t == "exit":
        L.append("  exit_ticket: fmla-pace")
    files = "your BrainBuffet project file" if c["app"] == "Illustrator" else "your .prproj project file"
    L += ["  organize:", "    binder:", "      - \"your Stinger Response Sheet\"", "    drive:",
          f"      - item: {q(files)}", "        folder: \"Project Files\""]
    if t in ("formative", "summative", "product"):
        L += ["      - item: \"your exported finished product\"", "        folder: \"Exports\""]
    else:
        L += ["  organize_grading:", f"    plus: {q('the project file is saved and backed up, and the student is at or past today’s pace goal')}",
              f"    minus: {q('no saved project file, or more than one class behind the pace goal')}"]
    L += ["  differentiation:",
          f"    iep504: {q('Turn on video captions and transcripts; the pace goal can stop one video earlier with the remaining video moved to the next class; print the page’s video table to check off.')}",
          f"    ell: {q('Captions and full transcripts are available on every BrainBuffet video; the vocab list with definitions stays open in a second tab; stinger sentence frame: I think ___ because ___.')}",
          f"    gt: {q('Finish today’s videos, then start the extension challenge: ' + ext_mod['ext'])}",
          "  materials:", f"    - {q('Lab Mac with GMetrix SMS and ' + c['app'])}"]
    L += [f"    - {q('BrainBuffet ' + c['app'] + ' Module ' + str(mm) + ' (' + mods[mm]['name'] + ')')}" for mm in P["mods"]]
    L += ["    - \"Headphones\"", "    - \"Stinger Response Sheet\""]
    L.append(folded("notes", sub_notes(c, P, slot, day)))
    body = student_body(c, unit, P, day, slot, label, title, today, alloc, days, ext_mod)
    slug = f"{unit}_{day[1]}" if day != "S" else f"s{unit}"
    write(f"{c['folder']}/fmla{unit}/{slug}.md", front(title, parent, c["top"], L) + body)
    teacher_page(c["folder"], unit, slug, title, parent, c["top"])

def sub_notes(c, P, slot, day):
    mods = c["mods"]
    t = slot[0]
    m = slot[1] if len(slot) > 1 else None
    p = pts_of(c, slot)
    worth = f"It's worth {p} points. " if p and t not in ("summative", "product") else ""
    base = ("For the sub: project today's stinger from the stinger deck and take attendance, then project this page. Students work at "
            "their own pace in BrainBuffet; circulate and check that each student's screen shows the video "
            "named in today's pace goal or later. ")
    if t == "work":
        extra = "Nothing is collected today: it's a work day. The walk-around pace check is the evidence; note anyone more than one class behind. "
    elif t == "exit":
        extra = "In the last 5 minutes, students post the Pace Check Exit Ticket in Schoology (screenshot + last video + reflection). "
    elif t == "vocab":
        extra = "Open today's Schoology vocabulary quiz at the start of the quiz block and close it after 15 minutes. "
    elif t == "worksheet":
        ws = mods[m].get("worksheet") or f"the three Critical Thinking questions in the {mods[m]['handbook']}"
        grade = mods[m].get("worksheet_grade", "Check system: ✓ all three answered in 3–5 sentences with a module term, ✓+ specific examples from the project, ✓− missing or one-line answers.")
        what = "Today's assignment is" if c["app"] == "Premiere Pro" else "The worksheet is"
        extra = f"{what} {ws}. Students do it in the last 25 minutes, after their videos. Collect it in Schoology. Teacher grading (on return): {grade} "
    elif t == "stinger":
        span = m or "this unit"
        extra = (f"In the last 8 minutes, walk the room and mark each Stinger Response Sheet on the check system: ✓ every stinger from {span} "
                 "is there with a 3-sentence answer, a copied partner answer and a synthesis; ✓+ answers go beyond 3 sentences; "
                 "✓− missing entries. Record marks on the roster. ")
    elif t == "product":
        extra = f"Summative grade: students submit {mods[m]['product']} in Schoology by the end of class. Teacher grading (on return): {mods[m]['rubric']} "
    elif t == "formative":
        extra = f"Formative grade: students submit {mods[m]['product']} in Schoology by the end of class. Teacher grading (on return): {mods[m]['rubric']} "
    else:
        sp = f" ({p} pts)" if p else ""
        extra = f"Summative grade{sp}: students submit {mods[m]['product']} in Schoology on the last S day. Teacher grading (on return): {mods[m]['rubric']} "
        for ex in P["extra"]:
            em = ex[1]
            ep = pts_of(c, ex)
            scale = f", scaled to {ep} points" if ep else ""
            extra += f"Also collect the Module {em} worksheet on the last S day as a formative grade{scale}: {mods[em]['worksheet_grade']} "
    if worth and t in ("worksheet", "vocab", "stinger"):
        worth = f"It's worth {p} points (scale the score to {p}). " if t == "worksheet" else worth
    return base + extra + worth + "Answer keys and BrainBuffet's finished example files stay with the teacher's resources and are not posted."

def student_body(c, unit, P, day, slot, label, title, today, alloc, days, ext_mod):
    t = slot[0]
    mods = c["mods"]
    m = slot[1] if len(slot) > 1 else None
    p = pts_of(c, slot)
    pw = f" ({p} points)" if p else ""
    span = slot[1] if t == "stinger" and len(slot) > 1 else "this unit"
    if t in ("vocab", "stinger"):
        m = None
    pw = f", {p} points" if p else ""
    graded = {"exit": "**Exit Ticket.** Post your Pace Check Exit Ticket in Schoology at the end of class.",
              "work": "**Work day, nothing graded.** Use all of today's work time to reach the pace goal.",
              "product": f"**{label} (summative{pw}).** Finish and submit it in Schoology by the end of class.",
              "vocab": f"**{label}{' (' + pw[2:] + ')' if p else ''}.** Review the key terms below, then take the Schoology vocabulary quiz.",
              "worksheet": (f"**{ws_name(c, m)}{' (' + pw[2:] + ')' if p else ''}.** "
                            + ("Answer the three Critical Thinking questions from the module Handbook in Schoology in the last 25 minutes of class."
                               if c["app"] == "Premiere Pro" else "Complete and submit it in the last 25 minutes of class.")),
              "stinger": f"**Stinger Sheet Check{' (' + pw[2:] + ')' if p else ''}.** Your Stinger Response Sheet for {span} gets checked at the end of class.",
              "formative": f"**{label} (formative).** Finish and submit it in Schoology by the end of class.",
              "summative": f"**{label} (summative{pw}).** Submit it in Schoology by the end of the last S day."}[t]
    head = "Today's graded assignment" if t != "work" else "Today"
    b = [f"# {title}", "", "{: .highlight }", f"{head}: {graded}", ""]
    if t == "summative" and P["extra"]:
        also = " and ".join(f"the **Module {ex[1]} Worksheet**{' (' + str(pts_of(c, ex)) + ' points)' if pts_of(c, ex) else ''}" for ex in P["extra"])
        b += ["{: .note }", f"Also due on the last S day: {also}, graded as a formative.", ""]
    b += ["## Today's Plan", "", "| Time | What you do |", "|---|---|"]
    b += [f"| {mins} min | {seg} |" for seg, mins, _ in timing(c, t)]
    b += ["", "## Stinger (~10 min)", "", "{% include lesson-parts/stinger.md %}", "", "## Stay on Pace", ""]
    if day == "S":
        s_keys = [d for d, _ in days if d.startswith("S")]
        if today:
            goals = [f"**S day {k[1:]}:** finish video {alloc[k][-1][0]} ({alloc[k][-1][3]})." for k in s_keys if alloc.get(k)]
            b += ["{: .important }", " ".join(goals) + " **The last S day:** finish, export and submit your project.", "", video_table(today), ""]
            if "F5" in P["slots"]:
                b += ["{: .note }", f"**Class order:** S{unit} day{'s' if len(s_keys) > 1 else ''} {', '.join(k[1:] for k in s_keys)}, then "
                      f"[{unit}.5]({unit}_5.md) ({slot_label(c, P['slots']['F5'], unit)}), then the last S{unit} day.", ""]
        else:
            b += ["{: .important }", "All of this unit's videos should be done by now. **S days:** finish, export and submit your project, then start the extension challenge.", ""]
    elif today:
        last = today[-1]
        b += ["{: .important }", f"**Pace goal:** by the end of class, finish **video {last[0]}: {last[3]}**.", "",
              f"Today's videos ({mmss(sum(v[1] for v in today))} of video):", "", video_table(today), ""]
    else:
        b += ["{: .important }", "**Pace goal:** all of this unit's videos should be finished. Catch up on anything you skipped, then work on the extension challenge.", ""]
    b += ["- **Behind?** Start at the first video you haven't finished and keep going. Watch with captions on and "
          "skip rewatching parts you already did.",
          f"- **Ahead?** Check your work against the video, then try the extension challenge: {ext_mod['ext']}", ""]
    if t == "vocab":
        groups = P["vocab_groups"]
        if len(groups) == 1:
            b += ["## Vocabulary Quiz (~15 min)", "",
                  "Review these terms for a few minutes, then take the **Unit vocabulary quiz** in Schoology. It's auto-graded.", "",
                  "### Key Terms", "", f"{{% include unit-vocab.html course=\"{c['key']}\" unit={unit} %}}", ""]
        else:
            glab, _, ginc = groups[slot[1]]
            b += ["## Vocabulary Quiz (~15 min)", "",
                  f"Review these terms for a few minutes, then take the **{glab} vocabulary quiz** in Schoology. It's auto-graded.", "",
                  f"### Key Terms: {glab}", "", "{: .vocab }", f"{{% include {ginc} %}}", "",
                  f"<div class=\"vocab-quiz no-print\" data-course=\"{c['key']}\" data-unit=\"{unit} {glab}\"></div>", ""]
    if t == "stinger":
        b += ["## Stinger Sheet Check (last ~8 min)", "",
              f"Before the check, make sure every stinger from {span} is on your sheet, each with:", "",
              "- [ ] the question rewritten in your own words",
              "- [ ] your answer, at least 3 sentences",
              "- [ ] your neighbor's answer, copied",
              "- [ ] 1–2 sentences on what your answers had in common", ""]
    if t == "formative":
        b += ["## Finish and Submit (formative)", ""] + product_checklist(mods[m], "Module " + str(m) + " product")
    if t == "product":
        pts = f" It's worth **{p} points**." if p else ""
        b += ["## Finished Product Checklist (summative)", "", f"This is one of this unit's two summatives.{pts}", ""] + product_checklist(mods[m], "summative")
    if t == "summative":
        pts = ""
        which = "the unit's second summative" if any(sl[0] == "product" for sl in P["slots"].values()) else "the unit's summative"
        b += ["## Finished Product Checklist (summative)", "", f"This is {which}.{pts}", ""] + product_checklist(mods[m], "summative")
        for ex in P["extra"]:
            b += [f"### Also due: Module {ex[1]} Worksheet (formative)", "", worksheet_text(c, ex[1]), ""]
    b += ["## BrainBuffet Work Time", "", start_steps(c, P["mods"]), ""]
    if t == "worksheet":
        b += [f"## {ws_name(c, m)} (last ~25 min)", "", worksheet_text(c, m), ""]
    if t == "exit":
        b += ["## Exit Ticket (last ~5 min)", "", "{% include lesson-parts/organize.html %}", "", "{% include exit-ticket/fmla-pace.md %}", ""]
    else:
        b += ["## Wrap-Up", "", "Save, back up your project file, and log out of GMetrix SMS.", "", "{% include lesson-parts/organize.html %}", ""]
    return "\n".join(b)

def graded_rows(c, unit, P):
    rows = []
    for day in day_keys(P):
        slot = P["slots"][day]
        lab = slot_label(c, slot, unit)
        p = pts_of(c, slot)
        kind = {"formative": " (formative product)", "summative": " (summative)", "product": " (summative)", "work": " (nothing graded)"}.get(slot[0], "")
        if p:
            kind = kind[:-1] + f", {p} pts)" if kind else f" ({p} pts)"
        num, link = (f"{unit}.{day[1]}", f"{unit}_{day[1]}.md") if day != "S" else (f"S{unit}", f"s{unit}.md")
        extra = "".join(f"; also the Module {ex[1]} Worksheet ({pts_of(c, ex) or 'formative'}{' pts' if pts_of(c, ex) else ''})" for ex in P["extra"]) if day == "S" else ""
        rows.append((num, link, lab + kind + extra))
    return rows

def summ_slots(P):
    return [P["slots"][d] for d in day_keys(P) if P["slots"][d][0] in ("product", "summative")]

def unit_index(c, unit, P, alloc, days):
    dates, ndays = UNIT_DATES[unit]
    lo, hi = s_days(unit, P)
    total = sum(v[1] for v in P["vids"])
    mods = c["mods"]
    head = f"{c['unit_label']} {'–'.join(str(m) for m in (P['mods'][0], P['mods'][-1])) if len(P['mods']) > 1 else P['mods'][0]}"
    fm = ["---", "layout: default", f"title: {q(c['top'] + ' | Unit ' + str(unit))}", f"nav_order: {unit}", f"parent: {q(c['top'])}",
          f"description: {q(P['title'])}", "has_children: true", "has_toc: false", "---"]
    b = [f"# Unit {unit} | {P['title']} ({dates})", "", "## Introduction", ""]
    for m in P["mods"]:
        b += [mods[m]["overview"], ""]
    b += [f"This unit replaces the regular {c['course_name']} Unit {unit} lessons while your teacher is on leave. Every class follows the same routine: a stinger, a pace check, then self-paced work in BrainBuffet {c['app']}.", "",
          "| | |", "|---|---|",
          f"| **BrainBuffet videos** | {P['vids'][0][0]}–{P['vids'][-1][0]} ({len(P['vids'])} videos, {mmss(total)} of video) |",
          f"| **Class periods** | {ndays} school days on the A/B calendar: {len(fkeys(P))} formative days plus {lo if lo == hi else f'{lo}–{hi}'} S days per section |",
          f"| **Summative{'s' if len(summ_slots(P)) > 1 else ''}** | " + "; ".join(mods[sl[1]]['product'] + pts_txt(pts_of(c, sl)).replace(', ', ' (', 1) + (')' if pts_of(c, sl) else '') for sl in summ_slots(P)) + " |", "",
          "## Graded Assignments", "", "| Day | Graded assignment |", "|---|---|"]
    b += [f"| [{n}]({l}) | {lab} |" for n, l, lab in graded_rows(c, unit, P)]
    b += ["", "## Pacing Guide", "", "Where you should be at the end of each class:", "",
          "| Class | Videos | Finish by the end of class |", "|---|---|---|"]
    for k, _ in days:
        vs = alloc.get(k, [])
        label = f"{unit}.{k[1]}" if k.startswith("F") else f"S{unit}, day {k[1:]}"
        if vs:
            b.append(f"| {label} | {vs[0][0]}–{vs[-1][0]} | {vs[-1][0]} {vs[-1][3]} |")
        else:
            b.append(f"| {label} | — | Catch up, then the extension challenge |")
    b.append(f"| S{unit}, last day(s) | — | Finish, export and submit the summative |")
    b += ["", "## Calendar of Events for This Unit", "", (f"{{% include calendar-of-events.html unit={unit} data=\"calendar_fmla_fdd\" %}}" if c["app"] == "Illustrator"
                                                     else f"{{% include calendar-of-events.html unit={unit} %}}"), "",
          "## Unit Vocabulary", "", f"{{% include unit-vocab.html course=\"{c['key']}\" unit={unit} %}}", ""]
    write(f"{c['folder']}/fmla{unit}/index.md", "\n".join(fm) + "\n" + "\n".join(b))

def section_index(c, cid, plans):
    rows = []
    for unit, P in plans.items():
        sm = P["slots"]["S"][1]
        rows.append(f"| [Unit {unit}](fmla{unit}/index.md) | {UNIT_DATES[unit][0]} | {P['title']} | " + "; ".join(c['mods'][sl[1]]['product_title'] for sl in summ_slots(P)) + " |")
    prep_extra = ("- Copy each module's footage (Modules 2–5, about 5 GB each) to `/Users/Shared/GMetrix` on every lab Mac. There's no Jamf, so this is by hand; one USB-C drive is fastest.\n"
                  "- Confirm Premiere Pro opens each module's starter project from that folder on one test Mac.\n"
                  if c["app"] == "Premiere Pro" else
                  "- Open each module's starter files on one test Mac to make sure fonts activate and files open.\n"
                  "- Check that Generate Vectors, Generative Shape Fill, Mockup and Firefly work on a student account (Module 6, Unit 6). If the district has them turned off, students can watch Module 6 and do the parts that don't need them.\n")
    if cid == "fdd":
        nf = max(len(fkeys(P)) for P in plans.values())
        graded = ["| Unit | " + " | ".join(f".{i}" for i in range(1, nf + 1)) + " | S (summative) |", "|---" * (nf + 2) + "|"]
        for unit, P in plans.items():
            r = {n.split(".")[-1] if "." in n else "S": lab for n, _, lab in graded_rows(c, unit, P)}
            graded.append(f"| {unit} | " + " | ".join(r.get(str(i), "—") for i in range(1, nf + 1)) + f" | {r['S']} |")
        graded_intro = ("Formatives are every module worksheet, a vocabulary quiz for each module's terms, and one Stinger Sheet Check "
                        "near the end that covers every stinger since the semester break. Summatives are the BrainBuffet module products. "
                        "Days marked *work day* have nothing graded: use them to stay on pace.")
    else:
        graded = ["| Day | Graded assignment |", "|---|---|",
                  "| F .1 | Exit Ticket: your progress, a screenshot and one thing you learned |",
                  "| F .2 | Vocabulary Quiz on the module's key terms (listed on the .2 page) |",
                  "| F .3 | Critical Thinking Questions: answer the three Critical Thinking questions in the module's Handbook |",
                  "| F .4 | Stinger Sheet Check |",
                  "| S | The finished product for the BrainBuffet module (summative) |"]
        graded_intro = "Each unit is one BrainBuffet module, graded the same way every unit."
    b = ["---", "layout: default", f"title: {q(c['top'])}", f"nav_order: {c['nav']}", "has_children: true", "has_toc: false",
         f"description: {q('Units 3–6 of ' + c['course_name'] + ' while the teacher is on leave, run entirely through BrainBuffet in GMetrix.')}", "---",
         f"# {c['top']}: {c['course_name']} During Leave", "",
         f"While your teacher is on leave, {c['course_name']} Units 3–6 run entirely through the BrainBuffet {c['app']} course in GMetrix SMS. These pages replace the regular unit pages for those units.", "",
         "| Unit | Dates | BrainBuffet content | Summative |", "|---|---|---|---|"] + rows + [
         "", "## Every Class", "",
         "1. **Stinger (10 min).** Answer the day's stinger on your Stinger Response Sheet.",
         "2. **Pace check (5 min).** Find today's pace goal on the day's page: the video you should finish by the end of class.",
         "3. **BrainBuffet work.** Watch each video and do every step in " + c["app"] + " as you go.",
         "4. **Save and back up** before you leave.", "",
         "## How You're Graded", "", graded_intro, ""] + graded + [
         "", "## For the Substitute", "",
         "- Start class by projecting today's stinger from the course's stinger deck and taking attendance. Then project the day's page (find it on the unit page or the calendar).",
         "- Students work at their own pace. Circulate and check that each screen shows the pace-goal video or later.",
         "- Each day's teacher page has the full plan and the grading notes. Add `-teacher` to the end of the page's address, for example `3_1-teacher.html`.",
         "- Students who are ahead do the extension challenge listed on the page.", "",
         "## Before Leave (teacher checklist)", "",
         "- Build each unit's Schoology vocabulary quiz from the **Download Schoology Vocab Quiz (QTI)** button on the unit page or the .2 page.",
         "- Post the exit ticket, " + ("Critical Thinking Questions" if c["app"] == "Premiere Pro" else "worksheet") + ", product and summative assignments in Schoology for each unit.",
         "- Print a class set of Stinger Response Sheets.", prep_extra]
    write(f"{c['folder']}/index.md", "\n".join(b))

def vocab_include(rel, terms):
    lines = []
    for term, d in sorted(terms, key=lambda x: x[0].lower()):
        lines += [f"**{term}**", f": {d}", ""]
    write(f"_includes/{rel}", "\n".join(lines).rstrip() + "\n")

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

# Internal grading schema (FDD): never printed on a page.
FDD_SCHEMA = dict(formatives=12, formative_pts=120, summative_pts=300)

def schema_check(c, plans):
    graded = [sl for P in plans.values() for d in day_keys(P) for sl in [P["slots"][d]] + (P["extra"] if d == "S" else [])
              if sl[0] != "work"]
    form = [sl for sl in graded if sl[0] not in ("summative", "product")]
    f_pts = sum(raw_pts(c, sl) for sl in form)
    s_pts = sum(raw_pts(c, sl) or 0 for sl in graded if sl[0] in ("summative", "product"))
    print(f"FDD schema: {len(form)} formatives / {f_pts} pts, {s_pts} summative pts")
    got = dict(formatives=len(form), formative_pts=f_pts, summative_pts=s_pts)
    return [f"FDD schema {k}: planned {v}, got {got[k]}" for k, v in FDD_SCHEMA.items() if got[k] != v]

def fmla_calendar(plans):
    """FMLA FDD calendar: the shared calendar, with each F5 taking one S day per section, right after the S video days."""
    import yaml
    cal = yaml.safe_load(open(os.path.join(ROOT, "_data/calendar.yml")))
    for unit, P in plans.items():
        if "F5" not in P["slots"]:
            continue
        lo, _ = s_days(unit, P)
        skip = 2 * (lo - 1) if P["s_videos"] else 0   # S video days, one per section, come before the .5
        seen = 0
        for week in cal[unit]:
            for day in week["days"]:
                if day.get("unit") == unit and day.get("link") == f"s{unit}":
                    if skip <= seen < skip + 2:
                        day["label"], day["link"] = f"F | {unit}.5", f"{unit}_5"
                    seen += 1
    with open(os.path.join(ROOT, "_data/calendar_fmla_fdd.yml"), "w") as f:
        f.write("# Generated by scripts/fmla/gen_fmla.py from calendar.yml; don't edit by hand.\n")
        yaml.safe_dump(cal, f, sort_keys=False, allow_unicode=True)

def main():
    exit_tickets()
    for old in glob.glob(os.path.join(ROOT, "_includes/vocab/fmla-ai-*.md")):
        os.remove(old)
    warnings = []
    for cid, c in COURSES.items():
        units = FDD_PLAN if cid == "fdd" else ADD_UNITS
        plans = {u: unit_plan(cid, u) for u in units}
        PLANS.update({(c["key"], u): P for u, P in plans.items()})
        section_index(c, cid, plans)
        for unit, P in plans.items():
            for _, terms, inc in P["vocab_groups"]:
                vocab_include(inc, terms)
            days = plan_days(unit, P)
            alloc = allocate(P, days)
            assert sum(len(v) for v in alloc.values()) == len(P["vids"])
            warnings += check(cid, unit, P, alloc, days)
            unit_index(c, unit, P, alloc, days)
            for day in day_keys(P):
                lesson_page(c, unit, P, day, alloc, days)
            load = sum(P["weight"].values()) / 60 if cid == "fdd" else None
            print(cid, unit, {k: f"{v[0][0]}-{v[-1][0]}" if v else "-" for k, v in alloc.items()},
                  f"BB load {sum(P['weight'].values())/3600:.1f}h in {sum(w for _, w in days)/60:.1f}h (+last S day)" if cid == "fdd" else "")
        if cid == "fdd":
            warnings += schema_check(c, plans)
            fmla_calendar(plans)
    for w in warnings:
        print("WARNING:", w)

if __name__ == "__main__":
    main()
