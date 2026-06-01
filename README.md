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
  -> Creative Brief Document
  -> Symbology Direction
  -> Style Direction
  -> Art Critic Review
  -> Brief Approval
  -> Creative Brief Record
  -> Provider-Neutral Image Prompt Plan
  -> Prompt Plan Critique
```

The visual gates are Symbology, Style, then Minimalist-to-Maximalist intensity when needed. The final prompt plan includes Faithful, Amplified, and Minimal variants.

### Text To Suno Music

```text
Text Reference
  -> Source Record
  -> Meaning Interview
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
```

The Vocal / Lyric gate is required. If the artist wants lyrics or intelligible words, Artist OS drafts lyrics and includes them in review before final prompt locking. The first sound output targets Suno Custom Mode fields: title, lyrics or instrumental choice, Style of Music, Exclude, and optional advanced notes.

## Repository Contents

```text
AGENTS.md                    Agent operating rules
CONTEXT.md                   Product language and domain context
THEORY.md                    Shared Artist OS theory
ARCHITECTURE.md              Workflow and data-flow architecture
docs/metadata-schema.md      Metadata field reference
docs/storage.md              Local Workspace Library rules
docs/text-to-sound/          Suno-specific theory and architecture
schemas/                     JSON schemas and SQLite schema
examples/                    Valid example records
skills/                      Codex skill source files
bin/                         Local install and workspace helpers
```

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

Uninstall the local Artist OS skill entries with:

```bash
bin/uninstall-codex-dev-skills
```
