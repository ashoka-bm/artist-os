from __future__ import annotations

import unittest
from pathlib import Path

from json_schema_validator import (
    REPO_ROOT,
    ValidationError,
    iter_validation_targets,
    load_json,
    validate,
    validate_file,
)


class SchemaValidationTests(unittest.TestCase):
    def test_examples_and_fixtures_validate(self) -> None:
        targets = iter_validation_targets(include_fixtures=True)
        self.assertGreaterEqual(len(targets), 16)
        for schema_path, data_path in targets:
            with self.subTest(data=data_path.relative_to(REPO_ROOT)):
                validate_file(schema_path, data_path)

    def test_invalid_review_record_missing_drifted_fails(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "review-record.schema.json"
        data_path = REPO_ROOT / "tests" / "invalid" / "review-record.missing-drifted.json"
        with self.assertRaisesRegex(ValidationError, "missing required field 'drifted'"):
            validate_file(schema_path, data_path)

    def test_review_record_accepts_bounded_sub_agent_mode(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "review-record.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "reviews" / "review-record.json"
        validate_file(schema_path, data_path)

    def test_review_record_accepts_fallback_separated_pass_mode(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "review-record.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "reviews" / "review-record.json"
        record = load_json(data_path)
        record["reviewer_execution"]["execution_mode"] = "fallback_separated_pass"
        schema = load_json(schema_path)
        validate(record, schema, schema)

    def test_sound_prompt_plan_requires_emotional_tension_contract(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "sound-prompt-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-suno" / "sound-prompt-plan.json"
        record = load_json(data_path)
        del record["emotional_tension_contract"]
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "missing required field 'emotional_tension_contract'"):
            validate(record, schema, schema)

    def test_prompt_branch_requires_branch_emotional_tension_preservation(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "prompt-branch-set.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-image" / "prompt-branch-set.json"
        record = load_json(data_path)
        del record["branches"][0]["emotional_tension_preservation"]
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "missing required field 'emotional_tension_preservation'"):
            validate(record, schema, schema)

    def test_review_record_requires_emotional_tension_review(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "review-record.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "reviews" / "review-record.json"
        record = load_json(data_path)
        del record["emotional_tension_review"]
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "missing required field 'emotional_tension_review'"):
            validate(record, schema, schema)

    def test_review_record_requires_tension_intensity_assessments(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "review-record.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "reviews" / "review-record.json"
        record = load_json(data_path)
        del record["emotional_tension_review"]["tension_intensity_assessments"]
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "missing required field 'tension_intensity_assessments'"):
            validate(record, schema, schema)


if __name__ == "__main__":
    unittest.main()
