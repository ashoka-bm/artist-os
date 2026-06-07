from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


REVIEWER_SKILLS = [
    ("skills/art-critic-review/SKILL.md", "artist-os-art-critic-review"),
    ("skills/critique-asset/SKILL.md", "artist-os-critique-asset"),
    ("skills/writing-method-review/SKILL.md", "artist-os-writing-method-review"),
]


class ReviewerSkillContractTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
