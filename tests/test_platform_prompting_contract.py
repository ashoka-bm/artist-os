from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PLATFORMS = REPO_ROOT / "skills" / "artist-os" / "references" / "platforms"


class PlatformPromptingContractTests(unittest.TestCase):
    def _read(self, filename: str) -> str:
        return (PLATFORMS / filename).read_text(encoding="utf-8")

    def test_seedance_platform_docs_pin_codex_output_and_english_boundary(self) -> None:
        for filename in (
            "seedance-cinematic-animation-prompting.md",
            "seedance-instagram-prompting.md",
        ):
            text = self._read(filename)
            with self.subTest(filename=filename):
                self.assertIn("## Codex Output Format", text)
                self.assertIn("Seedance prompt:", text)
                self.assertIn("Reference bindings:", text)
                self.assertIn("Generation boundary:", text)
                self.assertIn("explicit artist approval", text)
                self.assertIn("Do not include a Chinese version", text)

    def test_seedance_platform_docs_do_not_include_chinese_prompt_text(self) -> None:
        for filename in (
            "seedance-cinematic-animation-prompting.md",
            "seedance-instagram-prompting.md",
        ):
            text = self._read(filename)
            with self.subTest(filename=filename):
                self.assertNotRegex(text, r"[\u4E00-\u9FFF]")

    def test_elevenlabs_v3_doc_pins_codex_and_provider_output_shapes(self) -> None:
        text = self._read("elevenlabs-v3-voiceover.md")
        for required in (
            "## Codex Output Format",
            "return only the enhanced spoken text by default",
            "Do not add a heading, explanation, bullet list, rationale, markdown fence, or tag audit",
            "## ElevenLabs Prompt Output",
            "preserve every original spoken word in order",
            "add only square-bracket voice, breath, pause, or delivery tags",
            "avoid markdown, commentary, field labels, JSON, XML, SSML",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_elevenlabs_v3_doc_rejects_non_voice_tags_and_generation_permission(self) -> None:
        text = self._read("elevenlabs-v3-voiceover.md")
        for required in (
            "Calling ElevenLabs, rendering TTS, uploading audio, or making any provider-backed generation call still requires explicit per-call artist approval",
            "Do not use tags such as `[standing]`, `[grinning]`, `[pacing]`, or `[music]`",
            "Do not invent new dialogue lines",
            "Do not remove, rewrite, reorder, or replace original words",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
