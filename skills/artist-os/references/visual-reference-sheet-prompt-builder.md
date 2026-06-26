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

## Promotion Rule

Promote a character, location, product, object, setting, or prop into reference status only when the story or downstream medium needs visual continuity. Use promotion when the subject is main, recurring, meaning-bearing, handled closely, blocking-critical, or likely to drift across scenes or generated outputs. Do not promote incidental background details.

For promoted subjects, draft prompt plans only. Generating the actual reference images still requires Generation Approval and later Output Records.

## Promoted Character Reference Package Template

When a main or recurring character is promoted, create a `reference_sheet_type = "character"` Visual Reference Sheet Plan with `view_layout.layout_type = "multi_image_reference_package"` and three planned reference outputs:

1. `character_identity_plate`: one dead-on identity image that locks face, head shape, hair, skin or surface quality, age, expression baseline, and any identity-bearing marks.
2. `character_turnaround_sheet`: one full-body turnaround sheet that locks silhouette, proportions, outfit, scale, and front / side / rear views.
3. `character_macro_detail_card`: one multi-section detail card that locks eyes, mouth, skin or surface texture, hair texture, hands, costume material, accessories, scars, markings, wear, and other small continuity details.

Use this framework, adapting only the bracketed parts:

```text
PROMOTED CHARACTER REFERENCE PACKAGE
Create three separate reference images for the same [DESCRIBE CHARACTER AND CLOTHING], all on a flat matte neutral gray background, all in [INSERT DESIRED STYLE].

IMAGE 1 - DEAD-ON IDENTITY PLATE
Straight-on portrait or upper-body identity plate. Neutral expression unless the Character Template requires otherwise. Preserve face structure, head shape, hair, eye shape, skin or surface texture, age, visible marks, and identity-bearing accessories. Clean studio lighting, no environment, no text, no extra figures.

IMAGE 2 - FULL-BODY TURNAROUND SHEET
Full-body front, side, rear, and three-quarter views of the same character. Full body visible head to feet in every view. Preserve proportions, silhouette, outfit, fabric, footwear, scale, posture baseline, and approved costume details. Clean studio lighting, no environment, no text, no extra figures.

IMAGE 3 - MACRO DETAIL CARD
One image divided into clean sections showing the same character's defining details: eyes, mouth, skin or surface texture, hair texture, hands, costume material, accessories, markings, wear, and other continuity-critical details. Preserve the same identity and style. No environment, no text unless labels are explicitly requested for human review.
```

Use the Character Template as authority. If a detail is inferred, mark it provisional unless the artist approved it.

## Character Four-View Reference Sheet Template

Use this framework faithfully, adapting only the bracketed parts:

```text
CHARACTER REFERENCE SHEET FOR STYLE
Show the same [DESCRIBE CHARACTER AND CLOTHING]
Character reference sheet - four views on a neutral gray background:
[VIEW 1 - FULL BODY, FRONT] Full-body front-facing three-quarter view of this character, full body visible head to feet.
[VIEW 2 - FULL BODY, REAR] Full-body rear view of the same character, directly from behind. Full body visible head to feet.
[VIEW 3 - FRONT CLOSE-UP] Head and shoulders close-up, straight-on front view. Sharp detail on skin texture, accessories, and costume surface detail. Chest and shoulder armour/clothing visible at the bottom of frame.
[VIEW 4 - PROFILE CLOSE-UP] Head and shoulders close-up, 90-degree left profile view. Neck and upper shoulder visible.
Lighting & presentation: Clean studio lighting - soft key light upper left, gentle fill from the right. Consistent character identity, proportions, and costume details across all four views. No text, no watermarks, no extra figures, no background environment, in the below style... [INSERT DESIRED STYLE]
```

Use this smaller four-view sheet when the character needs lightweight continuity but has not been promoted into the full three-image package.

## Promoted Setting / Location Reference Package Template

When a location or world setting is promoted, create a `reference_sheet_type = "setting"` Visual Reference Sheet Plan with `view_layout.layout_type = "three_angle_reference_package"` and three planned reference outputs:

1. `location_establishing_angle`: a wide orientation image that locks geography, boundaries, entrances, exits, light sources, scale, and major spatial anchors.
2. `location_reverse_angle`: a reverse or alternate angle that shows the same place from the opposite side and confirms spatial continuity.
3. `location_functional_angle`: a staging or interaction angle that shows where characters, camera, props, vehicles, or action can move.

Use this framework, adapting only the bracketed parts:

```text
PROMOTED SETTING / LOCATION REFERENCE PACKAGE
Create three separate images of the same [DESCRIBE LOCATION], all in [INSERT DESIRED STYLE]. Keep the same architecture, geography, entrances, exits, windows, doors, furniture, landmarks, scale, light direction, weather or time of day, and fixed spatial anchors across all three images. No characters unless explicitly requested. Leave useful negative space for later staging.

IMAGE 1 - ESTABLISHING ANGLE
Wide establishing view that shows the full layout, major boundaries, entry and exit points, primary light sources, and the location's emotional pressure.

IMAGE 2 - REVERSE ANGLE
Reverse or alternate view from the opposite side of the same location. Preserve all spatial anchors and make the relationship to the establishing angle clear.

IMAGE 3 - FUNCTIONAL / STAGING ANGLE
Practical staging view that shows the path of movement, interaction zones, foreground / midground / background layers, and any areas where characters, props, vehicles, or camera movement will operate.
```

Do not create a new location-specific core record unless the existing Visual Reference Sheet Plan fails a real workflow. Generated location images become Output Records or imported asset metadata before downstream use.

## Promoted Product / Object Reference Sheet Template

When a product, object, or prop is promoted, create a `reference_sheet_type = "product"` or `reference_sheet_type = "object"` Visual Reference Sheet Plan with `view_layout.layout_type = "multi_section_reference_sheet"` and one planned `object_multi_angle_sheet` output. The output is one image divided into sections for the object's important angles and details.

Use this framework, adapting the object details:

```text
PROMOTED OBJECT MULTI-ANGLE REFERENCE SHEET
Create one image divided into clean sections for the same [DESCRIBE OBJECT], on a flat matte neutral gray background, in [INSERT DESIRED STYLE].

SECTION 1 - FRONT / IDENTITY VIEW
Full object visible from the front or front three-quarter angle. Preserve shape, color, material, proportions, scale cues, and identity-bearing marks.

SECTION 2 - SIDE / DEPTH VIEW
Full side or profile view showing thickness, silhouette, handles, ports, hinges, legs, seams, or depth-critical details.

SECTION 3 - REAR / BACK VIEW
Full rear view showing back construction, surface wear, material transitions, markings, controls, vents, cables, or approved logos.

SECTION 4 - MACRO DETAIL
Close-up of the object's most story-critical details: material grain, screen, glass, buttons, cracks, seams, wear, labels, hardware, or transformation marks.

Lighting & presentation: Clean studio lighting, consistent object identity, no extra objects, no character hands unless scale or handling is explicitly required, no environment, no text unless labels are explicitly requested for human review.
```

## Output

Emit a Visual Reference Sheet Plan that validates against `schemas/visual-reference-sheet-plan.schema.json`.

The plan must include:

- `reference_sheet_type`,
- `subject_ref` when a Character Template, Output Record, or asset already exists,
- `subject_description`,
- `style_direction_summary`,
- `view_layout` describing the planned image, angles, panels, or package outputs,
- `reference_outputs` when the subject is promoted into a multi-image or multi-section package,
- one complete `prompt_text`,
- `generation_policy` with approval required,
- `output_record_refs`, empty until generation or import exists,
- traceability back to Artist Meaning, Character Template, style decision, source evidence, or gate decision.

Do not generate the image. Stop at the prompt plan unless the artist explicitly approves generation.
