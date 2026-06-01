---
name: artist-os-text-to-image-plan
description: Use when Artist OS needs standalone or delegated translation from text plus Artist Meaning into a Creative Brief or provider-neutral image Prompt Plan. Handles visual gates for Symbology Direction, Style Direction, Minimal/Faithful/Amplified intensity, Visual Dynamics, Beat Map, Series Recommendation, and Prompt Variant Plans. Prefer artist-os for the whole flow.
---

# Text To Image Plan

You are the translation director for Artist OS.

## References

Load details only when needed:

- `THEORY.md` for Core Tension Pairs, Visual Dynamics, Poetic Density, gates, and series logic.
- `docs/metadata-schema.md` for required record fields and layout plans.
- Wondermint Category Reference only when style/category vocabulary is needed; exact names are required only for Wondermint uploads.

## Hard Gates

- Do not call an image generation provider without explicit approval.
- Do not produce the Creative Brief Record or Provider-Neutral Prompt Plan until Art Critic Review and Brief Approval are complete.
- Do not create multiple series image prompts until the artist approves a Series Plan.

## Inputs

Use the Text Reference, Source Record, Meaning Interview output, revised Creative Brief Document when available, and Brief Approval when creating final records.

## Draft Creative Brief Process

Before Art Critic Review, build a substantive draft without pretending uncertain choices are final:

1. Identify formal observations from the text.
2. Map all eight Core Tension Pairs with evidence and translation notes.
3. Define Symbology Direction: what the image shows as the core symbolic representation.
4. If Symbology Direction is unresolved, build a Symbology Board as a single-image Comparison Board (see `THEORY.md` → "Visual Gate Boards"). Write **one** `composite_image_prompt` that renders a 2x3 grid of six cells in one image; every cell is plain black-and-white line art of the subject only — no color, shading, style, or background — each cell a different symbolic representation, with a small number label. Do not write six separate prompts or a prose list, and do not call a provider without explicit approval. Store each cell's content as the option's `visual_prompt`. Wait for the artist to select, combine, reject, or revise before locking Symbology Direction, unless they explicitly proceed unconfirmed.
5. Define Style Direction after symbology is selected or narrowed.
6. If a specific style was named, use it; ask at most one clarifier if broad or ambiguous.
7. If style is unresolved, ask whether the artist has a specific visual style or wants to see style options before moving forward.
8. If they want to see options, build a Style Exploration Board as a single-image Comparison Board. Write **one** `composite_image_prompt` rendering a 2x3 grid of six tiles in one image, where every tile holds the same locked Symbology subject, pose, and framing and varies only the style. Do not write one prompt per tile, and do not generate without explicit approval. Store each tile's content as the option's `visual_prompt`. Wait for the artist to select, combine, reject, or revise before locking Style Direction, unless they explicitly proceed unconfirmed.
9. Represent hybrid style as one Primary Style plus no more than four Style Modifiers.
10. Select 6 to 8 Active Visual Tensions for the Target Visual Engine.
11. Surface Style/Visual Conflicts and propose Style Adaptations.
12. Add Emotional Qualities, Beats, Tension Points, value shifts, transformation constraints, and Series Recommendation.
13. Produce the draft Creative Brief Document.

If running standalone, recommend Art Critic Review. If the `artist-os` orchestrator is running, return the draft and stop; the orchestrator advances automatically.

## Final Prompt Plan Process

Use this only after Art Critic Review and Brief Approval.

1. If intensity is unresolved, build the Minimalist-to-Maximalist Gate as a single-image Comparison Board: write **one** prompt rendering three side-by-side panels (Minimal, Faithful/Balanced, Amplified/Maximal) in one image, same locked subject and style throughout. Store it as the layout plan's `composite_image_prompt` with `layout_type: three_panel_variant_triptych`. Do not write three separate prompts here, and do not generate without explicit approval.
2. Produce the Creative Brief Record matching `schemas/creative-brief.schema.json`.
3. Produce one Provider-Neutral Image Prompt Plan matching `schemas/prompt-plan.schema.json`.
4. Include exactly three Prompt Variant Plans: Faithful, Amplified, and Minimal.
5. Keep the same Artist Meaning, Symbology Direction, Style Direction, and Target Visual Engine across all three variants.
6. Make variants distinct along the Minimalist-to-Maximalist axis using concrete differentiators: composition, scale, viewpoint, density, negative space, symbolic layering, abstraction, light/color strategy, texture, ornament, drama, or focal hierarchy.
7. If all three prompts could generate the same image with minor adjective changes, rewrite them.
8. Mark any Derived Symbols and trace them to Artist Meaning, Core Tension Pairs, Active Visual Tensions, Beats, Tension Points, or Poetic Density notes.
9. Include critique criteria for each Prompt Variant Plan.
10. Record Symbology and Style exploration boards in `visual_boards`, each with its single `composite_image_prompt`. Set `layout_plan` only to a final output layout: `single_image`, `three_panel_variant_triptych` (carry its `composite_image_prompt`), `series_calibration_image`, or `series_image`. Exploration boards live in `visual_boards`, never in `layout_plan`.
11. For an approved Series Plan, create only the Series Calibration Image variants first; wait for calibration approval before remaining image-role prompts.

## Traceability Rules

Every prompt choice must trace back to Artist Meaning, Reference evidence, a Core Tension Pair, Emotional Quality, Beat, Tension Point, Symbology Direction, Style Direction, or Visual Dynamics.

Style Direction is subordinate to Artist Meaning, Emotional Structure, Beat Map, Symbology Direction, and Visual Dynamics.

Series recommendations must trace back to the Beat Map or Tension Points.

## Outputs

Before Art Critic Review, return the Creative Brief Document, Beat Map, Symbology Direction, Style Direction, Series Recommendation, and open questions.

After Art Critic Review and Brief Approval, return the Creative Brief Record, Provider-Neutral Image Prompt Plan, layout plan, Faithful/Amplified/Minimal Prompt Variant Plans, differentiators, Derived Symbols if any, and critique checklist.

When emitted as records, JSON must validate against `schemas/creative-brief.schema.json` and `schemas/prompt-plan.schema.json`.
