# Seedance Instagram And Creator Prompting

Use this after storyboard approval when the selected provider route is Seedance and the output is an Instagram Reel, TikTok-style clip, creator vlog, talking head, UGC ad, fashion/editorial campaign, product reveal, short explainer insert, or social B-roll package.

This file governs prompt preparation only. Calling Seedance, uploading references, rendering video, or making any provider-backed generation call still requires explicit artist approval.

## Goal

Create short, platform-native Seedance prompts that feel like social video: immediate hook, clear subject, one readable idea, natural creator delivery, fast but legible movement, and enough negative space for later text overlays when needed.

Write all prompt text in English. Do not include Chinese prompt text or a Chinese prompt pass unless the artist explicitly requests a separate experiment.

## Inputs

Consume:

- approved storyboard shots or micro-journey shot list,
- approved hook, script, dialogue, caption, or voiceover refs,
- creator identity reference and current `@image` tag mapping,
- approved audio ref and current `@audio` tag mapping when lip-sync is needed,
- product, garment, object, location, or style reference files,
- target aspect ratio, usually 9:16 unless the plan says otherwise.

Preserve the creator's exact words. Do not rewrite dialogue, punch up phrasing, add claims, or invent product promises inside the Seedance prompt.

## Choose The Social Format Family

Pick one before writing:

- **Locked talking head**: studio, podcast, desk, or seated creator. Best for reflective, direct-to-camera lines.
- **Vlog selfie / handheld POV**: creator holds the frame; use first-person or found-footage logic. Best for tours, confessions, reveals, day-in-the-life clips.
- **Observer phone footage**: someone else films the creator. Best for casual meetups, public demos, social proof, or candid-feeling moments.
- **Product reveal / demo**: product is the hero. Keep hands, object state, and before/after change legible.
- **Fashion/editorial Reel**: garment is the hero. Fast cuts, model movement, direct attitude, macro fabric/detail shots, negative-space wides.
- **B-roll montage**: no dialogue or light VO; deliberate cuts show process, proof, setting, texture, or transformation.
- **Motion-graphics insert**: only when the visual system is graphic-first. Keep text generation outside Seedance when possible; prompt the background/card motion, not gibberish text.

## Hook Logic

The first shot must earn attention. Use one:

- question hook: the creator asks or implies a question the viewer wants answered;
- surprising statement: one bold claim or odd fact, with a pause or held look;
- story-in-the-moment: drop into location, action, and problem without backstory;
- visual action hook: object held up, silent pause, unexpected movement, reveal, or frame placement;
- big promise: show what the viewer gains, not what the creator will discuss.

For story-shaped social clips, reduce the arc to five lines before prompting: situation, desire, conflict, change, result. Prompt the moment, not the explanation.

## Prompt Template

Use this plain-text structure for most creator/social prompts:

```text
FORMAT: [duration]s / [single continuous shot OR N-cut b-roll] / [one-line social concept]

SUBJECT: [@image tag and role].

WARDROBE / PRODUCT / PROP: [only what must be controlled].

ENVIRONMENT: [specific location, lighting source, ambient context].

STYLE ANCHOR: [social format family, camera identity, framing, lighting, realism, reference scope].

DELIVERY: [Lip-sync driven by @audio1 OR No dialogue].

LOGIC RULE: [continuity, camera behavior, shot family, reference scope, hook/readability guard].

NEGATIVE PROMPT: [only narrow failures: no music, no captions, no visible camera object, no podium, no extra text, etc.]

ACTION:

[time header] - [camera position only]. [One continuous take if applicable.]

[Action prose with dialogue inline where it lands.]
```

For fashion/editorial Reels, one flowing paragraph is acceptable when the target tool favors compact prompts. Use `Cut to.` between shots and end with a diegetic-audio line.

## Codex Output Format

When Codex prepares a Seedance social or creator prompt package for review, return the package in this order:

1. `Social format family:` the selected family and duration.
2. `Reference bindings:` one compact line or table mapping each provider tag to its file, role, and scope.
3. `Seedance prompt:` one English plain-text code block containing the complete prompt.
4. `Negative prompt:` only the narrow social failure fixes needed for this clip.
5. `Generation boundary:` one sentence stating that Seedance upload, render, or generation still requires explicit artist approval.

Do not include a Chinese version, alternate prompt pass, caption-rendering instruction, provider upload instruction, or generation-ready claim outside that boundary sentence.

## Shot Family Rules

### Single Continuous Shot

Use for talking heads, vlog selfies, dialogue, tours, and one-take reactions.

- Use one time header only.
- Do not put internal timestamps in the action body.
- Include `Single continuous shot. No cuts, no jumps, no zoom` unless a zoom or pan is explicitly part of the concept.
- Pair dialogue with physical beats: breath before, line, held look after.
- Keep action density low: about 5-6 beats max for 15 seconds, fewer for shorter clips.

### Multi-Cut B-Roll

Use for process, packing, mirror, product, outfit, or proof montages.

- Use explicit time brackets for deliberate cuts.
- Each cut has its own camera position and one action.
- Use same-angle jump cuts only when progress/time passing is the point.
- Match motion direction across cuts when smoothness matters; break rhythm with a smash cut only for surprise or reset.

## Talking Head And Vlog Rules

- `@audio` belongs in DELIVERY as `Lip-sync driven by @audio1.` Keep it clean; do not describe mic character, room tone, device audio, or ambience if an audio file controls voice.
- If no audio file exists, estimate duration from word count and push back if the line is too long for 15 seconds.
- Put emotion before the line: `he says calmly, "..."`.
- Use ellipses for real pauses already present in the audio or approved script.
- Trust the model on micro-expression. Give at most one opening performance note and one closing beat.
- For creator delivery, make it feel like a coffee-shop conversation: connected, not over-presented.
- Avoid "perfecting" energy. Let the body move naturally: casual hand gestures, breath, leaning in, held eye contact.

## Found-Footage And Phone Logic

For selfie/vlog clips, the frame is the camera. Avoid spawning a visible phone or duplicate camera.

Use:

- `The viewer's perspective is the handheld frame throughout.`
- `The frame sways naturally with the creator's stride.`
- `The perspective lowers onto the empty ledge and locks.`

Avoid:

- `he sets the camera down`,
- `the phone is visible`,
- `his hands hold the camera object`,
- repeated negatives like `no phone, no duplicate camera` unless a prior render failed.

If the creator physically pans, describe it as diegetic motion: `he turns the handheld frame toward the window`. Before and after that move, keep only natural handheld sway.

## Fashion / Product / UGC Rules

- Make the hero clear: face, product, garment, or action. Do not split priority across all four.
- Fashion: every shot needs model movement, even if subtle. Include one negative-space wide and one direct-attitude beat.
- Garment prompts prioritize silhouette, fabric, hardware, colorway, and movement over biography.
- Product prompts prioritize handling, scale, before/after, texture, logo visibility policy, and the exact reveal.
- UGC prompts should feel casual and specific: a hand reaches, a creator reacts, a product is tried, proof appears.
- Keep active subjects low. One creator plus one product is easier than a crowd.

## Framing For Overlays

Do not ask Seedance to render captions, title text, UI labels, or brand copy unless the approved plan explicitly wants generated text. It will often garble text.

Instead, reserve space:

- subject in left third, right two-thirds clean negative space;
- subject in lower third, upper two-thirds sky/wall/product surface;
- product in one third, clean counter or wall beside it.

State the frame geometry in STYLE ANCHOR and LOGIC RULE when overlay space matters.

## Common Failure Fixes

- **Muffled voice**: strip DELIVERY to `Lip-sync driven by @audio1.`
- **Frozen subject**: add `Natural head movement and hand gestures evolve organically with the speech, no static movement, no looping.`
- **Looping gestures**: add `hand gestures evolve organically, no repeated looping gesture.`
- **Visible duplicate camera/phone**: replace physical camera language with `frame`, `perspective`, and `viewer POV`; state the surface is empty.
- **Podium or stage appears**: reframe as casual meetup or informal circle; add `nothing in front of the creator`; use `no podium` only if needed.
- **Wrong warm lighting**: repeat the lighting source in FORMAT, ENVIRONMENT, STYLE ANCHOR, and LOGIC RULE.
- **Plasticky face**: move to medium close-up or close-up; add visible pores, freckles, eye moisture, natural skin texture.
- **Unnatural walk**: specify relaxed gait, arm swing, weight shift, and object handling.
- **Too many things happening**: remove beats or split into another generation.
- **Reference bleed**: scope each reference with `contributes only... never...`.
- **Subject recenters despite overlay space**: use exact frame fractions, such as `body fully contained within the leftmost third`.

## Social Review Before Generation Approval

Block or revise the prompt if:

- prompt text is not English,
- the hook is missing or buried after setup,
- dialogue was rewritten,
- a creator identity, audio, product, garment, or location tag lacks a reference file or scope,
- the prompt tries to render captions or title text that should be added in edit,
- a single shot contains too many actions for its duration,
- a vlog prompt risks visible camera/phone duplication,
- fashion/product prompts do not make the hero object legible,
- the result no longer serves the approved micro-journey or Intended Feeling.
