# Character Templates, Reference Sheets, And Illustration Plans

Status: accepted.

Artist OS will treat character creation as an intent shortcut, not as a fifth medium. A character request may produce text planning, visual reference prompts, image assets, video planning support, or illustrated written-work support, but it routes into the existing medium journeys or cross-medium coordinators.

## Decision

Add three support records:

- **Character Template**: a lightweight, versioned planning seed for a character's identity, dramatic function, voice / behavior cues, provisional or approved visual identity, and continuity constraints.
- **Visual Reference Sheet Plan**: a provider-neutral prompt package for reference sheets, covering characters, products, objects, settings, and future reference-sheet subjects.
- **Illustration Plan**: a cross-medium coordinator for illustrated written works such as children's books, comics, story-with-images projects, covers plus interiors, and diagram-rich explainers.

Character Templates and Visual Reference Sheet Plans are cross-medium support assets. They do not replace Text Medium Plans, Image Medium Plans, Video Medium Plans, Creative Briefs, Prompt Plans, Output Records, or Long-Work Stewardship.

Illustration Plan is distinct from Video Storyboard. A Video Storyboard remains time-based and belongs to Video Journey: timed Storyboard Shots, camera movement, motion, transitions, script/audio relationships, and Video Audio Posture. An Illustration Plan is page, spread, panel, diagram, or cover based; it coordinates written structure with still-image outputs and visual continuity.

## Character Reference Questions

For story or character workflows with recurring characters, Artist OS asks once whether the artist wants Character Templates and optional Character Reference Sheet prompts. If the artist declines, the strategy is recorded as `declined` and the system does not ask again in the same flow. If the artist defers, the strategy is recorded as `deferred` and the system proceeds without nagging.

The system may offer reference-sheet repair later only when the artist explicitly asks for better consistency, reference sheets, drift repair, or related help.

## Authority

Character Template is a planning seed. In cumulative or full long-form work, Long-Work Stewardship remains the canon authority. Durable character facts that must govern later parts become Long-Work `continuity_rules` with `rule_type = "character"`. Draft-discovered or generation-discovered changes become `proposed_continuity_updates` until approved through the required path.

## Provider Boundary

Character Reference Sheet prompts and other Visual Reference Sheet prompts may be drafted automatically. Generated reference-sheet images require explicit Generation Approval and normal Output Records. Imported reference sheets are user-provided assets and should keep provenance when used downstream.

## Consequences

- The conductor can route "character" as an intent shortcut while keeping medium ownership clear.
- Text-only projects can use Character Templates for voice and continuity without visual generation.
- Video Journey may consume Character Templates and Visual Reference Sheet Plans without making them video-specific records.
- Illustrated written works can use Text Journey and Image Journey together without misusing Video Medium Plan.
- Future agents have an ADR-backed boundary for "storyboard" routing: ambiguous storyboard requests ask a disambiguation question; children's book, comic, picture-book, and diagram-rich storyboards map to Illustration Plan; film, reel, animation, trailer, and video-generator storyboards map to Video Journey.
