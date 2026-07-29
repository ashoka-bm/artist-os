from __future__ import annotations

import unittest
from pathlib import Path

from artist_os_schema_validator import (
    REPO_ROOT,
    ValidationError,
    iter_validation_targets,
    load_json,
    validate,
    validate_file,
)


LONG_WORK_SUPPORT = "long_work_stewardship"
WORKFLOW_SCALE_SCHEMA_NAMES = {
    "beat-plan.schema.json",
    "image-medium-plan.schema.json",
    "sound-medium-plan.schema.json",
    "text-medium-plan.schema.json",
    "video-medium-plan.schema.json",
}


def routing_support_overlap(record: dict) -> set[str]:
    routing = record["workflow_scale_routing"]
    return set(routing["activated_supports"]) & set(routing["skipped_supports"])


def routing_recommended_skip_overlap(record: dict) -> set[str]:
    routing = record["workflow_scale_routing"]
    return set(routing["recommended_supports"]) & set(routing["skipped_supports"])


class SchemaValidationTests(unittest.TestCase):
    def test_one_of_requires_exactly_one_match(self) -> None:
        schema = {
            "oneOf": [
                {"type": "string"},
                {"type": "string", "minLength": 1},
            ],
        }
        with self.assertRaisesRegex(ValidationError, "matched 2 oneOf branches"):
            validate("ambiguous", schema, schema)

    def test_date_time_format_rejects_invalid_or_naive_values(self) -> None:
        schema = {"type": "string", "format": "date-time"}
        for value in [
            "not-a-date",
            "2026-07-29T12:00:00",
            "20260729T120000+0000",
            "2026-W31-3T12:00:00+00:00",
            "2026-07-29T12:00:00+00:00:30",
        ]:
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValidationError, "valid RFC 3339 date-time"):
                    validate(value, schema, schema)

    def test_object_property_count_is_enforced(self) -> None:
        schema = {
            "type": "object",
            "minProperties": 2,
            "maxProperties": 2,
        }
        with self.assertRaisesRegex(ValidationError, "fewer than 2 properties"):
            validate({"left": 1}, schema, schema)
        with self.assertRaisesRegex(ValidationError, "more than 2 properties"):
            validate({"left": 1, "right": 2, "extra": 3}, schema, schema)

    def test_schema_valued_additional_properties_are_validated(self) -> None:
        schema = {
            "type": "object",
            "properties": {"known": {"type": "string"}},
            "additionalProperties": {"type": "integer"},
        }
        validate({"known": "yes", "dynamic": 1}, schema, schema)
        with self.assertRaisesRegex(ValidationError, r"\$\.dynamic: expected integer"):
            validate({"known": "yes", "dynamic": "no"}, schema, schema)

    def test_unsupported_schema_keyword_fails_closed(self) -> None:
        schema = {
            "oneOf": [
                {"type": "string"},
                {"type": "integer", "futureKeyword": True},
            ],
        }
        with self.assertRaisesRegex(ValidationError, "unsupported schema keyword"):
            validate("value", schema, schema)

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
        record["reviewer_execution"]["fallback_reason"] = "host_cannot_spawn_sub_agent"
        schema = load_json(schema_path)
        validate(record, schema, schema)

    def test_review_record_rejects_fallback_without_reason(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "review-record.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "reviews" / "review-record.json"
        record = load_json(data_path)
        record["reviewer_execution"]["execution_mode"] = "fallback_separated_pass"
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "missing required field 'fallback_reason'"):
            validate(record, schema, schema)

    def test_review_record_rejects_fallback_reason_for_bounded_sub_agent(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "review-record.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "reviews" / "review-record.json"
        record = load_json(data_path)
        record["reviewer_execution"]["fallback_reason"] = "host_cannot_spawn_sub_agent"
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "matched a schema it should not"):
            validate(record, schema, schema)

    def test_fallback_review_record_fixture_validates(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "review-record.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "reviews" / "fallback-review-record.json"
        record = load_json(data_path)
        self.assertEqual(record["reviewer_execution"]["execution_mode"], "fallback_separated_pass")
        self.assertTrue(record["reviewer_execution"]["sub_agent_required"])
        self.assertIn(
            record["reviewer_execution"]["fallback_reason"],
            ["host_cannot_spawn_sub_agent", "tool_policy_blocks_sub_agent_spawn"],
        )
        validate_file(schema_path, data_path)

    def test_sound_prompt_plan_requires_emotional_tension_contract(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "sound-prompt-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-suno" / "sound-prompt-plan.json"
        record = load_json(data_path)
        del record["emotional_tension_contract"]
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "missing required field 'emotional_tension_contract'"):
            validate(record, schema, schema)

    def test_sound_medium_plan_accepts_medium_output_shape_recommendation(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "sound-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-suno" / "sound-medium-plan.json"
        record = load_json(data_path)
        record["medium_output_shape_recommendation"] = {
            "requested_shape": None,
            "recommended_shape": "song",
            "accepted_shape": "song",
            "rationale": "One compact song can hold the threshold beat without needing a sequence.",
            "alternatives_considered": ["instrumental_track", "sound_sequence"],
            "tradeoffs": [
                "An instrumental track would preserve mood but lose the requested lyric-bearing pressure.",
                "A sound sequence would over-expand a single threshold beat."
            ],
            "conflict": {
                "has_conflict": False,
                "conflict_summary": None,
                "resolution": "not_needed",
                "gate_decision_id": None
            }
        }
        schema = load_json(schema_path)
        validate(record, schema, schema)

    def test_sound_output_shape_recommendation_accepts_sequence_when_sequence_plan_is_true(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "sound-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-suno" / "sound-medium-plan.json"
        record = load_json(data_path)
        record["story_mode"] = "sequence"
        record["sequence_plan"] = {
            "is_sequence": True,
            "requires_sequence_approval": True,
            "sequence_summary": "Three related sound works preserve departure, rupture, and residue as separate movements."
        }
        record["medium_output_shape_recommendation"] = {
            "requested_shape": "song",
            "recommended_shape": "sound_sequence",
            "accepted_shape": "sound_sequence",
            "rationale": "The Beat Plan needs separate sound works rather than one track arrangement.",
            "alternatives_considered": ["song", "cinematic_score"],
            "tradeoffs": [
                "A single song would compress too many turns into one hook.",
                "A cinematic score would keep continuity but blur the separate movement approvals."
            ],
            "conflict": {
                "has_conflict": True,
                "conflict_summary": "The requested song is smaller than the story movement needs.",
                "resolution": "accepted_recommendation",
                "gate_decision_id": "gate_sound_shape_sequence"
            }
        }
        schema = load_json(schema_path)
        validate(record, schema, schema)

    def test_sound_output_shape_recommendation_must_match_work_type_for_single_work(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "sound-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-suno" / "sound-medium-plan.json"
        record = load_json(data_path)
        record["medium_output_shape_recommendation"] = {
            "requested_shape": "song",
            "recommended_shape": "instrumental_track",
            "accepted_shape": "instrumental_track",
            "rationale": "Invalid: accepted shape must match the concrete sound work type.",
            "alternatives_considered": ["song"],
            "tradeoffs": ["Invalid shape mismatch guard."],
            "conflict": {
                "has_conflict": False,
                "conflict_summary": None,
                "resolution": "not_needed",
                "gate_decision_id": None
            }
        }
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "expected const 'instrumental_track'"):
            validate(record, schema, schema)

    def test_sound_output_shape_recommendation_rejects_story_or_image_shape(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "sound-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-suno" / "sound-medium-plan.json"
        record = load_json(data_path)
        record["medium_output_shape_recommendation"] = {
            "requested_shape": "single_image",
            "recommended_shape": "three_part_sequence",
            "accepted_shape": "three_part_sequence",
            "rationale": "Invalid: Story Mode and image shapes must not become sound output shapes.",
            "alternatives_considered": ["song"],
            "tradeoffs": ["Invalid shape guard."],
            "conflict": {
                "has_conflict": False,
                "conflict_summary": None,
                "resolution": "not_needed",
                "gate_decision_id": None
            }
        }
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "not one of"):
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

    def test_long_work_stewardship_fixtures_validate(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "long-work-stewardship-record.schema.json"
        fixture_paths = [
            REPO_ROOT / "tests" / "fixtures" / "long-work" / "foundation-stewardship-record.json",
            REPO_ROOT / "tests" / "fixtures" / "long-work" / "deactivated-stewardship-record.json",
            REPO_ROOT / "tests" / "fixtures" / "long-work" / "album-stewardship-record.json",
            REPO_ROOT / "tests" / "fixtures" / "long-work" / "image-series-stewardship-record.json",
            REPO_ROOT / "tests" / "fixtures" / "long-work" / "text-stewardship-record.json",
            REPO_ROOT / "tests" / "fixtures" / "long-work" / "cumulative-text-rehearsal" / "text-stewardship-record.json",
        ]
        for data_path in fixture_paths:
            with self.subTest(data=data_path.relative_to(REPO_ROOT)):
                validate_file(schema_path, data_path)

    def test_stewardship_activation_reason_accepts_length_floor_fields(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "long-work-stewardship-record.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "long-work" / "foundation-stewardship-record.json"
        record = load_json(data_path)
        self.assertTrue(record["activation_reason"]["meets_length_floor"])
        self.assertEqual(
            record["activation_reason"]["length_floor_override"],
            {"overridden": False, "rationale": ""},
        )
        schema = load_json(schema_path)
        validate(record, schema, schema)

    def test_stewardship_record_requires_activation_summary(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "long-work-stewardship-record.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "long-work" / "foundation-stewardship-record.json"
        record = load_json(data_path)
        del record["long_work_stewardship_activation"]
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "missing required field 'long_work_stewardship_activation'"):
            validate(record, schema, schema)

    def test_stewardship_record_rejects_paused_status(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "long-work-stewardship-record.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "long-work" / "foundation-stewardship-record.json"
        record = load_json(data_path)
        record["stewardship_status"] = "paused"
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "not one of"):
            validate(record, schema, schema)

    def test_deactivated_stewardship_record_requires_deactivation_reason(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "long-work-stewardship-record.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "long-work" / "deactivated-stewardship-record.json"
        record = load_json(data_path)
        record["long_work_stewardship_activation"]["deactivation_reason"] = ""
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "deactivation reason"):
            validate(record, schema, schema)

    def test_stewardship_activation_reason_requires_meets_length_floor(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "long-work-stewardship-record.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "long-work" / "foundation-stewardship-record.json"
        record = load_json(data_path)
        del record["activation_reason"]["meets_length_floor"]
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "missing required field 'meets_length_floor'"):
            validate(record, schema, schema)

    def test_stewardship_activation_reason_requires_length_floor_override(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "long-work-stewardship-record.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "long-work" / "foundation-stewardship-record.json"
        record = load_json(data_path)
        del record["activation_reason"]["length_floor_override"]
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "missing required field 'length_floor_override'"):
            validate(record, schema, schema)

    def test_stewardship_activation_reason_requires_cumulative_dependency(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "long-work-stewardship-record.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "long-work" / "foundation-stewardship-record.json"
        record = load_json(data_path)
        record["activation_reason"]["requires_part_to_part_dependency"] = False
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "requires cumulative dependency"):
            validate(record, schema, schema)

    def test_stewardship_activation_reason_requires_length_floor_or_override(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "long-work-stewardship-record.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "long-work" / "foundation-stewardship-record.json"
        record = load_json(data_path)
        record["activation_reason"]["meets_length_floor"] = False
        record["activation_reason"]["length_floor_override"] = {
            "overridden": False,
            "rationale": "",
        }
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "requires the length floor"):
            validate(record, schema, schema)

    def test_stewardship_activation_reason_length_floor_override_requires_rationale(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "long-work-stewardship-record.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "long-work" / "foundation-stewardship-record.json"
        record = load_json(data_path)
        record["activation_reason"]["meets_length_floor"] = False
        record["activation_reason"]["length_floor_override"] = {
            "overridden": True,
            "rationale": "",
        }
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "override rationale is required"):
            validate(record, schema, schema)

    def test_album_release_package_plan_fixture_validates(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "release-package-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "release-packages" / "album-release-package-plan.json"
        validate_file(schema_path, data_path)

    def test_cross_medium_plan_fixture_validates(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "cross-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "release-packages" / "cross-medium-plan.json"
        validate_file(schema_path, data_path)

    def test_cross_medium_plan_requires_exactly_one_primary(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "cross-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "release-packages" / "cross-medium-plan.json"
        schema = load_json(schema_path)
        record = load_json(data_path)
        record["media"][1]["medium_role"] = "primary"
        record["media"][1]["serves_primary"] = None
        with self.assertRaisesRegex(
            ValidationError,
            "matches fewer than minContains|matches more than maxContains",
        ):
            validate(record, schema, schema)

    def test_cross_medium_plan_rejects_a_missing_primary_role(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "cross-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "release-packages" / "cross-medium-plan.json"
        schema = load_json(schema_path)
        record = load_json(data_path)
        record["media"][0]["medium_role"] = "supporting"
        record["media"][0]["serves_primary"] = record["primary_medium"]
        with self.assertRaisesRegex(ValidationError, "matches fewer than minContains"):
            validate(record, schema, schema)

    def test_cross_medium_plan_requires_two_media(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "cross-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "release-packages" / "cross-medium-plan.json"
        schema = load_json(schema_path)
        record = load_json(data_path)
        record["media"] = [record["media"][0]]
        with self.assertRaisesRegex(ValidationError, "has fewer than 2 items|derived_from media must match active media"):
            validate(record, schema, schema)

    def test_cross_medium_plan_effective_scale_must_be_max(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "cross-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "release-packages" / "cross-medium-plan.json"
        schema = load_json(schema_path)
        record = load_json(data_path)
        record["effective_project_scale"]["scale_level"] = "structured_single_artifact"
        with self.assertRaisesRegex(ValidationError, "Effective Project Scale must be the max"):
            validate(record, schema, schema)

    def test_cross_medium_plan_primary_medium_must_match_primary_role(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "cross-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "release-packages" / "cross-medium-plan.json"
        schema = load_json(schema_path)
        record = load_json(data_path)
        record["primary_medium"] = "audio"
        with self.assertRaisesRegex(
            ValidationError,
            "primary_medium 'audio' must equal the medium of the single primary-role media entry",
        ):
            validate(record, schema, schema)

    def test_cross_medium_plan_supporting_serves_primary_must_match(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "cross-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "release-packages" / "cross-medium-plan.json"
        schema = load_json(schema_path)
        record = load_json(data_path)
        record["media"][1]["serves_primary"] = "audio"
        with self.assertRaisesRegex(ValidationError, "serves_primary must equal primary_medium"):
            validate(record, schema, schema)

    def test_cross_medium_plan_primary_serves_primary_must_be_null(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "cross-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "release-packages" / "cross-medium-plan.json"
        schema = load_json(schema_path)
        record = load_json(data_path)
        record["media"][0]["serves_primary"] = "video"
        with self.assertRaisesRegex(ValidationError, "serves_primary must be null"):
            validate(record, schema, schema)

    def test_cross_medium_plan_rejects_duplicate_media_entries(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "cross-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "release-packages" / "cross-medium-plan.json"
        schema = load_json(schema_path)
        record = load_json(data_path)
        record["media"].append(dict(record["media"][1]))
        with self.assertRaisesRegex(ValidationError, "must not duplicate media entries"):
            validate(record, schema, schema)

    def test_cross_medium_plan_production_order_must_match_active_media(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "cross-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "release-packages" / "cross-medium-plan.json"
        schema = load_json(schema_path)
        record = load_json(data_path)
        record["production_order"].append(
            {
                "order_index": 3,
                "medium": "text",
                "step_summary": "Unexpected text work.",
                "status": "planned",
                "required_before_media": [],
            }
        )
        with self.assertRaisesRegex(ValidationError, "Production order media must match active media"):
            validate(record, schema, schema)

    def test_cross_medium_plan_production_dependencies_must_reference_active_media(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "cross-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "release-packages" / "cross-medium-plan.json"
        schema = load_json(schema_path)
        record = load_json(data_path)
        record["production_order"][0]["required_before_media"] = ["text"]
        with self.assertRaisesRegex(ValidationError, "required_before_media must only reference active media"):
            validate(record, schema, schema)

    def test_cross_medium_plan_derived_from_must_match_active_media(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "cross-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "release-packages" / "cross-medium-plan.json"
        schema = load_json(schema_path)
        record = load_json(data_path)
        record["effective_project_scale"]["derived_from"].append(
            {"medium": "text", "medium_scale_level": "compact_artifact"}
        )
        with self.assertRaisesRegex(ValidationError, "derived_from media must match active media"):
            validate(record, schema, schema)

    # --- Cross-Medium Plan: planned deliverables and shared references ---
    #
    # The exactly-one-primary, duplicate-media, primary-role, serves_primary,
    # derived_from, and production-order negatives are already covered above; these
    # cover only the fields this slice adds. The schema pins each entry's shape; the
    # cross-field rules live in validate_cross_medium_plan_contract because the local
    # validator has no keyword that can express them.

    CMP_SCHEMA = REPO_ROOT / "schemas" / "cross-medium-plan.schema.json"
    CMP_FIXTURE = REPO_ROOT / "tests" / "fixtures" / "cross-medium" / "article-with-photos-rehearsal" / "cross-medium-plan-article.json"

    def cross_medium_rehearsal(self) -> tuple[dict, dict]:
        return load_json(self.CMP_SCHEMA), load_json(self.CMP_FIXTURE)

    def test_cross_medium_rehearsal_plan_validates(self) -> None:
        validate_file(self.CMP_SCHEMA, self.CMP_FIXTURE)

    def test_cross_medium_rehearsal_supporting_image_plan_validates(self) -> None:
        validate_file(
            REPO_ROOT / "schemas" / "image-medium-plan.schema.json",
            REPO_ROOT / "tests" / "fixtures" / "cross-medium" / "article-with-photos-rehearsal" / "image-medium-plan.json",
        )

    def test_cross_medium_plan_requires_planned_deliverables(self) -> None:
        schema, record = self.cross_medium_rehearsal()
        del record["planned_deliverables"]
        with self.assertRaisesRegex(ValidationError, "missing required field 'planned_deliverables'"):
            validate(record, schema, schema)

    def test_cross_medium_plan_requires_shared_references_key(self) -> None:
        schema, record = self.cross_medium_rehearsal()
        del record["shared_references"]
        with self.assertRaisesRegex(ValidationError, "missing required field 'shared_references'"):
            validate(record, schema, schema)

    def test_cross_medium_plan_allows_empty_shared_references(self) -> None:
        # The Shared Story Spine may be the only shared material; an empty list is honest.
        schema, record = self.cross_medium_rehearsal()
        record["shared_references"] = []
        validate(record, schema, schema)

    def test_cross_medium_plan_rejects_duplicate_deliverable_ids(self) -> None:
        schema, record = self.cross_medium_rehearsal()
        record["planned_deliverables"][1]["deliverable_id"] = record["planned_deliverables"][0]["deliverable_id"]
        with self.assertRaisesRegex(ValidationError, "must not duplicate deliverable_id"):
            validate(record, schema, schema)

    def test_cross_medium_plan_deliverables_must_name_active_media(self) -> None:
        schema, record = self.cross_medium_rehearsal()
        record["planned_deliverables"][1]["medium"] = "audio"
        with self.assertRaisesRegex(ValidationError, "deliverables must only reference active media"):
            validate(record, schema, schema)

    def test_cross_medium_plan_requires_a_deliverable_for_every_active_medium(self) -> None:
        # The plan is the Package Compilation checklist; an activated medium that
        # promises nothing cannot be checked off later.
        schema, record = self.cross_medium_rehearsal()
        record["planned_deliverables"] = [
            item for item in record["planned_deliverables"] if item["medium"] != "image"
        ]
        with self.assertRaisesRegex(ValidationError, "needs at least one planned deliverable"):
            validate(record, schema, schema)

    def test_cross_medium_plan_complete_deliverable_requires_output_record(self) -> None:
        schema, record = self.cross_medium_rehearsal()
        record["planned_deliverables"][0]["output_record_id"] = None
        with self.assertRaisesRegex(ValidationError, "complete deliverable .* requires an output_record_id"):
            validate(record, schema, schema)

    def test_cross_medium_plan_deliverable_id_pattern_is_enforced(self) -> None:
        schema, record = self.cross_medium_rehearsal()
        record["planned_deliverables"][0]["deliverable_id"] = "civic_garden_article_text"
        with self.assertRaisesRegex(ValidationError, "does not match"):
            validate(record, schema, schema)

    def test_cross_medium_plan_rejects_duplicate_shared_reference_ids(self) -> None:
        schema, record = self.cross_medium_rehearsal()
        duplicate = dict(record["shared_references"][0])
        record["shared_references"].append(duplicate)
        with self.assertRaisesRegex(ValidationError, "must not duplicate shared_reference_id"):
            validate(record, schema, schema)

    def test_shared_reference_must_serve_at_least_two_media(self) -> None:
        # A single-medium reference belongs to that Medium Plan, not the coordinator.
        schema, record = self.cross_medium_rehearsal()
        record["shared_references"][0]["shared_with_media"] = ["text"]
        with self.assertRaisesRegex(ValidationError, "fewer than 2 items"):
            validate(record, schema, schema)

    def test_shared_reference_media_must_be_active(self) -> None:
        schema, record = self.cross_medium_rehearsal()
        record["shared_references"][0]["shared_with_media"] = ["text", "audio"]
        with self.assertRaisesRegex(ValidationError, "must only reference active media"):
            validate(record, schema, schema)

    def test_shared_reference_rejects_duplicate_media(self) -> None:
        schema, record = self.cross_medium_rehearsal()
        record["shared_references"][0]["shared_with_media"] = ["text", "text"]
        with self.assertRaisesRegex(ValidationError, "must not duplicate media"):
            validate(record, schema, schema)

    # --- Cross-Medium Plan approval and Mixed-Media Critic vocabulary ---

    GATE_SCHEMA = REPO_ROOT / "schemas" / "gate-decision.schema.json"
    APPROVAL_GATE = REPO_ROOT / "tests" / "fixtures" / "cross-medium" / "article-with-photos-rehearsal" / "cross-medium-plan-approval-gate.json"
    COMPLETENESS_GATE = REPO_ROOT / "tests" / "fixtures" / "cross-medium" / "article-with-photos-rehearsal" / "package-format-completeness-gate.json"
    WAIVER_GATE = REPO_ROOT / "tests" / "fixtures" / "cross-medium" / "article-with-photos-rehearsal" / "package-slot-waiver-gate.json"
    MIXED_MEDIA_REVIEW = REPO_ROOT / "tests" / "fixtures" / "cross-medium" / "article-with-photos-rehearsal" / "mixed-media-critic-review-record.json"

    def test_cross_medium_gate_and_review_fixtures_validate(self) -> None:
        for schema_path, data_path in [
            (self.GATE_SCHEMA, self.APPROVAL_GATE),
            (self.GATE_SCHEMA, self.COMPLETENESS_GATE),
            (self.GATE_SCHEMA, self.WAIVER_GATE),
            (REPO_ROOT / "schemas" / "review-record.schema.json", self.MIXED_MEDIA_REVIEW),
        ]:
            with self.subTest(data=data_path.name):
                validate_file(schema_path, data_path)

    def test_cross_medium_approval_gate_requires_the_plan_ref(self) -> None:
        schema = load_json(self.GATE_SCHEMA)
        record = load_json(self.APPROVAL_GATE)
        record["upstream_refs"] = [
            ref for ref in record["upstream_refs"] if ref["ref_type"] != "cross_medium_plan"
        ]
        with self.assertRaisesRegex(ValidationError, "matches fewer than minContains"):
            validate(record, schema, schema)

    def test_cross_medium_approval_gate_requires_the_review_ref(self) -> None:
        # Approval cannot precede Mixed-Media Critic Review, so the gate must name it.
        schema = load_json(self.GATE_SCHEMA)
        record = load_json(self.APPROVAL_GATE)
        record["upstream_refs"] = [
            ref for ref in record["upstream_refs"] if ref["ref_type"] != "review_record"
        ]
        with self.assertRaisesRegex(ValidationError, "matches fewer than minContains"):
            validate(record, schema, schema)

    def test_mixed_media_review_of_a_plan_must_name_the_beat_plan(self) -> None:
        # Executable form of "the Shared Story Spine is reused by id".
        schema = load_json(REPO_ROOT / "schemas" / "review-record.schema.json")
        record = load_json(self.MIXED_MEDIA_REVIEW)
        record["upstream_context"]["governing_refs"] = [
            ref for ref in record["upstream_context"]["governing_refs"] if ref["ref_type"] != "beat_plan"
        ]
        with self.assertRaisesRegex(ValidationError, "matches fewer than minContains"):
            validate(record, schema, schema)

    def test_cross_medium_plan_review_must_be_the_mixed_media_critic(self) -> None:
        schema = load_json(REPO_ROOT / "schemas" / "review-record.schema.json")
        record = load_json(self.MIXED_MEDIA_REVIEW)
        record["review_role"] = "story_critic"
        with self.assertRaisesRegex(ValidationError, "expected const 'mixed_media_critic'"):
            validate(record, schema, schema)

    # --- Package Format Selection And Completeness Gate ---

    def test_package_gate_requires_the_completeness_block(self) -> None:
        schema = load_json(self.GATE_SCHEMA)
        record = load_json(self.COMPLETENESS_GATE)
        del record["package_completeness"]
        with self.assertRaisesRegex(ValidationError, "missing required field 'package_completeness'"):
            validate(record, schema, schema)

    def test_completeness_block_belongs_only_to_the_package_gate(self) -> None:
        schema = load_json(self.GATE_SCHEMA)
        record = load_json(self.COMPLETENESS_GATE)
        record["gate_type"] = "output_acceptance"
        with self.assertRaisesRegex(
            ValidationError, "expected const 'package_format_selection_and_completeness'"
        ):
            validate(record, schema, schema)

    def test_waiver_verdict_requires_a_named_slot(self) -> None:
        # "A general 'ship anyway' decision does not waive unnamed missing deliverables."
        schema = load_json(self.GATE_SCHEMA)
        record = load_json(self.WAIVER_GATE)
        del record["package_completeness"]["waived_slot_id"]
        with self.assertRaisesRegex(ValidationError, "missing required field 'waived_slot_id'"):
            validate(record, schema, schema)

    def test_named_slot_requires_the_waiver_verdict(self) -> None:
        schema = load_json(self.GATE_SCHEMA)
        record = load_json(self.COMPLETENESS_GATE)
        record["package_completeness"]["waived_slot_id"] = "inline_photo"
        with self.assertRaisesRegex(ValidationError, "expected const 'required_slot_waived'"):
            validate(record, schema, schema)

    def test_package_gate_rejects_unknown_completeness_verdict(self) -> None:
        schema = load_json(self.GATE_SCHEMA)
        record = load_json(self.COMPLETENESS_GATE)
        record["package_completeness"]["completeness_verdict"] = "ship_anyway"
        with self.assertRaisesRegex(ValidationError, "is not one of"):
            validate(record, schema, schema)

    def test_release_package_plan_still_validates_after_seam_annotation(self) -> None:
        # Slice 6 (ADR 0014 D11) added a non-functional top-level description; the
        # shipped Album v1 record must still validate (the only schema edit this slice makes).
        schema_path = REPO_ROOT / "schemas" / "release-package-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "release-packages" / "album-release-package-plan.json"
        validate_file(schema_path, data_path)

    def test_release_package_plan_title_unchanged(self) -> None:
        # The validator dispatches validate_release_package_plan_contract on this exact
        # title; a rename would silently disable every Album v1 cross-item invariant.
        schema = load_json(REPO_ROOT / "schemas" / "release-package-plan.schema.json")
        self.assertEqual(schema["title"], "ReleasePackagePlan")

    def test_release_package_plan_records_seam_migration(self) -> None:
        # The ADR 0014 D11 plan/output seam is recorded in the schema itself, not only in prose.
        schema = load_json(REPO_ROOT / "schemas" / "release-package-plan.schema.json")
        description = schema.get("description", "")
        for marker in ("Cross-Medium Plan", "Asset Package", "ADR 0014"):
            with self.subTest(marker=marker):
                self.assertIn(marker, description)

    def test_character_template_fixture_validates(self) -> None:
        validate_file(
            REPO_ROOT / "schemas" / "character-template.schema.json",
            REPO_ROOT / "tests" / "fixtures" / "characters" / "character-template.json",
        )

    def test_seedance_prompt_package_fixture_validates(self) -> None:
        validate_file(
            REPO_ROOT / "schemas" / "seedance-prompt-package.schema.json",
            REPO_ROOT / "tests" / "fixtures" / "video-journey" / "seedance-prompt-package.json",
        )

    def test_seedance_prompt_package_requires_english_policy(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "seedance-prompt-package.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "video-journey" / "seedance-prompt-package.json"
        record = load_json(data_path)
        record["language_policy"]["prompt_language"] = "Chinese"
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "expected const 'English'"):
            validate(record, schema, schema)

    def test_seedance_prompt_package_rejects_chinese_prompt_text(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "seedance-prompt-package.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "video-journey" / "seedance-prompt-package.json"
        record = load_json(data_path)
        record["clip_batches"][0]["prompt_text"] = "镜头缓慢推进到半开的门。"
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "matched a schema it should not"):
            validate(record, schema, schema)

    def test_visual_reference_sheet_plan_fixture_validates(self) -> None:
        validate_file(
            REPO_ROOT / "schemas" / "visual-reference-sheet-plan.schema.json",
            REPO_ROOT / "tests" / "fixtures" / "characters" / "visual-reference-sheet-plan.json",
        )

    def test_reference_inventory_fixture_validates(self) -> None:
        validate_file(
            REPO_ROOT / "schemas" / "reference-inventory.schema.json",
            REPO_ROOT / "tests" / "fixtures" / "references" / "reference-inventory.json",
        )

    def test_reference_inventory_review_only_images_are_not_provider_inputs(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "reference-inventory.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "references" / "reference-inventory.json"
        record = load_json(data_path)
        image = record["subjects"][0]["expected_outputs"][0]
        image["review_only"] = True
        image["provider_input_allowed"] = False
        image["provider_role_hints"] = ["review_only"]
        image["allowed_use_scope"] = ["human_review_only", "internal_review"]
        schema = load_json(schema_path)
        validate(record, schema, schema)

    def test_reference_inventory_rejects_review_only_provider_input(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "reference-inventory.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "references" / "reference-inventory.json"
        record = load_json(data_path)
        image = record["subjects"][0]["expected_outputs"][0]
        image["review_only"] = True
        image["provider_input_allowed"] = True
        image["allowed_use_scope"] = ["human_review_only", "internal_review"]
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "expected const False"):
            validate(record, schema, schema)

    def test_reference_inventory_rejects_review_only_provider_scope(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "reference-inventory.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "references" / "reference-inventory.json"
        record = load_json(data_path)
        image = record["subjects"][0]["expected_outputs"][0]
        image["review_only"] = True
        image["provider_input_allowed"] = False
        image["allowed_use_scope"] = ["human_review_only", "provider_input"]
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "matched a schema it should not"):
            validate(record, schema, schema)

    def test_reference_inventory_rejects_unknown_lifecycle_status(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "reference-inventory.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "references" / "reference-inventory.json"
        record = load_json(data_path)
        record["subjects"][0]["subject_status"] = "maybe_reference"
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "not one of"):
            validate(record, schema, schema)

    def test_reference_inventory_accepts_empty_scan_inventory(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "reference-inventory.schema.json"
        record = load_json(REPO_ROOT / "tests" / "fixtures" / "references" / "reference-inventory.json")
        record["subjects"] = []
        record["medium_plan_refs"] = []
        record["scan_history"] = [
            {
                "scan_id": "refscan_empty_project",
                "scanned_at": "2026-06-25T18:55:00Z",
                "scan_scope": "project",
                "medium_plan_ref": None,
                "summary": "Continuity scan found no promoted visual reference subjects.",
                "candidates_found": 0,
            }
        ]
        record["traceability_summary"] = [
            {
                "source_type": "continuity_scan",
                "source_ref": "refscan_empty_project",
                "note": "The empty inventory still records the policy and scan result.",
            }
        ]
        schema = load_json(schema_path)
        validate(record, schema, schema)

    def test_reference_inventory_tracks_partial_strategy_missing_outputs_and_variants(self) -> None:
        record = load_json(REPO_ROOT / "tests" / "fixtures" / "references" / "reference-inventory.json")
        hallway = record["subjects"][1]
        character = record["subjects"][0]

        self.assertEqual(hallway["strategy_status"], "accepted_partial")
        self.assertEqual(hallway["package_readiness"], "planned")
        self.assertEqual(
            hallway["missing_outputs"],
            ["location_establishing_angle", "location_reverse_angle", "location_functional_angle"],
        )
        self.assertEqual(character["variants"][0]["variant_kind"], "wardrobe_variant")
        self.assertEqual(
            character["variants"][0]["expected_outputs"][0]["reference_kind"],
            "wardrobe_variant",
        )

    def test_promoted_visual_reference_sheet_package_fixtures_validate(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "visual-reference-sheet-plan.schema.json"
        fixtures = [
            (
                REPO_ROOT / "tests" / "fixtures" / "characters" / "promoted-door-keeper" / "visual-reference-sheet-plan.json",
                "character",
                "multi_image_reference_package",
                {
                    "character_identity_plate": 1,
                    "character_turnaround_sheet": 1,
                    "character_macro_detail_card": 1,
                },
            ),
            (
                REPO_ROOT / "tests" / "fixtures" / "locations" / "hallway-threshold" / "visual-reference-sheet-plan.json",
                "setting",
                "three_angle_reference_package",
                {
                    "location_establishing_angle": 1,
                    "location_reverse_angle": 1,
                    "location_functional_angle": 1,
                },
            ),
            (
                REPO_ROOT / "tests" / "fixtures" / "objects" / "old-tv" / "visual-reference-sheet-plan.json",
                "object",
                "multi_section_reference_sheet",
                {"object_multi_angle_sheet": 1},
            ),
        ]
        for data_path, sheet_type, layout_type, expected_roles in fixtures:
            with self.subTest(data=data_path.relative_to(REPO_ROOT)):
                validate_file(schema_path, data_path)
                record = load_json(data_path)
                self.assertEqual(record["reference_sheet_type"], sheet_type)
                self.assertEqual(record["view_layout"]["layout_type"], layout_type)
                actual_roles = {
                    output["output_role"]: output["image_count"]
                    for output in record["reference_outputs"]
                }
                self.assertEqual(actual_roles, expected_roles)
                self.assertEqual(record["output_record_refs"], [])

    def test_visual_reference_sheet_requires_reference_outputs(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "visual-reference-sheet-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "characters" / "visual-reference-sheet-plan.json"
        record = load_json(data_path)
        del record["reference_outputs"]
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "missing required field 'reference_outputs'"):
            validate(record, schema, schema)

    def test_visual_reference_sheet_accepts_character_variant_output_roles(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "visual-reference-sheet-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "characters" / "visual-reference-sheet-plan.json"
        roles = [
            "character_expression_sheet",
            "character_pose_action_sheet",
            "character_wardrobe_sheet",
            "character_style_variant_sheet",
        ]
        schema = load_json(schema_path)
        for role in roles:
            with self.subTest(role=role):
                record = load_json(data_path)
                record["reference_outputs"][0]["output_role"] = role
                validate(record, schema, schema)

    def test_reference_strategy_accepts_partial_acceptance_across_mediums(self) -> None:
        fixtures = [
            (
                "image-medium-plan.schema.json",
                "tests/fixtures/text-to-image/image-medium-plan.json",
                ["character_reference_strategy", "visual_reference_sheet_strategy"],
            ),
            (
                "video-medium-plan.schema.json",
                "tests/fixtures/video-journey/video-medium-plan.json",
                ["character_reference_strategy", "visual_reference_sheet_strategy"],
            ),
            (
                "text-medium-plan.schema.json",
                "tests/fixtures/text-journey/text-medium-plan.json",
                ["character_reference_strategy"],
            ),
            (
                "illustration-plan.schema.json",
                "tests/fixtures/illustration/illustration-plan.json",
                ["character_reference_strategy", "visual_reference_sheet_strategy"],
            ),
        ]
        for schema_name, fixture_path, strategy_fields in fixtures:
            with self.subTest(fixture=fixture_path):
                schema_path = REPO_ROOT / "schemas" / schema_name
                data_path = REPO_ROOT / fixture_path
                record = load_json(data_path)
                for field in strategy_fields:
                    if field not in record:
                        record[field] = {
                            "status": "accepted",
                            "decision_ref": "gate_reference_strategy_partial",
                            "visual_reference_sheet_plan_refs": ["vrs_selected_reference"],
                            "notes": "Artist accepted selected recommended reference subjects."
                        }
                        if field == "character_reference_strategy":
                            record[field]["character_template_refs"] = ["char_selected_reference"]
                    record[field]["status"] = "accepted_partial"
                    record[field]["notes"] = "Artist accepted selected recommended reference subjects."
                schema = load_json(schema_path)
                validate(record, schema, schema)

    def test_illustration_plan_fixture_validates(self) -> None:
        validate_file(
            REPO_ROOT / "schemas" / "illustration-plan.schema.json",
            REPO_ROOT / "tests" / "fixtures" / "illustration" / "illustration-plan.json",
        )

    def test_release_package_plan_v1_rejects_single_bundle(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "release-package-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "release-packages" / "album-release-package-plan.json"
        record = load_json(data_path)
        record["package_subtype"] = "single_bundle"
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "expected const 'album'"):
            validate(record, schema, schema)

    def test_release_package_plan_requires_album_systems_and_calibration(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "release-package-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "release-packages" / "album-release-package-plan.json"
        schema = load_json(schema_path)
        for required_field in ["album_sonic_system", "album_visual_system", "album_calibration"]:
            with self.subTest(required_field=required_field):
                record = load_json(data_path)
                del record[required_field]
                with self.assertRaisesRegex(ValidationError, f"missing required field '{required_field}'"):
                    validate(record, schema, schema)

    def test_release_package_plan_requires_package_level_album_cover(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "release-package-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "release-packages" / "album-release-package-plan.json"
        record = load_json(data_path)
        record["deliverables"] = [
            deliverable
            for deliverable in record["deliverables"]
            if deliverable["deliverable_type"] != "album_cover"
        ]
        schema = load_json(schema_path)
        with self.assertRaisesRegex(
            ValidationError,
            "requires exactly one required package-level album_cover deliverable",
        ):
            validate(record, schema, schema)

    def test_release_package_plan_requires_one_sound_deliverable_per_track(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "release-package-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "release-packages" / "album-release-package-plan.json"
        record = load_json(data_path)
        record["deliverables"] = [
            deliverable
            for deliverable in record["deliverables"]
            if not (
                deliverable["deliverable_type"] == "track_sound_prompt_plan"
                and deliverable["track_id"] == "track_door_02"
            )
        ]
        schema = load_json(schema_path)
        with self.assertRaisesRegex(
            ValidationError,
            "track 'track_door_02' requires exactly one required track_sound_prompt_plan deliverable",
        ):
            validate(record, schema, schema)

    def test_release_package_plan_requires_one_track_cover_deliverable_per_track(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "release-package-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "release-packages" / "album-release-package-plan.json"
        record = load_json(data_path)
        record["deliverables"] = [
            deliverable
            for deliverable in record["deliverables"]
            if not (
                deliverable["deliverable_type"] == "track_cover_image_prompt_plan"
                and deliverable["track_id"] == "track_door_03"
            )
        ]
        schema = load_json(schema_path)
        with self.assertRaisesRegex(
            ValidationError,
            "track 'track_door_03' requires exactly one required track_cover_image_prompt_plan deliverable",
        ):
            validate(record, schema, schema)

    def test_release_package_plan_track_cover_ref_must_match_deliverable(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "release-package-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "release-packages" / "album-release-package-plan.json"
        record = load_json(data_path)
        record["tracks"][0]["track_cover_deliverable_id"] = "deliv_track_02_cover"
        schema = load_json(schema_path)
        with self.assertRaisesRegex(
            ValidationError,
            "track 'track_door_01' track_cover_deliverable_id must reference its required Track Cover deliverable",
        ):
            validate(record, schema, schema)

    def test_release_package_plan_arc_album_requires_stewardship_refs(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "release-package-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "release-packages" / "album-release-package-plan.json"
        record = load_json(data_path)
        record["long_work_stewardship_record_ids"] = []
        schema = load_json(schema_path)
        with self.assertRaisesRegex(
            ValidationError,
            "arc_album requires at least one Long-Work Stewardship record id",
        ):
            validate(record, schema, schema)

    def test_release_package_plan_arc_album_requires_track_part_refs(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "release-package-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "release-packages" / "album-release-package-plan.json"
        record = load_json(data_path)
        record["tracks"][0]["album_beat_ref"]["long_work_part_id"] = None
        schema = load_json(schema_path)
        with self.assertRaisesRegex(
            ValidationError,
            "track 'track_door_01' requires a non-null long_work_part_id",
        ):
            validate(record, schema, schema)

    def test_release_package_plan_requires_all_album_calibration_subchecks(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "release-package-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "release-packages" / "album-release-package-plan.json"
        record = load_json(data_path)
        for subcheck in record["album_calibration"]["subchecks"]:
            if subcheck["subcheck_type"] == "visual_direction":
                subcheck["subcheck_type"] = "sonic_direction"
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "matches more than maxContains 1"):
            validate(record, schema, schema)

    def test_release_package_plan_rejects_missing_sound_visual_fit_subcheck(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "release-package-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "release-packages" / "album-release-package-plan.json"
        record = load_json(data_path)
        record["album_calibration"]["subchecks"] = [
            subcheck
            for subcheck in record["album_calibration"]["subchecks"]
            if subcheck["subcheck_type"] != "sound_visual_fit"
        ]
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "has fewer than 3 items|matches fewer than minContains 1"):
            validate(record, schema, schema)

    def test_review_record_accepts_long_work_reviewer(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "review-record.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "reviews" / "review-record.json"
        record = load_json(data_path)
        record["review_role"] = "long_work_reviewer"
        record["artifact_under_review"] = {
            "artifact_type": "long_work_stewardship",
            "artifact_id": "lws_door_left_lit_foundation",
            "path_or_ref": "tests/fixtures/long-work/foundation-stewardship-record.json",
        }
        record["upstream_context"]["governing_refs"].append(
            {
                "ref_type": "long_work_stewardship",
                "ref_id": "lws_door_left_lit_foundation",
                "path_or_ref": "tests/fixtures/long-work/foundation-stewardship-record.json",
            }
        )
        schema = load_json(schema_path)
        validate(record, schema, schema)

    def test_review_record_accepts_release_package_plan_review(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "review-record.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "reviews" / "review-record.json"
        record = load_json(data_path)
        record["review_role"] = "mixed_media_critic"
        record["artifact_under_review"] = {
            "artifact_type": "release_package_plan",
            "artifact_id": "rpp_door_left_lit_album",
            "path_or_ref": "tests/fixtures/release-packages/album-release-package-plan.json",
        }
        record["upstream_context"]["governing_refs"].append(
            {
                "ref_type": "release_package_plan",
                "ref_id": "rpp_door_left_lit_album",
                "path_or_ref": "tests/fixtures/release-packages/album-release-package-plan.json",
            }
        )
        schema = load_json(schema_path)
        validate(record, schema, schema)

    def test_review_record_accepts_illustration_plan_review(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "review-record.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "reviews" / "review-record.json"
        record = load_json(data_path)
        record["review_role"] = "illustration_plan_reviewer"
        record["artifact_under_review"] = {
            "artifact_type": "illustration_plan",
            "artifact_id": "ilp_threshold_picture_book",
            "path_or_ref": "tests/fixtures/illustration/illustration-plan.json",
        }
        record["upstream_context"]["governing_refs"].append(
            {
                "ref_type": "illustration_plan",
                "ref_id": "ilp_threshold_picture_book",
                "path_or_ref": "tests/fixtures/illustration/illustration-plan.json",
            }
        )
        schema = load_json(schema_path)
        validate(record, schema, schema)

    def test_text_form_schemas_accept_article(self) -> None:
        for schema_name in [
            "text-medium-plan.schema.json",
            "text-creative-brief.schema.json",
            "text-generation-plan.schema.json",
        ]:
            with self.subTest(schema=schema_name):
                schema = load_json(REPO_ROOT / "schemas" / schema_name)
                validate("article", schema["$defs"]["text_form"], schema)

    def test_gate_decision_accepts_long_work_checkpoint(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "gate-decision.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "gates" / "symbology-gate.json"
        record = load_json(data_path)
        record["gate_type"] = "long_work_checkpoint"
        record["upstream_refs"][0] = {
            "ref_type": "long_work_stewardship",
            "ref_id": "lws_door_left_lit_foundation",
            "path_or_ref": "tests/fixtures/long-work/foundation-stewardship-record.json",
        }
        schema = load_json(schema_path)
        validate(record, schema, schema)

    def test_gate_decision_accepts_release_package_gates(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "gate-decision.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "gates" / "symbology-gate.json"
        schema = load_json(schema_path)
        for gate_type in ["release_package_plan_approval", "album_calibration"]:
            with self.subTest(gate_type=gate_type):
                record = load_json(data_path)
                record["gate_type"] = gate_type
                record["upstream_refs"][0] = {
                    "ref_type": "release_package_plan",
                    "ref_id": "rpp_door_left_lit_album",
                    "path_or_ref": "tests/fixtures/release-packages/album-release-package-plan.json",
                }
                validate(record, schema, schema)

    def test_gate_decision_accepts_text_journey_gates(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "gate-decision.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "gates" / "symbology-gate.json"
        schema = load_json(schema_path)
        text_gate_types = [
            "research_grounding",
            "writing_method",
            "format_length",
            "text_form",
            "voice_pov",
            "structure",
            "fidelity_transformation",
            "publication_use",
            "review_presentation",
            "brief_approval",
            "draft_generation_approval",
        ]
        for gate_type in text_gate_types:
            with self.subTest(gate_type=gate_type):
                record = load_json(data_path)
                record["gate_type"] = gate_type
                validate(record, schema, schema)

    def test_gate_decision_accepts_character_and_illustration_gates(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "gate-decision.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "gates" / "symbology-gate.json"
        schema = load_json(schema_path)
        for gate_type, ref_type, ref_id, path in [
            (
                "character_reference_strategy",
                "character_template",
                "char_door_keeper",
                "tests/fixtures/characters/character-template.json",
            ),
            (
                "visual_reference_sheet_strategy",
                "visual_reference_sheet_plan",
                "vrs_door_keeper",
                "tests/fixtures/characters/visual-reference-sheet-plan.json",
            ),
            (
                "illustration_plan_approval",
                "illustration_plan",
                "ilp_threshold_picture_book",
                "tests/fixtures/illustration/illustration-plan.json",
            ),
        ]:
            with self.subTest(gate_type=gate_type):
                record = load_json(data_path)
                record["gate_type"] = gate_type
                record["upstream_refs"][0] = {
                    "ref_type": ref_type,
                    "ref_id": ref_id,
                    "path_or_ref": path,
                }
                validate(record, schema, schema)

    def test_gate_decision_accepts_video_journey_gates(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "gate-decision.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "gates" / "symbology-gate.json"
        schema = load_json(schema_path)
        video_gate_types = [
            "video_format",
            "scene_sequence",
            "shot_logic",
            "motion_pacing_transition",
            "audio_posture",
        ]
        for gate_type in video_gate_types:
            with self.subTest(gate_type=gate_type):
                record = load_json(data_path)
                record["gate_type"] = gate_type
                validate(record, schema, schema)

    def test_text_creative_brief_requires_review_and_brief_approval_refs(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "text-creative-brief.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-journey" / "text-creative-brief.json"
        record = load_json(data_path)
        record.pop("approval_refs", None)
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "missing required field 'approval_refs'"):
            validate(record, schema, schema)

    def test_text_generation_plan_requires_approval_and_post_plan_gate_contract(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "text-generation-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-journey" / "text-generation-plan.json"
        record = load_json(data_path)
        record.pop("approval_refs", None)
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "missing required field 'approval_refs'"):
            validate(record, schema, schema)

    def test_text_generation_plan_requires_length_policy_and_review_presentation(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "text-generation-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-journey" / "text-generation-plan.json"
        schema = load_json(schema_path)
        for field in ["length_policy", "review_presentation"]:
            with self.subTest(field=field):
                record = load_json(data_path)
                record.pop(field, None)
                with self.assertRaisesRegex(ValidationError, f"missing required field '{field}'"):
                    validate(record, schema, schema)

    def test_image_and_sound_final_records_require_approval_refs(self) -> None:
        cases = [
            ("creative-brief.schema.json", "tests/fixtures/text-to-image/creative-brief.json"),
            ("prompt-plan.schema.json", "tests/fixtures/text-to-image/prompt-plan.json"),
            ("sound-creative-brief.schema.json", "tests/fixtures/text-to-suno/sound-creative-brief.json"),
            ("sound-prompt-plan.schema.json", "tests/fixtures/text-to-suno/sound-prompt-plan.json"),
        ]
        for schema_name, fixture_path in cases:
            with self.subTest(schema=schema_name, fixture=fixture_path):
                schema = load_json(REPO_ROOT / "schemas" / schema_name)
                record = load_json(REPO_ROOT / fixture_path)
                record.pop("approval_refs", None)
                with self.assertRaisesRegex(ValidationError, "missing required field 'approval_refs'"):
                    validate(record, schema, schema)

    def test_image_prompt_plan_accepts_midjourney_provider_target(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "prompt-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-image" / "prompt-plan.json"
        record = load_json(data_path)
        midjourney_target = record["provider_targets"][0]
        self.assertEqual(midjourney_target["provider"], "midjourney")
        self.assertEqual(midjourney_target["provider_prompt_style"], "suffix_parameters")
        self.assertIn("--ar 4:5", midjourney_target["rendered_suffix"])
        self.assertEqual(
            {rendered["variant_type"] for rendered in midjourney_target["rendered_prompts"]},
            {"faithful", "amplified", "minimal"},
        )
        validate_file(schema_path, data_path)

    def test_image_prompt_plan_rejects_unknown_provider_target_parameter(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "prompt-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-image" / "prompt-plan.json"
        record = load_json(data_path)
        record["provider_targets"][0]["parameters"]["unsupported_midjourney_flag"] = "--foo"
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "unsupported_midjourney_flag"):
            validate(record, schema, schema)

    def test_sound_prompt_plan_requires_exactly_three_variants(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "sound-prompt-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-suno" / "sound-prompt-plan.json"
        record = load_json(data_path)
        record["prompt_variants"] = record["prompt_variants"][:2]
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "fewer than 3|minContains"):
            validate(record, schema, schema)

    def test_sound_prompt_plan_requires_one_of_each_variant_type(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "sound-prompt-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-suno" / "sound-prompt-plan.json"
        record = load_json(data_path)
        record["prompt_variants"][1]["variant_type"] = "faithful"
        record["prompt_variants"][2]["variant_type"] = "faithful"
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "matches more than maxContains 1"):
            validate(record, schema, schema)

    def test_sound_prompt_plan_requires_platform_renderings(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "sound-prompt-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-suno" / "sound-prompt-plan.json"
        record = load_json(data_path)
        record.pop("platform_renderings", None)
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "missing required field 'platform_renderings'"):
            validate(record, schema, schema)

    def test_sound_prompt_plan_rejects_suno_rendering_without_custom_mode_outputs(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "sound-prompt-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-suno" / "sound-prompt-plan.json"
        record = load_json(data_path)
        suno_rendering = record["platform_renderings"][0]
        self.assertEqual(suno_rendering["platform"], "suno")
        del suno_rendering["outputs"]["suno_custom_mode_outputs"]
        schema = load_json(schema_path)
        with self.assertRaisesRegex(
            ValidationError,
            "missing required field 'suno_custom_mode_outputs'|matches fewer than minContains",
        ):
            validate(record, schema, schema)

    def test_sound_prompt_plan_rejects_lyrics_required_without_lyrics(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "sound-prompt-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-suno" / "sound-prompt-plan.json"
        record = load_json(data_path)
        record["lyrics"]["present"] = False
        record["lyrics"]["text"] = ""
        suno_outputs = record["platform_renderings"][0]["outputs"]["suno_custom_mode_outputs"]
        suno_outputs["instrumental"] = True
        suno_outputs["lyrics"]["mode"] = "none"
        suno_outputs["lyrics"]["text"] = ""
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "expected const True"):
            validate(record, schema, schema)

    def test_sound_prompt_plan_rejects_generated_suno_lyrics_when_lyrics_are_approved(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "sound-prompt-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-suno" / "sound-prompt-plan.json"
        record = load_json(data_path)
        self.assertEqual(record["vocal_lyric_policy"]["lyrics_mode"], "new_lyrics")
        suno_outputs = record["platform_renderings"][0]["outputs"]["suno_custom_mode_outputs"]
        suno_outputs["lyrics"]["mode"] = "generate_in_suno"
        suno_outputs["lyrics"]["text"] = "Generate fitting lyrics from the prompt."
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "expected const 'custom'"):
            validate(record, schema, schema)

    def test_sound_prompt_plan_rejects_generated_variant_intent_when_lyrics_are_approved(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "sound-prompt-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-suno" / "sound-prompt-plan.json"
        record = load_json(data_path)
        self.assertEqual(record["vocal_lyric_policy"]["lyrics_mode"], "new_lyrics")
        intent = record["prompt_variants"][0]["platform_output_intent"]
        intent["lyrics"]["mode"] = "generate_in_suno"
        intent["lyrics"]["text"] = "Generate fitting lyrics from the prompt."
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "expected const 'custom'"):
            validate(record, schema, schema)

    def test_sound_prompt_plan_accepts_phonetic_vocals_custom_mode_mapping(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "sound-prompt-plan.schema.json"
        data_path = (
            REPO_ROOT
            / "tests"
            / "fixtures"
            / "text-to-suno"
            / "sound-prompt-plan-phonetic-vocals.json"
        )
        record = load_json(data_path)
        self.assertEqual(record["vocal_lyric_policy"]["lyrics_mode"], "phonetic_vocals")
        suno_outputs = record["platform_renderings"][0]["outputs"]["suno_custom_mode_outputs"]
        self.assertFalse(suno_outputs["instrumental"])
        self.assertEqual(suno_outputs["lyrics"]["mode"], "generate_in_suno")
        self.assertIn("intelligible lyrics", " ".join(suno_outputs["exclude"]).lower())
        validate_file(schema_path, data_path)

    def test_sound_prompt_plan_rejects_phonetic_vocals_as_instrumental(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "sound-prompt-plan.schema.json"
        data_path = (
            REPO_ROOT
            / "tests"
            / "fixtures"
            / "text-to-suno"
            / "sound-prompt-plan-phonetic-vocals.json"
        )
        record = load_json(data_path)
        suno_outputs = record["platform_renderings"][0]["outputs"]["suno_custom_mode_outputs"]
        suno_outputs["instrumental"] = True
        suno_outputs["lyrics"]["mode"] = "none"
        schema = load_json(schema_path)
        with self.assertRaises(ValidationError):
            validate(record, schema, schema)

    def test_sound_prompt_plan_accepts_instrumental_custom_mode_mapping(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "sound-prompt-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-suno" / "sound-prompt-plan.json"
        record = load_json(data_path)
        record["vocal_lyric_policy"]["lyrics_mode"] = "instrumental"
        record["lyrics"]["present"] = False
        record["lyrics"]["text"] = ""
        suno_outputs = record["platform_renderings"][0]["outputs"]["suno_custom_mode_outputs"]
        suno_outputs["instrumental"] = True
        suno_outputs["lyrics"]["mode"] = "none"
        suno_outputs["lyrics"]["text"] = ""
        for variant in record["prompt_variants"]:
            intent = variant["platform_output_intent"]
            intent["instrumental"] = True
            intent["lyrics"]["mode"] = "none"
            intent["lyrics"]["text"] = ""
        schema = load_json(schema_path)
        validate(record, schema, schema)  # instrumental branch must validate

    def test_sound_prompt_plan_rejects_instrumental_suno_rendering_with_lyrics_text(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "sound-prompt-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-suno" / "sound-prompt-plan.json"
        record = load_json(data_path)
        record["vocal_lyric_policy"]["lyrics_mode"] = "instrumental"
        record["lyrics"]["present"] = False
        record["lyrics"]["text"] = ""
        suno_outputs = record["platform_renderings"][0]["outputs"]["suno_custom_mode_outputs"]
        suno_outputs["instrumental"] = True
        suno_outputs["lyrics"]["mode"] = "none"
        suno_outputs["lyrics"]["text"] = "These words should not be here."
        for variant in record["prompt_variants"]:
            intent = variant["platform_output_intent"]
            intent["instrumental"] = True
            intent["lyrics"]["mode"] = "none"
            intent["lyrics"]["text"] = ""
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "expected const ''"):
            validate(record, schema, schema)

    def test_sound_prompt_plan_rejects_instrumental_variant_intent_with_lyrics_text(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "sound-prompt-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-suno" / "sound-prompt-plan.json"
        record = load_json(data_path)
        record["vocal_lyric_policy"]["lyrics_mode"] = "instrumental"
        record["lyrics"]["present"] = False
        record["lyrics"]["text"] = ""
        suno_outputs = record["platform_renderings"][0]["outputs"]["suno_custom_mode_outputs"]
        suno_outputs["instrumental"] = True
        suno_outputs["lyrics"]["mode"] = "none"
        suno_outputs["lyrics"]["text"] = ""
        for variant in record["prompt_variants"]:
            intent = variant["platform_output_intent"]
            intent["instrumental"] = True
            intent["lyrics"]["mode"] = "none"
            intent["lyrics"]["text"] = ""
        record["prompt_variants"][0]["platform_output_intent"]["lyrics"]["text"] = "These words should not be here."
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "expected const ''"):
            validate(record, schema, schema)

    def test_sound_prompt_plan_rejects_non_suno_renderer_for_suno_platform(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "sound-prompt-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-suno" / "sound-prompt-plan.json"
        record = load_json(data_path)
        self.assertEqual(record["platform_renderings"][0]["platform"], "suno")
        record["platform_renderings"][0]["renderer"] = "udio_custom"
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "suno_custom_mode"):
            validate(record, schema, schema)

    def test_sound_prompt_plan_rejects_non_neutral_target_platform(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "sound-prompt-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-suno" / "sound-prompt-plan.json"
        record = load_json(data_path)
        record["target_platform"] = "suno"
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "expected const 'platform_neutral'"):
            validate(record, schema, schema)

    def test_sound_prompt_plan_rejects_invalid_platform_readiness_status(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "sound-prompt-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-suno" / "sound-prompt-plan.json"
        record = load_json(data_path)
        record["platform_renderings"][0]["readiness_check"]["status"] = "kinda_ready"
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "is not one of"):
            validate(record, schema, schema)

    def test_beat_plan_requires_story_structure_for_non_single_beat_modes(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "beat-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "story" / "freytag-rehearsal" / "beat-plan.json"
        schema = load_json(schema_path)
        for story_mode in ["beat_pair", "three_part_sequence", "sequence", "scene", "arc", "world"]:
            with self.subTest(story_mode=story_mode):
                record = load_json(data_path)
                record["story_mode"] = story_mode
                del record["story_structure"]
                with self.assertRaisesRegex(ValidationError, "missing required field 'story_structure'"):
                    validate(record, schema, schema)

    def test_beat_plan_allows_single_beat_without_story_structure(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "beat-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "story" / "beat-plan.json"
        record = load_json(data_path)
        self.assertEqual("single_beat", record["story_mode"])
        del record["story_structure"]
        schema = load_json(schema_path)
        validate(record, schema, schema)

    def test_beat_plan_requires_workflow_scale_routing(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "beat-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "story" / "beat-plan.json"
        record = load_json(data_path)
        del record["workflow_scale_routing"]
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "missing required field 'workflow_scale_routing'"):
            validate(record, schema, schema)

    def test_beat_plan_accepts_story_movements_grouping_small_beats(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "beat-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "story" / "freytag-rehearsal" / "beat-plan.json"
        record = load_json(data_path)
        record["story_movements"] = [
            {
                "movement_id": "smov_tower_restoration",
                "movement_label": "Restoration Passage",
                "movement_role": "restoration",
                "summary": "The warning is received, the tower's purpose changes, and the aftermath lands.",
                "beat_ids": [
                    "beat_tower_climax",
                    "beat_tower_falling_action",
                    "beat_tower_denouement",
                ],
                "purpose": "Group the restoration-sized passage without replacing the smaller Beat records.",
                "scale_notes": "This is larger than a Beat because it contains warning, consequence, and residue.",
            }
        ]
        schema = load_json(schema_path)
        validate(record, schema, schema)

    def test_beat_plan_story_movements_require_grouped_beat_ids(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "beat-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "story" / "freytag-rehearsal" / "beat-plan.json"
        record = load_json(data_path)
        record["story_movements"] = [
            {
                "movement_id": "smov_tower_restoration",
                "movement_label": "Restoration Passage",
                "movement_role": "restoration",
                "summary": "A larger passage is present, but it has no Beat ids.",
                "purpose": "Invalid movement without grouped Beats.",
                "scale_notes": "Story Movements organize Beats; they do not replace them.",
            }
        ]
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "missing required field 'beat_ids'"):
            validate(record, schema, schema)

    def test_text_medium_plan_requires_workflow_scale_routing(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "text-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-journey" / "text-medium-plan.json"
        record = load_json(data_path)
        del record["workflow_scale_routing"]
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "missing required field 'workflow_scale_routing'"):
            validate(record, schema, schema)

    def test_text_medium_plan_requires_length_policy(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "text-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-journey" / "text-medium-plan.json"
        record = load_json(data_path)
        del record["length_policy"]
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "missing required field 'length_policy'"):
            validate(record, schema, schema)

    def test_image_medium_plan_requires_workflow_scale_routing(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "image-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-image" / "image-medium-plan.json"
        record = load_json(data_path)
        del record["workflow_scale_routing"]
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "missing required field 'workflow_scale_routing'"):
            validate(record, schema, schema)

    def test_sound_medium_plan_requires_workflow_scale_routing(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "sound-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-suno" / "sound-medium-plan.json"
        record = load_json(data_path)
        del record["workflow_scale_routing"]
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "missing required field 'workflow_scale_routing'"):
            validate(record, schema, schema)

    def test_video_medium_plan_fixture_validates(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "video-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "video-journey" / "video-medium-plan.json"
        validate_file(schema_path, data_path)

    def test_video_medium_plan_requires_composite_storyboard_default(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "video-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "video-journey" / "video-medium-plan.json"
        record = load_json(data_path)
        del record["storyboard_generation_policy"]["default_generated_storyboard_artifact"]
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "missing required field 'default_generated_storyboard_artifact'"):
            validate(record, schema, schema)

    def test_video_medium_plan_requires_workflow_scale_routing(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "video-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "video-journey" / "video-medium-plan.json"
        record = load_json(data_path)
        del record["workflow_scale_routing"]
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "missing required field 'workflow_scale_routing'"):
            validate(record, schema, schema)

    def test_video_medium_plan_requires_narrative_depth(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "video-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "video-journey" / "video-medium-plan.json"
        record = load_json(data_path)
        del record["narrative_depth"]
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "missing required field 'narrative_depth'"):
            validate(record, schema, schema)

    def test_video_medium_plan_full_story_requires_story_template_ref(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "video-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "video-journey" / "video-medium-plan.json"
        record = load_json(data_path)
        record["narrative_depth"] = "full_story"
        record["story_template_ref"] = None
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "expected string"):
            validate(record, schema, schema)

    def test_video_medium_plan_micro_journey_requires_template_ref(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "video-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "video-journey" / "video-medium-plan.json"
        record = load_json(data_path)
        record["narrative_depth"] = "micro_journey"
        record["story_template_ref"] = None
        record["micro_journey_template_ref"] = None
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "expected string"):
            validate(record, schema, schema)

    def test_video_medium_plan_accepts_micro_journey_template_ref(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "video-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "video-journey" / "video-medium-plan.json"
        record = load_json(data_path)
        record["narrative_depth"] = "micro_journey"
        record["story_template_ref"] = None
        record["micro_journey_template_ref"] = "product_reveal"
        schema = load_json(schema_path)
        validate(record, schema, schema)

    def test_video_medium_plan_accepts_promoted_micro_journey_template_refs(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "video-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "video-journey" / "video-medium-plan.json"
        schema = load_json(schema_path)

        for template_ref in ["problem_solution_demo", "how_to_tip_demo"]:
            with self.subTest(template_ref=template_ref):
                record = load_json(data_path)
                record["narrative_depth"] = "micro_journey"
                record["story_template_ref"] = None
                record["micro_journey_template_ref"] = template_ref
                validate(record, schema, schema)

    def test_video_medium_plan_rejects_unpromoted_micro_journey_template_ref(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "video-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "video-journey" / "video-medium-plan.json"
        record = load_json(data_path)
        record["narrative_depth"] = "micro_journey"
        record["story_template_ref"] = None
        record["micro_journey_template_ref"] = "social_proof_receipt"
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "is not one of"):
            validate(record, schema, schema)

    def test_video_medium_plan_utility_sequence_requires_asset_purpose_brief(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "video-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "video-journey" / "video-medium-plan.json"
        record = load_json(data_path)
        record["narrative_depth"] = "utility_sequence"
        record["story_template_ref"] = None
        record["asset_purpose_brief"] = None
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "expected object"):
            validate(record, schema, schema)

    def test_video_medium_plan_accepts_utility_sequence_asset_purpose_brief(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "video-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "video-journey" / "video-medium-plan.json"
        record = load_json(data_path)
        record["narrative_depth"] = "utility_sequence"
        record["story_template_ref"] = None
        record["micro_journey_template_ref"] = None
        record["asset_purpose_brief"] = {
            "role_use_context": "Reusable insert asset for creator explainer videos.",
            "subject": "Approved still frame of the AI video workflow toolkit.",
            "visual_purpose": "Make the workflow feel concrete and repeatable.",
            "placement": ["under voiceover", "section transition"],
            "duration_target": "6-8 seconds",
            "shot_or_asset_count": "one looping B-roll utility asset",
            "motion_behavior": "Subtle product spin or timeline insert from the approved still.",
            "loop_or_resolution_behavior": "Returns to the approved still or resolves to a held transition plate.",
            "style_constraints": ["preserve approved still composition", "avoid generic AI UI"],
            "reference_or_continuity_needs": ["approved still frame", "workflow toolkit style reference"],
            "audio_text_posture": "Silent raw asset; preserve only approved still text.",
            "success_criteria": ["loops cleanly", "keeps the approved still recognizable"],
            "downstream_export_notes": "Provider-specific loop and frame-rate instructions wait for export."
        }
        schema = load_json(schema_path)
        validate(record, schema, schema)

    def test_workflow_scale_supports_are_enum_backed(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "beat-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "story" / "beat-plan.json"
        record = load_json(data_path)
        record["workflow_scale_routing"]["recommended_supports"].append("unsupported_helper")
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "not one of"):
            validate(record, schema, schema)

    def test_workflow_scale_skipped_supports_are_enum_backed(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "image-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-image" / "image-medium-plan.json"
        record = load_json(data_path)
        record["workflow_scale_routing"]["skipped_supports"].append("unsupported_helper")
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "not one of"):
            validate(record, schema, schema)

    def test_workflow_scale_trigger_signals_are_enum_backed(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "sound-medium-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-suno" / "sound-medium-plan.json"
        record = load_json(data_path)
        record["workflow_scale_routing"]["trigger_signals"].append("unsupported_signal")
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "not one of"):
            validate(record, schema, schema)

    def test_workflow_scale_routing_supports_are_not_both_activated_and_skipped(self) -> None:
        targets = [
            (schema_path, data_path)
            for schema_path, data_path in iter_validation_targets(include_fixtures=True)
            if schema_path.name in WORKFLOW_SCALE_SCHEMA_NAMES
        ]
        self.assertGreaterEqual(len(targets), 4)

        for _schema_path, data_path in targets:
            record = load_json(data_path)
            with self.subTest(data=data_path.relative_to(REPO_ROOT)):
                self.assertEqual(set(), routing_support_overlap(record))
                self.assertEqual(set(), routing_recommended_skip_overlap(record))

    def test_workflow_scale_routing_detects_long_work_activation_skip_contradiction(self) -> None:
        record = load_json(REPO_ROOT / "tests" / "fixtures" / "story" / "beat-plan.json")
        record["workflow_scale_routing"]["activated_supports"].append(LONG_WORK_SUPPORT)

        self.assertIn(LONG_WORK_SUPPORT, routing_support_overlap(record))

    def test_workflow_scale_routing_long_work_recommendation_matches_scale_fixture_intent(self) -> None:
        compact_or_structured_paths = [
            REPO_ROOT / "tests" / "fixtures" / "story" / "beat-plan.json",
            REPO_ROOT / "tests" / "fixtures" / "text-to-image" / "single-image-rehearsal" / "beat-plan.json",
            REPO_ROOT / "tests" / "fixtures" / "text-to-image" / "single-image-rehearsal" / "image-medium-plan.json",
            REPO_ROOT / "tests" / "fixtures" / "text-to-suno" / "sound-medium-plan.json",
            REPO_ROOT / "tests" / "fixtures" / "text-journey" / "article-rehearsal" / "beat-plan.json",
            REPO_ROOT / "tests" / "fixtures" / "text-journey" / "article-rehearsal" / "text-medium-plan.json",
            REPO_ROOT / "tests" / "fixtures" / "text-journey" / "op-ed-rehearsal" / "beat-plan.json",
            REPO_ROOT / "tests" / "fixtures" / "text-journey" / "op-ed-rehearsal" / "text-medium-plan.json",
        ]
        cumulative_paths = [
            REPO_ROOT / "tests" / "fixtures" / "text-to-image" / "three-image-series-rehearsal" / "beat-plan.json",
            REPO_ROOT / "tests" / "fixtures" / "text-to-image" / "three-image-series-rehearsal" / "image-medium-plan.json",
            REPO_ROOT / "tests" / "fixtures" / "text-journey" / "cumulative-text-rehearsal" / "beat-plan.json",
            REPO_ROOT / "tests" / "fixtures" / "text-journey" / "cumulative-text-rehearsal" / "text-medium-plan.json",
        ]

        for data_path in compact_or_structured_paths:
            record = load_json(data_path)
            routing = record["workflow_scale_routing"]
            with self.subTest(data=data_path.relative_to(REPO_ROOT)):
                self.assertIn(routing["scale_level"], {"compact_artifact", "structured_single_artifact"})
                self.assertNotIn(LONG_WORK_SUPPORT, routing["recommended_supports"])
                self.assertNotIn(LONG_WORK_SUPPORT, routing["activated_supports"])
                self.assertIn(LONG_WORK_SUPPORT, routing["skipped_supports"])

        for data_path in cumulative_paths:
            record = load_json(data_path)
            routing = record["workflow_scale_routing"]
            with self.subTest(data=data_path.relative_to(REPO_ROOT)):
                self.assertEqual("cumulative_work", routing["scale_level"])
                self.assertIn(LONG_WORK_SUPPORT, routing["recommended_supports"])
                self.assertNotIn(LONG_WORK_SUPPORT, routing["activated_supports"])
                self.assertNotIn(LONG_WORK_SUPPORT, routing["skipped_supports"])

    def test_image_output_shapes_do_not_use_three_part_sequence(self) -> None:
        image_schema = load_json(REPO_ROOT / "schemas" / "image-medium-plan.schema.json")
        creative_schema = load_json(REPO_ROOT / "schemas" / "creative-brief.schema.json")

        with self.assertRaisesRegex(ValidationError, "not one of"):
            validate("three_part_sequence", image_schema["properties"]["presentation_mode"], image_schema)

        with self.assertRaisesRegex(ValidationError, "not one of"):
            validate("three_part_sequence", creative_schema["properties"]["series_recommendation"]["properties"]["mode"], creative_schema)

    def test_single_image_fixture_keeps_story_structure_optional(self) -> None:
        beat_plan_path = (
            REPO_ROOT / "tests" / "fixtures" / "text-to-image" / "single-image-rehearsal" / "beat-plan.json"
        )
        image_plan_path = (
            REPO_ROOT / "tests" / "fixtures" / "text-to-image" / "single-image-rehearsal" / "image-medium-plan.json"
        )
        beat_plan = load_json(beat_plan_path)
        image_plan = load_json(image_plan_path)

        self.assertEqual("single_beat", beat_plan["story_mode"])
        self.assertNotIn("story_structure", beat_plan)
        self.assertEqual("single_image", image_plan["presentation_mode"])
        self.assertEqual(1, len(image_plan["image_roles"]))
        self.assertFalse(image_plan["series_plan"]["is_series"])

        validate_file(REPO_ROOT / "schemas" / "beat-plan.schema.json", beat_plan_path)
        validate_file(REPO_ROOT / "schemas" / "image-medium-plan.schema.json", image_plan_path)

    def test_single_image_accepts_medium_output_shape_recommendation(self) -> None:
        image_plan_path = (
            REPO_ROOT / "tests" / "fixtures" / "text-to-image" / "single-image-rehearsal" / "image-medium-plan.json"
        )
        image_plan = load_json(image_plan_path)
        image_plan["medium_output_shape_recommendation"] = {
            "requested_shape": None,
            "recommended_shape": "single_image",
            "accepted_shape": "single_image",
            "rationale": "The emotional complexity compresses best into one threshold image.",
            "alternatives_considered": ["compressed_arc", "image_series"],
            "tradeoffs": [
                "A series would over-explain the unresolved threshold.",
                "A compressed arc would weaken the single held choice."
            ],
            "conflict": {
                "has_conflict": False,
                "conflict_summary": None,
                "resolution": "not_needed",
                "gate_decision_id": None
            }
        }

        schema = load_json(REPO_ROOT / "schemas" / "image-medium-plan.schema.json")
        validate(image_plan, schema, schema)

    def test_three_image_fixture_is_image_series(self) -> None:
        beat_plan_path = (
            REPO_ROOT / "tests" / "fixtures" / "text-to-image" / "three-image-series-rehearsal" / "beat-plan.json"
        )
        image_plan_path = (
            REPO_ROOT / "tests" / "fixtures" / "text-to-image" / "three-image-series-rehearsal" / "image-medium-plan.json"
        )
        beat_plan = load_json(beat_plan_path)
        image_plan = load_json(image_plan_path)

        self.assertEqual("sequence", beat_plan["story_mode"])
        self.assertIn("story_structure", beat_plan)
        self.assertEqual("image_series", image_plan["presentation_mode"])
        self.assertEqual(3, len(image_plan["image_roles"]))
        self.assertTrue(image_plan["series_plan"]["is_series"])

        validate_file(REPO_ROOT / "schemas" / "beat-plan.schema.json", beat_plan_path)
        validate_file(REPO_ROOT / "schemas" / "image-medium-plan.schema.json", image_plan_path)

    def test_image_series_accepts_medium_output_shape_recommendation(self) -> None:
        image_plan_path = (
            REPO_ROOT
            / "tests"
            / "fixtures"
            / "text-to-image"
            / "three-image-series-rehearsal"
            / "image-medium-plan.json"
        )
        image_plan = load_json(image_plan_path)
        image_plan["medium_output_shape_recommendation"] = {
            "requested_shape": "image_series",
            "recommended_shape": "image_series",
            "accepted_shape": "image_series",
            "rationale": "The Beat Plan needs separate image roles for absence, pressure, and residue.",
            "alternatives_considered": ["single_image", "compressed_arc"],
            "tradeoffs": [
                "A single image would collapse necessary emotional movement.",
                "A compressed arc would preserve movement but lose role-level calibration."
            ],
            "conflict": {
                "has_conflict": False,
                "conflict_summary": None,
                "resolution": "accepted_recommendation",
                "gate_decision_id": None
            }
        }

        schema = load_json(REPO_ROOT / "schemas" / "image-medium-plan.schema.json")
        validate(image_plan, schema, schema)

    def test_image_output_shape_recommendation_must_match_presentation_mode(self) -> None:
        image_plan_path = (
            REPO_ROOT
            / "tests"
            / "fixtures"
            / "text-to-image"
            / "three-image-series-rehearsal"
            / "image-medium-plan.json"
        )
        image_plan = load_json(image_plan_path)
        image_plan["medium_output_shape_recommendation"] = {
            "requested_shape": "image_series",
            "recommended_shape": "image_series",
            "accepted_shape": "single_image",
            "rationale": "Invalid: accepted shape must match the concrete presentation mode.",
            "alternatives_considered": ["image_series"],
            "tradeoffs": ["Invalid shape mismatch guard."],
            "conflict": {
                "has_conflict": False,
                "conflict_summary": None,
                "resolution": "not_needed",
                "gate_decision_id": None
            }
        }

        schema = load_json(REPO_ROOT / "schemas" / "image-medium-plan.schema.json")
        with self.assertRaisesRegex(ValidationError, "expected const 'single_image'"):
            validate(image_plan, schema, schema)

    def test_image_output_shape_recommendation_rejects_story_mode_as_shape(self) -> None:
        image_plan_path = (
            REPO_ROOT / "tests" / "fixtures" / "text-to-image" / "single-image-rehearsal" / "image-medium-plan.json"
        )
        image_plan = load_json(image_plan_path)
        image_plan["medium_output_shape_recommendation"] = {
            "requested_shape": "three_part_sequence",
            "recommended_shape": "three_part_sequence",
            "accepted_shape": "three_part_sequence",
            "rationale": "Invalid: Story Mode must not become an image output shape.",
            "alternatives_considered": ["single_image"],
            "tradeoffs": ["Invalid shape guard."],
            "conflict": {
                "has_conflict": False,
                "conflict_summary": None,
                "resolution": "not_needed",
                "gate_decision_id": None
            }
        }

        schema = load_json(REPO_ROOT / "schemas" / "image-medium-plan.schema.json")
        with self.assertRaisesRegex(ValidationError, "not one of"):
            validate(image_plan, schema, schema)


class AssetPackageContractTests(unittest.TestCase):
    SCHEMA_PATH = REPO_ROOT / "schemas" / "asset-package.schema.json"
    FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "release-packages" / "asset-package.json"

    def test_asset_package_fixture_validates(self) -> None:
        validate_file(self.SCHEMA_PATH, self.FIXTURE_PATH)

    def test_asset_package_filled_slot_requires_output_record(self) -> None:
        record = load_json(self.FIXTURE_PATH)
        record["slots"][0]["output_record_id"] = None
        schema = load_json(self.SCHEMA_PATH)
        with self.assertRaisesRegex(ValidationError, "filled slot requires an output_record_id"):
            validate(record, schema, schema)

    def test_asset_package_waived_slot_requires_waiver_gate(self) -> None:
        record = load_json(self.FIXTURE_PATH)
        record["slots"][1]["completeness"] = "waived"
        record["slots"][1]["output_record_id"] = None
        schema = load_json(self.SCHEMA_PATH)
        with self.assertRaisesRegex(ValidationError, "waived slot requires a recorded waiver_gate_id"):
            validate(record, schema, schema)

    def test_asset_package_waived_slot_forbids_output_record(self) -> None:
        record = load_json(self.FIXTURE_PATH)
        record["slots"][1]["completeness"] = "waived"
        record["slots"][1]["waiver_gate_id"] = "gate_missing_soundtrack_waived"
        schema = load_json(self.SCHEMA_PATH)
        with self.assertRaisesRegex(ValidationError, "waived slot must not carry an output_record_id"):
            validate(record, schema, schema)

    def test_asset_package_complete_status_forbids_missing_slot(self) -> None:
        record = load_json(self.FIXTURE_PATH)
        record["slots"][1]["completeness"] = "missing"
        record["slots"][1]["output_record_id"] = None
        schema = load_json(self.SCHEMA_PATH)
        with self.assertRaisesRegex(ValidationError, "complete package has a missing slot"):
            validate(record, schema, schema)

    def test_asset_package_missing_slot_forbids_output_record(self) -> None:
        record = load_json(self.FIXTURE_PATH)
        record["status"] = "partial"  # avoid the complete-status check so the missing->null check fires
        record["slots"][1]["completeness"] = "missing"  # leave output_record_id non-null
        schema = load_json(self.SCHEMA_PATH)
        with self.assertRaisesRegex(ValidationError, "missing slot must not carry an output_record_id"):
            validate(record, schema, schema)

    def test_asset_package_album_rejects_video_slots(self) -> None:
        record = load_json(self.FIXTURE_PATH)
        record["package_format_id"] = "album"
        record["package_format_ref"] = "docs/structure-library/package-format/album.md"
        schema = load_json(self.SCHEMA_PATH)
        with self.assertRaisesRegex(ValidationError, "slots not defined by its Package Format"):
            validate(record, schema, schema)

    def test_asset_package_complete_video_package_requires_soundtrack(self) -> None:
        record = load_json(self.FIXTURE_PATH)
        record["slots"] = [record["slots"][0]]
        schema = load_json(self.SCHEMA_PATH)
        with self.assertRaisesRegex(ValidationError, "requires exactly 1 active 'soundtrack_audio'"):
            validate(record, schema, schema)

    def test_asset_package_rejects_unknown_top_level_field(self) -> None:
        record = load_json(self.FIXTURE_PATH)
        record["unexpected_field"] = "nope"
        schema = load_json(self.SCHEMA_PATH)
        with self.assertRaisesRegex(ValidationError, "unexpected fields"):
            validate(record, schema, schema)

    # --- Per-slot waivers: one Gate Decision per waived required slot ---
    #
    # ADR 0014 and docs/gates/canonical-gates.md both say a waiver names ONE slot, so
    # "a general 'ship anyway' decision does not waive unnamed missing deliverables".
    # Before this slice a single shared waiver_gate_id across every waived slot
    # validated, which is exactly that forbidden decision.

    ARTICLE_PACKAGE = REPO_ROOT / "tests" / "fixtures" / "cross-medium" / "article-with-photos-rehearsal" / "asset-package-article.json"

    def article_package(self) -> tuple[dict, dict]:
        return load_json(self.SCHEMA_PATH), load_json(self.ARTICLE_PACKAGE)

    def test_article_package_fixture_validates(self) -> None:
        validate_file(self.SCHEMA_PATH, self.ARTICLE_PACKAGE)

    def test_waived_slots_must_not_share_one_gate_decision(self) -> None:
        schema, record = self.article_package()
        for slot in record["slots"]:
            slot["completeness"] = "waived"
            slot["output_record_id"] = None
            slot["waiver_gate_id"] = "gate_civic_garden_ship_anyway"
        with self.assertRaisesRegex(ValidationError, "waiver_gate_id must not be shared across slots"):
            validate(record, schema, schema)

    def test_distinct_per_slot_waivers_are_accepted(self) -> None:
        # The escape hatch stays open, but only one named slot at a time.
        schema, record = self.article_package()
        record["slots"][2]["completeness"] = "waived"
        record["slots"][2]["output_record_id"] = None
        record["slots"][2]["waiver_gate_id"] = "gate_civic_garden_waive_inline_photo_hose"
        validate(record, schema, schema)

    def test_filled_slot_must_not_carry_a_waiver_gate(self) -> None:
        schema, record = self.article_package()
        record["slots"][0]["waiver_gate_id"] = "gate_civic_garden_waive_inline_photo_hose"
        with self.assertRaisesRegex(ValidationError, "filled slot must not carry a waiver_gate_id"):
            validate(record, schema, schema)

    def test_article_package_cannot_complete_with_a_missing_required_slot(self) -> None:
        schema, record = self.article_package()
        record["slots"][2]["completeness"] = "missing"
        record["slots"][2]["output_record_id"] = None
        with self.assertRaisesRegex(ValidationError, "complete package has a missing slot"):
            validate(record, schema, schema)

    def test_article_package_requires_exactly_one_article_text(self) -> None:
        schema, record = self.article_package()
        record["slots"].append(dict(record["slots"][0], output_record_id="out_civic_garden_article_text_002"))
        with self.assertRaisesRegex(ValidationError, "requires exactly 1 active 'article_text'"):
            validate(record, schema, schema)

    def test_article_package_requires_at_least_one_inline_photo(self) -> None:
        schema, record = self.article_package()
        record["slots"] = [record["slots"][0]]
        with self.assertRaisesRegex(ValidationError, "requires at least 1 active 'inline_photo'"):
            validate(record, schema, schema)


if __name__ == "__main__":
    unittest.main()
