# Typst Version-Drift Fixes

Pre-0.13 `@preview` packages commonly emit deprecated idioms. Apply these mechanically while vendoring.

| Old (breaks on 0.13+) | New | Notes |
|---|---|---|
| `type(x) == "string"` | `type(x) == str` | `type()` returns a type, not a string. |
| `type(x) == "integer"` | `type(x) == int` | Same. |
| `type(x) == "dictionary"` | `type(x) == dictionary` | Same. |
| `locate(loc => ...)` | `context { ... }` | `locate` removed in favor of `context`. |
| `style(styles => ...)` | `context { ... }` | Same pattern. |
| `image(path: "...")` | `image(source: "...")` or positional `image("...")` | Parameter renamed in 0.13. |
| `#show par: set block(spacing: ...)` | `#set par(spacing: ...)` | Direct set rule added. |
| Top-level `#columns(n)[...]` | `#set page(columns: n)` | Top-level usage discouraged. |
| `toml("lang.toml")` + `linguify(...)` | Inline the strings you need | Drops a dep entirely if i18n is single-language. |

## Detection grep

Before trimming, scan the upstream `lib.typ` for things that will break:

```bash
grep -nE 'type\(.+\) == "|locate\(|style\(.+=>|image\(path:|#show par: set block\(spacing' lib.typ
```

Any hit → fix it in the vendored copy.

## Deeper reference

The project's `typst` skill has a fuller `references/version-drift.md` with explanations for each item and context on why the pre-0.12 forms were deprecated. Consult it when a fix in the table above doesn't fit the exact pattern in your package.
