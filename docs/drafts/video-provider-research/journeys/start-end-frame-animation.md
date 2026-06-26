# Draft Journey: Start/End Frame Animation

Status: research draft.

## End Product

A controlled animation that moves from an approved start frame to an approved end frame.

## Likely Inputs

- Start frame.
- End frame.
- Character or subject reference.
- Motion description.
- Camera path.
- Duration and aspect ratio.

## Prompt Needs

- Start-frame provider binding.
- End-frame provider binding when supported.
- Clear middle action.
- Continuity rules between frames.
- Camera movement that does not fight the frame transition.

## Known Risks

- The provider jumps from first image to last without believable transition.
- The middle action is too vague.
- The final frame is ignored or only loosely reached.
- Character identity or style changes between frames.

## Artist OS Mapping

Start and end frames should be Output Records before provider video export. The provider export should reference both frames and link back to the Storyboard Shot or sequence they realize.
