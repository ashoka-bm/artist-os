# Dan Kieft Cinematic Seedance Updated Analysis

Status: research draft.

Source: `/Users/ashokaji/Desktop/Video Ref/Dan Kieft Cinematic Seedance Updated.md`

Provider or platform: Seedance 2, GPT Image 2.

## Why It Matters

This reference is not mainly a story-template source. It is a practical post-storyboard prompt protocol for turning a selected scene or shot batch into a Seedance-ready prompt. Its value is in output discipline, reference handling, shot batching, continuity, audio binding, and asset-prep requirements.

## Useful Patterns

- Treat Seedance prompt writing as an export layer after story, format, and storyboard decisions are already known.
- Keep one generation to a short scene or shot batch, roughly 4-15 seconds and no more than six shots unless the user explicitly asks for more.
- Derive shot count from duration instead of picking a shot count first.
- Render a Seedance prompt in Chinese, with dialogue and provider tags left in the forms the provider expects.
- Keep the output shape strict: one prompt block, a mirrored translation for review, and one recommended duration note.
- Do not mix shot-list planning with prompt export. A shot list is a planning artifact; a Seedance prompt is a provider artifact.
- If a finished shot list is handed over, ask which shots are being exported this round and confirm the current reference-tray mapping before writing.
- Treat provider reference tags as volatile bindings. The tag assignment is local to the current provider session and must be confirmed each generation.
- Reintroduce relevant reference tags in every shot because provider shots do not reliably remember previous shots.
- Place a tag next to the noun it controls, not in a loose reference list.
- Avoid restating visual details already carried by a strong reference tag unless a small instruction is needed to clarify scope.
- Use different reference types by shot size: face identity for identity, body or turnaround sheet for wide and medium shots, detail sheet for close views or visible texture.
- Separate start-frame animation from all-reference prompting. Start-frame mode should describe motion from the starting image rather than tagging every asset.
- Use plain camera language in the final prompt and keep one camera movement per shot.
- Push shot size tighter as stakes rise, vary scale and angle across cuts, and avoid repeating the same shot size too often.
- Preserve realism with targeted texture and motion-blur instructions rather than long negative-prompt lists.
- Keep continuity instructions simple: match start frame, head/body orientation, background, and action order where needed.
- When an audio reference drives a spoken line, bind the audio inline to the speaking action and avoid transcribing the carried line into the prompt.
- Keep music and ambience as explicit decisions. Do not add provider sound instructions unless the approved audio posture requires them.
- Prepare reusable subjects with GPT Image 2 reference assets before scene work: turnaround sheet, dead-on identity plate, and macro detail sheet where needed.

## Framework Mapping

- **Story Template:** no direct promotion. This source does not define an audience journey.
- **Video Medium Plan:** no direct field promotion yet. It can supply duration, storyboard shots, audio posture, selected references, and approved visual style.
- **Provider Media Bindings:** should eventually map Artist OS asset ids to the provider's current tag names and roles.
- **Provider Export Renderer:** strongest home. The renderer can apply Chinese formatting, tag placement, duration-derived shot count, and output shape.
- **Direction Notes:** the reusable camera judgment maps to `direction-notes/cinematic-coverage-and-camera-direction.md`.
- **Reference Preparation:** supports future Visual Reference Sheet Plan guidance for recurring characters, objects, products, vehicles, animals, and props.
- **Shot List Artifact:** supports a separate planning artifact mode before prompt rendering, not a replacement for Video Medium Plan.

## Failure Modes To Guard

- Exporting an entire shot list as one prompt without batching.
- Letting provider syntax leak into provider-neutral story or storyboard records.
- Writing a prompt before duration, shot selection, references, and dialogue are confirmed.
- Using too many shots, per-shot durations, beat headers, or mixed planning/prompt output.
- Losing provider tags in translation or revision.
- Treating a tag as permanent across generations.
- Overloading close-ups with full-body character sheets.
- Letting audio tags stand alone without an inline voice-consistency instruction.
- Adding default music or ambience that was not approved.
- Asking Seedance to hold too much action, too many subjects, or too many camera moves at once.

## Open Questions

- Should Artist OS store provider tag mappings as a temporary export-session record, or only in a manual export packet?
- Should shot-list HTML become a first-class draft artifact, or remain a provider-research helper?
- Should GPT Image 2 reference-sheet preparation be promoted into the image/reference journey before video export?
- How much of the strict Chinese output shape belongs in a Seedance-specific renderer versus human-facing operator guidance?
