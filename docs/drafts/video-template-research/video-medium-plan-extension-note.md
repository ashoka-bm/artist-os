# Draft Video Medium Plan Extension Note

Status: research draft.

This note translates the video-template grilling decisions into a possible Video Medium Plan extension. It is not canonical and does not change schemas or the main Artist OS skill.

## Purpose

The Video Medium Plan should carry enough binding video decisions that script, storyboard, and provider export do not improvise. It should remain provider-neutral.

## Candidate Fields

These are the first fields to consider if this moves toward implementation:

| Candidate Field | Purpose | Suggested Status |
| --- | --- | --- |
| `narrative_depth` | Routes the output as `full_story`, `micro_journey`, or `utility_sequence`. | Schema candidate |
| `format_template_ref` | Names the binding video format template. | Schema candidate |
| `story_structure_ref` | Links to selected Story Structure when `narrative_depth = full_story`. | Existing concept / schema candidate |
| `micro_journey_template_ref` | Links to selected Micro-Journey Template when `narrative_depth = micro_journey`. | Draft candidate |
| `utility_sequence_plan_ref` | Links to an Asset Purpose Brief or utility sequence plan when `narrative_depth = utility_sequence`. | Draft candidate |
| `hook_posture` | Names the chosen hook posture when relevant. | Schema candidate or skill-guided field |
| `speaker_posture` | Names speaker relationship and delivery posture for speaker-led formats. | Schema candidate or skill-guided field |
| `provider_preferences` | Captures named provider preferences as non-binding notes. | Schema candidate as notes |

## Guidance, Not Fields Yet

These should remain skill guidance until repeated runs prove durable storage is needed:

- hook-entry vocabulary,
- moment anchors: location, action, raw thought, visible emotion, dialogue,
- on-camera connection checks,
- point-plus-paint support,
- edit cut vocabulary,
- Seedance 2 prompt tendencies,
- provider-specific constraints,
- detailed cut choices unless they affect storyboard transitions.

## Narrative Depth Routing

### `full_story`

Use when the output needs emotional, narrative, rhetorical, or conceptual movement.

Required planning:

- Story Structure or Story Template.
- Opening tension or hook.
- Desire, question, or audience need.
- Obstacle, conflict, misconception, or pressure.
- Turn or change.
- Payoff or result.

Typical outputs:

- personal story,
- documentary mini-arc,
- reframe explainer,
- cinematic sketch,
- transformation story.

### `micro_journey`

Use when the output is functional, promotional, social, or showcase-led but still needs hook and payoff.

Required planning:

- Micro-Journey Template.
- Hook.
- Object of attention.
- Viewer reason to care.
- Proof, reveal, or sensory payoff.
- Ending beat.

Typical outputs:

- unboxing,
- product reveal,
- UGC testimonial,
- influencer moment,
- fashion fit check,
- quick before/after demo.

### `utility_sequence`

Use when the output is an asset or supporting clip rather than a self-contained audience journey.

Required planning:

- Asset Purpose Brief or utility sequence plan.
- Role in larger video.
- Subject.
- Visual purpose.
- Duration.
- Motion.
- Style constraints.
- Success criteria.
- Placement/use context.

Typical outputs:

- title card,
- b-roll loop,
- product spin,
- style test,
- transition plate,
- camera-control test.

## Flow Placement

1. Orientation captures Format Intent, provider preference, and provisional Narrative Depth.
2. Artist Meaning and Creative Brief capture Intended Feeling and must-preserve constraints.
3. Beat Plan owns story movement for `full_story`.
4. Medium Output Shape Recommendation confirms Narrative Depth and likely Format Template.
5. Video Medium Plan records binding Narrative Depth and Format Template.
6. Script and storyboard drafting apply direction notes.
7. Storyboard approval locks provider-neutral planning.
8. Production Route chooses provider or renderer.
9. Provider Export renders platform-specific prompts or packets.

## Review Checks

- Does Narrative Depth match the requested output?
- Does `full_story` have a real turn and payoff?
- Does `micro_journey` have a reason to care and an ending beat?
- Does `utility_sequence` have functional purpose and success criteria?
- Does hook posture point toward payoff?
- Does speaker posture preserve Intended Feeling?
- Are provider preferences non-binding before storyboard approval?
- Did provider export avoid changing the approved plan?

## Open Questions

- Should `hook_posture` and `speaker_posture` become required only for certain Format Templates?
- Should Micro-Journey Templates live under Cultural Format Structure or a dedicated Video Template library?
- Should `utility_sequence_plan_ref` point to a new Asset Purpose Brief record or remain a Video Medium Plan section?
- Should provider preferences live in Video Medium Plan, Production Route, or both?
