# Video Journey

The Video Journey translates an approved Beat Plan into time-based visual work: a single motion moment, a short clip, a scene, a sequence, a trailer, or a longer arc.

## Best Fit

Use the Video Journey when the final work should include:

- motion,
- scene progression,
- camera or subject movement,
- transitions,
- performance,
- time-based reveal,
- montage,
- visual rhythm,
- a longer emotional arc.

## Route

```text
Approved Beat Plan with Project-Level Workflow Scale Routing
  -> Video Format Gate
  -> Scene / Sequence Gate
  -> Shot Logic Gate
  -> Motion Gate
  -> Visual Style Gate
  -> Pacing / Transition Gate
  -> Video Plan with Medium-Level Workflow Scale Routing, when schema-backed
  -> Video Critic Review
  -> Video Prompt Plan
  -> Prompt Critic Review
  -> Prompt Lock Gate
  -> Generation Approval Gate
  -> Output Critic Review
  -> Output Acceptance Gate
```

## Gates

- Video Format Gate: single clip, scene, sequence, trailer, loop, or longer arc?
- Scene / Sequence Gate: how many beats become timed units?
- Shot Logic Gate: what is the camera relationship to each beat?
- Motion Gate: what moves, how much, and why?
- Visual Style Gate: what visual language carries the Beat Plan?
- Pacing / Transition Gate: how fast do beats unfold and how do they connect?
- Workflow Scale Routing: should this stay one clip or scene, or does it need sequence, calibration, Long-Work, or full long-form support?
- Calibration Gate: for longer video, approve a style/motion test before full production.

## Reviews

- Story Critic Review happens before this journey as a bounded sub-agent review.
- Beat Reviewer sub-agent is mandatory for scene, sequence, trailer, or arc plans.
- Video Critic Review checks whether shot progression, motion, pacing, and transition logic preserve the Beat Plan as a bounded sub-agent review.
- Art Critic Review sub-agent may be used inside Video Critic Review when visual style or image composition is unresolved.
- Prompt Critic Review checks video prompt readiness, continuity constraints, shot clarity, provider-neutral language, and generation risks as a bounded sub-agent review.
- Output Critic Review checks generated video against Artist Meaning, Beat Plan, Video Plan, and Prompt Plan as a bounded sub-agent review.

## Video-Specific Concerns

Video cannot rely on mood words alone. It needs decisions about:

- duration,
- aspect ratio,
- shot count,
- camera movement,
- subject movement,
- scene continuity,
- temporal order,
- transition behavior,
- visual consistency,
- whether the output loops or resolves.

Longer video should use calibration before full generation. Do not create many generated clips without explicit approval.
