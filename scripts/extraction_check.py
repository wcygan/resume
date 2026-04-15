#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""ATS text-extraction regression check.

Shells out to `pdftotext`, `pdftotext -layout`, and Apache Tika and runs the
seven assertions defined in .claude/context/text-extraction-hypothesis.md
against the extracted text.

Exit codes:
  0 - all assertions passed for every available extractor
  1 - one or more assertions failed
  2 - preflight failure (missing binary, missing fixtures, missing PDF)

On failure, a per-extractor breakdown is written to `.extraction/report.md`
(gitignored).
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tomllib
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path

RESUME_DIR = Path(__file__).resolve().parent.parent
DEFAULT_PDF = RESUME_DIR / "will_cygan_resume.pdf"
DEFAULT_FIXTURES = Path(__file__).resolve().parent / "extraction-check.fixtures.toml"
DEFAULT_REPORT_DIR = RESUME_DIR / ".extraction"

BLUE = "\033[34m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
GRAY = "\033[90m"
RESET = "\033[0m"


def c(color: str, msg: str) -> str:
    return f"{color}{msg}{RESET}"


class Assertion(StrEnum):
    NON_EMPTY = "1-non-empty"
    SECTION_ORDER = "2-section-order"
    NAME_CONTACT = "3-name-contact"
    JOB_CONTIGUITY = "4-job-contiguity"
    DATE_FORMAT = "5-date-format"
    MOJIBAKE = "6-mojibake"
    CROSS_EXTRACTOR = "7-cross-extractor"
    SOFT_HYPHEN = "8-soft-hyphen"
    KEYWORD_ROUNDTRIP = "9-keyword-roundtrip"
    URL_DEDUP = "10-url-dedup"
    SECTION_BOUNDARY = "11-section-boundary"


# -- Extractors ---------------------------------------------------------------

@dataclass
class Extractor:
    name: str
    argv: list[str]


def detect_tika(pdf: Path) -> Extractor | None:
    tika_jar_env = os.environ.get("TIKA_JAR")
    if tika_jar_env and Path(tika_jar_env).exists() and shutil.which("java"):
        return Extractor("tika", ["java", "-jar", tika_jar_env, "--text", str(pdf)])
    if shutil.which("tika"):
        return Extractor("tika", ["tika", "--text", str(pdf)])
    jar_candidates = [
        RESUME_DIR / "template" / "tika-app.jar",
        Path("/opt/homebrew/opt/tika/libexec/tika-app.jar"),
    ]
    for jar in jar_candidates:
        if jar.exists() and shutil.which("java"):
            return Extractor("tika", ["java", "-jar", str(jar), "--text", str(pdf)])
    return None


def build_extractors(pdf: Path) -> tuple[list[Extractor], list[str]]:
    avail: list[Extractor] = []
    skipped: list[str] = []

    if shutil.which("pdftotext"):
        avail.append(Extractor("pdftotext", ["pdftotext", str(pdf), "-"]))
        avail.append(Extractor(
            "pdftotext -layout", ["pdftotext", "-layout", str(pdf), "-"]
        ))
    else:
        skipped.append("pdftotext: missing. Install with `brew install poppler`.")

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
    name: Assertion
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


@dataclass
class EvaluationResult:
    results: list[ExtractorResult]
    cross: AssertionResult
    skipped: list[str]

    @property
    def ok(self) -> bool:
        return all(r.ok for r in self.results) and self.cross.ok

    def any_fails(self, assertion: Assertion) -> bool:
        if assertion == Assertion.CROSS_EXTRACTOR:
            return not self.cross.ok
        return any(
            not r.ok
            for er in self.results
            for r in er.results
            if r.name == assertion
        )


def _collapse_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s)


def assert_non_empty(text: str, min_bytes: int) -> AssertionResult:
    n = len(text.encode("utf-8"))
    return AssertionResult(
        ok=n >= min_bytes,
        name=Assertion.NON_EMPTY,
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
        detail_parts.append(f"order mismatch: found {list(zip(found, indices))}")
    if ok:
        detail_parts.append(f"all {len(expected)} headers in order")
    return (
        AssertionResult(
            ok=ok, name=Assertion.SECTION_ORDER, detail="; ".join(detail_parts)
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
            name=Assertion.NAME_CONTACT,
            detail=f"name {name!r} not in first {head_bytes} chars",
        )
    # Name+email with no whitespace triggers ATS field-mapping glue bugs.
    glued = re.search(re.escape(name) + re.escape(email), text)
    if glued:
        return AssertionResult(
            ok=False,
            name=Assertion.NAME_CONTACT,
            detail=f"name+email glued at {glued.start()} — ATS field map hazard",
        )
    name_idx = text.find(name)
    email_idx = text.find(email)
    if email_idx == -1:
        return AssertionResult(
            ok=False,
            name=Assertion.NAME_CONTACT,
            detail=f"email {email!r} not found in extracted text",
        )
    gap = abs(email_idx - name_idx)
    if gap > glue_window:
        return AssertionResult(
            ok=False,
            name=Assertion.NAME_CONTACT,
            detail=f"name at {name_idx}, email at {email_idx} (gap {gap} > {glue_window})",
        )
    return AssertionResult(
        ok=True,
        name=Assertion.NAME_CONTACT,
        detail=f"name+email within {gap} chars",
    )


def assert_job_blocks(
    text: str, jobs: list[dict], window: int
) -> tuple[AssertionResult, int]:
    flat = _collapse_ws(text)
    failures = []
    matched = 0
    for j in jobs:
        title = j["title"]
        company = j["company"]
        date_start = j["date_start"]
        date_end = j["date_end"]
        ok_for_job = False
        for m in re.finditer(re.escape(title), flat):
            slice_ = flat[m.start() : m.start() + window]
            if company in slice_ and date_start in slice_ and date_end in slice_:
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
                ok=False, name=Assertion.JOB_CONTIGUITY, detail="; ".join(failures)
            ),
            matched,
        )
    return (
        AssertionResult(
            ok=True,
            name=Assertion.JOB_CONTIGUITY,
            detail=f"{matched}/{len(jobs)} jobs contiguous within {window} chars",
        ),
        matched,
    )


def assert_date_format(text: str, regex: str) -> AssertionResult:
    matches = re.compile(regex).findall(_collapse_ws(text))
    if not matches:
        return AssertionResult(
            ok=False,
            name=Assertion.DATE_FORMAT,
            detail="no date range matched the allowed regex",
        )
    return AssertionResult(
        ok=True,
        name=Assertion.DATE_FORMAT,
        detail=f"{len(matches)} date range(s) matched",
    )


_PUA_RE = re.compile(r"[\uE000-\uF8FF]")


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
    # Private Use Area (U+E000–U+F8FF) is where Font Awesome and other icon
    # fonts live. A PUA codepoint surviving extraction means either an icon
    # font was substituted mid-render or a stray fa-icon call leaked through
    # — either way an ATS sees garbage tofu where real text should be.
    pua_chars = _PUA_RE.findall(text)
    if pua_chars:
        unique = {ord(c) for c in pua_chars}
        sample = ", ".join(f"U+{cp:04X}" for cp in sorted(unique)[:3])
        hits.append(
            f"{len(pua_chars)} PUA codepoint(s) ({sample}"
            f"{'…' if len(unique) > 3 else ''}) — likely icon-font tofu"
        )
    if hits:
        return AssertionResult(ok=False, name=Assertion.MOJIBAKE, detail="; ".join(hits))
    return AssertionResult(ok=True, name=Assertion.MOJIBAKE, detail="clean")


def assert_section_boundary(
    text: str, section_headers: list[str]
) -> AssertionResult:
    # Between every pair of adjacent top-level section headers, there must be
    # at least one blank line. Section-boundary parsers (common in resume ATS
    # pipelines) rely on paragraph breaks to split sections; without them,
    # the tail of one section merges into the header of the next.
    lines = text.split("\n")
    header_lines: list[tuple[str, int]] = []
    for header in section_headers:
        for i, line in enumerate(lines):
            if header in line:
                header_lines.append((header, i))
                break
    if len(header_lines) < 2:
        return AssertionResult(
            ok=True,
            name=Assertion.SECTION_BOUNDARY,
            detail=f"only {len(header_lines)} section header(s) located; nothing to check",
        )
    failures: list[str] = []
    for (prev, prev_i), (nxt, nxt_i) in zip(header_lines, header_lines[1:]):
        has_blank = any(lines[j].strip() == "" for j in range(prev_i + 1, nxt_i))
        if not has_blank:
            failures.append(f"{prev!r} -> {nxt!r}: no blank line between")
    if failures:
        return AssertionResult(
            ok=False,
            name=Assertion.SECTION_BOUNDARY,
            detail="; ".join(failures),
        )
    return AssertionResult(
        ok=True,
        name=Assertion.SECTION_BOUNDARY,
        detail=f"{len(header_lines) - 1} adjacent section pair(s) separated by blank line",
    )


def assert_keyword_roundtrip(text: str, required: list[str]) -> AssertionResult:
    # Guards against ligature collapse (e.g. "Flink" becoming "Fl nk") and
    # font-substitution regressions that silently drop technical terms. The
    # token must survive extraction as a plain substring — case-sensitive and
    # not split by whitespace — because that's what an ATS keyword search sees.
    if not required:
        return AssertionResult(
            ok=True,
            name=Assertion.KEYWORD_ROUNDTRIP,
            detail="no required keywords declared",
        )
    missing = [kw for kw in required if kw not in text]
    if missing:
        return AssertionResult(
            ok=False,
            name=Assertion.KEYWORD_ROUNDTRIP,
            detail=f"missing keyword(s): {missing}",
        )
    return AssertionResult(
        ok=True,
        name=Assertion.KEYWORD_ROUNDTRIP,
        detail=f"all {len(required)} required keyword(s) present",
    )


def assert_no_soft_hyphen(text: str) -> AssertionResult:
    # U+00AD (soft hyphen) leaks into extractor output when Typst auto-hyphenates
    # across line breaks. Tika then splits the word across a paragraph boundary,
    # turning e.g. "involuntary" into "invol\n\nuntary" — a real ATS failure.
    n = text.count("\u00AD")
    if n:
        return AssertionResult(
            ok=False,
            name=Assertion.SOFT_HYPHEN,
            detail=f"U+00AD x{n} — set `#set text(hyphenate: false)` in source",
        )
    return AssertionResult(ok=True, name=Assertion.SOFT_HYPHEN, detail="clean")


# Matches http/https URLs. Trailing punctuation is trimmed so ".", ")", "," at
# sentence boundaries don't produce spurious distinct URLs.
_URL_RE = re.compile(r"https?://[^\s<>\"'()]+")


def assert_url_dedup(text: str) -> AssertionResult:
    seen: dict[str, int] = {}
    for m in _URL_RE.finditer(text):
        url = m.group(0).rstrip(".,;:)]>")
        seen[url] = seen.get(url, 0) + 1
    dupes = {u: n for u, n in seen.items() if n > 1}
    if dupes:
        listing = ", ".join(f"{u} x{n}" for u, n in sorted(dupes.items()))
        return AssertionResult(
            ok=False,
            name=Assertion.URL_DEDUP,
            detail=f"duplicate URL(s): {listing}",
        )
    return AssertionResult(
        ok=True,
        name=Assertion.URL_DEDUP,
        detail=f"{len(seen)} unique URL(s), all appearing once",
    )


def assert_cross_extractor(
    results: list[ExtractorResult], max_byte_ratio: float = 1.5
) -> AssertionResult:
    if len(results) < 2:
        return AssertionResult(
            ok=True,
            name=Assertion.CROSS_EXTRACTOR,
            detail=f"skipped — only {len(results)} extractor(s) available",
        )
    orders = {r.extractor: r.section_order for r in results}
    counts = {r.extractor: r.job_count for r in results}
    sizes = {r.extractor: len(r.text.encode("utf-8")) for r in results}
    first_order = next(iter(orders.values()))
    first_count = next(iter(counts.values()))

    problems = []
    if any(o != first_order for o in orders.values()):
        problems.append(f"section order diverges: {orders}")
    if any(n != first_count for n in counts.values()):
        problems.append(f"job count diverges: {counts}")
    # Byte-count ratio: one extractor producing >1.5x the bytes of another
    # signals a major extraction divergence (e.g. one extractor capturing
    # a trailing URL block, or one missing a whole section).
    min_size = min(sizes.values())
    max_size = max(sizes.values())
    if min_size > 0:
        ratio = max_size / min_size
        if ratio > max_byte_ratio:
            problems.append(
                f"byte-count ratio {ratio:.2f}x > {max_byte_ratio}x "
                f"(sizes: {sizes})"
            )
    if problems:
        return AssertionResult(
            ok=False, name=Assertion.CROSS_EXTRACTOR, detail="; ".join(problems)
        )
    return AssertionResult(
        ok=True,
        name=Assertion.CROSS_EXTRACTOR,
        detail=(
            f"all {len(results)} extractors agree ({first_count} jobs, "
            f"sizes within {max_size / max(min_size, 1):.2f}x)"
        ),
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
    job_res, matched = assert_job_blocks(text, jobs, th["job_block_window_chars"])
    er.results.append(job_res)
    er.job_count = matched
    er.results.append(assert_date_format(text, dates["allowed_range_regex"]))
    er.results.append(
        assert_no_mojibake(
            text, mj["forbidden_chars"], mj["flagged_chars"], mj["allowed_chars"]
        )
    )
    er.results.append(assert_no_soft_hyphen(text))
    er.results.append(
        assert_keyword_roundtrip(text, fx.get("keywords", {}).get("required", []))
    )
    er.results.append(assert_url_dedup(text))
    er.results.append(assert_section_boundary(text, sect))
    return er


def evaluate_pdf(pdf: Path, fx: dict) -> EvaluationResult:
    extractors, skipped = build_extractors(pdf)
    results: list[ExtractorResult] = []
    if extractors:
        with ThreadPoolExecutor(max_workers=len(extractors)) as pool:
            futures = [pool.submit(evaluate, e, fx) for e in extractors]
            results = [f.result() for f in futures]
    cross = assert_cross_extractor(results)
    return EvaluationResult(results=results, cross=cross, skipped=skipped)


def fmt_result(r: AssertionResult) -> str:
    tag = c(GREEN, "PASS") if r.ok else c(RED, "FAIL")
    return f"  {tag} {r.name.value}: {r.detail}"


_SLUG_RE = re.compile(r"[^a-z0-9]+")


def _slug(s: str) -> str:
    return _SLUG_RE.sub("-", s.lower()).strip("-")


def write_report(ev: EvaluationResult, report_dir: Path) -> list[Path]:
    report_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    lines: list[str] = ["# Extraction check report", ""]
    if ev.skipped:
        lines.append("## Skipped extractors")
        for s in ev.skipped:
            lines.append(f"- {s}")
        lines.append("")
    for er in ev.results:
        slug = _slug(er.extractor)
        raw_path = report_dir / f"{slug}.txt"
        raw_path.write_text(er.text)
        written.append(raw_path)

        lines.append(f"## {er.extractor}")
        lines.append(f"- raw text: `{raw_path.name}`")
        for r in er.results:
            tag = "PASS" if r.ok else "FAIL"
            lines.append(f"- **{tag}** {r.name.value}: {r.detail}")
        lines.append("")
    tag = "PASS" if ev.cross.ok else "FAIL"
    lines.append("## Cross-extractor")
    lines.append(f"- **{tag}** {ev.cross.name.value}: {ev.cross.detail}")
    report_path = report_dir / "report.md"
    report_path.write_text("\n".join(lines) + "\n")
    written.append(report_path)
    return written


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="extraction_check.py",
        description="ATS text-extraction regression check.",
    )
    p.add_argument("--pdf", type=Path, default=DEFAULT_PDF,
                   help=f"Path to PDF to check (default: {DEFAULT_PDF}).")
    p.add_argument("--fixtures", type=Path, default=DEFAULT_FIXTURES,
                   help=f"Path to fixtures TOML (default: {DEFAULT_FIXTURES}).")
    p.add_argument("--report-dir", type=Path, default=DEFAULT_REPORT_DIR,
                   help=f"Directory for report.md on failure (default: {DEFAULT_REPORT_DIR}).")
    p.add_argument("--report", action="store_true",
                   help="Always write report.md, even on PASS.")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    pdf: Path = args.pdf

    print(c(BLUE, "extraction-check: preflight..."))
    if not pdf.exists():
        print(c(RED, f"PDF not found: {pdf}"))
        print(c(YELLOW, "Run `just compile` first."))
        return 2
    fx = load_fixtures(args.fixtures)
    extractors, skipped = build_extractors(pdf)
    for s in skipped:
        print(c(YELLOW, f"  skip: {s}"))
    if not extractors:
        print(c(RED, "No extractors available. Install poppler and/or tika."))
        return 2

    print(c(BLUE, f"Running {len(extractors)} extractor(s) on {pdf}..."))
    for e in extractors:
        print(c(GRAY, f"[{e.name}] {' '.join(e.argv)}"))

    try:
        ev = evaluate_pdf(pdf, fx)
    except RuntimeError as ex:
        print(c(RED, f"  extractor error: {ex}"))
        return 2

    for er in ev.results:
        print(c(BLUE, f"-- {er.extractor} --"))
        for r in er.results:
            print(fmt_result(r))
    print(fmt_result(ev.cross))

    if ev.ok:
        if args.report:
            for p in write_report(ev, args.report_dir):
                print(c(GRAY, f"  wrote {p}"))
        print(c(
            GREEN,
            f"extraction-check: PASS "
            f"({', '.join(r.extractor for r in ev.results)} — "
            f"{ev.results[0].job_count} jobs, {len(ev.results[0].section_order)} sections)",
        ))
        return 0

    for p in write_report(ev, args.report_dir):
        print(c(YELLOW, f"  wrote {p}"))
    print(c(RED, "extraction-check: FAIL"))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
