from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path

from artist_os_schema_validator import validate_file


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "release-evidence" / "1.0.0" / "manifest.json"
RUN_PATH = REPO_ROOT / "release-evidence" / "1.0.0" / "rehearsal-run.json"
EXPECTED_JOURNEYS = {
    "image",
    "video_v0",
    "audio",
    "text",
    "album_v1",
    "cross_medium",
}
REQUIRED_KINDS = {
    "image": {"source_record", "artist_meaning", "transformation_brief", "beat_plan", "image_medium_plan", "creative_brief", "prompt_plan"},
    "video_v0": {"source_record", "artist_meaning", "transformation_brief", "beat_plan", "video_medium_plan"},
    "audio": {"source_record", "artist_meaning", "transformation_brief", "beat_plan", "sound_medium_plan", "sound_creative_brief", "sound_prompt_plan"},
    "text": {"source_record", "artist_meaning", "transformation_brief", "beat_plan", "text_medium_plan", "text_creative_brief", "text_generation_plan"},
    "album_v1": {"source_record", "artist_meaning", "transformation_brief", "long_work_stewardship", "release_package_plan", "pre_calibration_review", "release_package_plan_approval", "sound_medium_plan", "image_medium_plan", "album_calibration"},
    "cross_medium": {"cross_medium_plan", "mixed_media_review", "cross_medium_plan_approval", "package_completeness_gate", "asset_package"},
}


class ReleaseEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        cls.run_record = json.loads(RUN_PATH.read_text(encoding="utf-8"))

    def test_manifest_records_all_six_passing_dry_run_journeys(self) -> None:
        self.assertEqual(self.manifest["release_version"], "1.0.0")
        self.assertFalse(self.manifest["provider_calls_made"])
        rehearsals = self.manifest["rehearsals"]
        self.assertEqual({entry["journey"] for entry in rehearsals}, EXPECTED_JOURNEYS)
        self.assertTrue(all(entry["result"] == "passed" for entry in rehearsals))

    def test_rehearsal_run_records_the_executed_verification(self) -> None:
        self.assertEqual(self.manifest["rehearsal_run"], str(RUN_PATH.relative_to(REPO_ROOT)))
        self.assertEqual(self.run_record["release_version"], "1.0.0")
        self.assertEqual(self.run_record["release_ref"], "v1.0.0")
        self.assertEqual(self.run_record["result"], "passed")
        self.assertEqual(self.run_record["command_exit_status"], 0)
        self.assertFalse(self.run_record["provider_calls_made"])
        self.assertEqual(set(self.run_record["journeys"]), EXPECTED_JOURNEYS)
        self.assertGreater(self.run_record["tests_run"], 0)
        observed_digest = hashlib.sha256(
            self.run_record["observed_output"].encode()
        ).hexdigest()
        self.assertEqual(self.run_record["observed_output_sha256"], observed_digest)

        command_modules = set(self.run_record["command"])
        for rehearsal in self.manifest["rehearsals"]:
            for supporting_test in rehearsal["supporting_tests"]:
                module = supporting_test.removesuffix(".py").replace("/", ".")
                self.assertIn(module, command_modules)

        unique_paths = sorted(
            {
                record["path"]
                for rehearsal in self.manifest["rehearsals"]
                for record in rehearsal["records"]
            }
        )
        digest_lines = []
        for relative in unique_paths:
            digest = hashlib.sha256((REPO_ROOT / relative).read_bytes()).hexdigest()
            digest_lines.append(f"{digest}  {relative}\n")
        record_set_digest = hashlib.sha256("".join(digest_lines).encode()).hexdigest()
        record_count = sum(len(item["records"]) for item in self.manifest["rehearsals"])
        self.assertEqual(self.run_record["record_entries"], record_count)
        self.assertEqual(self.run_record["unique_records"], len(unique_paths))
        self.assertEqual(self.run_record["record_set_sha256"], record_set_digest)

        tracked = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
        ).stdout
        source_lines = []
        for raw_path in sorted(value for value in tracked.split(b"\0") if value):
            relative = raw_path.decode()
            if relative.startswith("release-evidence/1.0.0/"):
                continue
            digest = hashlib.sha256((REPO_ROOT / relative).read_bytes()).hexdigest()
            source_lines.append(f"{digest}  {relative}\n")
        source_digest = hashlib.sha256("".join(source_lines).encode()).hexdigest()
        self.assertEqual(self.run_record["source_surface_sha256"], source_digest)

    def test_every_evidence_record_exists_and_validates(self) -> None:
        for rehearsal in self.manifest["rehearsals"]:
            with self.subTest(journey=rehearsal["journey"]):
                kinds = {record["kind"] for record in rehearsal["records"]}
                self.assertTrue(REQUIRED_KINDS[rehearsal["journey"]].issubset(kinds))
                for record in rehearsal["records"]:
                    validate_file(REPO_ROOT / record["schema"], REPO_ROOT / record["path"])
                for supporting_test in rehearsal["supporting_tests"]:
                    self.assertTrue((REPO_ROOT / supporting_test).is_file())

    def test_every_rehearsal_output_is_represented_by_an_output_record(self) -> None:
        for rehearsal in self.manifest["rehearsals"]:
            listed = {record["path"]: record for record in rehearsal["records"]}
            for output_path in rehearsal["concrete_output_records"]:
                with self.subTest(journey=rehearsal["journey"], output=output_path):
                    self.assertEqual(listed[output_path]["schema"], "schemas/output-record.schema.json")
                    output = json.loads((REPO_ROOT / output_path).read_text(encoding="utf-8"))
                    self.assertIn("output_artifact", output)

    def test_album_lineage_reaches_the_approved_album_beat_authority(self) -> None:
        album = next(
            item for item in self.manifest["rehearsals"] if item["journey"] == "album_v1"
        )
        records = {
            item["kind"]: json.loads((REPO_ROOT / item["path"]).read_text(encoding="utf-8"))
            for item in album["records"]
        }
        package = records["release_package_plan"]
        stewardship = records["long_work_stewardship"]
        self.assertEqual(package["source_id"], records["source_record"]["source_id"])
        self.assertEqual(
            package["artist_meaning_id"],
            records["artist_meaning"]["artist_meaning_id"],
        )
        self.assertEqual(
            package["transformation_brief_id"],
            records["transformation_brief"]["transformation_brief_id"],
        )
        self.assertEqual(stewardship["beat_plan_id"], package["album_beat_plan_id"])

    def test_complete_packages_reference_only_recorded_accepted_outputs(self) -> None:
        for rehearsal in self.manifest["rehearsals"]:
            package_path = rehearsal.get("asset_package")
            if not package_path:
                continue
            outputs = {}
            for output_path in rehearsal["concrete_output_records"]:
                output = json.loads((REPO_ROOT / output_path).read_text(encoding="utf-8"))
                outputs[output["output_record_id"]] = output
            package = json.loads((REPO_ROOT / package_path).read_text(encoding="utf-8"))
            self.assertEqual(package["status"], "complete")
            for slot in package["slots"]:
                if slot["completeness"] == "filled":
                    output = outputs[slot["output_record_id"]]
                    self.assertTrue(output["acceptance_state"]["accepted_work"])
                    self.assertEqual(output["acceptance_state"]["output_acceptance_status"], "accepted")


if __name__ == "__main__":
    unittest.main()
