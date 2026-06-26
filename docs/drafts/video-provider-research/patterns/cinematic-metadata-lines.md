# Draft Pattern: Cinematic Metadata Lines

Status: research draft.

Some compact provider prompts end with fixed metadata lines for location, style, and audio. This can make the prompt easier to paste and can keep provider defaults stable, but it can also override the approved creative direction.

## Draft Rule

Metadata lines should be generated from approved Artist OS records:

- `Location` from Video Scene setting and time of day.
- `Style` from Style Direction and Video Style Expression.
- `Audio` from Audio Plan.

Do not hardcode a universal style line in Artist OS. A named style can be used only when the artist selected it or approved it.

## Risks

- A fixed style line contaminates unrelated work.
- Audio posture becomes generic and loses dialogue, music, or sound-design requirements.
- Location metadata is too short to preserve a meaningful setting.
- Provider exports look consistent but no longer trace to Artist Meaning.
