# Gates And Reviews

This is the canonical Artist OS contract for gates, critic roles, reviewer roles, and review execution.

Use this file before adding or changing a journey. Medium-specific docs can add local gates, but shared gate order and review rules live here.

## Shared Gate Order

The default cross-medium journey uses this gate order:

```text
Routing Gate
  -> Meaning Confirmation Gate
  -> Research Grounding Gate, when timely or public-facing work may need current evidence
  -> Interpretation Gate
  -> Story Gate
  -> Story Critic Review
  -> Story Approval Gate
  -> Long-Work Readiness / Checkpoints, when the work is cumulative
  -> Medium Gates
  -> Format Length Gate, when the artist overrides the default length standard
  -> Medium Critic Review
  -> Brief Approval Gate
  -> Prompt Critic Review
  -> Prompt Branch Gate, when curator batches are requested
  -> Prompt Lock Gate
  -> Review Presentation Gate, for written Output Artifacts
  -> Generation Approval Gate, or Draft Generation Approval Gate for text drafting
  -> Output Critic Review
  -> Output Acceptance Gate
```

Provider-backed generation always requires explicit approval. Drafting briefs, boards, prompt plans, lyrics, scripts, shot lists, comparison boards, or other dry-run artifacts is allowed.

## Gate Completion Rule

A gate is complete, an approval given, a waiver granted, or an option selected only when it comes from an explicit artist turn: an actual artist response in the conversation. The agent must not infer approval from silence, treat its own recommendation as the artist's answer, self-approve, or assume the artist would obviously want a choice. "Obvious," "low-risk," "trivial," or "an obvious fix" does not waive this requirement. An obvious choice is still the artist's choice.

Recording a Gate Decision, approval, selection, or waiver the artist did not actually make is forbidden. It fabricates provenance and breaks the audit trail that every downstream record inherits.

This rule applies to every gate in this document, including Brief Approval, Series/Sequence approval, Generation Approval, Draft Generation Approval, and blocking-finding waivers.

## Continuation Rule

After an explicit artist turn completes a gate, answers a Decision Interview question, or corrects a project detail, the agent must not stop with only acknowledgement or persistence status. It must either:

- continue immediately into the next unlocked pipeline step, or
- ask the next concrete required gate or Decision Interview question when artist input is still the blocker.

This is especially important for small confirmations and corrections such as spelling, terminology, rights policy, genre, vocal mode, calibration details, or approval of a recommended answer. Recording the answer is required, but recording alone is not a complete artist-facing turn. The artist should never have to ask "what is next?" to recover the workflow.

## Canonical Gates

### Routing Gate

Chooses the intended output road: image, video, music/audio, text, mixed-media, or multiple outputs.

Complete when the artist chooses a target road or explicitly asks Artist OS to recommend one.

### Meaning Confirmation Gate

Confirms what the Reference means to the artist and what must survive transformation.

Complete when Artist Meaning, must-preserve details, may-transform details, avoid list, intended feeling, target medium/story-shape direction, and success criteria are captured through the Decision Interview or explicitly marked safe to proceed unconfirmed.

### Research Grounding Gate

Offers online research or artist-provided source grounding before public-facing, timely, factual, trend-aware, or platform-native text hardens into an argument, audience promise, examples, or claims.

Complete when the artist accepts research, declines research, provides source material instead, or explicitly allows the piece to proceed unresearched. When asking, recommend research if current facts, market context, platform discourse, examples, statistics, or recent developments would materially strengthen the work; recommend skipping it if the work should stay personal, timeless, private, poetic, or source-bound.

If accepted, the research scope must be concrete enough to browse: topic, audience, geography or market when relevant, recency expectations when relevant, and source preferences or exclusions when relevant. The agent must summarize the sources and dates used, separate sourced facts from interpretation, and keep research subordinate to Artist Meaning. Do not silently browse or insert current factual claims when this gate is unresolved.

### Interpretation Gate

Confirms the cross-medium interpretation before Story or Medium planning hardens.

Complete when formal observations, Emotional Structure, Core Tension Pairs, Poetic Density notes, transformation constraints, and the intended audience feeling are coherent enough to proceed.

### Story Gate

Chooses the Story Mode: one compressed beat, beat pair, three-part sequence, sequence, scene, arc, or world.

Complete when the artist selects, combines, revises, rejects, or explicitly allows an unconfirmed Story Mode to proceed.

When multiple Story Modes are plausible, ask one direct Decision Interview question with a recommended Story Mode before drafting the Beat Plan. Do not silently choose between single image, compressed arc, and image series when more than one would preserve Artist Meaning.

### Story Approval Gate

Approves the Beat Plan before medium translation.

Complete when Story Mode, Beat Roles, intended feeling, tension movement, symbolic progression, and known open questions are accepted or explicitly waived.

The Beat Plan must include minimum tension criteria before Story Approval. These criteria define the minimum active tensions and adjacent-beat movement required for the work to create enough contrast.

### Medium Gate

Chooses how the approved Beat Plan becomes a medium-specific work.

Examples:

- image: Symbology, Presentation Mode, Style,
- video: Format, Scene / Sequence, Shot Logic, Motion, Visual Style, Pacing / Transition,
- sound: Sound Work Type, Sonic Concept, Genre / Production, Tempo / Groove, Vocal / Lyric, Arrangement / Form,
- text: Writing Method, Format Length when overridden, Text Form, Voice / Point Of View, Structure, Fidelity / Transformation, Review Presentation,
- mixed media: Scope, Medium Selection, Role Assignment, Cross-Media Continuity, Production Order.

Complete when the medium-specific gates required for that output are selected, revised, rejected, or explicitly allowed to proceed unconfirmed.

At medium gates, present the strongest recommendation first, then ask for artist confirmation or correction. Avoid broad menus unless the artist asks to explore.

### Format Length Gate

Confirms or overrides the Format Length Standard when the artist wants a different word count than the default for the selected Cultural Format Structure and publication use.

Complete when the Text Medium Plan applies the default Format Length Standard, or when the artist explicitly sets a different target, range, or flexibility. The agent should not ask this gate by default when the standard clearly fits; it should state the applied target briefly and continue. Ask only when the artist names a length, the assignment or platform implies a different length, the format standard conflicts with Artist Meaning, or the recommended shape would be harmed by the default.

When overridden, store the override in `length_policy.artist_override` and record a Gate Decision with `gate_type = "format_length"`.

### Brief Approval Gate

Approves the medium-specific Creative Brief Document after the Medium Critic Review has revised it, before any Creative Brief Record, Prompt Plan, or Text Generation Plan is created. The brief is the meaning contract everything downstream inherits, so it must be ratified before a plan is locked on top of it.

Complete when the artist accepts the revised brief, or revises it and re-approves. On changes, re-run the critic only for the affected areas. Store the decision as a Gate Decision with `gate_type = "brief_approval"`.

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

### Draft Generation Approval Gate

Approves locally drafting a written Output Artifact from an approved Text Generation Plan, even when no paid provider call is made. This is distinct from the Generation Approval Gate: it governs the Text Journey's drafting step, not a cost-bearing provider call or other irreversible external action.

Complete with explicit artist approval to draft. Store the decision as a Gate Decision with `gate_type = "draft_generation_approval"`.

### Review Presentation Gate

Chooses how the artist wants to review a drafted written Output Artifact: Markdown, a local HTML mockup, or both.

Complete when the artist accepts or declines an HTML mockup. Ask this for written format outputs before Draft Generation Approval or before the first concrete draft is created. Recommend HTML mockup for articles, op-eds, LinkedIn-style posts, newsletters, essays, speeches, pitch pages, artist statements, and other written pieces where layout, scanning, or reading flow affects review. Recommend Markdown-only for tiny notes, source-bound private drafts, or cases where the artist only wants raw text.

Creating a local HTML mockup is allowed after the draft exists and does not require provider-backed generation approval. It must not publish, upload, or replace the canonical written Output Artifact. Store the decision as a Gate Decision with `gate_type = "review_presentation"` and carry it into the Text Generation Plan's `review_presentation`.

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
- `emotional_tension_review`,
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

Boundary: Story Critic owns the Story Approval contract. It decides whether the Beat Plan preserves Artist Meaning, uses the right Story Mode scale, carries enough arc or sequence logic, keeps symbolic progression coherent, and defines minimum tension criteria strong enough for downstream medium work. It does not replace the Beat Reviewer when individual beat mechanics need method review.

Use Story Critic when Story Mode, length, meaning preservation, symbolic progression, or Beat Plan authority is uncertain, or when a proposed later change would alter Story Approval. Use Beat Reviewer when the question is whether each beat performs one meaningful move, pivots cleanly, earns its turn, differs from adjacent beats, and avoids false endings or locked-ahead journeys. When both are needed, run Beat Reviewer first, then have Story Critic consume that Review Record before Story Approval.

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
