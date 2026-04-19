# CLAUDE.md

Professional resume built with Typst. GitHub Actions compiles to PDF on push/PR to `main`.

## What

- **`will_cygan_resume.typ`** — single source of truth. Uses the `modern-cv` Typst template (v0.8.0). Renders to `will_cygan_resume.pdf`.
- **`work-experience/`** — long-form LinkedIn-style role write-ups used as raw material when rewriting bullets. Not compiled.
- **`advice/`** — curated hiring-manager, ATS, and interviewer guidance (STAR/XYZ, quantification, readability). Consumed by the resume skills.
- **`scripts/`** — `dev.ts` (cross-platform watch + PDF open) and `run-local-ci.ts` (local CI check).
- **`.claude/agents/`** — 12 reviewer personas (hiring-manager, bar-raiser, ats-parser, recruiter-triage, domain-sme-systems, typography-reviewer, etc.) used by the panel skills.
- **`.claude/skills/`** — resume workflows: `resume-panel`, `resume-panel-focus`, `resume-tailor-panel`, `resume-debate`, `resume-diff`, `resume-interview-rehearsal`, `resume-optimizer`.
- **`archive/`** — deprecated LaTeX source. Read-only reference; do not edit.

## Why

Maintain one authoritative resume that compiles deterministically and can be stress-tested through multiple hiring lenses (ATS, recruiter triage, hiring manager, bar raiser, SME) before every send. Correctness and review rigor beat velocity.

## How

```bash
just dev       # live preview — watches and opens the PDF
just compile   # one-shot typst compile
just ci        # local CI, run before pushing
```

`dev` and `ci` run single-file Python scripts (`scripts/dev.py`, `scripts/run-local-ci.py`) via `uv run` — PEP 723 inline metadata, no venv or `pyproject.toml`. Edit `will_cygan_resume.typ` directly. Tinymist (VSCode) is a drop-in alternative to `just dev`.

## Reviewing and editing the resume

Prefer invoking a skill over hand-driving the review:

- Broad multi-angle review → `resume-panel` (fans out all 12 reviewer sub-agents, consolidates findings).
- Single-section review → `resume-panel-focus` (work-experience, skills, projects, formatting, narrative, or header).
- Job-description tailoring → `resume-tailor-panel` with the JD as input.
- Before/after diff review against a git ref → `resume-diff`.
- Debate a single bullet → `resume-debate`.
- Interview prep from current resume → `resume-interview-rehearsal`.

When rewriting bullets, pull source material from `work-experience/` and methodology from `advice/` — the skills already know how to route there.

Each project in `work-experience/*.md` carries a **Relevance Score** (1–5 + rationale) — the author's prior for what belongs on the resume. Reviewers use it to flag buried leads (high-RS material missing from the resume) and wasted real estate (low-RS material on it). Rubric: `work-experience/RELEVANCE.md`.

## ATS-extraction design rules

The resume is stress-tested by `/extraction-check` (pdftotext, pdftotext -layout, Tika/PDFBox) on every change. The following rules exist because they are the source-side fixes for real extraction failures we've observed — do not undo them without re-running the gate.

- **`#set text(hyphenate: false)` at the top of `will_cygan_resume.typ`.** Typst auto-hyphenates long words with a soft hyphen (U+00AD); Tika/PDFBox splits the word into separate paragraphs, so ATSs on Workday/Greenhouse/Lever-style stacks cannot keyword-match `involuntary`, `characteristics`, `performance`, etc.
- **Uniform 3-char month abbreviations** in date ranges (`Feb 2022 – Mar 2024`, never `March`). A tightened ATS date regex expecting 3-char abbreviations drops the range otherwise.
- **No Font Awesome icons.** The compile host does not have the FA font; `fa-icon(...)` renders as tofu. In `template/modern-cv.typ` the icon `let` bindings are intentionally empty (`#let github-icon = []`, etc.). Do not restore `fa-icon(...)` calls unless the font is bundled and verified on CI.
- **URL display text = canonical path without scheme** (`github.com/wcygan`, `linkedin.com/in/wcygan`, `wcygan.net`). The link `href` keeps `https://`; the display text omits it. This gives ATSs keyword-searchable tokens (`github.com`, `linkedin.com`) while keeping display text distinct from Tika's URL annotation trailer so `url-dedup` stays green.
- **No duplicated link annotations.** Never pass `title-link` to multiple `resume-entry` blocks pointing at the same URL — Tika emits one annotation per call, and `url-dedup` fails when any URL appears >1× in the trailer.
- **Blank line between Skills and Education.** `-layout` extraction needs a paragraph break between the last skills row and the `Education` header so section-boundary parsers don't merge them. Preserved via `#parbreak() + #v(12pt)`.

If `/extraction-check` fails after a change, read `.extraction/{pdftotext,pdftotext-layout,tika}.txt` directly before editing the assertion logic — the extractor output is almost always right.

## Notes

- Output PDF: `will_cygan_resume.pdf`. CI artifacts retained 30 days.
- Never commit changes under `archive/`.
