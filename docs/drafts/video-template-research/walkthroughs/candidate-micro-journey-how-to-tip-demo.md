# Candidate Micro-Journey Walkthrough: How-To Tip Demo

Status: Draft walkthrough for template research. This file tests whether `how_to_tip_demo` deserves promotion into `micro_journey_template_ref` or should continue to map to an existing schema-supported id.

## Sample Request

Create a 20-30 second vertical Reel or Short teaching creators one repeatable move for turning an approved still frame into a better video prompt or storyboard shot.

The video should show that a still frame alone is not yet an animation plan. The creator should learn to add six missing pieces before animation: subject, action, camera movement, lighting, continuity reference, and payoff/end frame.

## Routing Decision

- `narrative_depth`: `micro_journey`
- Candidate template: `how_to_tip_demo`
- Current schema-safe fallback: `creator_showcase_moment`, only if a validating Video Medium Plan must choose an existing enum value.
- Cultural Format Structure: `educational_reel_micro_lesson`
- Supporting utility structure: `utility_process_steps`, used only as a step scaffold inside the micro-journey.

The central job is not to tell a full story or produce a neutral process asset. The viewer moves from "I have a still frame but do not know how to animate it well" to "I know the repeatable move for turning the still into a better shot prompt."

## Why This Is Not `full_story` And Not `utility_sequence`

This is not `full_story` because it does not need a full narrative arc, protagonist pressure, emotional turn, reversal, or complete story template. It has a compact educational movement: confusion, promise, method, result.

This is not only `utility_sequence` because the video must earn attention, promise a useful transformation, and end with a payoff the viewer can apply. A utility sequence can organize the steps, but the governing structure is a micro-journey from not knowing the move to being able to repeat it.

## Candidate Micro-Journey Fit

`how_to_tip_demo` fits when the desired output teaches one practical action quickly.

Expected movement:

1. Name the pain or missed opportunity.
2. Promise one repeatable tip.
3. Demonstrate the tip in a small number of visible steps.
4. Show the improved result.
5. Close with a save, repeat, or use cue.

For this sample, the repeatable action is: turn an approved still frame into an animation-ready shot prompt by filling the missing direction slots.

## Nearest Current Schema-Supported Id

Nearest id: `creator_showcase_moment`.

Why it is insufficient: `creator_showcase_moment` is strongest when the creator's taste, skill, or process is the memory. In this sample, the audience should remember and repeat a specific action. The creator may appear, but the educational move is the product.

Other nearby id: `product_reveal`.

Why it is insufficient: there is no product reveal as the main payoff. The payoff is a better prompt or storyboard shot. Treating this as `product_reveal` would over-weight reveal mechanics and under-weight learning clarity.

Current schema-valid route: use `how_to_tip_demo`.

## Cultural Format Structure Fit

Primary fit: `educational_reel_micro_lesson`.

This format expects one useful idea quickly, a clear promise, a compact teaching sequence, and a recap or save cue. It matches the requested 20-30 second Reel or Short.

Secondary influence: `short_social_hook_loop`.

The first frame should make the problem legible immediately, and the ending can loop back to the first frame by showing the original still again with the improved prompt layered beside it.

## Required Video Medium Plan Payload

A Video Medium Plan for this walkthrough should carry:

- `narrative_depth`: `micro_journey`
- `micro_journey_template_ref`: `how_to_tip_demo`
- `story_template_ref`: none
- `asset_purpose_brief`: none, unless a separate prompt-card asset package is requested
- Candidate note: `how_to_tip_demo`
- Cultural Format Structure: `educational_reel_micro_lesson`
- Output format: vertical short video, 9:16, 20-30 seconds
- Learning objective: teach one repeatable move for converting a still frame into a stronger animation prompt or storyboard shot
- Object of attention: approved still frame plus the prompt-building move
- Hook posture: correction or misconception
- Promised tip: fill the six missing direction slots before animation
- Proof/payoff: visible before/after prompt comparison or still-to-shot storyboard comparison
- Ending beat: save/use cue
- Shot count target: 5-7 shots
- Shot scale needs: close or medium-close views for creator explanation; readable prompt-card inserts
- Audio/text posture: voiceover-led or on-camera explanation with concise on-screen labels; exact wording belongs to Text Journey
- Reference needs: approved still frame, visual style reference, any desired creator identity reference, and prompt-card visual style
- Provider notes: no provider-specific syntax at this stage; provider export happens only after storyboard approval

## Draft 6-Shot Outline

1. Hook: Open on the approved still frame beside a weak prompt card: "Animate this." The visual problem is clear immediately.
2. Promise: Creator or text overlay names the move: "Before animation, add six shot directions."
3. Step 1: Fill subject and action from the still: who or what is moving, and what visible action should happen.
4. Step 2: Add camera movement and lighting: the shot becomes filmable instead of generic.
5. Step 3: Add continuity reference and payoff/end frame: the animation now has a target and a stopping point.
6. Result/payoff: Show weak prompt versus improved shot prompt, then return to the still with the improved storyboard direction attached. End with a save/use cue.

## Risks And Common Failure Modes

- Too many teaching points for a 20-30 second format.
- On-screen text becomes too dense to read.
- The video drifts into general prompt advice instead of one repeatable move.
- The payoff is only verbal and does not show a visible before/after improvement.
- The fallback id causes reviewers to judge it as a creator showcase instead of a teaching template.
- The exact script gets locked too early, before Text Journey has produced the final wording.
- Provider-specific instructions contaminate the storyboard before the provider export stage.

## Promotion Recommendation

Recommendation: **promote after one more confirming walkthrough**.

`how_to_tip_demo` has become its own `micro_journey_template_ref` after a second walkthrough confirmed the same pattern. The id supports clearer review criteria: one learning objective, compressed steps, visible result, and a repeat/use cue.

Do not merge it into `utility_process_steps`. That utility sequence can support the middle of the video, but it does not govern the hook, promise, proof, or payoff.

## What This Teaches The Framework

This walkthrough shows that some short videos need a teaching journey even when they do not need a full story. The framework should separate:

- process scaffolding, which explains ordered steps;
- micro-journey routing, which creates hook-to-payoff viewer movement;
- cultural format structure, which adapts the movement to a recognizable platform shape.

It also confirms that schema-valid fallbacks are useful for draft work but can hide important intent. `how_to_tip_demo` deserves promotion if the framework wants repeatable short educational videos to route cleanly.
