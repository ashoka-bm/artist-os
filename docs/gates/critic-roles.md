# Critic Roles And Writing Method Reviewers

## Critic Roles

Critics strengthen the work without taking authority away from Artist Meaning.

### Meaning Reviewer

Checks whether a plan has drifted from the artist's stated meaning, constraints, or success criteria.

Use when later interpretation, story, medium translation, or output appears to override Artist Meaning.

### Story Critic

Checks meaning preservation, Story Mode scale, Beat Plan coherence, Beat size, tension movement, symbolic continuity, and whether the Beat Plan should exist at this length.

Boundary: Story Critic owns the Story Approval contract. It decides whether the Beat Plan preserves Artist Meaning, uses the right Story Mode scale, carries enough arc or sequence logic, keeps symbolic progression coherent, keeps Story Movements separate from Beats, and defines minimum tension criteria strong enough for downstream medium work. It does not replace the Beat Reviewer when individual beat mechanics need method review.

Use Story Critic when Story Mode, length, meaning preservation, symbolic progression, Story Movement grouping, or Beat Plan authority is uncertain, or when a proposed later change would alter Story Approval. Use Beat Reviewer when the question is whether each Beat performs one smallest meaningful move, pivots cleanly, earns its turn, differs from adjacent Beats, and avoids false endings or locked-ahead journeys. When both are needed, run Beat Reviewer first, then have Story Critic consume that Review Record before Story Approval.

Drift check: compare the Beat Plan against the Reference, Artist Meaning, Transformation Brief, Emotional Structure, and must-preserve constraints.

Block when Beats name only facts, events, or symbols without an intended feeling, when a Beat lacks a real Expectation Turn, when a Beat is actually a glued-together Story Movement doing several independent jobs, when the Beat Plan does not define minimum tension criteria, when a Beat falls below the required primary tension intensity, or when adjacent Beats in a sequence repeat the same tension profile without an artist-approved reason.

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

The Long-Work Reviewer cannot activate Long-Work Stewardship, record an activation, or waive a missing activation. It may recommend activation, block unsafe expansion, or require the conductor to present the Long-Work Stewardship Activation Gate again when a deferred or waived project reaches a concrete continuity-risk point.

For active stewardship, the Long-Work Reviewer owns the Medium Mapping Checkpoint review before the artist sees the concise part map. The normal Medium Critic still owns medium-specific artistic strength and brief review. Clean routine checkpoints may pass automatically; the reviewer should require an artist-facing gate only when the checkpoint blocks, proposes a continuity or story-authority change, needs a waiver, or reviews the initial map for multiple dependent parts.

Drift check: compare the Long-Work Stewardship Record and current part or output against Artist Meaning, Beat Plan, Medium Plan, active Long-Work Continuity Rules, approved prior parts, and relevant Output Records.

Block when a recommended activation is unresolved before dependent bulk expansion, when active stewardship has multiple dependent parts and the initial Medium Mapping Checkpoint is unresolved, when Long-Work Readiness is `repair_before_expansion`, when a checkpoint required before continuing is unresolved, when a part resolves a later emotional movement too early, when adjacent parts repeat without an active meaning-bearing continuity rule, when a proposed continuity update changes meaning or story movement without returning to Story Approval, or when project memory would cross Artist OS Project boundaries without explicit artist import or reuse.

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

Checks the `writing-beats` method: each beat is the smallest meaningful movement, one move per beat, meaningful pivots, no glued-together beats, no Story Movement mislabeled as a Beat, no false endings, and no locked-ahead journey without approval.

Use for multi-beat Story Plans, image series, video scenes/sequences, sound arrangements, lyric-bearing plans, mixed-media beat assignment, and journey-shaped text.

Drift check: compare each beat against the previous beat, the chosen journey path, Artist Meaning, and source material. Flag beats that pivot because they are interesting rather than because the journey earned them. Block when a candidate Beat contains multiple causal or emotional jobs that should be split before Story Approval.

### Shape Reviewer

Checks the `writing-shape` method: opening promise, paragraph-by-paragraph necessity, format choices, transitions, missing examples, and reader-facing coherence.

Use for articles, essays, artist statements, treatments, scripts, release copy, and other finished written artifacts.

Drift check: compare each paragraph or block against the chosen opening, source pile, and article promise. Flag sections that drift to a different thesis without deliberately changing the opening.
