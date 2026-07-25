# Multi-Medium Projects and Medium Activation

Status: accepted for the constrained 1.0 route on 2026-07-25; schema and
medium-activation foundations exist, while the approval/review lifecycle and
final conductor wiring remain tracked in `docs/release-1.0.md`.

A project is one Reference, one Artist Meaning, and one Beat Plan — the
medium-neutral Shared Story Spine — plus a medium layer that can carry any subset
of image, video, audio, and text. The artist activates the media they want, now or
later. There is no separate "second medium" flow and no "inheritance": because a
project has exactly one spine, every active medium uses it by construction.

This ADR exists because the conductor did not act on that model. Routing said only
"run that flow to completion, then run the next one" (a full spine from Source
Record), and each medium mode file said "produce a Transformation Brief, Beat Plan,
Medium Plan" with no "…unless they already exist." So activating a second medium on
the same Reference (e.g. a Suno track after a video) re-derived the whole meaning
spine — the observed "spinning." The fix is to make the conductor recognize the
one-project model and only build the medium-specific part.

## Decisions

- **D1 — Verbatim spine; divergence lives downstream.** The Shared Story Spine
  (Artist Meaning, Transformation Brief, Beat Plan) is immutable shared truth.
  Activating a medium reuses it as-is and expresses all medium-specific reshaping in
  that medium's own Medium Plan via Expectation Turn Translation (the Beat Plan owns
  the turn; the Medium Plan owns how it becomes visible/sonic/textual). The Beat Plan
  is never forked or edited for another medium.

- **D2 — Meaning-identity is the project boundary.** One project = one Reference +
  one Artist Meaning + one Beat Plan spine, with any subset of the four media active.
  Selecting, compressing, or emphasizing a subset of beats for a medium is normal
  medium-specific work, not a story change. A genuinely different meaning or story
  from the same Reference is a new project that links back to the same Source Record.

- **D3 — State, approve coordination, then proceed; Story Approval stands.**
  When the artist asks for a medium that is not yet active, the conductor names
  the spine it is building on (Artist Meaning + Beat Plan; Story Approval
  already holds on the unchanged Beat Plan), drafts the Cross-Medium Plan, runs
  Mixed-Media Critic Review, and asks for Cross-Medium Plan Approval. Only then
  does it continue into the supporting Medium Plan. This reuses a real prior
  approval on an unchanged record without re-running the Story gate while still
  giving cross-medium roles, deliverables, order, and continuity their own
  explicit authority. Medium-specific reviews and downstream gates run fresh.

- **D4 — Per-medium scale is additive; effective project scale is derived.**
  Medium-Level Workflow Scale Routing is decided per medium and may recommend supports
  the others did not. The Beat Plan's Project-Level Workflow Scale Routing stays the
  frozen as-of-Story-Approval baseline (consistent with D1). The project's Effective
  Project Scale is the maximum over its active media and is surfaced on the
  Cross-Medium Plan / `project.json`, not by rewriting the Beat Plan. This amends ADR
  0007: project scale is the Beat-Plan baseline plus per-medium escalation, read from
  the coordinator. (Whether a medium recommends Long-Work Stewardship is governed by
  ADR 0013, and whether stewardship becomes active is governed by ADR 0015.)

- **D4′ — Thin coordinator over separate medium bodies.** The medium layer is a lazy,
  project-level **Cross-Medium Plan** (a generalization of the album-only Release
  Package Plan) that materializes when a second medium is activated or the
  artist explicitly requests multiple outputs. It lists each active medium and
  its medium-plan ref and owns the artist-confirmed primary medium, planned
  deliverables, shared references, production order, cross-medium continuity,
  and Effective Project Scale. The heavy medium-specific
  bodies stay separate, lean, and independently locked. The medium plans are not
  collapsed into one record: the four bodies are largely disjoint, so a unified schema
  would be the sum of all bodies (~85KB+) loaded whole to author any single medium — a
  direct regression of the Schema Load Economy (PR #15) — and one record holding a
  locked medium beside an in-progress one re-introduces the D1 provenance hazard one
  layer down. Coordination together, realization apart.

- **D5 — Resume state is a projection, not an artifact.** `project.json` carries
  durable resume state (current checkpoint, next phase, media index → Cross-Medium
  Plan + spine refs). The reset-handoff prompt, post-compaction rehydration, and
  activating a later medium in a fresh thread are all thin on-demand projections of
  that single durable state. No `resume-packet.json` is persisted. One durable source,
  three behaviors — this is the convergence: the state that lets a project continue in
  a fresh thread (reset) or after compaction (rehydration) also lets a new medium be
  activated without re-deriving meaning.

- **D6 — Detection is SQLite-first.** On a new request the conductor queries
  `artist-os.sqlite` for a project with an approved Beat Plan: one clear match → offer
  to continue/activate, naming it; several → ask which; none → cold start. (Reuses the
  existing "query SQLite first, then `project.json`" rule.)

- **D7 — The plan and approval are the provenance for the hop.** Activating a
  medium first writes the reviewed and approved Cross-Medium Plan and its Gate
  Decision. After approval, the conductor writes that medium's Medium Plan and
  a lightweight `medium_activated` event in `events.jsonl`. Cross-medium
  lineage is explicit through the Cross-Medium Plan and existing `*_id`
  references. No inheritance record or sibling field is needed.

- **D8 — Approve the coordinator, then enter at Phase 8; offer reset.**
  Activating a not-yet-active medium enters the Cross-Medium interstitial
  first, then the supporting Medium Plan phase after approval and runs the
  medium-specific tail sequentially. Conditional phases re-evaluate for that
  medium. It may run in-thread, but a not-yet-active medium is a reset-eligible
  checkpoint, so the conductor offers the reset handoff when context is high.

  (D9 — Long-Work Stewardship activation threshold — is recorded separately in ADR 0013.)

- **D10 — Primary and supporting media.** The Cross-Medium Plan records a **Medium
  Role** per active medium: `primary` or `supporting`. The primary medium is fully
  fleshed out; a supporting medium defaults to the compact treatment tier (a lean Medium
  Plan; the reduced review count is deferred until the scale-gated-review-count lever
  lands, so supporting media reuse the full standard bounded review set for now) and
  takes continuity direction from the *primary medium's
  realization* in addition to the Shared Story Spine (the cover obeys the song; the
  photos obey the article's framing). Medium Role (importance) and medium-level
  Workflow Scale Routing (depth) are distinct axes — the role seeds the default scale,
  which the artist may override. The conductor recommends the primary from the output
  type (video for a video; the song for a music video; text for an article with
  photos) and the artist confirms; it is not hard-coded. This generalizes the Album
  Track Cover and Illustration Plan patterns. Rollout is two-part: the lean supporting
  Medium Plan and the "serves primary" continuity link need no contract change; the
  review reduction depends on the grill-gated scale-gated-review-count lever and lands
  after that gate clears.

## Consequences

- Activating a medium runs Cross-Medium Plan → Mixed-Media Critic → Plan
  Approval → supporting Medium Plan → Draft Brief → Critic → Brief Approval →
  Final Records → downstream, reusing `transformation_brief_id` /
  `beat_plan_id` by reference. No contract change to the spine schemas.
- The Cross-Medium Plan is created lazily — only when a project has a second active
  medium or the artist explicitly requests multiple outputs. Single-medium
  projects rely on the `project.json` media index. The Release
  Package Plan is split along the plan/output seam (D11, resolved in ADR 0014): its
  planning role belongs to this coordinator, its finished-bundle role to the Asset
  Package. It is not unified into this coordinator as a plan-profile nor stacked beside
  it.
- `project.json` gains a defined resume-state section (checkpoint, next phase, media
  index) — the durable half of the cost-tiering reset/resume levers.
- ADR 0007 is amended (project scale = Beat-Plan baseline + per-medium escalation,
  surfaced on the coordinator). The Beat Plan's scale field remains the frozen baseline.
- Implementing the conductor behavior edits `SKILL.md` (the eval-locked conductor
  spine) and owes a real conductor re-bless; this ADR records the design so it can be
  built cold when scheduled.
- The concept previously drafted as "Cross-Medium Warm Start" is retired in favor of
  Medium Activation: the cheap behavior (no re-derivation) is the only behavior in the
  one-project model, not a special mode.
- Supporting media reuse the compact-tier machinery rather than a new "treatment"
  concept; `medium_role` is a new field on the Cross-Medium Plan. The album Release
  Package Plan's `primary_medium` is the specialized ancestor of this role.
