# Evidence Walkthrough: Documentary Mini-Profile For A Ceramicist

Status: research draft.

Candidate tested: `documentary_mini_profile`.

## Sample Request

Create a 60-90 second mini-profile of a ceramicist who makes small-batch cups. The surface topic is handmade pottery, but the real value is the maker's judgment: knowing when a piece should stay imperfect, when to trim, when to discard, and when a glaze accident becomes the point.

The piece should feel observed, tactile, and human. It should not become a product ad, craft tutorial, or generic studio montage.

## Routing Decision

- Candidate Cultural Format Structure: `documentary_mini_profile`.
- Recommended `narrative_depth`: `micro_journey`.
- Current schema-supported fallback: `creator_showcase_moment`.
- Story Template influence: Observation Reframe Move.
- Provider posture: provider-neutral.

## Recommended Narrative Depth And Alternatives

Recommended: `micro_journey`.

Why: the viewer moves from "this person makes cups" to "this person is making taste decisions under uncertainty." The piece has a hook and payoff, but it does not need a full life arc.

Alternatives:

- `full_story`: use if the ceramicist's career change, public failure, or personal transformation becomes the governing movement.
- `utility_sequence`: use only if the output is a functional studio B-roll package without profile meaning.

## Story Template Fit

Primary influence: Observation Reframe Move.

Structure:

1. Signal: the maker shapes a cup.
2. Common read: handmade pottery is about craft and prettiness.
3. Reframe: the real work is judgment under uncertainty.
4. Proof: the maker keeps one irregular mark and discards another piece.
5. Payoff: the viewer sees authorship in the decision, not just the object.

Secondary influence: Human Kebab if the piece opens on a tactile studio detail, widens into context, then returns to the maker with changed meaning.

## Proposed Cultural Format Structure Shape

`documentary_mini_profile` should carry:

- human entry;
- observed work;
- context / nut graf;
- tension or common misread;
- proof through action, decision, artifact, or response;
- return to the opening person or action;
- kicker that lands the profile's point.

This shape worked for the AI creator profile and still works for a non-AI craftsperson, which suggests it is a true format grammar rather than an AI-workflow-specific pattern.

## Required Video Medium Plan Payload

The Video Medium Plan should carry:

- `narrative_depth = micro_journey`;
- `micro_journey_template_ref = creator_showcase_moment`, when the creator's judgment is the compact memory;
- Cultural Format Structure rationale: `documentary_mini_profile`;
- human subject and role: ceramicist;
- profile promise: taste is visible in what the maker keeps, changes, and rejects;
- observed-work scenes: wheel, trimming, glaze, shelf, discard bin;
- context / nut graf: handmade work is a series of judgment calls;
- tension: imperfection can be flaw or character;
- proof object: one kept irregular cup and one discarded piece;
- return/kicker image: the finished cup in hand, with the irregular mark now meaningful;
- audio posture: interview-led, voiceover-led, or mixed;
- text refs: name/title and one short phrase only;
- reference needs: studio, tools, clay texture, hands, finished pieces;
- provider notes: downstream only after storyboard approval.

## Draft Shot / Beat Outline

1. **Human Entry**
   Close shot of clay wobbling slightly under the ceramicist's hands. The maker pauses instead of forcing it smooth.

2. **Observed Work**
   Medium shot of the studio: wheel, shelves, trimming tools, drying cups. The viewer meets the work before explanation.

3. **Context / Nut Graf**
   Interview or voiceover ref: "Most people think the goal is perfect. The harder part is knowing which imperfection belongs."

4. **Common Misread**
   Quick fragments of finished cups on shelves. The obvious read is beauty, craft, and product.

5. **Tension**
   The maker examines two pieces: one with an irregular rim, one with a cracked foot. Both are imperfect, but not equally alive.

6. **Proof Of Judgment**
   The cracked piece goes to the discard area. The irregular rim stays. The maker makes the decision visible without overexplaining.

7. **Observed Consequence**
   Glaze is applied to the kept cup in a way that makes the irregular rim feel intentional.

8. **Return**
   Return to the opening hand-and-clay gesture, now understood as authorship rather than hesitation.

9. **Kicker**
   Final shot of the finished cup in someone's hand. The irregular mark catches light. The piece ends on the decision, not the sale.

## Risks And Common Failure Modes

- The profile becomes a product ad for cups.
- The video turns into a pottery tutorial.
- The subject explains judgment but never demonstrates it.
- The piece has beautiful studio atmosphere but no nut graf.
- The tension between flaw and character is too vague.
- The ending displays product polish without returning to meaning.
- On-screen text over-explains what the observed action can show.

## Promotion Recommendation

Recommendation: **promote `documentary_mini_profile` as a Cultural Format Structure**.

This second walkthrough confirms the format works outside AI-creator content. The shared structure is stable:

- human entry;
- observed work;
- context / nut graf;
- tension;
- proof through decision;
- return;
- kicker.

It should not become a Story Template because it is not one fixed narrative argument. It should not become a Micro-Journey Template because it is an audience-facing format grammar that can support `micro_journey` or, in larger cases, `full_story`.

## What This Teaches The Framework

The framework needs a named documentary profile format so agents do not force profile requests into explainer, showcase, testimonial, or mood montage shapes.

The reviewer check should ask: do we meet a specific human through observed behavior, does the nut graf reframe the work, does proof happen through action, and does the ending return with new meaning?
