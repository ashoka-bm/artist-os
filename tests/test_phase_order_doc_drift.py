from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


# Single-source-of-truth (SSoT) drift guard for PHASE ORDER.
#
# The canonical, numbered phase sequence for the shared image/sound/text spine
# lives in exactly one place: `skills/artist-os/SKILL.md` under the
# `## Phase Order` heading. README.md and ARCHITECTURE.md restate the same spine
# at a higher altitude (overview diagrams), and AGENTS.md + ARCHITECTURE.md both
# carry a pointer back to the canonical home.
#
# The SSoT decision (already made -- this test does not re-litigate it) is
# "Overview allowed": SKILL.md is the sole canonical numbered order; README and
# ARCHITECTURE MAY keep their overview diagrams, but two things must hold or the
# overviews silently rot into a contradictory second source of truth:
#   (a) the SSoT pointers back to SKILL.md must remain, and
#   (b) the overviews must not CONTRADICT the canonical order.
#
# This file makes that policy executable, cheaply, with stdlib only. It does NOT
# require the overviews to be verbatim copies (they are deliberately leaner) --
# it only pins the order-preserving "spine" of milestones shared by all of them,
# plus the pointers/disclaimer that keep ownership unambiguous.
#
# Failure modes this catches:
#   * a spine milestone silently dropped or reordered in the canonical itself
#     (which should force a deliberate ANCHOR_PHASES update, not pass quietly),
#   * a README overview that drifts out of order or loses a milestone,
#   * a README overview heading/diagram removed or renamed,
#   * a botched canonical edit that breaks the 1..N numbering (e.g. two "7."s),
#   * deletion of the SSoT ownership pointers / disclaimer.


CANONICAL_SKILL = "skills/artist-os/SKILL.md"
README = "README.md"
AGENTS = "AGENTS.md"
ARCHITECTURE = "ARCHITECTURE.md"


# The ordered "spine" milestones shared by the canonical Phase Order AND all
# three README overview diagrams, matched as CASE-INSENSITIVE SUBSTRINGS.
#
# These were chosen so each phrase appears (as a substring) in the canonical
# numbered list AND in each of the three README diagrams, and so none collides
# ambiguously. In particular "Story Critic Review" and "Output Critic Review"
# are each matched IN FULL -- never a bare "Critic Review" -- because both occur
# and a bare substring would match the wrong (earlier) one and defeat the
# order check. This list is the deliberate, reviewed contract: changing the
# canonical spine should require editing this list on purpose.
ANCHOR_PHASES = [
    "Source Record",
    "Meaning",
    "Transformation Brief",
    "Beat Plan",
    "Story Critic Review",
    "Medium Plan",
    "Brief Approval",
    "Prompt Plan Critique",
    "Output Record",
    "Output Critic Review",
    "Output Acceptance Gate",
]


def assert_subsequence(testcase, anchors, entries, label):
    """Assert ``anchors`` appear across ``entries`` as an order-preserving subsequence.

    ``entries`` is an ORDERED ``list[str]`` of DISCRETE units -- parsed milestone
    titles or diagram step lines -- NOT one flat blob of prose. This distinction
    is the whole point: matching anchors against a flat section string lets an
    anchor bind to an incidental prose mention inside some step's *body* (the
    spine phrases recur many times in the explanatory prose), so reordering the
    numbered milestones themselves slips through unnoticed. Matching against the
    discrete entries -- and consuming each entry at most once -- makes reordering
    provably catchable.

    Algorithm: walk the anchors in order, holding ``last`` = index of the entry
    that satisfied the previous anchor. For each anchor, scan entries at indices
    ``> last`` for the first whose lowercased text CONTAINS the lowercased anchor.
    Because we only ever look past ``last``, each entry is consumed at most once.

    On failure we distinguish two cases so the message points straight at the
    real problem:
      * the anchor DOES appear in an earlier entry (index ``<= last``) -> it is
        present but OUT OF ORDER (the milestones were reordered), or
      * the anchor appears nowhere -> a spine milestone is MISSING.
    The message names the anchor and ``label`` (which doc/diagram).
    """
    lowered = [entry.lower() for entry in entries]
    last = -1
    for anchor in anchors:
        needle = anchor.lower()
        found = None
        for i in range(last + 1, len(lowered)):
            if needle in lowered[i]:
                found = i
                break
        if found is not None:
            last = found
            continue
        # Not found after ``last``. Decide between out-of-order vs missing by
        # checking whether the anchor appears in any already-consumed entry.
        appears_earlier = any(needle in lowered[i] for i in range(0, last + 1))
        if appears_earlier:
            testcase.fail(
                f"[{label}] phase-order spine out of order: {anchor!r} appears "
                f"before the preceding milestone (expected it later)."
            )
        else:
            testcase.fail(
                f"[{label}] phase-order spine milestone missing: {anchor!r} not "
                f"found in the entry list."
            )


class CanonicalPhaseOrderTests(unittest.TestCase):
    """The canonical source itself is well-formed.

    Guards `skills/artist-os/SKILL.md` -> `## Phase Order`: a clean, gapless
    1..N numbered list whose milestones still run in the expected spine order.
    """

    def _phase_order_section(self) -> str:
        # Slice from the `## Phase Order` line up to (but not including) the next
        # heading matching `^#{2,3} ` -- which is `### Medium Specifics`. Slicing
        # by heading rather than line number keeps the test robust to edits above
        # and below the section.
        text = (REPO_ROOT / CANONICAL_SKILL).read_text(encoding="utf-8")
        lines = text.splitlines()
        start = None
        for i, line in enumerate(lines):
            if line.strip() == "## Phase Order":
                start = i
                break
        self.assertIsNotNone(
            start, msg="`## Phase Order` heading not found in canonical SKILL.md"
        )

        end = len(lines)
        for i in range(start + 1, len(lines)):
            if re.match(r"^#{2,3} ", lines[i]):
                end = i
                break
        return "\n".join(lines[start:end])

    def _milestone_titles(self, section: str) -> list[str]:
        # Parse the ordered list of milestone TITLES from the numbered lines.
        # Each step is `N. **Title** -- ...`; capture the bold text between the
        # first `**...**` on a numbered line. We match TITLES, not the section
        # prose, because the spine phrases recur inside step bodies (e.g. "Beat
        # Plan" appears repeatedly in the prose) -- matching prose lets anchors
        # bind to incidental mentions and silently miss a reordering.
        return re.findall(r"(?m)^\s*\d+\.\s+\*\*(.+?)\*\*", section)

    def test_numbered_list_is_sequential_from_one(self) -> None:
        # The numbered step lines must be 1,2,3,...,N -- contiguous, starting at
        # 1, no gaps or dupes. This catches a botched edit such as two "7."s or a
        # skipped number, which would otherwise read fine to a human skimming.
        section = self._phase_order_section()
        numbers = [
            int(m.group(1)) for m in re.finditer(r"(?m)^\s*(\d+)\.", section)
        ]
        self.assertTrue(numbers, msg="No numbered steps found under `## Phase Order`")
        self.assertEqual(
            numbers,
            list(range(1, len(numbers) + 1)),
            msg=f"Phase Order numbering is not a gapless 1..N sequence: {numbers}",
        )

    def test_canonical_spine_in_order(self) -> None:
        # Guard the canonical against silently losing or reordering a spine
        # milestone. We match against the parsed milestone TITLES (one discrete
        # entry per numbered step), NOT the section prose, so swapping two
        # milestone titles (e.g. step 4 <-> step 10) is caught as out-of-order
        # instead of binding to an incidental prose mention. If this fails, the
        # canonical changed and ANCHOR_PHASES must be revisited deliberately --
        # not patched away.
        titles = self._milestone_titles(self._phase_order_section())
        assert_subsequence(self, ANCHOR_PHASES, titles, "canonical Phase Order")

    def test_every_numbered_step_has_a_bold_title(self) -> None:
        # Every numbered step must carry a bold `**Title**`. If a step loses its
        # title, it silently drops out of the parsed title list and would no
        # longer participate in the spine-order check above -- a milestone could
        # then be reordered or removed unnoticed. Pin the counts equal, using the
        # SAME section slice for both, so the spine check always sees every step.
        section = self._phase_order_section()
        titles = self._milestone_titles(section)
        step_numbers = re.findall(r"(?m)^\s*(\d+)\.", section)
        self.assertEqual(
            len(titles),
            len(step_numbers),
            msg=(
                "Phase Order step count and bold-title count disagree: "
                f"{len(step_numbers)} numbered steps but {len(titles)} bold "
                "titles -- a numbered step is missing its `**Title**` and would "
                "drop out of the spine-order check."
            ),
        )


class ReadmeOverviewDriftTests(unittest.TestCase):
    """README overview diagrams must not contradict the canonical order.

    The three medium overviews live under known `### ` subsection headings
    inside `## Workflows`. We key off those exact headings deliberately and pull
    the FIRST fenced ```text block after each, so the `## Repository Contents`
    fenced blocks (and other fenced blocks in the file) are never matched.
    """

    # Exact subsection headings; if any is renamed/removed, locating it fails
    # and the test fails -- which is the point (the overview was changed).
    OVERVIEW_HEADINGS = [
        "### Text To Image",
        "### Text To Suno Music",
        "### Text To Text (Text Journey)",
    ]

    def _read(self) -> str:
        return (REPO_ROOT / README).read_text(encoding="utf-8")

    def _first_text_block_after(self, text: str, heading: str) -> str:
        heading_idx = text.find(heading)
        self.assertNotEqual(
            heading_idx,
            -1,
            msg=f"README overview heading not found (removed/renamed?): {heading!r}",
        )
        after = text[heading_idx + len(heading):]
        match = re.search(r"```text\n(.*?)```", after, re.DOTALL)
        self.assertIsNotNone(
            match,
            msg=f"No fenced ```text block found after README heading {heading!r}",
        )
        return match.group(1)

    def _diagram_steps(self, block: str) -> list[str]:
        # Split a fenced diagram block into an ordered list of DISCRETE step
        # entries -- one per non-empty line -- rather than one flat blob. The
        # first line is the input (e.g. `Text Reference`); subsequent lines are
        # `  -> Phase`. Strip surrounding whitespace and a leading `-> ` arrow.
        # We keep every line (anchors are a subsequence, so non-anchor entries
        # like `Style Direction` are simply skipped), and matching per-entry --
        # consuming each at most once -- makes a reordered diagram catchable.
        entries = []
        for raw in block.splitlines():
            line = raw.strip()
            if not line:
                continue
            if line.startswith("-> "):
                line = line[len("-> "):]
            entries.append(line)
        return entries

    def test_each_overview_preserves_spine_order(self) -> None:
        text = self._read()
        for heading in self.OVERVIEW_HEADINGS:
            with self.subTest(heading=heading):
                block = self._first_text_block_after(text, heading)
                entries = self._diagram_steps(block)
                assert_subsequence(self, ANCHOR_PHASES, entries, heading)


class SsotPointerTests(unittest.TestCase):
    """The SSoT ownership pointers and disclaimer must persist.

    AGENTS.md and ARCHITECTURE.md both point at the canonical home, and
    ARCHITECTURE.md explicitly disclaims being a third copy. Deleting these is
    how the overviews would quietly become a competing source of truth.
    """

    # NOTE: this fragment contains a Unicode RIGHTWARDS ARROW (U+2192) and
    # backticks. It is copied byte-for-byte out of AGENTS.md / ARCHITECTURE.md,
    # not retyped, so the characters match exactly.
    POINTER_FRAGMENT = '`skills/artist-os/SKILL.md` → "Phase Order"'
    DISCLAIMER_FRAGMENT = "does not maintain a third copy"

    # NOTE: these use ``assertTrue(fragment in big_text, ...)`` rather than
    # ``assertIn`` deliberately: ``assertIn`` dumps the ENTIRE document body into
    # the failure message (and CI log) on mismatch. A plain boolean keeps the
    # failure to the helpful ``msg`` alone.
    def test_agents_keeps_canonical_pointer(self) -> None:
        self.assertTrue(
            self.POINTER_FRAGMENT in (REPO_ROOT / AGENTS).read_text(encoding="utf-8"),
            msg="AGENTS.md lost the SSoT pointer to the canonical Phase Order.",
        )

    def test_architecture_keeps_canonical_pointer(self) -> None:
        self.assertTrue(
            self.POINTER_FRAGMENT
            in (REPO_ROOT / ARCHITECTURE).read_text(encoding="utf-8"),
            msg="ARCHITECTURE.md lost the SSoT pointer to the canonical Phase Order.",
        )

    def test_architecture_keeps_not_a_third_copy_disclaimer(self) -> None:
        self.assertTrue(
            self.DISCLAIMER_FRAGMENT
            in (REPO_ROOT / ARCHITECTURE).read_text(encoding="utf-8"),
            msg="ARCHITECTURE.md lost its 'not a third copy' SSoT disclaimer.",
        )


if __name__ == "__main__":
    unittest.main()
