# Story Structures

Story Structure entries describe reusable movement patterns. They help Artist OS adapt emotional, symbolic, narrative, rhetorical, or experiential movement before any Medium Plan chooses an output shape.

Read this index first, then open only the entry that matches the project.

| Entry id | File | Use when |
| --- | --- | --- |
| `three_act_structure` | [three-act-structure.md](three-act-structure.md) | The work needs setup, escalation, climax, and resolution. |
| `hero_journey` | [hero-journey.md](hero-journey.md) | The work centers on threshold crossing, ordeal, transformation, and return. |
| `freytag_dramatic_arc` | [freytag-dramatic-arc.md](freytag-dramatic-arc.md) | The work rises to a peak turn, then follows consequence into final state. |
| `kishotenketsu` | [kishotenketsu.md](kishotenketsu.md) | The work needs introduction, development, turn, and reconciliation without requiring conflict as the main engine. |
| `problem_reframe_return` | [problem-reframe-return.md](problem-reframe-return.md) | The work starts with a felt problem, changes the frame, then returns the audience to action, perception, or meaning. |
| `save_the_cat_beat_sheet` | [save-the-cat-beat-sheet.md](save-the-cat-beat-sheet.md) | The work needs commercial beat visibility, midpoint pressure, low point, and opening/final state contrast. |
| `dan_harmon_story_circle` | [dan-harmon-story-circle.md](dan-harmon-story-circle.md) | The work needs a compact cycle of need, threshold, cost, return, and change. |
| `seven_point_structure` | [seven-point-structure.md](seven-point-structure.md) | The work needs plot-driven turns, pinch points, midpoint reversal, climax, and resolution. |
| `fichtean_curve` | [fichtean-curve.md](fichtean-curve.md) | The work should begin in crisis and escalate through repeated pressure toward climax and consequence. |
| `in_medias_res_revelation` | [in-medias-res-revelation.md](in-medias-res-revelation.md) | The work should begin in charged action, then reveal missing context until the opening is reinterpreted. |
| `frame_story_nested_return` | [frame-story-nested-return.md](frame-story-nested-return.md) | The work depends on a frame, memory, testimony, document, archive, or story-within-story return. |

## Chooser Guide

Choose by the work's governing movement, not by medium or asset count.

Story Structure entry **Typical Beat Roles** are craft functions, not literal `beat_role` enum values. When adapting a Story Structure into a Beat Plan, map those functions into schema-valid Beat Roles such as `invitation`, `grounding`, `threshold`, `build`, `rupture`, `reveal`, `reversal`, `surrender`, `consequence`, `return`, `closure`, or `residue`.

- Use `three_act_structure` when the work has a central question that should build through commitment, escalation, midpoint change, climax, and final state.
- Use `freytag_dramatic_arc` when the rise to a peak turn and the falling consequence after that peak are both structurally important.
- Use `hero_journey` when threshold crossing, ordeal, transformation, boon, and return are the real engine.
- Use `kishotenketsu` when contrast or recontextualization matters more than conflict escalation.
- Use `problem_reframe_return` when the work is primarily rhetorical, reflective, explanatory, or experiential: the audience feels a problem, receives a reframe, then returns with changed perception or action.
- Use `save_the_cat_beat_sheet` when commercial pacing, beat visibility, midpoint pressure, low point, and opening/final contrast matter.
- Use `dan_harmon_story_circle` when the governing movement is a compact loop: familiar state, need, threshold, search, find, cost, return, change.
- Use `seven_point_structure` when genre momentum, pinch points, midpoint reversal, and plot-turn clarity matter.
- Use `fichtean_curve` when the work should start inside pressure and reveal context through escalating crises.
- Use `in_medias_res_revelation` when delayed context should reinterpret a charged opening.
- Use `frame_story_nested_return` when the act of telling, remembering, finding, or receiving a nested story changes the frame.

## Common Confusion Pairs

- `three_act_structure` vs `freytag_dramatic_arc`: choose three-act when the central question and decisive answer dominate; choose Freytag when peak pressure and aftermath/consequence dominate.
- `three_act_structure` vs `hero_journey`: choose three-act for broad dramatic progression; choose Hero's Journey only when departure, threshold, ordeal, boon, and return are meaningful, not decorative.
- `freytag_dramatic_arc` vs `kishotenketsu`: choose Freytag for escalation into a peak and consequence; choose Kishotenketsu for pattern, turn, and reconciliation without requiring victory or defeat.
- `save_the_cat_beat_sheet` vs `three_act_structure`: choose Save The Cat when granular commercial beat placement and opening/final image contrast matter; choose three-act when broader setup, confrontation, and resolution are enough.
- `save_the_cat_beat_sheet` vs `seven_point_structure`: choose Save The Cat when granular commercial beat placement, false victory or defeat, low point, and opening/final state contrast matter; choose seven-point when lean plot turns, pinch points, midpoint reversal, and resolution are enough.
- `dan_harmon_story_circle` vs `hero_journey`: choose Story Circle for compact cyclical need, cost, return, and change; choose Hero's Journey when mythic threshold, ordeal, boon, and return are structurally meaningful.
- `seven_point_structure` vs `three_act_structure`: choose seven-point when pinch points and midpoint reversal need explicit planning; choose three-act when the story only needs a broader dramatic arc.
- `fichtean_curve` vs `seven_point_structure`: choose Fichtean Curve when the work begins in crisis and escalates through pressure; choose seven-point when planned turns and pinch points organize the plot.
- `in_medias_res_revelation` vs `fichtean_curve`: choose in medias res when delayed context and reinterpretation matter most; choose Fichtean Curve when repeated crises drive the movement.
- `frame_story_nested_return` vs `in_medias_res_revelation`: choose frame story when a narrator, archive, memory, document, or testimony layer matters; choose in medias res when the main structure is charged entry plus delayed cause.
- `problem_reframe_return` vs Cultural Format Structure: use this as Story Structure only when the deep movement is problem to reframe to return. Use a Cultural Format Structure when the question is article, op-ed, how-to, scene, or other audience-facing form grammar.

## Do Not Use Story Structure For

- choosing image count, shot count, section count, song length, or video duration,
- replacing the artist's meaning,
- forcing a canonical template onto a compact `single_beat`,
- selecting article type, social format, screenplay format, or publication container.
