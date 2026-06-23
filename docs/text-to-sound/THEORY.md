# Text To Sound Theory

Text-to-sound is a meaning-preserving transformation from a Text Reference into a platform-neutral Sound Prompt Plan with final platform renderings, such as Suno Custom Mode for the first sound version. It reuses the shared Artist OS layers: Reference, Artist Meaning, Formal Analysis, Emotional Structure, Beat Plan, Poetic Density, Transformation Brief, Sound Medium Plan, Brief Approval, Prompt Variant Plans, Review Records, and provenance.

This layer defines the sound-specific translation model. It should not duplicate the shared Artist OS theory unless the sound workflow needs a medium-specific rule.

## Target Sound Work

Text-to-sound is broader than text-to-music. Record the intended sound work type before locking the brief:

- `song`
- `instrumental_track`
- `ambient_soundscape`
- `cinematic_score`
- `spoken_word_bed`
- `ritual_audio`
- `sound_design_piece`
- `sonic_logo`

The work type changes the questions Artist OS asks. A song needs Vocal / Lyric Policy. An instrumental score needs instrumentation, arrangement, and motif choices. A soundscape may need location, texture, and spatial movement more than genre.

## Sonic Concept Direction

Sonic Concept Direction replaces Symbology Direction for sound. It defines the core sound-world or sonic metaphor that carries Artist Meaning.

It should answer:

- What is the sound-world?
- What should the listener feel physically or emotionally?
- What sonic image, motif, gesture, or atmosphere carries the meaning?
- What must not be literalized?
- What source details become musical or sound-design functions?

## Genre And Production Direction

Genre Direction is the musical equivalent of Style Direction. It must remain subordinate to Artist Meaning, Emotional Structure, Beat Plan, and Sonic Dynamics.

Represent genre as one Primary Genre plus bounded modifiers:

- `primary_genre`
- `subgenres`
- `production_style`
- `style_modifiers`
- `reference_artists_or_works`, optional
- `avoid_genres`
- `genre_conflicts`
- `confirmation_status`

Do not create equal-weight genre piles. If the artist asks for a hybrid, synthesize one Primary Genre and no more than four modifiers.

## Tempo And Groove Direction

Tempo is both a technical setting and an emotional decision. Record exact tempo only when useful; otherwise record a range and felt tempo.

Recommended fields:

- `bpm`
- `bpm_range`
- `tempo_feel`
- `tempo_stability`
- `tempo_changes`
- `meter`
- `groove_feel`
- `swing_or_shuffle`
- `rhythmic_density`

Tempo choices must trace back to Artist Meaning, Reference evidence, Emotional Structure, Beat Plan, or Sonic Dynamics.

## Vocal And Lyric Policy

Text-to-sound must ask whether the work should have lyrics before the final brief and prompt plan are locked.

The artist should choose one of:

- `instrumental`: no lyrics or intelligible words.
- `source_text_verbatim`: use the Text Reference as lyrics, preserving the artist's words.
- `source_text_adapted`: adapt the Text Reference into singable lyrics while preserving Artist Meaning.
- `new_lyrics`: write new lyrics from the approved Creative Brief.
- `spoken_word`: use spoken or chanted language rather than sung lyrics.
- `phonetic_vocals`: use non-lexical syllables, mouth sounds, or wordless voice.

If the artist chooses `source_text_adapted` or `new_lyrics`, Artist OS must draft lyrics before Brief Approval or as a required revision before final Prompt Plan locking. The drafted lyrics become reviewable project material and must preserve:

- Artist Meaning,
- must-preserve details,
- Emotional Structure,
- Beat Plan,
- Poetic Density,
- constraints around forbidden changes,
- rights notes for source text.

Do not invent lyrics when the artist has not approved lyrics. Do not use private or copyrighted source text as lyrics beyond the artist's stated rights and intended use.

When lyrics are requested, write them against the Arrangement Plan. Lyrics should not be drafted as loose poem text unless the artist explicitly wants unstructured lyrics. Each lyric section should have a structural function, a tension role, and traceability back to Artist Meaning, Beat Plan, and Poetic Density Notes.

Recommended lyric section fields:

- section name,
- section function,
- tension role,
- bars or phrase count when known,
- lyric text,
- hook or refrain line when present,
- preserved source details,
- transformed source details,
- delivery notes,
- traceability notes.

## Sonic Dynamics

Sonic Dynamics names the formal forces that make a sound work active, coherent, tense, immersive, unstable, memorable, or emotionally precise. It is separate from Emotional Structure.

Core Sonic Tension Pairs:

- Consonant / Dissonant
- Stable / Unstable
- Resolved / Unresolved
- Expected / Surprising
- Regular / Syncopated
- Rhythmic / Floating
- Sparse / Dense
- Soft / Loud
- Slow / Fast
- Smooth / Rough
- Clean / Distorted
- Bright / Dark
- High / Low
- Dry / Reverberant
- Near / Far
- Intimate / Expansive
- Human / Mechanical

For a sound prompt plan, record the active 6 to 8 Sonic Tension Pairs with evidence and translation notes. Do not score all pairs by default.

## Arrangement And Form

Sound unfolds over time, so the Beat Plan should translate into an Arrangement Plan.

Think about song structure at three nested levels:

```text
Song
  -> Sections
    -> Phrases
      -> Bars / beats
```

Definitions:

- Beat: the basic pulse.
- Bar / Measure: a group of beats, usually four beats in common 4/4 song forms.
- Phrase: a musical sentence, often 4 or 8 bars.
- Section: a larger formal unit such as intro, verse, chorus, bridge, breakdown, outro, instrumental, or silence.

Record:

- target duration or duration range,
- meter,
- estimated BPM,
- estimated bars,
- sections,
- emotional function of each section,
- tension role of each section,
- motif or hook behavior,
- dynamic arc,
- entry and removal of instruments,
- silence, rests, pauses, or dropouts,
- ending behavior.

Common section vocabulary:

- Intro,
- Verse,
- Pre-Chorus,
- Chorus,
- Post-Chorus / Refrain,
- Verse 2,
- Bridge / Breakdown,
- Final Chorus,
- Outro / Tag.

Useful section-function vocabulary:

- Invitation,
- Grounding,
- Build,
- Release,
- Development,
- Contrast,
- Rupture,
- Return,
- Closure,
- Residue.

The section labels are less important than the tension movement. A useful arrangement plan does not only say `Intro -> Verse -> Chorus -> Bridge -> Outro`; it says how the song moves through `Invitation -> Grounding -> Build -> Release -> Development -> Contrast -> Return -> Closure`.

### Default 2-Minute Song Template

When the artist wants a compact song and has not specified structure, use this as a starting point, then adapt it to genre, tempo, lyric density, and Artist Meaning:

```text
duration: 120 seconds
meter: 4/4
estimated_bpm: 120
estimated_bars: 60

sections:
  - Intro, 0:00-0:08, 4 bars, establish sound world, invitation
  - Verse 1, 0:08-0:24, 8 bars, introduce image/story, grounding
  - Pre-Chorus, 0:24-0:32, 4 bars, build tension, intensification
  - Chorus 1, 0:32-0:48, 8 bars, first payoff/hook, first release
  - Verse 2, 0:48-1:04, 8 bars, develop and vary, development
  - Pre-Chorus 2, 1:04-1:12, 4 bars, stronger build, intensification
  - Chorus 2, 1:12-1:28, 8 bars, fuller payoff, expanded release
  - Bridge / Breakdown, 1:28-1:44, 8 bars, contrast or rupture, perspective shift
  - Final Chorus, 1:44-1:56, 6 bars, transformed return, final release
  - Outro / Tag, 1:56-2:00, 2 bars, closure or unresolved exit, residue
```

For modern short-form songs that need immediate attention, use a compressed hook-first form. For folk, singer-songwriter, ceremonial, or lyric-forward work, give the verses more room and reduce pop compression.

### Section Tension Mapping

Each section should record:

- structural function,
- active Emotional Tension Pairs,
- active Sonic Tension Pairs,
- transformation notes.

Section-level tension mapping lets lyrics, instrumentation, arrangement, and production move together. For example, a Bridge / Breakdown may strip the arrangement down, destabilize harmony, expose the voice, and shift the lyric from external scene to interior admission.

For multi-Beat references, recommend whether the work should be a single track, a movement-based track, a suite, or multiple alternate sound directions. Do not create multiple final sound prompt plans without artist approval.

## Prompt Variants

The text-to-sound flow keeps Faithful, Amplified, and Minimal variants.

- Faithful: closest to the approved Creative Brief and selected sound direction.
- Amplified: pushes the strongest tension, sound-world, and poetic density while preserving Artist Meaning.
- Minimal: strips the work to its essential sonic engine.

Each variant must name concrete sonic differentiators, such as tempo, instrumentation, texture, rhythm, harmony, vocal treatment, arrangement density, silence, dynamics, mix perspective, or production finish.

For the first sound version, each Prompt Variant Plan must also produce `platform_output_intent`: title, instrumental intent, lyrics mode and text, style prompt intent, and exclusions. A platform renderer then turns that neutral intent into provider-native fields such as Suno's Style of Music and Exclude. Platform renderers may change wording and field placement, but they may not change Artist Meaning, Vocal / Lyric Policy, approved lyrics, Arrangement Plan, Sonic Dynamics, or traceability.

Suno Platform Rendering should make the final Custom Mode output practical and production-aware: compact musical style language, section-aware lyric tags when helpful, vocal/lyric policy alignment, controlled endings, concrete exclusions, and readiness checks. Those mechanics belong to the renderer, not to the upstream sound theory.

## Dry Run Boundary

The text-to-sound slice is dry-run first. Drafting lyrics, briefs, prompt plans, critique checklists, and Review Records is allowed. Calling a sound, music, or voice generation provider requires explicit artist approval.
