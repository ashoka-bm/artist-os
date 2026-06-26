# Evidence Walkthrough: Social Proof Receipt For Waitlist Demand

Status: research draft.

Candidate tested: `social_proof_receipt`.

## Sample Request

Create a 15-25 second vertical launch short for a creator template pack. The video should open with a waitlist counter and a few anonymized request snippets from creators asking for the pack. Then it should reveal that the first version is available.

The viewer should feel that the product is being released in response to visible demand, not pushed cold.

## Routing Decision

- `narrative_depth`: `micro_journey`.
- Candidate template: `social_proof_receipt`.
- Current schema-supported fallback: `ugc_testimonial`.
- Cultural Format Structure: `short_social_hook_loop`, with optional `product_explainer_demo` support.
- Provider posture: provider-neutral.

## Why This Is Not `full_story`

This video does not need a full story arc. The movement is a compact credibility sequence:

1. Demand exists.
2. The viewer sees proof of demand.
3. The release appears as the answer.
4. The viewer knows why it matters now.

## Why This Is Not `utility_sequence`

The video is not just a launch graphic or receipt montage. The proof changes the viewer's stance from "why should I care?" to "people like me already asked for this." That trust movement makes it a micro-journey.

## Candidate Micro-Journey Fit

`social_proof_receipt` fits because the proof artifact is the trust carrier.

Core movement:

```text
demand signal -> proof detail -> release/context -> reason people care -> action/payoff
```

Required decisions:

- What proof artifact opens the video: waitlist, comments, requests, reviews, or DMs?
- Is the proof real, anonymized, dramatized, or composite?
- What privacy and claim-safety notes are needed?
- What product/context appears after the proof?
- What action or payoff closes the video?

## Nearest Current Schema-Supported Id

Use `ugc_testimonial` as the schema-supported fallback.

Why it is sufficient:

- Both build trust through evidence from other people.
- Both need claim, consent, and proof safety handling.
- Both can use social evidence before asking for action.

Why it is insufficient:

- `ugc_testimonial` implies a person or user experience carries the claim.
- This video centers the waitlist and request artifacts.
- The key review questions are proof provenance, legibility, privacy, and whether the product reveal answers the demand.

## Cultural Format Structure Fit

Primary fit: `short_social_hook_loop`.

Why:

- The proof should appear in the first seconds.
- The release reveal should arrive quickly.
- The ending can loop back to the waitlist counter or request snippet.

Secondary fit: `product_explainer_demo` only if the release includes one concise shot of what is inside the template pack.

## Required Video Medium Plan Payload

The Video Medium Plan should carry:

- `narrative_depth = micro_journey`;
- `micro_journey_template_ref = ugc_testimonial` until candidate promotion;
- rationale note: candidate pattern is `social_proof_receipt`;
- object of attention: waitlist demand plus template-pack release;
- proof artifacts: waitlist number, anonymized request snippets, launch comments;
- proof provenance: real, anonymized, approved, or dramatized;
- privacy/consent constraints;
- claim-safety constraints;
- product/context reveal;
- reason people care: creators requested this exact workflow;
- payoff: first version is now available;
- CTA or exit beat;
- text legibility and vertical safe-zone notes;
- provider notes: downstream only after storyboard approval.

## Draft Shot / Beat Outline

1. **Demand Signal**
   Open on a waitlist counter or launch dashboard detail. Keep the number readable and truthful.

2. **Proof Detail**
   Hold on two anonymized snippets: "Do you have the template?" and "Can you share the workflow?"

3. **Pattern**
   Quick stack of request cards shows this is repeated demand, not one isolated message.

4. **Release Reveal**
   Cut to the template pack cover, table of contents, or workflow board.

5. **Reason People Care**
   Show one concrete inside view: hook prompts, storyboard cards, or finished example frame.

6. **Payoff / Action**
   End on the release state: "Version 1 is live" or "The waitlist gets it first." Optional loop returns to the waitlist counter.

## Risks, Failure Modes, And Proof Safety

- The waitlist number is fabricated or inflated.
- The proof is too fast or too tiny to read.
- Private details are exposed in screenshots.
- The product reveal does not answer the request.
- The video uses social proof to imply unsupported popularity.
- The CTA feels manipulative because the evidence is vague.
- Dramatized receipts are styled as literal customer proof.

Proof safety rules:

- Use real proof only with permission or anonymization.
- Do not show identifiable private messages without explicit approval.
- Do not imply endorsements from people who only asked a question.
- Label or visually distinguish composites from literal receipts.
- Keep the claim scale aligned with the proof shown.

## Promotion Recommendation

Recommendation: **defer promotion, but keep candidate active**.

This second proof-artifact walkthrough strengthens the case that `social_proof_receipt` has distinct needs, especially provenance and privacy. It still remains close to `ugc_testimonial`, and the prior findings asked for at least two more cases before promotion.

One more case should test review/rating proof for an existing product. Promote only if that case shows the same recurring needs without relying on a named speaker or face-to-camera testimonial.

## What This Teaches The Framework

`social_proof_receipt` may deserve its own id, but the framework should be conservative because trust videos can easily become testimonial variants. The deciding distinction is whether the proof artifact itself carries credibility.

The reviewer check should ask: is the proof legitimate, readable, privacy-safe, proportionate to the claim, and directly connected to the product/context reveal?
