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
Approved Beat Plan with Project-Level Workflow Scale Routing
  -> Long-Work Stewardship Record, when Workflow Scale Routing activates it
  -> Sound Work Type Gate
  -> Sonic Concept Gate
  -> Genre / Production Gate
  -> Tempo / Groove Gate
  -> Vocal / Lyric Gate
  -> Arrangement / Form Gate
  -> Sound Medium Plan with Medium-Level Workflow Scale Routing
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
- Workflow Scale Routing: should this stay one structured sound work, or does it need sequence, Long-Work, or full long-form support?
- Sequence Approval Gate: required before multiple tracks, movements, or alternate sound directions are created.

## Reviews

- Story Critic Review happens before this journey as a bounded sub-agent review.
- Beat Reviewer sub-agent is mandatory for multi-section, sequence, or lyric-bearing sound plans.
- Sound Critic Review checks Sonic Concept, Genre / Production, Tempo / Groove, Vocal / Lyric Policy, Arrangement / Form, Sonic Dynamics, lyrics when present, and platform readiness as a bounded sub-agent review.
- Long-Work Reviewer checks readiness, checkpoints, cumulative drift, continuity rules, motif/voice continuity, and proposed continuity updates when cumulative or full long-form sound support is active.
- Prompt Critic Review checks provider-neutral prompt quality, Suno readiness when applicable, variant distinction, traceability, and missing sonic constraints as a bounded sub-agent review.
- Output Critic Review checks generated or drafted audio against Artist Meaning, Beat Plan, Sound Medium Plan, and Prompt Plan as a bounded sub-agent review.

## Current Implementation

The current text-to-Suno slice implements this route through the Suno Sound Prompt Plan, Output Record, Output Critic Review, and Output Acceptance Gate contracts. The Sound Medium Plan records Medium-Level Workflow Scale Routing. The Sound Creative Brief carries `beat_plan_id`; the referenced Beat Plan is authoritative.

When Workflow Scale Routing activates Long-Work Stewardship for sound, create a foundation Long-Work Stewardship Record after Story Approval and enrich it after the Sound Medium Plan maps Beats to tracks, movements, sections, or sequence parts. The Sound Medium Plan owns Sonic Dynamics, sequence planning, arrangement/form, vocal/lyric policy, and sound-role details; the stewardship record references sound part ids and tracks cumulative readiness, checkpoints, part status, continuity rules, and drift.
