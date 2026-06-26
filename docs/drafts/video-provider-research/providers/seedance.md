# Seedance Draft Notes

Status: research draft.

Seedance appears in the current references as the model behavior being prompted through a Higgsfield-style workflow. The most useful early research concerns prompt structure, shot-family formatting, reference scoping, and recurring model failures.

## Current Pattern Hypotheses

- Seedance 2 exports should default to 24 frames per second when the provider prompt accepts frame-rate language.
- A Seedance 2 prompt may perform better in Chinese; keep English only as an authoring or review translation when needed.
- A single generation should be planned as a 15-second-or-less clip unless the provider settings prove otherwise.
- Multi-clip sequences should use the last frame of the previous clip as the next clip's starting continuity reference when the platform supports it.
- Provider prompts should name a concrete camera body or capture style, plus a specific lighting setup, when those details support the approved Video Style Expression.
- Raw Seedance clips should usually request no subtitles and no music unless the approved Audio Posture requires otherwise.
- Talking or interacting characters should be framed medium shot or closer so faces, lip motion, and interaction cues remain legible.
- Seedance scenes should limit the number of active subjects; extra subjects increase identity and action drift.
- Background motion should be simple and explicit, such as moving lights, drifting fabric, swaying trees, passing people, or animated props.
- Visual style reference images should be mapped separately from identity, object, wardrobe, or scene references.
- Action should be minimized and staged as one readable movement per shot when possible.
- Film grain can be added as a style finish when it matches the approved Video Style Expression.
- Single continuous shots should avoid internal timestamps unless a cut is desired.
- Multi-cut b-roll can use repeated time brackets to force deliberate cuts.
- Camera lock, diegetic camera movement, and operator camera movement need distinct language.
- Uploaded audio should drive lip-sync without extra microphone-character prose.
- Reference images need scoped roles to prevent unwanted transfer.
- Negative prompts should stay lean unless a known failure justifies a targeted addition.
- Influencer video prompting adds stronger identity locks, wardrobe-reference routing, product/logo visibility rules, and content recipes such as UGC talking head, product reveal, lifestyle plandid, GRWM, and brand integration.
- Animation workflows may use a simpler style/action/camera prompt when character sheets, storyboard panels, or start/end frames already carry the design.
- Seedance should be tested by camera-control type: pan, tracking, POV, orbit, macro zoom, side-scroll, fixed camera, and jump-cut/editing behavior.
- Cinematic Seedance exports need a stricter renderer protocol than the general checklist: duration-derived shot count, six-shot default cap, Chinese prompt body, 24fps scene header, no beat headers, no per-shot durations, mirrored English review translation, and complete re-output on revision.
- Reference tray tags are volatile provider bindings. They should be confirmed before prompt export, placed next to the noun they control, repeated in every shot where needed, and mirrored in the English review translation.
- Start-frame animation should be handled separately from all-reference prompting; a start frame usually needs motion instructions, not repeated image tags.
- Audio references should be bound inline to the speaking action. If the audio clip carries the line, the prompt should not also transcribe the same line as text.
- Recurring subjects may need GPT Image 2 reference assets before Seedance scene work: turnaround sheet, dead-on identity plate, and close-up detail sheet.

## Draft Role

Seedance-specific behavior belongs in a provider-target prompt renderer after storyboard approval. The renderer can consume Video Medium Plan data and output a manual prompt without changing the neutral plan.

See also: [Seedance Cinematic Prompt Protocol](seedance-cinematic-prompt-protocol.md).
