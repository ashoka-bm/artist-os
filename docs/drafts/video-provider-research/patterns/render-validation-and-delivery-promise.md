# Draft Pattern: Render Validation And Delivery Promise

Status: research draft.

OpenMontage treats the final render as an artifact that must be inspected before it is presented. It checks duration, frame validity, audio, subtitles, and whether the output kept the promised video type.

## Draft Principle

A finished video should be checked against its delivery promise, not only against file existence. If the promise was motion-led, source-led, dialogue-led, graphic-led, or real-footage-based, the review should test that promise directly.

## Possible Checks

- File exists and passes ffprobe.
- Duration matches planned runtime.
- Resolution and aspect ratio match target platform.
- Sampled frames are not black or broken.
- Captions are present when promised.
- Audio is not silent or clipping.
- Music or narration posture matches the plan.
- Overlays are readable.
- Source/generated balance matches the approved route.
- Slideshow risk is low when a motion-led video was promised.

## Artist OS Mapping

This belongs after provider generation or local rendering. A render report can feed an Output Record and a Video Output Critic Review, but it should not be required for storyboard-only work.
