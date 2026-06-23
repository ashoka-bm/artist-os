# Artist OS

[![CI](https://github.com/ashoka-bm/artist-os/actions/workflows/ci.yml/badge.svg)](https://github.com/ashoka-bm/artist-os/actions/workflows/ci.yml)

Artist OS is a Codex skill bundle for transforming artist-provided text into structured creative prompt plans while preserving the artist's meaning, intended feeling, emotional arc, and provenance.

The current dry-run workflows are:

- Text reference to Provider-Neutral Image Prompt Plan.
- Text reference to storyboard-ready Video Medium Plan (Video Journey v0).
- Text reference to Sound Prompt Plan with Suno Custom Mode rendering.
- Text reference to Text Generation Plan and drafted written output (Text Journey).
- Album v1 Release Package Plan for ordered tracks, album/track cover planning, release copy, and calibration.

Dry-run means the skills produce briefs, prompt plans, lyrics when requested, written drafts, critique records, and metadata. They do not call paid generation providers without explicit approval.

## Install In Codex

Clone the repo, then install the local skills:

```bash
bin/install-codex-dev-skills
```

This installs one public skill:

```text
artist-os
```

Restart Codex or open a new thread after installing so skill discovery refreshes.

Start all Artist OS work with `artist-os`. It turns any reference into a complete creative release system for albums, essays, Substack pieces, LinkedIn posts, long-form writing, image collections, video storyboard plans, audio works, and coordinated release packages. It routes unclear work into image, video, audio, or text through the required gates, then loads internal mode files for isolated planning, review, and editorial-pass work.

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
  -> Suno Custom Mode rendering
  -> Prompt Plan Critique
  -> optional Generation Approval Gate
  -> Output Record, when an artifact exists
  -> Output Critic Review
  -> Output Acceptance Gate
```

The Vocal / Lyric gate is required. If the artist wants lyrics or intelligible words, Artist OS drafts lyrics and includes them in review before final prompt locking. The sound plan stays platform-neutral until the final rendering step. The first sound renderer targets Suno Custom Mode fields: title, lyrics or instrumental choice, Style of Music, Exclude, and optional advanced notes.

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

All critic and reviewer stages run as bounded sub-agent reviews. The creating agent does not self-review its own Story, Medium, Prompt, or Output review stage. Provider-backed generation still requires explicit approval; the output lifecycle applies after a generated, imported, drafted, or edited artifact exists.

## Repository Contents

```text
AGENTS.md                    Agent operating rules
CONTEXT.md                   Product language and domain context
THEORY.md                    Shared Artist OS theory
ARCHITECTURE.md              Workflow and data-flow architecture
docs/metadata-schema.md      Metadata field reference
docs/storage.md              Local Workspace Library rules
docs/progress.md             Current roadmap, transition state, and completed milestones
docs/pipeline-contract.md    Typed step input/output contract
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
```

## Architecture Direction

Artist OS now has a shared story layer for the implemented image, video v0, Suno, and text dry-run slices: every output is one or more approved beats translated into a medium. A single image can be one compressed key emotional movement; an image series stages several movements; a video, song, text piece, or mixed-media package can unfold more beats over time.

The governing rule is emotional primacy. Artist OS should grab attention, trigger a strong emotion, and forge a simple mental link. Plans must express a feeling rather than only communicate a fact, so Beat Plans, Medium Plans, and briefs now track Intended Feeling, Key Emotional Movements, Expectation Turns, and Minimum Tension Criteria.

The current dry-run slices are text-to-image, video storyboard planning, text-to-Suno, and the text-to-text Text Journey. The remaining planned cross-medium architecture lives in:

```text
docs/story/
docs/output-journeys/
docs/writing/
```

The shared cross-medium schemas now exist for Transformation Briefs, Beat Plans, Image, Video, Sound, and Text Medium Plans, Long-Work Stewardship Records, Review Records, Gate Decisions, Prompt Branch Sets, Text Generation Plans, and Output Records. The image, video v0, Suno, and text dry-run slices translate the shared Beat Plan through medium-specific Medium Plans before producing final brief records, prompt plans, generation plans, or storyboard-ready handoffs that preserve emotional movement and tension criteria. Creative Brief Records carry `beat_plan_id` rather than duplicate embedded Beat summaries. The current plan is to run end-to-end dry-run rehearsals before finished-video support or provider adapters.

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

For repo development and tests, the internal Workspace Library can still live at:

```text
workspace-library/artist-os/
```

The repo-local development library is ignored by this repository's git rules. User-chosen Wondermint Roots should live outside git repositories, or the containing repository should explicitly ignore both `Wondermint/` and `.wondermint/`.

Do not commit generated media, private artist references, secrets, API keys, or paid-service credentials.

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
