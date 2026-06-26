# Research-Backed Video Cultural Format Structure Library

Status: research draft.

Cultural Format Structures describe audience-facing video grammar. They do not replace Story Structure, Micro-Journey Templates, Utility Sequence Templates, or Video Medium Plan execution fields.

Use these after accepted output shape and before scene/shot planning hardens.

## Starting Set

| Format Structure | Audience Expectation | Typical Parts | Rhythm | Compatible Narrative Depth | Template Dependencies | Video Medium Plan Must Carry |
| --- | --- | --- | --- | --- | --- | --- |
| `short_social_hook_loop` | Instant recognition, fast payoff, often rewatchable loop. | First-frame hook, context, proof/escalation, payoff, loop/CTA. | Fast cuts, no dead air. | `utility_sequence`, `micro_journey` | Micro-Journey by default. | Hook timing, safe-zone text, loop behavior, CTA, shot density. |
| `educational_reel_micro_lesson` | One useful idea quickly. | Misconception/problem, promise, teach step, example, recap/save cue. | Tight chunks with visual signaling. | `utility_sequence`, `micro_journey` | Utility Sequence; Micro-Journey when moving from confusion to clarity. | Learning objective, segment labels, signaling, text refs. |
| `youtube_explainer_deep_dive` | Orientation, credible explanation, satisfying payoff. | Hook, stakes, thesis/map, chapters, examples, synthesis, close. | Slower than Shorts with retention resets. | `utility_sequence`, `micro_journey`, sometimes `full_story` | Micro-Journey plus utility sections; Story Template for case-led explainers. | Chapter scenes, evidence visual refs, VO/text refs. |
| `product_explainer_demo` | Understand what it is, why it matters, and how it works. | Problem, solution, how it works, benefits, CTA. | Often 60-120 seconds; solution appears early. | `utility_sequence`, `micro_journey` | Utility Sequence primary. | Product shots, demo steps, benefit claims, CTA placement. |
| `product_launch_hero_film` | Anticipation, reveal, proof, memorable brand promise. | Tension/opportunity, reveal, capability montage, human use, proof, CTA. | High first cue, multiple peaks. | `micro_journey`, sometimes `full_story` | Micro-Journey; Story Template for narrative launch films. | Product timing, reveal shot, proof beats, CTA. |
| `trailer_teaser` | Premise, genre, stakes, escalation, withheld resolution. | Cold open, premise, threat/problem, escalation montage, title/tag. | Strong start, pullback, build to peak. | `full_story` | Approved Story Template/Beat Plan. | Source-beat mapping, spoiler limits, title/music cues. |
| `montage_mood_film` | Meaning through accumulation, contrast, rhythm, and texture. | Motif, variations, compression/escalation, turn, final image. | Music-led; cuts create logic. | `utility_sequence`, `micro_journey`, sometimes `full_story` | Micro-Journey or Utility Sequence. | Motif map, juxtaposition logic, transition rhythm. |
| `music_video_performance_concept` | The song becomes visible through performance, concept, story, or atmosphere. | Intro, verse system, chorus lift, bridge/turn, final image. | Locked to song structure. | `micro_journey`, `full_story`, `utility_sequence` | Song-section Micro-Journey; Story Template for narrative music videos. | Lyric/audio refs, section timing, performance setups. |
| `scripted_scene` | A contained situation with pressure and change. | Establish, catalyst, rising pressure, dilemma/decision, changed state/exit. | Beat changes, not montage speed. | `full_story` | Scene Story Template. | Scene beats, blocking, shot progression, dialogue refs. |
| `sitcom_sketch_scene` | Comic premise, escalation, reversals, laugh/tag. | Premise, setup, attempts, complication, punch/payoff, tag. | Quick setup-punch cycles. | `micro_journey`, `full_story` | Comic Scene Template plus joke micro-patterns. | Comic beats, reaction shots, timing, dialogue refs. |
| `influencer_ugc_testimonial` | Native-feeling personal proof, not a polished commercial. | Creator hook, problem/experience, product/use, proof/result, recommendation/CTA. | Fast but conversational. | `utility_sequence`, `micro_journey` | Utility Sequence. | Creator role, proof shots, disclosure/CTA refs, product visibility. |
| `fashion_campaign_film` | Clothes as world, identity, movement, and desire. | Visual thesis, look/world intro, movement/texture sequence, attitude turn, brand signal. | Atmospheric; often music-forward. | `micro_journey`, `full_story`, `utility_sequence` | Micro-Journey by default. | Look priorities, wardrobe continuity, movement vocabulary, final brand cue. |
| `speech_opening_keynote_hook` | Attention, relevance, credibility, and reason to listen. | Hook, topic, relevance, credibility, preview or contrast turn. | Direct and spoken. | `utility_sequence`, `micro_journey`, sometimes `full_story` | Utility opener; Micro-Journey for contrast-based openings. | Opening seconds, speaker blocking, slide/prop refs, text/VO refs. |
| `documentary_mini_profile` | Meet a specific person through observed behavior, context, and a small but meaningful turn. | Human entry, observed work, context/nut graf, tension or common misread, proof through action/decision/artifact, return, kicker. | Observational, specific, patient enough for proof; 60-90 seconds in compact form. | `micro_journey`, sometimes `full_story`, limited `utility_sequence` | Micro-Journey by default; Story Template only for larger life/career arcs. | Human subject/role, observed-work scenes, nut graf, tension, proof decision/artifact, return/kicker image, sparse text refs. |

## Placement Rules

- Use Cultural Format Structure to make the video culturally legible.
- Use Story Template to govern deep movement.
- Use Micro-Journey Template for compact hook-to-payoff movement.
- Use Utility Sequence Template for functional asset packages.
- Use provider export only after storyboard approval.

## Gaps Before Promotion

- Add video-specific Cultural Format Structure entry format if canonical promotion happens.
- Decide whether video formats share the existing `docs/structure-library/cultural-format/` family or need a video-only subsection.
- Research podcast/interview clips, live-event recap, game trailer, livestream promo, and accessibility/caption standards.
