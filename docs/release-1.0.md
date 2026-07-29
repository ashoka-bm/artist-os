# Artist OS 1.0 Release Contract

Status: **scope frozen and artist-approved on 2026-07-25**.

This document is the authoritative boundary and completion checklist for
Artist OS 1.0. `docs/progress.md` records implementation history and later
roadmap ideas; when a roadmap item conflicts with this contract, this contract
wins.

## Release Claim

Artist OS 1.0 is a Codex-only supported, dry-run creative operating system that turns an
artist-provided text Reference into traceable image plans, storyboard-ready
video plans, sound plans, written drafts, Album v1 plans, and constrained
multi-medium packages while preserving Artist Meaning, Intended Feeling,
review authority, and provenance.

Dry-run means Artist OS can create and review briefs, plans, prompts, written
artifacts, provider-specific prompt packages, and metadata. It can import
artist-owned outputs and compile accepted outputs into a package. It does not
promise provider-backed generation, publishing, or finished video rendering.

## Change Control

The freeze works as follows:

- An item enters or leaves 1.0 only through an explicit artist-approved edit to
  this document.
- New feature ideas go to post-1.0 unless they replace an existing in-scope item
  without increasing release risk.
- Bug fixes, safety fixes, database reliability work, and documentation
  corrections may enter 1.0 when they protect an existing release promise.
- A discovered blocker may add work to the completion checklist, but it does
  not silently expand the product claim.
- The release is complete only when every checkbox under **Blocking Completion
  Backlog** is complete and the **Release Gate** passes.

## In Scope

### Shared typed pipeline

- Source Record, Artist Meaning, Transformation Brief, Beat Plan, Medium Plan,
  Creative Brief, Prompt Plan or Text Generation Plan, Output Record, Review
  Record, Gate Decision, and Asset Package traceability.
- Explicit artist gates, mandatory bounded reviews, blocking-finding handling,
  and recorded waivers.
- Project persistence before phase advancement, SQLite-backed discovery,
  resume state, and manual output import.

### Implemented medium journeys

- Image: single images, series, collections, Prompt Variant Plans, and Prompt
  Branch Sets.
- Video v0: Video Medium Plans, sequences, scenes, storyboard shots, composite
  storyboard-sheet planning, reference planning, and optional post-storyboard
  Seedance Prompt Packages. Finished video is not a 1.0 promise.
- Audio: Sound Medium Plans and Sound Prompt Plans with Suno Custom Mode
  field exports, plus ElevenLabs v3 voice-over prompt preparation for approved
  text. These prepare provider fields; they do not generate audio. Provider
  calls are not a 1.0 promise.
- Text: Text Medium Plans, Text Generation Plans, approved local drafting,
  conformance review, Clear Writing Pass, Human Voice Pass, and revision Output
  Records.
- Illustrated written work: Text Journey coordinated with Image Journey through
  an Illustration Plan.

### Album v1

“Album v1” names the first revision of the Album workflow; it is not a separate
product version from Artist OS 1.0.

- A sound-primary Album Release Package Plan with ordered tracks, album and
  Track Cover planning, release copy, Album Sonic System, Album Visual System,
  representative calibration, Mixed-Media Critic Review, and normal per-output
  gates.
- Album is the only 1.0 Release Package subtype.

### Constrained Cross-Medium Plan orchestration

General Cross-Medium Plan orchestration outside Album is part of 1.0 with this
exact boundary:

1. A Cross-Medium Plan materializes only when the artist activates a second
   medium on an existing project or explicitly requests a multi-output package.
2. Every active medium reuses one unchanged Shared Story Spine: Artist Meaning,
   Transformation Brief, Beat Plan, and the standing Story Approval.
3. Artist OS recommends one primary medium and the artist confirms it. Every
   other medium is supporting by default.
4. The Cross-Medium Plan owns Medium Roles, planned deliverables, production
   order, Effective Project Scale, shared references, and cross-medium
   continuity. Medium-specific creative decisions remain in independently
   reviewed and locked Medium Plans.
5. Supporting media default to compact treatment but retain the standard
   medium-specific reviews and gates.
6. Production is sequential in 1.0. The primary realization anchors supporting
   media when the approved production order requires it.
7. Mixed-Media Critic Review checks the plan before the artist approves it.
   Production does not expand into supporting media while the plan is
   unapproved.
8. A material change to included media, Medium Roles, production order, or
   shared continuity invalidates the prior plan approval, reruns the affected
   review, and requires a new artist decision.
9. Package Compilation runs only after the included concrete outputs have
   accepted Output Records. Missing deliverables require an explicit recorded
   waiver.

Cross-medium 1.0 does not include arbitrary workflow graphs, simultaneous
multi-medium production, multiple primary media, campaign management,
publishing, distribution, or automatic reconciliation of conflicting medium
decisions.

### Storage reliability and manual learning

- Files remain the source of truth and SQLite remains a rebuildable query
  projection.
- Database sync must be fault-isolated, scoped where appropriate,
  non-destructive toward unrelated projects, and self-healing for learning
  reads.
- Feedback, Learning Records, and Performance Signals may be captured and
  reviewed through explicit commands.
- Learning review and promotion are manual and human-gated in 1.0.
- The conductor does not automatically run session-start learning review,
  automatically apply stored learnings, triage open projects, run Close-Out
  capture, or mutate its behavior from local rules in 1.0.

### Distribution

- Codex installation, update, path validation, Workspace Library setup, resume,
  and uninstall after the packaged artifact passes release certification.
- The repository and packaged Codex bundle are the supported 1.0 distribution
  surfaces.
- Source-checkout installation is currently a development surface, not the
  released 1.0 install path.

## Explicitly Post-1.0

- Provider adapters, API-key setup, guaranteed provider-backed generation, and
  provider-run or output-batch records.
- Finished video generation and publishing or distribution automation.
- Automatic human-edit detection in the visible Artist Library.
- EP, Single Bundle, Visual Album, campaign, and publishing-specific routers.
- Parallel general multi-medium production and campaign calendars.
- Claude, Cursor, or other host support beyond the current Codex distribution.
- Durable taste memory, calibration-choice records, and accepted-work
  promotion records.
- Automatic conductor self-improvement: session-start learning application,
  open-project triage, automatic Close-Out capture, and automatically loaded
  behavior-changing local rules.

## Blocking Completion Backlog

The order is intentional: close the contract, protect persistence, then certify
the release.

### 1. Freeze and documentation

- [x] Record the artist-approved 1.0 product claim, in-scope behavior,
  exclusions, and change-control rule in this document.
- [x] Reconcile the mixed-media status language so thin Cross-Medium Plan
  orchestration is distinguished from deferred package and campaign routers.
- [x] Make `docs/progress.md` point to this contract instead of treating provider
  expansion or automatic edit detection as the immediate release path.
- [x] Record the 1.0 split in ADR 0016: database hardening and manual learning
  surfaces are in; automatic conductor wiring is deferred.
- [x] Reconcile Long-Work activation, Album approval order, conditional Story
  Critic applicability, mandatory Output Critic review, Lyrics Draft
  provenance, conditional Package Compilation, and per-slot package waivers
  across the current contracts.
- [x] Align the root architecture, story architecture, medium journey diagrams,
  canonical critic/gate docs, storage docs, and runtime Markdown with the
  frozen target behavior. Historical drafts remain point-in-time records.

### 2. Complete the thin Cross-Medium Plan lifecycle

- [x] Add `cross_medium.plan` to the typed pipeline and structural transition
  list, including lazy creation, Mixed-Media Critic Review, artist approval,
  material-change invalidation, and terminal Asset Package compilation.
- [x] Extend the Cross-Medium Plan schema with schema-backed planned
  deliverables and shared references, plus valid and invalid fixtures.
- [x] Add the required Cross-Medium Plan gate and review vocabulary to Gate
  Decision and Review Record schemas, including artifact/upstream refs, with
  valid fixtures and negative tests.
- [x] Add the Package Format Selection and Completeness gate vocabulary and
  upstream refs, and require one Gate Decision for each waived required slot.
- [x] Wire the conductor to create the plan on second-medium activation or an
  explicit multi-output request, confirm one primary medium, keep supporting
  media sequential, and refuse expansion before approval.
- [x] Add transition and behavior tests that prove the Shared Story Spine is
  reused by id and is not recreated for a supporting medium.
- [x] Run one fixture-backed rehearsal from a primary medium through a supporting
  medium, accepted Output Records, Package Format selection, Completeness gate,
  and Asset Package creation.

This section is complete as implementation. The changed conductor passed its
real behavior evaluation and the current digest was blessed on 2026-07-28.
The Cross-Medium fixture lives in
`tests/fixtures/cross-medium/article-with-photos-rehearsal/` and is indexed by
`release-evidence/1.0.0/manifest.json`. The adjacent
`rehearsal-run.json` records the executed six-route verification command,
environment, result, and record-set digest.

### 3. Integrate database reliability hardening

- [x] Rebase or selectively integrate `self-improvement-db-hardening` onto the
  release branch without the automatic conductor loop from
  `conductor-learning-loop`.
- [x] Preserve per-project fault isolation, scoped sync, event integrity,
  read-path self-healing, and a read-only status surface.
- [x] Keep feedback and learning capture/review explicitly invoked; do not add
  session-start application, automatic triage, or automatic Close-Out behavior.
- [x] Re-run the database suite against corrupt siblings, missing event logs,
  stale indexes, fresh databases, and scoped writes.

### 4. Clear release regressions

- [x] Resolve the stale conductor eval lock by running the real conductor
  behavior eval and blessing only a passing, current digest.
- [x] Make the local schema validator implement every JSON Schema keyword used
  by repository schemas—or fail closed on unsupported keywords—including
  `oneOf`, `format`, `minProperties`, `maxProperties`, and schema-valued
  `additionalProperties`. Add negative probes and make zero validation targets
  a failure.
- [x] Harden manual output import: confine all resolved paths to the Workspace
  Library, validate the complete manifest and upstream lineage, make
  record/event persistence atomic or recoverable, update manifest/resume state,
  refresh SQLite, and test traversal and event-write failure.
- [x] Confirm all schemas and fixtures validate after validator hardening.
- [x] Confirm the full unit suite, Python compilation, shell syntax checks,
  JSON parsing, skill lint, path doctor, storage smoke, and
  distribution-manifest checks pass from a clean checkout.
- [x] Smoke-test install, update, Workspace Library setup, resume discovery,
  output import, and uninstall in disposable directories.

### 5. Distribution correctness

- [x] Build a materialized Codex bundle containing every `MANIFEST.json`
  include and none of its exclusions.
- [x] Decide which commands are runtime versus developer-only, then ensure each
  shipped command carries its required examples, tests, eval resources, or is
  excluded from the runtime bundle.
- [x] Verify `doctor` against the installed target rather than the source
  checkout.
- [x] Cover copy mode and symlink mode, update, and uninstall while preserving
  the Workspace Library.
- [x] Prove the installed runtime still works after the checkout is moved or
  removed.
- [x] Generate an artifact checksum and verify artifact version, commit SHA,
  `VERSION`, changelog, and release tag agree.

### 6. Public release readiness

- [x] Publish a supported-environment matrix for Codex, operating systems,
  Python, Bash, and Git based on completed release smoke tests.
- [x] Choose and ship a license, or explicitly declare 1.0 private/internal.
- [x] Add security-reporting and supported-version guidance.
- [x] Document the privacy/network boundary: local persistence, Codex host/model
  processing, optional web research, and absent provider-generation adapters.
- [x] Add a five-minute quickstart, expected gates/output locations, resume,
  update, doctor troubleshooting, uninstall, and a concise Video v0 example.
- [x] Reconcile `CHANGELOG.md` against the full 1.0 commit range and decide
  whether untagged 0.2–0.4 entries are internal milestones or require justified
  immutable tags.

### 7. Release certification

- [x] Run end-to-end dry-run rehearsals for image, video v0, audio, text, Album
  v1, and the constrained Cross-Medium Plan route.
- [x] Store tracked rehearsal evidence in a defined release-evidence manifest;
  ignored `.tmp` output is not release proof.
- [x] Verify that every concrete artifact in the rehearsals has an Output Record
  before review and acceptance, and that packages contain only accepted or
  explicitly waived slots.
- [x] Review public language for claims that exceed this contract.
- [x] Move the completed changelog entries into a `1.0.0` release section, set
  `VERSION` to `1.0.0`, and verify their consistency.
- [x] Tag 1.0 only after the working tree is clean and every release command
  below passes.

## Release Gate

Run from the repository root:

```bash
bin/validate-examples
python3 -m unittest discover -s tests -p 'test_*.py'
python3 -m py_compile $(rg --files -g '*.py')
bash -n bin/install-codex-dev-skills bin/uninstall-codex-dev-skills
bash -n bin/install-codex-skills bin/uninstall-codex-skills
bin/artist-os-lint
bin/artist-os-paths validate
bin/artist-os-paths doctor
bin/artist-os-storage-smoke
bin/artist-os-eval status
bin/artist-os-build-bundle --require-clean
jq empty schemas/*.json examples/*.json
jq empty release-evidence/1.0.0/*.json
git diff --check
test -z "$(git status --porcelain)"
```

The gate passes only when:

- every command exits successfully,
- the conductor digest is backed by a real passing eval,
- all six release rehearsals have recorded evidence,
- a materialized release artifact passes installed-target verification and the
  exclusion/sensitive-file scan,
- no blocking review finding or unrecorded waiver remains,
- `VERSION` and the latest released changelog header both say `1.0.0`,
- and every blocking backlog item above is checked.

## Baseline At Freeze

On 2026-07-25:

- `bin/validate-examples` validated 113 records successfully;
- Python compilation, shell syntax checks, and `git diff --check` passed;
- the unit suite ran 419 tests with one failure:
  `test_real_conductor_matches_blessed_lock`, caused by a stale conductor eval
  lock on `main`;
- `self-improvement-db-hardening` contained the database reliability work but
  had not yet been integrated into `main`.

This baseline is evidence for the backlog, not a release pass.
