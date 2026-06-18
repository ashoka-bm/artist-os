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
  -> Minimalist-to-Maximalist Direction
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

Artist OS now has the core of a shared story architecture where every output is one or more approved beats translated into a medium. The existing First Slice and Text-to-Sound Slice remain the implemented dry-run paths, and they now reference a shared Beat Plan while keeping embedded Beat summaries as transitional compatibility fields.

Planning docs for that direction live in:

- `docs/progress.md`
- `docs/story/THEORY.md`
- `docs/story/ARCHITECTURE.md`
- `docs/gates-and-reviews.md`
- `docs/output-journeys/`

Shared schemas for the Transformation Brief, Beat Plan, Long-Work Stewardship Record, Image Medium Plan, Sound Medium Plan, Review Record, Gate Decision, Prompt Branch Set, and Output Record now exist. The image and Suno flows consume the shared Beat Plan through medium-specific planning records; a later cleanup can remove embedded Beat summaries from the medium-specific brief schemas after downstream examples and consumers are stable.

## Data Flow

1. `artist-os` starts the workflow and conducts the phase handoffs.
2. `artist-os-ingest-reference` creates a Source Record.
3. `artist-os-meaning-interview` captures Artist Meaning and transformation constraints.
4. `artist-os-text-to-image-plan` creates the shared Transformation Brief from Artist Meaning, Formal Analysis, Emotional Structure, Poetic Density, transformation constraints, candidate Story Modes, and medium routing.
5. `artist-os-text-to-image-plan` creates the shared Beat Plan. This is the authoritative story spine consumed by image planning.
6. For multi-beat, series, or ambiguous Beat Plans, `artist-os-writing-method-review` runs as a mandatory bounded Beat Reviewer sub-agent before medium planning.
7. For Cumulative Work only, the workflow creates a foundation Long-Work Stewardship Record after Story Approval, then enriches it after the Medium Plan maps approved beats into image roles, text sections, chapters, scenes, or movements.
8. `artist-os-text-to-image-plan` consumes the shared Beat Plan and creates the Image Medium Plan. It defines Symbology Direction first, using six concise symbolic options when unresolved, asks whether the work should become a single image, emotional arc, or multi-image presentation, and keeps the full board prompt internal unless the artist asks for it.
9. `artist-os-text-to-image-plan` uses Style Direction directly if specific, or asks whether the artist has a specific vision or wants style exploration.
10. If style remains broad or unresolved, `artist-os-text-to-image-plan` shows six concise suggested styles, asks whether the artist wants one of them or something else, and keeps the full board prompt internal unless requested.
11. `artist-os-text-to-image-plan` consumes the Image Medium Plan and adds Symbology Direction, Style Direction, medium-local Beat summaries, and Series Recommendation to the draft Creative Brief Document.
12. `artist-os-art-critic-review` is mandatory and runs as a bounded sub-agent. It strengthens the Creative Brief Document, resolves Open Questions, improves Symbology Direction, Style Direction, and Visual Dynamics, and increases Poetic Density without overriding Artist Meaning.
13. After Brief Approval, if intensity remains open, `artist-os-text-to-image-plan` shows three concise Minimal / Faithful-Balanced / Amplified-Maximal detail options before prompt locking.
14. `artist-os-text-to-image-plan` creates the Creative Brief Record with `transformation_brief_id` and `beat_plan_id`, then one Provider-Neutral Image Prompt Plan with Faithful, Amplified, and Minimal Prompt Variant Plans based on the approved Symbology Direction and Style Direction.
15. If the artist wants a curator batch, `artist-os-text-to-image-plan` creates a Prompt Branch Set: usually five meaning-equivalent prompt branches that vary style, setting, symbol, composition, and palette/light while preserving the same kernel.
16. If the artist approves a Series Plan, `artist-os-text-to-image-plan` creates three calibration Prompt Variant Plans for the Series Calibration Image first.
17. After the artist approves one calibration direction, `artist-os-text-to-image-plan` records the Calibration Choice and can create one Provider-Neutral Image Prompt Plan per remaining Image Role.
18. Generation, import, drafting, or human editing creates an Output Record for the concrete Output Artifact before review or acceptance. For Cumulative Work, the Long-Work Stewardship Record is updated with the part status and output reference.
19. `artist-os-critique-asset` runs as a bounded sub-agent and compares the Prompt Plan, Prompt Branch Set, Output Record, or Generated Work against the approved Creative Brief.
20. The Workspace Library records prompts, settings, outputs, image paths, sidecar metadata, stewardship records, and review notes. Output Records validate against `schemas/output-record.schema.json`, image sidecars validate against `schemas/asset-metadata.schema.json`, and the SQLite index at `workspace-library/artist-os/artist-os.sqlite` is refreshed from those files.

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
- Provider setup, API keys, host adapters, and media ingestion come after the manual image and Suno workflows are proven.
- `workspace-library/artist-os/` stores private project records and media locally and is ignored by git.
- `workspace-library/artist-os/artist-os.sqlite` is the local query index for resuming projects across sessions; the project folders remain the durable source artifacts.

## Provenance Invariant

Every Prompt Variant Plan and Output Artifact must trace back to:

- Artist Meaning,
- evidence from the Reference,
- the Creative Brief,
- Style Direction,
- Emotional Structure,
- Visual Dynamics or Sonic Dynamics,
- the Beat or Tension Point,
- the Transformation Brief,
- the Prompt Plan,
- and the Output Record when an output artifact exists.

## Provider Boundary

Generation providers come later. The current implementation produces Provider-Neutral Image Prompt Plans and Suno Sound Prompt Plans as dry-run artifacts. A later Provider Adapter may call a media model, but it must record provider, model, prompt, settings, seed if available, output path, and cost-bearing approval.
