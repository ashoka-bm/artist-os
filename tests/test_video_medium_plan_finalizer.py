from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from artist_os_schema_validator import validate_file


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKET = REPO_ROOT / "tests/fixtures/video-journey/laundromat-compact-video-authoring-packet.json"
SCHEMA = REPO_ROOT / "schemas/video-medium-plan.schema.json"
COMMAND = REPO_ROOT / "bin/artist-os-video-finalize"


class VideoMediumPlanFinalizerTests(unittest.TestCase):
    def test_finalizer_builds_valid_video_medium_plan_from_compact_packet(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "video-medium-plan.json"
            result = subprocess.run(
                [sys.executable, str(COMMAND), str(PACKET), "--output", str(output)],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("validated", result.stdout)
            validate_file(SCHEMA, output)

            record = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(record["narrative_depth"], "micro_journey")
            self.assertEqual(record["micro_journey_template_ref"], "problem_solution_demo")
            self.assertEqual(len(record["storyboard_shots"]), 2)

            first_shot = record["storyboard_shots"][0]
            self.assertEqual(first_shot["scene_id"], "vscene_laundromat_after_hours")
            self.assertEqual(first_shot["time_range"]["start_seconds"], 0)
            self.assertEqual(first_shot["visual_unit"]["intended_feeling"], "wrongness")
            self.assertEqual(first_shot["visual_unit"]["shot_design"]["shot_scale"], "wide")
            self.assertEqual(first_shot["reference_refs_used"], [])

    def test_finalizer_reports_schema_errors(self) -> None:
        packet = json.loads(PACKET.read_text(encoding="utf-8"))
        packet["shots"][0]["scale"] = "macro"

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            packet_path = tmp_path / "packet.json"
            output = tmp_path / "video-medium-plan.json"
            packet_path.write_text(json.dumps(packet), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(COMMAND), str(packet_path), "--output", str(output)],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("FAIL:", result.stderr)
            self.assertIn("macro", result.stderr)

    def test_print_template_emits_packet_that_finalizes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            packet_path = tmp_path / "template-packet.json"
            output = tmp_path / "video-medium-plan.json"

            template_result = subprocess.run(
                [sys.executable, str(COMMAND), "--print-template"],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(template_result.returncode, 0, template_result.stderr)
            packet = json.loads(template_result.stdout)
            self.assertIn("format", packet)
            self.assertIn("symbology", packet)
            self.assertIn("shots", packet)
            packet_path.write_text(json.dumps(packet), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(COMMAND), str(packet_path), "--output", str(output)],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            validate_file(SCHEMA, output)

    def test_finalizer_accepts_lean_alias_packet_without_fixture_shape(self) -> None:
        packet = {
            "video_medium_plan_id": "vmp_alias_packet",
            "source_id": "src_alias",
            "artist_meaning_id": "meaning_alias",
            "transformation_brief_id": "tb_alias",
            "beat_plan_id": "bp_alias",
            "format": {
                "video_format": "short_social_video",
                "modifier": "micro_trailer",
                "duration_seconds": 12,
                "aspect_ratio": "9:16",
                "publication_use": "social_post",
            },
            "symbology": {
                "core_image": "a warning object in an ordinary room",
                "active_absence": True,
            },
            "style_direction": {
                "rendering_style": "grounded cinematic horror",
                "camera_style": "practical light",
                "visual_texture": "wet reflections",
                "edit_style": "sharp cuts",
            },
            "visual_dynamics": [
                {"tension": "ordinary/haunted", "intensity": "high"},
            ],
            "video_scenes": [
                {
                    "scene_id": "vscene_alias",
                    "setting": "ordinary room",
                    "duration_target_seconds": 12,
                }
            ],
            "audio_plan": {"audio_mode": "sound_design"},
            "shots": [
                {
                    "shot_id": "vshot_alias_001",
                    "beat_id": "beat_alias",
                    "kem_id": "kem_alias",
                    "start": 0,
                    "duration": 3,
                    "scale": "wide",
                    "angle": "eye_level",
                    "emphasis": "environment",
                    "camera_movement": "static",
                    "subject_movement": "one object moves",
                    "transition_in": "fade_from_black",
                    "transition_out": "hard_cut",
                    "feeling": "unease",
                    "prompt": "Ordinary room with one impossible moving object.",
                }
            ],
        }

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            packet_path = tmp_path / "lean-packet.json"
            output = tmp_path / "video-medium-plan.json"
            packet_path.write_text(json.dumps(packet), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(COMMAND), str(packet_path), "--output", str(output)],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            validate_file(SCHEMA, output)
            record = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(record["video_format"]["duration_target_seconds"], 12)
            self.assertEqual(record["symbology_direction"]["confirmation_status"], "unconfirmed")
            self.assertEqual(record["storyboard_shots"][0]["scene_id"], "vscene_alias")

    def test_finalizer_accepts_compact_audio_cue_aliases(self) -> None:
        packet = {
            "video_medium_plan_id": "vmp_audio_alias_packet",
            "source_id": "src_audio_alias",
            "artist_meaning_id": "meaning_audio_alias",
            "transformation_brief_id": "tb_audio_alias",
            "beat_plan_id": "bp_audio_alias",
            "audio_plan": {
                "audio_mode": "sound_design",
                "audio_cues": [
                    {
                        "ref": "washer spin",
                        "role": "machine rhythm",
                        "description": "Washer rotation and low circular hum.",
                        "shot_ids": ["vshot_audio_alias_001"],
                    }
                ],
            },
            "shots": [
                {
                    "shot_id": "vshot_audio_alias_001",
                    "beat_id": "beat_audio_alias",
                    "kem_id": "kem_audio_alias",
                    "start": 0,
                    "duration": 3,
                    "scale": "wide",
                    "angle": "eye_level",
                    "emphasis": "environment",
                    "camera_movement": "static",
                    "subject_movement": "one object moves",
                    "feeling": "unease",
                    "prompt": "Ordinary room with one impossible moving object.",
                }
            ],
        }

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            packet_path = tmp_path / "audio-alias-packet.json"
            output = tmp_path / "video-medium-plan.json"
            packet_path.write_text(json.dumps(packet), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(COMMAND), str(packet_path), "--output", str(output)],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            validate_file(SCHEMA, output)
            record = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(record["audio_plan"]["audio_cues"][0]["audio_ref"], "audio_washer_spin")
            self.assertEqual(record["audio_plan"]["audio_cues"][0]["used_by_shot_ids"], ["vshot_audio_alias_001"])

    def test_finalizer_reports_missing_compact_fields_together(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            packet_path = tmp_path / "bad-packet.json"
            output = tmp_path / "video-medium-plan.json"
            packet_path.write_text(json.dumps({"source_id": "src_only"}), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(COMMAND), str(packet_path), "--output", str(output)],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("video_medium_plan_id", result.stderr)
            self.assertIn("artist_meaning_id", result.stderr)
            self.assertIn("'shots' or 'storyboard_shots'", result.stderr)


if __name__ == "__main__":
    unittest.main()
