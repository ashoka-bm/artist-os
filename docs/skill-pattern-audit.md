<!-- Generated 2026-06-26 by the agentic-skill-patterns auditor (artist-os-pattern-audit workflow). Profiled the live repo; every gap survived an adversarial verify pass (0 false gaps). Catalog + evidence: ~/code/personal/agentic-skill-patterns. -->

> **Historical snapshot (2026-06-26).** This report describes the repository at
> the time it was generated. Several findings and counts have since been
> resolved or superseded. Do not use it as current release status; use
> `docs/release-1.0.md` and `docs/progress.md`.

## Audit: Artist OS

Archetype: Conductor / gated-pipeline (+ Stateful-engine; weak third axis: multi-harness-portability)

Artist OS is a single thin public conductor (`skills/artist-os/SKILL.md`) driving a fixed 17-step typed Phase Order through 9 named Hard Gates, dispatching disposable workers via a JSON Delegation Packet / Subagent Result contract. Approval is a deterministic primitive (no inferred approval; never end on "recorded"); reviewers are mandatory, blind, and emit schema-validated Review Records. The recurring conductor weakness the archetype warns about — orchestration staying prose — is exactly Artist OS's open center of gravity: the packet/result contract is prose+JSON-example with no schema, while only the Review Record half of worker I/O is executable.

Every gap below survived adversarial verification (zero false gaps). Two ratings were corrected against the verifier: A14 is the denylist-only half (the "stale count citation" premise is false — no `9 Hard Gates`/`17-step`/`11 roles` literal strings exist to guard), and A9's mechanization delta is smaller than first stated because `review-record.schema.json` already requires `reviewer_execution.source_skill`. Three gaps the verifier surfaced are folded in (A16 AGENTS.md drift, A17 routing sub-route coverage, and the ADR-0011 runtime `review_only` check folded into A6 as a concrete sub-case).

---

### A1. Serialized preflight/gate token in the conductor transcript  (impact: HIGH / effort: LOW)
- Has: 9 named Hard Gates, the Gate Completion Rule ("never complete a gate ... on the artist's behalf", SKILL.md:56), the Continuation Rule, the Autopilot 4-way classifier, and a persisted `GateDecision` record (`schemas/gate-decision.schema.json`).
- Gap: Gate compliance is invisible in the live transcript. The conductor never emits a checkable per-phase state line before a mutating/provider step, so there is no runtime evidence the gate contract was consulted; the `GateDecision` is written after the fact to the workspace library, not in-transcript, so no reviewer/eval reading the conversation can assert on it. A model can self-approve by silently skipping the consult. (Prior A2, still open.)
- Steal: #11 Serialized preflight/gate token from impeccable (`skill/SKILL.md`) + wondermint (pinned-wording assertion) — print one literal serialized state line (`IMPECCABLE_PREFLIGHT: ... mutation=open`) before any edit; the most safety-critical state is valid only after a *separate* user turn, making self-approval structurally unfakeable.
- Apply:
  1. Name the gates as ordered tokens drawn from the existing Shared Gate Order (`routing meaning brief prompt_lock generation_approval output_acceptance`) and fix their order.
  2. Require the conductor to print one line before any provider call or persist-before-advance step, e.g. `ARTIST_OS_GATE: meaning=pass brief=pass prompt_lock=pass generation_approval=open`.
  3. Make `generation_approval`/`brief_approval` flip to `pass` ONLY after a separate artist message (mirror impeccable's shape=pass-after-confirmation); skipped states must carry a real reason.
  4. Add a contract/drift test (alongside `test_gate_enforcement`) pinning the token wording, and extend the conductor-behavior eval-spec to assert the line appears before provider steps.
- Watch out: A gate that defaults to `pass` or is skip-on-missing is no gate at all. The token only helps if a downstream check or human actually reads it — pair the emission with an eval/reviewer assertion or it is just more prose.

### A2. bless command re-hashes SKILL.md without verifying a passing grade  (impact: HIGH / effort: LOW)
- Has: `bin/artist-os-eval` implements the full digest gate — `blessed.lock` pins sha256 of SKILL.md, `is_blessed()`/`cmd_status()` exit 1 on mismatch (RED by design right now), `test_conductor_eval_lock.py` makes it CI-red, and `cmd_start` is heavily guarded (refuses to clobber without `--force`, clears stale traces/grade).
- Gap: `cmd_bless` (lines 104-108) is unguarded — it calls `write_lock(root)` unconditionally. It never checks that a `grade.md` exists, was produced against the CURRENT conductor digest, and records a PASS. An operator can edit SKILL.md, see CI go red, and run `bin/artist-os-eval bless` to turn it green without ever running the token-spending eval. One unguarded bless defeats every start-side guard. (Pattern 12's named watch-out.)
- Steal: #12 Eval re-bless digest gate from artist-os (its own pattern, hardened) — step 3: guard `bless` so it refuses against a missing or stale grade; the grade records both a PASS verdict and the digest it was graded against.
- Apply:
  1. Have `cmd_start` stamp the conductor digest into the scaffolded `grade.md` (e.g. `graded_against_sha256:`).
  2. In `cmd_bless`, before `write_lock`: load the active role's `grade.md`, fail if missing; fail if `graded_against_sha256 != conductor_digest(root)`; fail unless the grade records an overall PASS.
  3. Add a `CliTests` case: editing SKILL.md after a passing grade then `bless` must exit non-zero until a fresh passing grade for the new digest exists.
  4. Update `evals/README.md` to state bless consumes the grade and cannot run without one.
- Watch out: The gate proves the file changed, not that behavior is still correct. Do not let the digest-in-grade check be satisfiable by hand-editing the grade to PASS without re-running — keep human-runs-the-eval as the documented real guarantee.

### A3. Subagent return contract has no schema and fails no test  (impact: HIGH / effort: MED)
- Has: `docs/subagent-orchestration.md` fully defines the Delegation Packet and the Subagent Result envelope with a closed 7-value status enum, a closed confidence enum, and the "status authoritative / recommended_next_action advisory" rule (lines 158-183). The reviewer half is executable (`schemas/review-record.schema.json` + `test_reviewer_skill_contract.py`).
- Gap: The packet/result shapes are prose + a JSON example only. `schemas/` has NO `delegation-packet.schema.json` or `subagent-result.schema.json` (confirmed against all 30 schemas), the validator's `FIXTURE_SCHEMA_MAP` has no entry, and grep of tests/ for `delegation|subagent.result|forbidden_action|status enum` returns zero. A worker returning an out-of-enum status, omitting status, or renaming a forbidden_action passes every CI check. (Prior A1, still fully open; the recent reference-inventory work added executable enforcement everywhere EXCEPT the worker I/O boundary.)
- Steal: #16 Fixed-status implementer return contract from artist-os (own richer enum) / gbrain (allowlist parity) — each worker returns JSON whose status is a small closed enum, one value per controller action; the conductor REJECTS (not coerces) a malformed result; capability surface pinned to one allowlist by a test.
- Apply:
  1. Add `schemas/subagent-result.schema.json` encoding the EXISTING enum verbatim (7-value status, 3-value confidence, 4-value recommended_next_action, `finding_fingerprints` composite key) plus `schemas/delegation-packet.schema.json`; wire both into `FIXTURE_SCHEMA_MAP` exactly like `reference-inventory.json` (validator line ~304).
  2. Add `tests/fixtures/subagent/` golden fixtures (one per status) plus an invalid missing-status fixture, and a `test_schema_validation.py` case asserting valid ones pass and missing-status is rejected.
  3. Add a contract test (sibling to `test_reviewer_skill_contract.py`) pinning the load-bearing tokens (`status is authoritative` + literal enum members) so prose cannot drift from schema.
  4. Derive `forbidden_actions` and the Standing Authorization "never authorizes" list from one source constant pinned by a test (see A4).
- Watch out: Do NOT import superpowers' narrower 4-status set — Artist OS already has a branch-complete enum. The Artifact-Per-Worker status list (line 289) is deliberately narrower than the general list, so the schema must allow both shapes (role-conditioned required-status or a superset), not collapse them.

### A4. Subagent capability surface + forbidden_actions not derived from one test-pinned allowlist  (impact: HIGH / effort: MED)
- Has: `docs/subagent-orchestration.md` defines the Delegation Packet `allowed_outputs` + `forbidden_actions` (`do_not_call_providers`, `do_not_generate_media`, `do_not_record_gate_decisions`, ...) plus a Standing Authorization scoping repeated verbatim across SKILL.md, gates-and-reviews.md, pipeline-contract.md. The Review Record half IS schema-enforced.
- Gap: The privileged-capability surface is prose + a JSON example only. No delegation/result schema exists; grep of tests/ for `forbidden_action` returns zero. The model-visible capability list and any runtime enforcement are hand-maintained copies with no single allowlist and no pinning test — renaming `do_not_call_providers`, dropping a forbidden action, or widening `allowed_outputs` fails no CI test. (Pattern 14's silent-divergence hole; the open A1 tail.)
- Steal: #14 Schema/enforcement parity for privileged surfaces from gbrain (`brain-allowlist.ts` + `brain-allowlist.test.ts`) — derive the worker tool set from one registry filtered by an explicit allowlist; the constraint appears in BOTH the model-visible JSONSchema and a fail-closed check, pinned against upstream so a rename fails CI.
- Apply:
  1. Put the worker capability vocabulary (`allowed_outputs` + `forbidden_actions` values) in ONE Python/JSON allowlist module in `bin/` or `schemas/`.
  2. Make the A3 delegation/result schema enums generated from (or asserted equal to) that allowlist, validated through `artist_os_schema_validator.py` like Review Records, keeping the richer 7-status Subagent Result enum.
  3. Add a unittest pinning the allowlist names so a rename or silent widening turns CI red, and assert the doc JSON example uses only allowlisted tokens.
- Watch out: Parity-by-convention (two lists "kept in sync") is exactly the failure this kills — if no test fails on rename you do not have parity. A schema at rest still does not enforce at the use site; pair with a runtime check (ADR-0011's `review_only` follow-up is the analog — see A6).

### A5. No mandatory executable output floor inside the provider/render chokepoint  (impact: HIGH / effort: MED)
- Has: `docs/pipeline-contract.md:241` requires provider adapters to refuse generation unless the request carries an approved-not-pending Generation Approval gate whose upstream refs match the Prompt Plan/Branch Set and whose scope fits — "Missing, mismatched, stale, or merely waived gates are hard failures." The first Hard Gate and Standing Authorization scoping reinforce this; Output Records are schema-validated and an Output Critic sub-agent is mandatory.
- Gap: Every one of those is prose. No provider/render/compose module exists (only `bin/artist-os-paths` matches `render`); the Output Critic is conductor-invoked, so an agent that skips the reviewer ships anyway, and the line-241 "hard failures" are enforced by no function returning a failed status. (The "reviewer is advisory" loophole; the open Part C / OpenMontage transfer.)
- Steal: #18 Tool-embedded hard gate from OpenMontage (`video_compose.py::_pre_compose_validation()`) — the gate lives in the single unavoidable compose tool every workflow funnels through and returns a FAILED ToolResult (hard block, not warning), so the floor holds even when the advisory reviewer is skipped.
- Apply:
  1. Make the provider/import/export step a real callable (a `bin/` adapter entrypoint or a validator function the adapter MUST invoke), not a prose step.
  2. Run the line-241 floor in code pre-execution: Generation Approval approved-not-pending, upstream refs match Prompt Plan/Branch Set ids, scope fits — returning a hard failed status on any violation.
  3. Make a missing/absent approval artifact itself a hard failure (never skip-on-missing); cover with a test asserting a refused call cannot emit an Output Record.
- Watch out: OpenMontage's own hole — `delivery_promise` is skipped-with-a-warning when absent, so an agent that never emits it bypasses the gate. Skip-on-missing is how a "hard" gate leaks: a missing approval input must itself be a hard failure. Note: ADR-0011's own open Follow-Up (line 71) — "add review checks preventing `review_only` images from being used as provider inputs" — is the same use-site-enforcement gap on an already-schema-pinned invariant; land it as a concrete sub-case of this floor.

### A6. Executable anti-silent-substitution blocker at the provider/style/voice lock point  (impact: HIGH / effort: MED)
- Has: `docs/pipeline-contract.md:241` requires adapters to verify upstream refs match the locked Prompt Plan / Sound Prompt Plan / Prompt Branch Set; `schemas/prompt-plan.schema.json` locks `provider_targets` (provider enum + `model_version`); `docs/subagent-orchestration.md` forbids silently skipping provider-boundary checks.
- Gap: All prose — no provider adapter in code, so nothing fires when a LOCKED provider, model_version, style, or voice becomes UNAVAILABLE between Prompt Lock and generation. The contract covers mismatch/stale/waived gates but not locked-choice-now-unavailable, where the dangerous default is to "degrade gracefully" to the next available provider — a silent swap shipping something the artist never approved. No test asserts an unavailable locked choice escalates rather than substitutes. (Open Part C / OpenMontage transfer.)
- Steal: #21 Anti-silent-substitution blocker from OpenMontage (`video_compose.py` + `test_documentary_governance.py`) — at the point the locked runtime is consumed, return a STRUCTURED BLOCKER (locked value + available options + logged decision) for any unavailable runtime; never a silent engine swap; a test asserts the blocker fires (not a swap).
- Apply:
  1. Add a small dependency-free `bin/` availability check invoked at generation time that reads the locked `provider_targets[].provider` + `model_version` from the approved Prompt Plan.
  2. On unavailable-but-locked: return a structured blocker with the locked value, available options, and a logged decision (write a `GateDecision` `gate_status=blocked`, `proceed_unconfirmed=false`) — escalate to the artist; never auto-select a substitute.
  3. Distinguish locked choices (post-Prompt-Lock — must escalate) from open selection (pre-lock — graceful fallback fine); block even when the lock artifact is absent (no-lock = block/escalate).
  4. Add a behavioral test asserting the blocker fires for an unavailable locked provider and unknown providers are rejected.
- Watch out: Here graceful degradation IS the bug — resist the instinct to fall back. Guard the skip-on-missing leak: an absent locked-value artifact must still block/escalate, not be treated as "any provider is fine."

### A7. Digest gate and eval scenarios do not cover new character / illustration / reference routes  (impact: MED / effort: LOW)
- Has: `blessed.lock` digest-pins only SKILL.md; eval-spec.md T1-T6 cover image/suno/text/video-storyboard flows + a review + a missing-Reference start, graded as ordered TRACEs.
- Gap: Two coupled holes. (1) The SKILL.md edits that flipped the lock RED add character-creation, illustrated-work/Illustration Plan, and storyboard-vs-illustration routing plus a 9th hard-gate bullet, but T1-T6 has no character/illustration/promoted-reference assertion (grep returns nothing) — so even after a correct re-bless the eval validates the OLD six journeys, not the new routes; CI proves the conductor CHANGED, not that the new behavior PASSES. (2) Load-bearing behavior in unpinned mode files can be edited without flipping the digest gate (the A3-prior gap, now wider with the new mode files unpinned).
- Steal: #12 Eval re-bless digest gate (extend the digest set) from artist-os + gbrain capture/replay — pattern 12 watch-out: pinning only the top file leaves delegated/mode-file logic unguarded; extend the digest set AND exercise the routes the conductor now advertises before a re-bless can pass.
- Apply:
  1. Add T7/T8/T9 to eval-spec.md: character-creation → Character Template (+ optional Visual Reference Sheet); illustrated-written-work → Text Journey then Illustration Plan with the Illustration Plan Reviewer + Approval gate; storyboard-vs-Illustration-Plan disambiguation — each with per-trace checklists.
  2. Extend `blessed.lock` to a `{file -> sha256}` map including `illustration-plan.md`, `character-template.md`, `visual-reference-sheet-prompt-builder.md`, `text-journey.md`, `critique-asset.md`; update `is_blessed()`/`cmd_status()`/`write_lock()` to iterate.
  3. Update `test_conductor_eval_lock.py` to assert every pinned file matches.
  4. Re-run the manual eval over the expanded set, then bless (now also stamping mode-file digests).
- Watch out: Pinning more files raises re-bless friction — pin only behavior-critical mode files or operators start blind-blessing. These additions only bite if the bless-against-grade guard (A2) lands first.

### A8. Digest/drift guard does not cover the high-traffic delegated mode files  (impact: MED / effort: LOW)
- Has: SKILL.md is an explicitly thin conductor deferring all methodology to single-source-of-truth files; its body is digest-pinned (`blessed.lock` + `test_conductor_eval_lock.py`) and several mode files have token-pin contract tests (`test_text_journey_skill_contract.py`, `test_reviewer_skill_contract.py`, `test_medium_plan_skill_contract.py`).
- Gap: The pattern's named hedge ("guard the conductor AND high-traffic mode files") is applied unevenly. The digest gate pins ONLY SKILL.md. Among the files the conductor defers to at full depth, several have NO digest pin and NO token contract test: `critique-asset.md` (Prompt/Output Critic, Phase steps 13 & 16), `text-to-image-plan.md`, and the new `illustration-plan.md`, `character-template.md`, `visual-reference-sheet-prompt-builder.md`. A trim stripping load-bearing setup out of `critique-asset.md` fails no CI test, while the same edit to SKILL.md would go red — and "follow at full depth" is prose-enforced, so an unguarded mode file is exactly where the method can rot undetected.
- Steal: #1 Read-skill-from-disk inline composition (enforcement hedge) from gstack / artist-os' own `blessed.lock` — extend the already-built digest + token-pin machinery to the remaining high-traffic mode files.
- Apply:
  1. Add a second digest set (in `blessed.lock` or a sibling lockfile) covering `critique-asset.md`, `text-to-image-plan.md`, `illustration-plan.md`, `character-template.md`, `visual-reference-sheet-prompt-builder.md`.
  2. Extend `test_conductor_eval_lock.py` (or a parallel test) to recompute each file's sha256 and go CI-red on an unblessed edit; wire `bin/artist-os-eval bless` to refresh all digests together.
  3. For newly-pinned files lacking one, add a lightweight token contract test (e.g. `critique-asset.md` still carries its Output Critic blocking-finding language).
  4. Scope the digest set to genuinely load-bearing hot-path files; lean on token-pin tests for the long tail to avoid re-bless fatigue.
- Watch out: Pin too many low-churn files and routine tweaks force a re-bless, training maintainers to bless blindly. Keep relying on the loud anchor resolver (`bin/artist-os-paths`, never cwd) so a missing mode file fails loudly rather than the conductor proceeding without its method. (Closely related to A7 — coordinate the two as one digest-set expansion.)

### A9. Reviewer blindness / no-self-review asserted in prose, never proven at runtime  (impact: MED / effort: MED)
- Has: `docs/gates-and-reviews.md:184` states the creating agent must not self-review and must pass a narrow packet; `docs/subagent-orchestration.md` defines the `blind_verifier` role and (line ~254) "the verifier ... does not receive the first critic's reasoning"; `test_reviewer_skill_contract.py` pins those tokens. Notably, `schemas/review-record.schema.json:47-51` ALREADY requires `reviewer_execution.source_skill` (the reviewing skill identity) — so the repo is closer to mechanization than first apparent.
- Gap: The blindness itself is unenforced. The Delegation Packet shape is prose+JSON-example with no schema (only `review-record.schema.json` exists), so nothing prevents a packet from bundling the author's draft PLUS its reasoning into a reviewer's context — a self-review wearing a reviewer's hat. The contract test only greps prose tokens; no field attests which `upstream_records` the reviewer was (or was NOT) given. Given `source_skill` already exists, the true remaining delta is the artifact-side creating-agent identity + a test that fails if it equals `source_skill`, plus the blind-packet input schema.
- Steal: #3 Blind independent reviewer (blind-packet half) from gstack (`review/SKILL.md`: "subagent must be truly independent", "do NOT use run_in_background") — launch each reviewer with a strictly bounded context (artifact location + upstream record/rule + output format) and deliberately omit the author's reasoning; the allowed contents are an enumerated, reviewable surface.
- Apply:
  1. Add `schemas/delegation-packet.schema.json` with `additionalProperties:false`; wire into the validator + a fixture test so a packet carrying author-reasoning fields is rejected. (Shared with A3/A4 — build once.)
  2. For `blind_verifier`/critic packets, add a schema variant whose allowed inputs enumerate ONLY {artifact location, upstream records, rule-being-checked, output format} and explicitly forbid a `prior_critic_reasoning`/`author_rationale` field.
  3. Add the artifact-side creating-agent identity and a test that fails if it equals `reviewer_execution.source_skill` (mechanizing gates-and-reviews.md:184) — this is the small true delta since `source_skill` already exists.
  4. Extend the existing token contract test to assert the new packet schema is referenced from the reviewer skills.
- Watch out: "Blind" leaks easily — the schema must FORBID the reasoning field, not just omit it from the example. Do not over-rotate into the full Subagent Result envelope here (that is A3); scope this to the blind-packet input surface to keep it MED.

### A10. Fingerprint-merge + agreement-confidence machinery is prose-only and cannot dedupe  (impact: MED / effort: MED)
- Has: The Review Record half is executable (`review-record.schema.json` finding `$def` with severity enum, pinned by `test_reviewer_skill_contract.py`). `docs/subagent-orchestration.md` defines `finding_fingerprints` as a composite key (artifact_id, location_or_field, upstream_rule, claimed_drift) + a worker confidence enum + a Reduction section ("group by fingerprint, dedupe, raise aggregate confidence on independent agreement").
- Gap: The fingerprint + agreement-boost + gating machinery lives ONLY in the prose JSON example and Reduction prose. grep finds zero `fingerprint` in schemas/ and tests/, and zero `confidence` field in `review-record.schema.json`. So (a) a worker emitting a fingerprint keyed on the volatile free-text summary fails no test and dedupe silently no-ops; (b) merged-finding confidence and any threshold gate exist nowhere in code; (c) the conductor is the same thread doing reduction, so "agreement boosted confidence" has no executable check that two independent workers actually collided.
- Steal: #3 Blind reviewer + fingerprint merge + confidence gate from gstack (`review-army.ts`) + artist-os' own `blind_verifier` — keep dedupe/confidence-boost/gating in CODE, parse one JSONL finding per reviewer, dedupe by composite fingerprint, gate on severity-AND-confidence.
- Apply:
  1. Pin `finding_fingerprints` to the existing composite key with `additionalProperties:false` + the confidence enum in the A3 schema, wired into `FIXTURE_SCHEMA_MAP`.
  2. Add a collision test: two worker results citing the same defect produce IDENTICAL fingerprints, and a reduction over them yields one merged finding with boosted aggregate confidence.
  3. Move dedupe + agreement-boost + threshold into a small dependency-free reduction helper the conductor calls, gating on severity-AND-confidence.
  4. Pin the Reduction prose tokens (dedupe by fingerprint, raise confidence on agreement, preserve minority) with a contract test.
- Watch out: A fingerprint including volatile fields never collides; keep the key stable. A confidence gate that suppresses low-confidence findings can bury a real low-confidence blocking item — gate on severity-AND-confidence. Confidence-boost-on-agreement assumes real independence — if one packet/system prompt is reused across "independent" reviewers, agreement is correlated noise.

### A11. Wave Model fan-in join is prose-only, not an event-driven aggregator  (impact: MED / effort: MED)
- Has: `docs/subagent-orchestration.md` Wave Model (70-84) defines a deterministic non-polling join (freeze → dispatch → collect → reconcile → validate → persist → advance) with "must not advance while worker results are still unresolved if required" (line 84) + Pressure Check 8. Reduction rules (240-254) specify deterministic merge. `events.jsonl` exists; `finding_fingerprints` gives a merge key.
- Gap: The whole fan-out/fan-in is instructions the conductor model is trusted to follow — no executable terminal-child accounting, no claim condition. grep for `aggregator|child_done|inbox|claimant|fan-in` finds only prose. Nothing posts a terminal event per worker, nothing blocks the merge until all required workers are terminal, and reconciliation is inline LLM work. A conductor that loses track of an unresolved required worker can advance anyway.
- Steal: #5 Aggregator-as-claimant join from gbrain (`subagent-aggregator.ts`; apply-step-4 JSON-event-log variant) — each worker appends a `child_done` event on terminal status and decrements an outstanding counter; the aggregator step runs only at zero, then merges by a fixed deterministic reducer. (Workers are LLM subagents, not queued jobs — use the event-log variant, NOT a Postgres queue.)
- Apply:
  1. For Parallel Production waves, write one terminal event per worker to `events.jsonl` (`{type:'worker_terminal', task_id, status}`), idempotent (dedupe on `task_id`).
  2. Add a small executable preflight (in `bin/` or via `bin/artist-os-paths`) that reads `events.jsonl` for a `wave_id` and returns ready/not-ready by checking every required `task_id` has a terminal event — turning Pressure Check 8 into a code check.
  3. Specify the merge as a fixed reducer in fingerprint order; pin the ordering with a multi-worker fixture test.
  4. Add a test asserting the readiness check returns not-ready when any required worker lacks a terminal event.
- Watch out: Deterministic concatenation is NOT cross-child synthesis — Artist OS's Reduction legitimately reasons across workers, so model that as a separate bounded conductor step AFTER the deterministic join. The terminal event must be idempotent or a crash-replay double-counts. Do not build a job queue.

### A12. Two-phase crash-resumable persistence for in-flight subagent work  (impact: MED / effort: MED)
- Has: Persist-before-advance is a hard gate and a Synchronization Barrier; every step appends one JSON object to `events.jsonl`; manifest+events+SQLite let resume query state (SKILL.md:274). Subagent results carry a rich status enum + a Failure And Degradation matrix.
- Gap: The event log is single-state — events are appended AFTER a step lands, not as a `pending` row written BEFORE a side-effecting step and flipped to terminal after. No two-phase row, no idempotent tag per step, no schema for `events.jsonl`. Worker results are never durably persisted (`.tmp/artist-os/<task_id>/` only, "must not be treated as resume authority"). A run killed mid-wave (after a paid generation, or after workers returned but before reconcile+persist) loses in-flight output and resume re-derives from the last manifest. No test kills mid-step and asserts the resumed run reaches the same terminal state.
- Steal: #4 Externalized-state crash-resumable agent loop from gbrain (`subagent.ts`, `subagent-handler.test.ts` crash-replay) + impeccable requeue-on-restart — persist two-phase rows (`pending` → `complete`/`failed`); on resume trust terminal rows, re-run only `pending` rows flagged idempotent.
- Apply:
  1. Give `events.jsonl` a schema (`schemas/event-record.schema.json`): task_id, phase, step_kind, state enum (pending|complete|failed), idempotent bool, timestamp; wire into `FIXTURE_SCHEMA_MAP` with fixture + test.
  2. For each side-effecting step append a `pending` event before and a matching terminal event after, tagging idempotent (drafting/planning) vs non-idempotent (paid generation, visible publish).
  3. Add a `resume <project_id>` routine to `bin/artist-os-db` that treats terminal rows as authoritative and reports the first non-terminal idempotent step; have SKILL.md resume call it before re-asking the artist.
  4. Add a test truncating `events.jsonl` mid-step and asserting resume identifies it and does NOT re-run a non-idempotent step flagged complete.
- Watch out: The idempotency flag is load-bearing — a resume that re-runs an unflagged paid generation bills the artist twice. Keep `events.jsonl` canonical and `.tmp` advisory so the disposable worker output never becomes a competing source of truth.

### A13. Logical status + revert view over the durable work unit  (impact: MED / effort: MED)
- Has: The named work unit is real and largely executable: `project.json` (`schemas/project-manifest.schema.json`) + `events.jsonl` + sidecars + `artist-os.sqlite`, files as source of truth. `bin/artist-os-db` manages init/setup/sync and indexes current_stage, gate statuses, records, outputs, reference inventory. `status=missing` and `visible_missing` are first-class derived states, test-pinned. Resume queries SQLite then project.json.
- Gap: Two halves of pattern 17 are absent. (1) No progress/status VIEW: `bin/artist-os-db` exposes only `list` and `show` — no command rendering current phase / percent-through-the-17-step Phase Order / open blockers (pending gates, unresolved blocking findings), though percent is derivable. (2) No logical revert at phase/gate/task granularity over the event log — undoing a phase means manual file surgery or raw git (wrong granularity). The resume-before-re-ask discipline is prose, not enforced.
- Steal: #17 Durable resumable work unit from wshobson conductor (track = spec + phased plan + registry + git-linked status + logical revert) — progress queryable as a status view; resume reads the manifest before re-asking; revert operates on the recorded plan, not raw git reset; index rows stay derived; `missing` is historical not actionable.
- Apply:
  1. Add `bin/artist-os-db status <project_id>` joining indexed current_stage against the fixed Shared Gate Order to print current phase, percent, and open blockers; test a known fixture renders expected phase/percent.
  2. Add `bin/artist-os-db revert <project_id> --to-phase <phase>` over events.jsonl/manifest at phase granularity: mark later records historical (`status=reverted`), never delete; refuse to revert across a paid/irreversible step without an explicit waiver.
  3. Make SKILL.md resume call `status` first and quote it, so resume-before-re-ask is observable.
  4. Pin a test that a reverted phase's later records are marked historical (not deleted) and resume after revert lands on the reverted phase.
- Watch out: If the SQLite index drifts from files-as-truth, the status/percent view lies — keep the index strictly derived; treat `missing` as historical. Revert must mark, not delete, or it destroys the provenance the sibling-folder layout protects.

### A14. AI-tell denylist linter over Artist OS's own user-facing copy  (impact: LOW / effort: LOW)
- Has: Three real drift guards in the stdlib CI target: `test_phase_order_doc_drift.py` (subsequence spine), `test_schema_shared_block_drift.py` (recursive byte-equality), `test_version_changelog_consistency.py` (VERSION == top CHANGELOG header).
- Gap: No `validateProse`-style AI-tell denylist runs over Artist OS's own README/SKILL/docs, even though the skill critiques style-replacing-meaning in others' work. (NOTE — corrected per verifier: the count-derivation half of this gap is NOT real. grep across skills/, docs/, README.md finds NONE of the literal strings `9 Hard Gates`/`17-step`/`11 reusable roles`/`9 Pressure Checks` — gates, pressure checks, and roles are un-numbered bullets/tables with no cited count, so a count-derivation guard would have nothing to guard. Only the denylist half stands.)
- Steal: #9 Build-time / drift guards as quality gates from impeccable (`build.js validateProse`) — a tiny script with ~20 denylisted AI tells (em-dash-as-joiner, "delve", "seamless", "tapestry") wired into one verify target that exits non-zero with a printed rationale.
- Apply:
  1. Add a stdlib test carrying a short high-precision AI-tell denylist and run it over `README.md`/`SKILL.md`/`docs/*.md`, failing on any hit so Artist OS practices the prose discipline it enforces.
  2. Wire it into the same `unittest discover` target the other drift guards run in.
- Watch out: A hand-maintained denylist rots; keep it short and high-precision or it false-positives on legitimate copy and gets disabled. (Do NOT build a count-derivation guard — there are no count citations to guard.)

### A15. Named decision principles + explicit never-auto-decide class for Autopilot  (impact: MED / effort: MED)
- Has: Autopilot (SKILL.md 179-202) replaces the user's pacing judgment and classifies every response into 4 buckets; it enumerates a concrete never-auto-decide set inline (provider-backed generation, paid, uploads, destructive, gate approvals, waivers, acceptance), repeated across four docs. The audit-trail half is strong: `GateDecision` records + `decision_interview` persistence + `events.jsonl` keep decisions on disk.
- Gap: Artist OS has the side-effect never-auto-decide list and an audit trail but lacks the pattern's middle layer — a short NUMBERED principle set with explicit tiebreaker order, and a three-way taste taxonomy separating Mechanical (auto-decide silently) from Taste (auto-decide but surface at ONE final gate). Today every non-mechanical creative judgment is forced to a per-question Decision Interview — the opposite failure for compact/autopilot work. No named principle set is recorded as "principle invoked" in the `GateDecision`.
- Steal: #2 Auto-decide with named principles + decision classification + audit trail from gstack (`autoplan/SKILL.md`) — 6 named principles with phase-dependent tiebreakers; classify every decision Mechanical / Taste / User-Challenge; Edit-append each to a Decision Audit Trail; only two human gates.
- Apply:
  1. Add a short numbered principle list to Autopilot (e.g. preserve-meaning-first, lightest-orchestration, bias-to-action, traceability-over-speed) with explicit tiebreaker order.
  2. Define a Taste class for creative micro-choices Artist OS may auto-decide and surface at one consolidated gate (instead of a Decision Interview per choice), keeping the enumerated User-Challenge/never-auto list as-is.
  3. When the conductor auto-decides, record class + principle invoked + choice into `GateDecision` (add optional `decision_class` + `principle_invoked`).
  4. Add a contract test asserting the principle list and three class names still exist in SKILL.md.
- Watch out: If the User-Challenge class is vague the model rationalizes user-owned creative choices as Taste — keep it concrete and enumerated; do not let creative-meaning choices drift into Taste-auto-decide. Keep the audit trail on disk, never accumulated in context.

### A16. AGENTS.md has zero reference-inventory coverage — doc drift on the newest landed feature  (impact: MED / effort: LOW)
- Has: The reference-inventory feature is fully landed and executably enforced — `docs/storage.md`, `docs/metadata-schema.md`, `docs/pipeline-contract.md`, `schemas/project-manifest.schema.json`, and `bin/artist-os-db` (`publish-visible-reference`, `index_reference_inventory`) all gained reference-inventory paths/commands; the schema is test-pinned.
- Gap: `AGENTS.md` mentions reference-inventory nowhere (grep -ci returns 0), even though it is the agent-facing contributor doc and every other surface gained the paths. This is single-source-of-truth erosion on the newest shipped record type, and no drift guard would catch it — there is no test asserting AGENTS.md mentions every active record type. (Surfaced by the verifier; not in the original findings.)
- Steal: #9 Build-time / drift guards as quality gates from impeccable (`generateCounts` derive-from-source discipline) — derive the authoritative record-type set from the schemas/validator map and fail CI when a doc that must enumerate them is out of sync.
- Apply:
  1. Add the reference-inventory record (paths, `publish-visible-reference`, the two SQLite tables) to `AGENTS.md` alongside the other record types.
  2. Add a stdlib drift test deriving the active record-type set from `FIXTURE_SCHEMA_MAP` (or the schemas dir) and asserting AGENTS.md mentions each, so a future new record type that skips the contributor doc fails CI.
- Watch out: Derive the expected record-type set from source (the schema map), never hardcode the list, or the guard rots as silently as the doc it guards.

### A17. Binary routing eval cannot regression-test which sub-route fires  (impact: MED / effort: MED)
- Has: `evals/routing/routing_eval.py` fires raw user queries through real `available_skills` (binary artist-os/none, 100% at 7 runs post-collapse) — a tested artifact, not a meta-prompt. The conductor-behavior eval (A7) covers the TRACE side for T1-T6.
- Gap: The routing eval label set is binary, so it cannot verify WHICH sub-route fires (character vs illustration vs storyboard vs text). The new prose intent shortcuts the deep-dive predates — character creation → Character Template; illustrated written work → Text Journey then Illustration Plan; storyboard disambiguation; blog/Substack/LinkedIn → Text Journey with Research Grounding — are untested by either eval at the routing layer. A reworded route that silently mis-fires to the wrong sub-journey passes the binary eval. (Surfaced by the verifier; distinct from A7's conductor-trace coverage.)
- Steal: #13 With-skill vs without-skill / scenario-asserted eval from wondermint ({prompt, assertions[]} JSON) — extend the routing harness from binary classification to per-route assertions, reusing the real-`available_skills` harness.
- Apply:
  1. Extend `routing-evals.json` rows from a binary label to an expected sub-route/intent label (character_template, illustration_plan, video_storyboard, text_journey, ...).
  2. Update `routing_eval.py` to assert the fired route matches the expected sub-route, not just artist-os/none.
  3. Add adversarial near-miss rows (storyboard-as-video vs storyboard-as-illustration; "children's book" vs "comic") so the disambiguation routes are pinned.
- Watch out: Small-N LLM-judged routing is noisy — report variance and do not over-read a single run. Keep the harness firing the RAW query through real `available_skills` (not a meta-prompt) so it measures real triggering.

### A18. Enumerated action-class → confirmation-gate matrix with default-to-strictest  (impact: MED / effort: LOW)
- Has: The privileged surface is fail-shut (first Hard Gate forbids any provider/render call without per-call approval); Standing Authorization is scoped by action class, stated identically across four docs; the reference work adds an in-schema action-class rule (`review_only` → `provider_input_allowed:false`, test-pinned).
- Gap: The action-class boundary is scattered prose (a long forbidden-action sentence repeated across four docs) rather than ONE enumerated action-class → required-gate table with a default-to-strictest rule for unrecognized actions. A renamed or newly-added side-effecting action (a new export/upload path) is classified by no single source and fails no CI test. (The A4 capability-allowlist gap viewed from the gate side.)
- Steal: #10 Mode→gate approval matrix from wondermint (Operating Modes matrix + `confirmation-gates.md`) — enumerate action classes mapped to required gates so approval is a table lookup; unknown actions default to the strictest row.
- Apply:
  1. Collapse the repeated forbidden-action prose into ONE action-class table (draft-only / internal-subagent-spawn / persist-state / provider-generation / paid-or-upload / destructive) → required gate, in a single referenced doc; have the four docs link it instead of restating.
  2. Add an explicit rule that any unrecognized/newly-added action defaults to the strictest gate.
  3. Derive the subagent `forbidden_actions` surface from that one table and pin it with a test (shared with A4).
  4. Pair the matrix with the serialized gate token (A1) so a reviewer sees the lookup ran in-transcript.
- Watch out: A matrix read-but-not-narrated gives no transcript evidence (pair with A1). The classic failure is a billing/destructive action defaulting to a weak gate when unrecognized — default to strictest. Watch the four duplicate copies drifting if you keep them instead of pointing all at the single table.

### A19. Creative-medium promise locked at planning is not re-validated against the output  (impact: MED / effort: MED)
- Has: Medium plans carry typed categorical promises: `image-medium-plan.schema.json` pins `presentation_mode` (single/compressed_arc/series via if-then const), text has `audience_promise`, illustration has `illustrated_work_type`, video types the motion deliverable. The validator enforces these at plan time + one Python cross-item contract (`validate_release_package_plan_contract`).
- Gap: The promise is locked at planning but never machine-re-checked at output. `output-record.schema.json` carries a free-text `target_media_type` + a `medium_plan_id` ref, but no cross-item validator asserts the produced output still honors the locked plan's presentation_mode / illustrated-vs-photographic / motion promise. Structure-only validation passes while creative intent drifts (illustration creeping into a photographic brief, static frames passing as motion).
- Steal: #19 Typed-and-locked creative-promise invariant from OpenMontage (`delivery_promise.py` + `validate_cuts()`) — the promise is locked at proposal and a measurable invariant is re-computed at compose, deliberately refusing to count text/stat/chart cards as motion.
- Apply:
  1. Pick the one categorical promise per medium that must survive end-to-end (image: presentation_mode + photographic-vs-illustrated; video: motion-led vs slideshow; text: audience_promise/voice) and ensure it is a locked field on the medium plan.
  2. Add a validator cross-item contract — alongside `validate_release_package_plan_contract` — asserting an Output Record's measurable property matches the locked promise (an image_series output must declare N>1 distinct images; an illustrated plan's output must not be tagged photographic).
  3. Include a deliberate loophole-closer (the "animated slides aren't motion" move) pinned with a fixture test.
- Watch out: If the promise artifact is optional the re-check becomes skip-on-missing — make the locked promise field required at planning. A near-miss invariant that only warns is a downgrade waiting to happen; the threshold must hard-fail.

### A20. No cheap-judge gate before expensive transformation/generation passes  (impact: MED / effort: LOW)
- Has: Cost discipline is structural only at the provider boundary (per-call approval, no batch-by-implication — Pressure Check 6) and via orchestration-mode economy ("choose the lightest mode"). Workflow Scale Routing sizes stewardship, not whether a source merits a pass.
- Gap: No cached cheap classifier in front of the expensive planning/generation tier. A source goes straight into token-expensive Meaning → Research Grounding → Interpretation → Story passes regardless of whether it merits one, and a resume/re-run re-pays for unchanged inputs (no content-hash verdict cache, no success-only cooldown). grep finds no significance/verdict/cheap-judge mechanism. Cost-skipping rests entirely on the conductor choosing the lightest mode — incidental, not structural.
- Steal: #6 Cheap-judge gate before expensive work from gbrain (`synthesize.ts`, `dream_verdicts` table) — a cached cheap "significance verdict" keyed by file+content-hash gates the expensive tier; a cooldown written ONLY on success; per-transcript idempotency; all in durable state.
- Apply:
  1. Define the single expensive tier (the full planning pass, or a provider generation) and a binary "is this source worth a full pass?" question a cheap model answers.
  2. Add a content-hash-keyed verdict record in the existing durable substrate (a `verdicts` table in `bin/artist-os-db` alongside `reference_inventory_items`) so identical/resumed inputs short-circuit; gate the expensive pass on the cached verdict.
  3. Write a `last_completion_ts` cooldown ONLY on success; key idempotency on the source content hash.
  4. Wire the verdict shape into `FIXTURE_SCHEMA_MAP` with a fixture + test, matching reference-inventory.
- Watch out: A cooldown written on success AND failure lets a flapping failure suppress legitimate work — success only. A content hash omitting a field the expensive tier consumes serves a stale verdict forever; hash exactly the inputs the pass reads. A too-lenient judge defeats the purpose — calibrate against real artist traffic.

### A21. Model-tier selection is not centralized behind one resolver  (impact: LOW / effort: LOW)
- Has: No model-config / tier resolver exists (grep returns nothing). The only model identifier anywhere is `routing_eval.py:155` (`--model` default `opus`), used solely for the eval harness. The pipeline names no models; the host registry carries transform config, not model tiers.
- Gap: Model-tier selection (reviewers vs workers vs a future cheap judge) is neither centralized nor auditable. Today there is one implicit model, so a future cheap-judge gate (A20) or any haiku-vs-opus split would scatter model strings with no single tunable decision point and no override precedence — a swap would be a multi-site edit.
- Steal: #6 Centralizing model-tier selection (companion) from gbrain (`model-config.ts`) — a 6-tier resolver with a precedence chain (CLI > config > deprecated > default > env > fallback) and named aliases, so every choice names a tier through the resolver instead of embedding a string.
- Apply:
  1. Add a single tier resolver (`bin/` module or `model-tiers.json`) with named aliases (judge / worker / reviewer) and precedence env > config > default.
  2. Replace `routing_eval.py:155`'s literal `opus` with a resolver lookup so no literal model ID lives outside the resolver.
  3. Adopt the resolver at the same time as the A20 cheap-judge gate so judge and expensive tiers both name their model through it.
  4. Pin the resolver's defaults and alias set with a stdlib test (like `test_host_registry.py`).
- Watch out: This only pays off once there is more than one model in play (A20). Introducing it before any second tier is speculative abstraction — sequence it WITH A20, not before. Keep the default tier explicit so a missing override never silently falls through to an expensive model.

### A22. Generate-but-commit transformer factory + per-host git-diff freshness gate is deferred  (impact: MED / effort: MED)
- Has: `packaging/hosts.json` is a data-only registry (codex active identity transform; claude-code/cursor `status:"stub"` with null transform fields + documented sandbox block). `packaging/README.md` + ADR-0008 explicitly state the generator (`bin/artist-os-generate`) is deferred "Later" work and codex's identity transform IS today's installer. `test_host_registry.py` pins registry shape + stub-null fields + the installer-reads-registry drift gate; `test_dist_manifest.py` resolves every skill-body reference under a manifest include.
- Gap: There is NO per-host transform function, NO placeholder-substitution build loop, and NO `git diff --exit-code` freshness gate (grep for `git diff` returns nothing; `bin/artist-os-generate` and `packaging/build/` do not exist). Honest today (one host, identity transform), but the day claude-code or cursor gets real transform values there is no mechanism that regenerates the per-host tree and fails CI on drift — and the stub-null test even ENFORCES those fields stay null, so populating them requires building the generator+gate or the test breaks.
- Steal: #8 Config-driven transformer factory from impeccable (`PROVIDERS` + `createTransformer` + `build.js`, 12 committed harness dirs) / gstack (`HostConfig` + `validateAllConfigs`) — one host-neutral body with placeholders; each host a declarative config; a build loop writes a COMMITTED per-host dir; CI runs the generator + `git diff --exit-code` per host as a true hard fail.
- Apply:
  1. Build `bin/artist-os-generate <host|all> [--dry-run]` where `materialize_host(config)` for codex is exactly today's identity install, writing `packaging/build/<host>/` with an "AUTO-GENERATED — do not edit" header (already specified in ADR-0008's "Later" section).
  2. When the first stub host gets real transform values, add `test_host_generate_freshness.py` that runs the generator into a temp tree and asserts byte-equality against the committed `packaging/build/<host>/` (stdlib equivalent of `git diff --exit-code`).
  3. Add a "no remaining `{{`" assertion over generated output if a host body needs substitution.
  4. Add a HARNESSES.md-style capability matrix (currently absent) and pin a test that its host rows match `hosts.json` keys.
- Watch out: Generate-but-commit duplicates the source N times; the freshness gate is the ONLY thing keeping them honest, so it must be a true hard fail, never skip-on-missing. Do NOT build the generator before a host actually diverges — ADR-0008 deliberately defers it; premature machinery is the heavy gstack DSL the ADR consciously rejected.

### A23. Secret-scan drift guard backing the secrets-banned-from-markdown rule  (impact: LOW / effort: LOW)
- Has: The user-state-outside-skill split is fully and executably closed — mutable state lives outside the read-only skill dir (Wondermint Root sibling layout; dev repo-local `workspace-library/`); `packaging/MANIFEST.json` excludes `workspace-library/`, `*.sqlite`, `.env`, `.tmp/`, pinned by `test_dist_manifest.py`/`test_host_registry.py`; resume survives deletion of the visible folder; `bin/artist-os-paths` never returns cwd.
- Gap: The pattern's explicit watch-out — a secrets-banned-from-markdown rule with no scanner is prose that rots — is the one narrow residual. Storage docs route secrets to `.env` and MANIFEST excludes it, but there is NO secret-scan over the tree (no wondermint `SECRET_RE` analogue) that would fail CI if a token/key/credential were committed into a markdown doc, schema fixture, or mode file.
- Steal: #15 User-state-outside-skill split from wondermint (`SECRET_RE` tree scan; secrets banned from markdown) — back the "no secrets in markdown" discipline with an executable secret-scan; the path split + MANIFEST exclusions are the executable half, the scan closes the prose half.
- Apply:
  1. Add a lightweight secret-scan to `bin/` (or `bin/artist-os-secret-scan`) using a small regex set (API keys, bearer tokens, private-key headers) over `schemas/`, `docs/`, `skills/`, fixtures.
  2. Wire it into the stdlib suite as a drift guard (`test_secret_scan.py`) so a committed secret fails CI like the other guards.
  3. Add an allowlist for obvious test placeholders to avoid false positives.
- Watch out: `docs/storage.md` flags an unresolved `~/Wondermint` vs `~/Documents/Wondermint` convergence between Artist OS and the Wondermint Marketplace skill — two competing folder conventions fragment state and break resume; resolve the external root before adding more state, independent of the secret-scan.

### A24. Copy-mode installer has no per-file diff protection or --overwrite-local opt-in  (impact: LOW / effort: MED)
- Has: `bin/install-codex-dev-skills` has real safety guards: refuses non-skill dirs, refuses on skill-name mismatch, refuses to overwrite a non-symlink, idempotent symlink handling, retired-skill cleanup with name verification, and a post-install `bin/artist-os-paths doctor` gate. Symlink-mode (dev default) edits flow back to the checkout — nothing to clobber.
- Gap: In copy-mode (the path a real non-checkout host install takes) the installer does an unconditional `cp SKILL.md` and `rm -rf references; cp -R`. If a user edited the installed copy, the upgrade silently overwrites it with no per-file diff check and no `--overwrite-local` opt-in.
- Steal: #8 Config-driven transformer factory (install-integrity mechanics) from gbrain (`skillpack/installer.ts`) — per-file diff protection that skips locally-modified files unless `--overwrite-local`, plus atomic tmp+rename write and a `.lock` with stale-PID detection.
- Apply:
  1. In the copy branch of `install_skill`, before `cp`, hash the target against the last-installed source; if it differs from both, skip and warn "locally modified, pass --overwrite-local to replace".
  2. Add an `--overwrite-local` flag that bypasses the skip; default preserve.
  3. Write via tmp file + atomic rename so a crash mid-copy never leaves a half-written SKILL.md.
  4. Add `test_install_overwrite_protection.py` exercising the copy branch against a temp install with a locally-modified target.
- Watch out: Scope this to copy-mode only — symlink-mode has no such risk, and over-engineering the dev-install path (the only one exercised today) adds friction for the one live host.

### A25. No slim marketplace subtree build + independently-versioned release step that refuses on drift  (impact: LOW / effort: MED)
- Has: `packaging/MANIFEST.json` is an authoritative include/exclude surface (ships THEORY/ARCHITECTURE/AGENTS/CONTEXT, validator, bin/docs/schemas/skills/packaging; excludes workspace-library, `*.sqlite`, `.env`, `.git`, `__pycache__`, `packaging/build`), pinned by `test_dist_manifest.py`. VERSION + CHANGELOG kept consistent. The Claude marketplace path is documented as deferred.
- Gap: The manifest is an include/exclude LIST, not a build that materializes a slim subtree, and there is no release step that bundles + version-stamps an artifact and refuses to publish on drift (impeccable's `release.mjs` / `./plugin` slim subtree). Fine for Codex dev-install (symlink/copy); a real gap only at the Claude marketplace milestone, where the sandbox block requires bundling referenced content inside the plugin dir (no reads outside, no `$CLAUDE_PLUGIN_ROOT` expansion).
- Steal: #8 Config-driven transformer factory (marketplace publishing mechanics) from impeccable (`release.mjs` + `./plugin` slim subtree, ~291MB → ~0.3MB) — build a slim subtree from the manifest, version the artifact independently, and refuse to publish when generated artifacts diverge from committed source.
- Apply:
  1. When the Claude host is built, drive a `packaging/build/claude-code/` slim subtree from MANIFEST include/exclude (the bundle the sandbox requires inside the plugin dir).
  2. Add a release step that stamps VERSION into the bundle and refuses to publish if the regenerated subtree differs from the committed one (reuse the A22 freshness gate).
  3. Dereference the `references/` symlinks at bundle time since Claude plugins cannot read outside the plugin dir.
- Watch out: Don't let durable user/runtime state live inside the generated overwrite-on-install tree — MANIFEST already excludes `workspace-library`/`*.sqlite`, preserve that in any slim-subtree build. Do not build this before the Claude host milestone; it is correctly deferred.

---

## What Artist OS already does well (verified, not gaps)

These were confirmed against the live repo as genuinely done — do NOT re-recommend them:

- **Thin-conductor progressive disclosure (pattern #1 core):** SKILL.md is explicitly thin, defers all methodology to single-source-of-truth docs + 21 internal mode files, and duplicates no methodology between conductor and members. (The only residual is the digest *coverage* gap A8, not the disclosure model.)
- **Routing as a tested artifact (pattern #13/#20):** `routing_eval.py` fires raw queries through real `available_skills` (binary, 100% at 7 runs) — not a meta-prompt. (Residual A17 is sub-route granularity, not the harness.)
- **Tiered, CI-gated, stdlib-only tests:** 305 tests across ~20 files; schema validation + contract tests + drift guards (phase-order subsequence, schema shared-block byte-equality, version/changelog) + the conductor eval-lock digest gate, all dependency-free.
- **Provider boundary fail-shut (pattern #21 intent):** the first Hard Gate forbids any provider/render/generation call without explicit per-call approval; Standing Authorization is scoped to internal worker spawning only and never authorizes generation/uploads/paid/destructive/approvals/waivers/acceptance.
- **Persist-before-advance + externalized durable state (pattern #4/#17 core):** schema-backed records + `project.json` + `events.jsonl` + `artist-os.sqlite` query index live outside the read-only skill dir; `missing`/`visible_missing` are first-class derived, test-pinned states.
- **Reference-inventory landed with executable enforcement on day one:** schema + validator map + fixture + 3 CI tests (including the `review_only → provider_input_allowed:false` invariant) + two SQLite tables + indexer — the same enforcement Review Records get, closing the usual "new schema with no validator+test" risk.
- **Eval re-bless digest gate exists and is working as designed:** `blessed.lock` + `test_conductor_eval_lock.py` are RED right now precisely because SKILL.md changed without a re-bless. (The hardening gaps are A2 unguarded-bless and A7/A8 coverage, not the gate itself.)

## Changes since the original study

- **Reference Inventory went from ADR to fully-landed schema-backed record:** `schemas/reference-inventory.schema.json` + `FIXTURE_SCHEMA_MAP` wiring + fixture + 3 dedicated tests make it a CI gate; the `review_only → provider_input_allowed:false` trust-boundary rule is encoded in-schema and test-pinned. ADR-0011 still lists an open runtime use-site check (folded into A5/A6).
- **Hard Gates grew 8 → 9** (a dedicated Long-Work Stewardship gate); the prior-art 8-gate / 17-step description is superseded.
- **Illustration planning is now a first-class pipeline branch:** new schema + `illustration-plan.md` mode + pipeline-contract step (Illustration Plan Reviewer + Approval gate, routing approved units through Image Journey, NOT Video Journey) + a Phase Order step-12 insert. Adds a new reviewer surface and approval gate the prior deep-dive predates.
- **Stateful-engine axis thickened:** `bin/artist-os-db` grew to ~82KB to add `index_reference_inventory` (two new SQLite tables), a path resolver, and a `publish-visible-reference` subcommand; storage/metadata/pipeline-contract/project-manifest all gained reference-inventory paths.
- **The conductor eval-lock is RED on purpose right now:** SKILL.md sha256 (4ae149c6…) ≠ `blessed.lock` (907ff921…, blessed 2026-06-25); ADR-0011 defers the `accepted_partial` conductor-text change until the manual eval is re-run and re-blessed. The digest gate is currently the only thing flagging the divergence — and `eval-spec.md` T1-T6 was NOT extended to the new routes (A7), so a re-bless would validate the old six journeys.
- **Test count rose from ~19 files to 305 tests** (304 green + 1 intentional eval-lock RED); `tests/fixtures/` gained `references/`, `locations/`, `objects/` subtrees with promoted-subject fixtures (promoted-door-keeper, hallway-threshold, old-tv).
- **`AGENTS.md` has no reference-inventory mention yet** — a doc-coverage gap surfaced by the verifier (A16).

---

Priority order: A1, A2 (cheapest universal hedges — serialized gate token #11 and the unguarded-bless digest hardening #12, both HIGH/LOW and real for Artist OS), then A7, A8, A14, A16, A18, A20, A21 (remaining LOW-effort drift/digest/route guards #9/#12/#20), then A3, A4, A5, A6 (HIGH-impact/MED-effort: schema the worker contract, pin the capability allowlist, embed the output floor and anti-substitution blocker in code), then A9, A10, A11, A12, A13, A15, A17, A19, A22 (MED/MED), then A23, A24, A25 (LOW-impact, mostly deferred until the Claude-host milestone).

Cross-cutting note: Every surveyed plugin's correctness ultimately rests on the model faithfully following long markdown. The two cheapest, most transferable hedges — recommend these before adding more prose: (1) Serialized state tokens that make gate compliance observable in the transcript (pattern #11). (2) Drift / digest guards that make silent erosion of a safety contract impossible (patterns #9, #12, #20).
