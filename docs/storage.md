# Artist OS Storage

Artist OS stores real project work in a local, uncommitted Workspace Library. The repository keeps schemas, examples, and skills; private references, generated images, prompts, and project history stay outside git.

Default root:

```text
workspace-library/artist-os/
```

The query database lives at:

```text
workspace-library/artist-os/artist-os.sqlite
```

SQLite is the local search/index layer. The per-project files remain the durable source artifacts for briefs, prompt plans, sidecar metadata, images, and event history.

## Project Layout

Each project gets one folder:

```text
workspace-library/artist-os/projects/<project_id>/
├── project.json
├── events.jsonl
├── source/
│   ├── source-record.json
│   ├── reference.txt
│   └── media/
├── meaning/
│   └── meaning-interview.json
├── story/
│   ├── transformation-brief.json
│   └── beat-plan.json
├── stewardship/
│   └── long-work-stewardship-<id>.json
├── medium-plans/
│   ├── image-medium-plan.json
│   └── sound-medium-plan.json
├── gates/
│   ├── interpretation.json
│   ├── symbology.json
│   ├── style.json
│   └── detail.json
├── briefs/
│   ├── creative-brief.draft.md
│   └── creative-brief.record.json
├── prompt-plans/
│   └── prompt-plan.json
├── critiques/
├── exports/
└── assets/
    ├── reference/
    ├── boards/
    ├── generated/
    └── final/
```

## SQLite Index

The SQLite database validates against the schema in `schemas/artist-os-library.sql`. It indexes:

- projects,
- project paths,
- gate and creative decisions,
- record paths,
- assets and image sidecars,
- event history.

Agents should query this database first when a user asks about old projects, previous prompts, image paths, decisions, or where to resume.

Initialize or refresh it with:

```bash
bin/artist-os-db setup
bin/artist-os-db sync
```

Useful reads:

```bash
bin/artist-os-db list
bin/artist-os-db show <project_id>
```

`index.json` is optional as a human-readable export. It is not the primary index once SQLite exists.

If a project was previously indexed but its `project.json` is not found during sync, SQLite marks that project with `status = missing`. This preserves the old reference without pretending the project is still resumable.

## Manifest

Every project has `project.json`, validated by `schemas/project-manifest.schema.json`. It records:

- project identity and status,
- current stage,
- paths to source, meaning, gate, brief, prompt-plan, critique, and asset files,
- selected symbology, style, presentation mode, and detail mode,
- generated image paths and sidecar metadata paths.

## Event Log

Every meaningful step appends one JSON object to `events.jsonl`:

- stage entered,
- user answer,
- options shown,
- selection made,
- visualization requested or declined,
- record written,
- image generated or imported,
- critique result.

The event log preserves process history even when the current manifest is updated.

## Image Storage

Store images under `assets/`:

- `assets/reference/`: user-provided reference images or visual source material.
- `assets/boards/`: symbology, style, or detail comparison boards.
- `assets/generated/`: intermediate generated works.
- `assets/final/`: accepted final works.

Each image should have a sidecar metadata file with the same basename plus `.json`, for example:

```text
assets/boards/symbology-board-001.png
assets/boards/symbology-board-001.json
```

Sidecar metadata should include source project, stage, prompt or prompt-plan reference, provider/model when applicable, rights notes, created time, and critique status.

Sidecar metadata validates against `schemas/asset-metadata.schema.json`.

## Asset Destinations

Use these destinations for each asset type:

- Text Reference: `source/reference.txt`
- Source Record: `source/source-record.json`
- user-provided reference media: `source/media/` or `assets/reference/` with sidecar metadata
- Artist Meaning / Meaning Interview: `meaning/artist-meaning.json`
- Transformation Brief: `story/transformation-brief.json`
- Beat Plan: `story/beat-plan.json`
- Long-Work Stewardship Records: `stewardship/long-work-stewardship-*.json`
- Image Medium Plan: `medium-plans/image-medium-plan.json`
- Sound Medium Plan: `medium-plans/sound-medium-plan.json`
- Text Medium Plan: `medium-plans/text-medium-plan.json`
- gate decisions: `gates/*.json`
- generated or imported visual boards: `assets/boards/` with sidecar metadata
- draft Creative Brief: `briefs/creative-brief.draft.md`
- approved Creative Brief Record: `briefs/creative-brief.record.json`
- approved Text Creative Brief Record: `briefs/text-creative-brief.record.json`
- Provider-Neutral Prompt Plan: `prompt-plans/prompt-plan.json`
- Text Generation Plan: `prompt-plans/text-generation-plan.json`
- Prompt Branch Set: `prompt-plans/prompt-branch-set.json`
- Output Records: `outputs/*.json`
- Review Records and critique records: `critiques/`
- intermediate Generated Works: `assets/generated/` with sidecar metadata
- accepted final images: `assets/final/` with sidecar metadata
- shareable packages or exports: `exports/`

## Persistence Rule

Agents must persist before moving stages:

1. Create or update `project.json`.
2. Write the stage record under the matching folder.
3. Append an event to `events.jsonl`.
4. Store images in `assets/` with sidecar metadata.
5. Run or mirror the equivalent of `bin/artist-os-db sync` so `artist-os.sqlite` reflects the latest manifest, events, and assets.

If persistence fails, report that before proceeding.

## Package Setup

Installing the local Codex dev skills also initializes the Workspace Library:

```bash
bin/install-codex-dev-skills
```

The installer runs:

```bash
bin/artist-os-db setup
```

Use `ARTIST_OS_LIBRARY_ROOT=/path/to/library` to choose a different local library location.
