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

- **Keep**: every symbol referenced in `will_cygan_resume.typ`. Grep the resume: `grep -oE '[a-z][a-z-]+[(\[]' will_cygan_resume.typ | sort -u` → cross-reference against the package's public exports.
- **Drop**: unused template functions (cover letters, letters, invoices, etc.), non-English language tables, helpers only those functions use.
- **Drop deps** where possible:
  - `@preview/linguify` — inline the English strings you need, delete the import and all `linguify(...)` / `lflib._linguify(...)` calls.
  - `@preview/cetz`, `@preview/tidy`, etc. — usually keep if load-bearing.
- **Keep deps** where the cost of forking exceeds the benefit:
  - `@preview/fontawesome` — small, stable, load-bearing for icons. Keep the import, pin the version.

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

The top-of-file comment in `template/<pkg>.typ` is the source of truth. Format:

```typ
// Vendored from https://github.com/<owner>/<pkg> @ tag <tag>.
// <LICENSE> — Copyright (c) <year> <author>.
// Trimmed: <what was removed>. Fixed: <version-drift changes>.
```

---

## Workflow B — Bootstrap a new in-house template

Use when the user wants to author a template from scratch (not forked from upstream).

### 1. Pick a filename and symbol prefix

`template/<name>.typ`. Public functions should be prefixed (e.g. `academic-cv-entry`, `cover-letter-block`) to avoid collisions when multiple templates are imported.

### 2. Start from this skeleton

```typ
// In-house template authored <date> for <use case>.

// Drop if the template doesn't use icons.
#import "@preview/fontawesome:0.5.0": *

#let color-accent = rgb("#262F99")
#let color-body = rgb("#333333")

#let <template-name>(
  author: (:),
  paper-size: "us-letter",
  body,
) = {
  set document(
    author: author.firstname + " " + author.lastname,
    title: "<Title>",
  )
  set text(
    font: ("Source Sans Pro", "Source Sans 3"),
    size: 11pt,
    fill: color-body,
    fallback: true,
  )
  set page(paper: paper-size, margin: (x: 15mm, y: 10mm))
  set par(spacing: 0.75em, justify: true)
  set heading(numbering: none, outlined: false)

  body
}
```

Add helper functions (entry rows, bullet blocks, headers) only as the user asks for them — resist speculative surface.

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
