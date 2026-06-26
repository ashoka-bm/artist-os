# Seedance 2 Platform Notes Analysis

## Reference

- Reference id: `ref_seedance_2_platform_notes_001`
- Title: `Seedance 2 Platform Notes From Conversation`
- Source path: `conversation:2026-06-26:user-pasted-reference`
- Date analyzed: 2026-06-26
- Provider or platform: Seedance 2
- Reference type: provider-specific direction notes
- Reuse policy: provider-export guidance only; do not turn these into story templates

## What It Is

This Reference is a compact list of practical Seedance 2 prompt rules. The notes are useful because they identify provider behavior that should shape final prompt rendering: duration, language, frame rate, continuity, framing, lighting, action density, background motion, style references, and finishing texture.

The notes are not story structure. They do not decide hook, payoff, narrative turn, or audience journey.

## Directional Notes To Preserve

- Add `24 frames per second` or equivalent prompt language.
- Try the final prompt in Chinese.
- Keep videos to 15 seconds or less.
- Use the last frame of the previous sequence as a continuity input when chaining clips.
- Mention a concrete camera or capture style.
- Specify lighting style.
- Default to no subtitles and no music for raw visual clips unless the approved audio plan says otherwise.
- Use medium or closer shots when characters talk or interact.
- Limit active subjects.
- Add simple background motion.
- Include a visual style reference image when style consistency matters.
- Minimize action so the generator has fewer moving obligations.
- Add film grain when it matches the approved style.

## Mapping To Template Layers

- Story templates: no direct change. These notes do not create narrative structure.
- Direction library: add as Seedance 2 provider direction.
- Format templates: affects which formats are safer for Seedance, especially close interaction, small casts, and compact scenes.
- Provider exports: directly affects Seedance 2 prompt rendering.

## Draft Risks

- Treating 15 seconds as the story length instead of the provider clip length.
- Applying `no music` to a final video that needs music in post.
- Adding camera-body detail even when it fights the approved style.
- Letting style reference images override identity references.
- Overusing background animation until it competes with the subject.
- Cramming a complete narrative arc into one provider clip instead of batching scenes.

## Draft Rule

Seedance 2 should receive a small, controlled scene segment. The story template can be larger, but each Seedance export should handle one readable beat, short action chain, or compact hook/payoff movement.
