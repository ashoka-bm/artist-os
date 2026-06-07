from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((REPO_ROOT / path).read_text(encoding="utf-8"))


class PipelineTransitionTests(unittest.TestCase):
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

    def test_image_medium_plan_to_image_creative_brief(self) -> None:
        image_plan = load("tests/fixtures/text-to-image/image-medium-plan.json")
        creative_brief = load("tests/fixtures/text-to-image/creative-brief.json")

        self.assertEqual(creative_brief["beat_plan_id"], image_plan["beat_plan_id"])
        self.assertEqual(creative_brief["source_id"], image_plan["source_id"])
        self.assertEqual(creative_brief["artist_meaning_id"], image_plan["artist_meaning_id"])
        self.assertEqual(creative_brief["transformation_brief_id"], image_plan["transformation_brief_id"])
        self.assertIn("beat_plan_id", creative_brief)
        self.assertIn("transformation_brief_id", creative_brief)
        self.assertGreaterEqual(len(creative_brief["beats"]), 1)

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

        self.assertEqual(sound_brief["beat_plan_id"], sound_plan["beat_plan_id"])
        self.assertEqual(sound_brief["source_id"], sound_plan["source_id"])
        self.assertEqual(sound_brief["artist_meaning_id"], sound_plan["artist_meaning_id"])
        self.assertEqual(sound_brief["transformation_brief_id"], sound_plan["transformation_brief_id"])
        self.assertIn("transformation_brief_id", sound_brief)
        self.assertGreaterEqual(len(sound_brief["beats"]), 1)

    def test_image_creative_brief_to_prompt_plan(self) -> None:
        creative_brief = load("tests/fixtures/text-to-image/creative-brief.json")
        image_plan = load("tests/fixtures/text-to-image/image-medium-plan.json")
        prompt_plan = load("tests/fixtures/text-to-image/prompt-plan.json")

        self.assertEqual(prompt_plan["brief_id"], creative_brief["brief_id"])
        self.assertEqual(prompt_plan["source_id"], creative_brief["source_id"])
        self.assertEqual(prompt_plan["artist_meaning_id"], creative_brief["artist_meaning_id"])
        self.assertEqual(prompt_plan["transformation_brief_id"], creative_brief["transformation_brief_id"])
        self.assertEqual(prompt_plan["beat_plan_id"], creative_brief["beat_plan_id"])
        self.assertEqual(prompt_plan["image_medium_plan_id"], image_plan["image_medium_plan_id"])

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

        self.assertEqual(sound_prompt["brief_id"], sound_brief["brief_id"])
        self.assertEqual(sound_prompt["source_id"], sound_brief["source_id"])
        self.assertEqual(sound_prompt["artist_meaning_id"], sound_brief["artist_meaning_id"])
        self.assertEqual(sound_prompt["transformation_brief_id"], sound_brief["transformation_brief_id"])
        self.assertEqual(sound_prompt["beat_plan_id"], sound_brief["beat_plan_id"])
        self.assertEqual(sound_prompt["sound_medium_plan_id"], sound_plan["sound_medium_plan_id"])

    def test_review_record_reviews_declared_artifact(self) -> None:
        review = load("tests/fixtures/reviews/review-record.json")

        self.assertEqual(review["reviewer_execution"]["execution_mode"], "bounded_sub_agent")
        self.assertTrue(review["reviewer_execution"]["sub_agent_required"])
        self.assertIn("artist_meaning_id", review["upstream_context"])
        self.assertIn("matched", review)
        self.assertIn("drifted", review)
        self.assertIn("findings", review)
        self.assertIn("recommended_revision", review)
        self.assertIn(review["approval_status"], {"approve", "revise", "block"})


if __name__ == "__main__":
    unittest.main()
