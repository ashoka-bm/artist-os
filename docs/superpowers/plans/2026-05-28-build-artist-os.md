# Build Artist OS Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build Artist Generation from planning docs into a working agent operating system that can ingest text, interview the artist about meaning, extract emotional structure, and produce a text-to-image transformation plan.

**Architecture:** Start with product documentation and schemas, then add manual skills before adding setup scripts or generation adapters. The first vertical slice should be text-only so the core artistic model can be tested without paid API calls or binary media handling.

**Tech Stack:** Markdown skills, JSON Schema, example JSON fixtures, shell commands, and later Codex-compatible skill packaging. No runtime framework is needed for the first slice.

---

## Recommendation

Start by building the product layer, not tooling. The next concrete milestone should be:

> Given a short text passage and a Meaning Interview, an agent can produce a Creative Brief Document, run Art Critic Review, wait for Brief Approval, then generate a Creative Brief Record and Provider-Neutral Image Prompt Plan that trace every choice back to Artist Meaning and the Reference.

The Provider-Neutral Image Prompt Plan contains three Prompt Variant Plans from the same approved Creative Brief: Faithful, Amplified, and Minimal.

## Post-Grill Product Updates

This plan has been executed and then refined by the 23-question style, direction, and series review. The product docs are now authoritative where older task templates in this plan are narrower.

Current required additions:

- Style Direction is a Creative Brief layer separate from Emotional Structure and Visual Dynamics.
- Style Direction is chosen after the first Artist Meaning, Emotional Structure, and Beat Map pass, and before Art Critic Review.
- Artist-specified style skips the full Style Interview, with at most one Style Clarifier.
- Hybrid style uses one Primary Style plus bounded Style Modifiers.
- Style Direction is the last priority and cannot override Artist Meaning, Emotional Structure, Beat Map, or Visual Dynamics.
- Style/Visual Conflicts are surfaced and stored with proposed Style Adaptations.
- Style Interview is adaptive, uses a fallback order only when needed, can stop early, and produces a Style Recommendation.
- Style Recommendation can enter Art Critic Review unconfirmed; Brief Approval confirms style unless the artist explicitly excludes it.
- Wondermint subcategories are optional Artist OS metadata unless preparing Wondermint upload.
- Series Recommendation is evaluated for multi-Beat References but can still choose single image.
- Triptych is for clear three-part transformation; image series is for extended sequence, motif evolution, or world exploration.
- Style Progression can be recommended in the First Slice but becomes executable only after Series Plan approval.
- Approved Series Plans start with one Series Calibration Image selected by the most representative Calibration Image Role.
- Series Calibration uses three calibration Prompt Variant Plans; remaining series images use one prompt per Image Role by default.
- Calibration Choice updates visual language and continuity rules, but not Artist Meaning, Core Tension Pairs, or Beat Map without explicit artist direction.
- Prompt Variant Plan labels stay Faithful, Amplified, and Minimal; Variant Test Axis Labels explain unresolved creative dimensions being tested.

This is the smallest useful version of the operating system. It proves the theory before we spend time on image/audio/video ingestion, provider APIs, setup scripts, or host adapters.

## File Structure

Create or modify these files in this order:

- Modify: `PROGRESS.md`  
  Track each completed task and the current next step.
- Create: `THEORY.md`  
  Product-layer art model: source object, formal components, emotional components, story beats, personal meaning, and transformation.
- Create: `ARCHITECTURE.md`  
  Product-layer data flow from source input to archive.
- Create: `docs/metadata-schema.md`  
  Human-readable manifest model.
- Create: `AGENTS.md`  
  Product-layer operating rules for agents working in this repo.
- Create: `schemas/source-record.schema.json`  
  Machine-checkable Source Record schema.
- Create: `schemas/creative-brief.schema.json`  
  Machine-checkable Creative Brief Record and Beat Map schema.
- Create: `examples/text-source.md`  
  Small text fixture for the first workflow.
- Create: `examples/text-creative-brief.example.json`  
  Expected structured output fixture.
- Create: `skills/ingest-reference/SKILL.md`  
  First manual skill: source intake only.
- Create: `skills/meaning-interview/SKILL.md`  
  Second manual skill: Meaning Interview.
- Create: `skills/text-to-image-plan/SKILL.md`  
  Third manual skill: convert the Creative Brief into a Provider-Neutral Image Prompt Plan with Faithful, Amplified, and Minimal Prompt Variant Plans.
- Create: `skills/art-critic-review/SKILL.md`  
  Mandatory reviewer skill: strengthen the Creative Brief Document before Brief Approval.
- Create: `skills/critique-asset/SKILL.md`  
  Fourth manual skill: critique output against emotional intent.

Do not create `setup`, `hosts/`, `lib/`, provider adapters, or generated `SKILL.md.tmpl` files until the manual workflow works. `bin/` now contains dev-only Codex symlink install helpers, not production packaging.

## Task 1: Artistic Theory Document

**Files:**

- Create: `THEORY.md`
- Modify: `PROGRESS.md`

- [x] **Step 1: Create `THEORY.md`**

Write a concise theory document with these sections:

```markdown
# Artistic Theory

Artist Generation treats an artwork as layered evidence. Artist OS should not turn a Reference into a prompt directly. It should first identify what the Reference is, what it does formally, what it seems to feel like, what changes inside it, and what it means to the artist.

## Layer 1: Reference

The Reference is the user-provided material: text, image, video, audio, or mixed media.

Record:

- media type,
- title or working name,
- source path or reference,
- user context,
- rights notes,
- target transformation.

## Layer 2: Artist Meaning

Artist Meaning is the artist's stated interpretation of what a Reference means and what must survive transformation. Artist Meaning has final authority over agent interpretation.

## Layer 3: Formal Analysis

Formal Analysis names observable properties.

For text:

- voice,
- diction,
- imagery,
- pacing,
- point of view,
- metaphor,
- structure,
- conflict,
- reversal.

For images:

- color,
- value,
- line,
- shape,
- form,
- space,
- texture,
- contrast,
- balance,
- rhythm,
- movement,
- unity,
- variety.

For audio:

- tempo,
- dynamics,
- timbre,
- harmony,
- melody,
- rhythm,
- density,
- silence,
- repetition,
- tension and release.

For video:

- shot rhythm,
- motion,
- framing,
- camera distance,
- edit tempo,
- color grade,
- scene contrast,
- performance energy.

## Layer 4: Emotional Structure

Emotional Structure is the full emotional model of a Reference inside a Creative Brief. Record it with evidence and confidence.

Artist OS uses Core Tension Pairs instead of bipolar sliders. Each pole can be present independently, and the tension between the poles carries meaning.

The first Core Tension Pairs are:

- Attraction / Repulsion,
- Proximity / Distance,
- Order / Chaos,
- Stillness / Motion,
- Legibility / Opacity,
- Control / Surrender,
- Safety / Threat,
- Presence / Absence.

Each Tension Pair records:

- salience,
- pole A presence,
- pole B presence,
- tension intensity,
- evidence,
- optional artist note,
- translation notes.

Emotional Qualities capture freeform artist language that does not fit the core set.

## Layer 5: Visual Dynamics

Visual Dynamics names the formal forces that make a visual work active, coherent, tense, immersive, unstable, or memorable.

Keep Visual Dynamics separate from Emotional Structure. Emotional Structure describes the felt charge. Visual Dynamics describes the formal engine.

For text-to-image, Visual Dynamics describes the Target Visual Engine of the generated image. It does not pretend the text literally has visual properties. Each visual choice must trace back to Artist Meaning, Reference evidence, Emotional Structure, Beat Map, or Critical Heuristics.

The Core Visual Tension Pairs library is:

- Light / Dark,
- Saturated / Muted,
- Warm / Cool,
- Harmonious / Discordant,
- Dense / Sparse,
- Geometric / Organic,
- Sharp / Diffuse,
- Linear / Painterly,
- Textured / Smooth,
- Representational / Non-Representational,
- Flat / Deep,
- Balanced / Unbalanced,
- Centered / Decentered,
- Singular / Repetitive.

For the First Slice, record only the active 6 to 8 visual tensions with evidence and translation notes.

Use Monumental / Intimate only when scale, embodiment, installation, performance, or immersive environments matter.

## Layer 6: Beats And Tension Points

A Beat is the smallest meaningful change, contrast, turn, or pressure point in a Reference that carries Emotional Payload.

A Tension Point is meaningful contrast or unresolved pressure that carries emotion without requiring before/after change.

Each Beat records:

- before state,
- after state,
- what changed,
- value shift,
- emotional payload,
- source evidence,
- user confirmation.

## Layer 7: Meaning-Preserving Transformation

Meaning-Preserving Transformation changes medium or form while preserving Artist Meaning, selected Formal Analysis, Visual Dynamics, Emotional Structure, and relevant Beats or Tension Points.

Do not preserve surface form by default. Preserve emotional function. Change the medium-specific form only after naming what emotional role each source detail plays.

## First Slice

The First Slice is Text Reference to Image Prompt Plan. It is a Dry Run: no provider-backed generation calls.
```

- [x] **Step 2: Update `PROGRESS.md`**

Record that `THEORY.md` now holds the product-layer art model. Next step becomes `ARCHITECTURE.md`.

- [x] **Step 3: Verify**

Run:

```bash
sed -n '1,260p' THEORY.md
```

Expected: the theory supports text first but leaves room for images, audio, and video.

## Task 2: Product Architecture

**Files:**

- Create: `ARCHITECTURE.md`
- Modify: `PROGRESS.md`

- [x] **Step 1: Create `ARCHITECTURE.md`**

Write:

````markdown
# Architecture

Artist Generation is an agent operating system for transforming artistic intent across media.

## First Vertical Slice

The First Slice is Text Reference to Image Prompt Plan:

```text
Text source
  -> Source Record
  -> Meaning Interview
  -> Creative Brief Document
  -> Art Critic Review
  -> revised Creative Brief Document
  -> Brief Approval
  -> Creative Brief Record
  -> Provider-Neutral Image Prompt Plan
  -> critique checklist
  -> archive record
```

No paid generation call is required for the first slice.

## Data Flow

1. `artist-os-ingest-reference` creates a Source Record.
2. `artist-os-meaning-interview` captures Artist Meaning and transformation constraints.
3. `artist-os-text-to-image-plan` creates a draft Creative Brief Document.
4. `artist-os-art-critic-review` is mandatory. It strengthens the Creative Brief Document, resolves Open Questions, and increases Poetic Density without overriding Artist Meaning.
5. After Brief Approval, `artist-os-text-to-image-plan` creates the Creative Brief Record and one Provider-Neutral Prompt Plan with Faithful, Amplified, and Minimal Prompt Variant Plans.
6. `artist-os-critique-asset` compares outputs against the approved Creative Brief.
7. The archive records prompts, settings, outputs, and review notes.

## State Model

Use committed examples for test fixtures. Do not commit real user inputs or generated media until storage policy is decided.

Recommended later local state:

```text
~/.artistgen/projects/<slug>/
├── sources/
├── briefs/
├── outputs/
├── taste-memory.jsonl
└── sessions/
```

## Skill Boundary

Each skill has one job:

- `artist-os-ingest-reference`: records the source.
- `artist-os-meaning-interview`: captures Artist Meaning.
- `artist-os-text-to-image-plan`: transforms Artist Meaning into image direction.
- `artist-os-art-critic-review`: mandatory review that improves the Creative Brief Document before Brief Approval.
- `artist-os-critique-asset`: evaluates the Generated Work or Prompt Plan.

Skills may read earlier outputs, but they should not silently rewrite them. If a later skill discovers a contradiction, it records the contradiction and asks the user before changing the Creative Brief.

## Provider Boundary

Generation providers come later. The first implementation produces Provider-Neutral Prompt Plans. A later Provider Adapter may call an image model, but it must record provider, model, prompt, settings, seed if available, output path, and cost-bearing approval.
````

- [x] **Step 2: Fix nested fences**

When writing the file, replace inner triple-backtick examples with indented code blocks or four-backtick outer fences so Markdown renders correctly.

- [x] **Step 3: Update `PROGRESS.md`**

Record that `ARCHITECTURE.md` defines the first vertical slice and provider boundary. Next step becomes metadata schema.

- [x] **Step 4: Verify**

Run:

```bash
sed -n '1,260p' ARCHITECTURE.md
```

Expected: architecture names the first text-to-image slice and says generation providers come later.

## Task 3: Metadata Schema Documentation

**Files:**

- Create: `docs/metadata-schema.md`
- Create: `schemas/source-record.schema.json`
- Create: `schemas/creative-brief.schema.json`
- Modify: `PROGRESS.md`

- [x] **Step 1: Create `docs/metadata-schema.md`**

Write a human-readable schema guide with:

```markdown
# Metadata Schema

The manifest exists to preserve artistic intent and provenance. It should make every Generated Work traceable to a Reference, a Meaning Interview, a Creative Brief, a Beat Map, a Provider-Neutral Prompt Plan, and generation metadata.

## Source Record

Required fields:

- `source_id`
- `title`
- `media_type`
- `source_ref`
- `user_context`
- `rights_notes`
- `created_at`

## Creative Brief Record

Required fields:

- `source_id`
- `artist_meaning`
- `formal_observations`
- `core_tension_pairs`
- `emotional_qualities`
- `poetic_density_notes`
- `beats`
- `transformation_constraints`

## Output Record

Required fields once generation exists:

- `output_id`
- `source_id`
- `brief_id`
- `target_media_type`
- `provider`
- `model`
- `prompt`
- `settings`
- `output_ref`
- `review_status`
- `created_at`

## Rule

If a field affects artistic intent, reproducibility, rights, or review, record it.
```

- [x] **Step 2: Create `schemas/source-record.schema.json`**

Use this exact first schema:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://artist-generation.local/schemas/source-record.schema.json",
  "title": "SourceRecord",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "source_id",
    "title",
    "media_type",
    "source_ref",
    "user_context",
    "rights_notes",
    "created_at"
  ],
  "properties": {
    "source_id": { "type": "string", "pattern": "^src_[a-zA-Z0-9_-]+$" },
    "title": { "type": "string", "minLength": 1 },
    "media_type": { "type": "string", "enum": ["text", "image", "audio", "video", "mixed"] },
    "source_ref": { "type": "string", "minLength": 1 },
    "user_context": { "type": "string" },
    "rights_notes": { "type": "string" },
    "created_at": { "type": "string", "format": "date-time" }
  }
}
```

- [x] **Step 3: Create `schemas/creative-brief.schema.json`**

Use this exact first schema:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://artist-generation.local/schemas/creative-brief.schema.json",
  "title": "CreativeBriefRecord",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "brief_id",
    "source_id",
    "artist_meaning",
    "formal_observations",
    "visual_dynamics",
    "core_tension_pairs",
    "emotional_qualities",
    "poetic_density_notes",
    "beats",
    "transformation_constraints"
  ],
  "properties": {
    "brief_id": { "type": "string", "pattern": "^brief_[a-zA-Z0-9_-]+$" },
    "source_id": { "type": "string", "pattern": "^src_[a-zA-Z0-9_-]+$" },
    "artist_meaning": {
      "type": "object",
      "additionalProperties": false,
      "required": ["why_it_matters", "must_preserve", "may_transform"],
      "properties": {
        "why_it_matters": { "type": "string" },
        "must_preserve": { "type": "array", "items": { "type": "string" } },
        "may_transform": { "type": "array", "items": { "type": "string" } }
      }
    },
    "formal_observations": { "type": "array", "items": { "type": "string" } },
    "visual_dynamics": {
      "type": "object",
      "additionalProperties": false,
      "required": ["active_visual_tensions"],
      "properties": {
        "active_visual_tensions": {
          "type": "array",
          "minItems": 6,
          "maxItems": 8,
          "items": { "$ref": "#/$defs/visual_tension_pair_record" }
        },
        "conditional_visual_tensions": {
          "type": "array",
          "items": { "$ref": "#/$defs/visual_tension_pair_record" }
        }
      }
    },
    "core_tension_pairs": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "attraction_repulsion",
        "proximity_distance",
        "order_chaos",
        "stillness_motion",
        "legibility_opacity",
        "control_surrender",
        "safety_threat",
        "presence_absence"
      ],
      "properties": {
        "attraction_repulsion": { "$ref": "#/$defs/tension_pair_record" },
        "proximity_distance": { "$ref": "#/$defs/tension_pair_record" },
        "order_chaos": { "$ref": "#/$defs/tension_pair_record" },
        "stillness_motion": { "$ref": "#/$defs/tension_pair_record" },
        "legibility_opacity": { "$ref": "#/$defs/tension_pair_record" },
        "control_surrender": { "$ref": "#/$defs/tension_pair_record" },
        "safety_threat": { "$ref": "#/$defs/tension_pair_record" },
        "presence_absence": { "$ref": "#/$defs/tension_pair_record" }
      }
    },
    "emotional_qualities": { "type": "array", "items": { "type": "string" } },
    "poetic_density_notes": {
      "type": "object",
      "additionalProperties": false,
      "required": ["layered_meanings", "flattening_risks"],
      "properties": {
        "layered_meanings": {
          "type": "array",
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": ["detail", "meanings"],
            "properties": {
              "detail": { "type": "string" },
              "meanings": { "type": "array", "items": { "type": "string" } }
            }
          }
        },
        "flattening_risks": { "type": "array", "items": { "type": "string" } }
      }
    },
    "beats": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["before", "after", "value_shift", "emotional_payload", "evidence"],
        "properties": {
          "before": { "type": "string" },
          "after": { "type": "string" },
          "value_shift": { "type": "string" },
          "emotional_payload": { "type": "string" },
          "evidence": { "type": "string" }
        }
      }
    },
    "transformation_constraints": {
      "type": "object",
      "additionalProperties": false,
      "required": ["target_media_type", "preserve", "avoid"],
      "properties": {
        "target_media_type": { "type": "string", "enum": ["image", "audio", "video", "text"] },
        "preserve": { "type": "array", "items": { "type": "string" } },
        "avoid": { "type": "array", "items": { "type": "string" } }
      }
    }
  },
  "$defs": {
    "pole_record": {
      "type": "object",
      "additionalProperties": false,
      "required": ["presence"],
      "properties": {
        "presence": { "type": "number", "minimum": 0, "maximum": 1 }
      }
    },
    "tension_pair_record": {
      "type": "object",
      "additionalProperties": false,
      "required": ["salience", "poles", "tension_intensity", "evidence", "translation_notes"],
      "properties": {
        "salience": { "type": "string", "enum": ["not_salient", "low", "medium", "high"] },
        "poles": {
          "type": "object",
          "minProperties": 2,
          "maxProperties": 2,
          "additionalProperties": { "$ref": "#/$defs/pole_record" }
        },
        "tension_intensity": { "type": "number", "minimum": 0, "maximum": 1 },
        "evidence": { "type": "array", "items": { "type": "string" } },
        "artist_note": { "type": "string" },
        "translation_notes": { "type": "array", "items": { "type": "string" } }
      }
    },
    "visual_tension_pair_record": {
      "type": "object",
      "additionalProperties": false,
      "required": ["name", "poles", "tension_intensity", "evidence", "translation_notes"],
      "properties": {
        "name": {
          "type": "string",
          "enum": [
            "Light / Dark",
            "Saturated / Muted",
            "Warm / Cool",
            "Harmonious / Discordant",
            "Dense / Sparse",
            "Geometric / Organic",
            "Sharp / Diffuse",
            "Linear / Painterly",
            "Textured / Smooth",
            "Representational / Non-Representational",
            "Flat / Deep",
            "Balanced / Unbalanced",
            "Centered / Decentered",
            "Singular / Repetitive",
            "Monumental / Intimate"
          ]
        },
        "poles": {
          "type": "object",
          "minProperties": 2,
          "maxProperties": 2,
          "additionalProperties": { "$ref": "#/$defs/pole_record" }
        },
        "tension_intensity": { "type": "number", "minimum": 0, "maximum": 1 },
        "evidence": { "type": "array", "items": { "type": "string" } },
        "translation_notes": { "type": "array", "items": { "type": "string" } }
      }
    }
  }
}
```

- [x] **Step 4: Verify JSON syntax**

Run:

```bash
python3 -m json.tool schemas/source-record.schema.json >/dev/null
python3 -m json.tool schemas/creative-brief.schema.json >/dev/null
```

Expected: both commands exit with status 0.

- [x] **Step 5: Update `PROGRESS.md`**

Record that schema docs and first JSON schemas exist. Next step becomes examples.

## Task 4: Example Fixture

**Files:**

- Create: `examples/text-source.md`
- Create: `examples/text-creative-brief.example.json`
- Modify: `PROGRESS.md`

- [x] **Step 1: Create `examples/text-source.md`**

Use this source:

```markdown
# Text Source Example

The room was quiet except for the rain.
She folded the letter once, then again,
until the words became a square
small enough to hide in her palm.

At the door, she stopped.
Behind her, the lamp still burned.
Ahead, the street shone black and open.
```

- [x] **Step 2: Create `examples/text-creative-brief.example.json`**

Use this fixture:

```json
{
  "brief_id": "brief_text_rain_letter_001",
  "source_id": "src_text_rain_letter_001",
  "artist_meaning": {
    "why_it_matters": "This is about the moment before leaving something familiar.",
    "must_preserve": ["threshold", "private grief", "small decisive action"],
    "may_transform": ["literal letter", "rain", "lamp"]
  },
  "formal_observations": [
    "Quiet room contrasted with open street.",
    "The folded letter compresses language into a hidden object.",
    "The character pauses at a threshold.",
    "Light behind and dark street ahead create a before/after structure."
  ],
  "core_tension_pairs": {
    "attraction_repulsion": {
      "salience": "medium",
      "poles": {
        "attraction": { "presence": 0.45 },
        "repulsion": { "presence": 0.2 }
      },
      "tension_intensity": 0.45,
      "evidence": ["The rain, lamp, and folded letter create tactile softness around an act of concealment."],
      "artist_note": "The feeling should be tender, not grotesque.",
      "translation_notes": ["Use inviting light with a slight sense of emotional pressure."]
    },
    "proximity_distance": {
      "salience": "high",
      "poles": {
        "proximity": { "presence": 0.8 },
        "distance": { "presence": 0.7 }
      },
      "tension_intensity": 0.9,
      "evidence": ["The letter is hidden in the palm while the street waits outside."],
      "translation_notes": ["Frame the figure close to the viewer while placing the destination far away."]
    },
    "order_chaos": {
      "salience": "medium",
      "poles": {
        "order": { "presence": 0.75 },
        "chaos": { "presence": 0.25 }
      },
      "tension_intensity": 0.5,
      "evidence": ["The letter is folded into a square, while the rain and black street introduce uncertainty."],
      "translation_notes": ["Use clean geometry interrupted by weather texture."]
    },
    "stillness_motion": {
      "salience": "high",
      "poles": {
        "stillness": { "presence": 0.85 },
        "motion": { "presence": 0.4 }
      },
      "tension_intensity": 0.7,
      "evidence": ["The character stops at the door, but the open street implies imminent movement."],
      "translation_notes": ["Hold the figure still while the environment suggests movement."]
    },
    "legibility_opacity": {
      "salience": "high",
      "poles": {
        "legibility": { "presence": 0.35 },
        "opacity": { "presence": 0.8 }
      },
      "tension_intensity": 0.75,
      "evidence": ["The words become a hidden square, removing their readable meaning."],
      "translation_notes": ["Avoid readable text; use concealed marks or folded forms."]
    },
    "control_surrender": {
      "salience": "medium",
      "poles": {
        "control": { "presence": 0.7 },
        "surrender": { "presence": 0.45 }
      },
      "tension_intensity": 0.65,
      "evidence": ["The character folds the letter deliberately but faces an unknown street."],
      "translation_notes": ["Show a deliberate gesture at the edge of an uncontrollable environment."]
    },
    "safety_threat": {
      "salience": "high",
      "poles": {
        "safety": { "presence": 0.65 },
        "threat": { "presence": 0.55 }
      },
      "tension_intensity": 0.8,
      "evidence": ["The lamp remains behind while the street is black and open."],
      "translation_notes": ["Contrast warm interior light with a dark exterior threshold."]
    },
    "presence_absence": {
      "salience": "high",
      "poles": {
        "presence": { "presence": 0.55 },
        "absence": { "presence": 0.85 }
      },
      "tension_intensity": 0.85,
      "evidence": ["The letter remains physically present but its words are hidden."],
      "translation_notes": ["Represent a missing relationship through an object held close."]
    }
  },
  "emotional_qualities": ["private grief", "quiet resolve", "threshold feeling"],
  "poetic_density_notes": {
    "layered_meanings": [
      {
        "detail": "folded letter",
        "meanings": ["hidden language", "private grief", "controlled departure"]
      },
      {
        "detail": "lamp behind the character",
        "meanings": ["safety", "memory", "life being left behind"]
      },
      {
        "detail": "black open street",
        "meanings": ["threat", "possibility", "unknown future"]
      }
    ],
    "flattening_risks": [
      "Do not reduce the scene to a simple breakup image.",
      "Do not make the departure purely triumphant or purely tragic."
    ]
  },
  "beats": [
    {
      "before": "The character remains inside with the letter and the lamp.",
      "after": "The character stops at the door and faces the open street.",
      "value_shift": "attachment -> departure",
      "emotional_payload": "grief turning into resolve",
      "evidence": "Behind her, the lamp still burned. Ahead, the street shone black and open."
    }
  ],
  "transformation_constraints": {
    "target_media_type": "image",
    "preserve": ["threshold", "private grief", "choice before departure"],
    "avoid": ["literal readable text", "melodrama", "bright optimism"]
  }
}
```

- [x] **Step 3: Verify JSON syntax**

Run:

```bash
python3 -m json.tool examples/text-creative-brief.example.json >/dev/null
```

Expected: command exits with status 0.

- [x] **Step 4: Update `PROGRESS.md`**

Record the example fixture. Next step becomes manual skills.

## Task 5: Manual Skills For The First Slice

**Files:**

- Create: `skills/ingest-reference/SKILL.md`
- Create: `skills/meaning-interview/SKILL.md`
- Create: `skills/text-to-image-plan/SKILL.md`
- Create: `skills/art-critic-review/SKILL.md`
- Modify: `PROGRESS.md`

- [x] **Step 1: Create `skills/ingest-reference/SKILL.md`**

The skill must say:

```markdown
---
name: artist-os-ingest-reference
description: Create a Source Record for text, image, audio, video, or mixed References without generating new media.
---

# Ingest Reference

You are the intake archivist for Artist Generation.

## Hard Gate

Do not generate new media. Do not analyze Artist Meaning yet. Only create a Source Record.

## Inputs

Ask for or infer:

- title,
- media type,
- source reference,
- user context,
- rights notes.

## Output

Return a Source Record matching `schemas/source-record.schema.json`.

## Required Closing

After returning the Source Record, tell the user the next step is `artist-os-meaning-interview`.
```

- [x] **Step 2: Create `skills/meaning-interview/SKILL.md`**

The skill must say:

```markdown
---
name: artist-os-meaning-interview
description: Interview the artist about what a source means before formal or emotional analysis hardens into assumptions.
---

# Meaning Interview

You are the artist's meaning interviewer.

## Hard Gate

Do not generate media. Do not override the user's interpretation with your own.

## Questions

Ask these one at a time:

1. Why does this source matter to you?
2. What feeling must survive if the source changes medium?
3. What should not be copied literally?
4. Which details are sacred?
5. Which parts can change aggressively?
6. What should the new artifact make someone feel?

## Output

Return:

- `why_it_matters`,
- `must_preserve`,
- `may_transform`,
- `avoid`,
- `target_media_type`,
- `success_criteria`.

If the user's answers contradict the agent's likely interpretation, record the contradiction and let the user's meaning win.
```

- [x] **Step 3: Create `skills/text-to-image-plan/SKILL.md`**

The skill must say:

```markdown
---
name: artist-os-text-to-image-plan
description: Convert a Text Reference and Meaning Interview into a Creative Brief, Beat Map, and Provider-Neutral Image Prompt Plan.
---

# Text To Image Plan

You are the translation director for Artist OS.

## Hard Gate

Do not call an image generation provider. Produce a dry-run prompt plan only.

## Inputs

Read:

- Text Reference,
- Source Record,
- Meaning Interview output.

## Process

1. Identify formal observations from the text.
2. Map all eight Core Tension Pairs with pole presences, tension intensity, evidence, and translation notes.
3. Select 6 to 8 Active Visual Tensions from the Core Visual Tension Pairs library to define the Target Visual Engine, with evidence and translation notes.
4. Add Monumental / Intimate only when scale, embodiment, installation, performance, or immersive environments matter.
5. Capture Emotional Qualities that do not fit the core set.
6. Identify Beats, Tension Points, and value shifts.
7. Define what the image should preserve.
8. Define what the image should avoid.
9. Produce a draft Creative Brief Document.
10. Tell the user the next step is `artist-os-art-critic-review`.
11. Do not produce the Creative Brief Record or Provider-Neutral Prompt Plan until Art Critic Review and Brief Approval are complete.

## Output

Return:

- Creative Brief Document,
- Beat Map,
- Open Questions and Interpretive Confidence notes for Art Critic Review.

Do not produce the Creative Brief Record until the Creative Brief Document has passed Art Critic Review and received Brief Approval.

Every prompt choice must trace back to Artist Meaning, Reference evidence, a Core Tension Pair, an Emotional Quality, a Beat, or a Tension Point.
For visual output, prompt choices must also trace back to Visual Dynamics when they concern light, color, composition, space, texture, rhythm, focus, or visual form.

After Art Critic Review and Brief Approval, produce one Provider-Neutral Image Prompt Plan with exactly three Prompt Variant Plans:

- Faithful: closest to the approved Creative Brief.
- Amplified: pushes the strongest tension, Poetic Density, and Target Visual Engine without inventing new Artist Meaning. It may add Derived Symbols only when they are marked and traced to Artist Meaning, a Core Tension Pair, an Active Visual Tension, a Beat or Tension Point, or a Poetic Density note.
- Minimal: strips the image down to the essential emotional and visual engine without becoming underspecified.

Derived Symbols are review-visible inside the full Provider-Neutral Prompt Plan. They do not require a separate approval gate in the First Slice.

Each Prompt Variant Plan must include:

- variant type,
- prompt text,
- negative constraints,
- derived symbols, if any,
- traceability notes back to the approved Creative Brief,
- critique checklist.
```

- [x] **Step 4: Create `skills/art-critic-review/SKILL.md`**

The skill must say:

```markdown
---
name: artist-os-art-critic-review
description: Mandatory review that strengthens a Creative Brief Document before Brief Approval by resolving weak interpretations, increasing Poetic Density, and making the direction decisive.
---

# Art Critic Review

You are the art critic reviewer for Artist OS.

## Hard Gate

Do not override Artist Meaning. Do not produce the Creative Brief Record. Do not produce the Provider-Neutral Prompt Plan.

## Inputs

Read:

- Text Reference,
- Source Record,
- Meaning Interview output,
- draft Creative Brief Document,
- Open Questions and Interpretive Confidence notes.

## Process

1. Identify weak, thin, or under-supported interpretations.
2. Resolve Open Questions using the strongest available Reference evidence and Artist Meaning.
3. Apply Critical Heuristics in order:
   - preserve Artist Meaning,
   - stay anchored to Reference evidence,
   - deepen salient Core Tension Pairs,
   - strengthen Active Visual Tensions,
   - increase Poetic Density,
   - use medium-specific translation principles,
   - avoid literalism, preserve contradiction, make form carry meaning, and prefer layered specificity over generic mood.
4. Increase Poetic Density by finding layered meanings in details already present.
5. Strengthen Core Tension Pair translation notes.
6. Remove final ambiguity from the brief.
7. Produce a revised Creative Brief Document.
8. Ask for Brief Approval.

If the artist gives no additional feedback, deepen and emphasize the strongest existing findings. Do not invent a new Artist Meaning.

## Output

Return:

- revised Creative Brief Document,
- resolved Open Questions,
- Poetic Density improvements,
- Brief Approval request.
```

- [x] **Step 5: Update `PROGRESS.md`**

Record that the first four manual skills exist. Next step becomes critique skill.

## Task 6: Critique Skill

**Files:**

- Create: `skills/critique-asset/SKILL.md`
- Modify: `PROGRESS.md`

- [x] **Step 1: Create `skills/critique-asset/SKILL.md`**

Write:

```markdown
---
name: artist-os-critique-asset
description: Compare a Generated Work or Prompt Plan against the Creative Brief instead of judging surface similarity alone.
---

# Critique Asset

You are the critic for Artist OS.

## Hard Gate

Do not judge success by whether the output copies the source. Judge whether it preserves the intended emotional function.

## Inputs

Read:

- Source Record,
- Meaning Interview,
- Creative Brief,
- Beat Map,
- Provider-Neutral Prompt Plan,
- Generated Work or output description.

## Review Criteria

Evaluate:

- preserved Artist Meaning,
- preserved Core Tension Pairs,
- preserved Emotional Qualities,
- preserved Visual Dynamics,
- preserved Poetic Density,
- preserved Beat, Tension Point, or value shift,
- drift from Reference evidence,
- unwanted literal copying,
- flattening risks,
- missing provenance,
- recommended revision.

## Output

Return:

- `matched`,
- `drifted`,
- `revision_prompt`,
- `accept_reject_revise`,
- `taste_memory_note`.
```

- [x] **Step 2: Update `PROGRESS.md`**

Record that the first critique loop exists. Next step becomes dry-run walkthrough.

## Task 7: Product Agent Rules

**Files:**

- Create: `AGENTS.md`
- Modify: `PROGRESS.md`

- [x] **Step 1: Create `AGENTS.md` with product-layer rules**

Write an `AGENTS.md` that says:

```markdown
# Artist Generation Agent Rules

This file defines product-layer operating rules for agents building and running Artist OS.

## Documentation Layers

- Build-process docs guide repository construction: `README.md`, `PROGRESS.md`, `docs/IMPLEMENTATION_PLAN.md`, and `docs/gstack-repo-map.md`.
- Product docs define Artist OS: `CONTEXT.md`, `AGENTS.md`, `ARCHITECTURE.md`, `THEORY.md`, `docs/metadata-schema.md`, and `skills/`.

Move stable product rules into product docs. Keep progress notes focused on current status and next steps.

## Product Invariant

Every Generated Work must trace back to:

- Artist Meaning,
- evidence from the Reference,
- the Creative Brief,
- the Beat or Tension Point,
- the Transformation Plan,
- the Provider-Neutral Prompt Plan,
- and the Output Record.

## Operating Rules

- Do not make provider-backed generation calls without explicit user approval.
- Do not commit user-provided media, Generated Works, secrets, or API keys.
- Treat Emotional Structure as a hypothesis until the artist confirms it.
- Artist Meaning overrides agent interpretation.
- Preserve provenance before optimizing for speed.
- Use Dry Runs before invoking media generation providers.

## First Slice

The First Slice is Text Reference to Image Prompt Plan:

1. Ingest a Text Reference.
2. Run a Meaning Interview.
3. Produce a Source Record.
4. Produce a draft Creative Brief Document.
5. Run Art Critic Review.
6. Get Brief Approval.
7. Produce a Creative Brief Record.
8. Produce a Provider-Neutral Image Prompt Plan.
9. Produce critique criteria.
```

- [x] **Step 2: Update `PROGRESS.md`**

Record that `AGENTS.md` exists as the product-layer operating document for Artist OS.

- [x] **Step 3: Verify**

Run:

```bash
sed -n '1,220p' AGENTS.md
sed -n '1,220p' PROGRESS.md
```

Expected: `AGENTS.md` uses the terms from `CONTEXT.md` and states the provenance invariant.

## Task 8: Dry-Run Walkthrough

**Files:**

- Modify: `PROGRESS.md`
- Optionally modify: any skill whose instructions fail during the dry run.

- [x] **Step 1: Run the first workflow manually**

Use:

```bash
sed -n '1,120p' examples/text-source.md
sed -n '1,260p' examples/text-creative-brief.example.json
```

Then simulate the workflow:

1. `artist-os-ingest-reference` creates a Source Record for `examples/text-source.md`.
2. `artist-os-meaning-interview` uses the sample Artist Meaning from the example Creative Brief.
3. `artist-os-text-to-image-plan` produces a draft Creative Brief Document.
4. `artist-os-art-critic-review` revises the Creative Brief Document and asks for Brief Approval.
5. After Brief Approval, `artist-os-text-to-image-plan` produces the Creative Brief Record and one Provider-Neutral Prompt Plan containing Faithful, Amplified, and Minimal Prompt Variant Plans.
6. `artist-os-critique-asset` critiques the plan against the approved Creative Brief.

- [x] **Step 2: Record problems**

If any skill asks for unavailable data, repeats another skill's job, or fails to preserve provenance, edit that skill immediately.

- [x] **Step 3: Update `PROGRESS.md`**

Record:

- what worked,
- what failed,
- which skill should be improved next,
- whether the repo is ready for real image generation adapter planning.

## Task 9: Decide Whether To Add Tooling

**Files:**

- Modify: `docs/IMPLEMENTATION_PLAN.md`
- Modify: `PROGRESS.md`

- [ ] **Step 1: Review the dry-run result**

Only add tooling if the manual workflow repeats mechanical work.

Good reasons to add tooling:

- JSON validation is being done repeatedly.
- source IDs need deterministic generation.
- examples need schema validation in one command.
- prompt plans need a stable archive format.

Bad reasons to add tooling:

- copying GStack structure before this workflow needs it.
- adding host adapters before any skill works.
- adding provider APIs before dry-run prompt quality is good.

- [ ] **Step 2: Choose the next branch**

Pick exactly one:

- Add validation helper and tests.
- Add first image provider adapter.
- Harden Codex dev install into user-facing setup.
- Add image ingestion.

- [ ] **Step 3: Update `PROGRESS.md`**

Record the chosen next branch and why.

## Completion Criteria

This plan is complete when:

- Product docs exist: `AGENTS.md`, `THEORY.md`, `ARCHITECTURE.md`, `docs/metadata-schema.md`.
- First schemas exist and parse as JSON.
- Example text source and example Creative Brief Record exist.
- Manual skills exist for ingest, meaning interview, text-to-image planning, and critique.
- A dry-run walkthrough produces a traceable image prompt plan without paid generation.
- `PROGRESS.md` tells the next agent exactly what to do next.

## Not In Scope Yet

- Real image generation calls.
- Audio or video ingestion.
- Binary media storage.
- User-facing Codex setup script beyond the current dev symlink install helpers.
- Host adapters.
- Generated `SKILL.md.tmpl` pipeline.
- Taste memory persistence.
- Browser or preview server.

## Execution Note

This repo says not to commit unless the user asks. Treat each task as a checkpoint and run `git status --short` after it. Commit only if the user explicitly asks.
