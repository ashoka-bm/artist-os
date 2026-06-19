# Story Architecture

The story architecture defines the shared route Artist OS uses before branching into image, sound, and future video, text, or mixed-media output.

This is the planning contract for the shared story route. Formal schemas for Transformation Brief, Beat Plan, Long-Work Stewardship Record, Review Record, Gate Decision, and Output Record now live in `schemas/`.

## Shared Journey

```text
Reference Intake
  -> Meaning Journey
  -> Transformation Brief
  -> Story Journey
  -> Long-Work Stewardship, when cumulative
  -> Medium Journey
  -> Prompt Journey
  -> Generation Journey
  -> Output Review Journey
```

## Journey Responsibilities

### Reference Intake

Captures what the artist provided before interpretation.

Outputs:

- Source Record,
- rights notes,
- source context,
- target transformation notes when known.

Gate:

- Routing Gate, if the target output is unclear.

Review:

- no critic review by default; intake is descriptive.

### Meaning Journey

Captures what the Reference means to the artist.

Outputs:

- Artist Meaning,
- must-preserve details,
- may-transform details,
- avoid list,
- success criteria,
- artist emotional language.

Gate:

- Meaning Confirmation Gate.

Review:

- Meaning Reviewer, used when later plans may have drifted from Artist Meaning.

### Transformation Brief

Holds the cross-medium interpretation before Story or Medium planning.

Outputs:

- formal observations,
- Emotional Structure,
- Core Tension Pairs,
- Poetic Density notes,
- transformation constraints,
- candidate Story Modes,
- medium routing recommendation.

Gate:

- Interpretation Gate.

Review:

- optional Meaning Reviewer if the interpretation conflicts with artist-stated meaning.

### Story Journey

Turns the Transformation Brief into a Story / Beat Plan.

When a recognized movement pattern would help the work, select or adapt a Story Structure from `docs/structure-library/story/README.md` and store the project-specific adaptation in `story_structure` on the Beat Plan. The Story Structure guides movement, compression, expansion, and Beat Roles; it does not choose medium, output shape, asset count, or publication format.

Outputs:

- Story Mode,
- Adapted Story Structure, when used,
- Beat Plan,
- Beat Roles,
- tension movement,
- symbolic progression,
- open questions,
- scale recommendation.

Gate:

- Story Gate.
- Story Approval Gate.

Review:

- Story Critic Review.
- Beat Reviewer sub-agent, when beat sequencing or beat size needs a dedicated pass.

### Long-Work Stewardship

Protects projects whose parts build on each other after Story Approval.

Outputs:

- Long-Work Stewardship Record,
- planned Long-Work Parts,
- continuity rules,
- Long-Work Readiness,
- checkpoint plan,
- drift list.

Gate:

- Long-Work Checkpoint Gate.

Review:

- Long-Work Reviewer, used for readiness, checkpoints, cumulative drift, and proposed continuity updates.

The Beat Plan remains the story authority. The foundation record references the approved Beat Plan before medium-specific parts exist; the enriched record references the medium-specific part ids. Long-Work Stewardship does not duplicate beat movement, shot design, text section execution, sonic arrangement, or final acceptance.

Do not use Long-Work Stewardship for non-sequential portfolios, store collections, style explorations, or curator batches unless the parts build on each other.

### Medium Journey

Translates the approved Beat Plan into one or more medium-specific plans.

Outputs:

- Image Medium Plan,
- Video Medium Plan,
- Sound Medium Plan,
- Text Medium Plan,
- Mixed-Media Plan.

Gate:

- Medium Gate.
- medium-specific gates such as Symbology, Style, Motion, Vocal / Lyric, Arrangement, or Text Form.

Review:

- Art Critic Review,
- Video Critic Review,
- Sound Critic Review,
- Writing Critic Review,
- Mixed-Media Critic Review.

### Prompt Journey

Turns an approved Medium Plan into provider-neutral prompt plans.

Outputs:

- Provider-Neutral Image Prompt Plan,
- Video Prompt Plan,
- Sound Prompt Plan,
- Text Generation Plan,
- mixed output package.

Gate:

- Prompt Lock Gate.

Review:

- Prompt Critic Review.

### Generation Journey

Calls a provider only when the artist explicitly approves that call.

Outputs:

- Output Artifact,
- Output Record,
- Generated Work, when provider-generated,
- provider settings,
- cost-bearing approval record,
- sidecar metadata.

Gate:

- Generation Approval Gate.

Review:

- no pre-review beyond Prompt Critic; the Output Artifact is reviewed after it exists.

### Output Review Journey

Compares the generated or drafted output against the approved plan.

Outputs:

- Review Record,
- Output Acceptance Gate Decision,
- revision prompt,
- taste memory note,
- archive/export decision.

Gate:

- Output Acceptance Gate.

Review:

- Output Critic Review, with medium-specific criteria.

## Gates And Reviews

The canonical shared gate order, critic roles, reviewer roles, sub-agent review rule, and blocking behavior live in `docs/gates-and-reviews.md`.

Medium-specific journeys may add local gates, but they should not redefine shared gate order or reviewer authority here.

## Fork Rules

Artist OS can branch after Story Approval:

- one Beat Plan can produce one medium,
- one Beat Plan can produce several medium plans,
- a mixed-media project can coordinate multiple medium plans from the same beats,
- a long work can produce calibration outputs before full production,
- a series should not generate all outputs until the artist approves the sequence and any calibration step.

Do not branch earlier than needed. Artist Meaning and Story Approval should stay shared unless the artist wants different meanings for different outputs.

A project can contain more than one Long-Work Stewardship Record, one per Cumulative Work. Keep them separate when outputs share a project but do not share sequence, dependency, emotional arc, or cumulative continuity.

## Writing Method Integration

The writing methods are creation methods and review methods.

- Use Writing Fragments when the Reference or supporting material is underdeveloped.
- Use Writing Beats to create or review Beat Plans, especially for journey-shaped text, video, sound, image series, or mixed media.
- Use Writing Shape for finished written artifacts such as articles, artist statements, treatments, scripts, essays, and structured text companions.

The integration details live in `docs/writing/README.md`. The source method files in `docs/writing/references/` have higher authority for their own writing behavior.

## Current Repository Fit

The current First Slice can map onto the story architecture like this:

```text
Text Reference
  -> Source Record
  -> Artist Meaning
  -> Transformation Brief
  -> Beat Plan
  -> Long-Work Stewardship Record, when cumulative
  -> Image Medium Plan
  -> draft image Creative Brief
  -> Art Critic Review (Review Record)
  -> Brief Approval
  -> Creative Brief Record
  -> Provider-Neutral Image Prompt Plan
  -> Prompt Critic Review (Review Record)
  -> optional Prompt Branch Set
  -> Output Record, when an artifact exists
  -> Output Critic Review (Review Record)
  -> Output Acceptance Gate Decision
```

The image, Suno, and text workflows now consume the approved Beat Plan instead of each owning its own story model. Medium-specific brief records carry `beat_plan_id` and do not embed duplicate Beat summaries. Cumulative work also carries a Long-Work Stewardship Record so later parts stay traceable to the approved arc without turning non-sequential collections into heavy story projects.
