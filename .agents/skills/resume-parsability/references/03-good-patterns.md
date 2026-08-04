# Good patterns

These are the preferred baseline patterns. They reduce ambiguity for both
linear and spatial extractors and retain useful PDF structure.

## Structure and reading order

- Use one narrative column in normal document flow.
- Author content in the same logical order a parser should consume it.
- Keep each job's employer, dates, title, location, and accomplishments in one
  contiguous source block.
- Use stable, conventional section labels such as Experience, Education, and
  Skills.
- Separate adjacent sections clearly in source and extracted text.
- Use real Typst headings rather than bold text that merely looks like a
  heading.
- Use native Typst lists rather than hand-drawn bullet characters.

The August 2026 right-aligned golden-resume follow-up used this tested
experience order:

```text
company -> role -> labeled date range -> labeled location -> accomplishments
```

That order is not a universal ATS schema. Its value is that it is explicit,
contiguous, consistent, and covered by a reviewed oracle. If another order is
required, define and test it before calling the layout robust.

## Contact information and links

- Keep unique name and contact facts in normal body content, even when they are
  visually presented at the top of the page.
- Use canonical, human-readable contact values. Labels are useful when a
  destination's purpose is ambiguous, but self-identifying email addresses and
  LinkedIn or GitHub domains may remain unlabeled after direct extraction and
  link validation.
- Use real link annotations with human-readable display text.
- Require each intended destination exactly once in the PDF annotation set.
- Keep displayed URL text canonical and readable; avoid malformed spacing or
  duplicate full URLs that Tika may echo again from annotations.

## Work authorization and sponsorship

When the candidate explicitly chooses to disclose verified status, keep it as
one concise, visible normal-flow line near the contact block. Treat it as a
canonical fact, not keyword decoration.

The Golden Resume uses:

```text
U.S. citizen · Authorized to work in the U.S. · No sponsorship required
```

Its evaluator requires this exact statement once after LinkedIn and before
Profile in every accepted extraction view. Never infer or synthesize
citizenship, work authorization, or sponsorship status for another candidate.

## Profile and projects

Profile and Projects are both optional, and they can coexist when they perform
different jobs:

- A Profile is a short interpretive thesis. Use it to clarify target role,
  seniority, specialization, domain focus, a career transition, or the theme
  connecting otherwise varied experience.
- Projects add evidence that the employment history does not already prove,
  such as current infrastructure practice, open-source work, independent
  products, research, or a new technical specialty.

Keep the Profile under a real `PROFILE` heading and usually to one short
paragraph. Prefer specific, supportable positioning over adjectives or a
keyword inventory. A model can infer generic collaboration or experience from
strong bullets; the Profile earns its space when it reduces material ambiguity.

Keep each project in one contiguous normal-flow record under a real `PROJECTS`
heading. A robust record may include a project name, a plain-language
descriptor, one labeled focus or date unit, an optional visible repository or
portfolio link, and native-list accomplishments. Require its facts and bullets
to remain inside the Projects window before the next section.

When both sections create page pressure, remove redundant Profile language and
weak or duplicative project material before shrinking type, collapsing every
section gap, or moving either section into a second column. The August 2026
Golden Resume locally passed with a short Profile and one Kubernetes project;
that is exact-artifact evidence, not a guarantee for longer content.

## Experience and education

- Use complete job titles rather than abbreviations when space permits.
- Use real or clearly identifiable company names. Greenhouse specifically
  recommends identifiers such as Inc., Co., LTD, or LLC.
- Use consistent, unambiguous date formats.
- Label otherwise ambiguous dates, for example `Graduation: May 2016`.
- When dates and locations must sit on the right, prefer one labeled metadata
  unit such as `Dates: ... · Location: ...` over two persistent right-side
  rows. Keep company and role together on the left in the same normal-flow
  record, and validate the exact font and content lengths.
- Keep education facts in adjacent normal flow rather than positioning the date
  independently across the page.
- Prevent a compact experience entry from splitting across pages when that can
  be done without absolute positioning or overflow.

## Skills and accomplishments

- Represent skills as labeled flow text when maximum portability matters.
- Keep category and values adjacent in source order.
- Use native lists for accomplishments so the PDF can expose L, Lbl, and LBody
  structures.
- Preserve important searchable terms exactly; test keyword round-trip after
  every font, wrap, or hyphenation change.

## Typography and export

- Set document language and disable automatic hyphenation for this dense resume
  use case.
- Prefer left-aligned body prose over layouts that create forced word
  fragmentation.
- Use embedded fonts with Unicode mappings.
- Keep PDF tags enabled.
- Treat PDF/UA-1 as a useful additional export check, not as an ATS guarantee.
- Keep the artifact text-based and image-free unless an image is genuinely
  necessary and has separate accessibility handling.

## Evidence behind the baseline

The controlled semantic-flow baseline passed:

- exact raw and NFC-plus-whitespace-canonical field counts;
- expected order;
- three job, one education, and one skills association window;
- Poppler plain, Poppler layout, Tika text, and decoded Poppler XML views;
- one-page Letter geometry and zero rotation;
- embedded Unicode fonts, no images, qpdf integrity, and exact links; and
- H1 and native list structure.

The later Golden Resume extended that baseline with a bounded Profile and one
bounded Projects record. Both survived Poppler plain/layout, Tika, and decoded
Poppler XML in the reviewed order while retaining the one-page structure.

Re-run these gates for the actual resume. A pattern's prior success is a
starting hypothesis, not a permanent exemption from testing.
