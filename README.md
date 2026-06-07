# Artist OS

Artist OS is a Codex skill bundle for transforming artist-provided text into structured creative prompt plans while preserving the artist's meaning, emotional arc, and provenance.

The current dry-run workflows are:

- Text reference to Provider-Neutral Image Prompt Plan.
- Text reference to Suno Sound Prompt Plan.

Dry-run means the skills produce briefs, prompt plans, lyrics when requested, critique records, and metadata. They do not call paid generation providers without explicit approval.

## Install In Codex

Clone the repo, then install the local skills:

```bash
bin/install-codex-dev-skills
```

This installs:

```text
artist-os
artist-os-ingest-reference
artist-os-meaning-interview
artist-os-text-to-image-plan
artist-os-text-to-suno-plan
artist-os-art-critic-review
artist-os-writing-method-review
artist-os-critique-asset
```

Restart Codex or open a new thread after installing so skill discovery refreshes.

Start normal end-to-end work with `artist-os`. It asks whether unclear text should become visual art or a Suno music prompt, then routes through the required gates.

## Workflows

### Text To Image

```text
Text Reference
  -> Source Record
  -> Meaning Interview
  -> Transformation Brief
  -> Beat Plan
  -> Story / Beat Review, for multi-beat or series plans
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

The visual gates are Symbology, Style, then Minimalist-to-Maximalist intensity when needed. The final prompt plan includes Faithful, Amplified, and Minimal variants. When the artist wants broad exploration, Artist OS can also create a Prompt Branch Set: a batch of meaning-equivalent prompts that vary style, setting, symbol, composition, and other approved axes for human curation.

### Text To Suno Music

```text
Text Reference
  -> Source Record
  -> Meaning Interview
  -> Transformation Brief
  -> Beat Plan
  -> Story / Beat Review, for multi-section or lyric-bearing plans
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
  -> Suno Sound Prompt Plan
  -> Prompt Plan Critique
  -> optional Generation Approval Gate
  -> Output Record, when an artifact exists
  -> Output Critic Review
  -> Output Acceptance Gate
```

The Vocal / Lyric gate is required. If the artist wants lyrics or intelligible words, Artist OS drafts lyrics and includes them in review before final prompt locking. The first sound output targets Suno Custom Mode fields: title, lyrics or instrumental choice, Style of Music, Exclude, and optional advanced notes.

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
docs/output-journeys/        Medium routes for image, video, sound, text, and mixed media
docs/writing/                Writing methods and reviewer integration
docs/text-to-sound/          Suno-specific theory and architecture
schemas/                     JSON schemas and SQLite schema
examples/                    Valid example records
skills/                      Codex skill source files
bin/                         Local install and workspace helpers
```

## Architecture Direction

Artist OS now has a shared story layer for the implemented image and Suno dry-run slices: every output is one or more approved beats translated into a medium. A single image can be one compressed beat; a video, song, text piece, or mixed-media package can unfold more beats over time.

The current dry-run slices remain text-to-image and text-to-Suno. The planned cross-medium architecture lives in:

```text
docs/story/
docs/output-journeys/
docs/writing/
```

The first shared cross-medium schemas now exist for Transformation Briefs, Beat Plans, Image and Sound Medium Plans, Review Records, Gate Decisions, Prompt Branch Sets, and Output Records. The existing image and Suno dry-run slices translate the shared Beat Plan through image-specific and sound-specific Medium Plans before producing their final brief records.

## Local State And Privacy

Real Artist OS project work is stored outside git in:

```text
workspace-library/artist-os/
```

That local library can contain artist references, generated media, project manifests, event logs, prompt plans, critiques, and the SQLite query index. It is ignored by git.

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

Uninstall the local Artist OS skill entries with:

```bash
bin/uninstall-codex-dev-skills
```
