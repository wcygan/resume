"""Unit contracts for the Golden Resume deep evaluator and stress matrix."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
from types import ModuleType

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_ROOT = REPO_ROOT / ".agents" / "skills" / "resume-parsability"
GOLDEN_FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "golden-resume"


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


evaluator = load_module(
    "golden_resume_evaluator",
    SKILL_ROOT / "scripts" / "evaluate_golden_resume.py",
)
matrix = load_module(
    "golden_resume_stress_matrix",
    SKILL_ROOT / "scripts" / "evaluate_golden_stress_matrix.py",
)


def test_tika_annotation_block_can_precede_later_page_text() -> None:
    uris = ["mailto:first@example.com", "https://example.com/profile"]
    text = (
        "First Last\n"
        "first@example.com\n"
        "mailto:first@example.com\n"
        "https://example.com/profile\n"
        "SKILLS\nPython\n"
    )

    visible, annotation_block, exact = evaluator.split_tika_visible_body(text, uris)

    assert exact
    assert annotation_block == uris
    assert "SKILLS\nPython" in visible
    assert "mailto:first@example.com" not in visible


def test_tika_duplicate_annotation_blocks_are_rejected() -> None:
    uris = ["https://example.com/profile"]
    text = "Body\nhttps://example.com/profile\nMore\nhttps://example.com/profile\n"

    visible, _, exact = evaluator.split_tika_visible_body(text, uris)

    assert not exact
    assert visible == text


def test_tika_command_uses_pinned_jar_when_executable_is_absent(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    tika_jar = tmp_path / "tika-app.jar"
    tika_jar.write_bytes(b"reviewed test placeholder")
    monkeypatch.setenv("TIKA_JAR", str(tika_jar))
    monkeypatch.setattr(
        evaluator.shutil,
        "which",
        lambda tool: "/usr/bin/java" if tool == "java" else None,
    )

    assert evaluator.tika_command("--version") == [
        "java",
        "-jar",
        str(tika_jar),
        "--version",
    ]


def test_tika_command_prefers_installed_executable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        evaluator.shutil,
        "which",
        lambda tool: "/opt/homebrew/bin/tika" if tool == "tika" else None,
    )

    assert evaluator.tika_command("-t", "resume.pdf") == [
        "tika",
        "-t",
        "resume.pdf",
    ]


def test_reviewed_patch_rejects_a_stale_old_value() -> None:
    document = {"experience": [{"company": "Original, Inc."}]}
    patches = [
        {
            "pointer": "/experience/0/company",
            "old": "Stale, Inc.",
            "new": "Replacement, Inc.",
        }
    ]

    with pytest.raises(ValueError, match="expected 'Stale, Inc.'"):
        matrix.apply_reviewed_patches(document, patches, "case data")


def test_negative_control_rejects_unexpected_collateral_failures() -> None:
    case = {
        "name": "negative-control",
        "expectation": "fail",
        "expected_failed_gates": ["right_metadata_geometry"],
    }
    report = {
        "automated_status": "Fail",
        "gates": {
            "all_text_views": False,
            "right_metadata_geometry": False,
        },
    }

    assert not matrix.case_expectation_met(case, report)


def test_frozen_inputs_reject_concurrent_drift(tmp_path: Path) -> None:
    renderer = tmp_path / "renderer.typ"
    renderer.write_text("baseline", encoding="utf-8")
    expected = {"renderer": matrix.sha256(renderer)}
    renderer.write_text("changed during matrix", encoding="utf-8")

    with pytest.raises(SystemExit, match="frozen renderer hash"):
        matrix.verify_frozen_inputs(
            {"renderer": renderer}, expected, "post-compile"
        )


def test_matrix_output_directory_must_stay_in_repository(tmp_path: Path) -> None:
    with pytest.raises(SystemExit, match="must remain inside the repository"):
        matrix.create_output_dir(tmp_path / "external-evidence")


def test_geometry_rejects_right_metadata_outside_content_box(tmp_path: Path) -> None:
    xml = tmp_path / "overflow.xml"
    xml.write_text(
        """<?xml version="1.0" encoding="UTF-8"?>
<pdf2xml>
  <page number="1" height="1188" width="918">
    <text top="100" left="67" width="90">Example Company</text>
    <text top="100" left="170" width="70">Example Role</text>
    <text top="120" left="40" width="900">
      Dates: 2020 - Present · Location: UnbreakableLocation
    </text>
  </page>
</pdf2xml>
""",
        encoding="utf-8",
    )
    oracle = {
        "geometry_content_box": {
            "page_width_points": 612.0,
            "left_margin_points": 44.64,
            "right_margin_points": 44.64,
            "tolerance_px": 1.0,
        },
        "geometry_rows": [
            {
                "label": "overflow",
                "left_fields": ["Example Company", "Example Role"],
                "right_field": (
                    "Dates: 2020 - Present · Location: UnbreakableLocation"
                ),
            }
        ],
    }

    result = evaluator.geometry_audit(xml, oracle)

    assert not result["rows"][0]["right_within_content"]
    assert not result["passes"]


def test_every_manifest_case_applies_to_fresh_reviewed_baselines() -> None:
    manifest_path = GOLDEN_FIXTURE_ROOT / "golden-resume-stress-matrix.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    baseline = manifest["baseline"]
    data_path = REPO_ROOT / baseline["data"]
    oracle_path = REPO_ROOT / baseline["oracle"]
    baseline_data = json.loads(data_path.read_text(encoding="utf-8"))
    baseline_oracle = json.loads(oracle_path.read_text(encoding="utf-8"))

    for case in manifest["cases"]:
        case_data = copy.deepcopy(baseline_data)
        case_oracle = copy.deepcopy(baseline_oracle)
        matrix.apply_reviewed_patches(case_data, case["data_patches"], "data")
        matrix.apply_reviewed_patches(case_oracle, case["oracle_patches"], "oracle")
        assert baseline_data == json.loads(data_path.read_text(encoding="utf-8"))
        assert baseline_oracle == json.loads(oracle_path.read_text(encoding="utf-8"))


def test_manifest_hashes_match_reviewed_inputs() -> None:
    manifest = json.loads(
        (GOLDEN_FIXTURE_ROOT / "golden-resume-stress-matrix.json").read_text(
            encoding="utf-8"
        )
    )
    baseline = manifest["baseline"]

    for label in ("source", "data", "renderer", "oracle"):
        assert matrix.sha256(REPO_ROOT / baseline[label]) == baseline["sha256"][label]
