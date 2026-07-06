# Text Journey

The Text Journey translates an approved Beat Plan into a written work. It can preserve the Reference closely, transform it into a new form, or use the Beat Plan as the structure for a different kind of writing.

## Best Fit

Use the Text Journey when the final work should be:

- a poem,
- a monologue,
- a prose scene,
- a short story,
- an article,
- lyrics,
- a script,
- a letter,
- a manifesto,
- a narrative treatment,
- a rewritten or transformed version of the original text.

## Route

```text
Approved Beat Plan with Project-Level Workflow Scale Routing
  -> Long-Work Stewardship Activation Gate, when recommended or artist-requested
  -> Long-Work Stewardship Record, when activated by the artist
  -> Research Grounding Gate, when timely or public-facing work may need current evidence
  -> Writing Method Gate
  -> Medium Output Shape Recommendation
  -> Medium-Level Workflow Scale Routing
  -> Medium Output Shape Conflict Decision, when needed
  -> Cultural Format Structure selection, when relevant
  -> Format Length Standard application, with override gate only when needed
  -> Text Form Gate
  -> Voice / Point Of View Gate
  -> Structure Gate
  -> Fidelity / Transformation Gate
  -> Text Medium Plan
  -> Draft Text Creative Brief
  -> Writing Critic Review
  -> Brief Approval
  -> Text Generation Plan
  -> Prompt Critic Review
  -> Prompt Lock Gate
  -> Review Presentation Gate
  -> Draft Generation Approval Gate
  -> Fresh-Context Drafting Pass
  -> Main-Agent Conformance Review
  -> Clear Writing Pass, when appropriate
  -> Human Voice Pass, when appropriate
  -> Main-Agent Final Check
  -> Output Critic Review
  -> Output Acceptance Gate
```

## Gates

- Research Grounding Gate: should the agent do online research or use artist-provided sources before the piece's argument, examples, or audience promise harden?
- Writing Method Gate: fragments, beats, shape, or a hybrid sequence?
- Medium Output Shape Recommendation: what text shape best preserves the approved Beat Plan and adapted Story Structure?
- Medium Output Shape Conflict Decision: if the artist-requested shape and recommended shape materially diverge, should the plan keep the requested shape, accept the recommendation, revise the shape, or proceed unconfirmed?
- Cultural Format Structure selection: what culturally recognized form grammar, Audience Hook, parts, payoff, and adaptation policy should shape the accepted text form?
- Format Length Standard: what target word-count range should this format use, and does the artist need to override it?
- Text Form Gate: poem, article, monologue, prose scene, script, lyrics, essay, letter, treatment, or other form?
- Voice / Point Of View Gate: who speaks, from what distance, and with what authority?
- Structure Gate: fragment, scene, sequence, arc, chapters, sections, verses, or hybrid?
- Fidelity / Transformation Gate: preserve source wording, adapt it, invert it, expand it, compress it, translate it, or create a new work from the approved Beat Plan?
- Publication / Use Gate: private draft, performance text, lyrics, social post, book fragment, prompt source, or other use?
- Review Presentation Gate: should Artist OS produce Markdown only, a local HTML mockup, or both for human review?

Ask the Research Grounding question for public-facing, timely, factual, trend-aware, or platform-native work such as articles, explainers, op-eds, trend analysis, LinkedIn posts, service writing, thought leadership, and launch copy. Recommend research when current facts, market context, platform discourse, examples, statistics, or recent developments would materially improve the piece. Recommend skipping it when the work should stay personal, timeless, private, poetic, or source-bound. If accepted, browse only within the agreed scope and summarize source dates before using the research.

Apply Format Length Standards automatically from `docs/structure-library/cultural-format/README.md` after Cultural Format Structure and publication use are known. Record the target range in `TextMediumPlan.length_policy` and carry it into `TextGenerationPlan.length_policy`. Ask the artist only when the default conflicts with their request, the assignment specifies a length, or the agent recommends an override. Drafting and editorial passes should treat the range as a reviewable target, not as a reason to damage Artist Meaning, structure, or voice.

Ask the Review Presentation question for written format outputs. Recommend a local HTML mockup when the piece benefits from layout, reading flow, hierarchy, or scanning review; recommend Markdown-only when the artist wants raw text. If accepted, create the HTML only after a concrete draft exists, store it as a review presentation artifact, and keep the drafted written Output Artifact canonical.

## Reviews

- Story Critic Review happens before this journey as a bounded sub-agent review.
- Writing Critic Review checks form, voice, point of view, structure, pacing, line or paragraph pressure, continuity, and fidelity to Artist Meaning as a bounded sub-agent review.
- Fragment Reviewer sub-agent checks raw material capture against `docs/writing/references/writing-fragments.SKILL.md`.
- Beat Reviewer sub-agent checks journey movement against `docs/writing/references/writing-beats.SKILL.md`.
- Shape Reviewer sub-agent checks reader-facing structure against `docs/writing/references/writing-shape.SKILL.md`.
- Prompt Critic Review checks generation instructions, missing constraints, tone drift, rights-sensitive language reuse, and revision readiness as a bounded sub-agent review.
- Output Critic Review checks the written draft against Artist Meaning, Beat Plan, Text Medium Plan, and any source-wording constraints as a bounded sub-agent review.
- Long-Work Reviewer checks readiness, first-part or interval checkpoints, cumulative drift, voice/fidelity continuity, premature resolution, and proposed continuity updates when cumulative or full long-form text support is active.

## Drafting Boundary

Text Medium Plans, Text Creative Briefs, and Text Generation Plans may be drafted automatically once their upstream approvals are complete. Producing the actual written Output Artifact requires Draft Generation Approval, even when the agent drafts it locally without a paid provider call.

After Draft Generation Approval, draft the written Output Artifact in a fresh-context sub-agent using a bounded Text Draft Packet. The Text Draft Packet is an internal handoff template assembled from approved records; do not persist it as a separate schema-backed record. The sub-agent must return the draft plus a compact draft trace mapping each section to the source Beat or structure role, Intended Feeling, and key constraint preserved. Persist the compact draft trace in the Output Record `traceability_summary`; do not create a separate Draft Trace record. The drafting sub-agent must not run the Human Voice Pass during first drafting. The main agent then performs a conformance review against the approved Artist Meaning, Text Medium Plan, Text Creative Brief, Text Generation Plan, source-wording policy, and structure before any Human Voice Pass or Output Critic Review.

Create an Output Record for every concrete draft or rewrite artifact that could be reviewed, compared, accepted, or rolled back. The fresh-context draft, Clear Writing rewrite, Human Voice rewrite, and any human-edited version each receive their own Output Record linked to the prior artifact. Rewrite Output Records preserve the original draft trace in `traceability_summary` and add compact rewrite trace notes naming what changed, which pass policy authorized it, which protected features were preserved, and which prior Output Record was rewritten.

If the draft has strong prose but fails the approved structure, section jobs, Intended Feeling, source-wording policy, or other Text Generation Plan constraints, structure wins. Do not run the Human Voice Pass to rescue it. Send a tight correction packet back to a fresh-context drafting pass or revise the governing plan if the artist explicitly changes direction.

After a written Output Artifact exists, run a Clear Writing Pass when the Text Generation Plan requires or recommends it, then run a Human Voice Pass by default unless the Text Generation Plan marks it optional or skipped for form-sensitive reasons. Run each editorial pass in a bounded fresh-context sub-agent with only the current artifact text, the relevant pass skill and references, the Text Generation Plan policy for that pass, protected features, necessary Artist Meaning or brief constraints, and explicit do-not-change rules. The default order is Clear Writing Pass before Human Voice Pass, because clarity edits can make prose feel more generic and the Human Voice Pass can restore natural rhythm afterward. The Text Generation Plan may reverse or skip either pass when the form requires it.

After editorial passes, the main agent performs a final check against Artist Meaning, Text Medium Plan, Text Creative Brief, Text Generation Plan, source-wording policy, protected features, and structure before Output Critic Review.

For long text where Workflow Scale Routing identifies cumulative or full long-form support, create a foundation Long-Work Stewardship Record after Story Approval and enrich it after the Text Medium Plan maps Beats to text sections or other medium parts. The Text Medium Plan owns Medium-Level Workflow Scale Routing, Medium Output Shape Recommendation, Cultural Format Structure, text form, voice, structure, fidelity, publication use, and section jobs; the stewardship record references text section or chapter ids and tracks cumulative progress, readiness, checkpoints, continuity rules, and drift.

Plot-tracker-style documents, act trackers, open-thread lists, and character continuity summaries are Stewardship Views over Text Medium Plan and Long-Work Stewardship state. They are not separate story-authority records.

The Text Generation Plan must set `human_voice_pass_policy` to `required`, `recommended`, `optional`, or `skip`, with `degree` set to `light`, `standard`, or `deep` when the pass is not skipped. It must also name protected features such as line breaks, character voice, source wording, rhetoric, meter, repetition, formal tone, or deliberate artificiality.

The Text Generation Plan must include the accepted `length_policy` and `review_presentation` decision. The drafting packet should tell the fresh-context drafter the target word count and acceptable range; the conformance review should flag drafts that miss the range materially unless the miss is justified by Artist Meaning or an artist-approved override.

A Clear Writing Pass is separate from the Human Voice Pass. The Text Generation Plan must decide whether the Clear Writing Pass is required, recommended, optional, or skipped for the specific text form. Apply `skills/artist-os/references/clear-writing-pass.md` for direct explanatory, professional, public-facing, or reader-guidance prose; avoid applying it blindly to poems, lyrics, dialogue, manifestos, experimental prose, or source-preserving adaptations where compression or plainness would damage the intended form.

## Writing Methods

Artist OS uses three high-authority writing references:

- `writing-fragments`: mine raw material without imposing structure.
- `writing-beats`: assemble a journey one beat at a time.
- `writing-shape`: turn a pile into a finished article or structured written piece.

Use the smallest method that matches the work:

- If the artist has scattered ideas, start with fragments.
- If the piece wants sequence, pivots, scenes, or experiential movement, use beats.
- If the piece wants a finished reader-facing argument, article, statement, or treatment, use shape.

When using `shape`, produce the Medium Output Shape Recommendation before locking Primary Text Form, then select or adapt the Cultural Format Structure for the accepted shape. Map Cultural Format Structure parts to `structure_plan.sections`; do not let the format parts replace section jobs, Intended Feeling, or Expectation Turn translation.

Keep these levels distinct:

- Cultural Format Structure `function`: the audience-facing job of a recognizable format part, such as hook, reveal, why-now, turn, payoff, or close.
- Section `structure_role`: the local position or role of one Text Medium Plan section inside the accepted form.
- Section `section_job`: the concrete drafting instruction for that section, including what it must do with Artist Meaning, Intended Feeling, and Expectation Turn translation.

The current Text schemas are conservative. Refine them through rehearsals only when beats, form, cultural format structure, section shape, narrative pressure, or writing-specific review criteria reveal a real gap.

Orientation may capture the artist's early fidelity preference. The Text Medium Plan owns the durable fidelity policy; if Orientation already answered it clearly, carry that answer forward without re-asking.
