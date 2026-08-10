"""Acquire and normalize local evidence from PDF inspection tools.

This module deliberately owns tool discovery and process mechanics, while its
callers own policy.  The fast active-resume check may continue with whichever
text extractors are present; the Golden evaluator explicitly requires every
tool needed for its broader mechanical audit.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

DEFAULT_TIMEOUT_SECONDS = 60
HOMEBREW_TIKA_JAR = Path("/opt/homebrew/opt/tika/libexec/tika-app.jar")


class PdfEvidenceError(RuntimeError):
    """Base error for a local PDF-evidence operation."""


class ToolUnavailableError(PdfEvidenceError):
    """A required local PDF tool could not be found."""


class ProcessTimeoutError(PdfEvidenceError):
    """A local PDF tool exceeded its bounded execution time."""


class ProcessFailureError(PdfEvidenceError):
    """A local PDF tool completed unsuccessfully."""


@dataclass(frozen=True)
class Extractor:
    """One text extraction representation and its command."""

    name: str
    argv: tuple[str, ...]


@dataclass(frozen=True)
class ProcessResult:
    """Captured result of a local inspection command."""

    argv: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str


@dataclass(frozen=True)
class FontEvidence:
    raw: str
    embedded: str
    subset: str
    unicode: str


@dataclass(frozen=True)
class QdfEvidence:
    """Normalized structural and link inventory from qpdf QDF output."""

    has_struct_tree_root: bool
    has_mark_info: bool
    structure_counts: dict[str, int]
    uris: tuple[str, ...]


@dataclass(frozen=True)
class TextExtractorDiscovery:
    """Available text representations and explicit missing-tool notes."""

    extractors: tuple[Extractor, ...]
    skipped: tuple[str, ...]


def tika_command(
    *arguments: str,
    environ: Mapping[str, str] | None = None,
    which: Callable[[str], str | None] = shutil.which,
    jar_candidates: Sequence[Path] = (HOMEBREW_TIKA_JAR,),
) -> list[str] | None:
    """Return the canonical Tika command, or ``None`` when unavailable.

    Precedence is intentionally identical for every caller: a PATH executable,
    then the explicitly configured ``TIKA_JAR``, then the existing Homebrew
    adapter.  A JAR is usable only with a local Java executable.
    """
    if which("tika") is not None:
        return ["tika", *arguments]

    environment = os.environ if environ is None else environ
    configured_jar = environment.get("TIKA_JAR")
    candidates = ([Path(configured_jar)] if configured_jar else []) + list(jar_candidates)
    if which("java") is None:
        return None
    for jar in candidates:
        if jar.is_file():
            return ["java", "-jar", str(jar), *arguments]
    return None


def require_tools(
    tools: Sequence[str],
    *,
    require_tika: bool = False,
    which: Callable[[str], str | None] = shutil.which,
    environ: Mapping[str, str] | None = None,
) -> None:
    """Enforce a caller-selected set of local tools.

    This is intentionally not used by the active extraction gate: it is the
    Golden evaluator's full-tool policy, not a module-wide policy.
    """
    missing = [tool for tool in tools if which(tool) is None]
    if require_tika and tika_command(
        "--version", environ=environ, which=which
    ) is None:
        missing.append("tika or TIKA_JAR with java")
    if missing:
        raise ToolUnavailableError(
            f"required tools are unavailable: {', '.join(missing)}"
        )


def discover_text_extractors(
    pdf: Path,
    *,
    environ: Mapping[str, str] | None = None,
    which: Callable[[str], str | None] = shutil.which,
) -> TextExtractorDiscovery:
    """Discover available text views without requiring a complete tool set."""
    available: list[Extractor] = []
    skipped: list[str] = []
    if which("pdftotext") is not None:
        available.extend(
            (
                Extractor("pdftotext", ("pdftotext", str(pdf), "-")),
                Extractor(
                    "pdftotext -layout",
                    ("pdftotext", "-layout", str(pdf), "-"),
                ),
            )
        )
    else:
        skipped.append("pdftotext: missing. Install with `brew install poppler`.")

    tika = tika_command("--text", str(pdf), environ=environ, which=which)
    if tika is not None:
        available.append(Extractor("tika", tuple(tika)))
    else:
        skipped.append(
            "tika: missing. Install with `brew install tika` "
            "or set TIKA_JAR with Java available."
        )
    return TextExtractorDiscovery(tuple(available), tuple(skipped))


def run_process(
    argv: Sequence[str],
    *,
    cwd: Path | None = None,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    check: bool = True,
    stdout_path: Path | None = None,
    stderr_path: Path | None = None,
) -> ProcessResult:
    """Run one local inspection command with normalized errors and capture."""
    command = tuple(str(argument) for argument in argv)
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            check=False,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
        )
    except FileNotFoundError as error:
        raise ToolUnavailableError(f"tool is unavailable: {command[0]}") from error
    except subprocess.TimeoutExpired as error:
        raise ProcessTimeoutError(
            f"{' '.join(command)} timed out after {timeout_seconds}s"
        ) from error

    result = ProcessResult(command, completed.returncode, completed.stdout, completed.stderr)
    if stdout_path is not None:
        stdout_path.parent.mkdir(parents=True, exist_ok=True)
        stdout_path.write_text(result.stdout, encoding="utf-8")
    if stderr_path is not None:
        stderr_path.parent.mkdir(parents=True, exist_ok=True)
        stderr_path.write_text(result.stderr, encoding="utf-8")
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ProcessFailureError(
            f"{' '.join(command)} failed (rc={result.returncode}): {detail[:400]}"
        )
    return result


def command_version(argv: Sequence[str], *, cwd: Path | None = None) -> str:
    """Return the first version line while preserving process failure context."""
    result = run_process(argv, cwd=cwd)
    output = result.stdout + result.stderr
    return output.strip().splitlines()[0] if output.strip() else ""


def parse_pdfinfo(text: str) -> dict[str, str | None]:
    """Normalize the small pdfinfo field set the resume contracts consume."""
    values: dict[str, str | None] = {}
    for key in ("Pages", "Page size", "Page rot", "Tagged"):
        match = re.search(rf"^{re.escape(key)}:\s*(.+)$", text, flags=re.MULTILINE)
        values[key] = match.group(1).strip() if match else None
    return values


def page_count(pdf: Path, *, cwd: Path | None = None) -> int:
    """Read the page count through pdfinfo and translate malformed evidence."""
    values = parse_pdfinfo(run_process(("pdfinfo", str(pdf)), cwd=cwd).stdout)
    try:
        return int(values["Pages"] or "")
    except ValueError as error:
        raise PdfEvidenceError("pdfinfo did not emit a valid 'Pages:' line") from error


def parse_fonts(text: str) -> list[FontEvidence]:
    """Normalize Poppler's font table to the embedding fields used by gates."""
    fonts: list[FontEvidence] = []
    for line in text.splitlines():
        match = re.search(r"\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$", line)
        if match:
            fonts.append(FontEvidence(line, match.group(1), match.group(2), match.group(3)))
    return fonts


def count_images(text: str) -> int:
    """Count Poppler image rows, excluding its header and summary lines."""
    return sum(bool(re.match(r"\s*\d+\s+\d+\s+", line)) for line in text.splitlines())


def parse_qdf(text: str, structure_tags: Sequence[str]) -> QdfEvidence:
    """Normalize qpdf's QDF structure and URI inventory without applying policy."""
    return QdfEvidence(
        has_struct_tree_root="/StructTreeRoot" in text,
        has_mark_info="/MarkInfo" in text,
        structure_counts={
            tag: len(re.findall(rf"/S /{re.escape(tag)}\b", text))
            for tag in structure_tags
        },
        uris=tuple(re.findall(r"/URI \((.*?)\)", text)),
    )


def capture_pdf_evidence(
    pdf: Path,
    output_dir: Path,
    *,
    cwd: Path | None = None,
    include_xml: bool = False,
    include_qdf: bool = False,
    render_dpi: int | None = None,
) -> dict[str, ProcessResult]:
    """Capture named raw evidence files needed by the deep Golden evaluator.

    Callers decide which commands are required.  This helper only executes and
    writes raw evidence; it never applies a passing/failing PDF policy.
    """
    artifact = str(pdf)
    output_dir.mkdir(parents=True, exist_ok=True)
    commands: list[tuple[str, tuple[str, ...], Path, Path]] = [
        ("pdfinfo", ("pdfinfo", artifact), output_dir / "pdfinfo.txt", output_dir / "pdfinfo.stderr"),
        ("pdffonts", ("pdffonts", artifact), output_dir / "pdffonts.txt", output_dir / "pdffonts.stderr"),
        ("pdfimages", ("pdfimages", "-list", artifact), output_dir / "pdfimages.txt", output_dir / "pdfimages.stderr"),
        ("poppler_plain", ("pdftotext", artifact, "-"), output_dir / "poppler-plain.txt", output_dir / "pdftotext-plain.stderr"),
        ("poppler_layout", ("pdftotext", "-layout", artifact, "-"), output_dir / "poppler-layout.txt", output_dir / "pdftotext-layout.stderr"),
    ]
    if include_xml:
        commands.append(("poppler_xml", ("pdftohtml", "-xml", "-hidden", "-i", "-stdout", artifact), output_dir / "poppler.xml", output_dir / "pdftohtml.stderr"))
    tika = tika_command("-t", artifact)
    if tika is None:
        raise ToolUnavailableError("Tika requires either the tika executable or TIKA_JAR with java")
    commands.append(("tika", tuple(tika), output_dir / "tika.txt", output_dir / "tika.stderr"))

    results = {
        name: run_process(argv, cwd=cwd, check=False, stdout_path=stdout, stderr_path=stderr)
        for name, argv, stdout, stderr in commands
    }
    results["qpdf_check"] = run_process(
        ("qpdf", "--check", artifact), cwd=cwd, check=False,
        stdout_path=output_dir / "qpdf-check.stdout", stderr_path=output_dir / "qpdf-check.stderr",
    )
    qpdf_check = results["qpdf_check"]
    (output_dir / "qpdf-check.txt").write_text(
        qpdf_check.stdout + qpdf_check.stderr, encoding="utf-8"
    )
    if include_qdf:
        results["qpdf_qdf"] = run_process(
            ("qpdf", "--qdf", "--object-streams=disable", artifact, str(output_dir / "qdf.pdf")),
            cwd=cwd, check=False, stderr_path=output_dir / "qdf.stderr",
        )
    if render_dpi is not None:
        pages = parse_pdfinfo(results["pdfinfo"].stdout)["Pages"]
        render = ["pdftoppm", "-png", "-r", str(render_dpi)]
        if pages == "1":
            render.append("-singlefile")
        render.extend((artifact, str(output_dir / f"render-{render_dpi}dpi")))
        results["render"] = run_process(
            render, cwd=cwd, check=False, stderr_path=output_dir / "render.stderr"
        )
    return results
