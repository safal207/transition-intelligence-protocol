"""Validation for explicit Initialization Feedback Protocol to TIP handoffs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tip.ifp_validator import DEFAULT_IFP_SCHEMA_PATH, validate_ifp_file
from tip.validator import (
    DEFAULT_SCHEMA_PATH,
    ValidationResult,
    load_json,
    validate_file,
    validate_schema_subset,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HANDOFF_SCHEMA_PATH = ROOT / "schemas" / "ifp-tip-handoff.schema.json"


def validate_handoff_invariants(data: dict[str, Any]) -> list[str]:
    """Validate consistency inside a handoff record."""

    errors: list[str] = []
    status = data.get("status")
    source = data.get("source")
    target = data.get("target")
    mapping = data.get("mapping")
    verification = data.get("verification")

    if not all(isinstance(item, dict) for item in (source, target, mapping, verification)):
        return errors

    if source.get("ready_state") != mapping.get("source_ready_state"):
        errors.append("$.mapping.source_ready_state: must match $.source.ready_state")

    if target.get("state_summary") != mapping.get("target_state"):
        errors.append("$.mapping.target_state: must match $.target.state_summary")

    if status == "verified":
        if verification.get("source_verified") is not True:
            errors.append("$.verification.source_verified: verified handoff requires true")
        if verification.get("mapping_verified") is not True:
            errors.append("$.verification.mapping_verified: verified handoff requires true")
        evidence = verification.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            errors.append("$.verification.evidence: verified handoff requires evidence")

    return errors


def validate_handoff_file(path: Path, schema: dict[str, Any]) -> ValidationResult:
    try:
        data = load_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        return ValidationResult(path, [f"$: unable to read valid JSON: {exc}"])

    errors = validate_schema_subset(schema, data)
    if isinstance(data, dict):
        errors.extend(validate_handoff_invariants(data))
    return ValidationResult(path, errors)


def validate_handoff_bundle(
    handoff_path: Path,
    ifp_path: Path,
    tip_path: Path,
    handoff_schema_path: Path = DEFAULT_HANDOFF_SCHEMA_PATH,
    ifp_schema_path: Path = DEFAULT_IFP_SCHEMA_PATH,
    tip_schema_path: Path = DEFAULT_SCHEMA_PATH,
) -> ValidationResult:
    """Validate the handoff record and both referenced protocol records together."""

    handoff_schema = load_json(handoff_schema_path)
    ifp_schema = load_json(ifp_schema_path)
    tip_schema = load_json(tip_schema_path)

    handoff_result = validate_handoff_file(handoff_path, handoff_schema)
    ifp_result = validate_ifp_file(ifp_path, ifp_schema)
    tip_result = validate_file(tip_path, tip_schema)

    errors = list(handoff_result.errors)
    errors.extend(f"IFP {error}" for error in ifp_result.errors)
    errors.extend(f"TIP {error}" for error in tip_result.errors)

    if errors:
        return ValidationResult(handoff_path, errors)

    handoff = load_json(handoff_path)
    ifp = load_json(ifp_path)
    tip = load_json(tip_path)

    source = handoff["source"]
    target = handoff["target"]
    mapping = handoff["mapping"]

    if source["record_id"] != ifp["id"]:
        errors.append("$.source.record_id: does not match the referenced IFP record id")

    if target["record_id"] != tip["id"]:
        errors.append("$.target.record_id: does not match the referenced TIP record id")

    if ifp["status"] != "ready":
        errors.append("IFP $.status: handoff source must have status 'ready'")

    if ifp["readiness"]["ready"] is not True:
        errors.append("IFP $.readiness.ready: handoff source must be ready")

    if ifp["readiness"].get("next_protocol") != "TIP":
        errors.append("IFP $.readiness.next_protocol: handoff source must target 'TIP'")

    if source["ready_state"] != ifp["subject"]["target_state"]:
        errors.append("$.source.ready_state: does not match the IFP target state")

    if target["state_summary"] != tip["state"]["summary"]:
        errors.append("$.target.state_summary: does not match the TIP state summary")

    if mapping["source_ready_state"] != ifp["subject"]["target_state"]:
        errors.append("$.mapping.source_ready_state: does not match the IFP target state")

    if mapping["target_state"] != tip["state"]["summary"]:
        errors.append("$.mapping.target_state: does not match the TIP state summary")

    return ValidationResult(handoff_path, errors)
