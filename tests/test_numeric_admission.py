"""Regression tests for TIP numeric admission.

Covers the shared JSON ingress used by TIP, IFP and handoff records, the
in-memory schema-subset API, and the command line, using the actual modules.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tip.validator import (
    InvalidJSONError,
    LOW_CONFIDENCE_THRESHOLD,
    load_json,
    loads_json,
    validate_schema_subset,
    validate_target,
)

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "json" / "startup-pivot.tip.json"
CONFIDENCE_SCHEMA = {"type": "number", "minimum": 0, "maximum": 1}


class JsonIngressTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory(prefix="tip-numeric-")
        self.tmp = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def write(self, name: str, text: str) -> Path:
        path = self.tmp / name
        path.write_text(text, encoding="utf-8")
        return path

    def test_non_finite_literals_are_rejected(self) -> None:
        for token in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(token=token):
                with self.assertRaises(InvalidJSONError):
                    loads_json('{"cause": {"confidence": %s}}' % token)

    def test_overflowing_numeric_tokens_are_rejected(self) -> None:
        for token in ("1e309", "-1e309"):
            with self.subTest(token=token):
                with self.assertRaises(InvalidJSONError):
                    loads_json('{"confidence": %s}' % token)

    def test_invalid_json_error_is_a_value_error(self) -> None:
        self.assertTrue(issubclass(InvalidJSONError, ValueError))

    def test_malformed_json_is_rejected(self) -> None:
        path = self.write("malformed.json", "{ nope ")
        with self.assertRaises(ValueError):
            load_json(path)

    def test_legitimate_numbers_survive(self) -> None:
        parsed = loads_json('{"a": 0, "b": 0.5, "c": 1, "d": 1e308, "e": -0.25}')
        self.assertEqual(
            parsed, {"a": 0, "b": 0.5, "c": 1, "d": 1e308, "e": -0.25}
        )

    def test_quoted_strings_are_not_reinterpreted(self) -> None:
        parsed = loads_json('{"a": "NaN", "b": "Infinity", "c": "1e309"}')
        self.assertEqual(parsed, {"a": "NaN", "b": "Infinity", "c": "1e309"})

    def test_file_ingress_rejects_nan(self) -> None:
        text = EXAMPLE.read_text(encoding="utf-8").replace(
            '"confidence": 0.72', '"confidence": NaN'
        )
        path = self.write("nan.tip.json", text)
        with self.assertRaises(InvalidJSONError):
            load_json(path)

    def test_all_shipped_examples_still_load(self) -> None:
        loaded = 0
        for path in sorted((ROOT / "examples" / "json").glob("*.json")):
            load_json(path)
            loaded += 1
        for path in sorted((ROOT / "schemas").glob("*.json")):
            load_json(path)
            loaded += 1
        self.assertGreater(loaded, 0)


class SchemaSubsetNumericTest(unittest.TestCase):
    def errors(self, value: object) -> list[str]:
        return validate_schema_subset(CONFIDENCE_SCHEMA, value, "$.cause.confidence")

    def test_non_finite_floats_supplied_in_memory_are_rejected(self) -> None:
        for value in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value):
                errors = self.errors(value)
                self.assertTrue(errors)
                self.assertIn("not a finite number", errors[0])

    def test_boundaries_are_accepted(self) -> None:
        for value in (0, 0.0, 0.5, 1, 1.0):
            with self.subTest(value=value):
                self.assertEqual(self.errors(value), [])

    def test_out_of_range_is_rejected(self) -> None:
        self.assertIn("above maximum", self.errors(1.1)[0])
        self.assertIn("below minimum", self.errors(-0.1)[0])

    def test_bool_and_string_impostors_are_rejected(self) -> None:
        for value in (True, False, "0.5"):
            with self.subTest(value=value):
                errors = self.errors(value)
                self.assertTrue(errors)
                self.assertIn("expected type", errors[0])

    def test_huge_integers_do_not_raise(self) -> None:
        errors = validate_schema_subset({"type": "integer"}, 10**400, "$.big")
        self.assertEqual(errors, [])


class LowConfidenceSafeguardTest(unittest.TestCase):
    """The existing low-confidence gates must keep firing."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory(prefix="tip-lowconf-")
        self.tmp = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def test_threshold_unchanged(self) -> None:
        self.assertEqual(LOW_CONFIDENCE_THRESHOLD, 0.5)

    def test_low_confidence_without_safeguards_still_fails(self) -> None:
        record = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        record["cause"]["confidence"] = 0.1
        record.get("transition", {})["reversibility"] = "low"
        path = self.tmp / "low.tip.json"
        path.write_text(json.dumps(record), encoding="utf-8")
        results = validate_target(path)
        self.assertFalse(results[0].ok, "low-confidence safeguards must still apply")


class CommandLineTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory(prefix="tip-cli-")
        self.tmp = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.base = EXAMPLE.read_text(encoding="utf-8")

    def run_cli(self, path: Path) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, "-m", "tip", "validate", str(path)],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )

    def write(self, name: str, text: str) -> Path:
        path = self.tmp / name
        path.write_text(text, encoding="utf-8")
        return path

    def test_baseline_example_passes(self) -> None:
        result = self.run_cli(self.write("baseline.tip.json", self.base))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("OK", result.stdout)

    def test_nan_confidence_fails_cleanly(self) -> None:
        text = self.base.replace('"confidence": 0.72', '"confidence": NaN')
        result = self.run_cli(self.write("nan.tip.json", text))
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("FAIL", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_overflow_confidence_fails_cleanly(self) -> None:
        text = self.base.replace('"confidence": 0.72', '"confidence": 1e309')
        result = self.run_cli(self.write("overflow.tip.json", text))
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_out_of_range_confidence_still_fails(self) -> None:
        text = self.base.replace('"confidence": 0.72', '"confidence": 1.1')
        result = self.run_cli(self.write("high.tip.json", text))
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("above maximum", result.stdout)

    def test_malformed_json_fails_cleanly(self) -> None:
        result = self.run_cli(self.write("malformed.tip.json", "{ nope "))
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
