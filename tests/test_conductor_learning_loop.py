"""ADR 0016 Step 4: the conductor carries the self-improvement loop, and the
loop round-trips end to end through the CLI.

Two halves:
  1. A prose-integrity drift guard on skills/artist-os/SKILL.md — near-zero
     cost between full conductor evals, same shape as the other drift guards.
     It pins that the Learning Loop sections and verb references EXIST; the
     behavioral grading stays in the (manual, blessed) conductor eval.
  2. The end-to-end round trip: close-out feedback -> event + scoped sync ->
     surfaced with rule text at the next start -> candidate adopted locally ->
     review complete -> status reflects it.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sqlite3
import tempfile
import unittest
from contextlib import closing
from contextlib import redirect_stderr
from contextlib import redirect_stdout
from importlib.machinery import SourceFileLoader
from io import StringIO
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL = REPO_ROOT / "skills" / "artist-os" / "SKILL.md"


def load_artist_os_db():
    loader = SourceFileLoader("artist_os_db", str(REPO_ROOT / "bin" / "artist-os-db"))
    spec = importlib.util.spec_from_loader("artist_os_db", loader)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


artist_os_db = load_artist_os_db()


def minimal_manifest(project_id: str) -> dict:
    return {
        "project_id": project_id,
        "title": "Door Left Lit",
        "status": "active",
        "current_stage": "prompt_plan",
        "created_at": "2026-05-31T00:00:00Z",
        "updated_at": "2026-05-31T00:00:00Z",
        "summary": "A threshold image project.",
        "paths": {
            "project_dir": f"projects/{project_id}",
            "events": f"projects/{project_id}/events.jsonl",
            "source_record": f"projects/{project_id}/source/source-record.json",
            "meaning_interview": f"projects/{project_id}/meaning/meaning-interview.json",
            "creative_brief_record": f"projects/{project_id}/briefs/creative-brief.record.json",
            "prompt_plan": f"projects/{project_id}/prompt-plans/prompt-plan.json",
        },
        "decisions": {
            "interpretation_status": "complete",
            "symbology_status": "complete",
            "style_status": "complete",
            "detail_status": "complete",
        },
        "assets": [],
    }


class ConductorLearningLoopProseTests(unittest.TestCase):
    """The conductor must carry the loop's sections and name its verbs.

    Substring pins only — wording may evolve freely; a full re-grade happens
    in the conductor eval, and this guard just catches accidental deletion
    (token rot) between evals.
    """

    def setUp(self) -> None:
        self.text = SKILL.read_text(encoding="utf-8")

    def test_carries_rules_block_with_dated_entry(self) -> None:
        self.assertIn("\n## Rules\n", self.text)
        self.assertRegex(self.text, r"(?m)^- \d{4}-\d{2}-\d{2}: ")
        self.assertIn("never by live self-edit", self.text)

    def test_carries_learning_loop_section_and_verbs(self) -> None:
        self.assertIn("\n## Learning Loop\n", self.text)
        for needle in (
            "bin/artist-os-db status",
            "pending-learning-reviews",
            "learnings-report",
            "review-learnings",
            "add-feedback",
            "add-learning",
            "add-conductor-rule",
            "conductor-rules.md",
        ):
            self.assertIn(needle, self.text, f"SKILL.md must reference {needle}")

    def test_local_rules_are_additive_never_gate_loosening(self) -> None:
        self.assertIn("never loosen a Hard Gate", self.text)

    def test_close_out_and_triage_are_wired(self) -> None:
        self.assertIn("Anything to note before I close this out?", self.text)
        self.assertIn("still going or should be wrapped up", self.text)
        self.assertIn("Never edit this SKILL.md during a session.", self.text)


class LearningLoopRoundTripTests(unittest.TestCase):
    """The full loop, exactly as the conductor drives it."""

    def _capture(self, func, args) -> str:
        out = StringIO()
        with redirect_stdout(out), redirect_stderr(StringIO()):
            func(args)
        return out.getvalue()

    def test_close_out_to_next_start_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir)
            base = {"db": None, "library_root": str(library_root), "wondermint_root": None}
            proj_dir = library_root / "projects" / "proj_door_left_lit"
            proj_dir.mkdir(parents=True)
            (proj_dir / "project.json").write_text(
                json.dumps(minimal_manifest("proj_door_left_lit")), encoding="utf-8"
            )

            # 1. Close-Out captures feedback (event + scoped sync ride along).
            with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                artist_os_db.add_feedback(argparse.Namespace(
                    **base,
                    project_id="proj_door_left_lit",
                    feedback="Ask before expanding multiple parts.",
                    feedback_id="fb_ask_before_expand",
                    source="artist",
                    stage="project_completion",
                    output_record_id=None,
                    notes=None,
                ))

            # 2. Next session start: triage sees the open project + pending
            #    review; the promotion queue shows the item with commands.
            status_out = self._capture(
                artist_os_db.status_projects, argparse.Namespace(**base, project_id=None)
            )
            self.assertIn("proj_door_left_lit", status_out)
            self.assertIn("review=pending", status_out)
            queue = self._capture(artist_os_db.review_learnings, argparse.Namespace(**base))
            self.assertIn("Ask before expanding multiple parts.", queue)

            # 3. The artist approves staging it as a conductor candidate.
            with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                artist_os_db.add_learning(argparse.Namespace(
                    **base,
                    project_id="proj_door_left_lit",
                    learning_id="learn_ask_before_expand",
                    learning_type="candidate",
                    learning_rule="Ask before expanding multiple dependent parts.",
                    scope="conductor",
                    evidence_type="feedback_entry",
                    evidence_ref=["fb_ask_before_expand"],
                    evidence_summary=None,
                    occurrence_count=1,
                    promotion_reason=None,
                    mark_review_complete=True,
                    overwrite=False,
                ))

            # 4. Surfaced with rule text at start (learnings-report self-heals).
            report = self._capture(
                artist_os_db.learnings_report,
                argparse.Namespace(**base, project_id="proj_door_left_lit"),
            )
            self.assertIn("Ask before expanding multiple dependent parts.", report)
            self.assertIn("review=complete", report)

            # 5. Tier-2 adoption: local conductor rule, candidate superseded.
            with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                artist_os_db.add_conductor_rule(argparse.Namespace(
                    **base,
                    project_id="proj_door_left_lit",
                    rule="Ask before expanding multiple dependent parts.",
                    from_learning="learn_ask_before_expand",
                ))
            rules_text = (library_root / "conductor-rules.md").read_text(encoding="utf-8")
            self.assertIn("Ask before expanding multiple dependent parts.", rules_text)

            # 6. Status and the event history reflect the whole loop.
            status_out = self._capture(
                artist_os_db.status_projects, argparse.Namespace(**base, project_id=None)
            )
            self.assertIn("review=complete", status_out)
            self.assertIn("fresh", status_out)
            events = [
                json.loads(line)["event_type"]
                for line in (proj_dir / "events.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            for expected in ("feedback_received", "learning_recorded", "conductor_rule_adopted"):
                self.assertIn(expected, events)
            with closing(sqlite3.connect(library_root / "artist-os.sqlite")) as conn:
                indexed_types = {
                    row[0] for row in conn.execute("SELECT event_type FROM events").fetchall()
                }
            self.assertLessEqual(
                {"feedback_received", "learning_recorded", "conductor_rule_adopted"},
                indexed_types,
                "every loop write must be reflected in the index",
            )


if __name__ == "__main__":
    unittest.main()
