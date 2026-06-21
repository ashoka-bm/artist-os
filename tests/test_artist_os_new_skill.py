"""Guard: bin/artist-os-new-skill creates a new skill AND registers it in the
four sites test_skill_set_sync requires, so adding a skill is one command instead
of four hand-edits that are easy to half-finish.

Each test drives the real CLI against a minimal throwaway repo (ARTIST_OS_ROOT),
then asserts the on-disk result — the public-interface behavior, not internals.
"""
from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
NEW_SKILL = REPO / "bin" / "artist-os-new-skill"

_LOADER = importlib.machinery.SourceFileLoader("artist_os_lint", str(REPO / "bin" / "artist-os-lint"))
_SPEC = importlib.util.spec_from_loader("artist_os_lint", _LOADER)
linter = importlib.util.module_from_spec(_SPEC)
_LOADER.exec_module(linter)


def make_repo(tmp: str) -> Path:
    """A minimal bundle with the four registration sites the scaffold edits."""
    root = Path(tmp)
    (root / "THEORY.md").write_text("# Theory\n", encoding="utf-8")
    (root / "schemas").mkdir()
    (root / "docs").mkdir()
    skills = root / "skills"
    skills.mkdir()

    cond = skills / "artist-os"
    cond.mkdir()
    (cond / "SKILL.md").write_text(
        "---\nname: artist-os\ndescription: The conductor.\n---\n\n"
        "# Artist OS\n\n"
        "Paths resolve from `$ARTIST_OS_ROOT`.\n\n"
        "Delegate each phase's detailed checklist to the sibling skill that owns it: "
        "`skills/alpha`, `skills/beta`, and `skills/zeta`.\n",
        encoding="utf-8",
    )
    for sibling in ("alpha", "beta"):
        d = skills / sibling
        d.mkdir()
        (d / "SKILL.md").write_text(
            f"---\nname: artist-os-{sibling}\ndescription: A sibling.\n---\n\n# {sibling}\n",
            encoding="utf-8",
        )

    bin_dir = root / "bin"
    bin_dir.mkdir()
    (bin_dir / "install-codex-dev-skills").write_text(
        '#!/usr/bin/env bash\nset -euo pipefail\nskills=(\n  "alpha"\n  "beta"\n)\n',
        encoding="utf-8",
    )

    evals = root / "evals" / "routing"
    evals.mkdir(parents=True)
    (evals / "routing-evals.json").write_text(
        json.dumps({"skills": ["artist-os", "alpha", "beta", "none"], "evals": []}, indent=2) + "\n",
        encoding="utf-8",
    )
    return root


def run_scaffold(root: Path, *args: str) -> subprocess.CompletedProcess:
    env = {**os.environ, "ARTIST_OS_ROOT": str(root)}
    return subprocess.run([sys.executable, str(NEW_SKILL), *args], capture_output=True, text=True, env=env)


def registration_files(root: Path) -> dict[str, str]:
    """The three sync-site files, for before/after byte comparison."""
    return {
        "installer": (root / "bin" / "install-codex-dev-skills").read_text(encoding="utf-8"),
        "conductor": (root / "skills" / "artist-os" / "SKILL.md").read_text(encoding="utf-8"),
        "routing": (root / "evals" / "routing" / "routing-evals.json").read_text(encoding="utf-8"),
    }


def delegation_line(conductor_text: str) -> str:
    return next(l for l in conductor_text.splitlines() if "Delegate each phase" in l)


class CreateTests(unittest.TestCase):
    def test_creates_lint_clean_skill_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            proc = run_scaffold(root, "gamma")
            self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
            md = root / "skills" / "gamma" / "SKILL.md"
            self.assertTrue(md.exists(), "scaffold should create skills/gamma/SKILL.md")
            self.assertEqual(linter.lint_skill(md, root), [], "scaffolded skill must lint clean")
            self.assertIn(
                "$ARTIST_OS_ROOT", md.read_text(encoding="utf-8"),
                "the template must ship the anchor sentence so the lint-clean check is contingent on it",
            )

    def test_prints_authoring_todos(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            proc = run_scaffold(root, "gamma")
            self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
            for token in ("description", "phase order", "eval case"):
                self.assertIn(token, proc.stdout, f"expected the TODO list to mention {token!r}")


class InstallerRegistrationTests(unittest.TestCase):
    def test_registers_in_installer_array(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            self.assertEqual(run_scaffold(root, "gamma").returncode, 0)
            text = (root / "bin" / "install-codex-dev-skills").read_text(encoding="utf-8")
            match = re.search(r"skills=\((.*?)\)", text, re.DOTALL)
            self.assertIsNotNone(match)
            self.assertIn("gamma", re.findall(r'"([a-z0-9-]+)"', match.group(1)))


class ConductorRegistrationTests(unittest.TestCase):
    def test_registers_in_conductor_delegation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            self.assertEqual(run_scaffold(root, "gamma").returncode, 0)
            text = (root / "skills" / "artist-os" / "SKILL.md").read_text(encoding="utf-8")
            # Found by the same skills/<name> scan test_skill_set_sync uses...
            self.assertIn("gamma", re.findall(r"skills/([a-z0-9-]+)", text))
            # ...and inserted grammatically into the Oxford-comma delegation list:
            # exactly one " and ", as the trailing "A, and B" becomes "A, B, and C".
            line = delegation_line(text)
            self.assertTrue(line.endswith("and `skills/gamma`."), line)
            self.assertEqual(line.count(" and "), 1, f"delegation list must keep one Oxford 'and': {line}")

    def test_aborts_and_writes_nothing_when_delegation_phrasing_changed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            cond = root / "skills" / "artist-os" / "SKILL.md"
            cond.write_text(
                "---\nname: artist-os\ndescription: c.\n---\n\n# Artist OS\n\n"
                "Paths resolve from `$ARTIST_OS_ROOT`.\n\n"
                "Delegate each phase's detailed checklist to these skills in a totally new shape.\n",
                encoding="utf-8",
            )
            installer_before = (root / "bin" / "install-codex-dev-skills").read_text(encoding="utf-8")
            proc = run_scaffold(root, "gamma")
            self.assertNotEqual(proc.returncode, 0, "should fail when the delegation anchor is gone")
            self.assertFalse((root / "skills" / "gamma").exists(), "no skill dir on a pre-flight abort")
            self.assertEqual(
                (root / "bin" / "install-codex-dev-skills").read_text(encoding="utf-8"),
                installer_before,
                "installer must be untouched on a pre-flight abort",
            )


class RoutingRegistrationTests(unittest.TestCase):
    def test_registers_in_routing_skills_array(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            self.assertEqual(run_scaffold(root, "gamma").returncode, 0)
            data = json.loads((root / "evals" / "routing" / "routing-evals.json").read_text(encoding="utf-8"))
            self.assertIn("gamma", data["skills"])
            self.assertEqual(data["skills"][-1], "none", "the 'none' sentinel must stay last")


class FourWaySyncTests(unittest.TestCase):
    def test_new_skill_lands_in_all_four_sites(self) -> None:
        # The scaffold's whole reason to exist: one command keeps the four sync
        # sites test_skill_set_sync enforces from drifting apart.
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            self.assertEqual(run_scaffold(root, "gamma").returncode, 0)
            installer = (root / "bin" / "install-codex-dev-skills").read_text(encoding="utf-8")
            conductor = (root / "skills" / "artist-os" / "SKILL.md").read_text(encoding="utf-8")
            routing = json.loads((root / "evals" / "routing" / "routing-evals.json").read_text(encoding="utf-8"))
            self.assertTrue((root / "skills" / "gamma" / "SKILL.md").exists())  # on disk
            self.assertIn("gamma", re.findall(r"skills=\((.*?)\)", installer, re.DOTALL)[0])  # installer
            self.assertIn("gamma", re.findall(r"skills/([a-z0-9-]+)", conductor))  # conductor
            self.assertIn("gamma", routing["skills"])  # routing eval


class ValidationTests(unittest.TestCase):
    def test_rejects_invalid_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            proc = run_scaffold(root, "Gamma Skill")
            self.assertNotEqual(proc.returncode, 0)
            self.assertFalse((root / "skills" / "Gamma Skill").exists())

    def test_rejects_duplicate_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            before = registration_files(root)
            proc = run_scaffold(root, "alpha")  # already exists in the fixture
            self.assertNotEqual(proc.returncode, 0)
            self.assertNotIn("Traceback", proc.stderr, "duplicate must fail with a clean message")
            self.assertIn("A sibling.", (root / "skills" / "alpha" / "SKILL.md").read_text(encoding="utf-8"))
            self.assertEqual(registration_files(root), before, "no registration site may change on a rejected dup")


class ReservedNameTests(unittest.TestCase):
    def test_rejects_reserved_sentinel_names(self) -> None:
        # 'none' is the routing sentinel and 'artist-os' is the conductor; neither
        # may be scaffolded, and a rejection must change nothing.
        for reserved in ("none", "artist-os"):
            with tempfile.TemporaryDirectory() as tmp:
                root = make_repo(tmp)
                before = registration_files(root)
                proc = run_scaffold(root, reserved)
                self.assertNotEqual(proc.returncode, 0, f"{reserved!r} must be rejected")
                # Assert the rejection comes from the RESERVED guard specifically —
                # not an unrelated fixture guard (dir-exists / routing-drift) that
                # would also satisfy a bare returncode check.
                self.assertIn("reserved", proc.stderr.lower(), f"{reserved!r} must hit the reserved guard: {proc.stderr}")
                self.assertNotIn("Traceback", proc.stderr)
                self.assertEqual(registration_files(root), before, f"{reserved!r} rejection must write nothing")


class DriftRegistrationTests(unittest.TestCase):
    def test_aborts_when_name_already_in_routing(self) -> None:
        # If routing skills[] already lists a name with no skill dir (the drift
        # state the sync test catches), scaffolding it must NOT double-insert.
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            routing_path = root / "evals" / "routing" / "routing-evals.json"
            data = json.loads(routing_path.read_text(encoding="utf-8"))
            data["skills"].insert(-1, "drifted")  # before 'none', no skills/drifted dir
            routing_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            before = registration_files(root)
            proc = run_scaffold(root, "drifted")
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("routing", proc.stderr)
            self.assertNotIn("Traceback", proc.stderr)
            after = json.loads(routing_path.read_text(encoding="utf-8"))
            self.assertEqual(after["skills"].count("drifted"), 1, "must not double-insert into routing skills[]")
            self.assertEqual(registration_files(root), before, "drift abort must write nothing")

    def test_aborts_when_name_already_in_installer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            installer = root / "bin" / "install-codex-dev-skills"
            installer.write_text(installer.read_text(encoding="utf-8").replace('  "beta"\n', '  "beta"\n  "drift2"\n'), encoding="utf-8")
            before = registration_files(root)
            proc = run_scaffold(root, "drift2")
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("installer", proc.stderr)
            self.assertEqual(registration_files(root), before, "installer drift abort must write nothing")

    def test_aborts_when_name_already_in_conductor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            cond = root / "skills" / "artist-os" / "SKILL.md"
            cond.write_text(
                cond.read_text(encoding="utf-8").replace("and `skills/zeta`.", "`skills/zeta`, and `skills/drift3`."),
                encoding="utf-8",
            )
            before = registration_files(root)
            proc = run_scaffold(root, "drift3")
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("conductor", proc.stderr)
            self.assertEqual(registration_files(root), before, "conductor drift abort must write nothing")


class CleanErrorTests(unittest.TestCase):
    def test_unreadable_registration_file_fails_cleanly(self) -> None:
        # A present-but-unreadable registration file must surface as a clean FAIL
        # during pre-flight, never a raw traceback, and write nothing.
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            installer = root / "bin" / "install-codex-dev-skills"
            before = registration_files(root)
            installer.chmod(0o000)
            try:
                proc = run_scaffold(root, "gamma")
            finally:
                installer.chmod(0o644)
            self.assertNotEqual(proc.returncode, 0)
            self.assertNotIn("Traceback", proc.stderr, "an unreadable site must fail cleanly")
            self.assertIn("FAIL", proc.stderr)
            self.assertFalse((root / "skills" / "gamma").exists())
            self.assertEqual(registration_files(root), before)

    def test_installer_membership_ignores_commented_entries(self) -> None:
        # A commented-out token in the installer array must not be read as a real
        # member and block a genuinely-new name.
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            installer = root / "bin" / "install-codex-dev-skills"
            installer.write_text(
                installer.read_text(encoding="utf-8").replace('  "beta"\n', '  "beta"\n  # "gamma" was removed earlier\n'),
                encoding="utf-8",
            )
            proc = run_scaffold(root, "gamma")
            self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
            array = re.findall(r"skills=\((.*?)\)", installer.read_text(encoding="utf-8"), re.DOTALL)[0]
            self.assertIn("gamma", re.findall(r'"([a-z0-9-]+)"', array))


class ExistingDirTests(unittest.TestCase):
    def test_rejects_existing_unregistered_skill_dir(self) -> None:
        # A skill dir present on disk but not registered must be rejected cleanly,
        # and its hand-written content must never be deleted by the rollback path.
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            orphan = root / "skills" / "orphan"
            orphan.mkdir()
            (orphan / "SKILL.md").write_text(
                "---\nname: artist-os-orphan\ndescription: hand-written.\n---\n\nKEEP THIS CONTENT\n",
                encoding="utf-8",
            )
            before = registration_files(root)
            proc = run_scaffold(root, "orphan")
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("already exists", proc.stderr)
            self.assertNotIn("Traceback", proc.stderr)
            self.assertIn("KEEP THIS CONTENT", (orphan / "SKILL.md").read_text(encoding="utf-8"))
            self.assertEqual(registration_files(root), before)


class AtomicCommitTests(unittest.TestCase):
    def test_rolls_back_when_a_registration_write_fails(self) -> None:
        # Make the last registration target unwritable: the scaffold must roll the
        # earlier writes back, remove the new skill dir, and fail cleanly.
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            routing_path = root / "evals" / "routing" / "routing-evals.json"
            before = registration_files(root)
            routing_path.chmod(0o444)
            try:
                proc = run_scaffold(root, "gamma")
            finally:
                routing_path.chmod(0o644)
            self.assertNotEqual(proc.returncode, 0)
            self.assertNotIn("Traceback", proc.stderr, "a write failure must surface as a clean FAIL")
            self.assertFalse((root / "skills" / "gamma").exists(), "skill dir must be rolled back")
            self.assertEqual(registration_files(root), before, "all registration sites must be rolled back")


if __name__ == "__main__":
    unittest.main()
