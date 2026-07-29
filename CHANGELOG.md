# Changelog

All notable changes to Artist OS are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
A changelog entry records the user-facing change, not the branch or commit narrative.

## [Unreleased]

## [1.0.0] - 2026-07-29

### Added

- Self-contained Codex release bundle with copy and symlink installation,
  installed-target verification, safe updates and uninstall, artifact metadata,
  and a SHA-256 checksum.
- Tracked, executable release evidence for the image, Video v0, audio, text,
  Album v1, and constrained Cross-Medium dry-run journeys.
- MIT license, security and support policies, privacy/network guidance,
  supported-environment matrix, and five-minute quickstart.
- Artist OS 1.0 release contract with an artist-approved scope freeze,
  change-control rule, explicit exclusions, blocking completion backlog, and
  release gate.
- Constrained Cross-Medium 1.0 target contract: lazy plan creation, one
  artist-confirmed primary medium, sequential supporting media, material-change
  invalidation, and terminal provider-free Asset Package compilation.
- Cross-Medium Plan `planned_deliverables` and `shared_references`: the plan now
  carries the checklist Package Compilation ticks off, and the references two or
  more active media depend on. Every active medium needs at least one planned
  deliverable, and a complete deliverable must name its Output Record.
- Cross-Medium Plan review and approval vocabulary: a Review Record can name a
  `cross_medium_plan` as the reviewed artifact (Mixed-Media Critic only, and it
  must name the governing Beat Plan), and a Gate Decision with
  `gate_type = "cross_medium_plan_approval"` must reference both the plan and its
  review.
- Package Format Selection And Completeness Gate vocabulary:
  `gate_type = "package_format_selection_and_completeness"` with a
  `package_completeness` block recording the Package Format, the completeness
  verdict, and — for a waiver only — the single `waived_slot_id`.
- A tracked fixture-backed Cross-Medium rehearsal at
  `tests/fixtures/cross-medium/article-with-photos-rehearsal/`: text primary plus
  image supporting over one reused Shared Story Spine, through accepted Output
  Records, the article-with-photos Package Format, the Completeness gate, and a
  complete Asset Package.
- `bin/artist-os-db status [project_id]`: read-only per-project status rows —
  status, stage, learning-review state, and index staleness against the
  on-disk manifest (ADR 0016).
- `bin/artist-os-db review-learnings`: plain-language promotion queue showing
  pending feedback with the exact command per choice, plus staged conductor
  candidates.
- `bin/artist-os-db add-conductor-rule`: adopt a local conductor rule as a
  dated line in `<workspace_library>/conductor-rules.md` (upgrade-safe, no
  eval re-bless), superseding the source candidate learning.
- `bin/artist-os-db sync --project <project_id>`: scoped sync that indexes one
  manifest and skips the missing-sweep; the feedback/learning/performance/
  review write commands now ride on it and also append their events to
  `events.jsonl`.
- `learnings-report` now prints each learning's actual rule text, scope, and
  evidence count; the learning-surfacing verbs self-heal (re-index from files
  before reading) and work on a fresh clone with no database.
- Manual image, sound, video, text, and mixed-media output import now validates the full Project
  Manifest and upstream lineage, confines durable paths to the active project,
  updates resume state, and refreshes SQLite.

- Reference Inventory (`schemas/reference-inventory.schema.json`): a project-level
  continuity record for promoted character, location, and object references — it
  owns effective policy, scan history, subject / package / per-output readiness,
  storage paths, Output Record refs, and provider-neutral role hints. Promoted
  subjects reuse `VisualReferenceSheetPlan` (character = 3 images, location = 3
  angles, object = 1 multi-section sheet). See ADR 0011.
- `bin/artist-os-db`: indexes Reference Inventory items and reference images
  (new `reference_inventory_items` / `reference_inventory_images` tables) and adds
  `publish-visible-reference`, which copies a reference Output Artifact into the
  visible Artist Library `References/<Category>/<subject>/{Review Drafts,Accepted}`
  folders and refreshes the SQLite index.
- Standing Sub-Agent Authorization: the conductor may spawn bounded internal
  sub-agents for mandatory reviews, validation, drafting passes, and approved
  orchestration without per-spawn approval. Review Records carry
  `reviewer_execution.fallback_reason` when a host or active tool policy forces
  the degraded reviewer fallback.
- Video path defaults a requested storyboard generation to one composite
  multi-panel storyboard sheet; individual storyboard stills are a separate
  artifact requiring their own provider approval and Output Records.
- Delegated worker I/O is now schema-backed with
  `schemas/delegation-packet.schema.json` and
  `schemas/subagent-result.schema.json`, plus fixture and contract coverage for
  status, recommended action, and forbidden-action vocabularies.

### Changed

- Current architecture, journey, gate, storage, packaging, and runtime
  documentation now distinguish implemented foundations from unfinished 1.0
  behavior and post-1.0 work.
- Long-Work Stewardship now consistently requires ADR 0013 eligibility plus
  explicit ADR 0015 artist activation; routing recommendations do not create a
  stewardship record.
- Micro-video planning now requires a compact Video Creative Brief, bounded
  Video Critic Review, and explicit Brief Approval before storyboard handoff or
  generation.
- Embedded Sound Creative Brief lyrics are planning material; standalone lyric
  outputs use Text Journey approval and Output Record provenance.
- Suno output wording now says “Custom Mode field export” to avoid implying
  that Artist OS generates audio.
- Image outputs now record `reference_refs_used` so downstream usage is traceable
  back to Reference Inventory subjects (availability lives in the inventory; usage
  lives on the consuming output).
- `bin/artist-os-eval bless` now refuses to update `blessed.lock` unless the
  conductor-behavior grade records the live conductor digest and
  `Overall result: PASS`; `start` stamps the digest into the scaffolded grade.

### Fixed

- The local schema validator now enforces every JSON Schema keyword used by the
  repository (`oneOf`, date-time `format`, property counts, and schema-valued
  `additionalProperties`) and fails closed when a future unsupported keyword
  appears. `bin/validate-examples` also fails when it discovers zero targets.
- Output import journals the Output Record, event, and Project Manifest as a
  recoverable transaction, preventing a failed write or interrupted process
  from leaving partial durable state.
- `bin/artist-os-db sync` is fault-isolated: one corrupt or wrong-shape
  `project.json` or event line no longer aborts indexing for sibling
  projects, present-but-broken manifests are not swept to `missing`, and a
  missing or unreadable `events.jsonl` preserves previously indexed events
  instead of erasing them (ADR 0016).
- Asset Package waivers are now genuinely per slot. A `complete` package whose
  required slots were all waived by one shared `waiver_gate_id` used to validate,
  which is exactly the general “ship anyway” decision the release contract
  forbids; waiver gate ids must now be distinct, and a `filled` slot may not
  carry one at all.

The `0.2.0`, `0.3.0`, and `0.4.0` sections below document internal development
milestones. They were not certified distribution bundles and do not require
retroactive immutable tags. `1.0.0` is the first fully certified
distribution.

## [0.4.0] - 2026-06-21

### Added

- `bin/artist-os-eval`: gates re-blessing on the (manual, token-spending)
  conductor-behavior eval. `status` reports whether the live conductor still
  matches the eval-validated digest in `evals/conductor-behavior/blessed.lock`,
  `bless` records the current conductor as validated, and `start` snapshots the
  conductor and scaffolds a grade sheet for a run. `tests/test_conductor_eval_lock.py`
  turns the digest check into a CI gate, so editing the conductor without
  re-blessing fails loudly.
- `bin/artist-os-db learnings-report [project_id]`: a read-only close-out that
  summarizes each project's learning-review state, linked learnings, and
  performance signals, ending with the next action.

## [0.3.0] - 2026-06-21

### Added

- `bin/artist-os-lint`: a skill linter that flags any skill whose frontmatter is
  missing a non-empty `name:` or `description:`, that references repo-root paths
  without the `$ARTIST_OS_ROOT` anchor sentence, or that references a doc/schema
  that does not resolve under the bundle root. Human-readable FAIL output and a
  non-zero exit, so it runs both as a CLI and in CI.
- `bin/artist-os-new-skill <name>`: scaffolds a lint-clean `skills/<name>/SKILL.md`
  and registers the skill in the three sync sites the suite enforces — the
  installer `skills=( … )` array, the conductor delegation list, and the routing
  eval `skills[]` — then prints the authoring steps that remain. Aborts without
  writing anything if a registration anchor cannot be found.

## [0.2.0] - 2026-06-21

### Added

- Multi-host distribution foundation (ADR 0008): a `bin/artist-os-paths` anchor
  resolver, a `packaging/hosts.json` host registry, and a `packaging/MANIFEST.json`
  travel manifest. `artist-os-paths doctor` verifies an installed bundle and
  fails loud on any missing manifest path or orphaned skill-body reference.

### Changed

- Skill bodies that reference repo-root docs and schemas now state that those
  paths resolve from `$ARTIST_OS_ROOT`.
- `bin/install-codex-dev-skills` reads Codex's install target and skill prefix
  from the host registry and verifies the bundle with `artist-os-paths doctor`
  after installing.

## [0.1.0] - 2026-06-20

Initial versioned release.
