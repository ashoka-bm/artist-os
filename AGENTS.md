# Artist OS Agent Rules

These rules apply to agents building or running Artist OS inside this repository.

## Source Of Truth

Read `CONTEXT.md` before changing product language.

Use these product docs as durable references:

- `THEORY.md`
- `ARCHITECTURE.md`
- `docs/metadata-schema.md`
- `schemas/`
- `skills/`

Use `README.md`, `PROGRESS.md`, and `docs/superpowers/plans/` for build-process context.

## Product Invariant

Every Prompt Variant Plan and Generated Work must trace back to:

- Artist Meaning,
- evidence from the Reference,
- the Creative Brief,
- Emotional Structure,
- Visual Dynamics,
- the Beat or Tension Point,
- the Transformation Plan,
- the Provider-Neutral Prompt Plan,
- and the Output Record when generation exists.

Provider-Neutral Image Prompt Plan records should validate against `schemas/prompt-plan.schema.json`.

## Operating Rules

- Do not make provider-backed generation calls without explicit user approval.
- Do not commit user-provided media, Generated Works, secrets, or API keys.
- Treat Emotional Structure as a hypothesis until the artist confirms it.
- Artist Meaning overrides agent interpretation.
- Preserve provenance before optimizing for speed.
- Use Dry Runs before invoking media generation providers.
- Keep Derived Symbols marked and traceable.
- Keep Visual Dynamics separate from Emotional Structure.
- Keep Style Direction separate from Emotional Structure and Visual Dynamics.
- Treat Style Direction as the last priority after Artist Meaning, Emotional Structure, Beat Map, and Visual Dynamics.
- Use a short Style Interview when the artist has not named a style directly.
- Surface Style/Visual Conflicts and record proposed Style Adaptations instead of silently letting style override Visual Dynamics.
- Use the Wondermint Category Reference only as seed vocabulary unless preparing a Wondermint upload, where exact accepted subcategory names are required.
- Recommend a Series Plan when multiple significant Beats would be flattened into one image, but do not create multiple image prompt plans without artist approval.
- For an approved Series Plan, produce three calibration Prompt Variant Plans for one Series Calibration Image first and wait for artist approval before producing the remaining series.
- Use Prompt Variant Plans to test named unresolved creative axes when that is more useful than simple intensity variation.

## First Slice

The First Slice is Text Reference to Image Prompt Plan:

1. Ingest a Text Reference.
2. Run a Meaning Interview.
3. Produce a Source Record.
4. Produce a draft Creative Brief Document.
5. Define Style Direction.
6. Add a Series Recommendation when the Beat Map calls for it.
7. Run Art Critic Review.
8. Get Brief Approval.
9. Produce a Creative Brief Record.
10. Produce a Provider-Neutral Image Prompt Plan with Faithful, Amplified, and Minimal Prompt Variant Plans.
11. Critique the Prompt Plan against the approved Creative Brief.

## Provider Boundary

The current repository state is dry-run first. Provider Adapters, setup scripts, host adapters, and API-key-backed generation come after the manual First Slice works.
