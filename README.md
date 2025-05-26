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
typst watch will_cygan_resume.typ
```

## Generate Final Resume

To generate the final resume as `will_cygan_resume.pdf`:
```bash
typst compile will_cygan_resume.typ will_cygan_resume.pdf
```

Or to generate with the default name `will_cygan_resume.pdf`:
```bash
typst compile will_cygan_resume.typ
```

## GitHub Actions

This repository includes a GitHub Actions workflow that automatically compiles the resume on every push and pull request. The workflow:

1. Sets up Typst using the [setup-typst action](https://github.com/marketplace/actions/setup-typst)
2. Compiles `will_cygan_resume.typ` to `will_cygan_resume.pdf`
3. Uploads the compiled PDF as a workflow artifact
4. Verifies the compilation was successful

The workflow runs on Ubuntu and uses Typst version ^0.13.0. You can download the compiled resume from the Actions tab after each successful run.