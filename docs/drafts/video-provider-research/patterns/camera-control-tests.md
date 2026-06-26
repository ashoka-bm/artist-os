# Draft Pattern: Camera Control Tests

Status: research draft.

Camera movement can be treated as a test axis in animation provider research. The animation prompt pack shows several camera-control types: pan, tracking shot, first-person POV, orbit, macro zoom, side-scroll, and fixed security-camera framing.

## Draft Principle

Separate camera-control exploration from final narrative generation. A camera-control test should isolate one camera behavior and one clear character action.

## Test Types

- Pan: camera moves horizontally with or across the action.
- Tracking: camera follows behind, beside, or ahead of the subject.
- POV: camera represents the character's viewpoint.
- Orbit: camera circles a mostly stationary subject.
- Macro zoom: camera moves into an extreme detail or reflection.
- Side-scroll: camera moves laterally with a subject in profile.
- Fixed camera: camera remains locked while action moves through frame.

## Prompt Needs

- One primary action.
- One camera behavior.
- Clear start and end composition.
- Motion speed and steadiness.
- Whether cuts are allowed.
- Whether motion blur is desired or harmful.

## Artist OS Mapping

Camera-control tests map to `Storyboard Shot.camera_movement`, Shot Design, and Motion / Pacing / Transition Gate. They can become provider dry-runs before committing to a full generated sequence.
