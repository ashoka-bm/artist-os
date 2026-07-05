# Seedance Cinematic Prompt Protocol

Status: research draft.

This protocol captures detailed Seedance 2 prompt-export behavior from the cinematic Seedance reference. It is downstream of the approved Video Medium Plan and storyboard-ready package. It must not change the provider-neutral story or format decision flow.

## Boundary

- Do not call a provider from this protocol.
- Do not generate or upload media without explicit approval.
- Use this only to produce or review a manual Seedance prompt packet.
- Keep Story Template, Micro-Journey Template, Cultural Format Structure, and Video Medium Plan decisions upstream.

## Export Modes

Use one mode at a time:

- **Shot-list planning mode:** create a human-readable shot plan. It does not output Chinese prompt text or provider tags.
- **Prompt export mode:** turn a selected scene or selected shot batch into provider-ready prompt text.

If the user gives a finished shot list and asks for prompts, do not assume the whole list fits. First confirm the shot range for this batch, the current reference tray mapping, and any dialogue or audio clips.

## Prompt Output Contract

A Seedance cinematic prompt packet should carry:

- one English prompt block for the whole selected scene or batch;
- one reference binding table that names every reference file, provider tray tag, role, and shot scope;
- one recommended duration line for the whole scene or batch.

Draft renderer constraints:

- Write final prompts in English. Do not create Chinese prompt blocks, Chinese translations, or Chinese provider tags unless the artist explicitly asks for a separate experimental translation.
- Keep the generated clip at 4-15 seconds unless the user explicitly chooses otherwise.
- Derive shot count from duration: 4-6 seconds usually supports 1-2 shots, 7-10 seconds supports 3-4 shots, and 11-15 seconds supports 4-6 shots.
- Keep six shots as the default maximum.
- Include 24fps in the scene header.
- Preserve the approved aspect ratio from the Video Medium Plan or state any provider limitation before export.
- Do not add beat headers to the provider prompt.
- Do not add per-shot durations inside the shots.
- Re-output the complete prompt packet on revision so no stale shot or tag state is left behind.
- Keep music, ambience, and subtitles governed by the approved audio/text posture instead of defaulting them into every prompt.
- Preserve the approved aspect ratio and storyboard shot order from the Video Medium Plan.
- Do not add new story events, character decisions, camera motivations, spoken lines, music, subtitles, wardrobe, props, or symbols that are not present in the approved storyboard package or approved references.

## Reference Tag Protocol

Provider tag bindings are session-local. They must be read from the current provider tray or supplied by the operator before final prompt rendering.

Draft rules:

- Put whitespace around provider tags so they do not touch punctuation.
- Reintroduce relevant tags in every shot.
- Attach a tag to the noun it controls.
- Use the identity noun on first mention in each shot before switching to pronouns.
- Do not over-describe details already controlled by a reference tag.
- Keep tags in English-readable prompt text exactly as they appear in the current provider tray.
- Bind every tag to a local reference file path or accepted Output Record before final prompt rendering.

Reference selection should follow shot scale:

- close identity or face reference: use when identity must be preserved, especially close and medium shots;
- body or turnaround sheet: use for wide, full, and medium shots where clothing, silhouette, or proportions matter;
- detail reference: use for close-ups, extreme close-ups, and medium shots where texture is visible;
- style reference: keep separate from identity, wardrobe, prop, and location references.

## Start-Frame Mode

Start-frame animation is a different export case from all-reference prompting. When the uploaded image is the opening frame, the prompt should describe motion from that frame and avoid treating the image as a normal repeated reference tag.

For multi-part generation, the Production Route may use the last accepted frame of one generated clip as the start frame of the next clip. That frame is a continuity asset, not a story decision. It should be recorded as an Output Record or asset metadata before it becomes a provider binding.

## Audio Handling

When an audio reference drives speech, bind the audio inline at the moment of speech. The audio reference should carry the voice, timbre, and pacing. Do not transcribe a spoken line into the prompt when the clip itself carries the line.

If one spoken line is split across a cut, treat it as a risk. Separate audio clips may be required for separate shots. Keep emotional direction on the face and performance unless changing the voice is explicitly intended.

## Camera And Coverage Rules

- Use direct camera-facing language in the prompt.
- Use one camera movement per shot.
- Avoid complex moves that make the model solve camera, action, and identity at the same time.
- Vary angle and shot scale across cuts.
- Push tighter as the scene stakes rise.
- Do not repeat the same shot size for too many consecutive shots.
- Prefer reaction, reveal, and hold-beat coverage when tension matters.

## Craft Guards

- Keep action density low enough for the clip length.
- Keep spoken lines short enough for the selected duration.
- Order action before dialogue when the movement sets up the line.
- Preserve continuing-frame, background, head, and body orientation with short continuity instructions.
- Use targeted realism language for skin, hair, texture, motion blur, and non-plastic surfaces when realism matters.
- Keep negative instructions narrow and tied to known failure modes.
- Watch for moderation-sensitive wording around profanity, explicit body language, and branded products.

## Reference Asset Preparation

Recurring subjects should have reference material before scene export:

- turnaround sheet for full-body or full-object continuity;
- dead-on identity plate for the clearest subject anchor;
- close-up detail sheet for texture and feature continuity.

These assets belong in the reference-prep journey before Seedance prompting. GPT Image 2 is the default implemented image-generation route for approved reference outputs and start frames unless another implemented route is explicitly selected. Once approved, the resulting assets can be mapped through Provider Media Bindings into the current provider tag tray.
