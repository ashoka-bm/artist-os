# Draft Pattern: Provider Video Prompt Structure

This pattern describes short-form provider prompts after storyboard approval. It is draft guidance, not the Video Journey contract.

## Core Shape

A provider-target prompt often needs these sections:

- Format: duration, shot family, and one-line concept.
- Subject: identity or main visual authority.
- Wardrobe: visible clothing and continuity details.
- Props: only named props that matter to the shot.
- Environment: setting, light, ambience, and fixed spatial facts.
- Style anchor: camera look, lens behavior, color, realism, and texture.
- Delivery: dialogue, lip-sync, no dialogue, or audio relationship.
- Logic rule: continuity, shot count, camera constraints, reference scope, and anti-failure guards.
- Negative prompt: short list of specific exclusions.
- Action: time-based performance, blocking, camera movement, and shot progression.

## Shot Families

Single continuous shots use one action header and flowing action prose. They are the best fit for talking heads, vlogs, walk-throughs, dialogue scenes, and other one-take performances.

Multi-cut b-roll uses separate timed action blocks for each cut. It is the best fit for montage, packing sequences, mirror actions, and deliberate angle changes.

Static observational shots use lock-first language. They are the best fit when any camera drift would break the shot.

Found-footage shots treat the frame as part of the scene. They need careful language so the provider does not render duplicate equipment.

## Translation From Artist OS

The provider prompt should be rendered from approved planning records:

- Video format supplies duration and output shape.
- Video Style Expression supplies camera, motion, edit, color, and light.
- Storyboard Shots supply time ranges, action, movement, blocking, and transitions.
- Shot Design supplies shot scale, camera angle, composition, and visual emphasis.
- Audio Plan and Text Track Refs supply dialogue, voiceover, lip-sync, or no-dialogue posture.
- Traceability notes preserve the link back to Artist Meaning and Beat Plan.

## Compact Animation Shape

Some animated workflows use a shorter prompt shape when strong visual references already exist:

- Style: target animation language and rendering texture.
- Action: what the subject does from start to finish.
- Camera: camera path, lens feel, motion speed, and cut behavior.
- Environment: only when it is not already controlled by the frame or storyboard reference.

Use this compact shape only in provider-target drafts. The neutral Video Medium Plan should still hold the full storyboard, motion, blocking, transition, and traceability data.

## Compact Multi-Shot Shape

Another animation export shape compresses the plan into timed shot paragraphs:

- `[MM:SS - MM:SS]` timecode.
- Shot size.
- Lens shorthand.
- Camera angle.
- Camera movement.
- Action and dialogue in one paragraph.

This is useful when the provider prompt has a strict length limit. It should be generated from approved shots, not invented as a replacement for Video Medium Plan review.

The same shape can apply to cinematic/live-action prompts. In that case, `Style` and `Audio` metadata should be rendered from approved Video Style Expression and Audio Plan rather than copied from a fixed framework default.

## Seedance Cinematic Shape

Seedance cinematic exports may require a stricter provider-specific shape:

- one selected scene or selected shot batch;
- scene header with shot count and 24fps;
- Chinese prompt body, with dialogue and provider tags left in the provider-expected form;
- flat shot numbering rather than beat headers;
- no per-shot durations inside the shot text;
- shot count derived from total duration, with six shots as the default maximum;
- mirrored English review translation that preserves the same tags and shot structure;
- one recommended duration line after the translation.

This shape belongs in the Seedance renderer. It should not replace the neutral storyboard or Video Medium Plan.

## Fashion Campaign Shape

Fashion campaign exports can compress the sequence into one flowing paragraph:

- Shot specs remain mandatory.
- `Cut to.` separates shots.
- The garment leads the description.
- The model moves in every shot.
- At least one wide uses deliberate negative space.
- At least one closer shot carries direct attitude.

Use this only when the work is garment-led or fashion/editorial. General cinematic prompts should not inherit its streetwear assumptions.
