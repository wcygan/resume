# Evidence and claim boundaries

Resume parsability is not one binary property. Keep each evaluation layer
separate so a strong result in an early layer does not silently become a claim
about a later one.

## Contents

- Evaluation layers and defensible statements
- Local result vocabulary
- Greenhouse guidance
- PDF/UA and tag boundaries

## Evaluation layers

| Layer | Question | Suitable evidence |
| --- | --- | --- |
| Artifact integrity | Is this a valid, inspectable PDF with the intended page geometry? | Hash, `qpdf --check`, `pdfinfo`, render |
| Text extraction | Do tested engines recover the intended characters and ordering? | Raw Poppler and Tika outputs, XML text nodes |
| PDF structure | Are headings, lists, links, and document tags represented? | QDF/JSON structure, annotations, tagged status |
| Field association | Are title, employer, dates, location, education, and skills grouped correctly? | Reviewed oracle, exact counts, bounded ordered windows |
| External ATS behavior | Does a named ATS populate the intended fields? | Authorized upload/UAT, captured field-by-field result |
| Recruiting outcome | Does the resume advance or produce a callback? | Employer process data with many uncontrolled variables |

Never collapse these layers into one "ATS score."

## Defensible statements

Prefer precise language:

- "Text-layer compatible with Poppler 26.03.0 and Tika 3.3.0 under the
  tested environment."
- "All oracle facts occurred exactly once and all five bounded association
  windows passed in four acceptance views."
- "The PDF is tagged and contains H1, H2, list, and link structures."
- "The rendered page had no observed clipping, overlap, or detached bullets."
- "Greenhouse behavior is untested; manual verification remains required."

Avoid:

- "ATS-safe," "guaranteed to parse," or "passes every ATS."
- "Tika is what Greenhouse uses" without current primary evidence.
- "PDF/UA means screen-reader certified."
- "Clean extraction predicts callback probability."
- A percentage score whose denominator and ground truth are undefined.

## Local result vocabulary

Use the status together with the layer it describes.

- **Pass:** every declared local gate passed under the recorded toolchain.
- **Conditional:** core content survived locally, but semantics were absent,
  extractor behavior differed, a risky construct was used, or the evidence is
  too tool-dependent to recommend as a baseline.
- **Fail:** required content was missing, duplicated, reordered, associated
  with the wrong record, structurally absent when required, mechanically
  invalid, or visually defective.
- **Untested:** no evidence was collected for that layer. External ATS behavior
  is normally Untested even when local extraction is Pass.

Report dimensions when one overall status would hide useful nuance:

```text
Local text extraction: Pass
Field association: Pass
PDF semantic structure: Pass
Visual rendering: Pass
External ATS/Greenhouse UAT: Untested
```

## Greenhouse guidance

The official Greenhouse Support article, [Unsuccessful resume
parse](https://support.greenhouse.io/hc/en-us/articles/200989175-Unsuccessful-resume-parse),
was checked on 2026-08-04; the page says it was last updated 2026-03-02.
Greenhouse says its parser may fail or partially parse resumes that:

- exceed 2.5 MB;
- use spaced-out letters;
- contain graphics, photos, or word art;
- are uploaded as images rather than documents;
- use complex tables, headers, or footers;
- place name/contact data in a header, footer, or text box;
- use columns;
- lack clear sections or use inconsistent formats;
- use company names without identifying terms such as Inc., Co., LTD, or LLC;
  or
- abbreviate job titles instead of using complete titles.

Attribute these items to Greenhouse. The local Typst experiments independently
reproduced risks for page-header contact, columns, layout containers, source
order, and related structures, but did not causally test every vendor item.
Greenhouse also says failed or partial parses require manual correction and
verification.

Vendor pages and products change. Recheck the primary source before making a
current vendor-specific claim.

## PDF/UA and tags

Typst normally emits a tagged PDF. `--pdf-standard ua-1` adds conformance
checks and can improve structural discipline. It does not prove:

- correct field mapping by an ATS;
- correct behavior in every assistive technology;
- human accessibility acceptance; or
- hiring success.

Conversely, a no-tags PDF can still yield readable plain text. This is why text
extraction and document structure must be audited separately.
