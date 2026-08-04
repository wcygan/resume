---
name: resume-parsability
description: "Evaluate, design, troubleshoot, and compare resume PDFs for robust text and field extraction. Use for ATS parsability questions, Greenhouse resume-parse feedback, Profile or Projects section decisions, Tika or Poppler disagreement, Typst resume layout choices, reading order, field association, controlled PDF experiments, parser-friendly templates, PDF tags, fonts, links, columns, tables, headers, absolute placement, hyphenation, hidden text, or deciding whether a resume change is structurally safe. Produces bounded local evidence and never equates extractor agreement with ATS, screen-reader, or hiring success."
---

# Resume Parsability

Design and evaluate resume PDFs as structured evidence, not as screenshots and
not as universal ATS scores. The goal is a resume that remains visually useful
to people while its facts, relationships, and links survive multiple local PDF
representations.

## Required companion skills

- Before creating or changing `.typ` source, locate and read the current
  `typst-author` skill. Verify syntax against its local Typst documentation,
  follow its formatting decision, compile the result, and inspect the latest
  render.
- When PDF layout or rendering matters, locate and read the current `pdf` skill
  and use its render-and-inspect workflow.

These companion skills provide current authoring and PDF mechanics. This skill
provides the resume-specific evidence model, design rules, experiments, and
claim boundaries.

Use the project-local `resume-review` skill instead when the task is about
content quality, job tailoring, bullet wording, narrative, seniority signal,
or interview preparation and does not require mechanical PDF analysis.

## Source precedence

Use evidence in this order:

1. The user's requested outcome, current source, compiled PDF, and reviewed
   factual oracle.
2. Repository instructions, fixtures, scripts, and observed extractor output.
3. The focused references in this skill.
4. Current official vendor documentation for vendor-specific claims.
5. General memory only when the sources above do not settle the question.

Do not inherit a broad claim merely because an older project document says
extractor agreement is equivalent to ATS success. Apply the layered evidence
boundary in this skill.

## Reference router

Read only the references needed for the task. For mixed tasks, read the union
before acting.

| Task cue | Required reference |
| --- | --- |
| Explain what a local parse test can prove, answer an ATS or Greenhouse question, or phrase conclusions | [Evidence and claim boundaries](references/01-evidence-and-claims.md) |
| Extract, inspect, or compare a PDF with Typst, Tika, Poppler, qpdf, or rendering tools | [Parser and PDF tools](references/02-parser-and-pdf-tools.md) |
| Design or recommend a robust resume structure | [Good patterns](references/03-good-patterns.md) |
| Decide whether Profile and Projects should coexist or how to structure them | [Good patterns](references/03-good-patterns.md) and [Bad patterns](references/04-bad-patterns.md) |
| Diagnose a known failure or identify patterns to remove | [Bad patterns](references/04-bad-patterns.md) |
| Review columns, tables, manual bullets, styled labels, spacers, PDF/UA, or other context-sensitive choices | [Conditional patterns](references/05-conditional-patterns.md) |
| Create or revise Typst source | [Typst implementation patterns](references/06-typst-implementation.md) plus the current `typst-author` skill |
| Isolate one formatting variable, build a fixture, or rank variants | [Controlled experiments](references/07-controlled-experiments.md) |
| Work in this repository or run its existing checks | [Project workflow](references/08-project-workflow.md) |
| Accept a final PDF or produce a parsability report | [Acceptance checklist](references/09-acceptance-checklist.md) |
| Revisit the exact evidence learned in the August 2026 study | [Session findings](references/10-session-findings.md) |

## Entry contract

Before changing a resume or declaring a result, record:

```text
Task: review | diagnose | change | experiment | compare
Source and compiled PDF:
Artifact hash or baseline identity:
Intended page count and page size:
Authoritative facts and their expected order:
Association windows for profile, jobs, projects, education, and skills:
Expected links:
Extractor and compiler versions:
Allowed source/PDF edits:
Visual acceptance standard:
External ATS/UAT evidence, if any:
```

Infer low-risk project details from the checkout. Ask only when a missing choice
would change facts, page count, target system, or acceptance criteria.

## Core workflow

1. Freeze the input source and PDF identity. Preserve raw artifacts.
2. State the layer being evaluated: artifact, text, document structure,
   structured fields, external ATS behavior, or human outcome.
3. Define a reviewed oracle of unique facts, expected order, and bounded
   relationships before inspecting output.
4. Compile deterministically when source is available. Keep PDF tags enabled;
   use no-tags only as an explicit negative control.
5. Run the repository quick gate when applicable, then inspect Poppler plain,
   Poppler layout, Tika, and coordinate-aware XML for deeper work.
6. Test exact field counts, order, and bounded profile/job/project/education/skills
   associations. Presence alone is insufficient.
7. Audit page geometry, fonts, images, links, PDF integrity, and semantic tags.
8. Render every page and inspect reading order, clipping, wrapping, alignment,
   and detached markers.
9. Treat extractor disagreement as a finding. Do not choose the convenient
   output and discard the others.
10. Report local evidence separately from external ATS behavior and residual
    uncertainty.

## Golden Resume quick path

This repository packages the complete controlled fixture under
`tests/fixtures/golden-resume/`: source, compiled PDF, anonymous data,
responsive renderer, reviewed oracle, and stress manifest. This skill owns the
evaluators and knows that fixture path. Treat the fixture directory as
authoritative; do not recreate Golden source or PDF copies at the repository
root.

```sh
just golden-check
just golden-stress
```

The recipe rebuilds the PDF with the pinned Source Sans 3 cuts, then runs:

```sh
uv run --no-project \
  .agents/skills/resume-parsability/scripts/evaluate_golden_resume.py
```

The deep evaluator preserves raw Poppler and Tika output, separates Tika's one
exact link-annotation block from visible-body field counts, creates a
separate NFC-plus-whitespace diagnostic view, checks bounded Profile and
Projects records along with the other sections, and gives the Golden Resume's
work-authorization statement its own named gate. That gate requires
`U.S. citizen · Authorized to work in the U.S. · No sponsorship required`
exactly once after LinkedIn and before Profile in every raw and canonical view.
The stress command runs the same renderer with reviewed JSON data/oracle
patches for long company, role, date, location, URL, and project values. It
accepts either collision-free one-row metadata or the template's source-order
preserving stacked-right fallback, renders every page, and requires the
unbreakable company and location controls to fail their exact reviewed gate
sets. Reports are written beneath `.extraction/golden-resume-stress/`. Passing
automated reports still
leave visual inspection and external ATS behavior as separate acceptance
layers.

## Non-negotiable rules

- Preserve raw extraction. A canonical diagnostic view may apply Unicode NFC
  and whitespace collapse only; it must not delete soft hyphens, punctuation,
  zero-width characters, icons, or URLs.
- Require facts to be associated with the correct record, not merely found
  somewhere in the document.
- Treat citizenship, work authorization, and sponsorship status as
  user-authoritative facts. Never infer or synthesize them from location, name,
  employment history, or other resume context. When a verified statement is
  intentionally present, keep it visible in normal flow and test it as a
  canonical fact.
- Prefer single-column, sequential normal flow with semantic headings and
  native lists.
- Do not hide canonical facts, duplicate text invisibly, or use an image of
  text to improve a visual score.
- Do not describe Tika, PDFBox, Poppler, or PDF tags as proof of a specific
  ATS implementation unless current primary evidence establishes that fact.
- Do not call a resume "ATS-safe" or predict callback probability from this
  workflow.
- Re-run after compiler, font, extractor, operating-system, locale, or layout
  changes. PDF serialization and reading order are implementation-sensitive.

## Completion report

Lead with the outcome and include:

- the exact artifact and toolchain tested;
- raw and canonical results by extractor view;
- field count, order, and bounded-association results;
- PDF structure, font, image, link, integrity, and visual results;
- the smallest source-side recommendation supported by evidence;
- a local classification of Pass, Conditional, or Fail; and
- an explicit statement that external ATS behavior remains untested unless an
  authorized UAT result was actually observed.
