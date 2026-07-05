"""Guard helpers for future Artist OS provider and import adapters.

These helpers do not call providers or touch files. They make the approval and
provenance checks reusable so adapters can fail before any paid or external
action happens.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class AdapterGuardError(ValueError):
    """Raised when an adapter request violates Artist OS boundary rules."""


@dataclass(frozen=True)
class ProviderGenerationRequest:
    project_id: str
    source_id: str
    artist_meaning_id: str
    upstream_ref_type: str
    upstream_ref_id: str
    provider: str
    model: str
    artifact_scope: str


def _approval_text(gate_decision: dict[str, Any]) -> str:
    parts: list[str] = [
        str(gate_decision.get("decision", "")),
        str(gate_decision.get("artist_response", "")),
        str(gate_decision.get("selected_option", {}).get("label", "")),
    ]
    for option in gate_decision.get("options_presented", []):
        parts.append(str(option.get("label", "")))
        parts.append(str(option.get("summary", "")))
    return " ".join(parts).lower()


def assert_generation_approval(
    gate_decision: dict[str, Any],
    request: ProviderGenerationRequest,
) -> None:
    """Require an exact approved Generation Approval gate for a provider request.

    The current GateDecision schema keeps provider/model/scope in the human
    decision text rather than separate fields, so this guard requires those
    tokens to appear in the approved gate text and the upstream reference to
    match structurally.
    """
    if gate_decision.get("gate_type") != "generation_approval":
        raise AdapterGuardError("provider generation requires a generation_approval gate")
    if gate_decision.get("gate_status") != "approved":
        raise AdapterGuardError("generation approval gate is not approved")
    if gate_decision.get("proceed_unconfirmed") is not False:
        raise AdapterGuardError("generation approval cannot proceed unconfirmed")

    for field in ["project_id", "source_id", "artist_meaning_id"]:
        if gate_decision.get(field) != getattr(request, field):
            raise AdapterGuardError(f"generation approval {field} does not match request")

    upstream_refs = {
        (ref.get("ref_type"), ref.get("ref_id"))
        for ref in gate_decision.get("upstream_refs", [])
    }
    expected_ref = (request.upstream_ref_type, request.upstream_ref_id)
    if expected_ref not in upstream_refs:
        raise AdapterGuardError("generation approval does not reference the requested plan or batch")

    approval_text = _approval_text(gate_decision)
    for label, value in (
        ("provider", request.provider),
        ("model", request.model),
        ("artifact scope", request.artifact_scope),
    ):
        if value.lower() not in approval_text:
            raise AdapterGuardError(f"generation approval does not name requested {label}")


def assert_provider_output_record(
    output_record: dict[str, Any],
    request: ProviderGenerationRequest,
    gate_decision: dict[str, Any],
) -> None:
    """Verify a returned provider artifact can be recorded as an Output Record."""
    assert_generation_approval(gate_decision, request)

    if output_record.get("project_id") != request.project_id:
        raise AdapterGuardError("output record project_id does not match request")
    if output_record.get("source_id") != request.source_id:
        raise AdapterGuardError("output record source_id does not match request")
    if output_record.get("artist_meaning_id") != request.artist_meaning_id:
        raise AdapterGuardError("output record artist_meaning_id does not match request")

    origin = output_record.get("origin", {})
    if origin.get("origin_type") != "provider_generated":
        raise AdapterGuardError("provider adapter must emit origin_type provider_generated")
    if origin.get("generation_approval_ref") != gate_decision.get("gate_decision_id"):
        raise AdapterGuardError("output record must point at the matching generation approval gate")

    generation = output_record.get("generation", {})
    if generation.get("provider") != request.provider:
        raise AdapterGuardError("output record provider does not match request")
    if generation.get("model") != request.model:
        raise AdapterGuardError("output record model does not match request")


def assert_import_output_record(output_record: dict[str, Any]) -> None:
    """Verify an imported or human-edited artifact keeps non-provider provenance."""
    origin = output_record.get("origin", {})
    origin_type = origin.get("origin_type")
    if origin_type not in {"artist_imported", "human_edited"}:
        raise AdapterGuardError("import adapter must emit artist_imported or human_edited output")
    if origin.get("generation_approval_ref") is not None:
        raise AdapterGuardError("imported and human-edited outputs must not use generation approval")

    generation = output_record.get("generation", {})
    for field in ["provider", "model", "seed", "estimated_cost", "actual_cost"]:
        if generation.get(field) is not None:
            raise AdapterGuardError(f"imported output must not set generation.{field}")
    if generation.get("settings") != {}:
        raise AdapterGuardError("imported output generation.settings must be empty")

    if origin_type == "human_edited" and not output_record.get("previous_output_record_id"):
        raise AdapterGuardError("human-edited output revisions must reference the previous Output Record")
