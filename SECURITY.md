# Security Policy

## Supported versions

Artist OS supports the latest `1.0.x` release. Older development milestones
and untagged source snapshots do not receive security fixes.

## Reporting a vulnerability

Use GitHub's private security-advisory flow for this repository:

`https://github.com/ashoka-bm/artist-os/security/advisories/new`

Please include the affected version, operating system, reproduction steps,
impact, and any suggested mitigation. Do not include private artist material,
API keys, credentials, or paid-provider data in the report.

Please do not open a public issue for an unpatched vulnerability. A public
advisory can be coordinated after a fix or mitigation is available.

## Security boundary

Artist OS 1.0 is a local, dry-run planning system. It does not ship provider
adapters, accept API keys, or make provider-generation calls. User project
files remain outside the installed bundle in the selected Wondermint Root.
