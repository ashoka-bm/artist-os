# Long-Work Stewardship Mapping

Long-Work Stewardship remains the continuity authority. These Novel Craft mappings do not create a story bible, new continuity record, or alternate source of truth. Cultural Format Structure entries describe recognizable document grammar. Stewardship Views project readable slices from the Text Medium Plan and the Long-Work Stewardship Record.

| Entry | CFS, Stewardship View, or both | Projects from Long-Work Stewardship / Medium Plan |
| --- | --- | --- |
| `novel_outline` | Both | Text Medium Plan text form, structure plan, section/chapter map, adapted Story Structure summary, Long-Work `governing_arc`, `part_plan`, `readiness_review`, and checkpoint risks. |
| `chapter` | Both | Text Medium Plan chapter or section jobs plus Long-Work `part_plan` entries with `part_kind: chapter` or `scene`, `part_job`, `intended_feeling`, `expected_state`, `must_preserve`, `must_not_resolve_yet`, dependencies, status, and checkpoint summaries. |
| `scene_card` | Both | Text Medium Plan scene/section mapping plus Long-Work `part_plan` entries with `part_kind: scene`, dependencies, assigned Beat Roles, continuity rules, and open drift items. |
| `sequence_arc` | Both | Text Medium Plan section/chapter grouping plus Long-Work `governing_arc`, ordered `part_plan`, dependencies, checkpoints, and continuity rules for structure, pacing, character, motif, or setting. |
| `character_brief` | Stewardship View first, CFS when delivered as a document | Long-Work continuity rules with `rule_type: character` or `voice`, proposed continuity updates, drift items from approved prior parts, and Medium Plan voice/POV constraints. |
| `relationship_arc` | Stewardship View first, CFS when delivered as a document | Long-Work continuity rules with `rule_type: character`, relationship-related proposed continuity updates, affected part ids, dependencies, and checkpoints where relationship state changes. |
| `subplot_tracker` | Stewardship View first, CFS when delivered as a document | Text Medium Plan structure plan, Long-Work `part_plan`, continuity rules with `rule_type: structure`, `character`, `motif`, or `pacing`, proposed continuity updates, and checkpoint summaries. |
| `open_thread_tracker` | Stewardship View first, CFS when delivered as a document | Long-Work `must_not_resolve_yet`, `continuity_rules`, `proposed_continuity_updates`, `checkpoints`, `drift_management.open_drift_items`, and Text Medium Plan section jobs/payoff decisions. |
| `plot_tracker` | Stewardship View first, CFS when delivered as a document | Beat Plan and adapted Story Structure summary, Text Medium Plan structure plan, Long-Work `governing_arc`, `part_plan`, continuity rules, checkpoints, readiness review, and open drift items. |
| `treatment_outline` | CFS first, Stewardship View when generated from existing project state | Text Medium Plan form/voice/structure decisions, Beat Plan movement, Long-Work `governing_arc`, ordered `part_plan`, and relevant continuity rules or proposed updates. |

## Translation Rules

- Novel Craft "story bible" maps to Artist OS Project Memory expressed through approved Artist Meaning, Beat Plan, Text Medium Plan, Long-Work Stewardship Record, Output Records, Review Records, and Gate Decisions.
- Novel Craft extraction maps to `proposed_continuity_updates`; verified and approved items may become Long-Work `continuity_rules`.
- Novel Craft verification maps to Long-Work Reviewer behavior, checkpoint review, and required approval on proposed continuity updates.
- Novel Craft chapter briefs map to Text Medium Plan chapter/section jobs plus Long-Work Parts.
- Novel Craft character sheets, relationship maps, world rules, subplots, and open threads are Stewardship Views unless the user explicitly asks for a delivered document in that format.
- No view may silently change continuity. Changes discovered during drafting remain proposed until the required approval path accepts them.
- View-first entries may display projected status, risks, dependencies, open questions, and proposed changes, but they may not mutate Long-Work Stewardship, Beat Plan, Medium Plan, Output Records, Review Records, or Gate Decisions.

## Internal View Names

When these entries are used internally as Stewardship Views rather than delivered as documents, use the view name; reserve the CFS entry name for a deliverable document. This matches the per-entry "Authority mode" notes in the cultural-format library.

- `character_brief` → `character_continuity_view` internally; keep `character_brief` for a delivered document.
- `relationship_arc` → `relationship_continuity_view` internally; keep `relationship_arc` for a delivered document.
- `scene_card` → `scene_brief` or `scene_stewardship_view` internally; keep `scene_card` for a delivered document.
- `subplot_tracker`, `open_thread_tracker`, and `plot_tracker` are Stewardship Views by default, not ordinary CFS entries.
