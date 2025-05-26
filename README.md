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

## Local CI with Act

This repository includes a Deno script to run GitHub Actions locally using [Act](https://github.com/nektos/act). This provides fast feedback for testing workflow changes without pushing to GitHub.

### Prerequisites

- [Deno](https://deno.land/) - JavaScript/TypeScript runtime
- [Act](https://github.com/nektos/act) - Run GitHub Actions locally
- [Docker](https://www.docker.com/) - Required by Act

### Usage

```bash
# Run the workflow locally
./scripts/run-local-ci.ts

# Run with verbose output
./scripts/run-local-ci.ts --verbose

# Dry run to see what would execute
./scripts/run-local-ci.ts --dry-run

# Show help
./scripts/run-local-ci.ts --help

# List available workflows
./scripts/run-local-ci.ts --list
```

### Features

- **Fast Feedback**: Test workflow changes locally without pushing
- **Real-time Output**: Stream compilation output in real-time
- **Artifact Simulation**: Simulates GitHub Actions artifact upload
- **Error Handling**: Clear error messages and exit codes
- **Prerequisites Check**: Validates that Act and Docker are available