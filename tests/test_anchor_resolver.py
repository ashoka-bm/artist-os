"""Behavioral guard for bin/artist-os-paths (the $ARTIST_OS_ROOT resolver).

Covers the resilience properties ADR 0008 relies on: raw output that round-trips
through a real shell capture even when the path contains a space, loud failure
on a bad anchor (never a silent cwd fallback, and no misleading path on stdout),
a `get` that fails loud on a mistyped key, and — critically — negative cases
proving `validate`/`doctor` actually return non-zero on a broken bundle, not just
pass on the golden one.
"""
from __future__ import annotations

import json
import os
import shlex
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RESOLVER = REPO / "bin" / "artist-os-paths"

VALID_CODEX = {
    "displayName": "Codex",
    "status": "active",
    "cliCommand": "codex",
    "skillPrefix": "artist-os-",
    "conductorUnprefixed": True,
    "globalRoot": ".codex/skills",
    "usesEnvVars": True,
    "linkingStrategy": "symlink-or-copy",
    "frontmatter": {"mode": "passthrough"},
    "pathRewrites": [],
}


def run(args, env_override=None):
    env = dict(os.environ)
    env.pop("ARTIST_OS_ROOT", None)
    if env_override:
        env.update(env_override)
    return subprocess.run([sys.executable, str(RESOLVER), *args], capture_output=True, text=True, env=env)


def make_bundle(root: Path, *, skill_body="# demo\n", manifest_include=None, hosts=None) -> Path:
    """Materialize a minimal valid bundle (markers + packaging) for negative tests."""
    (root / "THEORY.md").write_text("x", encoding="utf-8")
    (root / "schemas").mkdir(exist_ok=True)
    (root / "skills" / "demo").mkdir(parents=True, exist_ok=True)
    (root / "skills" / "demo" / "SKILL.md").write_text(skill_body, encoding="utf-8")
    pkg = root / "packaging"
    pkg.mkdir(exist_ok=True)
    (pkg / "hosts.json").write_text(
        json.dumps(hosts or {"primaryHost": "codex", "hosts": {"codex": VALID_CODEX}}), encoding="utf-8"
    )
    (pkg / "MANIFEST.json").write_text(
        json.dumps({"include": manifest_include or ["THEORY.md", "schemas/", "skills/", "packaging/"], "exclude": []}),
        encoding="utf-8",
    )
    return root


class AnchorResolverTests(unittest.TestCase):
    # --- positive resolution / output contract ---
    def test_root_is_raw_and_equals_repo(self) -> None:
        result = run(["root"])
        self.assertEqual(result.returncode, 0, result.stderr)
        printed = result.stdout.strip()
        self.assertTrue(Path(printed).is_dir(), f"root did not resolve to a dir: {printed!r}")
        self.assertEqual(Path(printed), REPO)

    def test_root_round_trips_through_real_shell_capture(self) -> None:
        # Genuinely exercise $(...) capture + word-splitting in bash; the repo
        # path contains a space, so a shell-quoted or split value fails `test -d`.
        env = dict(os.environ)
        env.pop("ARTIST_OS_ROOT", None)
        cmd = f"r=$({shlex.quote(sys.executable)} {shlex.quote(str(RESOLVER))} root); test -d \"$r\""
        self.assertEqual(subprocess.run(["bash", "-c", cmd], env=env).returncode, 0)

    def test_get_string_value_is_raw(self) -> None:
        result = run(["get", "codex", "skillPrefix"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "artist-os-")

    def test_get_boolean_is_json_lowercase(self) -> None:
        result = run(["get", "codex", "conductorUnprefixed"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "true")

    def test_get_absent_key_fails_loud(self) -> None:
        self.assertEqual(run(["get", "codex", "skllPrefix"]).returncode, 3)

    def test_get_unknown_host_fails_loud(self) -> None:
        self.assertEqual(run(["get", "nohost", "skillPrefix"]).returncode, 1)

    def test_get_present_null_is_empty_success(self) -> None:
        result = run(["get", "claude-code", "skillPrefix"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "")

    def test_validate_passes_on_repo(self) -> None:
        self.assertEqual(run(["validate"]).returncode, 0)

    def test_doctor_passes_on_repo(self) -> None:
        self.assertEqual(run(["doctor"]).returncode, 0)

    # --- loud failure: never a silent cwd fallback, never a misleading path ---
    def test_bad_anchor_fails_loud_with_empty_stdout(self) -> None:
        for bad in ("/definitely/not/an/artist-os/bundle", "relative/path"):
            result = run(["root"], env_override={"ARTIST_OS_ROOT": bad})
            self.assertNotEqual(result.returncode, 0, f"{bad!r} should fail")
            self.assertEqual(result.stdout.strip(), "", "must not print any path on a failed resolve")

    # --- negative: the gates can actually fail (not just pass on the golden bundle) ---
    def test_doctor_fails_on_missing_manifest_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            make_bundle(Path(tmp), manifest_include=["THEORY.md", "schemas/", "skills/", "packaging/", "NOPE.md"])
            result = run(["doctor"], env_override={"ARTIST_OS_ROOT": tmp})
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("NOPE.md", result.stdout + result.stderr)

    def test_doctor_fails_on_orphaned_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            make_bundle(Path(tmp), skill_body="# demo\n\nSee `docs/does-not-exist.md` for details.\n")
            result = run(["doctor"], env_override={"ARTIST_OS_ROOT": tmp})
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("docs/does-not-exist.md", result.stdout + result.stderr)

    def test_validate_fails_on_active_host_missing_field(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            broken = {"primaryHost": "codex", "hosts": {"codex": {"status": "active", "globalRoot": ".codex/skills"}}}
            make_bundle(Path(tmp), hosts=broken)
            self.assertNotEqual(run(["validate"], env_override={"ARTIST_OS_ROOT": tmp}).returncode, 0)

    def test_validate_fails_on_stub_with_nonnull_field(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            broken = {
                "primaryHost": "codex",
                "hosts": {
                    "codex": VALID_CODEX,
                    "claude-code": {
                        "status": "stub", "skillPrefix": "should-be-null", "usesEnvVars": None,
                        "linkingStrategy": None, "pathRewrites": None, "frontmatter": None,
                        "conductorUnprefixed": None, "globalRoot": None,
                    },
                },
            }
            make_bundle(Path(tmp), hosts=broken)
            self.assertNotEqual(run(["validate"], env_override={"ARTIST_OS_ROOT": tmp}).returncode, 0)


if __name__ == "__main__":
    unittest.main()
