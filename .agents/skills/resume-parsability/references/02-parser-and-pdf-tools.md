# Parser and PDF tools

Use multiple representations because each answers a different question. Keep
every raw output and record the exact versions used.

## Contents

- Prerequisites, version capture, and compilation
- Text, coordinate, and mechanical PDF views
- Rendering and raw-versus-canonical evidence
- Oracle and bounded-association checks

## Prerequisites and version capture

For a full local audit, require PATH-discoverable versions of:

- Typst;
- Apache Tika;
- Poppler: `pdfinfo`, `pdffonts`, `pdfimages`, `pdftotext`, `pdftohtml`,
  `pdftoppm`;
- qpdf; and
- `rg`.

Capture the environment before comparing runs:

```sh
typst --version
tika --version
pdfinfo -v
qpdf --version
uname -a
locale
```

Do not silently compare results produced by different compiler, font,
extractor, operating-system, or locale versions.

## Compile

Normal tagged export:

```sh
typst compile --root "$repo_root" "$source_typ" "$resume_pdf"
```

PDF/UA-1 comparison:

```sh
typst compile --root "$repo_root" --pdf-standard ua-1 \
  "$source_typ" "$resume_pdf"
```

Use `--no-pdf-tags` only for an explicit negative control. Typst tags PDFs by
default, and disabling tags removes structural evidence while plain text may
remain.

## Text and coordinate views

```sh
pdftotext "$resume_pdf" "$evidence_dir/poppler-plain.txt"
pdftotext -layout "$resume_pdf" "$evidence_dir/poppler-layout.txt"
pdftohtml -xml -hidden -i -stdout "$resume_pdf" \
  > "$evidence_dir/poppler.xml"
tika -t "$resume_pdf" > "$evidence_dir/tika.txt"
tika -x "$resume_pdf" > "$evidence_dir/tika.xhtml"
```

Interpret them as follows:

| View | Useful signal | Does not prove |
| --- | --- | --- |
| Poppler plain | Linear/content-stream text and coarse order | Visual column reconstruction or ATS behavior |
| Poppler `-layout` | Spatial grouping and visual whitespace | Semantic field relationships |
| Poppler XML | Coordinates, runs, and decoded text nodes | One universal reading order |
| Tika text | Independent Java-family extraction order | A named ATS implementation |
| Tika XHTML | Tika markup plus extracted text | Correct PDF semantic tags or link annotations |

Extractor disagreement is evidence of portability risk. Do not select the
output that best matches expectations and discard the rest.

Tika plain text may append link-annotation destinations after the page that
contains them. The block is terminal for a one-page PDF but can precede later
page text. Preserve the full raw output. Only when exactly one contiguous block
matches the reviewed URI sequence should the evaluator remove those annotation
lines from visible-body field counts and report the block as its own link
signal. Reject duplicate blocks; do not delete arbitrary URLs or use this
separation to conceal a duplicated visible value.

## Mechanical PDF audit

```sh
pdfinfo "$resume_pdf" > "$evidence_dir/pdfinfo.txt"
pdffonts "$resume_pdf" > "$evidence_dir/pdffonts.txt"
pdfimages -list "$resume_pdf" > "$evidence_dir/pdfimages.txt"
qpdf --check "$resume_pdf" > "$evidence_dir/qpdf-check.txt" 2>&1
qpdf --json "$resume_pdf" > "$evidence_dir/qpdf.json"
qpdf --qdf --object-streams=disable "$resume_pdf" \
  "$evidence_dir/qpdf-qdf.pdf"
rg -a -n '/StructTreeRoot|/MarkInfo|/S /H1\b|/S /H2\b|/S /L\b|/S /Lbl\b|/S /LBody\b|/S /Table\b|/S /TR\b|/URI\b' \
  "$evidence_dir/qpdf-qdf.pdf" \
  > "$evidence_dir/structure-and-links.txt" || true
```

Treat the grep as an inventory, not an exact assertion. Parse the actual `/URI`
values from QDF or qpdf JSON and compare their sorted multiset with the oracle;
mere `/URI` presence cannot prove the intended destinations or counts.

Check:

- intended page count, size, and zero rotation;
- `Tagged: yes` when semantic structure is expected;
- all fonts embedded with Unicode mappings;
- no unexpected raster images;
- qpdf syntax and stream integrity;
- `StructTreeRoot` and `MarkInfo`;
- expected H1/H2 and native list tags;
- table tags only when a table was intentionally used; and
- the exact expected URI multiset, not merely "some links exist."

QDF tag presence demonstrates PDF structure. It does not certify ATS mapping or
screen-reader behavior.

## Render and inspect

Render all pages at a stable resolution:

```sh
pdftoppm -png -r 144 "$resume_pdf" "$evidence_dir/render"
```

Inspect the latest images for clipping, overlap, bad wraps, ambiguous columns,
detached bullet markers, broken glyphs, page splits, and visual order. A clean
render cannot prove clean extraction, and clean extraction cannot prove a
clean render.

## Raw and canonical evidence

Raw output is authoritative. Save it byte-for-byte before normalization.

A secondary canonical diagnostic view may:

1. normalize Unicode to NFC; and
2. collapse runs of whitespace.

It must retain soft hyphens, punctuation, zero-width characters, icon tokens,
replacement characters, and URLs. Do not repair words or reorder lines.

Use the canonical view to distinguish harmless line wrapping from missing or
reordered content. Never use it to conceal a raw failure.

## Oracle and association checks

Define before extraction:

- every key field expected exactly once;
- the expected global order;
- expected link destinations; and
- bounded windows for each present section and record, including Profile,
  jobs, Projects, education, and skills.

For each bounded window:

1. start at the first canonical field for the entity;
2. stop at the next entity or section boundary;
3. require every expected field exactly once inside the segment; and
4. require the fields in the declared order.

This catches a resume where every word exists but a title is attached to the
wrong employer or date range.
