# Bad patterns

Avoid these as resume baselines. Some are direct local failures; others are
vendor-documented risks or defects found in the broader challenge corpus.

## Directly observed local failures

### Split two-row job metadata

Authoring one row as title/location and a second as employer/date can produce a
visually elegant entry whose serialized order conflicts with a structured
field oracle. The controlled specimen failed its association windows.

Important attribution: that specimen was authored in the problematic order.
Do not misreport the result as an extractor independently inventing the order.

### Two independently right-aligned metadata rows

In a later controlled follow-up, normal-flow company/date and role/location
rows looked correct and Tika retained each visual row, but Poppler plain text
grouped the repeated left and right edges as separate columns. Grid, table, and
inline placement variants did not fix that disagreement. Adding labels to both
right-side rows also did not prevent one job's first bullet from appearing
before its right-side fields in Poppler plain.

Do not treat normal flow alone as proof that a repeated two-edge layout has a
stable linear order. If flush-right dates and locations are required, test a
single labeled right-side unit before accepting two persistent metadata rows.

### Grid-based job metadata

A row-major layout grid contained every field once but failed raw and canonical
bounded associations. A layout container is not automatically a semantic
record.

### Contact data in a PDF page header

The controlled page-header specimen lost a visible contact label and URI
annotation in the tested views. Do not keep the only copy of name, email,
phone, or profile links in a page header, footer, or floating text box.

### Absolute placement

When source order and coordinates conflicted, Poppler and Tika chose different
orders. Avoid `place` or equivalent absolute positioning for canonical resume
facts.

### Hidden or duplicate canonical text

Invisible duplicate facts contaminate counts and can cause one field to map to
multiple records. Never add hidden name, company, contact, title, date, or
keyword text to influence a parser.

### Disabling PDF tags

`--no-pdf-tags` preserved plain text while removing `StructTreeRoot` and
`MarkInfo`. Readable text is not a substitute for semantic document structure.

## Profile and project anti-patterns

Avoid a generic Profile that merely repeats the headline, restates obvious
experience, or supplies unsupported claims such as "world-class," "expert," or
"results-driven." Keyword stuffing at the top adds tokens without adding
evidence and can cause both people and models to over-weight self-description.

Avoid decorative project cards, occupied sidebars, grids, or multiple columns
for canonical project facts. Do not split a project name, descriptor, focus,
dates, link, and bullets into independently positioned regions. Do not include
tutorial exercises or projects that merely duplicate stronger employment
evidence when the page space would be better spent on material accomplishments.

Profile and Projects do not become valuable merely because a page has room.
Each section needs a distinct editorial purpose and its own bounded extraction
window.

## Text-layer defects found in the challenge corpus

- U+FFFD replacement characters from icon or font failures.
- Private Use Area glyphs from icon fonts.
- Zero-width characters embedded in otherwise normal words.
- Manual word splits and soft-hyphen fragments.
- Duplicate link annotations or repeated URI trailers.
- URI trailers inserted between logically related body records.
- Malformed visible URLs with spaces between tokens.
- Date, title, or company tokens serialized before the record they describe.

Do not remove a detector merely because one operating system hides the
character. Test exact keyword round-trip and compare multiple extractors.

## Vendor-documented risks

Greenhouse warns about:

- image resumes;
- graphics, photos, and word art;
- spaces between letters;
- complex tables, headers, and footers;
- contact information in a header, footer, or text box;
- columned layouts;
- unclear sections and inconsistent formatting;
- company names without identifying terms; and
- incomplete job titles.

It also says it cannot parse resumes larger than 2.5 MB. Attribute these limits
and warnings to Greenhouse rather than presenting them as universal parser
laws.

## Invalid remediation strategies

- Do not repair extractor output and call the PDF fixed.
- Do not remove punctuation, URLs, zero-width characters, or soft hyphens from
  the acceptance view to manufacture a pass.
- Do not loosen association windows before checking whether the layout is
  wrong.
- Do not select one favorable extractor and ignore a disagreeing view.
- Do not convert the resume to a screenshot or full-page background image.
- Do not add invisible keyword stuffing or duplicate facts.
- Do not claim a vendor pass from Tika or Poppler alone.
