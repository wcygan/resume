"""Canonical facts and independently reviewed extraction rules.

The active resume's expected candidate facts are selected from its JSON data
source.  The TOML fixture deliberately contains only rules for evaluating a
PDF representation; it must not become a second, stale copy of the resume.
"""

from __future__ import annotations

import json
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RESUME_DATA = REPO_ROOT / "will_cygan_resume-data.json"


class ExpectationError(ValueError):
    """A canonical fact or independently reviewed rule is malformed."""


@dataclass(frozen=True)
class CandidateFacts:
    name: str
    email: str
    required_head_facts: tuple[str, ...]


@dataclass(frozen=True)
class JobFacts:
    title: str
    company: str
    date_start: str
    date_end: str


@dataclass(frozen=True)
class EducationFacts:
    title: str
    date: str


@dataclass(frozen=True)
class CanonicalFacts:
    candidate: CandidateFacts
    jobs: tuple[JobFacts, ...]
    project_titles: tuple[str, ...]
    education: EducationFacts
    keywords: tuple[str, ...]


@dataclass(frozen=True)
class ParsabilityRules:
    section_order: tuple[str, ...]
    allowed_date_range_regex: str
    min_bytes: int
    job_block_window_chars: int
    name_head_bytes: int
    contact_glue_window: int
    forbidden_chars: tuple[str, ...]
    flagged_chars: tuple[str, ...]
    allowed_chars: tuple[str, ...]


@dataclass(frozen=True)
class ExtractionExpectations:
    facts: CanonicalFacts
    rules: ParsabilityRules


_CONTENT_TABLES = frozenset({"candidate", "jobs", "projects", "education", "keywords"})


def _mapping(value: object, path: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ExpectationError(f"{path} must be an object")
    return value


def _string(value: object, path: str) -> str:
    if not isinstance(value, str) or not value:
        raise ExpectationError(f"{path} must be a non-empty string")
    return value


def _strings(value: object, path: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise ExpectationError(f"{path} must be a non-empty list of strings")
    return tuple(_string(item, f"{path}[{index}]") for index, item in enumerate(value))


def _integer(value: object, path: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ExpectationError(f"{path} must be a positive integer")
    return value


def _optional_string(value: object, path: str) -> str | None:
    if value is None:
        return None
    return _string(value, path)


def _date_range(value: object, path: str) -> tuple[str, str]:
    dates = _string(value, path)
    start, separator, end = dates.partition(" - ")
    if not separator or not start or not end:
        raise ExpectationError(
            f"{path} must use the canonical 'Month YYYY - Month YYYY or Present' format"
        )
    return start, end


def load_canonical_facts(data_path: Path = DEFAULT_RESUME_DATA) -> CanonicalFacts:
    """Select expected candidate facts from a resume JSON data source.

    This selection knows the content schema, not the Typst renderer or its
    output.  A canonical data edit therefore updates expectation inputs on the
    next check without a paired fixture edit.
    """
    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ExpectationError(f"canonical resume data is missing: {data_path}") from error
    except json.JSONDecodeError as error:
        raise ExpectationError(f"canonical resume data is invalid JSON: {data_path}: {error}") from error

    root = _mapping(data, "resume data")
    contact = _mapping(root.get("contact"), "contact")
    email = _mapping(contact.get("email"), "contact.email")
    required_head_facts = tuple(
        value
        for value in (
            _optional_string(contact.get("location"), "contact.location"),
            _optional_string(
                contact.get("work_authorization"), "contact.work_authorization"
            ),
        )
        if value is not None
    )
    candidate = CandidateFacts(
        name=_string(contact.get("name"), "contact.name"),
        email=_string(email.get("display"), "contact.email.display"),
        required_head_facts=required_head_facts,
    )

    experience = root.get("experience")
    if not isinstance(experience, list) or not experience:
        raise ExpectationError("experience must be a non-empty list")
    jobs: list[JobFacts] = []
    for index, item in enumerate(experience):
        job = _mapping(item, f"experience[{index}]")
        start, end = _date_range(job.get("dates"), f"experience[{index}].dates")
        jobs.append(
            JobFacts(
                title=_string(job.get("role"), f"experience[{index}].role"),
                company=_string(job.get("company"), f"experience[{index}].company"),
                date_start=start,
                date_end=end,
            )
        )

    projects = root.get("projects")
    if not isinstance(projects, list) or not projects:
        raise ExpectationError("projects must be a non-empty list")
    project_titles = tuple(
        _string(_mapping(project, f"projects[{index}]").get("name"), f"projects[{index}].name")
        for index, project in enumerate(projects)
    )

    education_data = _mapping(root.get("education"), "education")
    education = EducationFacts(
        title=_string(education_data.get("institution"), "education.institution"),
        date=_string(education_data.get("graduation"), "education.graduation"),
    )

    skills = root.get("skills")
    if not isinstance(skills, list) or not skills:
        raise ExpectationError("skills must be a non-empty list")
    keywords: list[str] = []
    for index, item in enumerate(skills):
        values = _string(
            _mapping(item, f"skills[{index}]").get("values"), f"skills[{index}].values"
        )
        keywords.extend(value.strip() for value in values.split(",") if value.strip())
    if not keywords:
        raise ExpectationError("skills must contain at least one keyword")

    return CanonicalFacts(
        candidate=candidate,
        jobs=tuple(jobs),
        project_titles=project_titles,
        education=education,
        keywords=tuple(keywords),
    )


def load_parsability_rules(fixtures_path: Path) -> ParsabilityRules:
    """Load reviewed extraction rules that are intentionally independent of content."""
    try:
        fixture_data = tomllib.loads(fixtures_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ExpectationError(f"extraction rules file is missing: {fixtures_path}") from error
    except tomllib.TOMLDecodeError as error:
        raise ExpectationError(f"extraction rules file is invalid TOML: {fixtures_path}: {error}") from error

    copied_content = sorted(_CONTENT_TABLES.intersection(fixture_data))
    if copied_content:
        raise ExpectationError(
            "extraction rules must not copy canonical resume facts; "
            f"remove TOML table(s): {', '.join(copied_content)}"
        )

    sections = _mapping(fixture_data.get("sections"), "sections")
    dates = _mapping(fixture_data.get("dates"), "dates")
    thresholds = _mapping(fixture_data.get("thresholds"), "thresholds")
    mojibake = _mapping(fixture_data.get("mojibake"), "mojibake")
    return ParsabilityRules(
        section_order=_strings(sections.get("expected_order"), "sections.expected_order"),
        allowed_date_range_regex=_string(
            dates.get("allowed_range_regex"), "dates.allowed_range_regex"
        ),
        min_bytes=_integer(thresholds.get("min_bytes"), "thresholds.min_bytes"),
        job_block_window_chars=_integer(
            thresholds.get("job_block_window_chars"),
            "thresholds.job_block_window_chars",
        ),
        name_head_bytes=_integer(thresholds.get("name_head_bytes"), "thresholds.name_head_bytes"),
        contact_glue_window=_integer(
            thresholds.get("contact_glue_window"), "thresholds.contact_glue_window"
        ),
        forbidden_chars=_strings(mojibake.get("forbidden_chars"), "mojibake.forbidden_chars"),
        flagged_chars=_strings(mojibake.get("flagged_chars"), "mojibake.flagged_chars"),
        allowed_chars=_strings(mojibake.get("allowed_chars"), "mojibake.allowed_chars"),
    )


def load_active_expectations(
    fixtures_path: Path,
    data_path: Path = DEFAULT_RESUME_DATA,
) -> ExtractionExpectations:
    """Combine canonical resume facts with separately reviewed parser rules."""
    return ExtractionExpectations(
        facts=load_canonical_facts(data_path),
        rules=load_parsability_rules(fixtures_path),
    )
