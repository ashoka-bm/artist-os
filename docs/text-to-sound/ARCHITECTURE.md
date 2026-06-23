# Text To Sound Architecture

The Text-to-Sound Slice is a complete dry-run Artist OS workflow from Text Reference to a platform-neutral Sound Prompt Plan with a final platform rendering, such as Suno Custom Mode.

```text
Text Reference
  -> Source Record
  -> Meaning Interview
  -> Transformation Brief
  -> Beat Plan
  -> Story Critic Review, when required
  -> Sound Medium Plan
  -> Draft Sound Creative Brief Document
  -> Sound Work Type
  -> Sonic Concept Direction
  -> Genre / Production Direction
  -> Tempo / Groove Direction
  -> Vocal / Lyric Policy
  -> preliminary Arrangement / Form skeleton, when lyrics are required
  -> Lyrics Draft, when required
  -> Arrangement / Form Direction
  -> Sonic Dynamics
  -> Sequence Recommendation
  -> Music / Sound Critic Review
  -> revised Sound Creative Brief Document
  -> Brief Approval
  -> Sound Creative Brief Record
  -> Sound Prompt Plan
  -> Platform Rendering, Suno Custom Mode for the first implementation
  -> Prompt Critic Review
  -> optional Generation Approval Gate
  -> Output Record, when an artifact exists
  -> Output Critic Review
  -> Output Acceptance Gate
  -> Workspace Library persistence
```

No provider-backed generation call is required for this slice.

## Reused Shared Stages

Reuse the existing Artist OS stages where they are medium-neutral:

1. Ingest the Text Reference and create a Source Record.
2. Run a Meaning Interview.
3. Preserve Artist Meaning as final authority.
4. Create the shared Transformation Brief.
5. Create the shared Beat Plan and Poetic Density Notes.
6. Translate the Beat Plan into a Sound Medium Plan.
7. Produce an artist-readable Sound Creative Brief Document before the structured Sound Creative Brief Record.
8. Run Music / Sound Critic Review as a bounded sub-agent before Brief Approval.
9. Create structured records only after Brief Approval. Sound Creative Brief Records validate against `schemas/sound-creative-brief.schema.json`.
10. Produce Faithful, Amplified, and Minimal Prompt Variant Plans.
11. Preserve traceability from every prompt choice back to the approved brief, Beat Plan, and Sound Medium Plan.
12. Produce a platform-neutral Sound Prompt Plan, then render platform-specific fields at the Platform Rendering Boundary.

## Sound-Specific Gates

The Text-to-Sound Slice has sound-specific gates. Do not move past a gate until it is complete or the artist explicitly says to proceed unconfirmed.

### Sound Work Type Gate

Choose the concrete sound work type before sonic concept details harden: song, instrumental track, ambient soundscape, cinematic score, spoken-word bed, ritual audio, sound design piece, or sonic logo. Default to `song` only when the artist asked for music, a song, or lyrics; otherwise ask or recommend one clear direction.

### Sonic Concept Gate

Ask what sonic concept or sound-world should carry the Artist Meaning. If unresolved, show concise options rather than forcing a default.

Examples:

- intimate voice and room tone
- sparse piano with static
- nocturnal electronic pulse
- ritual percussion and drone
- ambient field-recording texture
- cinematic chamber score

### Genre / Production Gate

Ask whether the artist has a specific genre or production vision. If not, offer concise candidate directions.

Record one Primary Genre or production mode plus bounded modifiers. Surface Genre/Sonic Conflicts when the selected genre weakens the required Sonic Dynamics.

### Tempo / Groove Gate

Ask whether the artist has a tempo, BPM range, or felt motion in mind. If not, recommend one from the Beat Plan and Emotional Structure.

Record BPM or range, meter, groove feel, tempo stability, rhythmic density, and tempo-change rationale.

### Vocal / Lyric Gate

Before final brief approval and before prompt locking, ask:

> Should this sound work have lyrics or intelligible words?

Valid directions:

- no lyrics / instrumental,
- use the source text verbatim,
- adapt the source text into lyrics,
- write new lyrics from the approved brief,
- spoken word,
- phonetic or wordless vocals.

If the artist chooses adapted or new lyrics, define a preliminary Arrangement / Form skeleton before drafting lyrics, then create a Lyrics Draft before final prompt locking. The Lyrics Draft must be reviewed as part of the Creative Brief Document or as a required revision to it. Do not silently generate lyrics inside the final prompt.

The Lyrics Draft should include:

- title or working title,
- section labels when useful,
- each section's function and tension role,
- lyrics,
- hook or refrain lines when present,
- notes on what source details were preserved,
- notes on what was transformed,
- delivery notes,
- rights notes,
- traceability to Artist Meaning, Beats, and Poetic Density Notes.

### Arrangement / Form Gate

Define the time structure: intro, verse, chorus, bridge, movement, drop, silence, outro, or other sections appropriate to the sound work type.

Use the nested model `Song -> Sections -> Phrases -> Bars / beats`. A good Arrangement Plan should include duration, meter, estimated BPM, estimated bars, sections, section functions, and section tension roles.

If the artist wants a compact song and has not specified structure, use the default 2-minute structure as a starting point:

```text
Intro -> Verse 1 -> Pre-Chorus -> Chorus 1 -> Verse 2 -> Pre-Chorus 2 -> Chorus 2 -> Bridge / Breakdown -> Final Chorus -> Outro / Tag
```

Map that structure to a tension curve:

```text
Invitation -> Grounding -> Build -> Release -> Development -> Stronger Build -> Expanded Release -> Contrast / Rupture -> Return -> Closure / Residue
```

Adapt the template for the medium. Modern short-form songs may start with a hook; folk, singer-songwriter, ceremonial, and lyric-forward works may need longer verses and a less compressed chorus cycle.

When the Beat Plan has several significant turns, recommend whether the work should be a single continuous track, a multi-section track, a suite, or separate alternate sound directions. Do not create multiple final sound prompt plans until the artist approves the sequence recommendation.

## Sound Prompt Plan Contract

A Sound Prompt Plan validates against `schemas/sound-prompt-plan.schema.json`. It is platform-neutral until `platform_renderings[]` maps one selected Prompt Variant Plan into a provider-native output shape.

A Sound Prompt Plan should include:

- `prompt_plan_id`
- `brief_id`
- `source_id`
- `artist_meaning_id`
- `transformation_brief_id`
- `beat_plan_id`
- `sound_medium_plan_id`
- `target_media_type: "sound"`
- `sound_work_type`
- `target_platform: "platform_neutral"`
- `description`
- `style_prompt_summary`
- `sonic_concept_summary`
- `genre_direction_summary`
- `tempo_groove_summary`
- `vocal_lyric_policy`
- `lyrics`, when required and approved
- `arrangement_plan`
- `song_structure`, including sections, bars, phrase notes, and section tension roles when applicable
- `instrumentation_plan`
- `sonic_dynamics_summary`
- `prompt_variants`
- `platform_renderings`
- `traceability_summary`
- `critique_checklist`

Each Prompt Variant Plan should include:

- `variant_type`: `faithful`, `amplified`, or `minimal`
- `variant_test_axis_label`
- `sonic_differentiators`
- `prompt_text`
- `platform_output_intent`
- `negative_constraints`
- `derived_sonic_elements`
- `traceability_notes`
- `critique_checklist`

## Platform Rendering Boundary

Platform Rendering is the final generator-specific translation step. It may translate approved neutral prompt intent into provider-native fields, syntax, controls, upload guidance, and readiness checks. It may not change Artist Meaning, Vocal / Lyric Policy, approved lyrics, the Arrangement Plan, Sonic Dynamics, or traceability.

Each `platform_renderings[]` entry should include:

- `platform`
- `renderer`
- `source_variant_type`
- `rendering_status`
- `outputs`
- `platform_constraints`
- `readiness_check`
- `traceability_summary`

For the first implementation, use `platform: "suno"` and `renderer: "suno_custom_mode"`. The required Suno-facing fields live under `outputs.suno_custom_mode_outputs`:

- `mode: "custom"`
- `title`
- `instrumental`: true when no lyrics or intelligible words are wanted.
- `lyrics.mode`: `none`, `custom`, or `generate_in_suno`.
- `lyrics.text`: required when using custom lyrics.
- `style_of_music`: the primary Suno style field.
- `exclude`: unwanted instruments, genres, vocal qualities, moods, or structures.
- `advanced_options.duration_target`: artist-facing length target or model-length note.
- `advanced_options.model`: optional, left blank when the artist has not chosen a Suno model.
- `advanced_options.inspo_or_persona`: optional, left blank unless the artist has a rights-safe Suno Inspo or Persona.

For `vocal_lyric_policy.lyrics_mode = "phonetic_vocals"`, keep `instrumental: false` and set `lyrics.mode: "generate_in_suno"`. The `lyrics.text` instruction should ask Suno for non-lexical voice such as breath, hums, vowels, or syllables, and `exclude` must block intelligible lyrics, spoken words, and clear language. Do not paste source words or newly written lyrics for this mode.

`style_of_music` should be a dense but readable comma-separated Suno prompt. It should synthesize Artist OS metrics into musical language:

- genre and subgenre,
- tempo and meter,
- groove and rhythm,
- instrumentation,
- vocal direction,
- mood and energy,
- arrangement movement,
- production finish,
- dynamic contrast,
- section behavior,
- key negative intent when important.

Do not include traceability notes, schema language, pair scores, or Artist OS internal field names inside `style_of_music`. Those remain in the structured record.

Use `skills/artist-os/references/platforms/suno-output.md` for the Suno Platform Rendering rules. Other generators should add sibling renderer references and emit their own `platform_renderings[]` entries without changing the upstream Sound Medium Plan or Sound Prompt Plan contract.

## Critique Criteria

Critique sound prompt plans against:

- Artist Meaning,
- evidence from the Text Reference,
- Emotional Structure,
- Sonic Dynamics,
- Beat Plan,
- Poetic Density,
- Genre / Production Direction,
- Tempo / Groove Direction,
- Vocal / Lyric Policy,
- Lyrics Draft when present,
- Arrangement Plan,
- transformation constraints.

The best-sounding option is not acceptable if it loses Artist Meaning.
