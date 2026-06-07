# Text Journey

The Text Journey translates an approved Beat Plan into a written work. It can preserve the Reference closely, transform it into a new form, or use the Beat Plan as the structure for a different kind of writing.

## Best Fit

Use the Text Journey when the final work should be:

- a poem,
- a monologue,
- a prose scene,
- a short story,
- lyrics,
- a script,
- a letter,
- a manifesto,
- a narrative treatment,
- a rewritten or transformed version of the original text.

## Route

```text
Approved Beat Plan
  -> Writing Method Gate
  -> Text Form Gate
  -> Voice / Point Of View Gate
  -> Structure Gate
  -> Fidelity / Transformation Gate
  -> Writing Critic Review
  -> Text Generation Plan
  -> Prompt Critic Review
  -> Prompt Lock Gate
  -> Draft Generation Approval Gate
  -> Output Critic Review
  -> Output Acceptance Gate
```

## Gates

- Writing Method Gate: fragments, beats, shape, or a hybrid sequence?
- Text Form Gate: poem, monologue, prose scene, script, lyrics, essay, letter, treatment, or other form?
- Voice / Point Of View Gate: who speaks, from what distance, and with what authority?
- Structure Gate: fragment, scene, sequence, arc, chapters, sections, verses, or hybrid?
- Fidelity / Transformation Gate: preserve source language, adapt it, invert it, expand it, compress it, translate it, or create a new work from the approved Beat Plan?
- Publication / Use Gate: private draft, performance text, lyrics, social post, book fragment, prompt source, or other use?

## Reviews

- Story Critic Review happens before this journey as a bounded sub-agent review.
- Writing Critic Review checks form, voice, point of view, structure, pacing, line or paragraph pressure, continuity, and fidelity to Artist Meaning as a bounded sub-agent review.
- Fragment Reviewer sub-agent checks raw material capture against `docs/writing/references/writing-fragments.SKILL.md`.
- Beat Reviewer sub-agent checks journey movement against `docs/writing/references/writing-beats.SKILL.md`.
- Shape Reviewer sub-agent checks reader-facing structure against `docs/writing/references/writing-shape.SKILL.md`.
- Prompt Critic Review checks generation instructions, missing constraints, tone drift, rights-sensitive language reuse, and revision readiness as a bounded sub-agent review.
- Output Critic Review checks the written draft against Artist Meaning, Beat Plan, Text Plan, and any source-language constraints as a bounded sub-agent review.

## Writing Methods

Artist OS uses three high-authority writing references:

- `writing-fragments`: mine raw material without imposing structure.
- `writing-beats`: assemble a journey one beat at a time.
- `writing-shape`: turn a pile into a finished article or structured written piece.

Use the smallest method that matches the work:

- If the artist has scattered ideas, start with fragments.
- If the piece wants sequence, pivots, scenes, or experiential movement, use beats.
- If the piece wants a finished reader-facing argument, article, statement, or treatment, use shape.

Do not lock schemas for text plans until beats, form, section shape, narrative pressure, and writing-specific review criteria are refined.
