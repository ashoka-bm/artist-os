# Promoted Reference Inventory And Storage

Status: accepted.

Artist OS will treat promoted character, location, and object references as a project-level continuity system, not as loose prompt text or provider-specific media slots.

## Decision

Promotion starts as an agent recommendation. It becomes binding only when the artist answers the relevant `character_reference_strategy` or `visual_reference_sheet_strategy` gate. Partial acceptance is a first-class strategy state: `accepted_partial` means the artist accepted only selected recommended subjects, while declined subjects remain known continuity risks and should not be silently re-asked in the same flow. Accepted subjects use `subject_status = "accepted_for_planning"`.

Promoted visual reference subjects reuse `VisualReferenceSheetPlan`. A promoted main character plans three separate reference images: dead-on identity plate, full-body turnaround sheet, and macro detail card. A promoted location plans three separate angle images: establishing, reverse, and functional or staging. A promoted object plans one multi-section image with multiple angles and macro details.

Each generated reference image gets its own Output Record. A character package normally creates three Output Records, a location package creates three Output Records, and an object package creates one Output Record. The Visual Reference Sheet Plan stores multiple `output_record_refs`, so one generated reference image can be regenerated, replaced, reviewed, or accepted without rewriting the whole package.

Artist OS adds a schema-backed Reference Inventory record. The inventory owns effective reference policy, scan history, reference subjects, categories, names, slugs, recommendation status, gate status, continuity-risk notes, package readiness, per-output readiness, Visual Reference Sheet Plan refs, Output Record refs, active output refs, visible storage paths, and provider-neutral role hints. It does not own story canon.

Subject output counts describe the base subject package only. Variant outputs are nested under their variant owner and remain available to Reference Readiness and the SQLite image index without changing the base subject's count fields. `generated_output_count` is a current-state count, not a cumulative lifetime count; accepted outputs no longer count as generated drafts.

Long-Work Stewardship owns canon rules for cumulative or long-form projects. When a reference becomes canon-critical, stewardship links to the Reference Inventory item and records the continuity rule. Reference Inventory remains asset and status authority; Long-Work Stewardship remains story authority.

## Storage

Generated and imported reference images should appear in the visible Artist Library project folder under category and subject folders:

```text
References/
├── Characters/<character-slug>/
│   ├── Review Drafts/
│   └── Accepted/
├── Locations/<location-slug>/
│   ├── Review Drafts/
│   └── Accepted/
└── Objects/<object-slug>/
    ├── Review Drafts/
    └── Accepted/
```

The visible folders help the artist inspect and choose references. The hidden Workspace Library remains the provenance source of truth through Output Records, sidecar metadata, event logs, and the SQLite index.

## Reference Image Rules

Location reference images default to no characters. A staging or scale figure is allowed only when the artist approves it or when blocking cannot be understood without scale. A scale figure must not define character identity unless it links to an accepted character reference.

Visible labels are off by default for reference images intended as downstream provider inputs. Labels may be created for human-review contact sheets only; those labeled assets must be marked review-only and not provider-input-safe.

Reference Inventory may store provider-neutral role hints such as `identity_reference`, `location_reference`, `object_reference`, `detail_reference`, and `review_only`. Provider-specific upload ids, media bindings, model syntax, Seedance-style tags, and runtime roles belong in future adapter or export records, not in the core inventory.

## Lifecycle

Reference Inventory uses separate status layers:

- `subject_status`: `candidate`, `recommended`, `accepted_for_planning`, `declined`, `deferred`, or `reactivated`.
- `package_readiness`: `missing`, `planned`, `partially_accepted`, `accepted`, `needs_regeneration`, `waived`, or `retired`.
- per-output `output_status`: `planned`, `imported_candidate`, `generated_draft`, `accepted`, `rejected`, `replaced`, `retired`, or `waived`.
- per-output `readiness`: `missing`, `planned`, `draft_generated`, `accepted`, or `waived`.

`accepted_for_planning` unlocks automatic Visual Reference Sheet Plan prompt drafting. Drafting prompts is non-costly and reversible. Generation remains a separate explicit approval gate. Reference Readiness is a later gate: required outputs must be `accepted` or `waived` before storyboard export, image prompt export, illustration prompt export, or provider video generation.

## Consequences

- Video Journey can recommend reference subjects without silently expanding scope.
- Reviewers can distinguish fully accepted reference strategy from partial acceptance.
- Artists can browse generated reference drafts and accepted references in predictable folders.
- Provider adapters can consume accepted references later without adding provider syntax to core records.
- Long-form projects can promote reference facts into Long-Work Stewardship only when they become canon rules.

## Follow-Up Implementation

- Add reviewer packet checks that surface declined, deferred, or waived required references as risk notes.
- Add adapter/export records for provider-specific media bindings without putting provider syntax into the core inventory.
