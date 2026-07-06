# Canonical Gates

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

### Long-Work Stewardship Activation Gate

Chooses whether to activate Long-Work Stewardship when Artist OS recommends it or the artist asks for it. This is a separate artist-facing pause immediately after Story Approval and before Medium Plan expansion.

Complete when the artist activates, defers, waives, or deactivates Long-Work Stewardship. Activation creates the foundation Long-Work Stewardship Record immediately. Defer and waive create Gate Decisions only; they do not create placeholder stewardship records. Waiving a recommended activation is a risky waiver, but no artist-authored reason is required.

Use shared core wording with one medium-specific sentence. Core wording:

> This is starting to behave like a longer work, where later parts will need to remember what earlier parts set up. I recommend activating Long-Work Stewardship. It gives the project a lightweight memory: what each part is meant to carry, what must stay consistent, what should not resolve too early, and where we should pause to check the arc. It adds a little structure, but it helps protect the feeling and continuity of the work as it grows.
>
> Do you want to activate it now?

Offer exactly: Activate, Defer, Waive and continue. Clear agreement activates. Ambiguous soft agreement defers. Explicit refusal waives. If the artist requested stewardship below the normal threshold, record that it was artist-requested rather than system-required.

If active stewardship later proves unnecessary because the Medium Plan is compact, ask for lightweight confirmation to deactivate it as unnecessary, record the decision through this gate type, mark the stewardship record superseded, and continue with the compact flow.

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

For the Video Format Gate, the recommendation must include the story type and Beat Plan shape before the artist is asked to choose. State what the story is, how many smallest Story Beats or Story Movements it appears to need, the recommended video format, and why that format fits better than nearby alternatives. Do not start with a broad video format menu when the Reference or Beat Plan gives enough material to recommend.

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

Handles artist-facing decisions from a Long-Work Checkpoint inside active stewardship.

Once Long-Work Stewardship is active, checkpoint creation and clean checkpoint passes are automatic. A clean pass may be summarized with a short status line such as "Continuity checkpoint passed." Do not ask the artist to approve routine process mechanics.

Complete when a checkpoint requires an artist-facing decision and the artist approves, revises, waives, or blocks that decision. Artist-facing checkpoint decisions are required when the checkpoint blocks, proposes a continuity or story-authority change, needs a waiver to continue, or when the initial Medium Mapping Checkpoint maps an active stewardship project into multiple dependent parts.

The initial Medium Mapping Checkpoint is artist-facing only when the Medium Plan creates multiple dependent parts. Run Long-Work Reviewer first, present the revised concise part map, and ask whether the longer work is unfolding correctly before bulk expansion. The artist may approve, revise, or explicitly waive this mapping review. A waiver affects only that checkpoint; stewardship remains active.

Store artist-facing checkpoint decisions as Gate Decisions with `gate_type = "long_work_checkpoint"` and summarize them in the Long-Work Stewardship Record for resume state.

When Long-Work Readiness is `pending`, run the readiness pass before expansion. When Long-Work Readiness is `repair_before_expansion`, do not produce multiple downstream prompts, drafts, or outputs until the issue is repaired or the artist explicitly waives the block.

Before the initial Medium Mapping Checkpoint is approved or waived, Artist OS may create one clearly labeled calibration or sample part if it helps the artist judge direction. It must not expand multiple dependent parts. Existing approval gates still apply: dry-run sample plans need no new approval, text draft samples need Draft Generation Approval, and provider-backed media samples need Generation Approval.

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
