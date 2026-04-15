---
name: typst-vendor
description: Vendor @preview Typst packages into template/ or bootstrap new in-house Typst templates from scratch. Use when the user asks to vendor, fork, copy, pin, localize, or maintain a Typst template; when a @preview package breaks on a newer typst version; when creating a new template.typ from scratch; or says things like "vendor modern-cv", "fork this typst package", "bring this template in-repo", "write our own resume template". Keywords typst, vendor, fork, @preview, template, modern-cv, fontawesome, linguify, typst.toml, lib.typ, MIT attribution, version drift.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Typst Template Vendor

Maintains `template/*.typ` — templates that started life as `@preview` packages and got copied in-repo for control, plus any templates authored from scratch. The current vendored template is `template/modern-cv.typ` (forked from `@preview/modern-cv:0.8.0`).

Two workflows: **vendor** (fork an upstream `@preview` package) and **bootstrap** (write a new template from scratch). Pick one.

## Before starting either workflow

1. Read `will_cygan_resume.typ` line 1 to see what's currently imported.
2. `ls template/` to see what's already vendored.
3. Confirm `just compile` works today — you want a clean baseline before making changes.

---

## Workflow A — Vendor an upstream `@preview` package

Use when the user wants to fork a package in `template/`. Record the package name, pinned version, and tag.

### 1. Clone at the pinned tag

```bash
cd /tmp && rm -rf <pkg> && git clone https://github.com/<owner>/<pkg> && cd <pkg> && git checkout <tag>
```

### 2. Inspect what you're vendoring

- `typst.toml` → declared `compiler` version, `entrypoint` (usually `lib.typ`), author, license.
- `lib.typ` → count lines and enumerate public `#let` exports: `grep -n "^#let [a-z]" lib.typ`.
- First lines of `lib.typ` → transitive `@preview` deps.
- `lang.toml` if it exists → signals `linguify` usage for i18n.

### 3. Identify what to keep vs drop

- **Keep symbols** referenced in `will_cygan_resume.typ`. Grep the resume: `grep -oE '[a-z][a-z-]+[(\[]' will_cygan_resume.typ | sort -u` → cross-reference against the package's public exports.
- **Drop symbols** for unused template modes (cover letters, letters, invoices), non-English language tables, and helpers only those functions use.
- **Decide each transitive `@preview` dep** using [references/preview-dep-playbook.md](references/preview-dep-playbook.md) — canonical keep/inline/drop verdicts for common deps (`linguify`, `fontawesome`, `cetz`, `tidy`, etc.).

### 4. Fix typst version drift

The most common reasons old `@preview` packages break on newer typst: see [Version drift fixes](#version-drift-fixes) below. Apply all applicable fixes in the same pass.

### 5. Write `template/<pkg>.typ`

- Top-of-file comment: attribution to upstream, license, source tag, list of removed sections.
- Keep formatting close to upstream to ease future diffs.
- Keep public symbol names identical so the resume's import site doesn't change.

### 6. Flip the import

```diff
- #import "@preview/<pkg>:<ver>": *
+ #import "template/<pkg>.typ": *
```

### 7. Verify

```bash
just compile              # must produce will_cygan_resume.pdf, no errors
ls -la will_cygan_resume.pdf
```

Font-missing warnings are fine (typst falls back). Real errors aren't.

### 8. Record the provenance

The top-of-file comment in `template/<pkg>.typ` is the source of truth — upstream URL, tag, license, what you trimmed, what you fixed. License wording matters and varies: see [references/license-headers.md](references/license-headers.md) for copy-pasteable blocks for MIT / BSD / Apache-2.0 / MPL-2.0 / CC-BY-4.0 and the anti-patterns to avoid.

---

## Workflow B — Bootstrap a new in-house template

Use when the user wants to author a template from scratch (not forked from upstream).

### 1. Pick a filename and symbol prefix

`template/<name>.typ`. Public functions should be prefixed (e.g. `academic-cv-entry`, `cover-letter-block`) to avoid collisions when multiple templates are imported.

### 2. Start from a skeleton

Pick the closest starter in [references/bootstrap-skeletons.md](references/bootstrap-skeletons.md): resume, cover letter, academic CV, or touying slides. Each one is minimal — just imports, color constants, and a single template function with `set document` / `set text` / `set page` / heading rules. Add helper functions (entry rows, bullet blocks, headers) only as the user asks — resist speculative surface.

### 3. Wire it in and verify

```diff
- #import "template/modern-cv.typ": *
+ #import "template/<name>.typ": *
```

Then `just compile`.

---

## Version drift fixes

See [references/version-drift-fixes.md](references/version-drift-fixes.md) for the full table and a detection grep you can run on any freshly-cloned upstream `lib.typ`. At minimum, always fix `type(x) == "string"` → `type(x) == str`; the rest depend on what the package uses.

---

## Maintenance

Keep a local clone of each upstream at `/tmp/<pkg>` (or under `~/src/`) for periodic diffs. When upstream releases a new tag:

```bash
git -C /tmp/<pkg> fetch --tags
git -C /tmp/<pkg> diff <current-tag>..<new-tag> -- lib.typ lang.toml
```

Cherry-pick only hunks that touch symbols you kept. Most upstream churn will be in cover-letter / i18n code you already dropped.

---

## Guardrails

- **Do not touch `archive/`**. Deprecated LaTeX, read-only.
- **Do not edit `will_cygan_resume.typ` content** beyond the single import-line swap. The vendor skill changes templates, not resume prose.
- **Preserve attribution.** Never vendor without a top-of-file comment naming upstream + license.
- **Verify by compile, not by eye.** `just compile` must exit 0 and produce a PDF before declaring the vendor done.
- **Pin, don't float.** Upstream clones check out a specific tag; vendored files name that tag in the header.

---

## References

- [version-drift-fixes.md](references/version-drift-fixes.md) — typst 0.13+ deprecation table + detection grep.
- [preview-dep-playbook.md](references/preview-dep-playbook.md) — keep/inline/drop verdicts for common transitive `@preview` deps.
- [bootstrap-skeletons.md](references/bootstrap-skeletons.md) — starter templates for resume / cover letter / academic CV / slides.
- [license-headers.md](references/license-headers.md) — copy-pasteable attribution headers per license.
