# Evidence Walkthrough: How-To Tip Demo For Lighting

Status: research draft.

Candidate tested: `how_to_tip_demo`.

## Sample Request

Create a 20-30 second vertical Reel or Short teaching creators one repeatable lighting move for better talking-head videos: turn the body slightly away from the window, then let the face rotate back toward the light so the shot gains shape instead of looking flat.

The viewer should leave with one usable move they can try immediately before recording their next video.

## Routing Decision

- `narrative_depth`: `micro_journey`.
- Candidate template: `how_to_tip_demo`.
- Current schema-supported fallback: `creator_showcase_moment`.
- Cultural Format Structure: `educational_reel_micro_lesson`.
- Supporting utility structure: `utility_process_steps`, only for the middle demonstration.
- Provider posture: provider-neutral.

## Why This Is Not `full_story`

This video does not need a complete story arc. It needs a compressed teaching journey:

1. Show the common mistake.
2. Promise one move.
3. Demonstrate the move.
4. Show the visible improvement.
5. Close with a repeat cue.

## Why This Is Not `utility_sequence`

The middle may use process steps, but the output is not a neutral instruction asset. It must earn attention, make the viewer feel the before state is weak, and land a practical payoff. That makes it a micro-journey.

## Candidate Micro-Journey Fit

`how_to_tip_demo` fits because the viewer is meant to learn one repeatable action, not admire the creator or watch a product reveal.

Core movement:

```text
common mistake -> promised tip -> small demonstration -> visible result -> repeat cue
```

Required decisions:

- What is the one mistake?
- What is the one move?
- What visual before/after proves the move?
- How many steps can fit without over-teaching?
- What should the viewer remember as the repeatable cue?

## Nearest Current Schema-Supported Id

Use `creator_showcase_moment` as the schema-supported fallback if the plan must validate today.

Why it is insufficient:

- The creator can appear, but the creator is not the main memory.
- The viewer should remember the lighting move, not the creator's taste or persona.
- `creator_showcase_moment` can under-specify learning objective, step compression, and repeat cue.

Do not route as `quick_before_after_demo` unless the video removes the teaching layer and becomes only a visible improvement comparison.

## Cultural Format Structure Fit

Primary fit: `educational_reel_micro_lesson`.

Why:

- One useful idea must appear quickly.
- The promise is practical and repeatable.
- The payoff is a visible side-by-side or reset shot.
- The ending can ask viewers to save or try the move.

Secondary fit: `short_social_hook_loop` if the final improved frame loops back to the opening flat frame.

## Required Video Medium Plan Payload

The Video Medium Plan should carry:

- `narrative_depth = micro_journey`;
- `micro_journey_template_ref = how_to_tip_demo`;
- rationale note: candidate pattern is `how_to_tip_demo`;
- learning objective: teach one lighting move for talking-head videos;
- object of attention: subject position relative to window light;
- hook posture: correction of a common mistake;
- promised tip: turn body away, face back toward light;
- steps: flat setup, rotation, face return, result;
- proof visual: before/after lighting shape on face;
- payoff: more dimensional talking-head frame;
- ending cue: "Try this before recording";
- text/audio posture: on-camera or voiceover-led with sparse labels;
- reference needs: room/window setup, subject framing, before/after stills;
- provider notes: downstream only after storyboard approval.

## Draft Shot / Beat Outline

1. **Hook / Mistake**
   Front-facing talking-head shot near a window looks flat. Text or voiceover: "If your window light looks flat, try this."

2. **Promise**
   Creator points to the window direction and names the move: "Turn your body away, then bring your face back to the light."

3. **Step 1**
   Show the body rotating slightly away from the window. Keep the camera angle steady.

4. **Step 2**
   Show the face turning back toward the window while the body remains angled.

5. **Proof**
   Split or quick cut: flat frame versus shaped frame. The cheek shadow and eye light should be legible.

6. **Payoff / Repeat Cue**
   End on the improved frame with a compact cue: "Body away. Face to light."

## Risks And Common Failure Modes

- The video teaches too many lighting concepts at once.
- The before/after is not visually different enough.
- The creator personality overwhelms the teachable move.
- The tip is worded as abstract lighting theory rather than a physical action.
- The proof depends on gear instead of body/light placement.
- The final cue is too long to remember.

## Promotion Recommendation

Recommendation: **promote `how_to_tip_demo`**.

This second walkthrough confirms the candidate works outside AI-video prompting. It has the same governing movement as the first test: one pain or missed opportunity, one promised move, compressed demonstration, visible result, repeat cue.

`how_to_tip_demo` is now promoted into `micro_journey_template_ref`.

## What This Teaches The Framework

`how_to_tip_demo` is the right home for short educational videos where the viewer should leave able to do one thing. It should remain separate from `utility_process_steps` because it governs audience movement, not only ordered actions.

The reviewer check should ask: is there one learning objective, are the steps compressed, is the result visible, and does the ending give a repeatable cue?
