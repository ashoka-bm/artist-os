# JACKVSAI Fashion Campaign Prompt Framework Analysis

## Reference

- Reference id: `ref_jackvsai_fashion_campaign_prompt_framework_001`
- Title: `JACKVSAI Fashion Campaign Prompt Framework`
- Source path: `/Users/ashokaji/Downloads/jackvsai-fashion-campaign-prompt-framework (1).skill`
- Date analyzed: 2026-06-24
- Provider or platform: Seedance, Kling, Higgsfield, and comparable AI video generators
- Reference type: zipped skill bundle with fashion campaign prompt framework
- Reuse policy: analyze and rewrite in Artist OS language; do not install or copy wholesale

## What It Is

This reference defines a compact prompt framework for streetwear and editorial fashion campaign videos. It treats the garment as the hero, not the model. The output is a one-paragraph 15-second shot sequence under 1,000 characters, designed for fast, punchy AI video generators.

## Video Types

- Streetwear campaign video.
- Editorial fashion video.
- Garment-led look sequence.
- Urban model movement prompt.
- Styled look or outfit prompt from a reference image.

## Assumed Inputs

- Reference image of a garment, outfit, model, flat lay, or product shot.
- Subject or model descriptor.
- Action or movement energy.
- Location.
- Expression or attitude.
- Lighting mood.
- Optional garment pieces, accessories, footwear, and styling notes.

## Prompt Structure

The framework outputs one flowing paragraph. It uses 6 to 7 shots by default, each 2 to 3 seconds, with a maximum of 4 seconds. Every shot includes shot size, lens, camera angle, camera movement, garment or model motion, and duration. Shots are separated with the phrase `Cut to.` The prompt ends with a fixed realism and audio line.

The framework differs from the general cinematic compact export in three ways:

- It has a stricter 1,000-character limit.
- It requires movement in every shot.
- It requires at least one negative-space wide and one direct-attitude beat.

## Reusable Patterns

- Fashion prompt analysis should prioritize garment details before model identity.
- Garment detail should be distributed across the edit: silhouette in wides, fabric and hardware in close-ups, colorway against the environment.
- Editorial fashion needs movement even when the pose is quiet: weight shift, chin raise, shoulder roll, fabric brush, stride, lean, turn.
- Negative space can be a required campaign grammar, not only a composition option.
- Direct eye contact can serve as a planned attitude beat.
- Handheld energy can be the default for streetwear, while static shots require model movement to carry the frame.

## Failure Modes

- The model becomes the subject and the garment becomes incidental.
- The prompt burns the 1,000-character budget on atmosphere instead of garment detail.
- One or more shots are static and lose editorial energy.
- No wide shot establishes silhouette or negative space.
- No attitude beat gives the sequence campaign force.
- Garment pieces are mentioned once and then disappear across later shots.

## Conflicts

This framework should not replace general multi-shot exports. It is fashion-specific and optimized for high-energy streetwear/editorial work. Its fixed closing line is useful as a provider export convention but should remain configurable if a different approved audio or style direction exists.

## Mapping To Artist OS

- Garment reference maps to Source Record, product/wardrobe reference, or Output Record.
- Fashion campaign intent maps to Style Direction, Shot Design, and a future campaign/package plan.
- Negative-space wide maps to composition strategy and Visual Dynamics.
- Attitude beat maps to Intended Feeling, model performance, and Shot Design.
- Garment-first detail maps to reference scoping and provider export text.

## Draft Fields To Consider

- `garment_hero_required`
- `fashion_campaign_mode`
- `compact_prompt_char_limit`
- `movement_required_every_shot`
- `negative_space_wide_required`
- `attitude_beat_required`
- `garment_detail_distribution`
- `fashion_closing_audio_line`

## Open Questions

- Should fashion campaign work belong under Video Journey, UGC Campaign Content Factory, or a separate fashion/editorial package journey?
- How should Artist OS preserve garment fidelity when the reference is a flat lay without a model?
- Should negative-space wide and attitude beat become configurable fashion-review checks?
- Which provider handles garment texture and silhouette-in-motion most reliably?
