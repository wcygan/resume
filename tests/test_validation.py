"""Focused contracts for the shared resume validation plans."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

from resume_tools import validation


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_local_ci_adapter() -> ModuleType:
    path = REPO_ROOT / "scripts" / "run-local-ci.py"
    spec = importlib.util.spec_from_file_location("local_ci_adapter", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def step_names(intent: validation.ValidationIntent) -> list[str]:
    return [step.name for step in validation.plan_for(intent)]


def test_change_intents_select_reviewed_check_membership_and_order() -> None:
    assert step_names(validation.ValidationIntent.CONTENT) == [
        "compile-resume",
        "page-budget",
        "extraction-check",
    ]
    assert step_names(validation.ValidationIntent.RENDERER) == [
        "compile-resume",
        "page-budget",
        "extraction-check",
        "compile-golden",
        "golden-check",
        "golden-stress",
    ]
    assert step_names(validation.ValidationIntent.FULL) == [
        "compile-resume",
        "page-budget",
        "extraction-check",
        "test",
        "compile-golden",
        "golden-check",
        "golden-stress",
    ]


def test_plan_failure_preserves_status_and_stops_before_later_checks() -> None:
    seen: list[tuple[str, ...]] = []

    def runner(command: tuple[str, ...]) -> int:
        seen.append(command)
        return 23 if command == validation.EXTRACTION_CHECK.command else 0

    messages: list[str] = []
    run = validation.run_plan("renderer", runner=runner, report=messages.append)

    assert run.returncode == 23
    assert [result.step.name for result in run.results] == [
        "compile-resume",
        "page-budget",
        "extraction-check",
    ]
    assert seen == [
        validation.COMPILE_RESUME.command,
        validation.PAGE_BUDGET.command,
        validation.EXTRACTION_CHECK.command,
    ]
    assert "evidence: .extraction" in messages[-1]


def test_clean_renderer_plan_builds_golden_provenance_before_evaluation(
    monkeypatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(validation, "REPO_ROOT", tmp_path)
    provenance = tmp_path / validation.COMPILE_GOLDEN.evidence_locations[-1]
    assert not provenance.exists()
    seen: list[tuple[str, ...]] = []

    def runner(command: tuple[str, ...]) -> int:
        seen.append(command)
        if command == validation.COMPILE_GOLDEN.command:
            provenance.parent.mkdir(parents=True)
            provenance.write_text("fresh provenance", encoding="utf-8")
        if command == validation.GOLDEN_CHECK.command:
            assert provenance.is_file(), "Golden evaluation requires fresh provenance"
        return 0

    run = validation.run_plan("renderer", runner=runner, report=lambda _message: None)

    assert run.ok
    assert seen.index(validation.COMPILE_GOLDEN.command) < seen.index(
        validation.GOLDEN_CHECK.command
    )


def test_missing_command_is_translated_and_records_its_evidence() -> None:
    def runner(_command: tuple[str, ...]) -> int:
        raise FileNotFoundError("uv is unavailable")

    messages: list[str] = []
    run = validation.run_plan("compile", runner=runner, report=messages.append)

    assert run.returncode == 127
    assert run.results[0].error == "uv is unavailable"
    assert "artifact-provenance" in messages[-1]


def test_cli_returns_the_plan_failure_status(monkeypatch) -> None:
    failed_step = validation.StepResult(validation.COMPILE_RESUME, 19)
    failed_run = validation.ValidationRun(
        validation.ValidationIntent.COMPILE, (failed_step,)
    )
    monkeypatch.setattr(validation, "run_plan", lambda _intent: failed_run)

    assert validation.main(["compile"]) == 19


def test_just_and_workflow_adapters_delegate_to_the_validation_module() -> None:
    justfile = (REPO_ROOT / "justfile").read_text(encoding="utf-8")
    extraction_workflow = (
        REPO_ROOT / ".github" / "workflows" / "extraction-check.yml"
    ).read_text(encoding="utf-8")
    compile_workflow = (
        REPO_ROOT / ".github" / "workflows" / "compile-resume.yml"
    ).read_text(encoding="utf-8")

    for intent in ("content", "renderer", "full"):
        assert f"-m resume_tools.validation {intent}" in justfile
    assert "-m resume_tools.validation full" in extraction_workflow
    assert "-m resume_tools.validation compile" in compile_workflow
    assert "scripts/extraction_check.py" not in extraction_workflow
    assert "resume_tools.artifact resume" not in compile_workflow


def test_local_ci_passes_the_selected_workflow_to_act(monkeypatch) -> None:
    local_ci = load_local_ci_adapter()
    calls: list[list[str]] = []

    class Result:
        returncode = 0

    def fake_run(command: list[str], **_kwargs: object) -> Result:
        calls.append(command)
        return Result()

    monkeypatch.setattr(local_ci.subprocess, "run", fake_run)
    assert local_ci.run_workflow("extraction-check.yml", None, False, False) == 0

    assert calls == [[
        "act",
        "--workflows",
        ".github/workflows/extraction-check.yml",
        "--platform",
        local_ci.DEFAULT_PLATFORM,
    ]]
