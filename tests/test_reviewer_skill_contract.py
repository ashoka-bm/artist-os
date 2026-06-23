from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


REVIEWER_SKILLS = [
    ("skills/artist-os/references/art-critic-review.md", "artist-os-art-critic-review"),
    ("skills/artist-os/references/critique-asset.md", "artist-os-critique-asset"),
    ("skills/artist-os/references/writing-method-review.md", "artist-os-writing-method-review"),
]


# The medium critics enforce the blocking rules that live in the shared
# gates-and-reviews contract (Shot Design, the Expectation Turn, minimum
# tension criteria). They must point at that contract so its rules cannot
# drift out of the skills that actually run the reviews. The Beat Reviewer
# (writing-method-review) enforces a different contract section and is
# intentionally excluded.
MEDIUM_CRITIC_SKILLS = [
    "skills/artist-os/references/art-critic-review.md",
    "skills/artist-os/references/critique-asset.md",
]

CONDUCTOR_SKILL = "skills/artist-os/SKILL.md"


class ReviewerSkillContractTests(unittest.TestCase):
    def test_conductor_exposes_review_modes(self) -> None:
        text = (REPO_ROOT / CONDUCTOR_SKILL).read_text(encoding="utf-8")
        self.assertIn("Internal mode map", text)
        for skill_path, _source_skill in REVIEWER_SKILLS:
            with self.subTest(skill=skill_path):
                self.assertIn(skill_path, text)

    def test_reviewer_skills_require_schema_valid_review_record_first(self) -> None:
        required_fragments = [
            "schemas/review-record.schema.json",
            "Review Record JSON",
            "Put this object first",
            "bounded_sub_agent",
            "sub_agent_required",
            "source_skill",
            "artifact_under_review",
            "upstream_context",
            "matched",
            "drifted",
            "findings",
            "recommended_revision",
            "approval_status",
        ]

        for skill_path, source_skill in REVIEWER_SKILLS:
            text = (REPO_ROOT / skill_path).read_text(encoding="utf-8")
            with self.subTest(skill=skill_path):
                for fragment in required_fragments:
                    self.assertIn(fragment, text)
                self.assertIn(source_skill, text)

    def test_reviewer_skills_keep_sub_agent_and_drift_rules(self) -> None:
        for skill_path, _source_skill in REVIEWER_SKILLS:
            text = (REPO_ROOT / skill_path).read_text(encoding="utf-8")
            with self.subTest(skill=skill_path):
                self.assertIn("bounded reviewer sub-agent", text)
                self.assertIn("separate from the creating agent", text)
                self.assertIn("Always check for drift", text)
                self.assertIn("Only the artist can waive", text)

    def test_medium_critics_reference_gates_contract(self) -> None:
        for skill_path in MEDIUM_CRITIC_SKILLS:
            text = (REPO_ROOT / skill_path).read_text(encoding="utf-8")
            with self.subTest(skill=skill_path):
                self.assertIn("docs/gates-and-reviews.md", text)
                self.assertIn("Shot Design", text)


if __name__ == "__main__":
    unittest.main()
