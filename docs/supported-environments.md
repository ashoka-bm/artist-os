# Supported environments

Artist OS 1.0 supports the self-contained Codex bundle on the environment
certified below.

| Component | Supported and certified |
|---|---|
| Host | Codex CLI/Desktop using Codex skill discovery |
| Codex CLI | `0.144.1` |
| Operating system | macOS `26.5.2`, Apple silicon (`arm64`) |
| Python | CPython `3.14.3`; repository CI also exercises `3.12` and `3.13` |
| Bash | GNU Bash `3.2.57` |
| Git | Apple Git `2.50.1` |
| Install modes | Materialized-bundle copy and symlink modes |

The runtime uses only the Python standard library. Newer patch versions are
expected to work, but the table records the combinations actually exercised
for the 1.0 release.

Ubuntu remains CI-covered for the Python test and schema-validation suites, but
the complete Codex Desktop and installed-bundle release smoke was certified on
macOS. Claude Code, Cursor, Windows, and provider-backed generation are not
supported by Artist OS 1.0.

See `SUPPORT.md` for reporting guidance.
