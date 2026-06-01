# Artist OS Agent Rules

These rules apply to agents building or running Artist OS inside this repository.

## Source Of Truth

Read `CONTEXT.md` before changing product language.

Use these product docs as durable references:

- `THEORY.md`
- `ARCHITECTURE.md`
- `docs/text-to-sound/THEORY.md`
- `docs/text-to-sound/ARCHITECTURE.md`
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
- Visual Dynamics or Sonic Dynamics, depending on target medium,
- the Beat or Tension Point,
- the Transformation Plan,
- the Provider-Neutral Prompt Plan,
- and the Output Record when generation exists.

Provider-Neutral Image Prompt Plan records should validate against `schemas/prompt-plan.schema.json`.

Sound Creative Brief records should validate against `schemas/sound-creative-brief.schema.json`.

Suno Sound Prompt Plan records should validate against `schemas/sound-prompt-plan.schema.json`.

## Operating Rules

- Do not make provider-backed generation calls without explicit user approval.
- Do not commit user-provided media, Generated Works, secrets, or API keys.
- Treat Emotional Structure as a hypothesis until the artist confirms it.
- Artist Meaning overrides agent interpretation.
- Preserve provenance before optimizing for speed.
- Use Dry Runs before invoking media generation providers.
- Persist real Artist OS project work in `workspace-library/artist-os/`; do not leave project state only in the chat context.
- Store images in the matching `assets/` subfolder and create a same-basename sidecar that validates against `schemas/asset-metadata.schema.json`.
- If the Workspace Library is missing, initialize it with `bin/artist-os-db setup` before starting or resuming project work.
- Use `workspace-library/artist-os/artist-os.sqlite` as the local query index; refresh it with `bin/artist-os-db sync` after project manifests, events, or assets change.
- Treat SQLite projects with `status = missing` as historical references whose project folder was not found during the latest sync; do not resume them until the files are restored.
- Do not commit generated media, private artist references, or Workspace Library project folders.
- Keep Derived Symbols marked and traceable.
- Keep Visual Dynamics separate from Emotional Structure.
- Keep Sonic Dynamics separate from Emotional Structure.
- Keep Style Direction separate from Emotional Structure and Visual Dynamics.
- Treat Style Direction as the last priority after Artist Meaning, Emotional Structure, Beat Map, and Visual Dynamics.
- When the artist has not named a specific style directly, ask whether they have a specific vision or want to explore what art style to use.
- Run visual choice gates in this default order: Symbology Gate, Style Gate, then Minimalist-to-Maximalist Gate.
- Do not move from Interpretation to Visualization/Symbolic, Visualization/Symbolic to Style, or Style to Detail until the current stage is complete or the artist explicitly says to proceed unconfirmed.
- At the Symbology Gate, show six concise symbolic representations, ask which one the artist wants, ask whether the work should be a single image, emotional arc, or multi-image presentation, and ask whether they want it visualized.
- At the Style Gate, show six concise suggested styles, ask whether the artist wants some of them or has something else in mind, and ask whether they want the styles visualized.
- Surface Style/Visual Conflicts and record proposed Style Adaptations instead of silently letting style override Visual Dynamics.
- Use the Wondermint Category Reference only as seed vocabulary unless preparing a Wondermint upload, where exact accepted subcategory names are required.
- Recommend a Series Plan when multiple significant Beats would be flattened into one image, but do not create multiple image prompt plans without artist approval.
- For triptych or image-series recommendations, capture an internal 0-1 Series Amplitude Plan for each suggested image and vary adjacent images on at least two dimensions unless sameness is intentional.
- For an approved Series Plan, produce three calibration Prompt Variant Plans for one Series Calibration Image first and wait for artist approval before producing the remaining series.
- Use Prompt Variant Plans to test named unresolved creative axes when that is more useful than simple intensity variation.
- Before locking final Prompt Variant Plans, use the Minimalist-to-Maximalist Gate to compare visual intensity once symbology and style are selected.
- After every meaningful Artist OS phase, update the project manifest, write the stage record, append an event to `events.jsonl`, store any images with sidecar metadata in the Workspace Library, and refresh the SQLite index.

## First Slice

The First Slice is Text Reference to Image Prompt Plan:

1. Ingest a Text Reference.
2. Run a Meaning Interview.
3. Produce a Source Record.
4. Produce a draft Creative Brief Document.
5. Define Symbology Direction with a visual Symbology Board when unresolved.
6. Define Style Direction.
7. Add a Series Recommendation when the Beat Map calls for it.
8. Run Art Critic Review.
9. Get Brief Approval.
10. Use the Minimalist-to-Maximalist Gate when intensity is unresolved.
11. Produce a Creative Brief Record.
12. Produce a Provider-Neutral Image Prompt Plan with Faithful, Amplified, and Minimal Prompt Variant Plans.
13. Critique the Prompt Plan against the approved Creative Brief.

## Text-To-Sound Slice

The Text-to-Sound Slice is Text Reference to Suno Sound Prompt Plan:

1. Ingest a Text Reference.
2. Run a Meaning Interview.
3. Produce a Source Record.
4. Produce a draft Sound Creative Brief Document.
5. Define Sonic Concept Direction.
6. Define Genre / Production Direction.
7. Define Tempo / Groove Direction.
8. Ask whether the work should have lyrics or intelligible words.
9. If adapted or new lyrics are requested, draft the lyrics and include them in brief review before prompt locking.
10. Define Arrangement / Form Direction and Sonic Dynamics.
11. Run Music / Sound Critic Review.
12. Get Brief Approval.
13. Produce a Sound Creative Brief Record.
14. Produce a Suno Sound Prompt Plan with Faithful, Amplified, and Minimal Prompt Variant Plans.
15. Critique the Prompt Plan against the approved Sound Creative Brief.

## Provider Boundary

The current repository state is dry-run first. Provider Adapters, setup scripts, host adapters, and API-key-backed generation come after the manual First Slice works.
