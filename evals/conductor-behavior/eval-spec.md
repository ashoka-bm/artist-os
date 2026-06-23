# Conductor behavior eval

Goal: verify that trimming `skills/artist-os/SKILL.md` preserves the conductor's
*behavior* — phase order, hard-gate enforcement, internal mode delegation, medium
quirks, and start-condition handling. Each test produces an ordered TRACE; we
grade the trace against a checklist. Baseline (current conductor) defines the
"correct" behavior the trimmed version must reproduce.

## Test prompts

The full-flow prompts include tiny synthetic References so the conductor can
trace beyond Source Record without inventing user material. Keep the
missing-Reference prompt as a separate start-condition guard.

- **T1 (image, full flow):** "Here's a poem:
  'My mother's hands fold light into bread.
  Flour gathers in every line.
  When she rests them, the room keeps working.'
  I want to turn it into visual art. Go on autopilot — assume I approve the
  recommended option at every gate and approve generation — and take it all the
  way."
- **T2 (suno, full flow):** "Here is my journal entry:
  'At 3:17 the apartment hums like a wire. I count the ceiling cracks and wait
  for morning to forgive me. Sleep stays in the next room, breathing without me.'
  Turn it into a Suno track. Autopilot, I approve recommended choices and
  generation; take it to the end."
- **T3 (review start-condition):** "I already generated an image for my 'saltmarsh'
  project and have the brief and prompt plan. Can you review the image against it?"
- **T4 (text, full flow):** "Here is my journal entry:
  'I packed the blue mug last because it made the apartment look inhabited. The
  hallway smelled like rain and old paint. I did not cry until I turned in the
  keys and heard the lock answer for me.'
  Turn it into a short personal essay. Autopilot — I approve the recommended
  choice at every gate, and approve drafting and the editorial passes; take it
  all the way."
- **T5 (missing Reference start-condition):** "Here's a poem about my mother's
  hands. I want to turn it into visual art. Go on autopilot — assume I approve
  the recommended option at every gate and approve generation — and take it all
  the way."
- **T6 (video storyboard, full flow):** "Here is my journal entry:
  'The hallway light stayed on after everyone left. The door was open just
  enough to make the dark room look like it was waiting for me. I stood there
  until the floor stopped creaking.'
  Turn it into a short film storyboard with scenes, shot list, camera angles,
  motion, audio posture, and storyboard frame prompts. Autopilot — assume I
  approve the recommended choice at every gate, but do not generate any actual
  images or finished video."

## Checklist (assertions per trace)

### T1 — image
1. Phases in order: Source Record → Artist Meaning → Transformation Brief → Beat Plan → Beat Review (if multi-beat) → Image Medium Plan → Draft Creative Brief → Art Critic Review → Brief Approval → Final Records → (optional Branch Set) → Prompt Plan Critique → Generation Approval → Output Record → Output Critic Review → Output Acceptance.
2. Delegates through internal modes: `skills/artist-os/references/ingest-reference.md`, `skills/artist-os/references/meaning-interview.md`, `skills/artist-os/references/text-to-image-plan.md`, `skills/artist-os/references/writing-method-review.md`, `skills/artist-os/references/art-critic-review.md`, and `skills/artist-os/references/critique-asset.md`.
3. Hard gates enforced: provider-approval (per call), brief-approval before Creative Brief Record, series approval before multiple series prompts, Output Record before acceptance, persist each phase.
4. Visual gates run in order Symbology → Style during Image Medium Plan; Presentation Mode decided in the Symbology gate.
5. IMAGE QUIRK: visual gates run in order Symbology → Style during Image Medium Plan; later visual variation is handled by Prompt Variant Strategy, not another visual gate.

### T2 — suno
1. Phases in order: Source Record → Artist Meaning → Transformation Brief → Beat Plan → Beat Review (if multi-section/lyric) → Sound Medium Plan → Draft Sound Creative Brief → Music/Sound Critic Review → Brief Approval → Final Records → Prompt Plan Critique → Generation Approval → Output Record → Output Critic Review → Output Acceptance.
2. Delegates through internal modes: `skills/artist-os/references/ingest-reference.md`, `skills/artist-os/references/meaning-interview.md`, `skills/artist-os/references/text-to-suno-plan.md`, `skills/artist-os/references/art-critic-review.md` in sound critic mode, and `skills/artist-os/references/critique-asset.md`.
3. SUNO QUIRK A: Vocal/Lyric resolved before locking the brief (lyrics/phonetic/instrumental chosen).
4. SUNO QUIRK B: NO image-style Prompt Branch Set in the Suno flow.
5. Hard gates: provider-approval, brief-approval before Sound Creative Brief Record, sequence approval before multiple sequence plans, Output Record before acceptance, persist each phase.

### T3 — review start-condition
1. Does NOT restart the full creation flow.
2. Identifies/asks for governing project, brief, prompt plan, medium plan, beat plan, Artist Meaning, Source Record.
3. Creates an Output Record (against output-record schema) if none exists.
4. Jumps to Output Critic Review then Output Acceptance Gate.
5. Output Critic runs as a bounded sub-agent through `skills/artist-os/references/critique-asset.md` and emits a Review Record.

### T4 — text
1. Orientation resolves the output as Text, fixes one Primary Text Form (essay), and resolves the source-wording question (preserve / adapt / create new) before planning hardens.
2. Phases in order: Source Record → Artist Meaning → Transformation Brief → Beat Plan → Beat Review (if multi-beat) → Text Medium Plan → Draft Text Creative Brief → Writing Critic Review → Brief Approval → Final Records → Prompt Plan Critique → Draft Generation Approval → Output Record (draft) → Output Critic Review → Output Acceptance.
3. Delegates through internal modes: `skills/artist-os/references/ingest-reference.md`, `skills/artist-os/references/meaning-interview.md`, `skills/artist-os/references/text-journey.md`, `skills/artist-os/references/writing-method-review.md` for beat review and Writing Critic Review, `skills/artist-os/references/critique-asset.md`, `skills/artist-os/references/clear-writing-pass.md`, and `skills/artist-os/references/human-voice-pass.md`.
4. Step 6 works the text gates in the medium plan: Writing Method, Text Form, Voice / Point of View, Structure, Fidelity / Transformation, Publication / Use. Medium Plan validates against text-medium-plan; Final Records validate against text-creative-brief and text-generation-plan.
5. TEXT QUIRK A: the Critic Review uses `skills/artist-os/references/writing-method-review.md` in Writing Critic / Shape Reviewer mode, NOT `skills/artist-os/references/art-critic-review.md`.
6. TEXT QUIRK B: Draft Generation Approval is a hard gate even though no paid provider call is made — local drafting is still gated.
7. TEXT QUIRK C: the written Output Artifact is drafted in a fresh-context sub-agent from a Text Draft Packet; that sub-agent does NOT run the editorial passes during first drafting.
8. TEXT QUIRK D: the main agent runs a conformance review before any editorial pass; if structure, section jobs, Intended Feeling, source-wording policy, or Text Generation Plan constraints fail, it corrects the draft before polishing (structure wins over prose).
9. TEXT QUIRK E: editorial passes run Clear Writing Pass before Human Voice Pass by default, each as a separate bounded fresh-context sub-agent, and each concrete rewrite gets a new Output Record with `origin.origin_type = "agent_rewritten"` and `previous_output_record_id`.
10. Hard gates: brief-approval before Text Creative Brief Record and Text Generation Plan, Draft Generation Approval before drafting, Output Record before acceptance, persist each phase.

### T5 — missing Reference
1. Routes to the requested medium from the user's intent without re-asking the top-level medium question.
2. Does NOT invent the absent poem, journal entry, letter, or other Reference content.
3. Stops before Source Record ingestion and asks for the missing text Reference.
4. Does not run Artist Meaning, Transformation Brief, Beat Plan, Medium Plan, or downstream review before the Reference exists.
5. Explains that autopilot approval cannot bypass missing required source material.

### T6 — video storyboard
1. Routes storyboard/video/film language to `skills/artist-os/references/video-journey.md`.
2. Produces storyboard-ready Video Medium Plan / handoff only; does NOT claim finished video generation.
3. Uses the shared visual gate order Symbology → Style before video-specific gates.
4. Works video gates: Video Format, Scene / Sequence, Shot Logic, Motion / Pacing / Transition, and Audio Posture.
5. Requires explicit provider-backed Generation Approval before generated storyboard stills or any rendered video provider call.
6. Requires normal Output Records for generated or imported storyboard stills before review or acceptance.
7. Does NOT create a Video Prompt Plan in v0.

## Scoring
Each assertion: pass / partial / fail with evidence quote from the trace.
Baseline establishes the target; trimmed must match the baseline's pass set.

## Subagent prompt template

Spawn one general-purpose subagent per test prompt with this instruction
(substitute the scenario and the trace-specific sections). Run baseline and
trimmed with identical prompts; only the SKILL.md on disk differs between runs.

> You are tracing the behavior of the Artist OS conductor skill, exactly as
> written. Read and follow ONLY the skill file at
> `<repo>/skills/artist-os/SKILL.md` (plus any files IT explicitly tells you to
> read). Do not improvise behavior that isn't in the skill.
>
> Scenario (the user's message): "<T1 / T2 / T3 / T4 / T5 / T6 prompt>"
>
> Produce a precise ORDERED TRACE of what the conductor does. Do NOT call any
> generator and do NOT write project files. The trace is a numbered list; each
> step states: (a) phase name, (b) internal mode file it loads, (c) any hard
> gate enforced and the approval it requires, (d) any record/schema produced,
> (e) where it would pause for artist input.
>
> Then add the trace-specific sections — T1: "VISUAL GATES" (gate order;
> Presentation Mode and Prompt Variant Strategy timing) + "HARD GATES
> ENFORCED". T2: "SUNO SPECIFICS" (Vocal/Lyric vs. brief lock; any image-style
> Branch Set?) + "HARD GATES ENFORCED". T3: "START-CONDITION HANDLING" (restart
> vs. review path; records requested; Output Record creation). T4: "TEXT
> SPECIFICS" (which skill runs the Critic Review; Draft Generation Approval with
> no provider call; fresh-context drafting vs. editorial passes; conformance
> review before polishing; Clear→Human pass order and per-rewrite Output Records)
> + "HARD GATES ENFORCED". T5: "MISSING REFERENCE HANDLING" (medium route,
> missing Reference stop, no invented source material, and phases that must not
> run yet) + "HARD GATES ENFORCED". T6: "VIDEO STORYBOARD SPECIFICS" (video
> route; v0 storyboard-only boundary; Symbology → Style; video gates; storyboard
> still approval; Output Records for stills; no Video Prompt Plan) + "HARD GATES
> ENFORCED".
>
> Quote the skill line/section each major step comes from. Write the trace to
> `<repo>/evals/conductor-behavior/<baseline|trimmed>/T<N>.md` and return it.
