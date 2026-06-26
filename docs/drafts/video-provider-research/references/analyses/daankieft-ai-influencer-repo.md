# DaanKieft AI Influencer Repository Analysis

## Reference

- Reference id: `ref_daankieft_ai_influencer_repo_001`
- Title: `DaanKieft/ai-influencer`
- Source path: `https://github.com/DaanKieft/ai-influencer`
- Date analyzed: 2026-06-24
- Provider or platform: Higgsfield, Seedance 2.0, GPT Image 2, Marketing Studio, Higgsfield Soul, Virality Predictor
- Reference type: GitHub repository, app implementation, bundled skills, prompt docs
- Reuse policy: analyze and rewrite in Artist OS language; do not copy code or long prompt docs

## What It Is

This repository is a local-first AI Influencer Studio. It combines a React/Vite app, browser-local influencer records, Higgsfield OAuth and generation utilities, prompt builders, bundled Higgsfield skills, and reference docs for influencer stills, Seedance video, product ads, and campaign generation.

For Artist OS, the repository is useful because it shows a full production system around identity continuity, reference slots, prompt builders, media upload roles, campaign planning, batch generation, and post-generation analysis. It is not just a prompt guide.

## Major Subsystems

- Influencer creation flow: profile, references, physical description, backstory, model choice, and three image variations.
- Character and product reference sheets: full-body influencer sheets and six-panel product sheets.
- Photo Studio: reference-driven still generation for influencer images.
- Seedance influencer video guide: creator/influencer prompt rules, recipes, identity lock, and failure modes.
- Higgsfield generation utilities: upload, media caching, image generation, video generation, job polling, and resume behavior.
- Higgsfield bundled skills: generic generation, Soul identity, product photoshoot, and content factory.
- Marketing Studio content factory: campaign planning, UGC formats, preset routing, batch permission gates, asset packs, scheduling, and cost reporting.
- Virality Predictor route: finished-video analysis for hook, retention, and attention.

## Video And Content Types

- UGC talking head.
- Product reveal.
- Lifestyle plandid.
- GRWM or mirror video.
- Brand integration.
- Street interview.
- Unboxing.
- Product review.
- ASMR-style product handling.
- TV spot, hyper-motion, wild-card, virtual try-on, and product showcase campaign assets.
- Still-image influencer photo sets.
- Character reference sheets and product reference sheets.

## Assumed Inputs

- Influencer identity image or generated influencer still.
- Optional character sheet, close-up face references, wardrobe references, product references, and prop references.
- Product image or product URL for Marketing Studio.
- Optional avatar or Higgsfield Soul reference.
- Exact transcript or audio for dialogue-led video.
- Campaign goal, product category, video count, date range, and platform use.
- Approved style still or reference images when producing consistent visual packages.

## Prompt And System Patterns

The repo separates prompt behavior by task:

- GPT Image 2 stills use concise or structured photographic prompts depending on whether the task is fresh image generation or reference-driven editing.
- Photo Studio treats reference-conditioned images as edits. It gives placement, pose, scene, lighting, camera, and framing without re-describing the reference.
- Seedance video uses shot-family formatting, identity locks, reference scoping, and anti-failure rules.
- Marketing Studio ads use presets, hooks, settings, products, avatars, modes, and batch-level campaign planning.
- Campaign generation uses a staged flow: research, plan, batch generation, publishing, and cost comparison.

## Reusable Patterns

- Treat identity continuity as infrastructure, not a per-prompt afterthought.
- Separate identity, wardrobe, close-up face detail, product, style, and scene references by role.
- Create calibration artifacts before video generation when character consistency matters.
- Store generated prompts, selected images, model choice, aspect ratio, references, and backstory context with the influencer record.
- Use different prompt strategies for reference edits versus open-ended generation.
- Route content by end product: influencer still, reference sheet, UGC video, product ad, campaign batch, motion package, or analysis report.
- Use provider capability limits to constrain journey design before proposing output shapes.
- Add permission gates before paid or batch provider generation.
- Use finished-video analysis as a separate downstream review route.

## Failure Modes

- Identity drift across generated influencer images or campaign clips.
- Outfit or product role confusion when several reference images are passed.
- Re-describing a strong identity reference and diluting the edit instruction.
- Text/logo errors in generated stills or ad cards.
- Provider model mismatch: using a general video model for Marketing Studio ad work or vice versa.
- Campaign plans that exceed provider clip duration limits.
- Product or logo visibility loss in UGC/product shots.
- Random presenter casting when no avatar is passed.
- Generated clips failing mid-batch without retry tracking.

## Conflicts

The repository includes production code, bundled third-party skills, and copyrighted prompt docs. Artist OS should not import them wholesale. It should extract patterns in original language and keep provider execution separate from the neutral Video Journey.

The repo also contains app-level assumptions that may not fit Artist OS directly: influencer monetization language, local browser storage, Antigravity/Claude setup, Higgsfield OAuth, and direct generation calls. Artist OS needs durable provenance, gate records, Output Records, and explicit generation approval.

## Mapping To Artist OS

- Influencer profile maps to Character Template plus Source Record and reference assets.
- Character sheet maps to Visual Reference Sheet Plan and generated/imported Output Records.
- Photo Studio stills map to Image Journey or supporting calibration outputs.
- Seedance video prompting maps to post-storyboard provider export drafts.
- Marketing Studio campaign planning maps to a future campaign/package journey, not the core Video Medium Plan.
- Virality Predictor maps to a future Output Critic or Performance Signal path after a generated clip exists.
- Higgsfield upload roles map to provider adapter media bindings, not core schema fields.

## Draft Fields To Consider

- `identity_system_required`
- `character_sheet_ref`
- `close_up_face_refs`
- `wardrobe_ref_scope`
- `product_ref_scope`
- `provider_media_bindings`
- `campaign_format_bucket`
- `marketing_studio_preset`
- `hook_id_or_name`
- `setting_id_or_name`
- `avatar_strategy`
- `generation_batch_gate_ref`
- `performance_analysis_ref`

## Open Questions

- Should Artist OS model AI influencer identity as a Character Template, a dedicated Persona Record, or a provider-specific identity kit?
- Which influencer journeys belong in Artist OS's artistic transformation system, and which are better treated as commercial campaign tooling?
- Should Marketing Studio campaign planning live under release-package planning, a future ad-campaign module, or a separate provider adapter?
- How should Artist OS represent provider media roles such as image, start image, audio, product, avatar, hook, and setting without contaminating core records?
- What minimum Output Record metadata is needed for generated campaign batches and performance analysis?
