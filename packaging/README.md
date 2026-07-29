# Artist OS distribution / packaging

This directory holds the **hand-authored source** that describes how Artist OS
skills are packaged and installed across hosts. It is not build output.

- `hosts.json` — the host registry, one entry per target host. `codex` is the
  primary, active host and its entry is the identity transform of today's
  installer (`pathRewrites: []`, passthrough frontmatter, symlink-or-copy
  linking). `claude-code` and `cursor` are `status: "stub"` placeholders for the
  future per-host generator; their transform fields are `null` until a host
  actually diverges. See ADR 0008.
- `MANIFEST.json` — the authoritative set of files that must travel with an
  installed bundle so the public skill body and internal mode files resolve
  paths from `$ARTIST_OS_ROOT`, plus an exclusion list that keeps private state
  (`workspace-library/`, `artist-os-library/`, `*.sqlite`, `.env`, …) out of any
  bundle.

`globalRoot` in the registry is **relative to `$HOME`** (e.g. `.codex/skills`
means `$HOME/.codex/skills`); a host installer may override the base (Codex via
`CODEX_SKILLS_DIR`). The registry stores the home-relative segment, not the
absolute path.

## Anchor resolution

The anchor `$ARTIST_OS_ROOT` is resolved at runtime by `bin/artist-os-paths`:

```
bin/artist-os-paths root          # print the resolved bundle root
bin/artist-os-paths doctor        # verify manifest paths AND every skill-body reference resolve
bin/artist-os-paths list-hosts    # list registered hosts and their status
bin/artist-os-paths get <host> <key>   # read a registry value
bin/artist-os-paths validate      # check the registry's shape
```

`root` and `get` print a single **raw** value on one line, meant to be captured
with command substitution (`r=$(bin/artist-os-paths root)`); the output is not
shell-quoted, so do not `eval` it. `get` exits non-zero on an unknown host or an
unknown key (so a typo fails loud) and prints empty only for a present-but-null
field.

Resolution uses a loud fallback chain — `ARTIST_OS_ROOT` env var (sentinel
checked) → resolver-relative bundle root → `git rev-parse --show-toplevel` — and
**never** falls back to the working directory. `doctor` fails loud if any
manifest path, or any file named in a skill body, is missing under the root.

## Runtime and developer commands

Everything in the `MANIFEST.json` include list must ship in the 1.0 bundle—the canonical root docs
(`THEORY.md`, `ARCHITECTURE.md`, `AGENTS.md`, `CONTEXT.md`), the
root helper modules, selected runtime commands, `docs/`, `schemas/`, the public
`artist-os` skill plus internal mode files under `skills/artist-os/references/`, and this `packaging/`
dir—and is the single source of truth, edited by hand.

Shipped runtime commands are `artist-os-db`, `artist-os-import-output`,
`artist-os-paths`, `artist-os-video-finalize`, `install-codex-skills`, and
`uninstall-codex-skills`.

The bundle excludes checkout-only commands whose inputs live in tests,
examples, or eval resources: `artist-os-build-bundle`, `artist-os-eval`,
`artist-os-lint`, `artist-os-new-skill`, `artist-os-storage-smoke`,
`validate-examples`, `install-codex-dev-skills`, and
`uninstall-codex-dev-skills`. Tracked release-certification evidence also stays
in the repository because it points to repository-only fixtures and tests.

## Build and verify

Generate the ignored Codex install tree, archive, release metadata, and
checksum:

```bash
bin/artist-os-build-bundle --require-clean
```

The output lives in `packaging/build/codex/`. Its root contains a
Codex-discoverable `SKILL.md` plus the complete manifest surface. Materializing
from Git-tracked files prevents ignored local files from leaking into an
artifact. Verification runs `doctor` against the materialized target, scans
exclusions, sensitive filenames, and private-key markers, checks
version/commit/manifest metadata, and rejects symlinks.

Verify an existing bundle:

```bash
bin/artist-os-build-bundle \
  --verify-bundle packaging/build/codex/artist-os-1.0.0 \
  --expected-version 1.0.0 \
  --expected-commit "$(git rev-parse HEAD)"
```

`bin/install-codex-skills` defaults to a full copy. `--mode symlink`
intentionally links Codex to the extracted bundle. Both modes verify the
installed target and preserve the separate Workspace Library during update and
uninstall.

Generated trees under `packaging/build/<host>/` are never edited by hand.
Future non-Codex host transforms remain deferred; see ADR 0008.
