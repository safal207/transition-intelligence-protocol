"""Validation utilities for Initialization Feedback Protocol records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tip.validator import ValidationResult, load_json, validate_schema_subset


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IFP_SCHEMA_PATH = ROOT / "schemas" / "ifp-record.schema.json"


def validate_ifp_invariants(data: dict[str, Any]) -> list[str]:
    """Validate IFP readiness rules that JSON shape alone cannot express."""

    errors: list[str] = []
    status = data.get("status")
    feedback = data.get("feedback")
    correction = data.get("correction")
    readiness = data.get("readiness")

    feedback_passed = feedback.get("passed") if isinstance(feedback, dict) else None
    readiness_ready = readiness.get("ready") if isinstance(readiness, dict) else None
    evidence = readiness.get("evidence") if isinstance(readiness, dict) else None
    correction_required = correction.get("required") if isinstance(correction, dict) else None
    changes = correction.get("changes") if isinstance(correction, dict) else None

    if status == "ready" and feedback_passed is not True:
        errors.append("$.feedback.passed: ready status requires passed feedback")

    if status == "ready" and readiness_ready is not True:
        errors.append("$.readiness.ready: ready status requires readiness confirmation")

    if readiness_ready is True and (not isinstance(evidence, list) or not evidence):
        errors.append("$.readiness.evidence: ready initialization requires evidence")

    if correction_required is True and (not isinstance(changes, list) or not changes):
        errors.append("$.correction.changes: required correction must record at least one change")

    if feedback_passed is False and readiness_ready is True:
        errors.append("$.readiness.ready: failed feedback cannot produce a ready initialization")

    return errors


def discover_ifp_files(target: Path) -> list[Path]:
    """Return IFP JSON files from a file or directory target."""

    if target.is_file():
        return [target]
    if target.is_dir():
        return sorted(target.glob("*.ifp.json"))
    raise FileNotFoundError(f"Target not found: {target}")


def validate_ifp_file(path: Path, schema: dict[str, Any]) -> ValidationResult:
    try:
        data = load_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        return ValidationResult(path, [f"$: unable to read valid JSON: {exc}"])

    errors = validate_schema_subset(schema, data)
    if isinstance(data, dict):
        errors.extend(validate_ifp_invariants(data))
    return ValidationResult(path, errors)


def validate_ifp_target(
    target: Path,
    schema_path: Path = DEFAULT_IFP_SCHEMA_PATH,
) -> list[ValidationResult]:
    schema = load_json(schema_path)
    ifp_files = discover_ifp_files(target)
    if not ifp_files:
        return [ValidationResult(target, ["No .ifp.json files found"])]
    return [validate_ifp_file(path, schema) for path in ifp_files]
