# Output Journeys

Output journeys describe the roads Artist OS can take after Artist Meaning and Story Approval. They are intentionally medium-specific, but they all consume the same story layer.

Shared path:

```text
Reference
  -> Source Record
  -> Artist Meaning
  -> Transformation Brief
  -> Story / Beat Plan with Project-Level Workflow Scale Routing
  -> Long-Work Stewardship, when Workflow Scale Routing activates it
  -> Medium Plan with Medium-Level Workflow Scale Routing
  -> Creative Brief or storyboard-ready handoff
  -> Prompt Plan or Text Generation Plan, when the medium has one
  -> Generation Approval Gate or Draft Generation Approval Gate, when required
  -> Output Record, when an artifact exists
  -> Output Critic Review
  -> Output Acceptance Gate
```

Journeys in this directory:

- `image.md`: still images and image series. **Implemented.**
- `video.md`: storyboard-ready Video Medium Plans for clips, scenes, sequences, trailers, and longer arcs. **Implemented as v0 planning.**
- `sound.md`: songs, instrumental tracks, soundscapes, scores, spoken-word beds, Sound Prompt Plans, and Suno renderings. **Implemented.**
- `text.md`: rewrites, poems, monologues, scenes, scripts, and larger written forms. **Implemented.**
- `illustrated-written-work.md`: children's books, comics, story-with-images projects, covers plus interiors, and diagram-rich written works coordinated by Illustration Plan. **Planning contract exists.**
- `mixed-media.md`: coordinated outputs across multiple media. **Not built yet — forward-looking design.**

Writing-method integration lives in `docs/writing/README.md`. Its referenced `writing-fragments`, `writing-beats`, and `writing-shape` skill files are high-authority for raw material capture, beat-by-beat journey creation, and finished written shape.

Workflow Scale Routing decides which scale supports are active. It is persisted on the Beat Plan at project level and on each Medium Plan at medium level.

Long-Work Stewardship applies only when Workflow Scale Routing activates it because outputs build on each other through sequence, dependency, emotional arc, or cumulative continuity. Related but non-sequential portfolios, collections, store sets, or broad prompt branches should stay on the lighter collection review path.

A compact multi-beat `arc` does not automatically trigger Long-Work Stewardship, image-series expansion, sound-sequence planning, or long-text handling. Trigger those paths when the artist accepts expansion or when the medium plan creates dependent parts whose later outputs rely on earlier outputs. When adjacent beats overlap or can be held together, the medium may recommend a compact shape such as a short written work, compressed visual arc, or single multi-section sound work.

## Gates And Reviews

The canonical shared gate order, critic roles, reviewer roles, mandatory bounded sub-agent review rule, and blocking behavior live in `docs/gates-and-reviews.md`.

Standing Sub-Agent Authorization is also canonical there: Artist OS may spawn bounded internal sub-agents automatically for mandatory reviews, validation, drafting passes, audits, and approved orchestration patterns.

Each journey file in this directory lists its local medium gates and medium-specific reviewers.
