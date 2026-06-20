from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class StoryStructureContractTests(unittest.TestCase):
    def _read(self, relative_path: str) -> str:
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    def _story_entry_links(self, relative_path: str) -> set[str]:
        text = self._read(relative_path)
        return {
            match.group(1)
            for match in re.finditer(r"\]\(story/([a-z0-9-]+\.md)\)", text)
        } | {
            match.group(1)
            for match in re.finditer(r"\]\(([a-z0-9-]+\.md)\)", text)
            if relative_path == "docs/structure-library/story/README.md"
        }

    def test_story_structure_indexes_reference_existing_entries(self) -> None:
        links = self._story_entry_links("docs/structure-library/story/README.md")
        self.assertGreaterEqual(len(links), 1)

        for link in links:
            with self.subTest(link=link):
                self.assertTrue(
                    (REPO_ROOT / "docs/structure-library/story" / link).is_file()
                )

    def test_story_structure_indexes_stay_aligned(self) -> None:
        story_readme_links = self._story_entry_links(
            "docs/structure-library/story/README.md"
        )
        top_level_links = self._story_entry_links("docs/structure-library/README.md")
        compatibility_links = self._story_entry_links(
            "docs/structure-library/story-structures.md"
        )

        self.assertSetEqual(story_readme_links, top_level_links)
        self.assertSetEqual(story_readme_links, compatibility_links)

    def test_conductor_routes_story_structure_into_beat_plan(self) -> None:
        text = self._read("skills/artist-os/SKILL.md")

        for required in (
            "docs/structure-library/story/README.md",
            "story_structure",
            "rather than applying it unchanged",
            "schemas/beat-plan.schema.json",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_story_architecture_keeps_story_structure_boundary(self) -> None:
        text = self._read("docs/story/ARCHITECTURE.md")

        for required in (
            "store the project-specific adaptation in `story_structure`",
            "does not choose medium, output shape, asset count, or publication format",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_promoted_story_structure_fixtures_cover_role_adaptation(self) -> None:
        fixture_expectations = {
            "tests/fixtures/story/three-act-rehearsal/beat-plan.json": {
                "entry_id": "three_act_structure",
                "roles": {"invitation", "threshold", "reversal", "closure"},
            },
            "tests/fixtures/story/hero-journey-rehearsal/beat-plan.json": {
                "entry_id": "hero_journey",
                "roles": {"grounding", "threshold", "rupture", "transformation", "return"},
            },
            "tests/fixtures/story/kishotenketsu-rehearsal/beat-plan.json": {
                "entry_id": "kishotenketsu",
                "roles": {"grounding", "build", "reveal", "closure"},
            },
            "tests/fixtures/story/freytag-rehearsal/beat-plan.json": {
                "entry_id": "freytag_dramatic_arc",
                "roles": {"grounding", "build", "reversal", "consequence", "residue"},
            },
        }

        for fixture_path, expectation in fixture_expectations.items():
            with self.subTest(fixture=fixture_path):
                data = json.loads((REPO_ROOT / fixture_path).read_text(encoding="utf-8"))
                self.assertEqual(
                    expectation["entry_id"],
                    data["story_structure"]["library_entry_id"],
                )
                self.assertTrue(
                    expectation["roles"].issubset(
                        {beat["beat_role"] for beat in data["beats"]}
                    )
                )


if __name__ == "__main__":
    unittest.main()
