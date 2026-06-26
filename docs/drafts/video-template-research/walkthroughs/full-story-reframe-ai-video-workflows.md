# Full-Story Walkthrough: AI Video Workflow Reframe

Status: research draft.

Purpose: test `narrative_depth = full_story` with a reframe / argument story, not a repeated-escalation sketch. This is not a canonical Video Medium Plan, schema fixture, Creative Brief, Prompt Plan, or provider export.

## Source Narrative

Template narrative:

> I saw this -> most people think it means this -> it actually means this -> here is the move.

Applied to AI video workflows:

- I saw people chasing full video generation.
- Most people think this means creators should prompt finished videos directly.
- It actually means direction, still-frame approval, and visual judgment matter more.
- The move is: still frame first, approve, animate, package.

## Walkthrough Packet

### Narrative Depth

`full_story`

Rationale: this is more than a quick product reveal or utility sequence. It carries an argument with a visible reframe: the obvious read of AI video progress is "prompt the final video"; the stronger read is "control the frame, approve the direction, then animate deliberately."

### Format Intent

Short social creator explainer with supporting B-roll and motion graphics.

### Accepted Output Shape

Primary shape: `short_social_video`

Format modifiers:

- `explainer_clip`
- `performance_clip`

Rationale: the creator likely delivers the argument directly, but the idea needs visual proof through still frames, storyboard panels, animation passes, and finished B-roll package examples.

### Required Story Structure / Story Movement

Recommended draft Story Template: `misread_signal_reframe_move`

Adapted movement:

1. Signal: people are chasing full AI video generation and expecting the model to solve the whole creative problem.
2. Common read: most people think this means creators should prompt complete finished videos directly.
3. Reframe: the real leverage is approving the visual direction before motion enters the process.
4. Implication: if the still frame is wrong, animation only makes the wrong decision more expensive and harder to control.
5. Move: build the frame first, approve it, animate it, then package the useful B-roll.
6. Payoff: the viewer leaves with a practical decision rule for AI video workflows.

Secondary draft pattern: `myth_reality_move`

- Myth: AI video quality means one prompt should produce the finished clip.
- Reality: usable video starts with controlled visual decisions.
- Move: use still-frame approval as the creative checkpoint before generation expands.

### Hook Posture

Primary hook posture: `surprising statement`

Possible hook: "The biggest AI video mistake is trying to generate the video first."

Secondary hook posture: `visual action`

Visual hook: show a chaotic grid of almost-good AI video outputs, then cut to one approved still frame that looks intentional and controllable.

### Payoff

The payoff should be a decision rule, not a generic anti-AI claim:

> Still frame first. Approve. Animate. Package.

The viewer should understand that AI video workflows are not only about prompting motion. They are about preserving creative judgment before motion multiplies the decision.

## Scenes Or Sections

### Section 1: The Signal

Purpose: show the trend or behavior that triggered the reframe.

Content:

- creator sees people chasing one-shot full video generation;
- quick montage or screen-like visual of many generated clips;
- the feeling is speed, noise, and almost-there outputs.

Key turn: the signal looks like "AI can now finish the whole video."

### Section 2: The Common Read

Purpose: name the interpretation most creators inherit.

Content:

- creator states or shows the common belief: prompt the final video directly;
- supporting visuals show prompt box -> generated clip -> disappointment or inconsistent result;
- optional on-screen phrase: "Prompt the finished video?"

Key turn: this read feels efficient but hides the control problem.

### Section 3: The Reframe

Purpose: reveal what the signal actually means.

Content:

- approved still frame appears as the control point;
- visual comparison: bad motion from weak frame vs strong motion from approved frame;
- creator explains that direction, composition, lighting, subject clarity, and continuity must be approved before animation.

Key turn: the important object is not the final video prompt; it is the approved frame and the decision behind it.

### Section 4: The Move

Purpose: give the viewer a repeatable method.

Content:

- simple process flow: still frame -> approval -> animation -> B-roll package;
- show one approved still becoming a short motion asset;
- show several finished B-roll uses in a grid or timeline.

Key turn: the method turns vague generation into a controlled workflow.

### Section 5: The Payoff

Purpose: lock the rule and make it memorable.

Content:

- final visual lockup: "Still frame first. Approve. Animate. Package.";
- creator or motion graphic ties the process to better creative direction;
- ending beat should feel like sharper judgment, not just a production tip.

## Storyboard Scope

Recommended scope: 8 to 10 Storyboard Shots.

Possible shot distribution:

1. Hook shot: chaotic full-video generation grid.
2. Creator reaction or narration setup.
3. Prompt-to-finished-video attempt.
4. Inconsistent or almost-right result.
5. Approved still frame as the control point.
6. Side-by-side proof of weak frame vs approved frame.
7. Process flow: still -> approve -> animate -> package.
8. One still becoming an animated B-roll asset.
9. Finished B-roll package grid or timeline.
10. Final rule lockup.

Storyboard priorities:

- make the misread legible quickly;
- show the reframe visually, not only verbally;
- preserve the difference between "prompting a finished video" and "directing an approved still into motion";
- keep the final rule simple enough to remember.

Do not generate storyboard stills, motion clips, or final video without explicit Generation Approval.

## Audio / Text Posture

Video Audio Posture: `voiceover` or `mixed`.

Text Journey likely required for:

- exact hook line;
- voiceover script;
- on-screen labels for the process flow;
- final rule lockup wording if the artist wants variants.

The Video Medium Plan should carry timing, placement, and text refs only. It should not absorb full script drafting.

Sound Journey is not required unless music or sound design becomes a first-class deliverable.

## Reference Needs

Likely reference needs:

- approved still frame example;
- visual style reference for the B-roll package;
- example of a weak or uncontrolled generated output, if safe and useful;
- process-flow graphic style reference;
- creator identity reference if the creator appears on camera;
- product/toolkit reference if a specific workflow package is shown.

Continuity-critical visual facts:

- the approved still must remain the same visual anchor as it becomes motion;
- the final B-roll package should visibly derive from the approved still and not become a generic asset grid.

## Provider Preferences As Non-Binding Notes

Provider preference notes are downstream only:

- Seedance, Higgsfield, Runway, Sora, Veo, Remotion, or HyperFrames can be considered after storyboard approval;
- provider duration limits may require segmenting the storyboard, but should not change the approved argument;
- frame rate, language experiments, camera/lens details, lighting recipes, no subtitles/music, and last-frame continuity belong in provider export, not core story fields;
- if using a code renderer for motion graphics, preserve the same story movement and approved visual hierarchy.

## Risks / Gaps In Current Framework

- This walkthrough confirms the need for `misread_signal_reframe_move` as a strong full-story pattern for creator education and argument videos.
- `full_story` can be compact and argument-led; it does not always mean fictional plot or scene drama.
- The boundary between `full_story` and `utility_sequence` needs attention: the process flow itself is utility-like, but the whole video is full story because it changes the viewer's interpretation.
- The boundary between Text Journey and Video Medium Plan matters. The argument needs strong lines, but exact wording should be drafted in Text Journey.
- The current Video Medium Plan schema still has no durable `narrative_depth` field, so this classification must live in rationale or traceability notes for now.

## Recommendations Before Promotion

1. Treat this as `full_story`, not `micro_journey`, because the viewer is moved through a misread, reframe, implication, and move.
2. Keep `misread_signal_reframe_move` as a draft Story Template candidate for creator education, analysis, and reframe videos.
3. Add future chooser guidance: when a utility method is embedded inside an argument, classify the whole video by the audience journey, not by the presence of a process graphic.
4. Do not promote schema fields yet. This walkthrough supports the candidate field `narrative_depth`, but more examples should prove whether it needs durable validation.
5. If this becomes a real Video Medium Plan, require Text Journey support for the hook, voiceover, and final rule variants before storyboard lock.
