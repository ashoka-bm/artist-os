# Character Template

Use this internal mode when an artist creates a character, or when a story has recurring characters that may need voice, behavior, visual, or continuity consistency.

Paths like `schemas/character-template.schema.json`, `schemas/visual-reference-sheet-plan.schema.json`, and `schemas/long-work-stewardship-record.schema.json` resolve from `$ARTIST_OS_ROOT`.

## Hard Gates

- Character is an intent shortcut, not a medium. Route the eventual output into text, image, video, Illustration Plan, or another implemented journey.
- Ask once whether the artist wants Character Templates and optional Character Reference Sheet prompts when recurring characters matter.
- If the artist declines, record `character_reference_strategy.status = "declined"` and do not ask again in the same flow.
- Draft Character Templates may support text-only planning and reference-sheet prompt drafting.
- Provider-backed generation requires either an approved Character Template or a Generation Approval that explicitly includes provisional character details.
- Do not make Character Template the story bible. Long-Work Stewardship remains canon authority for cumulative work.

## Standard Question

When recurring characters matter, ask:

> This story has recurring characters. Do you want Character Templates and optional Character Reference Sheet prompts before we plan the output? Templates help with voice and continuity; reference sheets add more control if you later generate illustrations, covers, storyboards, or video.

If yes, ask:

> Do you want templates only, or templates plus visual reference-sheet prompts?

Do not ask again after `declined` or `deferred` unless the artist explicitly asks for better consistency, reference sheets, character repair, or drift fixes.

## Process

1. Capture identity: name, role label, story function, first appearance, and notes.
2. Capture dramatic function: wants, fears, contradictions, arc state, and relationship pressure.
3. Capture voice and behavior cues for text-only continuity and drafting.
4. Capture `visual_identity` when known: physical description, clothing/costume, distinguishing features, style/proportion notes, and evidence status.
5. Mark inferred visual details as `agent_inferred` unless artist-provided or backed by an approved/generated/imported reference sheet.
6. Capture continuity constraints. Mark whether any should become Long-Work continuity-rule candidates.
7. Link Visual Reference Sheet Plans when the artist wants them.
8. Version rather than silently mutating a Character Template once downstream prompts/plans depend on it.

## Long-Work Interaction

Character Template is the planning seed. If a fact becomes durable canon for cumulative or full long-form work, promote it into Long-Work Stewardship as a `continuity_rule` with `rule_type = "character"`.

If drafting or generation discovers a character change, record it as a proposed continuity update; do not automatically mutate the Character Template or active continuity.

## Output

Emit a Character Template that validates against `schemas/character-template.schema.json`.
