# Resume repository guidance

This repository builds and evaluates William Cygan's resume. Keep content
claims traceable, keep mechanical validation distinct from hiring advice, and
inspect the generated PDF rather than reasoning from source alone.

## Authority

- `will_cygan_resume-data.json` is the authoritative resume content.
- `will_cygan_resume.typ` is a thin adapter that loads the JSON and invokes the
  shared renderer.
- `tests/fixtures/golden-resume/golden-resume-template.typ` is the active
  renderer used by both the personal resume and controlled Golden fixture.
- `will_cygan_resume.pdf` is the final artifact for visual acceptance.
- `work-experience/*.md` is supporting source material. It may contain drafts,
  in-flight work, or additional context that is not appropriate for the final
  resume without verification.
- `work-experience/RELEVANCE.md` records the author's prioritization prior; it
  is useful input, not objective truth.
- `advice/` contains source notes with mixed authority. Consult the
  `resume-review` evidence register before relying on them.
- `archive/` is historical and read-only unless the user explicitly requests
  archival work.

## Project-local skills

- Use `$resume-review` for content review, job tailoring, claim-grounded
  interview preparation, bullet refinement, and before/after content review.
- Use `$resume-parsability` for PDF extraction, field association, Greenhouse
  parsing questions, Typst structure, controlled fixtures, and mechanical PDF
  acceptance.
- For mixed work, use both. Editorial quality does not prove parsability, and
  clean extraction does not prove hiring effectiveness or external ATS
  behavior.

## Evidence rules

- Never invent metrics, scope, ownership, titles, dates, or technologies.
- Label consequential statements as fact, inference, practitioner heuristic,
  or preference when their status is not already obvious.
- Treat same-model reviewer agreement as one analysis, not independent
  evidence or consensus.
- Do not produce ATS scores, callback probabilities, or universal parsing
  guarantees.
- A supplied job description defines desired requirements, not facts about the
  candidate. Mark unsupported requirements as unknown or gaps.

## Change and validation workflow

1. Inspect the current JSON, supporting work-experience entries, and target
   role before editing content.
2. Make the narrowest truthful change in `will_cygan_resume-data.json` or the
   active renderer.
3. Rebuild with `just compile`.
4. Inspect the latest `will_cygan_resume.pdf` for page count, wrapping,
   clipping, hierarchy, and reading order.
5. Run `just page-budget` and the relevant focused checks. Run
   `just extraction-check` after content changes; run the deeper parsability
   gates when layout, fonts, links, structure, or renderer behavior changes.
6. Report what the evidence proves and what remains untested.

Useful commands:

```sh
just compile
just page-budget
just extraction-check
just test
just golden-check
just golden-stress
```
