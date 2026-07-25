# Output Journeys

Output journeys describe the roads Artist OS can take after Artist Meaning and Story Approval. They are intentionally medium-specific, but they all consume the same story layer.

Shared path:

```text
Reference
  -> Source Record
  -> Artist Meaning
  -> Transformation Brief
  -> Story / Beat Plan with Project-Level Workflow Scale Routing
  -> Long-Work Stewardship Activation Gate, when recommended or artist-requested
  -> Long-Work Stewardship, when activated by the artist
  -> Medium Plan with Medium-Level Workflow Scale Routing
  -> Cross-Medium Plan + Mixed-Media Critic + artist approval, when a second medium is activated outside Album
  -> Creative Brief or storyboard-ready handoff
  -> Prompt Plan or Text Generation Plan, when the medium has one
  -> Generation Approval Gate or Draft Generation Approval Gate, when required
  -> Output Record, when an artifact exists
  -> Output Critic Review
  -> Output Acceptance Gate
  -> Package Compilation, only for an approved or explicitly requested package
```

Journeys in this directory:

- `image.md`: still images and image series. **Implemented.**
- `video.md`: storyboard-ready Video Medium Plans for clips, scenes, sequences, trailers, and longer arcs. **Implemented as v0 planning.**
- `sound.md`: songs, instrumental tracks, soundscapes, scores, spoken-word
  beds, Sound Prompt Plans, and Suno Custom Mode field exports. **Implemented
  as dry-run planning; no audio generation.**
- `text.md`: rewrites, poems, monologues, scenes, scripts, and larger written forms. **Implemented.**
- `illustrated-written-work.md`: children's books, comics, story-with-images projects, covers plus interiors, and diagram-rich written works coordinated by Illustration Plan. **Planning contract exists.**
- `mixed-media.md`: Album v1 plus constrained general Cross-Medium Plan
  coordination. **Album v1 is implemented; the general schema/package
  foundation exists and its 1.0 review/approval and conductor lifecycle is
  tracked in `docs/release-1.0.md`.**

Writing-method integration lives in `docs/writing/README.md`. Its referenced `writing-fragments`, `writing-beats`, and `writing-shape` skill files are high-authority for raw material capture, beat-by-beat journey creation, and finished written shape.

Workflow Scale Routing decides which scale supports are recommended or active. It is persisted on the Beat Plan at project level and on each Medium Plan at medium level.

Long-Work Stewardship is recommended only when ADR 0013's two-condition threshold holds: BOTH a real cumulative dependency (outputs build on each other through sequence, dependency, emotional arc, or cumulative continuity) AND the per-medium length floor (video longer than ~5 minutes; text multi-chapter; audio a cumulative arc across tracks that is full-length ~8+ dependent tracks / ~30 minutes; image a book-scale ~20+ recurring-subject series), or when the artist explicitly asks for continuity tracking below threshold. ADR 0015 governs the artist-facing activation gate. An album, EP, portfolio, or collection of individual parts should not recommend stewardship by default however large — those, along with store sets and broad prompt branches, stay on the lighter collection review path. Neither the `cumulative_work` nor `full_long_form_project` scale level recommends stewardship by itself.

A compact multi-beat `arc` does not automatically trigger Long-Work Stewardship, image-series expansion, sound-sequence planning, or long-text handling. Trigger those paths when the artist accepts expansion or when the medium plan creates dependent parts whose later outputs rely on earlier outputs. When adjacent beats overlap or can be held together, the medium may recommend a compact shape such as a short written work, compressed visual arc, or single multi-section sound work.

## Gates And Reviews

The canonical shared gate order, critic roles, reviewer roles, mandatory bounded sub-agent review rule, and blocking behavior live in `docs/gates-and-reviews.md`.

Standing Sub-Agent Authorization is also canonical there: Artist OS may spawn bounded internal sub-agents automatically for mandatory reviews, validation, drafting passes, audits, and approved orchestration patterns.

Each journey file in this directory lists its local medium gates and medium-specific reviewers.
