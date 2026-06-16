# Prompt Branch Set

This is the canonical Artist OS procedure for building a Prompt Branch Set: a curator batch of meaning-equivalent prompts spread around an approved Prompt Plan.

Load this when the artist wants a curator batch, prompt exploration, mass production, or several meaning-equivalent prompts. The Prompt Branch Gate that approves the set is defined in `docs/gates-and-reviews.md`; this file is the build procedure. The current contract is image-oriented (it is driven from `skills/text-to-image-plan`); the Suno flow does not use an image-style Prompt Branch Set.

## Build Procedure

Use this only after an approved Provider-Neutral Image Prompt Plan exists.

1. Preserve the upstream lineage ids: `prompt_plan_id`, `brief_id`, `source_id`, `artist_meaning_id`, `transformation_brief_id`, `beat_plan_id`, and `medium_plan_id` (the approved Image Medium Plan id). Mint a new `prompt_branch_set_id` for the set itself.
2. Define the Meaning Kernel: what must stay identical across all branches, including `governing_intended_feeling`, `key_emotional_movement_ids`, and `minimum_tension_criteria`.
3. Define `must_preserve` and `must_not_change` from Artist Meaning, the Beat Plan, Image Medium Plan, and approved Prompt Plan.
4. Choose variation axes. For image batches, default to varying at least style, setting, symbol, composition, and palette/light unless the artist narrows the request.
5. Create five branches by default. Use a different count only when the artist asks.
6. Each branch must differ from every other branch on at least three major axes. Do not create five prompts that are only adjective swaps.
7. Each branch must include `branch_id`, `branch_label`, `branch_role`, `variation_axes`, `preserved_kernel`, `emotional_tension_preservation`, at least three `differentiators`, `prompt_text`, `negative_constraints`, `traceability_notes`, and `curator_notes`.
8. Branches may depart far from the literal setting if they preserve the kernel and trace the departure.
9. Before provider-backed generation from any branch, require explicit Generation Approval.
10. When the branch set will drive broad curator selection, run Prompt Critic Review as a bounded sub-agent and persist the Review Record.

The branch set is not a new Creative Brief and does not reopen Artist Meaning. It is a controlled spread around the approved kernel so AI generation has useful variance and the human can curate.

`emotional_tension_preservation` is the branch-level check against style-only drift. It must name the branch's Intended Feeling, Key Emotional Movement id, Expectation Turn Translation, tension profile, and minimum criteria. If a branch changes setting, symbol, or composition so much that this field becomes vague, revise the branch or drop it from the set.

Emit the set against `schemas/prompt-branch-set.schema.json`.
