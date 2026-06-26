# Draft Decision 0015: Schema Fields vs Skill Guidance

Status: accepted in draft.

Date: 2026-06-26

## Decision

The first implementation should be mostly skill guidance.

Only a small set of durable Video Medium Plan fields should be considered first:

- Narrative Depth.
- Binding Format Template.
- Selected structure refs.
- Hook posture.
- Speaker posture.
- Provider preference notes.

Direction-note vocabularies should remain skill guidance until repeated runs prove they need durable fields.

## Direction Notes That Stay As Guidance

- Hook-entry families.
- Moment anchors.
- On-camera connection and delivery rules.
- Edit cut vocabulary.
- Seedance 2 export tendencies.
- Provider-specific prompt constraints.

## Rationale

Schema fields should represent decisions with durable authority, downstream references, validation needs, or review significance. Craft vocabularies are useful, but making every craft choice schema-backed too early would overfit the system and slow iteration.

## Consequences

- Video Medium Plan can gain a small, reviewable decision surface without becoming a prompt template.
- Direction notes remain easier to revise as references accumulate.
- Promotion from guidance to schema should require repeated evidence that a decision must be queried, validated, reviewed, or preserved across stages.
