# Artist OS

[![CI](https://github.com/ashoka-bm/artist-os/actions/workflows/ci.yml/badge.svg)](https://github.com/ashoka-bm/artist-os/actions/workflows/ci.yml)

Artist OS is a Codex skill bundle for transforming artist-provided text into structured creative prompt plans while preserving the artist's meaning, intended feeling, emotional arc, and provenance.

The current dry-run workflows are:

- Text reference to Provider-Neutral Image Prompt Plan.
- Text reference to storyboard-ready Video Medium Plan (Video Journey v0).
- Text reference to Sound Prompt Plan with a Suno Custom Mode field export
  (not generated audio).
- Text reference to Text Generation Plan and drafted written output (Text Journey).
- Album v1 Release Package Plan for ordered tracks, album/track cover planning, release copy, and calibration.

Dry-run means the skills produce briefs, prompt plans, lyrics when requested,
written drafts, critique records, and metadata. Artist OS 1.0 ships no provider
adapter: a Generation Approval records permission but does not make a provider
call executable from this repository.

The artist-approved boundary and completion checklist for the first finished
version lives in `docs/release-1.0.md`. Thin Cross-Medium Plan orchestration is
part of that boundary; provider adapters, finished video, automatic conductor
self-improvement, and broader package routers are not.

> **Release status:** Artist OS 1.0 is the first certified Codex distribution.
> It is local-first and dry-run only: no provider adapter, publishing
> integration, or finished-video renderer ships in this release.

## Install In Codex

Download and extract `artist-os-1.0.0-codex.tar.gz`, choose a Wondermint Root
outside a Git repository, then run from the extracted bundle:

```bash
WONDERMINT_ROOT=/absolute/path/to/your/root \
  bin/install-codex-skills --mode copy
```

Copy mode is recommended and remains usable after the downloaded bundle is
moved or removed. Symlink mode is also supported with `--mode symlink`.

Restart Codex or open a new task after installing so skill discovery refreshes.
The [five-minute quickstart](docs/quickstart.md) covers the first project,
expected gates and output locations, resume, updates, doctor troubleshooting,
Video v0, and uninstall.

The certified environment is documented in
[supported environments](docs/supported-environments.md). Privacy and network
behavior is documented in
[privacy and network boundary](docs/privacy-and-network.md).

Start all Artist OS work with `artist-os`. The frozen 1.0 target turns an
artist-provided text Reference into traceable dry-run image plans,
storyboard-ready video plans, audio plans, written drafts, Album plans, or a
constrained multi-medium package. It routes unclear work through the required
gates, then loads internal mode files for isolated planning, review, and
editorial-pass work.

Automated CI exercises Ubuntu with Python 3.12–3.14. The complete packaged
installation matrix is certified on macOS as listed in the support matrix.

## Development Install In Codex

Contributors can install directly from a checkout:

```bash
WONDERMINT_ROOT=/absolute/path/to/your/root bin/install-codex-dev-skills
```

## Workflows

### Text To Image

```text
Text Reference
  -> Source Record
  -> Meaning Interview
  -> Transformation Brief
  -> Beat Plan
  -> Story Critic Review, for multi-beat or series plans
  -> Image Medium Plan
  -> Creative Brief Document
  -> Symbology Direction
  -> Style Direction
  -> Art Critic Review
  -> Brief Approval
  -> Creative Brief Record
  -> Provider-Neutral Image Prompt Plan
  -> optional Prompt Branch Set for curator batches
  -> Prompt Plan Critique
  -> optional Generation Approval Gate
  -> Output Record, when an artifact exists
  -> Output Critic Review
  -> Output Acceptance Gate
```

The shared visual gates are Symbology, then Style. The final prompt plan includes Faithful, Amplified, and Minimal variants guided by Prompt Variant Strategy, so variants differ meaningfully without adding another visual gate. When the artist wants broad exploration, Artist OS can also create a Prompt Branch Set: a batch of meaning-equivalent prompts that vary style, setting, symbol, composition, and other approved axes for human curation.

### Text To Suno Music

```text
Text Reference
  -> Source Record
  -> Meaning Interview
  -> Transformation Brief
  -> Beat Plan
  -> Story Critic Review, for multi-section or lyric-bearing plans
  -> Sound Medium Plan
  -> Sound Creative Brief Document
  -> Sonic Concept
  -> Genre / Production
  -> Tempo / Groove
  -> Vocal / Lyric Policy
  -> Arrangement / Form
  -> Music / Sound Critic Review
  -> Brief Approval
  -> Sound Creative Brief Record
  -> Sound Prompt Plan
  -> Suno Custom Mode field export
  -> Prompt Plan Critique
  -> optional Generation Approval Gate
  -> Output Record, when an artifact exists
  -> Output Critic Review
  -> Output Acceptance Gate
```

The Vocal / Lyric gate is required. If the artist wants lyrics or intelligible
words, Artist OS drafts lyrics and includes them in review before final prompt
locking. The sound plan stays platform-neutral until the final field-export
step. The first sound exporter targets Suno Custom Mode fields: title, lyrics
or instrumental choice, Style of Music, Exclude, and optional advanced notes.
It does not generate audio.

### Text To Text (Text Journey)

```text
Text Reference
  -> Source Record
  -> Meaning Interview
  -> Transformation Brief
  -> Beat Plan
  -> Story Critic Review, for multi-beat or sequence plans
  -> Text Medium Plan
  -> Text Creative Brief Document
  -> Writing Method / Text Form / Voice / Structure / Fidelity / Use gates
  -> Writing Critic Review
  -> Brief Approval
  -> Text Creative Brief Record
  -> Text Generation Plan
  -> Prompt Plan Critique
  -> Draft Generation Approval Gate
  -> drafted Output Record
  -> optional Clear Writing Pass, then optional Human Voice Pass
  -> Output Critic Review
  -> Output Acceptance Gate
```

The Text Journey drafts the written Output Artifact in a fresh-context sub-agent, runs a conformance review before any editorial pass, and runs Clear Writing Pass before Human Voice Pass when the Text Generation Plan requires or recommends them. Each concrete rewrite gets a new Output Record. Drafting requires Draft Generation Approval even though no paid provider is called.

All critic and reviewer stages run as bounded sub-agent reviews. The creating
agent does not self-review its own Story, Medium, Prompt, or Output review
stage. Provider-backed generation is outside 1.0; if a later or external
adapter is used, it still requires explicit approval. The output lifecycle
applies after a generated, imported, drafted, or edited artifact exists.

Artist OS has standing user authorization to spawn bounded internal sub-agents automatically for mandatory reviews, validation, drafting passes, audits, and approved orchestration patterns. This does not authorize provider-backed generation, paid actions, uploads, destructive actions, artist-facing gate approvals, waivers, or output acceptance.

## Repository Contents

```text
AGENTS.md                    Agent operating rules
CONTEXT.md                   Product language and domain context
THEORY.md                    Shared Artist OS theory
ARCHITECTURE.md              Workflow and data-flow architecture
docs/metadata-schema.md      Metadata field reference
docs/storage.md              Local Workspace Library rules
docs/release-1.0.md          Authoritative 1.0 scope and completion checklist
docs/progress.md             Current roadmap, transition state, and completed milestones
docs/pipeline-contract.md    Typed step input/output contract
docs/provider-import-adapter-contracts.md Provider/import execution boundary
docs/gates-and-reviews.md    Canonical gates, critic roles, and reviewer contract
docs/story/                  Shared story and beat architecture
docs/structure-library/      Story Structures and Cultural Format Structures
docs/output-journeys/        Medium routes for image, video, sound, text, and mixed media
docs/writing/                Writing methods and reviewer integration
docs/text-to-sound/          Suno-specific theory and architecture
docs/adr/                    Architecture Decision Records
schemas/                     JSON schemas and SQLite schema
examples/                    Valid example records
skills/                      Codex skill source files
evals/                       Routing and conductor-behavior evals
tests/                       Schema, transition, and contract tests
bin/                         Local install and workspace helpers
packaging/                   Distribution manifest, host registry, and build notes
release-evidence/            Tracked release rehearsal evidence
```

## Architecture Direction

Artist OS now has a shared story layer for the implemented image, video v0, Suno, and text dry-run slices: every output is one or more approved beats translated into a medium. A single image can be one compressed key emotional movement; an image series stages several movements; a video, song, text piece, or mixed-media package can unfold more beats over time.

The governing rule is emotional primacy. Artist OS should grab attention, trigger a strong emotion, and forge a simple mental link. Plans must express a feeling rather than only communicate a fact, so Beat Plans, Medium Plans, and briefs now track Intended Feeling, Key Emotional Movements, Expectation Turns, and Minimum Tension Criteria.

The current dry-run slices are text-to-image, video storyboard planning,
text-to-Suno, and the text-to-text Text Journey. Shared cross-medium
architecture lives in:

```text
docs/story/
docs/output-journeys/
docs/writing/
```

The shared cross-medium schemas exist for Transformation Briefs, Beat
Plans, Image, Video, Sound, and Text Medium Plans, Cross-Medium Plans,
Long-Work Stewardship Records, Review Records, Gate Decisions, Prompt Branch
Sets, Text Generation Plans, Output Records, and Asset Packages. The thin
general Cross-Medium Plan lifecycle ships in 1.0; EP, Single Bundle,
Visual Album, campaign, publishing, and distribution routers remain later
work. The image, video v0, Suno, and text dry-run slices translate the shared
Beat Plan through medium-specific Medium Plans before producing final brief
records, prompt plans, generation plans, or storyboard-ready handoffs that
preserve emotional movement and tension criteria. Creative Brief Records carry
`beat_plan_id` rather than duplicate embedded Beat summaries.

## Local State And Privacy

The accepted storage model for installed user runs stores user-facing files and internal project state under a user-chosen Wondermint Root:

```text
<wondermint_root>/
├── Wondermint/
│   └── Artist Library/
└── .wondermint/
    └── artist-os/
```

`Wondermint/Artist Library/` contains visible project outputs, Review Drafts, readable summaries, and artist-useful Personal Library notes. The hidden sibling `.wondermint/artist-os/` contains internal Workspace Library state such as project manifests, event logs, prompt plans, critiques, sidecars, feedback evidence, learning records, and performance signals. Basic installed-root setup, Project Pointer creation, manifest fields, SQLite indexing, visible-missing sync, and feedback/learning/performance record scaffolding are available. See `docs/storage.md` and `docs/progress.md`.

Use `bin/artist-os-import-output` to record an artist-owned or human-edited
local artifact as an Output Record without calling a provider. The command
validates the governing project and complete upstream lineage, confines durable
writes to that project, uses a recovery journal for the record/event/manifest
transaction, updates resume state, and refreshes SQLite. Image, sound, and text
planning records are schema-validated; video and mixed-media imports also
schema-validate their governing Video or Cross-Medium Plan and require exact
linked brief and planning records.

For repo development and tests, the internal Workspace Library can still live at:

```text
workspace-library/artist-os/
```

The repo-local development library is ignored by this repository's git rules. User-chosen Wondermint Roots should live outside git repositories, or the containing repository should explicitly ignore both `Wondermint/` and `.wondermint/`.

Do not commit generated media, private artist references, secrets, API keys, or
paid-service credentials. See `docs/privacy-and-network.md` for the complete
local-storage and Codex-processing boundary.

## Development

The repo remains the source of truth. Update files under `skills/`, then run:

```bash
bin/install-codex-dev-skills
```

The installer updates existing local Codex skills and creates missing links under `~/.codex/skills`.

Validate examples and fixtures with:

```bash
bin/validate-examples
```

Run tests with:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

When changing skill `description:` frontmatter or the `artist-os` conductor, also run the manual evals in `evals/`. They call `claude -p`, require auth, and cost tokens, so they are intentionally not part of the normal test suite.

Uninstall the local Artist OS skill entries with:

```bash
bin/uninstall-codex-dev-skills
```
