# Suno Platform Rendering

Use this only after the approved Sound Prompt Plan exists. The Suno renderer is a final platform-specific translation step: it maps the neutral Sound Prompt Plan into Suno Custom Mode fields without changing the approved sound-planning decisions.

Paths resolve from `$ARTIST_OS_ROOT` — the repo root in a checkout, the bundle root in a Codex install. If a referenced file is missing, run `bin/artist-os-paths doctor`. This file is loaded by `skills/artist-os/references/text-to-suno-plan.md` when a `platform_renderings[]` entry uses `platform: "suno"` and `renderer: "suno_custom_mode"`.

## Inputs

Consume:

- the approved Sound Creative Brief Record,
- the Sound Prompt Plan,
- the selected Prompt Variant Plan,
- `platform_output_intent`,
- Vocal / Lyric Policy,
- Lyrics Draft when present,
- Arrangement Plan and song sections,
- Sonic Dynamics,
- production direction,
- negative constraints,
- traceability notes.

Do not read private media, provider accounts, or uploaded audio unless the artist explicitly approves that provider-facing action.

## Output Location

Write Suno output only inside:

```json
{
  "platform_renderings": [
    {
      "platform": "suno",
      "renderer": "suno_custom_mode",
      "source_variant_type": "faithful",
      "rendering_status": "ready",
      "outputs": {
        "suno_custom_mode_outputs": {}
      },
      "platform_constraints": [],
      "readiness_check": {},
      "traceability_summary": []
    }
  ]
}
```

Do not add top-level Suno fields to the Sound Prompt Plan. Do not replace neutral `platform_output_intent` with Suno-only field names.

## Required Custom Mode Fields

Render:

- `mode: "custom"`,
- `title`,
- `instrumental`,
- `lyrics.mode`,
- `lyrics.text`,
- `style_of_music`,
- `exclude`,
- `advanced_options.duration_target`,
- `advanced_options.model`,
- `advanced_options.inspo_or_persona`,
- `suno_notes`.

Leave `advanced_options.model` or `advanced_options.inspo_or_persona` blank unless the artist chose a specific Suno model, Inspo, or Persona. Do not invent a persona, reference artist, or copyrighted soundalike target.

## Rendering Rules

Translate neutral intent into Suno-facing language:

- `platform_output_intent.style_prompt` becomes `style_of_music`.
- `platform_output_intent.exclude` and `production_direction.negative_constraints` become `exclude`.
- `platform_output_intent.title` becomes `title`.
- `platform_output_intent.instrumental` becomes `instrumental`.
- `platform_output_intent.lyrics` becomes `lyrics`.
- `arrangement_plan`, `song_structure.sections[]`, and Sonic Dynamics become compact musical direction inside `style_of_music` and section tags.

`style_of_music` should be dense, readable, comma-separated musical language. Include genre, tempo or felt tempo, meter when useful, groove, instrumentation, vocal posture, dynamic arc, production finish, section behavior, and key negative intent when important. Do not include traceability notes, schema names, field names, pair scores, or internal Artist OS rationale.

## Lyrics And Section Tags

When `lyrics.mode` is `custom`, render lyrics for singing:

- short lines,
- breathable punctuation,
- simple repeatable hooks when the approved plan calls for them,
- section tags that carry production direction.

Prefer house pipe-stacked section tags for Suno-facing lyrics when lyrics are present:

```text
[Section | emotion/energy | vocal style | key instruments | dynamics | space/effects | production behavior]
```

This is an Artist OS rendering convention, not upstream Artist Meaning. Use it only when it helps Suno execution. Do not force pipe tags into non-Suno renderings.

## Vocal Modes

For `lyrics_mode = "instrumental"`:

- set `instrumental: true`,
- set `lyrics.mode: "none"`,
- keep `lyrics.text` empty,
- add exclusions for unwanted voice when needed.

For lyric-bearing modes:

- set `instrumental: false`,
- use `lyrics.mode: "custom"` when approved lyrics exist,
- keep approved lyrics intact except for spacing, section tags, and punctuation needed for singability.

For `lyrics_mode = "phonetic_vocals"`:

- set `instrumental: false`,
- set `lyrics.mode: "generate_in_suno"`,
- use `lyrics.text` to request non-lexical voice such as breath, hums, vowels, or syllables,
- exclude intelligible lyrics, spoken words, and clear language.

## Ending Control

Carry ending behavior into the rendering. Use concrete ending instructions such as slow fade, hard stop, unresolved decay, stripped outro, repeated hook, or instrumental decay. Add exclusions for failure modes that would violate the plan, such as abrupt ending, extra spoken outro, or new lyrics after the final chorus.

## Optional Audio Reference Notes

If the approved plan needs exact chords, melody, groove, rare instrumentation, vocal reference, loop, or sample behavior, add an `suno_notes` item recommending an audio reference or Cover workflow. This is guidance only. Do not upload audio, use Cover, or call Suno without explicit artist approval for that provider action.

## Readiness Check

Set `readiness_check.status` to:

- `ready` when all required Suno fields are present and aligned,
- `needs_revision` when the rendering is usable but weak,
- `blocked` when it violates Vocal / Lyric Policy, misses required lyrics, lacks ending control, or drifts from Artist Meaning.

Include checks for:

- Custom Mode field completeness,
- Vocal / Lyric Policy alignment,
- section-level contrast,
- lyric singability when lyrics are present,
- ending control,
- concrete exclusions,
- instrumental no-voice constraints when instrumental,
- traceability to the selected Prompt Variant Plan and Sound Prompt Plan.

Prompt Critic must block a Suno rendering if it changes approved meaning, invents unapproved lyrics, leaves lyric mode ambiguous, uses generic section tags when the arrangement needs section-specific production direction, omits ending control, or lets instrumental tracks invite voice-like material.
