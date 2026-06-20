from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


# Leanness guard for the anti-evasion contract. A sibling framework hit a real
# failure where a model wrote findings as prose and walked past an approval
# gate, treating its own recommendation as the artist's decision. The fix names
# that evasion explicitly: the full rule lives once in the canonical gates doc
# (it governs ALL gates), and the conductor carries a short enforcement pointer
# to it. This test pins both so a future dedup or leanness pass cannot silently
# delete the rule or sever the conductor's pointer to it, which would let the
# route-around-the-gate bug back in.


GATES_DOC = "docs/gates-and-reviews.md"
CONDUCTOR_SKILL = "skills/artist-os/SKILL.md"


# Distinctive, load-bearing fragments of the canonical rule. Short enough that a
# legitimate rewording elsewhere is unaffected, specific enough that deleting the
# anti-evasion intent trips the test.
GATE_COMPLETION_RULE_FRAGMENTS = [
    "## Gate Completion Rule",
    "only when it comes from an explicit artist turn",
    "must not infer approval from silence",
    "An obvious choice is still the artist's choice.",
    "fabricates provenance",
]


# The conductor's enforcement bullet names the evasion and points at the
# canonical rule. Both must survive.
CONDUCTOR_ENFORCEMENT_FRAGMENTS = [
    "Never complete a gate, grant an approval, record a waiver, or select an option on the artist's behalf",
    'docs/gates-and-reviews.md',
    'Gate Completion Rule',
]


class GateEnforcementContractTests(unittest.TestCase):
    def test_canonical_rule_states_anti_evasion_contract(self) -> None:
        text = (REPO_ROOT / GATES_DOC).read_text(encoding="utf-8")
        for fragment in GATE_COMPLETION_RULE_FRAGMENTS:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, text)

    def test_conductor_names_evasion_and_points_to_canonical_rule(self) -> None:
        text = (REPO_ROOT / CONDUCTOR_SKILL).read_text(encoding="utf-8")
        for fragment in CONDUCTOR_ENFORCEMENT_FRAGMENTS:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, text)


if __name__ == "__main__":
    unittest.main()
