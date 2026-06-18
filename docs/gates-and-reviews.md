# Gates And Reviews

This is the canonical Artist OS contract for gates, critic roles, reviewer roles, and review execution.

Use this file before adding or changing a journey. Medium-specific docs can add local gates, but shared gate order and review rules live here.

## Shared Gate Order

The default cross-medium journey uses this gate order:

```text
Routing Gate
  -> Meaning Confirmation Gate
  -> Interpretation Gate
  -> Story Gate
  -> Story Critic Review
  -> Story Approval Gate
  -> Long-Work Readiness / Checkpoints, when the work is cumulative
  -> Medium Gates
  -> Medium Critic Review
  -> Prompt Critic Review
  -> Prompt Branch Gate, when curator batches are requested
  -> Prompt Lock Gate
  -> Generation Approval Gate
  -> Output Critic Review
  -> Output Acceptance Gate
```

Provider-backed generation always requires explicit approval. Drafting briefs, boards, prompt plans, lyrics, scripts, shot lists, comparison boards, or other dry-run artifacts is allowed.

## Canonical Gates

### Routing Gate

Chooses the intended output road: image, video, music/audio, text, mixed-media, or multiple outputs.

Complete when the artist chooses a target road or explicitly asks Artist OS to recommend one.

### Meaning Confirmation Gate

Confirms what the Reference means to the artist and what must survive transformation.

Complete when Artist Meaning, must-preserve details, may-transform details, avoid list, intended feeling, target medium/story-shape direction, and success criteria are captured through the Decision Interview or explicitly marked safe to proceed unconfirmed.

### Interpretation Gate

Confirms the cross-medium interpretation before Story or Medium planning hardens.

Complete when formal observations, Emotional Structure, Core Tension Pairs, Poetic Density notes, transformation constraints, and the intended audience feeling are coherent enough to proceed.

### Story Gate

Chooses the Story Mode: one compressed beat, beat pair, triptych, sequence, scene, arc, or world.

Complete when the artist selects, combines, revises, rejects, or explicitly allows an unconfirmed Story Mode to proceed.

When multiple Story Modes are plausible, ask one direct Decision Interview question with a recommended Story Mode before drafting the Beat Plan. Do not silently choose between single image, emotional arc, and series when more than one would preserve Artist Meaning.

### Story Approval Gate

Approves the Beat Plan before medium translation.

Complete when Story Mode, Beat Roles, intended feeling, tension movement, symbolic progression, and known open questions are accepted or explicitly waived.

The Beat Plan must include minimum tension criteria before Story Approval. These criteria define the minimum active tensions and adjacent-beat movement required for the work to create enough contrast.

### Medium Gate

Chooses how the approved Beat Plan becomes a medium-specific work.

Examples:

- image: Symbology, Presentation Mode, Style, Detail / Intensity,
- video: Format, Scene / Sequence, Shot Logic, Motion, Visual Style, Pacing / Transition,
- sound: Sound Work Type, Sonic Concept, Genre / Production, Tempo / Groove, Vocal / Lyric, Arrangement / Form,
- text: Writing Method, Text Form, Voice / Point Of View, Structure, Fidelity / Transformation,
- mixed media: Scope, Medium Selection, Role Assignment, Cross-Media Continuity, Production Order.

Complete when the medium-specific gates required for that output are selected, revised, rejected, or explicitly allowed to proceed unconfirmed.

At medium gates, present the strongest recommendation first, then ask for artist confirmation or correction. Avoid broad menus unless the artist asks to explore.

### Prompt Lock Gate

Approves final provider-neutral prompt plans or Text Generation Plans before generation, drafting, or export.

Complete when Prompt Critic Review findings are resolved or explicitly waived, and the artist approves the prompt plan or Text Generation Plan for dry-run completion, generation approval, or Draft Generation Approval.

### Prompt Branch Gate

Approves a Prompt Branch Set for curator batches, mass prompt exploration, or broad AI generation runs.

Complete when the artist accepts the branching goal, branch count, meaning kernel, axes allowed to vary, axes held constant, and minimum distinction rule. A Prompt Branch Set does not authorize provider-backed generation by itself; Generation Approval is still required per call or approved batch.

### Long-Work Checkpoint Gate

Approves or blocks a Long-Work Checkpoint inside a Cumulative Work.

Complete when the artist approves, revises, waives, or blocks the checkpoint decision. Checkpoints can be foundation, medium mapping, calibration, first part, interval, pre-completion, or completion checks. Store the artist-facing decision as a Gate Decision with `gate_type = "long_work_checkpoint"` and summarize it in the Long-Work Stewardship Record for resume state.

When Long-Work Readiness is `pending`, run the readiness pass before expansion. When Long-Work Readiness is `repair_before_expansion`, do not produce multiple downstream prompts, drafts, or outputs until the issue is repaired or the artist explicitly waives the block.

### Generation Approval Gate

Approves any provider-backed generation call, cost-bearing action, upload, or irreversible external action.

Complete only with explicit per-call artist approval. Approval for one call never implies approval for later calls.

### Output Acceptance Gate

Decides whether a drafted or generated output is accepted, revised, rejected, extended, archived, or exported.

Complete when Output Critic Review findings are resolved or waived and the artist chooses the next state.

## Review Execution Rule

All review stages are mandatory bounded sub-agent reviews.

The creating agent must not self-review its own Story, Medium, Prompt, or Output review stage. It must pass a narrow review packet to the reviewer sub-agent and apply blocking findings before advancing unless the artist explicitly waives the block.

Every critic and reviewer must check for drift. Drift means the artifact has moved away from the governing upstream material: the Reference, Artist Meaning, Transformation Brief, Beat Plan, Medium Plan, Prompt Plan, Text Generation Plan, or approved prior output. Reviewers should identify what the artifact drifted from, where the drift appears, whether it is harmful or artist-approved, and the smallest revision that restores alignment.

Reviewer sub-agents receive:

- review mode or critic role,
- artifact under review,
- Artist Meaning,
- Source Record or Reference summary when needed,
- Beat Plan when relevant,
- Medium Plan, Prompt Plan, or Text Generation Plan when relevant,
- open questions,
- desired output format.

Reviewer sub-agents return a Review Record that validates against `schemas/review-record.schema.json`.

If the host cannot spawn a sub-agent, the conductor may use a fallback separated review pass. The fallback must be clearly labeled, use only the same bounded review packet, keep `reviewer_execution.sub_agent_required: true`, and set `reviewer_execution.execution_mode: fallback_separated_pass`. This records that the sub-agent requirement still exists even though the host could not satisfy it.

The Review Record is the machine-readable output of the review stage. It must include:

- `review_record_id`,
- `project_id`,
- `review_role`,
- `reviewer_execution.execution_mode`: `bounded_sub_agent`, or `fallback_separated_pass` only when sub-agents are unavailable,
- `reviewer_execution.sub_agent_required: true`,
- `reviewer_execution.source_skill`,
- `artifact_under_review`,
- `upstream_context`,
- `matched`,
- `drifted`,
- `findings`,
- `recommended_revision`,
- `approval_status`: `approve`, `revise`, or `block`,
- `artist_waiver` when a waiver exists,
- `created_at`.

The reviewer may also return a revised brief, revision prompt, or taste memory note when the caller needs one, but that companion output never replaces the Review Record.

## Critic Roles

Critics strengthen the work without taking authority away from Artist Meaning.

### Meaning Reviewer

Checks whether a plan has drifted from the artist's stated meaning, constraints, or success criteria.

Use when later interpretation, story, medium translation, or output appears to override Artist Meaning.

### Story Critic

Checks meaning preservation, Story Mode scale, Beat Plan coherence, tension movement, symbolic continuity, and whether the Beat Plan should exist at this length.

Boundary: Story Critic owns meaning preservation, scale, arc, and symbolic progression. Beat Reviewer owns beat mechanics.

Drift check: compare the Beat Plan against the Reference, Artist Meaning, Transformation Brief, Emotional Structure, and must-preserve constraints.

Block when Beats name only facts, events, or symbols without an intended feeling, when a Beat lacks a real Expectation Turn, when the Beat Plan does not define minimum tension criteria, when a Beat falls below the required primary tension intensity, or when adjacent Beats in a sequence repeat the same tension profile without an artist-approved reason.

### Art Critic

Checks visual translation: Symbology Direction, Style Direction, Visual Dynamics, Shot Design, composition, image-role distinction, visual series coherence, and whether visual choices preserve Artist Meaning.

Drift check: compare visual choices against Artist Meaning, Beat Plan, Symbology Direction, Style Direction, Visual Dynamics, Shot Design, and Reference evidence. Flag style drift especially when style starts replacing meaning.

Block when the Symbology Gate was skipped without explicit permission, when the image plan expresses information but no clear feeling, when image roles do not translate the governing Expectation Turn, when the visual plan falls below its minimum tension criteria, when Shot Design defaults to repeated full-body framing without emotional need, or when a series repeats the same shot scale, camera angle, visual emphasis, composition, communication intent, or tension profile across adjacent image roles without an artist-approved reason.

### Video Critic

Checks video translation: format, scene progression, shot logic, motion, pacing, continuity, transitions, visual arc, and whether time-based choices preserve the Beat Plan.

Drift check: compare shot and motion choices against Artist Meaning, Beat Plan, Video Plan, Visual Style Direction, pacing intent, and approved prior frames or calibration clips.

### Sound Critic

Checks sound translation: Sonic Concept, Genre / Production, Tempo / Groove, Vocal / Lyric Policy, Arrangement / Form, Sonic Dynamics, lyrics when present, and platform readiness.

Drift check: compare sonic choices against Artist Meaning, Beat Plan, Sound Medium Plan, Sonic Concept, Arrangement Plan, Vocal / Lyric Policy, and source-language rights constraints. Flag genre drift when genre starts replacing meaning.

### Writing Critic

Checks written translation: form, voice, point of view, scene or section structure, prose/poetic pressure, continuity, pacing, and fidelity to Artist Meaning.

Writing Critic must use Fragment Reviewer, Beat Reviewer, or Shape Reviewer sub-agents when those method-specific concerns are present.

Drift check: compare written choices against Artist Meaning, source material, Beat Plan, Text Medium Plan, chosen voice, and the opening promise when using Writing Shape.

### Mixed-Media Critic

Checks whether selected media work together instead of duplicating, flattening, or accidentally contradicting each other.

It owns cross-media role assignment, continuity, divergence, and production order.

Drift check: compare each medium's role against Artist Meaning, Beat Plan, cross-media continuity decisions, and the other approved medium plans.

### Long-Work Reviewer

Checks Long-Work Stewardship for Cumulative Work: readiness before expansion, checkpoint status, part-to-part integrity, cumulative drift, continuity rules, proposed continuity updates, and whether a proposed change must return to Story Approval, Medium Plan approval, prompt revision, or artist confirmation.

Boundary: Long-Work Reviewer owns cumulative execution integrity, not Artist Meaning, Beat Plan authority, Medium Plan authority, or Output Acceptance.

Drift check: compare the Long-Work Stewardship Record and current part or output against Artist Meaning, Beat Plan, Medium Plan, active Long-Work Continuity Rules, approved prior parts, and relevant Output Records.

Block when Long-Work Readiness is `repair_before_expansion`, when a checkpoint required before continuing is unresolved, when a part resolves a later emotional movement too early, when adjacent parts repeat without an active meaning-bearing continuity rule, when a proposed continuity update changes meaning or story movement without returning to Story Approval, or when project memory would cross Artist OS Project boundaries without explicit artist import or reuse.

### Prompt Critic

Checks provider-neutral prompt quality, Text Generation Plan quality, traceability, variant distinctness, missing constraints, medium readiness, platform readiness, drafting readiness, and generation risks.

Drift check: compare prompt language or drafting instructions against Artist Meaning, Beat Plan, Medium Plan, review decisions, source-wording policy, and provider or drafting boundary constraints. Flag drift when fluent wording adds unsupported symbols, style, plot, lyrics, genre, camera logic, structure, voice, or emotional claims.

Block when a prompt or Text Generation Plan can render facts but does not direct the emotional effect, when it drops the approved Expectation Turn Translation, when it drops the approved Shot Design, when it drops approved text structure or source-wording policy, when it drops the approved minimum tension criteria, or when series prompts are visually different only by surface adjectives instead of shot scale, camera angle, composition, symbolic action, communication intent, and tension profile.

### Output Critic

Checks whether the drafted or generated output preserves Artist Meaning, Story Approval, Medium Plan, Prompt Plan or Text Generation Plan, and provenance.

Drift check: compare the output against Reference evidence, Artist Meaning, Beat Plan, Medium Plan, Prompt Plan or Text Generation Plan, approved variants, source-wording policy, and any prior accepted output in the same series.

## Writing Method Reviewers

The writing method reviewers are high-authority method reviewers, not general taste reviewers.

Their source methods live in:

- `docs/writing/references/writing-fragments.SKILL.md`
- `docs/writing/references/writing-beats.SKILL.md`
- `docs/writing/references/writing-shape.SKILL.md`

### Fragment Reviewer

Checks the `writing-fragments` method: raw material capture without premature structure.

Use when the source material is a fragment pile or when the artist is still developing raw material.

Drift check: compare captured fragments against the artist's actual language and source material. Flag cleaned-up fragments that lose the original noticing.

### Beat Reviewer

Checks the `writing-beats` method: one move per beat, meaningful pivots, no glued-together beats, no false endings, and no locked-ahead journey without approval.

Use for multi-beat Story Plans, image series, video scenes/sequences, sound arrangements, lyric-bearing plans, mixed-media beat assignment, and journey-shaped text.

Drift check: compare each beat against the previous beat, the chosen journey path, Artist Meaning, and source material. Flag beats that pivot because they are interesting rather than because the journey earned them.

### Shape Reviewer

Checks the `writing-shape` method: opening promise, paragraph-by-paragraph necessity, format choices, transitions, missing examples, and reader-facing coherence.

Use for articles, essays, artist statements, treatments, scripts, release copy, and other finished written artifacts.

Drift check: compare each paragraph or block against the chosen opening, source pile, and article promise. Flag sections that drift to a different thesis without deliberately changing the opening.

## Blocking Findings

A reviewer returns `block` when proceeding would violate Artist Meaning, provider boundaries, provenance, story approval, method authority, or medium readiness.

Unapproved harmful drift is a blocking finding when it changes Artist Meaning, breaks must-preserve constraints, invents unsupported material, violates rights constraints, or makes the output target a different work than the one approved.

Only the artist can waive a blocking finding. If waived, record the waiver in the project event log with the reason.
