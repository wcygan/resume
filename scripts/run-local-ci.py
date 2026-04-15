#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Run GitHub Actions workflows locally via `act`."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

WORKFLOWS_DIR = Path(".github/workflows")
DEFAULT_PLATFORM = "ubuntu-latest=catthehacker/ubuntu:act-latest"

# ANSI colors
BLUE = "\033[34m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
GRAY = "\033[90m"
RESET = "\033[0m"


def c(color: str, msg: str) -> str:
    return f"{color}{msg}{RESET}"


def check_prereqs() -> None:
    print(c(BLUE, "Checking prerequisites..."))
    missing: list[str] = []

    if shutil.which("act") is None:
        missing.append("act")
    else:
        r = subprocess.run(["act", "--version"], capture_output=True)
        if r.returncode != 0:
            missing.append("act")

    if shutil.which("docker") is None:
        missing.append("docker")
    else:
        r = subprocess.run(["docker", "info"], capture_output=True)
        if r.returncode != 0:
            missing.append("docker (daemon not running)")

    if missing:
        print(c(RED, f"Prerequisites check failed: missing/unavailable: {', '.join(missing)}"))
        print(c(YELLOW, "\nInstallation:"))
        print("  Act (macOS): brew install act")
        print("  Act (Linux): curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash")
        print("  Docker:      https://docs.docker.com/get-docker/")
        print(c(YELLOW, "\nMake sure Docker is installed and running."))
        sys.exit(1)

    print(c(GREEN, "Prerequisites check passed"))


def list_workflows() -> list[str]:
    if not WORKFLOWS_DIR.is_dir():
        return []
    return sorted(
        p.name for p in WORKFLOWS_DIR.iterdir()
        if p.is_file() and p.suffix in {".yml", ".yaml"}
    )


def cmd_list() -> None:
    print(c(BLUE, "Available workflows:"))
    wfs = list_workflows()
    if not wfs:
        print(c(YELLOW, "  No workflows found in .github/workflows/"))
        return
    for wf in wfs:
        print(f"  - {wf}")


def run_workflow(workflow: str, job: str | None, verbose: bool, dry_run: bool) -> int:
    print(c(BLUE, f"Running workflow: {workflow}"))
    if dry_run:
        print(c(YELLOW, "Dry run mode"))

    args: list[str] = []
    if job:
        args += ["--job", job]
    if verbose:
        args.append("--verbose")
    if dry_run:
        args.append("--dryrun")
    args += ["--platform", DEFAULT_PLATFORM]

    print(c(GRAY, f"Running: act {' '.join(args)}"))
    result = subprocess.run(["act", *args])
    if result.returncode == 0:
        print(c(GREEN, "\nWorkflow completed successfully"))
        pdf = Path("will_cygan_resume.pdf")
        if pdf.exists():
            print(c(GREEN, f"Resume PDF generated ({pdf.stat().st_size // 1024}KB)"))
        else:
            print(c(YELLOW, "PDF file not found in current directory"))
    else:
        print(c(RED, f"\nWorkflow failed with exit code: {result.returncode}"))
    return result.returncode


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="run-local-ci.py",
        description="Run GitHub Actions workflows locally via act.",
    )
    p.add_argument("--workflow", default="compile-resume.yml",
                   help="Specify workflow file (default: compile-resume.yml)")
    p.add_argument("--job", help="Run specific job only")
    p.add_argument("--verbose", action="store_true", help="Enable verbose output")
    p.add_argument("--dry-run", action="store_true", help="Show what would be executed")
    p.add_argument("--list", action="store_true", help="List available workflows")
    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.list:
        cmd_list()
        return 0

    check_prereqs()
    return run_workflow(args.workflow, args.job, args.verbose, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
