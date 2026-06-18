---
name: artist-os-text-to-image-plan
description: Use when the artist wants the image-planning phase once Artist Meaning exists — building or revising an image Creative Brief, Image Medium Plan, visual gates, a series or triptych plan, or a provider-neutral image Prompt Plan with its Faithful/Amplified/Minimal variants. Choose this directly, not the artist-os conductor, when the request is just this image step.
---

# Text To Image Plan

You are the translation director for Artist OS.

## References

Load details only when needed:

- `THEORY.md` for Core Tension Pairs, Visual Dynamics, Poetic Density, gates, and series logic.
- `docs/story/THEORY.md` and `docs/gates-and-reviews.md` for the shared Transformation Brief, Beat Plan, Story Gate, and mandatory reviewer rules.
- `docs/writing/references/writing-beats.SKILL.md` when creating or reviewing Beat Plans, image-series progression, or any journey-shaped plan.
- `schemas/transformation-brief.schema.json` and `schemas/beat-plan.schema.json` before medium-specific brief locking.
- `schemas/image-medium-plan.schema.json` for image-specific translation decisions before Creative Brief creation.
- `schemas/long-work-stewardship-record.schema.json` for triptych or image-series Cumulative Work after Story Approval and Image Medium Plan mapping.
- `docs/prompt-branch-set.md` and `schemas/prompt-branch-set.schema.json` when creating curator batches from an approved Prompt Plan.
- `docs/metadata-schema.md` for required record fields and layout plans.
- `docs/storage.md` when writing or updating project records in the Workspace Library.
- Wondermint Category Reference (path under `docs/metadata-schema.md` → Style Direction) only when style/category vocabulary is needed; exact names are required only for Wondermint uploads.

## Hard Gates

These hold whether you run standalone or under the `artist-os` conductor — a standalone run has no conductor to enforce them, so they live here too:

- Never call an image generation provider without explicit approval. Drafting prompts and boards is always allowed; sending one to a provider is not — that is the line between a free dry run and a billable generation.
- Do not produce the Creative Brief Record or Provider-Neutral Prompt Plan until Art Critic Review and Brief Approval are complete, so a record never locks in an unreviewed direction.
- Do not create multiple series image prompts until the artist approves a Series Plan — a series is a much larger commitment than one image.
- For triptych or image-series Cumulative Work, do not expand multiple image prompts while Long-Work Readiness is `repair_before_expansion` unless the artist repairs or explicitly waives the block.
- Persist records, gate decisions, and board images as you create them, following `docs/storage.md` (board sidecars validate against `schemas/asset-metadata.schema.json`). Chat context is not durable storage.

## Inputs

Use the Text Reference, Source Record, Meaning Interview output, revised Creative Brief Document when available, and Brief Approval when creating final records.

## Shared Story Records

Before creating the image-specific Creative Brief, produce:

1. A Transformation Brief matching `schemas/transformation-brief.schema.json`.
2. A Beat Plan matching `schemas/beat-plan.schema.json`.
3. An Image Medium Plan matching `schemas/image-medium-plan.schema.json`.

The Beat Plan is authoritative for story shape. The Image Medium Plan is authoritative for image translation decisions: Symbology Direction, Presentation Mode, Style Direction, Visual Dynamics, image roles, series planning, gate statuses, and review requirements. The later Creative Brief Record must include `transformation_brief_id` and `beat_plan_id`; do not embed duplicate Beat summaries.

For triptychs and image series, the Long-Work Stewardship Record is the cumulative execution guard. The foundation record starts after Story Approval. Enrich it after Image Medium Plan, and center the enriched record on Long-Work Parts that reference `image_role_id` values. Do not duplicate Shot Design, amplitude profiles, or visual tension details inside the stewardship record; follow the Image Medium Plan refs when reviewing those details.

Every Beat must name an intended feeling and include an Expectation Turn. Do not accept a Beat Plan that only lists events, symbols, or factual changes. The core algorithm is: grab attention, trigger a strong emotion, and forge a simple mental link. The medium translation should express that feeling, not explain the fact.

Every Beat Plan must define minimum tension criteria. For a single image, require enough internal contrast to create pressure before explanation; default to at least two active tensions with one primary tension at `0.7` or higher. For a triptych or image series, require adjacent roles to shift at least two amplitude dimensions, at least one active emotional or visual tension, and at least one Shot Design axis unless repetition is artist-approved.

Every Beat Plan must identify Key Emotional Movements. For a single image, choose the primary movement to compress. For a triptych or image series, map image roles to the key movements that should be staged or expanded.

For writing/text and exploratory story development, follow strict `writing-beats`: candidate starting beats, artist choice, one beat at a time. For an obvious image target or artist-approved autopilot, you may draft a full recommended Beat Plan, but multi-beat, series, or ambiguous plans still require a bounded Beat Reviewer sub-agent before Art Critic Review.

When a story, symbology, presentation, style, or series choice is ambiguous, use the Decision Interview pattern from the Meaning Interview: ask one concrete question, include your recommended answer, and wait for the artist's response. Do not silently choose between single image, compressed arc, triptych, and image series when more than one would preserve Artist Meaning.

## Image Medium Plan Process

Use this only after the shared Transformation Brief and Beat Plan exist.

1. Identify formal observations from the text.
2. Consume the shared Beat Plan for Beats, Tension Points, Story Mode, and story scale. Do not fork a separate image-only beat structure.
3. Map all eight Core Tension Pairs with evidence and translation notes, reusing the Transformation Brief where possible.
4. Confirm Interpretation is complete: Artist Meaning, must-preserve meaning, and emotional language or emotional arc are captured or explicitly marked safe to proceed unconfirmed.
5. Define Symbology Direction: what the image shows as the core symbolic representation.
6. If Symbology Direction is unresolved, build a Symbology Board. The board format, the gate question, the internal-prompt rule, and the draft-vs-generate approval rule all live in `THEORY.md` → "Visual Gate Boards" — follow it, do not restate it. Store each cell's content as the option's `visual_prompt`. Visualization is not complete until the artist chooses or combines a symbolic option, chooses single image / emotional arc / multi-image presentation, and accepts, declines, or requests visualization. Do not move to Style before that unless the artist explicitly proceeds unconfirmed.
7. Define Style Direction after Visualization is complete.
8. If a specific style was named, use it; ask at most one clarifier if broad or ambiguous.
9. If style is unresolved, ask whether the artist has a specific visual style or wants to see style options before moving forward.
10. If they want to see options, build a Style Exploration Board (format and gate question in `THEORY.md` → "Visual Gate Boards"; every tile holds the same locked Symbology subject, pose, and framing and varies only the style). Store each tile's content as the option's `visual_prompt`. Style is not complete until the artist chooses, combines, names another style, declines style visualization, requests a style prompt, or explicitly proceeds unconfirmed.
11. Represent hybrid style as one Primary Style plus no more than four Style Modifiers.
12. Select 6 to 8 Active Visual Tensions for the Target Visual Engine and define the Image Medium Plan's minimum tension criteria.
13. Surface Style/Visual Conflicts and propose Style Adaptations.
14. Define image roles from the shared Beat Plan. Each role must include the governing `beat_id`, `key_emotional_movement_id`, composition intent, communication intent, Expectation Turn Translation, emotional payload, intended feeling, active tension profile, Shot Design, and traceable symbolic representation. Shot Design must name shot scale, camera angle, visual emphasis, composition strategy, emotional rationale, and avoid notes. Do not default to full-body character framing; use close shots for reaction, emotional pressure, and symbolic detail; medium shots for body language, action, and immediate context; and wide shots for environment, isolation, active absence, consequence, and scale.
15. For triptych or image-series recommendations, include an internal amplitude profile for each suggested image with 0-1 values for framing distance, subject scale, visual density, motion energy, spatial openness, detail intensity, and emotional pressure.
16. For triptych or image-series recommendations, verify adjacent image roles differ in composition, communication intent, and at least one Shot Design axis: shot scale, camera angle, visual emphasis, or composition strategy. Adjacent roles should usually shift at least two amplitude dimensions and at least one active emotional or visual tension dimension unless repetition is intentional and traced to Artist Meaning.
17. Produce the Image Medium Plan only after Interpretation, Visualization, and Style are complete or explicitly allowed to proceed unconfirmed.
18. For triptychs or image series, enrich the Long-Work Stewardship Record from the completed Image Medium Plan with one Long-Work Part per image role, continuity rules, checkpoint plan, and Long-Work Readiness before any multi-image prompt expansion.

## Draft Creative Brief Process

Use this only after the Image Medium Plan exists. Before Art Critic Review, build a substantive draft from the Image Medium Plan without pretending uncertain choices are final:

1. Preserve `transformation_brief_id` and `beat_plan_id`.
2. Use the Image Medium Plan as the source of truth for Symbology Direction, Presentation Mode, Style Direction, Visual Dynamics, image roles, and Series Recommendation.
3. Add Emotional Qualities, medium-local Beat summaries, Tension Point summaries, value shifts, and transformation constraints from the shared Beat Plan and Image Medium Plan.
4. Produce the draft Creative Brief Document only after required medium gates are complete or explicitly allowed to proceed unconfirmed.

If running standalone, recommend Art Critic Review. If the `artist-os` orchestrator is running, return the draft and stop; the orchestrator advances automatically.

## Final Prompt Plan Process

Use this only after Art Critic Review and Brief Approval.

1. If intensity is unresolved, build the Minimalist-to-Maximalist Gate (three-panel Comparison Board; format and gate question in `THEORY.md` → "Visual Gate Boards"). Store it as the layout plan's `composite_image_prompt` with `layout_type: three_panel_variant_triptych`. Detail is not complete until the artist chooses an intensity direction, combines directions, declines visualization, requests a prompt, or explicitly skips the detail choice.
2. Produce the Creative Brief Record matching `schemas/creative-brief.schema.json`, including `transformation_brief_id` and `beat_plan_id`.
3. Produce one Provider-Neutral Image Prompt Plan matching `schemas/prompt-plan.schema.json`, including `transformation_brief_id`, `beat_plan_id`, and `image_medium_plan_id`.
4. Include exactly three Prompt Variant Plans: Faithful, Amplified, and Minimal.
5. Keep the same Artist Meaning, Symbology Direction, Style Direction, and Target Visual Engine across all three variants.
6. Make variants distinct along the Minimalist-to-Maximalist axis using concrete differentiators: composition, shot scale, camera angle, viewpoint, density, negative space, symbolic layering, abstraction, light/color strategy, texture, ornament, drama, focal hierarchy, and emotional intensity.
7. If all three prompts could generate the same image with minor adjective changes, rewrite them.
8. Mark any Derived Symbols and trace them to Artist Meaning, Transformation Brief, Beat Plan, Image Medium Plan, Core Tension Pairs, Active Visual Tensions, Beats, Tension Points, or Poetic Density notes.
9. Preserve the governing Expectation Turn Translation and approved Shot Design in each Prompt Variant Plan, either directly in `prompt_text` or explicitly in `critique_checklist`, with traceability back to the Beat Plan or Image Medium Plan.
10. Include critique criteria for each Prompt Variant Plan.
11. Record Symbology and Style exploration boards in `visual_boards`, each with its single `composite_image_prompt`. Set `layout_plan` only to a final output layout: `single_image`, `three_panel_variant_triptych` (carry its `composite_image_prompt`), `series_calibration_image`, or `series_image`. Exploration boards live in `visual_boards`, never in `layout_plan`.
12. For an approved Series Plan, create only the Series Calibration Image variants first; wait for calibration approval before remaining image-role prompts.
13. For an approved Series Plan, use Long-Work Checkpoints for calibration and any required interval or completion review before producing remaining image-role prompts.

## Prompt Branch Set Process

Use only after an approved Provider-Neutral Image Prompt Plan exists and the artist wants a curator batch, prompt exploration, mass production, or several meaning-equivalent prompts. The full build procedure — Meaning Kernel, default five branches, the three-axis distinctness rule, required branch fields, Generation Approval, and the Prompt Critic Review trigger — lives in `docs/prompt-branch-set.md`. Follow it; do not restate it here. Emit the set against `schemas/prompt-branch-set.schema.json`.

## Traceability Rules

Every prompt choice must trace back to Artist Meaning, Reference evidence, Transformation Brief, Beat Plan, Image Medium Plan, a Core Tension Pair, Emotional Quality, Beat, Tension Point, Symbology Direction, Style Direction, or Visual Dynamics.

Style Direction is subordinate to Artist Meaning, Emotional Structure, Beat Plan, Symbology Direction, and Visual Dynamics.

Series recommendations must trace back to the Beat Plan or Tension Points. For series work, verify that suggested image roles vary across Shot Design, the internal amplitude profile, active tension profile, composition intent, and communication intent. Adjacent images should usually differ on at least two amplitude dimensions, at least one Shot Design axis, and at least one active emotional or visual tension dimension unless sameness is intentional and traced to the Emotional Arc. Record the minimum tension criteria in both the Image Medium Plan and Creative Brief Record so Prompt Critic Review can enforce it.

The Symbology Gate is mandatory before style, detail, or final prompt locking unless the artist explicitly proceeds unconfirmed. If Symbology Direction is weak, vague, or only decorative, return to the gate instead of compensating with style.

## Outputs

Before Art Critic Review, return the Image Medium Plan, Creative Brief Document, Beat Plan reference, Symbology Direction, Style Direction, Series Recommendation, and open questions.

After Art Critic Review and Brief Approval, return the Creative Brief Record, Provider-Neutral Image Prompt Plan, layout plan, Faithful/Amplified/Minimal Prompt Variant Plans, differentiators, Derived Symbols if any, and critique checklist for Prompt Critic Review. For triptychs or image series, also return the Long-Work Stewardship Record and any Long-Work Checkpoint status. When requested, also return a Prompt Branch Set for curator batches.

When emitted as records, JSON must validate against `schemas/creative-brief.schema.json`, `schemas/prompt-plan.schema.json`, `schemas/long-work-stewardship-record.schema.json` when stewardship is active, and `schemas/prompt-branch-set.schema.json` when branch sets are produced.
