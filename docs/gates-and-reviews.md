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

Complete when Artist Meaning, must-preserve details, may-transform details, avoid list, and success criteria are captured or explicitly marked safe to proceed unconfirmed.

### Interpretation Gate

Confirms the cross-medium interpretation before Story or Medium planning hardens.

Complete when formal observations, Emotional Structure, Core Tension Pairs, Poetic Density notes, and transformation constraints are coherent enough to proceed.

### Story Gate

Chooses the Story Mode: one compressed beat, beat pair, triptych, sequence, scene, arc, or world.

Complete when the artist selects, combines, revises, rejects, or explicitly allows an unconfirmed Story Mode to proceed.

### Story Approval Gate

Approves the Beat Plan before medium translation.

Complete when Story Mode, Beat Roles, tension movement, symbolic progression, and known open questions are accepted or explicitly waived.

### Medium Gate

Chooses how the approved Beat Plan becomes a medium-specific work.

Examples:

- image: Symbology, Presentation Mode, Style, Detail / Intensity,
- video: Format, Scene / Sequence, Shot Logic, Motion, Visual Style, Pacing / Transition,
- sound: Sound Work Type, Sonic Concept, Genre / Production, Tempo / Groove, Vocal / Lyric, Arrangement / Form,
- text: Writing Method, Text Form, Voice / Point Of View, Structure, Fidelity / Transformation,
- mixed media: Scope, Medium Selection, Role Assignment, Cross-Media Continuity, Production Order.

Complete when the medium-specific gates required for that output are selected, revised, rejected, or explicitly allowed to proceed unconfirmed.

### Prompt Lock Gate

Approves final provider-neutral prompt plans before generation or export.

Complete when Prompt Critic Review findings are resolved or explicitly waived, and the artist approves the prompt plan for dry-run completion or generation approval.

### Prompt Branch Gate

Approves a Prompt Branch Set for curator batches, mass prompt exploration, or broad AI generation runs.

Complete when the artist accepts the branching goal, branch count, meaning kernel, axes allowed to vary, axes held constant, and minimum distinction rule. A Prompt Branch Set does not authorize provider-backed generation by itself; Generation Approval is still required per call or approved batch.

### Generation Approval Gate

Approves any provider-backed generation call, cost-bearing action, upload, or irreversible external action.

Complete only with explicit per-call artist approval. Approval for one call never implies approval for later calls.

### Output Acceptance Gate

Decides whether a drafted or generated output is accepted, revised, rejected, extended, archived, or exported.

Complete when Output Critic Review findings are resolved or waived and the artist chooses the next state.

## Review Execution Rule

All review stages are mandatory bounded sub-agent reviews.

The creating agent must not self-review its own Story, Medium, Prompt, or Output review stage. It must pass a narrow review packet to the reviewer sub-agent and apply blocking findings before advancing unless the artist explicitly waives the block.

Every critic and reviewer must check for drift. Drift means the artifact has moved away from the governing upstream material: the Reference, Artist Meaning, Transformation Brief, Beat Plan, Medium Plan, Prompt Plan, or approved prior output. Reviewers should identify what the artifact drifted from, where the drift appears, whether it is harmful or artist-approved, and the smallest revision that restores alignment.

Reviewer sub-agents receive:

- review mode or critic role,
- artifact under review,
- Artist Meaning,
- Source Record or Reference summary when needed,
- Beat Plan or Beat Map when relevant,
- Medium Plan or Prompt Plan when relevant,
- open questions,
- desired output format.

Reviewer sub-agents return a Review Record that validates against `schemas/review-record.schema.json`.

The Review Record is the machine-readable output of the review stage. It must include:

- `review_record_id`,
- `project_id`,
- `review_role`,
- `reviewer_execution.execution_mode: bounded_sub_agent`,
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

### Art Critic

Checks visual translation: Symbology Direction, Style Direction, Visual Dynamics, composition, image-role distinction, visual series coherence, and whether visual choices preserve Artist Meaning.

Drift check: compare visual choices against Artist Meaning, Beat Plan, Symbology Direction, Style Direction, Visual Dynamics, and Reference evidence. Flag style drift especially when style starts replacing meaning.

### Video Critic

Checks video translation: format, scene progression, shot logic, motion, pacing, continuity, transitions, visual arc, and whether time-based choices preserve the Beat Plan.

Drift check: compare shot and motion choices against Artist Meaning, Beat Plan, Video Plan, Visual Style Direction, pacing intent, and approved prior frames or calibration clips.

### Sound Critic

Checks sound translation: Sonic Concept, Genre / Production, Tempo / Groove, Vocal / Lyric Policy, Arrangement / Form, Sonic Dynamics, lyrics when present, and platform readiness.

Drift check: compare sonic choices against Artist Meaning, Beat Plan, Sound Plan, Sonic Concept, Arrangement Plan, Vocal / Lyric Policy, and source-language rights constraints. Flag genre drift when genre starts replacing meaning.

### Writing Critic

Checks written translation: form, voice, point of view, scene or section structure, prose/poetic pressure, continuity, pacing, and fidelity to Artist Meaning.

Writing Critic must use Fragment Reviewer, Beat Reviewer, or Shape Reviewer sub-agents when those method-specific concerns are present.

Drift check: compare written choices against Artist Meaning, source material, Beat Plan, Text Plan, chosen voice, and the opening promise when using Writing Shape.

### Mixed-Media Critic

Checks whether selected media work together instead of duplicating, flattening, or accidentally contradicting each other.

It owns cross-media role assignment, continuity, divergence, and production order.

Drift check: compare each medium's role against Artist Meaning, Beat Plan, cross-media continuity decisions, and the other approved medium plans.

### Prompt Critic

Checks provider-neutral prompt quality, traceability, variant distinctness, missing constraints, medium readiness, platform readiness, and generation risks.

Drift check: compare prompt language against Artist Meaning, Beat Plan, Medium Plan, review decisions, and provider boundary constraints. Flag prompt drift when fluent prompt wording adds unsupported symbols, style, plot, lyrics, genre, camera logic, or emotional claims.

### Output Critic

Checks whether the drafted or generated output preserves Artist Meaning, Story Approval, Medium Plan, Prompt Plan, and provenance.

Drift check: compare the output against Reference evidence, Artist Meaning, Beat Plan, Medium Plan, Prompt Plan, approved variants, and any prior accepted output in the same series.

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
