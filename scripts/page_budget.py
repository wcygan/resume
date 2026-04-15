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
import shutil
import subprocess
import sys
from pathlib import Path

RESUME_DIR = Path(__file__).resolve().parent.parent
DEFAULT_PDF = RESUME_DIR / "will_cygan_resume.pdf"
MAX_PAGES = 1

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"


def page_count(pdf: Path) -> int:
    out = subprocess.check_output(["pdfinfo", str(pdf)], text=True)
    for line in out.splitlines():
        if line.startswith("Pages:"):
            return int(line.split()[1])
    raise RuntimeError("pdfinfo did not emit a 'Pages:' line")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="page_budget.py")
    ap.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    ap.add_argument("--max-pages", type=int, default=MAX_PAGES)
    args = ap.parse_args(argv)

    if not shutil.which("pdfinfo"):
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
