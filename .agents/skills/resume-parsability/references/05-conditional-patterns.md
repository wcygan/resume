# Conditional patterns

These choices are not universally forbidden, but they require direct evidence
for the actual source, compiler, font, and extractor versions. Do not use them
as the default golden baseline.

## Two-column layouts

The controlled two-column specimen placed real content in both columns.
Canonical linear views retained fields and associations locally, while raw
phrases fragmented and Poppler layout followed the visual columns. Greenhouse
also lists columned layouts as a formatting risk.

Decision: use one column when portability matters. If two columns are required,
test every record across raw and canonical views and classify the result at
most Conditional unless external UAT supports more.

## Tables and grids

- A semantic skills table retained local associations and emitted Table/TR
  tags, but Greenhouse warns about complex tables.
- A grid used for job metadata failed local bounded associations.

Decision: a small skills table can be Conditional after direct validation.
Do not use a grid or table to divide one job record into spatial cells without
an oracle proving correct order and relationships.

## Styled labels instead of headings

Bold section labels can extract as readable text but omit H structure.

Decision: prefer real headings. If visual constraints require styled labels,
report text extraction separately from lost semantics.

## Literal bullets

Six literal bullet markers remained attached to their bodies across the tested
views and render, but they produced no L/Lbl/LBody tags. The full-resume
variant also failed a Poppler metadata association gate because of an adjacent
layout interaction.

Decision: use native lists. Do not claim that literal bullet semantics alone
caused or prevented a full-resume result.

## Automatic hyphenation

The paired probe showed engine-specific representations of the same wrapped
word:

- Poppler plain: soft hyphen plus a line break;
- Poppler XML: a visible hyphen;
- Tika: two fragments without a hyphen.

Decision: keep `hyphenate: false` for dense resumes unless the exact wrapped
keywords pass every extractor and platform gate.

## Flexible horizontal spacing

`#h(1fr)` passed in the tested golden resume when each job used one metadata
row: company and role on the left, then a single labeled `Dates:` and
`Location:` unit on the right. The same spacer used across two independent
company/date and role/location rows triggered Poppler column grouping. A
similar right-aligned education date escaped its intended section in an
earlier construction.

Decision: constrain flexible spacing to the exact tested component, labels,
font sizes, and content lengths. Re-test after any font or wording change. Keep
education and other short records in adjacent normal flow.

## Absolute placement whose local order happens to pass

One absolute-layout variant preserved the local canonical order, while the
paired conflict probe demonstrated that Poppler and Tika can choose opposite
orders.

Decision: local success does not make absolute placement a portable baseline.
Treat it as Conditional and prefer normal flow.

## PDF/UA-1

The PDF/UA-1 build retained local text and structural gates. This is useful,
but it is not ATS or assistive-technology certification.

Decision: use PDF/UA-1 when the document satisfies its requirements and the
toolchain supports it. Keep the external ATS and accessibility layers marked
Untested until separately verified.

## Fonts, ligatures, and decorative separators

These may be safe or unsafe depending on actual font mappings and extraction.
Treat them as Conditional when they introduce:

- missing Unicode mappings;
- replacement or Private Use Area characters;
- broken keyword round-trip;
- unexpected separator tokens; or
- different line wrapping across environments.

Prefer simple text separators and fonts proven embedded with Unicode mappings.
