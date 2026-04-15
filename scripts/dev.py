#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Opens the resume PDF and starts `typst watch`."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

RESUME_DIR = Path(__file__).resolve().parent.parent
PDF = "will_cygan_resume.pdf"
SRC = "will_cygan_resume.typ"


def open_pdf() -> None:
    print(f"Opening {PDF}...")
    try:
        if sys.platform == "darwin":
            subprocess.run(["open", PDF], check=False)
        elif sys.platform.startswith("linux"):
            subprocess.run(["xdg-open", PDF], check=False)
        elif sys.platform == "win32":
            os.startfile(PDF)  # type: ignore[attr-defined]
        else:
            print("Warning: unknown OS; trying xdg-open...")
            subprocess.run(["xdg-open", PDF], check=False)
    except FileNotFoundError as e:
        print(f"Could not open PDF automatically: {e}")


def main() -> int:
    os.chdir(RESUME_DIR)
    open_pdf()
    print("Starting typst watch...")
    return subprocess.run(["typst", "watch", SRC]).returncode


if __name__ == "__main__":
    raise SystemExit(main())
