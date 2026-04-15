# Comparing Extractor Outputs

## Core principle

When two extractors disagree, **neither is "right"** — they're both correct for their own reading-order heuristic. The disagreement itself is the finding. Real ATSs run on one of these parsers, so if Workday's Tika-based path sees 1 job and Greenhouse's pdftotext path sees 2, both populations will hit your resume and one will be broken for them.

The goal is *convergence*: reshape the Typst source until all three extractors produce the same structural output.

## What each extractor emphasizes

| Extractor | Reading-order strategy | Breaks on |
|---|---|---|
| `pdftotext` (no flags) | Content-stream order (the order glyphs were drawn). Fast, naive. | Multi-column layouts — dumps left column entirely, then right. |
| `pdftotext -layout` | Spatial-order with whitespace preserved. Tries to reconstruct visual layout. | Overlapping frames, tight vertical spacing, `place()` reflow. |
| Apache Tika (PDFBox) | Heuristic reading order; may group by bounding box. | Unusual font subsetting, some ligatures, decorative glyphs. |

Typst's default layout is single-column with sequential content flow, which is why all three agree on the real resume — it's structurally the ATS happy path.

## Manually compare outputs

To eyeball what each extractor sees (outside the gate):

```bash
# Dump each extractor to a file
pdftotext will_cygan_resume.pdf /tmp/naive.txt
pdftotext -layout will_cygan_resume.pdf /tmp/layout.txt
tika --text will_cygan_resume.pdf > /tmp/tika.txt

# Diff them
diff /tmp/naive.txt /tmp/layout.txt | head -40
diff /tmp/naive.txt /tmp/tika.txt | head -40
```

Useful when assertion 7 fires and you want to see *where* they diverged. Three-way `diff3` is often overkill; pair-wise diffs are easier to read.

Also useful: the browser Cmd-A / Cmd-C / paste-into-plain-text trick. That's what most applicants can actually test. It usually matches Tika's output roughly (browser PDF viewers use similar heuristics), but is less precise than the CLI extractors.

## The canonical disagreement signals

| Symptom | Interpretation | Fix |
|---|---|---|
| `pdftotext`: N jobs, `-layout`: M ≠ N jobs | Content-stream order differs from visual order. Likely a `grid` or `place()` call producing out-of-order flow. | Linearize the affected block so DOM order matches visual order. |
| All three produce wildly different byte counts | Whitespace handling differs radically. Usually harmless *unless* assertion 4 window fires. | Check extraction output manually; adjust whitespace in source. |
| Tika missing text that pdftotext has | Font embedding or encoding issue that Tika's PDFBox can't decode. | Switch font, or disable problematic ligatures. |
| `pdftotext -layout` has garbled columns | Two-column layout with tight gutters. | Widen gutter, or switch to single column (the safe default). |

## The cross-extractor assertion in detail

`assert_cross_extractor` checks two things across all available extractors:

1. **Section order** — `section_order` captures the sequence of expected headers as they appeared. All extractors must produce the same sequence.
2. **Job count** — `job_count` is how many jobs satisfied assertion 4 (title + company + dates within a 300-char window). All extractors must match.

If either diverges, assertion 7 fails with a dict showing each extractor's output for the quantity that differed.

Note: assertion 7 auto-skips when fewer than 2 extractors are available locally. CI always has all 3, so the cross-check always runs there.

## Adding an independent sanity check

When debugging a tricky layout change, add an **outside-the-script** check:

```bash
# How many times does "Senior Software Engineer" appear in each extractor?
for cmd in "pdftotext will_cygan_resume.pdf -" \
           "pdftotext -layout will_cygan_resume.pdf -" \
           "tika --text will_cygan_resume.pdf"; do
    echo -n "$cmd: "
    eval "$cmd" | grep -c "Senior Software Engineer"
done
```

If one extractor reports 0 and the others report 1, you've isolated which parser family is broken by the current layout.

## Rule of thumb

If you catch yourself arguing which extractor is "correct", stop. The ATS running tomorrow is using one of the three. Make them all agree.
