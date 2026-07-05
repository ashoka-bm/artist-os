# Draft Decision 0021: Source Material Intent Record Placement

## Status

Draft, from grilling session.

## Decision

Source Material Intent should be split across the video funnel:

- Video Orientation captures a recommendation-first `source_material_intent_recommendation`.
- Video Medium Plan records the authoritative current `source_material_intent`, including whether the orientation recommendation was accepted, revised, deferred, or superseded.
- Post-storyboard production routing turns the final current intent into concrete provider package work.

Provider-specific packages remain downstream:

- Seedance packages for video clip source material.
- Suno packages for music, song, score, or sound source material.
- ElevenLabs packages for voice-over or dialogue source material.

## Rationale

Source Material Intent must be visible early enough to guide planning, especially audio posture, shot timing, and script/dialogue needs. But it should not become final before the storyboard clarifies what source material the work actually needs.

Putting the authoritative version in the Video Medium Plan lets the plan reconcile early direction with later story, pacing, and audio decisions. Keeping provider packages downstream preserves the provider boundary and avoids making Seedance, Suno, or ElevenLabs shape the core story too early.

## Consequences

- The conductor needs recommendation-first Video Orientation wording for source-material layers.
- The Video Medium Plan schema likely needs a `source_material_intent` block.
- The post-storyboard production route should read the Video Medium Plan and ask only for missing package decisions.
- Provider package generation remains explicitly approved per provider call or batch.

## Open Questions

- What fields should `source_material_intent` contain?
- Should the Source Material Intent block include confidence and rationale?
- Should the system record declined layers, such as "no voice-over" or "no music", so later agents do not re-ask?
