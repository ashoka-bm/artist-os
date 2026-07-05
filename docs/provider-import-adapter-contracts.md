# Provider And Import Adapter Contracts

Artist OS remains dry-run first. Provider and import adapters are downstream execution helpers, not planning authority.

## Provider Adapter Boundary

A provider adapter may call an external generator only after `artist_os_adapter_guards.assert_generation_approval(...)` passes for the exact request.

The guard requires:

- `gate_type = "generation_approval"`,
- `gate_status = "approved"`,
- `proceed_unconfirmed = false`,
- matching `project_id`, `source_id`, and `artist_meaning_id`,
- an upstream ref to the exact Prompt Plan, Sound Prompt Plan, Prompt Branch Set, Visual Reference Sheet Plan, Video Medium Plan storyboard package, or approved batch being executed,
- explicit provider, model, and artifact scope named in the approved gate text.

Missing, stale, mismatched, unconfirmed, or merely adjacent approvals are hard failures. A Prompt Lock, Draft Generation Approval, Brief Approval, Output Acceptance, or waiver never authorizes provider-backed generation.

After a provider returns an artifact, the adapter must emit an Output Record with:

- `origin.origin_type = "provider_generated"`,
- `origin.generation_approval_ref` pointing at the matching Generation Approval Gate,
- provider/model/settings/cost metadata in `generation`,
- lineage back to Artist Meaning, Transformation Brief, Beat Plan, Medium Plan, Brief, and Prompt Plan or equivalent approved planning record.

## Import Adapter Boundary

An import adapter records an artifact the artist already owns or edited. It does not call a provider and does not require Generation Approval.

The guard `artist_os_adapter_guards.assert_import_output_record(...)` requires:

- `origin.origin_type = "artist_imported"` or `"human_edited"`,
- `origin.generation_approval_ref = null`,
- all provider generation metadata null, with empty `generation.settings`,
- `previous_output_record_id` when the artifact is a `human_edited` revision.

Imported artifacts still need normal Output Critic Review and Output Acceptance before they become accepted work.
