from __future__ import annotations

import json
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from artist_os_adapter_guards import assert_import_output_record
from artist_os_schema_validator import REPO_ROOT, load_json, validate


IMPORT_OUTPUT = REPO_ROOT / "bin" / "artist-os-import-output"
OUTPUT_SCHEMA = load_json(REPO_ROOT / "schemas" / "output-record.schema.json")
LINEAGE_FIXTURES = {
    "source/source-record.json": "tests/fixtures/story/source-record.json",
    "meaning/artist-meaning.json": "tests/fixtures/story/artist-meaning.json",
    "story/transformation-brief.json": "tests/fixtures/story/transformation-brief.json",
    "story/beat-plan.json": "tests/fixtures/story/beat-plan.json",
}
MEDIUM_LINEAGE_FIXTURES = {
    "image": {
        "medium-plans/image-medium-plan.json": "tests/fixtures/text-to-image/image-medium-plan.json",
        "briefs/creative-brief.record.json": "tests/fixtures/text-to-image/creative-brief.json",
        "prompt-plans/prompt-plan.json": "tests/fixtures/text-to-image/prompt-plan.json",
    },
    "sound": {
        "medium-plans/sound-medium-plan.json": "tests/fixtures/text-to-suno/sound-medium-plan.json",
        "briefs/sound-creative-brief.record.json": "tests/fixtures/text-to-suno/sound-creative-brief.json",
        "prompt-plans/sound-prompt-plan.json": "tests/fixtures/text-to-suno/sound-prompt-plan.json",
    },
    "text": {
        "medium-plans/text-medium-plan.json": "tests/fixtures/text-journey/text-medium-plan.json",
        "briefs/text-creative-brief.record.json": "tests/fixtures/text-journey/text-creative-brief.json",
        "prompt-plans/text-generation-plan.json": "tests/fixtures/text-journey/text-generation-plan.json",
        "outputs/text/output-records/out_text_door_left_lit_draft_001.json": (
            "tests/fixtures/text-journey/output-record-draft.json"
        ),
    },
}


def base_args(library_root: Path, artifact_path: Path) -> list[str]:
    return [
        sys.executable,
        str(IMPORT_OUTPUT),
        "--library-root",
        str(library_root),
        "--project-id",
        "proj_door_left_lit",
        "--file",
        str(artifact_path),
        "--origin",
        "artist_imported",
        "--output-record-id",
        "out_door_left_lit_imported_image_001",
        "--artifact-id",
        "artifact_door_left_lit_imported_image_001",
        "--source-id",
        "src_door_left_lit",
        "--artist-meaning-id",
        "meaning_door_left_lit",
        "--transformation-brief-id",
        "tb_door_left_lit",
        "--beat-plan-id",
        "bp_door_left_lit",
        "--medium-plan-id",
        "imp_door_left_lit",
        "--brief-id",
        "brief_door_left_lit",
        "--prompt-plan-id",
        "plan_door_left_lit",
        "--target-media-type",
        "image",
        "--artifact-kind",
        "image",
        "--description",
        "Artist-provided threshold image.",
        "--rights-notes",
        "Artist owns this imported review artifact.",
    ]


def write_manifest(
    library_root: Path,
    *,
    medium: str = "image",
    output_records_dir: str = "projects/proj_door_left_lit/outputs",
    events: str = "projects/proj_door_left_lit/events.jsonl",
) -> Path:
    project_dir = library_root / "projects" / "proj_door_left_lit"
    project_dir.mkdir(parents=True, exist_ok=True)
    for destination, source in {**LINEAGE_FIXTURES, **MEDIUM_LINEAGE_FIXTURES[medium]}.items():
        destination_path = project_dir / destination
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPO_ROOT / source, destination_path)

    medium_path_key = f"{medium}_medium_plan"
    medium_path = f"projects/proj_door_left_lit/medium-plans/{medium}-medium-plan.json"
    if medium == "image":
        brief_path = "projects/proj_door_left_lit/briefs/creative-brief.record.json"
        prompt_path = "projects/proj_door_left_lit/prompt-plans/prompt-plan.json"
    elif medium == "sound":
        brief_path = "projects/proj_door_left_lit/briefs/sound-creative-brief.record.json"
        prompt_path = "projects/proj_door_left_lit/prompt-plans/sound-prompt-plan.json"
    else:
        brief_path = "projects/proj_door_left_lit/briefs/text-creative-brief.record.json"
        prompt_path = "projects/proj_door_left_lit/prompt-plans/text-generation-plan.json"

    manifest = {
        "project_id": "proj_door_left_lit",
        "title": "Door Left Lit",
        "status": "active",
        "current_stage": "critique",
        "created_at": "2026-07-05T00:00:00Z",
        "updated_at": "2026-07-05T00:00:00Z",
        "summary": "Import adapter test project.",
        "resume_state": {
            "current_checkpoint": "prompt_plan",
            "next_phase": "Generation Approval",
            "media_index": [
                {
                    "medium": "audio" if medium == "sound" else medium,
                    "medium_role": "primary",
                    "medium_plan_ref": {
                        "image": "imp_door_left_lit",
                        "sound": "smp_door_left_lit",
                        "text": "tmp_door_left_lit",
                    }[medium],
                    "status": "active",
                    "artist_meaning_id": "meaning_door_left_lit",
                    "transformation_brief_id": "tb_door_left_lit",
                    "beat_plan_id": "bp_door_left_lit",
                }
            ],
        },
        "paths": {
            "project_dir": "projects/proj_door_left_lit",
            "events": events,
            "source_record": "projects/proj_door_left_lit/source/source-record.json",
            "artist_meaning": "projects/proj_door_left_lit/meaning/artist-meaning.json",
            "meaning_interview": "projects/proj_door_left_lit/meaning/artist-meaning.json",
            "transformation_brief": "projects/proj_door_left_lit/story/transformation-brief.json",
            "beat_plan": "projects/proj_door_left_lit/story/beat-plan.json",
            medium_path_key: medium_path,
            "creative_brief_record": brief_path,
            "prompt_plan": prompt_path,
            "output_records_dir": output_records_dir,
        },
        "decisions": {
            "interpretation_status": "complete",
            "symbology_status": "complete",
            "style_status": "complete",
            "detail_status": "complete",
        },
        "assets": [],
    }
    (project_dir / "project.json").write_text(json.dumps(manifest), encoding="utf-8")
    return project_dir


def configure_args_for_medium(args: list[str], medium: str) -> None:
    if medium == "sound":
        args[args.index("--brief-id") + 1] = "brief_door_left_lit_sound"
        args[args.index("--prompt-plan-id") + 1] = "plan_door_left_lit_sound"
        args[args.index("--medium-plan-id") + 1] = "smp_door_left_lit"
    elif medium == "text":
        args[args.index("--brief-id") + 1] = "brief_text_door_left_lit"
        args[args.index("--prompt-plan-id") + 1] = "plan_text_door_left_lit"
        args[args.index("--medium-plan-id") + 1] = "tmp_door_left_lit"
        args.extend(["--text-generation-plan-id", "plan_text_door_left_lit"])


class ImportOutputAdapterCliTests(unittest.TestCase):
    def test_imported_artifact_writes_schema_valid_output_record_and_event(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            library_root = root / "library"
            project_dir = write_manifest(
                library_root,
                output_records_dir="projects/proj_door_left_lit/relocated-output-records",
                events="projects/proj_door_left_lit/audit/import-events.jsonl",
            )
            artifact_path = root / "threshold.png"
            artifact_path.write_bytes(b"not a real png but enough for import provenance")

            proc = subprocess.run(
                base_args(library_root, artifact_path),
                capture_output=True,
                text=True,
            )

            self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
            output_path = (
                project_dir
                / "relocated-output-records"
                / "image"
                / "output-records"
                / "out_door_left_lit_imported_image_001.json"
            )
            self.assertTrue(output_path.is_file())

            record = json.loads(output_path.read_text(encoding="utf-8"))
            validate(record, OUTPUT_SCHEMA, OUTPUT_SCHEMA)
            assert_import_output_record(record)
            self.assertEqual(record["output_artifact"]["uri_or_path"], str(artifact_path.resolve()))
            self.assertEqual(record["origin"]["origin_type"], "artist_imported")
            self.assertIsNone(record["origin"]["generation_approval_ref"])
            self.assertEqual(record["generation"]["settings"], {})

            events = (project_dir / "audit" / "import-events.jsonl").read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(events), 1)
            event = json.loads(events[0])
            self.assertRegex(event["event_id"], r"^evt_door_left_lit_imported_image_001_")
            self.assertEqual(event["event_type"], "output_imported")
            self.assertEqual(event["stage"], "output_record")
            self.assertEqual(event["output_record_id"], "out_door_left_lit_imported_image_001")
            self.assertEqual(event["origin_type"], "artist_imported")

            manifest = json.loads((project_dir / "project.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["current_stage"], "critique")
            self.assertEqual(manifest["resume_state"]["current_checkpoint"], "output_record")
            self.assertEqual(manifest["resume_state"]["next_phase"], "Output Critic Review")
            self.assertEqual(manifest["assets"][-1]["asset_id"], "artifact_door_left_lit_imported_image_001")

            with closing(sqlite3.connect(library_root / "artist-os.sqlite")) as conn:
                indexed = conn.execute(
                    "SELECT output_record_id FROM output_artifacts WHERE output_record_id = ?",
                    ("out_door_left_lit_imported_image_001",),
                ).fetchone()
            self.assertEqual(indexed, ("out_door_left_lit_imported_image_001",))

    def test_human_edited_import_requires_previous_output_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            library_root = root / "library"
            write_manifest(library_root, medium="text")
            artifact_path = root / "edited.md"
            artifact_path.write_text("Edited draft\n", encoding="utf-8")
            args = base_args(library_root, artifact_path)
            args[args.index("--origin") + 1] = "human_edited"
            args[args.index("--target-media-type") + 1] = "text"
            args[args.index("--artifact-kind") + 1] = "text"
            configure_args_for_medium(args, "text")

            proc = subprocess.run(args, capture_output=True, text=True)

            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("previous Output Record", proc.stderr)
            output_path = (
                library_root
                / "projects"
                / "proj_door_left_lit"
                / "outputs"
                / "text"
                / "output-records"
                / "out_door_left_lit_imported_image_001.json"
            )
            self.assertFalse(output_path.exists())

    def test_human_edited_import_records_previous_output_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            library_root = root / "library"
            project_dir = write_manifest(library_root, medium="text")
            artifact_path = root / "edited.md"
            artifact_path.write_text("Edited draft\n", encoding="utf-8")
            args = base_args(library_root, artifact_path)
            args[args.index("--origin") + 1] = "human_edited"
            args[args.index("--output-record-id") + 1] = "out_door_left_lit_human_edit_001"
            args[args.index("--artifact-id") + 1] = "artifact_door_left_lit_human_edit_001"
            args[args.index("--target-media-type") + 1] = "text"
            args[args.index("--artifact-kind") + 1] = "text"
            configure_args_for_medium(args, "text")
            args.extend(["--previous-output-record-id", "out_text_door_left_lit_draft_001"])

            proc = subprocess.run(args, capture_output=True, text=True)

            self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
            output_path = (
                project_dir
                / "outputs"
                / "text"
                / "output-records"
                / "out_door_left_lit_human_edit_001.json"
            )
            record = json.loads(output_path.read_text(encoding="utf-8"))
            validate(record, OUTPUT_SCHEMA, OUTPUT_SCHEMA)
            assert_import_output_record(record)
            self.assertEqual(record["previous_output_record_id"], "out_text_door_left_lit_draft_001")
            self.assertEqual(record["origin"]["origin_type"], "human_edited")

    def test_audio_import_fallback_path_uses_artifact_kind_dimension(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            library_root = root / "library"
            project_dir = write_manifest(library_root, medium="sound")
            artifact_path = root / "song.mp3"
            artifact_path.write_bytes(b"audio")
            args = base_args(library_root, artifact_path)
            args[args.index("--output-record-id") + 1] = "out_door_left_lit_audio_import_001"
            args[args.index("--artifact-id") + 1] = "artifact_door_left_lit_audio_import_001"
            args[args.index("--target-media-type") + 1] = "sound"
            args[args.index("--artifact-kind") + 1] = "audio"
            configure_args_for_medium(args, "sound")

            proc = subprocess.run(args, capture_output=True, text=True)

            self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
            self.assertTrue(
                (
                    project_dir
                    / "outputs"
                    / "audio"
                    / "output-records"
                    / "out_door_left_lit_audio_import_001.json"
                ).is_file()
            )

    def test_rejects_project_without_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            library_root = root / "library"
            (library_root / "projects" / "proj_door_left_lit").mkdir(parents=True)
            artifact_path = root / "threshold.png"
            artifact_path.write_bytes(b"image")

            proc = subprocess.run(
                base_args(library_root, artifact_path),
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("project.json", proc.stderr)

    def test_rejects_malformed_created_at(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            library_root = root / "library"
            write_manifest(library_root)
            artifact_path = root / "threshold.png"
            artifact_path.write_bytes(b"image")
            args = base_args(library_root, artifact_path)
            args.extend(["--created-at", "not-a-date"])

            proc = subprocess.run(args, capture_output=True, text=True)

            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("created-at", proc.stderr)
            self.assertFalse((library_root / "projects" / "proj_door_left_lit" / "outputs").exists())

    def test_rejects_incomplete_project_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            library_root = root / "library"
            project_dir = write_manifest(library_root)
            manifest_path = project_dir / "project.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            del manifest["paths"]["creative_brief_record"]
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            artifact_path = root / "threshold.png"
            artifact_path.write_bytes(b"image")

            proc = subprocess.run(base_args(library_root, artifact_path), capture_output=True, text=True)

            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("project.json does not validate", proc.stderr)
            self.assertFalse((project_dir / "outputs").exists())

    def test_rejects_manifest_write_path_outside_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            library_root = root / "library"
            write_manifest(library_root, output_records_dir=str(root / "escaped"))
            artifact_path = root / "threshold.png"
            artifact_path.write_bytes(b"image")

            proc = subprocess.run(base_args(library_root, artifact_path), capture_output=True, text=True)

            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("outside project directory", proc.stderr)
            self.assertFalse((root / "escaped").exists())

    def test_rejects_missing_upstream_lineage(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            library_root = root / "library"
            write_manifest(library_root)
            artifact_path = root / "threshold.png"
            artifact_path.write_bytes(b"image")
            args = base_args(library_root, artifact_path)
            args[args.index("--prompt-plan-id") + 1] = "plan_missing"

            proc = subprocess.run(args, capture_output=True, text=True)

            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("upstream prompt plan", proc.stderr)
            self.assertFalse((library_root / "projects" / "proj_door_left_lit" / "outputs").exists())

    def test_event_write_failure_leaves_no_partial_record_or_manifest_update(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            library_root = root / "library"
            project_dir = write_manifest(
                library_root,
                events="projects/proj_door_left_lit/audit",
            )
            (project_dir / "audit").mkdir()
            manifest_before = (project_dir / "project.json").read_bytes()
            artifact_path = root / "threshold.png"
            artifact_path.write_bytes(b"image")

            proc = subprocess.run(base_args(library_root, artifact_path), capture_output=True, text=True)

            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("events path is not a file", proc.stderr)
            self.assertEqual((project_dir / "project.json").read_bytes(), manifest_before)
            self.assertFalse((project_dir / "outputs").exists())


if __name__ == "__main__":
    unittest.main()
