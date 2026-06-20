from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


# Single-source-of-truth (SSoT) drift guard for the project VERSION.
#
# The version string has exactly one canonical home: the `VERSION` file at the
# repo root (the install script reads it at runtime). CHANGELOG.md is NOT a
# second copy of the version -- its release headers are the changelog's own
# structure -- but the TOP released header and the VERSION file describe the
# same release and so must agree. This test makes that agreement executable,
# the same discipline the phase-order drift test applies to the phase sequence.
#
# Failure modes this catches:
#   * VERSION bumped without a matching CHANGELOG release header (or vice versa),
#   * a malformed VERSION string that the install script would surface verbatim,
#   * the `## [Unreleased]` staging section silently removed.


VERSION = "VERSION"
CHANGELOG = "CHANGELOG.md"

# Plain 3-component semver (MAJOR.MINOR.PATCH). A future maintainer who
# introduces pre-release/build suffixes (e.g. `0.2.0-rc.1`) may loosen this to
# the full SemVer grammar -- but until then, keeping it strict catches typos.
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")

# Version headers in the changelog, e.g. `## [0.1.0] - 2026-06-20` or
# `## [Unreleased]`. We capture only the bracketed token; the date (if any) is
# not part of the agreement we are guarding.
VERSION_HEADER_RE = re.compile(r"(?m)^##\s*\[([^\]]+)\]")


class VersionChangelogConsistencyTests(unittest.TestCase):
    def _version(self) -> str:
        path = REPO_ROOT / VERSION
        self.assertTrue(path.exists(), msg="VERSION file is missing at the repo root.")
        return path.read_text(encoding="utf-8").strip()

    def _changelog(self) -> str:
        path = REPO_ROOT / CHANGELOG
        self.assertTrue(path.exists(), msg="CHANGELOG.md is missing at the repo root.")
        return path.read_text(encoding="utf-8")

    def test_version_is_strict_semver(self) -> None:
        # The install script surfaces this string verbatim ("Artist OS v$version
        # ..."), so a malformed value would leak straight into user-facing output.
        version = self._version()
        self.assertRegex(
            version,
            SEMVER_RE,
            msg=(
                f"VERSION {version!r} is not strict MAJOR.MINOR.PATCH semver. "
                "If pre-release suffixes are now intended, loosen SEMVER_RE on "
                "purpose -- do not hand-edit VERSION around this guard."
            ),
        )

    def test_changelog_has_unreleased_section(self) -> None:
        # The `## [Unreleased]` staging section is where the next release's
        # entries accumulate. Losing it means new changes have nowhere to land.
        self.assertIn(
            "## [Unreleased]",
            self._changelog(),
            msg="CHANGELOG.md is missing its `## [Unreleased]` staging section.",
        )

    def test_top_released_version_matches_version_file(self) -> None:
        # Parse the bracketed version headers IN ORDER, drop the `Unreleased`
        # staging header (case-insensitive), and require the FIRST remaining
        # header -- the most recent release -- to equal the VERSION file. This is
        # the load-bearing agreement: bumping one without the other is the drift
        # we are guarding against.
        version = self._version()
        headers = VERSION_HEADER_RE.findall(self._changelog())
        released = [h for h in headers if h.strip().lower() != "unreleased"]
        self.assertTrue(
            released,
            msg="CHANGELOG.md has no released version header (only `Unreleased`?).",
        )
        top = released[0]
        self.assertEqual(
            top,
            version,
            msg=(
                f"VERSION is {version} but the top CHANGELOG release is {top} -- "
                "they must agree."
            ),
        )


if __name__ == "__main__":
    unittest.main()
