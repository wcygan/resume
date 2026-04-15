# Spec: Text Extraction as the ATS Optimization Target

Status: **Proposed — not yet implemented.**
Owner: Will Cygan
Last reviewed: 2026-04-14

## Hypothesis

**If closed-source ATS systems run LLMs or rule-based extractors on top of a plain-text dump from open-source PDF parsers, then the only failure mode a Typst-generated resume can realistically introduce is bad text extraction — specifically scrambled reading order, lost characters, or merged fields.**

Therefore, the entire ATS-side optimization surface reduces to one question:

> When three different open-source PDF-to-text extractors read `will_cygan_resume.pdf`, do they all produce a clean, contiguous, reading-order text stream with section headers, job titles, companies, and dates intact?

If the answer is yes across all three, the downstream ATS (whether it runs Tika + regex, Tika + LLM, or Tika + Workday's proprietary field mapper) has no remaining failure modes to trip on. If any extractor disagrees structurally, the PDF has a layout bug that will silently break for some real ATSs.

### What this hypothesis rejects

This spec explicitly **does not** pursue:

- Semantic similarity scoring (embedding cosine) — no ATS ground truth, high Goodhart risk.
- Keyword coverage percentages — reproduces the Jobscan keyword-stuffing failure mode.
- Match-score dashboards (Jobscan, Resume Matcher, Affinda) — marketing-grade numbers with no mechanistic link to callback rates.
- Structured-field extraction parsers (Affinda, Sovren, Textkernel) — they measure a layer downstream of what we can actually control in Typst.

Those are measuring the wrong thing. They optimize for a proxy that doesn't compose with the human reviewer step that actually decides callbacks.

### What this hypothesis asserts

- The `ats-parser` persona reads `.typ` source, not compiled bytes — it cannot verify extraction.
- The `resume-tailor-panel` skill covers qualitative JD gap analysis — it does not verify extraction either.
- A regression gate on real-parser output is the one piece of infrastructure neither persona nor skill can replace.
- Parseability is a property of the **Typst template and layout**, not of individual bullet edits. The check needs to fire on template/compiler/font changes, not on every bullet rewrite.

### Supporting evidence

- Web research (see prior session): enterprise ATSs overwhelmingly use Apache Tika / PDFBox / Poppler under the hood. No mainstream ATS ships a custom PDF renderer.
- Textkernel's own blog: reading-order ML takes column-gap correctness from 82% → 91%. Reading order is *the* failure mode, not character extraction.
- Practitioner reports: "semantic AI" is marketing; real recruiter search is boolean keyword lookup against extracted text.
- Independent tester with 15k-resume pipeline: two-column layouts produced `"Java XYZ Engineering College"` from left-column skills + right-column education. Not hallucination — spatial scramble.

## Methodology

A single `uv`-run Python script, `scripts/extraction_check.py` (PEP 723 inline metadata, no venv or `pyproject.toml` — matches `scripts/dev.py` and `scripts/run-local-ci.py`), exposed as `just extraction-check` and invoked from `just ci`.

### Extractors under test

Three heterogeneous open-source PDF-to-text engines, chosen because they represent the dominant parsing families real ATSs use:

| # | Extractor | Family | Invocation | Install |
|---|-----------|--------|------------|---------|
| 1 | `pdftotext` (Poppler) without flags | Linear content-stream dump | `pdftotext will_cygan_resume.pdf -` | `brew install poppler` |
| 2 | `pdftotext -layout` | Layout-preserving, visual-order | `pdftotext -layout will_cygan_resume.pdf -` | same as above |
| 3 | Apache Tika | JVM parser used by most enterprise ATSs | `java -jar tika-app.jar --text will_cygan_resume.pdf` | `brew install tika` (or pinned `.jar`) |

Rationale for the set:
- `pdftotext` (naive) models the cheap path many ATSs take.
- `pdftotext -layout` models visual-order extraction — different failure modes than naive.
- Tika models the JVM-enterprise path (PDFBox under the hood) that Workday, Greenhouse, and other enterprise ATSs most plausibly sit on.

Disagreement across the three is diagnostic. Agreement across the three is the pass signal.

### Assertions the script must run

For each extractor output, assert in order:

1. **Non-empty extraction**
   - Extractor returned >500 bytes of text. Catches image-only or encoding-broken PDFs.

2. **Standard section headers present, in order**
   - Expected: `Experience` (or `Professional Experience`), `Education`, `Skills`, `Projects` — whatever the current Typst source declares.
   - Order must match the visual order of the resume. Out-of-order sections indicate column/float scramble.

3. **Candidate name and contact line intact on a single line near the top**
   - `Will Cygan` appears in the first 400 bytes.
   - Email appears on the same or adjacent line. If `wcygan.io@gmail.com` gets glued to the name (`Will Cyganwcygan.io@gmail.com`), that's a known ATS field-mapping footgun — fail.

4. **Every job block extracts as a contiguous `Title / Company / Dates` triple**
   - For each `work-experience/*.md` source, confirm the role's title string, company string, and date range all appear within a 300-character window of each other in the extracted text.
   - A title appearing 2kB away from its company indicates reading-order scramble.

5. **Date format consistency**
   - All date ranges match a single regex (e.g., `/(Jan|Feb|.../) \d{4} [–-] (Present|(Jan|Feb|...) \d{4})/`).
   - Mixed formats cause ATS experience-duration miscalculation.

6. **No replacement characters or mojibake**
   - Zero occurrences of `\uFFFD` (`�`) in output. Catches font-encoding failures.
   - Zero smart quotes (`\u2018`, `\u2019`, `\u201C`, `\u201D`) or em/en dashes (`\u2013`, `\u2014`) unless explicitly allow-listed.

7. **Cross-extractor structural agreement**
   - Section-header order is identical across all three extractors.
   - Job-block count is identical across all three.
   - If any two extractors disagree on (2) or (4), fail with a diff showing where they diverge.

### Output format

On success: single-line summary, exit 0.

```
extraction-check: PASS (pdftotext, pdftotext -layout, tika — 4 jobs, 4 sections, no mojibake)
```

On failure: per-extractor breakdown to stdout, non-zero exit, and a `.extraction/report.md` with:
- Side-by-side text output from each extractor (first 50 lines).
- Which assertion failed and for which extractor.
- The specific bytes or regex that mismatched.

`.extraction/` is gitignored. No persistent storage of runs — this is a gate, not telemetry.

### Integration points

1. **`just extraction-check`** — new recipe in `justfile` that runs `uv run scripts/extraction_check.py`.
2. **`just ci`** — `scripts/run-local-ci.py` invokes `extraction_check.py` after `typst compile`. CI fails if extraction fails. (Either chain inside `run-local-ci.py` directly, or make the `ci` recipe a composite: `just compile && just extraction-check && uv run scripts/run-local-ci.py`. Pick one during implementation — see open questions.)
3. **GitHub Actions** — add Tika + Poppler to the workflow (both are small and cacheable). Gate PDF artifact upload on a passing extraction check. Python + `uv` is already available via `astral-sh/setup-uv@v3` if not already installed.
4. **No changes to `.claude/agents/ats-parser.md`** for now. The persona continues to review the `.typ` source qualitatively; this script handles the one thing the persona structurally cannot do.

### Explicit non-goals

- No variants matrix. There is one resume.
- No JD matching. `resume-tailor-panel` covers JD-specific qualitative review.
- No scoring. Pass/fail only.
- No persistent run history. The check is idempotent and its output is the compiled PDF itself.
- No Resume Matcher, no Affinda, no Ollama, no Qdrant, no embeddings.

## Decision rule

A change to `will_cygan_resume.typ` ships iff `just ci` passes, which requires `extraction-check` to pass. That's the entire rule.

If Tika and `pdftotext` disagree on job-block boundaries, something in the layout is brittle — likely a `grid` or `place()` call introducing positional ambiguity. Fix the Typst source, not the assertion.

## Out-of-scope future extensions (do not implement without re-review)

Listed only to document why they were considered and rejected at this spec's scope:

- **Per-commit extraction diff** — track extraction text byte-diff across commits. Would be telemetry; rejected as scope creep until a concrete use case emerges.
- **JD keyword smoke test** — "given a JD, does the extracted text contain the top-10 required terms verbatim?" — useful but duplicates what `resume-tailor-panel` does with richer judgment. Reconsider only if the panel becomes too expensive to run per JD.
- **OCR fallback check** — run the PDF through Tesseract and compare. Only relevant if we start generating image-heavy PDFs, which Typst does not.

## Open questions to resolve before implementation

1. **Tika packaging**: ship a pinned `tika-app.jar` in-repo (hermetic, ~70MB) or require `brew install tika` as a dev dependency (not hermetic, small setup friction)? Hermetic is better for CI reproducibility.
2. **macOS vs Linux CI parity**: confirm `pdftotext` and Tika produce byte-identical output on both. If not, pin the CI runner to one OS and document.
3. **Expected-content fixtures**: the assertions above reference specific strings (name, email, section headers). Where does the "expected" list live? Options: hard-coded in `extraction_check.py`, separate `extraction-check.fixtures.toml` alongside the script, or derived from parsing the `.typ` source. Derivation is brittle; a fixtures file is explicit and diff-reviewable.
4. **Failure verbosity**: on CI, how much of the extracted text do we dump on failure? A 50-line head seems reasonable; full dumps pollute PR comment threads.
5. **`just ci` composition**: wire `extraction-check` inside `scripts/run-local-ci.py` as an additional step, or chain it as a separate `just` dependency? Chaining in `justfile` keeps each Python script single-purpose; embedding in `run-local-ci.py` keeps one CI entry point. Minor, but pick one.
6. **Python deps via PEP 723**: `pypdf` or `pdfplumber` would avoid shelling to `pdftotext`, but the point is to exercise the *same* extractor real ATSs use — `pdftotext` via `subprocess` is deliberate. Confirm we stay on subprocess and only use Python-native libraries for orchestration + Tika/Poppler output diffing.

Resolve these four before writing code.
