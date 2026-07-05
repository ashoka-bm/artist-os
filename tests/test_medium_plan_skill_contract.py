from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


# Cheap regression guard for leanness work on the internal medium-plan modes.
# The public `artist-os` skill stays small; these internal files carry the
# load-bearing mode behavior and remain protected by contract tests.
#
# The guard pins what must SURVIVE a leanness edit, not the prose that may
# legitimately move out:
#
#   * canonical_refs  -- pointers to the single-source-of-truth docs. Dedup may
#                        collapse a restated rule, but the pointer itself must
#                        remain or the rule becomes unreachable (the 4eeec93 bug).
#   * format_refs     -- contracts already canonicalized elsewhere (Visual Gate
#                        Boards in THEORY.md; Suno Custom Mode Outputs in the
#                        sound ARCHITECTURE). The skill must reference them and
#                        explicitly NOT restate them ("do not restate").
#   * hard_gates      -- standalone safety rails. They are duplicated from the
#                        conductor ON PURPOSE: a standalone skill run has no
#                        conductor to enforce them. They must not be deduped
#                        into a bare reference.
#   * anchors         -- names of shared patterns whose DETAIL may move to a
#                        canonical doc (e.g. the >=0.7 tension default, the
#                        verbatim Decision Interview script), but whose NAME
#                        must stay so the skill still invokes the behavior.
#   * schema_ids      -- the records this skill is responsible for producing.
#
# Deliberately NOT pinned: the collapsible detail itself (the literal "0.7", the
# word-for-word interview script). Pinning those would block the dedup this
# guard is meant to make safe.
MEDIUM_PLAN_SKILLS = {
    "skills/artist-os/references/text-to-image-plan.md": {
        "canonical_refs": [
            "docs/gates-and-reviews.md",
            "THEORY.md",
        ],
        "format_refs": [
            "Visual Gate Boards",
        ],
        "hard_gates": [
            "a standalone run has no conductor",
            "Never call an image generation provider without explicit approval",
            "Do not produce the Creative Brief Record or Provider-Neutral Prompt Plan until Art Critic Review and Brief Approval",
            "Do not create multiple series image prompts until the artist approves a Series Plan",
            "Chat context is not durable storage",
        ],
        "anchors": [
            "Decision Interview",
            "minimum tension criteria",
            "Expectation Turn",
            "Shot Design",
            "primary medium's realization",
        ],
        "schema_ids": [
            "schemas/transformation-brief.schema.json",
            "schemas/beat-plan.schema.json",
            "schemas/image-medium-plan.schema.json",
            "schemas/character-template.schema.json",
            "schemas/visual-reference-sheet-plan.schema.json",
            "schemas/creative-brief.schema.json",
            "schemas/prompt-plan.schema.json",
            "schemas/prompt-branch-set.schema.json",
        ],
    },
    "skills/artist-os/references/text-to-suno-plan.md": {
        "canonical_refs": [
            "docs/gates-and-reviews.md",
            "docs/text-to-sound/THEORY.md",
            "docs/text-to-sound/ARCHITECTURE.md",
        ],
        "format_refs": [
            "Platform Rendering Boundary",
            "Suno Platform Rendering",
        ],
        "hard_gates": [
            "a standalone run has no conductor",
            "Never call Suno or any sound generation provider without explicit approval",
            "Do not produce the Sound Creative Brief Record or Sound Prompt Plan until Music / Sound Critic Review and Brief Approval",
            "Do not invent lyrics unless the artist chooses",
            "Do not lock the final platform rendering until Vocal / Lyric Policy is resolved",
            "Do not create multiple sequence prompt plans until the artist approves a sequence recommendation",
            "Chat context is not durable storage",
        ],
        "anchors": [
            "Decision Interview",
            "minimum tension criteria",
            "Expectation Turn",
            "primary medium's realization",
        ],
        "schema_ids": [
            "schemas/transformation-brief.schema.json",
            "schemas/beat-plan.schema.json",
            "schemas/sound-medium-plan.schema.json",
            "schemas/sound-creative-brief.schema.json",
            "schemas/sound-prompt-plan.schema.json",
            "skills/artist-os/references/platforms/suno-output.md",
        ],
    },
    "skills/artist-os/references/video-journey.md": {
        "canonical_refs": [
            "docs/output-journeys/video.md",
            "docs/gates-and-reviews.md",
            "THEORY.md",
        ],
        "format_refs": [
            "Visual Gate Boards",
        ],
        "hard_gates": [
            "standalone run has no conductor",
            "Never call a video, image, sound, or render provider without explicit approval",
            "Do not claim finished video generation is supported in v0",
            "Do not create a Video Prompt Plan in v0",
            "Do not create generated storyboard stills without Generation Approval",
            "Create/generate the storyboard",
            "Chat context is not durable storage",
        ],
        "anchors": [
            "Storyboard Shot",
            "Video Audio Posture",
            "Video Format Recommendation",
            "Expectation Turn",
            "Intended Feeling",
            "Shot Design",
            "primary medium's realization",
        ],
        "schema_ids": [
            "schemas/transformation-brief.schema.json",
            "schemas/beat-plan.schema.json",
            "schemas/video-medium-plan.schema.json",
            "schemas/character-template.schema.json",
            "schemas/visual-reference-sheet-plan.schema.json",
            "schemas/long-work-stewardship-record.schema.json",
            "schemas/output-record.schema.json",
            "skills/artist-os/references/storyboard-prompt-builder.md",
        ],
    },
}

CONDUCTOR_SKILL = "skills/artist-os/SKILL.md"
FOUNDATION_BEFORE_ENRICHMENT_FRAGMENT = (
    "If medium-level `workflow_scale_routing.activated_supports` newly includes "
    "`long_work_stewardship` and no foundation record exists, create the "
    "foundation record immediately before enrichment."
)


class MediumPlanSkillContractTests(unittest.TestCase):
    def _read(self, skill_path: str) -> str:
        return (REPO_ROOT / skill_path).read_text(encoding="utf-8")

    def test_conductor_exposes_medium_modes(self) -> None:
        text = self._read(CONDUCTOR_SKILL)
        self.assertIn("Internal mode map", text)
        for skill_path in MEDIUM_PLAN_SKILLS:
            with self.subTest(skill=skill_path):
                self.assertIn(skill_path, text)

    def test_conductor_recommends_video_format_from_story_shape(self) -> None:
        text = self._read(CONDUCTOR_SKILL)
        for required in (
            "Before asking for a video format, make a Video Format Recommendation",
            "what kind of story this is",
            "how many smallest Story Beats or Story Movements",
            "recommended video format",
            "why that format fits better than the nearest alternatives",
            "Use broad menus only when there is not enough story material",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_keeps_canonical_doc_references(self) -> None:
        # Dedup-by-reference may remove a restated rule, but never the pointer
        # to its canonical home.
        for skill_path, spec in MEDIUM_PLAN_SKILLS.items():
            text = self._read(skill_path)
            with self.subTest(skill=skill_path):
                for ref in spec["canonical_refs"]:
                    self.assertIn(ref, text)

    def test_references_but_does_not_restate_format_contracts(self) -> None:
        # The board / Suno-output formats are canonical elsewhere; this skill
        # must point at them and explicitly decline to re-specify them.
        for skill_path, spec in MEDIUM_PLAN_SKILLS.items():
            text = self._read(skill_path)
            with self.subTest(skill=skill_path):
                for ref in spec["format_refs"]:
                    self.assertIn(ref, text)
                self.assertIn("do not restate", text)

    def test_keeps_standalone_hard_gates(self) -> None:
        # These gates are duplicated from the conductor on purpose: a standalone
        # run has no conductor to enforce them. They must stay stated here.
        for skill_path, spec in MEDIUM_PLAN_SKILLS.items():
            text = self._read(skill_path)
            with self.subTest(skill=skill_path):
                for gate in spec["hard_gates"]:
                    self.assertIn(gate, text)

    def test_keeps_shared_pattern_anchors(self) -> None:
        # The detail behind these patterns may move to a canonical doc, but the
        # name must remain so the skill still invokes the behavior.
        for skill_path, spec in MEDIUM_PLAN_SKILLS.items():
            text = self._read(skill_path)
            with self.subTest(skill=skill_path):
                for anchor in spec["anchors"]:
                    self.assertIn(anchor, text)

    def test_declares_required_schema_ids(self) -> None:
        for skill_path, spec in MEDIUM_PLAN_SKILLS.items():
            text = self._read(skill_path)
            with self.subTest(skill=skill_path):
                for schema_id in spec["schema_ids"]:
                    self.assertIn(schema_id, text)

    def test_medium_level_long_work_activation_creates_foundation_before_enrichment(self) -> None:
        skill_paths = [CONDUCTOR_SKILL, *MEDIUM_PLAN_SKILLS]
        for skill_path in skill_paths:
            text = self._read(skill_path)
            with self.subTest(skill=skill_path):
                self.assertIn(FOUNDATION_BEFORE_ENRICHMENT_FRAGMENT, text)

    def test_orientation_keeps_promise_and_four_primary_choices(self) -> None:
        text = self._read(CONDUCTOR_SKILL)
        for phrase in [
            "Turn any reference into a complete creative release system",
            "raw spark to finished artifact",
            "- **Image**:",
            "- **Video**:",
            "- **Audio**:",
            "- **Text**:",
            "Album v1",
            "Full Long-Form Project",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)
        menu = text.split("> What do you want to create from this Reference?", 1)[1].split(
            "Then ask the medium-specific output-kind question",
            1,
        )[0]
        self.assertNotIn("- **Create an album**:", menu)
        self.assertNotIn("- **Develop a novel / long-form writing project**:", menu)
        self.assertNotIn("- **Publish a sharp blog essay**:", menu)
        self.assertNotIn("- **Launch a Substack piece**:", menu)
        self.assertNotIn("- **Create a LinkedIn post**:", menu)
        self.assertNotIn("- **Build a multi-output release package**:", menu)


# Slice 1 — Medium Activation (ADR 0012, D1-D8). These guard the behavioral fix
# at the text level, independent of the manual conductor-behavior eval: every
# medium mode reuses an existing Shared Story Spine instead of re-deriving it
# (the Suno re-spin fix), and the conductor carries the Medium Activation
# entry-mode rather than telling the artist to run each medium as a separate flow.
MEDIUM_SPINE_REUSE_FILES = [
    "skills/artist-os/references/text-to-image-plan.md",
    "skills/artist-os/references/text-to-suno-plan.md",
    "skills/artist-os/references/text-journey.md",
    "skills/artist-os/references/video-journey.md",
    "skills/artist-os/references/video-micro-journey-recipe.md",
]
SPINE_REUSE_MARKERS = ("Shared Story Spine", "do not re-derive")
SUNO_SPIN_LINE = "run that flow to completion, then run the next one"


class MediumActivationContractTests(unittest.TestCase):
    def _read(self, skill_path: str) -> str:
        return (REPO_ROOT / skill_path).read_text(encoding="utf-8")

    def test_medium_modes_consume_existing_spine(self) -> None:
        # A future leanness edit must not silently drop the anti-re-derivation rule.
        for skill_path in MEDIUM_SPINE_REUSE_FILES:
            text = self._read(skill_path)
            with self.subTest(skill=skill_path):
                self.assertIn("consume", text)
                for marker in SPINE_REUSE_MARKERS:
                    self.assertIn(marker, text)

    def test_conductor_has_medium_activation_section(self) -> None:
        text = self._read(CONDUCTOR_SKILL)
        for marker in (
            "## Medium Activation",
            "Shared Story Spine",
            "Enter at Phase 8",
            "medium_activated",
            "do not re-derive",
            "resume_state",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_conductor_no_longer_runs_each_medium_as_a_separate_flow(self) -> None:
        # The Suno re-spin line is gone; reuse is now automatic via Medium Activation.
        self.assertNotIn(SUNO_SPIN_LINE, self._read(CONDUCTOR_SKILL))

    def test_conductor_does_not_introduce_a_resume_packet(self) -> None:
        # Decided-against guard (D5): resume state is a projection on project.json.
        self.assertIn("do not write a separate `resume-packet.json`", self._read(CONDUCTOR_SKILL))


class MicroJourneyLeanPathContractTests(unittest.TestCase):
    def _read(self, skill_path: str) -> str:
        return (REPO_ROOT / skill_path).read_text(encoding="utf-8")

    def test_micro_journey_uses_thin_authoring_packet_before_schema(self) -> None:
        text = self._read("skills/artist-os/references/video-micro-journey-recipe.md")
        required = (
            "Compact Video Authoring Packet",
            "thin planning surface",
            "Do not read the schema for this step",
            "Finalize the Video Medium Plan Record",
            "bin/artist-os-video-finalize",
            "Do not use the full schema as the authoring surface",
            "bounded `record_builder` / `schema_validator` finalization pass",
            "stop at the completed Compact Video Authoring Packet with a\nreset handoff",
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_micro_journey_schema_read_is_after_packet_completion(self) -> None:
        text = self._read("skills/artist-os/references/video-micro-journey-recipe.md")
        packet_index = text.index("Produce the Compact Video Authoring Packet")
        finalization_index = text.index("Finalize the Video Medium Plan Record")
        schema_index = text.index("read\n   `schemas/video-medium-plan.schema.json` once")
        self.assertLess(packet_index, finalization_index)
        self.assertLess(finalization_index, schema_index)


# Slice 2 — Medium Roles (ADR 0012, D10). Multi-medium projects outside Album v1
# assign a primary/supporting Medium Role on the Cross-Medium Plan: the primary is
# recommended from the output type and the artist confirms (recommendation-first),
# supporting media default to the compact tier and take continuity from the primary
# medium's realization, and Medium Role (importance) stays distinct from Workflow
# Scale Routing (depth). The review-count reduction half is deferred.
class MediumRoleContractTests(unittest.TestCase):
    def _read(self, skill_path: str) -> str:
        return (REPO_ROOT / skill_path).read_text(encoding="utf-8")

    def test_conductor_states_medium_role_behavior(self) -> None:
        text = self._read(CONDUCTOR_SKILL)
        # Scope to the Medium Role Medium-Specifics bullet so common words
        # ("primary", "supporting", "compact") cannot satisfy the assertion from
        # elsewhere in the conductor.
        self.assertIn("- **Medium Role**", text)
        bullet = text.split("- **Medium Role**", 1)[1].split("\n- ", 1)[0]
        for marker in (
            "primary",
            "supporting",
            "compact treatment tier",
            "obeys the primary medium's realization",
            # Role-vs-scale distinction must be co-located so the two stay distinct.
            "Workflow Scale Routing",
            "seeds the default scale",
        ):
            with self.subTest(marker=marker, scope="medium_role_bullet"):
                self.assertIn(marker, bullet)
        # Recommendation-first primary selection (not hard-coded) lives in the
        # Medium Activation block.
        self.assertIn("Recommend the primary medium from the requested output type", text)
        self.assertIn("ask the artist to **confirm**", text)

    def test_conductor_defers_review_reduction_for_supporting_media(self) -> None:
        # D10: the reduced review count for the compact tier is deferred to the
        # scale-gated-review-count lever, so supporting media must reuse the full
        # standard bounded review set for now. Assert the conductor states the
        # deferral (positive) AND has not prematurely wired the deferred marker.
        text = self._read(CONDUCTOR_SKILL)
        self.assertIn("full standard bounded review set for now", text)
        self.assertNotIn("compact_scale_inline_review", text)


if __name__ == "__main__":
    unittest.main()
