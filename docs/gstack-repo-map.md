# GStack Repository Map

Last updated: 2026-05-30

## Why This Map Exists

We are using GStack as a reference for how to structure Artist Generation. The useful lesson is not "copy every directory." The useful lesson is how GStack turns a repo into an agent operating system:

- Skills are first-class workflows.
- Each skill has a specialist role.
- Setup and host adapters make the same workflows available to different agents.
- Persistent notes, learnings, and generated docs let agents resume work without relying on memory alone.
- Tooling is packaged as repeatable scripts rather than one-off instructions.

## Two Things Are Happening Here

Artist Generation has two tracks that must stay separate.

### Track 1: Build The Operating System

This is the work happening in this repository now. Its documents guide us and future agents while we design and build the artist operating system.

Current build-process documents:

- `README.md`: explains the repository's current purpose and direction while the product is being built.
- `PROGRESS.md`: records what changed, what we decided, and what to do next.
- `docs/IMPLEMENTATION_PLAN.md`: maps the staged path from idea to working system.
- `docs/gstack-repo-map.md`: explains what to borrow from GStack and when.

These are scaffolding documents. They help us build the product. They are not the final user-facing manual for artists.

### Track 2: Produce The Artist OS

This is the product outcome. It will be the actual system an artist or agent uses to ingest references, extract meaning, transform emotional structure across formats, generate assets, critique results, and archive provenance.

Future product artifacts:

- `AGENTS.md`: operating rules for agents inside the finished repo.
- `ARCHITECTURE.md`: product architecture and data flow.
- `THEORY.md`: the artistic theory behind formal analysis, emotion, story beats, and personal meaning.
- `docs/metadata-schema.md`: source, brief, output, and provenance schemas.
- `skills/`: the actual artist OS workflows.
- `bin/`, `lib/`, `schemas/`, and `test/`: implementation and verification.

The build-process docs should always point toward these product artifacts. Once a product artifact exists, it becomes the source of truth for that part of the system. The scaffolding doc should then link to it instead of duplicating it.

### Working Rule

When adding documentation, first decide which track it belongs to:

- If it helps us decide how to build Artist Generation, it belongs in the build-process layer.
- If it is part of how Artist Generation works for artists or agents, it belongs in the product layer.

Do not let process notes masquerade as product architecture, and do not bury product rules inside progress notes.

## GStack At A Glance

Observed top-level shape:

```text
gstack/
├── README.md
├── AGENTS.md
├── ARCHITECTURE.md
├── DESIGN.md
├── ETHOS.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── VERSION
├── SKILL.md
├── SKILL.md.tmpl
├── setup
├── package.json
├── hosts/
├── scripts/
├── bin/
├── lib/
├── docs/
├── test/
├── model-overlays/
├── browse/
├── extension/
└── many skill folders/
```

The repo has three broad layers:

1. Product docs and operating doctrine.
2. Skill workflows and generated host-specific variants.
3. Runtime tooling, setup, tests, and persistent state helpers.

## Layer 1: Docs And Operating Doctrine

GStack uses top-level docs to explain both product behavior and repository behavior:

- `README.md`: public product pitch, install flow, user-facing skill catalog.
- `AGENTS.md`: agent-facing repo instructions and skill list.
- `ARCHITECTURE.md`: why the system is built the way it is.
- `DESIGN.md`: design/product standards.
- `ETHOS.md`: guiding philosophy.
- `CONTRIBUTING.md`: contribution expectations.
- `CHANGELOG.md` and `VERSION`: release tracking.

Artist Generation should split this layer into build-process docs and product docs.

Build-process docs already present or planned:

- `README.md`: what we are building and why.
- `PROGRESS.md`: current status and handoff.
- `docs/IMPLEMENTATION_PLAN.md`: staged build plan.
- `docs/gstack-repo-map.md`: GStack lessons and repository framing.

Product docs to create:

- `AGENTS.md`: exact rules for agents working in this repo.
- `ARCHITECTURE.md`: data flow from source ingestion to generation/archive.
- `THEORY.md`: artistic model: formal elements, Emotional Structure, Core Tension Pairs, Beats, Tension Points, and Artist Meaning.
- `docs/metadata-schema.md`: source/brief/output manifest.

Recommendation: keep the early scaffolding docs short and explicit. Move stable product decisions into product docs as soon as they harden. This repo's hard part is conceptual integrity, not code volume.

## Layer 2: Skills As Specialist Workflows

GStack skill folders follow a repeatable pattern:

```text
skill-name/
├── SKILL.md
└── SKILL.md.tmpl
```

`SKILL.md.tmpl` is the source. `SKILL.md` is generated from the template. The template contains:

- frontmatter for name, description, triggers, allowed tools, and metadata.
- a role declaration: "You are a..."
- hard gates that say what the skill must not do.
- phases or steps.
- specific tool calls or shell commands.
- required outputs.
- STOP points where user confirmation is required.

Representative GStack roles:

- `office-hours`: product interrogation before planning.
- `plan-ceo-review`: strategic scope challenge.
- `plan-eng-review`: architecture, edge cases, tests, performance.
- `plan-design-review`: design quality.
- `review`: code review.
- `qa`: browser-based QA.
- `ship`: release.
- `context-save` and `context-restore`: session continuity.
- `learn`: cross-session learning management.

Artist Generation equivalent roles:

- `ingest-reference`: creates a source record without generating anything.
- `meaning-interview`: grills the user on personal meaning, sacred details, and desired transformation.
- `formal-analysis`: identifies observable components by medium.
- `emotional-structure`: maps evidence to Core Tension Pairs and Emotional Qualities with confidence.
- `beat-map`: identifies changes, value shifts, and emotional payloads.
- `transformation-plan`: plans how one medium becomes another.
- `generate-image`: creates or prepares image generation.
- `generate-audio`: creates or prepares audio generation.
- `generate-video`: creates or prepares video generation.
- `critique-asset`: compares output against the Creative Brief.
- `archive-asset`: records provenance, prompts, settings, rights notes, and review state.

Recommendation: start with plain `SKILL.md` files, not generated templates. Introduce `.tmpl` generation after two or three skills reveal duplicated structure.

## Layer 3: Setup And Onboarding

GStack has a serious `setup` script. It does several jobs:

- checks for required runtime dependencies.
- builds runtime binaries when stale.
- generates host-specific skill docs.
- verifies Playwright Chromium is installed.
- creates global state directories.
- links skills into the target agent host.
- supports multiple hosts, including Claude Code, Codex, Kiro, Factory, OpenCode, and others.
- handles naming preferences and migration cleanup.

GStack also has `bin/gstack-team-init`, which adds project-level onboarding:

- optional mode: recommends GStack in project docs.
- required mode: adds enforcement hooks so agents cannot proceed without GStack.
- avoids vendoring the full GStack repo into each project.

Artist Generation equivalent:

- First version: no complex setup. Use repo-local skills and docs.
- Current dev version: `bin/install-codex-dev-skills` links repo-local skills into Codex with namespaced symlinks.
- Next packaging version: decide whether to keep the dev symlink scripts, add a user-facing `setup`, or both.
- Later: add `hosts/` and generated host variants.
- Much later: add team-mode onboarding if other users install it.

Recommendation: do not start with a full setup script. Start with one host and one runnable workflow. Copy GStack's separation of concerns, not its maturity level.

## Layer 4: Host Adapters

GStack has `hosts/*.ts` and a typed `HostConfig` interface. Each host config defines:

- host name and display name.
- CLI command and aliases.
- global and local skill paths.
- which frontmatter fields the host supports.
- whether sidecar metadata is generated.
- path rewrites from Claude-specific paths to host-specific paths.
- suppressed resolvers for capabilities the host cannot support.
- runtime assets to symlink.
- linking strategy.

The Codex host is a useful reference because it:

- keeps only `name` and `description` frontmatter.
- generates `openai.yaml` metadata.
- rewrites Claude skill paths to `.agents/skills/gstack`.
- suppresses skills that would ask Codex to invoke itself.
- symlinks a smaller runtime surface.

Artist Generation equivalent:

- Codex should be the first supported host because this repo is being created in Codex.
- Keep skill frontmatter minimal.
- Avoid host abstraction until we have at least one working skill.
- When host support expands, define host-specific installation paths and capability gaps explicitly.

## Layer 5: Skill Generation Pipeline

GStack uses `scripts/gen-skill-docs.ts` to generate `SKILL.md` files from templates.

Key behaviors:

- discovers root-level and one-level-deep `SKILL.md.tmpl` files.
- transforms frontmatter per host.
- rewrites paths per host.
- applies resolver placeholders such as preambles and common blocks.
- generates sidecar metadata for hosts that need it.
- supports dry-run checks for CI.

Artist Generation equivalent:

- Start without generation.
- Once skill bodies share repeated sections, introduce templates for:
  - preamble.
  - source record format.
  - meaning interview rules.
  - provenance requirements.
  - rights/safety reminders.
  - output manifest format.

Candidate future command:

```bash
bun run gen:skill-docs --host codex
```

Recommendation: template only the parts that are truly repeated. Artist workflows will need more nuance than mechanical generation at first.

## Layer 6: Runtime Helpers

GStack's `bin/` contains many small executables:

- config management.
- path resolution.
- slug generation.
- learnings log/search.
- review log/read.
- timeline log/read.
- update check.
- host/platform detection.
- analytics.
- sync and memory helpers.

The pattern is important: skills do not rely only on prose. They call small deterministic helpers for repeatable operations.

Artist Generation equivalent helpers, eventually:

- `artistgen-paths`: resolves local state, inputs, outputs, and manifests.
- `artistgen-new-source`: creates a source record.
- `artistgen-manifest-validate`: validates JSON manifests.
- `artistgen-archive-output`: records generated output metadata.
- `artistgen-taste-log`: records accepted/rejected preferences.
- `artistgen-brief-render`: renders a human-readable creative brief.

Recommendation: create helpers only when a manual step repeats twice.

## Layer 7: Persistent State And Memory

GStack separates repo files from user-local state:

- repo files hold source code, docs, and skills.
- `~/.gstack/projects/<slug>/...` holds project-specific checkpoints, design docs, and learnings.
- skills like `context-save`, `context-restore`, and `learn` manage this state.

This avoids committing noisy or private session data while preserving continuity.

Artist Generation equivalent:

- committed examples belong in `examples/`.
- real user inputs and generated assets should probably live outside git or under ignored directories.
- manifests can be committed only when they are examples, not private artist work.
- a local taste memory should be ignored by git.

Candidate local state:

```text
~/.artistgen/projects/<slug>/
├── sources/
├── briefs/
├── outputs/
├── taste-memory.jsonl
└── sessions/
```

Recommendation: use `PROGRESS.md` while the repo is private and young. Add local state when actual user assets enter the workflow.

## Layer 8: Tests And Quality Gates

GStack tests:

- skill generation.
- host transforms.
- path helpers.
- memory helpers.
- browser behavior.
- upgrade migrations.
- e2e skill behavior.

Artist Generation equivalent:

- schema validation tests.
- text ingestion fixture tests.
- Creative Brief Record shape tests.
- beat-map fixture tests.
- host skill generation tests after templates exist.
- dry-run tests that do not call paid APIs.

Recommendation: the first tests should validate manifests and text workflow output shape. Do not test generation providers until adapters exist.

## Layer 9: Browser And Extension Runtime

GStack's `browse/` and `extension/` are a large runtime system:

- long-lived browser daemon.
- persistent tabs and cookies.
- fast browser control.
- extension UI and sidebar.
- security model for local and tunnel access.

Artist Generation may not need an equivalent browser runtime at first. However, the conceptual pattern is useful:

- when a workflow needs a reliable tool, wrap it in a daemon or helper instead of hoping the agent uses it consistently.
- stateful tools need explicit lifecycle and security boundaries.
- user assets and credentials must not leak into logs.

Possible future equivalent:

- local asset preview server.
- generation job queue.
- media inspection helpers.
- waveform/frame extraction.
- thumbnail/contact sheet generator.

Recommendation: defer this. For the first text-to-image workflow, the runtime can be files plus manifests.

## What To Copy Now

Copy these concepts immediately:

- two-tier docs: build-process docs and product docs.
- top-level docs as source of truth for their own track.
- skill roles with hard gates.
- clear phase outputs.
- user confirmation before irreversible or paid generation.
- manifest-first provenance.
- progress notes.
- start with one host.

## What To Copy Later

Copy these when the repo earns them:

- `setup` script.
- `hosts/` adapter system.
- generated `SKILL.md.tmpl` pipeline.
- local state root.
- learnings/taste memory helpers.
- CI checks for generated docs and schemas.

## What Not To Copy Yet

Do not copy these early:

- compiled binaries.
- browser daemon.
- extension UI.
- telemetry.
- multi-host installation.
- migration framework.
- elaborate analytics.

Those are useful only after the workflow proves itself.

## Suggested Artist Generation Evolution

### Stage 1: Separate The Docs

Create:

- `AGENTS.md`
- `ARCHITECTURE.md`
- `THEORY.md`
- `docs/metadata-schema.md`

Also clarify the existing scaffolding docs:

- `README.md` remains the repository-build entry point until the product is ready for external users.
- `PROGRESS.md` remains the current handoff log.
- `docs/IMPLEMENTATION_PLAN.md` remains the staged build plan.
- `docs/gstack-repo-map.md` remains the GStack reference.

Goal: make it clear which docs guide the building process and which docs define the product.

### Stage 2: Manual Skills

Create:

- `skills/ingest-reference/SKILL.md`
- `skills/meaning-interview/SKILL.md`
- `skills/transformation-plan/SKILL.md`

Goal: get one text-to-image planning loop working with manual skills. Codex dev symlink install is available through `bin/install-codex-dev-skills`, but full setup/host packaging remains later.

### Stage 3: Manifest And Validation

Create:

- `schemas/source-record.schema.json`
- `schemas/creative-brief.schema.json`
- `schemas/prompt-plan.schema.json`
- tests or a validation helper.

Goal: make Source Records, Creative Brief Records, and Provider-Neutral Prompt Plans consistent enough to trust.

### Stage 4: First Generation Adapter

Create:

- `.env.example`
- one provider-neutral adapter or host-native generation workflow.
- dry-run mode.

Goal: generate images while recording prompt, model, settings, and output metadata.

### Stage 5: Codex Packaging

Current dev tooling:

- `bin/install-codex-dev-skills`
- `bin/uninstall-codex-dev-skills`

Later create:

- minimal `setup`.
- Codex installation path.
- smoke test.

Goal: move from local symlink development install to clean installation for another Codex user.

### Stage 6: Template And Host System

Create:

- `SKILL.md.tmpl` files.
- `scripts/gen-skill-docs`.
- `hosts/codex`.
- later hosts as needed.

Goal: support multiple agent hosts without hand-maintaining every variant.

## Design Principle For This Repo

GStack is optimized for engineering work. Artist Generation should be optimized for preserving artistic intent across transformations.

That means our strongest invariant should not be "the agent generated an asset." It should be:

> The Generated Work can be traced back to Artist Meaning, Reference evidence, the Creative Brief, and the chosen Meaning-Preserving Transformation.

Everything else should serve that invariant.
