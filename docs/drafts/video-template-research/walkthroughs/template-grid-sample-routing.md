# Template Grid Sample Routing

Status: research draft.

These samples test whether the chooser grid covers common video requests without forcing every video into full story shape.

## Samples

| Sample Request | Narrative Depth | Template Choice | Cultural Format | Why |
| --- | --- | --- | --- | --- |
| 90s sitcom version of me where each career gets replaced by AI | `full_story` | Need Cost Changed Return plus repeated escalation sketch candidate | `sitcom_sketch_scene` | It has setup, escalation, comic reversal, consequence, and a fourth-wall payoff. |
| Explainer video toolkit motion graphics package | `utility_sequence` | `utility_graphics_identity_package` plus `utility_title_chapter_cards` | project-specific motion graphics package | It is a reusable asset package, not a story arc. |
| Approved still frame becomes a short B-roll insert | `utility_sequence` | `utility_looping_background_or_hold` or `utility_broll_coverage_set` | project-specific B-roll insert | The job is coverage/reuse under narration. |
| New product shown in 15 seconds for social | `micro_journey` | `product_reveal` | `short_social_hook_loop` | The object of attention is the product and the payoff is value proof. |
| Boxed creator kit opening on camera | `micro_journey` | `unboxing_reveal` | `short_social_hook_loop` | The journey is curiosity, opening, tactile reveal, and product payoff. |
| Customer says she was skeptical, tried it, and now trusts it | `micro_journey` | `ugc_testimonial` | `influencer_ugc_testimonial` | The audience movement is skepticism to trust through lived proof. |
| Fashion campaign showing a new lookbook in motion | `micro_journey` | `fashion_fit_check` or `creator_showcase_moment` | `fashion_campaign_film` | The point is identity, garment movement, and brand desire. |
| Speech opening about AI creativity | `micro_journey` | Observation Reframe Move compressed into a micro-journey | `speech_opening_keynote_hook` | The opener needs attention, relevance, a reframe, and a reason to listen. |

## Findings

- The four-layer split handles all eight samples.
- Existing schema-supported micro-journeys cover most near-term social/product/fashion/creator cases.
- The strongest schema candidates from research are `problem_solution_demo`, `how_to_tip_demo`, and `social_proof_receipt`.
- `order_pack_ritual` is useful, but it may belong in an ecommerce/lifestyle extension rather than the core enum.
- Utility sequences do not need a template ref yet if `asset_purpose_brief` stays strong.
- Video-specific Cultural Format Structures need more testing before canonical promotion.

## Next Tests

- Test `problem_solution_demo` against a product/service request.
- Test `how_to_tip_demo` against a creator education request.
- Test `social_proof_receipt` against review/rating/comment proof.
- Test a documentary mini-profile because none of the current samples cover it cleanly.
