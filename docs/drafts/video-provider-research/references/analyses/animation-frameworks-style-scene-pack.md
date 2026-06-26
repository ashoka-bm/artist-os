# Animation Frameworks Style And Scene Pack Analysis

## Reference

- Reference id: `ref_animation_frameworks_style_and_scene_pack_001`
- Title: `Animation Frameworks, Style Build, Character Sheet, Location Sheet, Scene Prompts`
- Source path: `/Users/ashokaji/.codex/attachments/27479c05-b3d0-4183-8493-9b37073651b3/pasted-text.txt`
- Date analyzed: 2026-06-24
- Provider or platform: GPT Image 2 and Seedance-style video prompting
- Reference type: reference-sheet and scene prompt examples
- Reuse policy: analyze and rewrite in Artist OS language; do not copy scene examples into production docs

## What It Is

This reference shows a fuller animation asset pipeline. It starts with style build and character sheet prompts, adds a location reference sheet, creates still image prompts for several scenes, then creates matching timecoded video prompts. It is useful because it separates reusable visual assets from scene-specific prompts.

## Video Types

- Flat 2D cartoon scene.
- Comedic animated short.
- Dialogue-led multi-character scene.
- Location-based animated scene pack.
- Still-to-video scene realization.

## Assumed Inputs

- Character description.
- Target cartoon or animation style.
- Character sheet.
- Location reference sheet.
- Scene still prompts.
- Video prompt requirements.
- Optional dialogue lines or audio/video refs.

## Prompt Structure

The reference uses a layered structure:

- Style build prompt: establishes the look.
- Character sheet prompt: four views for character continuity.
- Location reference sheet prompt: four views with negative space for character placement.
- Still scene prompts: one image prompt per scene using the same character, clothes, and style.
- Video prompts: timecoded shot paragraphs with camera specs, action, location, and audio metadata.

## Reusable Patterns

- Character and location sheets can be prepared before scene generation.
- Location sheets should reserve negative space for natural character placement.
- Still scene prompts can function as scene calibration artifacts before video.
- Video prompts can realize a still-scene idea through timed shots.
- Scene packs can share a character, style, and visual grammar while varying setting and action.
- Dialogue-led animated scenes may reference separate audio/video clips per speaker or line.

## Failure Modes

- The character sheet contains visible labels or text that later bleeds into generated scenes.
- Location sheets include characters, making later placement less flexible.
- Location panels have inconsistent lighting or style.
- Scene prompts drift from the approved character or style.
- Video prompts over-pack action into very short shot durations.
- Dialogue/audio references become unclear when several speakers are present.

## Conflicts

Some example content is comedic and scene-specific; it should not become generalized product language. The useful part is the asset pipeline and prompt contract, not the individual gag content.

## Mapping To Artist OS

- Style build maps to Style Direction and style calibration.
- Character sheet maps to Visual Reference Sheet Plan and Output Records.
- Location sheet may need a future Setting Reference Sheet Plan or a generalized Visual Reference Sheet Plan role.
- Still scene prompts map to storyboard stills or calibration Output Records.
- Video prompts map to provider-target compact multi-shot exports.

## Draft Fields To Consider

- `style_build_prompt`
- `character_sheet_ref`
- `location_sheet_ref`
- `scene_still_ref`
- `scene_pack_id`
- `negative_space_requirements`
- `speaker_audio_refs`
- `compact_video_prompt_ref`

## Open Questions

- Should location reference sheets become a first-class Artist OS artifact?
- Should scene still prompts always be generated before multi-shot video exports?
- How should multi-speaker dialogue refs be represented in provider exports?
- How much of this belongs in the post-storyboard provider layer versus upstream Video Medium Plan?
