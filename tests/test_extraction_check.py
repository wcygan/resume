"""Negative-fixture regression suite for scripts/extraction_check.py.

Each test compiles a deliberately-broken Typst source, runs evaluate_pdf in
process, and asserts the right assertion fires without unexpected collateral.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import extraction_check as ec  # noqa: E402

_ALL_ASSERTIONS = tuple(ec.Assertion)


def assert_only_fails(
    ev: ec.EvaluationResult,
    expected: ec.Assertion,
    allow_collateral: frozenset[ec.Assertion] = frozenset(),
) -> None:
    assert ev.any_fails(expected), f"expected {expected.value} to fail"
    for other in _ALL_ASSERTIONS:
        if other == expected or other in allow_collateral:
            continue
        assert not ev.any_fails(other), (
            f"unexpected collateral on {other.value}"
        )


def test_baseline_passes(
    broken_pdf: Callable[[str], Path],
    run_check: Callable[[Path], ec.EvaluationResult],
    require_pdftotext: None,
    require_tika: None,
) -> None:
    ev = run_check(broken_pdf("baseline"))
    assert ev.ok, [
        (er.extractor, r.name.value, r.detail)
        for er in ev.results
        for r in er.results
        if not r.ok
    ]


def test_nonstandard_headers_fails_section_order(
    broken_pdf: Callable[[str], Path],
    run_check: Callable[[Path], ec.EvaluationResult],
    require_pdftotext: None,
    require_tika: None,
) -> None:
    ev = run_check(broken_pdf("nonstandard-headers"))
    assert_only_fails(ev, ec.Assertion.SECTION_ORDER)


def test_glued_contact_fails_name_contact(
    broken_pdf: Callable[[str], Path],
    run_check: Callable[[Path], ec.EvaluationResult],
    require_pdftotext: None,
    require_tika: None,
) -> None:
    ev = run_check(broken_pdf("glued-contact"))
    assert_only_fails(ev, ec.Assertion.NAME_CONTACT)
    details = [
        r.detail for er in ev.results for r in er.results
        if r.name == ec.Assertion.NAME_CONTACT and not r.ok
    ]
    assert any("glued" in d for d in details), details


def test_smart_quotes_fails_mojibake(
    broken_pdf: Callable[[str], Path],
    run_check: Callable[[Path], ec.EvaluationResult],
    require_pdftotext: None,
    require_tika: None,
) -> None:
    ev = run_check(broken_pdf("smart-quotes"))
    assert_only_fails(ev, ec.Assertion.MOJIBAKE)
    details = [
        r.detail for er in ev.results for r in er.results
        if r.name == ec.Assertion.MOJIBAKE and not r.ok
    ]
    assert any("U+2018" in d or "U+2019" in d for d in details), details


def test_mixed_dates_fails_date_format(
    broken_pdf: Callable[[str], Path],
    run_check: Callable[[Path], ec.EvaluationResult],
    require_pdftotext: None,
    require_tika: None,
) -> None:
    # Numeric-only dates necessarily also break assertion 4 (baseline fixture's
    # date_start tokens no longer appear). Primary signal is the date-format
    # regex mismatch; job-contiguity collateral is documented and allowed.
    ev = run_check(broken_pdf("mixed-dates"))
    assert_only_fails(
        ev,
        ec.Assertion.DATE_FORMAT,
        allow_collateral=frozenset({ec.Assertion.JOB_CONTIGUITY}),
    )


def test_soft_hyphen_fails_soft_hyphen(
    broken_pdf: Callable[[str], Path],
    run_check: Callable[[Path], ec.EvaluationResult],
    require_pdftotext: None,
    require_tika: None,
) -> None:
    ev = run_check(broken_pdf("soft-hyphen"))
    assert ev.any_fails(ec.Assertion.SOFT_HYPHEN), (
        "expected 8-soft-hyphen to fail"
    )
    details = [
        r.detail for er in ev.results for r in er.results
        if r.name == ec.Assertion.SOFT_HYPHEN and not r.ok
    ]
    assert any("U+00AD" in d for d in details), details


def test_duplicated_url_fails_url_dedup(
    broken_pdf: Callable[[str], Path],
    run_check: Callable[[Path], ec.EvaluationResult],
    require_pdftotext: None,
    require_tika: None,
) -> None:
    # Only Tika emits the URL block where repeated link targets collapse to a
    # single duplicated line. pdftotext extractors render each visible label
    # at its in-flow position and don't re-echo the URL, so they pass. Accept
    # as long as at least one extractor's 10-url-dedup fires.
    ev = run_check(broken_pdf("duplicated-url"))
    assert ev.any_fails(ec.Assertion.URL_DEDUP), (
        "expected 10-url-dedup to fail on at least one extractor"
    )


def test_missing_keyword_fails_keyword_roundtrip(
    broken_pdf: Callable[[str], Path],
    run_check: Callable[[Path], ec.EvaluationResult],
    require_pdftotext: None,
    require_tika: None,
) -> None:
    ev = run_check(broken_pdf("missing-keyword"))
    assert_only_fails(ev, ec.Assertion.KEYWORD_ROUNDTRIP)
    details = [
        r.detail for er in ev.results for r in er.results
        if r.name == ec.Assertion.KEYWORD_ROUNDTRIP and not r.ok
    ]
    assert any("Rust" in d for d in details), details


def test_two_column_scrambles_reading_order(
    broken_pdf: Callable[[str], Path],
    run_check: Callable[[Path], ec.EvaluationResult],
    require_pdftotext: None,
    require_tika: None,
) -> None:
    # Two-column layouts scramble reading order. On small docs this commonly
    # surfaces as cross-extractor disagreement (assertion 7) rather than
    # per-extractor job-contiguity — accept either as a legitimate signal.
    ev = run_check(broken_pdf("two-column"))
    assert not ev.ok
    assert (
        ev.any_fails(ec.Assertion.JOB_CONTIGUITY)
        or ev.any_fails(ec.Assertion.CROSS_EXTRACTOR)
    )
