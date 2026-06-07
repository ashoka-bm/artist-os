# Sound Journey

The Sound Journey translates an approved Beat Plan into music, audio, or sound design. The current implemented target is a Suno Sound Prompt Plan, but the journey is broader than Suno.

## Best Fit

Use the Sound Journey when the final work should be:

- a song,
- an instrumental track,
- an ambient soundscape,
- a cinematic score,
- a spoken-word bed,
- ritual audio,
- a sound design piece,
- a sonic logo.

## Route

```text
Approved Beat Plan
  -> Sound Work Type Gate
  -> Sonic Concept Gate
  -> Genre / Production Gate
  -> Tempo / Groove Gate
  -> Vocal / Lyric Gate
  -> Arrangement / Form Gate
  -> Sound Critic Review
  -> Sound Prompt Plan
  -> Prompt Critic Review
  -> Prompt Lock Gate
  -> Generation Approval Gate
  -> Output Critic Review
  -> Output Acceptance Gate
```

## Gates

- Sound Work Type Gate: song, instrumental, soundscape, score, spoken-word bed, ritual audio, sound design, or sonic logo?
- Sonic Concept Gate: what sound-world carries Artist Meaning?
- Genre / Production Gate: what musical or production language should be used?
- Tempo / Groove Gate: what pace, meter, and felt motion serve the Beat Plan?
- Vocal / Lyric Gate: instrumental, verbatim source text, adapted source text, new lyrics, spoken word, phonetic vocals, or wordless voice?
- Arrangement / Form Gate: how do beats become sections, phrases, silence, build, release, rupture, return, and closure?
- Sequence Approval Gate: required before multiple tracks, movements, or alternate sound directions are created.

## Reviews

- Story Critic Review happens before this journey as a bounded sub-agent review.
- Beat Reviewer sub-agent is mandatory for multi-section, sequence, or lyric-bearing sound plans.
- Sound Critic Review checks Sonic Concept, Genre / Production, Tempo / Groove, Vocal / Lyric Policy, Arrangement / Form, Sonic Dynamics, lyrics when present, and platform readiness as a bounded sub-agent review.
- Prompt Critic Review checks provider-neutral prompt quality, Suno readiness when applicable, variant distinction, traceability, and missing sonic constraints as a bounded sub-agent review.
- Output Critic Review checks generated or drafted audio against Artist Meaning, Beat Plan, Sound Plan, and Prompt Plan as a bounded sub-agent review.

## Current Implementation

The current text-to-Suno slice implements this route through the Suno Sound Prompt Plan, Output Record, Output Critic Review, and Output Acceptance Gate contracts. Embedded `beats` remain in the Sound Creative Brief only as transitional medium-local summaries; `beat_plan_id` is authoritative.
