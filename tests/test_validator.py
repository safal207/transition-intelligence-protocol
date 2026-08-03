"""Tests that verify the TIP validator can both pass and fail correctly."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tip.validator import DEFAULT_SCHEMA_PATH, load_json, validate_file, validate_target


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"


def add_confidence_assessment(
    data: dict,
    *,
    human_confirmed: bool = False,
    assessor_type: str = "ai",
    method: str = "judgment",
) -> None:
    assessment = {
        "assessor": "test assessor",
        "assessor_type": assessor_type,
        "method": method,
        "rationale": "Observed signals support the cause, while uncertainty remains explicit.",
        "alternative_explanations": ["another cause may explain the same signals"],
        "human_confirmed": human_confirmed,
    }
    if method in {"statistical", "calibrated_model"}:
        assessment["calibration_reference"] = "test calibration record"
    data["cause"]["confidence_assessment"] = assessment


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
        add_confidence_assessment(data)
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

    def test_committed_record_requires_confidence_provenance(self) -> None:
        data = load_json(FIXTURES / "valid" / "minimal.tip.json")
        data["status"] = "committed"

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "committed-without-confidence-provenance.tip.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = validate_file(path, self.schema)

        self.assertFalse(result.ok)
        self.assertTrue(
            any(
                "committed records require confidence provenance" in error
                for error in result.errors
            ),
            result.errors,
        )

    def test_committed_confidence_requires_considered_alternative(self) -> None:
        data = load_json(FIXTURES / "valid" / "minimal.tip.json")
        data["status"] = "committed"
        add_confidence_assessment(data)
        data["cause"]["confidence_assessment"]["alternative_explanations"] = []

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "committed-without-alternative.tip.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = validate_file(path, self.schema)

        self.assertFalse(result.ok)
        self.assertTrue(
            any(
                "require at least one considered alternative" in error
                for error in result.errors
            ),
            result.errors,
        )

    def test_statistical_confidence_requires_calibration_reference(self) -> None:
        data = load_json(FIXTURES / "valid" / "minimal.tip.json")
        data["status"] = "committed"
        add_confidence_assessment(data, method="statistical")
        del data["cause"]["confidence_assessment"]["calibration_reference"]

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "statistical-without-calibration.tip.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = validate_file(path, self.schema)

        self.assertFalse(result.ok)
        self.assertTrue(
            any(
                "requires a calibration reference" in error
                for error in result.errors
            ),
            result.errors,
        )

    def test_high_consequence_commit_requires_human_confirmation(self) -> None:
        data = load_json(FIXTURES / "valid" / "minimal.tip.json")
        data["status"] = "committed"
        data["cause"]["confidence"] = 0.8
        add_confidence_assessment(data, human_confirmed=False)
        data["transition"]["reversibility"] = "low"
        data["transition"]["impact_scope"] = "bounded"
        data["transition"]["feedback_latency"] = "short"

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "high-consequence-without-human.tip.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = validate_file(path, self.schema)

        self.assertFalse(result.ok)
        self.assertTrue(
            any(
                "high-consequence commitments require human confirmation" in error
                for error in result.errors
            ),
            result.errors,
        )

    def test_high_consequence_commit_with_human_confirmation_passes(self) -> None:
        data = load_json(FIXTURES / "valid" / "minimal.tip.json")
        data["status"] = "committed"
        data["cause"]["confidence"] = 0.8
        add_confidence_assessment(data, human_confirmed=True)
        data["transition"]["reversibility"] = "low"
        data["transition"]["impact_scope"] = "bounded"
        data["transition"]["feedback_latency"] = "short"

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "high-consequence-with-human.tip.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = validate_file(path, self.schema)

        self.assertTrue(result.ok, result.errors)

    def test_low_confidence_commit_requires_high_reversibility(self) -> None:
        data = load_json(FIXTURES / "valid" / "minimal.tip.json")
        data["status"] = "committed"
        add_confidence_assessment(data)
        data["cause"]["confidence"] = 0.49
        data["transition"]["reversibility"] = "medium"
        data["transition"]["impact_scope"] = "bounded"
        data["transition"]["feedback_latency"] = "short"
        data["action"]["review_after"] = "after the pilot"

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "low-confidence-medium-reversibility.tip.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = validate_file(path, self.schema)

        self.assertFalse(result.ok)
        self.assertTrue(
            any(
                "low-confidence commitments require high reversibility" in error
                for error in result.errors
            ),
            result.errors,
        )

    def test_low_confidence_commit_requires_bounded_impact(self) -> None:
        data = load_json(FIXTURES / "valid" / "minimal.tip.json")
        data["status"] = "committed"
        add_confidence_assessment(data, human_confirmed=True)
        data["cause"]["confidence"] = 0.49
        data["transition"]["reversibility"] = "high"
        data["transition"]["impact_scope"] = "systemic"
        data["transition"]["feedback_latency"] = "short"
        data["action"]["review_after"] = "after the pilot"

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "low-confidence-systemic-impact.tip.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = validate_file(path, self.schema)

        self.assertFalse(result.ok)
        self.assertTrue(
            any(
                "low-confidence commitments require local or bounded impact" in error
                for error in result.errors
            ),
            result.errors,
        )

    def test_low_confidence_commit_requires_fast_feedback(self) -> None:
        data = load_json(FIXTURES / "valid" / "minimal.tip.json")
        data["status"] = "committed"
        add_confidence_assessment(data, human_confirmed=True)
        data["cause"]["confidence"] = 0.49
        data["transition"]["reversibility"] = "high"
        data["transition"]["impact_scope"] = "bounded"
        data["transition"]["feedback_latency"] = "long"
        data["action"]["review_after"] = "after the pilot"

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "low-confidence-long-feedback.tip.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = validate_file(path, self.schema)

        self.assertFalse(result.ok)
        self.assertTrue(
            any(
                "low-confidence commitments require immediate or short feedback" in error
                for error in result.errors
            ),
            result.errors,
        )

    def test_low_confidence_commit_requires_review_point(self) -> None:
        data = load_json(FIXTURES / "valid" / "minimal.tip.json")
        data["status"] = "committed"
        add_confidence_assessment(data)
        data["cause"]["confidence"] = 0.49
        data["transition"]["reversibility"] = "high"
        data["transition"]["impact_scope"] = "bounded"
        data["transition"]["feedback_latency"] = "short"

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "low-confidence-without-review-point.tip.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = validate_file(path, self.schema)

        self.assertFalse(result.ok)
        self.assertTrue(
            any(
                "low-confidence commitments require a concrete review point" in error
                for error in result.errors
            ),
            result.errors,
        )

    def test_low_confidence_ai_can_commit_bounded_reversible_pilot(self) -> None:
        data = load_json(FIXTURES / "valid" / "minimal.tip.json")
        data["status"] = "committed"
        add_confidence_assessment(data, human_confirmed=False, assessor_type="ai")
        data["cause"]["confidence"] = 0.49
        data["transition"]["reversibility"] = "high"
        data["transition"]["impact_scope"] = "bounded"
        data["transition"]["feedback_latency"] = "short"
        data["action"]["summary"] = "Run one bounded reversible pilot to collect evidence."
        data["action"]["review_after"] = "after five pilot sessions"

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "low-confidence-bounded-pilot.tip.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = validate_file(path, self.schema)

        self.assertTrue(result.ok, result.errors)

    def test_committed_record_cannot_have_high_defection_risk(self) -> None:
        data = load_json(FIXTURES / "valid" / "minimal.tip.json")
        data["status"] = "committed"
        add_confidence_assessment(data)
        data["cooperation"]["defection_risk"] = "high"
        data["cooperation"]["recommendation"] = "clarify"

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "committed-high-defection-risk.tip.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = validate_file(path, self.schema)

        self.assertFalse(result.ok)
        self.assertTrue(
            any(
                "committed records cannot have high defection risk" in error
                for error in result.errors
            ),
            result.errors,
        )

    def test_reviewed_record_requires_concrete_review_notes(self) -> None:
        data = load_json(FIXTURES / "valid" / "minimal.tip.json")
        data["status"] = "reviewed"

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "reviewed-without-review.tip.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = validate_file(path, self.schema)

        self.assertFalse(result.ok)
        self.assertTrue(
            any(
                "reviewed records require concrete review notes" in error
                for error in result.errors
            ),
            result.errors,
        )

    def test_reviewed_record_with_review_notes_passes(self) -> None:
        data = load_json(FIXTURES / "valid" / "minimal.tip.json")
        data["status"] = "reviewed"
        data["review"] = {
            "summary": "The clarification step produced an actionable request.",
            "actual_consequence": "The owner and next action are now explicit.",
            "evidence": ["clarified request record"],
            "next_state": "ready for a bounded action",
        }

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "reviewed-with-review.tip.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = validate_file(path, self.schema)

        self.assertTrue(result.ok, result.errors)

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
