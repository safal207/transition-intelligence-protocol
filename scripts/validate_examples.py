#!/usr/bin/env python3
"""Validate TIP JSON examples against the canonical schema.

Usage:
    python scripts/validate_examples.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "tip-record.schema.json"
EXAMPLES_DIR = ROOT / "examples" / "json"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def validate_required(schema: dict[str, Any], data: dict[str, Any], path: str = "$") -> list[str]:
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


def main() -> int:
    schema = load_json(SCHEMA_PATH)
    example_paths = sorted(EXAMPLES_DIR.glob("*.tip.json"))

    if not example_paths:
        print("No TIP examples found.")
        return 1

    failed = False
    for example_path in example_paths:
        data = load_json(example_path)
        errors = validate_required(schema, data)
        if errors:
            failed = True
            print(f"FAIL {example_path.relative_to(ROOT)}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK   {example_path.relative_to(ROOT)}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
