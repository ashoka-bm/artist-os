# Draft Decision 0018: Post-Storyboard Production Packages

## Status

Draft, from grilling session.

## Decision

After storyboard approval, Artist OS should create a post-storyboard production layer that prepares provider-ready ingredient packages before any finished-video assembly plan.

The initial package families are:

- Seedance video prompt packages for generated video clips.
- Suno prompt packages for generated music, song, score, or sound layers.
- ElevenLabs voice-over prompt packages for generated narration or dialogue audio.

These packages generate or prepare ingredients. They do not equal a finished assembled video.

Finished-video assembly belongs in a separate downstream Assembly Plan after required clips, music, voice-over, captions, stills, or imported assets exist as Output Records.

## Rationale

Seedance, Suno, and ElevenLabs do not share the same output contract. A Seedance package maps storyboard shots and visual references to video prompts. A Suno package maps approved sound intent to platform renderings. An ElevenLabs package prepares approved spoken text for TTS delivery. Treating them as one generic prompt would blur provider boundaries and weaken traceability.

Separating ingredient packages from assembly lets Artist OS guide the user automatically through each needed provider route while preserving explicit provider-generation approval. It also prevents a prompt-preparation step from implying that Artist OS has rendered, selected, edited, mixed, or exported a finished video.

## Consequences

- The Video Journey needs a post-storyboard routing step that asks what production layers are needed: video clips, music or sound, voice-over, captions/text, imported media, or assembly only.
- Seedance prompt packages can remain provider-specific post-storyboard exports.
- Suno packages should reuse the Sound Journey and Sound Prompt Plan platform-rendering boundary rather than invent a video-owned Suno schema.
- ElevenLabs voice-over packages require approved spoken text before prompt preparation.
- Assembly Plan work should wait until generated or imported ingredients have Output Records, unless the user is only drafting a future assembly plan.

## Open Questions

- Should the umbrella record be called `VideoProductionPlan`, `PostStoryboardProductionPlan`, or `ProductionPackagePlan`?
- Does the first implementation need a schema-backed Assembly Plan, or only route docs plus provider package schemas?
- Should captions and on-screen text become a fourth post-storyboard package family now, or stay in Text Journey until assembly work begins?
