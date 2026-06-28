# Style Direction

## Layer 6: Style Direction

Style Direction defines the artistic language used to express the Creative Brief. It is separate from Emotional Structure and Visual Dynamics.

### Stage Completion

Artist OS moves through three artist-facing visual planning stages: Interpretation, Visualization/Symbolic, and Style. Do not advance while the current stage still has an unanswered choice unless the artist explicitly says to proceed unconfirmed.

- **Interpretation complete**: Artist Meaning, must-preserve meaning, and emotional language or emotional arc are captured, or unresolved interpretation questions are marked safe to proceed unconfirmed.
- **Visualization/Symbolic complete**: the artist has selected or combined a symbolic representation, selected single image / compressed arc / image series, and accepted, declined, or requested visualization.
- **Style complete**: the artist has selected, combined, or named a style, or explicitly allowed an unconfirmed style recommendation to proceed; any offered visualization has been accepted, declined, or requested as a prompt.

Before choosing Style Direction by default, choose Symbology Direction: what the image shows as the core symbolic representation of Artist Meaning. Symbology is closer to meaning than style, so unresolved symbology should be explored visually before style is locked.

Explore it with a Symbology Board, built as a Comparison Board (see "Visual Gate Boards" below): one single image, a 2x3 grid of six cells, where every cell is plain black-and-white line art of the subject only — no color, shading, style, or background — so style does not obscure the symbolic choice. The six cells compare distinct symbolic representations such as figure, object, landscape, ritual scene, room, threshold, vessel, or abstraction. Wait for the artist to select, combine, reject, or revise options before locking Symbology Direction unless they explicitly choose to proceed unconfirmed.

At the gate, show only six concise symbolic representations and ask: "Which one would you like? Should this become a single image, a compressed arc, or an image series? Would you like it visualized?" Keep the full board prompt internal unless the artist asks for an image-generator prompt.

### Visual Gate Boards

The Symbology Gate and the Style Gate resolve open visual decisions by showing the artist the options laid out together in **one image** so they can compare and choose. This shared mechanic is the Comparison Board.

A Comparison Board is a single provider-neutral image-generation prompt that renders every option together inside one image as a labeled grid. It is never a list of separate prompts and never several images — the whole point is that one generation produces the full comparison. Store that one prompt as `composite_image_prompt` and store the per-cell content as the `visual_prompt` of each option.

The contract for every board:

- **One image, one prompt, one generation.** The `composite_image_prompt` describes the entire grid as a single image. Do not emit one prompt per option.
- **Grid layout.** Default to six cells in a 2x3 grid. Match the cell count to the number of options, never more than three cells per row. Cells are equal size with a small number label (1..N) and the same framing.
- **Hold everything constant except the dimension under test.** A board isolates one decision so the comparison is honest:
  - **Symbology Board** — vary the symbolic representation; every cell is line art of the subject only, no style.
  - **Style Exploration Board** — vary the style; every tile shows the same locked Symbology subject, pose, and framing so only style language changes.
- **Draft versus generate.** Drafting a board means writing its `composite_image_prompt` as text; this needs no provider call and is always allowed. Generating a board means sending that one prompt to a provider to render the image, which requires explicit, per-board generation approval. Both paths produce the same single prompt.
- **Prompt is internal by default.** Do not show `composite_image_prompt` to the artist at a gate unless they explicitly ask for an image-generator prompt. Show concise option labels or one-line descriptions, then ask the gate question.

A fillable skeleton for a Symbology Board prompt:

> One single image. A 2x3 grid of six equal square cells with thin gutters and a small number in each cell's corner. Black-and-white line art only — no shading, no color, plain white background — showing the same [subject] centered in every cell. Cell 1: [symbolic representation A]. Cell 2: [symbolic representation B]. Cell 3: [...]. Cell 4: [...]. Cell 5: [...]. Cell 6: [...]. Render as one image; do not output six separate images.

Do not call a provider-backed generator until the artist explicitly approves that generation call.

Style Direction should answer:

- should this feel photographic, illustrated, painterly, graphic, cinematic, comic, abstract, or material?
- should it look polished, raw, glossy, matte, grainy, minimal, maximal, stylized, or photoreal?
- which style choices preserve Artist Meaning?
- which style choices would flatten or betray the work?

Style Direction may be hybrid, but it must have one Primary Style and bounded Style Modifiers. Do not combine many styles at equal weight.

Style Direction is the last priority. It must not override Artist Meaning, Emotional Structure, Beat Plan, or Visual Dynamics. When a chosen style conflicts with the Target Visual Engine, surface the conflict and adapt the style instead of silently weakening the brief.

Choose Style Direction after the first pass of Artist Meaning, Emotional Structure, Beat Plan, and Symbology Direction, and before Art Critic Review. If the artist names a specific style directly, use it and record the reason. Do not run the full Style Interview unless no style was named. Ask at most one Style Clarifier if the named style is broad or internally ambiguous.

If the artist has not named a specific style, the first style gate is not a menu of styles. Ask whether they already have a specific visual vision or want to explore what art style to use. If they want exploration, ask for a rough direction in their own words, then use that direction to build candidate styles.

The Style Interview should be adaptive. If Artist Meaning or the Reference already points toward a style branch, ask the most useful next clarifier. When no branch is obvious, use this fallback order:

1. Should the image feel camera-based, hand-made, graphic/comic, or synthetic/digital?
2. Should it lean realistic/representational or stylized/abstracted?
3. Should the finish feel polished/glossy, raw/grainy, painterly/textured, or flat/minimal?
4. Should the cultural genre lean contemporary/everyday, surreal/dreamlike, fantasy/mythic, sci-fi/futuristic, historical, dark/horror, playful/whimsical, or folk/traditional?

Stop the Style Interview early when either Primary Style, bounded Style Modifiers, known conflicts, and alignment with Artist Meaning are clear, or when there is enough information to create a useful Style Exploration Board.

After the Style Interview or Style Exploration Board, synthesize a Style Recommendation and ask the artist to use it, adjust it, or name a different style. Do not make the artist assemble taxonomy from raw answers.

When Style Direction is unresolved, make Style a visual gate: ask whether the artist wants to see style options before moving forward. If yes, build a Style Exploration Board as a Comparison Board (see "Visual Gate Boards"): one single image, a 2x3 grid of six tiles, where every tile renders the same locked Symbology subject, pose, and framing in a different candidate style, so only the style language varies. Store the single grid prompt as `composite_image_prompt`. The board lets the artist compare style language without committing to separate full generations, and it does not replace Brief Approval. Default to six tiles, no more than three per row unless the artist asks otherwise. Do not call a provider-backed generator until the artist explicitly approves that generation call. Wait for artist response before locking Style Direction unless they explicitly choose to proceed unconfirmed.

At the gate, show only six concise suggested styles and ask: "Do you want some of these? Do you have something else in mind? Would you like this visualized?" Keep the full board prompt internal unless the artist asks for an image-generator prompt.

Use the Wondermint Category Reference as initial category vocabulary, but do not treat upload categories as the entire art ontology. Style Direction must serve the Creative Brief.
