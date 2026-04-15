# `@preview` Dependency Playbook

When vendoring, the upstream `lib.typ` usually imports a handful of other `@preview` packages. For each, decide: **keep** the import, **inline** the logic/data statically, or **drop** entirely.

## Decision rule

- **Keep** if it implements non-trivial rendering logic (drawing, layout, syntax highlighting). Forking it would cost more than maintaining the dep.
- **Inline** if it only encodes static data (language strings, unit tables, color palettes). Copy the bits you need as plain Typst values and delete the import.
- **Drop** if it's only used for a feature you've already trimmed (i18n for languages you don't use, icons for platforms you don't link to).

## Canonical verdicts

| Package | Size | Role | Default verdict | Notes |
|---|---|---|---|---|
| `fontawesome` | small | Icon font wrapper | **Keep** | Stable API, load-bearing for contact rows. Pin to 0.5+. |
| `linguify` | small | TOML-driven i18n | **Inline** | Copy English (or your language) strings as a dict; drop `toml()` + `linguify()` calls. This is where most upstream drift lives. |
| `cetz` | large | 2D drawing | **Keep** | Reimplementing is infeasible. |
| `cetz-plot` | large | Plotting on cetz | **Keep** | Same. |
| `fletcher` | large | Commutative diagrams | **Keep** | Same. |
| `tidy` | medium | API doc generation | **Drop** usually | Only imported if the template renders its own docs. Resume templates don't need it. |
| `polylux` / `touying` | large | Slide frameworks | **Keep** (if slides) / **Drop** (if resume) | Load-bearing for slide templates; irrelevant for CVs. |
| `codly` / `codly-languages` | medium | Code-block styling | **Keep** | Syntax highlighting logic is non-trivial. |
| `showybox` | medium | Styled boxes/callouts | **Keep** | Used for admonitions. |
| `cmarker` | medium | Inline Markdown | **Keep** | Parser, not reimplementable. |
| `hydra` | small | Running headers | **Keep** | Layout query logic. |
| `based` | tiny | Base64 en/decode | **Keep** | Smaller than your vendored file; not worth forking. |
| `valkyrie` | medium | Schema validation | **Inline** usually | Replace with plain `assert(type(x) == …)` checks for the fields you care about. |
| `unify` | medium | SI units | **Keep** | Unit tables are surprisingly intricate. |
| `physica` | medium | Physics notation | **Keep** | Same. |
| `subpar` | small | Subfigures | **Keep** | Layout, not data. |
| `gentle-clues` / `note-me` | medium | Admonitions | **Keep** | Styled rendering. |
| `droplet` | small | Drop caps | **Keep** | Typographic logic. |
| `chic-hdr` | small | Chic header/footer | **Inline** possible | Small enough to copy if you want full control; otherwise keep. |

## Heuristic when the package isn't listed

1. Open `@preview/<pkg>:<ver>/lib.typ` (or whatever the entrypoint is).
2. Is it mostly `#let some-dict = (...)` / `toml()` / TOML data? → **Inline**.
3. Is it mostly show/set rules, layout math, or path drawing? → **Keep**.
4. Does it have its own transitive `@preview` deps? Each layer adds fragility — lean toward **Keep** (to amortize that fragility at one level) or **Inline** aggressively (to cut the chain).

## Pinning

When you **keep** a dep, hard-pin the version in the vendored `template/<pkg>.typ` — don't float, don't use a newer version "just because". Upstream's tested combination is the one you want. If you need to bump, bump explicitly and re-run `just compile`.
