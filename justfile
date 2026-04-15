default:
    @just --list

# Live preview — opens the PDF and runs `typst watch`.
dev:
    uv run scripts/dev.py

# One-shot typst compile.
compile:
    typst compile will_cygan_resume.typ

# Run GitHub Actions workflows locally via act.
ci *ARGS:
    uv run scripts/run-local-ci.py {{ARGS}}

# ATS text-extraction regression check (pdftotext + Tika).
extraction-check:
    uv run scripts/extraction-check.py

# Negative-fixture regression suite for extraction-check.
# Requires typst, poppler (pdftotext), and tika on PATH.
test:
    uv run --with pytest pytest tests/ -v
