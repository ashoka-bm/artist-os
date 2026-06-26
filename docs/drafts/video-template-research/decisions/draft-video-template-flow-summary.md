# Draft Video Template Flow Summary

Status: draft consolidation.

Date: 2026-06-26

This summary consolidates draft Decisions 0001-0016. It is not a canonical ADR. Do not use it to change the main Artist OS skill, schemas, or Video Journey until promotion is approved.

## Core Decision

Artist OS should separate story movement, narrative depth, format, direction, and provider export.

Story movement belongs upstream. Video format belongs in Video Medium Plan. Provider-specific execution belongs after storyboard approval.

## Proposed Flow

1. **Orientation**
   - Capture Format Intent.
   - Capture provider preference if the artist names one.
   - Capture provisional Narrative Depth.

2. **Meaning Interview / Artist Meaning**
   - Capture Artist Meaning, must-preserve constraints, audience, and Intended Feeling.

3. **Beat Plan**
   - Select or adapt Story Structure for `full_story` outputs.
   - Define the turn, tension, misconception, desire, or promise the hook must open.
   - Preserve story authority.

4. **Medium Output Shape Recommendation**
   - Confirm or revise Format Intent.
   - Confirm Narrative Depth.
   - Recommend likely Format Template.

5. **Video Medium Plan**
   - Record binding Narrative Depth.
   - Select binding Format Template.
   - Reference selected Story Template or Micro-Journey Template when applicable.
   - Choose hook posture.
   - Choose speaker posture when speaker-led.
   - Set Video Audio Posture.
   - Set Video Style Expression.
   - Set reference strategy.
   - Define storyboard scope.
   - Preserve provider preferences as non-binding notes.

6. **Script / Storyboard Drafting**
   - Apply hook posture.
   - Apply conversational voice and point-plus-paint support when speaker-led.
   - Apply moment anchors when a beat needs immediacy.
   - Translate the Video Medium Plan into scenes and Storyboard Shots.

7. **Storyboard Approval**
   - Locks the provider-neutral storyboard-ready package.

8. **Production Route**
   - Choose Seedance 2, Higgsfield, OpenMontage, Remotion, HyperFrames, FFmpeg, or another route.
   - Account for references, duration, audio, style, shot complexity, provider limits, budget, and generation approval.

9. **Provider Export**
   - Render platform-specific prompts or production packets.
   - Preserve approved story, format, hook, delivery posture, references, and storyboard decisions.

## Narrative Depth

| Narrative Depth | Required Structure | Examples |
| --- | --- | --- |
| `full_story` | Story Template | personal story, documentary mini-arc, reframe explainer |
| `micro_journey` | Micro-Journey Template | unboxing, product reveal, UGC testimonial, fashion fit check |
| `utility_sequence` | Asset Purpose Brief or utility sequence plan | title card, b-roll loop, product spin, style test |

## Direction Notes

Direction Notes are craft rules. They do not own story authority.

Current direction-note families:

- hook-entry patterns,
- on-camera connection and delivery,
- zoom into the moment,
- Seedance 2 direction,
- narrative-depth routing,
- edit cut vocabulary.

## Accepted Draft Decisions

- `0001`: Format Intent is a strong preference.
- `0002`: Story Templates live with Story Structure.
- `0003`: On-camera delivery placement.
- `0004`: Hook posture placement.
- `0005`: Production Route after storyboard.
- `0006`: Narrative Depth routing.
- `0007`: Narrative Depth placement.
- `0008`: Format Template binding.
- `0009`: Video Medium Plan payload.
- `0010`: Scene embodiment placement.
- `0011`: Micro-Journey Template placement.
- `0012`: Utility sequence representation.
- `0013`: Create draft implementation summary now.
- `0014`: Edit cut vocabulary placement.
- `0015`: Schema fields vs skill guidance.
- `0016`: Create Video Medium Plan extension note.

## Promotion Questions

- Should Narrative Depth become a field on Video Medium Plan, Workflow Scale Routing, or both?
- Should Micro-Journey Templates become a subtype of Cultural Format Structure or a separate Video Template library?
- Should Asset Purpose Brief become a new record, a Video Medium Plan section, or an adapter-local planning packet?
- Which parts need schema support before implementation?
- Which parts can remain skill guidance for the first pass?

## Revisit Note

Do not promote this summary into canonical docs, schemas, or implementation plans yet.

Revisit promotion after sample walkthroughs for:

- one `full_story`,
- one `micro_journey`,
- one `utility_sequence`.
