"""Cross-record validation for the IFP-to-TIP handoff."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from tip.ifp_validator import DEFAULT_IFP_SCHEMA_PATH, validate_ifp_file
from tip.validator import (
    DEFAULT_SCHEMA_PATH,
    ValidationResult,
    load_json,
    validate_file,
)


def _prefix_errors(prefix: str, errors: list[str]) -> list[str]:
    return [f"{prefix}: {error}" for error in errors]


def validate_ifp_to_tip_handoff(
    tip_path: Path,
    ifp_path: Path,
    tip_schema_path: Path = DEFAULT_SCHEMA_PATH,
    ifp_schema_path: Path = DEFAULT_IFP_SCHEMA_PATH,
) -> ValidationResult:
    """Validate record shape and provenance across an IFP-to-TIP handoff."""

    tip_schema = load_json(tip_schema_path)
    ifp_schema = load_json(ifp_schema_path)

    tip_result = validate_file(tip_path, tip_schema)
    ifp_result = validate_ifp_file(ifp_path, ifp_schema)

    errors = _prefix_errors("TIP", tip_result.errors)
    errors.extend(_prefix_errors("IFP", ifp_result.errors))
    if errors:
        return ValidationResult(tip_path, errors)

    tip_data: dict[str, Any] = load_json(tip_path)
    ifp_data: dict[str, Any] = load_json(ifp_path)

    initialization = tip_data.get("initialization")
    if not isinstance(initialization, dict):
        errors.append("TIP.initialization: IFP-to-TIP handoff requires initialization metadata")
        return ValidationResult(tip_path, errors)

    feedback = ifp_data.get("feedback")
    readiness = ifp_data.get("readiness")
    subject = ifp_data.get("subject")

    if ifp_data.get("status") != "ready":
        errors.append("IFP.status: handoff source must have status 'ready'")

    if not isinstance(feedback, dict) or feedback.get("passed") is not True:
        errors.append("IFP.feedback.passed: handoff source requires passed feedback")

    if not isinstance(readiness, dict) or readiness.get("ready") is not True:
        errors.append("IFP.readiness.ready: handoff source must confirm readiness")

    if isinstance(readiness, dict) and readiness.get("next_protocol") != "TIP":
        errors.append("IFP.readiness.next_protocol: handoff source must target 'TIP'")

    if initialization.get("source_protocol") != "IFP":
        errors.append("TIP.initialization.source_protocol: expected 'IFP'")

    if initialization.get("source_record_id") != ifp_data.get("id"):
        errors.append("TIP.initialization.source_record_id: does not match the IFP record id")

    expected_ready_state = subject.get("target_state") if isinstance(subject, dict) else None
    if initialization.get("ready_state") != expected_ready_state:
        errors.append("TIP.initialization.ready_state: does not match the IFP target state")

    handoff_evidence = initialization.get("evidence")
    source_evidence = readiness.get("evidence") if isinstance(readiness, dict) else None
    if not isinstance(handoff_evidence, list) or not handoff_evidence:
        errors.append("TIP.initialization.evidence: handoff requires at least one evidence item")
    elif not isinstance(source_evidence, list) or not set(handoff_evidence).issubset(set(source_evidence)):
        errors.append("TIP.initialization.evidence: contains evidence not present in the IFP record")

    return ValidationResult(tip_path, errors)
