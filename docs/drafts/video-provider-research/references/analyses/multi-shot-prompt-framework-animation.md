# Multi-Shot Prompt Framework Animation Analysis

## Reference

- Reference id: `ref_multi_shot_prompt_framework_animation_001`
- Title: `Multi-Shot Prompt Framework Animation`
- Source path: `/Users/ashokaji/Downloads/multi-shot-prompt-framework-animation (1).md`
- Date analyzed: 2026-06-24
- Provider or platform: Seedance, Kling, Wan, Hailuo, Veo, Runway, Luma, Higgsfield
- Reference type: animation prompt-builder framework
- Reuse policy: analyze and rewrite in Artist OS language

## What It Is

This reference defines a compact prompt contract for animated multi-shot scenes. It produces a ready-to-paste provider prompt with timecoded shots, camera specs, dialogue embedded in action, location metadata, and a fixed audio line. The key constraint is length: the final prompt must stay under 1,500 characters.

## Video Types

- Multi-shot animated scene.
- Dialogue-led animated beat.
- Cinematic animated scene breakdown.
- Short action, comedy, surreal, or contemplative scene.

## Assumed Inputs

- Character description or character reference image.
- Action or script.
- Location.
- Time of day.
- Optional dialogue.
- Target animation style.

## Prompt Structure

The prompt is always a 15-second sequence. It uses 3 to 7 shots. Each shot has a timecode stamp, shot size, lens equivalent, camera angle, and camera movement. Shot duration ranges from 2 to 5 seconds. Each paragraph is one shot, and the final prompt ends with `Location:` and `Audio:` metadata.

The framework requires visual rhythm. Consecutive shots should vary size, lens, angle, and movement. Dialogue belongs inside the shot where it lands, never in a separate transcript block.

## Reusable Patterns

- A provider export can be a compressed rendering of the richer Video Medium Plan.
- Character identity can be distributed across shots instead of front-loaded.
- Shot design can be forced into concise technical syntax.
- Dialogue timing can be preserved by embedding lines in shot paragraphs.
- A hard character limit can be part of a provider-target export contract.
- The trim order matters: cut adjectives before cutting timecodes, dialogue, or camera specs.

## Failure Modes

- The prompt exceeds provider length limits and loses important instructions.
- A scene defaults to one repeated shot grammar instead of edited visual rhythm.
- Dialogue is listed separately and loses timing.
- Too many lines are forced into 15 seconds.
- Character description is dumped once and then lost across later shots.
- Location or audio metadata is omitted.

## Conflicts

The fixed 15-second contract is useful for a prompt framework but should not become a universal Artist OS rule. Artist OS Video Medium Plans can support any scale. The 1,500-character limit belongs to a provider export mode or compact prompt renderer.

## Mapping To Artist OS

- Video Medium Plan already stores scenes, shots, time ranges, camera movement, blocking, and audio refs.
- This framework maps to a compact `provider_prompt_text` renderer after storyboard approval.
- Shot size, lens, angle, and movement map to Shot Design plus `camera_movement`.
- Dialogue maps to Text Journey blocks and `script_ref`.
- Location metadata maps to Video Scene setting and time of day.

## Draft Fields To Consider

- `compact_prompt_char_limit`
- `shot_count`
- `shot_duration_rule`
- `technical_shot_syntax_required`
- `dialogue_inline_required`
- `location_metadata_line`
- `audio_metadata_line`
- `trim_priority`

## Open Questions

- Which providers actually need the 1,500-character ceiling?
- Should the compact renderer always produce exactly 15 seconds, or accept duration from the Video Medium Plan?
- Should lens equivalents be stored in neutral Shot Design or only emitted at export?
- How should the renderer handle scripts too long for the target duration?
