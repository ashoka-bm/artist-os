# Draft Decision 0017: Seedance Cinematic Reference Placement

Status: proposed.

Date: 2026-06-26

## Decision

The Dan Kieft Cinematic Seedance reference will be split by authority instead of implemented as one monolithic skill block.

Reusable directing guidance enters early during Video Medium Plan Shot Logic and Storyboard Shot Design. This includes coverage economy, shot scale progression, camera angle meaning, one primary camera movement per shot, tension through withholding or reveal, and directorial pushback when a camera choice weakens the beat.

Reference-prep guidance enters during Reference Strategy, Visual Reference Sheet Plan drafting, Reference Inventory, and Reference Readiness. Recurring or meaning-bearing characters, locations, products, objects, and props can be promoted before storyboard export when drift would weaken Artist Meaning, blocking, or audience trust.

Aspect ratio is an early format commitment carried by `VideoMediumPlan.video_format.aspect_ratio`. It should be checked during storyboard prompt packaging, reference-output planning when the reference must match a downstream frame, provider export, and final render validation. Exact resolution usually remains provider/request specific unless the output format requires it.

GPT Image 2 is the default implemented image-generation route for approved reference outputs, storyboard stills, start frames, identity plates, turnarounds, macro detail cards, and calibration stills until another image generator is intentionally promoted. Domain records remain provider-neutral; GPT Image 2 belongs in the Generation Approval packet or provider request layer.

Provider-specific prompt behavior stays after storyboard approval in Production Route, Provider Media Bindings, and Provider Export. This includes English prompt shape, `@image` / `@audio` tags, current reference tray mapping, Seedance duration brackets, 24fps language, prompt packet formatting, moderation preflight, and output-only provider packet rules.

Long or multi-part generation continuity is split by authority: the Video Medium Plan records continuity needs, while Production Route and Provider Media Bindings decide when the last frame of one generated clip becomes the starting frame of the next clip. Generated clips and extracted continuity frames require normal Output Record handling.

## Rationale

The document mixes three kinds of information:

- universal video-direction judgment;
- provider-neutral continuity and reference planning;
- Seedance-specific prompt syntax and platform behavior.

Putting all of it into the main Video Medium Plan would violate the provider-neutral core and make Seedance shape the story too early. Keeping all of it after storyboard approval would waste the best directorial guidance, because camera angle and shot scale are useful while planning the storyboard.

## Consequences

- Shot Design can use the good camera and coverage advice before provider selection.
- Video Critic Review can check whether camera choices serve the Beat's emotional job.
- Reference Inventory remains provider-neutral while still preparing the right reference outputs.
- Aspect ratio becomes a cross-stage check rather than only a prompt setting.
- GPT Image 2 can be used pragmatically as the first implemented image route without leaking provider syntax into core records.
- Last-frame continuity can support long generations without turning Seedance batching into story authority.
- Provider Export can be strict about Seedance syntax without changing the core video plan.
- A future Seedance adapter can consume approved storyboard shots and accepted references without inventing story, camera rationale, or continuity requirements.

## Current Draft Homes

- Section placement map: `docs/drafts/video-provider-research/seedance-cinematic-section-placement.md`
- Reusable directing note: `docs/drafts/video-template-research/direction-notes/cinematic-coverage-and-camera-direction.md`
- Seedance provider protocol: `docs/drafts/video-provider-research/providers/seedance-cinematic-prompt-protocol.md`
- Reference and provider boundaries: `docs/adr/0002-provider-neutral-core.md`, `docs/adr/0009-video-uses-shared-visual-planning.md`, `docs/adr/0011-promoted-reference-inventory-and-storage.md`
