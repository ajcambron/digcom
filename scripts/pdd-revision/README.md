# PDD revision generator

Builds the unlisted draft in `processes-revision/` (and `_includes/exit-ticket/pdd2-1-score*.md`) from the data files here:

- `units.py`: unit-level fields (dates, objectives, competition skills, core vs track, literacy/numeracy, GMetrix)
- `lessons_a.py`, `lessons_b.py`, `lessons_c.py`: the 36 formative lessons; `summatives.py`: S1–S9; `patches.py`: wording overrides
- `matrix.py`: ACP Photoshop (2025) objectives, TSA/SkillsUSA criteria, and the existing-lesson inventory (EX01–EX45)

Run from the repo root: `python3 scripts/pdd-revision/gen.py .`

Re-running overwrites every page in `processes-revision/`. Once you start hand-editing those pages, stop using the generator.
