"""Exercise non-finite input through each existing protocol-family entry point."""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tip.validator import validate_file
from tip.ifp_validator import validate_ifp_file
from tip.handoff_validator import validate_handoff_file, _resolve_evidence_file

ROOT = Path(__file__).resolve().parents[1]
TIP_EXAMPLE = ROOT / "examples/json/startup-pivot.tip.json"
IFP_EXAMPLE = ROOT / "examples/ifp/project-initialization.ifp.json"
HANDOFF = ROOT / "examples/handoff/project-to-next-step.handoff.json"
HANDOFF_TIP = ROOT / "examples/json/repository-next-step.tip.json"


class NumericEntryPointTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="tip-entrypoints-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.bad = self.root / "nonfinite.json"
        self.bad.write_text('{"unexpected": NaN}', encoding="utf-8")

    def assert_parse_rejection(self, result):
        self.assertFalse(result.ok)
        self.assertTrue(any("unable to read valid JSON" in e and "finite" in e for e in result.errors), result.errors)

    def cli(self, *args):
        return subprocess.run([sys.executable, "-m", "tip", *map(str, args)], cwd=ROOT,
                              text=True, capture_output=True, timeout=30)

    def assert_clean_failure(self, result):
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("FAIL", result.stdout)
        self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_tip_file_rejects_at_parse_time(self):
        self.assert_parse_rejection(validate_file(self.bad, {}))

    def test_ifp_file_rejects_at_parse_time(self):
        self.assert_parse_rejection(validate_ifp_file(self.bad, {}))

    def test_handoff_file_rejects_at_parse_time(self):
        self.assert_parse_rejection(validate_handoff_file(self.bad, {}))

    def test_json_evidence_rejects_nonfinite_document(self):
        path, error = _resolve_evidence_file("file:nonfinite.json", self.root)
        self.assertIsNone(path)
        self.assertIn("finite", error or "")

    def test_all_cli_schema_loads_fail_cleanly(self):
        commands = [
            ("validate", TIP_EXAMPLE, "--schema", self.bad),
            ("validate-ifp", IFP_EXAMPLE, "--schema", self.bad),
            ("validate-handoff", HANDOFF, "--ifp", IFP_EXAMPLE, "--tip", HANDOFF_TIP,
             "--handoff-schema", self.bad),
        ]
        for command in commands:
            with self.subTest(command=command[0]):
                result = self.cli(*command)
                self.assert_clean_failure(result)
                self.assertIn("finite", result.stdout)

    def test_all_cli_record_loads_reject_invalid_utf8(self):
        self.bad.write_bytes(b'{"value": "\xff"}')
        commands = [
            ("validate", self.bad),
            ("validate-ifp", self.bad),
            ("validate-handoff", self.bad, "--ifp", IFP_EXAMPLE, "--tip", HANDOFF_TIP),
        ]
        for command in commands:
            with self.subTest(command=command[0]):
                self.assert_clean_failure(self.cli(*command))

    def test_cli_literal_and_overflow_matrix(self):
        original = TIP_EXAMPLE.read_text(encoding="utf-8")
        needle = '"confidence": 0.72'
        self.assertEqual(original.count(needle), 1, "fixture changed: update the single-value mutation")
        for token in ("NaN", "Infinity", "-Infinity", "1e309", "-1e309"):
            with self.subTest(token=token):
                self.bad.write_text(original.replace(needle, '"confidence": ' + token, 1), encoding="utf-8")
                result = self.cli("validate", self.bad)
                self.assert_clean_failure(result)
                self.assertIn("finite", result.stdout)


if __name__ == "__main__":
    unittest.main()
