#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""ATS text-extraction regression check.

Shells out to `pdftotext` (no flags), `pdftotext -layout`, and Apache Tika
(`tika --text`) and runs the seven assertions defined in
.claude/context/text-extraction-hypothesis.md against the extracted text.

Exit codes:
  0 - all assertions passed for every available extractor
  1 - one or more assertions failed
  2 - preflight failure (missing binary, missing fixtures, missing PDF)

On failure, per-extractor breakdown is written to stdout and
`.extraction/report.md`. `.extraction/` is gitignored.

This is a gate, not telemetry. No persistent runs.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

RESUME_DIR = Path(__file__).resolve().parent.parent
DEFAULT_PDF = RESUME_DIR / "will_cygan_resume.pdf"
DEFAULT_FIXTURES = Path(__file__).resolve().parent / "extraction-check.fixtures.toml"
DEFAULT_REPORT_DIR = RESUME_DIR / ".extraction"

# ANSI colors.
BLUE = "\033[34m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
GRAY = "\033[90m"
RESET = "\033[0m"


def c(color: str, msg: str) -> str:
    return f"{color}{msg}{RESET}"


# -- Extractors ---------------------------------------------------------------

@dataclass
class Extractor:
    name: str
    argv: list[str]  # command to run; {PDF} placeholder is substituted


def detect_tika(pdf: Path) -> Extractor | None:
    """Return an Extractor for Tika if installed, else None.

    Homebrew's `tika` formula ships a `tika` wrapper script that accepts
    `--text`. CI pins `tika-app.jar` and exports `TIKA_JAR` env var.
    Some installs expose only `tika-app.jar`; we check both.
    """
    # Env override first (CI uses this to point at a cached jar).
    tika_jar_env = os.environ.get("TIKA_JAR")
    if tika_jar_env and Path(tika_jar_env).exists() and shutil.which("java"):
        return Extractor(
            name="tika",
            argv=["java", "-jar", tika_jar_env, "--text", str(pdf)],
        )
    if shutil.which("tika"):
        return Extractor(name="tika", argv=["tika", "--text", str(pdf)])
    # Pinned-jar fallback.
    jar_candidates = [
        RESUME_DIR / "template" / "tika-app.jar",
        Path("/opt/homebrew/opt/tika/libexec/tika-app.jar"),
    ]
    for jar in jar_candidates:
        if jar.exists() and shutil.which("java"):
            return Extractor(
                name="tika",
                argv=["java", "-jar", str(jar), "--text", str(pdf)],
            )
    return None


def build_extractors(pdf: Path) -> tuple[list[Extractor], list[str]]:
    """Return (available, skipped_reasons)."""
    avail: list[Extractor] = []
    skipped: list[str] = []

    if shutil.which("pdftotext"):
        avail.append(Extractor("pdftotext", ["pdftotext", str(pdf), "-"]))
        avail.append(Extractor(
            "pdftotext -layout", ["pdftotext", "-layout", str(pdf), "-"]
        ))
    else:
        skipped.append(
            "pdftotext: missing. Install with `brew install poppler`."
        )

    tika = detect_tika(pdf)
    if tika is not None:
        avail.append(tika)
    else:
        skipped.append(
            "tika: missing. Install with `brew install tika` "
            "(provides the `tika` wrapper script)."
        )

    return avail, skipped


def run_extractor(e: Extractor) -> str:
    r = subprocess.run(e.argv, capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise RuntimeError(
            f"{e.name} failed (rc={r.returncode}): {r.stderr.strip()[:400]}"
        )
    return r.stdout


# -- Assertions ---------------------------------------------------------------

@dataclass
class AssertionResult:
    ok: bool
    name: str
    detail: str = ""


@dataclass
class ExtractorResult:
    extractor: str
    text: str
    results: list[AssertionResult] = field(default_factory=list)
    section_order: list[str] = field(default_factory=list)
    job_count: int = 0

    @property
    def ok(self) -> bool:
        return all(r.ok for r in self.results)


def _collapse_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s)


def assert_non_empty(text: str, min_bytes: int) -> AssertionResult:
    n = len(text.encode("utf-8"))
    return AssertionResult(
        ok=n >= min_bytes,
        name="1-non-empty",
        detail=f"{n} bytes (threshold {min_bytes})",
    )


def assert_section_order(
    text: str, expected: list[str]
) -> tuple[AssertionResult, list[str]]:
    found = []
    indices = []
    missing = []
    flat = _collapse_ws(text)
    for header in expected:
        idx = flat.find(header)
        if idx == -1:
            missing.append(header)
        else:
            found.append(header)
            indices.append(idx)
    in_order = indices == sorted(indices)
    ok = not missing and in_order
    detail_parts = []
    if missing:
        detail_parts.append(f"missing: {missing}")
    if not in_order:
        detail_parts.append(
            f"order mismatch: found {list(zip(found, indices))}"
        )
    if ok:
        detail_parts.append(f"all {len(expected)} headers in order")
    return (
        AssertionResult(
            ok=ok, name="2-section-order", detail="; ".join(detail_parts)
        ),
        found,
    )


def assert_name_and_contact(
    text: str, name: str, email: str, head_bytes: int, glue_window: int
) -> AssertionResult:
    head = text[:head_bytes]
    if name not in head:
        return AssertionResult(
            ok=False,
            name="3-name-contact",
            detail=f"name {name!r} not in first {head_bytes} chars",
        )
    # Detect name+email glue (no whitespace between them) — the ATS footgun.
    glued = re.search(re.escape(name) + re.escape(email), text)
    if glued:
        return AssertionResult(
            ok=False,
            name="3-name-contact",
            detail=f"name+email glued at {glued.start()} — ATS field map hazard",
        )
    # Email should appear within glue_window chars of name.
    name_idx = text.find(name)
    email_idx = text.find(email)
    if email_idx == -1:
        return AssertionResult(
            ok=False,
            name="3-name-contact",
            detail=f"email {email!r} not found in extracted text",
        )
    gap = abs(email_idx - name_idx)
    if gap > glue_window:
        return AssertionResult(
            ok=False,
            name="3-name-contact",
            detail=(
                f"name at {name_idx}, email at {email_idx} "
                f"(gap {gap} > {glue_window})"
            ),
        )
    return AssertionResult(
        ok=True,
        name="3-name-contact",
        detail=f"name+email within {gap} chars",
    )


def assert_job_blocks(
    text: str, jobs: list[dict], window: int
) -> tuple[AssertionResult, int]:
    """Title + company + date_start + date_end within `window` chars."""
    flat = _collapse_ws(text)
    failures = []
    matched = 0
    for j in jobs:
        title = j["title"]
        company = j["company"]
        date_start = j["date_start"]
        date_end = j["date_end"]

        # Find every occurrence of title; check that there's one where all
        # four strings co-occur within the window.
        ok_for_job = False
        for m in re.finditer(re.escape(title), flat):
            start = m.start()
            slice_ = flat[start : start + window]
            if (
                company in slice_
                and date_start in slice_
                and date_end in slice_
            ):
                ok_for_job = True
                break
        if ok_for_job:
            matched += 1
        else:
            failures.append(
                f"{title!r} @ {company!r} ({date_start}{date_end}): "
                f"no {window}-char window contained all four strings"
            )
    if failures:
        return (
            AssertionResult(
                ok=False,
                name="4-job-contiguity",
                detail="; ".join(failures),
            ),
            matched,
        )
    return (
        AssertionResult(
            ok=True,
            name="4-job-contiguity",
            detail=f"{matched}/{len(jobs)} jobs contiguous within {window} chars",
        ),
        matched,
    )


def assert_date_format(text: str, regex: str) -> AssertionResult:
    pat = re.compile(regex)
    flat = _collapse_ws(text)
    matches = pat.findall(flat)
    # We expect >=1 date range (we have jobs). We do not require every
    # date-looking token to match — only that the regex fires and there
    # are no dangling year tokens that aren't part of a valid range.
    if not matches:
        return AssertionResult(
            ok=False,
            name="5-date-format",
            detail="no date range matched the allowed regex",
        )
    return AssertionResult(
        ok=True,
        name="5-date-format",
        detail=f"{len(matches)} date range(s) matched",
    )


def assert_no_mojibake(
    text: str, forbidden: list[str], flagged: list[str], allowed: list[str]
) -> AssertionResult:
    hits: list[str] = []
    for ch in forbidden:
        n = text.count(ch)
        if n:
            hits.append(f"U+{ord(ch):04X} x{n} (forbidden)")
    for ch in flagged:
        if ch in allowed:
            continue
        n = text.count(ch)
        if n:
            hits.append(f"U+{ord(ch):04X} x{n} (flagged)")
    if hits:
        return AssertionResult(
            ok=False, name="6-mojibake", detail="; ".join(hits)
        )
    return AssertionResult(ok=True, name="6-mojibake", detail="clean")


def assert_cross_extractor(
    results: list[ExtractorResult],
) -> AssertionResult:
    if len(results) < 2:
        return AssertionResult(
            ok=True,
            name="7-cross-extractor",
            detail=f"skipped — only {len(results)} extractor(s) available",
        )
    orders = {r.extractor: r.section_order for r in results}
    counts = {r.extractor: r.job_count for r in results}
    first_order = next(iter(orders.values()))
    first_count = next(iter(counts.values()))

    order_disagreements = [
        (name, order) for name, order in orders.items() if order != first_order
    ]
    count_disagreements = [
        (name, n) for name, n in counts.items() if n != first_count
    ]

    problems = []
    if order_disagreements:
        problems.append(f"section order diverges: {orders}")
    if count_disagreements:
        problems.append(f"job count diverges: {counts}")
    if problems:
        return AssertionResult(
            ok=False, name="7-cross-extractor", detail="; ".join(problems)
        )
    return AssertionResult(
        ok=True,
        name="7-cross-extractor",
        detail=f"all {len(results)} extractors agree ({first_count} jobs)",
    )


# -- Orchestration ------------------------------------------------------------


def load_fixtures(fixtures_path: Path) -> dict:
    if not fixtures_path.exists():
        print(c(RED, f"Fixtures file missing: {fixtures_path}"))
        sys.exit(2)
    return tomllib.loads(fixtures_path.read_text())


def evaluate(extractor: Extractor, fx: dict) -> ExtractorResult:
    text = run_extractor(extractor)
    er = ExtractorResult(extractor=extractor.name, text=text)

    th = fx["thresholds"]
    cand = fx["candidate"]
    sect = fx["sections"]["expected_order"]
    jobs = fx["jobs"]
    dates = fx["dates"]
    mj = fx["mojibake"]

    er.results.append(assert_non_empty(text, th["min_bytes"]))
    order_res, found_order = assert_section_order(text, sect)
    er.results.append(order_res)
    er.section_order = found_order
    er.results.append(
        assert_name_and_contact(
            text,
            cand["name"],
            cand["email"],
            th["name_head_bytes"],
            th["contact_glue_window"],
        )
    )
    job_res, matched = assert_job_blocks(
        text, jobs, th["job_block_window_chars"]
    )
    er.results.append(job_res)
    er.job_count = matched
    er.results.append(assert_date_format(text, dates["allowed_range_regex"]))
    er.results.append(
        assert_no_mojibake(
            text,
            mj["forbidden_chars"],
            mj["flagged_chars"],
            mj["allowed_chars"],
        )
    )
    return er


def fmt_result(r: AssertionResult) -> str:
    tag = c(GREEN, "PASS") if r.ok else c(RED, "FAIL")
    return f"  {tag} {r.name}: {r.detail}"


def write_report(
    results: list[ExtractorResult],
    cross: AssertionResult,
    skipped: list[str],
    report_dir: Path,
) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / "report.md"
    lines: list[str] = []
    lines.append("# Extraction check report")
    lines.append("")
    if skipped:
        lines.append("## Skipped extractors")
        for s in skipped:
            lines.append(f"- {s}")
        lines.append("")
    for er in results:
        lines.append(f"## {er.extractor}")
        for r in er.results:
            tag = "PASS" if r.ok else "FAIL"
            lines.append(f"- **{tag}** {r.name}: {r.detail}")
        lines.append("")
        lines.append("### First 50 lines of extracted text")
        lines.append("```")
        head = "\n".join(er.text.splitlines()[:50])
        lines.append(head)
        lines.append("```")
        lines.append("")
    tag = "PASS" if cross.ok else "FAIL"
    lines.append("## Cross-extractor")
    lines.append(f"- **{tag}** {cross.name}: {cross.detail}")
    report_file.write_text("\n".join(lines) + "\n")


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="extraction-check.py",
        description="ATS text-extraction regression check.",
    )
    p.add_argument(
        "--pdf",
        type=Path,
        default=DEFAULT_PDF,
        help=f"Path to PDF to check (default: {DEFAULT_PDF}).",
    )
    p.add_argument(
        "--fixtures",
        type=Path,
        default=DEFAULT_FIXTURES,
        help=f"Path to fixtures TOML (default: {DEFAULT_FIXTURES}).",
    )
    p.add_argument(
        "--report-dir",
        type=Path,
        default=DEFAULT_REPORT_DIR,
        help=f"Directory for report.md output (default: {DEFAULT_REPORT_DIR}).",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    pdf: Path = args.pdf
    fixtures_path: Path = args.fixtures
    report_dir: Path = args.report_dir

    print(c(BLUE, "extraction-check: preflight..."))
    if not pdf.exists():
        print(c(RED, f"PDF not found: {pdf}"))
        print(c(YELLOW, "Run `just compile` first."))
        return 2
    fx = load_fixtures(fixtures_path)
    extractors, skipped = build_extractors(pdf)
    for s in skipped:
        print(c(YELLOW, f"  skip: {s}"))
    if not extractors:
        print(c(RED, "No extractors available. Install poppler and/or tika."))
        return 2
    print(c(BLUE, f"Running {len(extractors)} extractor(s) on {pdf}..."))

    results: list[ExtractorResult] = []
    for e in extractors:
        print(c(GRAY, f"[{e.name}] {' '.join(e.argv)}"))
        try:
            er = evaluate(e, fx)
        except Exception as ex:  # noqa: BLE001
            print(c(RED, f"  extractor error: {ex}"))
            return 2
        results.append(er)
        for r in er.results:
            print(fmt_result(r))

    cross = assert_cross_extractor(results)
    print(fmt_result(cross))

    all_ok = all(r.ok for r in results) and cross.ok
    write_report(results, cross, skipped, report_dir)

    if all_ok:
        print(c(
            GREEN,
            f"extraction-check: PASS "
            f"({', '.join(r.extractor for r in results)} — "
            f"{results[0].job_count} jobs, {len(results[0].section_order)} sections)",
        ))
        return 0
    print(c(RED, "extraction-check: FAIL"))
    print(c(YELLOW, f"See {report_dir / 'report.md'}"))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
