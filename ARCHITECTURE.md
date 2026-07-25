# Architecture

Artist Generation is an agent operating system for transforming artistic intent across media.

## First Vertical Slice

The First Slice is Text Reference to Image Prompt Plan:

```text
Text Reference
  -> Source Record
  -> Meaning Interview
  -> Transformation Brief
  -> Beat Plan
  -> Image Medium Plan
  -> Creative Brief Document
  -> Symbology Direction
  -> Style Direction
  -> Series Recommendation
  -> Art Critic Review
  -> revised Creative Brief Document
  -> Brief Approval
  -> Creative Brief Record
  -> Provider-Neutral Image Prompt Plan
  -> optional Prompt Branch Set
  -> Prompt Critic Review
  -> optional Generation Approval Gate
  -> Output Record, when an artifact exists
  -> Output Critic Review
  -> Output Acceptance Gate
  -> Workspace Library persistence
```

No paid generation call is required for the First Slice.

Use `artist-os` as the orchestration skill for this workflow. It moves through the phases automatically, loading the relevant internal mode file on demand, and stops only at artist-input or approval gates. Debugging, resuming, or reworking a single phase happens by asking the conductor — the individual phases are internal mode files, not separately installable skills.

## Cross-Medium Direction

Artist OS uses a shared story architecture where every output is one or more
approved beats translated into a medium. The current dry-run paths are image,
video v0 storyboard planning, sound prompt planning, text drafting, and the
Album workflow. The constrained general Cross-Medium lifecycle is frozen into
1.0 but is not complete; `docs/release-1.0.md` tracks its remaining schema,
conductor, transition, and rehearsal work.

All journeys reference the shared Beat Plan. Medium-specific brief records
carry `beat_plan_id` rather than duplicating embedded Beat summaries.

Planning docs for that direction live in:

- `docs/progress.md`
- `docs/story/THEORY.md`
- `docs/story/ARCHITECTURE.md`
- `docs/gates-and-reviews.md`
- `docs/output-journeys/`

Shared schemas exist for the Transformation Brief, Beat Plan, Long-Work
Stewardship Record, Image, Video, Sound, and Text Medium Plans, Cross-Medium
Plan, Release Package Plan, Review Record, Gate Decision, Prompt Branch Set,
Text Generation Plan, Output Record, and Asset Package. Schema existence is not
the same as end-to-end completion; the release checklist is authoritative.

## Data Flow

The runtime phase sequence — the handoffs between skills and where each gate falls — is owned by the `artist-os` conductor (`skills/artist-os/SKILL.md` → "Phase Order"), and the typed record-to-record transitions are in `docs/pipeline-contract.md`. The First Vertical Slice diagram above shows the end-to-end image path; this section does not maintain a third copy of the step sequence.

## State Model

```text
reference_added
source_record_created
meaning_interview_complete
transformation_brief_created
beat_plan_created
medium_plan_created
draft_brief_created
art_critic_review_complete
brief_approved
creative_brief_record_created
prompt_plan_created
series_plan_approved
series_calibration_approved
critique_complete
output_record_created
output_critic_review_complete
output_acceptance_decided
archived
```

## Product Boundaries

Artist OS keeps public product behavior separate from local project state.

- `README.md` explains installation and usage.
- `THEORY.md`, `ARCHITECTURE.md`, `CONTEXT.md`, `docs/text-to-sound/`, schemas, examples, and `skills/` define product behavior.
- The supported 1.0 host is Codex. Other host adapters, provider setup, API
  keys, and provider-backed generation are post-1.0.
- `workspace-library/artist-os/` stores private project records and media locally and is ignored by git.
- `workspace-library/artist-os/artist-os.sqlite` is the local query index for resuming projects across sessions; the project folders remain the durable source artifacts.

## Provenance Invariant

Every Prompt Variant Plan, Text Generation Plan, and Output Artifact must trace back through the full lineage chain. That chain is defined once in `AGENTS.md` → "Product Invariant"; this doc does not keep a second copy.

## Provider Boundary

Artist OS 1.0 ships no provider adapter. The current implementation produces
Provider-Neutral Image Prompt Plans, platform-neutral Sound Prompt Plans with
Suno Custom Mode field exports, storyboard-ready Video Medium Plans, and Text
Generation Plans with approved local drafting. A future Provider Adapter may
call a media model, but it must preserve the existing approval and provenance
contracts.
