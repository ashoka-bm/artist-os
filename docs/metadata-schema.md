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
- `symbology_direction`
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
- `visual_boards`
- `symbology_direction_summary`
- `style_direction_summary`
- `target_visual_engine_summary`
- `layout_plan`
- `prompt_variants`
- `series_calibration`
- `traceability_summary`
- `critique_checklist`

## Symbology Direction

`symbology_direction` records what the image shows as its core symbolic representation before style is selected.

Required fields:

- `selection_method`: `artist_specified`, `symbology_board`, or `agent_recommended`
- `primary_symbolic_representation`
- `confirmation_status`: `artist_specified`, `confirmed`, or `unconfirmed`
- `alternatives_considered`
- `rationale`
- `avoid`

When unresolved, show six concise symbolic options and ask which one the artist wants, plus whether they want it visualized. Keep the full board prompt internal unless the artist explicitly asks for an image-generator prompt. Wait for artist selection, combination, rejection, or revision before confirming Symbology Direction.

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

If the artist does not name a specific style directly, ask whether they already have a specific visual vision or want to explore what art style to use. If they want exploration, ask for a rough direction and use an adaptive Style Interview only as far as needed to create a useful Style Exploration Board. When the Reference, Artist Meaning, and rough direction do not narrow the next question, use this fallback order:

1. Camera-based, hand-made, graphic/comic, or synthetic/digital?
2. Realistic/representational or stylized/abstracted?
3. Polished/glossy, raw/grainy, painterly/textured, or flat/minimal?
4. Contemporary/everyday, surreal/dreamlike, fantasy/mythic, sci-fi/futuristic, historical, dark/horror, playful/whimsical, or folk/traditional?

When Style Direction is unresolved, ask whether the artist wants to see style options before moving forward. If yes, show six concise suggested styles, ask whether the artist wants some of them or has something else in mind, and ask whether they want the styles visualized. Keep the board prompt internal unless the artist explicitly asks for an image-generator prompt.

## Visual Dynamics

`visual_dynamics.active_visual_tensions` contains the 6 to 8 active visual tensions selected from the Core Visual Tension Pairs library.

Use `visual_dynamics.conditional_visual_tensions` for `Monumental / Intimate` when scale, embodiment, installation, performance, or immersive environments matter.

For text-to-image work, Visual Dynamics describes the Target Visual Engine of the generated image. It must not pretend the text literally has visual properties.

## Visual Gates

The default First Slice has three visual gates. Each gate is a **Comparison Board**: a single provider-neutral prompt that renders every option together inside ONE image as a labeled grid (see `THEORY.md` → "Visual Gate Boards"). Never one prompt per option, never multiple images. The `composite_image_prompt` is internal by default; show concise options to the artist unless they explicitly ask for an image-generator prompt.

1. Symbology Board: one image, 2x3 grid of six cells, each cell plain black-and-white line art of the subject only (no style) comparing symbolic representations, before style is locked.
2. Style Exploration Board: one image, 2x3 grid of six tiles, each tile the same locked symbology subject in a different style, shown only after asking whether the artist wants to see style options.
3. Minimalist-to-Maximalist Gate: one image, three side-by-side panels comparing Minimal, Faithful/Balanced, and Amplified/Maximal intensity, after symbology and style are selected.

Exploration boards are stored in `visual_boards`, not `layout_plan`. The Minimalist-to-Maximalist Gate is a final-output layout, stored as `layout_plan` with `layout_type: three_panel_variant_triptych` and its own `composite_image_prompt`. Each board may be drafted as provider-neutral text or generated only after explicit, per-board artist approval for provider-backed generation.

`visual_boards[]` records pre-locking exploration artifacts:

- `board_type`: `symbology_board` or `style_mosaic_board`
- `status`: `proposed`, `drafted`, `generated`, `selected`, or `skipped`
- `panel_count`: 3 to 6
- `layout`: the grid, e.g. `2x3` (max three cells per row)
- `composite_image_prompt`: the single prompt that renders the whole grid as one image — the board's primary deliverable
- `requires_generation_approval`
- `selected_option_label`
- `options[]`

Each `options[]` entry includes label, `visual_prompt` (the content of that one cell, composed into `composite_image_prompt` — not a standalone image), decision focus, traceability notes, and risks. A board should use six options unless the artist asks otherwise. User-facing gate output should show option labels or one-line descriptions, not the full prompt.

## Prompt Variant Plans

Before Style Direction is locked, use a Symbology Board when multiple symbolic or compositional strategies remain plausible. The board contains six drafted or generated visual representations for the same Artist Meaning, Creative Brief, and Target Visual Engine unless the artist asks for fewer. It must be one line-drawing comparison image so the artist compares symbolic representation before art style. Wait for the artist to select, combine, reject, or revise options before confirming Symbology Direction. Each branch should include:

- branch label,
- symbolic or compositional strategy,
- what the artist can react to,
- traceability note,
- known risk or tradeoff.

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

The three Prompt Variant Plans must be visually distinct along the Minimalist-to-Maximalist axis. Do not create variants that only change adjectives. Each variant should name at least two differentiators, such as composition, subject scale, camera/viewpoint, density, symbolic layering, representation/abstraction, light/color strategy, texture/finish, negative space, ornament, scale, drama, or focal hierarchy. Each Prompt Variant Plan should preserve the selected Symbology Direction and Style Direction unless the artist explicitly asks to revisit an earlier gate.

Derived Symbols are review-visible inside the full Provider-Neutral Prompt Plan and do not require a separate First Slice approval gate.

`schemas/prompt-plan.schema.json` records the Provider-Neutral Image Prompt Plan. It is provider-neutral by design and must not include provider-specific settings, model names, seeds, cost metadata, or output paths.

`layout_plan` records final output arrangement before provider translation. It does not store pre-locking exploration boards:

- `single_image`: one generated image from one selected variant.
- `three_panel_variant_triptych`: one generated horizontal image with three equal square panels comparing Minimal, Faithful/Balanced, and Amplified/Maximal intensity after symbology and style are selected.
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
