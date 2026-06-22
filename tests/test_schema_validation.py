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
}


def routing_support_overlap(record: dict) -> set[str]:
    routing = record["workflow_scale_routing"]
    return set(routing["activated_supports"]) & set(routing["skipped_supports"])


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

    def test_fallback_review_record_fixture_validates(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "review-record.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "reviews" / "fallback-review-record.json"
        record = load_json(data_path)
        self.assertEqual(record["reviewer_execution"]["execution_mode"], "fallback_separated_pass")
        self.assertTrue(record["reviewer_execution"]["sub_agent_required"])
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
            REPO_ROOT / "tests" / "fixtures" / "long-work" / "album-stewardship-record.json",
            REPO_ROOT / "tests" / "fixtures" / "long-work" / "image-series-stewardship-record.json",
            REPO_ROOT / "tests" / "fixtures" / "long-work" / "text-stewardship-record.json",
        ]
        for data_path in fixture_paths:
            with self.subTest(data=data_path.relative_to(REPO_ROOT)):
                validate_file(schema_path, data_path)

    def test_album_release_package_plan_fixture_validates(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "release-package-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "release-packages" / "album-release-package-plan.json"
        validate_file(schema_path, data_path)

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

    def test_sound_prompt_plan_rejects_lyrics_required_without_lyrics(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "sound-prompt-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "text-to-suno" / "sound-prompt-plan.json"
        record = load_json(data_path)
        record["lyrics"]["present"] = False
        record["lyrics"]["text"] = ""
        record["suno_custom_mode_outputs"]["instrumental"] = True
        record["suno_custom_mode_outputs"]["lyrics"]["mode"] = "none"
        record["suno_custom_mode_outputs"]["lyrics"]["text"] = ""
        schema = load_json(schema_path)
        with self.assertRaisesRegex(ValidationError, "expected const True"):
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
        self.assertFalse(record["suno_custom_mode_outputs"]["instrumental"])
        self.assertEqual(record["suno_custom_mode_outputs"]["lyrics"]["mode"], "generate_in_suno")
        self.assertIn("intelligible lyrics", " ".join(record["suno_custom_mode_outputs"]["exclude"]).lower())
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
        record["suno_custom_mode_outputs"]["instrumental"] = True
        record["suno_custom_mode_outputs"]["lyrics"]["mode"] = "none"
        schema = load_json(schema_path)
        with self.assertRaises(ValidationError):
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

    def test_workflow_scale_supports_are_enum_backed(self) -> None:
        schema_path = REPO_ROOT / "schemas" / "beat-plan.schema.json"
        data_path = REPO_ROOT / "tests" / "fixtures" / "story" / "beat-plan.json"
        record = load_json(data_path)
        record["workflow_scale_routing"]["activated_supports"].append("unsupported_helper")
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

    def test_workflow_scale_routing_detects_long_work_activation_skip_contradiction(self) -> None:
        record = load_json(REPO_ROOT / "tests" / "fixtures" / "story" / "beat-plan.json")
        record["workflow_scale_routing"]["activated_supports"].append(LONG_WORK_SUPPORT)

        self.assertIn(LONG_WORK_SUPPORT, routing_support_overlap(record))

    def test_workflow_scale_routing_long_work_activation_matches_scale_fixture_intent(self) -> None:
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
                self.assertNotIn(LONG_WORK_SUPPORT, routing["activated_supports"])
                self.assertIn(LONG_WORK_SUPPORT, routing["skipped_supports"])

        for data_path in cumulative_paths:
            record = load_json(data_path)
            routing = record["workflow_scale_routing"]
            with self.subTest(data=data_path.relative_to(REPO_ROOT)):
                self.assertEqual("cumulative_work", routing["scale_level"])
                self.assertIn(LONG_WORK_SUPPORT, routing["activated_supports"])
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


if __name__ == "__main__":
    unittest.main()
