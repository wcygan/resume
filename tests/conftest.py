"""pytest fixtures for the extraction-check negative-fixture suite.

Each broken Typst source under tests/fixtures/broken/ is compiled to a
PDF exactly once per test session (the PDF is deterministic for a given
.typ + typst version), cached in a tmp dir, and handed to tests via the
`broken_pdf` fixture factory.

No tests are marked xfail — negative fixtures *must* fail the real
extraction-check, otherwise the gate is broken. The tests assert on
exit code AND on specific assertion-name substrings in stdout so a
future regression where the wrong assertion fires is caught.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "extraction-check.py"
BASELINE_FIXTURES = REPO_ROOT / "tests" / "fixtures" / "baseline.fixtures.toml"
BROKEN_DIR = REPO_ROOT / "tests" / "fixtures" / "broken"


def _have(binary: str) -> bool:
    return shutil.which(binary) is not None


def _have_tika() -> bool:
    if _have("tika"):
        return True
    if os.environ.get("TIKA_JAR") and Path(os.environ["TIKA_JAR"]).exists():
        return True
    for p in (
        REPO_ROOT / "template" / "tika-app.jar",
        Path("/opt/homebrew/opt/tika/libexec/tika-app.jar"),
    ):
        if p.exists():
            return True
    return False


@pytest.fixture(scope="session")
def require_typst() -> None:
    if not _have("typst"):
        pytest.skip("typst binary not available")


@pytest.fixture(scope="session")
def require_pdftotext() -> None:
    if not _have("pdftotext"):
        pytest.skip("pdftotext not available (brew install poppler)")


@pytest.fixture(scope="session")
def require_tika() -> None:
    if not _have_tika():
        pytest.skip("tika not available (brew install tika)")


@pytest.fixture(scope="session")
def broken_pdf(
    tmp_path_factory: pytest.TempPathFactory, require_typst: None
) -> Callable[[str], Path]:
    """Compile a broken/<name>.typ on demand, cache per session."""
    cache_dir = tmp_path_factory.mktemp("broken-pdfs")
    cache: dict[str, Path] = {}

    def _compile(name: str) -> Path:
        if name in cache:
            return cache[name]
        src = BROKEN_DIR / f"{name}.typ"
        if not src.exists():
            raise FileNotFoundError(src)
        pdf = cache_dir / f"{name}.pdf"
        r = subprocess.run(
            ["typst", "compile", str(src), str(pdf)],
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            raise RuntimeError(
                f"typst compile failed for {name}: {r.stderr}"
            )
        cache[name] = pdf
        return pdf

    return _compile


@pytest.fixture(scope="session")
def run_check(tmp_path_factory: pytest.TempPathFactory):
    """Return a callable that runs extraction-check.py against a given PDF."""
    report_root = tmp_path_factory.mktemp("extraction-reports")

    def _run(
        pdf: Path, fixtures: Path = BASELINE_FIXTURES
    ) -> subprocess.CompletedProcess[str]:
        report_dir = report_root / pdf.stem
        return subprocess.run(
            [
                "uv",
                "run",
                str(SCRIPT),
                "--pdf",
                str(pdf),
                "--fixtures",
                str(fixtures),
                "--report-dir",
                str(report_dir),
            ],
            capture_output=True,
            text=True,
        )

    return _run
