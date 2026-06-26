# Draft Micro-Journey Template Chooser

Status: research draft.

Use this chooser when `narrative_depth = micro_journey`: the video needs a hook and payoff, but not a full Story Structure. These templates are provider-neutral. Seedance, Higgsfield, or other platform rules belong in downstream provider export notes after the storyboard is approved.

Micro-journeys should still create audience movement. Each one needs:

- hook,
- object of attention,
- viewer reason to care,
- proof, reveal, demonstration, or sensory payoff,
- ending beat.

## Selection Rule

Choose the template by the viewer's journey, not by the platform or shot sequence.

| Template | Use when | Viewer movement |
| --- | --- | --- |
| `unboxing_reveal` | The object starts hidden or packaged. | Curiosity -> reveal -> proof -> desire or trust. |
| `product_reveal` | The product is introduced as the main object of attention. | Attention -> value signal -> detail proof -> payoff. |
| `ugc_testimonial` | A person validates a product, service, place, tool, or experience. | Skepticism or curiosity -> personal proof -> trust. |
| `fashion_fit_check` | Outfit, styling, transformation, or identity signal is the point. | First impression -> detail/fit proof -> confidence or vibe. |
| `quick_before_after_demo` | A visible change needs fast proof. | Problem state -> action -> changed state -> credibility. |
| `problem_solution_demo` | A relatable problem should resolve through a product, service, tool, or method. | Friction -> solution enters -> visible relief or outcome. |
| `how_to_tip_demo` | The viewer should learn one repeatable action quickly. | Common mistake or promise -> compact steps -> visible result -> repeat/use cue. |
| `creator_showcase_moment` | A creator wants to display taste, skill, process, personality, or result. | Hook -> distinctive behavior -> proof of taste/skill -> memorable signal. |
| `day_in_the_life_signal` | A lifestyle, work rhythm, identity, or routine should feel desirable or revealing. | Ordinary entry -> selected moments -> pattern or identity payoff. |

## Research Candidate Templates

These appeared repeatedly in the research threads, but they are not yet valid `micro_journey_template_ref` schema values. Use the nearest schema-supported id and record the candidate pattern in rationale or traceability notes until a promotion decision expands the enum.

| Candidate | Use when | Viewer movement | Nearest schema-supported id |
| --- | --- | --- | --- |
| `social_proof_receipt` | Reviews, comments, ratings, waitlists, or demand signals prove credibility. | Public signal -> proof detail -> reason people care. | `ugc_testimonial` |
| `order_pack_ritual` | Packing, assembly, fulfillment, gifting, or small-business ritual is the appeal. | Order cue -> careful assembly -> finished package payoff. | `unboxing_reveal` or `day_in_the_life_signal` |

## Overlap Notes

When two templates seem plausible, choose the one that owns the viewer's main reason to care:

- `product_reveal` vs `unboxing_reveal`: choose `product_reveal` when the value signal and use case matter more than concealment. Choose `unboxing_reveal` when curiosity, opening, hiddenness, or reveal order is the audience journey.
- `product_reveal` vs `creator_showcase_moment`: choose `product_reveal` when the product, feature, toolkit, or offer is the object of attention. Choose `creator_showcase_moment` when the creator's taste, behavior, authority, or process is what the viewer should remember.
- `creator_showcase_moment` vs `day_in_the_life_signal`: choose `creator_showcase_moment` when one compact proof of taste, skill, or point of view carries the payoff. Choose `day_in_the_life_signal` when selected routine moments create the identity or lifestyle signal.
- `quick_before_after_demo` vs `product_reveal`: choose `quick_before_after_demo` when the visible changed state is the proof. Choose `product_reveal` when the product's value is proven by feature, use context, or detail rather than transformation.
- `ugc_testimonial` vs `social_proof_receipt`: choose `ugc_testimonial` when a person carries the trust. Choose `social_proof_receipt` when the proof artifact itself carries the trust.
- `creator_showcase_moment` vs `how_to_tip_demo`: choose `creator_showcase_moment` when the creator's taste or skill is the memory. Choose `how_to_tip_demo` when the viewer should repeat the action.
- `quick_before_after_demo` vs `problem_solution_demo`: choose `quick_before_after_demo` when the changed state is the main proof. Choose `problem_solution_demo` when the viewer must first recognize a concrete friction and feel the solution's relief.

Do not choose a template because a provider, platform, or shot list resembles it. Provider handling stays downstream.

## `unboxing_reveal`

Use when: A product, object, or package begins concealed, wrapped, boxed, or withheld, and the video is built around opening, revealing, and proving why it matters.

Core movement: curiosity -> first reveal -> detail proof -> payoff -> exit beat.

Required decisions:

- What is hidden?
- Why should the viewer care before seeing it?
- What is the reveal order?
- What detail proves quality, usefulness, scale, texture, design, or desire?
- What final feeling should remain?
- What is the exit beat: pose, reaction, CTA, use, or next action?

Expected beats/parts:

1. Curiosity or reason to watch.
2. Opening gesture.
3. First product reveal.
4. Detail proof.
5. Payoff and exit beat.

Hook behavior: Tease the unseen object, unusual packaging, personal anticipation, problem solved, or "wait until you see this" detail.

Payoff behavior: Show the product clearly and connect it to feeling, use, identity, relief, beauty, or value.

Common failure modes:

- Opening the package before creating curiosity.
- Showing packaging but not product value.
- Too many details without one clear payoff.
- Ending without a final product pose, reaction, or use case.

What the Video Medium Plan must carry:

- product/object reference needs,
- reveal order,
- shot count and duration,
- key detail proof,
- close-up requirements,
- exit beat,
- provider preference notes only as downstream export notes.

## `product_reveal`

Use when: The video's main job is to introduce a product, collection item, feature, object, app screen, tool, or offer without an unboxing structure.

Core movement: attention signal -> product arrival -> value proof -> desire or action payoff.

Required decisions:

- What is the product or feature?
- What first visual makes it worth attention?
- What value claim or use case should be understood?
- What detail proves the claim?
- What should the viewer do or feel after the reveal?

Expected beats/parts:

1. Attention image or statement.
2. Clean product reveal.
3. Feature, texture, function, or context proof.
4. Comparison, use moment, or scale cue when useful.
5. Final product/value lockup.

Hook behavior: Lead with the most inspectable or surprising value signal, not generic product beauty.

Payoff behavior: Make the product's difference clear: what it changes, improves, expresses, unlocks, or makes easier.

Common failure modes:

- Treating the reveal as a beauty shot with no value proof.
- Showing too many features.
- Hiding the product behind style.
- Ending before the viewer understands why the product matters.

What the Video Medium Plan must carry:

- product subject,
- primary value signal,
- proof shot,
- use context,
- final lockup or CTA,
- reference/continuity needs for product accuracy.

## `ugc_testimonial`

Use when: The audience should trust a person, not just inspect an object. The video depends on lived proof, reaction, experience, recommendation, or before/after testimony.

Core movement: relatable starting point -> personal experience -> proof detail -> trust payoff.

Required decisions:

- Who is speaking or appearing?
- What skepticism, need, or desire does the viewer start with?
- What personal claim is being made?
- What concrete detail proves it?
- What trust payoff should land?

Expected beats/parts:

1. Relatable hook.
2. Speaker or user context.
3. Claim or experience.
4. Proof detail, result, or reaction.
5. Recommendation, changed state, or next step.

Hook behavior: Start from a specific lived problem, desire, doubt, surprise, or "I did not expect this" moment.

Payoff behavior: Convert the personal proof into trust, usefulness, reassurance, or desire.

Common failure modes:

- Generic praise with no concrete experience.
- Speaker feels scripted or over-polished.
- No visual proof supports the claim.
- Payoff becomes a sales pitch instead of earned trust.

What the Video Medium Plan must carry:

- speaker posture,
- claim,
- proof visual,
- shot scale for face/reaction,
- script or dialogue refs if words matter,
- authenticity constraints.

## `fashion_fit_check`

Use when: The video is about outfit, styling, body movement, identity, fit, transformation, styling choice, or fashion mood.

Core movement: first impression -> fit/details -> movement or styling proof -> identity/vibe payoff.

Required decisions:

- What outfit, piece, or style choice is being checked?
- What first impression should land?
- Which details matter: silhouette, fabric, color, fit, accessories, contrast, movement?
- What movement proves the fit or vibe?
- What feeling or identity should the final beat express?

Expected beats/parts:

1. First look or style promise.
2. Full or medium fit read.
3. Detail cutaways.
4. Movement, pose, transition, or styling variation.
5. Final confidence/vibe beat.

Hook behavior: Lead with transformation, strong first look, contrast, styling question, or identity promise.

Payoff behavior: Make the viewer feel the fit: confidence, elegance, edge, comfort, status, play, or transformation.

Common failure modes:

- No clear full-fit read.
- Details shown without movement.
- Styling lacks point of view.
- Final pose does not resolve the promised vibe.

What the Video Medium Plan must carry:

- outfit/reference needs,
- shot scale plan,
- detail list,
- motion or pose behavior,
- style constraints,
- final identity/vibe payoff.

## `quick_before_after_demo`

Use when: The main value is visible change: setup to result, problem to fix, blank to finished, messy to clean, old to new, or dull to elevated.

Core movement: before state -> action/compression -> after state -> proof of change.

Required decisions:

- What is the before state?
- What action causes the change?
- What must be shown for the after state to be credible?
- How much process is needed?
- What final comparison or result proves the change?

Expected beats/parts:

1. Before state.
2. Action or compressed process.
3. Transition or reveal.
4. After state.
5. Proof, comparison, or reaction.

Hook behavior: Make the before state legible and worth changing. The viewer should understand the gap quickly.

Payoff behavior: Show the changed state with enough proof that the transformation feels real.

Common failure modes:

- Before state is unclear.
- Process overwhelms the result.
- After state is not visibly different enough.
- Missing comparison shot.

What the Video Medium Plan must carry:

- before/after states,
- transformation action,
- proof shot,
- transition behavior,
- duration split between setup/process/result,
- reference continuity needs for state change.

## `problem_solution_demo`

Use when: A product, service, tool, workflow, or method matters because it resolves a specific problem the viewer can quickly recognize.

Core movement: friction -> solution enters -> visible proof -> relief/payoff.

Required decisions:

- What exact problem opens the video?
- What makes the problem visible or felt in the first seconds?
- What solution action enters after the problem is clear?
- What proof shows the solution caused the relief?
- What final state should the viewer remember?

Expected beats/parts:

1. Problem image.
2. Problem detail or escalation.
3. Solution entry.
4. Proof step.
5. Relief/payoff.
6. Optional loop or next-action beat.

Hook behavior: Lead with the friction, not the product. The viewer should recognize the pain before the solution appears.

Payoff behavior: Show relief, control, time saved, mess reduced, uncertainty resolved, or another solved-state proof.

Common failure modes:

- Problem is too vague.
- The video becomes a generic product reveal.
- Proof is only cosmetic before/after polish.
- Solution appears to replace human judgment when the intended value is support.
- Payoff is a slogan without a solved state.

What the Video Medium Plan must carry:

- problem visual,
- solution entry,
- proof of causal relief,
- viewer reason to care,
- final solved state,
- reference needs for the problem and solution object.

## `how_to_tip_demo`

Use when: The viewer should learn one repeatable action quickly, especially in short educational, creator, craft, workflow, or practical-advice videos.

Core movement: common mistake or promised tip -> compact steps -> visible result -> repeat/use cue.

Required decisions:

- What is the one learning objective?
- What mistake, missed opportunity, or useful promise earns attention?
- What steps are essential and what must be omitted?
- What result proves the tip worked?
- What repeatable cue should the viewer remember?

Expected beats/parts:

1. Mistake, missed opportunity, or promise.
2. Tip named in one compact move.
3. Step 1.
4. Step 2 or compressed middle.
5. Result/proof.
6. Repeat, save, or use cue.

Hook behavior: Start from a correction, practical promise, or visible weak state the viewer wants to improve.

Payoff behavior: Make the result visible and give the viewer a memorable action cue.

Common failure modes:

- Too many teaching points.
- Steps become dense text instead of visible action.
- The video becomes creator showcase instead of viewer learning.
- Result is verbal but not visible.
- Provider or production instructions contaminate the educational structure too early.

What the Video Medium Plan must carry:

- learning objective,
- promised tip,
- compressed step list,
- visible result/proof,
- repeat/use cue,
- text/audio posture,
- reference needs for before/result clarity.

## `creator_showcase_moment`

Use when: A creator, artist, founder, educator, maker, performer, or personality needs a compact moment that shows taste, process, skill, perspective, or result.

Core movement: attention hook -> distinctive action or point of view -> proof of craft/taste -> memorable signal.

Required decisions:

- What is being showcased: skill, process, taste, personality, result, or idea?
- What makes the creator distinct?
- What visual proof can show that distinction?
- What audience belief should change?
- What final signal should be remembered?

Expected beats/parts:

1. Creator hook.
2. Distinctive behavior, process, phrase, or visual.
3. Proof of skill, taste, result, or perspective.
4. Reaction, reveal, or point-plus-paint support.
5. Final creator signal.

Hook behavior: Start with a strong claim, visual action, surprising process step, personal stakes, or distinctive opinion.

Payoff behavior: Leave the viewer with a simple mental link between the creator and their value.

Common failure modes:

- Showcase becomes a generic montage.
- Personality appears but proof is missing.
- Too many ideas compete.
- Ending does not make the creator's signal memorable.

What the Video Medium Plan must carry:

- creator identity signal,
- proof object/action/result,
- speaker posture when applicable,
- hook posture,
- visual motif or repeated signal,
- final memory beat.

## `day_in_the_life_signal`

Use when: The video uses selected routine moments to communicate lifestyle, work rhythm, identity, aspiration, access, discipline, intimacy, or contrast.

Core movement: ordinary entry -> selective moments -> pattern recognition -> identity or lifestyle payoff.

Required decisions:

- Whose day or routine is shown?
- What identity, lifestyle, work rhythm, or contrast should emerge?
- Which moments prove the pattern?
- What should be omitted to avoid bland chronology?
- What final beat reveals the meaning of the day?

Expected beats/parts:

1. Entry moment.
2. First signal of routine or world.
3. Selected proof moments.
4. Pattern, contrast, or small turn.
5. End-state signal.

Hook behavior: Open on a specific, charged detail: unusual routine, aspirational setting, tension, contrast, or private-feeling access.

Payoff behavior: Turn the day into a readable identity signal, not just a sequence of events.

Common failure modes:

- Chronology replaces point of view.
- Too many low-value routine shots.
- No pattern or contrast emerges.
- Ending feels like stopping, not resolving.

What the Video Medium Plan must carry:

- routine/world signal,
- selected moments,
- omission rule,
- pacing pattern,
- final identity or lifestyle payoff,
- continuity/reference needs for recurring location, outfit, or objects.

## Video Medium Plan Carry-Forward Checklist

For any selected Micro-Journey Template, the Video Medium Plan should carry:

- selected micro-journey template id,
- hook posture,
- object of attention,
- viewer reason to care,
- proof/reveal/demo/sensory payoff,
- ending beat,
- duration target,
- shot count,
- shot-scale needs,
- audio or text posture,
- reference needs,
- provider preferences as non-binding downstream notes.

## Open Questions

- Should `order_pack_ritual` belong in the core enum or an ecommerce/lifestyle extension?
- Does `social_proof_receipt` deserve schema promotion after one more review/rating proof walkthrough?
