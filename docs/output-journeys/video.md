# Video Journey

The Video Journey translates an approved Beat Plan into time-based visual work. The v0 implementation is storyboard-ready planning only: it creates a Video Medium Plan with sequences, scenes, Storyboard Shots, shot list, motion, transitions, audio posture, text/audio references, and storyboard frame prompts. It does not generate finished video.

Video uses the shared visual planning language from the Image Journey. **Image Role** and **Storyboard Shot** are sibling realizations of a shared **Visual Unit**: an image realizes the unit as a still frame, while video adds time, motion, blocking, transitions, and script or audio relationships.

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

The Video Medium Plan is scale-general. It can support short social videos, single scenes, trailers, music videos, short films, feature films, episodic sequences, and other storyboardable video work. Long-form video uses Workflow Scale Routing and Long-Work Stewardship; it is not a separate artifact class.

## Route

```text
Approved Beat Plan with Project-Level Workflow Scale Routing
  -> Long-Work Stewardship Record, when Workflow Scale Routing activates it
  -> Symbology Gate
  -> Style Gate
  -> Video Format Gate
  -> Scene / Sequence Gate
  -> Shot Logic Gate
  -> Reference Strategy Gate, when characters, locations, or objects need continuity
  -> Motion / Pacing / Transition Gate
  -> Audio Posture Gate
  -> Video Medium Plan with Medium-Level Workflow Scale Routing
  -> Draft Video Creative Brief Document
  -> Video Critic Review
  -> Brief Approval Gate
  -> storyboard-ready package
  -> optional composite storyboard sheet Generation Approval Gate, default generated storyboard artifact
  -> Output Record, when a composite storyboard sheet is generated or imported
  -> optional individual storyboard still Generation Approval Gate, only when explicitly requested
  -> Output Record, when individual storyboard stills are generated or imported
  -> Output Critic Review
  -> Output Acceptance Gate
```

## Gates

- Symbology Gate: what should the work show as the core symbolic representation?
- Style Gate: what visual language should carry the meaning?
- Video Format Gate: short social video, single scene, trailer, montage, music video, short film, feature film, episodic sequence, or another format?
- Scene / Sequence Gate: does this need Video Sequences, Video Scenes only, or long-form stewardship?
- Shot Logic Gate: how does each Beat, Beat group, or Tension Point become timed Storyboard Shots?
- Reference Strategy Gate: which main characters, locations, objects, products, or props should be promoted into reference status before storyboard lock?
- Reference Readiness Gate: are required reference outputs accepted or explicitly waived before storyboard export?
- Motion / Pacing / Transition Gate: what moves, how fast do shots unfold, and how do they connect?
- Audio Posture Gate: silent, music-only, voiceover-led, dialogue-led, sound-design-led, mixed, or deferred?
- Workflow Scale Routing: should this stay compact, expand as a structured single artifact, or activate cumulative/full long-form supports?

## Reviews

- Story Critic Review happens before this journey as a bounded sub-agent review.
- Beat Reviewer sub-agent is mandatory for scene, sequence, trailer, arc, or long-form video plans.
- Video Critic Review checks shot progression, scene pacing, motion logic, transition logic, visual continuity over time, and script or audio alignment against Artist Meaning, Beat Plan, and Video Medium Plan.
- Art Critic Review criteria may support Video Critic Review when visual style, symbology, composition, or Visual Dynamics are unresolved.
- Writing Critic Review criteria may support Video Critic Review when script, dialogue, voiceover, captions, or on-screen text carry meaning.
- Output Critic Review checks generated or imported composite storyboard sheets, explicitly requested individual storyboard stills, or later generated video artifacts against Artist Meaning, Beat Plan, Video Medium Plan, and the approved plan that produced them.

## Current Implementation

The current Video Journey v0 implements a schema-backed Video Medium Plan and validates a compact fixture. Storyboard frame prompts belong to the Video Medium Plan. Requested storyboard generation defaults to one composite multi-panel storyboard sheet; individual panel stills are a separate artifact type that require explicit separate approval. A separate Video Prompt Plan waits until provider-neutral video generation instructions prove their fields.

Generated or imported composite storyboard sheets and individual storyboard stills are normal Output Records linked back to the relevant Video Medium Plan and, for individual stills, the relevant Storyboard Shot. Finished video generation, Remotion rendering, and provider-specific video jobs are future adapters; they consume Video Medium Plan data but do not define the domain model.

## Video-Specific Concerns

Video cannot rely on mood words alone. It needs decisions about:

- duration,
- aspect ratio,
- sequence and scene structure,
- shot count,
- camera movement,
- subject movement and blocking,
- scene continuity,
- promoted reference packages for main characters, locations, objects, products, or props,
- temporal order,
- transition behavior,
- visual consistency over time,
- audio posture,
- script, voiceover, dialogue, caption, or on-screen text timing,
- whether the output loops or resolves.

Longer video should use Long-Work Stewardship, checkpoints, and calibration before broad expansion. Do not create generated clips, composite storyboard sheets, or storyboard stills without explicit approval. Do not create individual storyboard stills unless the artist explicitly requests separate panel images.
