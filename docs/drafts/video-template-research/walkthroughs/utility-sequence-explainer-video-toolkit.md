# Utility Sequence Walkthrough: The Explainer Video Toolkit

Status: research draft.

This walkthrough tests `narrative_depth = utility_sequence` against a motion graphics / B-roll package request. It is not a canonical Video Medium Plan, schema fixture, Creative Brief, Prompt Plan, or provider export.

## Source Request

Build a complete B-roll package for a creator explainer called "The Explainer Video Toolkit." Seven graphics:

1. Intro title card: "The Explainer Video Toolkit" / "Hook, clarity, retention"
2. Kinetic infographic: "The Idea to Visual Gap"
3. Process flow: one sentence skill choices, final still, Seedance animation, finished B-roll
4. Hook card: "Earn attention fast"
5. Clarity card: "Make the idea visible"
6. Retention card: "Give viewers a reason to stay"
7. Key takeaway card: "Still frame first. Approve. Animate."

Style: match the approved Idea to Visual Gap still from Segment 2. Deep charcoal backgrounds, off-white text, restrained typography, clean geometric callouts, gold data highlights. 16:9.

## Routing

Narrative Depth: `utility_sequence`.

Reason: the request asks for a functional package of motion graphics assets, not a self-contained audience story. The payoff is functional: each graphic should make an explainer video clearer, more visual, and easier to retain.

Format Intent: complete B-roll / motion graphics package for a creator explainer.

Accepted Output Shape: `other` as "motion graphics B-roll package," with `explainer_clip` as the closest format modifier.

Story Structure: not required. No Story Template or Micro-Journey Template should be forced.

Asset Purpose Brief: required.

Provider Route: not selected. Seedance is mentioned only as one process step in the graphic content and as a possible downstream provider-export note; it does not define the package.

## Asset Purpose Brief

Role / Use Context: supporting visuals for a creator explainer video. The assets can sit under narration, between talking-head sections, or inside a production tutorial.

Subject: the creator's explainer-video workflow and the principle that still-frame approval should precede animation.

Visual Purpose: turn abstract production advice into clean, inspectable visual anchors.

Placement: likely distributed across an explainer segment:

- opening title near the start,
- Idea to Visual Gap when naming the problem,
- process flow when explaining the method,
- hook/clarity/retention cards as section markers,
- key takeaway near the end.

Duration Target: each asset can hold for 3-6 seconds as B-roll or 6-10 seconds if animated as a standalone insert. Any provider-generated motion clip should stay within provider limits during export.

Shot / Graphic Count: 7 graphics.

Motion Behavior: restrained kinetic typography, geometric reveals, line draws, data highlight sweeps, subtle parallax, and clean transitions. Motion should guide reading order rather than decorate.

Loop Or Resolve Behavior:

- title and section cards resolve cleanly into a held frame;
- infographic and process flow may animate in steps, then hold;
- no asset needs an infinite loop unless later requested for background use.

Style Constraints:

- 16:9;
- deep charcoal background;
- off-white text;
- restrained typography;
- clean geometric callouts;
- gold highlights for data, emphasis, arrows, or key nodes;
- match the approved Idea to Visual Gap still from Segment 2;
- avoid busy UI, neon excess, decorative gradients, and platform-specific generator artifacts.

Audio / Text Posture: text-on-graphic is required because these are title/infographic/card assets. No music, narration, or subtitles should be assumed inside the raw asset package. Narration or music belongs to the larger explainer unless separately planned.

Reference / Continuity Needs:

- approved Idea to Visual Gap still from Segment 2 as style reference;
- typography and color reference if available;
- no character, location, or product reference package needed unless the final explainer includes a recurring host, brand, or product.

Success Criteria:

- each asset is readable within 1-2 seconds;
- all seven graphics feel like one package;
- each graphic has a distinct function;
- gold highlights clarify hierarchy rather than add decoration;
- motion improves comprehension;
- no graphic invents story conflict or emotional arc;
- final takeaway makes the workflow memorable: still frame first, approve, animate.

Downstream Export Notes:

- provider preferences are non-binding until storyboard / package approval;
- if exporting to Seedance, test 24fps, <=15 second clips, no music, no subtitles beyond the designed text, and a clear camera/capture style only if relevant;
- if using Remotion, HyperFrames, or another code renderer, preserve the same asset purpose and style rules;
- if using Higgsfield or image-first generation, create still frames first, approve, then animate.

## Utility Sequence Items

### 1. Intro Title Card

Label: "The Explainer Video Toolkit" / "Hook, clarity, retention"

Purpose: establish the package title and the three-part viewer promise.

Placement: opening or segment reset.

Motion: title resolves first, subtitle locks in second, three small gold markers appear for hook, clarity, retention.

Success Criteria: viewer immediately understands the explainer is about making videos clearer and more retentive.

### 2. Kinetic Infographic: The Idea To Visual Gap

Label: "The Idea to Visual Gap"

Purpose: name the problem: strong ideas often fail because the audience cannot see them.

Placement: problem/setup section.

Motion: two endpoints appear, a gap opens between them, gold line or marker measures the gap, then a visual bridge begins to form.

Success Criteria: viewer understands the conceptual gap without narration doing all the work.

### 3. Process Flow

Label: "One sentence skill choices -> final still -> Seedance animation -> finished B-roll"

Purpose: show the practical workflow from idea compression to approved still to animation to usable asset.

Placement: method section.

Motion: four nodes build left to right; gold highlight advances one node at a time.

Success Criteria: viewer can remember the production order and sees that animation happens after still-frame approval.

### 4. Hook Card

Label: "Earn attention fast"

Purpose: section marker for attention capture.

Placement: hook section or transition into a hook example.

Motion: fast but restrained entrance, short gold pulse on "attention," then hold.

Success Criteria: the card feels quick and urgent without becoming loud.

### 5. Clarity Card

Label: "Make the idea visible"

Purpose: section marker for visual explanation.

Placement: clarity section or before visual-metaphor examples.

Motion: text appears with a simple geometric reveal, such as a line drawing becoming a shape.

Success Criteria: the card itself demonstrates visibility and clarity.

### 6. Retention Card

Label: "Give viewers a reason to stay"

Purpose: section marker for sustaining attention.

Placement: retention section or before payoff/continuity examples.

Motion: subtle timeline or progress marker extends in gold and lands on a final point.

Success Criteria: viewer feels continuation, not just another title card.

### 7. Key Takeaway Card

Label: "Still frame first. Approve. Animate."

Purpose: final workflow memory lock.

Placement: end of the explainer or after process demonstration.

Motion: three short beats, each phrase lands separately, then all three align into one final system.

Success Criteria: the audience leaves with the production rule intact.

## Storyboard Scope

Recommended storyboard package: one 7-panel composite storyboard sheet, one panel per graphic, before any individual still or animation generation.

Panel Requirements:

- show final held state for each graphic;
- include small motion notes below or beside each panel;
- keep typography legible;
- preserve the charcoal/off-white/gold system across all panels;
- mark which panels need stepwise animation.

Do not generate separate storyboard stills unless explicitly requested. Do not generate animation or finished video in v0.

## Video Medium Plan Carry-Forward

The Video Medium Plan should carry:

- `narrative_depth`: `utility_sequence` in rationale or traceability notes until a field exists;
- accepted output shape: motion graphics B-roll package;
- asset purpose brief;
- seven utility sequence items;
- 16:9 aspect ratio;
- package style system;
- storyboard scope: one 7-panel composite sheet by default;
- audio posture: no raw audio assumed;
- text posture: designed on-graphic text required;
- reference needs: approved Idea to Visual Gap still and any brand/type/color references;
- provider preferences: non-binding notes only.

## Risks / Gaps In Current Framework

- `utility_sequence` is not a schema field yet, so it must live in rationale, notes, or traceability.
- The current `storyboard_shots` schema requires `beat_id` and `key_emotional_movement_id`, which may be awkward for pure utility assets.
- The existing `video_output_shape` enum has no direct "motion graphics package" or "B-roll package" value; `other` plus rationale is currently the cleanest fit.
- Text-on-graphic wording is central here, but Video Medium Plan should avoid drafting larger script/caption content when a Text Generation Plan is needed. Short labels supplied by the artist can remain in the package.
- Provider mentions inside graphic content, such as "Seedance animation," can be confused with provider route selection. The plan should treat that as displayed process language unless the artist separately selects Seedance for generation.
- Review needs utility-specific checks: package coherence, readability, functional payoff, motion usefulness, and avoidance of fake story.

## Recommendations Before Promotion

1. Keep Asset Purpose Brief as skill guidance until at least two more utility walkthroughs prove the same fields recur.
2. Consider a future `utility_sequence_plan` or `asset_purpose_brief` field if these packages become common.
3. Consider adding `motion_graphics_package` and `b_roll_package` to future output-shape options only after more examples.
4. Add a utility-specific Video Critic Review bullet if repeated runs show that normal shot progression review misses package usefulness.
5. Test this same packet once as:
   - still-frame storyboard package;
   - Remotion/HyperFrames-style renderer plan;
   - Seedance/Higgsfield provider export.
6. Do not promote provider-specific instructions into the core Video Medium Plan. Keep "still frame first, approve, animate" as package logic and provider export as the final stage.
