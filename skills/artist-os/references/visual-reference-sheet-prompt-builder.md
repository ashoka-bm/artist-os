# Visual Reference Sheet Prompt Builder

Use this internal mode when Artist OS needs a provider-neutral Visual Reference Sheet Plan for a character, product, object, setting, prop, or style target. This is a prompt-planning mode, not a provider adapter.

Paths like `schemas/visual-reference-sheet-plan.schema.json`, `schemas/character-template.schema.json`, and `schemas/output-record.schema.json` resolve from `$ARTIST_OS_ROOT`.

## Hard Gates

- Drafting reference-sheet prompts is allowed automatically.
- Generating the actual reference sheet image requires explicit Generation Approval for that call or approved batch.
- Every generated or imported reference sheet used downstream needs provenance through an Output Record or Asset Metadata.
- If the artist declines reference sheets, record `declined` and do not ask again in the same flow.
- If Style Direction changes after a prompt is drafted, revise the Visual Reference Sheet Plan before generation.

## Inputs

Use the relevant subject record or description:

- Character Template for character sheets,
- artist-provided product, object, setting, or style description,
- Source Record and Artist Meaning,
- Transformation Brief or Beat Plan when they exist,
- Style Direction or a clearly marked provisional style,
- any imported reference assets and rights notes.

## Character Reference Sheet Template

Use this framework faithfully, adapting only the bracketed parts:

```text
CHARACTER REFERENCE SHEET FOR STYLE
Show the same [DESCRIBE CHARACTER AND CLOTHING]
Character reference sheet - four views on a neutral grey background:
[VIEW 1 - FULL BODY, FRONT] Full-body front-facing three-quarter view of this character, full body visible head to feet.
[VIEW 2 - FULL BODY, REAR] Full-body rear view of the same character, directly from behind. Full body visible head to feet.
[VIEW 3 - FRONT CLOSE-UP] Head and shoulders close-up, straight-on front view. Sharp detail on skin texture, accessories, and costume surface detail. Chest and shoulder armour/clothing visible at the bottom of frame.
[VIEW 4 - PROFILE CLOSE-UP] Head and shoulders close-up, 90-degree left profile view. Neck and upper shoulder visible.
Lighting & presentation: Clean studio lighting - soft key light upper left, gentle fill from the right. Consistent character identity, proportions, and costume details across all four views. No text, no watermarks, no extra figures, no background environment, in the below style... [INSERT DESIRED STYLE]
```

For character work, the subject description should come from `CharacterTemplate.visual_identity`. If details are inferred, keep them clearly provisional unless the artist approved them.

## Product / Object Reference Sheet Template

Use this framework for products and objects, adapting the product details:

```text
Product reference sheet - four views on a neutral grey background:
[VIEW 1 - FRONT, THREE-QUARTER] Front-facing three-quarter view of [PRODUCT]. Full object visible top to bottom. Include defining front features, material, color, scale cues, and any visible controls or openings.
[VIEW 2 - REAR, STRAIGHT-ON] Full rear view of the same [PRODUCT], directly from behind. Full object visible. Include defining rear features, surface details, material transitions, logos or markings only when approved, and what must not appear.
[VIEW 3 - FRONT CLOSE-UP] Close-up of the most important front detail. Sharp detail on materials, seams, surface texture, controls, display, glass, metal, fabric, or other defining features.
[VIEW 4 - PROFILE, LEFT SIDE] Left-profile close-up showing the object edge-on or in side silhouette. Show thickness, taper, material transition, buttons, ports, handles, or other side details.
Lighting & presentation: Clean studio lighting - soft key light upper left, gentle fill from the right. Consistent identity, proportions, color, and hardware/material details across all four views. [INSERT DESIRED STYLE]. No text, no watermarks, no extra objects, no background environment.
```

## Output

Emit a Visual Reference Sheet Plan that validates against `schemas/visual-reference-sheet-plan.schema.json`.

The plan must include:

- `reference_sheet_type`,
- `subject_ref` when a Character Template, Output Record, or asset already exists,
- `subject_description`,
- `style_direction_summary`,
- four-view `view_layout`,
- one complete `prompt_text`,
- `generation_policy` with approval required,
- `output_record_refs`, empty until generation or import exists,
- traceability back to Artist Meaning, Character Template, style decision, source evidence, or gate decision.

Do not generate the image. Stop at the prompt plan unless the artist explicitly approves generation.
