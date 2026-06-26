# Draft Decision 0007: Narrative Depth Placement

Status: accepted in draft.

Date: 2026-06-26

## Decision

Narrative Depth is captured provisionally during Orientation when the artist names the output type, then confirmed during Medium Output Shape Recommendation.

Video Medium Plan records the binding Narrative Depth and uses it to decide whether the video needs:

- a Story Template,
- a Micro-Journey Template,
- or a utility sequence plan.

## Rationale

Narrative Depth affects scope, questions, and planning effort, so Artist OS should identify it early. But it should not become binding until the system understands Artist Meaning and the chosen story movement well enough to know whether the output really needs a full story, micro-journey, or utility sequence.

## Consequences

- Orientation can make an early routing guess.
- Medium Output Shape Recommendation confirms or revises that guess.
- Video Medium Plan owns the binding narrative-depth decision for video.
- Review can flag mismatches, such as a `utility_sequence` trying to carry a full emotional arc or a `micro_journey` with no payoff.
