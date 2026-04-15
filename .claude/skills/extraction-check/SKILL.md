---
name: extraction-check
description: ATS text-extraction regression gate for the resume repo. Runs the compiled PDF through three open-source parsers (pdftotext, pdftotext -layout, Apache Tika) that real ATSs actually use, asserts clean extraction across seven structural checks, and surfaces disagreement between parsers as diagnostic signal. Use when the user asks about ATS parseability, text extraction, PDF parsing reliability, whether a resume variant breaks for ATSs, how the extraction gate works, running or debugging extraction-check, comparing extractor outputs, adding assertions, writing new broken fixtures, interpreting cross-extractor disagreement, or the text-extraction hypothesis at .claude/context/text-extraction-hypothesis.md. Keywords ATS, applicant tracking system, text extraction, PDF parsing, pdftotext, poppler, tika, Apache Tika, reading order, mojibake, cross-extractor, extraction check, regression gate, resume parser, parseability.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Extraction Check

Deterministic gate on `will_cygan_resume.pdf`. Shells to three open-source PDF-to-text parsers — `pdftotext`, `pdftotext -layout`, Apache Tika — that enterprise ATSs sit on, runs seven assertions on the output, and fails if any parser sees something structurally wrong.

The underlying hypothesis is in [`.claude/context/text-extraction-hypothesis.md`](../../context/text-extraction-hypothesis.md): text-extraction fidelity is the single highest-leverage ATS-side optimization, and real-world ATSs virtually all run on the same handful of open-source parsers. Beating those parsers is *equivalent* to passing ATS parsing at the file-format level.

## When to invoke this skill

- "Is this resume change safe for ATSs?" / "Will this parse cleanly?"
- "Why did extraction-check fail on [assertion X]?"
- "Run the extraction check" / "Compare what each extractor sees"
- "Add a new assertion / broken fixture / extractor"
- "How does the gate work?"
- "The CI Extraction Check job is failing — help me diagnose"
- Any mention of pdftotext, poppler, Tika, mojibake, reading order, or cross-extractor divergence

## Quickstart

```bash
just compile            # produce will_cygan_resume.pdf
just extraction-check   # run the 7-assertion gate on the compiled PDF
just test               # run the negative-fixture regression suite (6 pytest cases)
```

Prereqs on macOS: `brew install poppler tika typst`. CI installs pinned Tika 3.3.0.

## The seven assertions

| # | Name | What it checks |
|---|------|----------------|
| 1 | `1-non-empty` | Extracted text is >500 bytes (catches image-only or encoding-broken PDFs) |
| 2 | `2-section-order` | Declared section headers appear in the expected visual order |
| 3 | `3-name-contact` | Name and email are present, not glued together (ATS field-map footgun) |
| 4 | `4-job-contiguity` | Title / company / date-start / date-end co-occur within a 300-char window per job |
| 5 | `5-date-format` | At least one date range matches a consistent "Mon YYYY – …" format |
| 6 | `6-mojibake` | Zero replacement characters; no flagged smart-quote / em-dash characters |
| 7 | `7-cross-extractor` | All available extractors agree on section order and job count |

Assertion 7 is the canonical reading-order-scramble signal. When `pdftotext` says 2 jobs but `pdftotext -layout` says 1, the layout has a bug real ATSs will hit.

## Reading further

For anything deeper, read the relevant reference:

- [Architecture](references/architecture.md) — script layout, data model, how `evaluate_pdf` orchestrates parallel extractors
- [Running checks](references/running-checks.md) — local commands, CI workflow, interpreting output
- [Comparing outputs](references/comparing-outputs.md) — what each extractor tells you, resolving disagreement, manual cross-checks
- [Extending](references/extending.md) — adding an assertion, a new extractor, or a broken fixture; updating fixtures when the resume changes
- [Failure playbook](references/failure-playbook.md) — one entry per assertion: how failures look, root causes, how to fix

## Ground rules

- **Do not silently loosen an assertion to make it pass.** If the 300-char window fires on a legitimate layout, investigate the layout first. Adjust thresholds only with a commit-message reason.
- **Do not add a new extractor unless it represents a real ATS parser family.** `pypdf` / `pdfplumber` are Python-native and don't match ATS behavior — see the hypothesis spec for why.
- **The real resume is the ground truth for fixtures.** `scripts/extraction-check.fixtures.toml` is hand-maintained against `will_cygan_resume.typ`. When the resume gains a job or renames a section, update the TOML in the same commit.
- **Negative fixtures must fail cleanly.** Each broken `.typ` exists to prove one assertion fires. If a fixture trips multiple assertions unintentionally, tighten or split the fixture before shipping.
