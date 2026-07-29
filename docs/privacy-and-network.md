# Privacy and network boundary

Artist OS 1.0 is local-first, but using it through Codex is not the same as
keeping every prompt entirely on-device.

## What stays local

- The installed Artist OS bundle.
- The visible Artist Library under
  `<wondermint_root>/Wondermint/Artist Library/`.
- Internal project state, provenance, events, and SQLite index under
  `<wondermint_root>/.wondermint/artist-os/`.
- Imported artifacts, unless the artist separately uploads or shares them.

Files remain the source of truth. SQLite is a rebuildable local query index.
Artist OS does not upload the Workspace Library, publish outputs, or copy an
imported artifact merely because its path is recorded.

## What Codex may process

Codex and its configured model process the messages and file content supplied
to the task. That processing follows the privacy, retention, and account
controls of the Codex/OpenAI environment in which Artist OS is used. Keep
private References out of a task unless that environment is appropriate for
them.

## Optional network activity

Artist OS may use web research when the artist requests it or when current
facts are necessary and the artist accepts that research step. Search queries
and opened pages leave the local machine.

Artist OS 1.0 ships no media-provider adapter, API-key setup, publishing
integration, analytics ingestion service, or background synchronization. A
Generation Approval records permission for a future or external action; it
does not cause a provider call.

## Secrets and cloud folders

Do not place API keys, credentials, `.env` files, or paid-provider secrets in a
project or release bundle. A Wondermint Root may be placed in a cloud-synced
folder, but concurrent sync can create file conflicts; Artist OS does not
provide conflict-free cloud backup.
