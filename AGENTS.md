# Artist OS Agent Rules

These rules apply to agents building or running Artist OS inside this repository.

## Source Of Truth

Read `CONTEXT.md` before changing product language.

Use these product docs as durable references:

- `THEORY.md`
- `ARCHITECTURE.md`
- `docs/progress.md`
- `docs/pipeline-contract.md`
- `docs/gates-and-reviews.md`
- `docs/subagent-orchestration.md`
- `docs/story/THEORY.md`
- `docs/story/ARCHITECTURE.md`
- `docs/output-journeys/`
- `docs/structure-library/`
- `docs/writing/README.md`
- `docs/writing/references/`
- `docs/text-to-sound/THEORY.md`
- `docs/text-to-sound/ARCHITECTURE.md`
- `docs/metadata-schema.md`
- `docs/adr/`
- `schemas/`
- `skills/`

Use `README.md` for public install and sharing instructions.

## Product Invariant

Every Prompt Variant Plan, Text Generation Plan, and concrete Output Artifact must trace back to:

- Artist Meaning,
- evidence from the Reference,
- the governing Creative Brief,
- Emotional Structure,
- Visual Dynamics, Sonic Dynamics, or Text Medium Plan structure, depending on target medium,
- the Beat or Tension Point,
- the Transformation Brief,
- the Prompt Plan or Text Generation Plan,
- and the Output Record when an Output Artifact exists.

Provider-Neutral Image Prompt Plan records should validate against `schemas/prompt-plan.schema.json`.

Image Creative Brief records should validate against `schemas/creative-brief.schema.json`.

Sound Creative Brief records should validate against `schemas/sound-creative-brief.schema.json`.

Sound Prompt Plan records should validate against `schemas/sound-prompt-plan.schema.json`.

Text Creative Brief records should validate against `schemas/text-creative-brief.schema.json`.

Text Generation Plan records should validate against `schemas/text-generation-plan.schema.json`.

Prompt Branch Set records should validate against `schemas/prompt-branch-set.schema.json`.

Output Records should validate against `schemas/output-record.schema.json`.

Artist Meaning records should validate against `schemas/artist-meaning.schema.json`.

Gate Decision records should validate against `schemas/gate-decision.schema.json`.

Transformation Brief records should validate against `schemas/transformation-brief.schema.json`.

Beat Plan records should validate against `schemas/beat-plan.schema.json`.

Review Records should validate against `schemas/review-record.schema.json`.

## Operating Rules

These are the invariants that are not derivable from the product theory. The runtime rules they used to restate now live in their canonical docs (below), so this list stays short and authoritative.

- Do not make provider-backed generation calls without explicit user approval. Drafting prompts and boards is always allowed; sending them to a provider is not.
- Use Dry Runs before invoking any media generation provider.
- Do not commit user-provided media, Generated Works, Workspace Library project folders, private artist references, secrets, or API keys.
- Artist Meaning overrides agent interpretation. Treat Emotional Structure as a hypothesis until the artist confirms it.
- Preserve provenance before optimizing for speed. Keep Derived Symbols and Derived Sonic Elements marked and traceable to the Creative Brief.

## Git Workflow

This repository allows direct commits and pushes to `main` when the user explicitly asks for a direct `main` push or confirms it after being asked. Do not push to `main` by default when the target branch is ambiguous.

Everything else an agent needs at runtime is canonical elsewhere — point to it, do not restate it:

- **Gate order, gate semantics, critic/reviewer roles, review execution, blocking findings** → `docs/gates-and-reviews.md`. This is the canonical contract for the shared gate order and review rules; medium-specific docs may add local gates but do not redefine them.
- **Subagent delegation, parallel production, worker packets, and synchronization barriers** → `docs/subagent-orchestration.md`. This is the canonical contract for what subagents may do, what only the conductor may do, and when parallel work is allowed.
- **Visual Gate Boards, stage completion, style/series logic, Prompt Variant Plans** → `THEORY.md` (and `docs/text-to-sound/THEORY.md` + `ARCHITECTURE.md` for sound). This is the home for the Visual Gate Board contract, the four-stage completion rules, the separation of Emotional Structure / Visual Dynamics / Sonic Dynamics / Style Direction, Style-as-last-priority, the Wondermint Category Reference rule, and the Series Amplitude Plan.
- **Persistence and storage** → `docs/storage.md`: persist each phase before advancing (manifest, stage record, event, sidecar-tagged assets, SQLite refresh), use `artist-os.sqlite` as the query index, initialize with `bin/artist-os-db setup` when missing, and treat `status = missing` projects as historical until their files are restored.
- **The runtime phase order for each slice** → the `artist-os` conductor skill, `skills/artist-os`.

## Slices

Artist OS ships three dry-run slices:

- **First Slice** — Text Reference → Provider-Neutral Image Prompt Plan.
- **Text-to-Sound Slice** — Text Reference → Sound Prompt Plan (with Suno renderings).
- **Text Journey Slice** — Text Reference → Text Generation Plan and drafted written Output Records.

The authoritative phase order for each is owned by the `artist-os` conductor skill, `skills/artist-os/SKILL.md` → "Phase Order". Read it there rather than maintaining a second copy here.

## Provider Boundary

The current repository state is dry-run first. Provider Adapters, setup scripts, host adapters, and API-key-backed generation come after the manual image, Suno, and Text Journey slices work.
