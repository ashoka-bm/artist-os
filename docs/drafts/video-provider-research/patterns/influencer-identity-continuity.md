# Draft Pattern: Influencer Identity Continuity

Status: research draft.

AI influencer workflows need identity continuity before they need provider prompts. The DaanKieft AI Influencer repository treats the influencer as a persistent entity with images, prompts, wardrobe, backstory, generated variations, character sheets, and later photo/video outputs.

## Draft Principle

When the same person must appear across stills, videos, campaigns, or variants, create an identity system first. Do not rely on a single provider prompt to hold continuity across a batch.

## Likely Materials

- Main identity image.
- Character reference sheet or visual reference sheet.
- Close-up face details.
- Wardrobe cards.
- Optional backstory or persona notes.
- Product or prop reference sheets.
- Generated calibration stills.

## Reference Roles

- Identity: face, body, skin, hair, age, proportions.
- Wardrobe: outfit only.
- Close-up detail: skin texture, eye color, facial feature accuracy.
- Product: product shape, label, material, branding.
- Scene or style: setting, composition, color, or motion reference.

## Artist OS Mapping

- Character Template stores persistent persona and continuity constraints.
- Visual Reference Sheet Plan stores the plan for identity or product sheets.
- Output Records store generated or imported reference sheets and calibration stills.
- Provider export records bind local assets to provider-specific media roles.

## Risks

- One prompt tries to do identity, wardrobe, product, action, and camera logic at once.
- Wardrobe and identity references bleed into each other.
- A campaign batch uses random avatars and loses consistency.
- Generated identity assets are not recorded before downstream video work starts.
