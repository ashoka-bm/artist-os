# Artist OS Progress

This document records what has been created, what is transitional, and what comes next. Keep it current when changing architecture, schemas, skills, or tests.

## Current Goal

Artist OS has established the core typed transformation pipeline for the current image and Suno dry-run slices. The current refinement pass adds an emotional-primacy contract on top of that pipeline: records must now name the intended feeling, preserve the artist's authority through a Decision Interview, and carry enough tension movement for reviewers to judge whether the work expresses a feeling rather than only describing a fact.

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

Provider-backed generation remains out of scope without explicit approval.

### Shared Story Architecture

Added:

- `docs/story/THEORY.md`
- `docs/story/ARCHITECTURE.md`
- `docs/output-journeys/`

Story is now the shared layer: every output is one or more approved beats translated into a medium.

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

- `skills/first-slice-flow/SKILL.md`
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

Updated examples and fixtures for Artist Meaning, Beat Plans, Image Medium Plans, and Creative Brief Records to validate against the new contracts.

## Transitional Decisions

### Embedded Beats

`creative-brief.schema.json` and `sound-creative-brief.schema.json` still require embedded `beats`.

Current rule:

- `beat_plan_id` is authoritative.
- embedded `beats` are transitional medium-local summaries.

Later cleanup:

- remove embedded `beats` from medium-specific brief schemas once downstream consumers and examples are stable.

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
- `tests/json_schema_validator.py`
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

Added examples:

- `examples/image-medium-plan.example.json`
- `examples/sound-medium-plan.example.json`

Still future:

- `schemas/video-medium-plan.schema.json`
- `schemas/text-medium-plan.schema.json`
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
Beat Plan -> Image Medium Plan / Sound Medium Plan
Image Medium Plan -> Creative Brief
Sound Medium Plan -> Sound Creative Brief
Creative Brief + Medium Plan -> Prompt Plan
Prompt Plan / Prompt Branch Set -> Output Record
Output Record -> Output Critic Review Record
Output Critic Review Record -> Output Acceptance Gate Decision
Review Packet -> Review Record
```

These tests should check structure and routing, not AI quality.

Added emotional movement integrity coverage:

- Image Medium Plan image roles must reference Key Emotional Movements that exist in the governing Beat Plan.
- Creative Brief suggested images must reference Key Emotional Movements that exist in the governing Beat Plan.
- Key Emotional Movement `beat_ids` must point to existing Beat Plan beats.
- Beat `builds_toward_key_movement_id`, when present, must point to an existing Key Emotional Movement.

### Output Lifecycle Fixtures

Added fixtures for:

- `tests/fixtures/reviews/output-review-record.json`
- `tests/fixtures/reviews/output-review-blocked-waived-record.json`
- `tests/fixtures/gates/output-acceptance-gate.json`
- `tests/fixtures/gates/output-acceptance-waiver-gate.json`

These make the output lifecycle concrete without expanding Output Record into taste memory, calibration, or batch orchestration. They cover both the normal approval path and the blocked-review path where the artist explicitly waives a blocking Output Critic finding before Output Acceptance Gate proceeds.

## Current Best Next Step

This cleanup pass is complete enough to move from repair into consolidation. The immediate next pass should harden the emotional-primacy contract across sound, prompt plans, and reviewer packets before adding a new medium branch or provider adapter.

Reason:

- Transformation Brief, Beat Plan, Medium Plan, Review Record, Prompt Branch Set, Gate Decision, and Output Record schemas now exist,
- Artist Meaning now records a Decision Interview instead of relying on silent defaults,
- Beat Plans now carry Intended Feeling, Key Emotional Movements, Expectation Turns, and tension profiles,
- image Medium Plans and Creative Brief Records now preserve role-level emotional movement and tension,
- fixtures and tests now cover the output review, artist waiver, and acceptance lifecycle,
- transition tests now check emotional movement references across Beat Plan, Image Medium Plan, and Creative Brief fixtures,
- `skills/critique-asset/SKILL.md` now treats Output Record as the preferred reviewed artifact for concrete outputs,
- `skills/first-slice-flow/SKILL.md` now includes Output Record, Output Critic Review, and Output Acceptance Gate phases after generation/import/draft/edit,
- promotion concepts need real curation workflows before they become schemas or Output Record fields,
- output batch/group records need provider adapters or batch generation workflows before they become schemas.

Near-term plan:

1. Extend the same Intended Feeling, Key Emotional Movement, Expectation Turn, and Minimum Tension Criteria language into the sound-side schemas and examples where the current contracts are still looser than image.
2. Add Prompt Plan and Prompt Branch Set integrity checks so prompt variants preserve the approved Beat Plan, Medium Plan, tension criteria, and role distinctions.
3. Add reviewer fixture tests that fail when a review packet omits Intended Feeling, governing tension criteria, symbolic gate status, or emotional movement references.
4. Run one end-to-end dry-run rehearsal from Reference to Prompt Plan and update any docs or skill instructions that still feel under-specified.

Final verification for this pass:

- `bin/validate-examples`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `python3 -m py_compile $(rg --files -g '*.py')`
- `jq empty schemas/*.json examples/*.json tests/fixtures/*/*.json tests/invalid/*.json`
- `bash -n bin/install-codex-dev-skills bin/uninstall-codex-dev-skills`
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
  -> Prompt Plan
  -> optional Prompt Branch Set
  -> Output Record
  -> Review Record
  -> Gate Decision
```

Implemented branches:

- text-to-image through Image Medium Plan, Creative Brief Record, Provider-Neutral Image Prompt Plan, optional Prompt Branch Set, and output lifecycle fixtures,
- text-to-Suno through Sound Medium Plan, Sound Creative Brief Record, Suno Sound Prompt Plan, and output lifecycle contracts.

Not implemented yet:

- Video Medium Plan, Text Medium Plan, and Mixed-Media Plan schemas,
- provider adapters and real provider-backed generation calls,
- import adapters for artist-provided output artifacts,
- durable taste memory, calibration choice, accepted-work promotion, output batch, or provider-run records,
- removal of transitional embedded `beats` from medium-specific brief schemas.

This means the next work should be consolidation first, then expansion. Good next passes are:

- harden sound, prompt-plan, branch-set, and reviewer contracts against the emotional-primacy model,
- add the next Medium Plan schema and journey tests once the current image and sound contracts stabilize,
- build provider/import adapter contracts that emit Output Records,
- design curation records after real accepted outputs exist,
- remove embedded `beats` once downstream consumers only use `beat_plan_id`.

## Future Follow-Ups

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
