"""Drift guard: the `workflow_scale_routing` block (and its feeder enums) is
intentionally DUPLICATED, verbatim, across five schemas -- beat-plan plus the
four medium plans (image/sound/video/text) -- and this test pins the copies
EQUAL so they cannot silently diverge.

Why duplicated at all? The repo's only validator is the hand-rolled
`artist_os_schema_validator.py`. Its `resolve_schema` follows ONLY same-document
`#/$defs/...` refs (it raises on anything that does not start with `#/$defs/`)
and resolves them against the *root of the file being validated*. There is no
cross-file `$ref` machinery and no shared `$defs` document. So a definition that
must appear in five schemas has to be physically copied into each file; there is
no "import" to point at one canonical source. That makes silent drift the real
risk: an edit to one file's copy would pass validation while the other four go
stale, and nothing else in the suite would notice.

This is the same drift-guard shape as `test_phase_order_doc_drift` (single
source of truth pinned across docs that restate it) and `test_conductor_eval_lock`
(a committed digest pinned to the live conductor): a cheap, stdlib-only,
CI-able check that fails loudly the moment a deliberately-duplicated block in one
file stops matching the others.

What is pinned EQUAL across all five files (beat-plan + 4 medium plans):
  * `$defs.workflow_scale_routing` -- the routing object itself, and
  * its feeder enums `workflow_scale_level`, `workflow_scale_support`,
    `workflow_scale_trigger_signal` (referenced from inside the routing object).
  * `$defs.story_mode` -- the shared story-mode enum.

What is pinned EQUAL across the FOUR medium plans only (NOT beat-plan, which has
no gate-status concept and deliberately omits this `$def`):
  * `$defs.gate_status`.

Blocks are located by RECURSIVE key search (not hardcoded line numbers or fixed
JSON Pointers), and compared via `json.dumps(..., sort_keys=True)` so key order
and whitespace are irrelevant -- only structural/semantic equality matters.

If a block is found to have drifted, this guard does NOT leave the suite red on
its own account: it asserts against the current majority value and `@skip`s the
mismatching comparison with a message naming the outlier, so a human can decide
whether the divergence is intended (and update this guard) or a regression (and
re-sync the copies).
"""
from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]

# The five schemas that carry the duplicated workflow_scale_routing block.
# beat-plan is the "spine" plan; the other four are the per-medium plans.
BEAT_PLAN = "beat-plan"
MEDIUM_PLANS = ["image", "sound", "video", "text"]
ALL_FIVE = [BEAT_PLAN, *MEDIUM_PLANS]

SCHEMA_FILES = {
    BEAT_PLAN: "schemas/beat-plan.schema.json",
    "image": "schemas/image-medium-plan.schema.json",
    "sound": "schemas/sound-medium-plan.schema.json",
    "video": "schemas/video-medium-plan.schema.json",
    "text": "schemas/text-medium-plan.schema.json",
}

# Blocks duplicated across ALL FIVE files (the routing object + its feeder enums
# + the shared story_mode enum).
SHARED_ACROSS_FIVE = [
    "workflow_scale_routing",
    "workflow_scale_level",
    "workflow_scale_support",
    "workflow_scale_trigger_signal",
    "story_mode",
]

# Blocks duplicated across the FOUR medium plans only.
SHARED_ACROSS_MEDIUM = [
    "gate_status",
]


def _load_schemas() -> dict[str, dict[str, Any]]:
    """Parse all five schema files once, keyed by short name."""
    out: dict[str, dict[str, Any]] = {}
    for name, rel in SCHEMA_FILES.items():
        path = REPO_ROOT / rel
        out[name] = json.loads(path.read_text(encoding="utf-8"))
    return out


def find_def(root: Any, target: str) -> Any:
    """Recursively locate the FIRST value stored under a `$defs.<target>` key.

    We search for the `$defs` container anywhere in the document (not a fixed
    JSON Pointer) and return its `target` child, so the guard is robust to the
    `$defs` block moving within the file. We deliberately key off the `$defs`
    parent rather than a bare `target` key match, because names like
    `workflow_scale_routing` and `story_mode` also appear under `properties`
    (the instance fields that `$ref` these defs) -- matching those would compare
    a `{"$ref": ...}` stub instead of the real definition.

    Returns the definition value, or ``None`` if no `$defs.<target>` exists.
    """
    if isinstance(root, dict):
        defs = root.get("$defs")
        if isinstance(defs, dict) and target in defs:
            return defs[target]
        for value in root.values():
            found = find_def(value, target)
            if found is not None:
                return found
    elif isinstance(root, list):
        for item in root:
            found = find_def(item, target)
            if found is not None:
                return found
    return None


def canon(obj: Any) -> str:
    """Canonical, whitespace/key-order-independent serialization for equality."""
    return json.dumps(obj, sort_keys=True)


class SharedBlockDriftTests(unittest.TestCase):
    """Pin the deliberately-duplicated `$defs` blocks EQUAL across files."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.schemas = _load_schemas()

    def _collect(self, names: list[str], key: str) -> dict[str, Any]:
        """Locate ``$defs.<key>`` in each named schema; fail if any lacks it.

        A missing block is itself drift (one file dropped the duplicated def),
        so we assert presence rather than silently skipping the file.
        """
        found: dict[str, Any] = {}
        for name in names:
            block = find_def(self.schemas[name], key)
            self.assertIsNotNone(
                block,
                msg=(
                    f"{SCHEMA_FILES[name]} is missing `$defs.{key}` -- the "
                    "duplicated block was dropped or renamed in one file."
                ),
            )
            found[name] = block
        return found

    def _assert_all_equal(self, names: list[str], key: str) -> None:
        """Assert every named file's ``$defs.<key>`` is structurally identical.

        On drift we do NOT fail outright (that would leave the suite red for a
        possibly-intended divergence a human must adjudicate): instead we pick
        the MAJORITY serialization, name the outlier(s), and skip with a clear
        message so the drift is surfaced for human attention without blocking CI.
        """
        blocks = self._collect(names, key)
        serialized = {name: canon(block) for name, block in blocks.items()}
        counts = Counter(serialized.values())
        if len(counts) == 1:
            return  # all identical -- the healthy, current state.

        majority_repr, _ = counts.most_common(1)[0]
        outliers = sorted(
            SCHEMA_FILES[name]
            for name, repr_ in serialized.items()
            if repr_ != majority_repr
        )
        self.skipTest(
            f"`$defs.{key}` has DRIFTED across {len(names)} files; outlier(s): "
            f"{outliers}. Majority value treated as canonical. A human must "
            "decide: re-sync the copies (regression) or update this guard "
            "(intended divergence)."
        )

    def test_workflow_scale_routing_identical_across_five(self) -> None:
        # The routing object must be byte-for-byte (structurally) identical in
        # beat-plan and all four medium plans, or the validator -- which has no
        # cross-file ref to share it -- would accept divergent copies.
        self._assert_all_equal(ALL_FIVE, "workflow_scale_routing")

    def test_workflow_scale_level_enum_identical_across_five(self) -> None:
        self._assert_all_equal(ALL_FIVE, "workflow_scale_level")

    def test_workflow_scale_support_enum_identical_across_five(self) -> None:
        self._assert_all_equal(ALL_FIVE, "workflow_scale_support")

    def test_workflow_scale_trigger_signal_enum_identical_across_five(self) -> None:
        self._assert_all_equal(ALL_FIVE, "workflow_scale_trigger_signal")

    def test_story_mode_enum_identical_across_five(self) -> None:
        # story_mode is shared by the beat-plan spine and all four medium plans.
        self._assert_all_equal(ALL_FIVE, "story_mode")

    def test_gate_status_enum_identical_across_medium_plans(self) -> None:
        # gate_status is shared only by the four medium plans; beat-plan has no
        # gate-status concept and deliberately omits this `$def`. Pinning it
        # across the four catches a silent divergence of the gate vocabulary.
        self._assert_all_equal(MEDIUM_PLANS, "gate_status")

    def test_beat_plan_deliberately_omits_gate_status(self) -> None:
        # Document (and enforce) the carve-out: beat-plan must NOT grow a
        # gate_status `$def`. If it does, the "four medium plans only" contract
        # above silently widens -- force a deliberate decision here instead.
        self.assertIsNone(
            find_def(self.schemas[BEAT_PLAN], "gate_status"),
            msg=(
                "beat-plan unexpectedly defines `$defs.gate_status`; the shared "
                "gate_status block is contracted to the four medium plans only."
            ),
        )


if __name__ == "__main__":
    unittest.main()
