# Metadata Schema

Artist OS uses records to preserve meaning, provenance, and review history as a Reference moves toward generation.

## Record Types

### Source Record

A Source Record describes the Reference before interpretation.

Required fields:

- `source_id`
- `title`
- `media_type`
- `source_ref`
- `user_context`
- `rights_notes`
- `created_at`

### Creative Brief Record

A Creative Brief Record is the structured agent handoff created after Art Critic Review and Brief Approval.

Required sections:

- `brief_id`
- `source_id`
- `artist_meaning`
- `formal_observations`
- `style_direction`
- `visual_dynamics`
- `core_tension_pairs`
- `emotional_qualities`
- `poetic_density_notes`
- `beats`
- `series_recommendation`
- `transformation_constraints`

### Provider-Neutral Image Prompt Plan

A Provider-Neutral Image Prompt Plan is the structured dry-run generation plan created from an approved Creative Brief Record.

Required sections:

- `prompt_plan_id`
- `brief_id`
- `source_id`
- `target_media_type`
- `plan_mode`
- `provider_neutral`
- `style_direction_summary`
- `target_visual_engine_summary`
- `prompt_variants`
- `series_calibration`
- `traceability_summary`
- `critique_checklist`

## Style Direction

`style_direction` records the artistic language of the generated work. It is separate from Emotional Structure and Visual Dynamics.

Required fields:

- `selection_method`: `artist_specified`, `style_interview`, or `agent_recommended`
- `style_family`
- `style_mode`
- `primary_style`
- `confirmation_status`: `artist_specified`, `confirmed`, or `unconfirmed`
- `style_modifiers`
- `wondermint_subcategories` when available or when preparing Wondermint upload
- `rationale`
- `avoid`
- `style_conflicts`

Hybrid style is allowed, but it must be represented as one `primary_style` plus bounded `style_modifiers`. Avoid equal-weight style pileups.

Style Direction is the last priority. It must not override Artist Meaning, Emotional Structure, Beat Map, or Visual Dynamics. If style conflicts with the Target Visual Engine, record the conflict and proposed style adaptation.

Minimal style conflict fields:

- `style_conflicts[].conflict`
- `style_conflicts[].proposed_adaptation`
- `style_conflicts[].requires_artist_approval`

Use the Wondermint Category Reference at `/Users/ashokaji/code/fullstock/Wondermint Skill File/skills/wondermint-marketplace/skills/references/categories.md` as seed vocabulary for image/video/audio categories. `wondermint_subcategories` are useful for style mapping but are required only when preparing Wondermint upload. When uploading to Wondermint, use only exact accepted subcategory names from that file.

If the artist does not name a style directly, use an adaptive Style Interview. When the Reference and Artist Meaning do not narrow the next question, use this fallback order:

1. Camera-based, hand-made, graphic/comic, or synthetic/digital?
2. Realistic/representational or stylized/abstracted?
3. Polished/glossy, raw/grainy, painterly/textured, or flat/minimal?
4. Contemporary/everyday, surreal/dreamlike, fantasy/mythic, sci-fi/futuristic, historical, dark/horror, playful/whimsical, or folk/traditional?

## Visual Dynamics

`visual_dynamics.active_visual_tensions` contains the 6 to 8 active visual tensions selected from the Core Visual Tension Pairs library.

Use `visual_dynamics.conditional_visual_tensions` for `Monumental / Intimate` when scale, embodiment, installation, performance, or immersive environments matter.

For text-to-image work, Visual Dynamics describes the Target Visual Engine of the generated image. It must not pretend the text literally has visual properties.

## Prompt Variant Plans

A Provider-Neutral Image Prompt Plan contains exactly three Prompt Variant Plans:

- Faithful,
- Amplified,
- Minimal.

Each Prompt Variant Plan should include:

- variant type,
- variant test axis label, if testing an unresolved dimension,
- variant differentiators,
- prompt text,
- negative constraints,
- derived symbols, if any,
- traceability notes back to the approved Creative Brief,
- critique checklist.

The three Prompt Variant Plans must be visually distinct. Do not create variants that only turn the same image up or down. Each variant should name at least two differentiators, such as composition, subject scale, camera/viewpoint, density, literal/symbolic balance, representation/abstraction, light/color strategy, texture/finish, or focal hierarchy.

Derived Symbols are review-visible inside the full Provider-Neutral Prompt Plan and do not require a separate First Slice approval gate.

`schemas/prompt-plan.schema.json` records the Provider-Neutral Image Prompt Plan. It is provider-neutral by design and must not include provider-specific settings, model names, seeds, cost metadata, or output paths.

`layout_plan` records how the prompt should be arranged before provider translation:

- `single_image`: one generated image from one selected variant.
- `three_panel_variant_triptych`: one generated horizontal image with three equal square panels comparing Minimal, Faithful/modern, and Amplified/maximal directions.
- `style_mosaic_board`: one generated mosaic image comparing candidate styles using the same subject and visual engine. Default to six square tiles in a 2x3 grid, and use no more than three tiles per row unless the artist asks for another layout.
- `series_calibration_image`: one calibration image for an approved Series Plan.
- `series_image`: one image role inside an approved Series Plan.

For `single_image` and `series_calibration` plans, include Faithful, Amplified, and Minimal Prompt Variant Plans. For later approved `series_image` plans, use one prompt variant per Image Role by default unless the artist asks for variants.

## Series Recommendation

`series_recommendation` records whether the Beat Map would be better served by a single image, triptych, or image series.

Required fields:

- `mode`: `single_image`, `triptych`, or `image_series`
- `reason`
- `suggested_images`
- `style_progression`
- `calibration`
- `requires_artist_approval`

If the Reference has multiple significant Beats or Tension Points, include a real recommendation. Do not create multiple image Prompt Plans until the artist approves a Series Plan.

Style Progression can appear inside a Series Recommendation, but it becomes executable only after Series Plan approval.

Use `triptych` for a clear three-part emotional transformation. Use `image_series` for extended sequence, motif evolution, or world exploration.

After Series Plan approval, produce one Series Calibration Image before producing the rest of the series. Use artist feedback on that image to lock Style Direction and Target Visual Engine.

Series Calibration uses three Prompt Variant Plans for the selected Calibration Image Role. After the artist approves one calibration direction, remaining series images use one prompt per Image Role by default.

Minimal series calibration fields:

- `style_progression.proposed`
- `style_progression.progression_summary`
- `style_progression.beat_map_rationale`
- `calibration.required`
- `calibration.calibration_image_role`
- `calibration.uses_three_prompt_variants`

Do not add the full Calibration Choice record until the provider-backed or image-review workflow exists.

## Variant Test Axes

The three Prompt Variant Plans for a single image can test unresolved creative dimensions. Examples:

- realistic/cartoon,
- literal/symbolic,
- sparse/dense,
- restrained/intense,
- polished/raw.

When variants test an unresolved axis, record the axis and how each variant positions itself.

## Provenance Rules

Every meaningful generation choice must trace back to at least one of:

- Artist Meaning,
- Reference evidence,
- Core Tension Pair,
- Active Visual Tension,
- Emotional Quality,
- Beat,
- Tension Point,
- Poetic Density Note,
- Critical Heuristic.

Do not preserve surface form by default. Preserve emotional function and formal role.
