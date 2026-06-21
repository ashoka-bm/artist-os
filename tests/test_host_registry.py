"""Guard packaging/hosts.json shape and its agreement with the installer.

The registry is the config-validation guarantee ADR 0008 substitutes for the
compile-time typing a TypeScript registry would give. These assertions are the
Python equivalent of `artist-os-paths validate`, plus a drift gate that the
installer's Codex target/prefix is sourced from the registry (so the two cannot
silently disagree).
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REGISTRY = REPO / "packaging" / "hosts.json"
INSTALLER = REPO / "bin" / "install-codex-dev-skills"
NAME_RE = re.compile(r"^[a-z][a-z0-9-]*$")
ACTIVE_REQUIRED = {
    "skillPrefix": str,
    "globalRoot": str,
    "linkingStrategy": str,
    "conductorUnprefixed": bool,
    "usesEnvVars": bool,
    "pathRewrites": list,
    "frontmatter": dict,
}
STUB_NULL = ("skillPrefix", "usesEnvVars", "linkingStrategy", "pathRewrites", "frontmatter", "conductorUnprefixed")


class HostRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.hosts = self.registry["hosts"]

    def test_primary_host_is_present(self) -> None:
        self.assertIn(self.registry.get("primaryHost"), self.hosts)

    def test_names_valid_and_global_roots_unique(self) -> None:
        seen: dict[str, str] = {}
        for name, cfg in self.hosts.items():
            self.assertRegex(name, NAME_RE)
            self.assertIn(cfg.get("status"), ("active", "stub"))
            global_root = cfg.get("globalRoot")
            if global_root:
                self.assertNotIn(global_root, seen, f"globalRoot {global_root!r} duplicated")
                seen[global_root] = name

    def test_active_hosts_carry_required_fields(self) -> None:
        for name, cfg in self.hosts.items():
            if cfg.get("status") != "active":
                continue
            for field, typ in ACTIVE_REQUIRED.items():
                value = cfg.get(field)
                self.assertIsInstance(value, typ, f"{name}.{field} must be a {typ.__name__}")
                if typ is str:
                    self.assertTrue(value, f"{name}.{field} must be non-empty")

    def test_stub_hosts_null_transform_fields(self) -> None:
        for name, cfg in self.hosts.items():
            if cfg.get("status") != "stub":
                continue
            for field in STUB_NULL:
                self.assertIsNone(cfg.get(field), f"stub {name}.{field} must be null")

    def test_installer_sources_codex_target_from_registry(self) -> None:
        # Drift gate: the installer must read its Codex target/prefix from the
        # registry, not hardcode them, so registry and installer cannot diverge.
        text = INSTALLER.read_text(encoding="utf-8")
        self.assertIn('"$repo_root/bin/artist-os-paths" get codex globalRoot', text)
        self.assertIn('"$repo_root/bin/artist-os-paths" get codex skillPrefix', text)


if __name__ == "__main__":
    unittest.main()
