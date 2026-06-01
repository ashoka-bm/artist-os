# Artist Generation

This README currently describes the repository we are building, not a finished artist-facing product. It is part of the build-process documentation alongside `PROGRESS.md` and the reference docs in `docs/`.

Artist Generation is a repository for building agent-ready workflows that help artists create digital assets with AI. The initial target asset types are images, audio, and video, with room to add additional creative media formats as the system matures.

The goal is to become a robust plugin and skill collection that agents can use to plan, prompt, generate, evaluate, iterate, and package creative assets while preserving the artist's intent.

## Product Direction

Artists should be able to:

- Describe an artistic goal in natural language.
- Select or infer the right generation workflow for the medium.
- Iterate on prompts, references, constraints, and outputs.
- Track generated assets, source prompts, model settings, and rights notes.
- Hand work to agents without losing context between sessions.

Agents should be able to:

- Load clear project context at the start of a session.
- Choose the right media workflow from explicit skills or commands.
- Ask targeted questions when artistic direction is ambiguous.
- Produce structured outputs that can be reviewed, regenerated, or extended.
- Keep generation metadata attached to the resulting asset.

## GStack Inspiration

This repo borrows from GStack's shape, not by copying implementation wholesale, but by adopting the useful operating model:

- Top-level docs explain purpose, architecture, and current progress.
- Skills are the primary interface for agents.
- Workflows are specialist roles with clear triggers and outputs.
- Tooling should be scriptable, testable, and safe by default.
- Session memory should be explicit enough that a future agent can resume quickly.

## Documentation Tracks

There are two documentation tracks:

- Build-process docs help us build this repository: `README.md`, `PROGRESS.md`, `docs/IMPLEMENTATION_PLAN.md`, `docs/gstack-repo-map.md`, and `docs/superpowers/plans/2026-05-28-build-artist-os.md`.
- Product docs define the artist operating system itself: `AGENTS.md`, `ARCHITECTURE.md`, `THEORY.md`, `CONTEXT.md`, `docs/metadata-schema.md`, `docs/text-to-sound/`, `schemas/`, `examples/`, and `skills/`.

When a product document exists, it should become the source of truth for that area. Build-process docs should link to it rather than duplicate it.

Current structure:

```text
.
├── README.md
├── PROGRESS.md
├── AGENTS.md
├── ARCHITECTURE.md
├── CONTEXT.md
├── THEORY.md
├── examples/
│   ├── text-source.md
│   ├── asset-metadata.example.json
│   ├── text-creative-brief.example.json
│   ├── text-prompt-plan.example.json
│   ├── text-sound-creative-brief.example.json
│   ├── text-sound-prompt-plan.example.json
│   └── project-manifest.example.json
├── schemas/
│   ├── source-record.schema.json
│   ├── artist-os-library.sql
│   ├── asset-metadata.schema.json
│   ├── creative-brief.schema.json
│   ├── prompt-plan.schema.json
│   ├── sound-creative-brief.schema.json
│   ├── sound-prompt-plan.schema.json
│   └── project-manifest.schema.json
├── bin/
│   ├── artist-os-db
│   ├── install-codex-dev-skills
│   └── uninstall-codex-dev-skills
├── skills/
│   ├── first-slice-flow/
│   ├── ingest-reference/
│   ├── meaning-interview/
│   ├── text-to-image-plan/
│   ├── text-to-suno-plan/
│   ├── art-critic-review/
│   └── critique-asset/
├── docs/
│   ├── text-to-sound/
│   │   ├── THEORY.md
│   │   └── ARCHITECTURE.md
│   └── ...
└── docs/superpowers/plans/
```

Do not add `setup`, `hosts/`, `lib/`, or provider adapters until the manual First Slice proves the workflow.

## Workspace Library

Real Artist OS project work is stored outside git in:

```text
workspace-library/artist-os/
```

This local library stores project manifests, event logs, source records, meaning interviews, gate decisions, Creative Brief records, Prompt Plans, critiques, generated images, and image sidecar metadata. See `docs/storage.md`.

Generated media and private artist work must not be committed. The repository only commits schemas, examples, and skill instructions.

Each real project has a `project.json` manifest and `events.jsonl` history. Images live under `assets/reference`, `assets/boards`, `assets/generated`, or `assets/final`, and each image gets a same-basename `.json` sidecar that validates against `schemas/asset-metadata.schema.json`.

The searchable local database is:

```text
workspace-library/artist-os/artist-os.sqlite
```

It uses SQLite through Python's standard library and does not require an additional package install. Create or refresh it with:

```bash
bin/artist-os-db setup
bin/artist-os-db sync
```

## Codex Dev Install

Install the local Artist OS skills into Codex with symlinks:

```bash
bin/install-codex-dev-skills
```

This creates namespaced links under `~/.codex/skills`:

```text
artist-os
artist-os-ingest-reference
artist-os-meaning-interview
artist-os-text-to-image-plan
artist-os-text-to-suno-plan
artist-os-art-critic-review
artist-os-critique-asset
```

The `name:` field inside each role skill uses the same namespaced value, so invoke them with the `artist-os-*` names above.

For the normal end-to-end dry run, start with `artist-os`. It asks whether unclear text should become visual art or a Suno music prompt. The other skills are role-specific entry points for debugging or resuming a single phase.

The repo remains the source of truth. Editing files under `skills/` updates the installed Codex skills immediately through the symlinks. Codex may still require a new thread or app reload to refresh skill discovery.

The installer also creates the local Workspace Library folders and initializes `artist-os.sqlite`. Set `ARTIST_OS_LIBRARY_ROOT` before running it to use a different storage location.

Uninstall only these dev links with:

```bash
bin/uninstall-codex-dev-skills
```

## Current Milestone

The active milestone is the dry-run First Slice:

```text
Text Reference
  -> Source Record
  -> Meaning Interview
  -> Creative Brief Document
  -> Symbology Direction
  -> Style Direction
  -> Series Recommendation
  -> Art Critic Review
  -> Brief Approval
  -> Minimalist-to-Maximalist Direction
  -> Creative Brief Record
  -> Provider-Neutral Image Prompt Plan
```

This milestone does not call paid providers. It produces a Provider-Neutral Image Prompt Plan with Faithful, Amplified, and Minimal Prompt Variant Plans. The default visual gates are Symbology, Style, then Minimalist-to-Maximalist intensity. At each gate, show concise options first and keep the full image prompt internal unless the artist asks for it. Symbology uses six symbolic options and asks whether the work should become a single image, emotional arc, or multi-image presentation. Style uses six suggested styles, and intensity uses three Minimal/Faithful-Balanced/Amplified-Maximal options. Series Recommendation can propose single image, triptych, or image series without executing a series until the artist approves it.

The next planned medium slice is text-to-sound for Suno, documented in `docs/text-to-sound/`. It reuses the shared Artist OS workflow, but replaces visual gates with Sonic Concept, Genre / Production, Tempo / Groove, Vocal / Lyric, and Arrangement / Form gates. The Vocal / Lyric Gate is required: Artist OS must ask whether the work should have lyrics or intelligible words, and if adapted or new lyrics are requested, the lyrics must be drafted and reviewed before final prompt locking. The first sound prompt output targets Suno Custom Mode fields: title, lyrics or instrumental choice, Style of Music, Exclude, and optional advanced notes.

## Open Questions

- Which agent host should be packaged for first beyond the current Codex dev symlink install?
- Which media models and APIs are in scope for the first version?
- When should we add a full Series Plan or Calibration Choice schema?
- Should the next workflow run use a new artist-provided text Reference or the included example fixture?

## Development Notes

- Keep early changes small and reversible.
- Document decisions before encoding broad conventions.
- Put disposable experiments in `.tmp/`.
- Do not commit generated media, private artist references, secrets, API keys, or paid-service credentials.
