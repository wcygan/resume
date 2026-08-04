# Resume

A one-page Typst resume with JSON-backed content, a shared parser-friendly
renderer, controlled extraction fixtures, and project-local Codex review
skills.

## Authoritative artifacts

- `will_cygan_resume-data.json` contains the resume content.
- `will_cygan_resume.typ` loads the JSON and invokes the shared renderer.
- `tests/fixtures/golden-resume/golden-resume-template.typ` is the renderer.
- `will_cygan_resume.pdf` is the final artifact to inspect.

Supporting work history lives in `work-experience/`. It is raw evidence and
may contain additional, draft, or in-flight material not present in the final
resume.

## Build and validate

Install Typst, Poppler, Tika, qpdf, and uv for the complete local workflow.
The pinned Source Sans 3 font cuts are already under `fonts/source-sans-3/`.

```sh
just compile
just page-budget
just extraction-check
just test
```

Use `just dev` for a watched local preview.

## Project-local Codex skills

- `$resume-review` reviews and tailors content against documented evidence.
- `$resume-parsability` evaluates PDF extraction, field associations,
  structure, links, fonts, and controlled layout behavior.

The parsability checks are local evidence. They do not reproduce a commercial
ATS, certify screen-reader behavior, or predict hiring outcomes.

## Golden Resume

The controlled reference bundle lives under
`tests/fixtures/golden-resume/`. It includes anonymous data, source, a
reviewed oracle, a compiled PDF, a stress manifest, and the shared renderer.

```sh
just golden-check
just golden-stress
```

Reports and rendered evidence are written beneath `.extraction/`, which is
gitignored.
