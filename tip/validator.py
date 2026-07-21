"""Validation utilities for Transition Intelligence Protocol records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA_PATH = ROOT / "schemas" / "tip-record.schema.json"


class ValidationResult:
    """Simple validation result container."""

    def __init__(self, path: Path, errors: list[str]) -> None:
        self.path = path
        self.errors = errors

    @property
    def ok(self) -> bool:
        return not self.errors


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _matches_type(value: Any, expected_type: str) -> bool:
    type_checks = {
        "object": lambda item: isinstance(item, dict),
        "array": lambda item: isinstance(item, list),
        "string": lambda item: isinstance(item, str),
        "number": lambda item: isinstance(item, (int, float)) and not isinstance(item, bool),
        "integer": lambda item: isinstance(item, int) and not isinstance(item, bool),
        "boolean": lambda item: isinstance(item, bool),
        "null": lambda item: item is None,
    }
    check = type_checks.get(expected_type)
    return True if check is None else check(value)


def _type_is_valid(value: Any, expected_type: Any) -> bool:
    if isinstance(expected_type, str):
        return _matches_type(value, expected_type)
    if isinstance(expected_type, list):
        return any(isinstance(item, str) and _matches_type(value, item) for item in expected_type)
    return True


def validate_schema_subset(
    schema: dict[str, Any],
    data: Any,
    path: str = "$",
) -> list[str]:
    """Validate the dependency-free JSON Schema subset used by TIP."""

    errors: list[str] = []
    expected_type = schema.get("type")

    if not _type_is_valid(data, expected_type):
        errors.append(f"{path}: expected type {expected_type!r}")
        return errors

    enum_values = schema.get("enum")
    if enum_values is not None and data not in enum_values:
        errors.append(f"{path}: value {data!r} is not in {enum_values}")

    if isinstance(data, (int, float)) and not isinstance(data, bool):
        minimum = schema.get("minimum")
        maximum = schema.get("maximum")
        if minimum is not None and data < minimum:
            errors.append(f"{path}: value {data!r} is below minimum {minimum}")
        if maximum is not None and data > maximum:
            errors.append(f"{path}: value {data!r} is above maximum {maximum}")

    if isinstance(data, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in data:
                errors.append(f"{path}: missing required field '{key}'")

        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in data:
                if key not in properties:
                    errors.append(f"{path}.{key}: unexpected additional property")

        for key, value in data.items():
            child_schema = properties.get(key)
            if isinstance(child_schema, dict):
                errors.extend(validate_schema_subset(child_schema, value, f"{path}.{key}"))

    if isinstance(data, list):
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(data):
                errors.extend(validate_schema_subset(item_schema, item, f"{path}[{index}]"))

    return errors


def validate_invariants(data: dict[str, Any]) -> list[str]:
    """Validate semantic TIP rules that have explicit negative tests."""

    errors: list[str] = []
    status = data.get("status")
    cooperation = data.get("cooperation")
    action = data.get("action")

    if isinstance(action, dict):
        action_summary = action.get("summary")
        if status == "committed" and (
            not isinstance(action_summary, str) or not action_summary.strip()
        ):
            errors.append(
                "$.action.summary: committed records require a concrete action summary"
            )

    if not isinstance(cooperation, dict):
        return errors

    recommendation = cooperation.get("recommendation")
    defection_risk = cooperation.get("defection_risk")

    if status == "blocked" and recommendation == "commit":
        errors.append(
            "$.cooperation.recommendation: blocked records cannot recommend 'commit'"
        )

    if defection_risk == "high" and recommendation == "commit":
        errors.append(
            "$.cooperation.recommendation: high defection risk cannot directly recommend 'commit'"
        )

    return errors


def discover_tip_files(target: Path) -> list[Path]:
    """Return TIP JSON files from a file or directory target."""

    if target.is_file():
        return [target]
    if target.is_dir():
        return sorted(target.glob("*.tip.json"))
    raise FileNotFoundError(f"Target not found: {target}")


def validate_file(path: Path, schema: dict[str, Any]) -> ValidationResult:
    try:
        data = load_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        return ValidationResult(path, [f"$: unable to read valid JSON: {exc}"])

    errors = validate_schema_subset(schema, data)
    if isinstance(data, dict):
        errors.extend(validate_invariants(data))
    return ValidationResult(path, errors)


def validate_target(target: Path, schema_path: Path = DEFAULT_SCHEMA_PATH) -> list[ValidationResult]:
    schema = load_json(schema_path)
    tip_files = discover_tip_files(target)
    if not tip_files:
        return [ValidationResult(target, ["No .tip.json files found"])]
    return [validate_file(path, schema) for path in tip_files]
