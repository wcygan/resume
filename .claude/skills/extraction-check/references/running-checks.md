# Running Checks

## Local (macOS)

```bash
# One-time tool install
brew install poppler tika typst

# Per-run
just compile            # typst → will_cygan_resume.pdf
just extraction-check   # 7-assertion gate on the compiled PDF
just test               # pytest negative-fixture suite (6 cases)
```

Expected successful output of `just extraction-check`:

```
extraction-check: preflight...
Running 3 extractor(s) on .../will_cygan_resume.pdf...
[pdftotext] pdftotext .../will_cygan_resume.pdf -
[pdftotext -layout] pdftotext -layout .../will_cygan_resume.pdf -
[tika] tika --text .../will_cygan_resume.pdf
-- pdftotext --
  PASS 1-non-empty: 3412 bytes (threshold 500)
  PASS 2-section-order: all 4 headers in order
  PASS 3-name-contact: name+email within 66 chars
  PASS 4-job-contiguity: 2/2 jobs contiguous within 300 chars
  PASS 5-date-format: 2 date range(s) matched
  PASS 6-mojibake: clean
-- pdftotext -layout --
  ...
-- tika --
  ...
  PASS 7-cross-extractor: all 3 extractors agree (2 jobs)
extraction-check: PASS (pdftotext, pdftotext -layout, tika — 2 jobs, 4 sections)
```

Expected `just test`: `6 passed in ~3s`.

## CLI flags on the script

For ad-hoc testing against a non-default PDF (e.g., a variant):

```bash
uv run scripts/extraction_check.py \
    --pdf path/to/variant.pdf \
    --fixtures scripts/extraction-check.fixtures.toml \
    --report-dir /tmp/ext-report
```

Useful when experimenting with layout changes without committing them. The `--fixtures` flag is what lets the test suite point at `tests/fixtures/baseline.fixtures.toml` for the skeleton resumes.

## CI (GitHub Actions)

Workflow: `.github/workflows/extraction-check.yml`. Runs on push and PR to `main` / `master` as a **separate job** from `Compile Resume` so a red check tells you which gate failed without digging.

Steps:
1. `actions/checkout@v4`
2. `extractions/setup-just@v2` — `just` isn't preinstalled on Ubuntu runners.
3. `astral-sh/setup-uv@v4`
4. `typst-community/setup-typst@v4` (pinned `^0.13.0`)
5. `sudo apt-get install poppler-utils`
6. `actions/setup-java@v4` (Temurin 17)
7. `actions/cache@v4` keyed on `tika-app-${TIKA_VERSION}` (currently 3.3.0); if cache miss, `curl` the jar from `archive.apache.org`.
8. Export `TIKA_JAR=$HOME/.cache/tika/tika-app.jar` — the script's `detect_tika` probe picks this up.
9. `just compile` → `just extraction-check` → `just test`.
10. On failure, upload `.extraction/` as an artifact (14-day retention).

### Tika version pinning

`TIKA_VERSION` is a top-level env var in the workflow. Upgrades are deliberate — parser output can shift slightly across major versions, and pinning means an assertion-7 failure tells you *your resume* changed, not that Tika did. To upgrade:

1. Bump `TIKA_VERSION` in `.github/workflows/extraction-check.yml`.
2. Verify local `brew upgrade tika` matches.
3. Re-run `just extraction-check` locally — outputs may shift by a few bytes; that's fine if assertions still pass.
4. Commit with the version in the message.

## Interpreting output

**PASS with all 3 extractors agreeing** — ship. You are ATS-safe at the parsing layer.

**PASS with only 2 extractors (e.g., Tika skipped)** — the gate is incomplete locally. The script prints a skip message with install instructions. CI will exercise the full set.

**FAIL on any assertion** — the script exits 1 and writes `.extraction/report.md` with per-extractor breakdowns and the first 50 lines of each extractor's output. See the [failure playbook](failure-playbook.md) for how to diagnose each assertion.

**FAIL on assertion 7 (cross-extractor) but all other assertions pass** — the layout is ambiguous enough that different extractors see different structures. This is the canonical reading-order-scramble signal; layout almost certainly needs a fix before shipping.

## Where the report lands

On failure: `.extraction/report.md` at the repo root. The directory is gitignored. On PASS, the report is *not* written — stale reports from prior failures can be ignored or deleted.
