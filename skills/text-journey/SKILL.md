---
name: artist-os-text-journey
description: Use when the artist wants the text/writing path once Artist Meaning exists — building or revising a Text Medium Plan, Text Creative Brief, Text Generation Plan, fresh-context written draft, or text editorial pass flow. Choose this directly, not the artist-os conductor, when the request is just this text step.
---

# Text Journey

You are the text translation and drafting director for Artist OS. Build the Text Journey: preserve Artist Meaning through written form, structure, voice, source-wording policy, fresh-context drafting, editorial passes, Output Records, and review.

## References

Load details only when needed:

- `docs/output-journeys/text.md` for the route, drafting boundary, editorial pass order, and Text Draft Packet rules.
- `docs/writing/README.md` and `docs/writing/references/` for fragments, beats, and shape.
- `docs/structure-library/README.md`, then only the relevant `docs/structure-library/story/` or `docs/structure-library/cultural-format/` entry, when selecting or adapting Story Structure or Cultural Format Structure.
- `docs/story/THEORY.md` and `docs/gates-and-reviews.md` for the shared Transformation Brief, Beat Plan, Story Gate, and reviewer rules.
- `schemas/transformation-brief.schema.json` and `schemas/beat-plan.schema.json` before medium-specific planning.
- `schemas/text-medium-plan.schema.json` for text translation decisions before Text Creative Brief creation.
- `schemas/long-work-stewardship-record.schema.json` for cumulative long text after Story Approval and Text Medium Plan mapping.
- `schemas/text-creative-brief.schema.json` after Writing Critic Review and Brief Approval.
- `schemas/text-generation-plan.schema.json` after Brief Approval and prompt/generation planning.
- `schemas/output-record.schema.json` for every concrete draft or rewrite artifact.
- `skills/clear-writing-pass` and `skills/human-voice-pass` only for the separate editorial passes after a conforming draft exists.
- `docs/storage.md` when writing or updating project records in the Workspace Library.

## Hard Gates

These hold whether you run standalone or under the `artist-os` conductor:

- Do not create a Text Creative Brief Record or Text Generation Plan until Writing Critic Review and Brief Approval are complete.
- Do not draft the final written Output Artifact until Draft Generation Approval is explicit, even when the agent drafts locally without a paid provider call.
- Draft the written Output Artifact in a fresh-context sub-agent using a bounded Text Draft Packet.
- For cumulative long text, create and maintain a Long-Work Stewardship Record; do not draft later sections while Long-Work Readiness is `repair_before_expansion` unless the artist repairs or explicitly waives the block.
- The fresh-context drafting sub-agent must not run the Human Voice Pass or Clear Writing Pass during first drafting.
- Run main-agent conformance review before any editorial pass. If the draft fails Artist Meaning, structure, section jobs, Intended Feeling, source-wording policy, or Text Generation Plan constraints, structure wins; correct the draft before editorial polishing.
- Run Clear Writing Pass and Human Voice Pass as separate bounded fresh-context sub-agents only when the Text Generation Plan policy allows them.
- Create an Output Record for every concrete draft, rewrite, or human-edited artifact. Rewrites use `origin.origin_type = "agent_rewritten"` and must set `previous_output_record_id`.
- Persist records and gate decisions as you create them, following `docs/storage.md`. Chat context is not durable storage.

## Inputs

Use the Text Reference, Source Record, Artist Meaning Record, Transformation Brief, Beat Plan, Text Medium Plan when available, revised Text Creative Brief Document, Writing Critic Review, Brief Approval, Draft Generation Approval, and any existing Output Records.

## Shared Story Records

Before creating the text-specific brief, produce:

1. A Transformation Brief matching `schemas/transformation-brief.schema.json`.
2. A Beat Plan matching `schemas/beat-plan.schema.json`.
3. A Text Medium Plan matching `schemas/text-medium-plan.schema.json`.

The Beat Plan is authoritative for story shape, including any Adapted Story Structure stored in the Beat Plan. The Text Medium Plan is authoritative for text translation decisions: Medium Output Shape Recommendation, Adapted Cultural Format Structure, writing method, Primary Text Form, Text Form Modifiers, voice / point of view, structure, fidelity policy, publication/use, gate statuses, and review requirements. The later Text Creative Brief Record must include `transformation_brief_id`, `beat_plan_id`, and `text_medium_plan_id`; do not embed duplicate Beat records.

For cumulative long text, the Long-Work Stewardship Record protects execution across text sections, chapters, scenes, or poem movements. The foundation record starts after Story Approval. Enrich it after Text Medium Plan by referencing text section or other medium part ids. Do not duplicate section execution, voice, fidelity, or editorial policy fields inside the stewardship record; those remain owned by Text Medium Plan and Text Generation Plan.

Every Beat must name an Intended Feeling and include an Expectation Turn. Do not accept a Beat Plan that only lists events, themes, or facts. Text should make each section or paragraph do a different job in the reader's experience.

For exploratory writing, follow strict `writing-beats`: candidate starting beats, artist choice, one beat at a time. For an obvious compact text target or artist-approved autopilot, you may draft a full recommended Beat Plan, but multi-beat, journey-shaped, or structurally ambiguous text still requires a bounded Beat Reviewer sub-agent before Text Medium Plan locking.

## Text Medium Plan Process

Use this only after the shared Transformation Brief and Beat Plan exist.

1. Identify formal observations from the Reference: voice, diction, imagery, pacing, lineation, paragraph pressure, structure, repetition, reversal, and source-wording sensitivity.
2. Consume the shared Beat Plan, including Adapted Story Structure when present. If Story Structure needs selection or revision, use `docs/structure-library/README.md` and open only the relevant Story Structure entry. Do not fork a separate text-only beat structure.
3. Select the writing method: `fragments`, `beats`, `shape`, or `hybrid`. Use `shape` when the output is a reader-facing finished piece.
4. Produce a Medium Output Shape Recommendation before locking Primary Text Form. Include requested shape, recommended shape, accepted shape, rationale, alternatives considered, tradeoffs, and conflict status.
5. If the artist-requested shape and recommended shape materially diverge, record a Medium Output Shape Conflict and resolve it with one Decision Interview question before locking the Text Medium Plan.
6. Select or adapt the Cultural Format Structure after the Medium Output Shape Recommendation is accepted, revised, or explicitly allowed to proceed unconfirmed. Use `docs/structure-library/cultural-format/README.md` to choose an entry, then open only that entry file. Include Audience Hook, audience promise, adapted parts, turn or payoff, adaptation policy, failure modes, and any recommended Stewardship Views.
7. Define one Primary Text Form, such as poem, article, prose scene, short story, monologue, script, lyrics, letter, essay/artist statement, manifesto, treatment, rewrite, adaptation, or other. If the artist names multiple forms, choose or recommend one primary form and treat the rest as Text Form Modifiers or constraints.
8. Define voice / point of view: speaker, distance, register, authority, and voice constraints.
9. Define structure in the form's own terms: paragraphs, sections, acts, scenes, verses, argument moves, hook, turn, refrain, ending, or hybrid structure. Map adapted Cultural Format Structure parts to Text Medium Plan sections rather than replacing section jobs. Keep Cultural Format Structure `function` at the audience-facing format-part level, section `structure_role` at the local position level, and section `section_job` at the concrete drafting-instruction level.
10. For every section, paragraph group, act, scene, or verse, name the structure role, section job, Intended Feeling, Expectation Turn translation, source-wording notes, and how it must feel different from neighboring sections.
11. Define Fidelity Policy: preserve source wording, adapt, invert, expand, compress, translate, or create new text from meaning.
12. Define publication/use and rights/privacy notes.
13. Produce the Text Medium Plan only after writing method, Medium Output Shape Recommendation, Cultural Format Structure when relevant, text form, voice, structure, fidelity, and publication/use choices are complete or explicitly allowed to proceed unconfirmed.
14. When the text structure is cumulative, enrich the Long-Work Stewardship Record from the completed Text Medium Plan with one Long-Work Part per text section, chapter, scene, or poem movement; include readiness, checkpoints, continuity rules, and drift management before Draft Generation Approval. Plot-tracker-style Stewardship Views are projections over Text Medium Plan and Long-Work Stewardship state, not separate authority records.

## Draft Text Creative Brief Process

Use this only after the Text Medium Plan exists. Before Writing Critic Review, build a substantive draft brief from the Text Medium Plan:

1. Preserve `transformation_brief_id`, `beat_plan_id`, and `text_medium_plan_id`.
2. Use the Text Medium Plan as the source of truth for Medium Output Shape Recommendation, Adapted Cultural Format Structure, writing method, Primary Text Form, voice, structure, fidelity policy, and publication/use.
3. Add Artist Meaning, formal observations, Emotional Qualities, Poetic Density Notes, source-wording constraints, transformation constraints, and editorial pass recommendations.
4. Produce the draft Text Creative Brief Document only after required medium gates are complete or explicitly allowed to proceed unconfirmed.

If running standalone, recommend Writing Critic Review. If the `artist-os` conductor is running, return the draft and stop; the conductor advances automatically.

## Text Generation Plan Process

Use this only after Writing Critic Review and Brief Approval.

1. Produce the Text Creative Brief Record matching `schemas/text-creative-brief.schema.json`.
2. Produce one Text Generation Plan matching `schemas/text-generation-plan.schema.json`.
3. Include `text_medium_plan_id`, `transformation_brief_id`, and `beat_plan_id`.
4. Include fresh-context drafting instructions and require a draft trace.
5. Include section-level drafting jobs that map to `beat_id`, `key_emotional_movement_id`, Intended Feeling, and section distinction.
6. Include source-wording policy and rights notes.
7. Set Clear Writing Pass Policy and Human Voice Pass Policy to `required`, `recommended`, `optional`, or `skip`, with degree and protected features.
8. Default editorial order is Clear Writing Pass first, Human Voice Pass second, unless the form requires a different order or skip.
9. Include Output Record requirements: draft Output Record required, rewrite Output Record required, rewrite origin `agent_rewritten`, and `previous_output_record_id` required for rewrites.

## Fresh-Context Drafting

After Draft Generation Approval, assemble a Text Draft Packet. The packet is internal and not schema-backed. Include only:

- task,
- approved Artist Meaning summary and must-preserve constraints,
- Text Medium Plan,
- Text Creative Brief,
- Text Generation Plan,
- source text or allowed excerpts,
- source-wording policy and rights notes,
- structure execution plan,
- voice constraints,
- protected features,
- explicit do-not-change rules.

The drafting sub-agent returns:

- drafted artifact text,
- compact draft trace mapping each section to source Beat or structure role, Intended Feeling, and key constraint preserved,
- conformance risks for the main agent.

Persist the concrete draft as an Output Record with `origin.origin_type = "agent_drafted"` and the compact draft trace in `traceability_summary`.

For cumulative long text, update the Long-Work Stewardship Record when a section, chapter, scene, or poem movement is drafted, rewritten, reviewed, accepted, blocked, or skipped. First-part and interval checkpoints must be resolved before drafting later dependent parts when marked `required_before_continuing`.

## Editorial Passes

Run editorial passes only after the main agent confirms the draft follows the Text Generation Plan.

1. Clear Writing Pass: use `skills/clear-writing-pass` when required or recommended by the Text Generation Plan.
2. Human Voice Pass: use `skills/human-voice-pass` by default unless the Text Generation Plan marks it optional or skipped.
3. Each pass runs in its own bounded fresh-context sub-agent.
4. Each pass receives only the current artifact text, the relevant policy, protected features, necessary brief constraints, and do-not-change rules.
5. Each pass produces a rewritten artifact plus a compact change trace.
6. Persist each rewrite as a new Output Record with `origin.origin_type = "agent_rewritten"`, `previous_output_record_id`, preserved draft trace, and rewrite trace notes.
7. The main agent performs a final check against Artist Meaning, Text Medium Plan, Text Creative Brief, Text Generation Plan, source-wording policy, protected features, and structure before Output Critic Review.

## Traceability Rules

Every writing choice must trace back to Artist Meaning, Reference evidence, Transformation Brief, Beat Plan, Adapted Story Structure when present, Text Medium Plan, Medium Output Shape Recommendation, Adapted Cultural Format Structure when present, Text Creative Brief, Text Generation Plan, source-wording policy, a section job, Intended Feeling, Expectation Turn translation, Poetic Density Note, or editorial pass policy.

Text form, clarity, and naturalness are subordinate to Artist Meaning, Beat Plan, structure, fidelity policy, and protected features.

## Outputs

Before Writing Critic Review, return the Text Medium Plan, draft Text Creative Brief Document, Beat Plan reference, Medium Output Shape Recommendation, Adapted Cultural Format Structure when present, structure plan, fidelity policy, editorial pass recommendations, and open questions.

After Writing Critic Review and Brief Approval, return the Text Creative Brief Record and Text Generation Plan.

After Draft Generation Approval, return the fresh-context draft Output Record, draft trace, main-agent conformance result, any editorial rewrite Output Records, and final-check notes for Output Critic Review.

When emitted as records, JSON must validate against `schemas/text-medium-plan.schema.json`, `schemas/text-creative-brief.schema.json`, `schemas/text-generation-plan.schema.json`, `schemas/long-work-stewardship-record.schema.json` when stewardship is active, and `schemas/output-record.schema.json`.
