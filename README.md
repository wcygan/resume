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

Install [Tinymist Typst](https://marketplace.visualstudio.com/items?itemName=myriad-dreamin.tinymist) to enable live preview in VSCode.

This can be done through the Command Palette (Ctrl+Shift+P) with `Typst Preview: Preview Opened File`

## Generate Final Resume

To generate with the default name `will_cygan_resume.pdf`:

```bash
typst compile will_cygan_resume.typ
```
