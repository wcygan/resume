from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / ".agents" / "skills"

MARKDOWN_LINK = re.compile(r"]\(([^)]+\.md(?:#[^)]+)?)\)")
FRONTMATTER = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)


def skill_files() -> list[Path]:
    return sorted(SKILLS_ROOT.glob("*/SKILL.md"))


def frontmatter_value(body: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", body, re.MULTILINE)
    if match is None:
        return None
    return match.group(1).strip().strip('"')


def test_expected_project_local_skills_exist() -> None:
    names = {path.parent.name for path in skill_files()}

    assert {"resume-review", "resume-parsability"} <= names


def test_every_project_skill_has_matching_name_and_description() -> None:
    for path in skill_files():
        text = path.read_text()
        match = FRONTMATTER.match(text)

        assert match is not None, f"{path} is missing YAML frontmatter"
        body = match.group("body")
        assert frontmatter_value(body, "name") == path.parent.name
        assert frontmatter_value(body, "description")


def test_local_markdown_references_resolve() -> None:
    missing: list[str] = []

    for path in SKILLS_ROOT.rglob("*.md"):
        for target in MARKDOWN_LINK.findall(path.read_text()):
            target_path = target.split("#", 1)[0]
            if "://" in target_path:
                continue
            resolved = (path.parent / target_path).resolve()
            if not resolved.exists():
                missing.append(f"{path.relative_to(REPO_ROOT)} -> {target_path}")

    assert not missing, "Missing skill references:\n" + "\n".join(missing)


def test_resume_skill_trigger_boundaries_are_explicit() -> None:
    review = (SKILLS_ROOT / "resume-review" / "SKILL.md").read_text()
    parsability = (SKILLS_ROOT / "resume-parsability" / "SKILL.md").read_text()

    assert "Use resume-parsability instead" in review
    assert "Use the project-local `resume-review` skill instead" in parsability
    assert "Never invent facts" in review
    assert "never equates extractor agreement" in parsability


def test_active_guidance_has_no_legacy_claude_workflow_references() -> None:
    active_files = [
        REPO_ROOT / "AGENTS.md",
        REPO_ROOT / "scripts" / "extraction_check.py",
        REPO_ROOT / "work-experience" / "RELEVANCE.md",
        SKILLS_ROOT / "resume-review" / "SKILL.md",
        SKILLS_ROOT / "resume-parsability" / "references" / "08-project-workflow.md",
    ]
    banned = (".claude", "resume-panel", "resume-debate", "resume-tailor-panel")

    for path in active_files:
        text = path.read_text()
        for token in banned:
            assert token not in text, f"{token!r} remains in {path}"


def test_legacy_claude_configuration_is_absent() -> None:
    assert not (REPO_ROOT / ".claude").exists()
    assert not (REPO_ROOT / "CLAUDE.md").exists()


def test_review_skill_omits_unsupported_exact_statistics() -> None:
    text = "\n".join(
        path.read_text()
        for path in (SKILLS_ROOT / "resume-review").rglob("*.md")
    ).lower()

    for token in ("10.2x", "99.7%", "98.4%"):
        assert token not in text
