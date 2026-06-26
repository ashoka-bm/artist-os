# Draft Pattern: Render Runtime And Provider Governance

Status: research draft.

OpenMontage separates provider choice from render runtime choice. A video may use generated assets, retrieved clips, local TTS, music tools, Remotion, HyperFrames, and FFmpeg in one production path.

## Draft Principle

Artist OS should not hide technical path choices once they affect cost, quality, style, or feasibility. The production proposal should show the meaningful options and lock the approved path before execution.

## Choices To Surface

- Video generation provider, when generated motion is needed.
- Image generation provider, when stills or reference sheets are needed.
- TTS or voice path.
- Music source.
- Footage source.
- Render runtime: Remotion, HyperFrames, FFmpeg, or another backend.
- Fallback path and quality tradeoff.

## Governance Rules To Consider

- Provider-backed generation needs explicit approval.
- Runtime selection should happen before asset production when it shapes the visual language.
- If the approved runtime or provider fails, stop and propose alternatives.
- Record options considered, selected path, rationale, cost estimate, and approval reference.

## Artist OS Mapping

These choices belong in post-storyboard production records or provider adapters. They should not become fields inside the neutral Video Medium Plan unless repeated evidence shows a stable cross-provider requirement.
