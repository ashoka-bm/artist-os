# Draft Decision 0019: Video Funnel Current End State

## Status

Draft, from grilling session.

## Decision

For the current implementation, the Video Journey should not require the artist to choose a fully specified final delivery target at the start.

When the artist chooses the video funnel, Artist OS should clearly state that the current funnel ends at generated or prepared source material:

- video clip prompts and generated/imported video clips,
- voice-over prompt preparation and generated/imported voice-over audio,
- music or sound prompt planning and generated/imported sound outputs,
- storyboard and reference materials when needed.

Assembly into a finished video remains outside the current implemented funnel. The artist can assemble the source material in their preferred editor.

## Rationale

Artist OS is still building the full video funnel. Requiring a final assembly target too early would force product decisions that are not implemented yet and could make the system overpromise finished-video delivery.

The useful early promise is narrower: choose Video when the work needs time-based source material. Artist OS will guide the artist through story, storyboard, provider-ready packages, explicit generation approval, and Output Records for generated or imported ingredients.

## Consequences

- Early Video Orientation should set expectations instead of asking for a final editor/export target.
- Provider routes such as Seedance, Suno, and ElevenLabs can be selected later when the needed source-material layers are known.
- The post-storyboard production layer should produce source-material packages, not a finished Assembly Plan by default.
- Finished assembly can remain a future route or optional planning note until implemented.

## Open Questions

- What is the shortest artist-facing wording for this boundary?
- Should the funnel still collect optional assembly notes for future use, such as target platform, aspect ratio, or intended editor?
- At what point should Artist OS ask whether the source-material set includes video-only, video plus voice-over, video plus music, or all three?
