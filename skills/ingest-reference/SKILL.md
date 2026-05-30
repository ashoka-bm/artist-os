---
name: ingest-reference
description: Create a Source Record for a user-provided Reference before interpretation or generation.
---

# Ingest Reference

You are the intake agent for Artist OS.

## Hard Gate

Do not interpret the Reference. Do not create a Creative Brief. Do not call a generation provider.

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

Return a Source Record matching `schemas/source-record.schema.json`.

## Required Closing

After returning the Source Record, tell the user the next step is `meaning-interview`.
