# Cost-Tiering Hand-off — Remaining Work

Status: open backlog as of 2026-06-27. The full design rationale is in
`docs/drafts/cost-tiering/README.md`; real measurements and tooling are in
`docs/drafts/cost-tiering/measurements/`. This file lists only what we discussed
but have **not** built yet, prioritized, so any of it can be picked up cold.

## 2026-07-05 unblock decisions

Grill-with-docs decision session for the current branch unblock:

- Target: unblock the current branch, not expand cost-tiering scope.
- Re-bless validity: run a real manual conductor eval when the conductor lock is
  stale; do not blind-bless. Do not harden `bin/artist-os-eval bless` in this
  unblock slice.
- Done bar: conductor eval gate plus normal verification tests.
- Eval coverage: use the current signed-off T1-T6 conductor-behavior checklist;
  expanded character / illustration / promoted-reference coverage is follow-up
  work, not this unblock.
- Measurement: a fresh token curve and Queen Bee comparison are still required to
  prove the optimization win, but they are not required to unblock this branch.

Local status note from 2026-07-05: `bin/artist-os-eval status` was already green
for this checkout (`blessed_at` 2026-06-28), so no re-bless was needed before
running the verification suite.

Partial measurement note from 2026-07-05:

- Refreshed the copied Codex dev skill with `bin/install-codex-dev-skills`.
- Created a clean Codex Desktop measurement thread for a sub-60-second
  laundromat short-social video dry run.
- The run correctly routed to `narrative_depth = micro_journey` and loaded
  `video-micro-journey-recipe.md`, but the background turn stalled after
  creating project folders and before writing final records or a final response.
- Measurement from the stable partial rollout:
  - rollout:
    `~/.codex/sessions/2026/07/05/rollout-2026-07-05T12-33-20-019f3357-7f18-7722-a7a6-21964f51969b.jsonl`
  - 14 turns, 82,764 fresh input, 752,384 cache read, 14,284 output + reasoning,
    272,274 input-equivalent units.
  - Per-turn context: mean 60k, peak 85k, zero turns above the 90k cap.
  - Lean signals after fixing `compare-run.py` to count actual file-read tool
    calls instead of raw string mentions: micro-journey recipe loaded;
    `micro_journey` set; full-stack avoidance passed (`video-journey.md` and
    `storyboard-prompt-builder.md` were mentioned in routing text but not read
    as files).
  - Remaining bottleneck: the run still read `schemas/video-medium-plan.schema.json`
    in large chunks while authoring/finalizing the compact plan.
  - Curve written to
    `docs/drafts/cost-tiering/measurements/curves/lean-rerun-partial-2026-07-05.html`.
- Do not append this to `token-log.jsonl` as a successful run. It is useful
  diagnostic evidence, not a completed paired rerun.
- Fix applied after this measurement: `video-micro-journey-recipe.md` now separates
  the thin Compact Video Authoring Packet from the schema-backed Video Medium Plan
  Record, tells the main conversation not to read the schema during packet
  authoring, and prefers a bounded `record_builder` / `schema_validator`
  finalization pass so the heavy schema stays out of the conductor's long-lived
  context. `compare-run.py` now detects actual file reads for full-stack and schema
  signals, not raw string mentions.
- Next measurement should rerun the same short-social scenario after reinstalling
  the dev skill and should show fewer `schema file reads`; if it still reads the
  full schema in the parent thread, the next build is a real thin authoring view or
  sectioned schema finalizer.

Clean follow-up measurement from 2026-07-05:

- Reran the same laundromat short-social scenario in a fresh Codex Desktop thread
  after reinstalling the dev skill.
- Scope: stop at the completed Compact Video Authoring Packet; do not finalize the
  schema-backed Video Medium Plan Record; no provider calls, reviewer subagents,
  Workspace Library records, `video-journey.md`, `storyboard-prompt-builder.md`, or
  `schemas/video-medium-plan.schema.json`.
- Rollout:
  `~/.codex/sessions/2026/07/05/rollout-2026-07-05T12-45-50-019f3362-f116-7b62-8802-cdf2eee4befb.jsonl`
- Result:
  - 3 turns, 37,255 fresh input, 57,984 cache read, 3,306 output + reasoning,
    69,501 input-equivalent units.
  - Per-turn context: mean 32k, peak 42k, zero turns above the 90k cap.
  - Lean signals: micro-journey recipe loaded; `micro_journey` set; full video
    stack avoided; schema file reads = 0.
  - Compared to the split Sage Wells flat baseline: mean context/turn dropped from
    about 49k to 32k (-36%). Input-equivalent for this authoring-packet stage was
    70k.
- Curve written to
  `docs/drafts/cost-tiering/measurements/curves/lean-authoring-packet-2026-07-05.html`.
- This row was appended to `docs/drafts/cost-tiering/measurements/token-log.jsonl`.
- Caveat: this proves the lean authoring packet path, not full schema-backed
  finalization or reviewer cost. The next measurement should isolate a bounded
  finalization pass that reads `schemas/video-medium-plan.schema.json` once, ideally
  outside the parent conductor context.

Schema-finalization measurement from 2026-07-05:

- Ran isolated finalization-only Codex Desktop threads against the completed
  laundromat Compact Video Authoring Packet.
- Scope: do not use the Artist OS conductor flow; do not load `SKILL.md`,
  `CONTEXT.md`, `video-journey.md`, `storyboard-prompt-builder.md`, or
  `video-micro-journey-recipe.md`; read `schemas/video-medium-plan.schema.json`,
  write `.tmp/artist-os-cost-tiering/finalized-laundromat-video-medium-plan.json`,
  and validate with `artist_os_schema_validator.validate_file`.
- First unconstrained finalizer:
  - rollout:
    `~/.codex/sessions/2026/07/05/rollout-2026-07-05T12-50-05-019f3366-d5e0-7871-8165-851f72e30edf.jsonl`
  - validated successfully, but took 7 turns, 42,307 fresh input, 160,512 cache
    read, 14,442 output + reasoning, 173,894 input-equivalent units.
  - mean context 34k, peak 46k, schema file reads = 4.
- Logged replacement finalizer:
  - rollout:
    `~/.codex/sessions/2026/07/05/rollout-2026-07-05T12-53-02-019f3369-893d-7e70-ba4a-620510aad86d.jsonl`
  - 9 turns, 17,418 fresh input, 255,872 cache read, 7,061 output + reasoning,
    99,493 input-equivalent units.
  - mean context 30k, peak 35k, zero turns above the 90k cap.
  - Lean signals: full video stack avoided; `micro_journey` present; schema file
    reads = 5 in the finalizer cluster.
  - Wrote and validated the schema-backed Video Medium Plan in `.tmp/`.
  - Curve written to
    `docs/drafts/cost-tiering/measurements/curves/schema-finalization-2026-07-05.html`.
  - This row was appended to `docs/drafts/cost-tiering/measurements/token-log.jsonl`.
- Combined two-stage lean result for this laundromat scenario:
  - authoring packet: 69,501 input-equivalent units.
  - schema finalization: 99,493 input-equivalent units.
  - combined planning + schema-backed finalization: 168,994 input-equivalent units,
    compared with the split Sage Wells flat baseline of 2,102,228 input-equivalent
    units across its three sessions. This is not a perfect apples-to-apples journey
    comparison, but it shows the two-stage compact path is materially cheaper while
    still producing a validated Video Medium Plan.
- Remaining bottleneck: the schema finalizer still reads the full schema several
  times. The next build target is a thin authoring/finalization view or a
  deterministic record-builder command that can use the schema once and validate
  without repeated model-visible schema reads.

Implementation note from 2026-07-05:

- Added `bin/artist-os-video-finalize`, a deterministic finalizer for Compact
  Video Authoring Packet JSON. It expands flat compact shot rows into schema-backed
  Storyboard Shot / Visual Unit / Shot Design records, writes the Video Medium Plan,
  and validates it against `schemas/video-medium-plan.schema.json`.
- Added `tests/fixtures/video-journey/laundromat-compact-video-authoring-packet.json`
  as the thin packet fixture and `tests/test_video_medium_plan_finalizer.py` as the
  regression test.
- Updated `skills/artist-os/references/video-micro-journey-recipe.md` to prefer
  `bin/artist-os-video-finalize` when repo tooling is available, so future runs do
  not need to shape the full schema in the model context.
- Verification: `bin/validate-examples`, `python3 -m py_compile ...`, and
  `python3 -m unittest discover -s tests -p 'test_*.py'` all pass.

Clean finalizer-command measurement from 2026-07-05:

- Refreshed the copied Codex dev skill with `bin/install-codex-dev-skills`, then
  ran a fresh Codex Desktop thread that authored a compact laundromat packet and
  invoked `bin/artist-os-video-finalize`.
- Output:
  `.tmp/artist-os-cost-tiering/clean-finalizer-run-video-medium-plan.json`.
- Independent validation passed with
  `artist_os_schema_validator.validate_file(Path('schemas/video-medium-plan.schema.json'), ...)`.
- Rollout:
  `~/.codex/sessions/2026/07/05/rollout-2026-07-05T13-04-28-019f3374-019f-7843-bb52-2f9fc5e4c404.jsonl`
- Result:
  - 12 turns, 111,297 fresh input, 571,392 cache read, 12,766 output + reasoning,
    270,564 input-equivalent units.
  - Per-turn context: mean 57k, peak 73k, zero turns above the 90k cap.
  - Lean signals: micro-journey recipe loaded once; full video stack avoided;
    `micro_journey` present; manual schema file reads = 0 because schema use stayed
    inside `bin/artist-os-video-finalize`.
  - Generated and validated a schema-backed Video Medium Plan with
    `narrative_depth = micro_journey`, 16 storyboard shots, no text tracks, and
    `rendering_status = not_supported`.
  - Curve written to
    `docs/drafts/cost-tiering/measurements/curves/clean-finalizer-command-2026-07-05.html`.
  - This row was appended to `docs/drafts/cost-tiering/measurements/token-log.jsonl`.
- Caveat: this was successful but not cost-optimal. The first background turn had
  an expensive false start, needed a continuation prompt, and used the existing
  compact fixture / prior disposable output as shape and enum-vocabulary guidance.
  Treat it as proof that the deterministic command keeps schema expansion out of
  model-visible context, not as the final ideal authoring-cost number.

Strict no-example finalizer diagnostic from 2026-07-05:

- Ran one more fresh Codex Desktop thread with stricter constraints: no compact
  fixture, no prior `.tmp` finalizer packet/output, no finalizer source read, no
  manual schema read, and no full video stack. The thread could read the compact
  recipe and run `bin/artist-os-video-finalize --help`.
- Outcome: failed diagnostic measurement, not a successful benchmark. The compact
  recipe plus CLI help were insufficient for first-pass packet authoring; the
  thread entered a long validator-repair loop, discovering required packet fields
  one error at a time.
- Rollout:
  `~/.codex/sessions/2026/07/05/rollout-2026-07-05T13-50-12-019f339d-e199-7850-96dc-4942de111657.jsonl`
- Result:
  - 85 turns, 166,442 fresh input, 3,726,208 cache read, 16,585 output + reasoning,
    671,743 input-equivalent units.
  - Per-turn context: mean 46k, peak 54k, zero turns above the 90k cap.
  - Lean signals: micro-journey recipe loaded once; full video stack avoided;
    manual schema file reads = 0.
  - Packet written to
    `.tmp/artist-os-cost-tiering/strict-finalizer-run-packet.json`.
  - Final Video Medium Plan did not validate. The last independently observed
    validator failure before stopping was
    `$.symbology_direction: missing required field 'primary_symbolic_representation'`;
    the thread's final report cited the adjacent
    `$.symbology_direction: missing required field 'confirmation_status'` failure
    and confirmed it stopped during packet repair.
  - Curve written to
    `docs/drafts/cost-tiering/measurements/curves/strict-no-example-finalizer-diagnostic-2026-07-05.html`.
  - Do not append this run to `token-log.jsonl` as a successful row.
- Fix implemented after this diagnostic: `bin/artist-os-video-finalize` now exposes
  `--print-template` and `--print-contract`, accepts lean compact-packet aliases,
  fills schema boilerplate internally, and reports missing compact fields as a
  grouped error. `video-micro-journey-recipe.md` now points agents to the printed
  template instead of asking them to infer packet shape from prose, source, schema,
  fixtures, or old `.tmp` outputs. The next measurement should rerun the same
  strict no-example scenario and should no longer enter a validator-discovery loop.

Post-template strict finalizer measurement from 2026-07-05:

- Refreshed the copied Codex dev skill with `bin/install-codex-dev-skills`, then
  reran the same strict no-example laundromat scenario. The background thread was
  allowed to read the compact recipe and use `bin/artist-os-video-finalize
  --print-template` / `--print-contract`, but not fixtures, prior `.tmp` packets,
  finalizer source, the full schema, or the full video stack.
- Output:
  `.tmp/artist-os-cost-tiering/post-template-strict-run-video-medium-plan.json`.
- Independent validation passed with
  `artist_os_schema_validator.validate_file(Path('schemas/video-medium-plan.schema.json'), ...)`.
- Rollout:
  `~/.codex/sessions/2026/07/05/rollout-2026-07-05T14-17-03-019f33b6-76fd-7101-ad80-89b9418a6b36.jsonl`
- Result:
  - 10 turns, 42,630 fresh input, 368,896 cache read, 8,673 output + reasoning,
    148,904 input-equivalent units.
  - Per-turn context: mean 41k, peak 51k, zero turns above the 90k cap.
  - Lean signals: micro-journey recipe loaded once; full video stack avoided;
    `micro_journey` present; manual schema file reads = 0.
  - Generated and validated a schema-backed Video Medium Plan with
    `narrative_depth = micro_journey`, 16 storyboard shots, no text tracks, and
    `rendering_status = not_supported`.
  - Curve written to
    `docs/drafts/cost-tiering/measurements/curves/post-template-strict-finalizer-2026-07-05.html`.
  - This row was appended to `docs/drafts/cost-tiering/measurements/token-log.jsonl`.
- Caveat: one small retry removed optional `audio_cues` after the command rejected
  their shape. This is not the old validator-discovery loop: the run went from the
  failed strict diagnostic's 85 turns / 671,743 input-equivalent units to 10 turns /
  148,904 input-equivalent units, while preserving the same no-fixture/no-source/
  no-schema constraints.
- Follow-up packaging patch: `bin/artist-os-video-finalize` now normalizes compact
  `audio_cues` aliases (`ref` / `cue_id`, `shot_ids`) into schema-backed
  `audio_ref` / `used_by_shot_ids`, with a regression test. A future strict rerun
  should avoid even this optional-cue retry.

Governing model: **`cost ≈ turns × mean-context`**. The bill is ~90–95% re-read
context. Two independent, multiplying levers: cut the number of agent turns, and
cut the context each turn carries. Validate every change by regenerating a per-turn
curve (`measurements/token-curve.py`) and comparing the area under the line to the
Queen Bee baseline (`measurements/curves/queen-bee-2026-06-26.html`).

## Already done (context, not backlog)

- Design note + interactive medium×length artifact-budget grid.
- Measurement tooling: `token-report.py`, `token-curve.py`, `token-log.jsonl`, the Queen Bee baseline curve.
- Short-form video lean path: `skills/artist-os/references/video-micro-journey-recipe.md` + index-first SKILL.md routing (slice 1).
- Thin-index split of `THEORY.md`, `docs/gates-and-reviews.md`, `video-journey.md` into topic files (slice 2, PR #15).
- Local Codex dev install refreshed for testing.

---

## 0. Immediate / unblocking

| Item | What | Notes |
|---|---|---|
| **Conductor eval re-bless** | PR #15's only red test is `test_conductor_eval_lock`, tripped because `SKILL.md` changed (now also by the Schema Load Economy draft — `SKILL.md` + 4 mode files; one re-bless covers both). Run the manual conductor-behavior eval (`bin/artist-os-eval start` → `claude -p` scenarios → grade → `bin/artist-os-eval bless`), commit the re-bless. | Required before #15 merges. Do **not** blind-bless — memory already flags prior blind-blesses as debt, so this is the chance to do a real run. See `evals/README.md`. |
| **Measure the slice-1/2 win** | Run a sub-minute video test through the updated Codex skill, generate its curve, compare to the baseline. | Confirms mean-context + turns actually fell. The whole point of the tooling. |

---

## 1. Core remaining cost levers (designed, low-risk, build next)

These attack `turns × context` directly and carry no contract risk. Build, measure, repeat.

- **Generalize index-first loading to the surfaces still loaded whole.** Slice 2 did THEORY/gates/video-journey. Still monolithic:
  - The heavy **schemas** — `video-medium-plan` (~31KB), `sound-prompt-plan` (~40KB). **Drafted (uncommitted): Schema Load Economy** — a `SKILL.md` rule plus the four mode-file lead-ins (video/text/image/suno) now defer schema reads to record-production/validation time (read → shape JSON → validate in one pass → do not re-read), generalizing the recipe's "load once, at the end." That is the instruction-level half; the deeper *thin authoring view* (a compact per-record field summary so authoring never needs the full schema) or *sectioned schemas* remain the follow-up, still bounded by the validator's same-document `#/$defs` constraint. Conductor re-bless + a lean rerun (`measurements/compare-run.py`) are owed before this counts as proven. (See README "Reference loading".)
  - `skills/artist-os/references/storyboard-prompt-builder.md` (~324 lines) — split into a selector + per-mode recipes (same move as the video split).
  - Large contract/theory docs loaded whole when one section is needed: `docs/metadata-schema.md` (~452), `docs/pipeline-contract.md` (~444), `docs/subagent-orchestration.md` (~350). Apply the thin-index pattern or point phases at sections.
- **Portable reset handoff, built into the conductor.** The host-agnostic "we've reached a good stopping point — continue in a new thread" prompt at reset-eligible checkpoints (after Story Approval, Medium Plan lock, each storyboard/series batch, Output Acceptance). The recipe mentions it for video; the general conductor mechanism (when to fire, the prompt, the packet) is not in `SKILL.md`/the spine. Host-automated thread-spawn (Tier A) is an optional later upgrade. (README "Resume handoff".) **Proven by hand:** the Sage Wells short-form runs were the leanest measured (~41–54k ctx/turn vs ~100–126k for the single-session fairy-tale runs) purely from manual session-splitting, *not* the lean recipe (token-log notes) — i.e. the artist did the conductor's job because nothing prompted it. The artist explicitly reported (2026-06-28) not feeling prompted to start new threads except on the micro-journey path. Shares one primitive with the rehydration packet and the cross-medium warm start below — see **Convergence**.
- **Compact rehydration packet.** A small resume packet (`project.json` + last checkpoint) the agent rehydrates from after a reset/compaction, instead of re-reading the whole source set. Directly kills the post-compaction re-read storm (Pattern B: Queen Bee re-read SKILL.md ~140× and re-ran validation ~386× at turns 176–231). Pairs with the reset handoff.
- **Cross-medium warm start (shared-record reuse).** When a project already has an approved Artist Meaning + Transformation Brief + Beat Plan (+ Story Approval), a request for a *second medium on the same Reference* must **inherit** those medium-neutral records and enter at **Phase 8 (Medium Plan)**, running only the medium-specific tail (Medium Plan → Draft Brief → Critic → Brief Approval → Final Records). Today no path does this: `SKILL.md` routing says only "run that flow to completion, then run the next one" — a full spine from Source Record (`SKILL.md` Routing); and each medium mode file says "Before creating the brief, produce: Transformation Brief, Beat Plan, Medium Plan" with no "…unless they already exist" (e.g. `text-to-suno-plan.md` "Shared Story Records"). Result: the conductor **re-derives the entire meaning spine for the second medium** — the reported "spinning for ages" when an artist finished one journey (e.g. a fairy-tale video) and then asked for a matching Suno track. The records are already designed to be medium-neutral (schemas reference them by `transformation_brief_id` / `beat_plan_id`; the Suno path already says "do not fork a separate sound-only beat structure") — this only makes the conductor *act* on it. Fix = two surgical conductor edits, no contract change: **(a)** a Start Condition / routing branch "new medium on an existing project" that detects the approved shared records (query `artist-os.sqlite` / `project.json`), offers reuse recommendation-first ("You already have an approved Beat Plan and Transformation Brief for [project] — I'll reuse those and just build the Suno-specific plan on top: sonic concept, genre, tempo, vocal/lyric, arrangement. Sound right?"), and enters at Phase 8; **(b)** a one-line "consume the shared records if they already exist; do not re-derive" lead-in on each medium mode file. **Evidence caveat:** diagnosed from the code path — `token-log.jsonl` has no Suno run (all logged runs are video), so quantify with the before/after session transcript if a hard number is wanted. **RESOLVED via grilling 2026-06-28 → design locked in `docs/adr/0012-multi-medium-projects.md` (decisions D1–D8) + `docs/adr/0013-stewardship-activation-threshold.md` (D9); glossary terms added to `CONTEXT.md`.** The model was **reframed**: drop "inheritance / warm start" — a project has one Shared Story Spine and a medium layer that activates any subset of the four media (**Medium Activation**), so reusing the spine is automatic, not a special mode. Continued grilling added D10 (Medium Role: primary fully fleshed out, supporting → compact tier + obeys primary) and resolved D11/D12 → a two-stage model: **Stage 1 planning** (Cross-Medium Plan → prompts) and **Stage 2 packaging** (`docs/adr/0014-package-compilation-stage.md` — a terminal Package Compilation stage that intakes returned assets, arranges them by a named Package Format, gates on completeness, and emits an Asset Package). The Release Package Plan splits along the plan/output seam (planning → Cross-Medium Plan; finished bundle → Package Format / Asset Package). D13/D14 then specified Stage 2's internals: Package Formats live in an index-first `docs/structure-library/package-format/` library (album, article-with-photos, video-with-soundtrack), and the Asset Package is a thin persisted manifest referencing Output Records by id with per-slot completeness (filled/missing/waived). Still unbuilt (edits eval-locked `SKILL.md` → owes re-bless; RPP migration is separate work that must keep Album v1 green).

**Convergence.** The reset handoff, the rehydration packet, and the cross-medium warm start are the *same primitive* viewed three ways: a **compact shared-record packet** (Artist Meaning + Transformation Brief + Beat Plan + last checkpoint). Reset uses it to continue the *same* medium in a fresh thread; warm start uses it to begin a *different* medium without re-deriving meaning. Build the packet once and all three land together — the ideal flow being: finish journey → reset prompt fires → fresh thread → "Resume project X, now make a Suno track from it" → conductor rehydrates the packet and runs only the Sound tail (lean context *and* no re-derivation).
- **Decisions-first / lean-context interview phase.** Front-load all meaning decisions (story, symbology, emotion, style) in a lean context — no implementation docs loaded — then a hard boundary, then load-once-and-execute. Puts the many deliberation turns where context is cheap, and keeps the expensive-context phase to few turns. (README "decisions-first"; this was the front-loading idea.)
- **Apply the lean/express pattern to non-video mediums.** Slice 1 only built the video express path. Text, image, and audio still run the flat spine. Build their lean compact paths per the grid.
- **Validation discipline (valid-first-try).** The ~386 validation reads in Queen Bee were a fix-validate retry storm. Tighten record contracts / recipes so records validate on the first try instead of looping.

---

## 2. Higher-risk levers (grill-gated — do not build until grilled)

- **Scale Gate as a controller.** Promote `workflow_scale_routing` from a label to a controller that selects an artifact-budget profile, making Phase Order phases 5/10/13/16 conditional on `scale_level`. Today the spine is flat for non-video mediums.
- **Scale-gated review count.** Compact = 1 closing review, structured = 2, cumulative/full = full set. Needs a new `reviewer_execution.fallback_reason = compact_scale_inline_review` (with `sub_agent_required: false`) on `schemas/review-record.schema.json` — a change to a **locked contract record**. (The micro-journey recipe deliberately uses the standard bounded review until this lands.)
- **Record collapse (Compact Plan).** Fold brief + beat + medium + generation plan into one lightweight record for the compact tier. Highest risk: must still synthesize `transformation_brief_id` / `beat_plan_id` to keep AGENTS.md traceability, under the validator's `$defs` constraint.
- **Provisional scale read at Routing.** Decide scale before the Transformation Brief so the budget profile applies to phases 3–4 (authoritative routing still lands on the Beat Plan, per ADR 0007).

---

## 3. Verification & governance

- **Targeted Grill Me With Docs session** on the risky decision trees, ideally after a few measured runs: record-collapse traceability, scale escalation/de-escalation mid-flow (a "compact" piece discovered to be cumulative late), resume-handoff failure modes (artist ignores the prompt; resume requested mid-phase), cross-medium warm-start risks (a reused Beat Plan that no longer fits the new medium; an artist who wants the second medium to *diverge* in meaning, not inherit), inline-review independence threshold.
- **Eval coverage for the new behavior.** Per-tier minimum-artifact-set assertion in `evals/`/fixtures to lock the gradient; an assertion that the micro-journey path does not load the full video stack; a **cross-medium warm-start assertion** — a second-medium request on a project with an approved Artist Meaning + Transformation Brief + Beat Plan must *not* re-create those records (reuse by id) and must enter at Phase 8; plus the eval-spec T6 extension and the real conductor-behavior eval run already owed (see the reference-inventory memory).
- **Promote the design note to an ADR** (it amends ADR 0007 on workflow-scale-routing placement) once the model is approved.

---

## 4. Open decisions to resolve

1. Compact Plan: a new schema, or relax the medium-plan schemas conditionally on `scale_level`?
2. For `compact_artifact`, is one closing review enough, or do meaning-critical pieces still need one upstream check?
3. Provisional scale read at Routing: recorded anywhere, or ephemeral until the Beat Plan locks it? What's the minimal resume packet?
4. How are per-cell target counts validated — what does the per-tier minimum-artifact-set eval assert?
5. When exactly does the resume-handoff fire — every reset-eligible checkpoint, a context-size estimate, or both?
6. Which schemas earn a thin authoring view vs staying whole (saving vs validator-`$defs` complexity)?
7. Does `compact_scale_inline_review` need an artist-visible note that this tier trades reviewer independence for cost?
8. Cross-medium warm start: does the inherited Beat Plan need a light *medium-fit* re-confirmation (a song may want different sectioning than a video's shot arc), or does each Medium Plan's "consume the Beat Plan" step already absorb that without a new gate?
9. Is Story Approval inherited as-is for the second medium, or lightly re-affirmed against the new medium before Phase 8?
10. How is the "active project" chosen for a warm start — most-recent row in `artist-os.sqlite`, the project named in the resume packet, or always ask when more than one exists?

---

## Suggested sequence

Bank §0 first (re-bless to unblock #15, then measure the slice-1/2 win on a real run).
Then §1 in any order — each is low-risk and independently measurable; reset handoff + rehydration packet + decisions-first phase together give the biggest turn-count cut for long runs.
Hold §2 until the §3 grill clears the contract/traceability risks.

Operational habit worth adopting now (no code): **one project per session**, and do the
Tier-B reset by hand at clean checkpoints — it's the resume design done manually, and it
yields more before/after baseline curves. **For a second medium from finished work**, do the
warm start by hand too: start a fresh thread and tell it to *resume the existing project and
reuse the approved Artist Meaning / Transformation Brief / Beat Plan*, building only the new
medium's plan on top — e.g. "Resume project X and make a Suno track from its existing Beat
Plan; don't re-derive the meaning." That sidesteps the spine re-derivation until branch (a) ships.
