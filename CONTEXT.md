# Artist Generation

Artist Generation is the repository for Artist OS. This context defines the domain language for the artist-facing operating system.

## Language

**Artist Generation**:
The repository and project that builds Artist OS.
_Avoid_: Artist OS when referring to the repo itself

**Artist OS**:
The agent operating system that helps artists ingest references, extract meaning, transform emotional structure, generate assets, critique outputs, and preserve provenance.
_Avoid_: Artist repository, plugin, skill collection

**Skill**:
One agent workflow inside Artist OS.
_Avoid_: Agent, plugin

**Plugin**:
The packaged distribution form for Artist OS skills and tooling.
_Avoid_: Repository, operating system

**Reference**:
Any user-provided material the artist wants Artist OS to interpret or transform, including text, image, audio, video, or mixed media.
_Avoid_: Source, input, asset

**Source Record**:
The structured metadata record for a Reference.
_Avoid_: Reference, asset record

**Artist Meaning**:
The artist's stated interpretation of what a Reference means and what must survive transformation.
_Avoid_: Meaning, intent, vibe

**Emotional Primacy**:
The rule that creating the intended feeling is the governing goal of an Artist OS transformation. Beat Plans, tension profiles, Symbology Direction, Style Direction, Medium Plans, Prompt Plans, Text Generation Plans, and reviews exist to support the intended feeling while preserving Artist Meaning.
_Avoid_: Treating beats, style, composition, or prompt detail as successful when they do not create the intended emotion

**Intended Feeling**:
The audience feeling the transformation is trying to create as the emotional expression of Artist Meaning. A Beat Plan serves Intended Feeling; it is not successful merely because it has interesting structure.
_Avoid_: Mood label, style mood, factual theme

**Minimum Tension Criteria**:
The project-local reviewer threshold that defines how much contrast or movement a work needs to create its Intended Feeling. Defaults can seed the criteria, but the approved criteria belong to the specific work and can be raised, lowered, or redirected when Artist Meaning requires it.
_Avoid_: Universal taste score, global quality number, tension for its own sake

**Active Absence**:
The use of absence, omission, silence, negative space, missing figures, withheld resolution, or unseen causes as an active carrier of tension and Intended Feeling. Active Absence is not empty content; it is a deliberate pressure source.
_Avoid_: Treating minimal content as automatically weak, filling every gap with explanation

**Artist Meaning Record**:
The first-class structured record created by the Meaning Interview before agent interpretation. It preserves Artist Meaning independently so later Transformation Briefs, Beat Plans, Medium Plans, Prompt Plans, Text Generation Plans, and reviews can trace back to the artist's own authority.
_Avoid_: Burying Artist Meaning only inside a Creative Brief or Transformation Brief

**Meaning Interview**:
The short artist-facing interview that captures Artist Meaning and transformation constraints before analysis and planning.
_Avoid_: Grill me, interrogation

**Decision Interview**:
A bounded, one-question-at-a-time clarification sequence inside the Meaning Interview and major gates. Each question includes the agent's recommended answer, then waits for the artist's response before proceeding. It flushes out meaning, emotional target, must-preserve constraints, avoid constraints, medium direction, and success criteria before analysis hardens.
_Avoid_: Silent agent defaults, long surveys, generic brainstorming

**Orientation**:
The lightweight first-load exchange that identifies what kind of output the artist wants to create from a Reference before formal routing and planning harden.
_Avoid_: Orientation Gate, approval checkpoint, full medium planning, silent routing default

**Audio**:
The artist-facing Orientation label for sound outputs such as songs, instrumental tracks, soundscapes, scores, spoken-word beds, ritual audio, sound design pieces, and sonic logos.
_Avoid_: Renaming Sound Journey, Sound Medium Plan, or Sound Prompt Plan

**Recommended Answer**:
The agent's concrete proposed answer to a Decision Interview question, based on the Reference, Artist Meaning so far, and product rules. The artist can accept, revise, or reject it.
_Avoid_: Neutral multiple-choice menus when the agent has enough context to recommend

**Creative Brief**:
The approved medium-specific creative handoff before prompt planning. It compiles the relevant Artist Meaning, Transformation Brief, Beat Plan, and Medium Plan after critic review and Brief Approval.
_Avoid_: Transformation Brief, Beat Plan, Medium Plan, Emotional Brief

**Creative Brief Document**:
The artist-readable Markdown version of a Creative Brief.
_Avoid_: Creative Brief Record

**Creative Brief Record**:
The structured JSON version of an approved Creative Brief for agent handoff, validation, and Prompt Plan creation.
_Avoid_: Creative Brief Document, Transformation Brief, Beat Plan, Medium Plan

**Text Creative Brief**:
The text-specific Creative Brief that compiles Artist Meaning, Transformation Brief, Beat Plan, and Text Medium Plan into an approved handoff for written output planning.
_Avoid_: Text Medium Plan, Text Generation Plan

**Text Creative Brief Record**:
The structured JSON version of an approved Text Creative Brief for agent handoff, validation, and Text Generation Plan creation.
_Avoid_: Text Creative Brief Document, Text Medium Plan, Text Generation Plan

**Video Medium Plan**:
The video-specific Medium Plan that translates an approved Beat Plan into sequences, Video Scenes, timed Storyboard Shots, visual style, shot list, motion, transitions, script or audio relationships, and storyboard planning; v0 stops at storyboard-ready planning rather than finished video generation.
_Avoid_: Storyboard pre-plan, finished video, provider-specific video job

**Video Creative Brief**:
The video-specific Creative Brief that compiles Artist Meaning, Transformation Brief, Beat Plan, and Video Medium Plan into an approved handoff for video storyboard or future video prompt planning.
_Avoid_: Video Medium Plan, screenplay, finished storyboard

**Video Creative Brief Record**:
The structured JSON version of an approved Video Creative Brief for agent handoff, validation, and future video prompt planning.
_Avoid_: Video Creative Brief Document, Video Medium Plan, Video Prompt Plan

**Video Sequence**:
A Video Medium Plan container that groups Video Scenes into a larger movement, act, trailer section, montage passage, episode part, or feature-scale story unit.
_Avoid_: Beat Plan, Long-Work Stewardship, flat shot list

**Video Scene**:
A Video Medium Plan container that groups one or more Storyboard Shots around a setting, situation, Beat group, or local dramatic purpose.
_Avoid_: Storyboard Shot, Beat, finished clip

**Video Style Expression**:
The video-specific expression of Style Direction across rendering mode, camera style, motion style, edit style, caption typography, color, and light.
_Avoid_: Replacing Style Direction, visual style pileup

**Video Audio Posture**:
The Video Medium Plan decision that states whether the video is silent, music-only, voiceover-led, dialogue-led, sound-design-led, mixed, or deferred.
_Avoid_: Assuming every video needs music or dialogue

**Brief Approval**:
The artist's approval of a Creative Brief Document before Artist OS generates the Creative Brief Record.
_Avoid_: Acceptance Review

**Rough Brief Approval**:
The artist's explicit instruction to proceed with an incomplete or uncertain Creative Brief Document.
_Avoid_: Brief Approval when confidence is high

**Interpretive Confidence**:
A handoff label that tells the review step how strongly an interpretation is supported before final prompt planning.
_Avoid_: Final ambiguity

**Open Question**:
An unresolved interpretive gap that must be resolved before the final Prompt Plan or Text Generation Plan.
_Avoid_: Final prompt ambiguity

**Art Critic Review**:
A reviewer stage that strengthens the Creative Brief by resolving weak interpretations, increasing Poetic Density, and turning low-confidence notes into decisive artistic direction.
_Avoid_: Critique Asset, Acceptance Review

**Video Critic Review**:
A reviewer stage that checks shot progression, pacing, motion logic, transition logic, visual continuity over time, and script or audio alignment against Artist Meaning, Beat Plan, and Video Medium Plan.
_Avoid_: Art Critic Review alone, Writing Critic Review alone, Output Critic Review

**Review Record**:
The universal machine-readable output of any bounded reviewer sub-agent. It records reviewer role, reviewed artifact, upstream context, matched material, drift, findings, recommended revision, and approval status.
_Avoid_: Reviewer-specific machine-readable schemas unless a real downstream need appears

**Critical Heuristics**:
Reusable art-critical rules that Art Critic Review uses to deepen a Creative Brief without inventing new Artist Meaning.
_Avoid_: Generic best practices, taste, model preference

**Formal Analysis**:
The observable properties of a Reference.
_Avoid_: Emotional analysis

**Visual Dynamics**:
The formal forces that make a visual work active, coherent, tense, immersive, unstable, or memorable.
_Avoid_: Technicality, visual style only

**Visual Unit**:
The shared visual-planning unit that translates one Beat, Key Emotional Movement, or Tension Point into composition, style, visual tension, and Shot Design before it becomes a still image or video shot.
_Avoid_: Treating still images and video shots as unrelated planning objects

**Image Role**:
The still-image realization of a Visual Unit inside a single image, compressed arc, image series, portfolio, or collection, naming the function of that image such as opening image, threshold image, rupture image, return image, or resolution image.
_Avoid_: Storyboard Shot, frame, generic image

**Storyboard Shot**:
The atomic time-based video realization of a Visual Unit that adds duration, motion, blocking, transition, and script or audio relationships.
_Avoid_: Image Role, finished video clip, generated video

**Shot Design**:
The Visual Unit decision that names shot scale, camera angle, visual emphasis, and composition strategy. Shot Design serves Intended Feeling and the governing Expectation Turn; it is not a default full-body depiction of the subject.
_Avoid_: Generic full-body framing, camera variety for its own sake

**Shot Scale**:
The planned distance of the frame from the subject, such as extreme close-up, close-up, medium close-up, medium shot, medium wide, wide, or extreme wide. Close shots concentrate emotional pressure or symbolic detail; medium shots balance body language, action, and context; wide shots carry place, isolation, consequence, and scale.
_Avoid_: Treating every character image as a full-body shot

**Camera Angle**:
The planned viewpoint relationship to the subject, such as eye-level, high angle, low angle, overhead, Dutch/canted, profile, over-the-shoulder, or point-of-view. Camera Angle should express power, vulnerability, instability, intimacy, observation, or subjectivity when those forces matter.
_Avoid_: Neutral eye-level framing by default when the Beat needs a stronger perspective

**Visual Emphasis**:
The thing a Shot Design makes dominant: face or reaction, hands or object, body action, relationship between figures, environment, absence or negative space, symbolic detail, or scale/consequence.
_Avoid_: Centering the whole subject when the Beat needs one pressure point

**Shot Progression**:
The intentional change of Shot Design across adjacent Visual Units in an image series or video storyboard. Adjacent units should vary shot scale, camera angle, visual emphasis, or composition strategy unless repetition is artist-approved and tied to Artist Meaning.
_Avoid_: A series where every frame has the same full-body composition

**Sonic Dynamics**:
The formal forces that make a sound work active, coherent, tense, immersive, unstable, or memorable.
_Avoid_: Emotional Structure, genre only

**Style Direction**:
The artistic language or rendering mode used to express a Creative Brief, such as photoreal, cinematic, painterly, manga, cartoon, sketch, pixel art, folk, or surreal.
_Avoid_: Emotional Structure, Visual Dynamics

**Primary Style**:
The main Style Direction that controls the generated work's artistic language.
_Avoid_: Equal-weight style pileup

**Style Modifier**:
A secondary style, finish, mood, production, or genre influence that modifies the Primary Style.
_Avoid_: Unbounded hybrid style list

**Primary Text Form**:
The dominant written container for a Text Journey, such as poem, prose scene, short story, article, monologue, script, lyrics, letter, essay, manifesto, treatment, rewrite, or adaptation.
_Avoid_: Equal-weight pileup of text forms

**Text Form Modifier**:
A secondary written form influence that shapes the Primary Text Form without replacing its governing structure.
_Avoid_: Treating hybrid text forms as structureless

**Text Generation Plan**:
The structured post-brief plan for drafting or generating a written output while preserving the approved Text Medium Plan, voice, structure, source-wording policy, and review criteria.
_Avoid_: Text Prompt Plan, provider-only prompt

**Text Draft Packet**:
An internal fresh-context sub-agent handoff assembled from approved Text Journey records, source constraints, and drafting instructions to produce or revise a written Output Artifact.
_Avoid_: Schema-backed record, durable project artifact

**Human Voice Pass**:
A bounded skill-backed rewrite pass applied to a drafted written Output Artifact to make it sound less AI-written while preserving Artist Meaning, Text Medium Plan, Text Creative Brief, Text Generation Plan, source-wording policy, and structure.
_Avoid_: Generic warmth, untraceable rewrite, changing meaning to sound natural

**Human Voice Pass Policy**:
The Text Generation Plan decision that sets whether the Human Voice Pass is required, recommended, optional, or skipped, at what degree, and which formal features it must protect.
_Avoid_: Running humanization blindly across every text form

**Clear Writing Pass**:
A bounded editorial pass that improves clarity, concision, paragraph force, and reader guidance when those qualities serve the approved text form.
_Avoid_: Applying plainness to every written output, replacing voice with generic brevity

**Clear Writing Pass Policy**:
The Text Generation Plan decision that sets whether the Clear Writing Pass is required, recommended, optional, or skipped, at what degree, and which formal features it must protect.
_Avoid_: Treating clarity and concision as universal goals

**Style Priority**:
The rule that Style Direction is subordinate to Artist Meaning, Emotional Structure, Beat Plan, and Visual Dynamics.
_Avoid_: Style overriding the Creative Brief

**Style/Visual Conflict**:
A visible conflict between chosen Style Direction and required Visual Dynamics or Target Visual Engine.
_Avoid_: Silent style override

**Style Conflict Field**:
A compact Creative Brief Record field that records a Style/Visual Conflict, proposed Style Adaptation, and whether artist approval is required.
_Avoid_: Losing conflict decisions in prose only

**Style Adaptation**:
An intentional adjustment of Style Direction so it preserves Visual Dynamics while possibly producing a new or more interesting style expression.
_Avoid_: Abandoning the style without review

**Style Progression**:
An intentional change in Style Direction across images in a Series Plan, such as realism shifting toward cartoon, fantasy, abstraction, or another visual language.
_Avoid_: Inconsistent series style by accident

**Emotional Movement**:
The ordered change in Intended Feeling across Beats, sections, images, or outputs. In a Series Plan, Emotional Movement is the primary optimization; visual variety, amplitude shifts, composition changes, and style progression serve the emotional movement.
_Avoid_: Visual variety without a changed emotional pressure

**Arc Scale**:
The rule that the same underlying Emotional Movement can be compressed or expanded depending on output length. A single image usually compresses one key movement such as a climax, threshold, or residue. An image series stages several key movements. A longer arc can let one emotion build across several Beats before a major change, while still requiring each Beat to create some meaningful change.
_Avoid_: Forcing every micro-beat in a long arc to change emotion immediately, or letting long arcs repeat without movement

**Key Emotional Movement**:
A major emotional shift point in an arc. Key Emotional Movements are the emotional movements that must survive compression or expansion: a single image may compress one key movement, an image series may stage several key movements, and a longer arc may organize many smaller Beats around several key movements.
_Avoid_: Treating every Beat as equally structurally important, mirroring every Beat into a Key Emotional Movement, losing the major emotional shifts when compressing or expanding the work

**Substantial Beat Difference**:
The rule that adjacent Beats or image roles should differ enough to create real movement at the current Arc Scale. In short arcs and image series, adjacent Beats should differ on at least three meaningful axes, with at least one difference in Intended Feeling, active tension profile, or communication intent. In longer arcs, one larger emotion may build across multiple Beats, but each Beat still needs an Expectation Turn, and key movements carry the major emotional shifts. Composition, amplitude, symbol, light/color, density, motion, and spatial openness can support the difference, but surface variation alone is not enough.
_Avoid_: Different-looking beats that create the same emotional pressure in the same way, or long arcs where beats repeat without expectation/result movement

**Expectation Turn**:
The required beat-level change where a Beat sets, bends, frustrates, reverses, withholds, or complicates an expectation. Even when one emotion builds across several Beats, each Beat should create some unexpected result so the tension between expectation and outcome sharpens the Intended Feeling.
_Avoid_: Beats that merely continue, restate, or decorate the previous emotional state

**Expectation Turn Translation**:
The medium-specific expression of a Beat's Expectation Turn. The Beat Plan owns the expected direction, actual result, surprise function, and emotional counterpoint; the Medium Plan owns how that turn becomes visible, sonic, textual, or otherwise perceivable.
_Avoid_: Duplicating the Beat's Expectation Turn without explaining how the medium expresses it

**Style Interview**:
A short narrowing interview that starts by asking whether the artist has a specific visual vision or wants to explore what art style to use. It helps the artist choose Style Direction without needing to know style taxonomy.
_Avoid_: Long category survey or fixed menu of styles

**Style Clarifier**:
One targeted question used when the artist names a style that is broad or internally ambiguous.
_Avoid_: Full Style Interview when the artist already specified style

**Style Category Reference**:
A controlled or semi-controlled category list used as seed vocabulary for Style Direction, upload categorization, or provider prompt translation.
_Avoid_: Treating upload categories as the full art ontology

**Wondermint Category Reference**:
The initial Style Category Reference from `/Users/ashokaji/code/fullstock/Wondermint Skill File/skills/wondermint-marketplace/skills/references/categories.md`.
_Avoid_: Inventing Wondermint upload subcategories

**Style Decision Tree**:
A short set of questions where each answer narrows the likely Style Direction space by roughly half.
_Avoid_: Making artists browse every style category

**Style Interview Fallback Order**:
The default Style Interview sequence: medium language, representation, finish, then genre-world.
_Avoid_: Rigid order when Artist Meaning already narrows style

**Style Interview Stop Condition**:
The point where Primary Style, bounded Style Modifiers, known conflicts, and alignment with Artist Meaning are clear enough to stop asking style questions.
_Avoid_: Asking all fallback questions when style is already clear

**Style Recommendation**:
The agent-synthesized Style Direction proposed after a Style Interview for artist confirmation.
_Avoid_: Raw style answers without synthesis

**Style Exploration Board**:
One internal comparison-board prompt that can render six candidate Style Directions using the same subject, Artist Meaning, and Target Visual Engine. At the gate, the artist sees concise style option labels first; the full prompt stays internal unless requested.
_Avoid_: Showing the full image prompt by default or treating style samples as separate final artworks

**Symbology Direction**:
What the image shows as the core symbolic representation of Artist Meaning, such as a figure, object, landscape, ritual scene, room, threshold, vessel, or abstraction.
_Avoid_: Choosing art style before deciding what the image represents

**Active Absence Symbology**:
A Symbology Direction where absence itself is the symbolic representation: an omitted figure, empty room, untouched object, silence, negative space, withheld event, missing cause, or unresolved gap carries the work's Intended Feeling.
_Avoid_: Filling in missing subjects just because the medium can show them

**Symbology Gate**:
The first visual choice gate after Artist Meaning, where the artist decides how the work should be symbolically represented and whether the work should become a single image, compressed arc, or image series.
_Avoid_: Hiding symbolic representation inside final prompt variants

**Symbology Board**:
One internal comparison-board prompt for six symbolic representations of the same Artist Meaning and Creative Brief. At the gate, the artist sees concise symbolic option labels first; the full prompt stays internal unless requested.
_Avoid_: Showing the full image prompt by default or choosing style before symbolic representation

**Gate Decision**:
The durable record of an artist-facing gate choice, revision, rejection, skip, approval, or explicit permission to proceed unconfirmed. Gate-specific detail belongs in the relevant stage record, board, Medium Plan, Prompt Plan, Text Generation Plan, or Prompt Branch Set.
_Avoid_: Separate specialized decision schemas before a gate proves it needs one

**Style Gate**:
The second visual choice gate, where the artist chooses the artistic language for the selected Symbology Direction.
_Avoid_: Style overriding symbolic meaning

**Prompt Variant Strategy**:
The plan for how Prompt Variant Plans differ while preserving the approved meaning, symbology, Style Direction, Visual Dynamics, and Shot Design.
_Avoid_: Mandatory extra visual gate, arbitrary variation

**Prompt Branch Gate**:
The gate that approves a Prompt Branch Set strategy before generation: branch count, meaning kernel, variation axes, hold-constant rules, and minimum distinction rule.
_Avoid_: Generation Approval Gate, provider-backed generation approval

**Style Confirmation Status**:
Whether Style Direction is artist specified, confirmed, or unconfirmed before Brief Approval.
_Avoid_: Extra approval gate before Art Critic Review

**Target Visual Engine**:
The intended visual construction of a Generated Work, especially when the Reference is not already visual.
_Avoid_: Pretending text has literal visual properties

**Target Sonic Engine**:
The intended sound construction of a Generated Work, especially when the Reference is text.
_Avoid_: Treating genre or tempo as the whole sound direction

**Sonic Concept Direction**:
The core sound-world, sonic metaphor, or musical premise used to express Artist Meaning.
_Avoid_: Genre Direction

**Genre Direction**:
The musical language or genre frame used to express a Sound Creative Brief, represented as one Primary Genre plus bounded modifiers.
_Avoid_: Equal-weight genre pileup

**Tempo / Groove Direction**:
The target pace, felt motion, meter, rhythmic feel, and groove stability for a sound work.
_Avoid_: BPM only

**Vocal / Lyric Policy**:
The required decision about whether a sound work has lyrics or intelligible words, and whether those words are absent, source-verbatim, adapted, newly written, spoken, phonetic, or wordless.
_Avoid_: Silently inventing lyrics inside a final prompt

**Lyrics Draft**:
Reviewable lyrics created when the artist asks for adapted or new lyrics in a text-to-sound workflow.
_Avoid_: Hidden provider prompt text

**Arrangement / Form Direction**:
The time structure of a sound work, including sections, dynamic arc, entries, removals, silence, and ending behavior.
_Avoid_: Layout Plan

**Song Structure**:
The nested time architecture of a song: Song, Sections, Phrases, and Bars or beats.
_Avoid_: Treating a song as only a duration

**Section Function**:
The role one song section plays, such as invitation, grounding, build, release, development, contrast, rupture, return, closure, or residue.
_Avoid_: Section label only

**Section Tension Map**:
The section-by-section mapping of active Emotional Tension Pairs and Sonic Tension Pairs across a song.
_Avoid_: One static tension score for the whole song

**Text-To-Sound Slice**:
The dry-run workflow that transforms a text Reference into a Sound Prompt Plan plus final platform renderings such as Suno Custom Mode.
_Avoid_: Provider-backed music generation

**Sound Prompt Plan**:
A platform-neutral Prompt Plan expressed as Artist OS traceable sound concepts, Prompt Variant Plans, and platform output intent before final generator-specific rendering.
_Avoid_: Suno-only prompt contract, Sound Medium Plan

**Platform Rendering**:
The final generator-specific translation of a Sound Prompt Plan into provider-native fields, syntax, settings, upload guidance, and readiness checks.
_Avoid_: Changing Artist Meaning, replacing the Sound Prompt Plan

**Suno Platform Rendering**:
A Platform Rendering that maps approved sound prompt intent into Suno Custom Mode fields.
_Avoid_: Treating Suno Custom Mode as upstream sound-planning authority

**Derived Sonic Element**:
A new motif, sound, instrument, texture, hook, lyric image, or production gesture introduced by a Prompt Variant Plan because it strengthens approved Artist Meaning, Sonic Dynamics, Beat Plan, or Poetic Density.
_Avoid_: Unmarked invention

**Core Visual Tension Pairs**:
The standard Visual Dynamics library: Light/Dark, Saturated/Muted, Warm/Cool, Harmonious/Discordant, Dense/Sparse, Geometric/Organic, Sharp/Diffuse, Linear/Painterly, Textured/Smooth, Representational/Non-Representational, Flat/Deep, Balanced/Unbalanced, Centered/Decentered, and Singular/Repetitive.
_Avoid_: Color labels, composition tags

**Active Visual Tensions**:
The selected Core Visual Tension Pairs that materially shape a specific Creative Brief.
_Avoid_: Scoring every visual pair by default in the First Slice

**Series Amplitude Plan**:
The internal 0-1 visual amplitude profile for each suggested image in an image series, covering framing distance, subject scale, visual density, motion energy, spatial openness, detail intensity, and emotional pressure.
_Avoid_: Letting every image in a series use the same distance, density, and motion by accident

**Conditional Visual Tension Pair**:
A Visual Dynamics pair that appears only when relevant to the Reference or target medium.
_Avoid_: Always-required visual pair

**Emotional Structure**:
The full emotional model of a Reference inside a Creative Brief.
_Avoid_: Emotional Brief, vibe, mood

**Poetic Density**:
The degree to which one Reference, detail, Beat, Tension Point, or Generated Work can hold multiple meanings at once.
_Avoid_: Single meaning, message

**Poetic Density Notes**:
Qualitative notes that identify layered meanings, flattening risks, and details that carry multiple meanings.
_Avoid_: Poetic Density score

**Tension Pair**:
A paired emotional or formal opposition where each pole can be present independently and the relationship between them carries meaning.
_Avoid_: Bipolar slider

**Core Tension Pairs**:
The first standard set of Tension Pairs: Attraction/Repulsion, Proximity/Distance, Order/Chaos, Stillness/Motion, Legibility/Opacity, Control/Surrender, Safety/Threat, and Presence/Absence.
_Avoid_: Valence/arousal, Pain/Pleasure

**Tension Pair Record**:
The Creative Brief Record representation of one emotional or visual Tension Pair, including both pole presences, tension intensity, evidence, optional artist note, and translation notes.
_Avoid_: Slider value

**Tension Pair Salience**:
The relevance of a Tension Pair to a specific Reference, marked as not salient, low, medium, or high.
_Avoid_: Omitting a Core Tension Pair

**Emotional Qualities**:
Artist-specific or reference-specific descriptive terms that do not fit the Core Tension Pairs.
_Avoid_: Emotional Dimensions

**Emotional Arc**:
The emotional change over time or implied movement inside a Reference.
_Avoid_: Beat Plan

**Story Structure**:
The reusable movement pattern that describes how a work changes, holds, intensifies, breaks, returns, or remains unresolved before medium-specific planning.
_Avoid_: Format, output shape, asset count

**Story Structure Library**:
A reusable library of Story Structures that helps Artist OS adapt emotional, symbolic, narrative, rhetorical, or experiential movement before Medium Plans recommend output shape.
_Avoid_: Format Structure Library, template library, series template

**Story Structure Library Entry**:
One reusable Story Structure definition containing its movement pattern, typical Beat Roles, key turns, compression guidance, expansion guidance, medium affinities, common failure modes, and adaptation questions.
_Avoid_: Rigid outline, output-count template

**Adapted Story Structure**:
The project-specific Story Structure stored inside a Beat Plan, including library entry name, compact grounding metadata, core movement, adaptation summary, turn logic, compression rule, expansion rule, and failure modes.
_Avoid_: Separate story-authority record, output-shape recommendation

**Structure Grounding**:
The named source tradition, framework, research source, or artist-approved rationale that defines the parameters of a Story Structure or Cultural Format Structure.
_Avoid_: Unmarked invention, vague best practice

**Structure Grounding Tier**:
The authority level for Structure Grounding: canonical or field-recognized framework, craft authority, platform-era pattern evidence, or artist-defined/project-specific structure.
_Avoid_: Treating all structure sources as equally authoritative

**Cultural Format Structure**:
The culturally recognized audience-facing grammar of a format, such as an article, op-ed, short story, novel, screenplay, trailer, documentary short, video essay, sermon, artist statement, or hook-driven social post.
_Avoid_: Story Structure, asset count, provider format

**Cultural Format Structure Library**:
A reusable library of Cultural Format Structures that helps Artist OS make outputs coherent with established audience expectations for a form.
_Avoid_: Story Structure Library, generic template collection, style category list

**Cultural Format Structure Library Entry**:
One reusable Cultural Format Structure definition containing expected parts, audience promise, hook logic, turn/payoff behavior, pacing norms, required decisions, common failure modes, and adaptation questions.
_Avoid_: Fill-in-the-blank template, rigid formula

**Adapted Cultural Format Structure**:
The project-specific Cultural Format Structure stored inside a Medium Plan, including compact grounding metadata, audience promise, Audience Hook, adapted parts, turn or payoff, adaptation policy, failure modes, and recommended Stewardship Views.
_Avoid_: Replacing Medium Plan section structure, rigid template

**Platform Container**:
The publishing surface that packages an output for a specific platform or channel, such as Instagram Reel, TikTok photo post, YouTube Short, LinkedIn document carousel, Reddit AMA post, or Substack Note.
_Avoid_: Cultural Format Structure, Story Structure, creative template, platform constraints

**Research Grounding**:
An optional early text-planning decision to use online research or artist-provided sources to ground a public-facing, timely, factual, trend-aware, or platform-native written work in current evidence before the piece's argument, examples, or audience promise harden.
_Avoid_: Silent browsing, treating web research as required for private or purely expressive work, letting current trends override Artist Meaning

**Format Length Standard**:
The default word-count range and target used by a Text Medium Plan for a recognizable written format, derived from Cultural Format Structure and publication use before drafting. It gives the draft a reviewable size target without overriding Artist Meaning or an artist-approved length.
_Avoid_: Treating word count as a universal quality metric, confusing heuristic format length with external platform limits, silently expanding or compressing a piece against the artist's purpose

**Review Presentation**:
The artist-facing format used to review a drafted written Output Artifact, such as Markdown, HTML mockup, or both. HTML mockups are local review artifacts that make reading and layout review easier; they do not publish, upload, or replace the source draft.
_Avoid_: Provider-backed generation, publishing workflow, treating HTML as the canonical written artifact

**Release Package**:
A coordinated set of outputs prepared as one artist-facing release, such as an album, EP, single bundle, campaign, or visual album.
_Avoid_: Treating each asset as an unrelated project, Platform Container

**Release Package Plan**:
The schema-backed package-level coordination record for a Release Package, owning deliverables, medium roles, calibration status, production order, and cross-media continuity decisions.
_Avoid_: Medium Plan, Long-Work Stewardship Record, prose-only package notes

**Album**:
A Release Package whose primary medium is sound and whose parts usually include ordered tracks plus supporting text and visual assets.
_Avoid_: Generic Cumulative Work, Sound Medium Plan

**EP**:
A Release Package subtype for a shorter sound-primary release with multiple tracks.
_Avoid_: Album subtype

**Single Bundle**:
A Release Package subtype for one primary track plus supporting versions, covers, text, visuals, or related assets.
_Avoid_: Album subtype

**Visual Album**:
A Release Package subtype where visual outputs are primary companions to the sound release rather than supporting cover assets.
_Avoid_: Album Cohesion Mode, Album with stronger style

**Album Deliverable**:
A required or optional output inside an Album, such as the album title, album description, album cover, track Sound Prompt Plan, or track cover Image Prompt Plan.
_Avoid_: Treating album deliverables as unrelated outputs

**Working Release Copy**:
The early title or description text stored on a Release Package Plan so the package can be understood before polished release copy is drafted.
_Avoid_: Treating every title or description as a full Text Journey

**Working Track Title**:
The early title stored for an Album track before optional polished naming work.
_Avoid_: Forcing every track title through a full Text Journey

**Album Beat Plan**:
The album-level Beat Plan that owns track order, cross-track Emotional Movement, Key Emotional Movements, and each track's job in the album.
_Avoid_: Track-Level Beat Plan, Sound Medium Plan

**Track-Level Beat Plan**:
A Beat Plan for one track that deepens that track's internal movement while tracing back to the governing Album Beat Plan.
_Avoid_: Replacing the Album Beat Plan

**Album Cohesion Mode**:
The Album routing decision for whether tracks form a cumulative arc, a standalone collection, or a hybrid of dependent clusters and standalone tracks.
_Avoid_: Assuming every album needs Long-Work Stewardship

**Track Cover**:
The image deliverable for one Album track, translating the track's emotional movement while obeying album-level visual continuity rules.
_Avoid_: Unrelated cover art, generic song thumbnail

**Album Visual System**:
The lightweight package-level visual language that coordinates the album cover and Track Covers.
_Avoid_: Image Medium Plan, visual bible

**Album Sonic System**:
The lightweight package-level sonic language that coordinates the Album's tracks without replacing track-level Sound Medium Plans.
_Avoid_: Sound Medium Plan, separate sonic bible

**Album Calibration**:
The early Album checkpoint that tests whether representative sound and visual directions are moving correctly before final outputs are produced.
_Avoid_: Treating calibration as final acceptance, producing all album deliverables before checking sonic and visual language

**Album Calibration Subcheck**:
One directional verdict inside Album Calibration, such as sonic direction, visual direction, or sound-visual fit.
_Avoid_: Final Output Acceptance

**Calibration Track**:
The Album track selected to test whether the Album Sonic System and related visual direction are moving correctly.
_Avoid_: Automatically using track one or the lead single

**Calibration Track Cover**:
The Track Cover used during Album Calibration to test whether a track's emotional movement translates into the Album Visual System.
_Avoid_: Automatically using the album cover for visual calibration

**Audience Hook**:
The opening attention mechanism that creates enough curiosity, tension, beauty, identification, surprise, or promise for the audience to keep going.
_Avoid_: Clickbait, headline only, first sentence only

**Cultural Format Adaptation Policy**:
The Medium Plan decision for which Cultural Format Structure parts are required, mergeable, omittable, or invertible for a specific project.
_Avoid_: Treating cultural format parts as unchangeable slots

**Emotional Payload**:
The felt meaning carried by one Beat.
_Avoid_: Emotion, vibe

**Beat**:
The smallest meaningful change, contrast, turn, or pressure point in a Reference that carries Emotional Payload.
_Avoid_: Plot point, scene

**Series Recommendation**:
A Creative Brief recommendation for whether a Reference should become a single image or image series. A three-image sequence is an image series with three suggested images.
_Avoid_: Generating a series by default without artist approval

**Series Plan**:
An approved plan for multiple related images that preserve a larger Beat Plan or sequence of Tension Points.
_Avoid_: Prompt variants

**Three-Part Sequence**:
A Story Mode for a clear three-part transformation, such as before/threshold/after, invitation/rupture/consequence, or concealment/revelation/aftermath. It does not decide image count or create a special image output class.
_Avoid_: Triptych, image output shape, generic three variants

**Image Series**:
A multi-image Series Plan or Series Recommendation. This includes a three-image output when three images best serve the approved Beat Plan.
_Avoid_: Prompt variants

**Cumulative Work**:
A multi-output or long-form Artist OS Project where each part builds on prior parts through sequence, emotional arc, escalation, transformation, or dependency.
_Avoid_: Collection, portfolio, batch

**Long-Work Stewardship**:
The Artist OS guardrail layer for Cumulative Work that protects story structure, emotional arc, continuity, checkpoints, and approved part-to-part dependency.
_Avoid_: Story bible, collection review

**Long-Work Stewardship Record**:
The schema-backed Project Memory record for a Cumulative Work, centered on planned parts, checkpoints, continuity rules, readiness, and drift while referencing the Beat Plan as story authority.
_Avoid_: Beat Plan, story bible, Project Manifest

**Long-Work Part**:
One cumulative unit inside a Long-Work Stewardship Record, such as an image role, text section, chapter, scene, poem movement, song section, sound movement, video scene, or mixed-media movement.
_Avoid_: Prompt Variant Plan, Variant

**Long-Work Readiness**:
The readiness state for expanding a Cumulative Work. It may be pending before the readiness pass runs; after review, it is marked ready, ready with risks, repair before expansion, or waived.
_Avoid_: Quality score, taste score

**Long-Work Checkpoint**:
A required or optional stop in Long-Work Stewardship where Artist OS reviews cumulative integrity before continuing.
_Avoid_: Generic progress note

**Long-Work Reviewer**:
The bounded reviewer role that applies Long-Work Stewardship to readiness, checkpoints, cumulative drift, and proposed continuity updates.
_Avoid_: Story Critic, Art Critic, Output Critic

**Long-Work Continuity Rule**:
A first-class stewardship rule that preserves part-to-part continuity for emotional arc, symbol, visual language, voice, motif, character, setting, sonic language, structure, or pacing.
_Avoid_: Story bible entry, loose note

**Stewardship View**:
A readable projection of Medium Plan and Long-Work Stewardship state for a specific long-form need, such as a plot tracker, chapter tracker, act tracker, open-thread list, or character continuity view.
_Avoid_: Separate story authority, separate tracking record

**Proposed Continuity Update**:
A candidate change discovered from an Output Artifact, calibration, draft, or review that may become a Long-Work Continuity Rule only after the required approval.
_Avoid_: Silent canon update, automatic story bible update

**Collection Coherence Review**:
A lighter review for non-sequential portfolios, store sets, and curator batches that checks cohesion, meaningful variation, shared rules, and drift without imposing a story sequence.
_Avoid_: Long-Work Stewardship, Series Plan

**Series Calibration Image**:
The first generated image used to lock Style Direction, Target Visual Engine, and series language before producing the rest of an approved Series Plan.
_Avoid_: Generating the whole series before visual approval

**Calibration Image Role**:
The Image Role selected for the Series Calibration Image because it best represents the series' Style Direction, Target Visual Engine, and emotional tension.
_Avoid_: Automatically using the first Beat

**Calibration Choice**:
The artist's selected Series Calibration Image direction, recorded as durable visual language for the remaining Series Plan.
_Avoid_: Temporary generation preference

**Series Calibration Fields**:
The minimal Creative Brief Record fields that preserve Style Progression and Series Calibration requirements before the full Calibration Choice workflow exists.
_Avoid_: Full Calibration Choice schema too early

**Variant Test Axis**:
An unresolved creative dimension tested across Prompt Variant Plans, such as realism/cartoon, literal/symbolic, sparse/dense, or restrained/intense.
_Avoid_: Arbitrary variation

**Variant Test Axis Label**:
The field on a Prompt Variant Plan that states how that stable variant label tests an unresolved creative dimension.
_Avoid_: Replacing Faithful, Amplified, and Minimal labels

**Variant Differentiator**:
A concrete visual lever that makes one Prompt Variant Plan visually distinct from the others, such as composition, viewpoint, density, symbolic treatment, abstraction level, light/color strategy, texture, finish, or focal hierarchy.
_Avoid_: Only changing adjectives or intensity words

**Single-Generation Variant Comparison**:
One optional comparison image that lays multiple Prompt Variant Plans into a single generated image for artist review after Symbology Direction and Style Direction are selected.
_Avoid_: Mandatory variant comparison, treating the comparison image as a Series Plan

**Layout Plan**:
The Provider-Neutral Prompt Plan field that records final output arrangement: single image, three-panel variant comparison, series calibration image, or series image. Pre-locking exploration boards are recorded in visual boards, not Layout Plan.
_Avoid_: Hiding generation layout inside prompt prose only

**Visual Boards**:
The Provider-Neutral Prompt Plan field that records pre-locking Symbology Boards and Style Exploration Boards, including options, traceability, risks, selection status, and whether provider-backed generation was approved.
_Avoid_: Stuffing exploration-board options into Layout Plan prose

**Tension Point**:
A meaningful contrast or unresolved pressure that carries emotion but does not imply before/after change.
_Avoid_: Beat when no change is present

**Beat Plan**:
The required story-spine record for every output, including a single image. It may be compact when the output is one compressed beat, but it cannot be skipped.
_Avoid_: Optional story layer, image-only shortcut

**Transformation Plan**:
The legacy conceptual term for preserving meaning while changing medium or form. The typed pipeline records this as a **Transformation Brief**.
_Avoid_: Prompt Plan, new schema names using Transformation Plan

**Meaning-Preserving Transformation**:
Changing medium or form while preserving Artist Meaning, selected Formal Analysis, Emotional Structure, and relevant Beats or Tension Points.
_Avoid_: Format conversion, style transfer

**Medium Plan**:
The medium-specific translation record that explains how an approved Beat Plan becomes a specific medium. Image Medium Plan, Sound Medium Plan, Video Medium Plan, Text Medium Plan, and Mixed-Media Plan are specializations of this concept.
_Avoid_: Creative Brief, Prompt Plan, provider settings

**Medium Output Shape Recommendation**:
A Medium Plan recommendation for how an approved Beat Plan and adapted Story Structure should be realized in one medium, such as a text form, sound form, single compressed image, image series, short video, or longer sequence.
_Avoid_: Asset count, format decision before story structure, series-first recommendation

**Accepted Output Shape**:
The artist-approved or explicitly unconfirmed output shape that the Medium Plan will use after considering the requested shape, Medium Output Shape Recommendation, tradeoffs, and any Medium Output Shape Conflict.
_Avoid_: Requested shape, recommended shape

**Medium Output Shape Conflict**:
A surfaced conflict between the artist-requested output shape and the Medium Plan's story-preserving Medium Output Shape Recommendation.
_Avoid_: Silent override, silently obeying a shape that weakens Artist Meaning

**Workflow Scale Routing**:
The internal Artist OS routing decision that determines which planning, stewardship, review, and continuity supports are needed for the scale of a work. It keeps compact outputs from carrying long-work overhead while activating Long-Work Stewardship, Stewardship Views, checkpoints, and continuity helpers when a work becomes cumulative or long-form.
_Avoid_: Length Gate, user-facing gate, word-count trigger, asset-count trigger

**Workflow Scale Level**:
One of the internal routing levels used by Workflow Scale Routing: Compact Artifact, Structured Single Artifact, Cumulative Work, or Full Long-Form Project. Schema values are `compact_artifact`, `structured_single_artifact`, `cumulative_work`, and `full_long_form_project`.
_Avoid_: Size score, quality tier, fixed word-count band

**Project-Level Workflow Scale Routing**:
The first Workflow Scale Routing pass, run after Story Approval, that decides the scale of the Artist OS Project and whether durable canon management or Cumulative Work support is needed before medium-specific planning.
_Avoid_: Medium Output Shape Recommendation, text form choice

**Medium-Level Workflow Scale Routing**:
The medium-specific Workflow Scale Routing pass inside a Medium Plan. It decides which scale supports that output journey needs, because one project may contain both compact outputs and cumulative outputs.
_Avoid_: Replacing project-level routing, assuming every medium inherits the largest project scale

**Workflow Scale Routing Timing**:
Workflow Scale Routing may be estimated during Orientation, but the first authoritative Project-Level Workflow Scale Routing pass happens after Story Approval. Medium-Level Workflow Scale Routing happens inside each Medium Plan. If the artist changes scope, Workflow Scale Routing is rerun and later helpers are activated or skipped according to the revised scale.
_Avoid_: One-time guess before the Beat Plan, user-facing approval gate

**Workflow Scale Reroute**:
A revised Workflow Scale Routing decision caused by artist scope change or evidence that the current scale support is too light or too heavy. Upward reroutes may happen when the artist expands scope or dependent parts/durable canon needs appear. Downward reroutes after long-work state exists require explicit acknowledgement; existing stewardship or planning records should be preserved or superseded, not silently deleted.
_Avoid_: Silent downgrade, deleting stewardship state

**Workflow Scale Routing Field**:
The compact schema field used to persist Workflow Scale Routing on existing pipeline records. It contains `scale_level`, `rationale`, `trigger_signals`, `activated_supports`, `skipped_supports`, and `reroute_triggers`. Project-Level Workflow Scale Routing belongs on the Beat Plan. Medium-Level Workflow Scale Routing belongs on each Medium Plan. Artist OS does not use a standalone Workflow Scale Routing Record unless future projects prove routing needs its own lifecycle.
_Avoid_: Standalone routing record by default, chat-only routing decision

**Workflow Scale Routing Schema Adoption**:
Workflow Scale Routing should be schema-backed on Beat Plan and Medium Plans. Beat Plan records carry project-level routing. Text Medium Plan, Image Medium Plan, and Sound Medium Plan records all carry required medium-level routing. Adoption should reuse the same compact field shape rather than creating a standalone record.
_Avoid_: Docs-only routing after field shape is settled

**Compact Artifact**:
A work small enough for one output artifact to hold the whole approved movement without long-work continuity machinery, such as a single image, short poem, flash story, one compact song, or compressed visual arc.
_Avoid_: Single beat only, simple work

**Structured Single Artifact**:
One output artifact with internal sections, movements, scenes, arguments, or arrangement parts, but without dependent outputs across drafting or generation sessions.
_Avoid_: Cumulative Work, Long-Work Stewardship by default

**Full Long-Form Project**:
A large Cumulative Work with durable canon needs, such as a novel, novella, feature film, serialized fiction project, or comparable long narrative project. The upgrade trigger is durable canon management, not sheer length: recurring character states, world rules, timelines, subplots, open threads, voice/style continuity, extraction and verification, or whole-work synthesis. It may require specialized long-form supports such as plot trackers, character sheets, world-building records, chapter or scene briefs, style guides, extraction and verification, synthesis checkpoints, and publishing or completion audits.
_Avoid_: Any multi-beat arc, any long text, any image series

**Workflow Scale Support Bundle**:
The default set of planning, stewardship, review, continuity, and long-form helper tools activated for a Workflow Scale Level. Compact Artifacts use the core Artist OS pipeline without Long-Work Stewardship. Structured Single Artifacts add medium-owned section, movement, scene, argument, or arrangement planning. Cumulative Work adds Long-Work Stewardship, Long-Work Parts, readiness, checkpoints when needed, and Stewardship Views when useful. Full Long-Form Projects add durable canon tools such as plot trackers, character sheets, world-building records, chapter or scene briefs, style guides, extraction and verification, synthesis checkpoints, and publishing or completion audits.
_Avoid_: Enabling every helper for every project, skipping scale-specific support

**Workflow Scale Support**:
A named support module that Workflow Scale Routing may activate or skip. Initial schema values are `core_pipeline`, `medium_section_plan`, `cultural_format_structure`, `long_work_stewardship`, `long_work_parts`, `long_work_readiness`, `long_work_checkpoints`, `stewardship_views`, `plot_tracker`, `character_sheets`, `world_building`, `chapter_or_scene_briefs`, `style_guide`, `extraction_verification`, `synthesis_checkpoints`, `publishing_or_completion_audit`, and `collection_coherence_review`.
_Avoid_: Freeform helper names, duplicate support labels

**Workflow Scale Trigger Signal**:
A named reason that caused Workflow Scale Routing to choose a scale level. Initial schema values are `artist_requested_compact_output`, `artist_requested_long_form`, `artist_requested_sequence_or_series`, `single_artifact_can_hold_movement`, `internal_sections_or_movements_needed`, `dependent_parts_needed`, `durable_canon_needed`, `recurring_characters_needed`, `world_rules_or_timeline_needed`, `subplots_or_open_threads_needed`, `voice_or_style_continuity_needed`, `extraction_verification_needed`, `synthesis_or_batch_generation_needed`, `publication_or_completion_audit_needed`, and `collection_without_sequence`.
_Avoid_: Word-count-only trigger, asset-count-only trigger

**Planning View**:
A lightweight, non-authoritative helper view used to plan or explain one artifact, such as temporary character notes, world notes, act outline, chapter sketch, plot tracker, or treatment support. A Planning View does not create Long-Work Stewardship unless the project also creates dependent parts that need cumulative execution tracking.
_Avoid_: Long-Work Stewardship, authoritative canon record

**Prompt Plan**:
The generation-facing prompts and constraints for a specific model or medium.
_Avoid_: Creative Brief, Transformation Plan

**Provider-Neutral Prompt Plan**:
A Prompt Plan expressed in Artist OS concepts before provider-specific translation.
_Avoid_: Provider prompt

**Provider Target**:
An optional Prompt Plan translation block created when the artist requests a specific image generator, such as Midjourney. It stores provider-specific settings, rendered suffixes, and paste-ready prompts while keeping the approved Prompt Variant Plans provider-neutral.
_Avoid_: Making provider syntax the canonical prompt

**Midjourney Parameter Suffix**:
The provider-specific prompt-ending controls for Midjourney-family prompts, such as `--ar`, `--s`, `--c`, `--q`, `--seed`, `--raw`, and `--no`.
_Avoid_: Hiding Midjourney controls in prose, applying Midjourney syntax to providers that use API fields or workflow settings

**Prompt Variant Plan**:
One provider-neutral prompt direction inside a Provider-Neutral Prompt Plan.
_Avoid_: Generated Work, Variant before provider-backed generation

**Prompt Branch Set**:
A pre-generation batch of prompt branches derived from one approved Prompt Plan. It preserves the same Artist Meaning and meaning kernel while deliberately varying approved axes for human curation. Image Prompt Branch Sets currently vary axes such as style, setting, symbol, composition, and palette/light; other media can add medium-specific axes later.
_Avoid_: Variant, Generated Work, Prompt Variant Plan

**Actionable Prompt Branch Set**:
A Prompt Branch Set that will be used for provider-backed generation or serious curator selection. It requires Prompt Critic Review before use.
_Avoid_: Treating a draft branch set as generation-ready

**Faithful Prompt Variant**:
The Prompt Variant Plan that stays closest to the approved Creative Brief.
_Avoid_: Literal copy

**Amplified Prompt Variant**:
The Prompt Variant Plan that pushes the strongest tension, Poetic Density, and Target Visual Engine while preserving Artist Meaning.
_Avoid_: New Artist Meaning, exaggeration without provenance

**Derived Symbol**:
A new visual symbol introduced by a Prompt Variant Plan because it strengthens Artist Meaning, a Tension Pair, an Active Visual Tension, a Beat or Tension Point, or Poetic Density.
_Avoid_: Unmarked invention, pretending derived material came from the Reference

**Derived Symbol Review**:
Artist review of marked Derived Symbols as part of reviewing the full Provider-Neutral Prompt Plan.
_Avoid_: Separate approval gate in the First Slice

**Minimal Prompt Variant**:
The Prompt Variant Plan that strips the image down to the essential emotional and visual engine.
_Avoid_: Underspecified prompt

**Provider Adapter**:
Code or skill logic that translates a Provider-Neutral Prompt Plan into one provider's prompt and settings format.
_Avoid_: Provider Profile

**Dry Run**:
An Artist OS workflow that produces records, briefs, plans, and critique criteria without calling a media generation provider.
_Avoid_: Generation

**Provider-Backed Generation**:
An Artist OS workflow that calls a configured media generation provider to create Variants from a Prompt Plan.
_Avoid_: Dry Run

**Provider Profile**:
Local, uncommitted configuration that tells Artist OS which media generation providers are available and how to call them.
_Avoid_: API keys, .env

**Example Corpus**:
Committed sample References and records that are safe to share.
_Avoid_: Workspace Library

**Workspace Library**:
Local uncommitted storage for real artist References, Creative Briefs, gate decisions, Prompt Plans, Text Generation Plans, Generated Works, image files, sidecar metadata, and Output Records.
_Avoid_: Example Corpus

**Artist Library**:
The user-visible folder tree where artists browse project outputs, readable project summaries, and personal creative library entries.
_Avoid_: Workspace Library, internal project state

**Personal Library**:
The artist's reusable private collection of visible creative guidance such as structures, styles, voices, formats, and learnings, backed by internal Workspace Library records.
_Avoid_: Shipped Structure Library, raw feedback log, committed examples

**Wondermint Root**:
The user-chosen parent folder that contains the visible `Wondermint/` Artist Library folder and the sibling hidden `.wondermint/` Workspace Library folder.
_Avoid_: Installing private state inside the visible Artist Library

**Wondermint Root Setting**:
The user-facing configuration that chooses the Wondermint Root for both the visible Artist Library and hidden Workspace Library.
_Avoid_: Low-level Workspace Library override

**Wondermint Marketplace Skill State**:
Wondermint Marketplace account setup, onboarding state, API-key location, and non-secret operating preferences currently stored by the Wondermint Marketplace skill under `~/Wondermint/`.
_Avoid_: Artist OS Workspace Library, Artist Library, Wondermint Root

**Wondermint Marketplace Downloads**:
Purchased files saved by the Wondermint Marketplace skill under `~/Documents/Wondermint/downloads/`.
_Avoid_: Artist Library project output, Workspace Library asset

**Cloud-Synced Wondermint Root**:
A Wondermint Root placed inside a cloud-synced folder, allowed only with a warning that Workspace Library state may encounter sync conflicts.
_Avoid_: Treating cloud sync as a conflict-free backup system

**Review Draft**:
A human-readable draft Output Artifact placed in the Artist Library for artist review before acceptance, revision, archival, or export.
_Avoid_: Internal schema record, gate decision, event log

**Artist OS Project**:
One isolated Workspace Library unit for a single artist goal, which may be a single image, one song, a long written work, an image series, a store collection, or another bounded output journey.
_Avoid_: Book, global workspace, chat thread

**Artist OS Library Database**:
The SQLite query index at `workspace-library/artist-os/artist-os.sqlite`, refreshed from project manifests, event logs, and asset sidecars.
_Avoid_: Source of truth for binary media

**Missing Project**:
A project row in the Artist OS Library Database whose project folder or `project.json` was not found during the latest sync.
_Avoid_: Archived Project

**Visible Missing Project**:
An Artist OS Project whose Workspace Library state exists but whose Artist Library project folder or Project Pointer was not found during sync.
_Avoid_: Deleted Project, Missing Project

**Project Manifest**:
The `project.json` record that lets an agent reload one Artist OS project across sessions.
_Avoid_: Chat memory

**Project Pointer**:
The hidden file in an Artist Library project folder that records the Artist OS Project identity and lets agents reconnect the visible folder to Workspace Library state.
_Avoid_: Project Manifest, README, source of project truth

**Project README**:
The lightweight human-readable orientation file in an Artist Library project folder.
_Avoid_: Project Manifest, event log, full project record

**Project Memory**:
The durable per-project records, decisions, events, and accepted continuity context that let Artist OS resume one Artist OS Project without mixing it with another.
_Avoid_: Model memory, story bible, global memory

**Asset Metadata**:
The same-basename `.json` sidecar stored next to an image or export in the Workspace Library.
_Avoid_: Loose notes

**First Slice**:
The first complete Dry Run path through Artist OS: Text Reference to Image Prompt Plan.
_Avoid_: MVP

**Generated Work**:
An Output Artifact created by Artist OS or a provider from an approved Prompt Plan, Text Generation Plan, or Prompt Branch Set.
_Avoid_: Output Artifact when the origin was imported or human-authored

**Variant**:
One generated option within a generation set.
_Avoid_: Generated Work when referring to a specific option among alternatives; Prompt Branch, Prompt Variant Plan

**Accepted Work**:
An Output Artifact the artist approves as matching the intended meaning and use.
_Avoid_: Final asset

**Output Acceptance Gate**:
The artist-facing gate where the artist accepts, rejects, revises, archives, exports, or extends an Output Artifact after any required Output Critic Review.
_Avoid_: Acceptance Review, Critique, quality score

**Output Critic Review**:
The bounded sub-agent review that checks a drafted, generated, imported, or edited Output Artifact against Artist Meaning, Story Approval, Medium Plan, Prompt Plan or Text Generation Plan, approved branch or variant, and provenance before the Output Acceptance Gate.
_Avoid_: Artist acceptance, taste memory, calibration choice

**Output Artifact**:
Any concrete output that Artist OS can review, accept, archive, export, or use as calibration context, including Generated Works, artist imports, agent-drafted text, agent-rewritten text, and human-edited outputs.
_Avoid_: Generated Work when origin matters

**Output Record**:
The metadata and provenance record for any concrete output artifact Artist OS may review, accept, archive, export, or use as future calibration context, including provider-generated media, artist imports, agent-drafted text, agent-rewritten text, or human-edited outputs.
_Avoid_: Generated Work, Source Record, provider-only metadata

**Human-Edited Output Revision**:
A new Output Artifact revision created when an artist edits a visible Artist Library file, authoritative over the prior artifact for future continuation.
_Avoid_: Silent mutation of the previous Output Record

**Feedback Log**:
The durable record of artist feedback, acceptance decisions, revision requests, observed friction, and performance notes from Artist OS projects.
_Avoid_: Throwaway chat comments, only accepted preferences

**Learning Index**:
The cross-project index that references Feedback Log evidence and learned patterns so Artist OS can detect repeated preferences, corrections, and performance signals.
_Avoid_: Replacing per-project provenance

**Learning Candidate**:
A possible reusable preference, correction, process rule, format rule, or avoid rule extracted from Feedback Log evidence, edits, reviews, analytics, or output comparison.
_Avoid_: Hard rule from one weak signal

**Soft Learning**:
A reusable personal guidance signal that can bias Artist OS recommendations without overriding current Artist Meaning or approved project plans.
_Avoid_: Rule, blocker

**Hard Learning**:
A durable personal rule that Artist OS should apply by default because it has repeated evidence, strong analytics, explicit artist confirmation, or corrects a concrete schema/tooling mismatch.
_Avoid_: Taste guess, one-off preference

**Learning Rule**:
The concise applied instruction inside a Soft Learning or Hard Learning record, limited to roughly 600 characters and backed by separate evidence references.
_Avoid_: Full feedback transcript, mini skill file

**Learning Review**:
The classification pass that turns Feedback Log evidence into Learning Candidates and promotes patterns into Soft Learning or Hard Learning.
_Avoid_: Asking the artist to manually decide which raw feedback matters

**Performance Signal**:
A measured outcome attached to an Output Artifact, such as views, saves, shares, downloads, listens, completion rate, sales, playlist adds, comments, or a manual performance score.
_Avoid_: Artist preference, universal quality

**Performance Review**:
The interpretation pass that compares Performance Signals across outputs and proposes Learning Candidates.
_Avoid_: Replacing artist judgment with metrics

**Performance-Backed Learning**:
Soft Learning or Hard Learning promoted partly or fully from Performance Signals.
_Avoid_: Assuming high-performing means artistically correct

**Pending Learning Review**:
A project state indicating that Feedback Log evidence has not yet been classified for reusable learning.
_Avoid_: Finished learning, ignored feedback

**Output Batch**:
A future grouping record for comparing, costing, and managing multiple Output Records produced from the same Prompt Plan, Text Generation Plan, Prompt Branch Set, provider run, or curation pass.
_Avoid_: Adding batch-only fields to each Output Record before provider batch workflows exist

## Relationships

- **Artist Generation** produces **Artist OS**.
- **Artist OS** contains one or more **Skills**.
- A **Plugin** packages **Artist OS** for a specific agent host.
- A **Reference** has one **Source Record**.
- A **Reference** has **Artist Meaning** supplied by the artist.
- A **Meaning Interview** captures **Artist Meaning**.
- A confirmed **Artist Meaning Record** is versioned, not silently mutable. If the artist changes meaning later, create a superseding record and keep existing downstream records traceable to the version they used.
- Downstream records should reference the governing `artist_meaning_id` directly. `source_id` alone is not enough once a Reference can have multiple Artist Meaning versions.
- Downstream records may embed Artist Meaning summaries for readability and review packets, but `artist_meaning_id` is the authority. If an embedded summary conflicts with the referenced **Artist Meaning Record**, the referenced record wins.
- A **Reference** can produce one or more **Creative Briefs** after Artist Meaning, story, and medium planning are established.
- A **Visual Unit** is embedded inside the owning Medium Plan or storyboard plan; it is not a standalone record unless future rehearsals prove it needs its own lifecycle.
- An **Image Role** is the still-image realization of a **Visual Unit**.
- A **Storyboard Shot** is the time-based video realization of a **Visual Unit**.
- Adopt **Visual Unit** language in shared docs before migrating existing image schema fields; image schema churn waits until video rehearsals prove shared JSON schema definitions are useful.
- A **Beat Plan** remains story authority for video; **Video Sequence**, **Video Scene**, and **Storyboard Shot** are video execution structure.
- A **Video Sequence** groups **Video Scenes** for pacing, execution, continuity, or long-form navigation.
- **Video Sequences** are required only when scale, pacing, or stewardship needs scene groups; compact videos can plan directly with **Video Scenes** and **Storyboard Shots**.
- A **Video Scene** groups one or more **Storyboard Shots** and may map to one Beat, a Beat group, or a local dramatic purpose.
- The first schema-backed video planning artifact is a **Video Medium Plan** even when its implementation scope is storyboard-only.
- The first video validation target is **Video Medium Plan**; **Video Creative Brief Record** schema can follow after Video Medium Plan rehearsals prove the brief-specific fields.
- A **Video Medium Plan** is scale-general; feature films, episodic sequences, and other long-form video work use **Workflow Scale Routing** and **Long-Work Stewardship** rather than a separate video artifact.
- The v0 **Video Medium Plan** contains provider-neutral storyboard planning fields only; video generators, renderers, and Remotion-style animatic tools are downstream adapters, not domain authority.
- A **Text Generation Plan** owns drafted script, dialogue, voiceover, captions, social copy, and on-screen text wording; a **Video Medium Plan** owns their timing, placement, role, and relationship to Video Scenes and Storyboard Shots.
- A **Video Medium Plan** always states its **Video Audio Posture**, but Text Journey or Sound Journey records are created only when the selected posture needs drafted words or sound planning.
- Storyboard frame prompts belong to the v0 **Video Medium Plan**; a separate **Video Prompt Plan** waits until provider-neutral video generation instructions prove their fields.
- Generated storyboard stills are normal **Output Records** linked back to the relevant **Storyboard Shot**.
- **Video Style Expression** expresses the approved **Style Direction** over time; it does not replace or outrank Style Direction.
- A **Release Package** coordinates multiple outputs under one artist-facing release.
- A **Release Package Plan** coordinates selected Medium Plans and deliverables without replacing medium-specific planning authority.
- A **Release Package Plan** owns package subtype, deliverable list, required or optional status, Album Cohesion Mode when the package is an Album, track-to-deliverable mapping, package-level production order, Album Calibration state, cross-media continuity decisions, and references to governing plans and outputs.
- A **Release Package Plan** does not own song arrangement details, lyrics, genre, Sonic Dynamics, image Shot Design, Style Direction, prompt variants, title or description drafting rules, cumulative execution state, or part status.
- The first **Release Package Plan** schema should use the generic release-package name while implementing Album as the first supported package subtype.
- A **Release Package Plan** stores **Working Release Copy** early; polished title and description become Text deliverables only when the artist wants crafted release copy, options, or review.
- An **Album** is a **Release Package** whose primary medium is sound.
- **Album**, **EP**, **Single Bundle**, and **Visual Album** are sibling **Release Package** subtypes.
- A **Visual Album** is not an **Album Cohesion Mode**; it changes medium roles and expected deliverables.
- An **Album** has an artist-chosen track count; 10 tracks is an example, not a domain invariant.
- The first **Album** implementation requires album-level title, description, album cover, ordered tracks with **Working Track Titles**, one track Sound Prompt Plan per track, one track cover Image Prompt Plan per track, and package-level cross-media continuity rules.
- Track descriptions, lyrics, social captions, liner notes, and track story notes are optional Album deliverables unless the artist requests them or a track's approved direction requires them.
- Lyrics are conditional per Album track; each track's Sound Medium Plan owns Vocal / Lyric Policy and lyrics when required.
- An **Album Beat Plan** is the album story authority; **Track-Level Beat Plans** may deepen individual tracks but must trace back to the governing Album Beat Plan.
- Every Album track is represented by an Album Beat Plan Beat or Long-Work Part, but a **Track-Level Beat Plan** is created only when the track needs internal emotional movement beyond its album-level job.
- **Album Cohesion Mode** may be arc album, collection album, or hybrid album.
- An arc album activates **Cumulative Work** and **Long-Work Stewardship** by default; a collection album uses **Collection Coherence Review** by default; a hybrid album activates stewardship only for dependent clusters or a governing album arc.
- When **Album Cohesion Mode** activates **Long-Work Stewardship**, create the foundation Long-Work Stewardship Record after Story Approval and before approving the Release Package Plan so the Release Package Plan can reference an existing stewardship record.
- A collection album still requires explicit Album Sonic System, Album Visual System, Working Release Copy, and Collection Coherence Review, but it should not invent track-to-track escalation or dependency.
- A hybrid album uses one album-level **Release Package Plan** and one **Long-Work Stewardship Record** per dependent cluster or governing album arc.
- A **Track Cover** is governed by the track's assigned emotional movement and by album-level visual continuity rules.
- When a **Track-Level Beat Plan** exists, the **Track Cover** uses it as the primary track-specific authority while still tracing to the governing **Album Beat Plan** and **Release Package Plan**; otherwise it traces to the track's **Album Beat Plan** Beat or **Long-Work Part**.
- An **Album Visual System** owns shared visual language, allowed variation, recurring symbols or motifs, style constraints, and consistency rules across the album cover and Track Covers.
- An **Album Visual System** does not own individual cover Shot Design or prompt variants.
- Each Album cover deliverable gets its own Image Medium Plan generated from the shared **Album Visual System**.
- An **Album Sonic System** owns shared sonic language, allowed variation, recurring motifs, voice, instrumentation, production constraints, and consistency rules across Album tracks.
- An **Album Sonic System** does not own track arrangement, lyrics, section maps, or provider prompt fields.
- Each Album track gets its own Sound Medium Plan generated from the shared **Album Sonic System**.
- Every Album v1 **Release Package Plan** requires an **Album Sonic System** and an **Album Visual System**, even when either system is intentionally minimal.
- **Album Calibration** happens after representative calibration Sound and Image Medium Plans exist and before full expansion of remaining track Sound Prompt Plans, album cover, Track Covers, title, and description.
- **Album Calibration** approves or rejects direction only; final Output Artifacts still require their normal Prompt Lock, Generation Approval, Output Critic Review, and Output Acceptance gates.
- **Album Calibration** is one checkpoint by default, with **Album Calibration Subchecks** for sonic direction, visual direction, and sound-visual fit.
- **Album Calibration Subchecks** may be approved or revised independently; expansion may continue only for deliverables whose relevant subchecks are approved.
- Track Cover expansion requires approved visual direction and approved sound-visual fit.
- Album v1 uses a pre-calibration package review to confirm the Release Package Plan is coherent enough to test, and a post-calibration package review to confirm the calibrated direction is strong enough to expand.
- The artist must approve the Release Package Plan's Album Cohesion Mode, deliverables, Album Sonic System, Album Visual System, Calibration Track, and calibration visual target before calibration Medium Plans are created.
- Album v1 provider-backed generation approval may be per output or per enumerated batch, but must name the exact outputs, provider, model or tool, and cost-bearing scope.
- Album v1 uses individual Output Records for concrete audio, cover, and text artifacts; a package-level Output Record is deferred until an export or publishing workflow creates a concrete package artifact.
- The **Calibration Track** should be the track that best tests album identity, prioritizing strongest Key Emotional Movement, representative Album Sonic System traits, or collection-level release identity unless the artist overrides.
- **Album Calibration** uses the **Calibration Track Cover** by default; when the album cover is the main visual anchor and Track Covers are secondary variants, calibration may include the album cover plus a lightweight Track Cover direction.
- Album v1 production order is album-level Artist Meaning, Album Cohesion Mode, Album Beat Plan, foundation Long-Work Stewardship when activated, album package plan, pre-calibration Mixed-Media Critic Review, Release Package Plan Approval, representative calibration Sound and Image Medium Plans, Album Calibration, remaining track Sound Prompt Plans, album cover and Track Covers, title and description, then post-calibration package-level review.
- Album v1 uses **Mixed-Media Critic Review** with album-specific criteria rather than a separate Album Critic role.
- A **Release Package Plan** is created after the Album Beat Plan and before medium-specific Medium Plans; it starts with placeholder deliverables and is enriched with Medium Plan references as they are created.
- A **Release Package** becomes a **Cumulative Work** when its parts depend on sequence, emotional arc, continuity, or approved part-to-part relationships.
- A **Creative Brief** can be represented as a **Creative Brief Document** and a **Creative Brief Record**.
- A **Creative Brief Document** requires **Brief Approval** before producing the **Creative Brief Record**.
- **Rough Brief Approval** permits producing a **Creative Brief Record** while preserving uncertainty notes.
- **Interpretive Confidence** and **Open Questions** guide review, but final Prompt Plans and Text Generation Plans should not preserve unresolved ambiguity.
- **Art Critic Review** or **Writing Critic Review** resolves **Open Questions** before final Prompt Plan or Text Generation Plan creation.
- **Art Critic Review** may deepen and emphasize existing findings when the artist gives no additional feedback, but it cannot override **Artist Meaning**.
- The First Slice runs **Art Critic Review** after the draft **Creative Brief Document** and before **Brief Approval**.
- **Art Critic Review** is mandatory in the First Slice.
- **Art Critic Review** applies **Critical Heuristics** in this order: preserve **Artist Meaning**, stay anchored to **Reference** evidence, deepen salient **Core Tension Pairs**, strengthen **Active Visual Tensions**, increase **Poetic Density**, use medium-specific translation principles, then apply art-critical rules such as avoiding literalism, preserving contradiction, making form carry meaning, and preferring layered specificity over generic mood.
- A **Creative Brief** compiles approved upstream records into a medium-specific handoff; it does not own **Artist Meaning**, **Beat Plan**, or **Medium Plan**.
- **Style Direction** defines the artistic language of the generated work and must serve **Artist Meaning**.
- **Style Direction** is chosen after the first pass of **Artist Meaning**, **Emotional Structure**, **Beat Plan**, and **Symbology Direction**, and before **Art Critic Review**.
- **Style Direction** can be hybrid, but it must have one **Primary Style** and bounded **Style Modifiers**.
- **Style Priority** makes **Style Direction** the last priority after **Artist Meaning**, **Emotional Structure**, **Beat Plan**, and **Visual Dynamics**.
- A **Style/Visual Conflict** must be surfaced to the artist instead of silently letting style override **Visual Dynamics**.
- A **Style/Visual Conflict** can produce **Style Adaptation**, where the chosen style is modified to preserve the **Target Visual Engine**.
- **Style Conflict Fields** preserve **Style/Visual Conflicts** and proposed **Style Adaptations** in the **Creative Brief Record**.
- **Art Critic Review** may propose a default **Style Adaptation** and only ask for explicit approval when it materially changes the named style.
- **Style Interview** first asks whether the artist has a specific visual vision or wants to explore what art style to use when the artist has not named a specific style.
- **Symbology Gate** comes before **Style Gate** by default because symbolic representation is closer to **Artist Meaning** than art style.
- **Symbology Board** compares six concise symbolic options, asks for artist selection, and asks whether the work should become a single image, compressed arc, or image series before style is locked.
- For visual media, **Medium Output Shape Recommendation** should happen after **Symbology Direction** and before **Style Direction** so symbolic representation can inform compression or expansion before visual style hardens.
- For text, **Text Medium Plan** should produce **Medium Output Shape Recommendation** before locking **Primary Text Form** so story movement drives form choice.
- For sound, **Medium Output Shape Recommendation** chooses the sound form family and scale, while **Arrangement / Form Direction**, **Song Structure**, **Section Function**, and **Section Tension Map** own the detailed time structure.
- **Style Interview** is adaptive, with **Style Interview Fallback Order** used when the Reference and **Artist Meaning** do not already narrow the next question.
- **Style Interview** stops early when **Style Interview Stop Condition** is met.
- **Style Interview** produces a **Style Recommendation** for artist confirmation.
- When **Style Direction** is unresolved, show six concise suggested styles and ask whether the artist wants one of them, something else, or visualization.
- **Style Recommendation** can proceed into **Art Critic Review** unconfirmed if **Style Confirmation Status** records that state.
- **Brief Approval** is the hard approval gate for final **Style Direction** in the First Slice.
- **Brief Approval** confirms **Style Direction** unless the artist explicitly excludes style from approval.
- A direct artist-specified style skips the full **Style Interview** unless a **Style Clarifier** is needed.
- **Wondermint Category Reference** can seed **Style Direction** vocabulary, but Wondermint upload subcategories must remain exact when used for Wondermint uploads.
- Wondermint subcategories are useful mapping metadata, but required only when preparing Wondermint uploads.
- **Visual Dynamics** contains **Active Visual Tensions** chosen from the **Core Visual Tension Pairs** library.
- The First Slice outputs only **Active Visual Tensions** rather than all **Core Visual Tension Pairs**.
- A **Series Amplitude Plan** gives each suggested series image 0-1 values for framing distance, subject scale, visual density, motion energy, spatial openness, detail intensity, and emotional pressure.
- In an image series, adjacent image roles should usually differ on at least two **Series Amplitude Plan** dimensions unless visual sameness is intentional and traced to the **Emotional Arc**.
- In text-to-image work, **Visual Dynamics** describes the **Target Visual Engine**, not literal visual properties of the text.
- Every **Target Visual Engine** choice must trace back to **Artist Meaning**, **Reference** evidence, **Emotional Structure**, **Beat Plan**, or **Critical Heuristics**.
- **Monumental / Intimate** is a **Conditional Visual Tension Pair** for scale, embodiment, installation, performance, and immersive work.
- **Emotional Structure** contains **Core Tension Pairs**, **Emotional Qualities**, an **Emotional Arc**, and **Emotional Payloads**.
- A **Story Structure** is selected or adapted during **Story Journey** to help shape the **Beat Plan**.
- A **Story Structure** guides movement, but it does not override **Artist Meaning**, replace **Reference** evidence, or decide output shape directly.
- The **Story Structure Library** provides reusable Story Structures; a project uses an adapted Story Structure inside its **Beat Plan** rather than applying a generic template unchanged.
- The first implementation should store the selected **Adapted Story Structure** inside the **Beat Plan**, not as a separate story-authority record.
- **Story Structure Library Entry** medium affinities are recommendations, not constraints; they guide compression and expansion tradeoffs without forbidding an artist-chosen medium.
- **Story Structure Library** should be grounded in recognized story and narrative theory over time, not only internally invented movement patterns.
- Every **Story Structure Library Entry** and **Cultural Format Structure Library Entry** should include **Structure Grounding** before it is treated as canonical; provisional entries must be marked as provisional until researched.
- **Structure Grounding Tier** should distinguish canonical frameworks, craft authority, platform-era pattern evidence, and artist-defined or project-specific structures.
- Research should inform **Story Structure Library Entries** and **Cultural Format Structure Library Entries**, but entries should stay concise and contain the operational structure itself rather than citations or source-reference lists.
- Library entries may include compact grounding metadata such as researched/provisional status and **Structure Grounding Tier**, but should not include citations or source-reference lists.
- **Cultural Format Structure Library** complements **Story Structure Library**: Story Structure owns deep movement, while Cultural Format Structure owns culturally recognized audience-facing form.
- Social-media patterns such as carousel lessons, threads, AMAs, launch posts, and hook-demo-payoff posts are **Cultural Format Structures** by default; only deeper movement patterns such as reveal loops, before/after transformation, or problem/reframe/return belong in the **Story Structure Library**.
- External social platform limits such as Instagram, TikTok, YouTube, LinkedIn, Reddit, Substack, or X character counts, durations, API limits, and publishing restrictions are not first-class Artist OS validation rules; Wondermint upload requirements are the platform-specific exception.
- A project can combine one adapted **Story Structure** with one or more adapted **Cultural Format Structures** when a medium form has established expectations.
- **Cultural Format Structure** is selected or adapted during **Medium Plan** creation, not during **Story Journey**.
- **Medium Plans** produce a **Medium Output Shape Recommendation** from the approved **Beat Plan** and adapted **Story Structure**; the **Story Structure Library** does not choose the number of outputs.
- Every **Text Medium Plan** must include a **Medium Output Shape Recommendation**, even when the recommended shape is obvious or compact; image and sound plans may include the same recommendation object as optional rationale, while video and mixed-media adoption remain follow-up decisions.
- When the artist-requested output shape and the **Medium Output Shape Recommendation** materially diverge, record a **Medium Output Shape Conflict** and resolve it with one **Decision Interview** question before locking the **Text Medium Plan**.
- Select or adapt **Cultural Format Structure** after the **Medium Output Shape Recommendation** is accepted, revised, or explicitly allowed to proceed unconfirmed.
- Each adapted **Cultural Format Structure** must include a **Cultural Format Adaptation Policy** so recognizable form can be preserved, merged, omitted, or inverted without becoming a rigid formula.
- **Adapted Cultural Format Structure** parts map to Medium Plan sections, scenes, movements, or other parts; they do not replace the Medium Plan's execution structure.
- Every **Cultural Format Structure** must define **Audience Hook** logic for its format, but the hook does not have to be a headline, first sentence, or clickbait device.
- **Cultural Format Structure Library Entries** may recommend **Stewardship Views** for long or complex works, but those views remain projections over **Medium Plan** and **Long-Work Stewardship** state.
- Adapted **Story Structure** is required in the **Beat Plan** when `story_mode` is `beat_pair`, `three_part_sequence`, `sequence`, `scene`, `arc`, or `world`; it remains optional for `single_beat`.
- **Medium Output Shape Recommendation** is required in the **Text Medium Plan** and optional in the **Image Medium Plan** and **Sound Medium Plan**. In image work, it explains the choice among `single_image`, `compressed_arc`, and `image_series`; `presentation_mode` remains the accepted concrete image shape consumed downstream. In sound work, it explains the choice among sound-specific work types or `sound_sequence`; `sound_work_type`, `arrangement_direction`, and `sequence_plan` remain the concrete sound-planning fields.
- Image-specific **Series Recommendation** language should narrow toward **Medium Output Shape Recommendation** when the recommendation includes single compressed image, image series, video, or other visual forms.
- **Poetic Density** increases when a single element carries multiple meanings without collapsing them into one message.
- **Poetic Density Notes** capture **Poetic Density** without reducing it to a numeric score.
- **Core Tension Pairs** exist to support creative translation across media.
- A **Tension Pair** is stored as a **Tension Pair Record** in a **Creative Brief Record**.
- Every **Creative Brief Record** includes all eight **Core Tension Pairs**, each with **Tension Pair Salience**.
- A **Tension Pair Record** can describe either a **Core Tension Pair** or an **Active Visual Tension**.
- A **Beat Plan** contains one or more **Beats** or **Tension Points**.
- A **Beat** carries one **Emotional Payload**.
- A **Tension Point** carries one **Emotional Payload** without requiring before/after change.
- A **Series Recommendation** is required when a **Beat Plan** has more than one meaningful **Beat** or **Tension Point**.
- A **Series Recommendation** can still choose single image when compression preserves the work better than sequence.
- A **Three-Part Sequence** fits a clear three-part emotional structure such as before/threshold/after, invitation/rupture/consequence, or concealment/revelation/aftermath, but it does not decide image count.
- An **Image Series** fits any approved multi-image output, including exactly three images.
- A **Cumulative Work** needs long-work stewardship because later parts depend on prior parts or on an approved emotional arc.
- A portfolio, collection, curator batch, or store set is not automatically a **Cumulative Work** when the outputs are related but non-sequential.
- **Long-Work Stewardship** applies to **Cumulative Work**.
- **Collection Coherence Review** applies to related non-sequential sets without imposing **Long-Work Stewardship**.
- **Long-Work Stewardship** is schema-backed by a **Long-Work Stewardship Record**.
- **Collection Coherence Review** stays review behavior for now and should not get a separate schema until collection-level acceptance, store readiness, or batch-level promotion creates a real need.
- **Long-Work Stewardship** owns part-to-part integrity: assigned Beat Roles, approved order, emotional arc legibility, continuity rules, checkpoint readiness, and whether a proposed change must return to **Story Approval**.
- **Long-Work Stewardship** does not own **Artist Meaning**, **Core Tension Pairs**, **Beat Plan** authority, **Medium Plan** authority, or final acceptance.
- A **Long-Work Stewardship Record** references the governing **Beat Plan** rather than duplicating it.
- A **Long-Work Stewardship Record** is centered on one planned part per cumulative unit, such as an image role, text section, chapter, song section, video scene, or mixed-media movement.
- Plot-tracker-style templates are views over **Medium Plan** structure and **Long-Work Stewardship** execution state, not separate story-authority or tracking records.
- A **Stewardship View** may present plot tracker, act tracker, chapter tracker, open-thread, or character continuity information, but the authoritative state remains in **Medium Plan** and **Long-Work Stewardship** records.
- Subplots, open threads, and character-brief needs should first map to **Medium Plan** part structure, **Long-Work Continuity Rules**, **Proposed Continuity Updates**, or **Long-Work Checkpoints** before adding new records.
- Add a specialized continuity companion record only when repeated projects prove that **Long-Work Continuity Rules** cannot carry the needed subplot, thread, character, setting, or world continuity clearly.
- An **Artist OS Project** may have multiple **Long-Work Stewardship Records**, but each **Long-Work Stewardship Record** governs one **Cumulative Work**.
- A **Long-Work Stewardship Record** is updated in place for execution progress, but a governing Artist Meaning, Beat Plan, or Medium Plan change that alters cumulative structure creates a superseding stewardship record.
- A **Long-Work Part** is not a **Prompt Variant Plan** or **Variant**; prompt variants test directions, while Long-Work Parts carry cumulative story or emotional structure.
- A **Long-Work Part** stores generic stewardship state plus a reference to its medium-specific part; it does not duplicate Shot Design, amplitude profiles, section execution details, voice rules, or other Medium Plan-owned fields.
- A **Single-Generation Variant Comparison** does not create Long-Work Parts unless it represents an approved image series rather than a Minimal/Faithful/Amplified comparison.
- Create the **Long-Work Stewardship Record** after **Story Approval**, then enrich it after the **Medium Plan** maps approved Beats into medium-specific parts.
- For **Cumulative Work**, the route is Story Approval, then **Long-Work Stewardship Record** creation, then Medium Plan, then stewardship enrichment with Long-Work Parts, then Long-Work Readiness before expansion.
- **Long-Work Readiness** can block expansion when the state is pending or repair before expansion; expansion may continue only after readiness runs, repair happens, or the artist explicitly waives the block.
- **Long-Work Readiness** should use bands, not numeric quality scores.
- **Long-Work Readiness** checks story authority, part mapping, part job clarity, Expectation Turn preservation, emotional arc movement, premature resolution, continuity rules, checkpoint plan, open risks, and waiver path.
- **Long-Work Checkpoints** may be foundation, medium mapping, calibration, first part, interval, pre-completion, or completion checkpoints.
- A **Long-Work Stewardship Record** supports all checkpoint types, but only the checkpoints relevant to the medium, size, and risk of the Cumulative Work are required.
- A **Long-Work Checkpoint** decision is recorded as a **Gate Decision** and summarized in the **Long-Work Stewardship Record** for resume state.
- **Long-Work Reviewer** returns a **Review Record** for readiness, checkpoints, cumulative drift, and proposed continuity updates.
- **Long-Work Continuity Rules** are first-class objects in the **Long-Work Stewardship Record**.
- Changing a **Long-Work Continuity Rule** requires artist confirmation, Story Approval, Medium Plan approval, or prompt revision according to the rule's authority level.
- Output discoveries become **Proposed Continuity Updates** first; they become active **Long-Work Continuity Rules** only after the required artist confirmation or approval gate.
- A **Proposed Continuity Update** that changes meaning or story movement must return to **Story Approval** before becoming active.
- Artist-approved repetition, stillness, or reduced movement should become an explicit **Long-Work Continuity Rule** when it is meaning-bearing; use waiver only when the artist accepts a risk without changing the governing intent.
- For image series, the **Series Plan** remains the image-medium plan for what images should exist and how they visually translate the Beat Plan.
- For image series, the **Long-Work Stewardship Record** references Image Role ids and tracks cumulative execution state; it does not duplicate Shot Design, amplitude, or visual-tension details owned by the Image Medium Plan or Creative Brief.
- For long text, the **Text Medium Plan** owns text form, voice, point of view, structure, fidelity, publication use, and section jobs.
- For long text, the **Text Generation Plan** owns drafting instructions and editorial pass policy.
- For long text, the **Long-Work Stewardship Record** references text section, chapter, scene, or movement ids and tracks cumulative progress, checkpoints, arc integrity, voice drift, fidelity drift, and whether editorial passes changed protected structure.
- The first **Long-Work Stewardship** implementation should cover both image series and long text.
- The first long-text **Long-Work Stewardship** scope covers cumulative text sections, chapters, scenes, and poem movements; scripts, lyric cycles, and treatments can use those part kinds until a real specialized need appears.
- First-pass long-text readiness checks part mapping, distinct section jobs, emotional arc movement or intentional holding, premature resolution, voice continuity, fidelity continuity, and first-part checkpoint needs.
- A **Series Plan** requires artist approval before Artist OS produces multiple image Prompt Plans.
- An approved **Series Plan** starts with one **Series Calibration Image** before producing the rest of the series.
- The **Series Calibration Image** should use the **Calibration Image Role**, not automatically the first sequential Beat.
- The **Series Calibration Image** uses three calibration **Prompt Variant Plans** to lock visual language.
- After calibration approval, remaining series images get one prompt per **Image Role** by default.
- **Calibration Choice** updates the **Creative Brief Record** or **Series Plan** with accepted style traits, rejected style traits, locked visual rules, and notes for remaining images.
- **Calibration Choice** can update visual language, **Style Direction**, **Visual Dynamics** translation notes, locked visual rules, and series continuity rules.
- **Calibration Choice** cannot update **Artist Meaning**, **Core Tension Pairs**, or **Beat Plan** unless the artist explicitly says the calibration revealed a better meaning.
- A **Symbology Board** gives the artist human input before style and prompt locking by comparing six symbolic or compositional branches with concise option labels.
- A **Prompt Variant Plan** explores one approved image direction; a **Series Plan** creates multiple related images with distinct **Image Roles**.
- A **Prompt Branch Set** explores multiple meaning-equivalent prompt branches from one approved **Prompt Plan** for curator selection; it does not create **Variants** until provider-backed generation is explicitly approved.
- A requested image portfolio or collection routes toward **Prompt Branch Set** by default, while a requested ordered image story routes toward **Series Recommendation** or **Series Plan**.
- A draft **Prompt Branch Set** may be created without review, but an **Actionable Prompt Branch Set** requires **Prompt Critic Review** before generation or serious curator selection.
- A **Prompt Branch Set** remains a child of one approved **Prompt Plan**. A selected prompt branch can become a new **Prompt Plan** only after artist selection or direction approval.
- Every branch in a **Prompt Branch Set** preserves the same **Beat Plan**. If a branch changes the story movement, return to **Story Gate** or create a separate journey.
- A generated result from a prompt branch becomes taste memory, calibration context, or a promoted direction only after explicit artist confirmation.
- In the single-image First Slice, three **Prompt Variant Plans** should preserve the approved **Symbology Direction** and **Style Direction**, then vary minimalist-to-maximalist intensity.
- **Prompt Variant Plan** labels stay Faithful, Amplified, and Minimal even when using **Variant Test Axis Labels**.
- A **Series Plan** may include **Style Progression** when the Reference warrants a changing visual language across Beats.
- The First Slice may include **Style Progression** inside **Series Recommendation**, but it becomes executable only after **Series Plan** approval.
- **Series Calibration Fields** live in **Series Recommendation** before the full **Calibration Choice** workflow exists.
- A **Transformation Brief** defines the current **Meaning-Preserving Transformation** for the typed pipeline.
- A **Meaning-Preserving Transformation** can produce one or more **Provider-Neutral Prompt Plans** or **Text Generation Plans**.
- A **Text Generation Plan** is the Text Journey's post-brief generation contract; it occupies the same pipeline position as a **Prompt Plan** but is not a provider prompt plan.
- The First Slice produces one **Provider-Neutral Prompt Plan** containing three **Prompt Variant Plans**: **Faithful Prompt Variant**, **Amplified Prompt Variant**, and **Minimal Prompt Variant**.
- Every **Prompt Variant Plan** must trace back to the same approved **Creative Brief**.
- The **Amplified Prompt Variant** may introduce **Derived Symbols** if each one is marked and traced to **Artist Meaning**, a **Core Tension Pair**, an **Active Visual Tension**, a **Beat** or **Tension Point**, or a **Poetic Density Note**.
- **Derived Symbol Review** happens inside review of the full **Provider-Neutral Prompt Plan** and does not require a separate approval gate in the First Slice.
- A **Dry Run** stops at **Prompt Plan** and critique criteria.
- **Provider-Backed Generation** uses configured API keys to turn a **Prompt Plan** into **Variants**.
- A **Provider Profile** enables **Provider-Backed Generation**.
- A **Provider Adapter** translates a **Provider-Neutral Prompt Plan** for a provider.
- The **Example Corpus** contains safe committed examples.
- The **Workspace Library** contains real artist work and is not committed by default.
- The **Wondermint Root** contains sibling visible and hidden folders so deleting the **Artist Library** does not delete the **Workspace Library**.
- The **Wondermint Root Setting** is the preferred user-facing way to choose storage; low-level Workspace Library overrides remain for development and tests.
- The **Artist Library** presents user-facing outputs and readable summaries for artists, while the **Workspace Library** preserves internal project state and provenance.
- The **Artist Library** may contain **Review Drafts**, but not internal schema records, gate decisions, event logs, or sidecar metadata.
- Artist OS creates **Artist Library** project folders lazily as user-facing files appear, not as empty mirrors of Workspace Library structure.
- The **Personal Library** presents reusable artist-facing guidance in the **Artist Library**, while evidence, promotion status, and resolver indexes live in the **Workspace Library**.
- Only artist-useful creative guidance should appear as visible **Personal Library** notes; technical, schema, process, and tooling learnings stay internal.
- The **Workspace Library** contains many **Artist OS Projects**.
- Each **Artist OS Project** has its own **Project Memory**.
- **Project Memory** must not cross project boundaries unless the artist explicitly imports, references, or reuses material from another Artist OS Project.
- A single **Artist OS Project** can contain many **Output Artifacts** when they share the same governing **Artist Meaning**, source **Reference**, audience/use, collection intent, and continuity rules.
- Use separate **Artist OS Projects** when the governing meaning, source Reference, audience/use, or creative goal changes enough that shared Project Memory would create drift.
- The **Artist OS Library Database** indexes the **Workspace Library** so agents can find old projects, prompts, image paths, and resume points.
- A **Missing Project** can be searched as historical context but cannot be resumed until its files are restored.
- A **Visible Missing Project** remains resumable from the **Workspace Library** and may have its **Artist Library** folder restored.
- Each project in the **Workspace Library** has a **Project Manifest** and image files use **Asset Metadata** sidecars.
- Each project folder in the **Artist Library** has a **Project Pointer** that links it to one **Artist OS Project**.
- A **Project Pointer** uses the **Artist OS Project** id as its authority; relative Workspace Library hints are convenience only.
- A **Project README** orients humans and agents to visible outputs, status, and resume instructions without replacing the **Project Manifest**.
- The **First Slice** transforms a text **Reference** into an image **Prompt Plan** through a **Dry Run**.
- A **Prompt Plan** can produce one or more **Variants**.
- A **Variant** is a **Generated Work**.
- The **Output Acceptance Gate** approves, rejects, requests revisions, archives, exports, or extends an **Output Artifact**.
- An **Accepted Work** is an **Output Artifact** approved through the **Output Acceptance Gate**.
- By default, **Output Critic Review** happens before the **Output Acceptance Gate**. The artist can explicitly accept or waive critic drift findings, and that waiver should be recorded.
- An **Output Artifact** has one **Output Record**.
- A **Generated Work** is one kind of **Output Artifact**; its **Output Record** is the durable metadata and provenance record.
- A user edit to a visible Artist Library file creates a **Human-Edited Output Revision** with a new **Output Record**, linked to the prior **Output Record**.
- The schema for output provenance should be named `output-record.schema.json`, not `generated-work.schema.json`, because it records any **Output Artifact** origin.
- When relevant, an **Output Record** includes provider, model, settings, seed, generation approval reference, and estimated or actual cost. The event log preserves chronology; the Output Record preserves artifact provenance.
- When an **Output Artifact** comes from a **Prompt Branch Set**, its **Output Record** references both the parent **Prompt Plan** and the exact prompt branch that produced it.
- **Output Record** tracks review and acceptance state, but it does not yet own taste-memory promotion, calibration promotion, or accepted-work promotion fields. Those may become separate records when the curation loop is implemented.
- Individual **Output Records** are sufficient until provider adapters or batch-generation workflows create a real need for an **Output Batch** record.
- **Feedback Log** preserves raw evidence; **Learning Review** classifies it into **Learning Candidates**, **Soft Learning**, or **Hard Learning**.
- Each **Artist OS Project** may keep its own **Feedback Log**, while the **Learning Index** finds repeated patterns across projects.
- **Soft Learning** may guide future recommendations, but **Hard Learning** carries stronger default authority.
- A **Learning Rule** stays compact; detailed feedback, analytics, and output comparisons remain separate evidence.
- **Hard Learning** can come from repeated feedback, strong analytics, explicit artist confirmation, or a concrete schema/tooling mismatch.
- Artist OS marks completed projects with unclassified feedback as **Pending Learning Review** and may process them at the start of a later project.
- Relevant **Soft Learning** applies by default with brief disclosure; relevant **Hard Learning** applies by default unless it conflicts with current Artist Meaning or approved plans.
- **Performance Signals** and artist feedback are equal evidence classes for learning, but neither automatically overrides the other.
- When **Performance Signals** conflict with artist feedback, Artist OS preserves both and asks whether the current project should prioritize personal expression, performance optimization, or a hybrid.

## Example dialogue

> **Dev:** "Are we adding this rule to Artist Generation or Artist OS?"
> **Domain expert:** "If it guides how we build the repo, it belongs to Artist Generation. If it defines how artists and agents use the system, it belongs to Artist OS."
>
> **Dev:** "If a user uploads a song to make an image from it, is the song an asset?"
> **Domain expert:** "No. The song is the **Reference**. The metadata entry about that song is the **Source Record**."
>
> **Dev:** "Is the emotional brief the whole thing we generate before the image prompt?"
> **Domain expert:** "No. Avoid that term. The full artifact is the **Creative Brief**; its emotional section is **Emotional Structure**."
>
> **Dev:** "The model made three images from the poem. Are those assets?"
> **Domain expert:** "Call them **Variants**. If the artist approves one, it becomes an **Accepted Work**. Each image has an **Output Record**."
>
> **Dev:** "The reference looks playful, but the artist says it represents grief. Which meaning wins?"
> **Domain expert:** "The **Artist Meaning** wins. The playful form becomes evidence or contrast, not the authority."
>
> **Dev:** "The passage is calm but tense, then turns from attachment to departure. Is that all one emotion?"
> **Domain expert:** "No. The tension belongs in **Core Tension Pairs**; the movement is the **Emotional Arc**; grief turning into resolve is the **Emotional Payload** of the Beat."
>
> **Dev:** "Where do phrases like 'holy but rotten' or 'domestic but threatening' go?"
> **Domain expert:** "Those are **Emotional Qualities**. The repeatable core model is **Core Tension Pairs**."
>
> **Dev:** "Are Core Tension Pairs trying to be a psychology model?"
> **Domain expert:** "No. They exist to support creative translation across media."
>
> **Dev:** "If something is both painful and pleasant, should we average that into neutral?"
> **Domain expert:** "No. Model it as a **Tension Pair** so both poles remain present and the contradiction can be translated."
>
> **Dev:** "Should the core include Pain/Pleasure or Valence/Arousal?"
> **Domain expert:** "No. Use the **Core Tension Pairs**. They are more art-native and translate across media without flattening the work into good/bad feeling."
>
> **Dev:** "Can we store Order/Chaos as one number?"
> **Domain expert:** "No. Use a **Tension Pair Record** with order presence, chaos presence, tension intensity, evidence, artist note, and translation notes."
>
> **Dev:** "Should we omit Safety/Threat if it barely matters?"
> **Domain expert:** "No. Include it with **Tension Pair Salience** set to not salient, so records stay comparable without inventing meaning."
>
> **Dev:** "Why preserve multiple meanings instead of simplifying the message?"
> **Domain expert:** "Because **Poetic Density** is the point: one element can carry several meanings at once, and Artist OS should preserve that layered meaning."
>
> **Dev:** "Should we score Poetic Density from 1 to 10?"
> **Domain expert:** "No. Use **Poetic Density Notes** to record layered meanings and flattening risks without fake precision."
>
> **Dev:** "A still image has a red square pressed against a blue field. Is that a story beat?"
> **Domain expert:** "Only if there is a meaningful change. Otherwise it is a **Tension Point** carrying emotional pressure."
>
> **Dev:** "A song feels lonely and mechanical. Should the generated image include instruments?"
> **Domain expert:** "Not by default. A **Meaning-Preserving Transformation** can preserve loneliness, repetition, and metallic texture without copying musical surface details."
>
> **Dev:** "Does the first version call an image model?"
> **Domain expert:** "No. The first version is a **Dry Run** that produces the **Creative Brief** and **Prompt Plan**. **Provider-Backed Generation** comes after setup supports API keys."
>
> **Dev:** "Where do API keys go?"
> **Domain expert:** "In local secret storage such as `.env` or tool-managed auth. The **Provider Profile** records which providers are enabled, not the secrets themselves."
>
> **Dev:** "What path are we building first?"
> **Domain expert:** "The **First Slice** is text Reference to image Prompt Plan. Do not add media ingestion or provider calls yet."
>
> **Dev:** "Should the agent grill every artist before doing anything?"
> **Domain expert:** "No. Start with a short **Meaning Interview**: one required meaning question, then adaptive follow-ups only when needed."
>
> **Dev:** "Should the Creative Brief be Markdown or JSON?"
> **Domain expert:** "Both. The **Creative Brief Document** is for artist review; the **Creative Brief Record** is for agent handoff. If they disagree, the artist-approved document wins."
>
> **Dev:** "Should we create the JSON record before the artist reviews the Markdown brief?"
> **Domain expert:** "No. First create the **Creative Brief Document**, get **Brief Approval**, then generate the **Creative Brief Record** from the approved document."
>
> **Dev:** "Does 'mostly right, but make it more tender' count as Brief Approval?"
> **Domain expert:** "No. Revise the **Creative Brief Document** and ask again. 'Proceed with rough brief' counts as **Rough Brief Approval**."
>
> **Dev:** "Should the final Prompt Plan include uncertainty?"
> **Domain expert:** "No. **Interpretive Confidence** and **Open Questions** are review handoff signals. The reviewer resolves them before final prompt planning."
>
> **Dev:** "If the artist gives no more feedback, can the reviewer fill gaps?"
> **Domain expert:** "Yes. **Art Critic Review** should use best practice to deepen existing findings and increase **Poetic Density**, but it cannot override **Artist Meaning**."
>
> **Dev:** "Does the artist approve the raw Creative Brief draft?"
> **Domain expert:** "No. First run **Art Critic Review**, revise the **Creative Brief Document**, then ask for **Brief Approval**."
>
> **Dev:** "Can we skip Art Critic Review if the draft looks strong?"
> **Domain expert:** "Not in the First Slice. **Art Critic Review** is mandatory until Artist OS has explicit quality criteria for a fast path."
>
> **Dev:** "What does best practice mean when Art Critic Review fills gaps?"
> **Domain expert:** "Use **Critical Heuristics**: protect **Artist Meaning**, stay with **Reference** evidence, deepen the salient tensions, increase **Poetic Density**, translate through the target medium, and avoid generic literalism."
>
> **Dev:** "Should visual construction be part of the same Core Tension Pairs?"
> **Domain expert:** "No. Keep **Visual Dynamics** separate. Emotional tensions describe felt charge; **Active Visual Tensions** describe the formal engine."
>
> **Dev:** "For text-to-image, is Visual Dynamics analyzing the text or designing the image?"
> **Domain expert:** "It designs the **Target Visual Engine** of the generated image, but every choice must trace back to the text, **Artist Meaning**, **Emotional Structure**, or **Critical Heuristics**."
>
> **Dev:** "How should Artist OS choose a style if the artist does not know category names?"
> **Domain expert:** "Use a short **Style Interview** with a **Style Decision Tree**. The **Wondermint Category Reference** can seed vocabulary, but **Style Direction** must serve the Creative Brief."
>
> **Dev:** "When should Style Direction be chosen?"
> **Domain expert:** "After the first pass of **Artist Meaning**, **Emotional Structure**, and **Beat Plan**, but before **Art Critic Review**."
>
> **Dev:** "If the artist says 'manga' or 'cinematic photoreal,' do we still run the Style Interview?"
> **Domain expert:** "No. Accept the named style. Ask only one **Style Clarifier** if the style is too broad or ambiguous."
>
> **Dev:** "Can Style Direction be hybrid?"
> **Domain expert:** "Yes, but use one **Primary Style** plus bounded **Style Modifiers**. Do not let styles pile up at equal weight."
>
> **Dev:** "Can Style Direction override Visual Dynamics?"
> **Domain expert:** "No. Treat style as the last priority. Surface a **Style/Visual Conflict** and use it as a chance for **Style Adaptation**."
>
> **Dev:** "Does every Style/Visual Conflict need a separate user decision?"
> **Domain expert:** "No. **Art Critic Review** can propose a default **Style Adaptation**. Ask only if it materially changes the named style."
>
> **Dev:** "Can style change across a series?"
> **Domain expert:** "Yes, if the Reference warrants it. Use **Style Progression** intentionally inside the **Series Plan**."
>
> **Dev:** "Can Style Progression appear before the artist approves series mode?"
> **Domain expert:** "Yes, as a **Series Recommendation** only. It becomes executable after **Series Plan** approval."
>
> **Dev:** "Does every multi-Beat Reference become a series?"
> **Domain expert:** "No. Always evaluate series potential, but recommend single image when compression is stronger."
>
> **Dev:** "When should an image series have exactly three images instead of more?"
> **Domain expert:** "Use three images when the approved Beat Plan has three necessary image roles. Still record the output as an **Image Series**, not as a separate image class."
>
> **Dev:** "If a Series Plan is approved, do we generate the whole series immediately?"
> **Domain expert:** "No. First generate one **Series Calibration Image** to lock Style Direction and the Target Visual Engine."
>
> **Dev:** "Which image role should be used for the Series Calibration Image?"
> **Domain expert:** "Use the **Calibration Image Role**: the image that best represents the series' visual engine and emotional tension, not automatically the first Beat."
>
> **Dev:** "Does Series Calibration use one prompt or three?"
> **Domain expert:** "Use three calibration **Prompt Variant Plans** for the **Series Calibration Image**. After approval, remaining series images get one prompt each."
>
> **Dev:** "Is the selected calibration variant just a generation preference?"
> **Domain expert:** "No. Record it as a **Calibration Choice** that updates the **Creative Brief Record** or **Series Plan**."
>
> **Dev:** "Can Calibration Choice change Artist Meaning or Emotional Structure?"
> **Domain expert:** "No, not by default. It updates visual language and continuity rules unless the artist explicitly revises meaning."
>
> **Dev:** "Should Series Calibration be represented in the schema now?"
> **Domain expert:** "Yes, add minimal **Series Calibration Fields** now. Save the full **Calibration Choice** schema for the later image-review workflow."
>
> **Dev:** "Should Style/Visual Conflicts be represented in the schema now?"
> **Domain expert:** "Yes, add compact **Style Conflict Fields** so agents preserve conflicts, proposed adaptations, and whether approval is required."
>
> **Dev:** "Are Wondermint subcategories required in every Creative Brief?"
> **Domain expert:** "No. They are useful mapping metadata, but required only when preparing Wondermint upload."
>
> **Dev:** "Should the Style Interview ask questions in fixed order?"
> **Domain expert:** "No. It should be adaptive, with **Style Interview Fallback Order** as the default when context does not narrow the next question."
>
> **Dev:** "Can Style Interview recommend a style before asking all fallback questions?"
> **Domain expert:** "Yes. Stop once **Primary Style**, bounded **Style Modifiers**, known conflicts, and alignment with **Artist Meaning** are clear."
>
> **Dev:** "Should Style Interview just record answers?"
> **Domain expert:** "No. Synthesize a **Style Recommendation** and ask the artist to use it, adjust it, or name a different style."
>
> **Dev:** "Does Style Recommendation need explicit confirmation before Art Critic Review?"
> **Domain expert:** "No. It can proceed unconfirmed if **Style Confirmation Status** records it. **Brief Approval** remains the hard gate."
>
> **Dev:** "Does Brief Approval automatically approve Style Direction?"
> **Domain expert:** "Yes, unless the artist explicitly excludes style from approval."
>
> **Dev:** "Are the three single-image prompt variants always Faithful, Amplified, and Minimal?"
> **Domain expert:** "They can also test **Variant Test Axes** when ambiguity remains, such as realism versus cartoon or literal versus symbolic."
>
> **Dev:** "Should testing an unresolved axis replace the Faithful, Amplified, and Minimal labels?"
> **Domain expert:** "No. Keep stable variant labels and add a **Variant Test Axis Label** to each prompt."
>
> **Dev:** "If the Reference has several Beats, should the output stay one image?"
> **Domain expert:** "Not always. Add a **Series Recommendation**. A **Series Plan** needs artist approval before generating multiple image prompt plans."
>
> **Dev:** "Should the Provider-Neutral Image Prompt Plan produce one prompt?"
> **Domain expert:** "No. In the First Slice, create three **Prompt Variant Plans** from the same approved **Creative Brief**: Faithful, Amplified, and Minimal."
>
> **Dev:** "Can the Amplified Prompt Variant add new symbols?"
> **Domain expert:** "Yes, but mark them as **Derived Symbols** and trace each one back to the approved **Creative Brief**."
>
> **Dev:** "Do Derived Symbols need separate artist approval?"
> **Domain expert:** "Not in the First Slice. Keep them visible for **Derived Symbol Review** inside the full **Provider-Neutral Prompt Plan** review."
>
> **Dev:** "Can a user drop real songs and generated images into the repo?"
> **Domain expert:** "Real artist work belongs in the **Workspace Library**, not the committed **Example Corpus**."
>
> **Dev:** "Should our first image prompt format assume OpenAI?"
> **Domain expert:** "No. Keep a **Provider-Neutral Prompt Plan** in the core and use a **Provider Adapter** to translate later."
>
> **Dev:** "The prettiest Variant misses the Artist Meaning. Should we accept it?"
> **Domain expert:** "No. **Output Acceptance Gate** decides whether the **Output Artifact** preserves the approved meaning and upstream plan, not whether it is merely beautiful."

## Flagged ambiguities

- "artist repository", "artist operating system", "artist OS", "plugin", and "skill collection" were used interchangeably. Resolved: **Artist Generation** is the repository/project, **Artist OS** is the product, **Skill** is a workflow, and **Plugin** is the later packaged form.
- "source", "source object", "reference", "creative input", and "input" were used for the same user-provided material. Resolved: the artist-facing term is **Reference**; the stored metadata is a **Source Record**.
- "emotional brief", "creative brief", "formal analysis", "beat map", "transformation plan", and "prompt plan" were overlapping. Resolved: **Creative Brief** is the umbrella artifact; the others are named components or downstream generation-facing plans. **Emotional Brief** is retired; use **Emotional Structure** for the emotional section.
- "asset", "generated asset", "output", "artifact", and "digital asset" were ambiguous. Resolved: use **Output Artifact** for concrete reviewable outputs, **Generated Work** for created media, **Variant** for one generated option, **Accepted Work** for artist-approved media, and **Output Record** for metadata.
- "meaning", "intent", and "vibe" were too broad. Resolved: **Artist Meaning** is the artist's stated interpretation and has final authority over agent interpretation.
- "emotional components", "emotional structure", "vibe", "order and chaos", and "emotion" were overlapping. Resolved: **Emotional Structure** is the umbrella, with **Core Tension Pairs**, **Emotional Qualities**, **Emotional Arc**, and **Emotional Payload** as parts.
- The emotional model needs both repeatable structure and artist-specific language. Resolved: **Core Tension Pairs** are fixed; **Emotional Qualities** are freeform descriptors.
- **Core Tension Pairs** should be chosen for creative translation, not pure psychological classification.
- Bipolar sliders would collapse productive contradictions. Resolved: use **Tension Pairs**, where both poles can be present at once.
- The first **Core Tension Pairs** are locked as Attraction/Repulsion, Proximity/Distance, Order/Chaos, Stillness/Motion, Legibility/Opacity, Control/Surrender, Safety/Threat, and Presence/Absence.
- Pain/Pleasure, Valence/Arousal, Familiar/Strange, Sacred/Profane, Human/Nonhuman, Natural/Artificial, and Freedom/Constraint are not in the first core set. Some may appear later as derived metadata, Emotional Qualities, or domain-specific extensions.
- **Tension Pair Records** store each pole independently and include `tension_intensity`, evidence, optional artist note, and translation notes. `tension_intensity` is not mechanically derived from pole values.
- Every Creative Brief Record includes all eight Core Tension Pairs. Use **Tension Pair Salience** to mark weak or irrelevant pairs rather than omitting them.
- **Poetic Density** explains why Artist OS preserves layered and even contradictory meanings instead of reducing a Reference to one message.
- **Poetic Density** should be reviewed qualitatively through **Poetic Density Notes**, not numerically scored in v1.
- "story beat" risked implying literal plot. Resolved: **Beat** is a change-unit; **Tension Point** covers meaningful emotional pressure without before/after change.
- "transformation" could mean format conversion, style transfer, or literal copying. Resolved: **Meaning-Preserving Transformation** is the core model and does not preserve surface form by default.
- "generation" was ambiguous between prompt planning and paid provider calls. Resolved: v1 is **Dry Run** only; later **Provider-Backed Generation** should work after the user configures API keys.
- "API key setup" could imply committing secrets. Resolved: **Provider Profile** is local uncommitted provider configuration; secrets stay in `.env` or tool-managed auth and never in committed artifacts.
- "first workflow" was broad. Resolved: the **First Slice** is Text Reference to Image Prompt Plan.
- "grill me" described the tone but not the product concept. Resolved: **Meaning Interview** is the product term; default behavior is one required Artist Meaning question with adaptive follow-ups.
- "Creative Brief" could mean artist-readable prose or machine-readable data. Resolved: **Creative Brief Document** is Markdown; **Creative Brief Record** is JSON.
- First Slice creates the **Creative Brief Document** first. After **Brief Approval**, Artist OS creates the **Creative Brief Record**.
- **Brief Approval** requires explicit approval or proceed language. If the artist says to proceed despite uncertainty, record **Rough Brief Approval**.
- Uncertainty is allowed as a review handoff, not as a final state. **Interpretive Confidence** and **Open Questions** must be resolved before final Prompt Plans.
- **Art Critic Review** is the reviewer stage for Artist OS. It makes the Creative Brief more robust, layered, and decisive before prompt planning.
- In the First Slice, **Art Critic Review** is mandatory and runs before **Brief Approval**.
- **Critical Heuristics** are the explicit best-practice rules used by **Art Critic Review** when artist feedback leaves gaps.
- **Visual Dynamics** is a second interpretive layer beside **Emotional Structure**. The First Slice uses a library of 14 **Core Visual Tension Pairs** but records only **Active Visual Tensions**.
- **Style Direction** is a separate layer from **Emotional Structure** and **Visual Dynamics**.
- **Style Direction** is selected after the first meaning/emotional/beat/symbology pass and before **Art Critic Review**.
- Hybrid style is allowed only as one **Primary Style** plus bounded **Style Modifiers**.
- **Style Direction** is the last priority. It must not override **Artist Meaning**, **Emotional Structure**, **Beat Plan**, or **Visual Dynamics**.
- **Style/Visual Conflicts** should be shown to the artist and can become **Style Adaptations**.
- **Art Critic Review** may propose default **Style Adaptations** and only ask for explicit approval when the named style materially changes.
- The shared artist-facing visual gate order is **Symbology Gate** then **Style Gate**; later visual variation belongs to **Prompt Variant Strategy**.
- **Video Critic Review** is the integrated time-based review for video; it can use Art, Writing, or Sound review criteria as supporting checks without replacing their source records.
- Use a **Style Interview** and **Style Decision Tree** when the artist has not specified style directly.
- **Style Interview** is adaptive, using **Style Interview Fallback Order** only as the default.
- **Style Interview** can stop early when the stop condition is met.
- **Style Interview** should synthesize a **Style Recommendation** for confirmation.
- **Style Recommendation** can enter **Art Critic Review** unconfirmed; **Brief Approval** confirms final style.
- **Brief Approval** confirms **Style Direction** unless style is explicitly excluded.
- If the artist specifies style directly, skip the full **Style Interview** and ask at most one **Style Clarifier** if needed.
- The **Wondermint Category Reference** seeds style/category vocabulary but does not replace Artist OS art ontology.
- `wondermint_subcategories` are optional Artist OS metadata unless preparing a Wondermint upload.
- For text-to-image, **Visual Dynamics** describes the **Target Visual Engine** rather than literal visual qualities in the text.
- **Monumental / Intimate** is conditional for scale, embodiment, installation, performance, and immersive environments.
- The First Slice's **Provider-Neutral Prompt Plan** contains three **Prompt Variant Plans**: Faithful, Amplified, and Minimal.
- The **Amplified Prompt Variant** can add **Derived Symbols**, but they must be marked and justified through Creative Brief traceability.
- **Derived Symbol Review** is part of reviewing the full Prompt Plan; it is not a separate First Slice approval gate.
- If a Reference has multiple significant Beats, Artist OS should include a **Series Recommendation** for single image or image series. Do not create multiple image prompt plans until the artist approves a **Series Plan**.
- Multi-Beat References do not automatically become series. The recommendation can be single image when compression is more powerful.
- A **Series Plan** can use **Style Progression** when the Beat Plan supports a meaningful shift in visual language across images.
- **Style Progression** can be recommended in the First Slice, but not executed until **Series Plan** approval.
- An approved **Series Plan** must produce one **Series Calibration Image** first, then use artist feedback to lock the series direction before producing remaining image prompts or images.
- The **Series Calibration Image** should use the most representative **Calibration Image Role**, often the threshold or central image.
- **Series Calibration Image** uses three prompt variants. Remaining approved series images use one prompt per **Image Role** by default.
- **Calibration Choice** is durable project context for the remaining series, not a temporary preference.
- **Calibration Choice** does not rewrite **Artist Meaning**, **Core Tension Pairs**, or **Beat Plan** without explicit artist direction.
- Add minimal **Series Calibration Fields** to the Creative Brief Record now; defer full **Calibration Choice** schema until image review exists.
- Add compact **Style Conflict Fields** to the Creative Brief Record now.
- Three single-image **Prompt Variant Plans** may test unresolved **Variant Test Axes** instead of only varying intensity.
- Do not add another visual gate before locking Prompt Variant Plans; use **Prompt Variant Strategy** to choose meaningful variation axes.
- Keep **Prompt Variant Plan** labels stable. Use **Variant Test Axis Labels** to explain what each variant tests.
- Each **Prompt Variant Plan** must name concrete **Variant Differentiators** so the three prompts produce meaningfully different visual options.
- Use a **Single-Generation Variant Comparison** only when the artist wants multiple Prompt Variant Plans compared in one generated image.
- Store image arrangement decisions in the Prompt Plan's **Layout Plan**.
- "examples" and real user work needed separate storage. Resolved: **Example Corpus** is committed and safe to share; **Workspace Library** is local and uncommitted, with an **Artist OS Library Database**, a **Project Manifest** per project, and **Asset Metadata** sidecars for images and exports.
- Provider setup risked locking the domain model to one API. Resolved: Artist OS keeps a provider-neutral core and uses **Provider Adapters** for specific media providers.
- "accepted" needed a boundary. Resolved: an **Output Artifact** becomes an **Accepted Work** only through the **Output Acceptance Gate**.
- First Video Medium Plan validation uses a compact fixture while preserving scale-general fields and reroute triggers for long-form video.
- The conductor exposes Video routing through a minimal video skill that owns the Video Medium Plan process, gates, review boundary, outputs, and provider boundary.
- The first video skill is named `video-journey`; v0 may only produce storyboard-ready Video Medium Plans, but the skill owns the expandable video path.
