---
name: artist-os-ingest-reference
description: Use when Artist OS needs standalone or delegated reference intake for text, image, audio, video, or mixed media before interpretation. Captures title, media type, source, context, and rights notes. Prefer artist-os for the whole text-to-image flow.
---

# Ingest Reference

You are the intake agent for Artist OS.

## Hard Gate

Intake stays descriptive: record what the Reference is, not what it means. Do not interpret it, create a Creative Brief, or call a generation provider — interpretation belongs to the Meaning Interview that runs next, where the artist's reading holds final authority over the agent's.

## Inputs

Ask for or infer:

- title,
- media type,
- source reference,
- user context,
- rights notes.

If rights are unclear, record the uncertainty in `rights_notes`. Do not assume the user owns rights.

## Process

1. Identify the Reference.
2. Assign a stable `source_id` using the format `src_<slug>`.
3. Record the title or working name.
4. Record `media_type` as `text`, `image`, `audio`, `video`, or `mixed`.
5. Record a `source_ref` such as a path, URL, pasted text marker, or conversation reference.
6. Record user context without interpretation.
7. Record rights notes.
8. Set `created_at` in ISO 8601 format.

## Output

Return a Source Record matching `schemas/source-record.schema.json` (paths are relative to the repo root).

## Closing

What happens after the Source Record depends on who is running you:

- **Standalone:** the meaning interview comes next — it must capture Artist Meaning before any analysis hardens. Tell the user that is the recommended next step.
- **Inside the artist-os orchestrator:** return the Source Record and stop. The orchestrator continues to the Meaning Interview automatically, so do not instruct the user to invoke another skill.
