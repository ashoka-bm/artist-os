# Package Formats

Package Formats describe how a finished release arranges its accepted assets into slots; they are the Package Compilation completeness checklist, not story or output-shape grammar.

Read this index first, then open only the entry that matches the release.

| Entry id | File | Use when |
| --- | --- | --- |
| `album` | [album.md](album.md) | The finished release is an album: a repeating set of audio tracks gathered under one title and cover. |
| `article_with_photos` | [article-with-photos.md](article-with-photos.md) | The finished release is a written article carrying captioned inline photos. |
| `video_with_soundtrack` | [video-with-soundtrack.md](video-with-soundtrack.md) | The finished release is a single video paired with a soundtrack, optionally with a poster image. |

## Chooser Guide

Choose by the finished bundle's primary and supporting assets, mirroring Medium Roles: name the one asset the release is fundamentally about, then the supporting assets arranged around it.

- Use `album` when the release is fundamentally a set of audio tracks: the repeating `album_audio_track` is primary, and album title, album thumbnail, per-track cover image, and titles are supporting.
- Use `article_with_photos` when the release is fundamentally written prose: the `article_text` is primary, and captioned `inline_photo` assets are supporting.
- Use `video_with_soundtrack` when the release is fundamentally a single video: the `video` is primary, the `soundtrack_audio` is supporting, and the poster image is an optional supporting asset.

A Package Format only describes the slots a finished bundle should fill. It does not plan the prompts that produce those assets, decide how many beats or sections a work has, or invent new deliverables.

## Do Not Use Package Format For

- choosing prompts or plans — that is the Cross-Medium Plan's job during planning,
- inventing assets the artist never planned or generated,
- replacing Output Records as the source of truth for an accepted asset.
