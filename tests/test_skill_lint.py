"""Guard: bin/artist-os-lint encodes the skill-quality checks we otherwise run by
hand, so contributors get fast, offline feedback before a skill ships.

The linter's checks must stay anchored to the SHIPPED resolver logic
(bin/artist-os-paths) rather than re-declaring the reference regex, so a fixture
of deliberately-broken skills drives each failure mode RED while the real public
skills stay GREEN.
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

# Load bin/artist-os-lint (an extensionless script) as a module to call its pure
# check functions directly. Importing has no side effects (CLI dispatch is
# guarded by `if __name__ == "__main__"`). Same pattern as test_dist_manifest.
_LOADER = importlib.machinery.SourceFileLoader("artist_os_lint", str(REPO / "bin" / "artist-os-lint"))
_SPEC = importlib.util.spec_from_loader("artist_os_lint", _LOADER)
linter = importlib.util.module_from_spec(_SPEC)
_LOADER.exec_module(linter)


def make_root(tmp: str) -> Path:
    """A minimal directory that satisfies the bundle markers the resolver needs."""
    root = Path(tmp)
    (root / "THEORY.md").write_text("# Theory\n", encoding="utf-8")
    (root / "schemas").mkdir()
    (root / "skills").mkdir()
    (root / "docs").mkdir()
    return root


def make_skill(root: Path, name: str, frontmatter: str, body: str = "") -> Path:
    """Write skills/<name>/SKILL.md with the given frontmatter and body."""
    d = root / "skills" / name
    d.mkdir(parents=True)
    md = d / "SKILL.md"
    md.write_text(f"---\n{frontmatter}\n---\n\n{body}\n", encoding="utf-8")
    return md


class FrontmatterTests(unittest.TestCase):
    def test_skill_missing_description_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            skill = make_skill(root, "foo", "name: artist-os-foo")
            failures = linter.lint_skill(skill, root)
            self.assertTrue(
                any("description" in f for f in failures),
                f"expected a description failure, got: {failures}",
            )

    def test_well_formed_ref_free_skill_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            skill = make_skill(
                root,
                "foo",
                "name: artist-os-foo\ndescription: A real one-line description.",
                body="# Foo\n\nA ref-free editorial pass.",
            )
            self.assertEqual(linter.lint_skill(skill, root), [])


FM = "name: artist-os-foo\ndescription: A real one-line description."


class AnchorTests(unittest.TestCase):
    def test_reference_bearing_skill_without_anchor_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            (root / "docs" / "foo.md").write_text("# Foo doc\n", encoding="utf-8")
            skill = make_skill(root, "foo", FM, body="See `docs/foo.md` for the method.")
            failures = linter.lint_skill(skill, root)
            self.assertTrue(
                any("ARTIST_OS_ROOT" in f or "anchor" in f.lower() for f in failures),
                f"expected an anchor failure, got: {failures}",
            )

    def test_reference_bearing_skill_with_anchor_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            (root / "docs" / "foo.md").write_text("# Foo doc\n", encoding="utf-8")
            body = "Paths resolve from `$ARTIST_OS_ROOT`.\n\nSee `docs/foo.md` for the method."
            skill = make_skill(root, "foo", FM, body=body)
            self.assertEqual(linter.lint_skill(skill, root), [])

    def test_ref_free_skill_is_not_required_to_have_anchor(self) -> None:
        # A ref-free skill names no repo-root paths and so must NOT be flagged
        # for a missing anchor.
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            skill = make_skill(root, "foo", FM, body="A pass that names no docs/, schemas/, or skills/.")
            self.assertEqual(linter.lint_skill(skill, root), [])


class ReferenceResolutionTests(unittest.TestCase):
    def test_reference_to_missing_doc_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)  # docs/missing.md is deliberately not created
            body = "Paths resolve from `$ARTIST_OS_ROOT`.\n\nSee `docs/missing.md`."
            skill = make_skill(root, "foo", FM, body=body)
            failures = linter.lint_skill(skill, root)
            self.assertTrue(
                any("docs/missing.md" in f for f in failures),
                f"expected a missing-reference failure, got: {failures}",
            )


LINT = REPO / "bin" / "artist-os-lint"


class MoreFrontmatterTests(unittest.TestCase):
    def test_skill_missing_name_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            skill = make_skill(root, "foo", "description: Has a description but no name.")
            failures = linter.lint_skill(skill, root)
            self.assertTrue(any("name" in f for f in failures), f"got: {failures}")

    def test_no_frontmatter_block_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            d = root / "skills" / "foo"
            d.mkdir(parents=True)
            md = d / "SKILL.md"
            md.write_text("# Foo\n\nNo frontmatter at all.\n", encoding="utf-8")
            failures = linter.lint_skill(md, root)
            self.assertTrue(any("frontmatter" in f for f in failures), f"got: {failures}")

    def test_block_scalar_description_is_treated_as_empty(self) -> None:
        # A YAML folded/block scalar (`description: >`) parses to the bare ">"
        # indicator; that is not a usable one-line description and must fail.
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            skill = make_skill(root, "foo", "name: artist-os-foo\ndescription: >", body="folded text")
            failures = linter.lint_skill(skill, root)
            self.assertTrue(any("description" in f for f in failures), f"got: {failures}")

    def test_block_scalar_with_indent_or_chomp_indicator_is_empty(self) -> None:
        # YAML allows an indentation digit and/or chomp indicator after >/| ; all
        # are bare openers with no inline value and must fail the non-empty gate.
        for indicator in (">2", "|2-", "|1+", ">-", "|"):
            with tempfile.TemporaryDirectory() as tmp:
                root = make_root(tmp)
                skill = make_skill(root, "foo", f"name: artist-os-foo\ndescription: {indicator}", body="x")
                failures = linter.lint_skill(skill, root)
                self.assertTrue(any("description" in f for f in failures), f"{indicator!r}: {failures}")

    def test_unreadable_skill_md_reports_cleanly(self) -> None:
        # A glob match that is not a readable UTF-8 file must yield a failure
        # message, never a raw traceback.
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            (root / "skills" / "foo" / "SKILL.md").mkdir(parents=True)  # a directory, not a file
            failures = linter.lint_skill(root / "skills" / "foo" / "SKILL.md", root)
            self.assertTrue(any("read" in f.lower() for f in failures), f"got: {failures}")


class AnchorScopeTests(unittest.TestCase):
    def test_anchor_token_only_in_frontmatter_does_not_satisfy_body_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            (root / "docs" / "m.md").write_text("# m\n", encoding="utf-8")
            skill = make_skill(
                root,
                "foo",
                "name: artist-os-foo\ndescription: Mentions $ARTIST_OS_ROOT only here.",
                body="Follow the method in `docs/m.md`.",
            )
            failures = linter.lint_skill(skill, root)
            self.assertTrue(
                any("ARTIST_OS_ROOT" in f or "anchor" in f.lower() for f in failures),
                f"a body reference with the token only in frontmatter must fail; got: {failures}",
            )

    def test_doc_reference_only_in_frontmatter_lints_clean(self) -> None:
        # Pins the refs-side body scoping: a docs/ path mentioned only in the
        # frontmatter, with a ref-free anchor-free body, must NOT be flagged.
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            skill = make_skill(
                root,
                "foo",
                "name: artist-os-foo\ndescription: See `docs/foo.md` for context.",
                body="A body that references no repo-root paths.",
            )
            self.assertEqual(linter.lint_skill(skill, root), [])

    def test_bom_prefixed_valid_skill_lints_clean(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            d = root / "skills" / "foo"
            d.mkdir(parents=True)
            (d / "SKILL.md").write_text(
                "﻿---\nname: artist-os-foo\ndescription: A real one.\n---\n\nbody\n",
                encoding="utf-8",
            )
            self.assertEqual(linter.lint_skill(d / "SKILL.md", root), [])


class CliTests(unittest.TestCase):
    def test_cli_exits_zero_on_real_skills(self) -> None:
        # Pin ARTIST_OS_ROOT to the repo under test so a leaked ambient value
        # cannot make this lint a different bundle (false pass/flake).
        env = {**os.environ, "ARTIST_OS_ROOT": str(REPO)}
        proc = subprocess.run([sys.executable, str(LINT)], capture_output=True, text=True, env=env)
        self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
        self.assertIn("OK", proc.stdout)

    def test_cli_exits_nonzero_on_broken_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            make_skill(root, "foo", "name: artist-os-foo")  # no description
            env = {**os.environ, "ARTIST_OS_ROOT": str(root)}
            proc = subprocess.run([sys.executable, str(LINT)], capture_output=True, text=True, env=env)
            self.assertEqual(proc.returncode, 1, msg=proc.stdout + proc.stderr)
            self.assertIn("FAIL", proc.stdout)


class RealSkillsTests(unittest.TestCase):
    def test_all_real_skills_pass(self) -> None:
        # The shipped public skill set is the green baseline: the linter must not
        # flag any of them, or it would block every contributor on a false positive.
        failures: dict[str, list[str]] = {}
        for skill_md in sorted((REPO / "skills").glob("*/SKILL.md")):
            result = linter.lint_skill(skill_md, REPO)
            if result:
                failures[skill_md.parent.name] = result
        self.assertEqual(failures, {}, f"real skills should lint clean, got: {failures}")


if __name__ == "__main__":
    unittest.main()
