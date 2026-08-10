"""Contracts for the single Typst artifact-construction policy."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
from types import ModuleType

from resume_tools import artifact


def load_dev_adapter() -> ModuleType:
    path = Path(__file__).resolve().parents[1] / "scripts" / "dev.py"
    spec = importlib.util.spec_from_file_location("resume_dev_adapter", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sandbox(monkeypatch, tmp_path: Path) -> Path:
    (tmp_path / "fonts" / "source-sans-3").mkdir(parents=True)
    for name in ("SourceSans3-Regular.ttf", "SourceSans3-Bold.ttf"):
        (tmp_path / "fonts" / "source-sans-3" / name).write_bytes(name.encode())
    monkeypatch.setattr(artifact, "REPO_ROOT", tmp_path)
    return tmp_path


def test_compile_and_watch_share_the_pinned_policy(monkeypatch, tmp_path: Path) -> None:
    root = sandbox(monkeypatch, tmp_path)
    source = root / "resume.typ"
    output = root / "resume.pdf"
    data = root / "resume-data.json"
    source.write_text("#show: it => it", encoding="utf-8")
    data.write_text("{}", encoding="utf-8")
    request = artifact.CompileRequest(
        source=source,
        output=output,
        file_inputs={"data": data},
        dependencies_path=root / "deps.json",
    )

    compile = artifact.compile_command(request)
    watch = artifact.compile_command(request, watch=True)

    assert compile[0:2] == ["typst", "compile"]
    assert watch[0:2] == ["typst", "watch"]
    assert compile[2:] == watch[2:]
    assert ["--root", "."] == compile[2:4]
    assert ["--font-path", "fonts/source-sans-3"] == compile[4:6]
    assert ["--pdf-standard", "ua-1"] == compile[6:8]
    assert "data=/resume-data.json" in compile


def test_negative_fixture_policy_is_the_only_pdf_ua_exemption(
    monkeypatch, tmp_path: Path
) -> None:
    root = sandbox(monkeypatch, tmp_path)
    source = root / "fixture.typ"
    output = root / "fixture.pdf"
    source.write_text("#show: it => it", encoding="utf-8")
    request = artifact.CompileRequest(
        source=source,
        output=output,
        purpose=artifact.ArtifactPurpose.NEGATIVE_FIXTURE,
    )

    assert "--pdf-standard" not in artifact.compile_command(request)


def test_provenance_records_transitive_inputs_and_pinned_fonts(monkeypatch, tmp_path: Path) -> None:
    root = sandbox(monkeypatch, tmp_path)
    source = root / "resume.typ"
    renderer = root / "renderer.typ"
    data = root / "resume-data.json"
    output = root / "resume.pdf"
    dependencies = root / "deps.json"
    for path in (source, renderer, data, output):
        path.write_text(path.name, encoding="utf-8")
    dependencies.write_text(
        json.dumps({"inputs": ["resume.typ", "renderer.typ", "resume-data.json"]}),
        encoding="utf-8",
    )
    request = artifact.CompileRequest(
        source=source,
        output=output,
        file_inputs={"data": data},
        dependencies_path=dependencies,
        provenance_path=root / "provenance.json",
    )

    provenance_path = artifact.write_provenance(request)
    provenance = artifact.load_provenance(provenance_path)

    assert {record["path"] for record in provenance["typst_dependencies"]} == {
        "resume.typ",
        "renderer.typ",
        "resume-data.json",
    }
    assert provenance["inputs"] == {"data": "resume-data.json"}
    assert {record["path"] for record in provenance["font_assets"]} == {
        "fonts/source-sans-3/SourceSans3-Regular.ttf",
        "fonts/source-sans-3/SourceSans3-Bold.ttf",
    }


def test_freshness_rejects_changed_transitive_dependency(monkeypatch, tmp_path: Path) -> None:
    root = sandbox(monkeypatch, tmp_path)
    source = root / "resume.typ"
    renderer = root / "renderer.typ"
    output = root / "resume.pdf"
    dependencies = root / "deps.json"
    for path in (source, renderer):
        path.write_text(path.name, encoding="utf-8")
    dependencies.write_text(
        json.dumps({"inputs": ["resume.typ", "renderer.typ"]}), encoding="utf-8"
    )
    output.write_bytes(b"compiled")
    request = artifact.CompileRequest(
        source=source,
        output=output,
        dependencies_path=dependencies,
        provenance_path=root / "provenance.json",
    )
    provenance = artifact.build_provenance(request)

    renderer.write_text("changed renderer", encoding="utf-8")
    os.utime(renderer, None)
    freshness = artifact.evaluate_freshness(output, provenance)

    assert not freshness.is_fresh
    assert "renderer.typ" in freshness.stale
    assert "renderer.typ" in freshness.changed


def test_freshness_rejects_provenance_for_another_source(monkeypatch, tmp_path: Path) -> None:
    root = sandbox(monkeypatch, tmp_path)
    source = root / "resume.typ"
    other_source = root / "other.typ"
    output = root / "resume.pdf"
    dependencies = root / "deps.json"
    for path in (source, other_source):
        path.write_text(path.name, encoding="utf-8")
    dependencies.write_text(json.dumps({"inputs": ["resume.typ"]}), encoding="utf-8")
    output.write_bytes(b"compiled")
    request = artifact.CompileRequest(
        source=source, output=output, dependencies_path=dependencies
    )

    freshness = artifact.evaluate_freshness(
        output, artifact.build_provenance(request), source=other_source
    )

    assert not freshness.is_fresh
    assert freshness.stale == ("provenance was recorded for another source",)


def test_adapters_delegate_without_rebuilding_typst_flags() -> None:
    root = Path(__file__).resolve().parents[1]
    callers = [
        root / "justfile",
        root / "scripts" / "dev.py",
        root / "tests" / "conftest.py",
        root / ".agents" / "skills" / "resume-parsability" / "scripts" / "evaluate_golden_stress_matrix.py",
        root / ".github" / "workflows" / "compile-resume.yml",
        root / ".github" / "workflows" / "extraction-check.yml",
    ]

    for path in callers:
        text = path.read_text(encoding="utf-8")
        assert "--font-path" not in text, path
        assert "--pdf-standard" not in text, path
        assert '"typst", "compile"' not in text, path


def test_dev_adapter_opens_pdf_on_macos_without_name_error(monkeypatch) -> None:
    dev = load_dev_adapter()
    opened: list[tuple[list[str], bool]] = []

    def fake_run(command: list[str], *, check: bool) -> None:
        opened.append((command, check))

    monkeypatch.setattr(dev.sys, "platform", "darwin")
    monkeypatch.setattr(dev.subprocess, "run", fake_run)

    dev.open_pdf()

    assert opened == [(["open", dev.PDF], False)]
