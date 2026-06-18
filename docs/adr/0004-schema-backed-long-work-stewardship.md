# Schema-Backed Long-Work Stewardship

Status: accepted and implemented for the first image-series and long-text pass.

Artist OS adds a schema-backed Long-Work Stewardship Record for Cumulative Work: long-form or multi-output projects where each part builds on prior parts through sequence, emotional arc, escalation, transformation, or dependency. The Beat Plan remains the story authority; Long-Work Stewardship protects execution across planned parts, checkpoints, continuity rules, readiness, and drift without replacing Artist Meaning, the Beat Plan, Medium Plans, or Output Acceptance.

The record has a foundation state and an enriched state. The foundation record is valid after Story Approval, before a Medium Plan exists. It may have `medium_plan_id = null`, an empty `part_plan[]`, and pending readiness. The enriched record adds the Medium Plan reference, medium-specific Long-Work Parts, readiness, checkpoints, and progress updates before downstream expansion.

## Considered Options

- Use only the Beat Plan: rejected because it would make the story authority also own production state, checkpoints, output progress, and drift management.
- Use only Review Records and Gate Decisions: rejected because long work needs a resumable per-project state surface that can answer what part is next, which checkpoints are approved, and what continuity rules are active.
- Apply the same machinery to all multi-output collections: rejected because non-sequential portfolios, store sets, and curator batches need Collection Coherence Review, not full story-sequence stewardship.

## Consequences

Long-Work Stewardship is schema-backed from the start. Collection Coherence Review remains review behavior until collection-level acceptance, store readiness, or batch-level promotion creates a real need for a separate schema.
