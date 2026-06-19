from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class StoryStructureContractTests(unittest.TestCase):
    def _read(self, relative_path: str) -> str:
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")

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


if __name__ == "__main__":
    unittest.main()
