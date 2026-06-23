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

## Source vs generated

Everything the `MANIFEST.json` include list ships — the canonical root docs
(`THEORY.md`, `ARCHITECTURE.md`, `AGENTS.md`, `CONTEXT.md`), the
`artist_os_schema_validator.py` module, `bin/`, `docs/`, `schemas/`, the public
`artist-os` skill plus internal mode files under `skills/artist-os/references/`, and this `packaging/`
dir — is the single source of truth, edited by hand. The
future generator (`bin/artist-os-generate`, ADR 0008 "Later") will write
per-host install trees to `packaging/build/<host>/` (gitignored) carrying an
`AUTO-GENERATED — do not edit` header; those are never edited by hand. See
`docs/adr/0008-multi-host-skill-distribution.md`.
