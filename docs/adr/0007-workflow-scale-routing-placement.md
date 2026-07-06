# Workflow Scale Routing Placement

Status: accepted.

Artist OS uses Workflow Scale Routing to decide which planning, stewardship, review, and continuity supports are needed for the scale of a work. It is internal routing, not an artist-facing gate.

Workflow Scale Routing is persisted as a compact field on existing pipeline records:

- Project-Level Workflow Scale Routing belongs on the Beat Plan.
- Medium-Level Workflow Scale Routing belongs on each Medium Plan.

Artist OS does not create a standalone Workflow Scale Routing Record by default.

## Consequences

- Beat Plans can record whether the approved story movement is a Compact Artifact, Structured Single Artifact, Cumulative Work, or Full Long-Form Project before medium-specific planning begins.
- Each Medium Plan can record whether that medium stays compact, expands inside one artifact, or recommends cumulative/long-form supports.
- Long-Work Stewardship remains the guardrail layer for Cumulative Work; Workflow Scale Routing recommends whether that layer and related helpers are needed. ADR 0015 governs artist-facing activation.
- A standalone routing record should be added only if future projects prove routing needs independent lifecycle, review, querying, or revision history.

Amendment (ADR 0013 and ADR 0015): `long_work_stewardship` is now recommended by the ADR 0013 two-condition threshold (cumulative dependency AND the per-medium length floor) rather than auto-activated by the `cumulative_work` / `full_long_form_project` levels. Those levels still describe scale and still drive other supports; they no longer add stewardship by themselves. ADR 0015 requires an artist-facing activation gate before a Long-Work Stewardship Record is created.
