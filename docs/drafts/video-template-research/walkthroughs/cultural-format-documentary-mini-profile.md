# Cultural Format Walkthrough: Documentary Mini-Profile

Status: research draft.

## Sample Request

Create a 60-90 second mini-profile of a creator who uses AI video tools. The surface topic is the workflow, but the real value is the creator's taste, judgment, emotional direction, and ability to decide what a generated shot should mean.

The piece should feel observed, human, and specific. It should not become a software demo, product ad, or generic creator montage.

## Routing Decision

Route this as a Cultural Format Structure test because the current video format library has adjacent entries but no direct documentary mini-profile entry.

Closest existing fits:

- `youtube_explainer_deep_dive`: useful for context and synthesis, but too explanation-led.
- `creator_showcase_moment`: useful for a compact proof of taste or skill, but too small for a profile shape.
- `montage_mood_film`: useful for atmosphere and observed work, but not enough context or kicker.
- `influencer_ugc_testimonial`: useful for creator presence, but too proof/ad oriented.

The missing shape is a profile grammar: person, observed work, context, tension, proof, return, and kicker.

## Recommended Narrative Depth And Alternatives

Recommended: `micro_journey`.

Why: the piece needs audience movement from "this person uses AI tools" to "this person's real value is creative judgment." It has a hook and payoff, but it does not need a full Story Structure unless the sample expands into a bigger life or career arc.

Alternatives:

- `full_story`: use when the profile includes a decisive before/after life change, public conflict, career risk, or major transformation.
- `utility_sequence`: use when the piece is only a profile asset package or background B-roll set without a human turn.

For the sample request, `micro_journey` is the best fit.

## Story Template Fit

Primary fit: Observation Reframe Move.

Structure:

1. Signal: the creator works with AI video tools.
2. Common read: most people think the tools are the value.
3. Reframe: the tools only matter when directed by taste, judgment, and feeling.
4. Implication: the creator's real work is choosing what should survive and what should be cut.
5. Move: watch the person make decisions, not just operate software.
6. Payoff: the viewer leaves with sharper respect for human direction.

Secondary fit: Human Kebab.

Use Human Kebab when the profile opens on a lived scene, widens into context, then returns to the person with a larger meaning.

## Proposed Cultural Format Structure: `documentary_mini_profile`

Audience expectation: meet a person through observed behavior, specific context, and a small but meaningful turn.

Typical parts:

1. Human entry: a concrete person in a concrete place.
2. Observed work: what they are doing before they explain it.
3. Context / nut graf: why this person or moment matters.
4. Tension: the incomplete or mistaken read.
5. Proof: action, decision, artifact, or response that proves the real value.
6. Return: come back to the opening person with new meaning.
7. Kicker: a final image, line, or gesture that lands the profile's point.

Timing/rhythm:

- 0-5 seconds: human entry or charged detail.
- 5-20 seconds: observed work and viewer orientation.
- 20-45 seconds: context, tension, and stakes.
- 45-75 seconds: proof through decision or artifact.
- 75-90 seconds: return and kicker.

Visual grammar:

- close human details;
- workspace or environment;
- hands, screen, notes, prompts, rejected frames, selected frames;
- reaction and pause, not only output;
- one return image that means more the second time.

Audio/text grammar:

- voiceover or interview line can carry context;
- dialogue should be referenced, not drafted inside the Video Medium Plan;
- on-screen text should be sparse: name, role, short claim, or one key phrase;
- music should support observation, not inflate stakes.

Compatible `narrative_depth` values:

- primary: `micro_journey`;
- secondary: `full_story`;
- limited: `utility_sequence`.

## Required Video Medium Plan Payload

The Video Medium Plan should carry:

- `narrative_depth`: `micro_journey`;
- `micro_journey_template_ref`: nearest schema-supported id, likely `creator_showcase_moment`, with `documentary_mini_profile` recorded as Cultural Format Structure rationale;
- `story_template_ref`: null unless promoted to `full_story`;
- `asset_purpose_brief`: null unless routed as `utility_sequence`;
- accepted output shape: documentary mini-profile;
- human subject and role;
- profile promise;
- observed-work scenes;
- context / nut graf moment;
- tension or common misread;
- proof object, decision, or artifact;
- return/kicker image;
- audio posture: voiceover-led, interview-led, or mixed;
- text refs for name/title, on-screen phrase, captions, or interview excerpts;
- reference needs for person, workspace, recurring tools, generated stills, and screen state;
- provider preference notes only as downstream export notes after storyboard approval.

## Draft Shot / Beat Outline

1. **Human entry:** Close shot of the creator pausing over a still frame, hand hovering before selecting or rejecting it. The audience sees decision before tool.
2. **Observed work:** Medium shot of the workspace: screen, notes, visual references, and a rough storyboard grid. No tool explanation yet.
3. **Context / nut graf:** Voiceover or interview ref: "Everyone sees the AI output. The harder part is deciding what the output is supposed to feel like."
4. **Common misread:** Cut to quick fragments of polished generated clips or prompt windows. The obvious read is speed, automation, and novelty.
5. **Tension:** The creator rejects a technically impressive shot because it misses the emotional direction. Hold on the rejected frame long enough to understand why it is tempting.
6. **Proof of judgment:** The creator compares two options and chooses the quieter frame because it preserves the intended feeling. Show notes, gesture, or spoken rationale.
7. **Observed consequence:** The selected frame enters a storyboard or edit timeline. The work becomes more coherent, not just prettier.
8. **Return:** Return to the opening close shot, now with the chosen frame visible in context. The same pause reads as authorship, not hesitation.
9. **Kicker:** Final line or image: the creator steps back from the screen; the frame holds on the human decision, not the software interface.

## Risks And Common Failure Modes

- The profile becomes a tool demo instead of a human profile.
- The subject only explains their value rather than demonstrating it.
- The video overuses screen captures and loses human presence.
- The "AI is fast" angle overwhelms the taste/judgment angle.
- The profile has atmosphere but no nut graf.
- The ending stops instead of returning with a new meaning.
- On-screen text becomes a mini-essay.
- Provider notes creep into core story or shot planning.

## Promotion Recommendation

Promote after one more profile test.

Recommendation: **defer, then promote**.

Reason: `documentary_mini_profile` fills a real gap between `creator_showcase_moment`, `youtube_explainer_deep_dive`, and `montage_mood_film`. It should probably become a Cultural Format Structure, not a Story Template and not a Micro-Journey Template.

Promotion requirements:

- Test one non-AI creator profile, such as a musician, chef, designer, or craftsperson.
- Confirm the seven-part shape works without forcing full story structure.
- Add confusion guidance against `creator_showcase_moment`, `youtube_explainer_deep_dive`, and `influencer_ugc_testimonial`.

## What This Teaches The Framework

The current framework can route documentary profile work, but it lacks a named format for it. Without that format, agents may misclassify profiles as explainers, creator showcases, or mood montages.

The missing decision is not narrative depth. The missing decision is audience-facing format grammar.

`documentary_mini_profile` should teach the Video Journey to preserve three things at once:

- human specificity;
- contextual meaning;
- a return/kicker that changes how the viewer reads the opening person or scene.

This strengthens the Cultural Format Structure layer without contaminating Story Templates or provider export notes.
