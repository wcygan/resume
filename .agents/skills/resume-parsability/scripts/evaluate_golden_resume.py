#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""CLI adapter for the repository-owned Golden Resume evaluator."""

from __future__ import annotations

import argparse
import pathlib
import sys
from collections.abc import Sequence


REPO_ROOT = pathlib.Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from resume_tools import golden_evaluation  # noqa: E402


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate golden-resume.pdf with a reviewed oracle, Poppler, Tika, "
            "coordinate geometry, PDF structure, fonts, images, and links."
        )
    )
    parser.add_argument(
        "--pdf", type=pathlib.Path, default=golden_evaluation.DEFAULT_PDF
    )
    parser.add_argument(
        "--source", type=pathlib.Path, default=golden_evaluation.DEFAULT_SOURCE
    )
    parser.add_argument(
        "--provenance",
        type=pathlib.Path,
        help="Artifact provenance sidecar; defaults to the repository build location.",
    )
    parser.add_argument(
        "--oracle", type=pathlib.Path, default=golden_evaluation.DEFAULT_ORACLE
    )
    parser.add_argument(
        "--output-dir",
        type=pathlib.Path,
        help="Evidence directory. Defaults to a timestamped .extraction/golden-resume run.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    try:
        result = golden_evaluation.evaluate(
            golden_evaluation.EvaluationRequest(
                pdf=args.pdf,
                source=args.source,
                provenance=args.provenance,
                oracle=args.oracle,
                output_dir=args.output_dir,
            )
        )
    except golden_evaluation.GoldenEvaluationError as error:
        raise SystemExit(str(error)) from error

    print(f"Golden Resume automated local status: {result.automated_status}")
    print(f"Evidence: {result.evidence_directory}")
    print(f"Report: {result.report_markdown}")
    print("Visual inspection: Needs human review")
    print("External ATS / Greenhouse UAT: Untested")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
