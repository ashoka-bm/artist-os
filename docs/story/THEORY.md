# Story Theory

Artist OS treats story as the shared transformation layer between Artist Meaning and medium-specific planning. Story does not require plot, characters, dialogue, or fiction. Story means an ordered emotional, symbolic, formal, or experiential progression that can be compressed into one moment or expanded across many moments.

The story layer answers one question:

```text
What changes, holds, intensifies, breaks, returns, or remains unresolved?
```

Every medium consumes that answer differently. A single image can hold one story beat. A video can unfold a sequence of beats. A song can translate beats into sections, tension movement, lyrics, motif, and arrangement. A text output can rewrite the beats as prose, poetry, dialogue, or narrative structure.

## Story Layer Position

The shared transformation path is:

```text
Reference
  -> Source Record
  -> Artist Meaning
  -> Transformation Brief
  -> Story / Beat Plan
  -> Medium Plan
  -> Prompt Plan
  -> Output Record
  -> Output Critic Review
  -> Output Acceptance Gate
```

The current image and Suno workflows now use a first-class Beat Plan before medium planning. Embedded Beat summaries remain in medium-specific briefs only as transitional compatibility fields.

## Story Is Not Only Narrative

Use story broadly.

- An image is a single compressed beat, threshold, contradiction, or emotional pressure.
- A triptych is three staged beats, often before / threshold / after.
- An image series is a beat sequence with distinct image roles.
- A video is a timed beat sequence with motion, shot logic, pacing, and transitions.
- A song is a beat sequence translated into arrangement, tension map, lyric policy, and sonic development.
- A soundscape can be a changing field of pressure, proximity, density, and release.
- A text rewrite can preserve, invert, fragment, expand, or revoice the Beat Plan.

When Artist OS says "story," it may mean literal plot, emotional arc, symbolic progression, ritual sequence, conceptual turn, spatial journey, or formal transformation.

## Beat

A Beat is the smallest meaningful unit of transformation or pressure that can carry Artist Meaning into a medium.

A Beat may be:

- a change from one state to another,
- a contradiction held in one moment,
- a threshold or decision point,
- a reveal or concealment,
- an intensification,
- a collapse,
- a return,
- an aftermath,
- an unresolved pressure.

Each Beat should preserve traceability to Artist Meaning, Reference evidence, Emotional Structure, and transformation constraints. A Beat should not be added only because a medium needs more content.

Artist OS uses `docs/writing/references/writing-beats.SKILL.md` as the high-authority method for journey-shaped beat creation. When the Story Journey is uncertain, create candidate starting beats, let the artist choose, define only that beat, then offer 2-3 candidate next beats. Do not write or lock later beats ahead of the artist's choice unless the artist explicitly asks for an agent-recommended full outline.

## Tension Point

A Tension Point is meaningful unresolved pressure. It may not have a before / after movement, but it still carries story force.

Examples:

- attraction and repulsion existing together,
- presence felt through absence,
- safety contaminated by threat,
- stillness that feels ready to move,
- opacity that must remain opaque.

A single image often works best when it compresses several Tension Points into one decisive visual moment.

## Story Modes

Story Mode describes how many beats the output needs and what kind of progression they form.

- `single_beat`: one compressed moment, image, text fragment, sonic gesture, or short video beat.
- `beat_pair`: a contrast, before / after, call / response, conceal / reveal, or rupture / consequence.
- `triptych`: three staged beats, commonly before / threshold / after.
- `sequence`: several linked beats with distinct roles.
- `scene`: a contained unit with setting, action, pressure, and turn.
- `arc`: a full emotional or symbolic journey across sections, shots, images, movements, or chapters.
- `world`: a reusable symbolic, visual, sonic, or narrative system for many future works.

Do not equate longer with better. Choose the shortest Story Mode that preserves Artist Meaning.

## Beat Roles

Beat Roles describe what a beat does inside the larger shape. They are more important than plot labels.

Useful Beat Roles:

- invitation,
- grounding,
- encounter,
- threshold,
- build,
- rupture,
- reveal,
- concealment,
- reversal,
- surrender,
- transformation,
- consequence,
- return,
- closure,
- residue,
- unresolved echo.

These roles can map to image roles, video shots, song sections, audio movements, or rewritten text passages.

## Story Gate

The Story Gate confirms the output's story shape before medium-specific translation hardens.

Ask:

```text
Should this become one compressed beat, a short sequence, a scene, a longer arc, or a reusable world?
```

If the artist already named an output, adapt the gate:

- image: "Should this image hold one compressed beat, or should it become a series?"
- video: "Is this a single moment, a scene, a sequence, or a larger arc?"
- music/audio: "Should this be one track, a movement-based piece, a suite, or alternate sound directions?"
- text: "Should this become a fragment, a scene, a full piece, or a larger structure?"

The Story Gate is complete only when the artist selects, combines, revises, rejects, or explicitly allows an unconfirmed Story Mode to proceed.

## Story Critic Review

Story Critic Review checks whether the Beat Plan preserves Artist Meaning before medium decisions take over.

The Story Critic reviews:

- whether Artist Meaning remains dominant,
- whether each Beat has evidence or artist confirmation,
- whether the Beat Roles form a coherent shape,
- whether tension movement is legible without being over-explained,
- whether unresolved pressure is preserved when it matters,
- whether the selected Story Mode is too short, too long, or correctly scaled,
- whether any beat was added only to satisfy a medium format,
- whether the plan leaves avoidable ambiguity before medium translation.

Story Critic Review must include a separate Beat Reviewer sub-agent pass based on `docs/writing/references/writing-beats.SKILL.md` when the output has more than one beat, or when a single beat risks doing too many jobs.

The Story Critic can revise the Beat Plan, but cannot override Artist Meaning. If a revision changes the intended meaning or Story Mode, return to the artist for Story Approval.

## Story Approval

Story Approval happens before medium-specific prompt plans are locked.

Approval means:

- the Story Mode is accepted,
- the Beat Roles are accepted,
- the required emotional or symbolic movement is accepted,
- known open questions are resolved or marked safe to proceed unconfirmed.

After Story Approval, medium-specific branches may translate the Beat Plan into images, video, music/audio, text, or mixed-media outputs.

## Design Invariant

Every output is one or more approved story beats translated into a medium, reviewed at the story layer, reviewed at the medium layer, and traceable back to Artist Meaning.
