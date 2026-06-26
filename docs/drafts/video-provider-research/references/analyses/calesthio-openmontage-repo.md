# OpenMontage Repository Analysis

## Reference

- Reference id: `ref_calesthio_openmontage_repo_001`
- Title: `calesthio/OpenMontage`
- Source path: `https://github.com/calesthio/OpenMontage`
- Date analyzed: 2026-06-25
- Provider or platform: Remotion, HyperFrames, FFmpeg, open footage sources, stock APIs, image/video/TTS/music providers
- Reference type: GitHub repository, agentic video production system, pipeline architecture
- Reuse policy: analyze and rewrite in Artist OS language; do not copy code, bundled skills, or provider instructions

## What It Is

OpenMontage is a pipeline-driven video production system for AI coding assistants. It treats the agent as the producer and uses Python tools for execution, persistence, provider selection, media processing, and validation.

For Artist OS, the repo is useful because it models what can happen after a storyboard-ready package: production path selection, capability checks, asset planning, source retrieval, timeline assembly, renderer selection, cost governance, and render review. This is broader than a provider prompt pack.

## Major Subsystems

- Pipeline manifests in `pipeline_defs/` that define stages, required artifacts, tools, review focus, success criteria, and approval defaults.
- Stage director skills in `skills/pipelines/` that tell the agent how to execute each stage.
- Canonical artifacts such as research brief, proposal packet, script, scene plan, asset manifest, edit decisions, render report, final review, and publish log.
- Tool registry and provider selectors that expose available capabilities instead of assuming one provider path.
- Cost tracker and decision log for budget estimates, reserves, actual spend, alternatives, and approvals.
- Composition runtimes: Remotion for React-based programmatic video, HyperFrames for HTML/CSS/GSAP video, and FFmpeg for stitching/encoding.
- Validation gates: pre-compose checks, ffprobe review, frame sampling, audio analysis, subtitle checks, and delivery-promise enforcement.

## Video And Content Types

- Animated explainer.
- Talking head.
- Screen demo.
- Clip factory.
- Podcast repurpose.
- Cinematic edit.
- Animation-first video.
- Character animation.
- Hybrid source-plus-support video.
- Avatar spokesperson.
- Localization and dubbing.
- Documentary montage from retrieved real footage.

## Assumed Inputs

- User brief or topic.
- Optional reference video for transcript, pacing, style, keyframe, and scene analysis.
- Target platform, duration, aspect ratio, and delivery promise.
- Available provider menu and configured local tools.
- Optional source footage, screen recordings, podcast audio, product material, or character references.
- Budget and provider approval thresholds.
- Music, narration, subtitle, and publish requirements.

## Prompt And System Patterns

OpenMontage turns a video request into a production routing problem before it becomes a prompt-writing problem.

The reusable pattern is:

1. Identify the output family.
2. Select the matching production pipeline.
3. Inspect available capabilities and cost paths.
4. Create a proposal with creative direction, runtime, providers, budget, and risks.
5. Get approval before expensive generation or major creative commitment.
6. Produce canonical stage artifacts.
7. Assemble assets into edit decisions.
8. Render with the locked runtime.
9. Validate the finished video before presenting it.

## Reusable Patterns

- Treat post-storyboard work as pipeline selection, not one universal video export.
- Keep stage artifacts explicit so each step has a handoff contract.
- Separate source-led, generated, hybrid, motion-graphics, and character-animation paths.
- Lock render runtime and provider choices after approval; do not silently swap if the chosen path fails.
- Show capability availability before proposing a production path.
- Estimate cost before generation and reconcile cost after execution.
- Use real footage retrieval as a distinct journey from generated clip prompting.
- Validate output against the delivery promise, not just file existence.
- Keep renderer choice tied to visual grammar: React scene stack, HTML/GSAP motion, or direct FFmpeg assembly.

## Failure Modes

- Provider or render runtime silently changes after approval.
- The system promises motion-led video but produces a slideshow-like render.
- Asset generation starts before cost, runtime, or concept approval.
- Reference video analysis is used as imitation rather than transformed structure.
- Real-footage montage loses provenance, license, or source diversity.
- Mixed source/generated videos let support layers overpower source truth.
- Captions, music, or audio levels fail late because they were not planned early.
- Final render is accepted without frame, duration, audio, subtitle, or delivery-promise checks.

## Conflicts

OpenMontage is an executable production system with provider calls, local renderers, package setup, and bundled skills. Artist OS should not absorb it wholesale into the core Video Journey.

The repo also assumes the agent can run full production stages. Artist OS currently needs to preserve the boundary: storyboard-ready planning is canonical; provider execution and finished rendering remain draft downstream work until specific adapters are designed and approved.

## Mapping To Artist OS

- Pipeline selection maps to a future `Video Production Route` after the Video Storyboard.
- Proposal packet maps to a future post-storyboard production proposal with provider/runtime/cost choices.
- Scene plan overlaps with Artist OS Video Storyboard, but should not replace the Video Medium Plan.
- Asset manifest maps to Output Records, provider media bindings, and source provenance.
- Edit decisions map to a future timeline or assembly plan.
- Render report and final review map to Output Record plus Output Critic Review.
- Documentary montage suggests a retrieval-first journey that uses open footage rather than generated clips.
- Character animation suggests a deterministic local animation journey with rig plans and pose libraries, separate from Seedance-style image-to-video.

## Draft Fields To Consider

- `production_route`
- `reference_video_analysis_ref`
- `capability_menu_snapshot`
- `provider_options_considered`
- `render_runtime_options_considered`
- `selected_render_runtime`
- `runtime_lock_gate_ref`
- `cost_estimate_ref`
- `budget_approval_ref`
- `asset_manifest_ref`
- `edit_decisions_ref`
- `delivery_promise`
- `pre_compose_validation_ref`
- `render_report_ref`
- `post_render_review_ref`

## Open Questions

- Should Artist OS model post-storyboard production as one `Production Route` record or separate provider adapter records per output family?
- Which stage artifacts belong in core Artist OS, and which should stay adapter-local?
- How should Artist OS represent real-footage retrieval while preserving license, provenance, and source meaning?
- Should Remotion and HyperFrames be treated as providers, render runtimes, or implementation backends?
- What is the minimum render-review record needed before an Output Artifact can be considered usable?
- How should reference video analysis preserve structure and pacing without copying the original work too closely?
