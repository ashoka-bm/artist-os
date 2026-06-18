# Image Journey

The Image Journey translates an approved Beat Plan into still visual work: one image, a triptych, an image series, or a calibration image for a larger series.

## Best Fit

Use the Image Journey when the final work should be:

- one compressed visual beat,
- a symbolic portrait or object,
- a threshold image,
- a triptych,
- an image series,
- a visual style exploration,
- a Wondermint-ready still asset.

## Route

```text
Approved Beat Plan
  -> Long-Work Stewardship Record, for triptych or image series
  -> Symbology Gate
  -> Presentation Mode Gate
  -> Style Gate
  -> Detail / Intensity Gate
  -> Art Critic Review
  -> Provider-Neutral Image Prompt Plan
  -> Prompt Critic Review
  -> Prompt Lock Gate
  -> Generation Approval Gate
  -> Output Critic Review
  -> Output Acceptance Gate
```

## Gates

- Symbology Gate: what should the image show as the core symbolic representation?
- Presentation Mode Gate: single image, compressed arc, triptych, or image series?
- Style Gate: what visual language should carry the meaning?
- Detail / Intensity Gate: Minimal, Faithful-Balanced, or Amplified-Maximal?
- Series Approval Gate: required before multiple image prompt plans are created.
- Calibration Approval Gate: required before producing the rest of an approved series.
- Long-Work Checkpoint Gate: required when Long-Work Readiness, calibration, or another series checkpoint blocks expansion.

## Reviews

- Story Critic Review happens before this journey as a bounded sub-agent review.
- Beat Reviewer sub-agent is mandatory for triptychs, image series, or any ambiguous multi-beat image plan.
- Long-Work Reviewer checks readiness, checkpoints, cumulative drift, continuity rules, and proposed continuity updates for triptychs and image series.
- Art Critic Review checks Symbology Direction, Style Direction, Visual Dynamics, image-role distinction, and series coherence as a bounded sub-agent review.
- Prompt Critic Review checks provider-neutral prompt quality, variant distinction, traceability, and missing visual constraints as a bounded sub-agent review.
- Prompt Branch Gate is used when the artist wants a curator batch: multiple meaning-equivalent prompts that vary style, setting, symbol, composition, and other approved axes.
- Output Critic Review checks the generated or imported image against Artist Meaning, Beat Plan, image plan, and prompt plan as a bounded sub-agent review.

## Current Implementation

The current First Slice implements this route through the Provider-Neutral Image Prompt Plan, optional Prompt Branch Set, Output Record, Output Critic Review, and Output Acceptance Gate contracts. The image brief carries `beat_plan_id`; the referenced Beat Plan is authoritative.

For triptychs and image series, create a foundation Long-Work Stewardship Record after Story Approval and enrich it after the Image Medium Plan maps Beats to Image Roles. The Image Medium Plan owns Shot Design, amplitude, visual tensions, and image-role details; the stewardship record references Image Role ids and tracks cumulative readiness, checkpoints, part status, continuity rules, and drift.
