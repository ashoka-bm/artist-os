# Artist OS Progress

This document records what has been created, what is transitional, and what comes next. Keep it current when changing architecture, schemas, skills, or tests.

## Current Goal

Artist OS has established the core typed transformation pipeline for the current image, Suno, and text dry-run slices. The current refinement pass adds an emotional-primacy contract on top of that pipeline: records must now name the intended feeling, preserve the artist's authority through a Decision Interview, and carry enough tension movement for reviewers to judge whether the work expresses a feeling rather than only describing a fact.

Current implementation priority is dry-run output quality: generate the right briefs, plans, prompts, drafts, reviews, and records at the highest possible quality before adding external generation. API setup, provider credentials, provider adapters, and actual external image or Suno generation are intentionally deferred until the dry-run contracts and output quality are strong enough to support them.

```text
Step Input Record
  -> Agent / Skill Transformation
  -> Step Output Record
  -> Schema Validation
  -> Mandatory Reviewer Sub-Agent, when required
  -> Next Step Input Record
```

Every creation step should eventually have:

- one declared input record,
- one declared output record,
- one schema for the output,
- validation tests,
- clear next allowed steps,
- mandatory bounded sub-agent review when the gate requires review.

Every image, series, or arc-shaped plan should also preserve:

- the Intended Feeling it is trying to create,
- the Key Emotional Movements that survive compression or expansion,
- beat-level Expectation Turns,
- project-local Minimum Tension Criteria,
- medium-specific tension profiles and role distinctions,
- explicit artist decisions captured through `decision_interview`.

## Completed

### Current Dry-Run Slices

Implemented dry-run workflows:

- Text Reference to Provider-Neutral Image Prompt Plan.
- Text Reference to Suno Sound Prompt Plan.
- Text Reference to Text Generation Plan and drafted written Output Records (Text Journey).

Provider-backed generation remains out of scope without explicit approval.

### Shared Story Architecture

Added:

- `docs/story/THEORY.md`
- `docs/story/ARCHITECTURE.md`
- `docs/output-journeys/`

Story is now the shared layer: every output is one or more approved beats translated into a medium.

The Story Structure Library now includes the original core entries plus six additional researched craft frameworks: `save_the_cat_beat_sheet`, `dan_harmon_story_circle`, `seven_point_structure`, `fichtean_curve`, `in_medias_res_revelation`, and `frame_story_nested_return`.

Focused Story Structure rehearsals for those six new entries passed without schema changes. The main shared finding was that Story Structure craft labels must be mapped into schema-valid Beat Plan `beat_role` values rather than copied literally; `fichtean_curve` also needs quiet crisis pressure to remain valid, and `frame_story_nested_return` needs object/archive testimony to change the return frame before it counts as nested material.

Promoted representative fixtures for `save_the_cat_beat_sheet` and `fichtean_curve` to cover granular commercial beat mapping and quiet crisis pressure without adding six redundant Beat Plan fixtures.

A cross-medium rehearsal using the shared `fichtean_curve` Beat Plan found that Text, Image, and Sound can all preserve the same Story Structure while recommending compact medium shapes: short written work, compressed visual arc, and single multi-section sound work. Length and expansion gates should therefore consider dependency, accepted expansion, continuity, and medium-specific part planning rather than triggering from beat count or `story_mode = "arc"` alone.

Added Workflow Scale Routing as the internal scale decision layer. Beat Plans now carry Project-Level Workflow Scale Routing, and Text, Image, and Sound Medium Plans carry Medium-Level Workflow Scale Routing. The field records `scale_level`, rationale, trigger signals, activated supports, skipped supports, and reroute triggers so agents can choose the right support bundle without overusing Long-Work Stewardship for compact artifacts.

Workflow Scale Routing is schema-backed and required on:

- `schemas/beat-plan.schema.json`
- `schemas/text-medium-plan.schema.json`
- `schemas/image-medium-plan.schema.json`
- `schemas/sound-medium-plan.schema.json`

The initial Workflow Scale Levels are `compact_artifact`, `structured_single_artifact`, `cumulative_work`, and `full_long_form_project`. The governing placement decision is recorded in `docs/adr/0007-workflow-scale-routing-placement.md`.

### Gates And Reviews

Added:

- `docs/gates-and-reviews.md`

This is the canonical contract for:

- shared gate order,
- canonical gate definitions,
- critic roles,
- writing method reviewers,
- mandatory bounded sub-agent review execution,
- review packet and output format,
- drift checking,
- blocking findings and artist waivers.

All critics and reviewers must check for drift against governing upstream material.

### Writing Method Integration

Vendored high-authority writing method references:

- `docs/writing/references/writing-fragments.SKILL.md`
- `docs/writing/references/writing-beats.SKILL.md`
- `docs/writing/references/writing-shape.SKILL.md`

Bundled the same references inside:

- `skills/writing-method-review/references/`

Added:

- `docs/writing/README.md`
- `skills/writing-method-review/SKILL.md`

The installer now copies bundled references for copied skill installs.

### Shared Schemas

Added:

- `schemas/transformation-brief.schema.json`
- `schemas/beat-plan.schema.json`
- `schemas/review-record.schema.json`

Added examples:

- `examples/source-record.example.json`
- `examples/transformation-brief.example.json`
- `examples/beat-plan.example.json`
- `examples/review-record.example.json`

Updated docs and storage to recognize:

- `story/transformation-brief.json`
- `story/beat-plan.json`
- review records under `critiques/`

### Image And Suno Beat Plan Migration

Updated:

- `schemas/creative-brief.schema.json`
- `schemas/sound-creative-brief.schema.json`

Both now require:

- `transformation_brief_id`
- `beat_plan_id`

Updated examples:

- `examples/text-creative-brief.example.json`
- `examples/text-sound-creative-brief.example.json`
- `examples/project-manifest.example.json`

Updated skills:

- `skills/artist-os/SKILL.md`
- `skills/text-to-image-plan/SKILL.md`
- `skills/text-to-suno-plan/SKILL.md`

Image and Suno flows now sequence:

```text
Source Record
  -> Artist Meaning
  -> Transformation Brief
  -> Beat Plan
  -> Beat Reviewer sub-agent when required
  -> Medium Plan
  -> medium-specific brief
```

### Emotional Primacy And Tension Contracts

Added domain language for:

- Emotional Primacy,
- Intended Feeling,
- Minimum Tension Criteria,
- Active Absence,
- Decision Interview and Recommended Answer,
- Emotional Movement,
- Arc Scale,
- Key Emotional Movement,
- Substantial Beat Difference,
- Expectation Turn,
- Expectation Turn Translation,
- Active Absence Symbology.

Updated the core planning docs and skills so the governing rule is clear:

- creation of the intended emotion is primary,
- Beat Plans and Medium Plans support that emotion,
- symbolic representation cannot be skipped silently,
- absence can create tension when it is deliberate,
- long arcs may build one emotion across several beats, but every beat still needs an unexpected turn,
- short arcs and image series need faster, more visible movement between beats or image roles.

Updated schemas so this rule is durable:

- `schemas/artist-meaning.schema.json` requires `decision_interview`,
- `schemas/beat-plan.schema.json` requires `key_emotional_movements`, `tension_movement_plan`, beat `expectation_turn`, beat `intended_feeling`, and beat `tension_profile`,
- `schemas/image-medium-plan.schema.json` requires `visual_dynamics.minimum_tension_criteria`; image roles now carry `key_emotional_movement_id`, `communication_intent`, `expectation_turn_translation`, `intended_feeling`, and `tension_profile`,
- `schemas/creative-brief.schema.json` requires the image-series recommendation to carry role-level emotional movement, tension, expectation-turn translation, and series distinction fields.
- `schemas/sound-prompt-plan.schema.json` requires `emotional_tension_contract`, section-level Beat and Key Emotional Movement mapping, section-level Expectation Turn Translation, and variant-level emotional/tension preservation,
- `schemas/prompt-branch-set.schema.json` requires the meaning kernel and every branch to preserve Intended Feeling, Key Emotional Movement, Expectation Turn Translation, and Minimum Tension Criteria,
- `schemas/review-record.schema.json` requires `emotional_tension_review` with numeric tension intensity assessments, so every critic packet explicitly reviews Intended Feeling, Minimum Tension Criteria, claimed vs reviewer-assessed intensity, Key Emotional Movements, and Expectation Turns.

Updated examples and fixtures for Artist Meaning, Beat Plans, Image Medium Plans, Creative Brief Records, Suno Sound Prompt Plans, Prompt Branch Sets, and Review Records to validate against the hardened contracts.

### Embedded Beat Summary Cleanup

Removed transitional embedded `beats` from:

- `schemas/creative-brief.schema.json`,
- `schemas/sound-creative-brief.schema.json`,
- matching examples and fixtures.

Current rule:

- `beat_plan_id` is authoritative.
- medium-specific brief records do not duplicate Beat summaries.

## Transitional Decisions

### Review Records

`review-record.schema.json` exists, and active reviewer skills now require Review Record JSON as the first machine-readable output.

Added record mode to:

- `skills/art-critic-review/SKILL.md`
- `skills/critique-asset/SKILL.md`
- `skills/writing-method-review/SKILL.md`

Current rule:

- every reviewer runs as a bounded sub-agent,
- every reviewer checks drift,
- every reviewer emits a Review Record matching `schemas/review-record.schema.json`,
- companion prose or revised artifacts may follow the Review Record but do not replace it.

### Validation And Tests

Added:

- `bin/validate-examples`
- `artist_os_schema_validator.py`
- `tests/test_schema_validation.py`
- `tests/test_pipeline_transitions.py`
- `tests/fixtures/`
- `tests/invalid/`

The validation command and tests are dependency-free and use the repo-local schema subset validator.

Current validation coverage:

- `bin/validate-examples` validates examples and fixtures.
- `python3 -m unittest discover -s tests -p 'test_*.py'` runs schema and transition tests.

### Medium Plans

Medium Plan is now partially typed.

Added:

- `schemas/image-medium-plan.schema.json`
- `schemas/sound-medium-plan.schema.json`
- `schemas/text-medium-plan.schema.json`

Added examples:

- `examples/image-medium-plan.example.json`
- `examples/sound-medium-plan.example.json`

Still future:

- `schemas/video-medium-plan.schema.json`
- possibly a shared `schemas/medium-plan.schema.json`

## Completed Implementation Milestones

### 1. Validation Tooling

Added:

```text
bin/validate-examples
```

It validates example JSON files and fixture JSON files against their schemas using the repo-local validator.

Success condition met:

- one command validates all examples,
- command exits nonzero on schema mismatch,
- command is documented in README or Development docs.

### 2. Pipeline Contract

Added:

```text
docs/pipeline-contract.md
```

Each step should define:

- `step_id`
- input record type,
- output record type,
- output schema,
- reviewer required,
- gate required,
- next allowed steps.

Success condition met:

- text-to-image and text-to-Suno have explicit typed step maps,
- future video, text, mixed-media, and expanded sound branches can add steps without redefining the model.

### 3. Test Fixtures

Added:

```text
tests/fixtures/
  text-to-image/
  text-to-suno/
  story/
  reviews/
```

Success condition met:

- fixtures represent valid outputs for each pipeline step,
- validation tooling can run over fixtures and examples.

### 4. Schema Validation Tests

Added tests that verify:

- examples validate,
- fixtures validate,
- invalid records fail for meaningful reasons,
- review records include `matched`, `drifted`, `findings`, `recommended_revision`, and `approval_status`.

### 5. Transition Tests

Added tests that verify allowed record transitions:

```text
Source Record + Meaning Interview -> Transformation Brief
Transformation Brief -> Beat Plan
Beat Plan -> Long-Work Stewardship Record, when cumulative
Beat Plan -> Image Medium Plan / Sound Medium Plan / Text Medium Plan
Image Medium Plan / Text Medium Plan -> Long-Work Stewardship Record, when cumulative
Image Medium Plan -> Creative Brief
Sound Medium Plan -> Sound Creative Brief
Text Medium Plan -> Text Creative Brief
Creative Brief + Medium Plan -> Prompt Plan / Text Generation Plan
Prompt Plan / Text Generation Plan / Prompt Branch Set -> Output Record
Output Record -> Output Critic Review Record
Output Critic Review Record -> Output Acceptance Gate Decision
Review Packet -> Review Record
```

These tests should check structure and routing, not AI quality.

Added emotional movement integrity coverage:

- Image Medium Plan image roles must reference Key Emotional Movements that exist in the governing Beat Plan.
- Creative Brief suggested images must reference Key Emotional Movements that exist in the governing Beat Plan.
- Suno Sound Prompt Plan sections and variants must reference Beat Plan beats and Key Emotional Movements.
- Text Medium Plan and Text Generation Plan sections must reference Beat Plan beats and Key Emotional Movements.
- Text rewrite Output Records must point to a previous Output Record when `origin_type` is `agent_rewritten`.
- Prompt Branch Set meaning kernels and branches must reference Key Emotional Movements from the governing Beat Plan.
- Review Records must include numeric tension intensity assessments and reviewer verdicts against minimum intensity.
- Key Emotional Movement `beat_ids` must point to existing Beat Plan beats.
- Beat `builds_toward_key_movement_id`, when present, must point to an existing Key Emotional Movement.

### Long-Work Stewardship

Added the first schema-backed Project Memory record for Cumulative Work:

- `schemas/long-work-stewardship-record.schema.json`,
- image-series and long-text stewardship fixtures,
- schema validation coverage for both fixtures,
- transition coverage from Beat Plan and Medium Plan into Long-Work Stewardship,
- `long_work_reviewer` support in Review Records,
- `long_work_checkpoint` support in Gate Decisions.

This record applies to long text, image series, and future cumulative sequences whose parts build on each other. It does not apply automatically to non-sequential portfolios, store collections, or curator batches. Beat Plan remains the story authority; the stewardship record tracks part-to-part readiness, continuity, checkpoints, progress, and drift.

### Long-Work Stewardship Coherence Review

Reviewed the through line across schemas, tests, conductor skill, medium skills, pipeline docs, story docs, gates, storage, and output journeys. Tightened the lifecycle so it now has two explicit states:

- foundation stewardship after Story Approval, before a Medium Plan exists,
- enriched stewardship after the Medium Plan maps beats into image roles, text sections, chapters, scenes, or movements.

The schema now allows `medium_plan_id = null`, an empty `part_plan[]`, and `readiness_review.status = "pending"` for the foundation record. Review and Gate Decision schemas now let Long-Work Reviewer records and Long-Work Checkpoint gates point directly at `long_work_stewardship` records. Added fixture and transition coverage for this foundation state so the docs' "create after Story Approval" rule is mechanically valid.

### Output Lifecycle Fixtures

Added fixtures for:

- `tests/fixtures/reviews/output-review-record.json`
- `tests/fixtures/reviews/output-review-blocked-waived-record.json`
- `tests/fixtures/gates/output-acceptance-gate.json`
- `tests/fixtures/gates/output-acceptance-waiver-gate.json`

These make the output lifecycle concrete without expanding Output Record into taste memory, calibration, or batch orchestration. They cover both the normal approval path and the blocked-review path where the artist explicitly waives a blocking Output Critic finding before Output Acceptance Gate proceeds.

## Current Best Next Step

This cleanup pass is complete enough to move from repair into consolidation. The immediate next pass should run end-to-end dry-run rehearsals from Reference to Prompt Plan or Text Generation Plan, then tighten any docs, skill instructions, or schemas that still feel under-specified before adding a new medium branch or provider adapter.

Reason:

- Transformation Brief, Beat Plan, Medium Plan, Review Record, Prompt Branch Set, Gate Decision, and Output Record schemas now exist,
- Artist Meaning now records a Decision Interview instead of relying on silent defaults,
- Beat Plans now carry Intended Feeling, Key Emotional Movements, Expectation Turns, and tension profiles,
- image Medium Plans, Creative Brief Records, Suno Sound Prompt Plans, Text Medium Plans, Text Creative Brief Records, Text Generation Plans, Prompt Branch Sets, and Review Records now preserve emotional movement and tension criteria,
- fixtures and tests now cover the output review, artist waiver, and acceptance lifecycle,
- transition tests now check emotional movement references across Beat Plan, Image Medium Plan, Creative Brief, Sound Prompt Plan, Text Medium Plan, Text Generation Plan, Prompt Branch Set, Output Record, and Review Record fixtures,
- `skills/critique-asset/SKILL.md` now treats Output Record as the preferred reviewed artifact for concrete outputs and can review Text Generation Plans,
- `skills/artist-os/SKILL.md` now includes Output Record, Output Critic Review, and Output Acceptance Gate phases after generation/import/draft/edit,
- promotion concepts need real curation workflows before they become schemas or Output Record fields,
- output batch/group records need provider adapters or batch generation workflows before they become schemas.

Near-term plan:

1. Run one end-to-end dry-run rehearsal from Reference to Prompt Plan or Text Generation Plan for image, Suno, and Text Journey, and update any docs or skill instructions that still feel under-specified.
2. Add reviewer fixture tests for symbolic gate status and medium-gate completeness when review packets omit required gate context.
3. Add reviewer fixture tests for Text Generation Plan critique and text Output Critic packets once a full rehearsal produces natural review examples.
4. Design provider/import adapter contracts that emit Output Records without weakening the dry-run approval boundary.
5. Add provider-adapter hard guards: image and Suno adapters must refuse provider calls unless the request includes a matching approved Generation Approval Gate for that exact call or approved batch.
6. Keep focused regression coverage for rehearsal findings: fallback separated review execution and Suno `phonetic_vocals` Custom Mode mapping.

Final verification for this pass:

- `bin/validate-examples`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `python3 -m py_compile $(rg --files -g '*.py')`
- `jq empty schemas/*.json examples/*.json tests/fixtures/*/*.json tests/invalid/*.json`
- `bash -n bin/install-codex-dev-skills bin/uninstall-codex-dev-skills`
- manual evals in `evals/` after changing skill `description:` frontmatter or `skills/artist-os/SKILL.md`
- stale field scan for deferred promotion and batch fields

## Larger Roadmap Position

The repository now has the core transformation kernel:

```text
Reference
  -> Artist Meaning
  -> Transformation Brief
  -> Beat Plan
  -> Medium Plan
  -> Creative Brief Record
  -> Prompt Plan / Text Generation Plan
  -> optional Prompt Branch Set
  -> Output Record
  -> Review Record
  -> Gate Decision
```

Implemented branches:

- text-to-image through Image Medium Plan, Creative Brief Record, Provider-Neutral Image Prompt Plan, optional Prompt Branch Set, and output lifecycle fixtures,
- text-to-Suno through Sound Medium Plan, Sound Creative Brief Record, Suno Sound Prompt Plan, and output lifecycle contracts,
- Text Journey through Text Medium Plan, Text Creative Brief Record, Text Generation Plan, fresh-context draft Output Record, and editorial rewrite Output Record fixtures.
- Structure Library docs for reusable Story Structures and Cultural Format Structures, split into context-efficient per-entry files with chooser indexes.

Not implemented yet:

- Video Medium Plan and Mixed-Media Plan schemas,
- provider adapters and real provider-backed generation calls,
- import adapters for artist-provided output artifacts,
- durable taste memory, calibration choice, accepted-work promotion, output batch, or provider-run records.

This means the next work should be consolidation first, then expansion. Good next passes are:

- rehearse the image and Suno dry-run flows end to end against the hardened Story Structure and emotional-primacy model,
- rehearse the Text Journey end to end and harden any schema or skill gaps found in use,
- build provider/import adapter contracts that emit Output Records,
- design curation records after real accepted outputs exist.

Structure Library rehearsal status:

- Service article / how-to, op-ed, and short story Cultural Format Structure entries all rehearsed cleanly against Text Journey without schema changes.
- `three_act_structure` rehearsed cleanly as Story Journey / Beat Plan authority and is promoted at `tests/fixtures/story/three-act-rehearsal/beat-plan.json`. The rehearsal confirmed that Story Structure can guide movement, turn logic, compression, expansion, and failure modes without choosing medium, output shape, asset count, or Cultural Format Structure.
- `hero_journey` rehearsed cleanly as Story Journey / Beat Plan authority and is promoted at `tests/fixtures/story/hero-journey-rehearsal/beat-plan.json`. The rehearsal confirmed that `failure_modes` can carry anti-savior and anti-private-victory guardrails for canonical frameworks with stronger cultural baggage.
- `kishotenketsu` rehearsed cleanly as Story Journey / Beat Plan authority and is promoted at `tests/fixtures/story/kishotenketsu-rehearsal/beat-plan.json`. The rehearsal confirmed that Beat Plans can express contrast, recontextualization, and reconciliation without forcing conflict escalation.
- `freytag_dramatic_arc` rehearsed cleanly as Story Journey / Beat Plan authority and is promoted at `tests/fixtures/story/freytag-rehearsal/beat-plan.json`. The rehearsal confirmed that Beat Plans can preserve rise, peak turn, falling consequence, and residue; Freytag climax maps to Beat Plan `reversal` while Key Emotional Movement carries `role = "climax"`.
- After four passing Story Structure rehearsals, `story_structure` is required in `schemas/beat-plan.schema.json` for `beat_pair`, `three_part_sequence`, `sequence`, `scene`, `arc`, and `world`, and remains optional for `single_beat`.
- Image output shape no longer treats three-part structure as a separate image recommendation or presentation mode. Three images are modeled as `image_series`; the shared story-mode enum has been renamed from the legacy term to `three_part_sequence`.
- `tests/fixtures/text-to-image/single-image-rehearsal/` protects the first-class single-image path: `story_mode = "single_beat"` validates without `story_structure`, and the Image Medium Plan uses `presentation_mode = "single_image"` with one image role and `series_plan.is_series = false`.
- `tests/fixtures/text-to-image/three-image-series-rehearsal/` protects the three-image path as an image series: the Beat Plan uses `story_mode = "sequence"` with adapted `story_structure`, and the Image Medium Plan uses `presentation_mode = "image_series"` with three image roles.
- `schemas/image-medium-plan.schema.json` now accepts optional `medium_output_shape_recommendation` so image planning can record the reasoning behind `single_image`, `compressed_arc`, or `image_series` without replacing `presentation_mode` as the accepted concrete image shape.
- `schemas/sound-medium-plan.schema.json` now accepts optional `medium_output_shape_recommendation` so sound planning can record the reasoning behind sound-specific work types or `sound_sequence` without replacing `sound_work_type`, `arrangement_direction`, or `sequence_plan`.
- `tests/fixtures/text-journey/op-ed-rehearsal/` is the representative promoted fixture because it proves `primary_text_form = "article"` can combine with `cultural_format_structure.library_entry_id = "op_ed"` without article subtype enums.
- Structure Library audit pass confirmed there are two Structure Library families: Story Structure and Cultural Format Structure. The chooser indexes now document selection guidance, common confusion pairs, and what each library must not decide.
- Cultural Format Structure v1 for written content now includes 42 context-efficient per-entry files across core, editorial/nonfiction, internet-native writing, argument/persuasion, creative/literary, and long narrative / Novel Craft groups. Novel Craft concepts are mapped into Cultural Format Structure entries and Stewardship Views while Long-Work Stewardship remains the continuity authority.
- Focused Text Journey rehearsals for `interview_q_and_a`, `prose_poem`, `plot_tracker`, and `newsletter_dispatch` passed without schema changes. The chooser now documents their current schema mappings: interview Q&A defaults to `article`, prose poem uses `poem`, plot tracker uses `other` plus `private_draft`, and newsletter dispatch uses the broad text form that matches the issue's main thread while CFS carries newsletter grammar.
- Focused Text Journey rehearsals for `profile`, `review_criticism`, `case_study`, `thought_leadership_essay`, `framework_post`, and `serialized_installment` also passed without schema changes. The chooser now documents default mappings for article-like CFS entries, social-post handling for platform-native professional posts, confusion pairs against nearby formats, and the Long-Work Stewardship boundary for serialized installments.
- Focused Text Journey rehearsals for `news_article`, `explainer_article`, `list_article`, `trend_analysis`, `teardown_analysis`, `field_notes`, and `curated_roundup` passed without schema changes. The chooser now documents article defaults, valid `field_notes` mappings, additional confusion pairs, and the repeated publication-use pressure around editorial/web formats currently falling back to `other`.
- Focused Text Journey rehearsals for `manifesto`, `speech`, `open_letter`, and `pitch` passed without schema changes. The chooser now documents their current mappings to `manifesto`, `script` plus `performance_text`, `letter`, and conditional pitch forms, along with confusion pairs across argument and persuasion formats.
- Focused Text Journey rehearsals for the remaining entries — `hook_driven_article`, `feature_article`, `personal_essay`, `literary_scene`, `monologue`, `letter`, `lyric_poem`, `narrative_poem`, `screenplay_scene`, `novel_outline`, `chapter`, `scene_card`, `sequence_arc`, `character_brief`, `relationship_arc`, `subplot_tracker`, `open_thread_tracker`, and `treatment_outline` — passed without schema changes. All 42 Cultural Format Structure entries have now had at least one Text Journey rehearsal pass.
- Storage design accepted sibling user-facing and internal roots under a user-chosen Wondermint Root: visible `Wondermint/Artist Library/` for outputs, Review Drafts, readable summaries, and artist-useful Personal Library notes; hidden `.wondermint/artist-os/` for Workspace Library records, SQLite, Project Memory, Feedback Logs, Learning Index data, Performance Signals, and internal personal-library records. The decision is recorded in `docs/adr/0006-sibling-artist-library-and-workspace-library.md` and the contract is in `docs/storage.md`. Implemented support now includes `WONDERMINT_ROOT` / `--wondermint-root` routing, direct `--library-root` routing for low-level Workspace Library access, Project Pointer creation and preservation, manifest fields for visible and feedback state, SQLite indexes for visible paths / learning / performance signals, visible-missing sync, feedback/learning/performance schemas, and CLI scaffolding for feedback intake and learning review.

## Future Follow-Ups

- Promote repeated CFS rehearsal findings into fixtures only when an entry exposes schema-critical behavior or a durable transition contract not already covered by the representative article/op-ed fixtures.
- Implement human-edited Artist Library file detection and Output Record revision creation so edited Review Drafts or Accepted Works become authoritative `human_edited` Output Artifact revisions instead of mutating prior records.
- Design and implement user-owned Structure Library resolution inside the accepted storage model: private user-added or override Story Structure and Cultural Format Structure entries, lookup order before shipped entries, collision rules, unknown-format promotion path, metadata, and low-context resolver indexes.
- Design Personal Style Memory: a local, artist-specific style library where Artist OS can save reusable Style Directions, accepted style traits, rejected style traits, calibration notes, sample references, and provenance. The record should be private Workspace Library state, not committed project data, and it should never outrank Artist Meaning, Beat Plan, Visual Dynamics, or the governing Creative Brief.
- Design a Randomizer function for accepted or final-ready work. Given a locked Reference, Artist Meaning, Transformation Brief, Beat Plan, and final outcome target, it should create one or more meaning-equivalent alternate directions that preserve the heart of the work while varying approved axes such as art style, genre, world, setting, symbolic language, composition, palette, or medium treatment. This should build on the Prompt Branch Set idea, but may need its own post-final workflow when the artist wants a radically different world or genre after a final outcome exists.
- Design Artist OS Personality Profiles for the skill layer. The goal is to make artist-facing communication feel distinctive and less generic while preserving all product rules: clear Decision Interviews, Recommended Answers, provenance, approval gates, and no unapproved generation calls. Profiles should change tone and interaction texture, not alter Artist Meaning or pipeline behavior.
- Decide whether the remaining text-first structure fields should move into video and mixed-media Medium Plans after Text Journey, Image Medium Plan, and Sound Medium Plan rehearsals harden Medium Output Shape Recommendation behavior. Image and sound now have optional Medium Output Shape Recommendation rationale, but not adapted Cultural Format Structure.
- Revisit `publication_use.use_case` only after one or two more editorial/article rehearsals confirm that article/editorial use should not continue falling back to `other`.
- Add `taste-memory-record.schema.json` only when accepted outputs need durable reusable taste guidance.
- Add `calibration-choice.schema.json` only when calibration choices need to update future prompt planning in a structured way.
- Add an Output Batch or Provider Run record only when provider adapters need batch-level cost tracking, retry tracking, or comparative curation.
- Consider a shared emotional-movement definition or schema fragment after image and sound both need the same fields. Do not abstract it earlier than necessary.

## Definition Of Done For The Typed Pipeline

Artist OS reaches the next maturity level when:

- each step has a declared input and output record,
- each output record has a schema,
- each schema has at least one valid example,
- examples and fixtures validate in one command,
- mandatory reviewer stages produce Review Records,
- no step advances unless its output validates,
- blocking reviewer findings stop advancement unless explicitly waived by the artist.
