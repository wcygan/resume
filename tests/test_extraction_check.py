"""Negative-fixture regression suite for scripts/extraction-check.py.

For each broken tests/fixtures/broken/<name>.typ:
  1. Compile to PDF.
  2. Run extraction-check.py against it with the shared
     tests/fixtures/baseline.fixtures.toml.
  3. Assert exit code != 0.
  4. Assert the specific FAIL assertion-name substring is present in
     stdout, so a regression where a *different* assertion trips is
     caught.

Tests requiring Tika are marked with the `tika` marker and auto-skip
when Tika is missing.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

_ANSI = re.compile(r"\x1b\[[0-9;]*m")


def _stdout(r) -> str:
    return _ANSI.sub("", r.stdout + r.stderr)


# -- Sanity: the clean baseline must pass --------------------------------------


def test_baseline_passes(
    broken_pdf, run_check, require_pdftotext, require_tika
):
    """Sanity check: the clean skeleton passes every assertion.

    If this ever starts failing, the broken fixtures are all suspect —
    their defects may be collateral from an upstream baseline bug.
    """
    pdf = broken_pdf("baseline")
    r = run_check(pdf)
    assert r.returncode == 0, (
        f"baseline should pass; got rc={r.returncode}\n{_stdout(r)}"
    )
    assert "extraction-check: PASS" in _stdout(r)


# -- Per-defect tests ----------------------------------------------------------


def test_nonstandard_headers_fails_assertion_2(
    broken_pdf, run_check, require_pdftotext, require_tika
):
    """Renaming 'Work Experience' to 'My Journey' must trip section-order."""
    r = run_check(broken_pdf("nonstandard-headers"))
    out = _stdout(r)
    assert r.returncode != 0, (
        f"expected non-zero exit; got rc={r.returncode}\n{out}"
    )
    assert "FAIL 2-section-order" in out, (
        "expected assertion 2 to fail with 'missing: Work Experience'"
    )
    # Cleanliness: no other assertion should trip.
    for other in (
        "1-non-empty",
        "3-name-contact",
        "4-job-contiguity",
        "5-date-format",
        "6-mojibake",
    ):
        assert f"FAIL {other}" not in out, (
            f"unexpected collateral failure on {other}:\n{out}"
        )


def test_glued_contact_fails_assertion_3(
    broken_pdf, run_check, require_pdftotext, require_tika
):
    """Name + email with no whitespace must trip the contact-glue check."""
    r = run_check(broken_pdf("glued-contact"))
    out = _stdout(r)
    assert r.returncode != 0
    assert "FAIL 3-name-contact" in out
    assert "glued" in out, "expected 'glued' marker in failure detail"
    for other in ("1-non-empty", "2-section-order", "4-job-contiguity",
                  "5-date-format", "6-mojibake"):
        assert f"FAIL {other}" not in out, (
            f"unexpected collateral on {other}:\n{out}"
        )


def test_smart_quotes_fails_assertion_6(
    broken_pdf, run_check, require_pdftotext, require_tika
):
    """U+2018/2019 in body must trip mojibake."""
    r = run_check(broken_pdf("smart-quotes"))
    out = _stdout(r)
    assert r.returncode != 0
    assert "FAIL 6-mojibake" in out
    assert "U+2018" in out or "U+2019" in out
    for other in ("1-non-empty", "2-section-order", "3-name-contact",
                  "4-job-contiguity", "5-date-format"):
        assert f"FAIL {other}" not in out, (
            f"unexpected collateral on {other}:\n{out}"
        )


def test_mixed_dates_fails_assertion_5(
    broken_pdf, run_check, require_pdftotext, require_tika
):
    """Numeric-only date format must trip the date-format regex.

    Collateral on assertion 4 is expected: changing dates from
    'Jun 2019' to '06/2019' means baseline.fixtures.toml's date_start
    tokens no longer appear in the extracted text, so job contiguity
    also fails. We document the collateral and assert on assertion 5
    specifically (which is the primary signal this fixture exercises).
    """
    r = run_check(broken_pdf("mixed-dates"))
    out = _stdout(r)
    assert r.returncode != 0
    assert "FAIL 5-date-format" in out
    # Not asserting absence of 4-job-contiguity — it's expected collateral.
    # Do assert the other four stay clean.
    for other in ("1-non-empty", "2-section-order", "3-name-contact",
                  "6-mojibake"):
        assert f"FAIL {other}" not in out, (
            f"unexpected collateral on {other}:\n{out}"
        )


def test_two_column_fails_cross_extractor(
    broken_pdf, run_check, require_pdftotext, require_tika
):
    """Two-column layout must scramble reading order enough that either
    per-extractor assertion 4 fails OR cross-extractor assertion 7
    diverges. With all three extractors present, the cleanest signal is
    assertion 7 (job-count disagreement between pdftotext, -layout, tika)."""
    r = run_check(broken_pdf("two-column"))
    out = _stdout(r)
    assert r.returncode != 0, (
        f"expected non-zero exit for two-column:\n{out}"
    )
    # Either 4 trips on at least one extractor OR 7 trips. Both are
    # legitimate signals of reading-order scramble.
    assert ("FAIL 4-job-contiguity" in out) or (
        "FAIL 7-cross-extractor" in out
    ), (
        "expected two-column to trip either assertion 4 or 7:\n"
        f"{out}"
    )
