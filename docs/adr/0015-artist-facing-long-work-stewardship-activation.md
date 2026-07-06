# Artist-Facing Long-Work Stewardship Activation

Status: accepted.

ADR 0013 defines when Long-Work Stewardship is recommended: both cumulative
dependency and the medium-specific length floor must hold, or the artist must
explicitly ask for continuity tracking below that threshold. That threshold is
not enough by itself. Long-Work Stewardship adds process, memory, checkpoints,
and review overhead, so Artist OS must not silently activate it.

## Decision

When Artist OS recommends Long-Work Stewardship, it presents a separate
artist-facing activation gate immediately after Story Approval and before Medium
Plan expansion.

Use shared core wording, adapted by medium:

> This is starting to behave like a longer work, where later parts will need to
> remember what earlier parts set up. I recommend activating Long-Work
> Stewardship. It gives the project a lightweight memory: what each part is meant
> to carry, what must stay consistent, what should not resolve too early, and
> where we should pause to check the arc. It adds a little structure, but it
> helps protect the feeling and continuity of the work as it grows.
>
> Do you want to activate it now?

Offer three choices:

- **Activate** — create the foundation Long-Work Stewardship Record immediately.
- **Defer** — do not create the record yet; resurface the recommendation at the
  next concrete continuity-risk point.
- **Waive and continue** — continue without stewardship and record a risky
  waiver.

Clear agreement such as "sure," "yes," "keep track of it," or "do that" counts
as activation. Ambiguous answers such as "maybe," "not now," or "let's see"
count as defer. Explicit refusal such as "no," "skip it," or "too much process"
counts as waiver.

Declining recommended stewardship is a risky waiver, not a neutral preference.
No artist-authored reason is required; use a default reason such as "artist
chose to continue without long-work continuity tracking." The system continues,
but future reviewers may resurface the risk when dependent expansion, continuity
drift, or long-gap resume makes it relevant.

Defer and waive create Gate Decisions only. They do not create placeholder
Long-Work Stewardship Records. Activation creates the foundation record
immediately, before the Medium Plan exists, then the Medium Plan enriches it with
medium-specific parts.

If the artist explicitly requests stewardship below the default threshold,
activate the same Long-Work Stewardship Record type and record that the system
did not require it but the artist requested continuity tracking.

## Activation State Authority

Workflow Scale Routing may recommend stewardship, but it must not claim
stewardship is active before the artist accepts it.

The intended state model is:

- routing evidence records whether `long_work_stewardship` is recommended,
- the Gate Decision records the artist's activation, defer, waiver, or
  deactivation choice,
- `project.json.resume_state` carries the operational summary for resume/status
  views,
- a Long-Work Stewardship Record exists only when stewardship is active or was
  active and later superseded.

Schema follow-up: add `recommended_supports` to Workflow Scale Routing, add
`long_work_stewardship_activation` to Gate Decisions, add the activation summary
to `resume_state`, and remove `paused` from Long-Work Stewardship status if no
pause action is offered.

## Checkpoint Behavior

After stewardship is active, Artist OS creates and runs routine checkpoints
automatically. Clean checkpoints do not require artist approval; Artist OS may
show a brief status such as:

```text
Continuity checkpoint passed.
```

Artist-facing interruption is required only when a checkpoint blocks, a
continuity or story-authority change is proposed, a reviewer requires repair
before expansion, or an explicit waiver is needed.

The first Medium Mapping Checkpoint is different. When the Medium Plan creates
multiple dependent parts, Long-Work Reviewer checks the part map first, then the
artist sees a concise map and confirms, revises, or explicitly waives it before
bulk expansion. This checkpoint answers whether the approved arc is being
carried into the actual chapters, scenes, tracks, image roles, or other parts in
the right way.

If the Medium Plan proves the work is compact after stewardship was activated,
ask for lightweight confirmation to deactivate it as unnecessary. Record the
decision with the activation gate type, mark the stewardship record superseded,
and continue with the compact flow.

Before Medium Mapping approval, Artist OS may create one clearly labeled
calibration or sample part if it helps the artist judge direction. It must not
expand multiple dependent parts until the map is approved or explicitly waived.
Existing approvals still apply: dry-run sample plans need no new approval, text
draft samples need Draft Generation Approval, and provider-backed media samples
need Generation Approval.

## Consequences

- Long-Work Stewardship becomes opt-in at the moment of recommendation rather
  than an invisible support activated by routing.
- Waiving stewardship preserves artist control while keeping risk visible in the
  audit trail.
- Defer supports artists who are not ready to add process without treating that
  answer as refusal.
- Routine checkpoints can protect continuity without forcing approval fatigue.
- Initial Medium Mapping remains artist-facing because it is the first concrete
  shape of how the longer work will unfold.
