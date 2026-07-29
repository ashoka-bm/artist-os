# Artist OS Storage

Artist OS separates user-facing work from internal project state.

For installed user runs, Artist OS uses a user-chosen Wondermint Root. The root contains sibling visible and hidden folders:

```text
<wondermint_root>/
├── Wondermint/
│   └── Artist Library/
└── .wondermint/
    └── artist-os/
```

The visible Artist Library contains project outputs, Review Drafts, readable summaries, and Personal Library notes. The hidden Workspace Library contains schema-backed records, manifests, event logs, sidecars, feedback evidence, learning records, performance signals, and SQLite indexes.

The sibling layout is deliberate: deleting the visible `Wondermint/` folder should not delete the internal state needed to resume projects or preserve provenance.

For repo development and tests, the Workspace Library may still live at:

```text
workspace-library/artist-os/
```

The query database lives in the Workspace Library:

```text
<workspace_library>/artist-os.sqlite
```

SQLite is the local search/index layer. The per-project files remain the durable source artifacts for briefs, prompt plans, sidecar metadata, images, and event history.

Use `WONDERMINT_ROOT=/path/to/root` as the preferred user-facing storage override. This derives:

```text
/path/to/root/Wondermint/Artist Library/
/path/to/root/.wondermint/artist-os/
```

Use `ARTIST_OS_LIBRARY_ROOT=/path/to/library` only as a low-level Workspace Library override for development, tests, or compatibility with existing tooling.

All `bin/artist-os-db` commands that read or write the Workspace Library accept `--wondermint-root` or `--library-root`. Prefer `--wondermint-root` for installed user runs so the command can derive both the hidden Workspace Library and visible Artist Library. Use `--library-root` only when intentionally addressing a Workspace Library directly.

If a Wondermint Root is inside a cloud-synced folder, warn the user that visible outputs may sync well but internal Workspace Library state, especially SQLite, may encounter sync conflicts.

## Wondermint Skill Alignment

Artist OS and the Wondermint Marketplace skill both use Wondermint-branded local
folders, but they serve different storage roles.

Artist OS uses the Wondermint Root for creative project storage: visible Artist
Library files live under `<wondermint_root>/Wondermint/Artist Library/`, and
internal Workspace Library state lives under `<wondermint_root>/.wondermint/artist-os/`.

The Wondermint Marketplace skill currently stores account setup, onboarding
state, and non-secret operating preferences under `~/Wondermint/`. It stores
marketplace purchased files under `~/Documents/Wondermint/downloads/`.

When these systems converge, prefer `~/Documents` as the shared user-facing
Wondermint Root so Artist OS visible work lands in
`~/Documents/Wondermint/Artist Library/` alongside marketplace downloads in
`~/Documents/Wondermint/downloads/`. Keep Wondermint Marketplace account state
and API-key configuration out of the Artist OS Workspace Library and Artist
Library unless a later ADR explicitly migrates them.

## Artist Library Layout

Artist Library project folders are created lazily, only when there are user-facing files to show. Do not mirror internal Workspace Library structure into the visible folder, and do not create empty medium or export folders.

One visible project folder looks like:

```text
<wondermint_root>/Wondermint/Artist Library/Projects/<project_slug>/
├── README.md
├── .artist-os-project.json
└── <medium folders created as needed>/
    ├── Drafts/
    └── Accepted/
```

Medium folders include only folders with actual Review Drafts, Accepted Works, or other user-facing outputs, for example `Writing/`, `Images/`, or `Audio/`.

Reference folders are created only when generated or imported reference images exist. Organize them by category, subject, and review status:

```text
<wondermint_root>/Wondermint/Artist Library/Projects/<project_slug>/
└── References/
    ├── Characters/<character-slug>/
    │   ├── Review Drafts/
    │   └── Accepted/
    ├── Locations/<location-slug>/
    │   ├── Review Drafts/
    │   └── Accepted/
    └── Objects/<object-slug>/
        ├── Review Drafts/
        └── Accepted/
```

`Review Drafts/` contains generated or imported reference images that the artist can inspect but has not accepted as canonical. `Accepted/` contains reference images the artist accepted for downstream use. The visible folders are for artist browsing; Output Records, sidecar metadata, event logs, and the Reference Inventory remain the provenance source of truth.

The visible project `README.md` is a lightweight orientation file. It may include project title, plain-language summary, current status, visible outputs, last meaningful update, and how to ask Artist OS to resume the project. It should not include full Artist Meaning, full prompts, gate decisions, private feedback logs, performance analytics, schema paths, or raw event history.

The hidden `.artist-os-project.json` Project Pointer links the visible folder to the internal Artist OS Project. The project id is authoritative; relative Workspace Library hints are convenience only.

Example:

```json
{
  "schema_version": 1,
  "project_id": "proj_door_left_lit",
  "created_by": "artist-os",
  "workspace_root_hint": "../../../.wondermint/artist-os"
}
```

If a visible Artist Library project folder or Project Pointer disappears but the Workspace Library project still exists, treat the project as visible-missing, not deleted. It remains resumable from internal state, and Artist OS may offer to restore the visible folder.

If a user edits a visible Review Draft or Accepted Work, persist that edit as a new human-edited Output Artifact revision with its own Output Record linked to the previous Output Record. Do not silently mutate the older Output Record, and do not overwrite user-edited visible files without asking.

## Personal Library Layout

The visible Artist Library may contain a Personal Library for artist-useful reusable guidance:

```text
<wondermint_root>/Wondermint/Artist Library/Personal Library/
├── Structures/
├── Styles/
├── Voices/
├── Formats/
└── Learnings/
```

Only artist-useful creative guidance belongs here. Technical, schema, process, and tooling learnings stay internal.

The internal Workspace Library stores the machine-readable personal-library records, evidence links, promotion state, resolver indexes, feedback logs, and performance signals:

```text
<workspace_library>/personal-library/
├── structures/
├── styles/
├── voices/
├── formats/
├── learnings/
├── feedback-log/
└── performance-signals/
```

Soft Learning and Hard Learning records should keep their applied Learning Rule compact, roughly 600 characters. Detailed feedback, analytics, output comparisons, and evidence history stay in separate records referenced by id or path. Visible learning notes may be longer, but should still remain concise and artist-readable.

## Workspace Library Project Layout

Each project gets one folder:

```text
<workspace_library>/projects/<project_id>/
├── project.json
├── events.jsonl
├── feedback-log.jsonl
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
├── references/
│   └── reference-inventory.json
├── critiques/
├── outputs/
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
- concrete Output Artifacts from Output Records,
- Reference Inventory items and reference image paths,
- assets and image sidecars,
- event history,
- visible Artist Library paths and Project Pointer state,
- feedback and learning review status,
- performance signal references.

Agents should query this database first when a user asks about old projects, previous prompts, image paths, decisions, or where to resume.

Initialize or refresh it with:

```bash
bin/artist-os-db setup --wondermint-root /path/to/root
bin/artist-os-db sync --wondermint-root /path/to/root
bin/artist-os-db sync --project <project_id> --wondermint-root /path/to/root
```

`sync` is fault-isolated: one corrupt `project.json` or event line degrades to
a skipped-and-reported project, never an aborted sync, and a missing or
unreadable `events.jsonl` preserves the previously indexed events. Scoped
`sync --project` indexes exactly one manifest and never runs the missing-sweep;
it is what the feedback/learning write commands ride on, so their index writes
succeed even when an unrelated project is corrupt.

Useful reads:

```bash
bin/artist-os-db list --wondermint-root /path/to/root
bin/artist-os-db show <project_id> --wondermint-root /path/to/root
bin/artist-os-db status [project_id] --wondermint-root /path/to/root
```

`status` prints one row per project — status, stage, learning-review state,
and staleness (whether the index row still matches the on-disk manifest). It
opens the database read-only and never writes; the learning-surfacing verbs
(`pending-learning-reviews`, `learnings-report`, `review-learnings`) instead
self-heal by re-indexing from files immediately before they read, so a
learning present in files but missing from the index is still surfaced, and
all three work on a fresh clone with no database.

`index.json` is optional as a human-readable export. It is not the primary index once SQLite exists.

If a project was previously indexed but its `project.json` is not found during sync, SQLite marks that project with `status = missing`. This preserves the old reference without pretending the project is still resumable.

If a project is indexed and the Workspace Library project exists but its visible Artist Library folder is not found, mark the visible state as missing rather than marking the project missing.

## Manifest

Every project has `project.json`, validated by `schemas/project-manifest.schema.json`. It records:

- project identity and status,
- visible Artist Library path and Project Pointer state,
- current stage,
- paths to source, meaning, gate, brief, prompt-plan, critique, and asset files,
- the Reference Inventory path when promoted reference subjects exist,
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
- critique result,
- output acceptance or revision,
- user-facing file written or updated,
- feedback received,
- learning review marked pending or completed,
- performance signal imported.

The event log preserves process history even when the current manifest is updated.

## Image Storage

Store images under `assets/`:

- `assets/reference/`: user-provided reference images or visual source material.
- `assets/boards/`: symbology, style, or detail comparison boards.
- `assets/generated/`: intermediate generated works.
- `assets/final/`: accepted final works.

Generated and imported promoted reference images should keep category and subject organization inside `assets/reference/` or `assets/generated/`, matching the visible Artist Library reference folders when practical:

```text
assets/reference/characters/<character-slug>/
assets/reference/locations/<location-slug>/
assets/reference/objects/<object-slug>/
assets/generated/references/characters/<character-slug>/
assets/generated/references/locations/<location-slug>/
assets/generated/references/objects/<object-slug>/
```

Use sidecar metadata and Output Records to connect internal asset paths to visible `References/...` paths.

Use the storage helper to publish a generated or imported reference image into the visible project folder after an Output Record exists:

```bash
bin/artist-os-db publish-visible-reference proj_door_left_lit refimg_old_tv_multi_angle --state accepted --wondermint-root /path/to/root
```

The command copies the Output Artifact into `References/<Category>/<subject-slug>/Review Drafts/` or `Accepted/`, updates `reference-inventory.json` output readiness, records the visible file in `project.json`, appends an event when `events.jsonl` exists, and refreshes SQLite.

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
- Project Feedback Log: `feedback-log.jsonl`
- Soft Learning / Hard Learning records: `personal-library/learnings/`
- Performance Signals: `personal-library/performance-signals/`
- intermediate Generated Works: `assets/generated/` with sidecar metadata
- accepted final images: `assets/final/` with sidecar metadata
- shareable packages or exports: `exports/`
- Asset Package manifest: `exports/asset-package.json` (the internal persisted manifest; the compiled, artist-facing bundle materializes into the visible Artist Library `exports/` area)

## Persistence Rule

Agents must persist before moving stages:

1. Create or update `project.json`.
2. Write the stage record under the matching folder.
3. Append an event to `events.jsonl`.
4. Write or update any user-facing Artist Library file that should be visible to the artist.
5. Store images in `assets/` with sidecar metadata.
6. Run or mirror the equivalent of `bin/artist-os-db sync` so `artist-os.sqlite` reflects the latest manifest, events, visible paths, feedback state, and assets.

If persistence fails, report that before proceeding.

## Feedback, Learning, and Performance

Artist OS should append raw project feedback to the project Feedback Log as it arrives. At project completion, mark unclassified feedback as pending learning review rather than forcing the artist through a long cleanup step.

In 1.0, Learning Review, promotion, and application are explicitly invoked and
human-gated. The conductor does not run them automatically at session start or
apply stored Soft or Hard Learning by default. Automatic session-start review
and learning application remain part of the post-1.0 design in ADR 0016.

Concrete schema, process, or tool-field mismatches can become Hard Learning immediately. Taste and creative preferences usually start as Learning Candidates or Soft Learning unless repeated feedback, strong analytics, or explicit artist confirmation promotes them.

Performance Signals and artist feedback are equal evidence classes for learning. Neither automatically overrides the other. When they conflict, Artist OS should preserve both and ask whether the current project should prioritize personal expression, performance optimization, or a hybrid.

Useful write commands:

```bash
bin/artist-os-db add-feedback <project_id> --feedback "..." --wondermint-root /path/to/root
bin/artist-os-db add-learning <project_id> <learning_id> --learning-type soft --learning-rule "..." --wondermint-root /path/to/root
bin/artist-os-db add-performance-signal <project_id> <signal_id> --metric-name save_rate --metric-value 0.32 --signal-direction positive --wondermint-root /path/to/root
bin/artist-os-db mark-learning-review-complete <project_id> --wondermint-root /path/to/root
bin/artist-os-db pending-learning-reviews --wondermint-root /path/to/root
bin/artist-os-db learnings-report [project_id] --wondermint-root /path/to/root
bin/artist-os-db review-learnings --wondermint-root /path/to/root
bin/artist-os-db add-conductor-rule <project_id> --rule "..." --from-learning <learning_id> --wondermint-root /path/to/root
```

Each feedback, learning, performance-signal, and review-completion write also
appends its event to the project's `events.jsonl` (creating the log when the
manifest declares one that does not exist yet) and runs a scoped sync, so the
event history and the index reflect the write immediately.

`review-learnings` renders the promotion queue in plain language for someone
unfamiliar with the system: each pending feedback item with the exact command
to promote it (soft preference, hard rule, staged conductor candidate) or
dismiss it, then staged conductor candidates with the `add-conductor-rule`
command to adopt each one locally.

`learnings-report` prints each linked learning's actual rule text, scope, and
evidence count by reading the referenced record, noting records that are
missing on disk.

`learnings-report` is a read-only close-out: per project it shows the
learning-review state, the linked learnings, and any performance signals, then
prints the next action (which projects still owe a learning review). Run it at
the end of a session to see what to capture before moving on.

Learning and Performance Signal ids must match their schemas and cannot overwrite an existing record unless the command is run with `--overwrite`.

## Local Conductor Rules

`<workspace_library>/conductor-rules.md` holds local, additive conductor rules
adopted from this installation's learnings (ADR 0016 tier 2). Each entry is
one dated line written by `add-conductor-rule`, which also marks the source
candidate learning superseded, appends a `conductor_rule_adopted` event, and
refreshes the index. The conductor reads this file at session start after the
canonical `## Rules` in `skills/artist-os/SKILL.md`. Local rules may tighten
behavior or record preferences; they must never disable canonical gates,
approvals, or the never-auto-decide class. Because the file lives in the
Workspace Library, upgrading Artist OS never touches it — promoting a local
rule to every installation is a deliberate maintainer edit of `SKILL.md`
followed by one conductor-eval re-bless.

## Package Setup

Installing the local Codex dev skills also initializes the Workspace Library:

```bash
bin/install-codex-dev-skills
```

The installer runs:

```bash
bin/artist-os-db setup
```

Use `WONDERMINT_ROOT=/path/to/root` to choose the user-facing Wondermint Root for installed use. Use `ARTIST_OS_LIBRARY_ROOT=/path/to/library` only when you need to point tooling directly at a Workspace Library.
