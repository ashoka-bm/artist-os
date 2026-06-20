"""Guard: the installed skill set, the conductor's delegation set, and the
routing eval's target set must all match the skills that exist on disk.

This is the test that the routing eval itself cannot provide: the eval builds
its skill universe by globbing skills/*/SKILL.md directly, so it reports a skill
as routable even when bin/install-codex-dev-skills never registers it. That blind
spot once let the entire Text Journey slice (text-journey, clear-writing-pass,
human-voice-pass) ship unrouteable while the eval stayed green. These assertions
fail loudly the moment installed != delegated != eval-targeted again.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO / "skills"
INSTALLER = REPO / "bin" / "install-codex-dev-skills"
CONDUCTOR = SKILLS_DIR / "artist-os" / "SKILL.md"
ROUTING_EVALS = REPO / "evals" / "routing" / "routing-evals.json"


def on_disk_skills() -> set[str]:
    """Every skill directory that ships a SKILL.md."""
    return {p.parent.name for p in SKILLS_DIR.glob("*/SKILL.md")}


def installer_skills() -> set[str]:
    """Skills bin/install-codex-dev-skills registers: artist-os (installed
    explicitly) plus the names in the skills=( ... ) array."""
    text = INSTALLER.read_text(encoding="utf-8")
    found: set[str] = set()
    if 'install_skill "$repo_root/skills/artist-os"' in text:
        found.add("artist-os")
    match = re.search(r"skills=\((.*?)\)", text, re.DOTALL)
    if match:
        found |= set(re.findall(r'"([a-z0-9-]+)"', match.group(1)))
    return found


def conductor_delegated_skills() -> set[str]:
    """Sibling skills the conductor references by skills/<name> path, plus the
    conductor itself. Filtered to real skill directories so stray prose matches
    (e.g. skills/references) are ignored."""
    text = CONDUCTOR.read_text(encoding="utf-8")
    refs = set(re.findall(r"skills/([a-z0-9-]+)", text))
    refs.add("artist-os")
    return {r for r in refs if (SKILLS_DIR / r / "SKILL.md").exists()}


def eval_target_skills() -> set[str]:
    """Skills the routing eval treats as routing targets, minus the 'none'
    off-domain sentinel."""
    data = json.loads(ROUTING_EVALS.read_text(encoding="utf-8"))
    return {s for s in data["skills"] if s != "none"}


class SkillSetSyncTest(unittest.TestCase):
    def test_installer_registers_exactly_on_disk_skills(self) -> None:
        on_disk = on_disk_skills()
        installed = installer_skills()
        self.assertEqual(
            installed,
            on_disk,
            "bin/install-codex-dev-skills must register exactly the skills in skills/. "
            f"Missing from installer: {sorted(on_disk - installed)}; "
            f"installer-only: {sorted(installed - on_disk)}.",
        )

    def test_conductor_delegates_to_every_skill(self) -> None:
        on_disk = on_disk_skills()
        delegated = conductor_delegated_skills()
        self.assertEqual(
            delegated,
            on_disk,
            "The artist-os conductor must reference every skill by skills/<name> path. "
            f"Never delegated: {sorted(on_disk - delegated)}; "
            f"delegated but absent on disk: {sorted(delegated - on_disk)}.",
        )

    def test_routing_eval_targets_every_skill(self) -> None:
        on_disk = on_disk_skills()
        targets = eval_target_skills()
        self.assertEqual(
            targets,
            on_disk,
            "evals/routing/routing-evals.json skills[] (minus 'none') must match skills/ on disk. "
            f"Untested skills: {sorted(on_disk - targets)}; "
            f"tested but absent on disk: {sorted(targets - on_disk)}.",
        )


if __name__ == "__main__":
    unittest.main()
