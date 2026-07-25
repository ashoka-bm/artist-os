# Image Journey

The Image Journey translates an approved Beat Plan into still visual work: one image, an image series, or a calibration image for a larger series. A three-image sequence is treated as an image series, not as a separate output class.

## Best Fit

Use the Image Journey when the final work should be:

- one compressed visual beat,
- a symbolic portrait or object,
- a threshold image,
- an image series,
- a visual style exploration,
- a Wondermint-ready still asset.

## Route

```text
Approved Beat Plan with Project-Level Workflow Scale Routing
  -> Long-Work Stewardship Activation Gate, when recommended or artist-requested
  -> Long-Work Stewardship Record, when activated by the artist
  -> Symbology Gate
  -> Style Gate
  -> Image Medium Plan with Medium-Level Workflow Scale Routing
  -> Draft Image Creative Brief Document
  -> Art Critic Review
  -> Brief Approval Gate
  -> Image Creative Brief Record
  -> Prompt Variant Strategy
  -> Provider-Neutral Image Prompt Plan
  -> Prompt Critic Review
  -> Prompt Lock Gate
  -> Generation Approval Gate
  -> Output Record, when an artifact is generated or imported
  -> Output Critic Review
  -> Output Acceptance Gate
```

## Gates

- Symbology Gate: what should the image show as the core symbolic representation, and should it remain a single image or become an approved image series?
- Style Gate: what visual language should carry the meaning?
- Prompt Variant Strategy: how should Faithful, Amplified, Minimal, or other approved Prompt Variant Plans differ while preserving the locked symbology, style, Shot Design, and Visual Dynamics?
- Series Approval Gate: required before multiple image prompt plans are created.
- Calibration Approval Gate: required before producing the rest of an approved series.
- Long-Work Checkpoint Gate: required when Long-Work Readiness, calibration, or another series checkpoint blocks expansion.

## Reviews

- Story Critic Review happens before this journey when the plan is multi-beat,
  a series, ambiguous, or otherwise meets the shared applicability rule.
- Beat Reviewer sub-agent is mandatory for image series or any ambiguous multi-beat image plan.
- Long-Work Reviewer checks readiness, checkpoints, cumulative drift, continuity rules, and proposed continuity updates when image-series support is active.
- Art Critic Review checks Symbology Direction, Style Direction, Visual Dynamics, image-role distinction, and series coherence as a bounded sub-agent review.
- Prompt Critic Review checks provider-neutral prompt quality, variant distinction, traceability, and missing visual constraints as a bounded sub-agent review.
- Prompt Branch Gate is used when the artist wants a curator batch: multiple meaning-equivalent prompts that vary style, setting, symbol, composition, and other approved axes.
- Output Critic Review checks the generated or imported image against Artist Meaning, Beat Plan, image plan, and prompt plan as a bounded sub-agent review.

## Current Implementation

The current First Slice implements this route through the Provider-Neutral Image Prompt Plan, optional Prompt Branch Set, Output Record, Output Critic Review, and Output Acceptance Gate contracts. The image brief carries `beat_plan_id`; the referenced Beat Plan is authoritative.

When the artist asks for Midjourney prompts, keep the Prompt Variant Plans provider-neutral and add a `provider_targets[]` entry for Midjourney. That entry stores structured controls and renders the Midjourney paste-ready suffix / full prompts. Do not add Midjourney `--` parameters to providers that use API fields, settings panels, or workflows.

For image series or other cumulative image work, recommend Long-Work Stewardship after Story Approval when the ADR 0013 threshold holds, then create the foundation record only if the artist activates it under ADR 0015. Enrich active stewardship after the Image Medium Plan maps Beats to Image Roles and records Medium-Level Workflow Scale Routing. The Image Medium Plan owns Shot Design, amplitude, visual tensions, and image-role details; the stewardship record references Image Role ids and tracks cumulative readiness, checkpoints, part status, continuity rules, and drift.
