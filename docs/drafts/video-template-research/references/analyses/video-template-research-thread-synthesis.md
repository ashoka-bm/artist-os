# Video Template Research Thread Synthesis

Status: research draft.

Date: 2026-06-26.

This note consolidates the four background research threads:

- Story Templates.
- Micro-Journey Templates.
- Utility Sequence Templates.
- Cultural Format Structures.

The threads stayed research-only. They did not edit files, call providers, or generate media.

## Main Finding

The current Video Journey spine is sound:

1. Story Templates belong in Story Journey / Beat Plan.
2. Micro-Journey Templates belong in Video Medium Plan routing when the video needs compact hook-to-payoff movement.
3. Utility Sequence Templates belong in the Video Medium Plan `asset_purpose_brief` when the video is a functional asset package.
4. Cultural Format Structures belong after accepted output shape, where they guide audience-facing format grammar.
5. Provider export rules belong after storyboard approval.

Do not merge these layers. They answer different questions.

## Recommended Starting Library Sizes

| Library | Starting Count | Reason |
| --- | ---: | --- |
| Story Templates | 13 | Covers film, ads, journalism, speeches, creator education, explainers, and short-form story movement without listing every named craft framework. |
| Micro-Journey Templates | 11 | Keeps the current 9 schema-supported entries and leaves 2 research candidates for later proof. |
| Utility Sequence Templates | 9 | Covers the main functional asset patterns without inventing narrative arcs for asset packages. |
| Cultural Format Structures | 14 | Covers the most useful recognizable video grammars for Artist OS and AI-video planning, including documentary mini-profile. |

## Current Implementation Boundary

The current Video Medium Plan schema already supports:

- `narrative_depth`;
- `story_template_ref`;
- `micro_journey_template_ref`;
- `asset_purpose_brief`.

The current schema-supported micro-journey ids are:

- `unboxing_reveal`;
- `product_reveal`;
- `ugc_testimonial`;
- `fashion_fit_check`;
- `quick_before_after_demo`;
- `problem_solution_demo`;
- `how_to_tip_demo`;
- `creator_showcase_moment`;
- `day_in_the_life_signal`.

The remaining research candidates are:

- `social_proof_receipt`;
- `order_pack_ritual`.

These two should remain draft candidates until a separate schema promotion decision expands `micro_journey_template_ref`.

## Sources Clustered By Use

Story and narrative sources:

- Aristotle / Poetics for whole movement and beginning-middle-end logic.
- Pixar in a Box / Khan Academy for story spine thinking.
- Save the Cat, Dan Harmon, and StudioBinder for screenwriting and video structure.
- Duarte / TED and Monroe's Motivated Sequence for persuasion and speech movement.
- Nieman Storyboard, American Journalism Handbook, and NN/g for anecdote, nut graf, accordion, and inverted-pyramid patterns.
- Copyhackers, Copyblogger, Smart Insights, and Buffer for AIDA, PAS, and before-after-bridge patterns.

Short-form and marketing sources:

- TikTok Creative Codes and TikTok creative best practices.
- YouTube / Google creator and video-ad guidance.
- Meta Reels guidance.
- Shopify, Cohley, and Influee for UGC, ecommerce, unboxing, and testimonial patterns.
- FTC endorsement guidance for testimonial, review, sponsorship, and proof constraints.

Utility and format sources:

- TechSmith, Adobe, Inside the Edit, and Vimeo for B-roll, shot lists, lower thirds, and utility coverage.
- Smashing Magazine and broadcast-design references for motion graphics packages.
- Wistia and Atlassian / Loom for explainer and product-demo structure.
- StudioBinder for trailers, montage, music video, scenes, and transitions.
- Vanderbilt and educational-video research for learning-video segmenting and signaling.
- Kosmorama and fashion-film references for fashion campaign format grammar.
- Toastmasters and Duarte for speech openings and keynote hooks.

## Implementation Implications

- Keep promoted ids and draft candidates separated in the chooser.
- Add a chooser grid that maps video goal to `narrative_depth`, template family, cultural format, and Video Medium Plan payload.
- Run sample routing before promotion.
- Add reviewer checks later for hook honesty, payoff integrity, proof provenance, utility usefulness, and false-story inflation.

## Remaining Research Gaps

- Build a small annotated corpus of real videos to test coverage across Shorts, TikTok/Reels, YouTube explainers, trailers, UGC ads, fashion films, and product videos.
- Decide whether remaining candidate micro-journey ids belong in the schema enum or stay as Cultural Format Structure notes.
- Research podcast/interview clips, live-event recaps, game trailers, and livestream promos.
- Add claim-safety rules for testimonials, before/after content, reviews, ratings, sponsored creator material, and product claims.
- Test whether `storyboard_shots` are too heavy for pure utility packages or whether Asset Purpose Brief can keep them tractable.
