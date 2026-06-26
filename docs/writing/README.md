# Writing Layer

The Writing Layer adapts three high-authority writing skills into Artist OS. These files should be treated as source references for how writing material is gathered, shaped, and reviewed:

- `docs/writing/references/writing-fragments.SKILL.md`
- `docs/writing/references/writing-beats.SKILL.md`
- `docs/writing/references/writing-shape.SKILL.md`

Change those reference files as little as possible. If Artist OS needs different behavior, add an integration rule here or in a medium journey doc rather than rewriting the source method.

## Roles

### Writing Fragments

Use `writing-fragments` when the artist is still discovering raw material.

It creates the pile. It should not impose outline, phases, or final structure. Its job is to capture noticings, claims, vignettes, sharp sentences, half-thoughts, quotes, and related observations as raw material.

Artist OS adaptation:

- Use this before Transformation Brief creation when the artist has a topic, mood, image, memory, or partial idea but not enough Reference material.
- Store the fragment document as Reference material or supporting source material.
- Preserve the fragment rhythm: append as fragments emerge, re-read before writing, do not overwrite user edits.

Reviewer use:

- A Fragment Reviewer checks whether meaningful fragments were captured without premature structure.
- It should flag missing raw material, over-structuring, weak fragment separation, or loss of the artist's own language.

### Writing Beats

Use `writing-beats` when the work should become a journey rather than a thesis-first argument.

It creates one beat at a time. The user picks a starting beat, the agent writes only that beat, then offers candidate next beats. It never writes ahead.

Artist OS adaptation:

- Use this as the primary source for Beat Plan creation when the target output is narrative, experiential, sequential, video, song, text, or mixed-media.
- For non-text outputs, translate "write only that beat" into "define only that beat" until the artist chooses the next direction.
- Preserve the beat rhythm: one beat, stop, re-read current state, offer 2-3 next beats.

Reviewer use:

- A Beat Reviewer checks whether each beat does one thing, whether the journey has natural pivots, and whether later beats were written ahead without approval.
- It should flag glued-together beats, missing pivots, false endings, and beats added only because a medium needs more content.

### Writing Shape

Use `writing-shape` when raw material needs to become a coherent finished article or structured written piece.

It starts with candidate openings, forces a choice or hybrid, then grows the piece paragraph by paragraph. Each paragraph or block must earn its place and use a deliberate format.

Artist OS adaptation:

- Use this when the output medium is text, article, essay, long caption, script treatment, release note, artist statement, or any written artifact that needs a reader-facing argument or shape.
- Use it after a fragment pile exists or after a Beat Plan is approved, depending on whether the piece is thesis-led or journey-led.
- Preserve the shaping rhythm: candidate openings, user choice, paragraph-by-paragraph growth, format arguments, re-read before writing.

Reviewer use:

- A Shape Reviewer checks whether the opening defines what the piece must do, whether each paragraph earns its place, and whether format choices are deliberate.
- It should flag weak transitions, drift from the opening promise, prose that should be a list, lists that are not parallel, missing examples, and paragraphs doing two jobs.

## Creation Flow

The writing methods are not only review tools. They should shape creation from the start.

Use this default order when the artist is developing written source material:

```text
writing-fragments
  -> writing-beats, if the piece wants a journey
  -> writing-shape, if the piece wants a finished reader-facing article or structured text
```

Use this default order when the final output is image, video, sound, or mixed media:

```text
writing-fragments, optional when the Reference is underdeveloped
  -> writing-beats for Story / Beat Plan creation
  -> medium-specific journey
```

Use `writing-shape` for non-text media only when a written companion piece is part of the output package, such as an artist statement, treatment, voiceover script, release copy, or narrative outline.

## Review Flow

The canonical review execution rule, reviewer packet, output fields, blocking behavior, and responsibility boundaries live in `docs/gates-and-reviews.md`.

The short version: Fragment Reviewer, Beat Reviewer, and Shape Reviewer are mandatory bounded sub-agent reviews whenever their method-specific concerns are present. Standing Sub-Agent Authorization means Artist OS does not ask for separate approval before spawning those bounded internal reviewers.

## Authority Rule

If this integration doc conflicts with one of the referenced writing skill files, prefer the referenced skill file for writing-method behavior. Prefer Artist OS docs only for cross-medium routing, persistence, provider boundaries, and provenance.
