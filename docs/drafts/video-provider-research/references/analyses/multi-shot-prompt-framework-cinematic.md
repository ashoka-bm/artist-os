# Multi-Shot Prompt Framework Cinematic Analysis

## Reference

- Reference id: `ref_multi_shot_prompt_framework_cinematic_001`
- Title: `Multi-Shot Prompt Framework`
- Source path: `/Users/ashokaji/Downloads/multi-shot-prompt-framework.md`
- Date analyzed: 2026-06-24
- Provider or platform: Seedance, Kling, Sora, Veo, Runway, Luma, Hailuo, Wan, Higgsfield
- Reference type: cinematic prompt-builder framework
- Reuse policy: analyze and rewrite in Artist OS language

## What It Is

This reference is the cinematic/live-action sibling of the multi-shot animation framework. It turns an uploaded reference image and scene brief into a compact 15-second cinematic video prompt with timecoded shots and fixed metadata lines for location, style, and audio.

## Video Types

- Multi-shot cinematic scene.
- Reference-image-driven scene expansion.
- Short action, reveal, atmosphere, transformation, or surreal sequence.
- Live-action or grounded-realism provider prompt.

## Assumed Inputs

- Uploaded reference image.
- Subject or character identity inferred from that image.
- Action.
- Location.
- Time of day.
- Desired scene mood or cinematic intention.

## Prompt Structure

The output is always under 1,500 characters. It uses 3 to 7 shots totaling exactly 15 seconds. Each shot has a timecode, shot size, lens, camera angle, and camera movement. The final block includes three metadata lines: `Location`, fixed cinematic `Style`, and fixed diegetic `Audio`.

The framework treats lens and camera language as the main control surface. It emphasizes visual rhythm by varying shot size, lens, angle, and movement across consecutive shots.

## Reusable Patterns

- Uploaded reference images can be condensed into a short subject description used across shots.
- Multi-shot provider exports can be character-limited without losing timecodes and camera grammar.
- Fixed metadata lines can enforce a house style or provider-oriented default.
- The shot sequence can be designed from action intensity: fewer longer shots for contemplative scenes, more shorter shots for fast scenes.
- The prompt can preserve copy-paste usability by avoiding headers and lists inside the provider block.

## Failure Modes

- The fixed style line may override the user's desired style if applied blindly.
- The 15-second contract may not fit every Video Medium Plan.
- A reference image can be over-described and waste the character budget.
- The prompt may become camera-rich but emotionally thin if it does not preserve Beat Plan intent.
- Multiple characters can become cramped if introduced in one shot.

## Conflicts

The fixed "Christopher Nolan" style line is a framework default, not an Artist OS default. Artist OS should not hardcode a named-director style into general provider exports. If this pattern is promoted, the fixed style line should become a configurable style metadata line derived from approved Style Direction.

## Mapping To Artist OS

- The uploaded reference maps to Source Record, Character Template, Visual Reference Sheet, or Output Record depending on provenance.
- The 15-second shot sequence maps to Video Medium Plan Storyboard Shots.
- The final `Location` line maps to Video Scene setting and time of day.
- The final `Style` line maps to Video Style Expression.
- The final `Audio` line maps to Audio Plan.
- The character limit maps to a provider export renderer, not core planning.

## Draft Fields To Consider

- `reference_image_summary`
- `compact_prompt_char_limit`
- `fixed_or_configurable_style_line`
- `cinematic_metadata_block`
- `style_line_source`
- `subject_description_budget`
- `shot_variation_rule`

## Open Questions

- Which providers require or benefit from fixed metadata lines?
- Should Artist OS support named-director style references, and how should copyright/style-sensitive language be handled?
- Should the compact renderer accept a duration other than 15 seconds when the Video Medium Plan requires it?
- How should Beat Plan emotion be preserved under a strict character limit?
