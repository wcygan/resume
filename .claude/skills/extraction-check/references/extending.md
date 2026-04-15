# Extending

Three extensions you might want: a new assertion, a new extractor, a new broken fixture. Plus: keeping the fixtures TOML current when the real resume changes.

## Add a new assertion

1. Add an enum member:
   ```python
   # scripts/extraction_check.py
   class Assertion(StrEnum):
       ...
       LINK_INTEGRITY = "8-link-integrity"  # whatever you're checking
   ```

2. Write an `assert_<name>(text, ...) -> AssertionResult`:
   ```python
   def assert_link_integrity(text: str, expected_links: list[str]) -> AssertionResult:
       missing = [l for l in expected_links if l not in text]
       if missing:
           return AssertionResult(
               ok=False, name=Assertion.LINK_INTEGRITY,
               detail=f"missing links: {missing}",
           )
       return AssertionResult(
           ok=True, name=Assertion.LINK_INTEGRITY,
           detail=f"all {len(expected_links)} links present",
       )
   ```

3. Register in `evaluate()`:
   ```python
   er.results.append(assert_link_integrity(text, fx["links"]["expected"]))
   ```

4. Add the fixture data to **both** fixtures TOML files (real and test baseline):
   ```toml
   [links]
   expected = ["github.com/wcygan", "..."]
   ```

5. Add a negative fixture that trips it (see "Add a broken fixture" below), and a test in `tests/test_extraction_check.py`.

### Rule: assertions must be falsifiable

If the broken fixture you'd write to trip the new assertion is so contrived it would never happen in practice, the assertion isn't pulling its weight. Don't add it.

## Add a new extractor

Extractors are declared in `build_extractors(pdf)`. Add yours:

```python
if shutil.which("my-extractor"):
    avail.append(Extractor("my-extractor", ["my-extractor", str(pdf)]))
else:
    skipped.append("my-extractor: missing. Install with ...")
```

Three rules:

1. **It must model a real ATS parser family.** Check the hypothesis spec in `.claude/context/text-extraction-hypothesis.md`. Python-native parsers (`pypdf`, `pdfplumber`) are off the table — they don't match enterprise ATS behavior.
2. **It must exit non-zero on error.** `run_extractor` raises `RuntimeError` if the subprocess returns non-zero; honor that contract.
3. **It must print the extracted text to stdout.** Tool-specific output formats (JSON, XML, …) need a normalizer before becoming the captured `text`. Keep the normalizer small and local to `run_extractor`.

Once added, assertion 7 automatically includes it in the cross-extractor check.

## Add a new broken fixture

Negative fixtures prove the assertions actually fire. To add one:

1. **Start from the baseline.** Copy `tests/fixtures/broken/baseline.typ` to `tests/fixtures/broken/<name>.typ`.
2. **Mutate exactly one thing** to trip the target assertion.
3. **Add a one-line `// BROKEN: ...` header** describing the mutation. Don't rehash which assertion it trips — the test name says that.
4. **Add the test in `tests/test_extraction_check.py`:**
   ```python
   def test_my_defect_fails_section_order(
       broken_pdf, run_check, require_pdftotext, require_tika,
   ):
       ev = run_check(broken_pdf("my-defect"))
       assert_only_fails(ev, ec.Assertion.SECTION_ORDER)
   ```
5. **Run `just test`**. If collateral assertions trip, tighten the fixture or use `allow_collateral=frozenset({Assertion.X})` to document the expected collateral.

### Clean isolation is better than fewer fixtures

Five fixtures that each trip exactly one assertion are more debuggable than three fixtures that each trip several. Prefer splitting over combining.

## Updating fixtures when the resume changes

`scripts/extraction-check.fixtures.toml` is the expected-strings contract for `will_cygan_resume.typ`. When the resume gains a job, renames a section, or changes contact info, update this file **in the same commit**.

The TOML sections:

- `[candidate]` — name, email. Only these drive assertion 3 today.
- `[sections] expected_order` — the list of level-1 headers in visual order.
- `[[jobs]]` — one table per job. Title, company, date_start, date_end must each appear verbatim in extracted text within 300 chars of the title.
- `[dates] allowed_range_regex` — the regex assertion 5 uses. Widen only with reason.
- `[thresholds]` — `min_bytes`, `name_head_bytes`, `contact_glue_window`, `job_block_window_chars`.
- `[mojibake]` — `forbidden_chars` (always fail), `flagged_chars` (fail if present), `allowed_chars` (override flagged).

### Common update patterns

| Resume change | TOML update |
|---|---|
| New job added | Append a `[[jobs]]` block. Re-run `just extraction-check`. |
| Job dates changed | Update `date_start` / `date_end` on the matching block. |
| Section renamed | Update `expected_order`. Confirm new name is grep-able in extracted text. |
| Contact email changed | Update `[candidate].email`. |
| New section added (e.g., Publications) | Append to `expected_order` in visual-order position. Optionally add a new assertion for its content. |
| Switched to an em-dash in body (not just dates) | Add the em-dash to `allowed_chars` — but reconsider; em-dash may mojibake in some extractors. |

Run `just extraction-check` after every TOML edit. If it passes, the fixtures are in sync.

## Updating the baseline skeleton for tests

If the **test** baseline (`tests/fixtures/broken/baseline.typ` + `tests/fixtures/baseline.fixtures.toml`) drifts from assumptions in the assertion logic, update the TOML similarly. Baseline skeleton stays minimal — don't mirror the real resume's content. Its job is to compile cleanly and satisfy all 7 assertions with a 3-section, 2-job shape.
