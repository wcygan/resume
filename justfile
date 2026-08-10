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

# Rebuild and evaluate the Golden Resume with the repository-owned deep gate.
golden-check: golden
    uv run --no-project .agents/skills/resume-parsability/scripts/evaluate_golden_resume.py

# Compile and evaluate isolated content-length stresses through the Golden renderer.
golden-stress *ARGS:
    uv run --no-project .agents/skills/resume-parsability/scripts/evaluate_golden_stress_matrix.py {{ ARGS }}

# Run GitHub Actions workflows locally via act.
ci *ARGS:
    uv run scripts/run-local-ci.py {{ ARGS }}

# Validate resume-content changes through compile, page-budget, and extraction checks.
validate-content:
    uv run --no-project -m resume_tools.validation content

# Validate renderer changes through content, Golden, and stress checks.
validate-renderer:
    uv run --no-project -m resume_tools.validation renderer

# Run the complete CI-parity plan, including the project test suite.
validate-full:
    uv run --no-project -m resume_tools.validation full

# ATS text-extraction regression check (pdftotext + Tika).
extraction-check:
    uv run scripts/extraction_check.py

# Fail if the compiled PDF exceeds one page.
page-budget:
    uv run scripts/page_budget.py

# Run the full project test suite; full Golden checks need Typst, Poppler, qpdf, and Tika or TIKA_JAR with Java.
test:
    uv run --with pytest pytest tests/ -v
