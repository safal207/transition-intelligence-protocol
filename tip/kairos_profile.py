"""Dependency-free validation for the TIP-to-Kairos export profile."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from tip.validator import ValidationResult

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE_PATH = ROOT / "integrations" / "kairos" / "profile.v0.1.json"
COMMIT_RE = re.compile(
    r"^https://github\.com/safal207/transition-intelligence-protocol/commit/[0-9a-f]{40}$"
)
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
TIP_REPOSITORY = "https://github.com/safal207/transition-intelligence-protocol"


def _reject_constant(value: str) -> None:
    """Reject non-standard JSON constants."""
    raise ValueError(f"non-finite JSON constant: {value}")


def _load_strict_json(path: Path) -> Any:
    """Load strict JSON that rejects NaN and Infinity."""
    with path.open("r", encoding="utf-8") as file:
        return json.load(file, parse_constant=_reject_constant)


def _valid_timestamp(value: Any) -> bool:
    """Return whether value is a timezone-aware ISO timestamp."""
    if not isinstance(value, str):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def validate_kairos_export_data(
    data: Any, profile: dict[str, Any]
) -> list[str]:
    """Validate required export fields, provenance, exact commit, and authority."""
    if not isinstance(data, dict):
        return ["$: export root must be an object"]

    errors: list[str] = []
    for field in profile.get("required", []):
        if field not in data:
            errors.append(f"$: missing required field '{field}'")

    string_fields = [
        "schema",
        "protocol_version",
        "repository",
        "commit_ref",
        "starting_state_ref",
        "tension",
        "cause",
        "proposed_transition",
        "smallest_research_step",
    ]
    for field in string_fields:
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"$.{field}: must be a non-empty string")

    if data.get("schema") != "tip.kairos.export.v0.1":
        errors.append("$.schema: unsupported export schema")
    if data.get("repository") != TIP_REPOSITORY:
        errors.append("$.repository: must identify the TIP repository")
    if not isinstance(data.get("commit_ref"), str) or not COMMIT_RE.fullmatch(
        data["commit_ref"]
    ):
        errors.append("$.commit_ref: must reference an exact TIP commit")

    evidence = data.get("evidence_refs")
    if not isinstance(evidence, list) or not evidence:
        errors.append("$.evidence_refs: must contain at least one reference")
    elif any(not isinstance(item, str) or not item.startswith("https://") for item in evidence):
        errors.append("$.evidence_refs: every reference must be a non-empty HTTPS URL")

    provenance = data.get("provenance")
    if not isinstance(provenance, dict):
        errors.append("$.provenance: must be an object")
    else:
        for field in profile.get("provenance_required", []):
            if field not in provenance:
                errors.append(f"$.provenance: missing required field '{field}'")
        if not isinstance(provenance.get("producer"), str) or not provenance.get(
            "producer", ""
        ).strip():
            errors.append("$.provenance.producer: must be a non-empty string")
        if not _valid_timestamp(provenance.get("produced_at")):
            errors.append("$.provenance.produced_at: must be a timezone-aware timestamp")
        if not isinstance(provenance.get("data_digest"), str) or not DIGEST_RE.fullmatch(
            provenance["data_digest"]
        ):
            errors.append("$.provenance.data_digest: must be a sha256 digest")

    expected_authority = profile.get("authority")
    if data.get("authority") != expected_authority:
        errors.append("$.authority: must match the research-only no-execution boundary")

    return errors


def validate_kairos_export_file(
    path: Path, profile_path: Path = DEFAULT_PROFILE_PATH
) -> ValidationResult:
    """Validate one TIP export file against the versioned Kairos profile."""
    try:
        profile = _load_strict_json(profile_path)
        data = _load_strict_json(path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return ValidationResult(path, [f"$: unable to read valid JSON: {exc}"])
    if not isinstance(profile, dict):
        return ValidationResult(path, ["$: Kairos profile root must be an object"])
    return ValidationResult(path, validate_kairos_export_data(data, profile))
