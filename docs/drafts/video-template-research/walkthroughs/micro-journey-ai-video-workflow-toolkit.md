# Micro-Journey Walkthrough: AI Video Workflow Toolkit

Status: research draft.

Purpose: test `narrative_depth = micro_journey` with the draft Micro-Journey Template Chooser before promotion into canonical docs or schemas.

## Test Case

A creator reveals a compact AI video workflow toolkit they use to turn an approved still frame into animated B-roll.

Provider-specific platforms such as Seedance, Higgsfield, Runway, Sora, Veo, or Remotion remain downstream production notes only. This packet stops at provider-neutral storyboard planning.

## Selected Template

Selected micro-journey template id: `product_reveal`

Rationale: the main object of attention is not a hidden package but a useful creator toolkit. The viewer journey is attention -> value signal -> detail proof -> payoff.

Near-fit template: `unboxing_reveal`, if the creator frames the toolkit as a hidden stack, folder, prompt pack, or behind-the-scenes reveal.

## Routing

Narrative Depth: `micro_journey`

Format Intent: short social creator video

Accepted output shape: `short_social_video`

Format modifiers: `explainer_clip`, `performance_clip`

Publication/use: social post or review packet

Duration target: 20-35 seconds for the draft walkthrough. If a provider later imposes shorter clip limits, split into approved storyboard segments during provider export rather than changing the core plan.

## Audience Movement

Viewer starting state: curiosity or skepticism about how creators turn one still into usable animated B-roll.

Viewer movement: attention signal -> toolkit reveal -> workflow proof -> finished B-roll payoff -> memory beat.

Intended Feeling: practical possibility. The viewer should feel that turning a still into B-roll is concrete, inspectable, and repeatable rather than vague AI magic.

## Micro-Journey Decisions

Hook posture: visible transformation promise.

Object of attention: compact AI video workflow toolkit for turning approved stills into animated B-roll.

Viewer reason to care: creators need repeatable B-roll without restarting from scratch or losing visual consistency.

Primary value signal: one approved still can become multiple useful motion assets when the workflow is structured.

Proof / reveal / sensory payoff: show the still, the toolkit steps, and the resulting animated B-roll package as a clear before-to-output chain.

Ending beat: finished B-roll grid or quick sequence lockup with the idea: still first, approve, animate, package.

## Expected Parts

1. Attention signal: show the approved still next to an empty B-roll timeline or placeholder grid.
2. Toolkit reveal: reveal the workflow components as a compact set: still frame, prompt choices, final-frame continuity, animation pass, finished B-roll.
3. Detail proof: show one concrete example of the still becoming a short animated shot while preserving the visual subject.
4. Value proof: show multiple B-roll outputs or use contexts: intro plate, process insert, detail motion, transition plate.
5. Payoff lockup: show the finished B-roll package in a clean grid or timeline.

## Storyboard Scope

Recommended shot count: 5 storyboard shots.

Shot 1: Hook image. Approved still on the left, blank B-roll slots on the right. Purpose: make the gap visible.

Shot 2: Toolkit reveal. Hands, cursor, or clean motion graphic reveals the workflow components. Purpose: convert vague AI process into a compact system.

Shot 3: First proof. The still becomes one animated B-roll shot. Purpose: prove the core transformation.

Shot 4: Package proof. Several B-roll uses appear as a grid or timeline strip. Purpose: show this is not a one-off clip.

Shot 5: Ending beat. Final still-first workflow lockup. Purpose: leave the viewer with the mental link: approved still -> structured workflow -> finished B-roll.

## Audio And Text Posture

Audio posture: voiceover-led or mixed.

Voiceover role: explain the workflow in short claims tied to the visuals. The Video Medium Plan should store timing and refs only; exact wording belongs in a Text Generation Plan if drafted.

On-screen text role: short labels for workflow components and final lockup. Avoid dense subtitles in provider exports unless the target platform requires them.

Music/sound posture: optional restrained motion-design sound. Do not require music.

## Reference Needs

Required references:

- approved still frame that anchors the workflow,
- visual style reference for the B-roll package,
- subject/product/object reference if the still contains a recurring object or person,
- final-frame or continuity reference if provider export later splits the animation into segments.

Optional references:

- creator workspace or screen context,
- sample timeline / grid layout,
- brand typography or color system for motion graphics.

Reference risk: if the approved still is not treated as the anchor, the sequence may drift into generic AI-tool visuals and lose the product proof.

## Provider Preference Notes

Provider preferences are non-binding until after storyboard approval.

Possible downstream notes:

- Seedance 2 or similar short-form video generators may need segment splitting.
- Mention frame rate, camera, lighting, no subtitles/music, last-frame continuity, or language experiments only in provider export.
- Keep core storyboard prompts provider-neutral.
- If a provider has a short duration cap, preserve the approved five-shot logic by exporting as multiple short segments rather than compressing the micro-journey into an unclear single clip.

## Video Medium Plan Carry-Forward

The Video Medium Plan should carry:

- selected micro-journey template id: `product_reveal`,
- Narrative Depth: `micro_journey`,
- Format Intent: short social creator video,
- accepted output shape: `short_social_video`,
- hook posture: visible transformation promise,
- object of attention: AI video workflow toolkit,
- viewer reason to care: repeatable B-roll from an approved still,
- proof/reveal/sensory payoff: before-to-output chain from still to animated B-roll package,
- ending beat: final workflow lockup,
- storyboard scope: five shots,
- audio/text posture: voiceover-led or mixed with short labels,
- reference needs: approved still, style reference, continuity references as needed,
- provider preferences as downstream notes only.

## Risks And Gaps

- `micro_journey` is still skill guidance, not a schema field, so the selected template id must live in rationale, notes, or traceability for now.
- The current Video Medium Plan schema still requires Beat and Key Emotional Movement refs for Storyboard Shots. This is workable if the micro-journey has compact beats, but it may overburden simple creator videos.
- Exact voiceover or on-screen text wording belongs in Text Journey. The Video Medium Plan must not absorb script drafting.
- The chooser does not yet define how to choose between `product_reveal` and `creator_showcase_moment` when the creator's personality matters as much as the toolkit.
- Provider-specific duration limits should not reshape the core micro-journey before storyboard approval.

## Recommendations Before Promotion

1. Keep the Micro-Journey Template Chooser in draft until at least two more walkthroughs test different templates.
2. Add a small chooser note for overlap cases, especially `product_reveal` vs `creator_showcase_moment` and `product_reveal` vs `unboxing_reveal`.
3. Consider a future `micro_journey_template_ref` field only if repeated walkthroughs need querying, validation, or review against the selected template.
4. Add a Video Critic Review check later: for `micro_journey`, verify object of attention, viewer reason to care, proof/reveal/payoff, and ending beat.
5. Test a more human-led example next, such as `ugc_testimonial` or `creator_showcase_moment`, because this walkthrough is workflow/product-led.
