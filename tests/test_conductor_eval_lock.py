"""Guard: the committed conductor digest (evals/conductor-behavior/blessed.lock)
matches the live conductor, so editing skills/artist-os/SKILL.md without re-running
and re-blessing the (manual, token-spending) conductor-behavior eval fails loudly.

This is the CI-able half of the eval-regression gate: the eval RUN cannot be in CI
(it calls `claude -p`), but "the conductor changed since the last blessed run" is a
pure digest check — the same drift-guard shape as test_phase_order_doc_drift and
test_version_changelog_consistency.
"""
from __future__ import annotations

import importlib.machinery
import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EVAL = REPO / "bin" / "artist-os-eval"

_LOADER = importlib.machinery.SourceFileLoader("artist_os_eval", str(EVAL))
_SPEC = importlib.util.spec_from_loader("artist_os_eval", _LOADER)
ev = importlib.util.module_from_spec(_SPEC)
_LOADER.exec_module(ev)


def make_bundle(tmp: str, conductor: str = "conductor body v1\n") -> Path:
    root = Path(tmp)
    (root / "THEORY.md").write_text("# Theory\n", encoding="utf-8")
    (root / "schemas").mkdir()
    cond = root / "skills" / "artist-os"
    cond.mkdir(parents=True)
    (cond / "SKILL.md").write_text(conductor, encoding="utf-8")
    (root / "evals" / "conductor-behavior").mkdir(parents=True)
    return root


class LockTests(unittest.TestCase):
    def test_real_conductor_matches_blessed_lock(self) -> None:
        self.assertTrue(
            ev.is_blessed(REPO),
            "conductor changed since the last eval bless — re-run the conductor-behavior "
            "eval (evals/README.md) then `bin/artist-os-eval bless`.",
        )

    def test_stale_when_conductor_changes_after_blessing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_bundle(tmp, "v1\n")
            ev.write_lock(root)
            self.assertTrue(ev.is_blessed(root))
            (root / "skills" / "artist-os" / "SKILL.md").write_text("v2 changed\n", encoding="utf-8")
            self.assertFalse(ev.is_blessed(root))

    def test_bless_reblesses_a_changed_conductor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_bundle(tmp, "v1\n")
            ev.write_lock(root)
            (root / "skills" / "artist-os" / "SKILL.md").write_text("v2\n", encoding="utf-8")
            self.assertFalse(ev.is_blessed(root))
            ev.write_lock(root)
            self.assertTrue(ev.is_blessed(root))


class CliTests(unittest.TestCase):
    def _run(self, root: Path, *args: str) -> subprocess.CompletedProcess:
        env = {**os.environ, "ARTIST_OS_ROOT": str(root)}
        return subprocess.run([sys.executable, str(EVAL), *args], capture_output=True, text=True, env=env)

    def test_status_exit_codes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_bundle(tmp, "v1\n")
            ev.write_lock(root)
            self.assertEqual(self._run(root, "status").returncode, 0)
            (root / "skills" / "artist-os" / "SKILL.md").write_text("v2\n", encoding="utf-8")
            stale = self._run(root, "status")
            self.assertNotEqual(stale.returncode, 0)
            self.assertIn("STALE", stale.stdout + stale.stderr)

    def test_status_handles_malformed_lock_cleanly(self) -> None:
        # Non-JSON, and valid JSON that is not an object (would crash a bare .get()).
        for bad in ("not json {{{", "[1, 2, 3]", "42", '"a string"'):
            with tempfile.TemporaryDirectory() as tmp:
                root = make_bundle(tmp, "v1\n")
                (root / "evals" / "conductor-behavior" / "blessed.lock").write_text(bad, encoding="utf-8")
                proc = self._run(root, "status")
                self.assertNotEqual(proc.returncode, 0, f"{bad!r}")
                self.assertNotIn("Traceback", proc.stdout + proc.stderr, f"{bad!r}: {proc.stderr}")
                self.assertIn("STALE", proc.stdout + proc.stderr, f"{bad!r}")

    def test_start_refuses_to_clobber_existing_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_bundle(tmp, "v1\n")
            ev.write_lock(root)
            (root / "evals" / "conductor-behavior" / "grade-template.md").write_text("# grade\n", encoding="utf-8")
            snap = root / "evals" / "conductor-behavior" / "baseline-SKILL.md"

            self.assertEqual(self._run(root, "start", "baseline").returncode, 0)
            snap.write_text("PRECIOUS PRIOR RUN\n", encoding="utf-8")  # stand in for a real blessed snapshot

            blocked = self._run(root, "start", "baseline")
            self.assertNotEqual(blocked.returncode, 0, "a second start must not silently clobber the snapshot")
            self.assertNotIn("Traceback", blocked.stderr)
            self.assertEqual(snap.read_text(encoding="utf-8"), "PRECIOUS PRIOR RUN\n")

            forced = self._run(root, "start", "baseline", "--force")
            self.assertEqual(forced.returncode, 0, forced.stdout + forced.stderr)
            self.assertNotEqual(snap.read_text(encoding="utf-8"), "PRECIOUS PRIOR RUN\n")

    def test_start_clean_error_when_grade_template_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_bundle(tmp, "v1\n")  # make_bundle does not create grade-template.md
            ev.write_lock(root)
            proc = self._run(root, "start", "trimmed")
            self.assertNotEqual(proc.returncode, 0)
            self.assertNotIn("Traceback", proc.stderr)
            self.assertIn("grade-template", proc.stderr)

    def test_commands_fail_cleanly_when_conductor_missing(self) -> None:
        # resolve_root only requires the skills/ dir, so a bundle can lack the
        # conductor file; status/bless/start must fail cleanly, never traceback.
        for cmd in (["status"], ["bless"], ["start", "baseline"]):
            with tempfile.TemporaryDirectory() as tmp:
                root = make_bundle(tmp, "v1\n")
                ev.write_lock(root)  # computed while the conductor still exists
                (root / "evals" / "conductor-behavior" / "grade-template.md").write_text("# g\n", encoding="utf-8")
                (root / "skills" / "artist-os" / "SKILL.md").unlink()
                proc = self._run(root, *cmd)
                self.assertNotEqual(proc.returncode, 0, f"{cmd}")
                self.assertNotIn("Traceback", proc.stdout + proc.stderr, f"{cmd}: {proc.stderr}")

    def test_force_clears_stale_grade_and_traces(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_bundle(tmp, "v1\n")
            ev.write_lock(root)
            (root / "evals" / "conductor-behavior" / "grade-template.md").write_text("# grade template\n", encoding="utf-8")
            self.assertEqual(self._run(root, "start", "trimmed").returncode, 0)
            trace_dir = root / "evals" / "conductor-behavior" / "trimmed"
            (trace_dir / "grade.md").write_text("GRADE v1: ALL PASS\n", encoding="utf-8")
            (trace_dir / "T1.md").write_text("trace of v1\n", encoding="utf-8")
            (root / "skills" / "artist-os" / "SKILL.md").write_text("v2\n", encoding="utf-8")

            self.assertEqual(self._run(root, "start", "trimmed", "--force").returncode, 0)
            self.assertNotIn("PASS", (trace_dir / "grade.md").read_text(encoding="utf-8"),
                             "a forced re-snapshot must not keep the prior grade sheet")
            self.assertFalse((trace_dir / "T1.md").exists(), "stale traces must be cleared on --force")

    def test_start_stamps_conductor_digest_into_grade(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_bundle(tmp, "v1\n")
            ev.write_lock(root)
            (root / "evals" / "conductor-behavior" / "grade-template.md").write_text("# grade template\n", encoding="utf-8")

            proc = self._run(root, "start", "trimmed")

            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            grade = (root / "evals" / "conductor-behavior" / "trimmed" / "grade.md").read_text(encoding="utf-8")
            self.assertIn(f"graded_against_sha256: {ev.conductor_digest(root)}", grade)

    def test_bless_refuses_missing_grade(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_bundle(tmp, "v1\n")
            proc = self._run(root, "bless")

            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("grade", proc.stdout + proc.stderr)
            self.assertFalse(ev.is_blessed(root))

    def test_bless_refuses_stale_grade_digest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_bundle(tmp, "v1\n")
            ev.write_lock(root)
            (root / "evals" / "conductor-behavior" / "grade-template.md").write_text("# grade template\n", encoding="utf-8")
            self.assertEqual(self._run(root, "start", "trimmed").returncode, 0)
            (root / "skills" / "artist-os" / "SKILL.md").write_text("v2\n", encoding="utf-8")
            grade = root / "evals" / "conductor-behavior" / "trimmed" / "grade.md"
            grade.write_text(
                f"graded_against_sha256: {'0' * 64}\nOverall result: PASS\n",
                encoding="utf-8",
            )

            proc = self._run(root, "bless")

            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("stale", proc.stdout + proc.stderr)
            self.assertFalse(ev.is_blessed(root))

    def test_bless_refuses_grade_without_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_bundle(tmp, "v1\n")
            (root / "evals" / "conductor-behavior" / "grade-template.md").write_text("# grade template\n", encoding="utf-8")
            self.assertEqual(self._run(root, "start", "trimmed").returncode, 0)
            grade = root / "evals" / "conductor-behavior" / "trimmed" / "grade.md"
            grade.write_text(
                f"graded_against_sha256: {ev.conductor_digest(root)}\nOverall result: FAIL\n",
                encoding="utf-8",
            )

            proc = self._run(root, "bless")

            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("PASS", proc.stdout + proc.stderr)
            self.assertFalse(ev.is_blessed(root))

    def test_bless_accepts_current_passing_grade(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_bundle(tmp, "v1\n")
            ev.write_lock(root)
            (root / "evals" / "conductor-behavior" / "grade-template.md").write_text("# grade template\n", encoding="utf-8")
            (root / "skills" / "artist-os" / "SKILL.md").write_text("v2\n", encoding="utf-8")
            self.assertEqual(self._run(root, "start", "trimmed", "--force").returncode, 0)
            digest = ev.conductor_digest(root)
            grade = root / "evals" / "conductor-behavior" / "trimmed" / "grade.md"
            grade.write_text(
                f"graded_against_sha256: {digest}\nOverall result: PASS\n",
                encoding="utf-8",
            )

            proc = self._run(root, "bless")

            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertTrue(ev.is_blessed(root))


if __name__ == "__main__":
    unittest.main()
