# Illustrated Written Work Journey

The Illustrated Written Work Journey coordinates a written work with planned still images. It is for children's books, comics, picture-book storyboards, story-with-images projects, covers plus interiors, and diagram-rich explainers.

This is not video. If the final work needs timed shots, camera movement, transitions, audio posture, animation, or video-generator direction, route to Video Journey instead.

## Best Fit

Use this journey when the final work should include:

- pages or spreads,
- comic or panel sequence,
- spot illustrations,
- diagrams embedded in a written explanation,
- cover plus interior illustrations,
- reusable character or object reference sheets for consistency.

## Route

```text
Approved Beat Plan with Project-Level Workflow Scale Routing
  -> Character Template / Visual Reference Sheet strategy, when recurring consistency matters
  -> Text Medium Plan
  -> Illustration Plan
  -> Illustration Plan Reviewer
  -> Illustration Plan Approval Gate
  -> Image Journey support for page, spread, panel, diagram, cover, or reference-sheet prompts
  -> Generation Approval Gate, before provider-backed image generation
  -> Output Record, when images are generated or imported
  -> Output Critic Review
  -> Output Acceptance Gate
```

## Gates

- Character Reference Strategy: ask once whether Character Templates and optional Character Reference Sheet prompts are wanted. If declined, record `declined` and do not ask again in that flow.
- Visual Reference Sheet Strategy: for products, objects, settings, or props, ask once when consistency matters.
- Illustration Plan Approval: approve page/spread/panel/diagram logic before bulk image prompt expansion.
- Generation Approval: required for generated reference sheets and generated page/spread/panel/diagram images.

## Reviews

Illustration Plan Reviewer is a bounded cross-medium reviewer. It checks:

- page, spread, panel, and diagram logic,
- text-image fit,
- character consistency,
- visual continuity,
- audience or age fit when relevant,
- whether each image has a clear job,
- reference-sheet prompt alignment when used.

It may use Art Critic and Writing Critic criteria, but it emits one integrated Review Record with `review_role = "illustration_plan_reviewer"`.

## Current Implementation

The planning contract exists through `schemas/illustration-plan.schema.json`, `schemas/character-template.schema.json`, and `schemas/visual-reference-sheet-plan.schema.json`.

Text Journey owns the written artifact. Image Journey owns each generated still image or reference-sheet image. Illustration Plan coordinates the relationship between them without becoming a replacement for either medium plan.
