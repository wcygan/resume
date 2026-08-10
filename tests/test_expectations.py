"""Focused tests for canonical active-resume extraction expectations."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from resume_tools import expectations


REPO_ROOT = Path(__file__).resolve().parent.parent
ACTIVE_DATA = REPO_ROOT / "will_cygan_resume-data.json"
ACTIVE_RULES = REPO_ROOT / "scripts" / "extraction-check.fixtures.toml"


def test_canonical_data_change_updates_expected_facts_without_toml_edit(
    tmp_path: Path,
) -> None:
    data = json.loads(ACTIVE_DATA.read_text(encoding="utf-8"))
    data["experience"][0]["role"] = "Principal Software Engineer"
    changed_data = tmp_path / "resume-data.json"
    changed_data.write_text(json.dumps(data), encoding="utf-8")

    actual = expectations.load_active_expectations(ACTIVE_RULES, changed_data)

    assert actual.facts.jobs[0].title == "Principal Software Engineer"
    assert "Principal Software Engineer" not in ACTIVE_RULES.read_text(encoding="utf-8")


def test_reviewed_rules_do_not_change_with_canonical_content(
    tmp_path: Path,
) -> None:
    before = expectations.load_parsability_rules(ACTIVE_RULES)
    data = json.loads(ACTIVE_DATA.read_text(encoding="utf-8"))
    data["contact"]["name"] = "Changed Candidate"
    data["skills"][0]["values"] = "Different Keyword"
    changed_data = tmp_path / "resume-data.json"
    changed_data.write_text(json.dumps(data), encoding="utf-8")

    after = expectations.load_active_expectations(ACTIVE_RULES, changed_data)

    assert after.rules == before
    assert after.rules.allowed_date_range_regex
    assert after.rules.job_block_window_chars == 300
    assert after.facts.candidate.name == "Changed Candidate"
    assert after.facts.keywords[0] == "Different Keyword"


def test_rules_reject_copied_candidate_content(tmp_path: Path) -> None:
    copied_content = tmp_path / "copied-content.toml"
    copied_content.write_text(
        ACTIVE_RULES.read_text(encoding="utf-8") + '\n[candidate]\nname = "Copied"\n',
        encoding="utf-8",
    )

    with pytest.raises(expectations.ExpectationError, match="must not copy canonical"):
        expectations.load_parsability_rules(copied_content)


def test_invalid_canonical_date_has_a_field_specific_failure(tmp_path: Path) -> None:
    data = json.loads(ACTIVE_DATA.read_text(encoding="utf-8"))
    data["experience"][0]["dates"] = "2024 to Present"
    changed_data = tmp_path / "resume-data.json"
    changed_data.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(expectations.ExpectationError, match=r"experience\[0\]\.dates"):
        expectations.load_canonical_facts(changed_data)
