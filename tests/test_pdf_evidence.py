"""Focused contracts for the shared local PDF-evidence boundary."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from resume_tools import pdf_evidence


def test_tika_precedence_prefers_executable_over_configured_jar(
    tmp_path: Path,
) -> None:
    jar = tmp_path / "tika-app.jar"
    jar.write_bytes(b"test jar")

    command = pdf_evidence.tika_command(
        "--version",
        environ={"TIKA_JAR": str(jar)},
        which=lambda tool: "/usr/local/bin/tika" if tool == "tika" else "/usr/bin/java",
    )

    assert command == ["tika", "--version"]


def test_tika_uses_configured_jar_before_homebrew_fallback(tmp_path: Path) -> None:
    configured = tmp_path / "configured-tika.jar"
    fallback = tmp_path / "homebrew-tika.jar"
    configured.write_bytes(b"configured")
    fallback.write_bytes(b"fallback")

    command = pdf_evidence.tika_command(
        "-t",
        "resume.pdf",
        environ={"TIKA_JAR": str(configured)},
        which=lambda tool: "/usr/bin/java" if tool == "java" else None,
        jar_candidates=(fallback,),
    )

    assert command == ["java", "-jar", str(configured), "-t", "resume.pdf"]


def test_process_failure_timeout_and_evidence_capture(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    def failed_run(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(["pdfinfo"], 2, "", "broken input")

    monkeypatch.setattr(pdf_evidence.subprocess, "run", failed_run)
    with pytest.raises(pdf_evidence.ProcessFailureError, match="rc=2"):
        pdf_evidence.run_process(("pdfinfo", "resume.pdf"))

    def timed_out(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess[str]:
        raise subprocess.TimeoutExpired(["pdftotext"], 3)

    monkeypatch.setattr(pdf_evidence.subprocess, "run", timed_out)
    with pytest.raises(pdf_evidence.ProcessTimeoutError, match="timed out after 3s"):
        pdf_evidence.run_process(("pdftotext", "resume.pdf"), timeout_seconds=3)

    def succeeded(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(["pdfinfo"], 0, "Pages: 1\n", "diagnostic\n")

    monkeypatch.setattr(pdf_evidence.subprocess, "run", succeeded)
    stdout = tmp_path / "pdfinfo.txt"
    stderr = tmp_path / "pdfinfo.stderr"
    result = pdf_evidence.run_process(
        ("pdfinfo", "resume.pdf"), stdout_path=stdout, stderr_path=stderr
    )
    assert result.returncode == 0
    assert stdout.read_text() == "Pages: 1\n"
    assert stderr.read_text() == "diagnostic\n"


def test_normalizes_poppler_and_qpdf_evidence() -> None:
    assert pdf_evidence.parse_pdfinfo(
        "Pages:          1\nPage size:      612 x 792 pts (letter)\n"
        "Page rot:       0\nTagged:         yes\n"
    ) == {
        "Pages": "1",
        "Page size": "612 x 792 pts (letter)",
        "Page rot": "0",
        "Tagged": "yes",
    }
    fonts = pdf_evidence.parse_fonts(
        "name type encoding emb sub uni object ID\n"
        "ABCDE+SourceSans3 Type 1C Identity-H yes yes yes 8 0\n"
    )
    assert fonts == [
        pdf_evidence.FontEvidence(
            raw="ABCDE+SourceSans3 Type 1C Identity-H yes yes yes 8 0",
            embedded="yes",
            subset="yes",
            unicode="yes",
        )
    ]
    assert pdf_evidence.count_images("page num type width height\n  1   0 image 100 100\n") == 1
    qdf = pdf_evidence.parse_qdf(
        "/StructTreeRoot\n/MarkInfo\n/S /H1\n/S /H1\n/URI (https://example.com)\n",
        ("H1", "L"),
    )
    assert qdf.has_struct_tree_root and qdf.has_mark_info
    assert qdf.structure_counts == {"H1": 2, "L": 0}
    assert qdf.uris == ("https://example.com",)


def test_active_partial_discovery_and_golden_full_policy(tmp_path: Path) -> None:
    discovery = pdf_evidence.discover_text_extractors(
        tmp_path / "resume.pdf",
        which=lambda tool: "/usr/bin/pdftotext" if tool == "pdftotext" else None,
    )

    assert [extractor.name for extractor in discovery.extractors] == [
        "pdftotext",
        "pdftotext -layout",
    ]
    assert discovery.skipped and discovery.skipped[0].startswith("tika:")

    with pytest.raises(pdf_evidence.ToolUnavailableError, match="pdffonts"):
        pdf_evidence.require_tools(
            ("pdfinfo", "pdffonts"),
            require_tika=True,
            which=lambda tool: "/usr/bin/pdfinfo" if tool == "pdfinfo" else None,
        )
