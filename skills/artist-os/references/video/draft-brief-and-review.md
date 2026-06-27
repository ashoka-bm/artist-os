# Draft Video Creative Brief And Video Critic Review

## Draft Video Creative Brief Process

Use this only after the Video Medium Plan exists. Before Video Critic Review, build a substantive draft brief from the Video Medium Plan:

1. Preserve `transformation_brief_id`, `beat_plan_id`, and `video_medium_plan_id`.
2. Use the Video Medium Plan as the source of truth for Narrative Depth, Story or Micro-Journey Template refs, Asset Purpose Brief when present, Video Format, Video Style Expression, Visual Dynamics, sequences, scenes, Storyboard Shots, Video Audio Posture, text/audio refs, and storyboard generation policy.
3. Add Artist Meaning, formal observations, Emotional Qualities, Poetic Density Notes, transformation constraints, and review requirements.
4. Make the v0 boundary explicit: storyboard-ready planning only, no finished video generation.

If running standalone, recommend Video Critic Review. If the `artist-os` conductor is running, return the draft and stop; the conductor advances automatically.

## Video Critic Review

Use Video Critic Review before Brief Approval. Review only the bounded packet: Artist Meaning, Transformation Brief, Beat Plan, Video Medium Plan, draft Video Creative Brief Document, any supporting Text or Sound refs, and open questions.

Check:

- shot progression across adjacent Storyboard Shots,
- whether camera angle, shot scale, and camera movement serve the emotional job of the Beat instead of acting as decorative coverage,
- whether aspect ratio is explicit and preserved across storyboard frame prompts, planned reference outputs, and any requested storyboard generation policy,
- scene pacing and sequence pacing,
- motion logic,
- transition logic,
- visual continuity over time,
- script/audio/shot alignment,
- whether each Storyboard Shot preserves its smallest Story Beat, Intended Feeling, Expectation Turn Translation, and Shot Design,
- whether any Story Movement has been compressed into a single shot or panel without explicit artist approval,
- for `full_story`, whether Video Scenes and Storyboard Shots preserve the adapted Story Structure's key turns rather than replacing them with video-only sequence logic,
- whether promoted continuity-critical visual states remain consistent across adjacent Storyboard Shots and composite storyboard panels,
- whether Video Audio Posture is explicit and sufficient,
- whether long-form expansion needs Long-Work Stewardship before more parts are planned,
- whether storyboard frame prompts are provider-neutral and do not imply finished video generation,
- whether any requested storyboard generation defaults to one composite multi-panel storyboard sheet unless individual stills were explicitly requested,
- whether Character Templates and Visual Reference Sheet Plans, if used, are aligned with shot continuity and not silently invented.

Use Art Critic, Writing Critic, or Sound Critic criteria as supporting checks when those layers carry risk, but Video Critic Review owns the integrated time-based judgment. Emit a Review Record against `schemas/review-record.schema.json` with `review_role = "video_critic"`.
