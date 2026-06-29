from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sqlite3
import tempfile
import unittest
from contextlib import closing
from contextlib import redirect_stdout
from importlib.machinery import SourceFileLoader
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from artist_os_schema_validator import ValidationError
from artist_os_schema_validator import validate


REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIST_OS_DB_PATH = REPO_ROOT / "bin" / "artist-os-db"


def load_artist_os_db():
    loader = SourceFileLoader("artist_os_db", str(ARTIST_OS_DB_PATH))
    spec = importlib.util.spec_from_loader("artist_os_db", loader)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


artist_os_db = load_artist_os_db()


def minimal_manifest(project_id: str = "proj_door_left_lit") -> dict:
    return {
        "project_id": project_id,
        "title": "Door Left Lit",
        "status": "active",
        "current_stage": "prompt_plan",
        "created_at": "2026-05-31T00:00:00Z",
        "updated_at": "2026-05-31T00:00:00Z",
        "summary": "A threshold image project.",
        "paths": {
            "project_dir": f"projects/{project_id}",
            "events": f"projects/{project_id}/events.jsonl",
            "source_record": f"projects/{project_id}/source/source-record.json",
            "meaning_interview": f"projects/{project_id}/meaning/meaning-interview.json",
            "creative_brief_record": f"projects/{project_id}/briefs/creative-brief.record.json",
            "prompt_plan": f"projects/{project_id}/prompt-plans/prompt-plan.json",
        },
        "decisions": {
            "interpretation_status": "complete",
            "symbology_status": "complete",
            "style_status": "complete",
            "detail_status": "complete",
        },
        "assets": [],
    }


def minimal_output_record(project_id: str = "proj_door_left_lit") -> dict:
    return {
        "output_record_id": "out_door_left_lit_audio_001",
        "previous_output_record_id": None,
        "project_id": project_id,
        "source_id": "src_door_left_lit",
        "artist_meaning_id": "meaning_door_left_lit",
        "transformation_brief_id": "tb_door_left_lit",
        "beat_plan_id": "bp_door_left_lit",
        "medium_plan_id": "smp_door_left_lit",
        "brief_id": "brief_door_left_lit",
        "prompt_plan_id": "plan_door_left_lit",
        "target_media_type": "sound",
        "output_artifact": {
            "artifact_id": "artifact_door_left_lit_audio_001",
            "artifact_kind": "audio",
            "uri_or_path": "projects/proj_door_left_lit/outputs/audio/generated/door-left-lit.mp3",
            "mime_type": "audio/mpeg",
            "description": "Generated audio artifact.",
            "rights_notes": "Private review artifact.",
        },
        "origin": {
            "origin_type": "artist_imported",
            "created_by": "artist",
            "generation_approval_ref": None,
        },
        "generation": {
            "provider": "suno",
            "model": None,
            "settings": {},
            "seed": None,
            "estimated_cost": None,
            "actual_cost": None,
        },
        "review_state": {
            "output_critic_review_required": True,
            "review_record_id": None,
            "review_status": "not_reviewed",
        },
        "acceptance_state": {
            "output_acceptance_status": "pending",
            "accepted_work": False,
            "artist_decision_ref": None,
            "waiver_reason": None,
        },
        "traceability_summary": [
            {
                "source_type": "prompt_plan",
                "source_ref": "plan_door_left_lit",
                "note": "Produced from the prompt plan.",
            }
        ],
        "created_at": "2026-05-31T00:00:00Z",
    }


def minimal_image_output_record(project_id: str = "proj_door_left_lit") -> dict:
    record = minimal_output_record(project_id)
    record["output_record_id"] = "out_door_left_lit_image_001"
    record["medium_plan_id"] = "imp_door_left_lit"
    record["target_media_type"] = "image"
    record["output_artifact"] = {
        "artifact_id": "artifact_door_left_lit_image_001",
        "artifact_kind": "image",
        "uri_or_path": "projects/proj_door_left_lit/assets/generated/door-left-lit.png",
        "mime_type": "image/png",
        "description": "Generated image artifact.",
        "rights_notes": "Private review artifact.",
    }
    record["generation"]["provider"] = "OpenAI image generation tool"
    record["generation"]["model"] = "image_gen"
    return record


class ArtistOSDbStorageTests(unittest.TestCase):
    def test_wondermint_root_derives_workspace_and_artist_library_roots(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            args = argparse.Namespace(
                library_root=None,
                wondermint_root=str(root),
                artist_library_root=None,
            )

            self.assertEqual(
                artist_os_db.library_root_for(args),
                root / ".wondermint" / "artist-os",
            )
            self.assertEqual(
                artist_os_db.artist_library_root_for(args),
                root / "Wondermint" / "Artist Library",
            )

    def test_artist_os_library_root_env_overrides_wondermint_root_env_for_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            workspace = root / "custom-workspace"
            env = {
                "ARTIST_OS_LIBRARY_ROOT": str(workspace),
                "WONDERMINT_ROOT": str(root / "wondermint-parent"),
            }
            args = argparse.Namespace(library_root=None, wondermint_root=None)

            with patch.dict(os.environ, env, clear=False):
                self.assertEqual(artist_os_db.library_root_for(args), workspace)

    def test_setup_with_wondermint_root_creates_sibling_visible_and_hidden_roots(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            args = argparse.Namespace(
                db=None,
                library_root=None,
                wondermint_root=str(root),
            )

            with redirect_stdout(StringIO()):
                artist_os_db.setup_db(args)

            self.assertTrue((root / ".wondermint" / "artist-os" / "projects").is_dir())
            self.assertTrue((root / ".wondermint" / "artist-os" / "artist-os.sqlite").is_file())
            self.assertTrue((root / "Wondermint" / "Artist Library" / "Projects").is_dir())
            self.assertTrue((root / "Wondermint" / "Artist Library" / "Personal Library").is_dir())

    def test_link_visible_project_creates_pointer_and_readme_without_medium_folders(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            args = argparse.Namespace(
                project_id="proj_door_left_lit",
                project_slug="door-left-lit",
                title="Door Left Lit",
                summary="A threshold image project.",
                status="active",
                workspace_root_hint="../../../.wondermint/artist-os",
                wondermint_root=str(root),
                artist_library_root=None,
                overwrite_pointer=False,
                overwrite_readme=False,
            )

            with redirect_stdout(StringIO()):
                artist_os_db.link_visible_project(args)

            project_dir = root / "Wondermint" / "Artist Library" / "Projects" / "door-left-lit"
            pointer_path = project_dir / ".artist-os-project.json"
            readme_path = project_dir / "README.md"

            self.assertTrue(pointer_path.is_file())
            self.assertTrue(readme_path.is_file())
            self.assertEqual(
                sorted(path.name for path in project_dir.iterdir()),
                [".artist-os-project.json", "README.md"],
            )

            pointer = json.loads(pointer_path.read_text(encoding="utf-8"))
            self.assertEqual(pointer["project_id"], "proj_door_left_lit")
            self.assertEqual(pointer["workspace_root_hint"], "../../../.wondermint/artist-os")

            readme = readme_path.read_text(encoding="utf-8")
            self.assertIn("# Door Left Lit", readme)
            self.assertIn("proj_door_left_lit", readme)
            self.assertIn("A threshold image project.", readme)

    def test_link_visible_project_updates_manifest_and_indexes_visible_state_when_manifest_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            library_root = root / ".wondermint" / "artist-os"
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            workspace_project_dir.mkdir(parents=True)
            (workspace_project_dir / "project.json").write_text(
                json.dumps(minimal_manifest()),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                project_id="proj_door_left_lit",
                project_slug="door-left-lit",
                title="Door Left Lit",
                summary="A threshold image project.",
                status="active",
                workspace_root_hint="../../../.wondermint/artist-os",
                wondermint_root=str(root),
                artist_library_root=None,
                overwrite_pointer=False,
                overwrite_readme=False,
            )

            with redirect_stdout(StringIO()):
                artist_os_db.link_visible_project(args)

            manifest = json.loads((workspace_project_dir / "project.json").read_text(encoding="utf-8"))
            readme_path = "Wondermint/Artist Library/Projects/door-left-lit/README.md"
            self.assertEqual(
                manifest["artist_library"]["project_dir"],
                "Wondermint/Artist Library/Projects/door-left-lit",
            )
            self.assertEqual(
                manifest["artist_library"]["project_pointer_path"],
                "Wondermint/Artist Library/Projects/door-left-lit/.artist-os-project.json",
            )
            self.assertEqual(manifest["artist_library"]["visible_state"], "present")
            self.assertEqual(manifest["artist_library"]["project_pointer_state"], "present")
            self.assertEqual(manifest["artist_library"]["user_facing_files"][0]["path"], readme_path)

            with closing(sqlite3.connect(library_root / "artist-os.sqlite")) as conn:
                visible_state = conn.execute(
                    """
                    SELECT visible_state, artist_library_project_dir,
                           project_pointer_state, project_pointer_project_id
                    FROM project_visible_state
                    """
                ).fetchone()
                file_ref = conn.execute(
                    "SELECT path, file_role, status FROM artist_library_files"
                ).fetchone()

            self.assertEqual(
                visible_state,
                (
                    "present",
                    "Wondermint/Artist Library/Projects/door-left-lit",
                    "present",
                    "proj_door_left_lit",
                ),
            )
            self.assertEqual(file_ref, (readme_path, "readable_summary", "current"))

    def test_link_visible_project_with_visible_root_only_does_not_update_default_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            default_workspace = root / "default-workspace"
            workspace_project_dir = default_workspace / "projects" / "proj_door_left_lit"
            artist_library_root = root / "custom-visible" / "Artist Library"
            workspace_project_dir.mkdir(parents=True)
            original_manifest = minimal_manifest()
            (workspace_project_dir / "project.json").write_text(
                json.dumps(original_manifest),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                project_id="proj_door_left_lit",
                project_slug="door-left-lit",
                title="Door Left Lit",
                summary="A threshold image project.",
                status="active",
                workspace_root_hint="../../../.wondermint/artist-os",
                wondermint_root=None,
                artist_library_root=str(artist_library_root),
                overwrite_pointer=False,
                overwrite_readme=False,
            )

            with patch.object(artist_os_db, "DEFAULT_LIBRARY_ROOT", default_workspace):
                with patch.dict(os.environ, {}, clear=True):
                    with redirect_stdout(StringIO()):
                        artist_os_db.link_visible_project(args)

            manifest = json.loads((workspace_project_dir / "project.json").read_text(encoding="utf-8"))
            self.assertNotIn("artist_library", manifest)
            self.assertFalse((default_workspace / "artist-os.sqlite").exists())
            self.assertTrue(
                (
                    artist_library_root
                    / "Projects"
                    / "door-left-lit"
                    / ".artist-os-project.json"
                ).is_file()
            )

    def test_link_visible_project_preserves_existing_same_project_pointer_without_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            project_dir = root / "Wondermint" / "Artist Library" / "Projects" / "door-left-lit"
            project_dir.mkdir(parents=True)
            pointer_path = project_dir / ".artist-os-project.json"
            pointer_path.write_text(
                json.dumps({
                    "schema_version": 1,
                    "project_id": "proj_door_left_lit",
                    "workspace_root_hint": "custom-hint",
                    "user_note": "preserve me",
                }, sort_keys=True),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                project_id="proj_door_left_lit",
                project_slug="door-left-lit",
                title=None,
                summary=None,
                status=None,
                workspace_root_hint="../../../.wondermint/artist-os",
                wondermint_root=str(root),
                artist_library_root=None,
                overwrite_pointer=False,
                overwrite_readme=False,
            )

            with redirect_stdout(StringIO()):
                artist_os_db.link_visible_project(args)

            pointer = json.loads(pointer_path.read_text(encoding="utf-8"))
            self.assertEqual(pointer["workspace_root_hint"], "custom-hint")
            self.assertEqual(pointer["user_note"], "preserve me")

    def test_link_visible_project_rejects_wrong_shape_existing_pointer_without_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            project_dir = root / "Wondermint" / "Artist Library" / "Projects" / "door-left-lit"
            project_dir.mkdir(parents=True)
            (project_dir / ".artist-os-project.json").write_text("[]", encoding="utf-8")
            args = argparse.Namespace(
                project_id="proj_door_left_lit",
                project_slug="door-left-lit",
                title=None,
                summary=None,
                status=None,
                workspace_root_hint="../../../.wondermint/artist-os",
                wondermint_root=str(root),
                artist_library_root=None,
                overwrite_pointer=False,
                overwrite_readme=False,
            )

            with self.assertRaisesRegex(SystemExit, "not a JSON object"):
                artist_os_db.link_visible_project(args)

    def test_link_visible_project_rejects_slug_that_escapes_projects_folder(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            args = argparse.Namespace(
                project_id="proj_door_left_lit",
                project_slug="../escape",
                title=None,
                summary=None,
                status=None,
                workspace_root_hint="../../../.wondermint/artist-os",
                wondermint_root=tmpdir,
                artist_library_root=None,
                overwrite_pointer=False,
                overwrite_readme=False,
            )

            with self.assertRaisesRegex(SystemExit, "project_slug must be one folder name"):
                artist_os_db.link_visible_project(args)

    def test_link_visible_project_rejects_invalid_project_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            args = argparse.Namespace(
                project_id="../proj_escape",
                project_slug="door-left-lit",
                title=None,
                summary=None,
                status=None,
                workspace_root_hint="../../../.wondermint/artist-os",
                wondermint_root=tmpdir,
                artist_library_root=None,
                overwrite_pointer=False,
                overwrite_readme=False,
            )

            with self.assertRaisesRegex(SystemExit, "project_id must match"):
                artist_os_db.link_visible_project(args)

    def test_link_visible_project_does_not_retarget_existing_pointer_without_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            args = argparse.Namespace(
                project_id="proj_door_left_lit",
                project_slug="door-left-lit",
                title=None,
                summary=None,
                status=None,
                workspace_root_hint="../../../.wondermint/artist-os",
                wondermint_root=str(root),
                artist_library_root=None,
                overwrite_pointer=False,
                overwrite_readme=False,
            )
            with redirect_stdout(StringIO()):
                artist_os_db.link_visible_project(args)

            args.project_id = "proj_other"
            with self.assertRaisesRegex(SystemExit, "already links to proj_door_left_lit"):
                artist_os_db.link_visible_project(args)

    def test_publish_visible_output_copies_image_artifact_and_indexes_visible_review_draft(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            library_root = root / "workspace-library" / "artist-os"
            artist_library_root = root / "Wondermint" / "Artist Library"
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            output_records_dir = workspace_project_dir / "outputs"
            generated_dir = workspace_project_dir / "assets" / "generated"
            visible_project_dir = artist_library_root / "Projects" / "door-left-lit"
            output_records_dir.mkdir(parents=True)
            generated_dir.mkdir(parents=True)
            visible_project_dir.mkdir(parents=True)
            (visible_project_dir / ".artist-os-project.json").write_text(
                json.dumps({"schema_version": 1, "project_id": "proj_door_left_lit"}),
                encoding="utf-8",
            )
            image_path = generated_dir / "door-left-lit.png"
            image_path.write_bytes(b"fake png")
            output_record = minimal_image_output_record()
            (output_records_dir / "output-record-image-001.json").write_text(
                json.dumps(output_record),
                encoding="utf-8",
            )
            manifest = minimal_manifest()
            manifest["paths"]["project_dir"] = "projects/proj_door_left_lit"
            manifest["paths"]["output_records_dir"] = "projects/proj_door_left_lit/outputs"
            manifest["artist_library"] = {
                "project_dir": "Projects/door-left-lit",
                "project_pointer_path": "Projects/door-left-lit/.artist-os-project.json",
                "project_pointer_state": "present",
                "project_pointer_project_id": "proj_door_left_lit",
                "visible_state": "present",
                "user_facing_files": [],
            }
            (workspace_project_dir / "project.json").write_text(json.dumps(manifest), encoding="utf-8")
            args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
                artist_library_root=str(artist_library_root),
                project_id="proj_door_left_lit",
                output_record_id="out_door_left_lit_image_001",
                state="draft",
                filename="door-left-lit.png",
                medium_folder=None,
                overwrite=False,
            )

            with redirect_stdout(StringIO()):
                artist_os_db.publish_visible_output(args)

            destination = visible_project_dir / "Images" / "Drafts" / "door-left-lit.png"
            self.assertEqual(destination.read_bytes(), b"fake png")
            manifest_after = json.loads((workspace_project_dir / "project.json").read_text(encoding="utf-8"))
            self.assertEqual(
                manifest_after["artist_library"]["user_facing_files"][0]["path"],
                "Wondermint/Artist Library/Projects/door-left-lit/Images/Drafts/door-left-lit.png",
            )
            self.assertEqual(
                manifest_after["artist_library"]["user_facing_files"][0]["output_record_id"],
                "out_door_left_lit_image_001",
            )
            with closing(sqlite3.connect(library_root / "artist-os.sqlite")) as conn:
                file_ref = conn.execute(
                    "SELECT path, file_role, status, output_record_id FROM artist_library_files"
                ).fetchone()
                output_artifact = conn.execute(
                    "SELECT output_record_id, artifact_kind FROM output_artifacts"
                ).fetchone()

            self.assertEqual(
                file_ref,
                (
                    "Wondermint/Artist Library/Projects/door-left-lit/Images/Drafts/door-left-lit.png",
                    "review_draft",
                    "current",
                    "out_door_left_lit_image_001",
                ),
            )
            self.assertEqual(output_artifact, ("out_door_left_lit_image_001", "image"))

    def test_publish_visible_reference_copies_artifact_updates_inventory_and_indexes_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            library_root = root / "workspace-library" / "artist-os"
            artist_library_root = root / "Wondermint" / "Artist Library"
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            output_records_dir = workspace_project_dir / "outputs"
            references_dir = workspace_project_dir / "references"
            generated_dir = workspace_project_dir / "assets" / "generated"
            visible_project_dir = artist_library_root / "Projects" / "door-left-lit"
            output_records_dir.mkdir(parents=True)
            references_dir.mkdir(parents=True)
            generated_dir.mkdir(parents=True)
            visible_project_dir.mkdir(parents=True)
            (visible_project_dir / ".artist-os-project.json").write_text(
                json.dumps({"schema_version": 1, "project_id": "proj_door_left_lit"}),
                encoding="utf-8",
            )
            image_path = generated_dir / "door-left-lit.png"
            image_path.write_bytes(b"fake png")
            output_record = minimal_image_output_record()
            (output_records_dir / "output-record-image-001.json").write_text(
                json.dumps(output_record),
                encoding="utf-8",
            )
            inventory = json.loads(
                (REPO_ROOT / "tests" / "fixtures" / "references" / "reference-inventory.json").read_text(
                    encoding="utf-8"
                )
            )
            old_tv_subject = inventory["subjects"][2]
            old_tv_image = old_tv_subject["expected_outputs"][0]
            old_tv_image["output_record_id"] = "out_door_left_lit_image_001"
            old_tv_image["output_record_refs"] = ["out_door_left_lit_image_001"]
            old_tv_image["output_status"] = "generated_draft"
            old_tv_image["readiness"] = "draft_generated"
            old_tv_image["visible_path"] = None
            old_tv_subject["output_record_refs"] = ["out_door_left_lit_image_001"]
            old_tv_subject["active_output_refs"] = []
            old_tv_subject["package_readiness"] = "planned"
            old_tv_subject["generated_output_count"] = 1
            old_tv_subject["accepted_output_count"] = 0
            old_tv_subject["missing_outputs"] = ["object_multi_angle_sheet"]
            (references_dir / "reference-inventory.json").write_text(
                json.dumps(inventory),
                encoding="utf-8",
            )
            manifest = minimal_manifest()
            manifest["paths"]["project_dir"] = "projects/proj_door_left_lit"
            manifest["paths"]["output_records_dir"] = "projects/proj_door_left_lit/outputs"
            manifest["paths"]["reference_inventory"] = "projects/proj_door_left_lit/references/reference-inventory.json"
            manifest["artist_library"] = {
                "project_dir": "Projects/door-left-lit",
                "project_pointer_path": "Projects/door-left-lit/.artist-os-project.json",
                "project_pointer_state": "present",
                "project_pointer_project_id": "proj_door_left_lit",
                "visible_state": "present",
                "user_facing_files": [],
            }
            (workspace_project_dir / "project.json").write_text(json.dumps(manifest), encoding="utf-8")
            args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
                artist_library_root=str(artist_library_root),
                project_id="proj_door_left_lit",
                reference_image_id="refimg_old_tv_multi_angle",
                state="accepted",
                filename="old-tv-reference.png",
                review_only=False,
                overwrite=False,
            )

            with redirect_stdout(StringIO()):
                artist_os_db.publish_visible_reference(args)

            destination = visible_project_dir / "References" / "Objects" / "old-tv" / "Accepted" / "old-tv-reference.png"
            self.assertEqual(destination.read_bytes(), b"fake png")
            manifest_after = json.loads((workspace_project_dir / "project.json").read_text(encoding="utf-8"))
            self.assertEqual(
                manifest_after["artist_library"]["user_facing_files"][0]["path"],
                "Wondermint/Artist Library/Projects/door-left-lit/References/Objects/old-tv/Accepted/old-tv-reference.png",
            )
            self.assertEqual(
                manifest_after["artist_library"]["user_facing_files"][0]["file_role"],
                "accepted_reference",
            )
            inventory_after = json.loads((references_dir / "reference-inventory.json").read_text(encoding="utf-8"))
            self.assertEqual(inventory_after["subjects"][2]["package_readiness"], "accepted")
            self.assertEqual(inventory_after["subjects"][2]["accepted_output_count"], 1)
            self.assertEqual(inventory_after["subjects"][2]["missing_outputs"], [])
            self.assertEqual(
                inventory_after["subjects"][2]["expected_outputs"][0]["visible_path"],
                "Wondermint/Artist Library/Projects/door-left-lit/References/Objects/old-tv/Accepted/old-tv-reference.png",
            )
            self.assertEqual(
                inventory_after["subjects"][2]["expected_outputs"][0]["output_status"],
                "accepted",
            )
            with closing(sqlite3.connect(library_root / "artist-os.sqlite")) as conn:
                file_ref = conn.execute(
                    "SELECT path, file_role, output_record_id FROM artist_library_files"
                ).fetchone()
                image_ref = conn.execute(
                    """
                    SELECT reference_image_id, status, visible_path, output_record_id
                    FROM reference_inventory_images
                    WHERE reference_image_id = 'refimg_old_tv_multi_angle'
                    """
                ).fetchone()

            self.assertEqual(
                file_ref,
                (
                    "Wondermint/Artist Library/Projects/door-left-lit/References/Objects/old-tv/Accepted/old-tv-reference.png",
                    "accepted_reference",
                    "out_door_left_lit_image_001",
                ),
            )
            self.assertEqual(
                image_ref,
                (
                    "refimg_old_tv_multi_angle",
                    "accepted",
                    "Wondermint/Artist Library/Projects/door-left-lit/References/Objects/old-tv/Accepted/old-tv-reference.png",
                    "out_door_left_lit_image_001",
                ),
            )

    def test_publish_visible_reference_preserves_review_only_and_rejects_acceptance(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            library_root = root / "workspace-library" / "artist-os"
            artist_library_root = root / "Wondermint" / "Artist Library"
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            output_records_dir = workspace_project_dir / "outputs"
            references_dir = workspace_project_dir / "references"
            generated_dir = workspace_project_dir / "assets" / "generated"
            visible_project_dir = artist_library_root / "Projects" / "door-left-lit"
            output_records_dir.mkdir(parents=True)
            references_dir.mkdir(parents=True)
            generated_dir.mkdir(parents=True)
            visible_project_dir.mkdir(parents=True)
            (visible_project_dir / ".artist-os-project.json").write_text(
                json.dumps({"schema_version": 1, "project_id": "proj_door_left_lit"}),
                encoding="utf-8",
            )
            image_path = generated_dir / "door-left-lit.png"
            image_path.write_bytes(b"fake png")
            output_record = minimal_image_output_record()
            (output_records_dir / "output-record-image-001.json").write_text(
                json.dumps(output_record),
                encoding="utf-8",
            )
            inventory = json.loads(
                (REPO_ROOT / "tests" / "fixtures" / "references" / "reference-inventory.json").read_text(
                    encoding="utf-8"
                )
            )
            old_tv_subject = inventory["subjects"][2]
            old_tv_image = old_tv_subject["expected_outputs"][0]
            old_tv_image["output_record_id"] = "out_door_left_lit_image_001"
            old_tv_image["output_record_refs"] = ["out_door_left_lit_image_001"]
            old_tv_image["output_status"] = "generated_draft"
            old_tv_image["readiness"] = "draft_generated"
            old_tv_image["visible_path"] = None
            old_tv_image["review_only"] = True
            old_tv_image["provider_input_allowed"] = False
            old_tv_image["provider_role_hints"] = ["review_only"]
            old_tv_image["allowed_use_scope"] = ["human_review_only", "internal_review"]
            old_tv_subject["output_record_refs"] = ["out_door_left_lit_image_001"]
            old_tv_subject["active_output_refs"] = []
            old_tv_subject["package_readiness"] = "planned"
            old_tv_subject["generated_output_count"] = 1
            old_tv_subject["accepted_output_count"] = 0
            old_tv_subject["missing_outputs"] = ["object_multi_angle_sheet"]
            (references_dir / "reference-inventory.json").write_text(
                json.dumps(inventory),
                encoding="utf-8",
            )
            manifest = minimal_manifest()
            manifest["paths"]["project_dir"] = "projects/proj_door_left_lit"
            manifest["paths"]["output_records_dir"] = "projects/proj_door_left_lit/outputs"
            manifest["paths"]["reference_inventory"] = "projects/proj_door_left_lit/references/reference-inventory.json"
            manifest["artist_library"] = {
                "project_dir": "Projects/door-left-lit",
                "project_pointer_path": "Projects/door-left-lit/.artist-os-project.json",
                "project_pointer_state": "present",
                "project_pointer_project_id": "proj_door_left_lit",
                "visible_state": "present",
                "user_facing_files": [],
            }
            (workspace_project_dir / "project.json").write_text(json.dumps(manifest), encoding="utf-8")
            args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
                artist_library_root=str(artist_library_root),
                project_id="proj_door_left_lit",
                reference_image_id="refimg_old_tv_multi_angle",
                state="accepted",
                filename="old-tv-reference.png",
                review_only=False,
                overwrite=False,
            )

            with self.assertRaisesRegex(SystemExit, "review-only reference images cannot be published as accepted"):
                with redirect_stdout(StringIO()):
                    artist_os_db.publish_visible_reference(args)

            accepted_destination = (
                visible_project_dir / "References" / "Objects" / "old-tv" / "Accepted" / "old-tv-reference.png"
            )
            self.assertFalse(accepted_destination.exists())

            args.state = "draft"
            with redirect_stdout(StringIO()):
                artist_os_db.publish_visible_reference(args)

            inventory_after = json.loads((references_dir / "reference-inventory.json").read_text(encoding="utf-8"))
            image_after = inventory_after["subjects"][2]["expected_outputs"][0]
            self.assertTrue(image_after["review_only"])
            self.assertFalse(image_after["provider_input_allowed"])
            self.assertEqual(image_after["provider_role_hints"], ["review_only"])
            self.assertEqual(image_after["allowed_use_scope"], ["human_review_only", "internal_review"])
            self.assertEqual(image_after["output_status"], "generated_draft")
            self.assertTrue(
                (
                    visible_project_dir
                    / "References"
                    / "Objects"
                    / "old-tv"
                    / "Review Drafts"
                    / "old-tv-reference.png"
                ).is_file()
            )

    def test_installer_passes_wondermint_root_even_with_low_level_workspace_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            skills_dir = root / "skills"
            workspace = root / "custom-workspace"
            wondermint = root / "wondermint-parent"
            env = os.environ.copy()
            env.update({
                "CODEX_SKILLS_DIR": str(skills_dir),
                "ARTIST_OS_LIBRARY_ROOT": str(workspace),
                "WONDERMINT_ROOT": str(wondermint),
            })

            import subprocess

            result = subprocess.run(
                ["bash", "bin/install-codex-dev-skills"],
                cwd=REPO_ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=True,
            )

            self.assertTrue((workspace / "artist-os.sqlite").is_file())
            self.assertTrue((wondermint / "Wondermint" / "Artist Library" / "Projects").is_dir())
            self.assertIn(f"Workspace Library initialized at:\n  {workspace}", result.stdout)
            self.assertIn(
                f"Artist Library initialized at:\n  {wondermint / 'Wondermint' / 'Artist Library'}",
                result.stdout,
            )

    def test_sync_indexes_visible_files_feedback_learning_and_performance_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            project_dir = library_root / "projects" / "proj_door_left_lit"
            project_dir.mkdir(parents=True)
            manifest = {
                "project_id": "proj_door_left_lit",
                "title": "Door Left Lit",
                "status": "active",
                "current_stage": "prompt_plan",
                "created_at": "2026-05-31T00:00:00Z",
                "updated_at": "2026-05-31T00:00:00Z",
                "summary": "A threshold image project.",
                "artist_library": {
                    "project_dir": "Wondermint/Artist Library/Projects/door-left-lit",
                    "project_pointer_path": "Wondermint/Artist Library/Projects/door-left-lit/.artist-os-project.json",
                    "project_pointer_state": "present",
                    "project_pointer_project_id": "proj_door_left_lit",
                    "visible_state": "present",
                    "last_checked_at": "2026-05-31T00:00:00Z",
                    "user_facing_files": [
                        {
                            "path": "Wondermint/Artist Library/Projects/door-left-lit/Images/Drafts/symbology-board-001.png",
                            "file_role": "review_draft",
                            "status": "current",
                            "output_record_id": None,
                            "updated_at": "2026-05-31T00:00:00Z",
                        }
                    ],
                },
                "feedback_state": {
                    "feedback_log_path": "projects/proj_door_left_lit/feedback-log.jsonl",
                    "learning_review_status": "pending",
                    "learning_reviewed_at": None,
                    "learning_refs": [
                        {
                            "ref_id": "learn_rawer_first_drafts",
                            "learning_type": "soft",
                            "path": "personal-library/learnings/rawer-first-drafts.json",
                            "status": "active",
                        }
                    ],
                    "performance_signal_refs": [
                        {
                            "signal_id": "perf_symbology_board_001",
                            "path": "personal-library/performance-signals/symbology-board-001.json",
                            "status": "active",
                        }
                    ],
                },
                "paths": {
                    "project_dir": "projects/proj_door_left_lit",
                    "events": "projects/proj_door_left_lit/events.jsonl",
                    "source_record": "projects/proj_door_left_lit/source/source-record.json",
                    "meaning_interview": "projects/proj_door_left_lit/meaning/meaning-interview.json",
                    "creative_brief_record": "projects/proj_door_left_lit/briefs/creative-brief.record.json",
                    "prompt_plan": "projects/proj_door_left_lit/prompt-plans/prompt-plan.json",
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
            args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
            )

            with redirect_stdout(StringIO()):
                artist_os_db.sync_db(args)

            db_path = library_root / "artist-os.sqlite"
            with closing(sqlite3.connect(db_path)) as conn:
                visible_state = conn.execute(
                    """
                    SELECT visible_state, artist_library_project_dir,
                           project_pointer_state, project_pointer_project_id
                    FROM project_visible_state
                    """
                ).fetchone()
                file_ref = conn.execute(
                    "SELECT path, file_role, status FROM artist_library_files"
                ).fetchone()
                feedback_state = conn.execute(
                    "SELECT feedback_log_path, learning_review_status FROM project_feedback_state"
                ).fetchone()
                learning_ref = conn.execute(
                    "SELECT ref_id, learning_type, status FROM learning_refs"
                ).fetchone()
                performance_ref = conn.execute(
                    "SELECT signal_id, status FROM performance_signal_refs"
                ).fetchone()

            self.assertEqual(
                visible_state,
                (
                    "present",
                    "Wondermint/Artist Library/Projects/door-left-lit",
                    "present",
                    "proj_door_left_lit",
                ),
            )
            self.assertEqual(
                file_ref,
                (
                    "Wondermint/Artist Library/Projects/door-left-lit/Images/Drafts/symbology-board-001.png",
                    "review_draft",
                    "current",
                ),
            )
            self.assertEqual(feedback_state, ("projects/proj_door_left_lit/feedback-log.jsonl", "pending"))
            self.assertEqual(learning_ref, ("learn_rawer_first_drafts", "soft", "active"))
            self.assertEqual(performance_ref, ("perf_symbology_board_001", "active"))

    def test_sync_marks_deleted_visible_project_as_visible_missing_not_project_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            library_root = root / ".wondermint" / "artist-os"
            project_dir = library_root / "projects" / "proj_door_left_lit"
            project_dir.mkdir(parents=True)
            manifest = minimal_manifest()
            manifest["artist_library"] = {
                "project_dir": "Wondermint/Artist Library/Projects/door-left-lit",
                "project_pointer_path": "Wondermint/Artist Library/Projects/door-left-lit/.artist-os-project.json",
                "project_pointer_state": "present",
                "project_pointer_project_id": "proj_door_left_lit",
                "visible_state": "present",
            }
            (project_dir / "project.json").write_text(json.dumps(manifest), encoding="utf-8")
            args = argparse.Namespace(
                db=None,
                library_root=None,
                wondermint_root=str(root),
            )

            with redirect_stdout(StringIO()):
                artist_os_db.sync_db(args)

            with closing(sqlite3.connect(library_root / "artist-os.sqlite")) as conn:
                project_status = conn.execute("SELECT status FROM projects").fetchone()[0]
                visible_state = conn.execute(
                    """
                    SELECT visible_state, project_pointer_state, project_pointer_project_id
                    FROM project_visible_state
                    """
                ).fetchone()

            self.assertEqual(project_status, "active")
            self.assertEqual(visible_state, ("visible_missing", "missing", None))

    def test_sync_tolerates_manifest_with_empty_decisions(self) -> None:
        # Regression: a manifest with an empty `decisions` object once raised
        # KeyError in upsert_manifest, which bracket-accessed the NOT NULL status
        # fields after defaulting `decisions` to {}. Sync must skip the decisions
        # row (like it does for artist_library/feedback_state) instead of crashing.
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            library_root = root / ".wondermint" / "artist-os"
            project_dir = library_root / "projects" / "proj_door_left_lit"
            project_dir.mkdir(parents=True)
            manifest = minimal_manifest()
            manifest["decisions"] = {}
            (project_dir / "project.json").write_text(json.dumps(manifest), encoding="utf-8")
            args = argparse.Namespace(db=None, library_root=None, wondermint_root=str(root))

            with redirect_stdout(StringIO()):
                artist_os_db.sync_db(args)  # must not raise

            with closing(sqlite3.connect(library_root / "artist-os.sqlite")) as conn:
                project_row = conn.execute(
                    "SELECT status FROM projects WHERE project_id = ?", ("proj_door_left_lit",)
                ).fetchone()
                decision_rows = conn.execute(
                    "SELECT COUNT(*) FROM project_decisions WHERE project_id = ?", ("proj_door_left_lit",)
                ).fetchone()[0]

            self.assertEqual(project_row, ("active",), "project should still be indexed")
            self.assertEqual(decision_rows, 0, "empty decisions must index no project_decisions row")

    def test_sync_indexes_concrete_output_records_and_artifacts_from_output_records_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            project_id = "proj_door_left_lit"
            workspace_project_dir = library_root / "projects" / project_id
            output_records_dir = workspace_project_dir / "outputs" / "audio" / "output-records"
            output_records_dir.mkdir(parents=True)
            manifest = minimal_manifest(project_id)
            manifest["paths"]["output_records_dir"] = f"projects/{project_id}/outputs"
            (workspace_project_dir / "project.json").write_text(json.dumps(manifest), encoding="utf-8")
            output_record = minimal_output_record(project_id)
            (output_records_dir / "output-record-audio-001.json").write_text(
                json.dumps(output_record),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
            )

            with redirect_stdout(StringIO()):
                artist_os_db.sync_db(args)

            with closing(sqlite3.connect(library_root / "artist-os.sqlite")) as conn:
                record_rows = conn.execute(
                    """
                    SELECT record_type, path, status
                    FROM records
                    WHERE project_id = ? AND record_type = 'output_record'
                    """,
                    (project_id,),
                ).fetchall()
                artifact_row = conn.execute(
                    """
                    SELECT output_record_id, artifact_id, artifact_kind, uri_or_path,
                           origin_type, provider, review_status, acceptance_status
                    FROM output_artifacts
                    WHERE project_id = ?
                    """,
                    (project_id,),
                ).fetchone()

            self.assertEqual(
                record_rows,
                [
                    (
                        "output_record",
                        "projects/proj_door_left_lit/outputs/audio/output-records/output-record-audio-001.json",
                        "pending",
                    )
                ],
            )
            self.assertEqual(
                artifact_row,
                (
                    "out_door_left_lit_audio_001",
                    "artifact_door_left_lit_audio_001",
                    "audio",
                    "projects/proj_door_left_lit/outputs/audio/generated/door-left-lit.mp3",
                    "artist_imported",
                    "suno",
                    "not_reviewed",
                    "pending",
                ),
            )

    def test_sync_indexes_reference_inventory_items_and_images(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            project_id = "proj_door_left_lit"
            workspace_project_dir = library_root / "projects" / project_id
            references_dir = workspace_project_dir / "references"
            references_dir.mkdir(parents=True)
            manifest = minimal_manifest(project_id)
            manifest["paths"]["reference_inventory"] = f"projects/{project_id}/references/reference-inventory.json"
            (workspace_project_dir / "project.json").write_text(json.dumps(manifest), encoding="utf-8")
            inventory = json.loads(
                (REPO_ROOT / "tests" / "fixtures" / "references" / "reference-inventory.json").read_text(
                    encoding="utf-8"
                )
            )
            (references_dir / "reference-inventory.json").write_text(
                json.dumps(inventory),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
            )

            with redirect_stdout(StringIO()):
                artist_os_db.sync_db(args)

            with closing(sqlite3.connect(library_root / "artist-os.sqlite")) as conn:
                item_rows = conn.execute(
                    """
                    SELECT reference_item_id, category, subject_slug, current_status,
                           strategy_status, continuity_risk_level, visible_subject_dir
                    FROM reference_inventory_items
                    WHERE project_id = ?
                    ORDER BY category, subject_slug
                    """,
                    (project_id,),
                ).fetchall()
                image_rows = conn.execute(
                    """
                    SELECT reference_image_id, reference_item_id, role, status,
                           output_record_id, visible_path, provider_input_allowed,
                           review_only
                    FROM reference_inventory_images
                    WHERE project_id = ?
                    ORDER BY reference_item_id, role, reference_image_id
                    """,
                    (project_id,),
                ).fetchall()
                record_row = conn.execute(
                    """
                    SELECT record_type, path
                    FROM records
                    WHERE project_id = ? AND record_type = 'reference_inventory'
                    """,
                    (project_id,),
                ).fetchone()

            self.assertEqual(
                item_rows,
                [
                    (
                        "refsub_door_keeper",
                        "character",
                        "door-keeper",
                        "accepted_for_planning",
                        "accepted",
                        "high",
                        "Wondermint/Artist Library/Projects/door-left-lit/References/Characters/door-keeper",
                    ),
                    (
                        "refsub_hallway_threshold",
                        "location",
                        "hallway-threshold",
                        "accepted_for_planning",
                        "accepted_partial",
                        "high",
                        "Wondermint/Artist Library/Projects/door-left-lit/References/Locations/hallway-threshold",
                    ),
                    (
                        "refsub_old_tv",
                        "object",
                        "old-tv",
                        "accepted_for_planning",
                        "accepted",
                        "high",
                        "Wondermint/Artist Library/Projects/door-left-lit/References/Objects/old-tv",
                    ),
                ],
            )
            self.assertEqual(len(image_rows), 8)
            self.assertIn(
                (
                    "refimg_door_keeper_raincoat",
                    "refsub_door_keeper",
                    "character_wardrobe_sheet",
                    "planned",
                    None,
                    None,
                    1,
                    0,
                ),
                image_rows,
            )
            self.assertIn(
                (
                    "refimg_old_tv_multi_angle",
                    "refsub_old_tv",
                    "object_multi_angle_sheet",
                    "accepted",
                    "out_old_tv_reference",
                    "Wondermint/Artist Library/Projects/door-left-lit/References/Objects/old-tv/Accepted/old-tv-multi-angle.png",
                    1,
                    0,
                ),
                image_rows,
            )
            self.assertEqual(
                record_row,
                (
                    "reference_inventory",
                    "projects/proj_door_left_lit/references/reference-inventory.json",
                ),
            )

    def test_sync_preserves_reference_index_when_inventory_is_malformed(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            project_id = "proj_door_left_lit"
            workspace_project_dir = library_root / "projects" / project_id
            references_dir = workspace_project_dir / "references"
            references_dir.mkdir(parents=True)
            manifest = minimal_manifest(project_id)
            manifest["paths"]["reference_inventory"] = f"projects/{project_id}/references/reference-inventory.json"
            (workspace_project_dir / "project.json").write_text(json.dumps(manifest), encoding="utf-8")
            inventory = json.loads(
                (REPO_ROOT / "tests" / "fixtures" / "references" / "reference-inventory.json").read_text(
                    encoding="utf-8"
                )
            )
            inventory_path = references_dir / "reference-inventory.json"
            inventory_path.write_text(json.dumps(inventory), encoding="utf-8")
            args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
            )

            with redirect_stdout(StringIO()):
                artist_os_db.sync_db(args)

            malformed_inventory = json.loads(json.dumps(inventory))
            del malformed_inventory["subjects"][0]["subject_category"]
            inventory_path.write_text(json.dumps(malformed_inventory), encoding="utf-8")

            with redirect_stdout(StringIO()):
                artist_os_db.sync_db(args)

            with closing(sqlite3.connect(library_root / "artist-os.sqlite")) as conn:
                item_count = conn.execute(
                    "SELECT COUNT(*) FROM reference_inventory_items WHERE project_id = ?",
                    (project_id,),
                ).fetchone()[0]
                image_count = conn.execute(
                    "SELECT COUNT(*) FROM reference_inventory_images WHERE project_id = ?",
                    (project_id,),
                ).fetchone()[0]
                project_row = conn.execute(
                    "SELECT status FROM projects WHERE project_id = ?",
                    (project_id,),
                ).fetchone()

            self.assertEqual(project_row, ("active",))
            self.assertEqual(item_count, 3)
            self.assertEqual(image_count, 8)

    def test_reference_state_refresh_tolerates_missing_output_role_and_marks_retired(self) -> None:
        subject = {
            "expected_outputs": [
                {
                    "reference_output_id": "refout_retired_reference",
                    "output_status": "retired",
                }
            ],
            "planned_output_count": 1,
            "generated_output_count": 0,
            "accepted_output_count": 0,
            "output_record_refs": [],
            "active_output_refs": [],
            "missing_outputs": ["custom"],
            "package_readiness": "planned",
        }

        artist_os_db.refresh_reference_subject_state(subject)

        self.assertEqual(subject["missing_outputs"], [])
        self.assertEqual(subject["package_readiness"], "retired")

    def test_reference_readiness_blocks_missing_required_outputs_until_waived(self) -> None:
        inventory = json.loads(
            (REPO_ROOT / "tests" / "fixtures" / "references" / "reference-inventory.json").read_text(
                encoding="utf-8"
            )
        )

        blockers = artist_os_db.reference_readiness_blockers(inventory, "storyboard_export")
        blocked_roles = {blocker["output_role"] for blocker in blockers}

        self.assertIn("character_identity_plate", blocked_roles)
        self.assertIn("location_establishing_angle", blocked_roles)
        self.assertIn("location_reverse_angle", blocked_roles)
        self.assertNotIn("object_multi_angle_sheet", blocked_roles)

        for subject in inventory["subjects"]:
            for output in subject["expected_outputs"]:
                if output["required_before"] == "storyboard_export" and output["readiness"] != "accepted":
                    output["readiness"] = "waived"
                    output["output_status"] = "waived"
                    output["waiver_ref"] = "gate_reference_readiness_waiver"
            if subject["missing_outputs"]:
                subject["risk_notes"].append("Artist waived missing reference outputs for storyboard export.")

        self.assertEqual(
            artist_os_db.reference_readiness_blockers(inventory, "storyboard_export"),
            [],
        )

    def test_sync_skips_output_artifact_index_when_required_artifact_fields_are_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            project_id = "proj_door_left_lit"
            workspace_project_dir = library_root / "projects" / project_id
            output_records_dir = workspace_project_dir / "outputs"
            output_records_dir.mkdir(parents=True)
            manifest = minimal_manifest(project_id)
            manifest["paths"]["output_records_dir"] = f"projects/{project_id}/outputs"
            (workspace_project_dir / "project.json").write_text(json.dumps(manifest), encoding="utf-8")
            output_record = minimal_output_record(project_id)
            del output_record["output_artifact"]["mime_type"]
            (output_records_dir / "output-record-audio-001.json").write_text(
                json.dumps(output_record),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
            )

            with redirect_stdout(StringIO()):
                artist_os_db.sync_db(args)

            with closing(sqlite3.connect(library_root / "artist-os.sqlite")) as conn:
                record_count = conn.execute(
                    "SELECT COUNT(*) FROM records WHERE project_id = ? AND record_type = 'output_record'",
                    (project_id,),
                ).fetchone()[0]
                artifact_count = conn.execute(
                    "SELECT COUNT(*) FROM output_artifacts WHERE project_id = ?",
                    (project_id,),
                ).fetchone()[0]

            self.assertEqual(record_count, 1)
            self.assertEqual(artifact_count, 0)

    def test_project_manifest_schema_allows_visible_missing_null_pointer_project_id(self) -> None:
        schema = json.loads((REPO_ROOT / "schemas" / "project-manifest.schema.json").read_text(encoding="utf-8"))
        manifest = minimal_manifest()
        manifest["artist_library"] = {
            "project_dir": "Wondermint/Artist Library/Projects/door-left-lit",
            "project_pointer_path": "Wondermint/Artist Library/Projects/door-left-lit/.artist-os-project.json",
            "project_pointer_state": "missing",
            "project_pointer_project_id": None,
            "visible_state": "visible_missing",
        }

        validate(manifest, schema, schema)

    def test_project_manifest_schema_accepts_resume_state(self) -> None:
        # Slice 1 (ADR 0012 D5): optional resume_state projection + media index.
        schema = json.loads((REPO_ROOT / "schemas" / "project-manifest.schema.json").read_text(encoding="utf-8"))
        manifest = minimal_manifest()
        manifest["resume_state"] = {
            "current_checkpoint": "medium_plan",
            "next_phase": "Medium Plan",
            "effective_project_scale": "structured_single_artifact",
            "cross_medium_plan_ref": None,
            "media_index": [
                {
                    "medium": "image",
                    "medium_role": "primary",
                    "medium_plan_ref": "imp_door_left_lit",
                    "status": "complete",
                    "artist_meaning_id": "am_door_left_lit",
                    "transformation_brief_id": "tb_door_left_lit",
                    "beat_plan_id": "bp_door_left_lit",
                },
                {"medium": "audio", "status": "active", "beat_plan_id": "bp_door_left_lit"},
            ],
        }
        validate(manifest, schema, schema)

    def test_project_manifest_schema_resume_state_is_optional(self) -> None:
        # Backward compatibility: manifests with no resume_state still validate.
        schema = json.loads((REPO_ROOT / "schemas" / "project-manifest.schema.json").read_text(encoding="utf-8"))
        manifest = minimal_manifest()
        self.assertNotIn("resume_state", manifest)
        validate(manifest, schema, schema)

    def test_project_manifest_schema_rejects_unknown_medium_token(self) -> None:
        # 'sound' is not a medium token (the medium is 'audio'); the enum must bite.
        schema = json.loads((REPO_ROOT / "schemas" / "project-manifest.schema.json").read_text(encoding="utf-8"))
        manifest = minimal_manifest()
        manifest["resume_state"] = {
            "current_checkpoint": "medium_plan",
            "next_phase": "Medium Plan",
            "media_index": [{"medium": "sound", "status": "active"}],
        }
        with self.assertRaisesRegex(ValidationError, "is not one of"):
            validate(manifest, schema, schema)

    def test_project_manifest_schema_rejects_unknown_effective_scale(self) -> None:
        schema = json.loads((REPO_ROOT / "schemas" / "project-manifest.schema.json").read_text(encoding="utf-8"))
        manifest = minimal_manifest()
        manifest["resume_state"] = {
            "current_checkpoint": "medium_plan",
            "next_phase": "Medium Plan",
            "effective_project_scale": "nonsense",
            "media_index": [],
        }
        with self.assertRaisesRegex(ValidationError, "is not one of"):
            validate(manifest, schema, schema)

    def test_project_manifest_schema_rejects_duplicate_resume_media(self) -> None:
        schema = json.loads((REPO_ROOT / "schemas" / "project-manifest.schema.json").read_text(encoding="utf-8"))
        manifest = minimal_manifest()
        manifest["resume_state"] = {
            "current_checkpoint": "medium_plan",
            "next_phase": "Medium Plan",
            "media_index": [
                {"medium": "image", "status": "active"},
                {"medium": "image", "status": "complete"},
            ],
        }
        with self.assertRaisesRegex(ValidationError, "media_index must not duplicate medium entries"):
            validate(manifest, schema, schema)

    def test_project_manifest_schema_resume_state_rejects_unknown_key(self) -> None:
        # additionalProperties:false must reject stray keys inside resume_state.
        schema = json.loads((REPO_ROOT / "schemas" / "project-manifest.schema.json").read_text(encoding="utf-8"))
        manifest = minimal_manifest()
        manifest["resume_state"] = {
            "current_checkpoint": "medium_plan",
            "next_phase": "Medium Plan",
            "media_index": [],
            "resume_packet": "nope",
        }
        with self.assertRaisesRegex(ValidationError, "unexpected fields"):
            validate(manifest, schema, schema)

    def test_sync_marks_retargeted_project_pointer_as_visible_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            library_root = root / ".wondermint" / "artist-os"
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            visible_project_dir = root / "Wondermint" / "Artist Library" / "Projects" / "door-left-lit"
            workspace_project_dir.mkdir(parents=True)
            visible_project_dir.mkdir(parents=True)
            (visible_project_dir / ".artist-os-project.json").write_text(
                json.dumps({"schema_version": 1, "project_id": "proj_other"}),
                encoding="utf-8",
            )
            manifest = minimal_manifest()
            manifest["artist_library"] = {
                "project_dir": "Wondermint/Artist Library/Projects/door-left-lit",
                "project_pointer_path": "Wondermint/Artist Library/Projects/door-left-lit/.artist-os-project.json",
                "project_pointer_state": "present",
                "project_pointer_project_id": "proj_door_left_lit",
                "visible_state": "present",
            }
            (workspace_project_dir / "project.json").write_text(json.dumps(manifest), encoding="utf-8")
            args = argparse.Namespace(
                db=None,
                library_root=None,
                wondermint_root=str(root),
            )

            with redirect_stdout(StringIO()):
                artist_os_db.sync_db(args)

            with closing(sqlite3.connect(library_root / "artist-os.sqlite")) as conn:
                visible_state = conn.execute(
                    """
                    SELECT visible_state, project_pointer_state, project_pointer_project_id
                    FROM project_visible_state
                    """
                ).fetchone()

            self.assertEqual(visible_state, ("visible_missing", "retargeted", "proj_other"))

    def test_sync_marks_malformed_pointer_payload_as_invalid_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            library_root = root / ".wondermint" / "artist-os"
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            visible_project_dir = root / "Wondermint" / "Artist Library" / "Projects" / "door-left-lit"
            workspace_project_dir.mkdir(parents=True)
            visible_project_dir.mkdir(parents=True)
            (visible_project_dir / ".artist-os-project.json").write_text(
                json.dumps({"schema_version": 1, "project_id": ["proj_door_left_lit"]}),
                encoding="utf-8",
            )
            manifest = minimal_manifest()
            manifest["artist_library"] = {
                "project_dir": "Wondermint/Artist Library/Projects/door-left-lit",
                "project_pointer_path": "Wondermint/Artist Library/Projects/door-left-lit/.artist-os-project.json",
                "project_pointer_state": "present",
                "project_pointer_project_id": "proj_door_left_lit",
                "visible_state": "present",
            }
            (workspace_project_dir / "project.json").write_text(json.dumps(manifest), encoding="utf-8")
            args = argparse.Namespace(
                db=None,
                library_root=None,
                wondermint_root=str(root),
            )

            with redirect_stdout(StringIO()):
                artist_os_db.sync_db(args)

            with closing(sqlite3.connect(library_root / "artist-os.sqlite")) as conn:
                visible_state = conn.execute(
                    """
                    SELECT visible_state, project_pointer_state, project_pointer_project_id
                    FROM project_visible_state
                    """
                ).fetchone()

            self.assertEqual(visible_state, ("visible_missing", "invalid", None))

    def test_sync_resolves_project_relative_pointer_and_visible_file_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            library_root = root / ".wondermint" / "artist-os"
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            visible_project_dir = root / "Wondermint" / "Artist Library" / "Projects" / "door-left-lit"
            workspace_project_dir.mkdir(parents=True)
            visible_project_dir.mkdir(parents=True)
            (visible_project_dir / ".artist-os-project.json").write_text(
                json.dumps({"schema_version": 1, "project_id": "proj_door_left_lit"}),
                encoding="utf-8",
            )
            manifest = minimal_manifest()
            manifest["artist_library"] = {
                "project_dir": "Wondermint/Artist Library/Projects/door-left-lit",
                "project_pointer_path": ".artist-os-project.json",
                "project_pointer_state": "present",
                "project_pointer_project_id": "proj_door_left_lit",
                "visible_state": "present",
                "user_facing_files": [
                    {
                        "path": "Images/Drafts/missing.png",
                        "file_role": "review_draft",
                        "status": "current",
                    }
                ],
            }
            (workspace_project_dir / "project.json").write_text(json.dumps(manifest), encoding="utf-8")
            args = argparse.Namespace(
                db=None,
                library_root=None,
                wondermint_root=str(root),
            )

            with redirect_stdout(StringIO()):
                artist_os_db.sync_db(args)

            with closing(sqlite3.connect(library_root / "artist-os.sqlite")) as conn:
                visible_state = conn.execute(
                    "SELECT visible_state, project_pointer_state FROM project_visible_state"
                ).fetchone()
                file_status = conn.execute("SELECT status FROM artist_library_files").fetchone()[0]

            self.assertEqual(visible_state, ("present", "present"))
            self.assertEqual(file_status, "missing")

    def test_sync_marks_missing_user_facing_files_without_requiring_visible_root_mirror(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            library_root = root / ".wondermint" / "artist-os"
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            visible_project_dir = root / "Wondermint" / "Artist Library" / "Projects" / "door-left-lit"
            workspace_project_dir.mkdir(parents=True)
            visible_project_dir.mkdir(parents=True)
            (visible_project_dir / ".artist-os-project.json").write_text(
                json.dumps({"schema_version": 1, "project_id": "proj_door_left_lit"}),
                encoding="utf-8",
            )
            manifest = minimal_manifest()
            manifest["artist_library"] = {
                "project_dir": "Wondermint/Artist Library/Projects/door-left-lit",
                "project_pointer_path": "Wondermint/Artist Library/Projects/door-left-lit/.artist-os-project.json",
                "project_pointer_state": "present",
                "project_pointer_project_id": "proj_door_left_lit",
                "visible_state": "present",
                "user_facing_files": [
                    {
                        "path": "Wondermint/Artist Library/Projects/door-left-lit/Images/Drafts/missing.png",
                        "file_role": "review_draft",
                        "status": "current",
                    }
                ],
            }
            (workspace_project_dir / "project.json").write_text(json.dumps(manifest), encoding="utf-8")
            args = argparse.Namespace(
                db=None,
                library_root=None,
                wondermint_root=str(root),
            )

            with redirect_stdout(StringIO()):
                artist_os_db.sync_db(args)

            with closing(sqlite3.connect(library_root / "artist-os.sqlite")) as conn:
                file_status = conn.execute("SELECT status FROM artist_library_files").fetchone()[0]

            self.assertEqual(file_status, "missing")

    def test_sync_resolves_repo_relative_wondermint_visible_file_paths_before_project_relative_join(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            library_root = root / "workspace-library" / "artist-os"
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            visible_project_dir = root / "Wondermint" / "Artist Library" / "Projects" / "door-left-lit"
            workspace_project_dir.mkdir(parents=True)
            visible_project_dir.mkdir(parents=True)
            (visible_project_dir / ".artist-os-project.json").write_text(
                json.dumps({"schema_version": 1, "project_id": "proj_door_left_lit"}),
                encoding="utf-8",
            )
            visible_file = visible_project_dir / "Audio" / "Drafts" / "draft.mp3"
            visible_file.parent.mkdir(parents=True)
            visible_file.write_bytes(b"fake mp3")
            manifest = minimal_manifest()
            manifest["artist_library"] = {
                "project_dir": "Wondermint/Artist Library/Projects/door-left-lit",
                "project_pointer_path": "Wondermint/Artist Library/Projects/door-left-lit/.artist-os-project.json",
                "project_pointer_state": "present",
                "project_pointer_project_id": "proj_door_left_lit",
                "visible_state": "present",
                "user_facing_files": [
                    {
                        "path": "Wondermint/Artist Library/Projects/door-left-lit/Audio/Drafts/draft.mp3",
                        "file_role": "review_draft",
                        "status": "current",
                    }
                ],
            }
            (workspace_project_dir / "project.json").write_text(json.dumps(manifest), encoding="utf-8")
            args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
            )

            with patch.object(artist_os_db, "REPO_ROOT", root):
                with redirect_stdout(StringIO()):
                    artist_os_db.sync_db(args)

            with closing(sqlite3.connect(library_root / "artist-os.sqlite")) as conn:
                file_status = conn.execute("SELECT status FROM artist_library_files").fetchone()[0]

            self.assertEqual(file_status, "current")

    def test_add_feedback_appends_log_marks_pending_and_indexes_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            workspace_project_dir.mkdir(parents=True)
            (workspace_project_dir / "project.json").write_text(
                json.dumps(minimal_manifest()),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
                project_id="proj_door_left_lit",
                feedback="The first draft should be rawer.",
                feedback_id="fb_door_left_lit_test",
                source="artist",
                stage="project_completion",
                output_record_id=None,
                notes=None,
            )

            with redirect_stdout(StringIO()):
                artist_os_db.add_feedback(args)

            feedback_log = workspace_project_dir / "feedback-log.jsonl"
            entry = json.loads(feedback_log.read_text(encoding="utf-8").strip())
            manifest = json.loads((workspace_project_dir / "project.json").read_text(encoding="utf-8"))

            self.assertEqual(entry["feedback_id"], "fb_door_left_lit_test")
            self.assertEqual(entry["learning_review_status"], "pending")
            self.assertEqual(manifest["feedback_state"]["learning_review_status"], "pending")
            with closing(sqlite3.connect(library_root / "artist-os.sqlite")) as conn:
                pending = conn.execute(
                    "SELECT learning_review_status FROM project_feedback_state"
                ).fetchone()[0]
            self.assertEqual(pending, "pending")

    def test_add_feedback_validates_optional_output_record_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            workspace_project_dir.mkdir(parents=True)
            (workspace_project_dir / "project.json").write_text(
                json.dumps(minimal_manifest()),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
                project_id="proj_door_left_lit",
                feedback="The first draft should be rawer.",
                feedback_id="fb_door_left_lit_test",
                source="artist",
                stage="project_completion",
                output_record_id="bad_output_id",
                notes=None,
            )

            with self.assertRaisesRegex(SystemExit, "output_record_id must match"):
                artist_os_db.add_feedback(args)

    def test_add_feedback_rejects_absolute_feedback_log_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            workspace_project_dir.mkdir(parents=True)
            manifest = minimal_manifest()
            manifest["feedback_state"] = {
                "feedback_log_path": str(library_root.parent / "outside-feedback.jsonl"),
                "learning_review_status": "pending",
            }
            (workspace_project_dir / "project.json").write_text(
                json.dumps(manifest),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
                project_id="proj_door_left_lit",
                feedback="The first draft should be rawer.",
                feedback_id="fb_door_left_lit_test",
                source="artist",
                stage="project_completion",
                output_record_id=None,
                notes=None,
            )

            with self.assertRaisesRegex(SystemExit, "feedback_log_path"):
                artist_os_db.add_feedback(args)

    def test_add_feedback_rejects_parent_traversal_feedback_log_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            workspace_project_dir.mkdir(parents=True)
            manifest = minimal_manifest()
            manifest["feedback_state"] = {
                "feedback_log_path": "../outside-feedback.jsonl",
                "learning_review_status": "pending",
            }
            (workspace_project_dir / "project.json").write_text(
                json.dumps(manifest),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
                project_id="proj_door_left_lit",
                feedback="The first draft should be rawer.",
                feedback_id="fb_door_left_lit_test",
                source="artist",
                stage="project_completion",
                output_record_id=None,
                notes=None,
            )

            with self.assertRaisesRegex(SystemExit, "feedback_log_path"):
                artist_os_db.add_feedback(args)

    def test_add_learning_rejects_learning_rule_over_600_characters(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            workspace_project_dir.mkdir(parents=True)
            (workspace_project_dir / "project.json").write_text(
                json.dumps(minimal_manifest()),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
                project_id="proj_door_left_lit",
                learning_id="learn_too_long",
                learning_type="soft",
                learning_rule="x" * 601,
                scope=None,
                evidence_type="feedback_entry",
                evidence_ref=None,
                evidence_summary=None,
                occurrence_count=1,
                promotion_reason=None,
            )

            with self.assertRaisesRegex(SystemExit, "600 characters or fewer"):
                artist_os_db.add_learning(args)

    def test_learning_record_schema_requires_evidence_ref(self) -> None:
        schema = json.loads((REPO_ROOT / "schemas" / "learning-record.schema.json").read_text(encoding="utf-8"))
        record = {
            "learning_id": "learn_rawer_first_drafts",
            "learning_type": "soft",
            "status": "active",
            "learning_rule": "Keep first drafts rawer before polishing.",
            "scope": None,
            "source_project_ids": ["proj_door_left_lit"],
            "evidence_refs": [],
            "promotion_state": {
                "occurrence_count": 1,
                "promotion_reason": None,
            },
            "created_at": "2026-05-31T00:00:00Z",
            "updated_at": "2026-05-31T00:00:00Z",
        }

        with self.assertRaisesRegex(ValidationError, "evidence_refs"):
            validate(record, schema, schema)

    def test_add_learning_requires_evidence_ref_and_does_not_mark_feedback(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            workspace_project_dir.mkdir(parents=True)
            (workspace_project_dir / "project.json").write_text(
                json.dumps(minimal_manifest()),
                encoding="utf-8",
            )
            feedback_args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
                project_id="proj_door_left_lit",
                feedback="The first draft should be rawer.",
                feedback_id="fb_door_left_lit_test",
                source="artist",
                stage="project_completion",
                output_record_id=None,
                notes=None,
            )
            with redirect_stdout(StringIO()):
                artist_os_db.add_feedback(feedback_args)
            learning_args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
                project_id="proj_door_left_lit",
                learning_id="learn_rawer_first_drafts",
                learning_type="soft",
                learning_rule="Keep first drafts rawer before polishing.",
                scope=None,
                evidence_type="feedback_entry",
                evidence_ref=None,
                evidence_summary=None,
                occurrence_count=1,
                promotion_reason=None,
                mark_review_complete=True,
                overwrite=False,
            )

            with self.assertRaisesRegex(SystemExit, "at least one --evidence-ref"):
                artist_os_db.add_learning(learning_args)

            manifest = json.loads((workspace_project_dir / "project.json").read_text(encoding="utf-8"))
            feedback_entry = json.loads((workspace_project_dir / "feedback-log.jsonl").read_text(encoding="utf-8").strip())
            self.assertEqual(manifest["feedback_state"]["learning_review_status"], "pending")
            self.assertEqual(feedback_entry["learning_review_status"], "pending")

    def test_add_learning_writes_record_links_manifest_and_indexes_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            workspace_project_dir.mkdir(parents=True)
            (workspace_project_dir / "project.json").write_text(
                json.dumps(minimal_manifest()),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
                project_id="proj_door_left_lit",
                learning_id="learn_rawer_first_drafts",
                learning_type="hard",
                learning_rule="Fill the su-node fields exactly when tool output requires that schema.",
                scope="schema mismatch",
                evidence_type="tool_field_mismatch",
                evidence_ref=["fb_door_left_lit_test"],
                evidence_summary="Concrete tool-field mismatch.",
                occurrence_count=1,
                promotion_reason="Concrete schema mismatch can become hard learning immediately.",
                mark_review_complete=False,
                overwrite=False,
            )

            with redirect_stdout(StringIO()):
                artist_os_db.add_learning(args)

            learning_path = library_root / "personal-library" / "learnings" / "learn_rawer_first_drafts.json"
            record = json.loads(learning_path.read_text(encoding="utf-8"))
            manifest = json.loads((workspace_project_dir / "project.json").read_text(encoding="utf-8"))

            self.assertEqual(record["learning_type"], "hard")
            self.assertEqual(record["evidence_refs"][0]["evidence_type"], "tool_field_mismatch")
            self.assertEqual(
                manifest["feedback_state"]["learning_refs"][0]["path"],
                "personal-library/learnings/learn_rawer_first_drafts.json",
            )
            with closing(sqlite3.connect(library_root / "artist-os.sqlite")) as conn:
                learning_ref = conn.execute(
                    "SELECT ref_id, learning_type, status FROM learning_refs"
                ).fetchone()
            self.assertEqual(learning_ref, ("learn_rawer_first_drafts", "hard", "active"))

    def test_add_learning_validates_id_and_refuses_path_escape(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            workspace_project_dir.mkdir(parents=True)
            (workspace_project_dir / "project.json").write_text(
                json.dumps(minimal_manifest()),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
                project_id="proj_door_left_lit",
                learning_id="../escape",
                learning_type="soft",
                learning_rule="Stay compact.",
                scope=None,
                evidence_type="feedback_entry",
                evidence_ref=["fb_door_left_lit_test"],
                evidence_summary=None,
                occurrence_count=1,
                promotion_reason=None,
                mark_review_complete=False,
                overwrite=False,
            )

            with self.assertRaisesRegex(SystemExit, "learning_id must match"):
                artist_os_db.add_learning(args)

    def test_add_learning_refuses_existing_record_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            learning_dir = library_root / "personal-library" / "learnings"
            workspace_project_dir.mkdir(parents=True)
            learning_dir.mkdir(parents=True)
            (workspace_project_dir / "project.json").write_text(
                json.dumps(minimal_manifest()),
                encoding="utf-8",
            )
            (learning_dir / "learn_existing.json").write_text("{}", encoding="utf-8")
            args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
                project_id="proj_door_left_lit",
                learning_id="learn_existing",
                learning_type="soft",
                learning_rule="Stay compact.",
                scope=None,
                evidence_type="feedback_entry",
                evidence_ref=["fb_door_left_lit_test"],
                evidence_summary=None,
                occurrence_count=1,
                promotion_reason=None,
                mark_review_complete=False,
                overwrite=False,
            )

            with self.assertRaisesRegex(SystemExit, "record already exists"):
                artist_os_db.add_learning(args)

    def test_add_learning_can_mark_review_complete_and_classify_feedback(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            workspace_project_dir.mkdir(parents=True)
            (workspace_project_dir / "project.json").write_text(
                json.dumps(minimal_manifest()),
                encoding="utf-8",
            )
            feedback_args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
                project_id="proj_door_left_lit",
                feedback="The first draft should be rawer.",
                feedback_id="fb_door_left_lit_test",
                source="artist",
                stage="project_completion",
                output_record_id=None,
                notes=None,
            )
            with redirect_stdout(StringIO()):
                artist_os_db.add_feedback(feedback_args)
            learning_args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
                project_id="proj_door_left_lit",
                learning_id="learn_rawer_first_drafts",
                learning_type="soft",
                learning_rule="Keep first drafts rawer before polishing.",
                scope=None,
                evidence_type="feedback_entry",
                evidence_ref=["fb_door_left_lit_test"],
                evidence_summary="Artist requested rawer first drafts.",
                occurrence_count=1,
                promotion_reason=None,
                mark_review_complete=True,
                overwrite=False,
            )

            with redirect_stdout(StringIO()):
                artist_os_db.add_learning(learning_args)

            manifest = json.loads((workspace_project_dir / "project.json").read_text(encoding="utf-8"))
            feedback_entry = json.loads((workspace_project_dir / "feedback-log.jsonl").read_text(encoding="utf-8").strip())
            with closing(sqlite3.connect(library_root / "artist-os.sqlite")) as conn:
                pending_count = conn.execute(
                    "SELECT COUNT(*) FROM project_feedback_state WHERE learning_review_status = 'pending'"
                ).fetchone()[0]

            self.assertEqual(manifest["feedback_state"]["learning_review_status"], "complete")
            self.assertEqual(feedback_entry["classification_status"], "applied")
            self.assertEqual(feedback_entry["learning_review_status"], "complete")
            self.assertEqual(pending_count, 0)

    def test_add_learning_mark_review_complete_ignores_non_feedback_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            workspace_project_dir.mkdir(parents=True)
            (workspace_project_dir / "project.json").write_text(
                json.dumps(minimal_manifest()),
                encoding="utf-8",
            )
            feedback_args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
                project_id="proj_door_left_lit",
                feedback="The first draft should be rawer.",
                feedback_id="fb_door_left_lit_test",
                source="artist",
                stage="project_completion",
                output_record_id=None,
                notes=None,
            )
            with redirect_stdout(StringIO()):
                artist_os_db.add_feedback(feedback_args)
            learning_args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
                project_id="proj_door_left_lit",
                learning_id="learn_schema_field_mismatch",
                learning_type="soft",
                learning_rule="Fill tool fields exactly when the tool reports schema names.",
                scope=None,
                evidence_type="tool_field_mismatch",
                evidence_ref=["tool_run_001"],
                evidence_summary="Tool field mismatch.",
                occurrence_count=1,
                promotion_reason=None,
                mark_review_complete=True,
                overwrite=False,
            )

            with redirect_stdout(StringIO()):
                artist_os_db.add_learning(learning_args)

            manifest = json.loads((workspace_project_dir / "project.json").read_text(encoding="utf-8"))
            feedback_entry = json.loads((workspace_project_dir / "feedback-log.jsonl").read_text(encoding="utf-8").strip())
            with closing(sqlite3.connect(library_root / "artist-os.sqlite")) as conn:
                pending_count = conn.execute(
                    "SELECT COUNT(*) FROM project_feedback_state WHERE learning_review_status = 'pending'"
                ).fetchone()[0]

            self.assertEqual(manifest["feedback_state"]["learning_review_status"], "pending")
            self.assertEqual(feedback_entry["classification_status"], "unclassified")
            self.assertEqual(feedback_entry["learning_review_status"], "pending")
            self.assertEqual(pending_count, 1)

    def test_mark_learning_review_complete_keeps_project_pending_when_log_has_pending_entries(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            workspace_project_dir.mkdir(parents=True)
            (workspace_project_dir / "project.json").write_text(
                json.dumps(minimal_manifest()),
                encoding="utf-8",
            )
            for feedback_id, feedback_text in [
                ("fb_door_left_lit_one", "First feedback."),
                ("fb_door_left_lit_two", "Second feedback."),
            ]:
                feedback_args = argparse.Namespace(
                    db=None,
                    library_root=str(library_root),
                    wondermint_root=None,
                    project_id="proj_door_left_lit",
                    feedback=feedback_text,
                    feedback_id=feedback_id,
                    source="artist",
                    stage="project_completion",
                    output_record_id=None,
                    notes=None,
                )
                with redirect_stdout(StringIO()):
                    artist_os_db.add_feedback(feedback_args)
            review_args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
                project_id="proj_door_left_lit",
                feedback_id=["fb_door_left_lit_one"],
                classification_status="applied",
            )

            with redirect_stdout(StringIO()):
                artist_os_db.mark_learning_review_complete(review_args)

            manifest = json.loads((workspace_project_dir / "project.json").read_text(encoding="utf-8"))
            entries = [
                json.loads(line)
                for line in (workspace_project_dir / "feedback-log.jsonl").read_text(encoding="utf-8").splitlines()
            ]
            with closing(sqlite3.connect(library_root / "artist-os.sqlite")) as conn:
                pending_count = conn.execute(
                    "SELECT COUNT(*) FROM project_feedback_state WHERE learning_review_status = 'pending'"
                ).fetchone()[0]

            self.assertEqual(manifest["feedback_state"]["learning_review_status"], "pending")
            self.assertEqual(entries[0]["learning_review_status"], "complete")
            self.assertEqual(entries[1]["learning_review_status"], "pending")
            self.assertEqual(pending_count, 1)

    def test_add_performance_signal_writes_equal_weight_signal_and_indexes_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            workspace_project_dir.mkdir(parents=True)
            (workspace_project_dir / "project.json").write_text(
                json.dumps(minimal_manifest()),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
                project_id="proj_door_left_lit",
                signal_id="perf_symbology_board_001",
                metric_name="save_rate",
                metric_value="0.32",
                signal_direction="positive",
                source="manual_import",
                output_record_id=None,
                notes=None,
                overwrite=False,
            )

            with redirect_stdout(StringIO()):
                artist_os_db.add_performance_signal(args)

            signal_path = library_root / "personal-library" / "performance-signals" / "perf_symbology_board_001.json"
            record = json.loads(signal_path.read_text(encoding="utf-8"))
            manifest = json.loads((workspace_project_dir / "project.json").read_text(encoding="utf-8"))

            self.assertEqual(record["metric_value"], 0.32)
            self.assertEqual(record["evidence_weight"], "equal_to_artist_feedback")
            self.assertEqual(
                manifest["feedback_state"]["performance_signal_refs"][0]["path"],
                "personal-library/performance-signals/perf_symbology_board_001.json",
            )
            with closing(sqlite3.connect(library_root / "artist-os.sqlite")) as conn:
                signal_ref = conn.execute(
                    "SELECT signal_id, status FROM performance_signal_refs"
                ).fetchone()
            self.assertEqual(signal_ref, ("perf_symbology_board_001", "active"))

    def test_add_performance_signal_validates_id_and_refuses_existing_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            signal_dir = library_root / "personal-library" / "performance-signals"
            workspace_project_dir.mkdir(parents=True)
            signal_dir.mkdir(parents=True)
            (workspace_project_dir / "project.json").write_text(
                json.dumps(minimal_manifest()),
                encoding="utf-8",
            )
            (signal_dir / "perf_existing.json").write_text("{}", encoding="utf-8")
            args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
                project_id="proj_door_left_lit",
                signal_id="perf_existing",
                metric_name="save_rate",
                metric_value="0.32",
                signal_direction="positive",
                source="manual_import",
                output_record_id=None,
                notes=None,
                overwrite=False,
            )

            with self.assertRaisesRegex(SystemExit, "record already exists"):
                artist_os_db.add_performance_signal(args)

            args.signal_id = "../escape"
            with self.assertRaisesRegex(SystemExit, "signal_id must match"):
                artist_os_db.add_performance_signal(args)

    def test_add_performance_signal_validates_optional_output_record_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            workspace_project_dir.mkdir(parents=True)
            (workspace_project_dir / "project.json").write_text(
                json.dumps(minimal_manifest()),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
                project_id="proj_door_left_lit",
                signal_id="perf_symbology_board_001",
                metric_name="save_rate",
                metric_value="0.32",
                signal_direction="positive",
                source="manual_import",
                output_record_id="bad_output_id",
                notes=None,
                overwrite=False,
            )

            with self.assertRaisesRegex(SystemExit, "output_record_id must match"):
                artist_os_db.add_performance_signal(args)

    def test_auto_feedback_ids_include_microseconds_to_avoid_same_second_collision(self) -> None:
        first = artist_os_db.compact_timestamp("2026-06-20T12:00:00.123456+00:00")
        second = artist_os_db.compact_timestamp("2026-06-20T12:00:00.654321+00:00")

        self.assertNotEqual(first, second)
        self.assertEqual(len(first), 20)

    def test_list_and_show_commands_accept_library_root_routing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            workspace_project_dir.mkdir(parents=True)
            (workspace_project_dir / "project.json").write_text(
                json.dumps(minimal_manifest()),
                encoding="utf-8",
            )
            sync_args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
            )
            with redirect_stdout(StringIO()):
                artist_os_db.sync_db(sync_args)

            list_args = artist_os_db.parser().parse_args([
                "list",
                "--library-root",
                str(library_root),
            ])
            show_args = artist_os_db.parser().parse_args([
                "show",
                "proj_door_left_lit",
                "--library-root",
                str(library_root),
            ])

            list_output = StringIO()
            show_output = StringIO()
            with redirect_stdout(list_output):
                list_args.func(list_args)
            with redirect_stdout(show_output):
                show_args.func(show_args)

            self.assertIn("proj_door_left_lit", list_output.getvalue())
            self.assertEqual(
                json.loads(show_output.getvalue())["project"]["project_id"],
                "proj_door_left_lit",
            )

    def _load_schema(self, schema_name: str) -> dict:
        return json.loads(
            (REPO_ROOT / "schemas" / schema_name).read_text(encoding="utf-8")
        )

    def test_add_feedback_persists_record_that_revalidates_against_schema(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            workspace_project_dir.mkdir(parents=True)
            (workspace_project_dir / "project.json").write_text(
                json.dumps(minimal_manifest()),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
                project_id="proj_door_left_lit",
                feedback="The first draft should be rawer.",
                feedback_id="fb_door_left_lit_test",
                source="artist",
                stage="project_completion",
                output_record_id=None,
                notes=None,
            )

            with redirect_stdout(StringIO()):
                artist_os_db.add_feedback(args)

            feedback_log = workspace_project_dir / "feedback-log.jsonl"
            self.assertTrue(feedback_log.is_file())
            entry = json.loads(feedback_log.read_text(encoding="utf-8").strip())
            schema = self._load_schema("project-feedback-log-entry.schema.json")
            validate(entry, schema, schema)

    def test_add_learning_persists_record_that_revalidates_against_schema(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            workspace_project_dir.mkdir(parents=True)
            (workspace_project_dir / "project.json").write_text(
                json.dumps(minimal_manifest()),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
                project_id="proj_door_left_lit",
                learning_id="learn_rawer_first_drafts",
                learning_type="soft",
                learning_rule="Keep first drafts rawer before polishing.",
                scope=None,
                evidence_type="feedback_entry",
                evidence_ref=["fb_door_left_lit_test"],
                evidence_summary="Artist requested rawer first drafts.",
                occurrence_count=1,
                promotion_reason=None,
                mark_review_complete=False,
                overwrite=False,
            )

            with redirect_stdout(StringIO()):
                artist_os_db.add_learning(args)

            learning_path = (
                library_root
                / "personal-library"
                / "learnings"
                / "learn_rawer_first_drafts.json"
            )
            self.assertTrue(learning_path.is_file())
            record = json.loads(learning_path.read_text(encoding="utf-8"))
            schema = self._load_schema("learning-record.schema.json")
            validate(record, schema, schema)

    def test_add_performance_signal_persists_record_that_revalidates_against_schema(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            workspace_project_dir.mkdir(parents=True)
            (workspace_project_dir / "project.json").write_text(
                json.dumps(minimal_manifest()),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
                project_id="proj_door_left_lit",
                signal_id="perf_symbology_board_001",
                metric_name="save_rate",
                metric_value="0.32",
                signal_direction="positive",
                source="manual_import",
                output_record_id=None,
                notes=None,
                overwrite=False,
            )

            with redirect_stdout(StringIO()):
                artist_os_db.add_performance_signal(args)

            signal_path = (
                library_root
                / "personal-library"
                / "performance-signals"
                / "perf_symbology_board_001.json"
            )
            self.assertTrue(signal_path.is_file())
            record = json.loads(signal_path.read_text(encoding="utf-8"))
            schema = self._load_schema("performance-signal.schema.json")
            validate(record, schema, schema)

    def test_add_feedback_rejects_invalid_record_without_writing(self) -> None:
        # An empty --feedback passes argparse (required, but no content check) yet
        # violates the schema's minLength:1. Write-time validation must block the
        # write end to end: no feedback-log file is created and the manifest is
        # left byte-for-byte untouched (validation precedes the append, the
        # manifest update, and sync).
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            workspace_project_dir.mkdir(parents=True)
            manifest_path = workspace_project_dir / "project.json"
            manifest_path.write_text(
                json.dumps(minimal_manifest()),
                encoding="utf-8",
            )
            manifest_before = manifest_path.read_text(encoding="utf-8")
            args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
                project_id="proj_door_left_lit",
                feedback="",
                feedback_id="fb_door_left_lit_test",
                source="artist",
                stage="project_completion",
                output_record_id=None,
                notes=None,
            )

            with redirect_stdout(StringIO()):
                with self.assertRaisesRegex(
                    SystemExit,
                    "refusing to write malformed project-feedback-log-entry.schema.json",
                ):
                    artist_os_db.add_feedback(args)

            self.assertFalse((workspace_project_dir / "feedback-log.jsonl").exists())
            self.assertEqual(
                manifest_path.read_text(encoding="utf-8"), manifest_before
            )

    def test_add_learning_rejects_invalid_record_without_writing(self) -> None:
        # --occurrence-count 0 passes argparse (type=int, no range) but violates
        # the schema's promotion_state.occurrence_count minimum:1. Validation must
        # block the write_text path: no learning record file is created.
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            workspace_project_dir = library_root / "projects" / "proj_door_left_lit"
            workspace_project_dir.mkdir(parents=True)
            (workspace_project_dir / "project.json").write_text(
                json.dumps(minimal_manifest()),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                db=None,
                library_root=str(library_root),
                wondermint_root=None,
                project_id="proj_door_left_lit",
                learning_id="learn_rawer_first_drafts",
                learning_type="soft",
                learning_rule="Keep first drafts rawer before polishing.",
                scope=None,
                evidence_type="feedback_entry",
                evidence_ref=["fb_door_left_lit_test"],
                evidence_summary="Artist requested rawer first drafts.",
                occurrence_count=0,
                promotion_reason=None,
                mark_review_complete=False,
                overwrite=False,
            )

            with redirect_stdout(StringIO()):
                with self.assertRaisesRegex(
                    SystemExit,
                    "refusing to write malformed learning-record.schema.json",
                ):
                    artist_os_db.add_learning(args)

            learning_path = (
                library_root
                / "personal-library"
                / "learnings"
                / "learn_rawer_first_drafts.json"
            )
            self.assertFalse(learning_path.exists())

    def test_validate_record_accepts_valid_record(self) -> None:
        record = {
            "feedback_id": "fb_door_left_lit_test",
            "project_id": "proj_door_left_lit",
            "received_at": "2026-05-31T00:00:00Z",
            "source": "artist",
            "stage": None,
            "output_record_id": None,
            "feedback_text": "The first draft should be rawer.",
            "classification_status": "unclassified",
            "learning_review_status": "pending",
            "notes": None,
        }

        self.assertIsNone(
            artist_os_db.validate_record(record, "project-feedback-log-entry.schema.json")
        )

    def test_validate_record_rejects_missing_required_field(self) -> None:
        record = {
            "feedback_id": "fb_door_left_lit_test",
            "project_id": "proj_door_left_lit",
            "received_at": "2026-05-31T00:00:00Z",
            "source": "artist",
            "feedback_text": "The first draft should be rawer.",
            "classification_status": "unclassified",
            # learning_review_status is required and intentionally omitted
        }

        with self.assertRaisesRegex(
            SystemExit,
            "refusing to write malformed project-feedback-log-entry.schema.json",
        ):
            artist_os_db.validate_record(record, "project-feedback-log-entry.schema.json")

    def test_validate_record_rejects_wrong_typed_field(self) -> None:
        record = {
            "learning_id": "learn_rawer_first_drafts",
            "learning_type": "not_a_valid_enum_value",
            "status": "active",
            "learning_rule": "Keep first drafts rawer before polishing.",
            "scope": None,
            "source_project_ids": ["proj_door_left_lit"],
            "evidence_refs": [
                {
                    "evidence_type": "feedback_entry",
                    "ref": "fb_door_left_lit_test",
                    "summary": "Recorded as learning evidence.",
                }
            ],
            "promotion_state": {
                "occurrence_count": 1,
                "promotion_reason": None,
            },
            "created_at": "2026-05-31T00:00:00Z",
            "updated_at": "2026-05-31T00:00:00Z",
        }

        with self.assertRaisesRegex(
            SystemExit,
            "refusing to write malformed learning-record.schema.json",
        ):
            artist_os_db.validate_record(record, "learning-record.schema.json")

    def test_validate_record_rejects_extra_field_under_additional_properties_false(self) -> None:
        record = {
            "signal_id": "perf_symbology_board_001",
            "project_id": "proj_door_left_lit",
            "output_record_id": None,
            "captured_at": "2026-05-31T00:00:00Z",
            "source": "manual_import",
            "metric_name": "save_rate",
            "metric_value": 0.32,
            "signal_direction": "positive",
            "evidence_weight": "equal_to_artist_feedback",
            "notes": None,
            "unexpected_field": "should be rejected",
        }

        with self.assertRaisesRegex(
            SystemExit,
            "refusing to write malformed performance-signal.schema.json",
        ):
            artist_os_db.validate_record(record, "performance-signal.schema.json")

    def test_init_command_accepts_library_root_routing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            args = artist_os_db.parser().parse_args([
                "init",
                "--library-root",
                str(library_root),
            ])

            with redirect_stdout(StringIO()):
                args.func(args)

            self.assertTrue((library_root / "artist-os.sqlite").is_file())


class LearningsLoopTests(unittest.TestCase):
    """The feedback -> review -> complete state machine, the pending listing
    (previously untested), and the learnings-report close-out command."""

    def _seed_project(self, library_root: Path) -> dict:
        proj_dir = library_root / "projects" / "proj_door_left_lit"
        proj_dir.mkdir(parents=True)
        (proj_dir / "project.json").write_text(json.dumps(minimal_manifest()), encoding="utf-8")
        return {"db": None, "library_root": str(library_root), "wondermint_root": None}

    def _capture(self, func, args) -> str:
        buf = StringIO()
        with redirect_stdout(buf):
            func(args)
        return buf.getvalue()

    def test_loop_pending_then_complete_through_report_and_listing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            base = self._seed_project(library_root)

            fb_args = argparse.Namespace(
                **base,
                project_id="proj_door_left_lit",
                feedback="The first draft should be rawer.",
                feedback_id="fb_rawer_draft",
                source="artist",
                stage="project_completion",
                output_record_id=None,
                notes=None,
            )
            with redirect_stdout(StringIO()):
                artist_os_db.add_feedback(fb_args)

            report_args = argparse.Namespace(**base, project_id="proj_door_left_lit")
            pending_report = self._capture(artist_os_db.learnings_report, report_args)
            self.assertIn("proj_door_left_lit", pending_report)
            # Assert the per-project state line, not a bare word a footer could satisfy.
            self.assertIn("review=pending", pending_report)

            pending_list = self._capture(
                artist_os_db.pending_learning_reviews, argparse.Namespace(**base)
            )
            self.assertIn("proj_door_left_lit", pending_list)

            learn_args = argparse.Namespace(
                **base,
                project_id="proj_door_left_lit",
                learning_id="learn_rawer",
                learning_type="soft",
                learning_rule="Prefer rawer, less-polished first drafts for this artist.",
                scope=None,
                evidence_type="feedback_entry",
                evidence_ref=["fb_rawer_draft"],
                evidence_summary=None,
                occurrence_count=1,
                promotion_reason=None,
                mark_review_complete=True,
                overwrite=False,
            )
            with redirect_stdout(StringIO()):
                artist_os_db.add_learning(learn_args)

            done_report = self._capture(artist_os_db.learnings_report, report_args)
            self.assertIn("review=complete", done_report)  # per-project header, not the footer
            self.assertNotIn("review=pending", done_report)
            self.assertIn("learn_rawer", done_report)

            done_list = self._capture(
                artist_os_db.pending_learning_reviews, argparse.Namespace(**base)
            )
            self.assertNotIn("proj_door_left_lit", done_list)

    def test_learnings_report_honors_requested_project_id(self) -> None:
        # Index a real project, then confirm the WHERE clause distinguishes a known
        # id (succeeds) from an unknown one (SystemExit) — not just "empty DB raises".
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            base = self._seed_project(library_root)
            with redirect_stdout(StringIO()):
                artist_os_db.sync_db(argparse.Namespace(**base))

            known = self._capture(
                artist_os_db.learnings_report, argparse.Namespace(**base, project_id="proj_door_left_lit")
            )
            self.assertIn("proj_door_left_lit", known)

            with self.assertRaises(SystemExit):
                with redirect_stdout(StringIO()):
                    artist_os_db.learnings_report(argparse.Namespace(**base, project_id="proj_does_not_exist"))

    def test_report_does_not_label_never_reviewed_project_complete(self) -> None:
        # A synced project with no feedback is review=none; the footer must count it
        # as "with no feedback yet", never "complete" (assert the real footer text so
        # the bucket can't silently regress to the complete count).
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            base = self._seed_project(library_root)
            with redirect_stdout(StringIO()):
                artist_os_db.sync_db(argparse.Namespace(**base))
            report = self._capture(artist_os_db.learnings_report, argparse.Namespace(**base, project_id=None))
            self.assertIn("review=none", report)
            self.assertIn("with no feedback yet", report)
            self.assertNotIn("complete", report)

    def test_report_labels_not_applicable_distinctly(self) -> None:
        # A 'not_applicable' review (a valid schema enum) must show as such, not be
        # miscounted as "with no feedback yet".
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            base = self._seed_project(library_root)
            proj_json = library_root / "projects" / "proj_door_left_lit" / "project.json"
            manifest = json.loads(proj_json.read_text(encoding="utf-8"))
            manifest["feedback_state"] = {
                "feedback_log_path": "projects/proj_door_left_lit/feedback-log.jsonl",
                "learning_review_status": "not_applicable",
                "learning_reviewed_at": None,
            }
            proj_json.write_text(json.dumps(manifest), encoding="utf-8")
            with redirect_stdout(StringIO()):
                artist_os_db.sync_db(argparse.Namespace(**base))
            report = self._capture(artist_os_db.learnings_report, argparse.Namespace(**base, project_id=None))
            self.assertIn("review=not_applicable", report)
            self.assertIn("not applicable", report)
            self.assertNotIn("with no feedback yet", report)


if __name__ == "__main__":
    unittest.main()
