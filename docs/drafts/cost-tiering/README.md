# Cost Tiering — Medium × Length Artifact Budgets

Status: draft, under review. No behavior change yet.

Artist OS should produce fewer supporting documents and run fewer reviews for
short, cheap work, and reserve the full apparatus for long, expensive work. This
note maps every artifact onto a two-axis grid — medium cost on one axis, scope /
length on the other — and proposes two gates that select an **artifact budget**
per cell so only the right records get created at the right moment. The goal is
token spend, not new capability.

This completes the unfinished half of ADR 0007. That ADR already says Workflow
Scale Routing decides "which planning, stewardship, **review**, and continuity
supports are needed for the scale of a work." Today only the stewardship half is
wired: `compact_artifact` merely routes Long-Work supports into
`skipped_supports`. The review and planning halves were specified but never
enforced, so every project runs the full spine. This note specifies that
enforcement. It does not propose a new standalone routing record (ADR 0007 keeps
routing as a compact field on the Beat Plan and Medium Plan; that holds).

## The problem: the spine is flat, not graduated

A four-line poem and a feature film run the same 17-phase spine
(`skills/artist-os/SKILL.md` → "Phase Order") and the same mandatory reviews.
Two flat costs dominate, and neither shrinks with scope:

1. **Mandatory sub-agent reviews.** `docs/gates-and-reviews.md` → "Review
   Execution Rule" and `SKILL.md` both state *all* review stages are mandatory
   bounded sub-agent reviews. Reviewers fire at phases 5, 10, 13, and 16; each
   spawns a fresh sub-agent that reloads a packet plus
   `schemas/review-record.schema.json` and emits a full Review Record. A compact
   text piece pays for 3–4 reviewer spawns. This is the single largest line item
   and it is identical at every point on the grid.
2. **Full schema-backed records.** A compact text piece still creates Source
   Record → Artist Meaning → Transformation Brief → Beat Plan → Medium Plan →
   Draft Brief → Creative Brief Record → Text Generation Plan → Output Record.
   Several are backed by 14–21KB schemas, so the outputs are large too. Nine
   heavyweight records for something a paragraph could carry.

There is currently no reduction for compact work beyond skipping Long-Work
Stewardship. The only precedent for scale-aware shaping is video's
`micro_journey` classification, which skips full Story Structure
(`CONTEXT.md`). This note generalizes that instinct across all mediums.

## The grid

Y axis is medium cost (text cheapest → video most expensive). X axis is scope /
length, reusing the existing `workflow_scale_routing.scale_level` enum. Each cell
is a **target** artifact budget — the count of records plus reviews a work in
that cell should produce. Numbers are illustrative targets to show the gradient,
not hard quotas; the budget profiles below are the contract.

| Medium ↓ / Scope → | Compact | Structured single | Cumulative | Full long-form |
|---|---|---|---|---|
| **Video** | 9 | 14 | 21 | 30 |
| **Audio** | 7 | 11 | 16 | 22 |
| **Image** | 6 | 9 | 14 | 20 |
| **Text** | 4 | 7 | 12 | 17 |

Today every cell sits near the top-right value (~12–15 minimum, regardless of
position) because the spine is flat. The target is the gradient above: the
text-compact origin drops to ~4 artifacts; only video full long-form carries the
full ~27.

An interactive version of this grid is in `artifact-budget-grid.html` (open it in a
browser). Click any cell to pin its concrete record, review, and scale-support list
to the side panel; it stays pinned until another cell is selected, and hovering only
peeks without changing the panel. Each item carries a size badge (XS–XL, from its
backing schema/record footprint) and each cell shows a cost subtotal, so the grid
exposes expense — not just document count. Reviews are flagged as sub-agent runs,
the dominant token cost. The count badges equal the length of each cell's actual
document list, refining the illustrative counts above.

## Two dials

The grid is governed by two independent dials. Their product selects the cell.

### Dial 1 — Scope / Scale (the X axis)

Keyed on `workflow_scale_routing.scale_level`, already recorded on the Beat Plan
and Medium Plan. This dial selects a **review budget** and a **record-collapse
level**:

| Scale tier | Reviews run | Record shape |
|---|---|---|
| `compact_artifact` | 1 — Output Critic only | Collapse: one Capture note (Source + Meaning) + one Compact Plan (brief + beat + medium + generation/prompt plan folded) + Output Record |
| `structured_single_artifact` | 2 — one upstream critic (Story or Brief) + Output Critic | Keep Beat Plan, Medium Plan, Creative Brief Record, Prompt/Generation Plan, Output Record; Transformation Brief may fold into the Medium Plan |
| `cumulative_work` | full set (5, 10, 13, 16) | Full spine + Long-Work Stewardship + checkpoints |
| `full_long_form_project` | full set + interval/pre-completion/completion checkpoints | Everything, including readiness gates |

Review collapse is the larger and lower-risk saving: it touches no schema and no
provenance field. Record collapse is the larger structural change and carries
the one risk called out below.

### Dial 2 — Medium (the Y axis)

Already chosen at Routing; selects the spine variant and the medium-specific
extras. The lever is to let cheap mediums skip expensive extras at low scope:

- **Text** — cheapest. Compact skips HTML mockup, Clear Writing Pass, and Human
  Voice Pass unless asked. `text-medium-plan`, `text-creative-brief`,
  `text-generation-plan`; Illustration Plan only for illustrated work.
- **Image** — Symbology and Style Comparison Boards, Series Plan (sequential),
  Prompt Branch Set (portfolio), optional Character Template + Visual Reference
  Sheet. Compact single image skips the comparison boards.
- **Audio** — `sound-medium-plan`, `sound-creative-brief`, `sound-prompt-plan`
  (the largest schema in the repo), Suno platform rendering, sequence plans.
  Compact sketch skips platform rendering and sequence plans.
- **Video** — richest. Video Medium Plan (storyboard frame prompts embedded),
  composite storyboard sheet, style/reference image batch, Video Critic Review.
  Compact (`micro_journey`) skips full Story Structure and the style/reference
  batch. Note v0 already omits a Video Prompt Plan and its critique.

## Placement: provisional at Routing, authoritative at Beat Plan

ADR 0007 keeps scale routing internal (not an artist-facing gate) and recorded on
the Beat Plan. To stop paying for a full Transformation Brief before the tier is
known, the conductor makes a **provisional scale read** at Routing that selects
the budget profile for phases 3–4, then the Beat Plan records the **authoritative**
`workflow_scale_routing` as today. The provisional read only ever lowers cost up
front; the Beat Plan can still escalate the tier, which re-expands the budget
before medium planning. This honors 0007 (still internal, still Beat-Plan-recorded)
while letting the profile influence earlier phases. No new artist gate is added —
scale stays a routing inference, surfaced only if the artist's request is
ambiguous about scope.

## Short-form video: lean recipe + batched many-shot planning (the "express" path)

Naming note: this is about *turn-economy, not shot-economy*. The output is a fluid,
dynamic sub-minute video — typically ~one cut every 1–3 seconds, so roughly 20–60
distinct shots. The saving is in conversational turns, not in shots. "Single-pass"
means we plan the whole dense shot list in one batched pass, not that we make a
one-shot video.


Sub-one-minute social video (`micro_journey`, the video/compact cell) is the
highest-traffic compact case and today the most over-served. A 20-second clip
still hydrates the full video stack — `skills/artist-os/references/video-journey.md`,
`skills/artist-os/references/storyboard-prompt-builder.md` (~324 lines), the
**31KB** `schemas/video-medium-plan.schema.json`, and THEORY's gate sections —
all of which sit in the conductor context and are **re-billed on every turn**.
`micro_journey` is currently only a `narrative_depth` classification *inside* that
full plan; it lightens Story Structure but does not lighten the load. That
re-billed context, not the records or reviews, is the dominant cost.

Express rules for the video/compact cell:

- **Do not hydrate the full video stack.** Load a one-screen micro-journey recipe,
  not video-journey + storyboard-prompt-builder + the 31KB schema + THEORY gates.
- **One folded Compact Video Plan** (capture + format + style + continuity scan +
  storyboard frame prompts), not a full Video Medium Plan.
- **One inline review pass**, not two sub-agent spawns (see Context budget below).
- **Batched, few-turn planning — not shot-by-shot.** Produce the full dense shot list
  and storyboard frame prompts (the ~20–60 fluid cuts) in one batched pass from the lean
  recipe, then persist and stop. The failure mode to avoid is iterating one shot per turn
  across dozens of turns (Queen Bee). Do not compress the cut count to save turns — a
  fluid video needs its shots; save turns by batching the planning, not by thinning the
  edit. (Keeps the existing "don't force several beats into one panel" rule.)

Effect: a fluid multi-shot storyboard produced in a handful of batched turns instead of
dozens, with the lean recipe replacing the full stack. The win is the collapse of
re-billed per-turn context (roughly 20k+ → a few thousand) multiplied by far fewer turns
— the `cost ≈ turns × mean-context` model, attacked on both factors.

## Context budget: sub-agent vs inline, and the resume handoff

Two facts reframe cost for interactive flows:

- The conductor's whole context is **re-billed every turn**, so a lean window is the
  primary token lever. Context bloat and token spend are the same problem.
- A sub-agent is a **context-isolation tool, not inherently a cost-saver**. It costs
  a one-time isolated spawn (its own system prompt + the ~10KB review schema +
  packet) but keeps heavy review work out of the parent window. That trade only
  pays off when the parent has a long tail of turns to protect.

So gate the review *mechanism* by scale:

- `compact_artifact` / `structured_single_artifact` → **one inline fresh-eyes review
  pass**. Reuse the existing fallback-separated-pass machinery, but add a third
  legitimate `reviewer_execution.fallback_reason` = `compact_scale_inline_review`
  with `sub_agent_required: false`, so it is a sanctioned cost choice rather than a
  degraded host fallback. Tradeoff: loses reviewer independence (the conductor
  checks its own plan); acceptable at low stakes; keep the pass a delimited meaning
  check, not a rubber stamp.
- `cumulative_work` / `full_long_form_project` → **keep bounded sub-agent reviews**.
  The long tail of turns makes context isolation worth the spawn.

**Resume handoff at reset-eligible checkpoints.** Long journeys already persist full
state to disk at each Long-Work checkpoint (`project.json`, `events.jsonl`, SQLite
index), so context can be reset and rehydrated from a compact packet.

Measured cost model (from the Queen Bee curve, `measurements/curves/`):
**cost ≈ turns × mean-context.** Queen Bee = 244 turns × ~126k mean context ≈ 30.7M;
50% of the spend accrued after turn 126; Codex auto-compacted ~3× but only once
context hit ~227k. So the trigger was ~2.5× too high. Two independent, multiplying
levers: cut turn count (express path / single-shot) and cap per-turn context at
**~90k**.

Reset-eligible checkpoints — reset only at a point in the unfoldment where state is
fully persisted and the artist is not mid-decision: after Story Approval, after
Medium Plan lock, after each storyboard / series batch, after an Output Acceptance.
Never reset mid-task. Fire when a reset-eligible checkpoint is reached **and**
(context > ~90k or turn count is high).

Mechanism. The portable handoff is **what Artist OS implements** — deliberately
host-agnostic, because hosts differ in their own context/compaction settings and we
will not depend on those:

- **Primary — portable handoff prompt (host-agnostic).** At a reset-eligible checkpoint
  the conductor states that the run reached a good stopping point and everything is
  saved, then emits a paste-ready prompt to continue in a fresh thread:

  > We've reached a good stopping point and everything is saved. To save tokens, start
  > a new thread and paste this to continue:
  > "Resume Artist OS project [project_id] from [checkpoint]. Load project.json and the
  > last checkpoint; do not replay history. Next: [next phase]."

  Works on any host; nothing relies on the host's own context settings.
- **Optional — host-automated reset.** Where a host exposes session/thread spawning, the
  conductor may open the fresh thread itself and tell the artist "I started a new thread
  to save context — you can close this one." A seamless upgrade, not a requirement — the
  model cannot clear its own window, so this needs explicit host support.

The resume packet (project.json + last checkpoint) names the project id, checkpoint, and
next phase — enough to rehydrate without replaying the transcript. Re-run
`measurements/token-curve.py` on a future run and drop the HTML next to the baseline in
`measurements/curves/` to confirm the area under the curve shrank.

## Reference loading: index first, detail on demand

The largest loads after the spine are reference material, and the structure
libraries already model the right pattern: a thin index
(`docs/structure-library/story/README.md`,
`docs/structure-library/cultural-format/README.md`) plus one per-entry file, with
`SKILL.md` loading **only the selected entry** — not all ten. Adopt this as a
general loading rule and extend it to surfaces that still load whole:

- **Schemas** — the biggest monolithic loads (`video-medium-plan` ~31KB,
  `sound-prompt-plan` ~40KB). A record author rarely needs the full schema, only the
  active subset. Either split into a thin field index + sectioned detail, or keep one
  validation schema but author from a compact template and validate once at persist
  time. This is the hard one: it intersects the hand-rolled validator's same-document
  `#/$defs` constraint, so the full schema must stay loadable for validation even if
  authoring uses a lighter view.
- **Multi-mode reference files** that bundle several modes in one document — the video
  stack covers `full_story`, `micro_journey`, and `utility_sequence` together;
  `storyboard-prompt-builder.md` is ~324 lines. Split into a small selector + per-mode
  recipe so a micro-journey loads only its recipe (the same move as the express path
  above).
- **Large contract / theory docs** (`THEORY.md`, `pipeline-contract.md`,
  `metadata-schema.md`) loaded whole when one section is needed — point a phase at the
  section, not the file.

Principle: every reference surface should be loadable as index-first, detail-on-demand.
The index carries just enough to choose; the detail file is fetched only for the item
chosen.

## Measuring real spend (usable now)

Before and after any change, baseline with real data rather than the estimated cost
weights. Claude Code transcripts (`~/.claude/projects/<slug>/<session-id>.jsonl`)
carry per-turn `usage`: fresh input, cache creation, cache read, and output tokens.
`measurements/token-report.py` totals these for a session (and sub-agent transcripts),
and `measurements/token-log.jsonl` accumulates one record per test run, tagged by
medium / scale_level / output_kind. A first real data point — this 131-turn design
session — already shows the split: cache read + cache creation ≈ 60% and output ≈ 38%
of the billable-equivalent, fresh input ≈ 1%. That is the thesis confirmed: context
size and output volume are the cost.

Real Artist OS video runs measured (Codex, gpt-5.5, 2026-06-25..27, this repo) sharpen
the priority order. Four short-form-intent creation runs, all **90–95% `cache_read`**:

| run | raw tokens | turns |
|---|--:|--:|
| influencer post (sub-1-min social) | 8.7M | 81 |
| Star Money (fairy-tale video) | 12.7M | 89 |
| White Snake (fairy-tale video) | 23.0M | 192 |
| Queen Bee (fairy-tale video) | 30.7M | 244 |

Cost tracks **turns**, not output: generation is only ~100–190k in every one; the rest
is re-read context growing with each turn (Queen Bee's 244 turns is why it tops 30M).
Review sub-agents add ~945k combined (4 reviews, 142k–318k each) — only ~4% of a bloated
run. None of these were near a clean single-shot; each looped for dozens-to-hundreds of
turns with no context reset.

The correction this data forces: **conductor context bloat (cache_read over many
turns) is the first-order cost, not the reviews.** Lean context — index-first
loading, fewer turns, single-shot compact runs, and the resume/reset handoff — is the
top lever. Review-gating is real but second-order; it matters more *after* context is
lean (when ~945k of reviews is ~20% of a slim run rather than 4% of a bloated one).

Run more projects across cells to keep building the picture; see `measurements/README.md`.

## The one risk: traceability under record collapse

`AGENTS.md` requires provenance: every plan traces to the Creative Brief, and
final records carry `transformation_brief_id` and `beat_plan_id`. Collapsing the
brief + beat + medium + plan into one Compact Plan must therefore still **synthesize
those IDs** (self-referential within the collapsed record) so the audit trail and
downstream `*_id` references stay valid. The schema validator's same-document
`#/$defs` constraint and the existing required-field contracts must keep passing.
Review collapse carries no such risk. This asymmetry is why a phased rollout
should land review-gating first.

## Open questions to resolve before implementation

1. Is the Compact Plan a new schema, or do we relax the existing Medium Plan to
   absorb brief + generation-plan fields when `scale_level = compact_artifact`?
2. For `compact_artifact`, is one closing Output Critic review enough, or do
   meaning-critical pieces (e.g. a poem that hinges on one image) still warrant a
   single upstream meaning check?
3. Does the provisional-scale read at Routing need to be recorded anywhere, or is
   it ephemeral until the Beat Plan locks it?
4. How do the per-cell target counts get validated — do the eval fixtures gain a
   "minimum artifact set" assertion per tier so regressions are caught?
5. When should the resume-handoff prompt fire — every Long-Work checkpoint, a
   working-context-size estimate, or both? And what is the minimal resume packet?
6. For reference splitting, which schemas earn a thin authoring view versus staying
   whole (token saving vs the validator's same-document `#/$defs` complexity)?
7. Does `compact_scale_inline_review` (with `sub_agent_required: false`) need an
   explicit artist-visible note that this tier trades reviewer independence for cost?

## Next builds (decided 2026-06-27)

1. **Index-first reference loading** — split the heaviest reference surfaces (video stack,
   `storyboard-prompt-builder.md`) and make index-first a stated rule. Low-risk; cuts
   mean-context on every run.
2. **Portable reset handoff** — the host-agnostic "good stopping point → continue in a new
   thread" prompt at reset-eligible checkpoints, built into Artist OS itself (explicitly
   not host compaction settings, which vary per user).
3. **Lean recipe + batched many-shot planning** for short-form video — folds into (1);
   reframed as turn-economy (fluid multi-shot output, far fewer turns).

Record collapse stays deferred pending a targeted grill (traceability). Each build is
validated by regenerating a per-turn curve into `measurements/curves/` and comparing the
area under the line to the Queen Bee baseline.

## Implementation surfaces (not yet touched)

For review only — what a future change would edit:

- `skills/artist-os/SKILL.md` — Phase Order phases 5/10/13/16 become conditional
  on `scale_level`; "all reviewer stages are mandatory" gains a scale clause.
- `docs/gates-and-reviews.md` — "Review Execution Rule" gains the per-tier review
  budget table and the `compact_scale_inline_review` fallback reason.
- `docs/pipeline-contract.md` — "Workflow Scale Routing Contract" gains the
  record-collapse rules alongside the existing stewardship rules.
- `schemas/` — possibly a `compact-plan.schema.json`, or a `scale_level`-conditional
  relaxation on the medium-plan schemas; `review-record.schema.json` enum gains
  `compact_scale_inline_review` and allows `sub_agent_required: false` for it
  (a change to a locked contract record — flag for care).
- `skills/artist-os/references/` — a micro-journey express recipe file + a small
  selector, so compact video routes there instead of loading the full video stack;
  split `storyboard-prompt-builder.md` into selector + per-mode recipes.
- `skills/artist-os/SKILL.md` — "Persisting State" / "Autopilot" gain the
  resume-handoff contract (when and how the conductor emits the paste-ready prompt);
  Video routing sends `micro_journey` to the express recipe.
- reference loading — adopt "index first, detail on demand" as a stated rule; candidate
  splits for the heavy schemas and the large theory/contract docs.
- `evals/` — a per-tier minimum-artifact-set assertion to lock the gradient in.
- ADR — promote this note to an ADR once the model is approved (it amends 0007).
