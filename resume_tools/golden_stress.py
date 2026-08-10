"""Materialize reviewed semantic Golden Resume stress cases.

The stress manifest deliberately describes candidate-facing intent instead of
the incidental shape of the Golden fixture JSON or the evaluator's oracle.
This module is the sole translation boundary between those two representations.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any, Mapping


class StressSpecificationError(ValueError):
    """A reviewed stress manifest or its frozen baseline is inconsistent."""


@dataclass(frozen=True)
class SemanticMutation:
    """One reviewed change to a named resume field."""

    subject: str
    field: str
    value: str


@dataclass(frozen=True)
class StressCase:
    """A semantic Golden stress case and its reviewed expected outcome."""

    name: str
    description: str
    expectation: str
    mutations: tuple[SemanticMutation, ...]
    expected_failed_gates: tuple[str, ...] = ()


@dataclass(frozen=True)
class StressManifest:
    """Validated stress-manifest data consumed by the matrix dispatcher."""

    baseline: dict[str, Any]
    cases: tuple[StressCase, ...]


_REQUIRED_BASELINE_PATHS = ("source", "data", "renderer", "oracle")
_EXPERIENCE_RECORDS = {
    "northstar-experience": 0,
    "harbor-experience": 1,
    "cedar-experience": 2,
}
_PROJECT_RECORDS = {"kubernetes-project": 0}
_CONTACT_SUBJECTS = {
    "contact-portfolio": "portfolio",
    "contact-github": "github",
    "contact-linkedin": "linkedin",
}
_EXPERIENCE_FIELDS = frozenset(("company", "role", "dates", "location"))
_PROJECT_FIELDS = frozenset(("name", "descriptor", "focus"))
_CONTACT_FIELDS = frozenset(("display", "uri"))


def _mapping(value: object, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise StressSpecificationError(f"{label} must be an object")
    return value


def _keys(value: Mapping[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    if actual != expected:
        raise StressSpecificationError(
            f"{label} keys must be {sorted(expected)}, found {sorted(actual)}"
        )


def _string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise StressSpecificationError(f"{label} must be a non-empty string")
    return value


def _strings(value: object, label: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item for item in value
    ):
        raise StressSpecificationError(f"{label} must be an array of non-empty strings")
    return tuple(value)


def _validate_target(subject: str, field: str, label: str) -> None:
    if subject in _EXPERIENCE_RECORDS and field in _EXPERIENCE_FIELDS:
        return
    if subject in _PROJECT_RECORDS and field in _PROJECT_FIELDS:
        return
    if subject in _CONTACT_SUBJECTS and field in _CONTACT_FIELDS:
        return
    raise StressSpecificationError(f"{label} names unsupported target {subject}.{field}")


def parse_manifest(raw: object) -> StressManifest:
    """Validate the public semantic schema before any case is materialized."""
    document = _mapping(raw, "manifest")
    _keys(document, {"schema_version", "document", "baseline", "cases"}, "manifest")
    if document["schema_version"] != 1:
        raise StressSpecificationError("manifest schema_version must be 1")
    _string(document["document"], "manifest.document")

    baseline = _mapping(document["baseline"], "manifest.baseline")
    _keys(
        baseline,
        {"source", "data", "renderer", "oracle", "sha256"},
        "manifest.baseline",
    )
    for key in _REQUIRED_BASELINE_PATHS:
        _string(baseline[key], f"manifest.baseline.{key}")
    hashes = _mapping(baseline["sha256"], "manifest.baseline.sha256")
    _keys(hashes, set(_REQUIRED_BASELINE_PATHS), "manifest.baseline.sha256")
    for key in _REQUIRED_BASELINE_PATHS:
        digest = _string(hashes[key], f"manifest.baseline.sha256.{key}")
        if len(digest) != 64 or any(
            character not in "0123456789abcdef" for character in digest
        ):
            raise StressSpecificationError(
                f"manifest.baseline.sha256.{key} must be a lowercase SHA-256"
            )

    raw_cases = document["cases"]
    if not isinstance(raw_cases, list) or not raw_cases:
        raise StressSpecificationError("manifest.cases must be a non-empty array")
    cases: list[StressCase] = []
    names: set[str] = set()
    for position, raw_case in enumerate(raw_cases):
        label = f"manifest.cases[{position}]"
        case = _mapping(raw_case, label)
        allowed = {
            "name",
            "description",
            "expectation",
            "mutations",
            "expected_failed_gates",
        }
        if (
            not {"name", "description", "expectation", "mutations"} <= set(case)
            or set(case) - allowed
        ):
            raise StressSpecificationError(f"{label} has unsupported semantic case keys")
        name = _string(case["name"], f"{label}.name")
        if name in names:
            raise StressSpecificationError(f"manifest repeats case name {name!r}")
        names.add(name)
        description = _string(case["description"], f"{label}.description")
        expectation = _string(case["expectation"], f"{label}.expectation")
        if expectation not in {"pass", "fail"}:
            raise StressSpecificationError(f"{label}.expectation must be pass or fail")
        expected_failed_gates = _strings(
            case.get("expected_failed_gates", []), f"{label}.expected_failed_gates"
        )
        if expectation == "pass" and expected_failed_gates:
            raise StressSpecificationError(f"{label} pass cases cannot declare failed gates")
        if expectation == "fail" and not expected_failed_gates:
            raise StressSpecificationError(f"{label} fail cases must declare exact failed gates")

        raw_mutations = case["mutations"]
        if not isinstance(raw_mutations, list):
            raise StressSpecificationError(f"{label}.mutations must be an array")
        mutations: list[SemanticMutation] = []
        targets: set[tuple[str, str]] = set()
        for mutation_position, raw_mutation in enumerate(raw_mutations):
            mutation_label = f"{label}.mutations[{mutation_position}]"
            mutation = _mapping(raw_mutation, mutation_label)
            _keys(mutation, {"subject", "field", "value"}, mutation_label)
            subject = _string(mutation["subject"], f"{mutation_label}.subject")
            field = _string(mutation["field"], f"{mutation_label}.field")
            value = _string(mutation["value"], f"{mutation_label}.value")
            _validate_target(subject, field, mutation_label)
            target = (subject, field)
            if target in targets:
                raise StressSpecificationError(f"{label} repeats semantic target {subject}.{field}")
            targets.add(target)
            mutations.append(SemanticMutation(subject, field, value))
        if name == "baseline" and mutations:
            raise StressSpecificationError("baseline case cannot mutate reviewed inputs")
        if name != "baseline" and not mutations:
            raise StressSpecificationError(f"{label} must declare a semantic mutation")
        cases.append(StressCase(name, description, expectation, tuple(mutations), expected_failed_gates))

    if "baseline" not in names:
        raise StressSpecificationError("manifest must declare a baseline case")
    return StressManifest(copy.deepcopy(dict(baseline)), tuple(cases))


def _experience(data: dict[str, Any], subject: str) -> dict[str, Any]:
    records = data.get("experience")
    if not isinstance(records, list):
        raise StressSpecificationError("baseline data.experience must be an array")
    try:
        record = records[_EXPERIENCE_RECORDS[subject]]
    except IndexError as error:
        raise StressSpecificationError(f"baseline data has no reviewed {subject}") from error
    if not isinstance(record, dict):
        raise StressSpecificationError(f"baseline {subject} must be an object")
    return record


def _project(data: dict[str, Any], subject: str) -> dict[str, Any]:
    records = data.get("projects")
    if not isinstance(records, list):
        raise StressSpecificationError("baseline data.projects must be an array")
    try:
        record = records[_PROJECT_RECORDS[subject]]
    except IndexError as error:
        raise StressSpecificationError(f"baseline data has no reviewed {subject}") from error
    if not isinstance(record, dict):
        raise StressSpecificationError(f"baseline {subject} must be an object")
    return record


def _contact(data: dict[str, Any], subject: str) -> dict[str, Any]:
    contact = data.get("contact")
    if not isinstance(contact, dict):
        raise StressSpecificationError("baseline data.contact must be an object")
    record = contact.get(_CONTACT_SUBJECTS[subject])
    if not isinstance(record, dict):
        raise StressSpecificationError(f"baseline data has no reviewed {subject}")
    return record


def _record_for(data: dict[str, Any], subject: str) -> dict[str, Any]:
    if subject in _EXPERIENCE_RECORDS:
        return _experience(data, subject)
    if subject in _PROJECT_RECORDS:
        return _project(data, subject)
    if subject in _CONTACT_SUBJECTS:
        return _contact(data, subject)
    raise StressSpecificationError(f"unsupported reviewed subject {subject}")


def _replace_once(values: list[Any], before: str, after: str, label: str) -> None:
    matches = [position for position, value in enumerate(values) if value == before]
    if len(matches) != 1:
        raise StressSpecificationError(
            f"reviewed oracle {label} expected {before!r} exactly once, found {len(matches)}"
        )
    values[matches[0]] = after


def _oracle_list(oracle: dict[str, Any], key: str) -> list[Any]:
    values = oracle.get(key)
    if not isinstance(values, list):
        raise StressSpecificationError(f"reviewed oracle {key} must be an array")
    return values


def _oracle_window(oracle: dict[str, Any], label: str) -> dict[str, Any]:
    windows = _oracle_list(oracle, "association_windows")
    matches = [
        window
        for window in windows
        if isinstance(window, dict) and window.get("label") == label
    ]
    if len(matches) != 1:
        raise StressSpecificationError(
            f"reviewed oracle needs exactly one {label!r} association window"
        )
    return matches[0]


def _oracle_row(oracle: dict[str, Any], label: str) -> dict[str, Any]:
    rows = _oracle_list(oracle, "geometry_rows")
    matches = [
        row for row in rows if isinstance(row, dict) and row.get("label") == label
    ]
    if len(matches) != 1:
        raise StressSpecificationError(
            f"reviewed oracle needs exactly one {label!r} geometry row"
        )
    return matches[0]


def _replace_window_field(oracle: dict[str, Any], label: str, before: str, after: str) -> None:
    window = _oracle_window(oracle, label)
    fields = window.get("fields")
    if not isinstance(fields, list):
        raise StressSpecificationError(
            f"reviewed oracle {label!r} fields must be an array"
        )
    _replace_once(fields, before, after, f"{label!r} fields")
    if window.get("start") == before:
        window["start"] = after


def _replace_row_left_field(oracle: dict[str, Any], label: str, before: str, after: str) -> None:
    row = _oracle_row(oracle, label)
    fields = row.get("left_fields")
    if not isinstance(fields, list):
        raise StressSpecificationError(
            f"reviewed oracle {label!r} left_fields must be an array"
        )
    _replace_once(fields, before, after, f"{label!r} left_fields")


def _metadata(dates: str, location: str) -> str:
    return f"Dates: {dates} · Location: {location}"


def _project_focus(focus: str) -> str:
    return f"Focus: {focus}"


def _mutate_experience(
    data: dict[str, Any], oracle: dict[str, Any], mutation: SemanticMutation, before: str
) -> None:
    record = _experience(data, mutation.subject)
    window_label = mutation.subject.replace("-", " ")
    if mutation.field in {"company", "role"}:
        _replace_once(
            _oracle_list(oracle, "required_once"), before, mutation.value, "required_once"
        )
        _replace_once(
            _oracle_list(oracle, "required_order"), before, mutation.value, "required_order"
        )
        _replace_window_field(oracle, window_label, before, mutation.value)
        _replace_row_left_field(oracle, window_label, before, mutation.value)
    else:
        before_display = f"{mutation.field.title()}: {before}"
        after_display = f"{mutation.field.title()}: {mutation.value}"
        _replace_once(
            _oracle_list(oracle, "required_once"),
            before_display,
            after_display,
            "required_once",
        )
        _replace_once(
            _oracle_list(oracle, "required_order"),
            before_display,
            after_display,
            "required_order",
        )
        _replace_window_field(oracle, window_label, before_display, after_display)
        row = _oracle_row(oracle, window_label)
        right_field = row.get("right_field")
        expected_before = _metadata(
            before
            if mutation.field == "dates"
            else _string(record["dates"], f"{mutation.subject}.dates"),
            before
            if mutation.field == "location"
            else _string(record["location"], f"{mutation.subject}.location"),
        )
        expected_after = _metadata(
            mutation.value
            if mutation.field == "dates"
            else _string(record["dates"], f"{mutation.subject}.dates"),
            mutation.value
            if mutation.field == "location"
            else _string(record["location"], f"{mutation.subject}.location"),
        )
        if right_field != expected_before:
            raise StressSpecificationError(
                f"reviewed oracle {window_label!r} right_field expected "
                f"{expected_before!r}, found {right_field!r}"
            )
        row["right_field"] = expected_after


def _mutate_project(
    data: dict[str, Any], oracle: dict[str, Any], mutation: SemanticMutation, before: str
) -> None:
    window_label = mutation.subject.replace("-", " ")
    before_display = _project_focus(before) if mutation.field == "focus" else before
    after_display = (
        _project_focus(mutation.value) if mutation.field == "focus" else mutation.value
    )
    _replace_once(
        _oracle_list(oracle, "required_once"),
        before_display,
        after_display,
        "required_once",
    )
    _replace_once(
        _oracle_list(oracle, "required_order"),
        before_display,
        after_display,
        "required_order",
    )
    _replace_window_field(oracle, window_label, before_display, after_display)
    if mutation.field == "focus":
        row = _oracle_row(oracle, window_label)
        if row.get("right_field") != before_display:
            raise StressSpecificationError(
                f"reviewed oracle {window_label!r} right_field is stale"
            )
        row["right_field"] = after_display
    else:
        _replace_row_left_field(oracle, window_label, before_display, after_display)


def _mutate_contact(
    oracle: dict[str, Any], mutation: SemanticMutation, before: str
) -> None:
    if mutation.field == "display":
        _replace_once(
            _oracle_list(oracle, "required_once"), before, mutation.value, "required_once"
        )
        _replace_once(
            _oracle_list(oracle, "required_order"), before, mutation.value, "required_order"
        )
        if mutation.subject == "contact-linkedin":
            authorization = oracle.get("work_authorization")
            if not isinstance(authorization, dict) or authorization.get("after") != before:
                raise StressSpecificationError("reviewed oracle work authorization order is stale")
            authorization["after"] = mutation.value
    else:
        _replace_once(_oracle_list(oracle, "links"), before, mutation.value, "links")


def materialize_case(
    baseline_data: dict[str, Any], baseline_oracle: dict[str, Any], case: StressCase
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build independent data and oracle copies from one semantic case.

    The oracle is checked against the source value before each replacement.  A
    stale reviewed oracle therefore fails closed instead of silently accepting
    an unrelated rendered value.
    """
    data = copy.deepcopy(baseline_data)
    oracle = copy.deepcopy(baseline_oracle)
    for mutation in case.mutations:
        record = _record_for(data, mutation.subject)
        before = _string(
            record.get(mutation.field), f"baseline {mutation.subject}.{mutation.field}"
        )
        if mutation.subject in _EXPERIENCE_RECORDS:
            _mutate_experience(data, oracle, mutation, before)
        elif mutation.subject in _PROJECT_RECORDS:
            _mutate_project(data, oracle, mutation, before)
        else:
            _mutate_contact(oracle, mutation, before)
        record[mutation.field] = mutation.value
    return data, oracle
