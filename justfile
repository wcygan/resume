default:
    @just --list

# Live preview — opens the PDF and runs `typst watch`.
dev:
    uv run scripts/dev.py

# One-shot typst compile.
compile:
    uv run --no-project -m resume_tools.artifact resume

# Build the parser-friendly reference resume with the pinned Source Sans 3 cuts.
golden:
    uv run --no-project -m resume_tools.artifact golden

# Rebuild and evaluate the Golden Resume with the skill-owned deep gate.
golden-check: golden
    uv run --no-project .agents/skills/resume-parsability/scripts/evaluate_golden_resume.py

# Compile and evaluate isolated content-length stresses through the Golden renderer.
golden-stress *ARGS:
    uv run --no-project .agents/skills/resume-parsability/scripts/evaluate_golden_stress_matrix.py {{ARGS}}

# Run GitHub Actions workflows locally via act.
ci *ARGS:
    uv run scripts/run-local-ci.py {{ARGS}}

# Ordered validation plans. Individual commands below remain useful for
# focused diagnosis; use these plans for change acceptance and CI parity.
validate-content:
    uv run --no-project -m resume_tools.validation content

validate-renderer:
    uv run --no-project -m resume_tools.validation renderer

validate-full:
    uv run --no-project -m resume_tools.validation full

# ATS text-extraction regression check (pdftotext + Tika).
extraction-check:
    uv run scripts/extraction_check.py

# Fail if the compiled PDF exceeds one page.
page-budget:
    uv run scripts/page_budget.py

# Negative-fixture regression suite for extraction-check.
# Requires typst, poppler (pdftotext), and tika on PATH.
test:
    uv run --with pytest pytest tests/ -v
