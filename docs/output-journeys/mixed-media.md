# Mixed-Media Journey

> **Status: Album v1 is implemented; constrained general Cross-Medium Plan
> orchestration is frozen into 1.0 and is implemented.** The Cross-Medium Plan
> and Asset Package schemas, planned deliverables and shared references, the
> Mixed-Media Critic Review and approval vocabulary, the Package Format
> Selection And Completeness gate with per-slot waivers, the conductor wiring,
> and a tracked fixture-backed rehearsal
> (`tests/fixtures/cross-medium/article-with-photos-rehearsal/`) are in place.
> The route still owes the real conductor-behavior eval and its promotion into
> release-evidence, per `docs/release-1.0.md`. Broader package, campaign,
> publishing, and distribution routers are post-1.0.

The Mixed-Media Journey coordinates multiple output journeys from one approved Beat Plan. It is for projects where image, video, sound, text, or other media should share meaning and structure while expressing different parts of the work.

Album v1 is the first concrete Release Package route inside this branch. The
general 1.0 route is a smaller coordinator over existing medium journeys, not a
generic campaign system. The governing language for Release Package, Album,
Album Sonic System, Album Visual System, Album Calibration, Track Cover,
Cross-Medium Plan, and Medium Role lives in `CONTEXT.md`. The exact release
boundary lives in `docs/release-1.0.md`.

## Best Fit

Use the Mixed-Media Journey when the final work should include:

- an image plus music,
- a video plus soundtrack,
- a poem plus image series,
- a gallery sequence with sound,
- several coordinated assets from the same Reference.

Visual Album, campaign, publishing, and distribution-specific routing are not
part of 1.0. Artist OS may preserve those requests as planning notes, but it
must not claim a dedicated workflow for them.

## Route

### Album v1

```text
Approved Album Beat Plan
  -> Long-Work Stewardship Activation Gate, when Album Cohesion Mode recommends it
  -> Foundation Long-Work Stewardship, when activated by the artist
  -> Release Package Plan
  -> Pre-Calibration Mixed-Media Critic Review
  -> Release Package Plan Approval Gate
  -> Representative Sound Medium Plan for the Calibration Track
  -> Representative Image Medium Plan for the Calibration Track Cover
  -> Album Calibration Gate
  -> Remaining track Sound Medium Plans and Sound Prompt Plans
  -> Album cover and Track Cover Image Medium Plans and Prompt Plans
  -> Optional title, description, lyrics, liner notes, captions, or track story Text Journeys
  -> Post-Calibration Mixed-Media Critic Review
  -> Per-output Prompt Lock, Generation Approval, Output Critic Review, and Output Acceptance Gates
```

The Release Package Plan is package-level coordination only. It owns deliverables, track mapping, Album Cohesion Mode, Album Sonic System, Album Visual System, calibration status, production order, and cross-media continuity. It does not replace Sound Medium Plans, Image Medium Plans, Text Medium Plans, Long-Work Stewardship Records, Prompt Plans, Text Generation Plans, or Output Records.

When Album Cohesion Mode recommends Long-Work Stewardship, present the ADR 0015 activation gate before Release Package Plan approval. If the artist activates it, create the foundation Long-Work Stewardship Record before Release Package Plan approval. The Release Package Plan may reference that stewardship record, but it does not own part status, checkpoint state, readiness, or cumulative drift management.

Album Calibration is directional. It checks sonic direction, visual direction, and sound-visual fit after representative Sound and Image Medium Plans exist, before the remaining album deliverables expand. Final artifacts still go through the normal per-output gates.

### General Cross-Medium v1

```text
Existing project with an approved Shared Story Spine
  -> Second-medium activation or explicit multi-output request
  -> Mixed-Media Scope Gate
  -> Medium Selection Gate
  -> Role Assignment Gate
  -> Cross-Media Continuity Gate
  -> Production Order Gate
  -> Draft Cross-Medium Plan
  -> Mixed-Media Critic Review
  -> Cross-Medium Plan Approval Gate
  -> Sequential Medium-Specific Journeys from Phase 8
  -> Per-output Prompt, Generation, Review, and Acceptance Gates
  -> Package Format Selection and Completeness Gate
  -> Asset Package
```

The Cross-Medium Plan materializes lazily. It is not required for a
single-medium project. It appears when a second medium is activated or the
artist explicitly requests a multi-output package.

One primary medium anchors the plan. Supporting media default to compact
treatment, remain independently reviewed, and take continuity from the primary
realization when the approved production order requires it. General
multi-medium production is sequential in 1.0.

A material change to included media, Medium Roles, production order, or shared
continuity invalidates the standing Cross-Medium Plan approval. Rerun the
affected Mixed-Media Critic Review and obtain a new artist decision before
expansion continues.

### Medium Roles

For a general (non-album) multi-medium project, each active medium carries a **Medium Role** recorded on the **Cross-Medium Plan**. One medium is **primary** and the rest are **supporting**:

- The primary medium is recommended from the requested output type — video for a video, the song for a music video, text for an article with photos — and the artist confirms it. This is recommendation-first, not hard-coded, and honors the Gate Completion Rule.
- A **supporting medium** defaults to the compact treatment tier: a lean Medium Plan that takes continuity from the primary medium's realization in addition to the immutable Shared Story Spine (via Expectation Turn Translation), rather than forking the spine.
- **Medium Role** names importance (`primary` | `supporting`); **Workflow Scale Routing** names depth. The role seeds each medium's default Workflow Scale, and the artist may override it. The two are distinct.

The Album v1 Release Package Plan — with its `primary_medium` and per-deliverable `medium_role` — is the specialized ancestor of this general primary/supporting contract; Album Track Covers and Illustration Plan images are the established supporting-asset precedents.

The review-reduction half of the compact tier is deferred: supporting media reuse the full standard bounded review set for now, until the scale-gated-review-count lever lands. See the **Cross-Medium Plan**, **Medium Role**, **Primary Medium**, and **Supporting Medium** glossary entries in `CONTEXT.md`.

## Gates

- Release Package Plan Approval Gate: does the artist approve Album Cohesion Mode, deliverables, Album Sonic System, Album Visual System, Calibration Track, and calibration visual target as ready for representative Medium Plan creation?
- Album Calibration Gate: do the sonic direction, visual direction, and sound-visual fit subchecks approve expansion for the relevant deliverables?
- Mixed-Media Scope Gate: what is the package or experience?
- Medium Selection Gate: which media are included?
- Role Assignment Gate: which beats belong to which medium?
- Cross-Media Continuity Gate: what must stay consistent across media, and what may diverge?
- Production Order Gate: which output should be created first as calibration?
- Cross-Medium Plan Approval Gate: does the artist approve the Medium Roles,
  deliverables, production order, Effective Project Scale, and continuity rules
  before supporting-medium expansion?
- Generation Approval Gate: each provider-backed generation call still requires explicit approval.

## Reviews

- Story Critic Review happens before this journey when the shared Beat Plan is
  multi-beat, sequence-based, lyric-bearing, or otherwise ambiguous.
- Beat Reviewer sub-agent is mandatory when beats are assigned across multiple media.
- Album v1 uses Mixed-Media Critic Review with album-specific criteria, not a separate Album Critic role.
- Pre-calibration Mixed-Media Critic Review checks whether the Release Package Plan is coherent enough to test.
- Post-calibration Mixed-Media Critic Review checks whether the calibrated direction is strong enough to expand.
- Medium-specific critic reviews happen inside each selected output journey as bounded sub-agent reviews.
- Mixed-Media Critic Review checks whether the media work together instead of duplicating or contradicting each other accidentally as a bounded sub-agent review.
- Prompt Critic Review remains scoped to each medium-specific prompt or
  generation plan.
- Output Critic Review remains scoped to each concrete Output Artifact.
  Package Compilation validates completeness over the accepted Output Records;
  it does not invent a separate generated-package artifact.
- Mixed-Media Critic Review reruns only when cross-medium continuity,
  production order, or waiver scope is disputed or materially changed.

For a general Cross-Medium Plan, Mixed-Media Critic Review must check:

- one unchanged Shared Story Spine and standing Story Approval are reused,
- exactly one primary medium is artist-confirmed,
- every supporting medium has a distinct job and an explicit relationship to
  the primary realization,
- production order is sequential and internally consistent,
- continuity rules distinguish what must stay fixed from what may vary,
- each medium retains its normal reviews and gates,
- and Package Compilation cannot declare missing deliverables complete without
  an explicit waiver.

### Album v1 Review Criteria

Pre-calibration Mixed-Media Critic Review must check:

- traceability to Artist Meaning, Transformation Brief, Album Beat Plan, and any active Long-Work Stewardship Record,
- required deliverable completeness: title, description, album cover, one track Sound Prompt Plan deliverable per track, and one Track Cover deliverable per track,
- Album Sonic System and Album Visual System boundaries, including what each system must not own,
- Calibration Track and calibration visual target justification,
- cross-media continuity and drift risks,
- provider-boundary safety, including no open-ended generation approval.

Post-calibration Mixed-Media Critic Review must check:

- sonic direction, visual direction, and sound-visual fit subcheck outcomes,
- whether expansion is limited to deliverables whose relevant calibration subchecks are approved,
- whether remaining Sound Medium Plans and Image Medium Plans still respect the Album Sonic System and Album Visual System,
- whether optional text deliverables are justified by artist request or approved track direction,
- whether per-output gates remain intact before any concrete artifact is generated, drafted, imported, reviewed, or accepted.

## Coordination Rules

One Beat Plan can produce multiple Medium Plans, but each medium should have a distinct job.

Examples:

- image holds the symbolic threshold while music carries the emotional arc,
- video stages the sequence while text supplies voice or narration,
- image series shows transformation roles while sound supplies continuity,
- text names the hidden logic while visuals preserve ambiguity.

Mixed-media work should not multiply outputs just because it can. Add a medium only when it carries something the others cannot.

Album v1 uses individual Output Records for concrete audio, cover, and text artifacts. A package-level Output Record is deferred until an export or publishing workflow creates a concrete package artifact.
