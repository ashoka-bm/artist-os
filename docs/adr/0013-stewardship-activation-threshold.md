# Long-Work Stewardship Activation Threshold

Status: accepted.

Long-Work Stewardship (ADR 0004) is the guardrail layer for works whose parts must
stay continuous across a long arc: readiness gates, checkpoints, continuity rules,
and drift tracking. Today it is activated by Workflow Scale Routing (ADR 0007) when
the scale level is `cumulative_work` or `full_long_form_project` — that is, by
*multi-part-ness*. In practice multi-part is the wrong trigger: a three-track EP or a
short multi-section piece is multi-part but does not need cross-part stewardship, yet
it pays the overhead.

## Decision

Long-Work Stewardship activates only when **both** conditions hold — it is the
guardrail for continuity that is both real and too large to hold in working context,
so either condition alone is not enough:

1. **Cumulative dependency** — the parts depend on each other for continuity
   (recurring characters, world, or narrative carry across parts). A standalone
   collection, portfolio, or album of individual songs fails this and never activates
   stewardship, regardless of size.
2. **Length floor** — the arc is long enough that continuity cannot be tracked by hand.

Per-medium length-floor defaults (artist-overridable):

- **Video** — cumulative arc and longer than ~5 minutes.
- **Text** — cumulative arc and more than one chapter (multi-chapter).
- **Audio** — a cumulative arc *across* the tracks (Album Cohesion Mode = cumulative,
  not a collection of individual songs) and full-length (~8+ dependent tracks / ~30+
  minutes). An album of individual songs never qualifies, however long.
- **Image** — recurring-subject continuity and a book-scale continuous series (~20+
  images), or an illustrated long-form work whose stewardship rides on the text
  threshold above.

Below the gate — including most albums, EPs, portfolios, and short multi-part works —
stewardship does not activate even when Workflow Scale Routing is multi-part.
Medium-Level Workflow Scale Routing records the decision; this gate is the authority
for whether `activated_supports` includes `long_work_stewardship`, and for audio it
reuses the existing Album Cohesion Mode field for condition 1.

## Consequences

- Amends ADR 0004 and ADR 0007: stewardship is gated on the length/continuity
  threshold above, decoupled from the raw `cumulative_work` / `full_long_form_project`
  levels. Those levels still describe scale and still drive other supports; they no
  longer auto-activate stewardship by themselves.
- Cost: short and mid works (the common case, and the cost-tiering target) skip the
  stewardship records and readiness gates entirely.
- In a multi-medium project, each medium evaluates the threshold independently, so a
  project's Effective Project Scale (ADR 0012, D4) can be cumulative while no medium
  activates stewardship.
- Open: whether the length-floor defaults live in each medium mode file or in one
  shared routing rule; and how an artist override of a default is recorded.
