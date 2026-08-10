# Project workflow

Follow the repository's current JSON-driven build rather than older
source-layout assumptions.

## Authoritative files

- `will_cygan_resume-data.json` — resume content authority.
- `will_cygan_resume.typ` — thin adapter.
- `tests/fixtures/golden-resume/golden-resume-template.typ` — shared renderer.
- `will_cygan_resume.pdf` — final visual artifact.
- `work-experience/*.md` — supporting evidence and fuller history.
- `work-experience/RELEVANCE.md` — author prioritization prior.
- `scripts/extraction_check.py` and
  `scripts/extraction-check.fixtures.toml` — quick local extraction gate.
- `tests/fixtures/golden-resume/` — controlled parser-friendly fixture.

Do not edit the generated PDF directly. Do not treat the anonymous Golden
fixture as the user's factual resume.

## Review-only workflow

1. Read the JSON sections in scope.
2. Read the matching supporting entries and acronym definitions.
3. Inspect the current PDF when the request concerns hierarchy, density,
   wrapping, ordering, or page fit.
4. Return an evidence-led recommendation without changing files.

## Editing workflow

1. Confirm that the request authorizes edits and identify the factual envelope.
2. Edit the narrowest authoritative source.
3. Run `just compile`.
4. Inspect `will_cygan_resume.pdf` visually.
5. Run `just validate-content` for content-only changes.
6. Run `just validate-renderer` when changing the shared renderer, fonts, PDF
   structure, metadata geometry, or links.
7. Run `just validate-full` when changing extraction code, fixtures, validation
   infrastructure, or multiple repository-wide surfaces.

Use individual validation commands only to diagnose a failed plan step. The
shared plan owns acceptance membership, order, failure status, and evidence
locations.

Use the current `resume-parsability` acceptance checklist for mechanical
claims. Passing local checks does not establish external ATS or hiring
behavior.

## Comparison workflow

For a git-ref comparison, inspect the content authority at that ref:

```sh
git show <ref>:will_cygan_resume-data.json
```

Use a temporary file or worktree only when a baseline render is required, and
do not overwrite the working artifact. Record the compiler and renderer used
for both versions.
