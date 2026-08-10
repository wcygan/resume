"""Execute the repository's ordered resume-validation plans.

This module owns which checks belong to each change intent, their order, and
the evidence path to inspect after a failure.  Individual scripts retain their
specialist policies: artifact construction lives in :mod:`resume_tools.artifact`
and PDF inspection lives behind the existing page-budget and extraction-check
adapters.
"""

from __future__ import annotations

import argparse
import enum
import subprocess
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class ValidationIntent(enum.StrEnum):
    """The change scopes supported by the shared validation plan."""

    COMPILE = "compile"
    CONTENT = "content"
    RENDERER = "renderer"
    FULL = "full"


@dataclass(frozen=True)
class ValidationStep:
    """One ordered check and the durable location of its relevant evidence."""

    name: str
    command: tuple[str, ...]
    evidence_locations: tuple[Path, ...]


@dataclass(frozen=True)
class StepResult:
    """The result of one attempted validation step."""

    step: ValidationStep
    returncode: int
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.returncode == 0


@dataclass(frozen=True)
class ValidationRun:
    """A fail-fast plan execution and its original process status."""

    intent: ValidationIntent
    results: tuple[StepResult, ...]

    @property
    def returncode(self) -> int:
        return self.results[-1].returncode if self.results else 0

    @property
    def ok(self) -> bool:
        return self.returncode == 0


COMPILE_RESUME = ValidationStep(
    name="compile-resume",
    command=("uv", "run", "--no-project", "-m", "resume_tools.artifact", "resume"),
    evidence_locations=(
        Path("will_cygan_resume.pdf"),
        Path(".extraction/artifact-provenance/will_cygan_resume.pdf.json"),
    ),
)
PAGE_BUDGET = ValidationStep(
    name="page-budget",
    command=("uv", "run", "--no-project", "scripts/page_budget.py"),
    evidence_locations=(Path("will_cygan_resume.pdf"),),
)
EXTRACTION_CHECK = ValidationStep(
    name="extraction-check",
    command=("uv", "run", "--no-project", "scripts/extraction_check.py"),
    evidence_locations=(Path(".extraction"),),
)
TEST = ValidationStep(
    name="test",
    command=("uv", "run", "--with", "pytest", "pytest", "tests/", "-v"),
    evidence_locations=(),
)
COMPILE_GOLDEN = ValidationStep(
    name="compile-golden",
    command=("uv", "run", "--no-project", "-m", "resume_tools.artifact", "golden"),
    evidence_locations=(
        Path("tests/fixtures/golden-resume/golden-resume.pdf"),
        Path(".extraction/artifact-provenance/golden-resume.pdf.json"),
    ),
)
GOLDEN_CHECK = ValidationStep(
    name="golden-check",
    command=(
        "uv",
        "run",
        "--no-project",
        ".agents/skills/resume-parsability/scripts/evaluate_golden_resume.py",
    ),
    evidence_locations=(Path(".extraction/golden-resume"),),
)
GOLDEN_STRESS = ValidationStep(
    name="golden-stress",
    command=(
        "uv",
        "run",
        "--no-project",
        ".agents/skills/resume-parsability/scripts/evaluate_golden_stress_matrix.py",
    ),
    evidence_locations=(Path(".extraction/golden-resume-stress"),),
)


VALIDATION_PLANS: dict[ValidationIntent, tuple[ValidationStep, ...]] = {
    ValidationIntent.COMPILE: (COMPILE_RESUME,),
    # JSON/content changes must rebuild the observed artifact before checking
    # its page budget and text extraction.
    ValidationIntent.CONTENT: (COMPILE_RESUME, PAGE_BUDGET, EXTRACTION_CHECK),
    # The shared renderer also affects the Golden fixture and its stress cases.
    # Compile the fixture here rather than relying on the ``just golden-check``
    # recipe: the deep evaluator requires fresh artifact provenance.
    ValidationIntent.RENDERER: (
        COMPILE_RESUME,
        PAGE_BUDGET,
        EXTRACTION_CHECK,
        COMPILE_GOLDEN,
        GOLDEN_CHECK,
        GOLDEN_STRESS,
    ),
    # Repository-wide changes retain the renderer checks and add the regression
    # suite that proves the extraction assertions still reject broken fixtures.
    ValidationIntent.FULL: (
        COMPILE_RESUME,
        PAGE_BUDGET,
        EXTRACTION_CHECK,
        TEST,
        COMPILE_GOLDEN,
        GOLDEN_CHECK,
        GOLDEN_STRESS,
    ),
}

CommandRunner = Callable[[Sequence[str]], int]
Reporter = Callable[[str], None]


def _report(message: str) -> None:
    """Emit progress before the child process starts, even through a pipe."""
    print(message, flush=True)


def plan_for(intent: ValidationIntent | str) -> tuple[ValidationStep, ...]:
    """Return the immutable ordered plan for one declared change intent."""
    return VALIDATION_PLANS[ValidationIntent(intent)]


def run_command(command: Sequence[str]) -> int:
    """Run a step from the repository root without wrapping its exit status."""
    return subprocess.run(list(command), cwd=REPO_ROOT, check=False).returncode


def _format_evidence(step: ValidationStep) -> str:
    if not step.evidence_locations:
        return "the command output above"
    return ", ".join(str(location) for location in step.evidence_locations)


def run_plan(
    intent: ValidationIntent | str,
    *,
    runner: CommandRunner = run_command,
    report: Reporter = _report,
) -> ValidationRun:
    """Run one plan fail-fast, preserving failures and naming their evidence.

    A child process's nonzero status is returned unchanged so callers such as
    GitHub Actions and ``just`` observe the original failing gate.  A missing
    executable is translated to the conventional command-not-found status 127.
    """
    selected_intent = ValidationIntent(intent)
    results: list[StepResult] = []
    for step in plan_for(selected_intent):
        report(f"validation[{selected_intent}] {step.name}: {' '.join(step.command)}")
        try:
            returncode = runner(step.command)
        except OSError as error:
            result = StepResult(step, 127, str(error))
        else:
            result = StepResult(step, returncode)
        results.append(result)
        if not result.ok:
            detail = f": {result.error}" if result.error else ""
            report(
                f"validation[{selected_intent}] FAIL {step.name} "
                f"(exit {result.returncode}){detail}; evidence: {_format_evidence(step)}"
            )
            return ValidationRun(selected_intent, tuple(results))
    report(f"validation[{selected_intent}] PASS")
    return ValidationRun(selected_intent, tuple(results))


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m resume_tools.validation",
        description="Run an ordered resume validation plan.",
    )
    parser.add_argument("intent", choices=[intent.value for intent in ValidationIntent])
    parser.add_argument("--list", action="store_true", help="Print the selected plan without running it.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    intent = ValidationIntent(args.intent)
    if args.list:
        for step in plan_for(intent):
            print(f"{step.name}: {' '.join(step.command)}")
        return 0
    return run_plan(intent).returncode


if __name__ == "__main__":
    raise SystemExit(main())
