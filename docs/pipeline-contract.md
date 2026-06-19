# Pipeline Contract

Artist OS is a typed transformation pipeline. Each step consumes declared input records and produces one declared output record. The output must validate before the next step begins.

## Pipeline Rule

```text
Step Input Record(s)
  -> Agent / Skill Transformation
  -> Step Output Record
  -> Schema Validation
  -> Mandatory Reviewer Sub-Agent, when required
  -> Next Step Input Record(s)
```

No step advances unless its output validates against the declared schema. Review stages produce Review Records.

## Record Types

| Record type | Schema | Example |
| --- | --- | --- |
| Source Record | `schemas/source-record.schema.json` | `examples/source-record.example.json` |
| Artist Meaning | `schemas/artist-meaning.schema.json` | `examples/artist-meaning.example.json` |
| Gate Decision | `schemas/gate-decision.schema.json` | `examples/gate-decision.example.json` |
| Transformation Brief | `schemas/transformation-brief.schema.json` | `examples/transformation-brief.example.json` |
| Beat Plan | `schemas/beat-plan.schema.json` | `examples/beat-plan.example.json` |
| Long-Work Stewardship Record | `schemas/long-work-stewardship-record.schema.json` | `tests/fixtures/long-work/foundation-stewardship-record.json` |
| Image Medium Plan | `schemas/image-medium-plan.schema.json` | `examples/image-medium-plan.example.json` |
| Sound Medium Plan | `schemas/sound-medium-plan.schema.json` | `examples/sound-medium-plan.example.json` |
| Text Medium Plan | `schemas/text-medium-plan.schema.json` | `tests/fixtures/text-journey/text-medium-plan.json` |
| Creative Brief Record | `schemas/creative-brief.schema.json` | `examples/text-creative-brief.example.json` |
| Sound Creative Brief Record | `schemas/sound-creative-brief.schema.json` | `examples/text-sound-creative-brief.example.json` |
| Text Creative Brief Record | `schemas/text-creative-brief.schema.json` | `tests/fixtures/text-journey/text-creative-brief.json` |
| Provider-Neutral Image Prompt Plan | `schemas/prompt-plan.schema.json` | `examples/text-prompt-plan.example.json` |
| Prompt Branch Set | `schemas/prompt-branch-set.schema.json` | `examples/prompt-branch-set.example.json` |
| Suno Sound Prompt Plan | `schemas/sound-prompt-plan.schema.json` | `examples/text-sound-prompt-plan.example.json` |
| Text Generation Plan | `schemas/text-generation-plan.schema.json` | `tests/fixtures/text-journey/text-generation-plan.json` |
| Output Record | `schemas/output-record.schema.json` | `examples/output-record.example.json` |
| Review Record | `schemas/review-record.schema.json` | `examples/review-record.example.json` |

## Shared Steps

### `source.intake`

- Input: artist-provided Reference.
- Output: Source Record.
- Schema: `schemas/source-record.schema.json`.
- Skill: `skills/ingest-reference`.
- Reviewer required: no.
- Gate: Routing Gate if target medium is unclear.
- Next: `meaning.interview`.

### `meaning.interview`

- Input: Source Record and artist answers.
- Output: Artist Meaning.
- Schema: `schemas/artist-meaning.schema.json`.
- Skill: `skills/meaning-interview`.
- Reviewer required: Meaning Reviewer when later drift is suspected.
- Gate: Meaning Confirmation Gate.
- Next: `story.transformation_brief`.

The Meaning Interview uses a bounded Decision Interview: one question at a time, each with the agent's recommended answer, persisted in `decision_interview`. Do not advance to transformation brief while meaning, intended feeling, must-preserve constraints, avoid constraints, medium/story-shape direction, or success criteria are silently unresolved.

### `gate.decision`

- Input: current stage record, options presented, and artist response.
- Output: Gate Decision.
- Schema: `schemas/gate-decision.schema.json`.
- Skill: conductor or active medium planner.
- Reviewer required: no, unless the gate records an unwaived block or later drift is suspected.
- Gate: any canonical gate.
- Next: the stage unlocked by the gate decision.

### `story.transformation_brief`

- Input: Source Record and Artist Meaning.
- Output: Transformation Brief.
- Schema: `schemas/transformation-brief.schema.json`.
- Skill: medium planner or future story planner.
- Reviewer required: Meaning Reviewer when the interpretation may override Artist Meaning.
- Gate: Interpretation Gate.
- Next: `story.beat_plan`.

### `story.beat_plan`

- Input: Transformation Brief.
- Output: Beat Plan.
- Schema: `schemas/beat-plan.schema.json`.
- Skill: medium planner or future story planner.
- Structure rule: `story_structure` is required when `story_mode` is `beat_pair`, `triptych`, `sequence`, `scene`, `arc`, or `world`; it remains optional for `single_beat`.
- Reviewer required: Beat Reviewer sub-agent for multi-beat, sequence, series, lyric-bearing, scene, arc, or ambiguous plans.
- Gate: Story Gate and Story Approval Gate.
- Next: image, sound, video, text, or mixed-media medium planning.

### `long_work.stewardship`

- Input: approved Beat Plan; later enriched by Medium Plan, Output Records, Review Records, and Long-Work Checkpoint Gate Decisions.
- Output: Long-Work Stewardship Record.
- Schema: `schemas/long-work-stewardship-record.schema.json`.
- Skill: conductor, active medium planner, or future long-work stewardship skill.
- Reviewer required: Long-Work Reviewer for readiness, checkpoint, cumulative drift, and proposed continuity update reviews.
- Gate: Long-Work Checkpoint Gate when a checkpoint requires artist confirmation or waiver.
- Next: Medium Plan enrichment, Long-Work Readiness, prompt or draft expansion, checkpoint review, Output Review, or Story Approval if a proposed update changes story authority.

Create the Long-Work Stewardship Record only for Cumulative Work: triptychs, image series, long text, song sequences, video sequences, mixed-media sequences, or other work where later parts depend on prior parts or on an approved emotional arc. Do not create it for non-sequential portfolios, store sets, curator batches, or Prompt Branch Sets unless the artist makes them cumulative.

The foundation Long-Work Stewardship Record is valid immediately after Story Approval. At that point `medium_plan_id` may be `null`, `part_plan[]` may be empty, and Long-Work Readiness may be `pending`. After the Medium Plan exists, enrich the same record with `medium_plan_id`, one `part_plan[]` entry per cumulative unit, continuity rules, checkpoints, and readiness before expansion.

The Beat Plan remains the story authority. The Long-Work Stewardship Record references the Beat Plan and Medium Plan, records continuity rules and checkpoints, and blocks expansion when Long-Work Readiness is `repair_before_expansion` unless the artist repairs or explicitly waives the block.

### `review.record`

- Input: review packet.
- Output: Review Record.
- Schema: `schemas/review-record.schema.json`.
- Skill: critic or reviewer skill.
- Reviewer required: this is the reviewer output.
- Gate: any required review gate.
- Next: continue if `approval_status` is `approve`; revise if `revise`; stop unless artist waives if `block`.

The Review Record must include numeric tension intensity assessments. Reviewers compare claimed intensity against their own assessed intensity and the minimum required intensity, then set `meets_minimum`; downstream gates use that verdict when deciding whether a block can be waived or whether revision is required.

### `output.record`

- Input: Prompt Plan, Text Generation Plan, or Prompt Branch Set; generated, imported, drafted, rewritten, or edited output artifact; generation or Draft Generation Approval when required.
- Output: Output Record.
- Schema: `schemas/output-record.schema.json`.
- Skill: conductor, provider adapter, import adapter, or drafting skill.
- Reviewer required: Output Critic sub-agent before Output Acceptance Gate unless explicitly waived by the artist.
- Gate: Generation Approval Gate for provider-backed generation; Output Acceptance Gate for acceptance.
- Next: Output Critic Review, Output Acceptance Gate, calibration context, export, archive, or revision.

## Text-To-Image Steps

### `image.medium_plan`

- Input: Beat Plan, Transformation Brief, Artist Meaning, Source Record, visual gate decisions.
- Output: Image Medium Plan.
- Schema: `schemas/image-medium-plan.schema.json`.
- Skill: `skills/text-to-image-plan`.
- Reviewer required: Beat Reviewer sub-agent when the image plan is multi-beat, series, or ambiguous.
- Gate: Symbology Gate, Presentation Gate, Style Gate, Detail Gate.
- Next: `long_work.stewardship` enrichment when the image work is cumulative, otherwise `image.creative_brief`.

### `image.creative_brief`

- Input: Image Medium Plan, Beat Plan, Transformation Brief, Artist Meaning, Source Record, visual gate decisions.
- Output: Creative Brief Record.
- Schema: `schemas/creative-brief.schema.json`.
- Skill: `skills/text-to-image-plan`.
- Reviewer required: Art Critic sub-agent.
- Gate: Symbology Gate, Style Gate, Brief Approval Gate.
- Next: `image.prompt_plan`.

The Creative Brief Record must include `transformation_brief_id` and `beat_plan_id`. It does not embed Beat summaries; the referenced Beat Plan is authoritative for story shape and emotional movement.

### `image.prompt_plan`

- Input: approved Creative Brief Record and Image Medium Plan.
- Output: Provider-Neutral Image Prompt Plan.
- Schema: `schemas/prompt-plan.schema.json`.
- Skill: `skills/text-to-image-plan`.
- Reviewer required: Prompt Critic sub-agent.
- Gate: Prompt Lock Gate.
- Next: dry-run completion, Generation Approval Gate, or Output Review.

The Provider-Neutral Image Prompt Plan must include `transformation_brief_id`, `beat_plan_id`, and `image_medium_plan_id`.

### `image.prompt_branch_set`

- Input: approved Provider-Neutral Image Prompt Plan, Creative Brief Record, and Image Medium Plan.
- Output: Prompt Branch Set.
- Schema: `schemas/prompt-branch-set.schema.json`.
- Skill: `skills/text-to-image-plan`.
- Reviewer required: Prompt Critic sub-agent when the branch set will be used for generation or broad curator selection.
- Gate: Prompt Branch Gate and Generation Approval Gate before provider-backed generation.
- Next: dry-run curation, Generation Approval Gate, or Output Review.

The Prompt Branch Set preserves the same meaning kernel while deliberately varying style, setting, symbol, composition, and other approved axes. It is for curator batches, not for replacing the approved Prompt Plan.

The Prompt Branch Set must carry the governing Intended Feeling, Key Emotional Movement ids, Minimum Tension Criteria, and branch-level emotional/tension preservation. Each branch names the Key Emotional Movement and Expectation Turn Translation it preserves, so branch variation cannot drift into style-only exploration.

## Text-To-Suno Steps

### `sound.medium_plan`

- Input: Beat Plan, Transformation Brief, Artist Meaning, Source Record, sound gate decisions.
- Output: Sound Medium Plan.
- Schema: `schemas/sound-medium-plan.schema.json`.
- Skill: `skills/text-to-suno-plan`.
- Reviewer required: Beat Reviewer sub-agent for multi-section, sequence, or lyric-bearing plans.
- Gate: Sound Work Type, Sonic Concept, Genre / Production, Tempo / Groove, Vocal / Lyric, Arrangement / Form.
- Next: `sound.creative_brief`.

### `sound.creative_brief`

- Input: Sound Medium Plan, Beat Plan, Transformation Brief, Artist Meaning, Source Record, sound gate decisions.
- Output: Sound Creative Brief Record.
- Schema: `schemas/sound-creative-brief.schema.json`.
- Skill: `skills/text-to-suno-plan`.
- Reviewer required: Sound Critic sub-agent.
- Gate: Sonic Concept, Genre / Production, Tempo / Groove, Vocal / Lyric, Arrangement / Form, Brief Approval Gate.
- Next: `sound.prompt_plan`.

The Sound Creative Brief Record must include `transformation_brief_id` and `beat_plan_id`. It does not embed Beat summaries; the referenced Beat Plan is authoritative for story shape and emotional movement.

### `sound.prompt_plan`

- Input: approved Sound Creative Brief Record and Sound Medium Plan.
- Output: Suno Sound Prompt Plan.
- Schema: `schemas/sound-prompt-plan.schema.json`.
- Skill: `skills/text-to-suno-plan`.
- Reviewer required: Prompt Critic sub-agent.
- Gate: Prompt Lock Gate.
- Next: dry-run completion, Generation Approval Gate, or Output Review.

The Suno Sound Prompt Plan must include `transformation_brief_id`, `beat_plan_id`, and `sound_medium_plan_id`.

The Suno Sound Prompt Plan must include `emotional_tension_contract`, section-level Beat and Key Emotional Movement mapping, section-level Expectation Turn Translation, and variant-level `emotional_tension_preservation`. Prompt variants may vary sonic execution, but they must preserve the approved Intended Feeling and Minimum Tension Criteria.

## Text Journey Steps

### `text.medium_plan`

- Input: Beat Plan, Transformation Brief, Artist Meaning, Source Record, text gate decisions.
- Output: Text Medium Plan.
- Schema: `schemas/text-medium-plan.schema.json`.
- Skill: `skills/text-journey`.
- Reviewer required: Beat Reviewer sub-agent for multi-beat, sequence, scene, arc, or structurally ambiguous plans.
- Gate: Writing Method, Text Form, Voice / Point of View, Structure, Fidelity / Transformation, Publication / Use.
- Next: `long_work.stewardship` enrichment when the text work is cumulative, otherwise `text.creative_brief`.

Each `structure_plan.sections[]` entry must map to a Beat and Key Emotional Movement, name a section job, state the Intended Feeling, translate the Expectation Turn, and explain how the section differs from adjacent sections.

### `text.creative_brief`

- Input: Text Medium Plan, Beat Plan, Transformation Brief, Artist Meaning, Source Record, text gate decisions.
- Output: Text Creative Brief Record.
- Schema: `schemas/text-creative-brief.schema.json`.
- Skill: `skills/text-journey`.
- Reviewer required: Writing Critic sub-agent.
- Gate: Brief Approval Gate.
- Next: `text.generation_plan`.

The Text Creative Brief Record must include `transformation_brief_id`, `beat_plan_id`, and `text_medium_plan_id`. It does not embed Beat records; the referenced Beat Plan is authoritative for story shape and emotional movement.

### `text.generation_plan`

- Input: approved Text Creative Brief Record and Text Medium Plan.
- Output: Text Generation Plan.
- Schema: `schemas/text-generation-plan.schema.json`.
- Skill: `skills/text-journey`.
- Reviewer required: Prompt Critic sub-agent.
- Gate: Prompt Lock Gate and Draft Generation Approval Gate.
- Next: fresh-context draft Output Record, editorial rewrite Output Records, Output Critic Review, or Output Acceptance Gate.

The Text Generation Plan must require fresh-context drafting, a returned draft trace, main-agent conformance review, editorial pass policies, and Output Records for every concrete draft or rewrite artifact.

## Transition Rules

Allowed structural transitions:

```text
Source Record -> Artist Meaning
Gate Question -> Gate Decision
Artist Meaning -> Transformation Brief
Transformation Brief -> Beat Plan
Beat Plan -> Long-Work Stewardship Record, when cumulative
Long-Work Stewardship Record -> Long-Work Checkpoint Gate Decision, when a checkpoint requires artist decision
Beat Plan -> Image Medium Plan
Beat Plan -> Sound Medium Plan
Beat Plan -> Text Medium Plan
Image Medium Plan -> Long-Work Stewardship Record, when cumulative
Text Medium Plan -> Long-Work Stewardship Record, when cumulative
Image Medium Plan -> Creative Brief Record
Sound Medium Plan -> Sound Creative Brief Record
Text Medium Plan -> Text Creative Brief Record
Creative Brief Record -> Provider-Neutral Image Prompt Plan
Text Creative Brief Record -> Text Generation Plan
Provider-Neutral Image Prompt Plan -> Prompt Branch Set
Prompt Plan / Text Generation Plan / Prompt Branch Set -> Output Record
Output Record -> Long-Work Stewardship Record, when cumulative
Output Record -> Output Critic Review Record
Output Critic Review Record -> Output Acceptance Gate Decision
Sound Creative Brief Record -> Suno Sound Prompt Plan
Review Packet -> Review Record
```

Future medium branches should add transitions here before adding schemas or skills.

## Testing Rule

Every record type in this file should have:

- at least one example or fixture,
- schema validation coverage,
- transition coverage when it participates in a step transition.
