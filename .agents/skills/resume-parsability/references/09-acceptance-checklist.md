# Acceptance checklist

Use this checklist for a final resume, a structural template change, or a
variant ranking. Mark unavailable layers Untested rather than assuming them.

## 1. Scope and reproducibility

- [ ] Source, PDF, intended page size/count, and artifact hash recorded.
- [ ] Compiler, font, extractor, qpdf, OS, and locale versions recorded.
- [ ] Reviewed factual oracle and expected links frozen before extraction.
- [ ] Raw evidence stored in a deliberate evidence directory.

## 2. Text extraction

For Poppler plain, Poppler layout, Tika text, and decoded Poppler XML:

- [ ] Output is non-empty.
- [ ] Candidate name and contact values survive.
- [ ] Any user-confirmed citizenship, work-authorization, or sponsorship
      statement survives exactly once; no such status was inferred.
- [ ] Every canonical field appears the expected number of times.
- [ ] Sections occur in expected order.
- [ ] Keywords survive as exact substrings where required.
- [ ] No U+FFFD, unexpected Private Use Area, zero-width, or soft-hyphen
      contamination exists.
- [ ] Raw failures remain visible; canonicalization is only NFC plus whitespace
      collapse.

## 3. Field association

- [ ] A Profile, when present, stays between its heading and the next section
      and contains only supportable positioning language.
- [ ] A work-authorization statement, when present, remains in its reviewed
      header window; the Golden statement must follow LinkedIn and precede
      Profile in every accepted view.
- [ ] Every job window contains exactly its employer, date range, title,
      location, and accomplishments in the declared order.
- [ ] Each window stops before the next job or section boundary.
- [ ] Every project window contains its name, descriptor, labeled metadata,
      optional visible link, and accomplishments before the next section.
- [ ] Education contains institution, date, and degree before Skills or the
      next section.
- [ ] Each skills category remains adjacent to its values.
- [ ] Repeated employers or titles do not cause cross-record matches.
- [ ] Extractor disagreement is classified, not averaged away.

## 4. PDF mechanics and semantics

- [ ] Page count, page size, and rotation match the contract.
- [ ] `qpdf --check` passes.
- [ ] PDF is tagged unless no-tags is an intentional negative control.
- [ ] `StructTreeRoot` and `MarkInfo` are present.
- [ ] Real headings and native lists produce expected H/L/Lbl/LBody tags.
- [ ] All fonts are embedded with Unicode mappings.
- [ ] No unexpected raster images exist.
- [ ] URI annotation multiset exactly matches the oracle.
- [ ] Tika's one exact URI annotation block is preserved raw and matches the
      reviewed destinations before it is separated from visible-body counts,
      even when later-page text follows it.
- [ ] No hidden duplicate canonical text exists.

## 5. Visual inspection

- [ ] Every page was rendered from the final PDF at a stable DPI.
- [ ] No clipping, overlap, tofu, broken glyphs, or detached markers exist.
- [ ] Section hierarchy and reading order are visually clear.
- [ ] Columns, tables, or right-aligned metadata do not create ambiguity.
- [ ] No experience, project, or education entry splits unexpectedly.
- [ ] Contact information remains legible and selectable.

## 6. Cross-platform and regression evidence

- [ ] Project quick gate passes with all expected extractors available.
- [ ] Negative fixtures fail for the intended reason.
- [ ] Long company, role, location, date, URL, project metadata, and combined
      stress cases pass through the production renderer.
- [ ] Unbreakable company and location controls fail their exact reviewed gate
      sets, including the intended geometry gate and no undeclared failures.
- [ ] Platform-sensitive behavior was checked in the CI environment.
- [ ] The latest source—not a stale prior PDF—produced the inspected artifact.

## 7. Claim boundary

- [ ] Local results name exact tools and versions.
- [ ] PDF semantic tags are not described as field-mapping proof.
- [ ] Greenhouse advice is attributed to Greenhouse.
- [ ] External ATS UAT is marked Untested unless actually performed.
- [ ] No callback, ranking, or universal ATS claim is made.

## Report template

```text
Outcome:
Artifact and hash:
Toolchain:

Local text extraction:
- Poppler plain:
- Poppler layout:
- Tika:
- Poppler XML text nodes:

Field counts/order/associations:
PDF tags/fonts/images/links/integrity:
Visual inspection:
Conditional or failed patterns:
Recommended source change:
External ATS/Greenhouse UAT:
Residual uncertainty:
```
