"""Evaluate the Golden Resume behind one repository-owned interface.

The direct Golden command and the stress matrix are adapters at this module's
seam.  Evaluation policy, evidence paths, report construction, and the
structured result remain local to this implementation.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import platform
import re
import shutil
import sys
import unicodedata
import xml.etree.ElementTree as element_tree
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from resume_tools import artifact as artifact_tools
from resume_tools import pdf_evidence

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
GOLDEN_FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "golden-resume"
DEFAULT_PDF = GOLDEN_FIXTURE_ROOT / "golden-resume.pdf"
DEFAULT_SOURCE = GOLDEN_FIXTURE_ROOT / "golden-resume.typ"
DEFAULT_ORACLE = GOLDEN_FIXTURE_ROOT / "golden-resume-oracle.json"

REQUIRED_TOOLS = (
    "typst",
    "uv",
    "locale",
)

REQUIRED_PDF_TOOLS = (
    "pdfinfo",
    "pdffonts",
    "pdfimages",
    "pdftotext",
    "pdftohtml",
    "pdftoppm",
    "qpdf",
)


class GoldenEvaluationError(RuntimeError):
    """The Golden artifact could not be evaluated through its reviewed policy."""


@dataclass(frozen=True)
class EvaluationRequest:
    """Inputs for one Golden evaluation and its durable evidence directory."""

    pdf: pathlib.Path = DEFAULT_PDF
    source: pathlib.Path = DEFAULT_SOURCE
    provenance: pathlib.Path | None = None
    oracle: pathlib.Path = DEFAULT_ORACLE
    output_dir: pathlib.Path | None = None


@dataclass(frozen=True)
class EvaluationResult:
    """Caller-facing outcome without exposing the report-file schema."""

    automated_status: str
    gates: Mapping[str, bool]
    artifact_sha256: str
    page_count: int
    minimum_clearance_px: float | None
    stacked_rows: int
    render_paths: tuple[pathlib.Path, ...]
    evidence_directory: pathlib.Path
    report_json: pathlib.Path
    report_markdown: pathlib.Path

    @property
    def ok(self) -> bool:
        return self.automated_status == "Pass"

    @property
    def returncode(self) -> int:
        return 0 if self.ok else 1


def _canonical(text: str) -> str:
    """Apply the only allowed diagnostic normalization: NFC and whitespace collapse."""
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", text)).strip()


def _run(command: list[str], cwd: pathlib.Path) -> pdf_evidence.ProcessResult:
    return pdf_evidence.run_process(command, cwd=cwd, check=False)


def _require_tools() -> None:
    missing = [tool for tool in REQUIRED_TOOLS if shutil.which(tool) is None]
    try:
        pdf_evidence.require_tools(
            REQUIRED_PDF_TOOLS, require_tika=True, which=shutil.which
        )
    except pdf_evidence.ToolUnavailableError as error:
        missing.extend(str(error).removeprefix("required tools are unavailable: ").split(", "))
    if missing:
        raise GoldenEvaluationError(
            f"required tools are unavailable: {', '.join(missing)}"
        )


def _tika_command(*arguments: str) -> list[str]:
    """Use a local Tika executable or CI's explicitly pinned application JAR."""
    command = pdf_evidence.tika_command(*arguments, which=shutil.which)
    if command is not None:
        return command
    raise GoldenEvaluationError(
        "Tika requires either the tika executable or TIKA_JAR with java"
    )


def _create_output_dir(requested: pathlib.Path | None) -> pathlib.Path:
    if requested is None:
        stamp = dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%S.%fZ")
        requested = REPO_ROOT / ".extraction" / "golden-resume" / stamp
    output = requested.expanduser().resolve()
    output.mkdir(parents=True, exist_ok=False)
    return output


def _command_version(command: list[str]) -> str:
    return pdf_evidence.command_version(command, cwd=REPO_ROOT)


def _decoded_xml_text(path: pathlib.Path) -> str:
    root = element_tree.parse(path).getroot()
    return "\n".join(text for text in root.itertext())


def _split_tika_visible_body(
    text: str, expected_uris: list[str]
) -> tuple[str, list[str], bool]:
    """Separate Tika's visible body from its exact URI annotation block.

    Tika emits link annotation destinations after the page containing them.
    That block is terminal for a one-page resume but can precede later pages.
    Keep the raw file unchanged, evaluate visible field counts without the one
    exact block, and validate the annotations independently.
    """
    if not expected_uris:
        return text, [], True
    lines = text.splitlines(keepends=True)
    nonempty_lines = [
        (index, line.strip()) for index, line in enumerate(lines) if line.strip()
    ]
    if len(nonempty_lines) < len(expected_uris):
        return text, [], False
    matches: list[list[tuple[int, str]]] = []
    block_size = len(expected_uris)
    for start in range(len(nonempty_lines) - block_size + 1):
        candidate = nonempty_lines[start : start + block_size]
        if [line for _, line in candidate] == expected_uris:
            matches.append(candidate)
    if len(matches) != 1:
        observed = [line for _, line in nonempty_lines[-block_size:]]
        return text, observed, False

    annotation_lines = matches[0]
    excluded = {index for index, _ in annotation_lines}
    visible_body = "".join(
        line for index, line in enumerate(lines) if index not in excluded
    )
    return visible_body, [line for _, line in annotation_lines], True


def _forbidden_codepoints(text: str) -> list[str]:
    forbidden: set[int] = set()
    for character in text:
        codepoint = ord(character)
        if (
            character in {"\ufffd", "\u00ad", "\u200b", "\u200c", "\u200d", "\ufeff"}
            or 0xE000 <= codepoint <= 0xF8FF
        ):
            forbidden.add(codepoint)
    return [f"U+{codepoint:04X}" for codepoint in sorted(forbidden)]


def _ordered_once(
    text: str, fields: list[str]
) -> tuple[bool, dict[str, int], dict[str, int]]:
    counts = {field: text.count(field) for field in fields}
    positions = {field: text.find(field) for field in fields}
    ordered_positions = list(positions.values())
    passes = (
        all(count == 1 for count in counts.values())
        and all(position >= 0 for position in ordered_positions)
        and ordered_positions == sorted(ordered_positions)
    )
    return passes, counts, positions


def _association_results(
    text: str, windows: list[dict[str, object]]
) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for window in windows:
        start_token = str(window["start"])
        boundary_token = window["boundary"]
        fields = [str(field) for field in window["fields"]]
        start = text.find(start_token)
        if boundary_token is None:
            end = len(text)
            boundary_found = True
        else:
            end = text.find(str(boundary_token), start + len(start_token)) if start >= 0 else -1
            boundary_found = end >= 0
        segment = text[start:end] if start >= 0 and boundary_found else ""
        passes, counts, positions = _ordered_once(segment, fields)
        results.append(
            {
                "label": window["label"],
                "boundary": boundary_token,
                "boundary_found": boundary_found,
                "field_counts": counts,
                "field_positions": positions,
                "passes": start >= 0 and boundary_found and passes,
            }
        )
    return results


def _work_authorization_result(
    text: str, contract: dict[str, object]
) -> dict[str, object]:
    """Verify the exact eligibility statement and its intended header window."""
    statement = str(contract["statement"])
    after_token = str(contract["after"])
    before_token = str(contract["before"])

    statement_count = text.count(statement)
    after_count = text.count(after_token)
    before_count = text.count(before_token)
    statement_position = text.find(statement)
    after_position = text.find(after_token)
    before_position = text.find(before_token)

    exact_once = statement_count == 1
    ordered_window = (
        after_count == 1
        and before_count == 1
        and after_position >= 0
        and statement_position > after_position
        and before_position > statement_position
    )
    return {
        "statement": statement,
        "after": after_token,
        "before": before_token,
        "statement_count": statement_count,
        "after_count": after_count,
        "before_count": before_count,
        "statement_position": statement_position,
        "after_position": after_position,
        "before_position": before_position,
        "exact_once": exact_once,
        "ordered_window": ordered_window,
        "passes": exact_once and ordered_window,
    }


def _evaluate_text_view(text: str, oracle: dict[str, object]) -> dict[str, object]:
    required_once = [str(field) for field in oracle["required_once"]]
    required_order = [str(field) for field in oracle["required_order"]]
    counts = {field: text.count(field) for field in required_once}
    positions = {field: text.find(field) for field in required_order}
    ordered_positions = list(positions.values())
    associations = _association_results(text, oracle["association_windows"])
    forbidden = _forbidden_codepoints(text)
    required_once_pass = all(count == 1 for count in counts.values())
    required_order_pass = (
        all(position >= 0 for position in ordered_positions)
        and ordered_positions == sorted(ordered_positions)
    )
    passes = (
        bool(text.strip())
        and required_once_pass
        and required_order_pass
        and all(result["passes"] for result in associations)
        and not forbidden
    )
    return {
        "passes": passes,
        "nonempty": bool(text.strip()),
        "required_once_pass": required_once_pass,
        "required_order_pass": required_order_pass,
        "field_counts": counts,
        "field_positions": positions,
        "associations": associations,
        "forbidden_codepoints": forbidden,
    }


def _parse_pdfinfo(path: pathlib.Path) -> dict[str, str | None]:
    return pdf_evidence.parse_pdfinfo(path.read_text(encoding="utf-8"))


def _parse_fonts(path: pathlib.Path) -> list[dict[str, str]]:
    return [
        {
            "raw": font.raw,
            "embedded": font.embedded,
            "subset": font.subset,
            "unicode": font.unicode,
        }
        for font in pdf_evidence.parse_fonts(path.read_text(encoding="utf-8"))
    ]


def _count_images(path: pathlib.Path) -> int:
    return pdf_evidence.count_images(path.read_text(encoding="utf-8"))


def _qdf_audit(path: pathlib.Path, oracle: dict[str, object]) -> dict[str, object]:
    text = path.read_bytes().decode("latin-1", errors="replace")
    evidence = pdf_evidence.parse_qdf(text, oracle["minimum_structure_counts"])
    expected_minimums = {
        str(tag): int(count)
        for tag, count in oracle["minimum_structure_counts"].items()
    }
    expected_uris = [str(uri) for uri in oracle["links"]]
    return {
        "has_struct_tree_root": evidence.has_struct_tree_root,
        "has_mark_info": evidence.has_mark_info,
        "structure_counts": evidence.structure_counts,
        "structure_minimums_pass": all(
            evidence.structure_counts[tag] >= minimum
            for tag, minimum in expected_minimums.items()
        ),
        "uris": list(evidence.uris),
        "exact_uri_multiset": sorted(evidence.uris) == sorted(expected_uris),
    }


def _xml_nodes(path: pathlib.Path) -> list[dict[str, object]]:
    root = element_tree.parse(path).getroot()
    nodes: list[dict[str, object]] = []
    for node in root.iter("text"):
        nodes.append(
            {
                "text": _canonical("".join(node.itertext())),
                "top": float(node.attrib["top"]),
                "left": float(node.attrib["left"]),
                "width": float(node.attrib["width"]),
            }
        )
    return nodes


def _geometry_audit(path: pathlib.Path, oracle: dict[str, object]) -> dict[str, object]:
    root = element_tree.parse(path).getroot()
    pages = list(root.iter("page"))
    page_widths = {float(page.attrib["width"]) for page in pages}
    geometry_box = oracle["geometry_content_box"]
    page_width_points = float(geometry_box["page_width_points"])
    xml_page_width = next(iter(page_widths)) if len(page_widths) == 1 else 0.0
    coordinate_scale = xml_page_width / page_width_points if page_width_points else 0.0
    content_left = float(geometry_box["left_margin_points"]) * coordinate_scale
    content_right = xml_page_width - (
        float(geometry_box["right_margin_points"]) * coordinate_scale
    )
    tolerance = float(geometry_box["tolerance_px"])
    nodes = _xml_nodes(path)

    def find_unique(field: str) -> dict[str, object] | None:
        matches = [node for node in nodes if node["text"] == field]
        return matches[0] if len(matches) == 1 else None

    rows: list[dict[str, object]] = []
    right_edges: list[float] = []
    for row in oracle["geometry_rows"]:
        left_nodes = [find_unique(str(field)) for field in row["left_fields"]]
        right_node = find_unique(str(row["right_field"]))
        nodes_found = all(node is not None for node in left_nodes) and right_node is not None
        if nodes_found:
            concrete_left = [node for node in left_nodes if node is not None]
            concrete_right = right_node
            left_tops = [float(node["top"]) for node in concrete_left]
            right_top = float(concrete_right["top"])
            left_fields_same_baseline = max(left_tops) - min(left_tops) <= 1.0
            vertical_offset = right_top - max(left_tops)
            same_baseline = left_fields_same_baseline and abs(vertical_offset) <= 1.0
            stacked_right = left_fields_same_baseline and 1.0 < vertical_offset <= 24.0
            left_edge = max(float(node["left"]) + float(node["width"]) for node in concrete_left)
            clearance = (
                float(concrete_right["left"]) - left_edge if same_baseline else None
            )
            right_edge = float(concrete_right["left"]) + float(concrete_right["width"])
            left_boundary = min(float(node["left"]) for node in concrete_left)
            left_within_right_edge = left_edge <= right_edge + 1.0
            left_within_content = all(
                float(node["left"]) >= content_left - tolerance
                and float(node["left"]) + float(node["width"])
                <= content_right + tolerance
                for node in concrete_left
            )
            right_within_content = (
                float(concrete_right["left"]) >= content_left - tolerance
                and right_edge <= content_right + tolerance
            )
            right_aligned_to_content = abs(right_edge - content_right) <= tolerance
            positive_clearance = clearance is not None and clearance > 0
            right_edges.append(right_edge)
            if same_baseline:
                layout = "same-row"
            elif stacked_right:
                layout = "stacked-right"
            else:
                layout = "invalid"
        else:
            left_fields_same_baseline = False
            same_baseline = False
            stacked_right = False
            vertical_offset = None
            clearance = None
            right_edge = None
            left_within_right_edge = False
            left_within_content = False
            right_within_content = False
            right_aligned_to_content = False
            positive_clearance = False
            layout = "missing"
        rows.append(
            {
                "label": row["label"],
                "nodes_found_once": nodes_found,
                "left_fields_same_baseline": left_fields_same_baseline,
                "same_baseline": same_baseline,
                "stacked_right": stacked_right,
                "layout": layout,
                "vertical_offset_px": vertical_offset,
                "clearance_px": clearance,
                "positive_clearance": positive_clearance,
                "right_edge_px": right_edge,
                "left_within_right_edge": left_within_right_edge,
                "left_within_content": left_within_content,
                "right_within_content": right_within_content,
                "right_aligned_to_content": right_aligned_to_content,
                "passes": (
                    nodes_found
                    and left_fields_same_baseline
                    and left_within_right_edge
                    and left_within_content
                    and right_within_content
                    and right_aligned_to_content
                    and (stacked_right or (same_baseline and positive_clearance))
                ),
            }
        )
    common_right_edge = bool(right_edges) and max(right_edges) - min(right_edges) <= 1.0
    return {
        "content_box": {
            "page_width_px": xml_page_width,
            "left_px": content_left,
            "right_px": content_right,
            "tolerance_px": tolerance,
            "single_page_width": len(page_widths) == 1 and xml_page_width > 0,
        },
        "rows": rows,
        "common_right_edge": common_right_edge,
        "passes": (
            len(page_widths) == 1
            and xml_page_width > 0
            and all(row["passes"] for row in rows)
            and common_right_edge
        ),
    }


def _markdown_report(report: dict[str, object]) -> str:
    lines = [
        "# Golden Resume Parsability Report",
        "",
        f"- Automated local status: **{report['automated_status']}**",
        f"- Artifact: `{report['artifact']['path']}`",
        f"- SHA-256: `{report['artifact']['sha256']}`",
        f"- Evidence: `{report['evidence_directory']}`",
        "- Visual inspection: **Needs human review** of every generated page render",
        "- External ATS / Greenhouse UAT: **Untested**",
        "",
        "## Text and association views",
        "",
    ]
    for name, result in report["text_views"].items():
        lines.append(f"- {name}: {'Pass' if result['passes'] else 'Fail'}")
    work_authorization = report["work_authorization"]
    lines.extend(
        [
            "",
            "## Work authorization statement",
            "",
            (
                "- exact text and LinkedIn-to-Profile placement: "
                f"{'Pass' if work_authorization['passes'] else 'Fail'}"
            ),
        ]
    )
    for name, result in work_authorization["views"].items():
        lines.append(
            f"- {name}: {'Pass' if result['passes'] else 'Fail'} "
            f"(count={result['statement_count']})"
        )
    lines.extend(
        [
            "",
            "## PDF and geometry gates",
            "",
        ]
    )
    for name, passed in report["gates"].items():
        lines.append(f"- {name}: {'Pass' if passed else 'Fail'}")
    lines.extend(
        [
            "",
            "This is bounded local evidence from the recorded tools. It does not certify",
            "commercial ATS mapping, screen-reader behavior, recruiter outcomes, or callbacks.",
            "",
        ]
    )
    return "\n".join(lines)


def _evaluate(request: EvaluationRequest) -> EvaluationResult:
    _require_tools()

    pdf = request.pdf.expanduser().resolve()
    source = request.source.expanduser().resolve()
    oracle_path = request.oracle.expanduser().resolve()
    provenance_path = (
        request.provenance.expanduser().resolve()
        if request.provenance is not None
        else artifact_tools.provenance_path_for(pdf)
    )
    for required in (pdf, source, oracle_path, provenance_path):
        if not required.is_file():
            raise GoldenEvaluationError(f"required file does not exist: {required}")

    oracle = json.loads(oracle_path.read_text(encoding="utf-8"))
    output = _create_output_dir(request.output_dir)
    artifact = output / "golden-resume.pdf"
    shutil.copy2(pdf, artifact)

    versions = {
        "typst": _command_version(["typst", "--version"]),
        "tika": _command_version(_tika_command("--version")),
        "poppler": _command_version(["pdfinfo", "-v"]),
        "qpdf": _command_version(["qpdf", "--version"]),
        "uv": _command_version(["uv", "--version"]),
        "python": sys.version.splitlines()[0],
        "platform": platform.platform(),
        "locale": (_run(["locale"], REPO_ROOT).stdout).strip(),
    }
    (output / "tool-versions.json").write_text(
        json.dumps(versions, indent=2) + "\n", encoding="utf-8"
    )

    evidence_results = pdf_evidence.capture_pdf_evidence(
        artifact,
        output,
        cwd=REPO_ROOT,
        include_xml=True,
        include_qdf=True,
        render_dpi=144,
    )
    command_results = {
        name: result.returncode for name, result in evidence_results.items()
    }
    qpdf_check = evidence_results["qpdf_check"]
    early_pdfinfo = _parse_pdfinfo(output / "pdfinfo.txt")
    page_count = int(early_pdfinfo["Pages"] or 0)

    if any(returncode != 0 for returncode in command_results.values()):
        failures = [name for name, code in command_results.items() if code != 0]
        raise GoldenEvaluationError(
            f"evidence command failed: {', '.join(failures)}; see {output}"
        )

    tika_text = (output / "tika.txt").read_text(encoding="utf-8")
    expected_uris = [str(uri) for uri in oracle["links"]]
    (
        tika_visible_body,
        tika_uri_annotation_block,
        tika_uri_annotation_block_exact,
    ) = _split_tika_visible_body(tika_text, expected_uris)
    raw_views = {
        "poppler_plain_raw": (output / "poppler-plain.txt").read_text(encoding="utf-8"),
        "poppler_layout_raw": (output / "poppler-layout.txt").read_text(encoding="utf-8"),
        "tika_raw": tika_visible_body,
        "poppler_xml_text_raw": _decoded_xml_text(output / "poppler.xml"),
    }
    view_texts: dict[str, str] = {}
    text_views: dict[str, dict[str, object]] = {}
    for name, text in raw_views.items():
        canonical_name = name.replace("_raw", "_canonical")
        canonical_text = _canonical(text)
        view_texts[name] = text
        view_texts[canonical_name] = canonical_text
        text_views[name] = _evaluate_text_view(text, oracle)
        text_views[canonical_name] = _evaluate_text_view(canonical_text, oracle)

    work_authorization_views = {
        name: _work_authorization_result(text, oracle["work_authorization"])
        for name, text in view_texts.items()
    }
    work_authorization_pass = all(
        result["passes"] for result in work_authorization_views.values()
    )

    pdfinfo = early_pdfinfo
    expected_artifact = oracle["artifact"]
    artifact_contract = (
        pdfinfo["Pages"] == expected_artifact["pages"]
        and pdfinfo["Page size"] == expected_artifact["page_size"]
        and pdfinfo["Page rot"] == expected_artifact["rotation"]
        and pdfinfo["Tagged"] == expected_artifact["tagged"]
    )
    fonts = _parse_fonts(output / "pdffonts.txt")
    fonts_pass = bool(fonts) and all(
        font["embedded"] == font["subset"] == font["unicode"] == "yes"
        for font in fonts
    )
    image_count = _count_images(output / "pdfimages.txt")
    qdf = _qdf_audit(output / "qdf.pdf", oracle)
    geometry = _geometry_audit(output / "poppler.xml", oracle)
    qpdf_clean = (
        qpdf_check.returncode == 0
        and "No syntax or stream encoding errors found" in (output / "qpdf-check.txt").read_text()
    )
    provenance = artifact_tools.load_provenance(provenance_path)
    freshness = artifact_tools.evaluate_freshness(pdf, provenance, source=source)
    font_asset_hashes = {
        relative_path: hashlib.sha256((REPO_ROOT / relative_path).read_bytes()).hexdigest()
        for relative_path in oracle["font_assets"]
        if (REPO_ROOT / relative_path).is_file()
    }
    font_assets_pass = font_asset_hashes == oracle["font_assets"]

    render_paths = sorted(output.glob("render-144dpi*.png"))
    gates = {
        "source_pdf_current": freshness.is_fresh,
        "pinned_font_assets": font_assets_pass,
        "all_text_views": all(result["passes"] for result in text_views.values()),
        "work_authorization_statement": work_authorization_pass,
        "tika_exact_uri_annotation_block": tika_uri_annotation_block_exact,
        "tika_full_raw_codepoints": not _forbidden_codepoints(tika_text),
        "artifact_contract": artifact_contract,
        "qpdf_integrity": qpdf_clean,
        "embedded_subset_unicode_fonts": fonts_pass,
        "image_count": image_count <= int(expected_artifact["maximum_images"]),
        "semantic_structure": (
            qdf["has_struct_tree_root"]
            and qdf["has_mark_info"]
            and qdf["structure_minimums_pass"]
        ),
        "exact_links": qdf["exact_uri_multiset"],
        "right_metadata_geometry": geometry["passes"],
        "render_generated": len(render_paths) == page_count and page_count > 0,
    }
    automated_status = "Pass" if all(gates.values()) else "Fail"

    artifact_sha256 = hashlib.sha256(artifact.read_bytes()).hexdigest()
    report = {
        "automated_status": automated_status,
        "artifact": {
            "path": str(pdf),
            "source": str(source),
            "sha256": artifact_sha256,
            "source_current": freshness.is_fresh,
            "provenance": str(provenance_path),
            "freshness": {
                "stale": list(freshness.stale),
                "missing": list(freshness.missing),
                "changed": list(freshness.changed),
            },
            "pdfinfo": pdfinfo,
        },
        "oracle": str(oracle_path),
        "evidence_directory": str(output),
        "tool_versions": versions,
        "canonicalization": "Unicode NFC plus whitespace collapse only",
        "text_views": text_views,
        "work_authorization": {
            "contract": oracle["work_authorization"],
            "views": work_authorization_views,
            "passes": work_authorization_pass,
        },
        "tika": {
            "raw_output": str(output / "tika.txt"),
            "field_evaluation_scope": "visible body with one exact URI annotation block removed",
            "uri_annotation_block": tika_uri_annotation_block,
            "exact_uri_annotation_block": tika_uri_annotation_block_exact,
            "full_raw_forbidden_codepoints": _forbidden_codepoints(tika_text),
        },
        "pdf": {
            "font_asset_hashes": font_asset_hashes,
            "fonts": fonts,
            "image_count": image_count,
            "qpdf_clean": qpdf_clean,
            "qdf": qdf,
            "geometry": geometry,
            "renders": [str(path) for path in render_paths],
        },
        "gates": gates,
        "visual_inspection": "Needs human review of every generated page render",
        "external_ats_uat": "Untested",
    }
    report_json = output / "report.json"
    report_markdown = output / "report.md"
    report_json.write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    report_markdown.write_text(_markdown_report(report), encoding="utf-8")

    geometry_rows = geometry["rows"]
    clearances = [
        float(row["clearance_px"])
        for row in geometry_rows
        if row["clearance_px"] is not None
    ]
    return EvaluationResult(
        automated_status=automated_status,
        gates=MappingProxyType(dict(gates)),
        artifact_sha256=artifact_sha256,
        page_count=page_count,
        minimum_clearance_px=min(clearances) if clearances else None,
        stacked_rows=sum(row["layout"] == "stacked-right" for row in geometry_rows),
        render_paths=tuple(render_paths),
        evidence_directory=output,
        report_json=report_json,
        report_markdown=report_markdown,
    )


def evaluate(request: EvaluationRequest) -> EvaluationResult:
    """Evaluate one Golden artifact and return its structured outcome.

    All expected input, filesystem, and PDF-tool failures cross the seam as
    :class:`GoldenEvaluationError`.
    """

    try:
        return _evaluate(request)
    except GoldenEvaluationError:
        raise
    except (
        pdf_evidence.PdfEvidenceError,
        OSError,
        ValueError,
        KeyError,
    ) as error:
        raise GoldenEvaluationError(str(error)) from error
