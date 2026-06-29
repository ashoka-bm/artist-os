# Album

**Entry id**: `album`

**Scope**: A finished release that gathers a repeating set of audio tracks under one album identity (title and thumbnail), where each track carries its own cover image and titles.

**Use when**: The release is fundamentally a set of audio tracks meant to be experienced together as one named album.

**Slots**:

- Primary slot: `album_audio_track` — repeats once per track; the audio is what the album is fundamentally made of.
- Supporting slots: `album_title`, `album_thumbnail` (album-level, one each); per-track `song_cover_image`, `song_title`, and `image_title` (one of each per track).

**Required vs optional assets**:

- Required: one `album_title`, one `album_thumbnail`, and for every track one `album_audio_track`, one `song_cover_image`, one `song_title`, and one `image_title`.
- Optional: none in the first set; additional artist-facing notes are not part of the format's completeness contract.

**Per-asset metadata**:

- `album_title`, `song_title`, `image_title`: a title string carried in `slot_metadata.title`.
- `album_thumbnail`, `song_cover_image`: the accepted image Output Record; no caption is required.
- `album_audio_track`: the accepted audio Output Record; the track's position is given by Arrangement / order below.

**Arrangement / order**:

- Album-level slots (`album_title`, `album_thumbnail`) come first.
- Tracks follow in playback order; each track groups its `album_audio_track`, `song_cover_image`, `song_title`, and `image_title` together.

**Completeness rules**:

- Every planned asset has an accepted Output Record of the right type before the slot is `filled`.
- The album has exactly one accepted `album_title` and one accepted `album_thumbnail`.
- Every track has an accepted `album_audio_track`, `song_cover_image`, `song_title`, and `image_title`.
- A required gap blocks completion unless the artist explicitly waives it and the waiver is recorded.
