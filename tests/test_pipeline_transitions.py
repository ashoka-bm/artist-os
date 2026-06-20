from __future__ import annotations

import json
import unittest
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((REPO_ROOT / path).read_text(encoding="utf-8"))


LONG_WORK_SUPPORT = "long_work_stewardship"


def ref_pairs(refs: list[dict]) -> set[tuple[str, str]]:
    return {(ref["ref_type"], ref["ref_id"]) for ref in refs}


def timestamp(record: dict) -> datetime:
    return datetime.fromisoformat(record["created_at"].replace("Z", "+00:00"))


class PipelineTransitionTests(unittest.TestCase):
    def assert_support_sets_are_disjoint(self, record: dict, label: str) -> None:
        routing = record["workflow_scale_routing"]
        activated = set(routing["activated_supports"])
        skipped = set(routing["skipped_supports"])
        self.assertFalse(
            activated & skipped,
            f"{label} has supports in both activated_supports and skipped_supports",
        )

    def assert_long_work_support(self, record: dict, should_activate: bool, label: str) -> None:
        routing = record["workflow_scale_routing"]
        self.assert_support_sets_are_disjoint(record, label)
        if should_activate:
            self.assertIn(LONG_WORK_SUPPORT, routing["activated_supports"], label)
            self.assertNotIn(LONG_WORK_SUPPORT, routing["skipped_supports"], label)
        else:
            self.assertNotIn(LONG_WORK_SUPPORT, routing["activated_supports"], label)
            self.assertIn(LONG_WORK_SUPPORT, routing["skipped_supports"], label)

    def test_source_record_to_transformation_brief(self) -> None:
        source = load("tests/fixtures/story/source-record.json")
        artist_meaning = load("tests/fixtures/story/artist-meaning.json")
        transformation = load("tests/fixtures/story/transformation-brief.json")

        self.assertEqual(artist_meaning["source_id"], source["source_id"])
        self.assertEqual(transformation["source_id"], source["source_id"])
        self.assertEqual(transformation["artist_meaning_id"], artist_meaning["artist_meaning_id"])
        self.assertEqual(source["media_type"], transformation["formal_observations"]["media_type"])
        self.assertIn("the threshold between returning and leaving", artist_meaning["must_preserve"])

    def test_gate_decision_traces_to_artist_meaning_and_beat_plan(self) -> None:
        artist_meaning = load("tests/fixtures/story/artist-meaning.json")
        beat_plan = load("tests/fixtures/story/beat-plan.json")
        gate = load("tests/fixtures/gates/symbology-gate.json")

        self.assertEqual(gate["source_id"], artist_meaning["source_id"])
        self.assertEqual(gate["artist_meaning_id"], artist_meaning["artist_meaning_id"])
        self.assertEqual(gate["gate_type"], "symbology")
        self.assertEqual(gate["gate_status"], "selected")
        refs = {(ref["ref_type"], ref["ref_id"]) for ref in gate["upstream_refs"]}
        self.assertIn(("artist_meaning", artist_meaning["artist_meaning_id"]), refs)
        self.assertIn(("beat_plan", beat_plan["beat_plan_id"]), refs)

    def test_transformation_brief_to_beat_plan(self) -> None:
        transformation = load("tests/fixtures/story/transformation-brief.json")
        beat_plan = load("tests/fixtures/story/beat-plan.json")

        self.assertEqual(beat_plan["source_id"], transformation["source_id"])
        self.assertEqual(beat_plan["artist_meaning_id"], transformation["artist_meaning_id"])
        self.assertEqual(
            beat_plan["transformation_brief_id"],
            transformation["transformation_brief_id"],
        )
        self.assertGreaterEqual(len(beat_plan["beats"]), 1)

    def test_beat_plan_to_image_medium_plan(self) -> None:
        beat_plan = load("tests/fixtures/story/beat-plan.json")
        image_plan = load("tests/fixtures/text-to-image/image-medium-plan.json")

        self.assertEqual(image_plan["beat_plan_id"], beat_plan["beat_plan_id"])
        self.assertEqual(image_plan["source_id"], beat_plan["source_id"])
        self.assertEqual(image_plan["artist_meaning_id"], beat_plan["artist_meaning_id"])
        self.assertEqual(image_plan["transformation_brief_id"], beat_plan["transformation_brief_id"])
        self.assertEqual(image_plan["target_media_type"], "image")
        self.assertIn(
            image_plan["symbology_direction"]["confirmation_status"],
            {"artist_specified", "confirmed"},
        )
        self.assertIn(
            image_plan["style_direction"]["confirmation_status"],
            {"artist_specified", "confirmed"},
        )
        key_movement_ids = {
            movement["movement_id"] for movement in beat_plan["key_emotional_movements"]
        }
        for role in image_plan["image_roles"]:
            self.assertIn(role["key_emotional_movement_id"], key_movement_ids)
            self.assertIn("shot_design", role)
            self.assertTrue(role["shot_design"]["emotional_rationale"])

    def test_image_medium_plan_to_image_creative_brief(self) -> None:
        beat_plan = load("tests/fixtures/story/beat-plan.json")
        image_plan = load("tests/fixtures/text-to-image/image-medium-plan.json")
        creative_brief = load("tests/fixtures/text-to-image/creative-brief.json")
        art_review = load("tests/fixtures/reviews/image-art-critic-review-record.json")
        brief_gate = load("tests/fixtures/gates/image-brief-approval-gate.json")
        detail_gate = load("tests/fixtures/gates/image-detail-intensity-gate.json")

        self.assertEqual(creative_brief["beat_plan_id"], image_plan["beat_plan_id"])
        self.assertEqual(creative_brief["source_id"], image_plan["source_id"])
        self.assertEqual(creative_brief["artist_meaning_id"], image_plan["artist_meaning_id"])
        self.assertEqual(creative_brief["transformation_brief_id"], image_plan["transformation_brief_id"])
        self.assertIn("beat_plan_id", creative_brief)
        self.assertIn("transformation_brief_id", creative_brief)
        self.assertNotIn("beats", creative_brief)
        self.assertIn(
            creative_brief["symbology_direction"]["confirmation_status"],
            {"artist_specified", "confirmed"},
        )
        self.assertIn(
            creative_brief["style_direction"]["confirmation_status"],
            {"artist_specified", "confirmed"},
        )
        self.assertEqual(creative_brief["approval_refs"]["art_critic_review_id"], art_review["review_record_id"])
        self.assertEqual(art_review["review_role"], "art_critic")
        self.assertEqual(art_review["artifact_under_review"]["artifact_id"], creative_brief["brief_id"])
        self.assertEqual(creative_brief["approval_refs"]["brief_approval_gate_id"], brief_gate["gate_decision_id"])
        self.assertEqual(brief_gate["gate_type"], "brief_approval")
        self.assertIn(("review_record", art_review["review_record_id"]), ref_pairs(brief_gate["upstream_refs"]))
        self.assertGreater(timestamp(detail_gate), timestamp(brief_gate))
        key_movement_ids = {
            movement["movement_id"] for movement in beat_plan["key_emotional_movements"]
        }
        for suggested_image in creative_brief["series_recommendation"]["suggested_images"]:
            self.assertIn(suggested_image["key_emotional_movement_id"], key_movement_ids)
            self.assertIn("shot_design", suggested_image)
            self.assertTrue(suggested_image["shot_design"]["emotional_rationale"])

        suggested_images = creative_brief["series_recommendation"]["suggested_images"]
        shot_signatures = [
            (
                image["shot_design"]["shot_scale"],
                image["shot_design"]["camera_angle"],
                image["shot_design"]["visual_emphasis"],
            )
            for image in suggested_images
        ]
        for previous, current in zip(shot_signatures, shot_signatures[1:]):
            self.assertNotEqual(previous, current)

    def test_beat_key_movement_references_are_valid(self) -> None:
        beat_plan = load("tests/fixtures/story/beat-plan.json")

        beat_ids = {beat["beat_id"] for beat in beat_plan["beats"]}
        key_movement_ids = {
            movement["movement_id"] for movement in beat_plan["key_emotional_movements"]
        }

        for movement in beat_plan["key_emotional_movements"]:
            for beat_id in movement["beat_ids"]:
                self.assertIn(beat_id, beat_ids)

        for beat in beat_plan["beats"]:
            builds_toward = beat.get("builds_toward_key_movement_id")
            if builds_toward is not None:
                self.assertIn(builds_toward, key_movement_ids)

    def test_beat_plan_to_sound_medium_plan(self) -> None:
        beat_plan = load("tests/fixtures/story/beat-plan.json")
        sound_plan = load("tests/fixtures/text-to-suno/sound-medium-plan.json")

        self.assertEqual(sound_plan["beat_plan_id"], beat_plan["beat_plan_id"])
        self.assertEqual(sound_plan["source_id"], beat_plan["source_id"])
        self.assertEqual(sound_plan["artist_meaning_id"], beat_plan["artist_meaning_id"])
        self.assertEqual(sound_plan["transformation_brief_id"], beat_plan["transformation_brief_id"])
        self.assertEqual(sound_plan["target_media_type"], "sound")

    def test_sound_medium_plan_to_sound_creative_brief(self) -> None:
        sound_plan = load("tests/fixtures/text-to-suno/sound-medium-plan.json")
        sound_brief = load("tests/fixtures/text-to-suno/sound-creative-brief.json")
        sound_review = load("tests/fixtures/reviews/suno-sound-critic-review-record.json")
        brief_gate = load("tests/fixtures/gates/suno-brief-approval-gate.json")

        self.assertEqual(sound_brief["beat_plan_id"], sound_plan["beat_plan_id"])
        self.assertEqual(sound_brief["source_id"], sound_plan["source_id"])
        self.assertEqual(sound_brief["artist_meaning_id"], sound_plan["artist_meaning_id"])
        self.assertEqual(sound_brief["transformation_brief_id"], sound_plan["transformation_brief_id"])
        self.assertIn("transformation_brief_id", sound_brief)
        self.assertNotIn("beats", sound_brief)
        self.assertEqual(sound_brief["approval_refs"]["sound_critic_review_id"], sound_review["review_record_id"])
        self.assertEqual(sound_review["review_role"], "sound_critic")
        self.assertEqual(sound_review["artifact_under_review"]["artifact_id"], sound_brief["brief_id"])
        self.assertEqual(sound_brief["approval_refs"]["brief_approval_gate_id"], brief_gate["gate_decision_id"])
        self.assertEqual(brief_gate["gate_type"], "brief_approval")
        self.assertIn(("review_record", sound_review["review_record_id"]), ref_pairs(brief_gate["upstream_refs"]))

    def test_image_creative_brief_to_prompt_plan(self) -> None:
        creative_brief = load("tests/fixtures/text-to-image/creative-brief.json")
        image_plan = load("tests/fixtures/text-to-image/image-medium-plan.json")
        prompt_plan = load("tests/fixtures/text-to-image/prompt-plan.json")
        prompt_review = load("tests/fixtures/reviews/image-prompt-critic-review-record.json")
        prompt_lock_gate = load("tests/fixtures/gates/image-prompt-lock-gate.json")

        self.assertEqual(prompt_plan["brief_id"], creative_brief["brief_id"])
        self.assertEqual(prompt_plan["source_id"], creative_brief["source_id"])
        self.assertEqual(prompt_plan["artist_meaning_id"], creative_brief["artist_meaning_id"])
        self.assertEqual(prompt_plan["transformation_brief_id"], creative_brief["transformation_brief_id"])
        self.assertEqual(prompt_plan["beat_plan_id"], creative_brief["beat_plan_id"])
        self.assertEqual(prompt_plan["image_medium_plan_id"], image_plan["image_medium_plan_id"])
        self.assertEqual(prompt_plan["approval_refs"]["prompt_critic_review_id"], prompt_review["review_record_id"])
        self.assertEqual(prompt_review["review_role"], "prompt_critic")
        self.assertEqual(prompt_review["artifact_under_review"]["artifact_id"], prompt_plan["prompt_plan_id"])
        self.assertEqual(prompt_plan["approval_refs"]["prompt_lock_gate_id"], prompt_lock_gate["gate_decision_id"])
        self.assertEqual(prompt_lock_gate["gate_type"], "prompt_lock")
        self.assertIn(("review_record", prompt_review["review_record_id"]), ref_pairs(prompt_lock_gate["upstream_refs"]))

    def test_image_prompt_plan_to_prompt_branch_set(self) -> None:
        prompt_plan = load("tests/fixtures/text-to-image/prompt-plan.json")
        branch_set = load("tests/fixtures/text-to-image/prompt-branch-set.json")

        self.assertEqual(branch_set["prompt_plan_id"], prompt_plan["prompt_plan_id"])
        self.assertEqual(branch_set["brief_id"], prompt_plan["brief_id"])
        self.assertEqual(branch_set["source_id"], prompt_plan["source_id"])
        self.assertEqual(branch_set["artist_meaning_id"], prompt_plan["artist_meaning_id"])
        self.assertEqual(branch_set["transformation_brief_id"], prompt_plan["transformation_brief_id"])
        self.assertEqual(branch_set["beat_plan_id"], prompt_plan["beat_plan_id"])
        self.assertEqual(branch_set["medium_plan_id"], prompt_plan["image_medium_plan_id"])
        self.assertEqual(branch_set["branch_count_actual"], len(branch_set["branches"]))
        self.assertEqual(branch_set["branch_count_actual"], 5)
        beat_plan = load("tests/fixtures/story/beat-plan.json")
        key_movement_ids = {
            movement["movement_id"] for movement in beat_plan["key_emotional_movements"]
        }
        self.assertTrue(set(branch_set["meaning_kernel"]["key_emotional_movement_ids"]).issubset(key_movement_ids))
        for branch in branch_set["branches"]:
            preservation = branch["emotional_tension_preservation"]
            self.assertIn(preservation["key_emotional_movement_id"], key_movement_ids)
            self.assertTrue(preservation["expectation_turn_translation"])
            self.assertGreaterEqual(len(preservation["tension_profile"]), 1)

        styles = {branch["variation_axes"]["style_direction"] for branch in branch_set["branches"]}
        settings = {branch["variation_axes"]["setting"] for branch in branch_set["branches"]}
        symbols = {branch["variation_axes"]["symbolic_representation"] for branch in branch_set["branches"]}
        self.assertGreaterEqual(len(styles), 5)
        self.assertGreaterEqual(len(settings), 5)
        self.assertGreaterEqual(len(symbols), 5)

    def test_prompt_branch_set_to_output_record(self) -> None:
        branch_set = load("tests/fixtures/text-to-image/prompt-branch-set.json")
        output = load("tests/fixtures/outputs/output-record.json")

        self.assertEqual(output["prompt_branch_set_id"], branch_set["prompt_branch_set_id"])
        self.assertEqual(output["prompt_plan_id"], branch_set["prompt_plan_id"])
        self.assertEqual(output["brief_id"], branch_set["brief_id"])
        self.assertEqual(output["source_id"], branch_set["source_id"])
        self.assertEqual(output["artist_meaning_id"], branch_set["artist_meaning_id"])
        self.assertEqual(output["transformation_brief_id"], branch_set["transformation_brief_id"])
        self.assertEqual(output["beat_plan_id"], branch_set["beat_plan_id"])
        self.assertEqual(output["medium_plan_id"], branch_set["medium_plan_id"])
        branch_ids = {branch["branch_id"] for branch in branch_set["branches"]}
        self.assertIn(output["prompt_branch_id"], branch_ids)
        self.assertEqual(output["origin"]["origin_type"], "provider_generated")
        self.assertEqual(output["acceptance_state"]["output_acceptance_status"], "pending")

    def test_output_record_to_output_review_to_acceptance_gate(self) -> None:
        output = load("tests/fixtures/outputs/output-record.json")
        review = load("tests/fixtures/reviews/output-review-record.json")
        gate = load("tests/fixtures/gates/output-acceptance-gate.json")

        self.assertEqual(review["review_role"], "output_critic")
        self.assertEqual(review["artifact_under_review"]["artifact_type"], "output_record")
        self.assertEqual(review["artifact_under_review"]["artifact_id"], output["output_record_id"])
        self.assertEqual(review["upstream_context"]["source_id"], output["source_id"])
        self.assertEqual(review["upstream_context"]["artist_meaning_id"], output["artist_meaning_id"])
        self.assertEqual(review["approval_status"], "approve")
        for assessment in review["emotional_tension_review"]["tension_intensity_assessments"]:
            self.assertGreaterEqual(
                assessment["reviewer_assessed_intensity"],
                assessment["minimum_required_intensity"],
            )
            self.assertTrue(assessment["meets_minimum"])
        self.assertEqual(gate["gate_type"], "output_acceptance")
        self.assertEqual(gate["gate_status"], "approved")
        self.assertEqual(gate["artist_meaning_id"], output["artist_meaning_id"])
        refs = {(ref["ref_type"], ref["ref_id"]) for ref in gate["upstream_refs"]}
        self.assertIn(("output_record", output["output_record_id"]), refs)
        self.assertIn(("review_record", review["review_record_id"]), refs)
        self.assertFalse(gate["proceed_unconfirmed"])

    def test_blocked_output_review_can_proceed_only_with_artist_waiver(self) -> None:
        output = load("tests/fixtures/outputs/output-record.json")
        review = load("tests/fixtures/reviews/output-review-blocked-waived-record.json")
        gate = load("tests/fixtures/gates/output-acceptance-waiver-gate.json")

        self.assertEqual(review["review_role"], "output_critic")
        self.assertEqual(review["artifact_under_review"]["artifact_id"], output["output_record_id"])
        self.assertEqual(review["approval_status"], "block")
        self.assertTrue(review["artist_waiver"]["waived"])
        self.assertEqual(review["artist_waiver"]["waived_by"], "artist")
        failed_assessments = [
            assessment
            for assessment in review["emotional_tension_review"]["tension_intensity_assessments"]
            if not assessment["meets_minimum"]
        ]
        self.assertGreaterEqual(len(failed_assessments), 1)
        for assessment in failed_assessments:
            self.assertLess(
                assessment["reviewer_assessed_intensity"],
                assessment["minimum_required_intensity"],
            )
        self.assertEqual(gate["gate_type"], "output_acceptance")
        self.assertEqual(gate["gate_status"], "approved")
        self.assertIn("waive", gate["artist_response"].lower())
        refs = {(ref["ref_type"], ref["ref_id"]) for ref in gate["upstream_refs"]}
        self.assertIn(("output_record", output["output_record_id"]), refs)
        self.assertIn(("review_record", review["review_record_id"]), refs)
        self.assertFalse(gate["proceed_unconfirmed"])

    def test_sound_creative_brief_to_sound_prompt_plan(self) -> None:
        sound_brief = load("tests/fixtures/text-to-suno/sound-creative-brief.json")
        sound_plan = load("tests/fixtures/text-to-suno/sound-medium-plan.json")
        sound_prompt = load("tests/fixtures/text-to-suno/sound-prompt-plan.json")
        prompt_review = load("tests/fixtures/reviews/suno-prompt-critic-review-record.json")
        prompt_lock_gate = load("tests/fixtures/gates/suno-prompt-lock-gate.json")

        self.assertEqual(sound_prompt["brief_id"], sound_brief["brief_id"])
        self.assertEqual(sound_prompt["source_id"], sound_brief["source_id"])
        self.assertEqual(sound_prompt["artist_meaning_id"], sound_brief["artist_meaning_id"])
        self.assertEqual(sound_prompt["transformation_brief_id"], sound_brief["transformation_brief_id"])
        self.assertEqual(sound_prompt["beat_plan_id"], sound_brief["beat_plan_id"])
        self.assertEqual(sound_prompt["sound_medium_plan_id"], sound_plan["sound_medium_plan_id"])
        self.assertEqual(sound_prompt["approval_refs"]["prompt_critic_review_id"], prompt_review["review_record_id"])
        self.assertEqual(prompt_review["review_role"], "prompt_critic")
        self.assertEqual(prompt_review["artifact_under_review"]["artifact_id"], sound_prompt["prompt_plan_id"])
        self.assertEqual(sound_prompt["approval_refs"]["prompt_lock_gate_id"], prompt_lock_gate["gate_decision_id"])
        self.assertEqual(prompt_lock_gate["gate_type"], "prompt_lock")
        self.assertIn(("review_record", prompt_review["review_record_id"]), ref_pairs(prompt_lock_gate["upstream_refs"]))
        beat_plan = load("tests/fixtures/story/beat-plan.json")
        beat_ids = {beat["beat_id"] for beat in beat_plan["beats"]}
        key_movement_ids = {
            movement["movement_id"] for movement in beat_plan["key_emotional_movements"]
        }
        contract = sound_prompt["emotional_tension_contract"]
        self.assertTrue(set(contract["key_emotional_movement_ids"]).issubset(key_movement_ids))
        for preserved_turn in contract["expectation_turn_preservation"]:
            self.assertIn(preserved_turn["beat_id"], beat_ids)
            self.assertIn(preserved_turn["key_emotional_movement_id"], key_movement_ids)
        for section in sound_prompt["song_structure"]["sections"]:
            self.assertIn(section["beat_id"], beat_ids)
            self.assertIn(section["key_emotional_movement_id"], key_movement_ids)
            self.assertTrue(section["expectation_turn_translation"])
            self.assertGreaterEqual(len(section["tension_profile"]), 1)
        for variant in sound_prompt["prompt_variants"]:
            variant_movement_ids = variant["emotional_tension_preservation"]["key_emotional_movement_ids"]
            self.assertTrue(set(variant_movement_ids).issubset(key_movement_ids))

    def test_beat_plan_to_text_medium_plan(self) -> None:
        beat_plan = load("tests/fixtures/story/beat-plan.json")
        text_plan = load("tests/fixtures/text-journey/text-medium-plan.json")

        self.assertEqual(text_plan["beat_plan_id"], beat_plan["beat_plan_id"])
        self.assertEqual(text_plan["source_id"], beat_plan["source_id"])
        self.assertEqual(text_plan["artist_meaning_id"], beat_plan["artist_meaning_id"])
        self.assertEqual(text_plan["transformation_brief_id"], beat_plan["transformation_brief_id"])
        self.assertEqual(text_plan["target_media_type"], "text")
        self.assertEqual(text_plan["fidelity_policy"]["mode"], "adapt_source_wording")
        key_movement_ids = {
            movement["movement_id"] for movement in beat_plan["key_emotional_movements"]
        }
        for section in text_plan["structure_plan"]["sections"]:
            self.assertIn(section["key_emotional_movement_id"], key_movement_ids)
            self.assertTrue(section["section_job"])
            self.assertTrue(section["paragraph_distinction"])

    def test_text_medium_plan_to_text_creative_brief(self) -> None:
        text_plan = load("tests/fixtures/text-journey/text-medium-plan.json")
        text_brief = load("tests/fixtures/text-journey/text-creative-brief.json")
        writing_review = load("tests/fixtures/reviews/text-writing-critic-review-record.json")
        brief_gate = load("tests/fixtures/gates/text-brief-approval-gate.json")

        self.assertEqual(text_brief["text_medium_plan_id"], text_plan["text_medium_plan_id"])
        self.assertEqual(text_brief["beat_plan_id"], text_plan["beat_plan_id"])
        self.assertEqual(text_brief["source_id"], text_plan["source_id"])
        self.assertEqual(text_brief["artist_meaning_id"], text_plan["artist_meaning_id"])
        self.assertEqual(text_brief["transformation_brief_id"], text_plan["transformation_brief_id"])
        self.assertEqual(text_brief["target_media_type"], "text")
        self.assertEqual(text_brief["primary_text_form"], text_plan["text_form"]["primary_text_form"])
        self.assertEqual(text_brief["fidelity_policy"]["mode"], text_plan["fidelity_policy"]["mode"])
        self.assertNotIn("beats", text_brief)
        self.assertEqual(text_brief["approval_refs"]["writing_critic_review_id"], writing_review["review_record_id"])
        self.assertEqual(writing_review["review_role"], "writing_critic")
        self.assertEqual(writing_review["artifact_under_review"]["artifact_id"], text_brief["brief_id"])
        self.assertEqual(text_brief["approval_refs"]["brief_approval_gate_id"], brief_gate["gate_decision_id"])
        self.assertEqual(brief_gate["gate_type"], "brief_approval")
        self.assertIn(("review_record", writing_review["review_record_id"]), ref_pairs(brief_gate["upstream_refs"]))

    def test_text_creative_brief_to_text_generation_plan(self) -> None:
        text_plan = load("tests/fixtures/text-journey/text-medium-plan.json")
        text_brief = load("tests/fixtures/text-journey/text-creative-brief.json")
        generation_plan = load("tests/fixtures/text-journey/text-generation-plan.json")
        prompt_review = load("tests/fixtures/reviews/text-prompt-critic-review-record.json")
        prompt_lock_gate = load("tests/fixtures/gates/text-prompt-lock-gate.json")
        draft_gate = load("tests/fixtures/gates/text-draft-generation-approval-gate.json")

        self.assertEqual(generation_plan["brief_id"], text_brief["brief_id"])
        self.assertEqual(generation_plan["source_id"], text_brief["source_id"])
        self.assertEqual(generation_plan["artist_meaning_id"], text_brief["artist_meaning_id"])
        self.assertEqual(generation_plan["transformation_brief_id"], text_brief["transformation_brief_id"])
        self.assertEqual(generation_plan["beat_plan_id"], text_brief["beat_plan_id"])
        self.assertEqual(generation_plan["text_medium_plan_id"], text_plan["text_medium_plan_id"])
        self.assertTrue(generation_plan["fresh_context_drafting"]["required"])
        self.assertEqual(generation_plan["human_voice_pass_policy"]["status"], "recommended")
        self.assertEqual(generation_plan["clear_writing_pass_policy"]["status"], "recommended")
        self.assertLess(
            generation_plan["clear_writing_pass_policy"]["default_order"],
            generation_plan["human_voice_pass_policy"]["default_order"],
        )
        trace_source_types = {note["source_type"] for note in generation_plan["traceability_summary"]}
        self.assertIn("text_creative_brief", trace_source_types)
        post_plan_refs = generation_plan["approval_refs"]["post_plan_gates_required"]
        self.assertEqual(post_plan_refs["prompt_critic_review_id"], prompt_review["review_record_id"])
        self.assertEqual(prompt_review["review_role"], "prompt_critic")
        self.assertEqual(prompt_review["artifact_under_review"]["artifact_id"], generation_plan["text_generation_plan_id"])
        self.assertEqual(post_plan_refs["prompt_lock_gate_id"], prompt_lock_gate["gate_decision_id"])
        self.assertEqual(prompt_lock_gate["gate_type"], "prompt_lock")
        self.assertIn(("review_record", prompt_review["review_record_id"]), ref_pairs(prompt_lock_gate["upstream_refs"]))
        self.assertEqual(post_plan_refs["draft_generation_approval_gate_id"], draft_gate["gate_decision_id"])
        self.assertEqual(draft_gate["gate_type"], "draft_generation_approval")

    def test_text_generation_plan_to_draft_and_rewrite_output_records(self) -> None:
        generation_plan = load("tests/fixtures/text-journey/text-generation-plan.json")
        draft_output = load("tests/fixtures/text-journey/output-record-draft.json")
        clear_output = load("tests/fixtures/text-journey/output-record-clear-writing.json")
        rewrite_output = load("tests/fixtures/text-journey/output-record-human-voice.json")
        draft_gate = load("tests/fixtures/gates/text-draft-generation-approval-gate.json")

        self.assertEqual(draft_output["prompt_plan_id"], generation_plan["text_generation_plan_id"])
        self.assertEqual(draft_output["text_generation_plan_id"], generation_plan["text_generation_plan_id"])
        self.assertIsNone(draft_output["previous_output_record_id"])
        self.assertEqual(draft_output["target_media_type"], "text")
        self.assertEqual(draft_output["origin"]["origin_type"], "agent_drafted")
        self.assertEqual(draft_output["origin"]["generation_approval_ref"], draft_gate["gate_decision_id"])
        self.assertGreater(timestamp(draft_output), timestamp(draft_gate))
        draft_trace = [note for note in draft_output["traceability_summary"] if note["source_type"] == "medium_plan"]
        self.assertGreaterEqual(len(draft_trace), 1)
        self.assertIn("section", draft_trace[0]["note"].lower())
        generation_plan_trace = [
            note for note in draft_output["traceability_summary"]
            if note["source_type"] == "text_generation_plan"
        ]
        self.assertGreaterEqual(len(generation_plan_trace), 1)

        self.assertEqual(clear_output["prompt_plan_id"], generation_plan["text_generation_plan_id"])
        self.assertEqual(clear_output["text_generation_plan_id"], generation_plan["text_generation_plan_id"])
        self.assertEqual(clear_output["previous_output_record_id"], draft_output["output_record_id"])
        self.assertEqual(clear_output["origin"]["origin_type"], "agent_rewritten")
        clear_notes = [
            note for note in clear_output["traceability_summary"]
            if note["source_type"] == "output_record"
        ]
        self.assertGreaterEqual(len(clear_notes), 1)
        self.assertIn("clear writing", clear_notes[0]["note"].lower())
        self.assertGreater(timestamp(clear_output), timestamp(draft_output))

        self.assertEqual(rewrite_output["prompt_plan_id"], generation_plan["text_generation_plan_id"])
        self.assertEqual(rewrite_output["text_generation_plan_id"], generation_plan["text_generation_plan_id"])
        self.assertEqual(rewrite_output["previous_output_record_id"], clear_output["output_record_id"])
        self.assertEqual(rewrite_output["origin"]["origin_type"], "agent_rewritten")
        rewrite_notes = [
            note for note in rewrite_output["traceability_summary"]
            if note["source_type"] == "output_record"
        ]
        self.assertGreaterEqual(len(rewrite_notes), 1)
        self.assertIn("human voice", rewrite_notes[0]["note"].lower())
        self.assertGreater(timestamp(rewrite_output), timestamp(clear_output))

    def test_agent_rewritten_outputs_reference_previous_output(self) -> None:
        output_paths = [
            "tests/fixtures/text-journey/output-record-draft.json",
            "tests/fixtures/text-journey/output-record-clear-writing.json",
            "tests/fixtures/text-journey/output-record-human-voice.json",
            "tests/fixtures/outputs/output-record.json",
        ]

        for path in output_paths:
            output = load(path)
            if output["origin"]["origin_type"] == "agent_rewritten":
                self.assertIsNotNone(output["previous_output_record_id"], path)

    def test_review_record_reviews_declared_artifact(self) -> None:
        review = load("tests/fixtures/reviews/review-record.json")
        beat_plan = load("tests/fixtures/story/beat-plan.json")
        beat_ids = {beat["beat_id"] for beat in beat_plan["beats"]}
        key_movement_ids = {
            movement["movement_id"] for movement in beat_plan["key_emotional_movements"]
        }

        self.assertEqual(review["reviewer_execution"]["execution_mode"], "bounded_sub_agent")
        self.assertTrue(review["reviewer_execution"]["sub_agent_required"])
        self.assertIn("artist_meaning_id", review["upstream_context"])
        self.assertIn("matched", review)
        self.assertIn("drifted", review)
        self.assertIn("findings", review)
        self.assertIn("recommended_revision", review)
        self.assertIn(review["approval_status"], {"approve", "revise", "block"})
        self.assertIn("emotional_tension_review", review)
        for assessment in review["emotional_tension_review"]["tension_intensity_assessments"]:
            expected_meets_minimum = (
                assessment["reviewer_assessed_intensity"]
                >= assessment["minimum_required_intensity"]
            )
            self.assertEqual(assessment["meets_minimum"], expected_meets_minimum)
        for movement in review["emotional_tension_review"]["key_emotional_movements_reviewed"]:
            self.assertIn(movement["movement_id"], key_movement_ids)
        for turn in review["emotional_tension_review"]["expectation_turns_reviewed"]:
            self.assertIn(turn["beat_id"], beat_ids)

    def test_compact_and_structured_workflow_scale_routing_skips_long_work(self) -> None:
        compact_or_structured_paths = [
            "tests/fixtures/story/beat-plan.json",
            "tests/fixtures/text-to-image/single-image-rehearsal/beat-plan.json",
            "tests/fixtures/text-to-image/single-image-rehearsal/image-medium-plan.json",
            "tests/fixtures/text-to-image/image-medium-plan.json",
            "tests/fixtures/text-to-suno/sound-medium-plan.json",
            "tests/fixtures/text-journey/text-medium-plan.json",
            "tests/fixtures/text-journey/article-rehearsal/beat-plan.json",
            "tests/fixtures/text-journey/article-rehearsal/text-medium-plan.json",
            "tests/fixtures/text-journey/op-ed-rehearsal/beat-plan.json",
            "tests/fixtures/text-journey/op-ed-rehearsal/text-medium-plan.json",
            "tests/fixtures/story/freytag-rehearsal/beat-plan.json",
            "tests/fixtures/story/hero-journey-rehearsal/beat-plan.json",
            "tests/fixtures/story/kishotenketsu-rehearsal/beat-plan.json",
            "tests/fixtures/story/save-the-cat-rehearsal/beat-plan.json",
            "tests/fixtures/story/three-act-rehearsal/beat-plan.json",
            "tests/fixtures/story/fichtean-quiet-crisis-rehearsal/beat-plan.json",
        ]

        for path in compact_or_structured_paths:
            record = load(path)
            with self.subTest(path=path):
                self.assertIn(
                    record["workflow_scale_routing"]["scale_level"],
                    {"compact_artifact", "structured_single_artifact"},
                )
                self.assert_long_work_support(record, should_activate=False, label=path)

    def test_cumulative_workflow_scale_routing_activates_long_work(self) -> None:
        cumulative_paths = [
            "tests/fixtures/text-to-image/three-image-series-rehearsal/beat-plan.json",
            "tests/fixtures/text-to-image/three-image-series-rehearsal/image-medium-plan.json",
            "tests/fixtures/text-journey/cumulative-text-rehearsal/beat-plan.json",
            "tests/fixtures/text-journey/cumulative-text-rehearsal/text-medium-plan.json",
        ]

        for path in cumulative_paths:
            record = load(path)
            with self.subTest(path=path):
                self.assertEqual(record["workflow_scale_routing"]["scale_level"], "cumulative_work")
                self.assert_long_work_support(record, should_activate=True, label=path)

    def test_full_long_form_routing_requires_long_work_support(self) -> None:
        routing_record = {
            "workflow_scale_routing": {
                "scale_level": "full_long_form_project",
                "activated_supports": [
                    "core_pipeline",
                    LONG_WORK_SUPPORT,
                    "long_work_parts",
                    "long_work_readiness",
                    "long_work_checkpoints",
                ],
                "skipped_supports": [
                    "collection_coherence_review",
                ],
            }
        }

        self.assert_long_work_support(
            routing_record,
            should_activate=True,
            label="purpose-built full_long_form_project routing",
        )

    def test_beat_plan_to_foundation_long_work_stewardship(self) -> None:
        stewardship = load("tests/fixtures/long-work/foundation-stewardship-record.json")
        beat_plan = {
            "beat_plan_id": stewardship["beat_plan_id"],
            "source_id": stewardship["source_id"],
            "artist_meaning_id": stewardship["artist_meaning_id"],
            "workflow_scale_routing": {
                "scale_level": "cumulative_work",
                "activated_supports": ["core_pipeline", LONG_WORK_SUPPORT],
                "skipped_supports": ["collection_coherence_review"],
            },
        }

        self.assert_long_work_support(
            beat_plan,
            should_activate=True,
            label="purpose-built foundation source routing",
        )
        self.assertEqual(stewardship["beat_plan_id"], beat_plan["beat_plan_id"])
        self.assertEqual(stewardship["source_id"], beat_plan["source_id"])
        self.assertEqual(stewardship["artist_meaning_id"], beat_plan["artist_meaning_id"])
        self.assertIsNone(stewardship["medium_plan_id"])
        self.assertEqual(stewardship["part_plan"], [])
        self.assertEqual(stewardship["stewardship_status"], "planned")
        self.assertEqual(stewardship["readiness_review"]["status"], "pending")
        self.assertEqual(stewardship["checkpoints"][0]["checkpoint_type"], "foundation")

    def test_beat_plan_to_image_series_long_work_stewardship(self) -> None:
        beat_plan = {
            "beat_plan_id": "bp_door_left_lit",
            "source_id": "src_door_left_lit",
            "artist_meaning_id": "meaning_door_left_lit",
            "workflow_scale_routing": {
                "scale_level": "cumulative_work",
                "activated_supports": ["core_pipeline", LONG_WORK_SUPPORT],
                "skipped_supports": ["collection_coherence_review"],
            },
            "beats": [{"beat_id": "beat_threshold_001"}],
            "key_emotional_movements": [{"movement_id": "kem_threshold_001"}],
        }
        image_plan = {
            "image_medium_plan_id": "imp_door_left_lit",
            "workflow_scale_routing": {
                "scale_level": "cumulative_work",
                "activated_supports": ["core_pipeline", LONG_WORK_SUPPORT],
                "skipped_supports": ["collection_coherence_review"],
            },
            "image_roles": [{"image_role_id": "imgrole_threshold_001"}],
        }
        stewardship = load("tests/fixtures/long-work/image-series-stewardship-record.json")

        self.assert_long_work_support(beat_plan, should_activate=True, label="image series beat plan")
        self.assert_long_work_support(image_plan, should_activate=True, label="image series medium plan")
        self.assertEqual(stewardship["beat_plan_id"], beat_plan["beat_plan_id"])
        self.assertEqual(stewardship["source_id"], beat_plan["source_id"])
        self.assertEqual(stewardship["artist_meaning_id"], beat_plan["artist_meaning_id"])
        self.assertEqual(stewardship["medium_plan_id"], image_plan["image_medium_plan_id"])
        self.assertEqual(stewardship["target_media_type"], "image")
        self.assertEqual(stewardship["cumulative_work_type"], "image_series")

        image_role_ids = {role["image_role_id"] for role in image_plan["image_roles"]}
        beat_ids = {beat["beat_id"] for beat in beat_plan["beats"]}
        key_movement_ids = {
            movement["movement_id"] for movement in beat_plan["key_emotional_movements"]
        }
        for part in stewardship["part_plan"]:
            self.assertEqual(part["medium_part_ref"]["ref_type"], "image_role")
            self.assertIn(part["medium_part_ref"]["ref_id"], image_role_ids)
            self.assertIn(part["beat_id"], beat_ids)
            self.assertIn(part["key_emotional_movement_id"], key_movement_ids)
            self.assertNotIn("shot_design", part)
            self.assertNotIn("amplitude_profile", part)

    def test_text_medium_plan_to_long_work_stewardship(self) -> None:
        beat_plan = load("tests/fixtures/text-journey/cumulative-text-rehearsal/beat-plan.json")
        text_plan = load("tests/fixtures/text-journey/cumulative-text-rehearsal/text-medium-plan.json")
        stewardship = load("tests/fixtures/long-work/cumulative-text-rehearsal/text-stewardship-record.json")

        self.assert_long_work_support(beat_plan, should_activate=True, label="long text beat plan")
        self.assert_long_work_support(text_plan, should_activate=True, label="long text medium plan")
        self.assertEqual(stewardship["beat_plan_id"], beat_plan["beat_plan_id"])
        self.assertEqual(stewardship["source_id"], beat_plan["source_id"])
        self.assertEqual(stewardship["artist_meaning_id"], beat_plan["artist_meaning_id"])
        self.assertEqual(stewardship["medium_plan_id"], text_plan["text_medium_plan_id"])
        self.assertEqual(stewardship["target_media_type"], "text")
        self.assertEqual(stewardship["cumulative_work_type"], "long_text")

        section_ids = {
            section["section_id"]
            for section in text_plan["structure_plan"]["sections"]
        }
        for part in stewardship["part_plan"]:
            self.assertEqual(part["medium_part_ref"]["ref_type"], "text_section")
            self.assertIn(part["medium_part_ref"]["ref_id"], section_ids)
            self.assertIn(part["beat_id"], {beat["beat_id"] for beat in beat_plan["beats"]})
            self.assertIn(
                part["key_emotional_movement_id"],
                {movement["movement_id"] for movement in beat_plan["key_emotional_movements"]},
            )
            self.assertTrue(part["part_job"])
            self.assertNotIn("section_execution", part)
            self.assertNotIn("voice_point_of_view", part)


if __name__ == "__main__":
    unittest.main()
