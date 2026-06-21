# Changelog

All notable changes to Artist OS are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
A changelog entry records the user-facing change, not the branch or commit narrative.

## [Unreleased]

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
