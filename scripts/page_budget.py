#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Page-budget check on will_cygan_resume.pdf.

Shells out to `pdfinfo` (poppler) to read the page count and fails if it
exceeds MAX_PAGES. Kept separate from extraction-check: that gate is about
text-extraction fidelity; this one is about layout budget.

Exit codes:
  0 - page count within budget
  1 - page count over budget
  2 - preflight failure (missing pdfinfo, missing PDF)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from resume_tools import pdf_evidence

RESUME_DIR = REPO_ROOT
DEFAULT_PDF = RESUME_DIR / "will_cygan_resume.pdf"
MAX_PAGES = 1

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"


def page_count(pdf: Path) -> int:
    return pdf_evidence.page_count(pdf)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="page_budget.py")
    ap.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    ap.add_argument("--max-pages", type=int, default=MAX_PAGES)
    args = ap.parse_args(argv)

    try:
        pdf_evidence.require_tools(("pdfinfo",))
    except pdf_evidence.ToolUnavailableError:
        print(f"{RED}pdfinfo not found — install poppler "
              f"(brew install poppler / apt-get install poppler-utils){RESET}",
              file=sys.stderr)
        return 2
    if not args.pdf.exists():
        print(f"{RED}PDF not found: {args.pdf}{RESET}", file=sys.stderr)
        print(f"{YELLOW}Run `just compile` first.{RESET}", file=sys.stderr)
        return 2

    pages = page_count(args.pdf)
    if pages > args.max_pages:
        print(f"{RED}page-budget: FAIL — {pages} pages "
              f"(max {args.max_pages}){RESET}", file=sys.stderr)
        return 1
    print(f"{GREEN}page-budget: PASS — {pages}/{args.max_pages} page(s){RESET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
