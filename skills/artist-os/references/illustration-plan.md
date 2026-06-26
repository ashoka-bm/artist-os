# Illustration Plan

Use this internal mode when an artist wants an illustrated written work: children's book, picture book, comic, graphic story, story with spot illustrations, cover plus interior art, or diagram-rich written piece. User-facing phrases such as "children's book storyboard" and "comic storyboard" route here, not to Video Journey.

Paths like `schemas/illustration-plan.schema.json`, `schemas/character-template.schema.json`, `schemas/visual-reference-sheet-plan.schema.json`, `schemas/text-medium-plan.schema.json`, and `schemas/prompt-plan.schema.json` resolve from `$ARTIST_OS_ROOT`.

## Hard Gates

- Create the Illustration Plan only after the Text Medium Plan exists.
- Do not treat Illustration Plan as Video Medium Plan. It has no timed Storyboard Shots, Video Audio Posture, camera-motion contract, or finished-video promise.
- Ask once about Character Templates and optional Character Reference Sheet prompts when recurring characters matter. If declined, record `declined` and do not ask again in the same flow.
- Run Illustration Plan Reviewer before Illustration Plan Approval.
- Do not bulk-expand page, spread, panel, cover, or diagram image prompts before Illustration Plan Approval.
- Do not generate images or reference sheets without explicit Generation Approval.

## Inputs

Use:

- Source Record,
- Artist Meaning,
- Transformation Brief,
- approved Beat Plan,
- Text Medium Plan,
- Character Templates and Visual Reference Sheet Plans when accepted,
- existing Long-Work Stewardship Record when cumulative support is active,
- artist-provided illustrated work type or publication/use constraints.

## Process

1. Confirm the work is illustrated written work, not video. If "storyboard" is ambiguous, ask whether the artist means video storyboard or Illustration Plan.
2. Use the Text Medium Plan as the authority for written structure, section jobs, audience, length/page shape, publication/use, fidelity policy, and review presentation.
3. Choose `illustrated_work_type`: children's book, comic, graphic story, story with spot illustrations, diagram-rich explainer, cover plus interior, or other.
4. Resolve `character_reference_strategy` and `visual_reference_sheet_strategy`, and create or update Reference Inventory subjects when characters, locations, or objects need continuity. Do not re-ask declined strategies.
5. Build `page_or_panel_plan[]`. Each unit must name its page/spread/panel/diagram/cover job, text section refs, Beat ids, Key Emotional Movement ids, image type, prompt brief, character refs used, `reference_refs_used`, and style continuity notes.
6. Define text-image relationships. Images should add, reveal, pressure, clarify, or counterpoint the text; they should not merely duplicate it.
7. Define visual continuity rules, including character, setting, object, palette/light, style, and diagram conventions when relevant.
8. Set generation policy: Illustration Plan Approval before bulk prompt expansion; Reference Readiness before illustration prompt export; Generation Approval before image generation.
9. Emit the Illustration Plan and send it to Illustration Plan Reviewer.

## Illustration Plan Reviewer

Use a bounded reviewer with `review_role = "illustration_plan_reviewer"`. Review only the bounded packet: Artist Meaning, Transformation Brief, Beat Plan, Text Medium Plan, Illustration Plan, Character Templates, Visual Reference Sheet Plans, and open questions.

Check:

- page, spread, panel, and diagram logic,
- text-image fit,
- character consistency,
- visual continuity,
- audience or age fit when relevant,
- whether each image has a clear job,
- whether reference-sheet prompts align with the plan,
- whether the plan incorrectly drifted into video-specific timing, camera movement, transition, or audio posture.

The reviewer may apply Art Critic and Writing Critic criteria as supporting checks, but emits one integrated Review Record.

## Outputs

Before review, return the Illustration Plan, Character Reference Strategy, Visual Reference Sheet Strategy, page/spread/panel/diagram plan, visual continuity rules, text-image relationships, and open questions.

After Illustration Plan Review and Illustration Plan Approval, expand approved units through Image Journey support into Provider-Neutral Image Prompt Plans. Each generated or imported image receives an Output Record before Output Critic Review or Output Acceptance.
