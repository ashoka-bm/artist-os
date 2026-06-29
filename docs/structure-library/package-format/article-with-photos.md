# Article With Photos

**Entry id**: `article_with_photos`

**Scope**: A finished release that is a written article carrying captioned inline photos arranged within the prose.

**Use when**: The release is fundamentally written prose, and photos appear inline to support, illustrate, or punctuate the article.

**Slots**:

- Primary slot: `article_text` — the written article; one per release.
- Supporting slots: `inline_photo` — repeats once per inline photo, each with its own caption.

**Required vs optional assets**:

- Required: one `article_text`. At least one `inline_photo` is required when the article is planned with photos; each planned inline photo is required.
- Optional: additional inline photos beyond those planned are not part of the format's completeness contract.

**Per-asset metadata**:

- `article_text`: the accepted text Output Record.
- `inline_photo`: the accepted image Output Record plus a caption carried in `slot_metadata.caption`.

**Arrangement / order**:

- The `article_text` is the spine.
- Each `inline_photo` is placed at its intended position within the prose, in reading order.

**Completeness rules**:

- Every planned asset has an accepted Output Record of the right type before the slot is `filled`.
- The article has exactly one accepted `article_text`.
- Every planned `inline_photo` has an accepted image Output Record and a caption.
- A required gap blocks completion unless the artist explicitly waives it and the waiver is recorded.
