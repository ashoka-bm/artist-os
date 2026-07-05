# Video Provider Research Draft Space

This draft space collects reference analysis for video-provider prompt exports after Artist OS reaches the storyboard-ready package.

The canonical Video Journey stops at the `Video Medium Plan` and storyboard-ready package. This area explores what may happen after that boundary: provider-specific prompt exports, platform-specific material requirements, and repeatable video-output journeys. Nothing here changes the main skill contract until the pattern has enough evidence and is intentionally promoted.

## Boundary

- Main Artist OS video path stops at storyboard-ready planning.
- Draft provider work starts after storyboard approval.
- Provider-backed generation still requires explicit approval for the exact call or approved batch.
- Provider-specific rules must not leak into `Video Medium Plan`, shared Visual Dynamics, or core Artist OS theory.
- Third-party references are treated as inputs for analysis. Do not copy large passages or prompt packs into this repo.

## Research Flow

1. Add each reference to `references/reference-manifest.json`.
2. Write a short analysis in `references/analyses/`.
3. Extract reusable patterns into `patterns/`.
4. Map provider-specific behavior into `providers/`.
5. Map end-product journeys into `journeys/`.
6. Update `grids/video-output-journey-grid.md` when a repeated video type emerges.

## Promotion Rule

A draft pattern can move toward implementation only when it meets all conditions:

- The pattern appears across enough references or tests to outgrow one author's habit.
- The pattern preserves Artist Meaning, Beat Plan traceability, and Video Medium Plan provenance.
- The pattern belongs clearly as a provider adapter, journey template, schema field, or guidance note.
- The pattern does not weaken the provider-neutral Video Journey.

## Current Position

The first draft cluster covers Higgsfield and Seedance-style creator-clone video prompts: talking heads, handheld vlog one-takes, static walk-past b-roll, and multi-cut b-roll.

The newer draft cluster expands beyond prompt export into post-storyboard production routes: real-footage montage, generated explainers, hybrid source-support videos, local rigged character animation, render runtime governance, cost checkpoints, and post-render validation. These files are research notes, not production behavior.

The Seedance draft cluster now includes both a compact checklist and a stricter cinematic prompt protocol. The protocol covers English prompt shape, reference-tray tags, audio tags, shot-list handoff, start-frame handling, and GPT Image 2 reference prep. It remains a provider-export draft, not canonical Video Journey behavior.

See [Seedance Cinematic Reference Section Placement](seedance-cinematic-section-placement.md) for the current section-by-section implementation map.
