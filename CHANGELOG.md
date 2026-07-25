# Changelog

All notable changes to Artist OS are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
A changelog entry records the user-facing change, not the branch or commit narrative.

## [Unreleased]

### Added

- Artist OS 1.0 release contract with an artist-approved scope freeze,
  change-control rule, explicit exclusions, blocking completion backlog, and
  release gate.
- Constrained Cross-Medium 1.0 target contract: lazy plan creation, one
  artist-confirmed primary medium, sequential supporting media, material-change
  invalidation, and terminal provider-free Asset Package compilation.
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
