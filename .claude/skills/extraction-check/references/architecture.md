# Architecture

## Files

| Path | Role |
|---|---|
| `scripts/extraction_check.py` | Single Python file (PEP 723 inline metadata, stdlib only). Contains everything — the extractors, the 7 assertions, orchestration, reporting, and CLI. |
| `scripts/extraction-check.fixtures.toml` | Expected strings for the real resume. Hand-maintained against `will_cygan_resume.typ`. |
| `tests/conftest.py` | Session-scoped pytest fixtures: compile-on-demand for broken Typst sources, in-process caller of `evaluate_pdf`. |
| `tests/test_extraction_check.py` | 6 tests: 1 baseline sanity + 5 negative fixtures. |
| `tests/fixtures/broken/*.typ` | Minimal Typst sources each engineered to trip exactly one assertion. |
| `tests/fixtures/baseline.fixtures.toml` | Expected strings for the tiny skeleton resumes used in tests (separate from the real resume's fixtures). |
| `.github/workflows/extraction-check.yml` | Separate CI job (not chained into Compile Resume) so the reason for a red CI is legible at a glance. |

## Data model

```python
class Assertion(StrEnum):  # source of truth for the 7 assertion names
    NON_EMPTY, SECTION_ORDER, NAME_CONTACT, JOB_CONTIGUITY,
    DATE_FORMAT, MOJIBAKE, CROSS_EXTRACTOR

@dataclass
class Extractor:
    name: str            # "pdftotext", "pdftotext -layout", "tika"
    argv: list[str]      # command to run; output captured from stdout

@dataclass
class AssertionResult:
    ok: bool
    name: Assertion
    detail: str          # human-readable explanation

@dataclass
class ExtractorResult:
    extractor: str
    text: str            # raw stdout from the extractor
    results: list[AssertionResult]
    section_order: list[str]  # headers as they appeared, for cross-check
    job_count: int            # matched jobs, for cross-check

@dataclass
class EvaluationResult:
    results: list[ExtractorResult]
    cross: AssertionResult     # assertion 7
    skipped: list[str]         # skipped extractors with install instructions
    def ok(self) -> bool
    def any_fails(self, Assertion) -> bool   # tests call this
```

## Control flow

`evaluate_pdf(pdf, fx)` is the single entry point used by both the CLI and the pytest suite:

1. `build_extractors(pdf)` probes the machine — returns available extractors + a skip list with install hints for what's missing.
2. `ThreadPoolExecutor(max_workers=N)` runs `evaluate(extractor, fx)` concurrently. Tika JVM startup (~2s) parallelizes with pdftotext (~10ms) instead of serializing.
3. `evaluate` runs the 6 per-extractor assertions in order, capturing `section_order` and `job_count` for the cross-check.
4. `assert_cross_extractor(results)` compares section order + job count across extractors (skipped automatically when fewer than 2 are available).
5. Returns an `EvaluationResult`. CLI `main()` prints human output; tests inspect the structured result directly.

## Why three extractors, why these three

| Extractor | ATS family it models |
|---|---|
| `pdftotext` (Poppler, no flags) | Cheap-path enterprise parsers; naive content-stream dump |
| `pdftotext -layout` | Layout-aware enterprise parsers (Workday-class) |
| Apache Tika | JVM-based enterprise ATSs that embed PDFBox under the hood |

Python-native alternatives (`pypdf`, `pdfplumber`) are deliberately excluded. No enterprise ATS ships Python, and `pypdf` has its own reading-order quirks that don't match the parsers real ATSs run.

## Tika detection (why four code paths)

`detect_tika(pdf)` probes in this order:

1. `TIKA_JAR` env var (used by CI — pinned jar at a cached path)
2. `tika` command on PATH (Homebrew's `tika` formula)
3. `template/tika-app.jar` in-repo (hermetic fallback if vendored)
4. `/opt/homebrew/opt/tika/libexec/tika-app.jar` (Homebrew's libexec)

First hit wins. All paths end up invoking the same jar; differs only in whether we shell `tika --text` or `java -jar <jar> --text`.

## Fixtures TOML

Two fixtures files exist and serve different consumers:

- `scripts/extraction-check.fixtures.toml` — the **real resume's** expected strings. Used by `just extraction-check`.
- `tests/fixtures/baseline.fixtures.toml` — expected strings for the **skeleton resumes** in `tests/fixtures/broken/`. Used by `just test`.

They must stay in sync structurally (same TOML keys). If you add a TOML section to one, add it to the other.
