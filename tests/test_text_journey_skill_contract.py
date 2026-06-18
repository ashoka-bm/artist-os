from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


# Cheap regression guard for the Text Journey Slice skills. They shipped with
# routing-eval coverage (the `description:` triggers correctly) but no
# body-contract guard, unlike the reviewer family
# (test_reviewer_skill_contract.py) and the medium-plan family
# (test_medium_plan_skill_contract.py). This closes that gap.
#
# Same philosophy as the medium-plan guard: pin what must SURVIVE a leanness or
# dedup edit -- routing identity, canonical-doc pointers, standalone hard gates,
# pattern anchors, schema ids -- and NOT the collapsible detail a dedup pass may
# legitimately move out to a canonical doc.
#
# Two contract shapes live in one file because these three skills ship together
# as one feature but are structurally different:
#
#   * text-journey is a journey DIRECTOR, a sibling of the text-to-image-plan /
#     text-to-suno-plan medium-plan skills. Guarded with the same structured
#     dict the medium-plan guard uses.
#   * clear-writing-pass / human-voice-pass are bounded editorial-pass
#     SUB-AGENTS. Their load-bearing invariant is the boundary that separates
#     them from the Output Critic: they rewrite the artifact and MUST NOT emit a
#     Review Record. Guarded with a shared required-fragment list.


TEXT_JOURNEY_SKILL = "skills/text-journey/SKILL.md"

# The director skill. Mirrors MEDIUM_PLAN_SKILLS in the medium-plan guard.
TEXT_JOURNEY_SPEC = {
    "frontmatter_name": "artist-os-text-journey",
    # Pointers to single-source-of-truth docs. Dedup may collapse a restated
    # rule, but the pointer itself must remain or the rule becomes unreachable.
    "canonical_refs": [
        "docs/output-journeys/text.md",
        "docs/writing/README.md",
        "docs/story/THEORY.md",
        "docs/gates-and-reviews.md",
        "docs/storage.md",
    ],
    # Standalone safety rails. The skill states these hold "whether you run
    # standalone or under the artist-os conductor"; a standalone run has no
    # conductor to enforce them, so they must stay stated here.
    "hard_gates": [
        "whether you run standalone or under the",
        "Do not create a Text Creative Brief Record or Text Generation Plan until Writing Critic Review and Brief Approval are complete.",
        "Do not draft the final written Output Artifact until Draft Generation Approval is explicit",
        "Draft the written Output Artifact in a fresh-context sub-agent using a bounded Text Draft Packet.",
        "The fresh-context drafting sub-agent must not run the Human Voice Pass or Clear Writing Pass during first drafting.",
        "Chat context is not durable storage.",
    ],
    # Names of shared patterns whose detail may move to a canonical doc, but
    # whose name must stay so the skill still invokes the behavior.
    "anchors": [
        "Expectation Turn",
        "Intended Feeling",
        "Long-Work Stewardship Record",
        "Text Draft Packet",
        "Writing Critic Review",
        "Beat Plan",
    ],
    # The records this skill is responsible for producing.
    "schema_ids": [
        "schemas/transformation-brief.schema.json",
        "schemas/beat-plan.schema.json",
        "schemas/text-medium-plan.schema.json",
        "schemas/text-creative-brief.schema.json",
        "schemas/text-generation-plan.schema.json",
        "schemas/long-work-stewardship-record.schema.json",
        "schemas/output-record.schema.json",
    ],
}


# The two editorial passes. Mirrors REVIEWER_SKILLS in the reviewer guard.
EDITORIAL_PASS_SKILLS = [
    ("skills/clear-writing-pass/SKILL.md", "artist-os-clear-writing-pass"),
    ("skills/human-voice-pass/SKILL.md", "artist-os-human-voice-pass"),
]


class TextJourneyDirectorContractTests(unittest.TestCase):
    def _read(self) -> str:
        return (REPO_ROOT / TEXT_JOURNEY_SKILL).read_text(encoding="utf-8")

    def test_keeps_routing_identity(self) -> None:
        # A leanness refactor must not rename the skill out from under the
        # routing eval and conductor delegation table.
        self.assertIn(
            f"name: {TEXT_JOURNEY_SPEC['frontmatter_name']}", self._read()
        )

    def test_keeps_canonical_doc_references(self) -> None:
        # Dedup-by-reference may remove a restated rule, but never the pointer
        # to its canonical home.
        text = self._read()
        for ref in TEXT_JOURNEY_SPEC["canonical_refs"]:
            with self.subTest(ref=ref):
                self.assertIn(ref, text)

    def test_keeps_standalone_hard_gates(self) -> None:
        # These gates are duplicated from the conductor on purpose: a standalone
        # run has no conductor to enforce them.
        text = self._read()
        for gate in TEXT_JOURNEY_SPEC["hard_gates"]:
            with self.subTest(gate=gate):
                self.assertIn(gate, text)

    def test_keeps_shared_pattern_anchors(self) -> None:
        # The detail behind these patterns may move to a canonical doc, but the
        # name must remain so the skill still invokes the behavior.
        text = self._read()
        for anchor in TEXT_JOURNEY_SPEC["anchors"]:
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, text)

    def test_declares_required_schema_ids(self) -> None:
        text = self._read()
        for schema_id in TEXT_JOURNEY_SPEC["schema_ids"]:
            with self.subTest(schema_id=schema_id):
                self.assertIn(schema_id, text)


class EditorialPassContractTests(unittest.TestCase):
    def _read(self, skill_path: str) -> str:
        return (REPO_ROOT / skill_path).read_text(encoding="utf-8")

    def test_keeps_routing_identity(self) -> None:
        for skill_path, name in EDITORIAL_PASS_SKILLS:
            with self.subTest(skill=skill_path):
                self.assertIn(f"name: {name}", self._read(skill_path))

    def test_runs_as_bounded_rewrite_only_sub_agent(self) -> None:
        # The pass rewrites the current artifact in a fresh-context sub-agent;
        # it must never start a piece from scratch.
        for skill_path, _name in EDITORIAL_PASS_SKILLS:
            text = self._read(skill_path)
            with self.subTest(skill=skill_path):
                self.assertIn("bounded fresh-context editorial sub-agent", text)
                self.assertIn("Do not create a new piece from scratch", text)
                self.assertIn(
                    "Rewrite only the current written Output Artifact", text
                )

    def test_keeps_packet_completeness_gate(self) -> None:
        # If the packet lacks the artifact text, protected features, or
        # source-wording policy, the pass stops and asks -- it does not improvise.
        for skill_path, _name in EDITORIAL_PASS_SKILLS:
            text = self._read(skill_path)
            with self.subTest(skill=skill_path):
                self.assertIn("protected features", text)
                self.assertIn("source-wording policy", text)
                self.assertIn("stop and ask for the missing packet field", text)

    def test_keeps_policy_bounded_edit_degrees(self) -> None:
        # Degrees exist and the deep degree is gated on Text Generation Plan
        # authorization, so a pass cannot restructure on its own initiative.
        # Form sensitivity keeps it from flattening poems, lyrics, etc.
        for skill_path, _name in EDITORIAL_PASS_SKILLS:
            text = self._read(skill_path)
            with self.subTest(skill=skill_path):
                for degree in ("Light", "Standard", "Deep"):
                    self.assertIn(degree, text)
                self.assertIn("authorizes structural edits", text)
                self.assertIn("Do not flatten", text)

    def test_keeps_rewrite_output_contract(self) -> None:
        for skill_path, _name in EDITORIAL_PASS_SKILLS:
            text = self._read(skill_path)
            with self.subTest(skill=skill_path):
                for field in (
                    "rewritten_artifact",
                    "change_trace",
                    "conformance_notes",
                    "recommended_output_record_origin",
                    "agent_rewritten",
                ):
                    self.assertIn(field, text)

    def test_is_an_editorial_pass_not_a_reviewer(self) -> None:
        # The load-bearing boundary: an editorial pass rewrites; it does NOT
        # emit a Review Record. Blurring this would let a polish step
        # masquerade as Output Critic Review and skip the real gate.
        for skill_path, _name in EDITORIAL_PASS_SKILLS:
            text = self._read(skill_path)
            with self.subTest(skill=skill_path):
                self.assertIn("Do not emit a Review Record", text)
                self.assertIn("not Output Critic Review", text)


if __name__ == "__main__":
    unittest.main()
