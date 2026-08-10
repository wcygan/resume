"""Construct Typst resume artifacts and retain their input provenance.

All callers use this module for the compiler policy.  The sidecar provenance is
deliberately stored beneath ``.extraction``: it is reproducibility evidence,
not a second checked-in resume artifact.
"""

from __future__ import annotations

import argparse
import enum
import hashlib
import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
TYPST_ROOT_ARGUMENT = "."
FONT_DIRECTORY = Path("fonts/source-sans-3")
PDF_STANDARD = "ua-1"
PROVENANCE_SCHEMA_VERSION = 1


class ArtifactPurpose(enum.StrEnum):
    """The limited policy variations owned by this module."""

    RESUME = "resume"
    NEGATIVE_FIXTURE = "negative-fixture"


def _resolve(path: Path | str) -> Path:
    return Path(path).expanduser().resolve()


def _relative_to_root(path: Path | str) -> str:
    resolved = _resolve(path)
    try:
        return str(resolved.relative_to(REPO_ROOT))
    except ValueError as error:
        raise ValueError(f"artifact path must remain inside repository: {resolved}") from error


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass(frozen=True)
class CompileRequest:
    """The source, output, and file-backed Typst inputs for one artifact."""

    source: Path
    output: Path
    purpose: ArtifactPurpose = ArtifactPurpose.RESUME
    file_inputs: Mapping[str, Path] = field(default_factory=dict)
    string_inputs: Mapping[str, str] = field(default_factory=dict)
    dependencies_path: Path | None = None
    provenance_path: Path | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "source", _resolve(self.source))
        object.__setattr__(self, "output", _resolve(self.output))
        object.__setattr__(
            self,
            "file_inputs",
            {key: _resolve(value) for key, value in self.file_inputs.items()},
        )
        if self.dependencies_path is not None:
            object.__setattr__(self, "dependencies_path", _resolve(self.dependencies_path))
        if self.provenance_path is not None:
            object.__setattr__(self, "provenance_path", _resolve(self.provenance_path))


@dataclass(frozen=True)
class Freshness:
    """Whether an output still represents every recorded dependency."""

    is_fresh: bool
    stale: tuple[str, ...]
    missing: tuple[str, ...]
    changed: tuple[str, ...]


def provenance_path_for(output: Path | str) -> Path:
    """Return the disposable, deterministic sidecar path for an artifact."""
    output_name = _resolve(output).name
    return REPO_ROOT / ".extraction" / "artifact-provenance" / f"{output_name}.json"


def dependencies_path_for(output: Path | str) -> Path:
    output_name = _resolve(output).name
    return REPO_ROOT / ".extraction" / "artifact-provenance" / f"{output_name}.deps.json"


def request_for_resume() -> CompileRequest:
    output = REPO_ROOT / "will_cygan_resume.pdf"
    return CompileRequest(
        source=REPO_ROOT / "will_cygan_resume.typ",
        output=output,
        dependencies_path=dependencies_path_for(output),
        provenance_path=provenance_path_for(output),
    )


def request_for_golden() -> CompileRequest:
    output = REPO_ROOT / "tests/fixtures/golden-resume/golden-resume.pdf"
    return CompileRequest(
        source=REPO_ROOT / "tests/fixtures/golden-resume/golden-resume.typ",
        output=output,
        dependencies_path=dependencies_path_for(output),
        provenance_path=provenance_path_for(output),
    )


def compile_command(request: CompileRequest, *, watch: bool = False) -> list[str]:
    """Build the only supported Typst invocation for repository artifacts."""
    mode = "watch" if watch else "compile"
    command = [
        "typst",
        mode,
        "--root",
        TYPST_ROOT_ARGUMENT,
        "--font-path",
        str(FONT_DIRECTORY),
    ]
    if request.purpose is ArtifactPurpose.RESUME:
        command.extend(["--pdf-standard", PDF_STANDARD])
    for key, value in sorted(request.string_inputs.items()):
        command.extend(["--input", f"{key}={value}"])
    for key, path in sorted(request.file_inputs.items()):
        command.extend(["--input", f"{key}=/{_relative_to_root(path)}"])
    if request.dependencies_path is not None:
        command.extend(["--deps", _relative_to_root(request.dependencies_path)])
    command.extend([_relative_to_root(request.source), _relative_to_root(request.output)])
    return command


def pinned_font_assets() -> list[Path]:
    fonts = sorted((REPO_ROOT / FONT_DIRECTORY).glob("*.ttf"))
    if not fonts:
        raise RuntimeError(f"pinned font assets are missing beneath {FONT_DIRECTORY}")
    return fonts


def _dependency_record(path: Path, kind: str) -> dict[str, object]:
    stat = path.stat()
    return {
        "path": _relative_to_root(path),
        "kind": kind,
        "sha256": _sha256(path),
        "mtime_ns": stat.st_mtime_ns,
    }


def _load_typst_dependencies(path: Path) -> list[Path]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    raw_inputs = payload.get("inputs")
    if not isinstance(raw_inputs, list) or not all(isinstance(item, str) for item in raw_inputs):
        raise ValueError(f"invalid Typst dependency evidence: {path}")
    return [_resolve(REPO_ROOT / item.lstrip("/")) for item in raw_inputs]


def build_provenance(request: CompileRequest) -> dict[str, object]:
    """Create a serializable graph from Typst's transitive evidence plus fonts."""
    if request.dependencies_path is None or not request.dependencies_path.is_file():
        raise FileNotFoundError("one-shot compilation did not produce Typst dependency evidence")

    dependency_paths = _load_typst_dependencies(request.dependencies_path)
    dependency_paths.extend(request.file_inputs.values())
    dependency_paths.append(request.source)
    deduplicated = {path.resolve() for path in dependency_paths}
    missing = sorted(path for path in deduplicated if not path.is_file())
    if missing:
        raise FileNotFoundError(
            "recorded Typst dependency does not exist: " + ", ".join(map(str, missing))
        )

    return {
        "schema_version": PROVENANCE_SCHEMA_VERSION,
        "purpose": request.purpose,
        "source": _relative_to_root(request.source),
        "output": _relative_to_root(request.output),
        "inputs": {
            key: _relative_to_root(path) for key, path in sorted(request.file_inputs.items())
        },
        "string_inputs": dict(sorted(request.string_inputs.items())),
        "compile_command": compile_command(request),
        "typst_dependencies": [
            _dependency_record(path, "typst-input")
            for path in sorted(deduplicated, key=_relative_to_root)
        ],
        "font_assets": [_dependency_record(path, "pinned-font") for path in pinned_font_assets()],
    }


def write_provenance(request: CompileRequest) -> Path:
    if request.provenance_path is None:
        raise ValueError("compile request does not specify a provenance path")
    request.provenance_path.parent.mkdir(parents=True, exist_ok=True)
    request.provenance_path.write_text(
        json.dumps(build_provenance(request), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return request.provenance_path


def compile_artifact(
    request: CompileRequest, *, cwd: Path = REPO_ROOT, capture_output: bool = False
) -> subprocess.CompletedProcess[str]:
    """Compile once and write provenance only for a successful build."""
    request.output.parent.mkdir(parents=True, exist_ok=True)
    if request.dependencies_path is not None:
        request.dependencies_path.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        compile_command(request),
        cwd=cwd,
        check=False,
        text=True,
        capture_output=capture_output,
    )
    if result.returncode == 0 and request.provenance_path is not None:
        write_provenance(request)
    return result


def watch_artifact(request: CompileRequest, *, cwd: Path = REPO_ROOT) -> int:
    """Run Typst watch with the same policy; watch output is not accepted provenance."""
    return subprocess.run(compile_command(request, watch=True), cwd=cwd, check=False).returncode


def load_provenance(path: Path | str) -> dict[str, object]:
    return json.loads(_resolve(path).read_text(encoding="utf-8"))


def evaluate_freshness(
    output: Path | str,
    provenance: Mapping[str, object],
    *,
    source: Path | str | None = None,
) -> Freshness:
    """Fail closed when any transitive input or pinned font changed after build."""
    artifact = _resolve(output)
    if not artifact.is_file():
        return Freshness(False, ("artifact output is missing",), (), ())
    if provenance.get("schema_version") != PROVENANCE_SCHEMA_VERSION:
        return Freshness(False, ("provenance schema is unsupported",), (), ())
    if provenance.get("output") != _relative_to_root(artifact):
        return Freshness(False, ("provenance was recorded for another output",), (), ())
    if source is not None and provenance.get("source") != _relative_to_root(source):
        return Freshness(False, ("provenance was recorded for another source",), (), ())

    stale: list[str] = []
    missing: list[str] = []
    changed: list[str] = []
    artifact_mtime = artifact.stat().st_mtime_ns
    typst_dependencies = provenance.get("typst_dependencies")
    font_assets = provenance.get("font_assets")
    if not isinstance(typst_dependencies, list) or not isinstance(font_assets, list):
        return Freshness(False, ("provenance dependency records are invalid",), (), ())
    records = [*typst_dependencies, *font_assets]
    if not records:
        return Freshness(False, ("provenance records no dependencies",), (), ())
    for record in records:
        if not isinstance(record, dict) or not isinstance(record.get("path"), str):
            return Freshness(False, ("provenance contains an invalid dependency record",), (), ())
        relative_path = record["path"]
        try:
            path = _resolve(REPO_ROOT / relative_path)
            _relative_to_root(path)
        except ValueError:
            return Freshness(
                False,
                ("provenance references a path outside the repository",),
                (),
                (),
            )
        if not path.is_file():
            missing.append(relative_path)
            continue
        if path.stat().st_mtime_ns > artifact_mtime:
            stale.append(relative_path)
        expected_hash = record.get("sha256")
        if isinstance(expected_hash, str) and _sha256(path) != expected_hash:
            changed.append(relative_path)
    return Freshness(
        not stale and not missing and not changed,
        tuple(sorted(stale)),
        tuple(sorted(missing)),
        tuple(sorted(changed)),
    )


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile resume PDFs with recorded provenance.")
    parser.add_argument("target", choices=("resume", "golden"))
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    request = request_for_resume() if args.target == "resume" else request_for_golden()
    result = compile_artifact(request)
    if result.returncode == 0:
        print(f"Provenance: {request.provenance_path}")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
