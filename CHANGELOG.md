# Changelog

All notable changes to Artist OS are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
A changelog entry records the user-facing change, not the branch or commit narrative.

## [Unreleased]

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
