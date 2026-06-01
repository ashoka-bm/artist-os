# Artist Generation

Artist Generation is the project and repository that builds Artist OS. This context defines the domain language for the artist-facing operating system and keeps build-process terms separate from product terms.

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

**Meaning Interview**:
The short artist-facing interview that captures Artist Meaning and transformation constraints before analysis and planning.
_Avoid_: Grill me, interrogation

**Creative Brief**:
The structured interpretation of a Reference before generation, combining Artist Meaning, Formal Analysis, Emotional Structure, Beat Map, and Transformation Plan.
_Avoid_: Emotional brief when referring to the full artifact

**Creative Brief Document**:
The artist-readable Markdown version of a Creative Brief.
_Avoid_: Creative Brief Record

**Creative Brief Record**:
The structured JSON version of a Creative Brief for agent handoff and validation.
_Avoid_: Creative Brief Document

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
An unresolved interpretive gap that must be resolved before the final Prompt Plan.
_Avoid_: Final prompt ambiguity

**Art Critic Review**:
A reviewer stage that strengthens the Creative Brief by resolving weak interpretations, increasing Poetic Density, and turning low-confidence notes into decisive artistic direction.
_Avoid_: Critique Asset, Acceptance Review

**Critical Heuristics**:
Reusable art-critical rules that Art Critic Review uses to deepen a Creative Brief without inventing new Artist Meaning.
_Avoid_: Generic best practices, taste, model preference

**Formal Analysis**:
The observable properties of a Reference.
_Avoid_: Emotional analysis

**Visual Dynamics**:
The formal forces that make a visual work active, coherent, tense, immersive, unstable, or memorable.
_Avoid_: Technicality, visual style only

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

**Style Priority**:
The rule that Style Direction is subordinate to Artist Meaning, Emotional Structure, Beat Map, and Visual Dynamics.
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

**Symbology Gate**:
The first visual choice gate after Artist Meaning, where the artist decides how the work should be symbolically represented and whether the work should become a single image, emotional arc, or multi-image presentation.
_Avoid_: Hiding symbolic representation inside final prompt variants

**Symbology Board**:
One internal comparison-board prompt for six symbolic representations of the same Artist Meaning and Creative Brief. At the gate, the artist sees concise symbolic option labels first; the full prompt stays internal unless requested.
_Avoid_: Showing the full image prompt by default or choosing style before symbolic representation

**Style Gate**:
The second visual choice gate, where the artist chooses the artistic language for the selected Symbology Direction.
_Avoid_: Style overriding symbolic meaning

**Minimalist-to-Maximalist Gate**:
The third visual choice gate, where the artist compares Minimal, Faithful/Balanced, and Amplified/Maximal intensity after symbology and style are selected.
_Avoid_: Reopening symbology or style unless the artist asks

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
The dry-run workflow that transforms a text Reference into a Suno Sound Prompt Plan for the first sound version.
_Avoid_: Provider-backed music generation

**Suno Sound Prompt Plan**:
A Prompt Plan expressed as Artist OS traceable sound concepts plus Suno Custom Mode outputs.
_Avoid_: Cross-platform provider abstraction in the first sound version

**Derived Sonic Element**:
A new motif, sound, instrument, texture, hook, lyric image, or production gesture introduced by a Prompt Variant Plan because it strengthens approved Artist Meaning, Sonic Dynamics, Beat Map, or Poetic Density.
_Avoid_: Unmarked invention

**Core Visual Tension Pairs**:
The standard Visual Dynamics library: Light/Dark, Saturated/Muted, Warm/Cool, Harmonious/Discordant, Dense/Sparse, Geometric/Organic, Sharp/Diffuse, Linear/Painterly, Textured/Smooth, Representational/Non-Representational, Flat/Deep, Balanced/Unbalanced, Centered/Decentered, and Singular/Repetitive.
_Avoid_: Color labels, composition tags

**Active Visual Tensions**:
The selected Core Visual Tension Pairs that materially shape a specific Creative Brief.
_Avoid_: Scoring every visual pair by default in the First Slice

**Series Amplitude Plan**:
The internal 0-1 visual amplitude profile for each suggested image in a triptych or image series, covering framing distance, subject scale, visual density, motion energy, spatial openness, detail intensity, and emotional pressure.
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
_Avoid_: Beat Map

**Emotional Payload**:
The felt meaning carried by one Beat.
_Avoid_: Emotion, vibe

**Beat**:
The smallest meaningful change, contrast, turn, or pressure point in a Reference that carries Emotional Payload.
_Avoid_: Plot point, scene

**Beat Map**:
The changes, value shifts, and emotional payloads identified in a Reference.
_Avoid_: Story, plot

**Series Recommendation**:
A Creative Brief recommendation for whether a Reference should become a single image, triptych, or image series.
_Avoid_: Generating a series by default without artist approval

**Series Plan**:
An approved plan for multiple related images that preserve a larger Beat Map or sequence of Tension Points.
_Avoid_: Prompt variants

**Triptych**:
A three-image Series Plan or Series Recommendation for a clear three-part transformation.
_Avoid_: Generic three variants

**Image Series**:
A multi-image Series Plan or Series Recommendation for extended sequence, motif evolution, or world exploration.
_Avoid_: Prompt variants

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

**Single-Generation Variant Triptych**:
One horizontal image made of three equal square panels that compares Minimal/minimalist, Faithful/Balanced, and Amplified/Maximal intensity directions in a single generation after Symbology Direction and Style Direction are selected.
_Avoid_: Treating the comparison triptych as a Series Plan

**Layout Plan**:
The Provider-Neutral Prompt Plan field that records final output arrangement: single image, three-panel variant triptych, series calibration image, or series image. Pre-locking exploration boards are recorded in visual boards, not Layout Plan.
_Avoid_: Hiding generation layout inside prompt prose only

**Visual Boards**:
The Provider-Neutral Prompt Plan field that records pre-locking Symbology Boards and Style Exploration Boards, including options, traceability, risks, selection status, and whether provider-backed generation was approved.
_Avoid_: Stuffing exploration-board options into Layout Plan prose

**Image Role**:
The function of one image inside a Series Plan, such as opening image, threshold image, rupture image, return image, or resolution image.
_Avoid_: Variant

**Tension Point**:
A meaningful contrast or unresolved pressure that carries emotion but does not imply before/after change.
_Avoid_: Beat when no change is present

**Transformation Plan**:
The plan for preserving meaning while changing medium or form.
_Avoid_: Prompt plan

**Meaning-Preserving Transformation**:
Changing medium or form while preserving Artist Meaning, selected Formal Analysis, Emotional Structure, and relevant Beats or Tension Points.
_Avoid_: Format conversion, style transfer

**Prompt Plan**:
The generation-facing prompts and constraints for a specific model or medium.
_Avoid_: Creative Brief, Transformation Plan

**Provider-Neutral Prompt Plan**:
A Prompt Plan expressed in Artist OS concepts before provider-specific translation.
_Avoid_: Provider prompt

**Prompt Variant Plan**:
One provider-neutral prompt direction inside a Provider-Neutral Prompt Plan.
_Avoid_: Generated Work, Variant before provider-backed generation

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
Local uncommitted storage for real artist References, Creative Briefs, gate decisions, Prompt Plans, Generated Works, image files, sidecar metadata, and Output Records.
_Avoid_: Example Corpus

**Artist OS Library Database**:
The SQLite query index at `workspace-library/artist-os/artist-os.sqlite`, refreshed from project manifests, event logs, and asset sidecars.
_Avoid_: Source of truth for binary media

**Missing Project**:
A project row in the Artist OS Library Database whose project folder or `project.json` was not found during the latest sync.
_Avoid_: Archived Project

**Project Manifest**:
The `project.json` record that lets an agent reload one Artist OS project across sessions.
_Avoid_: Chat memory

**Asset Metadata**:
The same-basename `.json` sidecar stored next to an image or export in the Workspace Library.
_Avoid_: Loose notes

**First Slice**:
The first complete Dry Run path through Artist OS: Text Reference to Image Prompt Plan.
_Avoid_: MVP

**Generated Work**:
Any media object created by Artist OS from a Creative Brief.
_Avoid_: Asset, output

**Variant**:
One generated option within a generation set.
_Avoid_: Generated Work when referring to a specific option among alternatives

**Accepted Work**:
A Generated Work the artist approves as matching the intended meaning.
_Avoid_: Final asset

**Acceptance Review**:
The artist's decision about whether a Generated Work preserves the Creative Brief well enough to become an Accepted Work.
_Avoid_: Critique, quality score

**Output Record**:
The metadata and provenance record for a Generated Work.
_Avoid_: Generated Work, Source Record

## Relationships

- **Artist Generation** produces **Artist OS**.
- **Artist OS** contains one or more **Skills**.
- A **Plugin** packages **Artist OS** for a specific agent host.
- A **Reference** has one **Source Record**.
- A **Reference** has **Artist Meaning** supplied by the artist.
- A **Meaning Interview** captures **Artist Meaning**.
- A **Reference** can produce one or more **Creative Briefs**.
- A **Creative Brief** can be represented as a **Creative Brief Document** and a **Creative Brief Record**.
- A **Creative Brief Document** requires **Brief Approval** before producing the **Creative Brief Record**.
- **Rough Brief Approval** permits producing a **Creative Brief Record** while preserving uncertainty notes.
- **Interpretive Confidence** and **Open Questions** guide review, but final Prompt Plans should not preserve unresolved ambiguity.
- **Art Critic Review** resolves **Open Questions** before final Prompt Plan generation.
- **Art Critic Review** may deepen and emphasize existing findings when the artist gives no additional feedback, but it cannot override **Artist Meaning**.
- The First Slice runs **Art Critic Review** after the draft **Creative Brief Document** and before **Brief Approval**.
- **Art Critic Review** is mandatory in the First Slice.
- **Art Critic Review** applies **Critical Heuristics** in this order: preserve **Artist Meaning**, stay anchored to **Reference** evidence, deepen salient **Core Tension Pairs**, strengthen **Active Visual Tensions**, increase **Poetic Density**, use medium-specific translation principles, then apply art-critical rules such as avoiding literalism, preserving contradiction, making form carry meaning, and preferring layered specificity over generic mood.
- A **Creative Brief** contains **Artist Meaning**, **Formal Analysis**, **Style Direction**, **Visual Dynamics**, **Emotional Structure**, a **Beat Map**, **Series Recommendation**, and a **Transformation Plan**.
- **Style Direction** defines the artistic language of the generated work and must serve **Artist Meaning**.
- **Style Direction** is chosen after the first pass of **Artist Meaning**, **Emotional Structure**, **Beat Map**, and **Symbology Direction**, and before **Art Critic Review**.
- **Style Direction** can be hybrid, but it must have one **Primary Style** and bounded **Style Modifiers**.
- **Style Priority** makes **Style Direction** the last priority after **Artist Meaning**, **Emotional Structure**, **Beat Map**, and **Visual Dynamics**.
- A **Style/Visual Conflict** must be surfaced to the artist instead of silently letting style override **Visual Dynamics**.
- A **Style/Visual Conflict** can produce **Style Adaptation**, where the chosen style is modified to preserve the **Target Visual Engine**.
- **Style Conflict Fields** preserve **Style/Visual Conflicts** and proposed **Style Adaptations** in the **Creative Brief Record**.
- **Art Critic Review** may propose a default **Style Adaptation** and only ask for explicit approval when it materially changes the named style.
- **Style Interview** first asks whether the artist has a specific visual vision or wants to explore what art style to use when the artist has not named a specific style.
- **Symbology Gate** comes before **Style Gate** by default because symbolic representation is closer to **Artist Meaning** than art style.
- **Symbology Board** compares six concise symbolic options, asks for artist selection, and asks whether the work should become a single image, emotional arc, or multi-image presentation before style is locked.
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
- In a triptych or image series, adjacent image roles should usually differ on at least two **Series Amplitude Plan** dimensions unless visual sameness is intentional and traced to the **Emotional Arc**.
- In text-to-image work, **Visual Dynamics** describes the **Target Visual Engine**, not literal visual properties of the text.
- Every **Target Visual Engine** choice must trace back to **Artist Meaning**, **Reference** evidence, **Emotional Structure**, **Beat Map**, or **Critical Heuristics**.
- **Monumental / Intimate** is a **Conditional Visual Tension Pair** for scale, embodiment, installation, performance, and immersive work.
- **Emotional Structure** contains **Core Tension Pairs**, **Emotional Qualities**, an **Emotional Arc**, and **Emotional Payloads**.
- **Poetic Density** increases when a single element carries multiple meanings without collapsing them into one message.
- **Poetic Density Notes** capture **Poetic Density** without reducing it to a numeric score.
- **Core Tension Pairs** exist to support creative translation across media.
- A **Tension Pair** is stored as a **Tension Pair Record** in a **Creative Brief Record**.
- Every **Creative Brief Record** includes all eight **Core Tension Pairs**, each with **Tension Pair Salience**.
- A **Tension Pair Record** can describe either a **Core Tension Pair** or an **Active Visual Tension**.
- A **Beat Map** contains one or more **Beats** or **Tension Points**.
- A **Beat** carries one **Emotional Payload**.
- A **Tension Point** carries one **Emotional Payload** without requiring before/after change.
- A **Series Recommendation** is required when a **Beat Map** has more than one meaningful **Beat** or **Tension Point**.
- A **Series Recommendation** can still choose single image when compression preserves the work better than sequence.
- A **Triptych** fits a clear three-part emotional structure such as before/threshold/after, invitation/rupture/consequence, or concealment/revelation/aftermath.
- An **Image Series** fits extended sequence, motif evolution, or world exploration.
- A **Series Plan** requires artist approval before Artist OS produces multiple image Prompt Plans.
- An approved **Series Plan** starts with one **Series Calibration Image** before producing the rest of the series.
- The **Series Calibration Image** should use the **Calibration Image Role**, not automatically the first sequential Beat.
- The **Series Calibration Image** uses three calibration **Prompt Variant Plans** to lock visual language.
- After calibration approval, remaining series images get one prompt per **Image Role** by default.
- **Calibration Choice** updates the **Creative Brief Record** or **Series Plan** with accepted style traits, rejected style traits, locked visual rules, and notes for remaining images.
- **Calibration Choice** can update visual language, **Style Direction**, **Visual Dynamics** translation notes, locked visual rules, and series continuity rules.
- **Calibration Choice** cannot update **Artist Meaning**, **Core Tension Pairs**, or **Beat Map** unless the artist explicitly says the calibration revealed a better meaning.
- A **Symbology Board** gives the artist human input before style and prompt locking by comparing six symbolic or compositional branches with concise option labels.
- A **Prompt Variant Plan** explores one approved image direction; a **Series Plan** creates multiple related images with distinct **Image Roles**.
- In the single-image First Slice, three **Prompt Variant Plans** should preserve the approved **Symbology Direction** and **Style Direction**, then vary minimalist-to-maximalist intensity.
- **Prompt Variant Plan** labels stay Faithful, Amplified, and Minimal even when using **Variant Test Axis Labels**.
- A **Series Plan** may include **Style Progression** when the Reference warrants a changing visual language across Beats.
- The First Slice may include **Style Progression** inside **Series Recommendation**, but it becomes executable only after **Series Plan** approval.
- **Series Calibration Fields** live in **Series Recommendation** before the full **Calibration Choice** workflow exists.
- A **Transformation Plan** defines a **Meaning-Preserving Transformation**.
- A **Meaning-Preserving Transformation** can produce one or more **Provider-Neutral Prompt Plans**.
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
- The **Artist OS Library Database** indexes the **Workspace Library** so agents can find old projects, prompts, image paths, and resume points.
- A **Missing Project** can be searched as historical context but cannot be resumed until its files are restored.
- Each project in the **Workspace Library** has a **Project Manifest** and image files use **Asset Metadata** sidecars.
- The **First Slice** transforms a text **Reference** into an image **Prompt Plan** through a **Dry Run**.
- A **Prompt Plan** can produce one or more **Variants**.
- A **Variant** is a **Generated Work**.
- An **Acceptance Review** approves, rejects, or requests revisions to a **Generated Work**.
- An **Accepted Work** is a **Generated Work** approved through **Acceptance Review**.
- A **Generated Work** has one **Output Record**.

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
> **Domain expert:** "After the first pass of **Artist Meaning**, **Emotional Structure**, and **Beat Map**, but before **Art Critic Review**."
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
> **Dev:** "When is it a triptych instead of a larger image series?"
> **Domain expert:** "Use **Triptych** for clear three-part transformation. Use **Image Series** for extended sequence, motif evolution, or world exploration."
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
> **Domain expert:** "No. **Acceptance Review** decides whether the work preserves the **Creative Brief**, not whether it is merely beautiful."

## Flagged ambiguities

- "artist repository", "artist operating system", "artist OS", "plugin", and "skill collection" were used interchangeably. Resolved: **Artist Generation** is the repository/project, **Artist OS** is the product, **Skill** is a workflow, and **Plugin** is the later packaged form.
- "source", "source object", "reference", "creative input", and "input" were used for the same user-provided material. Resolved: the artist-facing term is **Reference**; the stored metadata is a **Source Record**.
- "emotional brief", "creative brief", "formal analysis", "beat map", "transformation plan", and "prompt plan" were overlapping. Resolved: **Creative Brief** is the umbrella artifact; the others are named components or downstream generation-facing plans. **Emotional Brief** is retired; use **Emotional Structure** for the emotional section.
- "asset", "generated asset", "output", "artifact", and "digital asset" were ambiguous. Resolved: use **Generated Work** for created media, **Variant** for one generated option, **Accepted Work** for artist-approved media, and **Output Record** for metadata.
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
- **Art Critic Review** is the GStack-style reviewer stage for Artist OS. It makes the Creative Brief more robust, layered, and decisive before prompt planning.
- In the First Slice, **Art Critic Review** is mandatory and runs before **Brief Approval**.
- **Critical Heuristics** are the explicit best-practice rules used by **Art Critic Review** when artist feedback leaves gaps.
- **Visual Dynamics** is a second interpretive layer beside **Emotional Structure**. The First Slice uses a library of 14 **Core Visual Tension Pairs** but records only **Active Visual Tensions**.
- **Style Direction** is a separate layer from **Emotional Structure** and **Visual Dynamics**.
- **Style Direction** is selected after the first meaning/emotional/beat/symbology pass and before **Art Critic Review**.
- Hybrid style is allowed only as one **Primary Style** plus bounded **Style Modifiers**.
- **Style Direction** is the last priority. It must not override **Artist Meaning**, **Emotional Structure**, **Beat Map**, or **Visual Dynamics**.
- **Style/Visual Conflicts** should be shown to the artist and can become **Style Adaptations**.
- **Art Critic Review** may propose default **Style Adaptations** and only ask for explicit approval when the named style materially changes.
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
- If a Reference has multiple significant Beats, Artist OS should include a **Series Recommendation** for single image, triptych, or image series. Do not create multiple image prompt plans until the artist approves a **Series Plan**.
- Multi-Beat References do not automatically become series. The recommendation can be single image when compression is more powerful.
- A **Series Plan** can use **Style Progression** when the Beat Map supports a meaningful shift in visual language across images.
- **Style Progression** can be recommended in the First Slice, but not executed until **Series Plan** approval.
- An approved **Series Plan** must produce one **Series Calibration Image** first, then use artist feedback to lock the series direction before producing remaining image prompts or images.
- The **Series Calibration Image** should use the most representative **Calibration Image Role**, often the threshold or central image.
- **Series Calibration Image** uses three prompt variants. Remaining approved series images use one prompt per **Image Role** by default.
- **Calibration Choice** is durable project context for the remaining series, not a temporary preference.
- **Calibration Choice** does not rewrite **Artist Meaning**, **Core Tension Pairs**, or **Beat Map** without explicit artist direction.
- Add minimal **Series Calibration Fields** to the Creative Brief Record now; defer full **Calibration Choice** schema until image review exists.
- Add compact **Style Conflict Fields** to the Creative Brief Record now.
- Three single-image **Prompt Variant Plans** may test unresolved **Variant Test Axes** instead of only varying intensity.
- Before locking those three Prompt Variant Plans, use the **Minimalist-to-Maximalist Gate** when intensity, density, or complexity could materially change the image.
- Keep **Prompt Variant Plan** labels stable. Use **Variant Test Axis Labels** to explain what each variant tests.
- Each **Prompt Variant Plan** must name concrete **Variant Differentiators** so the three prompts produce meaningfully different visual options.
- Use a **Single-Generation Variant Triptych** when the artist wants Minimal, Faithful/Balanced, and Amplified/Maximal intensity directions compared in one generated image.
- Store image arrangement decisions in the Prompt Plan's **Layout Plan**.
- "examples" and real user work needed separate storage. Resolved: **Example Corpus** is committed and safe to share; **Workspace Library** is local and uncommitted, with an **Artist OS Library Database**, a **Project Manifest** per project, and **Asset Metadata** sidecars for images and exports.
- Provider setup risked locking the domain model to one API. Resolved: Artist OS keeps a provider-neutral core and uses **Provider Adapters** for specific media providers.
- "accepted" needed a boundary. Resolved: a **Generated Work** becomes an **Accepted Work** only through **Acceptance Review**.
