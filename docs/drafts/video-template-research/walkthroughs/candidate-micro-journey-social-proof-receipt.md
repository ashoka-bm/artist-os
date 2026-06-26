# Candidate Micro-Journey Walkthrough: Social Proof Receipt

Status: research draft.

## Sample Request

Create a 20-second vertical short for a creator workflow product. The video should open with a fast cascade of real-looking comments, DMs, and review snippets from creators asking, "How did you make that AI video workflow?" It then reveals the workflow toolkit or tutorial that answers the demand.

The final beat should make the viewer feel that the product exists because there is visible demand, not because the creator is forcing a pitch.

## Routing Decision

- `narrative_depth`: `micro_journey` candidate.
- Candidate template: `social_proof_receipt`.
- Current schema-supported fallback: `ugc_testimonial`.
- Cultural Format Structure: `short_social_hook_loop`, with optional `product_explainer_demo` influence if the reveal includes a quick product/context shot.

The route should not write `social_proof_receipt` into `micro_journey_template_ref` yet because the current schema enum does not support that id. Use `ugc_testimonial` as the schema-valid fallback and record `social_proof_receipt` in rationale or traceability notes.

## Why This Is Not `full_story`

This video does not need a complete story movement with pressure, turn, consequence, and character-level payoff. It has a compact attention movement:

1. public demand exists;
2. the viewer sees proof of that demand;
3. the product/tutorial appears as the answer;
4. the viewer understands why it matters.

There is no need for Story Structure in the Beat Plan unless the video becomes a broader creator-origin story.

## Why This Is Not `utility_sequence`

This is not merely an asset package or functional proof insert. The public proof changes the viewer's stance from "why should I care?" to "people like me already want this." That makes it a micro-journey, not a utility sequence.

A utility version would only be a reusable review/comment montage asset. This request needs audience movement: curiosity -> credibility -> answer -> action.

## Candidate Micro-Journey Fit

`social_proof_receipt` fits when the proof artifact carries the trust:

- comments asking for the workflow;
- review snippets praising the result;
- creator messages requesting the template;
- waitlist or demand signals;
- visible public response to prior work.

The viewer movement is:

```text
public signal -> proof detail -> product/context -> reason people care -> payoff
```

This differs from `ugc_testimonial`, where one person or speaker carries the trust through lived experience.

## Nearest Current Schema-Supported Id

Use `ugc_testimonial` as the nearest schema-supported id.

Why it is sufficient:

- both templates build trust through evidence from other people;
- both need claim/proof safety;
- both can use captions, faces, comments, and review artifacts.

Why it is insufficient:

- `ugc_testimonial` implies a person, speaker, or user experience carries the claim;
- `social_proof_receipt` centers the proof artifact itself;
- review/comment/waitlist evidence needs different legibility, privacy, and provenance checks than a face-to-camera testimonial.

Recommendation: keep using `ugc_testimonial` as the schema fallback until at least two more walkthroughs prove that proof-artifact-led videos behave differently enough to deserve their own enum value.

## Cultural Format Structure Fit

Primary fit: `short_social_hook_loop`.

Audience expectations:

- the first frame should be readable immediately;
- proof should appear within the first 1-3 seconds;
- the product/context reveal should arrive quickly;
- the close should either loop back to demand or give a clear next action.

Secondary influence: `product_explainer_demo` if the video includes one concise workflow shot after the proof cascade.

Do not use `influencer_ugc_testimonial` unless a person speaks directly about their experience.

## Required Video Medium Plan Payload

The Video Medium Plan should carry:

- `narrative_depth = "micro_journey"`;
- `micro_journey_template_ref = "ugc_testimonial"` until schema promotion;
- rationale note: candidate pattern `social_proof_receipt`;
- object of attention: public demand signal plus workflow/tutorial answer;
- viewer reason to care: other creators already asked for this;
- proof artifacts: comments, DMs, reviews, waitlist, or request screenshots;
- proof provenance and privacy notes;
- text legibility constraints;
- safe-zone constraints for vertical video;
- product/context reveal;
- payoff definition;
- CTA or exit beat;
- downstream provider notes only after storyboard approval.

## Draft Shot / Beat Outline

1. **Public signal hook, 0-2s**
   Fast close-up cascade of comments or messages: "workflow?", "tutorial?", "how did you do this?", "template please." The viewer sees demand before the product appears.

2. **Proof artifact hold, 2-5s**
   One or two receipts pause long enough to read. Sensitive names, avatars, and private details are blurred or replaced with approved mockups.

3. **Demand pattern, 5-8s**
   More receipts group into a pattern: creators want the same workflow, not a random one-off answer.

4. **Product/context reveal, 8-12s**
   The workflow toolkit, tutorial board, or final still appears. The video makes clear what answers the demand.

5. **Reason people care, 12-16s**
   A quick visual shows the practical result: still frame first, approve, animate, finished B-roll, or another concise workflow outcome.

6. **Payoff / next action, 16-20s**
   End on the product/tutorial lockup with a simple action: "The workflow is ready," "Start with the still," or "Use the toolkit." Optional loop returns to the first comment cascade.

## Risks, Failure Modes, And Proof Safety

Common failure modes:

- fake-looking receipts weaken trust;
- proof appears too fast to read;
- private messages expose names, avatars, handles, or sensitive context;
- the product reveal arrives too late;
- the video shows demand but never explains the answer;
- the proof artifact overwhelms Artist Meaning and becomes pure social validation;
- the CTA feels disconnected from the proof.

Proof and claim safety notes:

- Use real receipts only with permission or with identifying details removed.
- Do not imply endorsements from people who did not endorse the product.
- Do not fabricate numbers, reviews, ratings, or waitlists.
- If receipts are dramatized, label or style them so they do not imply literal customer proof.
- Avoid unsupported claims such as "everyone asked for this" unless the proof supports that scale.
- Carry disclosure notes if any shown proof comes from paid creators, collaborators, or solicited testimonials.

## Promotion Recommendation

Recommendation: **defer promotion**.

`social_proof_receipt` is distinct enough to keep as a research candidate, but one walkthrough is not enough to promote it into `micro_journey_template_ref`. It should be tested against at least two more cases:

- review/rating proof for a product;
- waitlist or demand proof for a launch;
- comment/request proof for a tutorial or creator workflow.

Promote if those tests show the same recurring needs:

- proof artifact as the trust carrier;
- provenance/privacy handling;
- legibility and safe-zone rules;
- product/context reveal after public signal;
- payoff based on "this exists because people asked."

Merge into `ugc_testimonial` if most cases still depend on a speaker or named user experience.

## What This Teaches The Framework

This walkthrough shows that some micro-journeys build trust without a speaker. The proof artifact can be the protagonist of the short.

The framework needs a place to preserve:

- proof artifact type;
- provenance confidence;
- privacy/consent handling;
- legibility requirements;
- relation between public signal and product reveal.

For now, those details can live in Video Medium Plan rationale, traceability notes, and shot requirements while `micro_journey_template_ref` remains schema-valid as `ugc_testimonial`.
