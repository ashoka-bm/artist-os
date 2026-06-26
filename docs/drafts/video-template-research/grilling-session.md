# Video Template Flow Grilling Session

Status: active draft.

## Goal

Decide how Artist OS should place video story templates, video format choices, direction notes, and provider exports into the existing flow without weakening Artist Meaning, Beat Plan authority, Video Medium Plan authority, or provider neutrality.

## Existing ADR Constraints

- Provider-specific behavior belongs downstream of the provider-neutral core.
- Story Structure belongs in the Beat Plan.
- Cultural Format Structure belongs in the Medium Plan after Medium Output Shape Recommendation.
- Video uses shared visual planning through Visual Units and Storyboard Shots.
- Video v0 stops at storyboard-ready planning.
- Provider video generation, renderers, and prompt syntax remain downstream adapters.

## Working Terms

- **Story Template:** the audience journey: hook, turn, payoff, proof, move, emotional or rhetorical arc.
- **Format Template:** the video container: short video, talking head, b-roll sequence, motion graphics package, UGC ad, documentary montage, sketch, animation, hybrid source-support video.
- **Direction Notes:** craft and execution rules that improve a format or provider export: shot economy, close framing for interaction, hook/payoff discipline, limited subjects, film grain, no subtitles/music by default.
- **Provider Export:** final platform translation after storyboard approval: Seedance 2 prompt, Higgsfield prompt, OpenMontage route, Remotion/HyperFrames render plan.

## Current Recommendation

Artist OS should not choose format in only one place. It needs a two-stage decision:

1. **Format Intent** is captured early during Orientation or Meaning Interview as a constraint and expectation, for example "short video," "explainer," "social post," "cinematic sketch," or "product demo."
2. **Binding Format Template** is selected in the Video Medium Plan after Beat Plan exists, because the Beat Plan owns story movement and the Video Medium Plan owns video-specific translation.

This lets the artist say "I want a short video" early, while keeping the system from letting platform convenience override Artist Meaning.

## Proposed Flow

1. Reference intake.
2. Orientation captures output intent and likely medium.
3. Meaning Interview captures Artist Meaning, must-preserve constraints, audience, and rough format intent.
4. Transformation Brief translates meaning into transformation direction.
5. Beat Plan selects or adapts the Story Template.
6. Medium Output Shape Recommendation checks whether the intended format still fits the story.
7. Video Medium Plan selects the binding Format Template and translates Beats into Video Sequences, Scenes, Storyboard Shots, Video Style Expression, and Video Audio Posture.
8. Optional post-storyboard Production Route chooses provider/export strategy.
9. Provider Export renders Seedance 2, Higgsfield, OpenMontage, Remotion, or other platform-specific instructions.

## Open Decisions

1. Should early Format Intent be treated as artist preference, hard constraint, or recommendation?
2. Should Story Templates live in the Story Structure Library, a Video Story Template Library, or a social/video-specific Cultural Format Structure Library?
3. Does "short video" mean a medium output shape, a cultural format, a platform package, or all three in different layers?
4. Which decisions must be made before the Beat Plan so the story is scaled correctly?
5. Which decisions must wait until the Video Medium Plan so the format does not contaminate story authority?
6. Which decisions belong only after storyboard approval as Provider Export or Production Route?
7. How do we prevent sequence templates from masquerading as story templates?

## First Decision Under Review

Question: When the artist says "I want this as a short video," should that be binding immediately?

Recommended answer: no. Capture it immediately as **Format Intent**, use it to scale the Beat Plan, then confirm or revise it during Medium Output Shape Recommendation before the Video Medium Plan becomes binding.

## Accepted Decisions

### Decision 1: Early Format Intent Is A Strong Preference

Status: accepted in draft on 2026-06-26.

When the artist says "I want this as a short video," Artist OS captures that immediately as **Format Intent**. It is a strong preference and planning constraint, not an irreversible lock.

Format Intent can shape early scope, pacing, and Decision Interview questions. It becomes binding only after Medium Output Shape Recommendation confirms that the selected story movement fits the requested output shape.

### Decision 2: Story Templates Live With Story Structure

Status: accepted in draft on 2026-06-26.

Reusable story templates belong with Story Structure, not in a separate video-only story authority.

Video-specific audience conventions, containers, and platform habits belong in Format Templates, Cultural Format Structure, Direction Notes, or Provider Exports depending on their authority.

### Decision 3: On-Camera Delivery Placement

Status: accepted in draft on 2026-06-26.

Intended Feeling is captured upstream in Artist Meaning, Transformation Brief, and Creative Brief work.

Speaker posture is decided in the Video Medium Plan when the selected format is speaker-led.

Conversational voice and point-plus-paint support are enforced during script drafting. Provider Export preserves the approved delivery posture for voiceover, dialogue, avatar, creator clone, and talking-head prompts.

### Decision 4: Hook Posture Placement

Status: accepted in draft on 2026-06-26.

The Beat Plan defines the turn, tension, misconception, desire, or promise the hook must open.

The Video Medium Plan chooses the hook posture once the format is known: question, surprising statement, story-in-the-moment, big promise, or visual action.

Script drafting writes the exact hook. Provider Export renders the hook safely for the chosen platform.

### Decision 5: Production Route After Storyboard

Status: accepted in draft on 2026-06-26.

Provider or production route is not chosen as a binding decision before the storyboard exists.

Artist OS may capture provider preference early if the artist names one, but the binding Production Route is selected only after Video Medium Plan and storyboard approval.

### Decision 6: Narrative Depth Routing

Status: accepted in draft on 2026-06-26.

Not every video output requires a full Story Template.

Every video output needs a purpose and payoff, but Artist OS should route video requests by Narrative Depth:

- `full_story`: requires a Story Template.
- `micro_journey`: requires a Micro-Journey Template.
- `utility_sequence`: requires a Format Template, sequence plan, or asset-purpose brief, but not a Story Template.

### Decision 7: Narrative Depth Placement

Status: accepted in draft on 2026-06-26.

Narrative Depth is captured provisionally during Orientation when the artist names the output type, then confirmed during Medium Output Shape Recommendation.

Video Medium Plan records the binding Narrative Depth and uses it to decide whether the video needs a Story Template, Micro-Journey Template, or utility sequence plan.

### Decision 8: Format Template Binding

Status: accepted in draft on 2026-06-26.

Format Intent is captured early, the likely Format Template is recommended during Medium Output Shape Recommendation, and the binding Format Template is selected inside the Video Medium Plan.

### Decision 9: Video Medium Plan Payload

Status: accepted in draft on 2026-06-26.

Video Medium Plan should carry Narrative Depth, binding Format Template, selected Story Template or Micro-Journey Template if any, hook posture, speaker posture when speaker-led, Video Audio Posture, Video Style Expression, reference strategy, storyboard scope, and provider preferences as non-binding notes.

Provider-specific settings stay out until Production Route.

### Decision 10: Scene Embodiment Placement

Status: accepted in draft on 2026-06-26.

Scene-embodiment direction stays as Direction Notes.

Beat Plan defines the emotional turn. Video Medium Plan decides whether the Beat becomes a scene, narration, b-roll, graphics, or another video treatment. Script and storyboard drafting apply moment anchors when immediacy is needed.

### Decision 11: Micro-Journey Template Placement

Status: accepted in draft on 2026-06-26.

Micro-Journey Templates stay adjacent to Story Templates in the draft library, but they are lower-depth structures selected through Narrative Depth.

They should not enter the main Story Structure Library as full story structures unless they include desire, conflict, turn, and result.

### Decision 12: Utility Sequence Representation

Status: accepted in draft on 2026-06-26.

Utility sequences should not use Story Templates or Micro-Journey Templates.

They should use an Asset Purpose Brief or utility sequence plan that records role in the larger video, subject, visual purpose, duration, motion, style constraints, success criteria, and where the output will be used.

### Decision 13: Create Draft Implementation Summary Now

Status: accepted in draft on 2026-06-26.

Create a draft ADR-style implementation summary that consolidates Decisions 0001-0012 and states the proposed flow.

Keep it in draft decisions rather than canonical `docs/adr/` until main skill or schema changes are approved.

### Decision 14: Edit Cut Vocabulary Placement

Status: accepted in draft on 2026-06-26.

Edit cut vocabulary stays as Direction Notes.

Beat Plan defines emotional movement. Video Medium Plan may name desired edit behavior when it affects rhythm, clarity, transition logic, or viewer feeling. Storyboard Shots can include transition or cut intent. Production Route or edit planning turns cut intent into actual edit decisions.

### Decision 15: Schema Fields vs Skill Guidance

Status: accepted in draft on 2026-06-26.

First implementation should be mostly skill guidance.

Only a small set of durable Video Medium Plan fields should be considered first: Narrative Depth, binding Format Template, selected structure refs, hook posture, speaker posture, and provider preference notes.

Direction-note vocabularies such as hook types, moment anchors, and edit cuts stay as skill guidance until repeated runs prove they need durable fields.

### Decision 16: Create Video Medium Plan Extension Note

Status: accepted in draft on 2026-06-26.

Create a draft Video Medium Plan extension note under `docs/drafts/video-template-research/`.

The note lists candidate fields, separates schema candidates from skill guidance, and shows how `full_story`, `micro_journey`, and `utility_sequence` route through the flow.

## New References Added During Session

- Speech hook transcript: useful for hook-entry direction, especially question hooks, surprising statements, story openings, big promises, and visual action hooks.
- Five-line story transcript: useful for story-template structure: situation, desire, conflict, change, and result.
- YouTube speaking/script delivery transcript: useful for creator-led direction, especially conversational voice, connection over perfection, Intended Feeling, point-plus-paint support, and warm delivery.
- Storytelling zoom-into-the-moment transcript: useful for scene-level direction, especially location, action, raw thought, visible emotion, and dialogue.
- Seven cuts editing transcript: useful for edit-direction vocabulary, especially flow cuts, smash cuts, jump cuts, action cuts, wide-medium-close, match cuts, and rhythm cuts.

## Current Synthesis

The hook transcript belongs mainly in `direction-notes/`, because it teaches opening tactics that can serve many story templates.

The five-line story transcript belongs in `story-templates/`, because it defines a reusable story skeleton that can scale from a short video to a longer story.

The speaking/script delivery transcript belongs in `direction-notes/`, because it shapes script voice and performance after the story movement and format are known.

The zoom-into-the-moment transcript belongs in `direction-notes/`, because it tells script and storyboard planning how to embody a Beat as a lived scene rather than summarize it.

The seven-cuts transcript belongs in `direction-notes/`, because cuts express what a moment needs. They do not define story authority.

## Resolved Decision

Question: where should short-video story templates live?

Recommended answer: put reusable story movement in the Story Structure Library or a draft extension of it, and put platform-specific audience grammar in Cultural Format Structure / Format Template. A hook pattern such as "surprising statement" should be direction guidance unless it defines the whole audience journey.

Accepted answer: yes. Story movement belongs with Story Structure. Video-specific format and delivery guidance stays downstream.

## Next Decision Under Review

Question: where should on-camera delivery direction be decided?

Recommended answer: capture the desired viewer feeling upstream, then decide speaker posture in the Video Medium Plan only when the selected format is speaker-led. Script drafting should enforce conversational voice and point-plus-paint support.

Accepted answer: yes. Split delivery direction across upstream Intended Feeling, Video Medium Plan speaker posture, script checks, and provider export preservation.

## Next Decision Under Review

Question: where should hook posture be decided?

Recommended answer: the Beat Plan should define the turn or tension the hook must open. The Video Medium Plan should choose the hook posture, such as question, surprising statement, story-in-the-moment, big promise, or visual action, once format is known. Script drafting then writes the exact hook, and Provider Export renders it safely for the platform.

Accepted answer: yes. Hook posture is selected in Video Medium Plan, grounded by Beat Plan and finalized during script/provider export.

## Next Decision Under Review

Question: when should provider or production route be chosen?

Recommended answer: do not choose the provider before the storyboard exists. Capture provider preference early if the artist names one, but select the binding Production Route only after Video Medium Plan and storyboard approval. Provider choice can then account for the actual format, required references, duration, audio, style, shot complexity, budget, and platform limits.

Accepted answer: yes. Provider preference may be captured early, but binding Production Route selection happens after storyboard approval.

## Next Decision Under Review

Question: how do we prevent sequence templates from masquerading as story templates?

Recommended answer: require every Story Template to pass a story-core test: hook or opening tension, audience or character desire, obstacle/conflict, turn/change, and payoff/result. If a pattern only defines shot order, duration, camera movement, provider syntax, or visual sequence, it belongs in Format Template, Direction Notes, or Provider Export.

Accepted refinement: yes, but not every video needs the full story-core test. First route by Narrative Depth. Full stories need the full test; micro-journeys need hook, object of attention, reason to care, proof/reveal/payoff, and ending beat; utility sequences need purpose, constraints, and success criteria.

## Next Decision Under Review

Question: where should Narrative Depth be decided?

Recommended answer: capture a provisional Narrative Depth during Orientation when the artist names the output type, then confirm it during Medium Output Shape Recommendation. Video Medium Plan records the binding narrative depth and uses it to decide whether to apply a Story Template, Micro-Journey Template, or utility sequence plan.

Accepted answer: yes. Narrative Depth is provisional in Orientation, confirmed during Medium Output Shape Recommendation, and recorded as binding in Video Medium Plan.

## Next Decision Under Review

Question: when does the Format Template become binding?

Recommended answer: capture Format Intent early, recommend the likely Format Template during Medium Output Shape Recommendation, and make it binding inside the Video Medium Plan. That keeps early artist preference visible while ensuring the final format fits Artist Meaning, Narrative Depth, Story Template or Micro-Journey Template, audio posture, and production constraints.

Accepted answer: yes. Format Intent is early, likely Format Template is recommended during Medium Output Shape Recommendation, and binding Format Template belongs in Video Medium Plan.

## Next Decision Under Review

Question: what must the Video Medium Plan carry so downstream script, storyboard, and provider export do not improvise?

Recommended answer: Video Medium Plan should carry at least Narrative Depth, binding Format Template, selected Story Template or Micro-Journey Template if any, hook posture, speaker posture when speaker-led, Video Audio Posture, visual style expression, reference strategy, storyboard scope, and provider preferences as non-binding notes. Provider-specific settings should stay out until Production Route.

Accepted answer: yes. Video Medium Plan carries those binding decisions and keeps provider-specific settings downstream.

## Next Decision Under Review

Question: where should scene-embodiment direction, such as location/action/thought/emotion/dialogue, be applied?

Recommended answer: keep it as Direction Notes. Beat Plan defines the emotional turn; Video Medium Plan decides whether the Beat becomes a scene; script and storyboard drafting apply moment anchors when immediacy is needed.

Accepted answer: yes. Scene embodiment stays as Direction Notes and is applied during script/storyboard drafting after Beat Plan and Video Medium Plan decide what the Beat is doing.

## Next Decision Under Review

Question: where should Micro-Journey Templates live?

Recommended answer: keep them adjacent to Story Templates in the draft library, but treat them as lower-depth structures selected by Narrative Depth. They should not enter the main Story Structure Library as full story structures unless they include desire, conflict, turn, and result. In implementation, they may become a `micro_journey` subset of Cultural Format Structure or Video Template Library rather than Story Structure.

Accepted answer: yes. Micro-Journey Templates remain adjacent for research but are lower-depth structures, not full Story Structure entries unless they pass the full story-core test.

## Next Decision Under Review

Question: how should utility sequences be represented?

Recommended answer: utility sequences should not use Story Templates or Micro-Journey Templates. They should use an Asset Purpose Brief or utility sequence plan that records role in the larger video, subject, visual purpose, duration, motion, style constraints, success criteria, and where the output will be used. They still need purpose and payoff, but the payoff can be functional, such as "establish setting," "show texture," or "bridge two scenes."

Accepted answer: yes. Utility sequences use an Asset Purpose Brief or utility sequence plan, not Story or Micro-Journey Templates.

## Next Decision Under Review

Question: should these draft decisions be consolidated into a single implementation-facing ADR-style summary now, or kept only as individual draft decisions while we gather more references?

Recommended answer: create a draft ADR-style summary now under `docs/drafts/video-template-research/decisions/` that links Decisions 0001-0012 and states the proposed implementation flow. Keep it draft, not a canonical `docs/adr/` entry, until we decide to change the main skill/schema flow.

Accepted answer: yes. A draft implementation summary exists as `draft-video-template-flow-summary.md`.

## Next Decision Under Review

Question: where should edit cut vocabulary be applied?

Recommended answer: keep cut vocabulary as Direction Notes. Beat Plan defines emotional movement, Video Medium Plan may name edit behavior when it affects rhythm or viewer feeling, Storyboard Shots can include cut intent, and Production Route/edit planning turns that intent into actual edit decisions.

Accepted answer: yes. Edit cut vocabulary stays as Direction Notes and is applied by Video Medium Plan, Storyboard Shots, and later edit planning when it serves the moment.

## Next Decision Under Review

Question: which of these draft decisions should become schema-backed fields first, and which should stay skill guidance?

Recommended answer: first implementation should be mostly skill guidance, with only a small set of fields considered for Video Medium Plan: Narrative Depth, binding Format Template, selected structure refs, hook posture, speaker posture, and provider preference notes. Direction-note vocabularies such as hooks, moment anchors, and cuts should remain skill guidance until repeated runs prove they need durable fields.

Accepted answer: yes. Start mostly as skill guidance; only the small durable Video Medium Plan decision set should be considered for schema first.

## Next Decision Under Review

Question: what should the next implementation artifact be?

Recommended answer: create a draft Video Medium Plan extension note that lists the candidate fields, explains which are schema candidates and which remain guidance, and shows how `full_story`, `micro_journey`, and `utility_sequence` route through the flow. Keep it under `docs/drafts/video-template-research/`, not canonical docs, until promotion is approved.

Accepted answer: yes. A draft Video Medium Plan extension note exists as `video-medium-plan-extension-note.md`.

## Next Decision Under Review

Question: should the draft extension note be promoted into a canonical ADR or implementation plan now?

Recommended answer: no. Keep it draft until we have at least one or two sample walkthroughs using real video requests. The next useful step is to run example scenarios through the draft flow: one `full_story`, one `micro_journey`, and one `utility_sequence`.

Current answer: keep this as a revisit item. Do not promote yet.

Revisit trigger: after sample walkthroughs for one `full_story`, one `micro_journey`, and one `utility_sequence`.
