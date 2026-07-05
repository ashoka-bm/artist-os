from __future__ import annotations

import unittest

from artist_os_schema_validator import REPO_ROOT, ValidationError, load_json, validate, validate_file


class SubagentOrchestrationContractTests(unittest.TestCase):
    def test_delegation_packet_fixture_validates(self) -> None:
        validate_file(
            REPO_ROOT / "schemas" / "delegation-packet.schema.json",
            REPO_ROOT / "tests" / "fixtures" / "subagent" / "delegation-packet.json",
        )

    def test_subagent_result_fixture_validates(self) -> None:
        validate_file(
            REPO_ROOT / "schemas" / "subagent-result.schema.json",
            REPO_ROOT / "tests" / "fixtures" / "subagent" / "subagent-result.complete.json",
        )

    def test_subagent_result_rejects_missing_status(self) -> None:
        schema = load_json(REPO_ROOT / "schemas" / "subagent-result.schema.json")
        record = load_json(REPO_ROOT / "tests" / "fixtures" / "subagent" / "subagent-result.complete.json")
        del record["status"]

        with self.assertRaisesRegex(ValidationError, "missing required field 'status'"):
            validate(record, schema, schema)

    def test_subagent_result_rejects_unknown_status(self) -> None:
        schema = load_json(REPO_ROOT / "schemas" / "subagent-result.schema.json")
        record = load_json(REPO_ROOT / "tests" / "fixtures" / "subagent" / "subagent-result.complete.json")
        record["status"] = "maybe_done"

        with self.assertRaisesRegex(ValidationError, "not one of"):
            validate(record, schema, schema)

    def test_delegation_packet_rejects_unknown_forbidden_action(self) -> None:
        schema = load_json(REPO_ROOT / "schemas" / "delegation-packet.schema.json")
        packet = load_json(REPO_ROOT / "tests" / "fixtures" / "subagent" / "delegation-packet.json")
        packet["forbidden_actions"].append("do_not_improvise_new_authority")

        with self.assertRaisesRegex(ValidationError, "not one of"):
            validate(packet, schema, schema)

    def test_schema_enums_match_documented_contract_tokens(self) -> None:
        text = (REPO_ROOT / "docs" / "subagent-orchestration.md").read_text(encoding="utf-8")
        result_schema = load_json(REPO_ROOT / "schemas" / "subagent-result.schema.json")
        packet_schema = load_json(REPO_ROOT / "schemas" / "delegation-packet.schema.json")

        for token in result_schema["$defs"]["status"]["enum"]:
            self.assertIn(f"`{token}`", text)
        for token in result_schema["$defs"]["recommended_next_action"]["enum"]:
            self.assertIn(f"`{token}`", text)
        for token in packet_schema["$defs"]["forbidden_action"]["enum"]:
            self.assertIn(f'"{token}"', text)
        self.assertIn("Status is authoritative", text)


if __name__ == "__main__":
    unittest.main()
