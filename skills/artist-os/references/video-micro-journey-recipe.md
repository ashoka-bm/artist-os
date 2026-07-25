# Video — Micro-Journey Recipe (short-form, lean path)

Lean, self-contained path for short-form social video: short social clip, reel,
single dynamic clip, unboxing, creator post, demo, mini showcase — a compact
hook→payoff (`narrative_depth = micro_journey`), not a full Story Structure.

## Load economy — the point of this file

Do **not** load `skills/artist-os/references/video-journey.md`,
`skills/artist-os/references/storyboard-prompt-builder.md`, or the full `THEORY.md`
gate sections for this path. This recipe carries everything the planning
conversation needs. Load `schemas/video-medium-plan.schema.json` **once, at the
end**, in a finalization pass, to validate the final record — not during planning
or authoring. Escalate to the full `video-journey.md` only if the work turns out
to need full_story or long-form support (see Escalation).

The compact path has two different artifacts:

- **Compact Video Authoring Packet** — the thin planning surface used in the
  main conversation. Author from the field list below. It is not schema-backed
  and it is allowed to stay concise.
- **Video Medium Plan Record** — the schema-backed final record. Create it only
  after the packet is complete, by reading `schemas/video-medium-plan.schema.json`
  once, converting the packet into the required JSON shape, validating, and
  persisting it. Do not keep planning after this schema read; if more artist
  decisions are needed, ask them before finalization.

If repo tooling is available, prefer `bin/artist-os-video-finalize` as the
`record_builder` / `schema_validator` finalization pass: write the Compact Video
Authoring Packet to JSON, run the command, and let it expand the packet into the
schema-backed Video Medium Plan Record and validate it.

Before authoring JSON for the command, run:

```bash
bin/artist-os-video-finalize --print-template
```

Use that printed JSON as the compact packet contract. Fill its values and shot
list; do not infer required packet fields from `schemas/video-medium-plan.schema.json`,
do not inspect the command source, and do not copy old fixtures or `.tmp` outputs.
For a short text summary of the accepted compact fields, run:

```bash
bin/artist-os-video-finalize --print-contract
```

The finalizer owns schema boilerplate: provider boundary, story/template defaults,
compact workflow-scale routing, gates, review requirements, storyboard generation
policy, and optional character/reference strategies. The planning conversation
should provide the artist-specific IDs, format, symbology, style, visual dynamics,
scene/sequence labels when useful, audio posture, and shot list.

If the command is not available but the host can delegate, prefer a bounded
`record_builder` / `schema_validator` finalization pass for the Video Medium Plan
Record so the heavy schema stays out of the conductor's long-lived context. If
the host cannot delegate and the run is a token measurement, stop at the completed Compact Video Authoring Packet with a
reset handoff rather than pulling the full
schema into the parent thread.

Keep this fallback as a bounded `record_builder` / `schema_validator` finalization pass,
not an open-ended schema-authoring conversation.

This is **turn-economy, not shot-economy.** The output is a fluid, dynamic video —
typically ~one cut every 1–3 seconds, so roughly 20–60 distinct shots for a
sub-minute clip. Produce that whole dense shot list in **one batched pass**. Never
thin the cut count to save turns; save turns by batching the planning, not by
thinning the edit.

## Inputs and gates

Inputs (from the conductor, or confirm they exist if standalone): Reference, Artist
Meaning, Transformation Brief, Beat Plan.

If this medium is being activated on an existing project, these spine inputs already exist — consume the **Shared Story Spine** (Transformation Brief, Beat Plan, standing Story Approval) by reference; **do not re-derive** meaning or rebuild the Beat Plan.

The hard gates are unchanged — the lean path relaxes none of them:

- No video/image/render provider call without explicit per-call (or approved-batch)
  approval. Drafting the plan and storyboard frame prompts is allowed; generating is not.
- "Create/generate the storyboard" = one composite multi-panel storyboard sheet by
  default; individual stills are a separate, separately-approved batch.
- Every generated or imported sheet/still gets an Output Record before review or acceptance.
- Persist each step before advancing (`docs/storage.md`); chat is not durable storage.
- v0: no provider-neutral Video Prompt Plan; storyboard frame prompts live in the Video Medium Plan. Seedance Prompt Packages are optional post-storyboard provider exports.
- Preserve traceability: every shot traces to Artist Meaning, the Beat Plan, and the
  Video Medium Plan.

Keep the core algorithm visible: grab attention (hook in the first ~1–2 seconds),
trigger a strong emotion, forge one simple mental link. Every shot names its intended feeling.

## Steps (batched, few-turn)

1. **Confirm depth = micro_journey.** If the piece actually needs a full hook /
   pressure / turn / consequence / payoff across multiple scenes, stop and escalate to
   `video-journey.md`. Do not rebuild a full Story Structure inside this path.
2. **One quick Style Direction + light Symbology.** Recommend first, then confirm:
   rendering/camera/motion/edit/caption style, and the one core image that carries the
   meaning. Do not run full Symbology/Style board gates unless the artist asks.
3. **Light continuity scan.** Promote only a main character and/or one key object or
   location when drift would weaken meaning or audience trust. Offer the smallest useful
   reference batch (one style-calibration image + promoted refs) before any generation;
   record `declined`/`deferred` without re-asking.
4. **Batched shot list (the core, one pass).** Lay out the full fluid cut list mapping
   the Beat Plan's hook→payoff to ~20–60 shots. For each shot give: time range; shot
   scale + camera angle + camera/subject movement; blocking; transition in/out; intended
   feeling; a short symbolic/representation note; the storyboard frame prompt; and any
   script / audio / on-screen-text ref. Map shots to the smallest Beats — several shots
   may elaborate one beat, but do not compress multiple story turns into one shot. Keep
   cuts fluid and dynamic: vary scale, angle, and movement across adjacent cuts.
5. **Audio posture (one line):** silent / music-only / voiceover-led / dialogue-led /
   sound-design-led / mixed. Create Text or Sound Journey records only if drafted words or
   sound planning are actually needed.
6. **Produce the Compact Video Authoring Packet.** Do not read the schema for this step.
   If `bin/artist-os-video-finalize` is available, run `--print-template` first and
   fill that compact JSON surface. The packet must include only the fields the final record needs:
   source / Artist Meaning / Transformation Brief / Beat Plan ids; `narrative_depth =
   micro_journey`; `micro_journey_template_ref`; `workflow_scale_routing` with
   `scale_level = compact_artifact` unless it escalates; format and duration target;
   aspect ratio and publication/use; light Symbology and Style Direction; continuity
   decisions; the batched shot list; audio posture; storyboard generation policy; open
   questions; and traceability notes.
7. **Finalize the Video Medium Plan Record.** Only after the packet is complete,
   use `bin/artist-os-video-finalize` when available. Otherwise read
   `schemas/video-medium-plan.schema.json` once, shape the packet into
   schema-valid JSON, validate, persist, and then treat the schema as consulted.
   Do not use the full schema as the authoring surface and do not re-read it on
   later turns.
8. **Draft the compact Video Creative Brief Document.** Translate the finalized
   Video Medium Plan into a concise artist-readable meaning contract: intended
   feeling, hook-to-payoff movement, visual language, shot logic, continuity,
   audio posture, must-preserve constraints, and storyboard output boundary.
9. **Video Critic Review (standard bounded sub-agent).** Review only the bounded
   packet — Artist Meaning, Transformation Brief, Beat Plan, Video Medium Plan,
   compact Video Creative Brief, shot list, and open questions — checking meaning
   fidelity, hook strength, cut fluidity/variety, continuity of any promoted state,
   and that no story turn was compressed. Emit a Review Record
   (`schemas/review-record.schema.json`) with `review_role = "video_critic"`.
   Apply findings to the compact Video Creative Brief before advancing.
10. **Brief Approval (explicit artist gate).** Present the revised compact Video
    Creative Brief and wait for approval. Do not create the storyboard-ready
    handoff, Seedance package, or storyboard-generation request before approval.
11. **Storyboard on request = one composite multi-panel sheet** (provider-gated,
   per-call approval, Output Record). Use the approved shot count as the source of truth;
   if the sheet needs a different panel count for readability, state the proposed
   split/merge before generation approval.

## Reset / handoff (if it runs long)

A batched sub-minute clip should rarely need a reset. But if the planning conversation
passes a good stopping point — e.g., context is climbing high, or the Video Medium Plan
is persisted and storyboard work remains — use the portable reset handoff: state that the
run reached a good stopping point and everything is saved, then emit the paste-ready
prompt to continue in a fresh thread (project id + checkpoint + next phase). Persist and
offer the reset rather than letting context balloon.

## Escalation to the full path

Switch to `video-journey.md` only if the piece needs a full Story Structure across
multiple scenes/sequences, becomes cumulative or long-form (Long-Work Stewardship), or the
artist wants the full Video Medium Plan process. Carry over the Style Direction, continuity
scan, and any shot list already drafted.

## Output

Return the Compact Video Authoring Packet, the finalized Video Medium Plan Record when
validation has been run, the Video Critic Review Record when review has run, the
storyboard generation policy, and open questions. Storyboard sheet generation and its
Output Records follow on explicit approval.
