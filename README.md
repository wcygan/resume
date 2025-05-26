# Resume

This repository contains the guts of my resume.

## Typst

Install Typst and dependencies:

```bash
brew install typst
brew install --cask font-fontawesome
```

## Development Workflow

For live compilation with auto-reload during development:
```bash
typst watch resume.typ
```

## Generate Final Resume

To generate the final resume as `will_cygan_resume.pdf`:
```bash
typst compile resume.typ will_cygan_resume.pdf
```

Or to generate with the default name `resume.pdf`:
```bash
typst compile resume.typ
```