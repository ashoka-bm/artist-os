# Visual Dynamics

## Layer 5: Visual Dynamics

Visual Dynamics names the formal forces that make a visual work active, coherent, tense, immersive, unstable, or memorable.

Keep Visual Dynamics separate from Emotional Structure. Emotional Structure describes the felt charge. Visual Dynamics describes the formal engine.

For text-to-image, Visual Dynamics describes the Target Visual Engine of the generated image. It does not pretend the text literally has visual properties. Each visual choice must trace back to Artist Meaning, Reference evidence, Emotional Structure, Beat Plan, or Critical Heuristics.

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

### Series Amplitude Plan

When recommending an image series, add an internal Series Amplitude Plan to each suggested image. This is not a user-facing gate. It is a 0-1 numeric profile that keeps the series from repeating the same visual distance, density, motion, and scale.

Each suggested image gets:

- `framing_distance`: 0 = extreme close-up/intimate crop, 1 = panoramic or very wide framing.
- `subject_scale`: 0 = tiny or fragile subject presence, 1 = monumental or dominant subject presence.
- `visual_density`: 0 = sparse/minimal field, 1 = crowded/maximal field.
- `motion_energy`: 0 = still/static, 1 = active/turbulent.
- `spatial_openness`: 0 = enclosed/compressed, 1 = open/expansive.
- `detail_intensity`: 0 = stripped down/minimal detail, 1 = highly detailed/layered.
- `emotional_pressure`: 0 = quiet/low pressure, 1 = overwhelming/high pressure.

Across a series, adjacent images should usually change amplitude on at least two dimensions unless continuity is intentional. Tie amplitude changes to the Beat Plan or Emotional Arc: intimate pressure can move closer, expansive consequence can move wider, rupture can increase motion, and aftermath can reduce density or motion while keeping pressure high.

For series work, also create a per-image tension profile for the active emotional and visual tensions. Adjacent images should not carry the same tension shape unless repetition is the point and is explicitly traced to Artist Meaning. For example, if one image carries high attraction and high threat, the next might hold low attraction and high threat, or high attraction and low threat, so the series produces a felt shift rather than repeating the same charge.

### Shot Design

Every Image Role must include a Shot Design: shot scale, camera angle, visual emphasis, composition strategy, emotional rationale, and what to avoid. Shot Design is part of Visual Dynamics because the camera distance and viewpoint decide what the audience feels first.

Use shot scale as emotional grammar:

- Extreme close-up or close-up: use for internal pressure, reaction, fragile detail, embodied fear, symbolic objects, or a decision point that should feel unavoidable.
- Medium close-up or medium shot: use when face, gesture, body language, and immediate context must all stay readable.
- Medium wide: use when the body, threshold, relationship, or action needs space but should still feel personally attached.
- Wide or extreme wide: use for environment, isolation, scale, consequence, aftermath, active absence, or a subject overwhelmed by place.

Use camera angle as pressure:

- Eye-level keeps the viewer intimate, present, or observational.
- High angle can weaken, isolate, expose, or make a subject feel vulnerable.
- Low angle can make a subject, object, place, or threat feel powerful.
- Overhead can turn a scene into fate, pattern, ritual, or evidence.
- Dutch/canted angle can express instability, dread, rupture, or moral unease.
- Over-the-shoulder and point-of-view can make the audience share a relationship or subjective perception.

Do not default to a full-body shot. A full-body or medium-wide frame is correct only when the Beat needs the whole posture, spatial relationship, action, or threshold. If the emotional payload lives in a face, hand, object, absence, or environmental consequence, crop or pull back accordingly.

### Minimum Tension Criteria

Every Beat Plan and Medium Plan must define minimum tension criteria before prompt planning. These criteria are not universal taste scores; they are project-local thresholds that tell reviewers how much contrast or movement the work needs to satisfy Artist Meaning.

For a single image, the criteria should require enough internal contrast that the image creates pressure without needing explanation. Default when the artist has not specified otherwise: at least two active tensions, with one primary emotional or visual tension at `0.7` or higher.

For an image series, the criteria should require movement between adjacent images. Default when the artist has not specified otherwise: adjacent images shift at least two amplitude dimensions and at least one active emotional or visual tension, while changing composition, communication intent, and at least one Shot Design axis: shot scale, camera angle, visual emphasis, or composition strategy.

Reviewers should block when an artifact falls below its own minimum tension criteria unless the artist explicitly approves low-contrast repetition as the point.
