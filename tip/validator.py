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


def validate_required(schema: dict[str, Any], data: dict[str, Any], path: str = "$") -> list[str]:
    """Validate required fields and enum values for the supported schema subset."""

    errors: list[str] = []

    required = schema.get("required", [])
    for key in required:
        if key not in data:
            errors.append(f"{path}: missing required field '{key}'")

    properties = schema.get("properties", {})
    for key, value in data.items():
        child_schema = properties.get(key)
        if not isinstance(child_schema, dict):
            continue

        expected_type = child_schema.get("type")
        if expected_type == "object" and isinstance(value, dict):
            errors.extend(validate_required(child_schema, value, f"{path}.{key}"))
        elif expected_type == "array" and isinstance(value, list):
            item_schema = child_schema.get("items")
            if isinstance(item_schema, dict):
                for index, item in enumerate(value):
                    if isinstance(item, dict):
                        errors.extend(validate_required(item_schema, item, f"{path}.{key}[{index}]"))

        enum_values = child_schema.get("enum")
        if enum_values is not None and value not in enum_values:
            errors.append(f"{path}.{key}: value '{value}' is not in {enum_values}")

    return errors


def discover_tip_files(target: Path) -> list[Path]:
    """Return TIP JSON files from a file or directory target."""

    if target.is_file():
        return [target]
    if target.is_dir():
        return sorted(target.glob("*.tip.json"))
    raise FileNotFoundError(f"Target not found: {target}")


def validate_file(path: Path, schema: dict[str, Any]) -> ValidationResult:
    data = load_json(path)
    if not isinstance(data, dict):
        return ValidationResult(path, ["$: TIP record must be a JSON object"])
    return ValidationResult(path, validate_required(schema, data))


def validate_target(target: Path, schema_path: Path = DEFAULT_SCHEMA_PATH) -> list[ValidationResult]:
    schema = load_json(schema_path)
    tip_files = discover_tip_files(target)
    if not tip_files:
        return [ValidationResult(target, ["No .tip.json files found"])]
    return [validate_file(path, schema) for path in tip_files]
