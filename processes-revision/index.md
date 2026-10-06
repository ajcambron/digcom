---
layout: default
title: "PDD Revision (Draft)"
nav_order: 31
nav_exclude: true
search_exclude: true
has_children: true
has_toc: false
description: "First-draft revision of Processes of Digital Design, built backward from the ACP Photoshop exam, with SkillsUSA and TSA photography prep."
---
# Processes of Digital Design: Revision Draft 1

{: .warning }
**Unlisted draft.** Nothing here replaces the live [Processes of Digital Design](../processes/index.md) pages, which are unchanged, and nothing in Drive was edited. These pages are hidden from the site navigation and search.

**Goal:** by April 30, 2027, students are prepared to (1) pass the Adobe Certified Professional exam in Visual Design Using Adobe Photoshop, (2) compete in SkillsUSA Photography, and (3) submit a TSA Photographic Technology portfolio. Not every student competes: each unit separates the core for everyone from optional competition-track enrichment.

## Deliverables

1. [Coverage matrix](coverage-matrix.md): 81 rows (ACP objectives + TSA + SkillsUSA criteria) × 45 existing lessons. 34 rows covered by an existing lesson, 18 partial, 29 gaps; every row is covered in the revision.
2. [Scope & sequence](scope-and-sequence.md), unit by unit, with exam objectives, competition skills, existing lessons, class periods, assessment, core vs competition track, and literacy/numeracy.
3. The draft course, in the build format (`lesson:` front matter, paired teacher pages, calendar, exit tickets):

   - [Unit 1: Camera Fundamentals & Exposure](pdd1/index.md)
   - [Unit 2: Photoshop Foundations](pdd2/index.md)
   - [Unit 3: Photojournalism](pdd3/index.md)
   - [Unit 4: Light & Art Photography](pdd4/index.md)
   - [Unit 5: Image Correction](pdd5/index.md)
   - [Unit 6: Masks, Channels & Type](pdd6/index.md)
   - [Unit 7: Advanced Compositing](pdd7/index.md)
   - [Unit 8: Digital Painting & Vector](pdd8/index.md)
   - [Unit 9: Publishing, Delivery & Portfolio](pdd9/index.md)
   - [Unit 10: ACP Review, Practice Exams & Certification](pdd10/index.md)
   - [Unit 11: Photojournalism Profile & Nationals Prep](pdd11/index.md)
   - [Unit 12: Portfolio Polish & Deconstructed Identity](pdd12/index.md)
4. [Change log](change-log.md): moved, edited, added, and cut, with reasons.

## By the numbers

- **36 formative lessons:** 9 existing unchanged, 19 existing with light edits, **8 NEW** (2.1, 2.4, 4.4, 7.4, 8.4, 9.1, 9.3, 9.4).
- **9 summatives:** all existing projects, 0 NEW.
- **NEW lesson stubs** say what's missing in their teacher notes (start files, station cards, a spec sheet).

## Promoting the draft

When it's approved: move `processes-revision/pddN/` into `processes/pddN/`, change `parent:` from "PDD Draft | Unit N" to "PDD | Unit N" and `grandparent:` to "Processes of Digital Design", and remove `nav_exclude`/`search_exclude` from student pages (teacher pages keep `nav_exclude: true`).

## Assumptions

1. **ACP objectives** are from the official *Visual Design Using Adobe Photoshop* exam objectives, 2025 exam version (Photoshop v26.x), the PDF in Drive. Adobe's and Certiport's sites were blocked from this session, so check for a newer version before the testing window.
2. **SkillsUSA Photography** national technical standards are members-only (Pathful). The criteria K1–K12 were compiled from published state and national summaries; check them against the current national standards when you log in.
3. **TSA Photographic Technology** rules are from the 2025 & 2026 high school guide in Drive (*TSA Rules 26*). The 2026–27 theme ("Behind the Scenes" per a web search) is unverified. TSA's honor statement bans generative AI, so 7.4's AI work is ACP-only.
4. **Calendar:** the same `_data/calendar.yml` as FDD and ADD, A/B schedule. On that calendar the S10 exam meeting falls on 4/30 for one section and 5/3 for the other; the draft recommends testing both by 4/30.
5. **Period estimates** for existing lessons come from the materials themselves (slide counts, tutorial length). Most decks are image-only, so they were inventoried by title.
6. **Software:** Photoshop 26.11 (GMetrix's top supported version), run in Rosetta for GMetrix. Lightroom is not assumed; Camera Raw and Bridge replace it.
7. **Equipment:** Canon Rebel (T6-class, APS-C, ~1.6 crop) DSLRs with 18–55 mm kit lenses, tripods, and the Godox X Pro-C / X1R-C / Canon 600EX-RT flash kits. No dedicated macro lens; 4.4 uses the kit lens at closest focus, and extension tubes are an optional purchase.
8. **No Jamf:** practice files, Classroom in a Book files, and GMetrix files are copied by hand to `/Users/Shared/` on all 24 Macs (the same pattern ADD uses), with a master copy in Drive.
9. **BrainBuffet Photoshop** needs about 22 hours of class time for Modules 1–6 and 8; the strand provides about 17.5 hours in Units 2–9. Module 6 finishes in Unit 12, Module 8 starts as homework during S9, and Module 7 is Unit 12 enrichment.
10. **Vocabulary includes** (`_includes/vocab/pdd-*.md`) don't exist yet, so lessons have no `vocab:` lists and the F5 quiz button stays hidden until they're written.
11. **Prints and mounting** (11×14 on 16×20) cost money, so they are competition-track only; everyone else submits digital.
12. **Generative AI** in Photoshop is assumed enabled for student Adobe IDs; if the district disables it, 7.4 is a teacher demo.
