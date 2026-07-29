# Artist OS 1.0 quickstart

## Install in about five minutes

1. Download `artist-os-1.0.0-codex.tar.gz` and its adjacent
   `.tar.gz.sha256` file.
2. In the download directory, run
   `shasum -a 256 -c artist-os-1.0.0-codex.tar.gz.sha256`.
3. Extract the archive and choose a Wondermint Root outside a Git repository.
4. From the extracted `artist-os-1.0.0` directory, run:

```bash
WONDERMINT_ROOT=/absolute/path/to/wondermint-root \
  bin/install-codex-skills --mode copy
```

Copy mode is recommended because the installation remains usable if the
downloaded bundle is moved or deleted. Symlink mode is available for a
deliberately linked installation:

```bash
WONDERMINT_ROOT=/absolute/path/to/wondermint-root \
  bin/install-codex-skills --mode symlink
```

Restart Codex or open a new task so skill discovery refreshes.

## Start a project

In Codex, say:

> Use artist-os. Turn this text Reference into an image plan: [paste text]

Artist OS first captures what the Reference means to you, then moves through
the required Story, Medium, brief, review, and approval gates. It never records
an approval, waiver, or Output Acceptance on your behalf.

Internal state is stored in:

```text
<wondermint_root>/.wondermint/artist-os/
```

Readable outputs and Review Drafts appear when they exist in:

```text
<wondermint_root>/Wondermint/Artist Library/
```

## Resume

Ask Codex to resume the named Artist OS Project. To inspect available projects
directly:

```bash
ARTIST_OS_ROOT="$HOME/.codex/skills/artist-os" \
  "$HOME/.codex/skills/artist-os/bin/artist-os-db" list \
  --wondermint-root /absolute/path/to/wondermint-root
```

## Video v0 example

Say:

> Use artist-os. Turn this text Reference into a storyboard-ready short video
> plan: [paste text]

Video v0 produces a Video Medium Plan with scenes, timed Storyboard Shots,
motion, transitions, and audio posture. It may prepare a Seedance Prompt
Package after storyboard approval. It does not render finished video or call a
provider.

## Update and troubleshoot

Extract the newer release and run its installer with the same Wondermint Root
and install mode. The installer replaces only a verified Artist OS
installation and preserves the Workspace Library.

Verify the installed target:

```bash
ARTIST_OS_ROOT="$HOME/.codex/skills/artist-os" \
  "$HOME/.codex/skills/artist-os/bin/artist-os-paths" doctor
```

If Codex does not see the updated skill, open a new task or restart the app.
For reproducible problems, follow `SUPPORT.md`.

## Uninstall

```bash
CODEX_SKILLS_DIR="$HOME/.codex/skills" \
  "$HOME/.codex/skills/artist-os/bin/uninstall-codex-skills"
```

Uninstall removes the installed bundle but preserves the Artist Library,
Workspace Library, and SQLite index.
