# Metadata Schema

Artist OS uses records to preserve meaning, provenance, and review history as a Reference moves toward generation.

## Record Types

### Project Manifest

A Project Manifest tracks one Artist OS project across sessions. It lives in the local Workspace Library at `workspace-library/artist-os/projects/<project_id>/project.json` and validates against `schemas/project-manifest.schema.json`.

Required sections:

- `project_id`
- `title`
- `status`
- `current_stage`
- `created_at`
- `updated_at`
- `paths`
- `decisions`
- `assets`

The manifest points to the current records and assets. The process history lives in `events.jsonl`.

### Artist OS Library Database

The local SQLite database lives at `workspace-library/artist-os/artist-os.sqlite` and uses `schemas/artist-os-library.sql`.

It is the searchable index for agents returning to earlier sessions. It stores project summaries, current stage, selected decisions, record paths, asset paths, sidecar-derived metadata, and event rows. It should not store binary image data.

Use `bin/artist-os-db sync` after writing project manifests, event logs, or asset sidecars.

When a previously indexed project is not found during sync, the database marks its project row as `missing`. A `missing` project is historical search context, not a resumable project, until its files are restored.

### Asset Metadata

Asset Metadata is the sidecar record stored next to a reference image, visual board, Output Artifact, final image, or export. It validates against `schemas/asset-metadata.schema.json`.

Required fields:

- `asset_id`
- `project_id`
- `asset_type`
- `stage`
- `path`
- `created_at`
- `provenance`
- `rights_notes`
- `status`

The sidecar keeps image files traceable without committing the image itself. It records origin, related Source Record / Brief / Prompt Plan / visual board, provider details when applicable, rights notes, and critique status.

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

### Artist Meaning

Artist Meaning is the artist-authored authority record created by the Meaning Interview. It validates against `schemas/artist-meaning.schema.json`.

Required sections:

- `artist_meaning_id`
- `source_id`
- `version`
- `supersedes_artist_meaning_id`
- `why_it_matters`
- `must_preserve`
- `may_transform`
- `avoid`
- `target_media_type`
- `artist_emotional_language`
- `success_criteria`
- `decision_interview`
- `contradictions_or_overrides`
- `confirmation_status`
- `created_at`

Artist Meaning overrides agent interpretation. Later records should trace meaning-preserving decisions back to this record rather than to the agent's inferred analysis alone.

`decision_interview` persists the early artist participation loop. Each entry stores one question, the agent's recommended answer, the artist's response, the decision area, and whether the recommendation was accepted, revised, rejected, rough-approved, or left unconfirmed.

### Gate Decision

A Gate Decision records one artist-facing choice or explicit permission to proceed unconfirmed. It validates against `schemas/gate-decision.schema.json`.

Required sections:

- `gate_decision_id`
- `project_id`
- `source_id`
- `artist_meaning_id`
- `gate_type`
- `gate_status`
- `decision`
- `options_presented`
- `selected_option`
- `artist_response`
- `proceed_unconfirmed`
- `upstream_refs`
- `created_at`

Use Gate Decision records for Routing, Meaning Confirmation, Interpretation, Story, Story Approval, Medium Gates, Prompt Branch, Prompt Lock, Generation Approval, and Output Acceptance decisions.

### Transformation Brief

A Transformation Brief is the cross-medium interpretation record created after Artist Meaning and before Story / Beat planning. It validates against `schemas/transformation-brief.schema.json`.

Required sections:

- `transformation_brief_id`
- `source_id`
- `artist_meaning_id`
- `artist_meaning`
- `formal_observations`
- `emotional_structure`
- `poetic_density_notes`
- `transformation_constraints`
- `candidate_story_modes`
- `medium_routing_recommendation`
- `traceability_summary`

### Beat Plan

A Beat Plan is the shared story spine consumed by image, video, sound, text, and mixed-media journeys. It validates against `schemas/beat-plan.schema.json`.

Required sections:

- `beat_plan_id`
- `source_id`
- `artist_meaning_id`
- `transformation_brief_id`
- `story_mode`
- `story_gate_status`
- `beats`
- `tension_points`
- `key_emotional_movements`
- `tension_movement_plan`
- `arc_summary`
- `story_critic_review`
- `story_approval`
- `traceability_summary`

Each Beat must do one move, name `intended_feeling` separately from factual content, include `expectation_turn`, and include a `tension_profile`. `expectation_turn` records the expected direction, actual result, surprise function, and emotional counterpoint. `tension_movement_plan.minimum_tension_criteria` defines the project-local contrast threshold reviewers use to decide whether the plan has enough pressure. Multi-beat plans should be reviewed by a bounded Beat Reviewer sub-agent before medium translation.

`key_emotional_movements[]` identifies the major emotional shift points that should survive compression or expansion. Single-image plans usually identify one primary movement; triptychs and longer arcs may identify several.

Beats may optionally include `builds_toward_key_movement_id` when they are supporting Beats that build toward, complicate, or delay a Key Emotional Movement.

### Image Medium Plan

An Image Medium Plan is the typed image translation layer between the shared Beat Plan and the image Creative Brief. It validates against `schemas/image-medium-plan.schema.json`.

Required sections:

- `image_medium_plan_id`
- `source_id`
- `artist_meaning_id`
- `transformation_brief_id`
- `beat_plan_id`
- `target_media_type`
- `story_mode`
- `symbology_direction`
- `presentation_mode`
- `style_direction`
- `visual_dynamics`
- `image_roles`
- `series_plan`
- `gates`
- `review_requirements`
- `traceability_summary`

Each `image_roles[]` entry must state `beat_id`, `key_emotional_movement_id`, `composition_intent`, `communication_intent`, `expectation_turn_translation`, `intended_feeling`, `emotional_payload`, `tension_profile`, and `amplitude_profile`. For triptychs and image series, adjacent roles should also use `distinction_notes` to state composition, communication, and tension shifts. This keeps image planning focused on the feeling each frame creates, not only the object it depicts.

`visual_dynamics.minimum_tension_criteria` defines the minimum visible contrast for the image plan. For single images, it should name the internal contrast requirement. For series, it should name the required adjacent amplitude and tension shifts.

### Sound Medium Plan

A Sound Medium Plan is the typed sound translation layer between the shared Beat Plan and the Sound Creative Brief. It validates against `schemas/sound-medium-plan.schema.json`.

Required sections:

- `sound_medium_plan_id`
- `source_id`
- `artist_meaning_id`
- `transformation_brief_id`
- `beat_plan_id`
- `target_media_type`
- `story_mode`
- `sound_work_type`
- `sonic_concept_direction`
- `genre_direction`
- `tempo_groove_direction`
- `vocal_lyric_policy`
- `arrangement_direction`
- `sonic_dynamics`
- `sequence_plan`
- `gates`
- `review_requirements`
- `traceability_summary`

### Review Record

A Review Record captures one mandatory bounded sub-agent review. It validates against `schemas/review-record.schema.json`.

Required sections:

- `review_record_id`
- `project_id`
- `review_role`
- `reviewer_execution`
- `artifact_under_review`
- `upstream_context`
- `matched`
- `drifted`
- `findings`
- `recommended_revision`
- `approval_status`
- `created_at`

All critic and reviewer records include drift checking. A blocking finding must be revised or explicitly waived by the artist before the journey advances.

`upstream_context` must include the governing `artist_meaning_id` so reviews remain traceable to the Artist Meaning version they evaluated.

### Creative Brief Record

A Creative Brief Record is the structured agent handoff created after Art Critic Review and Brief Approval.

Required sections:

- `brief_id`
- `source_id`
- `artist_meaning_id`
- `transformation_brief_id`
- `beat_plan_id`
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

`beats` remains transitional now that image prompts use the shared Beat Plan. New records should keep `beat_plan_id` authoritative and use embedded `beats` only as medium-local summaries.

### Provider-Neutral Image Prompt Plan

A Provider-Neutral Image Prompt Plan is the structured dry-run generation plan created from an approved Creative Brief Record.

Required sections:

- `prompt_plan_id`
- `brief_id`
- `source_id`
- `artist_meaning_id`
- `transformation_brief_id`
- `beat_plan_id`
- `image_medium_plan_id`
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

Prompt Plans must preserve the lineage IDs from the approved Creative Brief and Image Medium Plan. `traceability_summary` and Prompt Variant trace notes may cite `transformation_brief`, `beat_plan`, and `medium_plan` directly.

### Prompt Branch Set

A Prompt Branch Set is a curator-facing batch of deliberately different prompts derived from one approved Prompt Plan. It validates against `schemas/prompt-branch-set.schema.json`.

Required sections:

- `prompt_branch_set_id`
- `prompt_plan_id`
- `brief_id`
- `source_id`
- `artist_meaning_id`
- `transformation_brief_id`
- `beat_plan_id`
- `medium_plan_id`
- `target_media_type`
- `branching_mode`
- `branch_count_requested`
- `branch_count_actual`
- `meaning_kernel`
- `variation_strategy`
- `branches`
- `curation_plan`
- `review_requirements`
- `traceability_summary`

Each branch must preserve the same meaning kernel while varying approved axes such as style, setting, symbol, composition, viewpoint, palette/light, texture, world, camera distance, or abstraction level. For image batches, five branches is the default curator batch size unless the artist asks for another count.

### Output Record

An Output Record is the metadata and provenance record for an Output Artifact. It validates against `schemas/output-record.schema.json`.

Required sections:

- `output_record_id`
- `project_id`
- `source_id`
- `artist_meaning_id`
- `transformation_brief_id`
- `beat_plan_id`
- `medium_plan_id`
- `brief_id`
- `prompt_plan_id`
- `target_media_type`
- `output_artifact`
- `origin`
- `generation`
- `review_state`
- `acceptance_state`
- `traceability_summary`
- `created_at`

Output Records cover provider-generated media, artist imports, agent-drafted text, and human-edited outputs. When an output comes from a Prompt Branch Set, the record should include both `prompt_branch_set_id` and `prompt_branch_id` as well as the parent `prompt_plan_id`.

### Sound Creative Brief Record

A Sound Creative Brief Record is the structured agent handoff created after Music / Sound Critic Review and Brief Approval. It validates against `schemas/sound-creative-brief.schema.json`.

It mirrors the image Creative Brief Record structure where the concepts are shared:

- `brief_id`
- `source_id`
- `transformation_brief_id`
- `beat_plan_id`
- `artist_meaning`
- `formal_observations`
- `core_tension_pairs`
- `emotional_qualities`
- `poetic_density_notes`
- `beats`
- `transformation_constraints`

It replaces image-specific sections with sound-specific sections:

- `sound_work_type`
- `sonic_concept_direction`
- `genre_direction`
- `tempo_groove_direction`
- `vocal_lyric_policy`
- `lyrics_draft`
- `arrangement_plan`
- `sonic_dynamics`
- `sequence_recommendation`

`sonic_dynamics.active_sonic_tensions` records the active 6 to 8 Sonic Tension Pairs using the same pair-record shape as Visual Dynamics: name, two independent pole presences, tension intensity, evidence, and translation notes.

`arrangement_plan.sections[]` records the section-level tension map. Each section includes section name, time range, bar range, section function, tension role, active emotional tensions, active sonic tensions, and transformation notes.

`beats` remains transitional now that sound prompts use the shared Beat Plan. New records should keep `beat_plan_id` authoritative and use embedded `beats` only as medium-local summaries.

### Suno Sound Prompt Plan

A Suno Sound Prompt Plan is the structured dry-run generation plan created from an approved Sound Creative Brief Record. It validates against `schemas/sound-prompt-plan.schema.json`.

Required sections:

- `prompt_plan_id`
- `brief_id`
- `source_id`
- `artist_meaning_id`
- `transformation_brief_id`
- `beat_plan_id`
- `sound_medium_plan_id`
- `target_media_type`
- `plan_mode`
- `sound_work_type`
- `target_platform`
- `description`
- `style_of_music`
- `sonic_concept_summary`
- `genre_direction_summary`
- `tempo_groove_summary`
- `vocal_lyric_policy`
- `lyrics`
- `arrangement_plan`
- `song_structure`
- `instrumentation_plan`
- `production_direction`
- `sonic_dynamics_summary`
- `prompt_variants`
- `sequence_calibration`
- `suno_custom_mode_outputs`
- `traceability_summary`
- `critique_checklist`

The three sound Prompt Variant Plans keep the same stable labels as image Prompt Variant Plans: Faithful, Amplified, and Minimal. They use `sonic_differentiators` instead of visual differentiators and `derived_sonic_elements` instead of Derived Symbols. Each variant also includes `suno_outputs` so the variant can be pasted into Suno Custom Mode.

For the first text-to-sound version, `suno_custom_mode_outputs` is the final platform-facing contract. It contains `title`, `instrumental`, `lyrics`, `style_of_music`, `exclude`, and optional Suno advanced notes. Later platform adapters can be added after the Suno flow works.

Suno Sound Prompt Plans must preserve the lineage IDs from the approved Sound Creative Brief and Sound Medium Plan. `traceability_summary` and Prompt Variant trace notes may cite `transformation_brief`, `beat_plan`, and `medium_plan` directly.

## Symbology Direction

`symbology_direction` records what the image shows as its core symbolic representation before style is selected.

Required fields:

- `selection_method`: `artist_specified`, `symbology_board`, or `agent_recommended`
- `primary_symbolic_representation`
- `confirmation_status`: `artist_specified`, `confirmed`, or `unconfirmed`
- `alternatives_considered`
- `rationale`
- `avoid`

When unresolved, show six concise symbolic options and ask which one the artist wants. Also ask whether the work should become a single image, an emotional arc, or a multi-image presentation, plus whether they want it visualized. Keep the full board prompt internal unless the artist explicitly asks for an image-generator prompt. Wait for artist selection, combination, rejection, or revision before confirming Symbology Direction.

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

Style Direction is the last priority. It must not override Artist Meaning, Emotional Structure, Beat Plan, or Visual Dynamics. If style conflicts with the Target Visual Engine, record the conflict and proposed style adaptation.

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

For triptych or image-series recommendations, each `series_recommendation.suggested_images[]` entry must include an internal `amplitude_profile` with 0-1 values:

- `framing_distance`: close-up to panoramic
- `subject_scale`: fragile/tiny to monumental/dominant
- `visual_density`: sparse to crowded
- `motion_energy`: still to turbulent
- `spatial_openness`: enclosed to expansive
- `detail_intensity`: minimal to layered
- `emotional_pressure`: quiet to overwhelming

Use amplitude values and each role's `tension_profile` to verify that a series changes visual rhythm and emotional pressure across image roles. Adjacent images should usually differ on at least two amplitude dimensions and one active tension dimension unless continuity is intentional and justified in `rationale`.

## Visual Gates

The default First Slice has three visual gates. Each gate is a **Comparison Board**: a single provider-neutral prompt that renders every option together inside ONE image as a labeled grid (see `THEORY.md` → "Visual Gate Boards"). Never one prompt per option, never multiple images. The `composite_image_prompt` is internal by default; show concise options to the artist unless they explicitly ask for an image-generator prompt.

Stage completion criteria:

- Interpretation is complete when Artist Meaning, must-preserve meaning, and emotional language or emotional arc are captured, or unresolved interpretation questions are marked safe to proceed unconfirmed.
- Visualization/Symbolic is complete when the artist has selected or combined a symbolic representation, chosen single image / emotional arc / multi-image presentation, and accepted, declined, or requested visualization.
- Style is complete when the artist has selected, combined, or named a style, or explicitly allowed an unconfirmed style recommendation to proceed; any offered visualization has been accepted, declined, or requested as a prompt.
- Detail is complete when the artist has selected Minimal, Faithful-Balanced, Amplified-Maximal, a combination, or explicitly skipped the detail choice; any offered visualization has been accepted, declined, or requested as a prompt.

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

Each Prompt Variant Plan must preserve the governing Expectation Turn Translation either in `prompt_text` or in `critique_checklist`, with traceability back to the Beat Plan or Image Medium Plan. This is enforced by Prompt Critic Review rather than a dedicated Prompt Plan field.

Derived Symbols are review-visible inside the full Provider-Neutral Prompt Plan and do not require a separate First Slice approval gate.

`schemas/prompt-plan.schema.json` records the Provider-Neutral Image Prompt Plan. It is provider-neutral by design and must not include provider-specific settings, model names, seeds, cost metadata, or output paths.

`layout_plan` records final output arrangement before provider translation. It does not store pre-locking exploration boards:

- `single_image`: one generated image from one selected variant.
- `three_panel_variant_triptych`: one generated horizontal image with three equal square panels comparing Minimal, Faithful/Balanced, and Amplified/Maximal intensity after symbology and style are selected.
- `series_calibration_image`: one calibration image for an approved Series Plan.
- `series_image`: one image role inside an approved Series Plan.

For `single_image` and `series_calibration` plans, include Faithful, Amplified, and Minimal Prompt Variant Plans. For later approved `series_image` plans, use one prompt variant per Image Role by default unless the artist asks for variants.

## Series Recommendation

`series_recommendation` records whether the Beat Plan would be better served by a single image, triptych, or image series.

Required fields:

- `mode`: `single_image`, `triptych`, or `image_series`
- `reason`
- `suggested_images`, each with `key_emotional_movement_id`, `expectation_turn_translation`, `amplitude_profile`, and a distinct communication role
- `minimum_tension_criteria`
- `style_progression`
- `calibration`
- `requires_artist_approval`

If the Reference has multiple significant Beats or Tension Points, include a real recommendation. Do not create multiple image Prompt Plans until the artist approves a Series Plan.

Style Progression can appear inside a Series Recommendation, but it becomes executable only after Series Plan approval.

Use `triptych` for a clear three-part emotional transformation. Use `image_series` for extended sequence, motif evolution, or world exploration.

Each suggested image should differ from adjacent images in visual composition, communication intent, and tension profile. A series should not repeat the same emotional claim with only surface style or pose changes unless repetition is intentional and artist-approved.

After Series Plan approval, produce one Series Calibration Image before producing the rest of the series. Use artist feedback on that image to lock Style Direction and Target Visual Engine.

Series Calibration uses three Prompt Variant Plans for the selected Calibration Image Role. After the artist approves one calibration direction, remaining series images use one prompt per Image Role by default.

Minimal series calibration fields:

- `style_progression.proposed`
- `style_progression.progression_summary`
- `style_progression.beat_plan_rationale`
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
