"""Guard packaging/MANIFEST.json: everything that must travel is actually covered.

This is the live drift gate ADR 0008 promises. It does NOT settle for prefix
containment ("docs/ is listed"); it resolves each referenced path to an existing
file under an included tree, and forces any root-level module that bin/*.py
imports into the manifest (the gap that left artist_os_schema_validator.py out).

The reference scan reuses the SHIPPED resolver logic (referenced_paths) rather
than re-declaring the regex, so the test cannot drift from what `doctor` checks.
"""
from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "packaging" / "MANIFEST.json"

# Load bin/artist-os-paths (an extensionless script) as a module to reuse its
# reference-scanning logic. Importing has no side effects (the CLI dispatch is
# guarded by `if __name__ == "__main__"`).
_LOADER = importlib.machinery.SourceFileLoader("artist_os_paths", str(REPO / "bin" / "artist-os-paths"))
_SPEC = importlib.util.spec_from_loader("artist_os_paths", _LOADER)
resolver = importlib.util.module_from_spec(_SPEC)
_LOADER.exec_module(resolver)

IMPORT_RE = re.compile(r"^\s*(?:from|import)\s+([a-zA-Z_]\w*)", re.MULTILINE)


def manifest_includes() -> list[str]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))["include"]


def covered_by(rel: str, includes: list[str]) -> bool:
    """True if rel is, or sits under, an included path."""
    for inc in includes:
        if inc.endswith("/"):
            if rel == inc.rstrip("/") or rel.startswith(inc):
                return True
        elif rel == inc:
            return True
    return False


def bin_root_module_deps() -> list[str]:
    """Root-level <module>.py files that bin/* scripts import."""
    mods: set[str] = set()
    for entry in sorted((REPO / "bin").glob("*")):
        if not entry.is_file():
            continue
        try:
            text = entry.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for mod in IMPORT_RE.findall(text):
            if (REPO / f"{mod}.py").exists():
                mods.add(f"{mod}.py")
    return sorted(mods)


class DistManifestTests(unittest.TestCase):
    def test_every_include_path_exists(self) -> None:
        for rel in manifest_includes():
            self.assertTrue((REPO / rel).exists(), f"manifest include {rel!r} does not exist under repo root")

    def test_skill_references_resolve_and_are_covered(self) -> None:
        includes = manifest_includes()
        refs = resolver.referenced_paths(REPO)  # shipped logic — single source with doctor
        self.assertTrue(refs, "expected to find doc/schema references in skill bodies")
        for ref in refs:
            self.assertTrue((REPO / ref).exists(), f"skill-referenced {ref!r} is missing under repo root")
            self.assertTrue(covered_by(ref, includes), f"skill-referenced {ref!r} is not under any manifest include")

    def test_bin_root_module_deps_are_in_manifest(self) -> None:
        includes = manifest_includes()
        deps = bin_root_module_deps()
        self.assertIn("artist_os_schema_validator.py", deps, "expected bin/ to import the root validator module")
        for mod in deps:
            self.assertTrue(covered_by(mod, includes), f"bin/ imports root module {mod!r} not covered by the manifest")


if __name__ == "__main__":
    unittest.main()
