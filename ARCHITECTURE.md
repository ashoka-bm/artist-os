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

Use `artist-os` as the normal orchestration skill for this workflow. It moves through the role skills automatically and stops only at artist-input or approval gates. The individual role skills remain available for debugging, resuming, or improving one phase.

## Cross-Medium Direction

Artist OS now has the core of a shared story architecture where every output is one or more approved beats translated into a medium. The implemented dry-run paths are the First Slice, Text-to-Sound Slice, and Text Journey. They all reference the shared Beat Plan; medium-specific brief records carry `beat_plan_id` rather than duplicating embedded Beat summaries.

Planning docs for that direction live in:

- `docs/progress.md`
- `docs/story/THEORY.md`
- `docs/story/ARCHITECTURE.md`
- `docs/gates-and-reviews.md`
- `docs/output-journeys/`

Shared schemas for the Transformation Brief, Beat Plan, Long-Work Stewardship Record, Image Medium Plan, Sound Medium Plan, Text Medium Plan, Review Record, Gate Decision, Prompt Branch Set, Text Generation Plan, and Output Record now exist. The image, Suno, and text flows consume the shared Beat Plan through medium-specific planning records, then preserve emotional movement and tension criteria through final records and review.

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
- Provider setup, API keys, host adapters, and media ingestion come after the manual image, Suno, and text workflows are proven.
- `workspace-library/artist-os/` stores private project records and media locally and is ignored by git.
- `workspace-library/artist-os/artist-os.sqlite` is the local query index for resuming projects across sessions; the project folders remain the durable source artifacts.

## Provenance Invariant

Every Prompt Variant Plan, Text Generation Plan, and Output Artifact must trace back through the full lineage chain. That chain is defined once in `AGENTS.md` → "Product Invariant"; this doc does not keep a second copy.

## Provider Boundary

Generation providers come later. The current implementation produces Provider-Neutral Image Prompt Plans and Suno Sound Prompt Plans as dry-run artifacts. A later Provider Adapter may call a media model, but it must record provider, model, prompt, settings, seed if available, output path, and cost-bearing approval.
