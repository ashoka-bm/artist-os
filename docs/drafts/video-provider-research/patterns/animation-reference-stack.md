# Draft Pattern: Animation Reference Stack

Status: research draft.

Animated video workflows need a reference stack before provider prompting. The stack can include a character sheet, style-restyled sheet, start frame, end frame, storyboard sheet, environment reference, and mixed-media subject references.

## Draft Principle

Use the smallest reference stack that controls the output. Strong visual references should reduce prompt length, not invite the prompt to re-describe every detail.

## Reference Types

- Character sheet: locks the character's design across motion.
- Style-restyled sheet: locks the visual language before animation.
- Start frame: anchors the first frame or initial composition.
- End frame: anchors the target reveal or final composition.
- Storyboard sheet: anchors several beats in order.
- Environment reference: controls setting or texture.
- Location sheet: anchors a reusable setting across several scenes or camera angles.
- Scene still: anchors a specific shot or scene before motion export.
- Mixed-media reference: separates animated subjects from live-action subjects.

## Artist OS Mapping

- Character sheet and style-restyled sheet map to Visual Reference Sheet Plan or calibration Output Records.
- Start and end frames map to Output Records linked to a Storyboard Shot.
- Storyboard sheet maps to storyboard-ready package output.
- Location sheets may map to Visual Reference Sheet Plan with a setting role until a dedicated setting-reference artifact exists.
- Scene stills map to storyboard stills or calibration Output Records.
- Provider export records should bind each reference to its provider role and scope.

## Risks

- Too many references conflict.
- A style reference overrides character identity.
- A storyboard sheet gives sequence but not enough motion detail.
- Start and end frames constrain composition but leave the middle action under-specified.
