"""Contracts for the Golden Resume deep evaluator and stress matrix."""

from __future__ import annotations

import importlib.util
import inspect
import json
import xml.etree.ElementTree as element_tree
from collections.abc import Callable
from pathlib import Path
from types import ModuleType

import pytest

from resume_tools import artifact, golden_evaluation, golden_stress


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_ROOT = REPO_ROOT / ".agents" / "skills" / "resume-parsability"
GOLDEN_FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "golden-resume"


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


matrix = load_module(
    "golden_resume_stress_matrix",
    SKILL_ROOT / "scripts" / "evaluate_golden_stress_matrix.py",
)


def compiled_evaluation_request(tmp_path: Path) -> golden_evaluation.EvaluationRequest:
    run_root = (
        REPO_ROOT
        / ".extraction"
        / "pytest-golden-evaluation"
        / tmp_path.parent.name
        / tmp_path.name
    )
    run_root.mkdir(parents=True, exist_ok=False)
    pdf = run_root / "golden-resume.pdf"
    dependencies = run_root / "typst-dependencies.json"
    provenance = run_root / "typst-provenance.json"
    compiled = artifact.compile_artifact(
        artifact.CompileRequest(
            source=GOLDEN_FIXTURE_ROOT / "golden-resume.typ",
            output=pdf,
            dependencies_path=dependencies,
            provenance_path=provenance,
        ),
        capture_output=True,
    )
    assert compiled.returncode == 0, compiled.stderr
    return golden_evaluation.EvaluationRequest(
        pdf=pdf,
        source=GOLDEN_FIXTURE_ROOT / "golden-resume.typ",
        provenance=provenance,
        oracle=GOLDEN_FIXTURE_ROOT / "golden-resume-oracle.json",
        output_dir=run_root / "evaluation",
    )


def evaluate_with_evidence_mutation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    mutate: Callable[[Path], None],
) -> golden_evaluation.EvaluationResult:
    request = compiled_evaluation_request(tmp_path)
    capture = golden_evaluation.pdf_evidence.capture_pdf_evidence

    def capture_then_mutate(*args: object, **kwargs: object) -> dict[str, object]:
        results = capture(*args, **kwargs)
        assert request.output_dir is not None
        mutate(request.output_dir)
        return results

    monkeypatch.setattr(
        golden_evaluation.pdf_evidence,
        "capture_pdf_evidence",
        capture_then_mutate,
    )
    return golden_evaluation.evaluate(request)


def test_golden_evaluation_exposes_one_operation() -> None:
    operations = {
        name
        for name, value in vars(golden_evaluation).items()
        if not name.startswith("_")
        and inspect.isfunction(value)
        and value.__module__ == golden_evaluation.__name__
    }

    assert operations == {"evaluate"}


def test_semantic_case_rejects_stale_reviewed_oracle_value() -> None:
    manifest = golden_stress.parse_manifest(
        json.loads(
            (GOLDEN_FIXTURE_ROOT / "golden-resume-stress-matrix.json").read_text(
                encoding="utf-8"
            )
        )
    )
    case = next(case for case in manifest.cases if case.name == "long-company")
    baseline_data = json.loads(
        (GOLDEN_FIXTURE_ROOT / "golden-resume-data.json").read_text(encoding="utf-8")
    )
    baseline_oracle = json.loads(
        (GOLDEN_FIXTURE_ROOT / "golden-resume-oracle.json").read_text(encoding="utf-8")
    )
    baseline_data["experience"][0]["company"] = "Stale Employer, Inc."

    with pytest.raises(golden_stress.StressSpecificationError, match="exactly once, found 0"):
        golden_stress.materialize_case(baseline_data, baseline_oracle, case)


def test_public_evaluation_returns_structured_result(tmp_path: Path) -> None:
    result = golden_evaluation.evaluate(compiled_evaluation_request(tmp_path))

    assert result.ok
    assert result.returncode == 0
    assert result.automated_status == "Pass"
    assert result.page_count == 1
    assert result.gates["right_metadata_geometry"]
    assert result.minimum_clearance_px is not None
    assert result.stacked_rows >= 0
    assert len(result.render_paths) == result.page_count
    assert result.report_json.is_file()
    assert result.report_markdown.is_file()


def test_public_evaluation_accepts_tika_uri_block_before_later_text(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    oracle = json.loads(
        (GOLDEN_FIXTURE_ROOT / "golden-resume-oracle.json").read_text(
            encoding="utf-8"
        )
    )
    annotation_block = "\n".join(oracle["links"]) + "\n"

    def move_annotations_before_skills(output: Path) -> None:
        tika = output / "tika.txt"
        text = tika.read_text(encoding="utf-8")
        assert text.count(annotation_block) == 1
        visible = text.replace(annotation_block, "", 1)
        marker = "\nSKILLS\n"
        assert marker in visible
        tika.write_text(
            visible.replace(marker, f"\n{annotation_block}SKILLS\n", 1),
            encoding="utf-8",
        )

    result = evaluate_with_evidence_mutation(
        tmp_path, monkeypatch, move_annotations_before_skills
    )

    assert result.gates["tika_exact_uri_annotation_block"]
    assert result.gates["all_text_views"]


def test_public_evaluation_rejects_duplicate_tika_uri_blocks(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    oracle = json.loads(
        (GOLDEN_FIXTURE_ROOT / "golden-resume-oracle.json").read_text(
            encoding="utf-8"
        )
    )
    annotation_block = "\n".join(oracle["links"]) + "\n"

    def duplicate_annotations(output: Path) -> None:
        tika = output / "tika.txt"
        text = tika.read_text(encoding="utf-8")
        assert text.count(annotation_block) == 1
        tika.write_text(text + "\n" + annotation_block, encoding="utf-8")

    result = evaluate_with_evidence_mutation(
        tmp_path, monkeypatch, duplicate_annotations
    )

    assert not result.ok
    assert not result.gates["tika_exact_uri_annotation_block"]


def test_public_evaluation_rejects_right_metadata_outside_content_box(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    oracle = json.loads(
        (GOLDEN_FIXTURE_ROOT / "golden-resume-oracle.json").read_text(
            encoding="utf-8"
        )
    )
    right_field = oracle["geometry_rows"][0]["right_field"]

    def overflow_right_metadata(output: Path) -> None:
        xml = output / "poppler.xml"
        tree = element_tree.parse(xml)
        matches = [
            node
            for node in tree.getroot().iter("text")
            if " ".join("".join(node.itertext()).split()) == right_field
        ]
        assert len(matches) == 1
        matches[0].set("left", "40")
        matches[0].set("width", "900")
        tree.write(xml, encoding="utf-8", xml_declaration=True)

    result = evaluate_with_evidence_mutation(
        tmp_path, monkeypatch, overflow_right_metadata
    )

    assert not result.ok
    assert not result.gates["right_metadata_geometry"]


def test_public_evaluation_translates_missing_inputs(tmp_path: Path) -> None:
    with pytest.raises(
        golden_evaluation.GoldenEvaluationError,
        match="required file does not exist",
    ):
        golden_evaluation.evaluate(
            golden_evaluation.EvaluationRequest(
                pdf=tmp_path / "missing.pdf",
                output_dir=tmp_path / "unused-evidence",
            )
        )


def test_negative_control_rejects_unexpected_collateral_failures() -> None:
    case = golden_stress.StressCase(
        name="negative-control",
        description="A fail case that does not permit unrelated gate failures.",
        expectation="fail",
        mutations=(),
        expected_failed_gates=("right_metadata_geometry",),
    )
    gates = {
        "all_text_views": False,
        "right_metadata_geometry": False,
    }

    assert not golden_stress.expectation_met(case, "Fail", gates)


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


def test_every_manifest_case_applies_to_fresh_reviewed_baselines() -> None:
    manifest_path = GOLDEN_FIXTURE_ROOT / "golden-resume-stress-matrix.json"
    manifest = golden_stress.parse_manifest(
        json.loads(manifest_path.read_text(encoding="utf-8"))
    )
    baseline = manifest.baseline
    data_path = REPO_ROOT / baseline["data"]
    oracle_path = REPO_ROOT / baseline["oracle"]
    baseline_data = json.loads(data_path.read_text(encoding="utf-8"))
    baseline_oracle = json.loads(oracle_path.read_text(encoding="utf-8"))

    for case in manifest.cases:
        case_data, case_oracle = golden_stress.materialize_case(
            baseline_data, baseline_oracle, case
        )
        assert case_data is not baseline_data
        assert case_oracle is not baseline_oracle
        assert baseline_data == json.loads(data_path.read_text(encoding="utf-8"))
        assert baseline_oracle == json.loads(oracle_path.read_text(encoding="utf-8"))


def test_manifest_hashes_match_reviewed_inputs() -> None:
    manifest = golden_stress.parse_manifest(
        json.loads(
        (GOLDEN_FIXTURE_ROOT / "golden-resume-stress-matrix.json").read_text(
            encoding="utf-8"
        )
        )
    )
    baseline = manifest.baseline

    for label in ("source", "data", "renderer", "oracle"):
        assert matrix.sha256(REPO_ROOT / baseline[label]) == baseline["sha256"][label]


def test_manifest_uses_only_semantic_mutations() -> None:
    manifest_path = GOLDEN_FIXTURE_ROOT / "golden-resume-stress-matrix.json"
    raw = json.loads(manifest_path.read_text(encoding="utf-8"))
    encoded = manifest_path.read_text(encoding="utf-8")

    assert raw["schema_version"] == 1
    assert '"pointer"' not in encoded
    assert '"old"' not in encoded
    assert '"data_patches"' not in encoded
    assert '"oracle_patches"' not in encoded
    assert "/experience/" not in encoded
    assert "/required_" not in encoded
    assert "/geometry_rows/" not in encoded
    assert "Dates: " not in encoded
    assert "Location: " not in encoded
    assert "Focus: " not in encoded
    for case in raw["cases"]:
        assert set(case) <= {
            "name",
            "description",
            "expectation",
            "expected_failed_gates",
            "mutations",
        }
        for mutation in case["mutations"]:
            assert set(mutation) == {"subject", "field", "value"}
            assert not mutation["subject"].isdigit()
            assert not mutation["field"].isdigit()


def test_manifest_schema_rejects_pointer_patch_surface() -> None:
    raw = json.loads(
        (GOLDEN_FIXTURE_ROOT / "golden-resume-stress-matrix.json").read_text(
            encoding="utf-8"
        )
    )
    raw["cases"][1]["mutations"][0]["pointer"] = "/experience/0/company"

    with pytest.raises(golden_stress.StressSpecificationError, match="keys must be"):
        golden_stress.parse_manifest(raw)


def test_semantic_mutations_update_reviewed_data_and_independent_oracle() -> None:
    manifest = golden_stress.parse_manifest(
        json.loads(
            (GOLDEN_FIXTURE_ROOT / "golden-resume-stress-matrix.json").read_text(
                encoding="utf-8"
            )
        )
    )
    case = next(case for case in manifest.cases if case.name == "combined-metadata-pressure")
    baseline_data = json.loads(
        (GOLDEN_FIXTURE_ROOT / "golden-resume-data.json").read_text(encoding="utf-8")
    )
    baseline_oracle = json.loads(
        (GOLDEN_FIXTURE_ROOT / "golden-resume-oracle.json").read_text(encoding="utf-8")
    )

    data, oracle = golden_stress.materialize_case(baseline_data, baseline_oracle, case)

    experience = data["experience"][0]
    assert experience == {
        **baseline_data["experience"][0],
        "company": "International Commerce Infrastructure Group, Inc.",
        "role": "Senior Principal Site Reliability Engineer",
        "dates": "September 2017 - Present",
        "location": "Washington, District of Columbia",
    }
    assert "International Commerce Infrastructure Group, Inc." in oracle["required_once"]
    assert "Senior Principal Site Reliability Engineer" in oracle["required_order"]
    northstar = next(
        window for window in oracle["association_windows"] if window["label"] == "northstar experience"
    )
    assert northstar["start"] == "International Commerce Infrastructure Group, Inc."
    assert northstar["fields"][2:] == [
        "Dates: September 2017 - Present",
        "Location: Washington, District of Columbia",
        *baseline_oracle["association_windows"][1]["fields"][4:],
    ]
    row = next(row for row in oracle["geometry_rows"] if row["label"] == "northstar experience")
    assert row["right_field"] == "Dates: September 2017 - Present · Location: Washington, District of Columbia"
    assert baseline_data["experience"][0]["company"] == "Northstar Systems, Inc."
    assert baseline_oracle["geometry_rows"][0]["right_field"] == "Dates: 2022 - Present · Location: Chicago, IL"


def test_every_semantic_value_updates_data_and_reviewed_oracle() -> None:
    manifest = golden_stress.parse_manifest(
        json.loads(
            (GOLDEN_FIXTURE_ROOT / "golden-resume-stress-matrix.json").read_text(
                encoding="utf-8"
            )
        )
    )
    baseline_data = json.loads(
        (GOLDEN_FIXTURE_ROOT / "golden-resume-data.json").read_text(encoding="utf-8")
    )
    baseline_oracle = json.loads(
        (GOLDEN_FIXTURE_ROOT / "golden-resume-oracle.json").read_text(encoding="utf-8")
    )

    for case in manifest.cases:
        data, oracle = golden_stress.materialize_case(baseline_data, baseline_oracle, case)
        rendered_data = json.dumps(data)
        rendered_oracle = json.dumps(oracle)
        for mutation in case.mutations:
            assert mutation.value in rendered_data
            assert mutation.value in rendered_oracle
