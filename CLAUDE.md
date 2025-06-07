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
- **`archive/`** - Contains deprecated LaTeX files and reference materials for historical purposes

### Build System
- **Typst** - Modern typesetting system for document generation
- **GitHub Actions** - Automated compilation on push/PR to main/master
- **Deno tasks** - Build automation with TypeScript scripts

### Development Workflow
1. Edit `will_cygan_resume.typ` 
2. Use `typst watch` for live preview (or VSCode Tinymist extension)
3. Test locally with `./scripts/run-local-ci.ts` before pushing
4. GitHub Actions will compile and store PDF artifact on push

## Resume Optimization Workflow

### Available Slash Commands
This project includes a systematic resume optimization system using Claude Code slash commands:

```bash
# Strategic Analysis (Run First)
/project:resume:review              # Comprehensive analysis with action plan

# Tactical Optimization (Run Based on Review)
/project:resume:bullets             # Optimize bullet points with STAR/XYZ methods
/project:resume:verbs               # Replace weak action verbs with stronger alternatives  
/project:resume:skills              # Restructure and optimize the skills section
/project:resume:tailor <job_desc>   # Tailor resume to specific job descriptions
```

### Recommended Optimization Process
1. **Strategic Planning:** Start with `/project:resume:review` for comprehensive analysis
2. **Tactical Execution:** Run suggested executor commands from the review
3. **Apply Changes:** Edit `will_cygan_resume.typ` based on recommendations
4. **Job-Specific Tailoring:** Use `/project:resume:tailor` with target job descriptions
5. **Iterative Improvement:** Re-run `/project:resume:review` after changes

### Knowledge Base
The commands leverage expert advice from the `/advice` directory, including:
- STAR/XYZ bullet point methodology
- ATS optimization strategies
- Industry-specific best practices
- Quantification techniques
- Action verb enhancement

## Important Notes

- The project uses the `modern-cv` Typst template for professional formatting
- PDF output is named `will_cygan_resume.pdf`
- CI artifacts are retained for 30 days
- The dev script (`scripts/dev.ts`) handles cross-platform PDF opening
- Always run `/project:resume:review` before making systematic changes
- Use the executor commands to maintain consistency with proven best practices