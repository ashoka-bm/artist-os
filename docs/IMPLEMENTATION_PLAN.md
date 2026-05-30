# Implementation Plan

Last updated: 2026-05-30

## Status Note

The first product-layer artifacts now exist: `CONTEXT.md`, `THEORY.md`, `ARCHITECTURE.md`, `AGENTS.md`, `docs/metadata-schema.md`, `schemas/`, `examples/`, and `skills/`.

Those product docs are authoritative over this early implementation plan. The 23-question style, direction, and series review added these required concepts to the First Slice:

- Style Direction, Style Interview, Primary Style, Style Modifiers, Style Confirmation Status, and Style/Visual Conflict handling.
- Series Recommendation, Triptych, Image Series, Style Progression, Series Calibration Image, Calibration Choice boundaries, and Variant Test Axis Labels.
- Wondermint categories as optional style/category mapping metadata, required only for Wondermint upload.

## Purpose

Artist Generation should let a user add any creative input, such as an image, video, song, text, or mixed reference set, then help an agent extract its emotional and artistic structure and transform that structure into new media formats.

The repository should grow into a GStack-inspired agent plugin: structured skills, specialist roles, onboarding scripts, durable project memory, and clear generation metadata.

## Document Tracks

There are two separate bodies of work:

1. Build the operating system.
2. Define and ship the operating system.

The current README, progress note, implementation plan, and GStack map belong to the first body of work. They help us build the repository and make decisions across sessions.

The future `AGENTS.md`, `ARCHITECTURE.md`, `THEORY.md`, metadata schemas, skills, tests, and helpers belong to the second body of work. They are the product artifacts that will make up the artist operating system itself.

Working rule: when a product artifact exists, move stable product decisions into it and let process docs link to it. Process docs should guide construction; product docs should define behavior.

## Success Condition

This plan is useful when a future agent can open it and understand:

- Which GStack patterns we are borrowing.
- What core artistic model we are building around.
- How ingestion, interpretation, generation, critique, and provenance fit together.
- Which steps to execute next without re-litigating the whole direction.

## GStack Patterns To Borrow

GStack is useful less as a codebase to copy and more as a product pattern for agent work.

### Repository Shape

Observed GStack structure:

```text
.
├── README.md
├── AGENTS.md
├── ARCHITECTURE.md
├── DESIGN.md
├── ETHOS.md
├── CONTRIBUTING.md
├── SKILL.md / SKILL.md.tmpl
├── skills as top-level folders
├── bin/
├── lib/
├── hosts/
├── docs/
├── scripts/
├── test/
└── model-overlays/
```

Recommended Artist Generation structure:

```text
.
├── README.md
├── PROGRESS.md
├── AGENTS.md
├── ARCHITECTURE.md
├── THEORY.md
├── docs/
│   ├── IMPLEMENTATION_PLAN.md
│   ├── gstack-repo-map.md
│   └── metadata-schema.md
├── skills/
│   ├── ingest-reference/
│   ├── meaning-interview/
│   ├── emotional-analysis/
│   ├── transformation-plan/
│   ├── generate-image/
│   ├── generate-audio/
│   ├── generate-video/
│   └── critique-asset/
├── hosts/
├── bin/
├── lib/
├── schemas/
├── examples/
├── test/
└── .tmp/
```

Add these incrementally. Do not create empty directories until a workflow needs them.

### Automation And Onboarding

Borrow these concepts:

- `setup` script: installs or links skills into the supported agent host.
- `hosts/`: separates Codex, Claude Code, OpenClaw, and future host differences.
- `bin/`: executable helpers for repeatable tasks.
- `scripts/`: development and generation scripts.
- `VERSION` and `CHANGELOG.md`: useful once external users install the plugin.
- `.env.example`: documents required API keys without exposing secrets.
- generated skill docs: skill templates can produce host-specific `SKILL.md` files later.

First version should support one host well, probably Codex because this repo is being built in Codex. Add host abstraction only after the first skill works.

### Agent Roles

GStack works because each skill has a specialist role. Artist Generation should use role separation too:

- `intake artist`: asks what the reference means to the user.
- `formal analyst`: identifies medium-specific formal properties.
- `emotional analyst`: maps formal signals to emotional hypotheses.
- `story analyst`: identifies beats, value shifts, and changes.
- `translation director`: decides how meaning transfers across formats.
- `generator`: calls image/audio/video tools.
- `critic`: compares the output against the Creative Brief.
- `archivist`: records prompts, inputs, outputs, provenance, and rights notes.

### Persistent Memory

Borrow the spirit of GStack's learnings and session tooling:

- `PROGRESS.md` for current repository status.
- Per-project creative preferences later, probably under a local ignored state directory.
- A manifest that records each Reference, Creative Brief, Generated Work, Output Record, and review note.
- A "taste memory" concept that tracks what the artist accepts, rejects, and revises.

## Core Artistic Model

The system should treat an artwork as layered evidence, not as a single prompt.

### Layer 1: Source Object

What the user adds:

- Image.
- Video.
- Audio/song.
- Text/poem/script.
- Moodboard or mixed references.

Capture:

- File path or external reference.
- Media type.
- User-provided title.
- Context of use.
- Rights/licensing notes.
- What the user wants transformed.

### Layer 2: Formal Components

These are observable properties of the work.

Visual examples:

- Color, value, line, shape, form, space, texture.
- Contrast, balance, emphasis, movement, pattern, rhythm, unity, variety, proportion.

Audio examples:

- Tempo, dynamics, timbre, harmony, melody, rhythm, density, silence, repetition, tension/release.

Video examples:

- Shot rhythm, motion, framing, camera distance, color grade, edit tempo, scene contrast, performance energy.

Text examples:

- Voice, diction, imagery, pacing, point of view, metaphor, structure, conflict, reversal.

Reference: Getty's formal analysis materials distinguish elements of art from principles of design and describe principles such as balance, emphasis, movement, rhythm, unity, and variety.

### Layer 3: Emotional Structure

These are interpretations, not facts. The system should label confidence and evidence.

Use Core Tension Pairs instead of bipolar sliders. Each pole can be present independently, and the tension between poles carries meaning.

The first Core Tension Pairs are:

- Attraction / Repulsion.
- Proximity / Distance.
- Order / Chaos.
- Stillness / Motion.
- Legibility / Opacity.
- Control / Surrender.
- Safety / Threat.
- Presence / Absence.

Each pair should record salience, pole A presence, pole B presence, tension intensity, evidence, optional artist note, and translation notes. Emotional Qualities preserve freeform artist language that does not fit the core set.

### Layer 4: Story Beats And Value Shifts

A beat is the smallest meaningful change the system can name.

For this repo, a beat should record:

- Before state.
- After state.
- What changed.
- Emotional value before.
- Emotional value after.
- Evidence from the source.
- Whether the user agrees.

StoryGrid's value-shift concept is useful here: story meaning comes from a human value changing from positive to negative, negative to positive, or changing in intensity.

Example:

```text
Beat: "The figure stops running and turns toward the storm."
Before: avoidance, fear, forward motion.
After: confrontation, resolve, stillness.
Value shift: fear -> courage.
Emotional payload: dread mixed with agency.
Translatable forms:
- Image: lone silhouette facing high-contrast sky.
- Audio: frantic rhythm drops into sustained low chord.
- Video: handheld motion cuts to locked-off frame.
```

### Layer 5: Personal Meaning

This is the "grill me" layer. The user explains what the source means to them.

The system should ask questions that expose:

- Why this reference matters.
- What should survive translation.
- What must not be copied literally.
- Which emotions are intended versus accidental.
- Which details are sacred.
- Which parts can be transformed aggressively.
- What the new artifact should make someone feel.

This layer should override agent guesses. If formal analysis says "cold and alienated" but the user says it represents relief, the user meaning wins and the contradiction is recorded.

## Workflow

### Phase 1: Ingest

Goal: accept source material and create a source record.

Outputs:

- `source_id`.
- media type.
- file/reference metadata.
- initial user note.
- rights/licensing warning if needed.

Do not generate anything in this phase.

### Phase 2: Meaning Interview

Goal: run a structured grill session before analysis hardens into assumptions.

Outputs:

- user intent.
- personal meaning.
- must-preserve qualities.
- allowed transformations.
- target media.
- success criteria.

The interview should be short by default and expandable when the user wants depth.

### Phase 3: Formal Analysis

Goal: break the source into observable components.

Outputs:

- medium-specific formal analysis.
- evidence snippets, timestamps, regions, or excerpts.
- uncertainty notes.

### Phase 4: Emotional Structure

Goal: convert formal evidence plus Artist Meaning into Emotional Structure.

Outputs:

- Core Tension Pair Records.
- Emotional Qualities.
- Emotional Arc.
- contradictions and ambiguities.
- confidence levels.

### Phase 5: Beat Map

Goal: express the source as changes over time or implied changes in a static work.

Outputs:

- beat list.
- value shifts.
- emotional payload per beat.
- translatable motifs.

### Phase 6: Transformation Plan

Goal: decide how the source should become another format.

Outputs:

- target format.
- preserved emotional core.
- changed formal strategy.
- prompt plan.
- generation settings.
- review checklist.

### Phase 7: Generate

Goal: call the appropriate generation tool or produce Provider-Neutral Prompt Plans for manual generation.

Outputs:

- Generated Work references.
- prompt and model metadata.
- seed/settings when available.
- failure notes.

### Phase 8: Critique And Iterate

Goal: compare the output to the Creative Brief, not merely to the Reference.

Outputs:

- what matched.
- what drifted.
- recommended revisions.
- accepted/rejected status.
- taste-memory update.

### Phase 9: Archive

Goal: make the work reproducible and understandable later.

Outputs:

- source record.
- brief.
- generated outputs.
- review notes.
- rights/provenance notes.

## Data Model Sketch

Start with JSON files or JSONL manifests before building a database.

```json
{
  "source_id": "src_20260528_001",
  "title": "Untitled storm reference",
  "media_type": "image",
  "source_uri": "inputs/storm-reference.png",
  "artist_meaning": {
    "why_it_matters": "It feels like choosing to stop running.",
    "must_preserve": ["defiance", "weather pressure", "small figure"],
    "may_transform": ["literal storm", "color palette"]
  },
  "formal_analysis": {
    "contrast": "high",
    "movement": "diagonal pressure from upper left",
    "palette": ["blue gray", "white", "black"]
  },
  "core_tension_pairs": {
    "safety_threat": {
      "poles": {
        "safety": { "presence": 0.2 },
        "threat": { "presence": 0.9 }
      },
      "tension_intensity": 0.85,
      "evidence": ["small figure faces weather pressure"],
      "translation_notes": ["contrast a vulnerable figure against an overwhelming environment"]
    },
    "control_surrender": {
      "poles": {
        "control": { "presence": 0.65 },
        "surrender": { "presence": 0.4 }
      },
      "tension_intensity": 0.7,
      "evidence": ["the figure turns toward the storm instead of fleeing"],
      "translation_notes": ["show deliberate posture inside uncontrollable conditions"]
    }
  },
  "emotional_qualities": ["dread", "resolve"],
  "beats": [
    {
      "before": "avoidance",
      "after": "confrontation",
      "value_shift": "fear -> courage",
      "evidence": "figure turns toward the storm"
    }
  ],
  "outputs": []
}
```

## Multi-Step Build Plan

### Step 1: Repository Context And Product Docs

Create the first product docs while keeping process docs separate:

- `AGENTS.md`: repo-specific agent behavior.
- `ARCHITECTURE.md`: plugin shape and data flow.
- `THEORY.md`: artistic and emotional model.
- `docs/metadata-schema.md`: first manifest schema.

Maintain the build-process references that guide this work:

- `docs/gstack-repo-map.md`: explicit mapping from GStack to this repo.
- `docs/IMPLEMENTATION_PLAN.md`: staged execution plan.
- `PROGRESS.md`: current handoff and status.

Verification:

- A future agent can read the docs and explain the project in under five minutes.
- Stable product rules live in product docs, not only in `README.md`, `PROGRESS.md`, or planning notes.

### Step 2: First Thin Workflow

Build a text-only ingestion workflow before handling binary media.

Why text first:

- Easy to test.
- No paid model calls required.
- Still exercises meaning interview, emotional analysis, beats, and transformation plan.

Deliverables:

- `skills/ingest-reference/SKILL.md`.
- `skills/meaning-interview/SKILL.md`.
- Example input in `examples/`.
- Example manifest in `examples/`.

Verification:

- Given a poem or short passage, the agent can produce a structured Creative Brief and Beat Map.

### Step 3: Image Workflow

Add image ingestion and image-to-image/image-to-prompt planning.

Deliverables:

- `skills/generate-image/SKILL.md`.
- image metadata schema additions.
- visual critique checklist.

Verification:

- Given an image reference and user meaning, the agent produces a prompt plan and critique checklist.

### Step 4: Cross-Format Translation

Translate one source into a different medium.

Candidate first cross-format:

- Text -> image.
- Image -> audio prompt.

Deliverables:

- `skills/transformation-plan/SKILL.md`.
- cross-format mapping tables.
- examples showing preserved emotion with changed formal components.

Verification:

- The output plan names what is preserved, what changes, and how success will be judged.

### Step 5: Generation Tool Adapters

Add actual tool calls only after prompts and metadata are stable.

Deliverables:

- `bin/` helper or host-native tool usage.
- `.env.example`.
- provider-neutral interface notes.

Verification:

- A dry run can produce prompts/configs without paid calls.
- A real run records provider, model, prompt, settings, and output references.

### Step 6: Critique And Taste Memory

Create an iteration loop that learns the artist's preferences.

Deliverables:

- `skills/critique-asset/SKILL.md`.
- accepted/rejected revision records.
- local ignored taste-memory format.

Verification:

- The next generation attempt can cite previous user preferences without rereading the whole history.

### Step 7: Onboarding And Host Support

Package the repo as a plugin/skill bundle.

Deliverables:

- setup script.
- host adapter for Codex first.
- generated docs if needed.
- smoke test.

Verification:

- A fresh checkout can install or link skills and run the text workflow.

## Research References

- Getty, "Understanding Formal Analysis": elements and principles of art/design, including balance, emphasis, movement, rhythm, unity, and variety. https://www.getty.edu/education/teachers/building_lessons/formal_analysis2.html
- StoryGrid, "Value Shift 101": story values as human experiences that change across units of story. https://storygrid.com/value-shift-101/
- Interaction Design Foundation, "Norman's Three Levels of Design": visceral, behavioral, and reflective levels as a useful emotional-design lens. https://www.interaction-design.org/literature/article/norman-s-three-levels-of-design

## Immediate Next Move

Create Step 1 docs, then choose the first text-only workflow. Avoid creating generation code until the theory, metadata, and review loop are explicit enough to test.
