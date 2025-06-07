# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository maintains a professional resume using Typst, a modern typesetting system. The resume is automatically compiled to PDF via GitHub Actions on push/PR.

## Common Development Commands

```bash
# Live development with auto-reload
deno task dev
# OR
typst watch will_cygan_resume.typ

# Compile to PDF
deno task compile
# OR
typst compile will_cygan_resume.typ

# Run local CI testing before pushing
./scripts/run-local-ci.ts
```

## Architecture & Key Files

### Source Files
- **`will_cygan_resume.typ`** - Main Typst source file using the modern-cv template (v0.8.0)
- **`work-experience.md`** - Reference material with detailed work experience (not directly used in compilation)

### Build System
- **Typst** - Modern typesetting system for document generation
- **GitHub Actions** - Automated compilation on push/PR to main/master
- **Deno tasks** - Build automation with TypeScript scripts

### Development Workflow
1. Edit `will_cygan_resume.typ` 
2. Use `typst watch` for live preview (or VSCode Tinymist extension)
3. Test locally with `./scripts/run-local-ci.ts` before pushing
4. GitHub Actions will compile and store PDF artifact on push

## Important Notes

- The project uses the `modern-cv` Typst template for professional formatting
- PDF output is named `will_cygan_resume.pdf`
- CI artifacts are retained for 30 days
- The dev script (`scripts/dev.ts`) handles cross-platform PDF opening