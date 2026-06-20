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


if __name__ == "__main__":
    unittest.main()
