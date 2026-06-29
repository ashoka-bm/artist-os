# Package Compilation and Asset Packages

Status: proposed.

The dry-run spine (ADR 0001) plans prompts: the artist runs them through external
generators and brings assets back. The pipeline intakes those assets as Output
Records and accepts them one by one, but it has **no terminal stage that assembles
the accepted assets into a finished, named release and confirms everything landed.**
The Release Package Plan partly hid this gap by mixing two different jobs —
*planning* the bundle (what will be made) and *defining the finished bundle* (what it
should contain when done).

The project is really two stages:

1. **Planning** — produce all the prompts/plans across media. Coordinated by the
   Cross-Medium Plan (ADR 0012). Output: prompts the artist generates from.
2. **Packaging** — after the generations return, compile the accepted assets into a
   named format and verify completeness. This stage did not exist.

## Decisions

- **D12 — A distinct Package Compilation stage.** A terminal stage runs after Output
  Acceptance: it intakes the returned or imported assets (as Output Records),
  arranges them by a chosen Package Format, gates on completeness, and produces an
  Asset Package. It is separate from planning; it calls no provider (it arranges
  assets the artist already generated or imported), preserving the dry-run boundary.

- **Package Format — named arrangement template.** A reusable template for how a
  finished release arranges its assets. First set: *album* (album title, album
  thumbnail, and per-song audio plus cover image and the song/image titles),
  *article-with-photos* (article text plus inline photos with captions),
  *video-with-soundtrack* (video plus audio plus optional poster). A Package Format
  mirrors Medium Roles (ADR 0012, D10): one primary asset with supporting assets
  arranged around it.

- **Asset Package — the compiled output artifact.** The accepted Output Records
  arranged per the Package Format, with completeness status. It is the finished,
  artist-facing bundle, distinct from the Release Package Plan that planned it and the
  Cross-Medium Plan that coordinated it.

- **Completeness gate.** The Stage-1 plan (Cross-Medium Plan + medium plans) is the
  checklist; the accepted Output Records are the ticks. Package Compilation cannot
  close the Asset Package while a planned deliverable lacks an accepted Output Record,
  unless the artist explicitly waives the missing deliverable (the same waiver posture
  as the Output Acceptance Gate). This is the "confirm everything landed" guarantee.

- **D11 resolution (supersedes the unify/stack framing).** The Release Package Plan is
  split along the plan/output seam, not unified into or stacked beside the
  Cross-Medium Plan: its *planning* role belongs to the Cross-Medium Plan (Stage 1);
  its *finished-bundle* role becomes the Package Format + Asset Package (Stage 2). An
  album is therefore a Cross-Medium Plan (plan) compiled through the *album* Package
  Format into an Asset Package. Reconciling the shipped Release Package Plan record to
  this split is a follow-on migration.

- **D13 — Index-first Package Format library.** Package Formats live in
  `docs/structure-library/package-format/` — an index README plus one file per format
  (album, article-with-photos, video-with-soundtrack), loaded index-first like the
  Story and Cultural-Format Structure libraries. Each format file defines its slots
  (primary + supporting, per ADR 0012 D10), required vs optional assets, per-asset
  metadata (titles, captions), arrangement/order, and the completeness rules that serve
  as the Completeness gate's checklist.

- **D14 — Asset Package is a thin persisted manifest.** The Asset Package is a small
  schema-backed record that references accepted Output Records by id, assigns them to
  format slots, records per-slot completeness (`filled` / `missing` / `waived`), and
  points at the Package Format and Cross-Medium Plan. It copies no asset content —
  Output Records stay the source of truth. It is persisted, not projected: unlike the
  resume state (ADR 0012 D5, deliberately a projection), the Asset Package is the
  durable deliverable and records waiver decisions. The rule: project scaffolding, but
  persist anything that is the deliverable or carries a decision.

## Consequences

- A new terminal phase (after Output Critic Review / Output Acceptance) — Package
  Compilation — activates whenever a project has deliverables to assemble, and is the
  natural home for multi-output and multi-medium projects (albums, article+photos,
  video+soundtrack).
- It builds on existing machinery: Output Records, the import path for returned
  assets, the Output Acceptance Gate, and the visible Artist Library `exports/` area
  where the Asset Package materializes.
- Planning and packaging become each other's verification: the plan is the checklist,
  the package is the proof.
- The shipped Release Package Plan migrates (planning → Cross-Medium Plan; bundle
  definition → Package Format / Asset Package). Design-only now; the migration is
  separate work and must keep Album v1 tests green.
- No provider is called during compilation; ADR 0001's dry-run boundary holds.

## Open

- Partial-package policy: when a missing deliverable may be waived, and how the
  `waived` status is surfaced to the artist (the Output Acceptance waiver posture).
- How the Asset Package materializes into the visible `exports/` layout in
  `docs/storage.md`.
- Naming: the format library sits beside `structure-library/` though a Package Format
  is an assembly template, not a story/format *structure* — confirm that path or give
  it its own top-level library dir.
