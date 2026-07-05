from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from artist_os_adapter_guards import assert_import_output_record
from artist_os_schema_validator import REPO_ROOT, load_json, validate


IMPORT_OUTPUT = REPO_ROOT / "bin" / "artist-os-import-output"
OUTPUT_SCHEMA = load_json(REPO_ROOT / "schemas" / "output-record.schema.json")


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
    output_records_dir: str = "projects/proj_door_left_lit/outputs",
    events: str = "projects/proj_door_left_lit/events.jsonl",
) -> Path:
    project_dir = library_root / "projects" / "proj_door_left_lit"
    project_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "project_id": "proj_door_left_lit",
        "title": "Door Left Lit",
        "status": "active",
        "current_stage": "output_record",
        "created_at": "2026-07-05T00:00:00Z",
        "updated_at": "2026-07-05T00:00:00Z",
        "summary": "Import adapter test project.",
        "paths": {
            "events": events,
            "source_record": "projects/proj_door_left_lit/source/source-record.json",
            "meaning_interview": "projects/proj_door_left_lit/meaning/artist-meaning.json",
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

    def test_human_edited_import_requires_previous_output_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            library_root = root / "library"
            write_manifest(library_root)
            artifact_path = root / "edited.md"
            artifact_path.write_text("Edited draft\n", encoding="utf-8")
            args = base_args(library_root, artifact_path)
            args[args.index("--origin") + 1] = "human_edited"
            args[args.index("--target-media-type") + 1] = "text"
            args[args.index("--artifact-kind") + 1] = "text"
            args[args.index("--medium-plan-id") + 1] = "tmp_door_left_lit"

            proc = subprocess.run(args, capture_output=True, text=True)

            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("previous Output Record", proc.stderr)
            output_dir = library_root / "projects" / "proj_door_left_lit" / "outputs"
            self.assertFalse(output_dir.exists())

    def test_human_edited_import_records_previous_output_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            library_root = root / "library"
            project_dir = write_manifest(library_root)
            artifact_path = root / "edited.md"
            artifact_path.write_text("Edited draft\n", encoding="utf-8")
            args = base_args(library_root, artifact_path)
            args[args.index("--origin") + 1] = "human_edited"
            args[args.index("--output-record-id") + 1] = "out_door_left_lit_human_edit_001"
            args[args.index("--artifact-id") + 1] = "artifact_door_left_lit_human_edit_001"
            args[args.index("--target-media-type") + 1] = "text"
            args[args.index("--artifact-kind") + 1] = "text"
            args[args.index("--medium-plan-id") + 1] = "tmp_door_left_lit"
            args.extend(["--previous-output-record-id", "out_door_left_lit_draft_001"])

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
            self.assertEqual(record["previous_output_record_id"], "out_door_left_lit_draft_001")
            self.assertEqual(record["origin"]["origin_type"], "human_edited")

    def test_audio_import_fallback_path_uses_artifact_kind_dimension(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            library_root = root / "library"
            project_dir = write_manifest(library_root)
            artifact_path = root / "song.mp3"
            artifact_path.write_bytes(b"audio")
            args = base_args(library_root, artifact_path)
            args[args.index("--output-record-id") + 1] = "out_door_left_lit_audio_import_001"
            args[args.index("--artifact-id") + 1] = "artifact_door_left_lit_audio_import_001"
            args[args.index("--target-media-type") + 1] = "sound"
            args[args.index("--artifact-kind") + 1] = "audio"
            args[args.index("--medium-plan-id") + 1] = "smp_door_left_lit"

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


if __name__ == "__main__":
    unittest.main()
