# Architecture

Artist Generation is an agent operating system for transforming artistic intent across media.

## First Vertical Slice

The First Slice is Text Reference to Image Prompt Plan:

```text
Text Reference
  -> Source Record
  -> Meaning Interview
  -> Creative Brief Document
  -> Style Direction
  -> Series Recommendation
  -> Art Critic Review
  -> revised Creative Brief Document
  -> Brief Approval
  -> Creative Brief Record
  -> Provider-Neutral Image Prompt Plan
  -> critique checklist
  -> archive record
```

No paid generation call is required for the First Slice.

## Data Flow

1. `ingest-reference` creates a Source Record.
2. `meaning-interview` captures Artist Meaning and transformation constraints.
3. `text-to-image-plan` creates the first pass of Artist Meaning, Emotional Structure, and Beat Map.
4. `text-to-image-plan` uses Style Direction directly if specified, or runs a short Style Interview when style is unclear.
5. `text-to-image-plan` adds Style Direction and Series Recommendation to the draft Creative Brief Document.
6. `art-critic-review` is mandatory. It strengthens the Creative Brief Document, resolves Open Questions, improves Style Direction and Visual Dynamics, and increases Poetic Density without overriding Artist Meaning.
7. After Brief Approval, `text-to-image-plan` creates the Creative Brief Record and one Provider-Neutral Image Prompt Plan with Faithful, Amplified, and Minimal Prompt Variant Plans.
8. If the artist approves a Series Plan, `text-to-image-plan` creates three calibration Prompt Variant Plans for the Series Calibration Image first.
9. After the artist approves one calibration direction, `text-to-image-plan` records the Calibration Choice and can create one Provider-Neutral Image Prompt Plan per remaining Image Role.
10. `critique-asset` compares the Prompt Plan or Generated Work against the approved Creative Brief.
11. The archive records prompts, settings, outputs, and review notes.

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
