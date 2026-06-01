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

Use `README.md` for public install and sharing instructions.

## Product Invariant

Every Prompt Variant Plan and Generated Work must trace back to:

- Artist Meaning,
- evidence from the Reference,
- the Creative Brief,
- Emotional Structure,
- Visual Dynamics or Sonic Dynamics, depending on target medium,
- the Beat or Tension Point,
- the Transformation Plan,
- the Prompt Plan,
- and the Output Record when generation exists.

Provider-Neutral Image Prompt Plan records should validate against `schemas/prompt-plan.schema.json`.

Sound Creative Brief records should validate against `schemas/sound-creative-brief.schema.json`.

Suno Sound Prompt Plan records should validate against `schemas/sound-prompt-plan.schema.json`.

## Operating Rules

These are the invariants that are not derivable from the product theory. The runtime rules they used to restate now live in their canonical docs (below), so this list stays short and authoritative.

- Do not make provider-backed generation calls without explicit user approval. Drafting prompts and boards is always allowed; sending them to a provider is not.
- Use Dry Runs before invoking any media generation provider.
- Do not commit user-provided media, Generated Works, Workspace Library project folders, private artist references, secrets, or API keys.
- Artist Meaning overrides agent interpretation. Treat Emotional Structure as a hypothesis until the artist confirms it.
- Preserve provenance before optimizing for speed. Keep Derived Symbols and Derived Sonic Elements marked and traceable to the Creative Brief.

Everything else an agent needs at runtime is canonical elsewhere — point to it, do not restate it:

- **Gates, boards, stage completion, style/series logic, Prompt Variant Plans** → `THEORY.md` (and `docs/text-to-sound/THEORY.md` + `ARCHITECTURE.md` for sound). This is the home for the gate order, the gate question wording, the Visual Gate Board contract, the four-stage completion rules, the separation of Emotional Structure / Visual Dynamics / Sonic Dynamics / Style Direction, Style-as-last-priority, the Wondermint Category Reference rule, and the Series Amplitude Plan.
- **Persistence and storage** → `docs/storage.md`: persist each phase before advancing (manifest, stage record, event, sidecar-tagged assets, SQLite refresh), use `artist-os.sqlite` as the query index, initialize with `bin/artist-os-db setup` when missing, and treat `status = missing` projects as historical until their files are restored.
- **The runtime phase order for each slice** → the `artist-os` conductor skill, `skills/first-slice-flow`.

## Slices

Artist OS ships two dry-run slices (no provider-backed generation):

- **First Slice** — Text Reference → Provider-Neutral Image Prompt Plan.
- **Text-to-Sound Slice** — Text Reference → Suno Sound Prompt Plan.

The authoritative phase order for each is owned by the `artist-os` conductor skill, `skills/first-slice-flow/SKILL.md` → "Phase Order". Read it there rather than maintaining a second copy here.

## Provider Boundary

The current repository state is dry-run first. Provider Adapters, setup scripts, host adapters, and API-key-backed generation come after the manual image and Suno slices work.
