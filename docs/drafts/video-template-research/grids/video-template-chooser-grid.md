# Draft Video Template Chooser Grid

Status: research draft.

Use this grid after Format Intent and before scene/shot planning hardens. It maps the user's desired video into the correct planning layer.

## Route

```text
Video goal
  -> narrative_depth
  -> Story Template, Micro-Journey Template, or Asset Purpose Brief
  -> Cultural Format Structure
  -> Video Medium Plan payload
  -> storyboard-ready package
  -> provider export only after storyboard approval
```

## Chooser Grid

| User Goal Signal | Narrative Depth | Primary Template Layer | Good Starting Template | Cultural Format Structure | Video Medium Plan Must Carry |
| --- | --- | --- | --- | --- | --- |
| Personal story, sketch, mini-doc, short film, story-led trailer | `full_story` | Story Template | Observation Reframe Move, Need Cost Changed Return, Plant Payoff Twist, Trailer Stakes Tease | `scripted_scene`, `sitcom_sketch_scene`, `trailer_teaser`, `youtube_explainer_deep_dive` | `story_template_ref`, Beat Plan story turns, scenes, shots, transitions, audio posture. |
| Product reveal, unboxing, creator proof, social proof, fit check | `micro_journey` | Micro-Journey Template | `product_reveal`, `unboxing_reveal`, `ugc_testimonial`, `fashion_fit_check` | `short_social_hook_loop`, `influencer_ugc_testimonial`, `fashion_campaign_film` | `micro_journey_template_ref`, hook, object of attention, proof/payoff, ending beat. |
| Before/after, how-to tip, problem/solution demo | `micro_journey` | Micro-Journey Template | `quick_before_after_demo`, `problem_solution_demo`, `how_to_tip_demo` | `educational_reel_micro_lesson`, `product_explainer_demo`, `short_social_hook_loop` | `micro_journey_template_ref`, problem/mistake, proof, result/payoff, ending cue. |
| Social receipt, waitlist proof, review/rating proof | `micro_journey` candidate | Micro-Journey candidate | `social_proof_receipt` | `short_social_hook_loop`, `influencer_ugc_testimonial`, `product_explainer_demo` | Use `ugc_testimonial` plus rationale/traceability note until schema promotion. |
| B-roll package, title cards, motion graphics, loops, transitions | `utility_sequence` | Asset Purpose Brief | `utility_broll_coverage_set`, `utility_title_chapter_cards`, `utility_graphics_identity_package`, `utility_looping_background_or_hold` | Usually none, or project-specific video format note | `asset_purpose_brief`, placement, motion behavior, loop/resolution, style constraints, success criteria. |
| YouTube explainer or educational video | Depends | Story, Micro-Journey, or Utility | Inquiry Loop, `how_to_tip_demo`, `utility_explainer_diagram_insert` | `youtube_explainer_deep_dive`, `educational_reel_micro_lesson` | Learning objective, thesis, chapter scenes, evidence visuals, VO/text refs. |
| Product demo or launch film | Depends | Micro-Journey or Utility, Story if narrative launch | `product_reveal`, `utility_product_demo_walkthrough`, Desire Funnel | `product_explainer_demo`, `product_launch_hero_film` | Product visibility, user job, feature proof, benefit claims, CTA. |
| Music video, fashion film, montage | Depends | Micro-Journey, Utility, or Story | `creator_showcase_moment`, `fashion_fit_check`, Plant Payoff Twist | `music_video_performance_concept`, `fashion_campaign_film`, `montage_mood_film` | Song/section timing, motif map, wardrobe/reference continuity, performance setups. |
| Speech opener or keynote hook | `micro_journey` or `utility_sequence` | Micro-Journey or Utility opener | Contrast Sparkline, Observation Reframe Move, `how_to_tip_demo` | `speech_opening_keynote_hook` | Opening seconds, audience relevance, speaker blocking, slide/prop refs, text/VO refs. |

## Current Schema Caveat

The current schema accepts nine `micro_journey_template_ref` ids:

- `unboxing_reveal`
- `product_reveal`
- `ugc_testimonial`
- `fashion_fit_check`
- `quick_before_after_demo`
- `problem_solution_demo`
- `how_to_tip_demo`
- `creator_showcase_moment`
- `day_in_the_life_signal`

Research candidates such as `social_proof_receipt` and `order_pack_ritual` should not be written into `micro_journey_template_ref` until the schema enum is expanded. Use the closest schema-supported id, then record the candidate in rationale or traceability notes.

## Promotion Questions

- Does `social_proof_receipt` deserve schema promotion after one more proof-type walkthrough?
- Should Utility Sequence Templates become a first-class template ref, or remain inside `asset_purpose_brief`?
- Should video Cultural Format Structures live inside the existing canonical Cultural Format Structure Library or remain video-only?
- Which reviewer checks belong in Video Critic Review before promotion?
