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

    def test_export_cannot_authorize_execution(self) -> None:
        record = copy.deepcopy(self.base)
        record["authority"]["execution_authorized"] = True
        errors = validate_kairos_export_data(record, self.profile)
        self.assertIn(
            "$.authority: must match the research-only no-execution boundary",
            errors,
        )

    def test_commit_ref_must_be_exact(self) -> None:
        record = copy.deepcopy(self.base)
        record["commit_ref"] = "https://github.com/safal207/transition-intelligence-protocol/tree/main"
        errors = validate_kairos_export_data(record, self.profile)
        self.assertIn("$.commit_ref: must reference an exact TIP commit", errors)


if __name__ == "__main__":
    unittest.main()
