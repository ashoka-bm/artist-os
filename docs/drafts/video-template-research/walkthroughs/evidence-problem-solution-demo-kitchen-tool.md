# Evidence Walkthrough: Problem-Solution Demo For A Kitchen Tool

Status: research draft.

Candidate tested: `problem_solution_demo`.

## Sample Request

Create a 20-30 second vertical short for a compact kitchen scraper that helps home cooks clean sticky dough and chopped herbs from a cutting board without wasting food or time.

The video should open on a familiar frustration: a cook tries to move sticky dough from the board, loses half of it on their fingers, and makes the counter messier. The scraper enters as the simple tool that changes the workflow. The viewer should leave feeling, "That fixes an annoying thing I know."

## Routing Decision

- `narrative_depth`: `micro_journey`.
- Candidate template: `problem_solution_demo`.
- Current schema-supported fallback: `quick_before_after_demo`.
- Cultural Format Structure: `short_social_hook_loop`, with light `product_explainer_demo` support.
- Provider posture: provider-neutral. No Seedance, Higgsfield, or render-platform assumptions.

## Why This Is Not `full_story`

The video does not need a complete Story Structure. It has no character arc, reversal, or lasting transformation. The viewer movement is compact:

1. Recognize the friction.
2. See the tool enter.
3. Watch the problem resolve.
4. Remember the relief.

## Why This Is Not `utility_sequence`

The video is not just a food-prep B-roll insert or product-use asset. The problem must be felt before the solution matters. The output needs a hook, proof, and payoff, not only a clean demonstration sequence.

## Candidate Micro-Journey Fit

`problem_solution_demo` fits because the video is organized around a named irritation and a causal fix.

Core movement:

```text
mess/friction -> simple tool enters -> problem visibly resolves -> relief/payoff
```

Required decisions:

- What exact kitchen frustration opens the video?
- How quickly can the frustration be understood without voiceover?
- What visible action proves the tool solves the problem?
- What final state shows relief: clean board, saved dough, faster transfer, or calmer cook?
- Should the close loop back to the opening mess?

## Nearest Current Schema-Supported Id

Use `quick_before_after_demo` as the schema-supported fallback.

Why it is insufficient:

- The changed state matters, but the key movement is problem recognition and relief.
- A generic before/after could show dirty board -> clean board without making the viewer feel the sticky, annoying moment.
- `problem_solution_demo` preserves the problem as the hook and the solution as the emotional release.

`product_reveal` is less accurate because the product is not the attraction by itself. The attraction is the solved frustration.

## Cultural Format Structure Fit

Primary fit: `short_social_hook_loop`.

Why:

- The opening must be instantly legible on a phone.
- The payoff can visually echo the opening: sticky mess -> clean transfer -> same motion now resolved.
- The ending can loop back to the initial cutting board setup.

Secondary fit: `product_explainer_demo` because the tool needs one clear use action, but the explainer layer should stay minimal.

## Required Video Medium Plan Payload

The Video Medium Plan should carry:

- `narrative_depth = micro_journey`;
- `micro_journey_template_ref = problem_solution_demo`;
- rationale note: candidate pattern is `problem_solution_demo`;
- object of attention: compact kitchen scraper;
- viewer reason to care: sticky prep mess becomes simple and controlled;
- problem visual: dough or chopped herbs sticking to fingers, knife, and board;
- solution entry: scraper slides under the food cleanly;
- proof visual: one clean transfer into a bowl or pan;
- payoff: board and hands stay clean, food is saved, workflow continues;
- ending beat: same board action repeated cleanly;
- audio/text posture: voiceover-led, caption-led, or silent with text labels;
- reference needs: product appearance, food texture, kitchen surface, hand scale;
- provider notes: downstream only after storyboard approval.

## Draft Shot / Beat Outline

1. **Hook / Problem Image**
   Close shot of sticky dough clinging to fingers and smearing across the cutting board.

2. **Problem Escalation**
   The cook tries to use a knife edge or fingers; the dough stretches, tears, and leaves residue.

3. **Solution Entry**
   The scraper appears beside the board. One hand slides it under the dough in a controlled motion.

4. **Proof Step**
   The scraper lifts and transfers the dough cleanly into a bowl. Hold long enough to show the clean board path.

5. **Relief Detail**
   Quick insert of clean fingers, less residue, and the scraper collecting the last bits.

6. **Payoff / Loop**
   Return to the board setup, but now the same motion is clean and repeatable. Optional text: "One move. Less mess."

## Risks And Common Failure Modes

- The problem is not sticky or annoying enough, so the solution feels trivial.
- The video becomes a generic product demo with no emotional friction.
- The proof is too fast to read.
- The tool appears magical because the messy step is skipped.
- Food styling becomes the focus instead of the solved workflow.
- The final payoff is a slogan without a visible clean result.

## Promotion Recommendation

Recommendation: **promote `problem_solution_demo`**.

This second distinct walkthrough confirms the candidate works outside software. It is not just a variant of `quick_before_after_demo`; it preserves a repeatable audience movement:

- the viewer recognizes a concrete friction;
- the solution enters after the problem is felt;
- proof shows causal relief;
- the ending lands on a solved state.

`problem_solution_demo` is now promoted into `micro_journey_template_ref`.

## What This Teaches The Framework

`problem_solution_demo` is a general-purpose short-form shape for product, service, workflow, and teaching videos. It should not be collapsed into `product_reveal` or `quick_before_after_demo`.

The reviewer check should ask: is the problem visible, does the solution directly address it, and does the payoff show relief rather than polish alone?
