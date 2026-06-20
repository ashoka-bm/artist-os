# Mixed-Media Journey

The Mixed-Media Journey coordinates multiple output journeys from one approved Beat Plan. It is for projects where image, video, sound, text, or other media should share meaning and structure while expressing different parts of the work.

## Best Fit

Use the Mixed-Media Journey when the final work should include:

- an image plus music,
- a video plus soundtrack,
- a poem plus image series,
- a visual album concept,
- a campaign or release package,
- a gallery sequence with sound,
- several coordinated assets from the same Reference.

## Route

```text
Approved Beat Plan with Project-Level Workflow Scale Routing
  -> Mixed-Media Scope Gate
  -> Medium Selection Gate
  -> Role Assignment Gate
  -> Cross-Media Continuity Gate
  -> Medium-Specific Journeys with Medium-Level Workflow Scale Routing
  -> Mixed-Media Critic Review
  -> Prompt Critic Review
  -> Prompt Lock Gate
  -> Generation Approval Gate
  -> Output Critic Review
  -> Output Acceptance Gate
```

## Gates

- Mixed-Media Scope Gate: what is the package or experience?
- Medium Selection Gate: which media are included?
- Role Assignment Gate: which beats belong to which medium?
- Cross-Media Continuity Gate: what must stay consistent across media, and what may diverge?
- Production Order Gate: which output should be created first as calibration?
- Generation Approval Gate: each provider-backed generation call still requires explicit approval.

## Reviews

- Story Critic Review happens before this journey as a bounded sub-agent review.
- Beat Reviewer sub-agent is mandatory when beats are assigned across multiple media.
- Medium-specific critic reviews happen inside each selected output journey as bounded sub-agent reviews.
- Mixed-Media Critic Review checks whether the media work together instead of duplicating or contradicting each other accidentally as a bounded sub-agent review.
- Prompt Critic Review checks the complete output package for traceability, consistency, sequencing, and generation risk as a bounded sub-agent review.
- Output Critic Review checks the generated package against Artist Meaning, Beat Plan, medium plans, and cross-media continuity decisions as a bounded sub-agent review.

## Coordination Rules

One Beat Plan can produce multiple Medium Plans, but each medium should have a distinct job.

Examples:

- image holds the symbolic threshold while music carries the emotional arc,
- video stages the sequence while text supplies voice or narration,
- image series shows transformation roles while sound supplies continuity,
- text names the hidden logic while visuals preserve ambiguity.

Mixed-media work should not multiply outputs just because it can. Add a medium only when it carries something the others cannot.
