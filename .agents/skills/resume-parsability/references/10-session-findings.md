# August 2026 session findings

This reference preserves the empirical findings that motivated the general
rules. It is a local Typst/PDF study, not a vendor certification.

## Environment and method

The final controlled run used:

- Typst 0.14.2;
- Apache Tika 3.3.0;
- Poppler 26.03.0;
- qpdf 12.3.2;
- Python 3.12.12 via uv 0.11.16;
- macOS/Darwin arm64 with `C.UTF-8` locale; and
- 144-DPI rendered inspection.

The suite held synthetic facts constant, varied one primary source/export
pattern, preserved raw evidence, used a secondary NFC-plus-whitespace view,
and tested five bounded association windows: three jobs, education, and skills.

## Controlled results

| Pattern | Observed result | Status |
| --- | --- | --- |
| Semantic normal flow | All text, order, association, structure, font, image, link, qpdf, and render gates passed | Pass |
| Semantic normal flow without tags | Text survived; StructTreeRoot and MarkInfo disappeared | Fail |
| Semantic normal flow with PDF/UA-1 | Local text and mechanical gates held; external behavior untested | Conditional |
| Bold-only section labels | Text held; heading semantics absent | Conditional |
| Literal manual bullets | Six markers stayed attached and lacked list tags; adjacent Poppler metadata association failed | Fail |
| Grid job metadata | Fields existed once; raw and canonical association windows failed | Fail |
| Split two-row metadata | Authored title/location then employer/date order violated the oracle | Fail |
| Skills table | Local associations held and Table/TR appeared | Conditional |
| Two occupied columns | Canonical linear views held locally; raw phrases fragmented and layout view followed columns | Conditional |
| Contact in page header | A visible label and URI were lost locally | Fail |
| Hyphenation enabled | Full resume held canonically; paired probe showed engine-specific word fragments | Conditional |
| Absolute layout with locally logical source | Canonical gates held locally; placement remained extractor-dependent | Conditional |
| Conflicting absolute coordinates | Poppler and Tika selected different orders | Fail |
| Hidden key-field duplicates | Six canonical keys duplicated in Poppler plain | Fail |
| Hyphenation-off micro-probe | Target word remained intact | Pass |
| Hyphenation-on micro-probe | Soft hyphen, visible hyphen, and split-without-hyphen appeared by engine | Conditional |
| Absolute coordinate-order probe | Poppler read coordinate order; Tika read source order | Fail |

Final count: 2 Pass, 7 Conditional, and 8 Fail.

## Golden baseline

The compiled golden resume used:

- one narrative column;
- repository-pinned Source Sans 3 Regular, Bold, and Italic cuts;
- true headings and native lists;
- body-held contact links with canonical, human-readable display text;
- one normal-flow experience metadata row with company and role on the left;
- one labeled `Dates:` and `Location:` unit flush-right on that row;
- labeled flow skills;
- education date in adjacent normal flow;
- hyphenation disabled;
- no images, tables, columns, page-header contact, absolute placement, or
  hidden text; and
- PDF/UA-1 export.

It was one 612 x 792 pt Letter page, rotation zero, tagged, qpdf-clean,
image-free, and used embedded Unicode-capable fonts. H1, H2, native list, and
link structures were present. The initial artifact's four expected URI
annotations matched
exactly. Poppler plain/layout, Tika, and decoded XML each retained every oracle
field once and passed all five bounded windows. Fresh PDF bytes were not treated
as deterministic because generated metadata may vary; extracted content and
structure were compared instead.

The final font selection promoted Source Sans 3 from a comparison variant to
the Golden Resume default. The selected PDF kept the variant's 10.25pt body,
0.45em paragraph leading, and 10.85pt organization names. The three checked-in
TTF cuts were byte-verified against Adobe's pinned upstream commit and retained
embedded subset Unicode mappings in the compiled PDF. Its final render was
pixel-identical to the reviewed Source Sans comparison render.

A subsequent Golden Resume revision added one anonymized Projects record for
an independently operated Kubernetes cluster. The project stayed in normal
flow between Experience and Education, mirrored the experience hierarchy with
the project name and descriptor on the left, used one labeled `Focus:` unit on
the right, and placed two accomplishments in a native list. Poppler
plain/layout, Tika, and decoded Poppler XML retained the project fields exactly
once and in the intended bounded record before Education. The one-row project
metadata shared a baseline and common right edge with the experience metadata,
with positive left/right clearance. The one-page result preserved the selected
10.25pt body size by changing vertical page margins from 0.52in to 0.44in and
standardized major-section spacing from 2em to 1.85em; no section received a
special-case gap. This is evidence for the exact content and font lengths, not
a universal Projects component exemption from re-testing.

The same artifact retained its short Profile above Experience. This established
a useful coexistence pattern: Profile supplied a concise interpretive thesis,
while Projects supplied Kubernetes evidence absent from the synthetic job
history. The sections were not merged, placed in cards, or moved into columns;
each had a true heading and a separate bounded association window. The skill's
Golden oracle and uv evaluator now preserve that distinction as a regression
contract.

A later editorial cleanup removed the redundant header tagline because the
Profile already carried the positioning thesis, and removed the phone number
from the contact block. A subsequent contact update added a labeled GitHub URL.
The contact block then removed redundant `Email:`, `Portfolio:`, `GitHub:`, and
`LinkedIn:` prefixes while retaining canonical visible values. Poppler plain,
Poppler layout, decoded XML, and Tika's visible body retained the values once
and in order. Tika appended the same four raw link destinations as a terminal
trailer before and after the label change, so labels had only masked that
extractor behavior in the former full-field oracle. The evaluator now preserves
the raw Tika output, validates that exact trailer independently, and evaluates
visible-body field counts separately. The current Golden oracle expects four
link annotations: email, portfolio, GitHub, and LinkedIn. Location remains
visible body text. This is local extractor evidence, not commercial ATS UAT.

The Golden contact block later added one muted, visible normal-flow line after
LinkedIn: `U.S. citizen · Authorized to work in the U.S. · No sponsorship
required`. The reviewed oracle requires that statement exactly once and before
Profile. It is direct eligibility metadata rather than Profile prose, a hidden
keyword, or a claim that a commercial ATS will use the field. Adding the line
initially pushed Skills to a second page. The one-page revision kept all type
sizes unchanged, reduced vertical page margins uniformly from 0.44in to 0.42in,
and reduced every major-section `above` gap from 1.85em to 1.75em. The resulting
artifact passed the full Golden gate and visual inspection.

A subsequent header refinement placed the portfolio, GitHub, and LinkedIn
display URLs on one centered normal-flow row while retaining three separate
link annotations. Removing the former standalone LinkedIn row restored the
header's previous vertical footprint, so the document returned to 0.44in
vertical margins and the uniform 1.85em major-section `above` gap. All visible
contact values and the work-authorization statement remained exact-once and in
order across Poppler plain/layout, Tika visible-body, and decoded XML views.
The evaluator now exposes this as a dedicated `work_authorization_statement`
gate with per-view counts and LinkedIn-to-Profile placement evidence, in
addition to the general field and order oracle. This protects a high-value
candidate-supplied fact without implying that every candidate has, or should
claim, the same status.

## Right-aligned metadata follow-up

A later controlled probe held the same three jobs and bullets constant while
comparing eleven ways to put dates and locations on the right. Two-row flexible
spacing, separate blocks, grid, table, inline placement, and two-row labeled
fields all looked plausible, but Poppler plain grouped repeated left and right
edges as separate columns. Tika and Poppler layout retained the visual rows.
Separate alignment blocks kept source order only by moving the right values to
their own visible lines. Dotted leaders polluted extracted text. An unlabeled
single row still let one right-side group fall after the first bullet in
Poppler plain.

The accepted construction combined each job into one metadata row: company and
role on the left, and `Dates: ... · Location: ...` as one flush-right unit. It
used no grid, table, absolute placement, hidden text, or duplicate facts. The
full resume passed exact field, order, and bounded-association checks in
Poppler plain/layout, Tika, and decoded XML across Avenir Next, Source Sans 3,
Helvetica Neue, IBM Plex Sans, and TWK Lausanne Pan preview. XML geometry also
showed a common right edge, shared baselines, and at least 42 pixels of
left/right clearance at 144 DPI. These results are exact-template evidence;
longer wording or another font still requires a fresh run.

That remaining content-length risk was later turned into a reviewed stress
matrix rather than a collection of copied `.typ` files. The Golden source now
loads canonical anonymous JSON through a reusable renderer. Eight supported
cases substitute long company, role, location, date, URL, project metadata, or
combined values while keeping the renderer, fonts, compiler flags, and
unaffected facts constant. Explicit oracle patches are reviewed independently
of extraction, and frozen base-data, renderer, and oracle hashes stop stale
experiments.

The first matrix run found two genuine implementation defects. A long right
unit could wrap `Location:` away from its value, breaking exact raw extraction,
and Tika could emit its URI annotation block after the page containing links
but before later-page body text. The renderer now measures complete left/right
units and chooses either a collision-free one-row layout or a complete
stacked-right unit. Long contact URLs wrap only as whole centered link units.
The evaluator locates exactly one reviewed URI block anywhere in raw Tika
output and renders every page. A uniform reduction of major-section trailing
space kept all realistic cases within the one-page budget without case-specific
styling. All eight supported cases then passed the deep local gates and visual
review. Intentionally unbreakable company and location tokens failed the exact
reviewed text, page-budget, and geometry gate set. A later hardening pass froze
the fixture adapter as well as data, renderer, and oracle throughout the run and
checked every row against the actual page content box. This demonstrates
bounded resilience to the tested values, not commercial ATS behavior or
arbitrary-length safety.

The complete Golden bundle was subsequently moved out of the repository root
to `tests/fixtures/golden-resume/`. Source, compiled PDF, canonical data,
renderer, reviewed oracle, and stress manifest now share one authoritative
fixture directory. The project-local skill retains the evaluator scripts and
routes its defaults to that bundle; `just golden`, `just golden-check`, and
`just golden-stress` remain the public entry points. This separation keeps
test-only assets discoverable without presenting them as a candidate's active
resume.

## Challenge-set sweep

A separate sweep compiled 22 reconstructed Typst resumes. All were tagged,
image-free, and used embedded Unicode fonts, yet the sweep still found:

- hidden icon tokens and replacement characters;
- zero-width tokens;
- manual hyphen fragments;
- duplicate URI trailers and duplicate targets;
- a URI trailer injected between body records;
- malformed visible URLs; and
- source-versus-coordinate order disagreement.

The strongest local specimens were the modified versions of resumes 165 and
108. The weakest hazards included resume 135 and the base resume 086. This was
a challenge-set ranking, not causal proof or ATS ground truth.

## Lessons that required correction

- The split-row result was an authored source-order failure, not proof that an
  extractor invented relationships.
- The grid could not be labeled Conditional after its measured association
  gates failed.
- The two-column result was not raw-extraction-safe merely because a collapsed
  whitespace view recovered the facts.
- The manual-bullet experiment needed baseline metadata and a micro-isolated
  change before interpretation; its final full-resume failure was an
  interaction, not a universal verdict on the glyph.
- PDF tags, text extraction, field association, visual rendering, external ATS
  behavior, and hiring outcomes must remain separate evidence layers.
