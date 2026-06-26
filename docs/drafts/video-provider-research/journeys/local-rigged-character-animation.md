# Draft Journey: Local Rigged Character Animation

Status: research draft.

## End Product

A deterministic animated character video built from reusable character specs, rig plans, pose libraries, action timelines, backgrounds, audio, and a browser-rendered composition.

## Likely Inputs

- Character Template or approved character concept.
- Script with action beats.
- Video Storyboard.
- Style Direction.
- Required emotions, actions, props, and backgrounds.
- Runtime choice such as HyperFrames, Remotion, or a comparable local animation backend.

## Prompt Or Production Needs

- Character design with silhouette, role, emotional range, and required actions.
- Rig plan with parts, pivots, layers, views, and constraints.
- Pose library.
- Scene plan with timed actions and camera/framing.
- Asset manifest for character parts, backgrounds, props, audio, and effects.
- Action timeline.
- Motion QA for readability, timing, and rig integrity.

## Known Risks

- Character acting is planned as narration-only instead of visible action.
- Rig complexity exceeds the approved budget or sample.
- One-off code paths make characters hard to reuse.
- Required emotions lack pose support.
- Renderer choice is made after design decisions that depend on it.

## Artist OS Mapping

This should stay separate from Seedance-style generated character clips. It is closer to a deterministic animation adapter that turns approved Storyboard Shots into rigged motion.
