# News Article

**Entry id**: `news_article`

**Scope**: A timely factual article gives the reader the most important verified information first, then adds context, evidence, and consequences.

**Structure grounding**: News lede, inverted pyramid, nut/context, evidence, and update convention.

**Grounding status**: `provisional`

**Grounding tier**: `craft_authority`

**Use when**: The piece must report what happened, why it matters now, who is affected, and what is known or still developing.

**Audience promise**: The reader will quickly understand the essential facts and leave with an accurate sense of significance, uncertainty, and next developments.

**Audience Hook logic**: Lead with the clearest news value: consequence, change, conflict, proximity, novelty, scale, or public stakes. The hook should not outpace what is verified.

**Expected parts**:

| Part | Function | Default policy |
| --- | --- | --- |
| Lede | States the essential new fact or development. | Required |
| Nut / why it matters | Explains significance, stakes, or affected parties. | Required |
| Key facts | Provides the most important verified details. | Required |
| Source / evidence support | Attributes claims and clarifies what is known. | Required |
| Context | Gives background needed to understand the development. | Required |
| Response / consequence | Shows reactions, impact, next steps, or unresolved questions. | Mergeable |
| Close / update path | Ends with current status, next known milestone, or open uncertainty. | Required |

**Turn or payoff behavior**: The turn usually comes through context or consequence: the event is not just what happened, but what changes, remains uncertain, or now requires attention.

**Pacing norms**:

- Put the most important verified information first.
- Avoid delaying the news behind scene-setting.
- Move from fact to context to consequence.
- Keep uncertainty visible instead of smoothing it into false closure.

**Required decisions**:

- What is the most important verified development?
- What makes it newsworthy now?
- What facts require attribution or qualification?
- What context is necessary but not dominant?
- What remains unknown or developing?

**Common failure modes**:

- The lede buries the actual news.
- The piece sounds like analysis before establishing facts.
- Source claims are presented as settled truth.
- Context overwhelms the current development.
- The close implies certainty the reporting does not support.

**Adaptation questions**:

- What does the reader need to know in the first sentence or paragraph?
- What is the public consequence or reader relevance?
- Which facts are confirmed, disputed, or still emerging?
- What background changes the meaning of the event?
- What should the reader watch next?

**Recommended Stewardship Views**:

- `fact_priority`
- `source_attribution`
- `open_threads`
