# Higgsfield Supercomputer Explainer Toolkit Graphics Analysis

## Reference

- Reference id: `ref_higgsfield_supercomputer_explainer_toolkit_graphics_001`
- Title: `Motion Graphics - Prompt for Higgsfield Supercomputer`
- Source path: `conversation:2026-06-24:user-pasted-reference`
- Date analyzed: 2026-06-24
- Provider or platform: Higgsfield Supercomputer
- Reference type: motion graphics package brief
- Reuse policy: analyze and rewrite in Artist OS language

## What It Is

This reference describes a seven-item motion-graphics b-roll package for a creator explainer called "The Explainer Video Toolkit." It names each graphic, supplies the text, and defines a restrained style based on an already approved still.

## Video Types

- Motion-graphics b-roll package.
- Explainer-video graphic system.
- Title card.
- Kinetic infographic.
- Process-flow graphic.
- Hook, clarity, retention, and takeaway cards.

## Assumed Inputs

- Approved "Idea to Visual Gap" still from Segment 2.
- Final text for seven graphics.
- 16:9 format.
- Style target: deep charcoal, off-white text, clean geometry, gold data highlights.
- The explainer's segment structure or at least where each graphic appears.

## Prompt Structure

This reference is package-based rather than scene-based. The output is not one video scene but a coherent set of seven graphics that should share typography, palette, layout logic, and motion behavior.

The approved still acts as the style authority. The provider prompt should preserve that style while varying content and layout by graphic role. The package needs a system prompt or style bible plus per-graphic instructions.

## Reusable Patterns

- A motion package can use an approved still as a calibration artifact.
- The package should define shared style once, then vary each graphic by role.
- Graphic text must be exact and should likely be rendered as editable or verified output when possible.
- B-roll packages need consistency across color, type, hierarchy, grid, and motion.
- Process graphics need a different structure from title or takeaway cards.

## Failure Modes

- AI-rendered text may contain spelling errors or gibberish.
- The seven cards may drift in style without a shared system.
- The process flow may become decorative instead of readable.
- Gold highlights may dominate instead of serving data emphasis.
- Motion may distract from clarity if animation rules are not constrained.

## Conflicts

This reference may not fit image-conditioned video prompting alone. Motion graphics often need tools that support text fidelity, editable design layers, or deterministic rendering. It should remain in draft research until the system decides whether this belongs to provider prompting, an HTML/Remotion render path, or a hybrid path.

## Mapping To Artist OS

- The approved still maps to an Output Record or calibration artifact.
- The seven graphics map to a package-level plan, not a single Storyboard Shot.
- Text content maps to Text Journey or exact text blocks.
- Visual style maps to Video Style Expression or a future motion-graphics style system.
- Each graphic can map to a Storyboard Shot, panel, or motion-graphics item depending on implementation.

## Draft Fields To Consider

- `package_graphic_count`
- `approved_style_still_ref`
- `shared_motion_graphics_system`
- `exact_text_blocks`
- `graphic_role`
- `text_fidelity_requirement`
- `editable_output_required`
- `provider_or_renderer_recommendation`

## Open Questions

- Should Artist OS generate these as provider prompts, HTML/Remotion compositions, or static graphics plus animation instructions?
- How should the system verify text fidelity?
- Does Higgsfield Supercomputer support reliable text rendering for title cards and process diagrams?
- Should each graphic become a separate output record or one package record?
