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
- Product docs define the artist operating system itself: `AGENTS.md`, `ARCHITECTURE.md`, `THEORY.md`, `CONTEXT.md`, `docs/metadata-schema.md`, `schemas/`, `examples/`, and `skills/`.

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
│   ├── text-creative-brief.example.json
│   └── text-prompt-plan.example.json
├── schemas/
│   ├── source-record.schema.json
│   ├── creative-brief.schema.json
│   └── prompt-plan.schema.json
├── bin/
│   ├── install-codex-dev-skills
│   └── uninstall-codex-dev-skills
├── skills/
│   ├── first-slice-flow/
│   ├── ingest-reference/
│   ├── meaning-interview/
│   ├── text-to-image-plan/
│   ├── art-critic-review/
│   └── critique-asset/
├── docs/
└── docs/superpowers/plans/
```

Do not add `setup`, `hosts/`, `lib/`, provider adapters, or generated media directories until the manual First Slice proves the workflow.

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
artist-os-art-critic-review
artist-os-critique-asset
```

The `name:` field inside each skill uses the same namespaced value, so invoke them with the `artist-os-*` names above.

For the normal end-to-end dry run, start with `artist-os`. The other skills are role-specific entry points for debugging or resuming a single phase.

The repo remains the source of truth. Editing files under `skills/` updates the installed Codex skills immediately through the symlinks. Codex may still require a new thread or app reload to refresh skill discovery.

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
  -> Style Direction
  -> Series Recommendation
  -> Art Critic Review
  -> Brief Approval
  -> Creative Brief Record
  -> Provider-Neutral Image Prompt Plan
```

This milestone does not call paid providers. It produces a Provider-Neutral Image Prompt Plan with Faithful, Amplified, and Minimal Prompt Variant Plans. Style Direction is subordinate to meaning and Visual Dynamics, and Series Recommendation can propose single image, triptych, or image series without executing a series until the artist approves it.

## Open Questions

- Which agent host should be packaged for first beyond the current Codex dev symlink install?
- Should generated assets be stored in this repo, outside the repo, or in a managed asset store?
- Which media models and APIs are in scope for the first version?
- When should we add a full Series Plan or Calibration Choice schema?
- Should the next workflow run use a new artist-provided text Reference or the included example fixture?

## Development Notes

- Keep early changes small and reversible.
- Document decisions before encoding broad conventions.
- Put disposable experiments in `.tmp/`.
- Do not commit generated media, secrets, API keys, or paid-service credentials.
