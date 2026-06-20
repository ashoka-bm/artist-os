# Workflow Scale Routing Placement

Status: accepted.

Artist OS uses Workflow Scale Routing to decide which planning, stewardship, review, and continuity supports are needed for the scale of a work. It is internal routing, not an artist-facing gate.

Workflow Scale Routing is persisted as a compact field on existing pipeline records:

- Project-Level Workflow Scale Routing belongs on the Beat Plan.
- Medium-Level Workflow Scale Routing belongs on each Medium Plan.

Artist OS does not create a standalone Workflow Scale Routing Record by default.

## Consequences

- Beat Plans can record whether the approved story movement is a Compact Artifact, Structured Single Artifact, Cumulative Work, or Full Long-Form Project before medium-specific planning begins.
- Each Medium Plan can record whether that medium stays compact, expands inside one artifact, or activates cumulative/long-form supports.
- Long-Work Stewardship remains the guardrail layer for Cumulative Work; Workflow Scale Routing only decides whether that layer and related helpers should activate.
- A standalone routing record should be added only if future projects prove routing needs independent lifecycle, review, querying, or revision history.
