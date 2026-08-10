# Golden Resume fixture

This directory is the complete, anonymous Golden Resume regression fixture for
the project-local `resume-parsability` skill.

This directory is authoritative. Do not add convenience copies of the source
or PDF at the repository root; use the `just` recipes below.

## Files

- `golden-resume.typ` — thin compile entry point.
- `golden-resume-template.typ` — reusable responsive renderer.
- `golden-resume-data.json` — canonical anonymous content.
- `golden-resume-oracle.json` — reviewed extraction, structure, link, and
  geometry expectations.
- `golden-resume-stress-matrix.json` — reviewed content-length cases and frozen
  baseline hashes.
- `golden-resume.pdf` — compiled reference artifact; do not edit it directly.

## Commands

From the repository root:

```sh
just golden
just golden-check
just golden-stress
```

The first command rebuilds the checked-in PDF. The other commands use thin
skill-owned CLI adapters over the repository-owned evaluator and write
disposable evidence beneath `.extraction/`. External ATS behavior remains
untested by this fixture.
