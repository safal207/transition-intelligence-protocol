"""Tests for explicit Initialization Feedback Protocol to TIP handoff validation."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tip.handoff_validator import validate_ifp_to_tip_handoff
from tip.validator import load_json


ROOT = Path(__file__).resolve().parents[1]
TIP_RECORD = ROOT / "examples" / "json" / "protocol-family-next-step.tip.json"
IFP_RECORD = ROOT / "examples" / "ifp" / "project-initialization.ifp.json"


class HandoffValidatorTests(unittest.TestCase):
    def test_valid_ifp_to_tip_handoff_passes(self) -> None:
        result = validate_ifp_to_tip_handoff(TIP_RECORD, IFP_RECORD)
        self.assertTrue(result.ok, result.errors)

    def test_wrong_source_record_id_fails(self) -> None:
        tip_data = load_json(TIP_RECORD)
        tip_data["initialization"]["source_record_id"] = "ifp.example.other"

        with tempfile.TemporaryDirectory() as directory:
            tip_path = Path(directory) / "wrong-source.tip.json"
            tip_path.write_text(json.dumps(tip_data), encoding="utf-8")
            result = validate_ifp_to_tip_handoff(tip_path, IFP_RECORD)

        self.assertFalse(result.ok)
        self.assertTrue(
            any("source_record_id" in error and "does not match" in error for error in result.errors),
            result.errors,
        )

    def test_unready_ifp_source_fails(self) -> None:
        ifp_data = load_json(IFP_RECORD)
        ifp_data["status"] = "configured"
        ifp_data["readiness"]["ready"] = False
        ifp_data["readiness"]["next_protocol"] = None

        with tempfile.TemporaryDirectory() as directory:
            ifp_path = Path(directory) / "not-ready.ifp.json"
            ifp_path.write_text(json.dumps(ifp_data), encoding="utf-8")
            result = validate_ifp_to_tip_handoff(TIP_RECORD, ifp_path)

        self.assertFalse(result.ok)
        self.assertTrue(any("status 'ready'" in error for error in result.errors), result.errors)
        self.assertTrue(any("confirm readiness" in error for error in result.errors), result.errors)
        self.assertTrue(any("target 'TIP'" in error for error in result.errors), result.errors)

    def test_handoff_evidence_must_come_from_ifp_source(self) -> None:
        tip_data = load_json(TIP_RECORD)
        tip_data["initialization"]["evidence"].append("unknown-evidence.txt")

        with tempfile.TemporaryDirectory() as directory:
            tip_path = Path(directory) / "foreign-evidence.tip.json"
            tip_path.write_text(json.dumps(tip_data), encoding="utf-8")
            result = validate_ifp_to_tip_handoff(tip_path, IFP_RECORD)

        self.assertFalse(result.ok)
        self.assertTrue(
            any("evidence not present in the IFP record" in error for error in result.errors),
            result.errors,
        )


if __name__ == "__main__":
    unittest.main()
