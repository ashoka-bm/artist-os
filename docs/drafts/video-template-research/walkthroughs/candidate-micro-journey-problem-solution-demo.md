# Candidate Micro-Journey Walkthrough: Problem-Solution Demo

Status: research draft.

Candidate tested: `problem_solution_demo`.

## Sample Request

Create a 20-30 second short social video for an AI video workflow tool.

The audience is creators who waste hours planning B-roll for explainers. The video should show the friction of staring at a blank timeline, then show the tool turning one approved still into a repeatable shot plan. The viewer should leave believing the tool removes planning friction without replacing creative judgment.

## Routing Decision

- `narrative_depth`: `micro_journey` candidate.
- Candidate template: `problem_solution_demo`.
- Current schema-supported fallback: `quick_before_after_demo` or `product_reveal`.
- Cultural Format Structure fit: `short_social_hook_loop` with support from `product_explainer_demo`.
- Provider posture: provider-neutral. No Seedance, Higgsfield, or render-platform assumptions.

## Why This Is Not `full_story`

This video does not need a complete Story Structure. It does not require a character arc, deep escalation, irreversible decision, or final changed identity.

The audience movement is compact:

1. Recognize the friction.
2. See the solution enter.
3. Trust the proof.
4. Understand the payoff.

That is enough for a short social proof-of-value video.

## Why This Is Not `utility_sequence`

The request is not only asking for a reusable B-roll package, title card set, loop, or process asset. It asks the viewer to move from frustration to relief.

The tool, not the asset package, is the point of attention. The video needs a compact audience journey, not just `asset_purpose_brief`.

## Candidate Micro-Journey Fit

`problem_solution_demo` fits because the viewer's reason to care begins with a relatable problem:

- creators waste time planning B-roll;
- blank timelines and messy notes create friction;
- one approved still becomes a structured shot plan;
- the payoff is repeatable creative control.

Core movement:

```text
friction -> solution enters -> visible proof -> relief/payoff
```

Required decisions:

- What exact problem opens the video?
- What makes the problem visually legible in the first seconds?
- What solution action should enter: upload still, select workflow, generate plan, approve shot list, or preview storyboard?
- What proof makes the claim believable?
- What final state should the viewer remember?

## Nearest Current Schema-Supported Id

Use `quick_before_after_demo` as the nearest schema-supported id if this walkthrough must become a validating Video Medium Plan today.

Why it is insufficient:

- `quick_before_after_demo` centers visible state change.
- This sample centers problem relief and causal solution logic.
- The proof is not only before/after. It is problem recognition, solution entry, structured output, and creative confidence.

Use `product_reveal` only if the video's main job becomes introducing the tool as an object or offer. That would weaken the problem-solution movement.

## Cultural Format Structure Fit

Primary fit: `short_social_hook_loop`.

Why:

- The first frame must show friction immediately.
- The payoff should arrive quickly.
- The ending can loop back to the problem: blank timeline -> structured plan -> no more blank timeline.

Secondary fit: `product_explainer_demo`.

Why:

- The tool needs a brief "how it works" proof.
- The video should show the relationship between approved still, generated shot plan, and creator approval.

## Required Video Medium Plan Payload

The Video Medium Plan should carry:

- `narrative_depth = micro_journey`;
- `micro_journey_template_ref = problem_solution_demo`;
- rationale note: candidate pattern is `problem_solution_demo`;
- hook posture: creator stuck before planning B-roll;
- object of attention: AI video workflow tool;
- viewer reason to care: less planning friction, more repeatable creative direction;
- problem visual: blank timeline, scattered notes, unclear B-roll list;
- solution entry: approved still becomes structured shot plan;
- proof visual: generated shot cards, scene order, or storyboard-ready outline;
- payoff: creator can approve, adjust, and animate from a clear plan;
- ending beat: blank timeline replaced by organized storyboard/shot plan;
- text/audio posture: voiceover-led or caption-led; no required music;
- reference needs: approved still, product UI state, example shot-card layout;
- provider notes: downstream only after storyboard approval.

## Draft Shot / Beat Outline

1. **Hook / Problem Image**
   Close shot of a creator looking at a blank timeline or empty B-roll board. On-screen text or voiceover names the friction: "Planning B-roll should not take the whole afternoon."

2. **Problem Detail**
   Quick inserts of scattered notes, unclear shot ideas, and a half-finished explainer outline. The viewer should understand the pain without a long setup.

3. **Solution Entry**
   The approved still appears as the anchor input. The tool interface or planning surface turns it into a structured starting point.

4. **Proof Step**
   The still expands into 4-6 planned shot cards: hook shot, process insert, detail close-up, transition, payoff frame. The proof should be visual, not only verbal.

5. **Creator Control Beat**
   The creator approves, reorders, or adjusts one shot card. This keeps the tool from feeling like it replaces creative judgment.

6. **Payoff / Relief**
   The blank timeline is now a clean storyboard-ready shot plan. End on the organized plan beside the original approved still.

7. **Loop Or Exit Beat**
   Optional loop: final organized plan visually echoes the opening blank board. Optional exit: "Still first. Approve. Animate."

## Risks And Common Failure Modes

- The opening problem is too vague, so the solution feels unearned.
- The video becomes a generic product reveal instead of problem relief.
- The before/after is cosmetic: messy screen to clean screen, but no clear workflow value.
- The tool appears to replace creative judgment instead of supporting it.
- The proof shot is unreadable on mobile.
- Too many UI details slow the micro-journey.
- The ending gives a slogan without showing the planned output.

## Promotion Recommendation

Recommendation: **promote, after one more distinct walkthrough**.

This candidate is meaningfully different from the current schema-supported ids:

- It is broader than `quick_before_after_demo`.
- It is more problem-led than `product_reveal`.
- It covers a common short-form and UGC pattern: pain, solution, proof, relief.

The second non-software sample worked; `problem_solution_demo` has been promoted into the `micro_journey_template_ref` enum.

## What This Teaches The Framework

`problem_solution_demo` fills a real gap between `product_reveal` and `quick_before_after_demo`.

The framework needs this distinction:

- `product_reveal`: the product is the attraction.
- `quick_before_after_demo`: the visible changed state is the proof.
- `problem_solution_demo`: the audience recognizes a friction, sees the solution enter, and trusts the causal relief.

This candidate also clarifies reviewer criteria. Video Critic Review should check whether the problem is legible, the solution actually addresses it, and the proof shows relief rather than only polish.
