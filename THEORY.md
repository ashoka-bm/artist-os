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

Style Direction should answer:

- should this feel photographic, illustrated, painterly, graphic, cinematic, comic, abstract, or material?
- should it look polished, raw, glossy, matte, grainy, minimal, maximal, stylized, or photoreal?
- which style choices preserve Artist Meaning?
- which style choices would flatten or betray the work?

Style Direction may be hybrid, but it must have one Primary Style and bounded Style Modifiers. Do not combine many styles at equal weight.

Style Direction is the last priority. It must not override Artist Meaning, Emotional Structure, Beat Map, or Visual Dynamics. When a chosen style conflicts with the Target Visual Engine, surface the conflict and adapt the style instead of silently weakening the brief.

Choose Style Direction after the first pass of Artist Meaning, Emotional Structure, and Beat Map, and before Art Critic Review. If the artist names a style directly, use it and record the reason. Do not run the full Style Interview unless no style was named. Ask at most one Style Clarifier if the named style is broad or internally ambiguous.

The Style Interview should be adaptive. If Artist Meaning or the Reference already points toward a style branch, ask the most useful next clarifier. When no branch is obvious, use this fallback order:

1. Should the image feel camera-based, hand-made, graphic/comic, or synthetic/digital?
2. Should it lean realistic/representational or stylized/abstracted?
3. Should the finish feel polished/glossy, raw/grainy, painterly/textured, or flat/minimal?
4. Should the cultural genre lean contemporary/everyday, surreal/dreamlike, fantasy/mythic, sci-fi/futuristic, historical, dark/horror, playful/whimsical, or folk/traditional?

Stop the Style Interview early when Primary Style, bounded Style Modifiers, known conflicts, and alignment with Artist Meaning are clear.

After the Style Interview, synthesize a Style Recommendation and ask the artist to use it, adjust it, or name a different style. Do not make the artist assemble taxonomy from raw answers.

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

The First Slice produces one Provider-Neutral Image Prompt Plan with three Prompt Variant Plans:

- Faithful: closest to the approved Creative Brief.
- Amplified: pushes the strongest tension, Poetic Density, and Target Visual Engine while preserving Artist Meaning.
- Minimal: strips the image down to the essential emotional and visual engine.

When the Creative Brief still contains unresolved creative dimensions, the three Prompt Variant Plans may test Variant Test Axes. For example, one variant may lean more realistic while another leans more cartoon, or one may be more literal while another is more symbolic. Each variant must name the axis it is testing.

Keep the stable labels Faithful, Amplified, and Minimal even when variants test an unresolved axis. Add a Variant Test Axis Label to explain what each variant is testing.

The Amplified Prompt Variant may use Derived Symbols, but each Derived Symbol must be marked and traced to the approved Creative Brief.

## First Slice

The First Slice is Text Reference to Image Prompt Plan. It is a Dry Run: no provider-backed generation calls.
