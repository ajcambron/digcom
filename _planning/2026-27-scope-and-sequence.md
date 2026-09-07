# DigCom 2026–27 Scope & Sequence (ACP Alignment Draft)

> Planning document — lives in `_planning/` so Jekyll does not publish it.
>
> **Goal:** Reorganize each course into cycles of 4–6 formative lessons + 1 summative,
> aligned to the Adobe Certified Professional 2025 exam objectives, with all objectives
> covered before spring break (March 26, 2027). Lessons that don't serve the exam move
> to **Extra Units** taught after spring break.

| Course | ACP Exam | Existing content reused |
|---|---|---|
| FDD (Foundations) | Graphic Design & Illustration Using **Illustrator** (v29) | fdd1, fdd4, fdd7 |
| PDD (Processes) | Visual Design Using **Photoshop** (v26) | pdd1 |
| ADD (Applications) | Digital Video Using **Premiere Pro** (v25) | add1, add2, add3, add5, add7, add8, add9 |

---

## Calendar Math (2026–27, every-other-day schedule)

- First student day **Aug 31 / Sep 1, 2026** → last day before spring break **Mar 25, 2027** (Mar 25 = conferences, schools closed; last student day is Mar 24).
- 120 student days ÷ 2 = **60 class meetings** per section before spring break.
- Jan 25–28 are HS exam days → budget **~58 instructional meetings**.
- Marking periods land cleanly: **MP1 ends Oct 30 = meeting 20**, **MP2 ends Jan 28 = meeting 43**.

**Pacing model: 8 units × 7 meetings (5 formative lessons + 2 summative work blocks) = 56 meetings**, leaving ~2–4 March meetings for ACP practice-exam review and certification testing before break.

| Unit | Meetings | Approx. dates | Anchor |
|---|---|---|---|
| 1 | 1–7 | Aug 31 – early Oct | |
| 2 | 8–14 | October | |
| 3 | 15–21 | late Oct – early Nov | MP1 ends at meeting 20 |
| 4 | 22–28 | Nov – early Dec | |
| 5 | 29–35 | Dec – mid Jan | Winter break splits this unit |
| 6 | 36–42 | mid Jan – early Feb | HS exams Jan 25–28 |
| 7 | 43–49 | February | MP2 ended at meeting 43 |
| 8 | 50–56 | late Feb – mid Mar | |
| Review + ACP exam | 57–60 | mid–late March | **All objectives covered; certify before break** |
| Extra Units | Apr 5 – Jun 11 | ~26 meetings | Post-exam enrichment |

---

## Shared-Block (`_includes`) Strategy

Existing reusable blocks stay the backbone so student-facing language is identical everywhere:
`organizedesign.md`, `organizevideo.md`, `premieresetup.md`, `delivervideo.md`/`exportvideo.md`,
`portfolio.md`, `designbrief.md`, `projectfolder.md`, `shareandsubmit.md`, `ctelessonplan.md`, rubrics.

**New blocks to create:**

1. **`_includes/vocab/…`** — one file per objective cluster (e.g., `vocab/ai-1-1.md`, `vocab/ps-3-2.md`, `vocab/pr-4-5.md`) containing the Adobe **Key Terms as a definition list**. Each lesson and its unit index include the same block, so vocabulary language is identical on every page it appears. ✅ Pattern implemented Sep 2026 for ADD Unit 1: `vocab/pr-1-1a.md`, `pr-1-1c.md`, `pr-1-4a-basics.md`, `pr-1-4c-shots.md`. **Source of truth is the Google Drive `Master Vocabulary.csv` / per-module `vocabulary.csv` files** under `Digital Communications Resources/Premiere Pro Certification/` (and the sibling `Illustrator Certification`/`Photoshop Certification`/`After Effects Certification` folders for FDD/PDD/the AE extra unit) — copy definitions verbatim from there, don't hand-write new ones, so site language matches the ACP exam key terms exactly. Still open: Units 2–8 need the same treatment (pull each unit's terms from the matching Module vocabulary.csv).
2. **Vocab callout** — add to `_config.yml` callouts (e.g., `vocab: {title: "Exam Vocabulary", color: blue}`) so every lesson opens with an explicit, visually consistent ACP vocabulary callout. Not yet added — the Unit 1 includes currently render as a plain `## Key Terms` heading + definition list, no colored box. Do this once, site-wide, rather than per unit.
3. **`_includes/organizephoto.md`** — PDD needs a Photoshop equivalent of organizedesign/organizevideo.
4. On each lesson page, the CTE lesson-plan **Standard(s)** field cites the ACP objective number (e.g., `ACP Ai 4.1.a`), and **Vocabulary** field is the include.

---

# FDD — Illustrator (ACP Graphic Design & Illustration)

Objective domains: 1 Design Industry · 2 Document Management · 3 Workflow & Interface · 4 Objects, Paths & Text · 5 Appearance & Position

### FDD Unit 1 | Design & the Design Industry *(reuse fdd1)*
| # | Lesson | Source | ACP |
|---|---|---|---|
| 1.1 | What is Design? | fdd1 index content | 1.1.a |
| 1.2 | Elements of Design | new (split from fdd1) | 1.4.a |
| 1.3 | Principles of Design | new (split from fdd1) | 1.4.a |
| 1.4 | Purpose, Audience & Client Goals | new | 1.1.a, 1.1.b |
| 1.5 | Communicating Design Plans | new | 1.1.c, 1.1.d |
| **S1** | **Design Elements Exercises** | fdd1/1_1 (promote to summative) | 1.4 |

**Vocab callouts:** client goals, target audience, demographics, accessibility · sketches, specifications, design process, wireframes, prototypes, iterations, change orders, drafts, feedback loop, style guide, project brief · project scope, scope creep, project timeline · space, line, shape, form, color and color value, texture · emphasis/focal point, unity/harmony, variety, balance, alignment, proximity, repetition, rhythm, scale, movement, negative space, contrast, rule of thirds

### FDD Unit 2 | Vector Documents & Workspace *(new)*
| # | Lesson | Source | ACP |
|---|---|---|---|
| 2.1 | Pixels vs. Paths | new | 1.3.a |
| 2.2 | The Illustrator Interface | new | 3.1.a, 3.1.b |
| 2.3 | Documents & Artboards | new | 2.1, 2.2 |
| 2.4 | Design Aids: Rulers, Guides, Grids, Views | new | 3.2 |
| 2.5 | Saving & File Formats | new | 2.4.a |
| **S2** | **Artboard Sampler** (multi-artboard shape compositions) | new | 2.1–2.2, 3.1–3.2 |

**Vocab callouts:** image resolution, image size, file types, pixel, raster, bitmap, vector, path, object, rasterizing, rendering, resizing, bleed, trim, live area · application bar, control panel, panels, toolbars, contextual taskbar · artboards, pasteboard · Outline, Pixel Preview, Presentation Mode

### FDD Unit 3 | Shape & Color *(reuse fdd4)*
| # | Lesson | Source | ACP |
|---|---|---|---|
| 3.1 | Color Theory | fdd4/1_1 | 1.4.a |
| 3.2 | Digital Color: Modes & Gamuts | new | 1.3.b |
| 3.3 | Shape Tools | new | 4.1.c |
| 3.4 | Swatches & Gradients | new | 3.3 |
| 3.5 | Align, Distribute & Arrange | new | 5.4 |
| **S3** | **Vector Self-Portrait** | fdd4/s4 | 3.3, 4.1.c, 5.4 |

**Vocab callouts:** color mode, gamut, CMYK, RGB, HSB, grayscale, hex values, spot, rich black · process, spot, and global swatches; Color Guide panel · gradient types, color stops, Gradient Mesh

### FDD Unit 4 | The Pen Tool & Paths *(reuse fdd7 structure)*
| # | Lesson | Source | ACP |
|---|---|---|---|
| 4.1 | Art Analysis & Inspiration Board | fdd7/7_1 | 1.1.c |
| 4.2 | Pen Tool Bootcamp (guided practice) | fdd7/7_2 expanded | 4.1.a, 4.1.b |
| 4.3 | Concept Sketches | fdd7/7_3 | 1.1.c |
| 4.4 | Refining Paths (Join, Simplify, Shape Builder, Pathfinder) | new | 4.2 |
| 4.5 | Peer Review | fdd7/7_4 | 1.1.c |
| **S4** | **Low-Poly Stained-Glass** | fdd7/s7 | 4.1, 4.2, 5.1 |

**Vocab callouts:** anchor points, segments, curve an angle · Curvature, Pencil, Paintbrush, Blob Brush, Line Segment · Simplify, Smooth, Join, Clean Up, Outline Stroke, Offset Path · Eraser, Scissors, Knife, Shape Builder, live paint, compound paths, Pathfinder · Selection, Direct Selection, Lasso, Group Selection, Isolation Mode

### FDD Unit 5 | Typography
| # | Lesson | Source | ACP |
|---|---|---|---|
| 5.1 | Type Anatomy & Classification | new (FDD outcome 5 language) | 1.4.b |
| 5.2 | Character Settings | new | 4.3.b |
| 5.3 | Paragraph Settings & Area Type | new | 4.3.c, 4.4.b |
| 5.4 | Type on a Path & Special Type | new | 4.3.a |
| 5.5 | Text Flow & Converting to Outlines | new | 4.4.a, 4.4.c |
| **S5** | **Typographic Poster** | new | 1.4.b, 4.3–4.4 |

**Vocab callouts:** font, size, font style, kerning, tracking, leading, horizontal and vertical scale, line length, baseline shift · area type vs. point type vs. type on a path, glyphs, placeholder text · threading text, wrapping text, overflow text · Character Styles, Paragraph Styles, converting text to outlines

### FDD Unit 6 | Layers, Appearance & Effects
| # | Lesson | Source | ACP |
|---|---|---|---|
| 6.1 | The Layers Panel | new | 3.5 |
| 6.2 | Appearance: Fill & Stroke | new | 5.2.a |
| 6.3 | Effects: Shadows, Glows & 3D | new | 5.2.b, 4.2.c |
| 6.4 | Opacity, Blending & Masks | new | 5.3 |
| 6.5 | Transformations & Live Corners | new | 5.1.b, 4.2.d |
| **S6** | **Album Cover / Gig Poster** | new | 3.5, 5.2–5.3 |

**Vocab callouts:** sublayers, stacking order, merge layers · Appearance panel, Eyedropper, Recolor Artwork · drop shadows, feathers, glows · Transparency panel, opacity masks, blending modes, clipping masks · scaling, warping, distorting, skewing, bounding box, reference points

### FDD Unit 7 | Brushes, Symbols, Patterns & Image Trace
| # | Lesson | Source | ACP |
|---|---|---|---|
| 7.1 | Brushes | new | 3.4 |
| 7.2 | Symbols & Graphic Styles | new | 3.4, 5.2.c |
| 7.3 | Pattern Making | new | 3.4.b |
| 7.4 | Image Trace | new | 4.1.d |
| 7.5 | Generative AI in Illustrator | new | 4.1.e |
| **S7** | **Sticker Pack / Merch Pattern** | new | 3.4, 4.1.d–e |

**Vocab callouts:** brush types, dynamic vs. static symbols, Generate Patterns, graphic styles · Trace presets, Ignore Color, Threshold, expanding · Generate Vectors, writing prompts

### FDD Unit 8 | The Working Designer: Copyright, Assets & Export
| # | Lesson | Source | ACP |
|---|---|---|---|
| 8.1 | Copyright, Licensing & AI Content | new | 1.2 |
| 8.2 | Project Management & the Client | new | 1.1.d |
| 8.3 | Placing & Linking Assets | new | 2.3 |
| 8.4 | Exporting for Screen & Print | new | 2.4.b |
| 8.5 | Packaging a Project | new | 2.4.c |
| **S8** | **Client Brand Project** (delivered as packaged files) — uses `designbrief.md` | new | 1.1, 1.2, 2.3–2.4 |

**Vocab callouts:** usage rights, public domain, copyright, intellectual property, derivative work, commercial use, attribution, work for hire, fair use, fair dealing, stock images, AI-generated content, restricted fonts, model and location releases · embedding, linking, Edit Original · Asset Export panel, Use Artboards, file packages

### FDD Extra Units (after spring break)
- **fdd8 | Yearbook Spread** (page-layout project; not on the Illustrator exam)
- Packaging & promotional design / branding campaign (FDD outcomes 3–4)
- Scale, measurement & sketchbook work (FDD outcome 2)
- Portfolio build-out (`portfolio.md` include)

---

# PDD — Photoshop (ACP Visual Design)

Objective domains: 1 Design Industry · 2 Project Setup & Interface · 3 Layers, Masks & Adjustments · 4 Adding Content · 5 Modifying Visual Elements · 6 Publishing

### PDD Unit 1 | Design Industry & Photography *(reuse pdd1)*
| # | Lesson | Source | ACP |
|---|---|---|---|
| 1.1 | Purpose, Audience & Client Goals | new | 1.1.a, 1.1.b |
| 1.2 | Elements & Principles Review | new (reuse FDD blocks) | 1.4.a |
| 1.3 | Photography Basics | pdd1/1_1 | 1.4.a |
| 1.4 | Composition for the Camera | new | 1.4.a |
| 1.5 | Communicating Design Plans | new (shared block w/ FDD 1.5) | 1.1.c, 1.1.d |
| **S1** | **Photo Composition Scavenger Hunt** | new | 1.4 |

**Vocab callouts:** client goals, target audience, demographics, accessibility · depth of field, field of view, white balance, rule of thirds, framing, aspect ratio · sketches, specifications, iterations, change orders, drafts, feedback loop, style guide, project briefs · project scope, scope creep, project timeline

### PDD Unit 2 | Photoshop Interface & Documents
| # | Lesson | Source | ACP |
|---|---|---|---|
| 2.1 | Raster Image Terminology | new | 1.3.a |
| 2.2 | New Documents & Presets | new | 2.1 |
| 2.3 | The Photoshop Interface | new | 2.2.a, 2.2.b |
| 2.4 | Navigation & Design Aids | new | 2.2.c, 2.2.d |
| 2.5 | Digital Color & the Histogram | new | 1.3.b |
| **S2** | **Studio Setup + Collage Warm-Up** | new | 2.1–2.2 |

**Vocab callouts:** image resolution, image size, pixel, raster, vector, resampling, resizing · width/height, orientation, resolution, color mode, bit depth, background, metadata · options bar, contextual taskbar, docking panels · color modes, bit depth, gamut, histogram

### PDD Unit 3 | Layers & Selections
| # | Lesson | Source | ACP |
|---|---|---|---|
| 3.1 | The Layers Panel | new | 3.1.a |
| 3.2 | Opacity & Blending Modes | new | 3.1.b |
| 3.3 | Selection Tools I (marquee, lasso, wand) | new | 5.1.a |
| 3.4 | Selection Tools II (Select Subject, Object Selection, Sky) | new | 5.1.a |
| 3.5 | Refining, Saving & Loading Selections | new | 5.1.b, 5.1.c |
| **S3** | **Impossible Composite** ("put yourself somewhere impossible") | new | 3.1, 5.1 |

**Vocab callouts:** grouping vs. linking, flattening and merging · fill opacity, opacity, blending mode · Quick Selection, Magic Wand, Select Subject, Object Selection, Selection Brush, Select Color Range · feather, expand, contract, inverse, deselect · channels

### PDD Unit 4 | Masks & Nondestructive Editing
| # | Lesson | Source | ACP |
|---|---|---|---|
| 4.1 | Destructive vs. Nondestructive | new | 1.3.c |
| 4.2 | Pixel Masks & Select and Mask | new | 3.2.a, 3.2.b |
| 4.3 | Vector, Clipping & Frame Masks | new | 3.2.c–e |
| 4.4 | Adjustment Layers | new | 3.3.a |
| 4.5 | Adjustment Presets & Smart Filters | new | 3.3.b |
| **S4** | **Surreal Landscape Composite** | new | 3.2–3.3 |

**Vocab callouts:** destructive vs. nondestructive editing · revealing, concealing, gradient mask, Select and Mask · clipping mask, Paste Into · adjustments vs. adjustment layers, Adjustment Brush, Smart Filters

### PDD Unit 5 | Retouching & Repair
| # | Lesson | Source | ACP |
|---|---|---|---|
| 5.1 | Healing & Clone Tools | new | 5.2.a |
| 5.2 | Content-Aware & Generative Remove | new | 5.2.a, 4.1.c |
| 5.3 | Exposure: Dodge, Burn & Sponge | new | 5.2.b |
| 5.4 | Crop, Straighten & Canvas | new | 5.3.a |
| 5.5 | Transformations | new | 5.3.b |
| **S5** | **Photo Restoration Project** | new | 5.2–5.3 |

**Vocab callouts:** healing tools, clone tools, Content-Aware, Remove, Find Distractions, Patch · Burn, Dodge, Sponge · Crop, Perspective Crop, Straighten, non-destructive crop, resampling · rotate, resize, warp, distort, skew, flip, perspective

### PDD Unit 6 | Drawing, Painting & Type
| # | Lesson | Source | ACP |
|---|---|---|---|
| 6.1 | Brushes & Patterns | new | 2.5, 4.1.a |
| 6.2 | Color, Swatches & Gradients | new | 2.4 |
| 6.3 | Vector Shapes & the Pen in Photoshop | new | 4.2 |
| 6.4 | Type Tools & Character Settings | new | 4.3.a, 4.3.b |
| 6.5 | Warp Text & Type as Graphics | new | 4.3.c |
| **S6** | **Movie Poster** | new | 4.1–4.3 |

**Vocab callouts:** Pencil, Brush, Smudge, Sharpen, Blur, Paint Bucket · Eraser, Background Eraser, Magic Eraser, History Brush · Gradient panel, transparency stops, ASE file · Pen, Freeform Pen, Curvature Pen, Custom Shape · Commit button, Type on a Path, Warp Text · rasterizing type, converting text to Smart Object

### PDD Unit 7 | Smart Objects, Filters & Styles
| # | Lesson | Source | ACP |
|---|---|---|---|
| 7.1 | Placing Assets & Smart Objects | new | 2.3 |
| 7.2 | Linked vs. Embedded | new | 2.3.a, 3.1.c |
| 7.3 | Filters & Smart Filters | new | 5.4.a |
| 7.4 | Layer Styles & Materials | new | 5.4.b, 5.4.c |
| 7.5 | AI Tools: Sky Replacement & Generative Fill | new | 4.1.c |
| **S7** | **Product Mockup / Album Art** | new | 2.3, 5.4 |

**Vocab callouts:** embedding, linking, Camera Raw, Convert to Link, Relink to File, linked Smart Objects, Edit Content · Convert to Layers, Convert to Smart Object · Smart Filters vs. filters · layer styles, materials, generative AI prompt writing

### PDD Unit 8 | Copyright, Publishing & Exam Prep
| # | Lesson | Source | ACP |
|---|---|---|---|
| 8.1 | Copyright & Licensing | new (shared block w/ FDD 8.1) | 1.2.a |
| 8.2 | Model & Location Releases | new | 1.2.b |
| 8.3 | Saving & Native Formats | new | 6.2.a |
| 8.4 | Export for Web, Print & Transparency | new | 6.1, 6.2.b |
| 8.5 | Delivery & File Management | new | 1.1.d |
| **S8** | **Client Deliverable Set** + ACP practice exam | new | 1.2, 6.1–6.2 |

**Vocab callouts:** usage rights, public domain, copyright, intellectual property, derivative work, commercial use, attribution, work for hire, fair use, fair dealing, AI-generated content · model release, location release · Quick Export, Export As, exporting artboards · file formats that support transparency, color space, saving as a copy

### PDD Extra Units (after spring break)
- Web design & online portfolio (PDD outcome 8 — HTML, SEO, web-safe fonts; not on the Photoshop exam) → `portfolio/googlesites.md`
- Print production & mounting/matting for display (PDD outcome 7)
- Morgue file / idea library development

---

# ADD — Premiere Pro (ACP Digital Video)

Objective domains: 1 Video Industry · 2 Project Setup & Interface · 3 Organizing Projects · 4 Creating & Modifying Elements · 5 Publishing
**This course mostly reorders existing units.** New unit numbers below; source unit in parentheses.

### ADD Unit 1 | Elements of Video & Pre-Production *(= current add1)* ✅ drafted Sep 2026
| # | Lesson | Source | ACP |
|---|---|---|---|
| 1.1 | Intro to Digital Video Production | add1/1_1 (was 1_4md) | 1.1.d |
| 1.2 | Pick a Topic | add1/1_2 (was 1_1; added Khan Academy/Adobe explainer-video technique section) | 1.1.a |
| 1.3 | Design Brief | add1/1_3 (was 1_2; `designbrief.md`) | 1.1.a, 1.1.c |
| 1.4 | Two-Column Script | add1/1_4 (was 1_3) | 1.1.c |
| 1.5 | Film Form & Shot Vocabulary | add1/1_5 — new | 1.4.c |
| **S1** | **Explainer Video** | add1/s1 | 1.1, 1.4 |

**Deliberately low-tech:** every lesson and the summative run on a personal smartphone (Blackmagic Camera app) and free browser-based editors (Google Vids, Canva, Adobe Express) — no lab software or hardware checkout required, so the project survives an unsettled first few weeks of the school year. Filenames were renumbered to match their frontmatter titles (see cleanup item 5, now resolved for add1), and the unit index was rewritten as a Driving-Question/Vocabulary overview matching the add3 pattern instead of the old "Basic Elements of Video" content dump.

**Vocab callouts:** client goals, target audience, demographics · shot list, scriptwriting, storyboarding, edit list, transcripts · frame rate, frame size, aspect ratio, safe areas, codecs, pixels, rendering · CU, ECU, MCU, MS, WS, LS, ELS, OTS, POV, cutaway · rule of thirds, foreground, background, depth of field, field of view

### ADD Unit 2 | Editing in Premiere *(= current add2)*
| # | Lesson | Source | ACP |
|---|---|---|---|
| 2.1 | What Does an Editor Do? | add2/2_4md | 1.4.b |
| 2.2 | Projects, Sequences & Bins | new | 2.1, 3.1, 3.2 |
| 2.3 | Video Editing Basics | add2/2_1 | 2.2, 2.3, 4.1 |
| 2.4 | Transitions / Conventions | add2/2_2 | 1.4.b, 4.5.b |
| 2.5 | Standards, Formats & Frame Rates | add2/2_3 | 1.1.b, 2.1.b |
| **S2** | **Television Scene Edit** | add2/s2 (`premieresetup.md`) | 2.1–2.4, 4.1 |

**Vocab callouts:** project settings, scratch disks, sequence presets, timecode · Project panel, Source/Program Monitors, Properties panel · playhead, JKL navigation, markers · In and Out points, insert, overwrite, lift, extract · bins, relinking, labeling clips · L and J cuts, cross cutting, match cuts, cutting on the action, cutaway, montage, jump cut

### ADD Unit 3 | ENG: The News Story *(= current add3)*
| # | Lesson | Source | ACP |
|---|---|---|---|
| 3.1 | Plan | add3/3_1 | 1.1.c |
| 3.2 | Make | add3/3_2 (`organizevideo.md`) | 4.1 |
| 3.3 | Edit + Text-Based Editing | add3/3_3 expanded | 4.2 |
| 3.4 | Captions & Accessibility | new | 1.2, 4.3.c |
| 3.5 | Peer Review & Revision | add3/3_4md | 1.1.c |
| **S3** | **News Story** | add3/s3 | 1.2, 4.2–4.3 |

**Vocab callouts:** captions, subtitles, audio descriptions · transcripts, auto transcribing, filler words, lift and extract, Cut (Extract), Delete (Ripple) · text overlays, color contrast, audio clarity · MOGRTs, point text, paragraph text

### ADD Unit 4 | Cinematography & Color *(reuses add7 lessons; Video Essay replaces the Music Video summative)*
| # | Lesson | Source | ACP |
|---|---|---|---|
| 4.1 | Video Styles: Essay, Doc, Music Video, PSA & More | new | 1.1.a, 1.1.b |
| 4.2 | Shot Analysis | add7/7_1 (retarget examples from music videos to video essays) | 1.4.b |
| 4.3 | Camera Moves, Angles, Framing, Exposure | add7/7_2 | 1.4.a, 1.4.c |
| 4.4 | Storyboard & Shot List | add7/7_4 | 1.1.c |
| 4.5 | Color Correction & Grading | add7/7_3 | 4.5.a |
| 4.6 | Transform, Resize & Speed | new | 4.4 |
| **S4** | **Video Essay** — solo shot-and-edited, no narration, story told through sequencing, natural sound, and original/royalty-free music only | new (replaces add7/s7) | 1.4, 4.4–4.5 |

**Lesson 4.1 defines the styles by purpose, audience, and convention** — video essay (visual argument, no narration), documentary (interview/VO-driven), news package (reporter-led, the Unit 3 form), music video (performance/concept cut to a track), PSA vs. commercial (cause vs. product persuasion), narrative short (the Unit 7 form) — so students can name what they're making and why the conventions differ. This doubles as NATAS category-selection literacy.

**Summative constraints are competition-derived:** solo photographer/editor + no narration = NATAS H-15 eligible; original/royalty-free audio keeps every entry clear of licensing documentation.

**Vocab callouts:** aperture, shutter speed, ISO, color space, white balance · sequencing shots, B-roll, establishing shots vs. closing shots, montage, matching shots, wide vs. tight shots · Lumetri: Basic Correction, Creative, LUTs · scale, rotation, letterboxing, Generative Expand · Rolling Edit, Ripple Edit, Rate Stretch, time remapping, freeze frame

### ADD Unit 5 | Audio & Podcasting *(= current add5)*
| # | Lesson | Source | ACP |
|---|---|---|---|
| 5.1 | Podcast Production Planner | add5/5_1 | 1.1.c, 1.1.d |
| 5.2 | Podcast Script | add5/5_2 | 1.1.c |
| 5.3 | Recording & Voice-Over | new | 4.7.e |
| 5.4 | Essential Sound: Mixing & Repair | new | 4.7.c, 4.7.d |
| 5.5 | Asset Management & Submission | add5/5_3 | 3.1 |
| **S5** | **Podcast Episode** (incl. add5/5_4 Final Export & Delivery + Reflect & Evaluate) | add5/s5 | 4.7, 5.3 |

**Vocab callouts:** clipping, levels, natural/ambient sound, room tone, foley, sampling rates · audio gain, conforming, fade handles · Enhance Speech, Loudness Auto-Match, Auto Ducking, Repair, Remix · voice-over record, scratch track · mono and stereo tracks, syncing audio

### ADD Unit 6 | Effects, Keyframes & Compositing *(new — Premiere-native replacement for the After Effects unit)*
| # | Lesson | Source | ACP |
|---|---|---|---|
| 6.1 | Effect Presets & Adjustment Layers | new (adapt add4 concepts) | 4.5.b, 4.5.c |
| 6.2 | Keyframes: Motion & Opacity | new (adapt add4/4_1 "Elements of Motion") | 4.6 |
| 6.3 | Keying & Green Screen | new | 4.5.d |
| 6.4 | Mattes, Masks & Picture-in-Picture | new | 4.5.d |
| 6.5 | Pacing | adapt add4/4_2 | 1.4.b |
| **S6** | **Title Sequence / Effects Reel** (in Premiere) | new | 4.5–4.6 |

**Vocab callouts:** adjustment layer, nesting, copy and paste attributes · keyframes, temporal and spatial interpolation · keying (Luma, Chroma, Ultra), mattes, alpha channel, picture-in-picture · motion, opacity, stacking order

### ADD Unit 7 | The Short Film *(= current add8 + production lessons from add9)*
| # | Lesson | Source | ACP |
|---|---|---|---|
| 7.1 | Standard Script Formatting | add8/8_1 | 1.1.c |
| 7.2 | Storyboarding | add8/8_2 | 1.1.c |
| 7.3 | Purpose & Description | add8/8_3 | 1.1.a |
| 7.4 | Production Plan | add9/9_3 | 1.1.d |
| 7.5 | Releases, Rights & Budget | add9/9_4 + new | 1.3 |
| **S7** | **Short Film** | add8/s8 | 1.1, 1.3, synthesis of 4.x |

**Vocab callouts:** scope and sequence, dailies, pre-production/post-production, tech sheets · talent release, rights, permissions, licensing, attribution, public spaces · usage rights, copyright, intellectual property, derivative work, remixing, AI-generated content

### ADD Unit 8 | Publishing & Delivery + Exam Prep
| # | Lesson | Source | ACP |
|---|---|---|---|
| 8.1 | Sequence QC: Gaps, Levels & Safe Margins | new | 5.1 |
| 8.2 | Auto Reframe & Multi-Platform Versions | new | 5.2 |
| 8.3 | Export & Media Encoder | new (grow `delivervideo.md`/`exportvideo.md`) | 5.3.a, 5.3.b |
| 8.4 | Archiving with the Project Manager | new | 5.3.c |
| 8.5 | ACP Practice Exam & Review | new | all |
| **S8** | **Multi-Platform Delivery** of the short film (16:9 / 9:16 / 1:1 + archive) | new | 5.1–5.3 |

**Vocab callouts:** gaps in timeline, safe margins · Auto Reframe, target aspect ratio, motion tracking, clip nesting · codecs, alpha channels, Quick Export, batch processing, queue · Project Manager, collect files, consolidate and transcode

### ADD Extra Units (after spring break)
- **add7 | Music Video** (former Unit 4 summative, add7/s7) — great post-exam project; copyright/licensing lesson from Unit 7 makes a natural lead-in, and students already have the cinematography skills
- **add4 | Motion Graphics (After Effects)** — whole unit including Suns and Moons, Scratch!, `exportae.md` (After Effects is not on the Premiere exam)
- **add9 | Production Book** as a standalone summative (remaining lessons: 9_1/9_2 script formatting duplicates of add8)
- Live switching & lighting design portions of add5 (podcast studio hardware — beyond exam scope)
- Portfolio build-out & year-end reel

---

## GMetrix / BrainBuffet Self-Guided Strand (last ~30 min of every class)

**Routine:** each block ends with ~30 minutes of self-paced work in the GMetrix BrainBuffet course for that course's app. 7 meetings/unit × 30 min ≈ **3.5 hrs of GMetrix time per unit, ~28 hrs before spring break** — enough to complete each course's video content (~10.5 hrs each) plus assessments and both practice tests, with slack for rewatching.

**Accountability:** GMetrix pre-assessment during Unit 1; a module-completion checkpoint due each summative week (enters the gradebook alongside the summative); GMetrix Practice Test 1 (training mode) and Practice Test 2 (testing mode) during the March review meetings before certification.

**Alignment note:** GMetrix courses are linear, so students run modules in order; the strand stays within ~1 module of the classroom topic and intentionally *leads* it in a few spots (pre-exposure) — flagged below.

### FDD ↔ BrainBuffet Adobe Illustrator 2025 (6 modules, ~17 hrs total class time per teacher syllabus)

Durations from the teacher syllabus (video / estimated class time): M1 2:12/3h · M2 2:00/3h · M3 1:30/3h · M4 2:20/4h · M5 1:52/3h · M6 0:46/1h. At ~3.5 hrs of strand time per unit, the course finishes with ~2 units' worth of slack for practice tests.

| FDD Unit | GMetrix Module | Topic overlap |
|---|---|---|
| 1 | M1 Getting Started (start) | students meet the software while class covers design theory — deliberate lead |
| 2 | M1 (finish) | interface, documents, artboards, vector vs. raster, saving — direct match |
| 3 | M2 Dobson Branding Style Guide | color modes, gamut, type classifications — direct match; the branding-guide concept previews the Unit 8 summative |
| 4 | M3 Dobson Poster | Layers panel, effects, gradients, brushes, symbols — previews Units 6–7 while class does pen tool |
| 5 | M4 Dobson Trifold (start) | text flow & typography in layout — direct match |
| 6 | M4 (finish) | clipping masks, opacity — direct match; copyright/Creative Commons portion previews Unit 8 |
| 7 | M5 Dobson Business Card | **Image Trace lives here** — direct match with lesson 7.4; client feedback loop previews Unit 8 |
| 8 | M6 Generative AI & Exam Tips (46 min) + Practice Test 1 | Firefly/mockups reinforce 7.5; short module leaves room to start testing |
| Review | Practice Tests 1 & 2 | |

**Teacher resources on hand** (stored locally at `Documents\Claude\digcom-teacher-resources\` — **never commit to the public repo**: answer keys and finished exemplars would be visible to students):
- `illustrator/` — Teacher Syllabus (module-by-module objective mappings + durations), 6 module Lesson Plan PDFs (teacher objectives, instructional strategies, extension challenges, cross-curricular ties, rubrics), Module 1–2 workbook answer keys, and finished exemplar files for all 6 modules (the "Dobson National Park" running client project: style guide → poster → trifold → business card), incl. the Module 2 client brief, Creative Commons worksheet (M4), and Image Trace worksheet (M5).
- `photoshop/` — full workbook answer keys for Modules 1–8 (confirms the 8-module structure) + M8 course-review quiz key & Kahoot.
- `premiere/` — Teacher Syllabus (module durations + objective mappings), 5 module Lesson Plan PDFs, the "Read Before You Download" storage-logistics sheet, and finished files for Modules 1–4: final deliverables (exported .mp4s incl. captioned versions + .srt sidecar) **and step-by-step scaffolding `.prproj` files keyed to each video lesson number** — useful for helping a stuck student jump to the current step without redoing prior lessons.
- Note: the Illustrator lesson plans/syllabus cite the *older* ACP objective numbering for Modules 1–4 and the 2025 numbering for Modules 5–6; the ACP citations in this plan follow the 2025 exam objectives PDF throughout.
- The M2 client brief + Dobson exemplars are also a ready-made model for the Unit 8 Client Brand Project summative (show a complete brand system without giving away *their* client's answer).

### PDD ↔ BrainBuffet Adobe Photoshop 2025 (8 modules, ~10.5 hrs video)
| PDD Unit | GMetrix Module | Topic overlap |
|---|---|---|
| 1 | M1 Getting Started | interface mini-project while class shoots photos — deliberate lead |
| 2 | M1 (finish) + M2 (start) | interface direct match; students begin enhancing their Unit 1 photos |
| 3 | M2 Image Enhancement & Retouching | layers/adjustment basics; retouching previews Unit 5 |
| 4 | M3 Advanced Compositing | masking — direct match |
| 5 | M3 (finish) | compositing consolidates while class retouches |
| 6 | M4 Movie Poster | **direct match — same summative as the class unit** |
| 7 | M5 Generative AI | matches lesson 7.5 |
| 8 | M6 Client Project Work | briefs, file management, delivery — direct match |
| Review | M8 Exam Preparation + Practice Tests 1 & 2 | M7 Mixed-Media → post-break enrichment |

### ADD ↔ BrainBuffet Adobe Premiere Pro 2025 (5 modules, ~26 hrs total class time per teacher syllabus)

Durations (video / estimated class time): M1 Barbershop Social Promo 1:50/5–6h · M2 Fire Academy Recruiting 2:05/6h · M3 Horror Chase "No Way Out" 2:15/6–7h · M4 Basketball Showreel 2:03/6h · M5 Exam Prep 0:38/2h. **≈26 hrs against the ~28 hr strand budget — the tightest of the three courses.** If a class drifts behind, assign video-watching (captioned, transcripted) as homework and keep the hands-on steps in class.

| ADD Unit | GMetrix Module | Topic overlap |
|---|---|---|
| 1 | M1 Barbershop Social Promo (start) | project setup, rough cut, **records a scripted voice-over** — parallels the Explainer Video exactly |
| 2 | M1 (finish) | interface, trimming, audio, Auto Reframe + vertical/square export — direct match |
| 3 | M2 Fire Academy Recruiting Video (start) | transcripts/text-based editing, captions & accessibility standards, two caption deliverables (burned-in + sidecar) — **direct match with News Story** |
| 4 | M2 (finish) + M3 Horror Chase (start) | M3: pacing, tension, color grading, cinematic crop — **direct match with Video Essay unit** |
| 5 | M3 (continue) | proxies, mixed formats, rolling credits, archiving; no dedicated audio module — add GMetrix practice questions for domain 4.7 |
| 6 | M3 (finish) + M4 Showreel (start) | M4: speed ramping, frame holds, animated lower thirds — **direct match with Effects & Keyframes unit** |
| 7 | M4 (finish) | multilingual captions, multi-format platform export — previews Unit 8 while class shoots the Short Film |
| 8 | M5 Exam Prep (2 hrs: green-screen keying, track matte, gap-fill mini-challenges) + Practice Test 1 | M5 explicitly targets objectives Modules 1–4 skipped |
| Review | Practice Tests 1 & 2 | |

**Premiere logistics (from the "Read Before You Download" sheet):** student asset downloads are **~5 GB per module** (M1 5.04, M2 4.77, M3 3.14, M4 4.89; optional 4K set is 186 GB — skip it). Download module-by-module via Dropbox (not Drive/OneDrive), share one asset download among students on the same machine (separate `.prproj` files each), and on tight machines delete a module's assets after finishing it. Plan lab storage before school starts.

**Mac lab deployment & storage hygiene (ADD lab is all Mac):**
- BrainBuffet assets live at the identical path on every machine — `/Users/Shared/PremiereAssets/Module N/` — so any student at any Mac opens their project with no relinking. Owner root, read-only for students (`chown -R root:wheel`, `chmod -R 755`). Push via Jamf/Apple Remote Desktop or one USB-C SSD; never 30 simultaneous downloads.
- Day-one Premiere setup (student-facing slide, per-user settings): Media Cache → auto-delete cache files older than 14 days + cap cache size; scratch/previews inside the project folder so they die with the project.
- The Mac is a workbench, not storage: all working files in `~/Movies/DigCom/<ProjectName>/` per the existing `projectfolder.md`/`organizevideo.md` structure; project files backed up to Google Drive at end of class (assets never go to Drive); confirm with IT whether student accounts persist or get wiped.
- **Restructure to-do — edit `_includes/delivervideo.md`:** add a **"Strike"** section as the final step of every video summative — after final export is delivered and the portfolio page is up: delete raw footage from the project folder, empty the Trash, keep only final export + `.prproj`. Graded as part of the summative checklist. (Maps to ACP Pr 3.1 asset organization and 5.3.c archiving — the cleanup routine *is* curriculum.)
- **Restructure to-do — edit the Blackmagic Camera app config step in `s1.md` (Explainer Video):** add **shoot 1080p, not 4K** alongside the existing H.264 setting — a 4–5× footage-size reduction for every project all year; 1080p covers every deliverable in the course.
- Safety net: monthly per-machine disk-usage sweep (Jamf policy or script) that reports and purges media caches >30 days, prior-marking-period `DigCom` folders, and stray exports in Downloads. The report doubles as a signal for which sections aren't striking.

---

## TSA Competition Integration (before Christmas)

Events whose deliverables already match fall unit summatives — the TSA annual theme becomes the assigned topic, and the unit's existing documentation (design brief, script, storyboard via `designbrief.md` etc.) doubles as the required TSA documentation:

| TSA Event | Course / Unit | Timing | Fit |
|---|---|---|---|
| **STEM Mass Media** (video broadcast + written news story, journalism practices) | ADD Unit 3 — ENG / News Story | late Oct – early Nov | Direct 1:1 — the summative *is* the entry |
| **Audio Podcasting** (theme-based podcast + development documentation) | ADD Unit 5 — Audio & Podcasting | Dec – mid Jan | Direct 1:1 — planner + script + episode = full entry |
| **Photographic Technology** (photo portfolio conveying the annual theme) | PDD Unit 1 (shoot) → curated through Unit 5 (retouch) | Sep shoot; Dec polish | Strong — start the portfolio in Unit 1, finish it with Unit 5 retouching skills |
| **Digital Video Production** (theme video + storyboard, script, equipment docs) | ADD Unit 1 — pre-production docs; Explainer Video as entry | Sep – early Oct | Strong — point the Explainer Video at the annual theme; docs map 1:1. (A more polished entry can be re-cut from the spring Short Film.) |
| **Promotional Design** (packet of 4+ printed items) | FDD Unit 5 — Typographic Poster as first packet item | December | Partial — seed it in Unit 5; the full packet is the natural spring Unit 8 client-brand summative |

### NATAS Mid-Atlantic High School Student Production Awards (ADD)

Regional student Emmys ([call for entries](https://natasmid-atlantic.org/students/high-school/2026-high-school-call-for-entries/)). Northern Delaware is eligible. **Timing is the constraint:** the 2026 cycle's eligibility window was Feb 16, 2025 – Feb 15, 2026 with entries due Feb 27 — so for the 2027 awards, only work completed by ~mid-Feb 2027 qualifies (verify the 2027 call when posted, ~fall 2026). That maps to ADD Units 1–6; the spring Short Film rolls to the *next* year's call.

| Category | ADD Unit | Timing | Fit |
|---|---|---|---|
| **H-02 Hard News / H-03 Feature News Report** | Unit 3 — News Story | late Oct – Nov | Direct — the 90-second news clip is the entry |
| **H-14 Multimedia Journalist** | Unit 3, solo students | late Oct – Nov | Direct for students who report/shoot/edit alone |
| **H-04 Short Form** | Unit 1 — Explainer Video | Sep – early Oct | Direct — single-subject presentation |
| **H-12 PSA / H-13 Commercial / H-16 Promotional Video** | Unit 1 alternate topics | Sep – early Oct | Strong — offer "community cause," "product," or "school hype" as Explainer Video topic choices and each student self-selects a category |
| **H-15 Video Essay** | Unit 4 — Video Essay summative | Nov – early Dec | Direct 1:1 — summative constraints (solo shot/edit, no narration, original/royalty-free audio) are written to the category rules |
| **H-17 Editor (craft)** | Unit 6 — Effects Reel summative | Jan – early Feb | Strong — composites/demo reels explicitly permitted; lands just before the deadline |

**Cautions:**
- **$35/entry**, teacher approval required, faculty involvement advisory only; at least ⅔ of an entry must be original material.
- **Unit 2's Television Scene Edit is not enterable** (copyrighted source footage) — H-17 entries must be composites of original-footage work.
- Unit 5 Podcast is enterable only if produced as a *video* podcast (the live-switcher studio version qualifies; audio-only does not — that's TSA Audio Podcasting's lane).

**Not included (would be shoehorned):**
- **On Demand Video** — produced on-site at conference in 36 hours; nothing to embed in curriculum (chapter/club prep activity only).
- **Music Production** — original musical composition; the curriculum teaches speech audio (podcasting), not composition.
- **Board Game Design** — game mechanics/packaging fabrication is the core, not taught.
- **Video Game Design, Fashion Design and Technology** — outside all three courses.
- **Webmaster** — website build lives in the post-spring-break portfolio units, not the fall.
- **Children's Stories** — borderline: the illustration side fits Illustrator, but a narrative picture book needs the full pen-tool/typography/layout stack plus sustained writing; if wanted, it's a spring FDD extension, not a fall unit.

---

## `_includes` Consolidation Audit (implemented July 2026)

**New shared blocks created** (working tree, not yet committed):
- `peerreview.md` — the full Plus/Delta protocol (was inline-only in add3/3_4; fdd7/7_4 was a 3-bullet stub). Now included by both; use in every critique lesson going forward.
- `production.md` — offload-daily / DIT / script-supervisor block (was duplicated with typos across add7/s7 and add8/s8, including a stray "film your Music Video" on the Short Film page). Also fixed: DIT = Digital Imaging Technician, not "Director of IT."
- `camerasetup.md` — Blackmagic Camera app config extracted from add1/s1, now with **1080p not 4K** added per the storage plan.

**Pages rewired to existing includes instead of reinvented content:**
- add5/5_3 (Asset Management) had its own folder scheme (`UNIT5_PODCAST_LASTNAME`), un-localized boilerplate ("[Your School District Name]", "Schoology/Canvas") — replaced with `organizevideo.md` + `shareandsubmit.md`.
- add5/5_4 (Final Export) — fixed DaVinci Resolve reference, wrong lesson cross-reference, added `shareandsubmit.md`.
- `delivervideo.md` gained the **Strike** section (propagates to every video summative automatically).
- fdd4/s4 (Vector Self-Portrait) was written in **MediaWiki markup** (wikitable, `[[File:]]`, `[url label]` links) that never rendered in Jekyll — converted to the standard overview-table format; dead image references removed.

**Deleted:** `ctelessonplan copy.md`, unused `projectfolder.md` (near-duplicate of `organizevideo.md`), stray `fdd8/s7 copy.md`, all `.DS_Store` files (now gitignored).

**Still open for the restructure:** the *Overview/Project Idea table* on unit indexes and summatives is the biggest remaining duplication — same fields (Driving Question / Learning Goals / Project Summary / Major Products / Making it Public / Rubric) hand-built in varying formats on ~12 pages. Worth a parameterized include (`{% include unitplan.md dq="..." %}`) during the restructure. Also: `organizedesign.md` vs `organizevideo.md` could merge into one parameterized `organize.md`. **Policy tension to resolve:** `premieresetup.md` tells students to put Premiere project files *in Google Drive*, while add5/5_4 correctly teaches local ("offline") editing — for the Mac lab, standardize on: work local, deliver/back up to Drive.

---

## Formative Assessment System (Schoology, fast-grade, AI-resistant)

**Design principles:** (1) anchor every formative to the student's *own working file* — AI can fabricate prose, but not a screenshot of their in-progress artboard/timeline matching today's step; (2) do it in class, timed, not take-home; (3) grade artifacts, not paragraphs; (4) everything on a 0–1–2 scale so grading is a thumbnail scan (~30 sec/student).

Five reusable formats — each lesson uses one, chosen by lesson type:

| # | Format | What students do | Schoology mechanics | Why AI-resistant |
|---|---|---|---|---|
| F1 | **Vocab Warm-Up** | 5-question quiz, first 5 min of class, application-level stems ("A client needs a logo that scales to a billboard — which file type?") | Auto-graded quiz drawing randomly from a per-unit question bank built from the ACP vocab includes; locked window during class | In-class, timed, randomized; zero grading time |
| F2 | **Screenshot Receipt** (exit ticket) | Screenshot of *their* file showing today's required evidence (named layers visible, clipping mask applied, marker at the L-cut) + one sentence naming the tool used | Assignment, image upload; 0–1–2 checklist rubric | Shows their unique in-progress work; can't be generated after the fact |
| F3 | **Two-Minute Drill** | Teacher announces a live micro-task ("convert this text to outlines and align to artboard center — go"); screenshot result | Assignment, 0/1; doubles as ACP live-in-the-app practice | Performed in the app under time; mirrors the exam format |
| F4 | **Fix-This-File** | Open a deliberately broken start file (RGB doc meant for print, gap in timeline, clipped audio, unnamed layers); fix it; submit screenshot | Assignment, 0–1–2 rubric keyed to the planted errors | Requires operating the software; errors are teacher-authored and rotate |
| F5 | **Structured Peer Review** | Complete a Plus/Delta using `peerreview.md` protocol; notes must cite timestamps/locations and tool vocabulary from the partner's actual work | Assignment or discussion; rubric grades *specificity*, not politeness | Graded on concrete references to a classmate's unique file |

**Mapping to lesson types:**
- Theory/industry lessons (design principles, copyright, film form) → **F1** + an F2 variant (annotate a provided example: "circle the focal point, name the principle that creates it")
- Tool lessons (majority of the course) → **F2** routinely, **F3** once per unit
- Planning lessons (briefs, scripts, storyboards) → F2 on the planning artifact **with an in-class-announced constraint** (e.g., "today's storyboard must include one OTS frame labeled in red") — the constraint is the AI tripwire
- Critique lessons → **F5**
- Pre-summative meeting → **F4** as review (built from that unit's most common student errors)
- The GMetrix strand's module checkpoints already serve as the self-guided formative; don't double-assess it.

**Written reflections** stay on summatives only, graded for specificity: must cite two concrete moments in the student's own file/footage ("at 0:32 I used a J-cut because…"). Generic reflection prose earns a conference, not a grade.

**Build-out during restructure:** each new lesson page ends with a "📤 Exit Ticket" block naming its formative (an include per format keeps language consistent); Schoology question banks built per unit from the `_includes/vocab/` files — same source, same language, no drift.

---

## Content Cleanup Noticed While Auditing (fix during restructure)

1. `applications/add4/s4.md` is a copy of add2's Television Scene Edit summative (wrong title/parent) — add4 has no real summative page.
2. `applications/add9/9_1.md` and `9_2.md` are both titled "Standard Script Formatting" (9_2 duplicates 9_1; both duplicate add8/8_1).
3. `applications/add3/index.md` and `add7/index.md`/`add8/index.md` intro paragraphs are copy-pasted from add2 ("editing an episode of a television show").
4. ~~`foundations/fdd8/` stray files~~ ✅ deleted July 2026; the unit remains an empty shell to build out.
5. Numbering mismatches: files whose frontmatter title doesn't match filename. ~~add1 (1_4md.md titled 1.1, etc.)~~ ✅ renumbered Sep 2026 during the Unit 1 revision. Still open: add7/7_3 titled 7.4 and 7_4 titled 7.3.
6. ~~`_includes/ctelessonplan copy.md`~~ ✅ deleted July 2026.
7. ~~`.DS_Store` files~~ ✅ deleted & gitignored July 2026. Built `_site/` is still committed (git rm at next commit); `_config.yml` email is still `your-email@example.com`; `/assets/images/favicon.ico` referenced in `_config.yml` 404s locally — verify the file exists.
