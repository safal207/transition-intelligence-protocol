"""Tests for Initialization Feedback Protocol validation."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tip.ifp_validator import (
    DEFAULT_IFP_SCHEMA_PATH,
    validate_ifp_file,
    validate_ifp_target,
)
from tip.validator import load_json


ROOT = Path(__file__).resolve().parents[1]
INVALID_FIXTURES = ROOT / "tests" / "fixtures" / "ifp" / "invalid"


class IFPValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_json(DEFAULT_IFP_SCHEMA_PATH)

    def test_ready_project_example_passes(self) -> None:
        path = ROOT / "examples" / "ifp" / "project-initialization.ifp.json"
        result = validate_ifp_file(path, self.schema)
        self.assertTrue(result.ok, result.errors)

    def test_invalid_ifp_fixtures_fail_for_expected_reason(self) -> None:
        expectations = {
            "ready-with-failed-feedback.ifp.json": "ready status requires passed feedback",
            "ready-without-evidence.ifp.json": "ready initialization requires evidence",
            "correction-without-changes.ifp.json": "required correction must record at least one change",
        }

        for filename, expected_error in expectations.items():
            with self.subTest(filename=filename):
                result = validate_ifp_file(INVALID_FIXTURES / filename, self.schema)
                self.assertFalse(result.ok, "Invalid IFP fixture unexpectedly passed")
                self.assertTrue(
                    any(expected_error in error for error in result.errors),
                    f"Expected {expected_error!r}, got {result.errors!r}",
                )

    def test_additional_ifp_top_level_property_fails(self) -> None:
        data = load_json(ROOT / "examples" / "ifp" / "project-initialization.ifp.json")
        data["unexpected"] = True

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "extra-top-level.ifp.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = validate_ifp_file(path, self.schema)

        self.assertFalse(result.ok)
        self.assertTrue(
            any("$.unexpected: unexpected additional property" in error for error in result.errors),
            result.errors,
        )

    def test_additional_ifp_nested_property_fails(self) -> None:
        data = load_json(ROOT / "examples" / "ifp" / "project-initialization.ifp.json")
        data["subject"]["extra_subject_field"] = "not allowed"

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "extra-nested.ifp.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = validate_ifp_file(path, self.schema)

        self.assertFalse(result.ok)
        self.assertTrue(
            any("$.subject.extra_subject_field: unexpected additional property" in error for error in result.errors),
            result.errors,
        )

    def test_empty_ifp_directory_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            results = validate_ifp_target(Path(directory))

        self.assertEqual(1, len(results))
        self.assertFalse(results[0].ok)
        self.assertIn("No .ifp.json files found", results[0].errors)


if __name__ == "__main__":
    unittest.main()
