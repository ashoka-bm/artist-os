# Utility Sequence Walkthrough: AI Workflow Toolkit Loop

Status: research draft.

Purpose: test `narrative_depth = utility_sequence` with a non-motion-graphics utility asset: a reusable B-roll loop / product spin / transition plate for creator explainer videos.

This is not a canonical Video Medium Plan, schema fixture, Creative Brief, Prompt Plan, storyboard still, provider export, or finished video.

## Test Case

A 6-8 second looping B-roll asset shows an approved still/frame of a creator's AI video workflow toolkit transforming into a subtle animated product spin, timeline insert, or transition plate. The asset supports future creator explainer videos. It is not meant to stand alone as a story.

## Routing

Narrative Depth: `utility_sequence`

Format Intent: reusable B-roll loop / product spin / transition plate

Accepted Output Shape: `other`, recorded as "reusable B-roll utility asset"

Format modifiers:

- `explainer_clip`
- `performance_clip`, only if the creator or host appears in the approved still

Story Structure: not required.

Micro-Journey Template: not required.

Asset Purpose Brief: required.

Provider Route: not selected. Seedance, Higgsfield, Runway, Sora, Veo, Remotion, HyperFrames, or other renderer choices remain downstream provider/export notes after storyboard approval.

## Asset Purpose Brief

Role / Use Context: reusable insert asset for creator explainer videos. It can bridge a talking-head section into a workflow explanation, sit under voiceover, open a process section, or serve as a transition plate between idea, still frame, animation, and finished B-roll.

Standalone Or Larger Work: belongs inside larger creator explainers. It should still function as a clean visual loop in an asset library, but it does not need its own story arc.

Subject: approved still/frame of the creator's AI video workflow toolkit.

Visual Purpose: make the workflow feel concrete, polished, and repeatable while preserving the approved still as the visual anchor.

Placement:

- between talking-head explanation and workflow breakdown;
- over narration about still-frame approval;
- as a short transition into B-roll examples;
- as a recurring visual motif in future creator explainers.

Duration Target: 6-8 seconds.

Shot / Asset Count: one utility asset with one to three storyboard states:

1. approved still/frame state;
2. subtle transformation or product-spin/timeline-insert state;
3. return or hold state for loopability.

Motion Behavior:

- subtle animated product spin, orbit, parallax, or timeline-slide behavior;
- no aggressive camera move;
- no new story event;
- motion should reveal utility and dimensionality, not create plot.

Loop / Resolution Behavior:

- preferred behavior: seamless or near-seamless loop back to the approved still/frame;
- acceptable behavior: resolve to a held transition plate that can cut into the next explainer section;
- avoid a hard ending that makes the asset feel like a complete standalone story.

Style Constraints:

- preserve the approved still/frame's composition and visual identity;
- keep movement minimal enough that continuity and object clarity survive;
- use clean creator-toolkit polish rather than abstract AI spectacle;
- avoid adding unrelated futuristic UI, random glowing circuits, unreadable panels, or fake platform interfaces.

Audio / Text Posture: silent by default. No music, subtitles, or voiceover inside the raw asset. If text labels are part of the approved still, preserve them; do not invent new script or caption wording.

Reference / Continuity Needs:

- approved still/frame as anchor;
- visual style reference for the creator toolkit;
- object/product reference if the toolkit has identifiable components;
- optional final-frame reference if exporting as multiple provider segments;
- optional brand/type/color reference if used across future explainers.

Success Criteria:

- the asset can loop or resolve cleanly in 6-8 seconds;
- the approved still remains recognizable;
- the toolkit reads as a concrete workflow object, not generic AI decoration;
- the motion adds usability: transition, emphasis, polish, dimensionality, or continuity;
- the asset can be reused under narration without competing with it;
- no fake conflict, character arc, or story turn is invented.

Downstream Export Notes:

- provider preferences are non-binding until storyboard approval;
- if using Seedance or another short-form video generator, keep the prompt focused on subtle movement, continuity, and loop/hold behavior;
- if using last-frame continuation, do it only during provider export after storyboard approval;
- if using Remotion, HyperFrames, or another code renderer, preserve the same asset role and loop criteria;
- mention frame rate, camera, lighting, no subtitles, no music, film grain, or language experiments only in provider export, not in core story fields.

## Utility Sequence Item

### Reusable AI Workflow Toolkit Loop

Purpose: create a reusable B-roll insert that turns one approved still/frame into a subtle animated asset for future creator explainers.

Visual Arc: still/frame anchor -> gentle product spin or timeline insert -> return/hold transition state.

Motion Notes:

- start from the approved still/frame;
- introduce a controlled orbit, parallax layer, product spin, or timeline slide;
- reveal no more than one added spatial or process relationship;
- return to the still-like composition or hold on a clean transition plate.

Use Cases:

- section transition;
- under-voiceover B-roll;
- workflow proof insert;
- recurring visual motif;
- bridge between still-frame approval and animation examples.

Avoid:

- adding story beats;
- adding unrelated UI;
- making the toolkit look different from the approved still;
- making motion so complex that the asset cannot loop or be reused.

## Storyboard Scope

Recommended storyboard package: one 3-panel composite storyboard sheet.

Panel 1: approved still/frame anchor.

Panel 2: subtle spin/timeline-insert transformation.

Panel 3: loop return or transition hold.

Storyboard requirements:

- preserve the approved still's composition;
- label loop direction or hold behavior;
- show what moves and what remains locked;
- state whether this is intended as seamless loop or transition plate;
- keep provider instructions out of storyboard frame prompts except as non-binding export notes.

Do not generate storyboard stills, animation, or finished video without explicit Generation Approval.

## Video Medium Plan Carry-Forward

The Video Medium Plan should carry:

- `narrative_depth`: `utility_sequence` in rationale or traceability notes until a field exists;
- accepted output shape: reusable B-roll utility asset;
- Asset Purpose Brief;
- role/use context: insert, loop, product spin, timeline insert, transition plate;
- duration target: 6-8 seconds;
- storyboard scope: one 3-panel composite sheet by default;
- loop/resolution behavior;
- silent audio posture;
- text posture: preserve existing approved-still text only;
- reference needs: approved still/frame, style reference, object/toolkit reference if needed;
- provider preferences: non-binding downstream notes only.

## Risks / Gaps In Current Framework

- `utility_sequence` remains guidance, not a schema field.
- `video_output_shape` lacks direct values for reusable B-roll loop, product spin, transition plate, or asset-library insert.
- `storyboard_shots` require Beat and Key Emotional Movement refs, which may be heavy for a one-asset loop.
- The current utility guidance says success criteria and loop/resolution behavior, but Video Critic Review does not yet explicitly check loop quality, reusability, or whether motion adds functional value.
- A pure utility asset still needs Intended Feeling and traceability, but the framework should avoid inflating that into false story movement.

## Recommendations Before Promotion

1. Keep Asset Purpose Brief as guidance for now, but this second utility walkthrough strengthens the case for a future `utility_sequence_plan` or `asset_purpose_brief` field.
2. Consider future output-shape values for `b_roll_loop`, `product_spin`, `transition_plate`, or a broader `utility_asset`.
3. Add a future Video Critic Review check for utility assets: loop/hold behavior, reusability, functional value of motion, and preservation of the approved still/reference.
4. Test one more utility case that is not workflow-related, such as a product-only spin, a title-card transition plate, or a texture/atmosphere loop.
5. Do not promote provider-specific loop instructions into the core plan; keep them in provider export.
