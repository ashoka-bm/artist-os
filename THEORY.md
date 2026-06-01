# Artistic Theory

Artist Generation treats an artwork as layered evidence. Artist OS should not turn a Reference into a prompt directly. It should first identify what the Reference is, what it does formally, what it seems to feel like, what changes inside it, and what it means to the artist.

## Layer 1: Reference

The Reference is the user-provided material: text, image, video, audio, or mixed media.

Record:

- media type,
- title or working name,
- source path or reference,
- user context,
- rights notes,
- target transformation.

## Layer 2: Artist Meaning

Artist Meaning is the artist's stated interpretation of what a Reference means and what must survive transformation. Artist Meaning has final authority over agent interpretation.

## Layer 3: Formal Analysis

Formal Analysis names observable properties.

For text:

- voice,
- diction,
- imagery,
- pacing,
- point of view,
- metaphor,
- structure,
- conflict,
- reversal.

For images:

- color,
- value,
- line,
- shape,
- form,
- space,
- texture,
- contrast,
- balance,
- rhythm,
- movement,
- unity,
- variety.

For audio:

- tempo,
- dynamics,
- timbre,
- harmony,
- melody,
- rhythm,
- density,
- silence,
- repetition,
- tension and release.

For video:

- shot rhythm,
- motion,
- framing,
- camera distance,
- edit tempo,
- color grade,
- scene contrast,
- performance energy.

## Layer 4: Emotional Structure

Emotional Structure is the full emotional model of a Reference inside a Creative Brief. Record it with evidence and confidence.

Artist OS uses Core Tension Pairs instead of bipolar sliders. Each pole can be present independently, and the tension between the poles carries meaning.

The first Core Tension Pairs are:

- Attraction / Repulsion,
- Proximity / Distance,
- Order / Chaos,
- Stillness / Motion,
- Legibility / Opacity,
- Control / Surrender,
- Safety / Threat,
- Presence / Absence.

Each Tension Pair records:

- salience,
- pole A presence,
- pole B presence,
- tension intensity,
- evidence,
- optional artist note,
- translation notes.

Emotional Qualities capture freeform artist language that does not fit the core set.

## Layer 5: Visual Dynamics

Visual Dynamics names the formal forces that make a visual work active, coherent, tense, immersive, unstable, or memorable.

Keep Visual Dynamics separate from Emotional Structure. Emotional Structure describes the felt charge. Visual Dynamics describes the formal engine.

For text-to-image, Visual Dynamics describes the Target Visual Engine of the generated image. It does not pretend the text literally has visual properties. Each visual choice must trace back to Artist Meaning, Reference evidence, Emotional Structure, Beat Map, or Critical Heuristics.

The Core Visual Tension Pairs library is:

- Light / Dark,
- Saturated / Muted,
- Warm / Cool,
- Harmonious / Discordant,
- Dense / Sparse,
- Geometric / Organic,
- Sharp / Diffuse,
- Linear / Painterly,
- Textured / Smooth,
- Representational / Non-Representational,
- Flat / Deep,
- Balanced / Unbalanced,
- Centered / Decentered,
- Singular / Repetitive.

For the First Slice, record only the active 6 to 8 visual tensions with evidence and translation notes.

Use Monumental / Intimate only when scale, embodiment, installation, performance, or immersive environments matter.

## Layer 6: Style Direction

Style Direction defines the artistic language used to express the Creative Brief. It is separate from Emotional Structure and Visual Dynamics.

Before choosing Style Direction by default, choose Symbology Direction: what the image shows as the core symbolic representation of Artist Meaning. Symbology is closer to meaning than style, so unresolved symbology should be explored visually before style is locked.

Explore it with a Symbology Board, built as a Comparison Board (see "Visual Gate Boards" below): one single image, a 2x3 grid of six cells, where every cell is plain black-and-white line art of the subject only — no color, shading, style, or background — so style does not obscure the symbolic choice. The six cells compare distinct symbolic representations such as figure, object, landscape, ritual scene, room, threshold, vessel, or abstraction. Wait for the artist to select, combine, reject, or revise options before locking Symbology Direction unless they explicitly choose to proceed unconfirmed.

### Visual Gate Boards

The Symbology Gate, the Style Gate, and the Minimalist-to-Maximalist Gate all resolve an open decision the same way: by showing the artist the options laid out together in **one image** so they can compare and choose. This shared mechanic is the Comparison Board.

A Comparison Board is a single provider-neutral image-generation prompt that renders every option together inside one image as a labeled grid. It is never a list of separate prompts and never several images — the whole point is that one generation produces the full comparison. Store that one prompt as `composite_image_prompt` and store the per-cell content as the `visual_prompt` of each option.

The contract for every board:

- **One image, one prompt, one generation.** The `composite_image_prompt` describes the entire grid as a single image. Do not emit one prompt per option.
- **Grid layout.** Default to six cells in a 2x3 grid; use three side-by-side panels for the intensity gate. Match the cell count to the number of options, never more than three cells per row. Cells are equal size with a small number label (1..N) and the same framing.
- **Hold everything constant except the dimension under test.** A board isolates one decision so the comparison is honest:
  - **Symbology Board** — vary the symbolic representation; every cell is line art of the subject only, no style.
  - **Style Exploration Board** — vary the style; every tile shows the same locked Symbology subject, pose, and framing so only style language changes.
  - **Minimalist-to-Maximalist Gate** — vary visual intensity; three panels hold the same locked subject and style while density, layering, complexity, scale, drama, ornament, and negative space change.
- **Draft versus generate.** Drafting a board means writing its `composite_image_prompt` as text; this needs no provider call and is always allowed. Generating a board means sending that one prompt to a provider to render the image, which requires explicit, per-board generation approval. Both paths produce the same single prompt.

A fillable skeleton for a Symbology Board prompt:

> One single image. A 2x3 grid of six equal square cells with thin gutters and a small number in each cell's corner. Black-and-white line art only — no shading, no color, plain white background — showing the same [subject] centered in every cell. Cell 1: [symbolic representation A]. Cell 2: [symbolic representation B]. Cell 3: [...]. Cell 4: [...]. Cell 5: [...]. Cell 6: [...]. Render as one image; do not output six separate images.

Do not call a provider-backed generator until the artist explicitly approves that generation call.

Style Direction should answer:

- should this feel photographic, illustrated, painterly, graphic, cinematic, comic, abstract, or material?
- should it look polished, raw, glossy, matte, grainy, minimal, maximal, stylized, or photoreal?
- which style choices preserve Artist Meaning?
- which style choices would flatten or betray the work?

Style Direction may be hybrid, but it must have one Primary Style and bounded Style Modifiers. Do not combine many styles at equal weight.

Style Direction is the last priority. It must not override Artist Meaning, Emotional Structure, Beat Map, or Visual Dynamics. When a chosen style conflicts with the Target Visual Engine, surface the conflict and adapt the style instead of silently weakening the brief.

Choose Style Direction after the first pass of Artist Meaning, Emotional Structure, Beat Map, and Symbology Direction, and before Art Critic Review. If the artist names a specific style directly, use it and record the reason. Do not run the full Style Interview unless no style was named. Ask at most one Style Clarifier if the named style is broad or internally ambiguous.

If the artist has not named a specific style, the first style gate is not a menu of styles. Ask whether they already have a specific visual vision or want to explore what art style to use. If they want exploration, ask for a rough direction in their own words, then use that direction to build candidate styles.

The Style Interview should be adaptive. If Artist Meaning or the Reference already points toward a style branch, ask the most useful next clarifier. When no branch is obvious, use this fallback order:

1. Should the image feel camera-based, hand-made, graphic/comic, or synthetic/digital?
2. Should it lean realistic/representational or stylized/abstracted?
3. Should the finish feel polished/glossy, raw/grainy, painterly/textured, or flat/minimal?
4. Should the cultural genre lean contemporary/everyday, surreal/dreamlike, fantasy/mythic, sci-fi/futuristic, historical, dark/horror, playful/whimsical, or folk/traditional?

Stop the Style Interview early when either Primary Style, bounded Style Modifiers, known conflicts, and alignment with Artist Meaning are clear, or when there is enough information to create a useful Style Exploration Board.

After the Style Interview or Style Exploration Board, synthesize a Style Recommendation and ask the artist to use it, adjust it, or name a different style. Do not make the artist assemble taxonomy from raw answers.

When Style Direction is unresolved, make Style a visual gate: ask whether the artist wants to see style options before moving forward. If yes, build a Style Exploration Board as a Comparison Board (see "Visual Gate Boards"): one single image, a 2x3 grid of six tiles, where every tile renders the same locked Symbology subject, pose, and framing in a different candidate style, so only the style language varies. Store the single grid prompt as `composite_image_prompt`. The board lets the artist compare style language without committing to separate full generations, and it does not replace Brief Approval. Default to six tiles, no more than three per row unless the artist asks otherwise. Do not call a provider-backed generator until the artist explicitly approves that generation call. Wait for artist response before locking Style Direction unless they explicitly choose to proceed unconfirmed.

Use the Wondermint Category Reference as initial category vocabulary, but do not treat upload categories as the entire art ontology. Style Direction must serve the Creative Brief.

## Layer 7: Beats And Tension Points

A Beat is the smallest meaningful change, contrast, turn, or pressure point in a Reference that carries Emotional Payload.

A Tension Point is meaningful contrast or unresolved pressure that carries emotion without requiring before/after change.

Each Beat records:

- before state,
- after state,
- what changed,
- value shift,
- emotional payload,
- source evidence,
- user confirmation.

## Layer 8: Series Recommendation

When a Reference contains more than one meaningful Beat or Tension Point, Artist OS should recommend whether the work is best served by:

- a single image that compresses the whole emotional arc,
- a triptych that stages a before, threshold, and after movement,
- an image series where each image has a distinct Image Role.

A multi-Beat Reference does not automatically become a series. Recommend a single image when compression into one symbol, threshold, or contradiction preserves the work more strongly than sequence.

Use a triptych when the Beat Map has a clear three-part emotional structure, such as before/threshold/after, invitation/rupture/consequence, or concealment/revelation/aftermath. Use an image series for extended sequence, motif evolution, or world exploration.

When the Reference warrants it, a Series Recommendation may propose Style Progression, where the visual language changes across images to express emotional movement. Style Progression must be intentional and trace back to the Beat Map.

Do not create multiple image prompt plans by default. A Series Plan requires artist approval, and Style Progression becomes executable only after that approval.

After a Series Plan is approved, produce one Series Calibration Image first. Use it to lock Style Direction, Target Visual Engine, and the shared visual language before producing the rest of the series.

Choose the Series Calibration Image by representativeness, not sequence order. Use the Image Role that best contains the series' Style Direction, Target Visual Engine, and emotional tension. This is often the threshold or central image, not necessarily the opening Beat.

Series Calibration uses three Prompt Variant Plans for the selected Calibration Image Role. After the artist approves one calibration direction, remaining series images use one prompt per Image Role by default.

The selected calibration direction becomes a Calibration Choice. Record accepted style traits, rejected style traits, locked visual rules, and notes for remaining images in the Creative Brief Record or Series Plan.

Calibration Choice can update visual language, Style Direction, Visual Dynamics translation notes, locked visual rules, and series continuity rules. It cannot update Artist Meaning, Core Tension Pairs, or Beat Map unless the artist explicitly says the calibration revealed a better meaning.

## Layer 9: Meaning-Preserving Transformation

Meaning-Preserving Transformation changes medium or form while preserving Artist Meaning, selected Formal Analysis, Style Direction, Visual Dynamics, Emotional Structure, and relevant Beats or Tension Points.

Do not preserve surface form by default. Preserve emotional function. Change the medium-specific form only after naming what emotional role each source detail plays.

## Prompt Variant Plans

Before final Prompt Variant Plans are locked, Artist OS should give the artist a visual intensity choice when Minimal, Faithful, and Amplified would materially change the work. By this point Symbology Direction and Style Direction should be selected or narrowed. Use a Minimalist-to-Maximalist Gate, built as a Comparison Board (see "Visual Gate Boards"): one single image of three side-by-side panels that keep the same approved meaning, symbology, Style Direction, and Target Visual Engine, while density, symbolic layering, visual complexity, scale, drama, ornament, and negative space change from Minimal to Faithful/Balanced to Amplified/Maximal. Store the single three-panel prompt as the layout plan's `composite_image_prompt`.

The Minimalist-to-Maximalist Gate is not a Series Plan and should not reopen symbology or style unless the artist explicitly asks to go back. Ask the artist to select, combine, reject, or revise intensity directions before final prompt locking whenever intensity would materially affect the image.

The First Slice produces one Provider-Neutral Image Prompt Plan with three Prompt Variant Plans:

- Faithful: closest to the approved Creative Brief.
- Amplified: pushes the strongest tension, Poetic Density, and Target Visual Engine while preserving Artist Meaning.
- Minimal: strips the image down to the essential emotional and visual engine.

When the Creative Brief still contains unresolved creative dimensions, the three Prompt Variant Plans may test Variant Test Axes inside the approved symbology and style. For example, one variant may be sparse and iconic, another balanced and readable, and another dense and layered. Each variant must name the axis it is testing.

Keep the stable labels Faithful, Amplified, and Minimal even when variants test an unresolved axis. Add a Variant Test Axis Label to explain what each variant is testing.

The Amplified Prompt Variant may use Derived Symbols, but each Derived Symbol must be marked and traced to the approved Creative Brief.

The three Prompt Variant Plans must create meaningful visual alternatives along the Minimalist-to-Maximalist axis. They should not be three near-identical prompts with adjective changes. Each variant must use concrete differentiators such as composition, camera distance, spatial depth, density, symbolic layering, abstraction level, color/light strategy, texture, finish, negative space, ornament, scale, drama, or focal hierarchy.

When the artist wants one generation for comparison, the three final intensity directions can be packed into a Single-Generation Variant Triptych: three equal square panels in one horizontal image. The left panel carries the Minimal/minimalist direction, the center the Faithful/balanced direction, and the right the Amplified/maximalist direction. This is not a Series Plan; it is a comparison layout for one approved image direction.

## First Slice

The First Slice is Text Reference to Image Prompt Plan. It is a Dry Run: no provider-backed generation calls.
