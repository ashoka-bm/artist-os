# Subagent Orchestration

Artist OS may use subagents to save main-thread context and wall-clock time, but subagents never share pipeline authority with the conductor.

This document defines the runtime contract for delegated work. It applies to required reviewer subagents, optional planning workers, parallel production workers, validators, and record-building helpers.

## Core Rule

Subagents may analyze, draft, validate, critique, or prepare disposable work packets.

Artist OS has standing user authorization to spawn bounded internal subagents automatically for mandatory reviews, validation, drafting passes, audits, and approved orchestration patterns. Do not ask for separate approval before each subagent.

This standing authorization only governs internal worker delegation. It never authorizes provider-backed generation, uploads, paid actions, destructive actions, artist-facing gate approvals, waivers, or output acceptance.

Only the conductor may:

- ask artist-facing gate or Decision Interview questions,
- record artist approvals, selections, waivers, or refusals,
- persist authoritative project records,
- advance the current pipeline phase,
- mutate `project.json`, `events.jsonl`, gate files, stewardship records, or SQLite indexes,
- call providers, upload files, spend money, or start irreversible actions.

If a subagent finds a needed artist decision, it returns `open_questions` for the conductor. It does not ask the artist directly.

## Orchestration Modes

Choose the lightest orchestration mode that protects provenance and quality.

Small projects should move quickly. Do not add fanout, blind verification, outside voices, or multi-specialist reviews when a single bounded worker or the mandatory reviewer is enough. Outside voices are independent review workers or external tools whose recommendations are informational until the conductor reduces them and, when needed, presents a decision to the artist. Larger projects, cumulative work, release packages, branch sets, and high-risk outputs should use more regular worker waves because the cost of drift, missed constraints, and context rot is higher.

Use this scale guide, aligned with `workflow_scale_routing` where applicable:

| Scale / scope | Examples | Delegation posture |
| --- | --- | --- |
| `compact_artifact` | single image, short poem, one prompt plan, one small text draft | Use mandatory reviewers and at most one or two prep workers when useful. Avoid fanout by default. |
| `structured_single_artifact` | article, essay, short story, video storyboard, single song with lyrics | Use Standard Orchestration, focused audits, and one critic per required stage. Add specialist checks only for real risk. |
| `cumulative_work` or `full_long_form_project` | image series, multi-section text, track sequence, chapter/scene set | Use Parallel Production after gates allow expansion. Add stewardship, artifact-per-worker execution, and readiness audits. |
| release package route | Album workflow; approved units inside the currently active medium of a general package | Use regular worker waves, specialist review fanout, reduction, calibration checks, and artifact-per-worker status reporting without running primary and supporting media simultaneously. |

### Standard Orchestration

Use this for compact single-output work: one image, one text plan, one sound prompt plan, or one video storyboard package.

The conductor runs the typed pipeline in order. Subagents are used for mandatory reviews and narrowly scoped prep work, but each phase still passes through validation, persistence, and any required gate before the next phase begins.

Good standard-mode parallel work:

- Source Record support: metadata notes, rights/privacy flags, evidence extraction, formal observations.
- Story prep: Story Mode candidates, structure candidates, beat-risk notes.
- Medium prep: candidate symbol sets, style tensions, sonic options, text-form options, shot-logic options.
- Validation: schema/path/readiness checks against a frozen draft packet.

### Parallel Production

Use this only when the approved project has independent units that can be worked without changing each other's authority.

Parallel Production may activate for:

- Prompt Variant Plans such as Faithful, Amplified, and Minimal,
- Prompt Branch Set branches,
- approved image series roles after Series Plan and calibration gates allow expansion,
- approved sound sequence parts after the Sequence Approval Gate and calibration gates allow expansion,
- Album v1 or release-package deliverables after package approval and relevant calibration subchecks,
- independent text sections, image roles, tracks, storyboard stills, or outputs when Long-Work Stewardship marks them ready,
- independent units inside the currently active medium of an approved general
  Cross-Medium package.

Do not activate Parallel Production merely because multiple media are
mentioned. General Cross-Medium production is sequential in 1.0: parallelism
may occur inside the currently active medium, but the primary and supporting
medium journeys do not execute simultaneously. Album retains its existing
package-specific parallelism after package approval and relevant calibration
subchecks.

## Wave Model

Parallel work happens in waves. Each wave consumes a frozen input packet and returns draft outputs for conductor integration.

```text
Freeze input packet
  -> dispatch eligible subagents
  -> collect outputs
  -> reconcile into one candidate stage output
  -> validate schemas or review records
  -> persist authoritative state
  -> ask the next required gate question, or advance
```

The conductor must not advance while worker results are still unresolved if those results are required for the current stage.

## Delegation Packet

Every delegated task should receive a bounded packet:

```json
{
  "task_id": "image.prompt_variant.faithful",
  "orchestration_mode": "parallel_production",
  "phase": "image.prompt_plan",
  "role": "variant_worker",
  "mode": "draft_only",
  "upstream_records": {
    "source_record_id": "source_...",
    "artist_meaning_id": "meaning_...",
    "transformation_brief_id": "tb_...",
    "beat_plan_id": "beat_...",
    "medium_plan_id": "image_medium_...",
    "creative_brief_id": "brief_..."
  },
  "input_paths": [],
  "allowed_outputs": [
    "draft_artifact",
    "traceability_notes",
    "risk_notes",
    "open_questions"
  ],
  "forbidden_actions": [
    "do_not_ask_artist",
    "do_not_record_gate_decisions",
    "do_not_persist_authoritative_state",
    "do_not_mutate_project_manifest_or_events",
    "do_not_call_providers",
    "do_not_generate_media"
  ],
  "return_format": "subagent_result"
}
```

Delegation Packets validate against `schemas/delegation-packet.schema.json`.
Use exact upstream record ids and paths whenever they exist. Workers must cite the upstream ids they used so the conductor can detect stale packets.

## Subagent Result

Subagents return one compact result:

```json
{
  "task_id": "image.prompt_variant.faithful",
  "status": "complete",
  "upstream_records_used": {
    "beat_plan_id": "beat_...",
    "medium_plan_id": "image_medium_...",
    "creative_brief_id": "brief_..."
  },
  "draft_artifact": {},
  "findings": [],
  "finding_fingerprints": [
    {
      "artifact_id": "...",
      "location_or_field": "...",
      "upstream_rule": "...",
      "claimed_drift": "..."
    }
  ],
  "confidence": "medium",
  "traceability_notes": [],
  "risk_notes": [],
  "open_questions": [],
  "validation_notes": [],
  "recommended_next_action": "integrate"
}
```

Subagent Results validate against `schemas/subagent-result.schema.json`.

Valid statuses are:

- `complete`
- `needs_conductor_decision`
- `blocked_by_missing_input`
- `blocked_by_policy`
- `invalid_upstream_packet`
- `failed`
- `rate_limited`

Valid `confidence` values are:

- `low`
- `medium`
- `high`

Worker `confidence` is local to that worker result. The conductor may compute an aggregate confidence during reduction, but it must not rewrite the worker's reported confidence in place.

Valid `recommended_next_action` values are:

- `integrate`: use the result in conductor-side synthesis.
- `revise_packet`: repair or resend the delegated packet before using the result.
- `escalate_open_questions`: present or resolve `open_questions` before continuing.
- `discard`: do not use this result.

When `status` is not `complete`, the conductor must not treat `recommended_next_action` as approval to advance. Status is authoritative; the next action is advisory.

Workers that return `findings` should return one `finding_fingerprints` entry per finding. Each fingerprint uses this composite key:

- `artifact_id`
- `location_or_field`
- `upstream_rule`
- `claimed_drift`

When a worker cannot compute a fingerprint, the conductor computes it before reduction.

Reviewer subagents still return `Review Record` objects that validate against `schemas/review-record.schema.json`. A reviewer may include a companion revision, but the Review Record remains the authority.

## Worker Roles

Use reusable worker roles instead of creating permanent personalities.

| Role | Use |
| --- | --- |
| `evidence_worker` | Extract evidence, formal observations, rights/privacy risks, and reference facts. |
| `story_candidate_worker` | Draft Story Mode or Beat Plan candidates from approved meaning. |
| `medium_analysis_worker` | Prepare medium-local options, tensions, style/structure conflicts, or readiness notes. |
| `variant_worker` | Draft one Prompt Variant Plan from an approved brief and medium plan. |
| `branch_worker` | Draft one Prompt Branch Set branch from an approved meaning kernel. |
| `record_builder` | Draft schema-backed records after required gates are complete. |
| `schema_validator` | Check a draft record against the relevant schema and report errors. |
| `critic_worker` | Run a bounded review and emit a Review Record. |
| `blind_verifier` | Independently verify a candidate finding from minimal context without seeing the first critic's reasoning. |
| `audit_worker` | Check phase completion, provenance completeness, prompt-lock readiness, storage consistency, or doc drift. |
| `reduction_worker` | Help cluster, fingerprint, and summarize multiple worker outputs for conductor review. |
| `output_record_worker` | Draft an Output Record for a concrete generated, imported, drafted, rewritten, or edited artifact. |

## Specialist Fanout

Use specialist fanout only when the project scale or risk justifies it. A compact project should not pay the overhead of a review army unless there is a specific concern.

Good fanout triggers:

- cumulative or release-package work,
- high-risk rights, privacy, source-wording, or safety constraints,
- conflicting critic findings,
- many branches, variants, tracks, sections, or outputs,
- artist-requested rigor before locking a plan.

Possible specialist lenses, assigned to the canonical reviewer roles in `docs/gates-and-reviews.md`:

- meaning drift,
- emotional tension,
- provenance,
- schema / contract,
- medium-specific fit,
- style drift for image or video,
- source-wording / rights for text, lyrics, or audio.

Each specialist gets a narrow checklist and a frozen packet. Specialists do not debate each other. The conductor reduces their outputs into one decision packet, Review Record, or artist-facing question.

## Reduction And Verification

When multiple workers return findings, the conductor must reduce them before changing the authoritative artifact.

Reduction rules:

- group findings by worker-supplied or conductor-computed fingerprint,
- dedupe repeated findings,
- preserve minority findings when they identify a distinct risk,
- raise aggregate confidence when independent workers identify the same issue from separate packets,
- let blocking provenance, approval, provider-boundary, or schema findings override style or preference recommendations,
- convert unresolved conflicts into conductor decisions or artist-facing questions.

Do not automatically apply outside-voice or specialist recommendations. Treat them as evidence for the conductor to integrate, revise, verify, or present to the artist.

Use blind verification for serious candidate findings when false positives would slow the artist or false negatives would damage provenance. The verifier receives only the artifact location, upstream records, the rule being checked, and the desired output format. It does not receive the first critic's reasoning.

Use fresh-context audit workers for:

- provenance completeness,
- schema validation,
- phase-completion checks,
- prompt-lock readiness,
- output-record completeness,
- Long-Work Readiness and checkpoint consistency,
- storage and doc-drift checks.

Audit workers return final structured results only. Handle malformed or incomplete audit results under Failure And Degradation.

## Failure And Degradation

Subagent failure must be explicit.

- Required reviewer failure: retry once if practical; if the host or tool policy blocks spawning despite Standing Sub-Agent Authorization, use the documented fallback separated review pass and record degraded execution.
- Optional prep-worker failure: continue without it when the conductor has enough context.
- Parallel Production worker failure: report the failed unit, continue only for independent successful units, and do not pretend the missing unit exists.
- Malformed structured output: ask the worker to repair once, then mark `failed`. Do not use the fallback separated review pass unless the host or tool policy blocks sub-agent spawning despite Standing Sub-Agent Authorization.
- Rate limits: mark `rate_limited`; the conductor may retry later or switch to sequential execution if the unit remains needed.

Partial fanout results are acceptable only when the missing workers are not required for the current gate, record, or output. Required critics, approval gates, schema validation, Output Records, and provider-boundary checks cannot be silently skipped.

## Artifact-Per-Worker

In Parallel Production, assign one worker per independent artifact or unit whenever possible.

Each artifact worker owns:

- one branch, variant, image role, text section, track, cover, storyboard still, or output,
- local retry or repair within the allowed packet,
- local verification that its returned artifact exists or validates enough for conductor review,
- a final status: `complete`, `failed`, `rate_limited`, `blocked_by_missing_input`, or `blocked_by_policy`.

This artifact status list is narrower than the general Subagent Result status list because it reports the final state of one artifact unit. General packet-level statuses such as `needs_conductor_decision` and `invalid_upstream_packet` remain valid for non-artifact workers.

The conductor collects artifact statuses, promotes only verified units into authoritative state, and surfaces missing or failed units before any artist approval that would imply the set is complete.

## Safe Parallelism

Parallelize only when worker outputs do not depend on each other.

Safe examples:

- three prompt variants drafted from the same approved Creative Brief,
- five Prompt Branch Set branches drafted from the same approved meaning kernel,
- independent album cover and track-prompt prep after relevant calibration approval,
- independent Output Critic Reviews for independent outputs,
- evidence extraction and rights-risk scan from the same Reference.

Unsafe examples:

- critiquing a draft before that draft exists,
- running Story Critic before Beat Reviewer when Story Critic must consume the Beat Review Record,
- running Style locking before Symbology locking in image or visual video planning,
- drafting final records before Brief Approval,
- expanding a cumulative series while Long-Work Readiness is `pending` or `repair_before_expansion`,
- allowing any worker to write `project.json`, `events.jsonl`, gate files, stewardship records, sidecars, or SQLite.

## Synchronization Barriers

The conductor must stop and synchronize at these barriers:

- schema validation after every record-producing step,
- persistence before phase advancement,
- explicit artist gates, approvals, selections, and waivers,
- Review Record integration and blocking-finding resolution,
- Story Approval before medium locking,
- Brief Approval before final records or prompt plans,
- Prompt Lock before generation, drafting, or export,
- Generation Approval before provider calls,
- Output Record before Output Critic Review or Output Acceptance,
- Long-Work Readiness and checkpoints before multi-part expansion,
- serialized writes to manifest, events, gate files, stewardship records, sidecars, and SQLite.

## Disposable Work

Workers may write disposable files only under `.tmp/artist-os/<task_id>/` when a host requires file output. Disposable files are not project state and must not be treated as resume authority.

The conductor may promote useful worker output by copying the reconciled result into the Workspace Library through the normal persistence path.

## Pressure Checks

Use these checks when reviewing orchestration changes:

1. If a worker asks the artist for approval, the design fails.
2. If a worker records a gate decision or waiver, the design fails.
3. If two workers can write the same project state file, the design fails.
4. If a draft can be critiqued before it exists, the design fails.
5. If the conductor can advance without validating and persisting the authoritative record, the design fails.
6. If provider approval for one call authorizes another call or batch by implication, the design fails.
7. If Parallel Production bypasses Story Approval, Brief Approval, Prompt Lock, Long-Work Readiness, or Output Records, the design fails.
8. If the conductor can advance while required worker results are unresolved, the design fails.
9. If an outside-voice or specialist recommendation changes an authoritative artifact without conductor reduction and any required artist gate, the design fails.
