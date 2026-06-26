# Video Template Research Draft Space

This draft space separates video story structure from output format and provider export.

The current rule is:

1. Story template first.
2. Format template second.
3. Provider export last.

Provider notes can improve execution, but they do not decide the audience journey.

## Layers

- `story-templates/`: reusable audience journeys such as hook, reframe, payoff, proof, and move.
- `micro-journey-template-chooser.md`: draft chooser for compact hook-to-payoff video journeys that do not need full Story Structure.
- `utility-sequence-templates/`: draft functional asset patterns for `utility_sequence` cases.
- `cultural-format-structures/`: draft video-specific audience-facing format grammars.
- `direction-notes/`: reusable craft guidance such as hook/payoff rules, on-camera delivery, moment embodiment, edit cut vocabulary, cinematic coverage, continuity, and provider limits.
- `format-templates/`: containers such as talking head, b-roll, documentary montage, motion graphics, UGC, fashion, and animation.
- `provider-exports/`: final platform renderings such as Seedance 2 prompt guidance.
- `references/`: source manifest and analysis notes for template references.
- `decisions/`: draft decisions made during template-flow grilling.
- `grids/`: comparison tables that show how the layers combine.
- `walkthroughs/`: sample packets used to test the draft routing on concrete video requests.
- `walkthrough-findings.md`: consolidated findings from the current walkthrough set.
- `revisit-notes.md`: follow-up items that should be reconsidered before promotion.

## Research-Backed Draft Libraries

The current research-backed expansion is:

- [Story Template Library](story-templates/research-backed-story-template-library.md)
- [Utility Sequence Template Library](utility-sequence-templates/research-backed-utility-sequence-library.md)
- [Video Cultural Format Structure Library](cultural-format-structures/research-backed-video-format-library.md)
- [Video Template Chooser Grid](grids/video-template-chooser-grid.md)
- [Template Grid Sample Routing](walkthroughs/template-grid-sample-routing.md)
- [Walkthrough Findings](walkthrough-findings.md)
- [Reference Insight Traceability](reference-insight-traceability.md)
- [Research Thread Synthesis](references/analyses/video-template-research-thread-synthesis.md)

## Direction Notes

- [Hook Entry Patterns](direction-notes/hook-entry-patterns.md)
- [On-Camera Connection And Delivery](direction-notes/on-camera-connection-and-delivery.md)
- [Zoom Into The Moment](direction-notes/zoom-into-the-moment.md)
- [Edit Cut Vocabulary](direction-notes/edit-cut-vocabulary.md)
- [Cinematic Coverage And Camera Direction](direction-notes/cinematic-coverage-and-camera-direction.md)
- [Story Template vs Sequence Template](direction-notes/story-template-vs-sequence-template.md)
- [Seedance 2 Direction](direction-notes/seedance-2-direction.md)

## Provider Export Notes

- [Seedance 2 Export](provider-exports/seedance-2-export.md)
- [Seedance Cinematic Prompt Protocol](../video-provider-research/providers/seedance-cinematic-prompt-protocol.md)

## Current Walkthroughs

- [Full Story: 90s Sitcom AI Replacement](walkthroughs/full-story-90s-sitcom-ai-replacement.md)
- [Micro-Journey: AI Video Workflow Toolkit](walkthroughs/micro-journey-ai-video-workflow-toolkit.md)
- [Utility Sequence: Explainer Video Toolkit](walkthroughs/utility-sequence-explainer-video-toolkit.md)
- [Candidate Micro-Journey: Problem-Solution Demo](walkthroughs/candidate-micro-journey-problem-solution-demo.md)
- [Candidate Micro-Journey: How-To Tip Demo](walkthroughs/candidate-micro-journey-how-to-tip-demo.md)
- [Candidate Micro-Journey: Social Proof Receipt](walkthroughs/candidate-micro-journey-social-proof-receipt.md)
- [Cultural Format: Documentary Mini-Profile](walkthroughs/cultural-format-documentary-mini-profile.md)
- [Evidence: Problem-Solution Demo For A Kitchen Tool](walkthroughs/evidence-problem-solution-demo-kitchen-tool.md)
- [Evidence: How-To Tip Demo For Lighting](walkthroughs/evidence-how-to-tip-demo-lighting.md)
- [Evidence: Social Proof Receipt For Waitlist Demand](walkthroughs/evidence-social-proof-receipt-waitlist-demand.md)
- [Evidence: Documentary Mini-Profile For A Ceramicist](walkthroughs/evidence-documentary-mini-profile-ceramicist.md)

## Promotion Rule

A story template should not be promoted until it has:

- a clear hook,
- a visible turn or reframe,
- a payoff,
- required inputs,
- a recommended format fit,
- and a provider-neutral structure that can survive multiple platforms.

Sequences without narrative turn stay as format or provider templates.

## Narrative Depth

Not every video needs a full Story Template. Draft routing uses three levels:

- `full_story`: Story Template required.
- `micro_journey`: Micro-Journey Template required.
- `utility_sequence`: purpose, role, constraints, and success criteria required.

Every output still needs a purpose and payoff.

## Current Implementation Boundary

The canonical Video Medium Plan schema now stores `narrative_depth`, `story_template_ref`, `micro_journey_template_ref`, and `asset_purpose_brief`.

The current `micro_journey_template_ref` enum supports nine ids:

- `unboxing_reveal`
- `product_reveal`
- `ugc_testimonial`
- `fashion_fit_check`
- `quick_before_after_demo`
- `problem_solution_demo`
- `how_to_tip_demo`
- `creator_showcase_moment`
- `day_in_the_life_signal`

Research candidates such as `social_proof_receipt` and `order_pack_ritual` stay in draft notes until a separate promotion patch expands the relevant library or enum.

Current evidence has promoted `problem_solution_demo`, `how_to_tip_demo`, and `documentary_mini_profile`. `social_proof_receipt` still needs one more proof type test before promotion.

Current placement decision for the cinematic Seedance reference: [Draft Decision 0017](decisions/0017-seedance-cinematic-reference-placement.md).
