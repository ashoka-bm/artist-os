# Seedance Cinematic And Animation Prompting

Use this after storyboard approval when the selected provider route is Seedance and the output is cinematic live-action, animated narrative, stylized animation, scene coverage, or storyboard-panel animation.

This file governs prompt preparation only. Calling Seedance, uploading references, rendering video, or making any provider-backed generation call still requires explicit artist approval.

## Inputs

Consume:

- approved Video Medium Plan and Storyboard Shots,
- approved aspect ratio and duration target,
- accepted reference files or Output Records,
- current provider tray tags such as `@image1`, `@audio1`, or start-frame mode,
- approved script, dialogue, audio posture, and text track refs,
- reference scope notes: identity, body, detail, location, object, style, start frame, or audio.

Do not invent story turns, new dialogue, new symbols, new wardrobe, new props, or new camera motivation. Translate the approved storyboard into a Seedance-ready prompt.

## English-Only Rule

Write Seedance prompts in English. Do not include Chinese prompt text, Chinese translations, Chinese camera tokens, or a Chinese prompt pass unless the artist explicitly asks for a separate experiment.

## Choose The Prompt Mode

- **Start-frame animation**: use when the uploaded image is the opening frame. Describe the motion out of that frame. Do not repeat normal `@image` tags as if they were reference tray bindings.
- **All-reference prompting**: use when Seedance references are tray-bound assets. Use provider tags inline next to the noun they control.
- **Storyboard-panel animation**: use when a storyboard sheet is the visual reference. Keep the prompt broad: animate the approved panel sequence, preserve character consistency, and name the motion path.
- **Shot-batch prompt**: use when turning selected Storyboard Shots into one Seedance generation. One batch covers about 4-15 seconds, max six shots by default.

If the user hands over a full shot list, do not assume the whole list fits. Ask which shots are in this batch and ask for the current reference tray mapping.

## Batch Rules

- Keep each generation between 4 and 15 seconds unless the artist explicitly chooses otherwise.
- Derive shot count from duration: 4-6s usually 1-2 shots; 7-10s usually 3-4 shots; 11-15s usually 4-6 shots.
- Cap at six shots by default.
- Include `24fps` when the provider prompt accepts frame-rate language.
- Do not add Beat headers.
- Do not put per-shot durations inside the prompt body.
- On revision, re-output the complete prompt packet, not only the changed shot.

## Reference Binding Rules

Before final prompt text, know what each reference file does.

- Identity or face ref: use in every shot where that subject appears, especially close and medium shots.
- Body or turnaround sheet: use for wide, full-body, and medium shots where silhouette, costume, or proportions matter. Avoid it in extreme close-ups when it confuses face detail.
- Macro detail ref: use for close-ups and medium shots where skin, hair, texture, surface, markings, or material detail is visible.
- Location ref: use for geometry, blocking, lighting layout, and continuity.
- Object or prop ref: use only where the object is handled, revealed, transformed, worn, opened, destroyed, or story-critical.
- Style ref: keep separate from identity, object, wardrobe, and location references.
- Audio ref: bind inline where speech happens. If the audio clip carries the line, do not also transcribe the line unless the workflow explicitly needs visible lip-sync text.

Place tags with whitespace around them, next to the noun they control: `the cavewoman @image1`, `the egg nest @image3`. Reintroduce relevant tags in every shot because each generated clip has no memory outside the current prompt.

Scope every reference. Say what it contributes and what it must not leak into the result: `@image2 contributes only the jacket shape and fabric texture, not face, body, color grade, or location`.

## Prompt Shape

Use one English code block plus a short reference binding table or mapping line outside it.

```text
Scene: [one-line setting and story purpose]. [N] shots / 24fps / [aspect ratio]. [rendering mode and realism/style line].

Shot 1 - [facing or angle]. [subject + reference tags] [one clear action, one camera move, continuity instruction].

Shot 2 - [facing or angle]. [subject + reference tags] [next action, one camera move, continuity instruction].

...

Recommended duration: [N] seconds. [one-line reason].
```

For a single continuous animated move, write one shot instead of forcing cuts:

```text
Scene: [setting]. Single continuous shot / 24fps / [aspect ratio].
[style]. [subject + tag] [action path]. Camera: [one movement only]. Preserve [reference continuity]. Recommended duration: [N] seconds.
```

## Codex Output Format

When Codex prepares a Seedance cinematic or animation prompt package for review, return the package in this order:

1. `Reference bindings:` one compact line or table mapping each provider tag to its file, role, and scope.
2. `Seedance prompt:` one English plain-text code block containing the complete prompt.
3. `Negative instructions:` only the narrow negatives needed for the approved storyboard.
4. `Generation boundary:` one sentence stating that Seedance upload, render, or generation still requires explicit artist approval.

Do not include a Chinese version, hidden translation, alternate prompt pass, provider upload instruction, or generation-ready claim outside that boundary sentence.

## Camera And Coverage

Choose camera language from the emotional job:

- wide or establishing: geography, scale, subject against world;
- full shot: body action, posture, walk, chase, dance, transformation;
- medium: dialogue, interaction, readable performance;
- close-up: emotion, reaction, identity;
- macro or extreme close-up: one detail carrying the whole moment.

Vary shot scale and angle across cuts. Do not stay at the same size for more than two consecutive shots. Use one camera movement per shot: push in, pull out, track, pan, tilt, orbit, handheld, locked/static. Avoid stacking moves such as track plus tilt plus push in.

For animation, still use grounded camera language. Lens terms can work as compositional shorthand, but keep the prompt readable: `wide 24mm low angle tracking` or `close-up 85mm static`.

## Style And Animation Rules

For animation, lock style before action:

- name the animation mode: 2D cartoon, cel-shaded, CGI feature animation, claymation, stop motion, PS1 retro, comic book, rubber hose, mixed media;
- name the texture and render behavior: flat fills, ink outlines, halftone, low-poly, visible fingerprints, brush texture, subsurface scattering;
- preserve character design from reference sheets before asking for motion;
- use style restyle sheets before scene prompts when the look must remain consistent.

For cinematic live-action, use concrete capture language only when it helps: camera type, lens feel, lighting source, practical light, deep focus, film grain, skin/hair realism, real surface texture. Do not rely on mood words alone.

## Craft Guards

- Keep action density low: roughly two or three actions per second maximum.
- Put action before dialogue when order matters.
- Prefer one sustained head turn or held look over back-and-forth head movements.
- Use motion blur only when speed matters.
- Keep continuity instructions short and physical: same hallway geometry, head on right, body stretching left, background remains unchanged.
- For recurring subjects, plan or use reference sheets before scene export: identity plate, full-body turnaround, and macro detail card.
- For start/end-frame animation, describe only the transition between the two frames and the one camera move that carries it.

## Negative Instructions

Keep negatives narrow and tied to known failure modes. Default to none unless the approved plan requires it. Useful targeted negatives:

- no subtitles,
- no music unless approved,
- no extra characters,
- no visible camera object,
- no camera movement for static locks,
- no logo or branded text,
- no plastic skin.

Do not stack generic negatives such as "no bad anatomy, no uncanny, no AI artifacts" unless a prior render shows that specific failure.

## Review Before Generation Approval

Block or revise the package if:

- prompt text is not English,
- a reference tag lacks a reference file or scope,
- the batch exceeds six shots without explicit approval,
- the prompt invents story, dialogue, props, wardrobe, or symbols,
- camera direction fights the emotional job,
- audio, subtitles, or music contradict the approved audio/text posture,
- action density is too high for duration,
- continuity depends on a reference output that has not been accepted or waived.
