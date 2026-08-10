"""pytest fixtures for the extraction-check negative-fixture suite.

Broken Typst sources under tests/fixtures/broken/ are compiled to PDF once
per session and fed to extraction_check.evaluate_pdf in-process (no subprocess,
no uv-run overhead, no stdout scraping). Tests assert on structured results.
"""

from __future__ import annotations

import shutil
import sys
from collections.abc import Callable
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
BASELINE_FIXTURES = REPO_ROOT / "tests" / "fixtures" / "baseline.fixtures.toml"
BASELINE_DATA = REPO_ROOT / "tests" / "fixtures" / "baseline-resume-data.json"
BROKEN_DIR = REPO_ROOT / "tests" / "fixtures" / "broken"

sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(REPO_ROOT))
import extraction_check as ec  # noqa: E402
from resume_tools import artifact, pdf_evidence


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
    if pdf_evidence.tika_command("--text", "/dev/null") is None:
        pytest.skip(
            "tika not available (brew install tika, or set TIKA_JAR with Java)"
        )


@pytest.fixture(scope="session")
def broken_pdf(require_typst: None) -> Callable[[str], Path]:
    cache_dir = REPO_ROOT / ".extraction" / "pytest-broken-pdfs"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache: dict[str, Path] = {}

    def _compile(name: str) -> Path:
        if name in cache:
            return cache[name]
        src = BROKEN_DIR / f"{name}.typ"
        pdf = cache_dir / f"{name}.pdf"
        request = artifact.CompileRequest(
            source=src,
            output=pdf,
            purpose=artifact.ArtifactPurpose.NEGATIVE_FIXTURE,
            dependencies_path=cache_dir / f"{name}.deps.json",
        )
        r = artifact.compile_artifact(request)
        if r.returncode != 0:
            raise RuntimeError(f"typst compile failed for {name}")
        cache[name] = pdf
        return pdf

    return _compile


@pytest.fixture(scope="session")
def run_check() -> Callable[[Path], ec.EvaluationResult]:
    fx_cache: dict[tuple[Path, Path], ec.expectations.ExtractionExpectations] = {}

    def _run(
        pdf: Path,
        fixtures: Path = BASELINE_FIXTURES,
        data: Path = BASELINE_DATA,
    ) -> ec.EvaluationResult:
        key = (fixtures, data)
        if key not in fx_cache:
            fx_cache[key] = ec.load_fixtures(fixtures, data)
        return ec.evaluate_pdf(pdf, fx_cache[key])

    return _run
