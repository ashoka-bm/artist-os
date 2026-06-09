# Conductor behavior eval

Goal: verify that trimming `skills/artist-os/SKILL.md` preserves the conductor's
*behavior* — phase order, hard-gate enforcement, sibling delegation, medium
quirks, and start-condition handling. Each test produces an ordered TRACE; we
grade the trace against a checklist. Baseline (current conductor) defines the
"correct" behavior the trimmed version must reproduce.

## Test prompts

- **T1 (image, full flow):** "Here's a poem about my mother's hands. I want to turn
  it into visual art. Go on autopilot — assume I approve the recommended option at
  every gate and approve generation — and take it all the way."
- **T2 (suno, full flow):** "Turn my journal entry about insomnia into a Suno track.
  Autopilot, I approve recommended choices and generation; take it to the end."
- **T3 (review start-condition):** "I already generated an image for my 'saltmarsh'
  project and have the brief and prompt plan. Can you review the image against it?"

## Checklist (assertions per trace)

### T1 — image
1. Phases in order: Source Record → Artist Meaning → Transformation Brief → Beat Plan → Beat Review (if multi-beat) → Image Medium Plan → Draft Creative Brief → Art Critic Review → Brief Approval → Final Records → (optional Branch Set) → Prompt Plan Critique → Generation Approval → Output Record → Output Critic Review → Output Acceptance.
2. Delegates to: ingest-reference, meaning-interview, text-to-image-plan, writing-method-review (beat review), art-critic-review, critique-asset.
3. Hard gates enforced: provider-approval (per call), brief-approval before Creative Brief Record, series approval before multiple series prompts, Output Record before acceptance, persist each phase.
4. Visual gates run in order Symbology → Style during Image Medium Plan; Presentation Mode decided in the Symbology gate.
5. IMAGE QUIRK: Minimalist-to-Maximalist (intensity) gate runs at Brief Approval (after symbology+style locked), NOT during the medium plan.

### T2 — suno
1. Phases in order: Source Record → Artist Meaning → Transformation Brief → Beat Plan → Beat Review (if multi-section/lyric) → Sound Medium Plan → Draft Sound Creative Brief → Music/Sound Critic Review → Brief Approval → Final Records → Prompt Plan Critique → Generation Approval → Output Record → Output Critic Review → Output Acceptance.
2. Delegates to: ingest-reference, meaning-interview, text-to-suno-plan, art-critic-review (sound critic), critique-asset.
3. SUNO QUIRK A: Vocal/Lyric resolved before locking the brief (lyrics/phonetic/instrumental chosen).
4. SUNO QUIRK B: NO image-style Prompt Branch Set in the Suno flow.
5. Hard gates: provider-approval, brief-approval before Sound Creative Brief Record, sequence approval before multiple sequence plans, Output Record before acceptance, persist each phase.

### T3 — review start-condition
1. Does NOT restart the full creation flow.
2. Identifies/asks for governing project, brief, prompt plan, medium plan, beat plan, Artist Meaning, Source Record.
3. Creates an Output Record (against output-record schema) if none exists.
4. Jumps to Output Critic Review then Output Acceptance Gate.
5. Output Critic runs as a bounded sub-agent (critique-asset) and emits a Review Record.

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
> Scenario (the user's message): "<T1 / T2 / T3 prompt>"
>
> Produce a precise ORDERED TRACE of what the conductor does. Do NOT call any
> generator and do NOT write project files. The trace is a numbered list; each
> step states: (a) phase name, (b) sibling skill it delegates to, (c) any hard
> gate enforced and the approval it requires, (d) any record/schema produced,
> (e) where it would pause for artist input.
>
> Then add the trace-specific sections — T1: "VISUAL GATES" (gate order;
> Presentation Mode and Minimalist-to-Maximalist timing) + "HARD GATES
> ENFORCED". T2: "SUNO SPECIFICS" (Vocal/Lyric vs. brief lock; any image-style
> Branch Set?) + "HARD GATES ENFORCED". T3: "START-CONDITION HANDLING" (restart
> vs. review path; records requested; Output Record creation).
>
> Quote the skill line/section each major step comes from. Write the trace to
> `<repo>/evals/conductor-behavior/<baseline|trimmed>/T<N>.md` and return it.
