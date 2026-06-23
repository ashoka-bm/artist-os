"""Guard: bin/artist-os-new-skill scaffolds internal Artist OS mode files.

The command name is kept for compatibility, but the architecture now exposes
only one public skill: `skills/artist-os/SKILL.md`. New specialized behavior is
added as `skills/artist-os/references/<mode>.md` and wired into the conductor by
hand when appropriate.
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
NEW_SKILL = REPO / "bin" / "artist-os-new-skill"


def make_repo(tmp: str) -> Path:
    """A minimal bundle with the single public conductor and references dir."""
    root = Path(tmp)
    (root / "THEORY.md").write_text("# Theory\n", encoding="utf-8")
    (root / "schemas").mkdir()
    (root / "docs").mkdir()
    conductor = root / "skills" / "artist-os"
    (conductor / "references").mkdir(parents=True)
    (conductor / "SKILL.md").write_text(
        "---\n"
        "name: artist-os\n"
        "description: The single public conductor.\n"
        "---\n\n"
        "# Artist OS\n\n"
        "Internal mode map:\n\n"
        "- Existing mode: `skills/artist-os/references/existing.md`.\n",
        encoding="utf-8",
    )
    (conductor / "references" / "existing.md").write_text("# Existing\n", encoding="utf-8")
    return root


def run_scaffold(root: Path, *args: str) -> subprocess.CompletedProcess:
    env = {**os.environ, "ARTIST_OS_ROOT": str(root)}
    return subprocess.run([sys.executable, str(NEW_SKILL), *args], capture_output=True, text=True, env=env)


class CreateTests(unittest.TestCase):
    def test_creates_internal_mode_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            proc = run_scaffold(root, "gamma-mode")
            self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
            md = root / "skills" / "artist-os" / "references" / "gamma-mode.md"
            self.assertTrue(md.exists(), "scaffold should create an internal mode file")
            text = md.read_text(encoding="utf-8")
            self.assertIn("# Gamma Mode", text)
            self.assertIn("$ARTIST_OS_ROOT", text)
            self.assertIn("Mode Contract", text)
            self.assertFalse((root / "skills" / "gamma-mode").exists(), "must not create a public skill dir")

    def test_does_not_edit_public_conductor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            conductor = root / "skills" / "artist-os" / "SKILL.md"
            before = conductor.read_text(encoding="utf-8")
            proc = run_scaffold(root, "gamma")
            self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
            self.assertEqual(conductor.read_text(encoding="utf-8"), before)
            self.assertIn("not registered as a public skill", proc.stdout)

    def test_prints_authoring_todos(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            proc = run_scaffold(root, "gamma")
            self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
            for token in ("Internal mode map", "phase order", "contract tests"):
                self.assertIn(token, proc.stdout, f"expected TODO list to mention {token!r}")


class ValidationTests(unittest.TestCase):
    def test_rejects_invalid_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            proc = run_scaffold(root, "Gamma Skill")
            self.assertNotEqual(proc.returncode, 0)
            self.assertFalse((root / "skills" / "artist-os" / "references" / "Gamma Skill.md").exists())

    def test_rejects_reserved_names(self) -> None:
        for reserved in ("none", "artist-os", "references"):
            with tempfile.TemporaryDirectory() as tmp:
                root = make_repo(tmp)
                proc = run_scaffold(root, reserved)
                self.assertNotEqual(proc.returncode, 0, f"{reserved!r} must be rejected")
                self.assertIn("reserved", proc.stderr.lower())
                self.assertNotIn("Traceback", proc.stderr)

    def test_rejects_existing_internal_mode_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            existing = root / "skills" / "artist-os" / "references" / "existing.md"
            before = existing.read_text(encoding="utf-8")
            proc = run_scaffold(root, "existing")
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("already exists", proc.stderr)
            self.assertEqual(existing.read_text(encoding="utf-8"), before)

    def test_rejects_existing_public_skill_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            public = root / "skills" / "orphan"
            public.mkdir()
            (public / "SKILL.md").write_text(
                "---\nname: artist-os-orphan\ndescription: hand-written.\n---\n\nKEEP THIS CONTENT\n",
                encoding="utf-8",
            )
            proc = run_scaffold(root, "orphan")
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("public skill directory", proc.stderr)
            self.assertIn("KEEP THIS CONTENT", (public / "SKILL.md").read_text(encoding="utf-8"))


class CleanErrorTests(unittest.TestCase):
    def test_missing_conductor_fails_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            (root / "skills" / "artist-os" / "SKILL.md").unlink()
            proc = run_scaffold(root, "gamma")
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("skills/artist-os/SKILL.md", proc.stderr)
            self.assertNotIn("Traceback", proc.stderr)
            self.assertFalse((root / "skills" / "artist-os" / "references" / "gamma.md").exists())


if __name__ == "__main__":
    unittest.main()
