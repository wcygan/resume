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


def test_missing_required_header_fact_fails_name_contact() -> None:
    result = ec.assert_name_and_contact(
        text="Will Cygan\nwcygan.io@gmail.com\nChicago, IL\n\nEXPERIENCE",
        name="Will Cygan",
        email="wcygan.io@gmail.com",
        head_bytes=200,
        glue_window=100,
        required_head_facts=[
            "U.S. citizen · Authorized to work in the U.S. · No sponsorship required"
        ],
    )

    assert not result.ok
    assert "required header fact" in result.detail


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


def test_soft_hyphen_fails_soft_hyphen_or_keyword_roundtrip(
    broken_pdf: Callable[[str], Path],
    run_check: Callable[[Path], ec.EvaluationResult],
    require_pdftotext: None,
    require_tika: None,
) -> None:
    # The soft-hyphen fixture wraps the word `involuntary` across a line via a
    # narrow block, which is the ATS-visible failure mode. U+00AD detection is
    # platform-dependent — macOS poppler surfaces the codepoint in extracted
    # text; Linux poppler strips it — so we accept either SOFT_HYPHEN (when the
    # extractor preserves the codepoint) or KEYWORD_ROUNDTRIP (the wrap breaks
    # `involuntary` into `involun\ntary`, which no longer contains the
    # substring) as a valid signal. Both catch the same hazard.
    ev = run_check(broken_pdf("soft-hyphen"))
    assert (
        ev.any_fails(ec.Assertion.SOFT_HYPHEN)
        or ev.any_fails(ec.Assertion.KEYWORD_ROUNDTRIP)
    ), "expected either 8-soft-hyphen or 9-keyword-roundtrip to fail"


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


def test_mojibake_flags_pua_glyphs() -> None:
    # Pure unit test — PUA codepoints (where Font Awesome lives) are painful to
    # force through a real Typst compile without the font installed, so we test
    # assert_no_mojibake directly. An fa-icon("github") call on a host with a
    # broken FA font would extract as a U+F09B codepoint.
    text = "Contact: \uF09B github.com/wcygan"
    r = ec.assert_no_mojibake(
        text=text,
        forbidden=["\uFFFD"],
        flagged=["\u2018", "\u2019"],
        allowed=["\u2013"],
    )
    assert not r.ok, "expected PUA codepoint to trip mojibake assertion"
    assert "PUA" in r.detail, r.detail
    assert "U+F09B" in r.detail, r.detail


def test_mojibake_clean_with_no_pua() -> None:
    # Ensure PUA extension doesn't false-positive on ordinary ASCII text.
    r = ec.assert_no_mojibake(
        text="Will Cygan – Senior Software Engineer",
        forbidden=["\uFFFD"],
        flagged=["\u2018", "\u2019", "\u201C", "\u201D", "\u2014"],
        allowed=["\u2013"],
    )
    assert r.ok, r.detail


def test_glued_sections_fails_section_boundary(
    broken_pdf: Callable[[str], Path],
    run_check: Callable[[Path], ec.EvaluationResult],
    require_pdftotext: None,
    require_tika: None,
) -> None:
    ev = run_check(broken_pdf("glued-sections"))
    assert ev.any_fails(ec.Assertion.SECTION_BOUNDARY), (
        "expected 11-section-boundary to fail"
    )


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
