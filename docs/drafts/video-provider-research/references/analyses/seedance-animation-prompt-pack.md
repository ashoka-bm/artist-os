# Seedance Animation Prompt Pack Analysis

## Reference

- Reference id: `ref_seedance_animation_prompt_pack_001`
- Title: `Dan Kieft's Seedance 2.0 AI Animation Prompt Pack`
- Source path: `/Users/ashokaji/.codex/attachments/18f50a2a-61c8-4ea3-a069-e5b97ae0a8ec/pasted-text.txt`
- Date analyzed: 2026-06-24
- Provider or platform: Higgsfield, Seedance 2.0, GPT Image 2
- Reference type: animation prompt pack and examples
- Reuse policy: analyze and rewrite in Artist OS language; do not copy examples into production docs

## What It Is

This reference shifts the research from creator-clone realism into animated character production. It shows how a character reference sheet can drive Seedance animation, how start and end frames can define a transition, how a storyboard image can become a video reference, and how restyled character sheets can lock different animation aesthetics before motion.

## Video Types

- Animated character sequence.
- Start-frame to end-frame transition.
- Storyboard-to-video animation.
- Mixed-media scene combining animated and live-action subjects.
- Camera-control test shot.
- Style-restyled animation clip.

## Assumed Inputs

- Character reference sheet generated or approved in GPT Image 2.
- Optional start frame and end frame.
- Optional multi-panel storyboard image.
- Optional live-action person reference.
- Optional environment reference.
- Optional second character, prop, or pursuer reference.
- Target animation style.
- Desired camera movement.

## Prompt Structure

The examples use a compact provider prompt shape: style, action, and camera. Some examples add environment. This differs from the richer creator-clone prompt template and suggests a lighter export shape for animation tests.

The core workflow is multi-step. First create or restyle the character reference sheet. Then create optional control images such as start/end frames or storyboard panels. Then send those references to Seedance with a simple motion prompt.

## Reusable Patterns

- Use a character sheet as the continuity anchor before animation.
- Generate start and end frames when the clip needs a controlled transformation or reveal.
- Use a storyboard image when the output needs several beats but the provider prompt should stay simple.
- Test camera movement as its own axis: pan, tracking, POV, orbit, macro zoom, side-scroll, fixed camera.
- Restyle the character sheet before animation when the target is a specific animation language.
- Keep the video prompt short when strong visual references already carry design and composition.

## Failure Modes

- The character drifts when no reference sheet anchors the design.
- Start/end frame transitions may skip the middle action if the motion prompt is too vague.
- Storyboard panels may animate out of order without explicit sequence language.
- Mixed-media scenes may blend live-action and animated references instead of preserving contrast.
- Hard camera moves can overwhelm action or create motion artifacts.
- Restyle prompts may preserve style but lose character features unless continuity is locked.

## Conflicts

This prompt pack is example-heavy and copyrighted. It should supply workflow categories and pattern evidence, not copied production text. It also uses a much simpler prompt structure than the creator-clone Seedance guides. Artist OS should preserve both possibilities: rich prompt export for dialogue/identity realism, compact prompt export when a strong storyboard or frame reference already carries the scene.

## Mapping To Artist OS

- Character reference sheet maps to Character Template and Visual Reference Sheet Plan.
- Start and end frames map to generated or imported Output Records linked to a Storyboard Shot.
- Storyboard panels map to Video Storyboard and storyboard-ready package.
- Restyled sheets map to Style Direction variants or style calibration artifacts.
- Camera-control examples map to `Storyboard Shot.camera_movement` and Shot Design.
- Mixed-media examples may require explicit reference-scope and rendering-mode rules.

## Draft Fields To Consider

- `animation_reference_sheet_required`
- `start_frame_ref`
- `end_frame_ref`
- `storyboard_reference_ref`
- `animation_style_calibration_ref`
- `camera_control_test_type`
- `mixed_media_reference_roles`
- `compact_animation_prompt`

## Open Questions

- Should animated character workflows use the same Visual Reference Sheet Plan as human character continuity?
- When should Artist OS produce start/end frames before provider video export?
- Should storyboard-to-video remain a provider export method, or become a first-class post-storyboard journey?
- How should hard camera-control prompts be reviewed before generation?
