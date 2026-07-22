from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from tip.kairos_profile import (
    DEFAULT_PROFILE_PATH,
    validate_kairos_export_data,
    validate_kairos_export_file,
)

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "integrations" / "kairos-export.tip.json"
FIXTURES = ROOT / "tests" / "fixtures" / "kairos-export-negative-fixtures.json"


class KairosExportProfileTests(unittest.TestCase):
    """Verify the reciprocal TIP export profile and no-execution boundary."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = json.loads(DEFAULT_PROFILE_PATH.read_text(encoding="utf-8"))
        cls.base = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        cls.fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))

    def test_canonical_export_is_valid(self) -> None:
        result = validate_kairos_export_file(EXAMPLE)
        self.assertTrue(result.ok, result.errors)

    def test_export_keys_match_receiver_contract(self) -> None:
        self.assertEqual(set(self.base), set(self.profile["required"]))
        self.assertIn("protocol", self.base)
        self.assertNotIn("schema", self.base)
        self.assertNotIn("authority", self.base)

    def test_negative_fixtures_fail_closed(self) -> None:
        self.assertGreaterEqual(len(self.fixtures["cases"]), 3)
        for case in self.fixtures["cases"]:
            with self.subTest(case=case["id"]):
                record = copy.deepcopy(self.base)
                del record[case["path"][0]]
                errors = validate_kairos_export_data(record, self.profile)
                self.assertTrue(
                    any(case["expected_error"] in error for error in errors),
                    errors,
                )

    def test_receiver_incompatible_extra_field_is_rejected(self) -> None:
        record = copy.deepcopy(self.base)
        record["schema"] = "tip.kairos.export.v0.1"
        errors = validate_kairos_export_data(record, self.profile)
        self.assertIn("$.schema: unexpected receiver-incompatible field", errors)

    def test_evidence_refs_must_be_unique_absolute_https_uris(self) -> None:
        duplicate = copy.deepcopy(self.base)
        duplicate["evidence_refs"].append(duplicate["evidence_refs"][0])
        duplicate_errors = validate_kairos_export_data(duplicate, self.profile)
        self.assertIn("$.evidence_refs: references must be unique", duplicate_errors)

        malformed = copy.deepcopy(self.base)
        malformed["evidence_refs"] = ["https://"]
        malformed_errors = validate_kairos_export_data(malformed, self.profile)
        self.assertIn(
            "$.evidence_refs: every reference must be an absolute HTTPS URI",
            malformed_errors,
        )

    def test_provenance_rejects_receiver_incompatible_extra_fields(self) -> None:
        record = copy.deepcopy(self.base)
        record["provenance"]["source_url"] = "https://example.com/source"
        errors = validate_kairos_export_data(record, self.profile)
        self.assertIn(
            "$.provenance.source_url: unexpected receiver-incompatible field",
            errors,
        )

    def test_profile_preserves_no_execution_boundary(self) -> None:
        authority = self.profile["handoff_authority"]
        self.assertEqual(authority["classification"], "RESEARCH_ONLY")
        self.assertFalse(authority["execution_authorized"])
        self.assertFalse(authority["clinical_authorized"])
        self.assertFalse(authority["merge_authorized"])

    def test_commit_ref_must_be_exact(self) -> None:
        record = copy.deepcopy(self.base)
        record["commit_ref"] = "https://github.com/safal207/transition-intelligence-protocol/tree/main"
        errors = validate_kairos_export_data(record, self.profile)
        self.assertIn("$.commit_ref: must reference an exact TIP commit", errors)


if __name__ == "__main__":
    unittest.main()
