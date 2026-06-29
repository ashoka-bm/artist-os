# Video With Soundtrack

**Entry id**: `video_with_soundtrack`

**Scope**: A finished release that is a single video paired with a soundtrack, optionally accompanied by a poster image.

**Use when**: The release is fundamentally a single video, with audio arranged as its soundtrack and an optional poster image presenting it.

**Slots**:

- Primary slot: `video` — the single video; one per release.
- Supporting slots: `soundtrack_audio` — the audio paired with the video; `poster_image` — an optional still that presents the video.

**Required vs optional assets**:

- Required: one `video` and one `soundtrack_audio`.
- Optional: one `poster_image`.

**Per-asset metadata**:

- `video`: the accepted video Output Record.
- `soundtrack_audio`: the accepted audio Output Record.
- `poster_image`: the accepted image Output Record when present; a title may be carried in `slot_metadata.title`.

**Arrangement / order**:

- The `video` is the spine.
- The `soundtrack_audio` is paired with the video as its soundtrack.
- The `poster_image`, when present, presents the release.

**Completeness rules**:

- Every planned asset has an accepted Output Record of the right type before the slot is `filled`.
- The release has exactly one accepted `video` and one accepted `soundtrack_audio`.
- The `poster_image` is optional; its absence does not block completion.
- A required gap blocks completion unless the artist explicitly waives it and the waiver is recorded.
