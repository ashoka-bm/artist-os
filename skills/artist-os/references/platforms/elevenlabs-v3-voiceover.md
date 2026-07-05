# ElevenLabs v3 Voice-Over Prompt Preparation

Use this reference when preparing existing script, dialogue, narration, monologue, or other spoken text for ElevenLabs v3 voice-over generation.

This file governs prompt preparation only. Calling ElevenLabs, rendering TTS, uploading audio, or making any provider-backed generation call still requires explicit per-call artist approval.

## Goal

Prepare dialogue or narration for expressive speech generation by adding voice-only audio tags while preserving the original text and meaning.

## Core Rules

- Add only voice, breath, pause, or delivery tags in square brackets.
- Use tags such as `[happy]`, `[sad]`, `[excited]`, `[angry]`, `[whisper]`, `[annoyed]`, `[appalled]`, `[thoughtful]`, `[surprised]`, `[laughing]`, `[chuckles]`, `[sighs]`, `[clears throat]`, `[short pause]`, `[long pause]`, `[exhales sharply]`, and `[inhales deeply]`.
- Similar contextually appropriate tags are allowed only when they describe vocal delivery, vocal emotion, breath, pause, or non-verbal voice sounds.
- Place tags immediately before, immediately after, or at a natural pause in the dialogue segment they modify.
- Keep tags contextually appropriate and emotionally natural.
- Preserve the original dialogue text and meaning.
- Do not invent new dialogue lines.
- Do not remove, rewrite, reorder, or replace original words.
- Do not turn existing narrative descriptions into tags.
- Do not use tags for body movement, facial expression, music, environmental sound, or non-voice sound effects.
- Do not use tags such as `[standing]`, `[grinning]`, `[pacing]`, or `[music]`.
- Do not add sensitive, NSFW, political, religious, hateful, profane, or otherwise unsafe implications.

## Emphasis Allowance

When it genuinely improves spoken delivery without changing meaning, the preparation pass may add emphasis by capitalizing selected words, adding a question mark or exclamation mark, or adding ellipses.

Use this allowance sparingly. If the artist requests exact text preservation, do not change capitalization or punctuation; add audio tags only.

## Working Prompt

Use this prompt shape when the task is to transform supplied spoken text into an ElevenLabs v3-ready prompt:

```text
You are an AI assistant specializing in preparing dialogue for ElevenLabs v3 speech generation.

Your goal is to add expressive voice-only audio tags to the provided dialogue while preserving the original wording and meaning.

Rules:
- Add only voice or delivery tags in square brackets, such as [laughing], [sighs], [whisper], [thoughtful], [excited], [annoyed], [surprised], [clears throat], [short pause], [inhales deeply].
- Place tags immediately before, after, or at a natural pause in the line they modify.
- Tags must describe vocal delivery, emotion, breath, pause, or non-verbal voice sounds.
- Do not add music, sound effects, movement, visual actions, or stage directions.
- Do not use tags like [standing], [grinning], [pacing], [music], or environmental sounds.
- Do not invent new dialogue.
- Do not remove, rewrite, reorder, or replace the original words.
- Do not turn existing narrative text into tags.
- Do not add sensitive, NSFW, political, religious, hateful, or profane implications.
- Keep tags contextually appropriate and emotionally natural.

Important:
Preserve the original dialogue text exactly unless emphasis changes were explicitly allowed. If emphasis is allowed, you may capitalize selected words, add a question mark or exclamation mark, or add ellipses when it improves delivery without changing meaning.

Output:
Return ONLY the enhanced dialogue text. Do not explain your choices.

Dialogue:
{{PASTE_DIALOGUE_HERE}}
```

## Codex Output Format

When Codex is preparing a specific ElevenLabs v3 prompt from supplied spoken text, return only the enhanced spoken text by default. Do not add a heading, explanation, bullet list, rationale, markdown fence, or tag audit unless the artist asks for review notes.

If the artist asks for the reusable preparation prompt, return only the reusable prompt template in a plain text code block.

If the artist asks for both the enhanced text and a review note, use this compact shape:

```text
Enhanced text:
[enhanced spoken text]

Review note:
[one short note about preservation, emphasis, or any line that could not be safely tagged]
```

## ElevenLabs Prompt Output

Return only the enhanced spoken text unless the artist asks for the reusable prompt itself.

The enhanced spoken text must:

- preserve every original spoken word in order,
- add only square-bracket voice, breath, pause, or delivery tags,
- keep any emphasis punctuation or capitalization meaning-preserving,
- avoid markdown, commentary, field labels, JSON, XML, SSML, stage directions, movement notes, sound effects, music notes, and environment notes.
