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

## Notes

- Output PDF: `will_cygan_resume.pdf`. CI artifacts retained 30 days.
- Never commit changes under `archive/`.
