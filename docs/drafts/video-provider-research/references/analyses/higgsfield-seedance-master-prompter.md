# Higgsfield / Seedance Master Prompter Analysis

## Reference

- Reference id: `ref_higgsfield_seedance_master_prompter_001`
- Title: `I Clone Master Prompter for Higgsfield`
- Source path: `/Users/ashokaji/Downloads/I_Clone_Master_Prompter_for_Higgsfield.md`
- Date analyzed: 2026-06-24
- Provider or platform: Higgsfield workflow targeting Seedance 2.0-style video generation
- Reference type: prompting guide and failure-mode playbook
- Reuse policy: analyze and rewrite; do not copy wholesale

## What It Is

This reference is the strongest current guide for provider-specific short video prompting after storyboard planning. It focuses on creator-clone video, talking heads, handheld vlogs, static observational shots, and multi-cut b-roll. It teaches prompt shape, shot-family selection, reference scoping, audio handling, and fixes for recurring video-model failures.

## Video Types

- Creator-clone talking head with lip-sync.
- Handheld vlog one-take.
- Found-footage or frame-as-device shot.
- Static observational walk-past.
- Multi-cut cinematic b-roll.
- Same-angle jump-cut montage.
- Mirror, packing, airport, hotel, and travel-style creator content.

## Assumed Inputs

- One identity reference image, usually treated as `@image_1`.
- Optional prop, composition, wardrobe, or style reference images.
- Optional audio file for lip-sync, usually treated as `@audio_1`.
- Exact transcript when dialogue is used.
- A desired duration, shot family, setting, and camera behavior.
- Provider-side generation UI that accepts tagged image and audio references.

## Prompt Structure

The reference uses a stable section order: format, subject, wardrobe, props, environment, style anchor, delivery, logic rule, negative prompt, and action. The most important structural idea is that action formatting changes by shot family. Single continuous shots use one time header and prose flow. Multi-cut b-roll uses one time-bracketed block per cut.

The guide separates style from choreography. Style anchor carries lens, camera identity, color, lighting, realism, and texture. Action carries blocking and performance. Logic rule carries continuity, camera constraints, reference scope, and anti-failure rules.

## Reusable Patterns

- Choose the shot family before writing the prompt.
- Keep dialogue exact and weave it into action beats.
- Trust identity references instead of over-describing the face.
- Scope every reference image by job: identity, prop, composition, style, lighting, or inspiration only.
- Prefer decisive details over alternatives inside the prompt.
- Use lean negative prompts except when a specific provider failure justifies more.
- Treat camera lock, diegetic camera motion, and operator camera motion as separate cases.
- Repeat non-default lighting across several prompt sections when the provider tends to ignore it.
- Match shot scale to fidelity needs; closer framing helps face realism.
- Preserve negative space by describing composition, not by asking the provider to render text.

## Failure Modes

- Duplicate visible camera or phone in found-footage shots.
- Muffled or colored audio when the prompt describes microphone character.
- Frozen subject when a locked tripod also freezes performance.
- Looping gestures across a longer take.
- Camera drift when "cinematic" primes motion despite a lock.
- Unnatural walking mechanics.
- Plastic or generic faces in wide shots.
- Reference bleed from composition or style images.
- Podium or lectern hallucination in informal crowd scenes.
- Cool or neutral lighting when warm light is requested.
- Too many action beats in too short a duration.

## Conflicts

This guide is provider-specific. It should not define the neutral Video Medium Plan. It also corrects some older prompt-pack habits: avoid rich audio-character descriptions for uploaded lip-sync audio, avoid negative prompts that name duplicate cameras unless tests prove they help, and avoid visible-hand camera-placement language when it triggers duplicate equipment.

## Mapping To Artist OS

- `Video Medium Plan.video_format` maps to duration, aspect ratio, and use case.
- `Video Style Expression` maps to camera style, motion style, edit style, and color/light style.
- `Storyboard Shot.time_range` maps to provider time brackets.
- `Storyboard Shot.camera_movement`, `subject_movement`, and `blocking` map to action and logic rules.
- `Storyboard Shot.visual_unit.shot_design` maps to shot scale, camera angle, visual emphasis, and composition.
- `Audio Plan` and `text_track_refs` map to delivery and exact dialogue handling.
- Future provider export records could render a Higgsfield/Seedance prompt from the approved storyboard package.

## Draft Fields To Consider

- `provider_target`
- `shot_family`
- `provider_reference_scope`
- `delivery_line`
- `logic_rule`
- `negative_prompt`
- `action_blocks`
- `known_failure_mode_guards`
- `generation_duration_source`

These belong in a draft provider-target export, not in the neutral Video Medium Plan unless repeated evidence says otherwise.

## Open Questions

- Which rules are Seedance-specific and which generalize to Higgsfield, Runway, Veo, Sora, or other providers?
- Should provider exports be plain Markdown, JSON records, or both?
- How should Artist OS represent uploaded provider tags without binding core records to `@image_1` and `@audio_1` syntax?
- What tests or dry-run fixtures prove that a provider export preserved the storyboard and Artist Meaning?
