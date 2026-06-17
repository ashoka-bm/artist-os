# Output Journeys

Output journeys describe the roads Artist OS can take after Artist Meaning and Story Approval. They are intentionally medium-specific, but they all consume the same story layer.

Shared path:

```text
Reference
  -> Source Record
  -> Artist Meaning
  -> Transformation Brief
  -> Story / Beat Plan
  -> Medium Plan
  -> Prompt Plan or Text Generation Plan
  -> Generation Approval Gate or Draft Generation Approval Gate, when required
  -> Output Record, when an artifact exists
  -> Output Critic Review
  -> Output Acceptance Gate
```

Journeys in this directory:

- `image.md`: still images, triptychs, and image series.
- `video.md`: short clips, scenes, sequences, trailers, and longer arcs.
- `sound.md`: songs, instrumental tracks, soundscapes, scores, spoken-word beds, and Suno prompt plans.
- `text.md`: rewrites, poems, monologues, scenes, scripts, and larger written forms.
- `mixed-media.md`: coordinated outputs across multiple media.

Writing-method integration lives in `docs/writing/README.md`. Its referenced `writing-fragments`, `writing-beats`, and `writing-shape` skill files are high-authority for raw material capture, beat-by-beat journey creation, and finished written shape.

## Gates And Reviews

The canonical shared gate order, critic roles, reviewer roles, mandatory bounded sub-agent review rule, and blocking behavior live in `docs/gates-and-reviews.md`.

Each journey file in this directory lists its local medium gates and medium-specific reviewers.
