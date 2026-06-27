# Artistic Theory

Artist Generation treats an artwork as layered evidence. Artist OS should not turn a Reference into a prompt directly. It should first identify what the Reference is, what it does formally, what it seems to feel like, what changes inside it, and what it means to the artist.

## Core Algorithm

Every transformation should satisfy this algorithm:

```text
grab attention
trigger a strong emotion
forge a simple mental link
```

The output should express a feeling, not explain a fact. If a plan cannot name the feeling it is trying to make the audience experience, it is not ready for prompt planning.

Every Beat, Tension Point, image role, Prompt Variant Plan, and Generated Work must target at least one clear emotion or emotional pressure. The emotion can be quiet, conflicted, unresolved, or indirect, but it cannot be absent. Facts, plot points, symbols, objects, style references, and genre choices are useful only when they help create that felt response.

## Layer Index

The layered evidence model and its shared visual-planning contracts live in per-topic files under `theory/`. Load only the one the current step needs:

- Layer 1: Reference, Layer 2: Artist Meaning — what the Reference is and the Decision Interview that captures Artist Meaning — `theory/reference-and-meaning.md`
- Layer 3: Formal Analysis, Layer 4: Emotional Structure — observable properties and the Core Tension Pairs emotional model — `theory/formal-and-emotional.md`
- Layer 5: Visual Dynamics — the formal engine, the Series Amplitude Plan, Shot Design, and minimum tension criteria — `theory/visual-dynamics.md`
- Layer 6: Style Direction — Stage Completion, the Visual Gate Boards / Comparison Board contract, and the Style Interview — `theory/style-direction.md`
- Layer 7: Beats And Tension Points, Layer 8: Series Recommendation, Layer 9: Meaning-Preserving Transformation — beat mechanics, series calibration, and medium transformation — `theory/beats-series-transformation.md`
- Prompt Variant Plans, First Slice — the Prompt Variant Strategy and the dry-run First Slice — `theory/prompt-variant-plans.md`

When another document points at `THEORY.md → "Visual Gate Boards"`, `THEORY.md → "Stage Completion"`, or the Style Interview, read `theory/style-direction.md`. When it points at `THEORY.md → minimum tension criteria`, the Series Amplitude Plan, or Shot Design, read `theory/visual-dynamics.md`. When it points at Prompt Variant Plans, read `theory/prompt-variant-plans.md`.
