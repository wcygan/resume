"""pytest fixtures for the extraction-check negative-fixture suite.

Broken Typst sources under tests/fixtures/broken/ are compiled to PDF once
per session and fed to extraction_check.evaluate_pdf in-process (no subprocess,
no uv-run overhead, no stdout scraping). Tests assert on structured results.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
BASELINE_FIXTURES = REPO_ROOT / "tests" / "fixtures" / "baseline.fixtures.toml"
BROKEN_DIR = REPO_ROOT / "tests" / "fixtures" / "broken"

sys.path.insert(0, str(SCRIPTS_DIR))
import extraction_check as ec  # noqa: E402


@pytest.fixture(scope="session")
def require_typst() -> None:
    if not shutil.which("typst"):
        pytest.skip("typst binary not available")


@pytest.fixture(scope="session")
def require_pdftotext() -> None:
    if not shutil.which("pdftotext"):
        pytest.skip("pdftotext not available (brew install poppler)")


@pytest.fixture(scope="session")
def require_tika() -> None:
    # Probe with a sentinel path; detect_tika doesn't read the PDF to decide.
    if ec.detect_tika(Path("/dev/null")) is None:
        pytest.skip("tika not available (brew install tika)")


@pytest.fixture(scope="session")
def broken_pdf(
    tmp_path_factory: pytest.TempPathFactory, require_typst: None
) -> Callable[[str], Path]:
    cache_dir = tmp_path_factory.mktemp("broken-pdfs")
    cache: dict[str, Path] = {}

    def _compile(name: str) -> Path:
        if name in cache:
            return cache[name]
        src = BROKEN_DIR / f"{name}.typ"
        pdf = cache_dir / f"{name}.pdf"
        r = subprocess.run(
            ["typst", "compile", str(src), str(pdf)],
            capture_output=True, text=True,
        )
        if r.returncode != 0:
            raise RuntimeError(f"typst compile failed for {name}: {r.stderr}")
        cache[name] = pdf
        return pdf

    return _compile


@pytest.fixture(scope="session")
def run_check() -> Callable[[Path], ec.EvaluationResult]:
    fx_cache: dict[Path, dict] = {}

    def _run(pdf: Path, fixtures: Path = BASELINE_FIXTURES) -> ec.EvaluationResult:
        if fixtures not in fx_cache:
            fx_cache[fixtures] = ec.load_fixtures(fixtures)
        return ec.evaluate_pdf(pdf, fx_cache[fixtures])

    return _run
