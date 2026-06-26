# Metadata Schema

Artist OS uses records to preserve meaning, provenance, and review history as a Reference moves toward generation.

## Record Types

Lineage id fields follow one naming convention. A record that exists for a single medium names the reference after that medium, matching the producing record's primary key: the Image Prompt Plan carries `image_medium_plan_id`, the Sound Prompt Plan carries `sound_medium_plan_id`. A record that can sit downstream of any medium — the Prompt Branch Set and the Output Record — carries the same value generically as `medium_plan_id`. The value is identical either way; only the field name changes with the record's scope. Do not "fix" this asymmetry when emitting records — each schema rejects the other spelling. One deliberate narrowing follows the same spirit: the Release Package Plan's deliverable `medium_plan_id` accepts only `imp`/`smp`/`tmp` (image, sound, text), never `vmp`/`mmp` — video is storyboard-only (v0, no finished deliverable yet) and a mixed-media plan is the package itself, not a deliverable inside it. Widen that pattern when video deliverables ship; until then it is intentional, not a bug.

### Status and approval vocabularies

Status enums intentionally split by role — do not unify them across records. A **verdict** vocabulary records what a reviewer or gate *decides* and uses verbs: `approve` / `revise` / `block` (Review Record `approval_status`; the Beat Plan review verdict). A **state** vocabulary records what a record *is* and uses adjective/past-tense forms: `approved` / `blocked` / `revise` / `waived` (Output Record `review_status`), with `needs_revision` in the Release Package and Asset Metadata. Acceptance and lifecycle are their own sets again (`pending` / `accepted` / `rejected` / `archived` / `exported`; `planned` / `active` / `complete`). Comparing across these as if they were one vocabulary is a mistake: `approve` (the act) and `approved` (the resulting state) are deliberately different tokens.

### Project Manifest

A Project Manifest tracks one Artist OS project across sessions. It lives in the local Workspace Library at `workspace-library/artist-os/projects/<project_id>/project.json` and validates against `schemas/project-manifest.schema.json`.

The manifest points to the current records and assets. The process history lives in `events.jsonl`.

The accepted storage model uses the manifest to track visible Artist Library state: project folder path, Project Pointer state, visible-missing state, feedback review status, and any user-facing files that should be restored or checked for human-edited revisions. Follow `schemas/project-manifest.schema.json` for the current record shape and `docs/storage.md` for the storage contract.

### Artist OS Library Database

The local SQLite database lives at `workspace-library/artist-os/artist-os.sqlite` and uses `schemas/artist-os-library.sql`.

It is the searchable index for agents resuming earlier sessions. Its indexed contents, the `bin/artist-os-db` commands, and the `missing`-project rule are defined in `docs/storage.md` → SQLite Index; do not restate them here.

SQLite indexes Artist Library paths, Project Pointer state, visible-missing state, Feedback Log review status, Learning Index references, and Performance Signal references. The database remains an index; the manifest, event logs, and sidecar records remain the durable source artifacts.

### Asset Metadata

Asset Metadata is the sidecar record stored next to a reference image, visual board, Output Artifact, final image, or export. It validates against `schemas/asset-metadata.schema.json`.

The sidecar keeps image files traceable without committing the image itself. It records origin, related Source Record / Brief / Prompt Plan / visual board, provider details when applicable, rights notes, and critique status.

### Source Record

A Source Record describes the Reference before interpretation. It validates against `schemas/source-record.schema.json`.

### Artist Meaning

Artist Meaning is the artist-authored authority record created by the Meaning Interview. It validates against `schemas/artist-meaning.schema.json`.

Artist Meaning overrides agent interpretation. Later records should trace meaning-preserving decisions back to this record rather than to the agent's inferred analysis alone.

`decision_interview` persists the early artist participation loop. Each entry stores one question, the agent's recommended answer, the artist's response, the decision area, and whether the recommendation was accepted, revised, rejected, rough-approved, or left unconfirmed.

### Gate Decision

A Gate Decision records one artist-facing choice or explicit permission to proceed unconfirmed. It validates against `schemas/gate-decision.schema.json`.

Use Gate Decision records for Routing, Meaning Confirmation, Interpretation, Story, Story Approval, Long-Work Checkpoints, Medium Gates, Prompt Branch, Prompt Lock, Generation Approval, and Output Acceptance decisions.

### Transformation Brief

A Transformation Brief is the cross-medium interpretation record created after Artist Meaning and before Story / Beat planning. It validates against `schemas/transformation-brief.schema.json`.

### Beat Plan

A Beat Plan is the shared story spine consumed by image, video, sound, text, and mixed-media journeys. It validates against `schemas/beat-plan.schema.json`.

Each Beat must do one move, name `intended_feeling` separately from factual content, include `expectation_turn`, and include a `tension_profile`. `expectation_turn` records the expected direction, actual result, surprise function, and emotional counterpoint. `tension_movement_plan.minimum_tension_criteria` defines the project-local contrast threshold reviewers use to decide whether the plan has enough pressure. Multi-beat plans should be reviewed by a bounded Beat Reviewer sub-agent before medium translation.

`key_emotional_movements[]` identifies the major emotional shift points that should survive compression or expansion. Single-image plans usually identify one primary movement; image series and longer arcs may identify several.

Beats may optionally include `builds_toward_key_movement_id` when they are supporting Beats that build toward, complicate, or delay a Key Emotional Movement.

### Long-Work Stewardship Record

A Long-Work Stewardship Record is per-project memory for Cumulative Work: a long written work, image series, song sequence, video sequence, or mixed-media sequence whose parts build on earlier parts. It validates against `schemas/long-work-stewardship-record.schema.json`.

Create this record after Story Approval only when the project contains Cumulative Work. The foundation version may set `medium_plan_id` to `null` and leave `part_plan` empty because medium-specific parts do not exist yet. Enrich it after the Medium Plan maps approved beats into medium-specific parts. It does not replace Artist Meaning, the Beat Plan, or the Medium Plan: the Beat Plan remains the story authority, the Medium Plan owns medium execution details, and stewardship tracks part-to-part integrity, readiness, checkpoints, continuity rules, progress, and drift.

Do not create a Long-Work Stewardship Record only because a project contains many related outputs. Non-sequential portfolios, store collections, style explorations, and curator batches should use lighter collection review behavior unless the parts build on each other.

Long-Work Readiness may be `pending` before the readiness pass runs. After review, use `ready`, `ready_with_risks`, `repair_before_expansion`, or `waived`. `repair_before_expansion` blocks later-part expansion until the issue is repaired or the artist explicitly waives the block through a Gate Decision.

Proposed continuity updates remain inactive until approved. If a proposed update changes Artist Meaning, Story Mode, Beat movement, or the emotional arc, return to Story Approval before making it active continuity.

### Character Template

A Character Template is a lightweight, versioned planning seed. It validates against `schemas/character-template.schema.json`.

Use it when a character needs continuity across text, image, video, or illustrated written work. It may stay `draft` for one-off planning. When downstream generation depends on it, either approve the template or make the Generation Approval explicitly include the provisional character details.

Character Templates do not replace Long-Work Stewardship. In cumulative or full long-form projects, durable character canon belongs in Long-Work `continuity_rules` with `rule_type = "character"`, and discovered changes become `proposed_continuity_updates` until approved.

### Visual Reference Sheet Plan

A Visual Reference Sheet Plan is a provider-neutral prompt package for a reference sheet. It validates against `schemas/visual-reference-sheet-plan.schema.json`.

It supports `character`, `product`, `object`, `setting`, and `style` reference-sheet targets. Drafting the prompt is planning work. Generated reference sheets require explicit Generation Approval and Output Records; imported reference sheets should keep provenance through asset metadata or Output Records when used downstream.

When the story promotes a subject into reference status, `reference_outputs` records the expected images before generation and is required on Visual Reference Sheet Plans. Promoted main characters plan three images: identity plate, full-body turnaround, and macro detail card. Promoted locations plan three angle images: establishing, reverse, and functional/staging. Promoted objects plan one multi-section sheet with multiple angles and details. Character variants can add their own expression, pose/action, wardrobe, or style-variant outputs without changing the base subject package counts.

Reference Inventory is a schema-backed record for project-level reference tracking. It validates against `schemas/reference-inventory.schema.json`. It records effective project reference policy, scan history, character/location/object subjects, recommendation reasons, strategy status, package readiness, expected outputs, missing output roles, active reference versions, Visual Reference Sheet Plan refs, Output Record refs, visible storage paths, provider-neutral role hints, and per-output readiness. It does not replace Visual Reference Sheet Plan or Long-Work Stewardship.

### Image Medium Plan

An Image Medium Plan is the typed image translation layer between the shared Beat Plan and the image Creative Brief. It validates against `schemas/image-medium-plan.schema.json`.

`medium_output_shape_recommendation`, when present, records why the image plan should become `single_image`, `compressed_arc`, or `image_series`. `presentation_mode` remains the accepted concrete image shape consumed downstream. Do not use Story Mode values such as `three_part_sequence` as image output shapes.

Each `image_roles[]` entry must state `beat_id`, `key_emotional_movement_id`, `composition_intent`, `communication_intent`, `expectation_turn_translation`, `intended_feeling`, `emotional_payload`, `tension_profile`, `shot_design`, and `amplitude_profile`. For image series, adjacent roles should also use `distinction_notes` to state composition, communication, shot-design, and tension shifts. This keeps image planning focused on the feeling each frame creates, not only the object it depicts.

`shot_design` names the frame's camera grammar:

- `shot_scale`: `extreme_close_up`, `close_up`, `medium_close_up`, `medium_shot`, `medium_wide`, `wide`, or `extreme_wide`
- `camera_angle`: `eye_level`, `high_angle`, `low_angle`, `overhead`, `dutch_angle`, `profile`, `over_the_shoulder`, or `point_of_view`
- `visual_emphasis`: `face_reaction`, `hands_or_object`, `body_action`, `relationship`, `environment`, `absence_negative_space`, `symbolic_detail`, or `scale_consequence`
- `composition_strategy`
- `emotional_rationale`
- `avoid`

Do not let `shot_design` default to full-body character framing. Close shots should be used when emotion, reaction, or symbolic detail carries the Beat. Medium shots should be used when body language, action, and context all matter. Wide shots should be used when environment, absence, isolation, threshold, or consequence carries the feeling.

`visual_dynamics.minimum_tension_criteria` defines the minimum visible contrast for the image plan. For single images, it should name the internal contrast requirement. For series, it should name the required adjacent amplitude and tension shifts.

### Video Medium Plan

A Video Medium Plan is the typed video translation layer between the shared Beat Plan and the Video Creative Brief. It validates against `schemas/video-medium-plan.schema.json`.

The v0 implementation is storyboard-ready planning only. It owns Narrative Depth, selected Story or Micro-Journey Template refs when present, Asset Purpose Brief for utility sequences, Video Format, Video Style Expression, Visual Dynamics over time, Video Sequences when needed, Video Scenes, Storyboard Shots, audio posture, text/audio refs, storyboard frame prompts, and storyboard generation policy. The default generated storyboard artifact is one composite multi-panel storyboard sheet. It does not create a Video Prompt Plan or finished video.

Video Medium Plans use the same Symbology Direction and Style Direction concepts as Image Medium Plans. Video adds medium-specific choices for rendering mode, camera style, motion style, edit style, scene/sequence structure, shot logic, motion/pacing/transition logic, and audio posture.

Generated or imported composite storyboard sheets require explicit provider-backed generation approval and normal Output Records linked back to the Video Medium Plan. Individual storyboard stills are a separate artifact type: they require explicit provider-backed generation approval that names individual stills or separate panel images, and normal Output Records linked back to the relevant Storyboard Shot. Finished video generation, render adapters, and provider-specific video jobs are downstream adapters.

### Sound Medium Plan

A Sound Medium Plan is the typed sound translation layer between the shared Beat Plan and the Sound Creative Brief. It validates against `schemas/sound-medium-plan.schema.json`.

### Text Medium Plan

A Text Medium Plan is the typed writing translation layer between the shared Beat Plan and the Text Creative Brief. It validates against `schemas/text-medium-plan.schema.json`.

Each `structure_plan.sections[]` entry must name the governing Beat, Key Emotional Movement, structure role, section job, Intended Feeling, Expectation Turn translation, source-wording notes, and paragraph distinction. Text planning must make every section or paragraph group do a different job instead of producing a smooth summary of the source.

`length_policy` records the accepted Format Length Standard: standard source, target word count, minimum, maximum, flexibility, rationale, and any artist override. Text Medium Plan owns the length decision because length changes the medium structure before drafting.

### Illustration Plan

An Illustration Plan is the cross-medium coordinator for illustrated written work. It validates against `schemas/illustration-plan.schema.json`.

Create it after a Text Medium Plan exists, because page, spread, panel, diagram, and cover decisions need the accepted text form, structure, length/page shape, audience, and publication/use. The Illustration Plan maps Text Medium Plan sections and Beat Plan movements to still-image jobs, visual continuity rules, text-image relationships, Character Templates, Visual Reference Sheet Plans, and downstream Image Prompt Plan refs.

Illustration Plan is not a Video Medium Plan. It has no Video Audio Posture, timed Storyboard Shots, camera-motion contract, or finished-video promise.

### Review Record

A Review Record captures one mandatory bounded sub-agent review. It validates against `schemas/review-record.schema.json`.

Fallback separated review records are allowed only when the host or active tool policy blocks sub-agent spawning despite Standing Sub-Agent Authorization. They must set `reviewer_execution.fallback_reason` to `host_cannot_spawn_sub_agent` or `tool_policy_blocks_sub_agent_spawn`.

All critic and reviewer records include drift checking. A blocking finding must be revised or explicitly waived by the artist before the journey advances.

`upstream_context` must include the governing `artist_meaning_id` so reviews remain traceable to the Artist Meaning version they evaluated.

`emotional_tension_review` must state the Intended Feeling reviewed, Minimum Tension Criteria checked, numeric `tension_intensity_assessments`, Key Emotional Movements reviewed, Expectation Turns reviewed, any missing context, and the reviewer conclusion. Each intensity assessment records the source, tension name, claimed intensity, reviewer-assessed intensity, minimum required intensity, `meets_minimum`, and an assessment note. Reviewers should not copy the claimed number silently; they independently judge whether the artifact earns that intensity. Do not hide this assessment only in `findings`; downstream gates need a stable field to verify that emotional primacy was reviewed.

Use `review_role = "long_work_reviewer"` for Long-Work Stewardship readiness, checkpoint, drift, and proposed-continuity reviews.

### Creative Brief Record

A Creative Brief Record is the structured agent handoff created after Art Critic Review and Brief Approval. It validates against `schemas/creative-brief.schema.json`.

Creative Brief Records do not embed Beat summaries. Use `beat_plan_id` to read the authoritative Beat Plan.

### Provider-Neutral Image Prompt Plan

A Provider-Neutral Image Prompt Plan is the structured dry-run generation plan created from an approved Creative Brief Record. It validates against `schemas/prompt-plan.schema.json`.

Prompt Plans must preserve the lineage IDs from the approved Creative Brief and Image Medium Plan. `traceability_summary` and Prompt Variant trace notes may cite `transformation_brief`, `beat_plan`, and `medium_plan` directly.

When the artist asks for a specific image generator, store that generator in optional `provider_targets[]` rather than changing the canonical `prompt_variants[]`. For Midjourney, set `provider_prompt_style = "suffix_parameters"`, fill structured parameters such as `aspect_ratio`, `stylize`, `chaos`, `quality`, `raw`, `seed_policy`, and `negative_prompt`, then render both `rendered_suffix` and per-variant `rendered_prompts[].full_prompt`. For API or workflow tools such as OpenAI image generation, Leonardo, Stable Diffusion WebUI, or ComfyUI, use the same block only as a provider translation target with `api_fields`, `structured_settings`, or `workflow_settings`; do not invent Midjourney-style `--` suffixes for tools that do not use them.

### Prompt Branch Set

A Prompt Branch Set is a curator-facing batch of deliberately different prompts derived from one approved Prompt Plan. It validates against `schemas/prompt-branch-set.schema.json`.

The build procedure, default branch count, meaning-kernel rules, and the `emotional_tension_preservation` anti-drift check are defined in `docs/prompt-branch-set.md`; do not restate them here.

### Output Record

An Output Record is the metadata and provenance record for an Output Artifact. It validates against `schemas/output-record.schema.json`.

Output Records cover provider-generated media, artist imports, agent-drafted text, agent-rewritten text, and human-edited outputs. When an output comes from a Prompt Branch Set, the record should include both `prompt_branch_set_id` and `prompt_branch_id` as well as the parent `prompt_plan_id`. Text Journey outputs should set `text_generation_plan_id` to the governing Text Generation Plan while keeping `prompt_plan_id` populated for the current shared Output Record contract.

For Text Journey drafts, persist the compact draft trace in `traceability_summary`: section or block, source Beat or structure role, Intended Feeling, and key constraint preserved. Text outputs may cite `text_generation_plan` directly in trace notes even while `prompt_plan_id` remains populated for the current shared contract. The Text Draft Packet is an internal sub-agent handoff, not a separate schema-backed record.

For Text Journey rewrite Output Records, set `previous_output_record_id`, preserve the original draft trace, and add compact rewrite trace notes: pass used, policy authorization, prior Output Record, changed pattern or clarity issue, and protected features preserved.

By contract, any Output Record with `origin.origin_type = "agent_rewritten"` must set `previous_output_record_id`. Text Journey transition tests enforce this for rewrite fixtures; add schema-level conditional enforcement only when the local schema validator supports conditionals.

Human-edited visible files in the Artist Library should become new Output Records with `origin.origin_type = "human_edited"` and `previous_output_record_id` pointing to the prior artifact when known. This preserves the artist's edit as an authoritative revision without mutating the earlier Output Record.

### Feedback, Learning, and Performance Records

Project Feedback Log entries validate against `schemas/project-feedback-log-entry.schema.json`. Learning Candidate, Soft Learning, and Hard Learning records validate against `schemas/learning-record.schema.json`. Performance Signals validate against `schemas/performance-signal.schema.json`.

Raw feedback stays in project logs until Learning Review classifies it. Reusable Learning Rules stay compact and evidence-backed; `learning_rule` is capped at 600 characters. Performance Signals have equal evidence weight with artist feedback without automatically overriding it.

### Sound Creative Brief Record

A Sound Creative Brief Record is the structured agent handoff created after Music / Sound Critic Review and Brief Approval. It validates against `schemas/sound-creative-brief.schema.json`.

It parallels the image Creative Brief Record, keeping the shared meaning-level sections and swapping the image-specific block for sound-specific sections (sonic concept, genre, tempo/groove, vocal/lyric, lyrics, arrangement, sonic dynamics, sequence). See the schema for exact fields.

Sound Medium Plan records may include `medium_output_shape_recommendation` to explain the choice among sound-specific shapes such as `song`, `instrumental_track`, `ambient_soundscape`, `cinematic_score`, `spoken_word_bed`, `ritual_audio`, `sound_design_piece`, `sonic_logo`, or `sound_sequence`. For single sound works, `accepted_shape` must match `sound_work_type`. For `sound_sequence`, `sequence_plan.is_sequence` must be true. Arrangement sections, song structure, and section tension maps remain owned by arrangement and prompt planning, not by output-shape recommendation.

`sonic_dynamics.active_sonic_tensions` records the active 6 to 8 Sonic Tension Pairs using the same pair-record shape as Visual Dynamics: name, two independent pole presences, tension intensity, evidence, and translation notes.

`arrangement_plan.sections[]` records the section-level tension map. Each section includes section name, time range, bar range, section function, tension role, active emotional tensions, active sonic tensions, and transformation notes.

Sound Creative Brief Records do not embed Beat summaries. Use `beat_plan_id` to read the authoritative Beat Plan.

### Text Creative Brief Record

A Text Creative Brief Record is the structured agent handoff created after Writing Critic Review and Brief Approval. It validates against `schemas/text-creative-brief.schema.json`.

Text Creative Brief Records do not embed Beat records. Use `beat_plan_id` to read the authoritative Beat Plan and `text_medium_plan_id` to read the authoritative writing structure.

### Sound Prompt Plan

A Sound Prompt Plan is the structured dry-run generation plan created from an approved Sound Creative Brief Record. It validates against `schemas/sound-prompt-plan.schema.json`.

`emotional_tension_contract` records the governing Intended Feeling, Key Emotional Movement ids, Minimum Tension Criteria, and Expectation Turn preservation that the Sound Prompt Plan must carry from the Beat Plan and Sound Medium Plan. Each `song_structure.sections[]` entry must name its `beat_id`, `key_emotional_movement_id`, `expectation_turn_translation`, `intended_feeling`, and `tension_profile` so the arrangement does not become a genre-only plan.

The three sound Prompt Variant Plans keep the same stable labels as image Prompt Variant Plans: Faithful, Amplified, and Minimal. They use `sonic_differentiators` instead of visual differentiators and `derived_sonic_elements` instead of Derived Symbols. Each variant also includes `emotional_tension_preservation` and `platform_output_intent` so the variant can be reviewed against the approved emotional/tension contract before any provider-specific rendering.

`platform_renderings[]` is the final platform-facing contract. For the first text-to-sound version, a Suno rendering stores `outputs.suno_custom_mode_outputs` with `title`, `instrumental`, `lyrics`, `style_of_music`, `exclude`, and optional Suno advanced notes. Later platform renderers add sibling entries without changing upstream sound planning.

Sound Prompt Plans must preserve the lineage IDs from the approved Sound Creative Brief and Sound Medium Plan. `traceability_summary`, Prompt Variant trace notes, and platform rendering trace notes may cite `transformation_brief`, `beat_plan`, and `medium_plan` directly.

### Text Generation Plan

A Text Generation Plan is the structured post-brief plan for drafting or generating a written Output Artifact. It validates against `schemas/text-generation-plan.schema.json`.

The Text Generation Plan owns the final draft instructions and editorial pass policies. It must require fresh-context drafting, forbid Human Voice Pass during first drafting, require a returned draft trace, carry the accepted length policy into drafting instructions, record the review presentation decision, and specify Output Record requirements for draft and rewrite artifacts. Its traceability notes may cite the approved Text Creative Brief as `text_creative_brief`.

## Symbology Direction

`symbology_direction` records what the image shows as its core symbolic representation before style is selected.

Required fields:

- `selection_method`: `artist_specified`, `symbology_board`, or `agent_recommended`
- `primary_symbolic_representation`
- `confirmation_status`: `artist_specified`, `confirmed`, or `unconfirmed`
- `alternatives_considered`
- `rationale`
- `avoid`

When unresolved, show six concise symbolic options and ask which one the artist wants. Also ask whether the work should become a single image, a compressed arc, or an image series, plus whether they want it visualized. Keep the full board prompt internal unless the artist explicitly asks for an image-generator prompt. Wait for artist selection, combination, rejection, or revision before confirming Symbology Direction.

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

For image-series recommendations, each `series_recommendation.suggested_images[]` entry must include an internal `amplitude_profile` with 0-1 values:

- `framing_distance`: close-up to panoramic
- `subject_scale`: fragile/tiny to monumental/dominant
- `visual_density`: sparse to crowded
- `motion_energy`: still to turbulent
- `spatial_openness`: enclosed to expansive
- `detail_intensity`: minimal to layered
- `emotional_pressure`: quiet to overwhelming

Use amplitude values, each role's `tension_profile`, and each role's `shot_design` to verify that a series changes visual rhythm and emotional pressure across image roles. Adjacent images should usually differ on at least two amplitude dimensions, one active tension dimension, and one Shot Design axis unless continuity is intentional and justified in `rationale`.

## Visual Gates

The default First Slice has two shared visual gates. Each gate can use a **Comparison Board**: a single provider-neutral prompt that renders every option together inside ONE image as a labeled grid (see `THEORY.md` → "Visual Gate Boards"). Never one prompt per option, never multiple images. The `composite_image_prompt` is internal by default; show concise options to the artist unless they explicitly ask for an image-generator prompt.

Stage completion criteria:

- Interpretation is complete when Artist Meaning, must-preserve meaning, and emotional language or emotional arc are captured, or unresolved interpretation questions are marked safe to proceed unconfirmed.
- Visualization/Symbolic is complete when the artist has selected or combined a symbolic representation, chosen single image / compressed arc / image series, and accepted, declined, or requested visualization.
- Style is complete when the artist has selected, combined, or named a style, or explicitly allowed an unconfirmed style recommendation to proceed; any offered visualization has been accepted, declined, or requested as a prompt.

1. Symbology Board: one image, 2x3 grid of six cells, each cell plain black-and-white line art of the subject only (no style) comparing symbolic representations, before style is locked.
2. Style Exploration Board: one image, 2x3 grid of six tiles, each tile the same locked symbology subject in a different style, shown only after asking whether the artist wants to see style options.

Exploration boards are stored in `visual_boards`, not `layout_plan`. Optional single-generation variant comparisons are final-output layouts, stored as `layout_plan` with `layout_type: three_panel_variant_comparison` and their own `composite_image_prompt`. Each board or comparison may be drafted as provider-neutral text or generated only after explicit, per-board artist approval for provider-backed generation.

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

The three Prompt Variant Plans must be visually distinct according to the Prompt Variant Strategy. Do not create variants that only change adjectives. Each variant should name at least two differentiators, such as composition, subject scale, camera/viewpoint, density, symbolic layering, representation/abstraction, light/color strategy, texture/finish, negative space, ornament, scale, drama, or focal hierarchy. Each Prompt Variant Plan should preserve the selected Symbology Direction and Style Direction unless the artist explicitly asks to revisit an earlier gate.

Each Prompt Variant Plan must preserve the governing Expectation Turn Translation either in `prompt_text` or in `critique_checklist`, with traceability back to the Beat Plan or Image Medium Plan. This is enforced by Prompt Critic Review rather than a dedicated Prompt Plan field.

Derived Symbols are review-visible inside the full Provider-Neutral Prompt Plan and do not require a separate First Slice approval gate.

`schemas/prompt-plan.schema.json` records the Provider-Neutral Image Prompt Plan. It is provider-neutral by design: `prompt_variants[]` must not include provider-specific settings, model names, seeds, cost metadata, or output paths. Optional `provider_targets[]` may carry provider-specific translations, suffixes, or API/workflow settings when the artist requested a provider-specific prompt output. Provider targets do not authorize provider-backed generation.

`layout_plan` records final output arrangement before provider translation. It does not store pre-locking exploration boards:

- `single_image`: one generated image from one selected variant.
- `three_panel_variant_comparison`: one generated horizontal image with equal panels comparing multiple Prompt Variant Plans after symbology and style are selected.
- `series_calibration_image`: one calibration image for an approved Series Plan.
- `series_image`: one image role inside an approved Series Plan.

For `plan_mode = "single_image"` and `plan_mode = "series_calibration"` records, include Faithful, Amplified, and Minimal Prompt Variant Plans. Their layout types are usually `single_image` or `series_calibration_image`. For later approved `plan_mode = "series_image"` records, use one prompt variant per Image Role by default unless the artist asks for variants.

## Series Recommendation

`series_recommendation` records whether the Beat Plan would be better served by a single image or image series. A three-image sequence is an image series with three suggested images.

Required fields:

- `mode`: `single_image` or `image_series`
- `reason`
- `suggested_images`, each with `key_emotional_movement_id`, `expectation_turn_translation`, `shot_design`, `amplitude_profile`, and a distinct communication role
- `minimum_tension_criteria`
- `style_progression`
- `calibration`
- `requires_artist_approval`

If the Reference has multiple significant Beats or Tension Points, include a real recommendation. Do not create multiple image Prompt Plans until the artist approves a Series Plan.

Style Progression can appear inside a Series Recommendation, but it becomes executable only after Series Plan approval.

Use `image_series` for any multi-image output, including a clear three-part emotional transformation, extended sequence, motif evolution, or world exploration.

Each suggested image should differ from adjacent images in Shot Design, visual composition, communication intent, and tension profile. A series should not repeat the same emotional claim with only surface style, pose changes, or repeated full-body framing unless repetition is intentional and artist-approved.

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
