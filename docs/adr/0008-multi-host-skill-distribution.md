# Multi-Host Skill Distribution

Status: accepted.

Artist OS will distribute its skills as a self-contained, install-anchored bundle resolved at runtime through one anchor, `$ARTIST_OS_ROOT`, governed by a data-only host registry, with the per-host generator deferred but seamed. We choose this over today's symlink-accidental reachability and over copying canonical docs into each skill, because the first orphans the reference surface on any non-symlink host and the second breaks single-source-of-truth.

The problem is concrete. An installed leaf skill lives at `~/.codex/skills/<name>/SKILL.md`, yet its body names ~38 repo-root-relative paths (`THEORY.md`, `AGENTS.md`, `docs/**`, `schemas/**`; the conductor alone references 27). Under copy-mode install only the ~20 in-repo skill files travel; the referenced files plus the ~110-file `docs/`+`schemas/` base sit *above* the installed directory and are unreachable. Symlink-mode reaches them only by accident — because the symlink resolves back into a checkout — and no sentence anywhere tells an agent where those paths are supposed to resolve from. Because those schemas are load-bearing for the provenance invariant (ADR 0003), they cannot simply be dropped from what installs.

The fix is a self-contained bundle made resolvable, not a transform engine. Skill bodies gain one anchor sentence naming `$ARTIST_OS_ROOT` and keep their bare path strings unchanged. A resolver, `bin/artist-os-paths`, computes the anchor via a loud fallback chain — an explicit env var, then the resolver's own bundle root, then `git rev-parse --show-toplevel`, else a non-zero exit naming what is missing and pointing at the doctor command — and never falls back to the current working directory. The installer materializes the bundle so every referenced doc and schema travels with the skills.

Multi-host support lives in data, not code. A `packaging/hosts.json` registry lifts the installer's hardcoded values into a Codex entry and stubs Claude Code and Cursor. Codex is the primary host and its entry is the identity transform of today's installer (`pathRewrites: []`, passthrough frontmatter, symlink-or-copy linking) — which is precisely why the generator can be deferred honestly: the "generator" for the only live host is what the installer already does. Adding a host later becomes config-fill plus one wiring script, not a restructure.

We mirror G-Stack's cheap, proven patterns: one data config per host, an all-hosts list with the host set derived from it, co-located validators exercised by a test, a single `usesEnvVars` switch for the anchor, a primary host with empty rewrites, and a config-to-bash bridge so the installer reads the registry instead of hardcoding paths. We deliberately skip its heavy machinery — no `.tmpl`/placeholder engine, no frontmatter transform DSL (allowlist/denylist/conditionalFields/renameFields/toolRewrites), no host-adapter escape hatch — which is still overkill for one public skill plus internal mode files across 2 hosts. The registry is JSON rather than TypeScript because the runtime is Python + bash with no TS toolchain; a `validate` subcommand plus a Python test recover the config-validation guarantee.

## Structure

- **Anchor.** The public skill body and internal mode files carry an anchor sentence: paths like `THEORY.md`, `docs/...`, `schemas/...`, and `skills/...` resolve from `$ARTIST_OS_ROOT` — the repo root in a checkout, the bundle root in a Codex install. If a referenced file is missing, run `bin/artist-os-paths doctor`.
- **Resolver.** `bin/artist-os-paths` (Python, modeled on `bin/artist-os-db`) with subcommands `root | get <host> <key> | doctor | list-hosts | validate`, emitting raw one-line output so the bash installer can consume it with quoted command substitution.
- **Host registry.** `packaging/hosts.json` — data only. Codex populated; `claude-code` and `cursor` carry `status: "stub"` with null transform fields, and the Claude stub records a `marketplace` block for later plugin packaging.
- **Manifest.** `packaging/MANIFEST.json` lists the reference surface that must travel (paths, not content) plus an exclusion list for private state (`workspace-library/`, `.tmp/`, `*.sqlite`, `.env`).
- **Boundary doc.** `packaging/README.md` states the source-vs-generated boundary; any future generated tree carries an `AUTO-GENERATED — do not edit` header so no installed copy becomes a second editable source of truth.

## What ships now vs later

**Now** (additive, except one anchor sentence per reference-bearing skill and the installer change):

- `bin/artist-os-paths` resolver with the loud fallback chain.
- The anchor sentence in the reference-bearing public skill body and internal mode files.
- `packaging/hosts.json`, `packaging/MANIFEST.json`, `packaging/README.md`.
- Installer materializes only the public `artist-os` skill while the internal mode files travel inside the bundle under `skills/artist-os/references/`. It reads Codex's prefix/target via `artist-os-paths get codex`, removes retired old public skill links, and runs `doctor` post-install and in CI to fail loud on orphaned references.
- New tests: `test_host_registry.py` (parse, primary-host key, name regex, root uniqueness, stub flags), `test_dist_manifest.py` (every manifest path exists and every bare doc/schema reference resolves to an existing file under an included tree — a live drift gate), `test_anchor_resolver.py` (loud-fail behavior + resolution from a temp install).

**Later** (the deferred generator — no source move, no test-path change):

- `bin/artist-os-generate <host|all> [--dry-run]` looping the registry, where `materialize_host(config)` is today's identity install for Codex.
- Populating the stub null fields per host; Claude plugin-marketplace packaging (which, per the sandbox research, must rewrite the bare repo-root references to skill-relative paths and bundle referenced content inside the plugin, since plugins cannot read outside their own directory); per-host frontmatter transforms and `pathRewrites` only when a host actually diverges; golden fixtures once a second transform style exists; further hosts as a one-line registry edit.

## Considered Options

- **Minimal seams, no materialized bundle** — lowest churn, but the anchor stays documentation-only, so copy-mode and Claude still orphan the references. Adopted as the spine and extended with the resolver + materialized bundle.
- **Walking-skeleton generator with golden trees now** — rejected for now: that is exactly the deferred work, and the seam slots it in later without restructuring.
- **Full path rewrite of all ~38 strings to `$ARTIST_OS_ROOT/...`** — rejected as highest-churn; it would force edits to the body-substring contract tests. We took its resolver + bundle idea but kept the path strings bare.
- **TypeScript registry** — rejected: no TS runtime in this repo. A `validate` subcommand plus a Python test recover the compile-time guard.

## Consequences

- **Resilience is real, not documented.** Everything travels, the anchor resolves with no cwd dependence, missing content fails loud via the resolver and `doctor`, and the manifest test keeps the travelling set honest.
- **SSoT is strengthened.** No doc or schema is duplicated as an editable copy; the new artifacts are a path list and a data registry. Phase Order stays solely in `skills/artist-os/SKILL.md`; the README overview diagrams, the byte-exact pointer fragments in `AGENTS.md` and `ARCHITECTURE.md`, and ARCHITECTURE.md's "does not maintain a third copy" line are untouched.
- **Multi-host is seam-ready.** Codex is supported; Claude Code (marketplace recorded) and Cursor are stubbed; adding the generator is config-fill plus one script reading `hosts.json` + `MANIFEST.json`.
- **At-risk tests are handled.** `test_phase_order_doc_drift` still owns the conductor's canonical phase order. `test_skill_set_sync` now protects the single public skill rather than every internal mode file. The contract tests pin logical modes at their internal paths. The registry/manifest directory is named `packaging/` rather than `dist/` to signal hand-authored source, not build output.
- **Tradeoffs.** Copy-mode now carries the whole bundle, so `install_skill` idempotence and refuse-overwrite need re-testing (doctor guards this). JSON loses compile-time typing (mitigated by validate + test). The Claude plugin sandbox **does** force the bundle inside the package: installed plugins cannot read outside their own directory, and `${CLAUDE_PLUGIN_ROOT}` does not expand in SKILL.md markdown (issue #9354). So `$ARTIST_OS_ROOT` is the Codex/checkout mechanism; the Claude host generator must rewrite the bare references to skill-relative paths and bundle the referenced content inside the plugin (a shared directory plus per-skill `references/` symlinks, which Claude dereferences at install). This is now a known generator requirement rather than an open question. The routing eval is high-variance, so the anchor edit should be re-checked in A/B worktrees even though the routable set is unchanged.
