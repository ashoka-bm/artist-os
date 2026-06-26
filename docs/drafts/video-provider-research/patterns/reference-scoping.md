# Draft Pattern: Reference Scoping

Provider video prompts need explicit reference scope. A reference can control identity, prop form, wardrobe, composition, style, lighting, or inspiration. The prompt should say which job each reference performs and what should not transfer.

## Scope Types

- Identity reference: controls face, body, and continuity.
- Prop reference: controls a named object.
- Wardrobe reference: controls clothing, material, and fit.
- Composition reference: controls framing and spatial arrangement.
- Style reference: controls visual language, color, or rendering style.
- Lighting reference: controls light direction, intensity, color, and shadow.
- Inspiration-only reference: informs the agent's description but should not be tagged in the provider prompt.
- Close-up face reference: controls skin texture, eyes, facial feature accuracy, and small identity details.
- Product sheet reference: controls product shape, materials, label, logo, and visible surfaces.
- Garment or outfit reference: controls silhouette, cut, fabric, construction, colorway, styling, footwear, and accessories.
- Avatar or Soul reference: controls presenter identity in provider-specific commercial workflows.
- Character sheet reference: controls animated character design and proportions.
- Start frame reference: controls the first frame of a video.
- End frame reference: controls the intended final frame or reveal.
- Storyboard reference: controls sequence order and major beat progression.
- Location sheet reference: controls setting continuity and available staging areas.
- Scene still reference: controls one scene's composition, mood, and subject placement.

## Provider Tag Placement

Some providers expose uploaded media as short session tags. Those tags are provider bindings, not durable Artist OS ids.

Draft tag rules for Seedance-style prompt export:

- Confirm the current tag mapping before rendering the prompt.
- Keep whitespace around each tag.
- Place the tag next to the noun it controls.
- Reintroduce the relevant tag in every shot where the subject, prop, style, or audio is needed.
- Do not use a loose tag list when the provider needs inline binding.
- Mirror provider tags in any human review translation.

## Draft Rule

Every provider export should carry a reference-scope block before final prompt rendering. This block should remain outside the neutral Video Medium Plan until the provider export layer proves its shape.

## Risk

Unscoped references can bleed unwanted faces, colors, lighting, compositions, or objects into the output. Over-describing an identity reference can also fight the provider's image-conditioning behavior.
