# Story Theory

Artist OS treats story as the shared transformation layer between Artist Meaning and medium-specific planning. Story does not require plot, characters, dialogue, or fiction. Story means an ordered emotional, symbolic, formal, or experiential progression that can be compressed into one moment or expanded across many moments.

The story layer answers one question:

```text
What changes, holds, intensifies, breaks, returns, or remains unresolved?
```

It must also answer what the audience is meant to feel. A Beat is not complete when it only names an event, object, or idea; it must name the intended feeling or emotional pressure that the medium will express.

Every medium consumes that answer differently. A single image can hold one story beat. A video can unfold a sequence of beats. A song can translate beats into sections, tension movement, lyrics, motif, and arrangement. A text output can rewrite the beats as prose, poetry, dialogue, or narrative structure.

Artist OS follows common production usage: a **Beat** is a meaningful story moment, not an act-sized summary. Larger containers are **Story Movements**. A Story Movement may be an act, sequence passage, mini-arc, or restoration sequence that groups several Beats. Do not store a Story Movement as one Beat unless it truly performs one indivisible emotional or causal move.

## Story Layer Position

The shared transformation path is:

```text
Reference
  -> Source Record
  -> Artist Meaning
  -> Transformation Brief
  -> Story / Beat Plan
  -> Long-Work Stewardship, when cumulative
  -> Medium Plan
  -> Prompt Plan
  -> Output Record
  -> Output Critic Review
  -> Output Acceptance Gate
```

The current image, Suno, video, and text workflows use a first-class Beat Plan before medium planning. Medium-specific briefs carry `beat_plan_id`; they do not embed duplicate Beat summaries.

Long-Work Stewardship exists only for Cumulative Work: long text, image series, songs or sound movements, video sequences, or mixed-media sequences where later parts depend on earlier parts. It protects continuity, readiness, checkpoints, emotional-arc expression, and drift across parts. It is not needed for a non-sequential portfolio, store collection, or curator batch whose pieces are related but do not build one after another.

## Story Is Not Only Narrative

Use story broadly.

- An image is a single compressed beat, threshold, contradiction, or emotional pressure.
- A three-part sequence is three staged Beats only when each part is one meaningful move; otherwise it is three Story Movements that contain smaller Beats.
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

A Beat should do one job. If a candidate Beat includes several independent jobs, such as setup plus threat plus protection plus aftermath, it is a Story Movement or scene group and must be split into smaller Beats before Story Approval. This keeps Artist OS aligned with storyboard, screenwriting, and beat-board practice, where each meaningful story moment can be named, reviewed, and translated into a panel, shot, section, or cue.

Each Beat should preserve traceability to Artist Meaning, Reference evidence, Emotional Structure, and transformation constraints. A Beat should not be added only because a medium needs more content.

Each Beat should express a feeling before it expresses a fact. The factual content can be simple, but the mental link should be immediate: a symbol, action, contrast, or sensory condition that makes the intended feeling legible.

Each Beat must include an Expectation Turn: the expected direction, actual result, surprise function, and emotional counterpoint. Even when one emotion builds across multiple Beats, each Beat needs some unexpected result, withholding, reversal, complication, or changed pressure.

Each Beat should also record a tension profile: the active emotional tensions, their 0-1 intensity, and what emotional job each tension performs. A Beat Plan should include minimum tension criteria so reviewers can tell whether the planned contrast is strong enough for the intended feeling.

## Story Movement

A Story Movement is a larger grouping of Beats. Use Story Movements when artists, storyboards, treatments, or structure libraries need act-level or sequence-level labels without inflating Beat size.

A Story Movement may be:

- an act,
- a scene passage,
- a mini-arc,
- a montage cluster,
- a trial sequence,
- a return sequence,
- a cinematic ending passage.

Story Movements can help reviewers see architecture, but they are not the story authority by themselves. The Beat Plan remains enforceable at the Beat level: every Beat still needs one move, an Intended Feeling, an Expectation Turn, and a tension profile.

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

Story Mode describes how many Beats or Story Movements the output needs and what kind of progression they form.

- `single_beat`: one compressed moment, image, text fragment, sonic gesture, or short video beat.
- `beat_pair`: two smallest meaningful Beats, often contrast, before / after, call / response, conceal / reveal, or rupture / consequence.
- `three_part_sequence`: three staged Story Movements or three Beats when each part is truly one move.
- `sequence`: several linked Beats with distinct roles.
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
- whether each Beat is the smallest meaningful move rather than a glued-together Story Movement,
- whether each Beat names an intended feeling and not only factual content,
- whether each Beat has a real Expectation Turn,
- whether the Beat Roles form a coherent shape,
- whether tension movement is legible without being over-explained,
- whether the Beat Plan meets its minimum tension criteria,
- whether Key Emotional Movements identify the major shifts that should survive compression or expansion,
- whether supporting Beats build toward, complicate, or delay a Key Emotional Movement rather than padding the arc,
- whether Story Movements, when present, group Beats without replacing Beat-level review,
- whether adjacent Beats shift tension profiles enough to produce felt movement,
- whether unresolved pressure is preserved when it matters,
- whether the selected Story Mode is too short, too long, or correctly scaled,
- whether any Beat was added only to satisfy a medium format,
- whether any Story Movement was mislabeled as one Beat,
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

If the approved Story Mode creates Cumulative Work, create a foundation Long-Work Stewardship Record before full medium expansion. At this point the record can have no medium-specific parts yet; enrich it after the Medium Plan maps beats into images, sections, chapters, scenes, or movements. The record should keep part-to-part continuity and readiness visible, but it must not become the authority for meaning or story. If a stewardship review proposes changing the meaning, Story Mode, Beat movement, or emotional arc, return to Story Approval.

## Design Invariant

Every output is one or more approved story beats translated into a medium, reviewed at the story layer, reviewed at the medium layer, and traceable back to Artist Meaning.
