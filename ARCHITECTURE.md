# Architecture

Artist Generation is an agent operating system for transforming artistic intent across media.

## First Vertical Slice

The First Slice is Text Reference to Image Prompt Plan:

```text
Text Reference
  -> Source Record
  -> Meaning Interview
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
  -> critique checklist
  -> Workspace Library persistence
```

No paid generation call is required for the First Slice.

Use `artist-os` as the normal orchestration skill for this workflow. It moves through the role skills automatically and stops only at artist-input or approval gates. The individual role skills remain available for debugging, resuming, or improving one phase.

## Data Flow

1. `artist-os` starts the workflow and conducts the phase handoffs.
2. `artist-os-ingest-reference` creates a Source Record.
3. `artist-os-meaning-interview` captures Artist Meaning and transformation constraints.
4. `artist-os-text-to-image-plan` creates the first pass of Artist Meaning, Emotional Structure, and Beat Map.
5. `artist-os-text-to-image-plan` defines Symbology Direction first, using six concise symbolic options when unresolved, asking whether the work should become a single image, emotional arc, or multi-image presentation, and keeping the full board prompt internal unless the artist asks for it.
6. `artist-os-text-to-image-plan` uses Style Direction directly if specific, or asks whether the artist has a specific vision or wants style exploration.
7. If style remains broad or unresolved, `artist-os-text-to-image-plan` shows six concise suggested styles, asks whether the artist wants one of them or something else, and keeps the full board prompt internal unless requested.
8. `artist-os-text-to-image-plan` adds Symbology Direction, Style Direction, and Series Recommendation to the draft Creative Brief Document.
9. `artist-os-art-critic-review` is mandatory. It strengthens the Creative Brief Document, resolves Open Questions, improves Symbology Direction, Style Direction, and Visual Dynamics, and increases Poetic Density without overriding Artist Meaning.
10. After Brief Approval, if intensity remains open, `artist-os-text-to-image-plan` shows three concise Minimal / Faithful-Balanced / Amplified-Maximal detail options before prompt locking.
11. `artist-os-text-to-image-plan` creates the Creative Brief Record and one Provider-Neutral Image Prompt Plan with Faithful, Amplified, and Minimal Prompt Variant Plans based on the approved Symbology Direction and Style Direction.
12. If the artist approves a Series Plan, `artist-os-text-to-image-plan` creates three calibration Prompt Variant Plans for the Series Calibration Image first.
13. After the artist approves one calibration direction, `artist-os-text-to-image-plan` records the Calibration Choice and can create one Provider-Neutral Image Prompt Plan per remaining Image Role.
14. `artist-os-critique-asset` compares the Prompt Plan or Generated Work against the approved Creative Brief.
15. The Workspace Library records prompts, settings, outputs, image paths, sidecar metadata, and review notes. Image sidecars validate against `schemas/asset-metadata.schema.json`, and the SQLite index at `workspace-library/artist-os/artist-os.sqlite` is refreshed from those files.

## State Model

```text
reference_added
source_record_created
meaning_interview_complete
draft_brief_created
art_critic_review_complete
brief_approved
creative_brief_record_created
prompt_plan_created
series_plan_approved
series_calibration_approved
critique_complete
archived
```

## Product Boundaries

Artist OS separates build-process documentation from product behavior.

- `README.md`, `PROGRESS.md`, and planning docs guide how this repository is being built.
- `THEORY.md`, `ARCHITECTURE.md`, `CONTEXT.md`, schemas, examples, and `skills/` define product behavior.
- Provider setup, API keys, host adapters, setup scripts, and media ingestion come after the manual workflow is proven.
- `workspace-library/artist-os/` stores private project records and media locally and is ignored by git.
- `workspace-library/artist-os/artist-os.sqlite` is the local query index for resuming projects across sessions; the project folders remain the durable source artifacts.

## Provenance Invariant

Every Prompt Variant Plan and Generated Work must trace back to:

- Artist Meaning,
- evidence from the Reference,
- the Creative Brief,
- Style Direction,
- Emotional Structure,
- Visual Dynamics,
- the Beat or Tension Point,
- the Transformation Plan,
- the Provider-Neutral Prompt Plan,
- and the Output Record when generation exists.

## Provider Boundary

Generation providers come later. The first implementation produces Provider-Neutral Prompt Plans. A later Provider Adapter may call an image model, but it must record provider, model, prompt, settings, seed if available, output path, and cost-bearing approval.
