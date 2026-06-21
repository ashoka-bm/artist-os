# Schema-backed Release Package Plan

Status: accepted.

Artist OS will introduce a schema-backed Release Package Plan as the package-level coordination record for multi-output artist releases, with Album as the first implemented package subtype. The schema should use the generic release-package name rather than an album-only name because Album, EP, Single Bundle, and Visual Album are sibling Release Package subtypes, but only Album behavior is implemented in v1.

The Release Package Plan is created after the Album Beat Plan and before full medium-specific expansion. It coordinates deliverables, package subtype, Album Cohesion Mode, track-to-deliverable mapping, production order, Album Calibration, Album Sonic System, Album Visual System, cross-media continuity decisions, and references to governing records; it does not replace Sound Medium Plans, Image Medium Plans, Text Medium Plans, Long-Work Stewardship Records, Prompt Plans, Text Generation Plans, or Output Records.

## Consequences

- Album v1 can coordinate tracks, album cover, Track Covers, title, description, calibration, and package-level review without scattering package decisions across medium records.
- Album v1 uses package-level review both before Album Calibration, to confirm the package is coherent enough to test, and after Album Calibration, to confirm the calibrated direction is strong enough to expand.
- Future EP, Single Bundle, Visual Album, and campaign support can reuse the top-level Release Package concept without renaming an album-only schema.
- Medium-specific creative authority remains local to existing Medium Plans and downstream prompt or generation records.
