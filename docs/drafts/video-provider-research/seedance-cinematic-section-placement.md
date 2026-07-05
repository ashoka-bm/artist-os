# Seedance Cinematic Reference Section Placement

Status: draft working agreement.

Source: `/Users/ashokaji/Desktop/Video Ref/Dan Kieft Cinematic Seedance Updated.md`

Purpose: decide where each section of the reference belongs in the Artist OS video flow without letting provider-specific syntax contaminate provider-neutral story, Beat Plan, or Video Medium Plan records.

## Placement Principle

Use the earliest layer where the idea is useful, but no earlier than its authority allows:

- reusable directing judgment belongs in Storyboard Shot Design;
- reference-prep decisions belong in Reference Strategy and Reference Readiness;
- aspect ratio belongs in `video_format.aspect_ratio` early and must survive reference, storyboard, provider export, and render validation;
- provider formatting, tags, language, model duration, and prompt output shape belong after storyboard approval in Provider Export;
- generation or upload actions remain behind explicit Generation Approval;
- shot-list artifacts are planning aids, not replacements for Video Medium Plan.

## Section Placement Matrix

| Source section | Core value | Flow placement | Implementation home | Decision |
| --- | --- | --- | --- | --- |
| Output rules / output-only contract | Prevent accidental provider calls, mixed modes, incomplete prompt packets, and extra commentary. | After storyboard approval, when rendering a Seedance prompt packet. | `docs/drafts/video-provider-research/providers/seedance-cinematic-prompt-protocol.md`; future Provider Export renderer. | Provider-export only. Do not put provider prompt output shape in Video Medium Plan. |
| Prompt request intake: freeform scene vs finished shot list | A finished shot list should be batched and confirmed before prompt rendering. | Production Route / Provider Export intake after approved storyboard or selected shot list. | Seedance prompt protocol; future export-session checklist. | Keep as export-session behavior. If the user asks for prompts from a shot list, confirm shot range, reference tray, and dialogue/audio first. |
| Hard prompt rules | English prompt body, one block, flat shots, duration-derived shot count, 24fps, no per-shot durations, complete re-output on revision. | Provider Export renderer. | Seedance prompt protocol and `provider-exports/seedance-2-export.md`. | Provider-specific. Store as renderer rules, not schema fields. |
| Exact prompt shape / never-produce list | A strict final packet shape reduces operator error. | Provider Export renderer and review checklist. | Future Seedance export packet template. | Useful, but only after storyboard approval. |
| Reference tags | Tags are volatile session bindings; tag placement affects provider behavior. | Provider Media Bindings after references are accepted and uploaded/imported for a provider session. | `patterns/reference-scoping.md`; Seedance prompt protocol; future Provider Media Binding / export-session record. | Do not store `@image` or `@audio` tags in core records. Store provider-neutral reference roles upstream and map to tags at export. |
| Character sheet ref types | Different reference outputs serve different shot scales. | Reference Strategy before storyboard lock; Reference Readiness before storyboard export; Provider Export tag mapping after upload. | `docs/adr/0011-promoted-reference-inventory-and-storage.md`; `patterns/character-location-reference-sheets.md`; Reference Inventory; Visual Reference Sheet Plan. | Already matches accepted architecture. Use identity plate, full-body turnaround, and macro detail card as planned Reference Outputs when continuity matters. |
| Start-frame vs all-reference mode | Start-frame animation uses the uploaded image as the first frame rather than normal repeated reference tags. | Production Route / Provider Export after storyboard approval; may consume an approved storyboard still or reference output. | Seedance prompt protocol; future Production Route adapter. | Provider-export distinction. Upstream Video Medium Plan may say a start frame is required, but not how Seedance tags it. |
| Last-frame continuity chaining | Long or multi-part generations can preserve continuity by using the last frame of one clip as the start frame of the next. | Production Route segmentation after storyboard approval; Provider Export for each batch; Output Record links after generation. | Seedance prompt protocol; future Production Route adapter and Provider Media Bindings. | Keep the continuity requirement visible upstream, but create last-frame start bindings after clips exist. Generation and extracted frames need Output Records. |
| Camera language | Camera angle, shot scale, and movement should serve emotional job, not decoration. | Early: Shot Logic and Storyboard Shot Design. Later: provider export translation. | `direction-notes/cinematic-coverage-and-camera-direction.md`; `skills/artist-os/references/video-journey.md`; `docs/output-journeys/video.md`. | Reusable directing guidance belongs early in Video Medium Plan. Provider prompt text stays downstream. |
| Angle reference / shot size / camera movement menus | A practical vocabulary for deciding what each shot should do emotionally. | Early as Shot Design guidance; downstream as provider-specific wording. | Direction note for meaning; Seedance protocol for syntax. | Split the concept from the syntax. Meaning early, language late. |
| Directorial pushback | If a requested camera choice weakens the beat, flag it once and still honor the artist's final choice. | Shot Design interview and storyboard review; also provider export if a late prompt request conflicts with the beat. | Direction note; Video Critic Review checklist. | Keep as general Artist OS behavior for camera decisions. |
| Shot List / Scene Overview mode | A separate planning artifact with plain-language coverage, not a prompt packet. | Optional planning helper during Shot Logic or after a Video Medium Plan when the artist asks for a shot list. | Future shot-list artifact template; possibly `docs/drafts/video-template-research/walkthroughs/` for examples. | Do not let this replace Video Medium Plan. Use as an artist-readable projection of Storyboard Shots. |
| Locked HTML shot-list template | Useful presentation format for human review. | Optional review artifact after shots exist or during a bounded shot-planning request. | Future local HTML artifact template, not core schema. | Store as draft artifact pattern only. Do not force HTML into the canonical plan. |
| Director vocabulary for shot-list mode | Beginner-friendly shot planning vocabulary. | Shot Logic and artist-facing shot-list artifact. | Direction note or future shot-list artifact guide. | Use the vocabulary early, but keep provider language out. |
| Timing / clock | Prevents overpacked generated clips and improves shot feasibility. | Shot Logic, Motion / Pacing / Transition Gate, and Provider Export. | Video Journey guidance plus Seedance protocol. | General principle belongs early; exact Seedance duration bands stay downstream. |
| One camera move per shot | Improves storyboard clarity and provider feasibility. | Early in Storyboard Shot Design; enforced again in provider export. | Direction note; Video Critic Review; Seedance protocol. | General enough to use before provider export. |
| Head moves / repeated actions | Model-specific motion limitation. | Provider Export feasibility check; optional risk note in storyboard if the intended platform is known. | Seedance protocol and future provider adapter. | Mostly provider-specific. Do not make it a universal storyboard law. |
| Realism line | Concrete provider wording to avoid plastic skin/hair. | Provider Export. | Seedance protocol; future prompt renderer. | Provider-specific wording. Upstream may record realism style, but not fixed Chinese text. |
| Continuity wording | Some continuity rules are universal; exact clauses are provider-specific. | Universal continuity in Video Medium Plan and Reference Inventory; provider-specific phrasing in export. | Video Journey continuity scan; Seedance protocol. | Split: continuity requirement early, phrasing late. |
| Voice / audio with `@audio` | Audio tags need inline binding and should not duplicate carried dialogue. | Provider Media Binding and Provider Export after audio refs exist. | Seedance protocol; future Provider Media Binding / export-session record. | Provider-specific. Upstream Video Audio Posture and text/audio refs say what audio does; export maps it. |
| Sound | Music, ambience, and sound effects must be intentional. | Video Audio Posture early; provider sound wording in export. | Video Journey; Seedance protocol. | Keep the decision early, keep exact wording downstream. |
| Moderation flags | Warns about provider rejection risks. | Provider Export preflight; possibly Production Route risk notes. | Seedance protocol; future provider preflight checklist. | Provider-specific safety/feasibility layer after storyboard approval. |
| Directing tips | Economy first, vary scale and angle, establish-build-payoff, one flowing motion, tension through withholding/reveal/sound. | Early in Shot Logic and Storyboard Shot Design. | `direction-notes/cinematic-coverage-and-camera-direction.md`; Video Journey; Video Critic Review. | Reusable directing guidance belongs early. Already promoted to storyboard planning. |
| Character / asset sheets with GPT Image 2 | Recurring subjects need reference outputs before scene work when drift would matter. | Reference Strategy before storyboard lock; Visual Reference Sheet Plan drafting; Generation Approval before provider calls; Reference Readiness before storyboard export. | Reference Inventory; Visual Reference Sheet Plan; ADR-0011. | Keep provider-neutral reference planning early. GPT Image 2-specific generation settings stay provider/export-side. |
| GPT Image 2 as first implemented image generator | Most current reference/still generation should route through GPT Image 2 because it is the first properly implemented image generator in Artist OS. | Generation Approval request for reference outputs, storyboard stills, start frames, identity plates, turnarounds, macro detail cards, and calibration stills. | Image generation adapter / Generation Approval packet; Visual Reference Sheet Plan; storyboard prompt package. | Treat GPT Image 2 as the default implemented image generation route unless the artist chooses another route or a future adapter is promoted. Do not hardcode GPT Image 2 syntax into provider-neutral records. |
| Turnaround sheet prompt | Creates continuity reference for body/object shape. | Visual Reference Sheet Plan drafting. | Visual Reference Sheet Plan; future provider-specific prompt template. | Plan the need upstream; provider prompt text remains draft template. |
| Identity ref | Strong anchor for face/object identity. | Visual Reference Sheet Plan and Reference Inventory. | ADR-0011 and Reference Inventory. | Already accepted as one of the promoted character Reference Outputs. |
| Aspect ratio and resolution | Aspect ratio is an early format commitment; exact resolution is usually a provider/model output setting. | Video Medium Plan `video_format.aspect_ratio`; storyboard prompt package; Visual Reference Sheet Plan output requirements; Generation Approval request; render validation. | `schemas/video-medium-plan.schema.json`; `storyboard-prompt-builder.md`; `patterns/render-validation-and-delivery-promise.md`; future provider request packet. | Aspect ratio must be checked early and carried through. Resolution stays provider/request specific unless the output format requires it. |
| Close-up detail sheet | Texture and feature continuity. | Visual Reference Sheet Plan and Reference Inventory. | ADR-0011 and Reference Inventory. | Already accepted as one of the promoted character Reference Outputs; can also apply to objects/products when texture matters. |
| Image prompts for start frames | Draft start-frame stills that later drive video motion. | Storyboard prompt package / Visual Reference Sheet Plan / optional generated storyboard stills, depending on role. | `storyboard-prompt-builder.md`; Video Medium Plan storyboard generation policy; Provider Export. | Need role routing: reference sheet, storyboard still, or provider start frame. Generation requires explicit approval. |
| Quick checklist | Operator preflight before sending a prompt. | Provider Export preflight. | Seedance prompt protocol; future export packet checklist. | Useful but downstream only. |

## Proposed Flow

1. **Beat Plan:** defines the emotional movement. No provider syntax.
2. **Video Medium Plan:** selects Narrative Depth, format, Video Style Expression, Reference Strategy, Video Scenes, and Storyboard Shots.
3. **Format and aspect ratio check:** records `video_format.aspect_ratio` and makes sure reference outputs, storyboard sheets, start frames, provider exports, and final renders can preserve it.
4. **Shot Logic / Shot Design:** uses the reusable camera and directing guidance: emotional job, coverage economy, shot scale, camera angle, camera movement, subject movement, one movement per shot, tension through withholding or reveal.
5. **Reference Strategy / Reference Readiness:** decides which characters, locations, products, props, or stateful visual facts need planned Reference Outputs before storyboard export. GPT Image 2 is the default implemented image generation route for approved reference outputs and storyboard stills unless another route is explicitly selected.
6. **Storyboard-ready package:** locks shots, timing, transitions, audio posture, storyboard frame prompts, aspect ratio, shot scale, camera angle, camera movement, subject movement, blocking, and continuity requirements.
7. **Production Route:** chooses Seedance, Higgsfield, OpenMontage, Remotion, HyperFrames, FFmpeg, or another route based on the approved storyboard.
8. **Provider Media Bindings:** maps accepted Reference Outputs, audio refs, start frames, last-frame continuity frames, and storyboard stills to provider session roles or tags.
9. **Provider Export:** applies Seedance-specific rules: English prompt shape, duration brackets, tag placement, 24fps, audio tag binding, moderation preflight, and complete prompt packet.
10. **Generation Approval:** required before any provider call, upload, render, extracted frame, or generated media.

## Grilling Questions

These are the decisions still worth confirming before promotion:

1. Should the artist-facing shot-list HTML artifact become a reusable optional output of Video Medium Plan, or stay as a provider-research helper?
   - Recommended answer: keep it optional and draft-only until at least two non-Seedance walkthroughs need the same artifact.
2. Should Provider Media Bindings become a schema-backed record now?
   - Recommended answer: not yet. Capture the concept in draft provider research until the first real provider adapter needs durable session ids.
3. Should directorial pushback become a general Artist OS instruction beyond video?
   - Recommended answer: keep it in video Shot Design for now; revisit if image composition or illustration planning needs the same behavior.
4. Should Seedance duration bands influence storyboard shot counts early?
   - Recommended answer: only as a non-binding provider preference. Storyboard shot count should serve the beat first; Seedance batching can split or merge after storyboard approval.
5. Should GPT Image 2-specific reference prompt text be copied into core Visual Reference Sheet Plan docs?
   - Recommended answer: no. Promote the reference-output roles, not the provider prompt wording.
6. Should GPT Image 2 be treated as the default implemented image-generation route for reference outputs and storyboard stills?
   - Recommended answer: yes, for now. Keep the domain records provider-neutral, but route approved generation packets to GPT Image 2 unless the artist selects another implemented route.
7. Should last-frame continuity become an upstream storyboard requirement or a downstream production binding?
   - Recommended answer: split it. Storyboard records the continuity need; Production Route and Provider Media Bindings decide when a generated clip's last frame becomes the next clip's start frame.
