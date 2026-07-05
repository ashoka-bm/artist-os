from __future__ import annotations

import unittest
from dataclasses import replace

from artist_os_adapter_guards import (
    AdapterGuardError,
    ProviderGenerationRequest,
    assert_generation_approval,
    assert_import_output_record,
    assert_provider_output_record,
)
from artist_os_schema_validator import REPO_ROOT, load_json


def fixture(path: str) -> dict:
    return load_json(REPO_ROOT / path)


REQUEST = ProviderGenerationRequest(
    project_id="proj_door_left_lit",
    source_id="src_door_left_lit",
    artist_meaning_id="meaning_door_left_lit",
    upstream_ref_type="prompt_branch_set",
    upstream_ref_id="pbs_door_left_lit_image_batch",
    provider="example-provider",
    model="example-image-model",
    artifact_scope="branch_empty_station faithful image",
)


class AdapterGuardTests(unittest.TestCase):
    def test_generation_approval_accepts_exact_scope(self) -> None:
        gate = fixture("tests/fixtures/gates/image-generation-approval-gate.json")
        assert_generation_approval(gate, REQUEST)

    def test_generation_approval_rejects_prompt_lock_gate(self) -> None:
        gate = fixture("tests/fixtures/gates/image-prompt-lock-gate.json")
        with self.assertRaisesRegex(AdapterGuardError, "generation_approval"):
            assert_generation_approval(gate, REQUEST)

    def test_generation_approval_rejects_mismatched_upstream_ref(self) -> None:
        gate = fixture("tests/fixtures/gates/image-generation-approval-gate.json")
        request = replace(REQUEST, upstream_ref_id="pbs_wrong")
        with self.assertRaisesRegex(AdapterGuardError, "does not reference"):
            assert_generation_approval(gate, request)

    def test_generation_approval_rejects_mismatched_provider(self) -> None:
        gate = fixture("tests/fixtures/gates/image-generation-approval-gate.json")
        request = replace(REQUEST, provider="other-provider")
        with self.assertRaisesRegex(AdapterGuardError, "provider"):
            assert_generation_approval(gate, request)

    def test_generation_approval_rejects_unconfirmed_gate(self) -> None:
        gate = fixture("tests/fixtures/gates/image-generation-approval-gate.json")
        gate["proceed_unconfirmed"] = True
        with self.assertRaisesRegex(AdapterGuardError, "unconfirmed"):
            assert_generation_approval(gate, REQUEST)

    def test_provider_output_record_must_point_at_matching_gate(self) -> None:
        gate = fixture("tests/fixtures/gates/image-generation-approval-gate.json")
        output = fixture("tests/fixtures/outputs/output-record.json")
        assert_provider_output_record(output, REQUEST, gate)

        output["origin"]["generation_approval_ref"] = "gate_wrong"
        with self.assertRaisesRegex(AdapterGuardError, "generation approval"):
            assert_provider_output_record(output, REQUEST, gate)

    def test_import_output_record_rejects_provider_metadata(self) -> None:
        output = fixture("tests/fixtures/outputs/output-record.json")
        output["origin"]["origin_type"] = "artist_imported"
        output["origin"]["generation_approval_ref"] = None
        with self.assertRaisesRegex(AdapterGuardError, "generation.provider"):
            assert_import_output_record(output)

    def test_import_output_record_accepts_artist_import_without_generation(self) -> None:
        output = fixture("tests/fixtures/outputs/output-record.json")
        output["origin"] = {
            "origin_type": "artist_imported",
            "created_by": "artist",
            "generation_approval_ref": None,
        }
        output["generation"] = {
            "provider": None,
            "model": None,
            "settings": {},
            "seed": None,
            "estimated_cost": None,
            "actual_cost": None,
        }
        assert_import_output_record(output)

    def test_human_edited_import_requires_previous_output_record(self) -> None:
        output = fixture("tests/fixtures/outputs/output-record.json")
        output["origin"] = {
            "origin_type": "human_edited",
            "created_by": "artist",
            "generation_approval_ref": None,
        }
        output["generation"] = {
            "provider": None,
            "model": None,
            "settings": {},
            "seed": None,
            "estimated_cost": None,
            "actual_cost": None,
        }
        output["previous_output_record_id"] = None
        with self.assertRaisesRegex(AdapterGuardError, "previous Output Record"):
            assert_import_output_record(output)


if __name__ == "__main__":
    unittest.main()
