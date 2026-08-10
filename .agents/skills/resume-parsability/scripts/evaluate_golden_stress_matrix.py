#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Compile and evaluate isolated content-length stresses for the Golden Resume."""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import json
import pathlib
import subprocess
import sys
from typing import Any


SKILL_ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO_ROOT = SKILL_ROOT.parents[2]
GOLDEN_FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "golden-resume"
DEFAULT_MANIFEST = GOLDEN_FIXTURE_ROOT / "golden-resume-stress-matrix.json"
EVALUATOR = SKILL_ROOT / "scripts" / "evaluate_golden_resume.py"
sys.path.insert(0, str(REPO_ROOT))

from resume_tools import artifact  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the reviewed Golden Resume content-length stress matrix."
    )
    parser.add_argument("--manifest", type=pathlib.Path, default=DEFAULT_MANIFEST)
    parser.add_argument(
        "--case",
        action="append",
        dest="cases",
        help="Run only the named case. May be repeated.",
    )
    parser.add_argument(
        "--output-dir",
        type=pathlib.Path,
        help="New evidence directory; defaults beneath .extraction/golden-resume-stress.",
    )
    parser.add_argument("--list", action="store_true", help="List case names and exit.")
    return parser.parse_args()


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=REPO_ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def pointer_parts(pointer: str) -> list[str]:
    if not pointer.startswith("/"):
        raise ValueError(f"JSON pointer must start with '/': {pointer}")
    return [part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/")]


def pointer_get(document: Any, pointer: str) -> Any:
    value = document
    for part in pointer_parts(pointer):
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def pointer_set(document: Any, pointer: str, new_value: Any) -> None:
    parts = pointer_parts(pointer)
    if not parts:
        raise ValueError("root replacement is not supported")
    parent = document
    for part in parts[:-1]:
        parent = parent[int(part)] if isinstance(parent, list) else parent[part]
    final = parts[-1]
    if isinstance(parent, list):
        parent[int(final)] = new_value
    else:
        parent[final] = new_value


def apply_reviewed_patches(document: Any, patches: list[dict[str, Any]], label: str) -> None:
    seen: set[str] = set()
    for patch in patches:
        pointer = str(patch["pointer"])
        if pointer in seen:
            raise ValueError(f"{label} patches repeat pointer {pointer}")
        seen.add(pointer)
        actual = pointer_get(document, pointer)
        if actual != patch["old"]:
            raise ValueError(
                f"{label} patch {pointer} expected {patch['old']!r}, found {actual!r}"
            )
        pointer_set(document, pointer, patch["new"])


def create_output_dir(requested: pathlib.Path | None) -> pathlib.Path:
    if requested is None:
        stamp = dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%S.%fZ")
        requested = REPO_ROOT / ".extraction" / "golden-resume-stress" / stamp
    output = requested.expanduser().resolve()
    try:
        output.relative_to(REPO_ROOT)
    except ValueError as error:
        raise SystemExit(
            f"stress evidence directory must remain inside the repository: {output}"
        ) from error
    if output == REPO_ROOT:
        raise SystemExit(f"unsafe output directory: {output}")
    output.mkdir(parents=True, exist_ok=False)
    return output


def relative_to_repo(path: pathlib.Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError as error:
        raise SystemExit(f"stress artifacts must remain inside the repository: {path}") from error


def write_json(path: pathlib.Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def case_expectation_met(case: dict[str, Any], report: dict[str, Any]) -> bool:
    expectation = case["expectation"]
    if expectation == "pass":
        return report["automated_status"] == "Pass"
    if expectation == "fail":
        expected_failed = set(case.get("expected_failed_gates", []))
        observed_failed = {name for name, passed in report["gates"].items() if not passed}
        return report["automated_status"] == "Fail" and expected_failed == observed_failed
    raise ValueError(f"unsupported expectation {expectation!r} in {case['name']}")


def markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# Golden Resume Stress Matrix",
        "",
        f"- Matrix status: **{report['matrix_status']}**",
        (
            f"- Scope: **{report['scope']}** "
            f"({report['selected_case_count']} of {report['total_case_count']} cases)"
        ),
        f"- Evidence: `{report['evidence_directory']}`",
        "- External ATS / Greenhouse UAT: **Untested**",
        "",
        "| Case | Expected | Observed | Met | Pages | Stacked rows | Minimum clearance (px) |",
        "| --- | --- | --- | --- | ---: | ---: | ---: |",
    ]
    for case in report["cases"]:
        clearance = case.get("minimum_clearance_px")
        clearance_text = "n/a" if clearance is None else f"{clearance:.1f}"
        lines.append(
            f"| {case['name']} | {case['expectation']} | {case['observed_status']} | "
            f"{'yes' if case['expectation_met'] else 'no'} | {case.get('page_count', 'n/a')} | "
            f"{case.get('stacked_rows', 'n/a')} | {clearance_text} |"
        )
    lines.extend(
        [
            "",
            "Each case uses the same renderer and a fresh copy of the reviewed baseline.",
            "Observed local extraction and geometry are not commercial ATS certification.",
            "",
        ]
    )
    return "\n".join(lines)


def verify_frozen_inputs(
    paths: dict[str, pathlib.Path], expected_hashes: dict[str, str], stage: str
) -> None:
    for label, path in paths.items():
        if not path.is_file():
            raise SystemExit(f"{stage}: missing frozen {label}: {path}")
        actual = sha256(path)
        expected = expected_hashes[label]
        if actual != expected:
            raise SystemExit(
                f"{stage}: frozen {label} hash is {actual}, expected {expected}"
            )


def main() -> int:
    args = parse_args()
    manifest_path = args.manifest.expanduser().resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    all_cases = manifest["cases"]
    if args.list:
        for case in all_cases:
            print(case["name"])
        return 0

    selected_names = set(args.cases or [])
    known_names = {case["name"] for case in all_cases}
    unknown = selected_names - known_names
    if unknown:
        raise SystemExit(f"unknown cases: {', '.join(sorted(unknown))}")
    cases = [case for case in all_cases if not selected_names or case["name"] in selected_names]

    baseline = manifest["baseline"]
    source_path = REPO_ROOT / baseline["source"]
    data_path = REPO_ROOT / baseline["data"]
    renderer_path = REPO_ROOT / baseline["renderer"]
    oracle_path = REPO_ROOT / baseline["oracle"]
    paths = {
        "source": source_path,
        "data": data_path,
        "renderer": renderer_path,
        "oracle": oracle_path,
    }
    verify_frozen_inputs(paths, baseline["sha256"], "matrix preflight")

    baseline_data = json.loads(data_path.read_text(encoding="utf-8"))
    baseline_oracle = json.loads(oracle_path.read_text(encoding="utf-8"))
    output = create_output_dir(args.output_dir)
    results: list[dict[str, Any]] = []

    for case in cases:
        verify_frozen_inputs(paths, baseline["sha256"], f"{case['name']} preflight")
        case_dir = output / case["name"]
        case_dir.mkdir()
        case_data = copy.deepcopy(baseline_data)
        case_oracle = copy.deepcopy(baseline_oracle)
        apply_reviewed_patches(case_data, case["data_patches"], f"{case['name']} data")
        apply_reviewed_patches(case_oracle, case["oracle_patches"], f"{case['name']} oracle")
        if baseline_data != json.loads(data_path.read_text(encoding="utf-8")):
            raise RuntimeError("baseline data mutated while building cases")
        if baseline_oracle != json.loads(oracle_path.read_text(encoding="utf-8")):
            raise RuntimeError("baseline oracle mutated while building cases")

        effective_data = case_dir / "input.json"
        effective_oracle = case_dir / "oracle.json"
        pdf = case_dir / "resume.pdf"
        dependencies = case_dir / "typst-dependencies.json"
        provenance = case_dir / "typst-provenance.json"
        write_json(effective_data, case_data)
        write_json(effective_oracle, case_oracle)

        compile_request = artifact.CompileRequest(
            source=source_path,
            output=pdf,
            file_inputs={"data": effective_data},
            dependencies_path=dependencies,
            provenance_path=provenance,
        )
        compile_command = artifact.compile_command(compile_request)
        compiled = artifact.compile_artifact(compile_request, capture_output=True)
        (case_dir / "compile.stdout").write_text(compiled.stdout, encoding="utf-8")
        (case_dir / "compile.stderr").write_text(compiled.stderr, encoding="utf-8")
        if compiled.returncode != 0:
            results.append(
                {
                    "name": case["name"],
                    "description": case["description"],
                    "expectation": case["expectation"],
                    "observed_status": "CompileError",
                    "expectation_met": False,
                    "compile_returncode": compiled.returncode,
                }
            )
            continue

        verify_frozen_inputs(paths, baseline["sha256"], f"{case['name']} post-compile")

        dependency_inputs = json.loads(dependencies.read_text(encoding="utf-8"))["inputs"]
        required_dependencies = {
            baseline["source"],
            baseline["renderer"],
            relative_to_repo(effective_data),
        }
        if not required_dependencies <= set(dependency_inputs):
            missing = sorted(required_dependencies - set(dependency_inputs))
            raise RuntimeError(f"{case['name']} dependency evidence missing {missing}")

        evaluation_dir = case_dir / "evaluation"
        evaluated = run(
            [
                sys.executable,
                str(EVALUATOR),
                "--pdf",
                str(pdf),
                "--source",
                str(source_path),
                "--provenance",
                str(provenance),
                "--oracle",
                str(effective_oracle),
                "--output-dir",
                str(evaluation_dir),
            ]
        )
        (case_dir / "evaluate.stdout").write_text(evaluated.stdout, encoding="utf-8")
        (case_dir / "evaluate.stderr").write_text(evaluated.stderr, encoding="utf-8")
        report_path = evaluation_dir / "report.json"
        if not report_path.is_file():
            results.append(
                {
                    "name": case["name"],
                    "description": case["description"],
                    "expectation": case["expectation"],
                    "observed_status": "EvaluationError",
                    "expectation_met": False,
                    "evaluation_returncode": evaluated.returncode,
                }
            )
            continue
        case_report = json.loads(report_path.read_text(encoding="utf-8"))
        verify_frozen_inputs(paths, baseline["sha256"], f"{case['name']} post-evaluation")
        geometry_rows = case_report["pdf"]["geometry"]["rows"]
        clearances = [
            row["clearance_px"]
            for row in geometry_rows
            if row["clearance_px"] is not None
        ]
        results.append(
            {
                "name": case["name"],
                "description": case["description"],
                "expectation": case["expectation"],
                "observed_status": case_report["automated_status"],
                "expectation_met": case_expectation_met(case, case_report),
                "minimum_clearance_px": min(clearances) if clearances else None,
                "page_count": int(case_report["artifact"]["pdfinfo"]["Pages"]),
                "stacked_rows": sum(row["layout"] == "stacked-right" for row in geometry_rows),
                "failed_gates": [
                    name for name, passed in case_report["gates"].items() if not passed
                ],
                "compile_returncode": compiled.returncode,
                "evaluation_returncode": evaluated.returncode,
                "compile_command": compile_command,
                "typst_dependencies": dependency_inputs,
                "artifact_sha256": sha256(pdf),
                "data_sha256": sha256(effective_data),
                "oracle_sha256": sha256(effective_oracle),
                "renderer_sha256": sha256(renderer_path),
                "report": relative_to_repo(report_path),
                "renders": [
                    relative_to_repo(pathlib.Path(path))
                    for path in case_report["pdf"]["renders"]
                ],
            }
        )

    verify_frozen_inputs(paths, baseline["sha256"], "matrix completion")
    all_expectations_met = bool(results) and all(
        case["expectation_met"] for case in results
    )
    matrix_status = "Pass" if all_expectations_met else "Fail"
    scope = "full" if len(cases) == len(all_cases) else "partial"
    report = {
        "matrix_status": matrix_status,
        "scope": scope,
        "selected_case_count": len(cases),
        "total_case_count": len(all_cases),
        "evidence_directory": str(output),
        "manifest": str(manifest_path),
        "baseline_hashes": baseline["sha256"],
        "source_sha256": sha256(source_path),
        "evaluator_sha256": sha256(EVALUATOR),
        "cases": results,
        "external_ats_uat": "Untested",
    }
    write_json(output / "matrix-report.json", report)
    (output / "matrix-report.md").write_text(markdown_report(report), encoding="utf-8")
    print(f"Golden Resume stress matrix: {matrix_status}")
    print(f"Scope: {scope} ({len(cases)} of {len(all_cases)} cases)")
    print(f"Evidence: {output}")
    for case in results:
        print(
            f"- {case['name']}: expected={case['expectation']} "
            f"observed={case['observed_status']} met={case['expectation_met']}"
        )
    return 0 if matrix_status == "Pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
