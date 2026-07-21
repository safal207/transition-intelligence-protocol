"""Tests that verify the TIP validator can both pass and fail correctly."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tip.validator import DEFAULT_SCHEMA_PATH, load_json, validate_file, validate_target


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"


class ValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_json(DEFAULT_SCHEMA_PATH)

    def test_valid_fixture_passes(self) -> None:
        path = FIXTURES / "valid" / "minimal.tip.json"
        result = validate_file(path, self.schema)
        self.assertTrue(result.ok, result.errors)

    def test_canonical_examples_pass(self) -> None:
        results = validate_target(ROOT / "examples" / "json")
        self.assertTrue(results, "Expected canonical TIP examples")
        failures = {str(result.path): result.errors for result in results if not result.ok}
        self.assertEqual({}, failures)

    def test_invalid_fixtures_are_rejected_for_the_expected_reason(self) -> None:
        expectations = {
            "missing-cause.tip.json": "missing required field 'cause'",
            "unsupported-status.tip.json": "value 'pending' is not in",
            "blocked-commit.tip.json": "blocked records cannot recommend 'commit'",
            "high-risk-commit.tip.json": "high defection risk cannot directly recommend 'commit'",
        }

        for filename, expected_error in expectations.items():
            with self.subTest(filename=filename):
                result = validate_file(FIXTURES / "invalid" / filename, self.schema)
                self.assertFalse(result.ok, "Negative fixture unexpectedly passed")
                self.assertTrue(
                    any(expected_error in error for error in result.errors),
                    f"Expected {expected_error!r}, got {result.errors!r}",
                )

    def test_committed_record_requires_concrete_action_summary(self) -> None:
        data = load_json(FIXTURES / "valid" / "minimal.tip.json")
        data["status"] = "committed"
        data["action"]["summary"] = "   "

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "committed-without-action.tip.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = validate_file(path, self.schema)

        self.assertFalse(result.ok)
        self.assertTrue(
            any(
                "committed records require a concrete action summary" in error
                for error in result.errors
            ),
            result.errors,
        )

    def test_additional_top_level_property_fails(self) -> None:
        data = load_json(FIXTURES / "valid" / "minimal.tip.json")
        data["unexpected"] = True

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "extra-top-level.tip.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = validate_file(path, self.schema)

        self.assertFalse(result.ok)
        self.assertTrue(
            any("$.unexpected: unexpected additional property" in error for error in result.errors),
            result.errors,
        )

    def test_additional_nested_property_fails(self) -> None:
        data = load_json(FIXTURES / "valid" / "minimal.tip.json")
        data["state"]["extra_state_field"] = "not allowed"

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "extra-nested.tip.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = validate_file(path, self.schema)

        self.assertFalse(result.ok)
        self.assertTrue(
            any("$.state.extra_state_field: unexpected additional property" in error for error in result.errors),
            result.errors,
        )

    def test_malformed_json_fails_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "broken.tip.json"
            path.write_text('{"id": ', encoding="utf-8")

            result = validate_file(path, self.schema)

        self.assertFalse(result.ok)
        self.assertTrue(any("unable to read valid JSON" in error for error in result.errors))

    def test_empty_directory_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            results = validate_target(Path(directory))

        self.assertEqual(1, len(results))
        self.assertFalse(results[0].ok)
        self.assertIn("No .tip.json files found", results[0].errors)


if __name__ == "__main__":
    unittest.main()
