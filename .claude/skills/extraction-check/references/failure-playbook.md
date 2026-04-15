# Failure Playbook

One entry per assertion: what the failure looks like, what it usually means, how to fix. Read the line numbers from `.extraction/report.md` to see which extractor's output triggered the failure.

## 1-non-empty

```
FAIL 1-non-empty: 142 bytes (threshold 500)
```

**What it means.** The PDF extracts to almost nothing. Almost always one of:

- PDF is image-only (scanned or Canva-exported without a text layer).
- Fonts are embedded in a way the extractor can't decode (subsetted with no ToUnicode mapping).
- PDF is somehow corrupt.

**Fix.** If you exported from something other than `typst compile`, re-export. If you're on `typst compile` and this trips, the font is the suspect — try switching to a standard font (Inter, Arial, Times) and recompiling.

## 2-section-order

```
FAIL 2-section-order: missing: ['Work Experience']
```
or
```
FAIL 2-section-order: order mismatch: found [('Projects', 412), ('Work Experience', 1204), ...]
```

**What it means.**

- *Missing* — the literal section-header string isn't in the extracted text. Either the resume renamed it (`"My Journey"` etc.) or it's not being rendered as text (e.g., styled as a vector shape).
- *Order mismatch* — the first-occurrence byte offsets are out of the declared order. This usually means a float/grid placed a later section before an earlier one in the content stream.

**Fix.** If renamed intentionally, update `expected_order` in the fixtures TOML. If visually correct but out of order in the extracted text, the layout is using `place()` or a `grid` in a way that reverses content-stream order — linearize the affected block.

## 3-name-contact

```
FAIL 3-name-contact: name+email glued at 42 — ATS field map hazard
```
or
```
FAIL 3-name-contact: name at 0, email at 380 (gap 380 > 200)
```

**What it means.**

- *Glued* — name and email appear as a single token with no whitespace between. Real ATSs will parse this as a single field and either the name or the email will be wrong in their database.
- *Gap exceeds window* — name and email are more than `contact_glue_window` bytes apart. Usually means a long contact block between them (address, multiple URLs) or that the header spans two visual rows with a lot of intervening text.

**Fix.**

- Glued: insert a linebreak or space between name and email in the Typst source. `#h(0.5em)` isn't always enough — a literal `\n` is safer.
- Gap: shorten the contact block, or accept the layout and widen `contact_glue_window` in the fixtures TOML with a commit-message rationale.

## 4-job-contiguity

```
FAIL 4-job-contiguity: 'Senior Software Engineer' @ 'LinkedIn' (March 2024Present): no 300-char window contained all four strings
```

**What it means.** For the named job, no 300-char slice of the extracted text contains all four of `title`, `company`, `date_start`, `date_end`. The extractor scrambled the job block — real ATSs will fail to associate this role with its employer or dates.

**Common causes.**

- Two-column layout (title left, company right) — naive pdftotext dumps columns sequentially.
- Dates placed in a header/footer region stripped by some extractors.
- A decorative separator (SVG, spacer) between title and company that grew too large.
- The TOML's `date_start` / `date_end` strings don't match what the extractor produces (em-dash vs en-dash vs hyphen).

**Fix.** Look at the `.extraction/report.md` — the first 50 lines of each extractor's output will show where the job block landed. If the strings are all present but farther apart than 300 chars, investigate the spacing. If one string is genuinely missing, it's a font-encoding or placement issue. Only widen the window as a last resort.

## 5-date-format

```
FAIL 5-date-format: no date range matched the allowed regex
```

**What it means.** No date range in the extracted text matches the month-name regex (`Mon YYYY – …`). Either dates are in numeric format (`01/2024`), abbreviated inconsistently, or missing entirely.

**Fix.** Standardize date format in the Typst source to `"Jan 2024 -- Present"` (Typst renders `--` as en-dash, which the regex accepts). If there's a legitimate reason for numeric dates, widen the regex in the TOML — but test with all 3 extractors because date normalization varies.

## 6-mojibake

```
FAIL 6-mojibake: U+FFFD x3 (forbidden)
```
or
```
FAIL 6-mojibake: U+2014 x2 (flagged)
```

**What it means.**

- *U+FFFD* (`�`) — replacement character. A glyph was drawn that the extractor couldn't decode. Font encoding issue.
- *U+2018/U+2019/U+201C/U+201D* — smart quotes. Typst or a copy-paste snuck them in. ATS parsers that do keyword search treat these as different characters than straight quotes.
- *U+2014* — em-dash. The repo uses en-dash for date ranges; em-dashes elsewhere in body text are flagged because they sometimes split tokens in parsers.
- *U+2013* — en-dash. Allow-listed. Only flagged if you removed it from `allowed_chars` by accident.

**Fix.**

- U+FFFD: switch font or disable the offending ligature. Rerun `just compile && just extraction-check`.
- Smart quotes: replace with straight quotes in Typst source. Typst's `set text(smartquote: false)` kills the auto-conversion globally.
- U+2014: replace with `--` (en-dash) or with a comma/colon.

## 7-cross-extractor

```
FAIL 7-cross-extractor: job count diverges: {'pdftotext': 2, 'pdftotext -layout': 1, 'tika': 2}
```
or
```
FAIL 7-cross-extractor: section order diverges: {...}
```

**What it means.** The extractors disagree on the document's structure. This is the reading-order-scramble signal and is usually triggered by:

- Two-column or multi-column layouts.
- `place()` absolute positioning that causes content-stream order to differ from visual order.
- Vertical spacing so tight that two lines overlap bounding boxes and one extractor groups them differently than another.

**Fix.** See [comparing-outputs.md](comparing-outputs.md) for the diagnostic workflow. Generally: reshape the layout until all three extractors produce the same structure. Single-column, sequential flow is the safe default.

### When assertion 7 fails but no per-extractor assertion does

This happens when each extractor individually produces a "plausible" output that satisfies assertions 1–6, but the extractors disagree on *which* plausible output is correct. This is the most diagnostic state — it means some real ATS will misread the resume and you don't know which. Always fix before shipping.

## When everything fails at once

If all 7 assertions fail, the problem is almost certainly upstream of extraction:

- Wrong PDF passed to `--pdf` (check the path).
- `typst compile` silently emitted an empty PDF (check stderr during compile).
- Fixtures TOML is missing or malformed (check `just extraction-check` preflight output).

Go to `.extraction/report.md` and look at the "First 50 lines of extracted text" section. If that's empty, it's a PDF problem, not a resume problem.
