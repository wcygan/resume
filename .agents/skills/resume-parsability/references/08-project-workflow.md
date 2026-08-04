# Project workflow

This repository already has a fast text-extraction regression gate. Reuse it;
do not replace it with ad hoc string checks. Use the deeper workflow in this
skill when layout, structure, links, or causal interpretation changes.

## Contents

- Authoritative files and quick commands
- Current coverage and limitations
- Known local hotspots
- Failure workflow and claim boundary

## Authoritative project files

- `will_cygan_resume-data.json` — authoritative resume content.
- `will_cygan_resume.typ` — thin JSON-to-renderer adapter.
- `will_cygan_resume.pdf` — compiled artifact.
- `tests/fixtures/golden-resume/` — complete Golden Resume test bundle:
  source, compiled PDF, canonical anonymous data, responsive renderer, reviewed
  oracle, stress manifest, and fixture documentation.
- `fonts/source-sans-3/` — pinned font cuts and license used by the Golden build.
- `tests/fixtures/golden-resume/golden-resume-template.typ` — active shared
  renderer for the personal resume and Golden fixture.
- `scripts/extraction_check.py` — Poppler/Tika regression gate.
- `scripts/extraction-check.fixtures.toml` — reviewed expected strings.
- `.agents/skills/resume-parsability/scripts/evaluate_golden_resume.py` — deep
  Golden Resume evaluator run through uv.
- `.agents/skills/resume-parsability/scripts/evaluate_golden_stress_matrix.py`
  — isolated case compiler and matrix evaluator.
- `tests/fixtures/broken/` — controlled negative fixtures.
- `tests/test_extraction_check.py` — gate regression tests.
- `.github/workflows/extraction-check.yml` — CI extractor environment.

## Quick commands

```sh
just compile
just extraction-check
just page-budget
just test
just golden
just golden-check
just golden-stress
```

`just golden-check` rebuilds the fixture PDF with the pinned Source Sans 3 cuts
and PDF/UA-1, then runs the skill-owned uv evaluator. Evidence is written
to a new timestamped directory beneath `.extraction/golden-resume/`; prior runs
are not silently selected as current evidence.

`just golden-stress` materializes each reviewed case from a fresh copy of the
canonical data and oracle, compiles it through the same fixture adapter and
renderer, and invokes the deep Golden evaluator. Use `--case <name>` for one
case. Evidence is written to a new timestamped directory beneath
`.extraction/golden-resume-stress/`.

To retain a report even on success:

```sh
uv run scripts/extraction_check.py --report
```

For a variant:

```sh
uv run scripts/extraction_check.py \
  --pdf path/to/variant.pdf \
  --fixtures path/to/reviewed-variant.fixtures.toml \
  --report-dir path/to/new-report-directory \
  --report
```

Do not reuse the main resume fixture for a variant with different facts.

## Current quick-gate coverage

The script currently checks:

1. non-empty extraction;
2. section order;
3. candidate name/contact presence and proximity;
4. job title/company/date proximity;
5. date format;
6. replacement characters, flagged punctuation, and Private Use Area glyphs;
7. cross-extractor section/job/byte-count agreement;
8. soft hyphens;
9. keyword round-trip;
10. duplicate extracted URLs; and
11. blank-line section boundaries.

It runs Poppler plain, Poppler layout, and Tika when available. A local run with
an extractor skipped is incomplete; CI should exercise the full configured set
and the report should record the emitted versions. Tika and Typst are exactly
pinned in the current workflow; GitHub Actions runners and apt-installed
Poppler/qpdf can still change.

## What the quick gate does not prove

The current gate is necessary but not a complete deep audit. It does not, by
itself, require:

- every canonical field exactly once;
- strict field order inside every job;
- bounded association windows for education and skills;
- PDF tags or specific H/list structures;
- font embedding and Unicode mappings;
- image absence;
- exact link annotation destinations;
- qpdf integrity; or
- visual rendering quality.

Use the full acceptance checklist when the template, layout primitives, fonts,
links, export flags, or section structure changes.

## Golden deep-gate coverage

The skill-owned Golden evaluator supplements the general quick gate. It checks:

1. the current fixture source and PDF relationship;
2. raw and NFC-plus-whitespace Poppler plain/layout, Tika visible-body, and
   decoded XML views, while preserving and separately validating Tika's one
   exact URI annotation block wherever it occurs in the raw output;
3. exact reviewed fields and global order;
4. a dedicated exact-once work-authorization gate between LinkedIn and Profile;
5. bounded Profile, three Experience, Projects, Education, and Skills windows;
6. forbidden replacement, private-use, zero-width, and soft-hyphen codepoints;
7. one-page Letter geometry, zero rotation, and tagged status;
8. pinned Source Sans asset hashes, embedded subset Unicode fonts, image
   absence, and qpdf integrity;
9. expected H1/H2/native-list structure and exact URI multiset;
10. collision-free same-row or reviewed stacked-right, common-right-edge
    metadata geometry; and
11. creation of 144-DPI PNGs for every page for required human inspection.

The stress matrix adds single-variable and combined content-length coverage.
Supported cases must retain exact fields, associations, links, one-page Letter
output, and valid responsive geometry inside the reviewed page content box.
Its unbreakable company and location controls must fail their exact reviewed
gate sets.

The script reports an automated local Pass or Fail. It deliberately reports
visual inspection as needing human review and external ATS/Greenhouse UAT as
Untested.

## Known local hotspots

The personal artifact and Golden fixture share one renderer. A renderer change
therefore has a wider blast radius than a JSON-only content change: rebuild and
inspect both artifacts, then run the Golden deep gate and relevant stress
cases.

Experience metadata uses responsive geometry with a reviewed stacked-right
fallback. Treat changes to organization, role, date, location, page width, or
text metrics as geometry changes; nearby extracted fields alone are not proof
of correct association.

The skills section uses a compact layout container. Keep it only while the
current extraction, ordering, and section-boundary gates pass, and do not copy
that structure into work-history records without a controlled experiment.

The two LinkedIn jobs share the same employer string. This makes exact counts
and bounded per-job relationships more important than a global presence check.

## Failure workflow

1. Read `.extraction/report.md` and each raw extractor text file.
2. Identify whether the failure is missing text, order, association, Unicode,
   link duplication, or section separation.
3. Inspect the JSON content, adapter, and renderer primitive that generated the
   region.
4. Fix the source-side structure before widening a threshold.
5. Add or update one reviewed fixture in the same change.
6. Run the narrow negative-fixture test, then all project checks.
7. For platform-sensitive cases, verify the Linux CI path as well as macOS.

Do not propagate older project prose that equates local extractor agreement
with full ATS success. The useful mechanics remain; the correct claim is a
bounded local extraction result.
