"""Tests for explicit IFP-to-TIP handoff validation."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tip.handoff_validator import validate_handoff_bundle


ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "examples" / "handoff" / "project-to-next-step.handoff.json"
IFP = ROOT / "examples" / "ifp" / "project-initialization.ifp.json"
TIP = ROOT / "examples" / "json" / "repository-next-step.tip.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


class HandoffValidatorTests(unittest.TestCase):
    def test_valid_handoff_bundle_passes(self) -> None:
        result = validate_handoff_bundle(HANDOFF, IFP, TIP)
        self.assertTrue(result.ok, result.errors)

    def test_source_record_id_must_match_ifp_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            handoff = load(HANDOFF)
            handoff["source"]["record_id"] = "ifp.example.other"
            handoff_path = root / "mismatched-source.handoff.json"
            write(handoff_path, handoff)

            result = validate_handoff_bundle(handoff_path, IFP, TIP)

        self.assertFalse(result.ok)
        self.assertTrue(
            any("does not match the referenced IFP record id" in error for error in result.errors),
            result.errors,
        )

    def test_ifp_source_must_be_ready(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ifp = load(IFP)
            ifp["status"] = "configured"
            ifp["readiness"]["ready"] = False
            ifp_path = root / "not-ready.ifp.json"
            write(ifp_path, ifp)

            result = validate_handoff_bundle(HANDOFF, ifp_path, TIP)

        self.assertFalse(result.ok)
        self.assertTrue(
            any("handoff source must have status 'ready'" in error for error in result.errors),
            result.errors,
        )
        self.assertTrue(
            any("handoff source must be ready" in error for error in result.errors),
            result.errors,
        )

    def test_target_state_must_match_tip_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            handoff = load(HANDOFF)
            different_state = "A different target state"
            handoff["target"]["state_summary"] = different_state
            handoff["mapping"]["target_state"] = different_state
            handoff_path = root / "state-mismatch.handoff.json"
            write(handoff_path, handoff)

            result = validate_handoff_bundle(handoff_path, IFP, TIP)

        self.assertFalse(result.ok)
        self.assertTrue(
            any("does not match the TIP state summary" in error for error in result.errors),
            result.errors,
        )

    def test_verified_handoff_requires_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            handoff = load(HANDOFF)
            handoff["verification"]["evidence"] = []
            handoff_path = root / "no-evidence.handoff.json"
            write(handoff_path, handoff)

            result = validate_handoff_bundle(handoff_path, IFP, TIP)

        self.assertFalse(result.ok)
        self.assertTrue(
            any("verified handoff requires evidence" in error for error in result.errors),
            result.errors,
        )


if __name__ == "__main__":
    unittest.main()
