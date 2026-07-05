from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
COMPARE_RUN = REPO_ROOT / "docs/drafts/cost-tiering/measurements/compare-run.py"


def load_compare_run():
    spec = importlib.util.spec_from_file_location("compare_run", COMPARE_RUN)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class CostTieringMeasurementTests(unittest.TestCase):
    def test_signals_count_actual_file_reads_not_route_mentions(self) -> None:
        compare_run = load_compare_run()
        lines = [
            {
                "type": "session_meta",
                "payload": {
                    "base_instructions": {
                        "text": (
                            "Route short clips to video-micro-journey-recipe.md; "
                            "do not load video-journey.md or storyboard-prompt-builder.md."
                        )
                    }
                },
            },
            {
                "type": "response_item",
                "payload": {
                    "type": "function_call",
                    "arguments": json.dumps(
                        {
                            "cmd": (
                                "sed -n '1,220p' "
                                "skills/artist-os/references/video-micro-journey-recipe.md"
                            )
                        }
                    ),
                },
            },
            {
                "type": "response_item",
                "payload": {
                    "type": "function_call",
                    "arguments": json.dumps(
                        {
                            "cmd": (
                                "printf '%s\\n' 'video-journey.md "
                                "storyboard-prompt-builder.md mentioned only'"
                            )
                        }
                    ),
                },
            },
            {
                "type": "response_item",
                "payload": {
                    "type": "message",
                    "content": [{"type": "output_text", "text": "narrative_depth = micro_journey"}],
                },
            },
        ]

        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as tmp:
            for line in lines:
                tmp.write(json.dumps(line) + "\n")
            path = tmp.name

        signals = compare_run.signals(path)

        self.assertEqual(signals["recipe"], 1)
        self.assertEqual(signals["video_journey"], 0)
        self.assertEqual(signals["storyboard_builder"], 0)
        self.assertGreater(signals["micro_journey"], 0)

    def test_signals_count_schema_file_reads(self) -> None:
        compare_run = load_compare_run()
        line = {
            "type": "response_item",
            "payload": {
                "type": "function_call",
                "arguments": json.dumps(
                    {"cmd": "sed -n '1,220p' schemas/video-medium-plan.schema.json"}
                ),
            },
        }
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as tmp:
            tmp.write(json.dumps(line) + "\n")
            path = tmp.name

        self.assertEqual(compare_run.signals(path)["schema_reads"], 1)


if __name__ == "__main__":
    unittest.main()
