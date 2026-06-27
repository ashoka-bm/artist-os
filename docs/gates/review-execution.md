# Review Execution And Blocking Findings

## Review Execution Rule

All review stages are mandatory bounded sub-agent reviews.

The creating agent must not self-review its own Story, Medium, Prompt, or Output review stage. It must pass a narrow review packet to the reviewer sub-agent and apply blocking findings before advancing unless the artist explicitly waives the block.

Every critic and reviewer must check for drift. Drift means the artifact has moved away from the governing upstream material: the Reference, Artist Meaning, Transformation Brief, Beat Plan, Medium Plan, Prompt Plan, Text Generation Plan, or approved prior output. Reviewers should identify what the artifact drifted from, where the drift appears, whether it is harmful or artist-approved, and the smallest revision that restores alignment.

Reviewer sub-agents receive:

- review mode or critic role,
- artifact under review,
- Artist Meaning,
- Source Record or Reference summary when needed,
- Beat Plan when relevant,
- Medium Plan, Prompt Plan, or Text Generation Plan when relevant,
- open questions,
- desired output format.

Reviewer sub-agents return a Review Record that validates against `schemas/review-record.schema.json`.

If the host cannot spawn a sub-agent or the active tool policy blocks spawning despite Standing Sub-Agent Authorization, the conductor may use a fallback separated review pass. The fallback must be clearly labeled, use only the same bounded review packet, keep `reviewer_execution.sub_agent_required: true`, set `reviewer_execution.execution_mode: fallback_separated_pass`, and record `reviewer_execution.fallback_reason` as either `host_cannot_spawn_sub_agent` or `tool_policy_blocks_sub_agent_spawn`. This records that the sub-agent requirement still exists even though the workflow is running in degraded mode.

The Review Record is the machine-readable output of the review stage. It must include:

- `review_record_id`,
- `project_id`,
- `review_role`,
- `reviewer_execution.execution_mode`: `bounded_sub_agent`, or `fallback_separated_pass` only when sub-agents are unavailable or blocked by host/tool policy despite Standing Sub-Agent Authorization,
- `reviewer_execution.sub_agent_required: true`,
- `reviewer_execution.source_skill`,
- `reviewer_execution.fallback_reason`: required only for `fallback_separated_pass`; forbidden for `bounded_sub_agent`,
- `artifact_under_review`,
- `upstream_context`,
- `emotional_tension_review`,
- `matched`,
- `drifted`,
- `findings`,
- `recommended_revision`,
- `approval_status`: `approve`, `revise`, or `block`,
- `artist_waiver` when a waiver exists,
- `created_at`.

The reviewer may also return a revised brief, revision prompt, or taste memory note when the caller needs one, but that companion output never replaces the Review Record.

## Blocking Findings

A reviewer returns `block` when proceeding would violate Artist Meaning, provider boundaries, provenance, story approval, method authority, or medium readiness.

Unapproved harmful drift is a blocking finding when it changes Artist Meaning, breaks must-preserve constraints, invents unsupported material, violates rights constraints, or makes the output target a different work than the one approved.

Only the artist can waive a blocking finding. If waived, record the waiver in the project event log with the reason.
